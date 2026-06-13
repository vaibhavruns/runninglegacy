import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# 1. PREMIUM PAGE SETUP
st.set_page_config(page_title="Running Journey", page_icon="⚡", layout="wide")

# Inject bulletproof CSS to guarantee 100% readability (Fixes the black-on-black text bug)
st.markdown("""
    <style>
    /* Force overall app dark background */
    .stApp {
        background-color: #0d1117 !important;
    }
    /* Force ALL text, markdown, paragraphs, and labels to be light and readable */
    html, body, [data-testid="stMarkdownContainer"] p, p, label, .stSelectbox, div {
        color: #c9d1d9 !important;
    }
    /* Bold/Header overrides */
    h1, h2, h3, h4, h5, h6, strong, .metric-val {
        color: #ffffff !important;
    }
    /* Premium KPI Card Design */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin-bottom: 30px;
    }
    .kpi-card {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #30363d;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        color: #10b981 !important;
        font-family: monospace;
    }
    .kpi-label {
        font-size: 0.85rem;
        color: #8b949e !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 5px;
    }
    /* Styling for the tables to prevent hidden text */
    .dataframe {
        color: #c9d1d9 !important;
        background-color: #161b22 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. ROBUST DATA CLEANING & LOADING ENGINE
@st.cache_data
def load_garmin_data():
    if not os.path.exists("activities.csv"):
        return None
    try:
        df = pd.read_csv("activities.csv")
        
        # Dynamically identify columns to avoid name mismatch errors
        date_col = [c for c in df.columns if 'Date' in c or 'Time' in c or 'Start' in c][0]
        dist_col = [c for c in df.columns if 'Distance' in c][0]
        pace_col = [c for c in df.columns if 'Pace' in c or 'Speed' in c][0]
        hr_col = [c for c in df.columns if 'Heart Rate' in c or 'HR' in c]
        
        # Convert Types safely
        df['Date'] = pd.to_datetime(df[date_col])
        df['Year'] = df['Date'].dt.year
        df['Distance_KM'] = pd.to_numeric(df[dist_col], errors='coerce').fillna(0)
        
        # Parse Paces safely into decimal minutes for clean graphing
        def parse_pace(x):
            try:
                if ':' in str(x):
                    parts = str(x).split(':')
                    return float(parts[0]) + (float(parts[1]) / 60.0)
                return float(x)
            except:
                return None
                
        df['Pace_Decimal'] = df[pace_col].apply(parse_pace)
        
        if hr_col:
            df['Heart_Rate'] = pd.to_numeric(df[hr_col[0]], errors='coerce')
        else:
            df['Heart_Rate'] = None
            
        # Categorization Engine
        def segment_run(km):
            if km >= 42.0: return "Full Marathon 🏆"
            elif km >= 21.2: return "Between Half & Full 📈"
            elif km >= 21.0: return "Half Marathon 🥈"
            elif km >= 10.0: return "10K Runs ⚡"
            else: return "Less than 10K 🌱"
            
        df['Category'] = df['Distance_KM'].apply(segment_run)
        return df
    except Exception as e:
        return None

df = load_garmin_data()

# ==========================================
# HEADER SECTION
# ==========================================
st.markdown("<h1 style='text-align: center; font-weight: 800; margin-bottom: 5px;'>🏃‍♂️ Running Journey</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8b949e !important;'>An interactive lifelong archive of discipline, volume, and endurance legacy.</p>", unsafe_allow_html=True)
st.markdown("<hr style='border-color: #30363d;'>", unsafe_allow_html=True)

if df is None:
    st.error("Error loading 'activities.csv'. Please check your repository configurations.")
else:
    # 3. HIGH-LEVEL CORE KPI METRICS
    total_runs = len(df)
    total_km = df['Distance_KM'].sum()
    avg_run_dist = df['Distance_KM'].mean()
    
    st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-card">
                <div class="kpi-value">{total_runs}</div>
                <div class="kpi-label">Lifetime Runs</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">{total_km:,.1f} KM</div>
                <div class="kpi-label">Total Volume Conquered</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">{avg_run_dist:.2f} KM</div>
                <div class="kpi-label">Avg Distance Per Run</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">{df['Year'].nunique()}</div>
                <div class="kpi-label">Years Tracked</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 4. ROW 1: YEAR-ON-YEAR VOLUME & CATEGORIES
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Year-on-Year Training Volume")
        yoy_volume = df.groupby('Year')['Distance_KM'].sum().reset_index()
        fig_yoy = px.bar(
            yoy_volume, x='Year', y='Distance_KM',
            text_auto='.1f', color='Distance_KM',
            color_continuous_scale='Viridis'
        )
        fig_yoy.update_layout(
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", 
            plot_bgcolor="rgba(0,0,0,0)", yaxis_title="Total Distance (KM)"
        )
        st.plotly_chart(fig_yoy, use_container_width=True)

    with col2:
        st.markdown("### 🗂️ Run Count by Category")
        cat_order = ["Full Marathon 🏆", "Between Half & Full 📈", "Half Marathon 🥈", "10K Runs ⚡", "Less than 10K 🌱"]
        cat_counts = df['Category'].value_counts().reindex(cat_order).fillna(0).reset_index()
        cat_counts.columns = ['Category', 'Runs']
        
        fig_cat = px.bar(
            cat_counts, x='Runs', y='Category', orientation='h',
            color='Runs', color_continuous_scale='Cividis'
        )
        fig_cat.update_layout(
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", 
            plot_bgcolor="rgba(0,0,0,0)", xaxis_title="Number of Activities", yaxis_title=""
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    st.markdown("<hr style='border-color: #30363d;'>", unsafe_allow_html=True)

    # 5. ROW 2: PACE AND HEART RATE DYNAMICS
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("### 📈 Pacing Profile over Time")
        # Filters outliers or empty paces
        pace_df = df[df['Pace_Decimal'].notna() & (df['Pace_Decimal'] < 12) & (df['Pace_Decimal'] > 3)].sort_values('Date')
        
        fig_pace = px.scatter(
            pace_df, x='Date', y='Pace_Decimal', color='Distance_KM',
            hover_data=['Distance_KM'], color_continuous_scale='Bluered',
            trendline="lowess", trendline_color_override="#10b981"
        )
        fig_pace.update_layout(
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", 
            plot_bgcolor="rgba(0,0,0,0)", yaxis_title="Pace (Min/KM)",
            yaxis=dict(autorange="reversed") # Faster paces are smaller numbers
        )
        st.plotly_chart(fig_pace, use_container_width=True)

    with col4:
        st.markdown("### ❤️ Cardiovascular Fitness Trend")
        if df['Heart_Rate'].notna().sum() > 0:
            hr_df = df[df['Heart_Rate'].notna() & (df['Heart_Rate'] > 90)].sort_values('Date')
            fig_hr = px.line(
                hr_df, x='Date', y='Heart_Rate', 
                color_discrete_sequence=["#ef4444"]
            )
            fig_hr.update_layout(
                template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", 
                plot_bgcolor="rgba(0,0,0,0)", yaxis_title="Avg Heart Rate (BPM)"
            )
            st.plotly_chart(fig_hr, use_container_width=True)
        else:
            st.info("Heart Rate data columns not detected or populated in the uploaded log format.")

    # 6. FASTEST EFFORTS LEADERS
    st.markdown("<hr style='border-color: #30363d;'>", unsafe_allow_html=True)
    st.markdown("### 🏅 All-Time Fastest Efforts Leaderboard")
    
    if df['Pace_Decimal'].notna().sum() > 0:
        fastest_efforts = df[df['Pace_Decimal'].notna() & (df['Distance_KM'] > 2)].sort_values(by='Pace_Decimal', ascending=True).head(5)
        
        # Displaying clean, legible summary entries
        for idx, row in fastest_efforts.iterrows():
            st.markdown(f"🏁 **{row['Date'].strftime('%d %B %Y')}** — Run distance of **{row['Distance_KM']:.2f} KM** completed with an elite pace of **{int(row['Pace_Decimal'])}:{int((row['Pace_Decimal']%1)*60):02d} /km**.")
