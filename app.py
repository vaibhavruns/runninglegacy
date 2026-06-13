import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. PREMIUM LIGHT MODE PAGE SETUP
st.set_page_config(
    page_title="Running Journey",
    page_icon="🏃‍♂️",
    layout="wide"
)

# Inject explicit clean-light typography and structural CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff !important;
        color: #212529 !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
    }
    html, body, [data-testid="stMarkdownContainer"] p, p, label, .stSelectbox div {
        color: #222222 !important;
    }
    h1, h2, h3, h4, h5, h6, strong {
        color: #111111 !important;
        font-weight: 700 !important;
    }
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin-bottom: 30px;
    }
    .kpi-card {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e9ecef;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
    }
    .kpi-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0076d6 !important;
    }
    .kpi-label {
        font-size: 0.85rem;
        color: #6c757d !important;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-top: 5px;
    }
    .ticker-wrap {
        background: #111111;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 25px;
        overflow: hidden;
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# 2. DATA PROCESSING ENGINE
@st.cache_data
def load_garmin_data():
    if not os.path.exists("activities.csv"):
        return None
    try:
        df = pd.read_csv("activities.csv")
        
        cols = list(df.columns)
        date_col = [c for c in cols if 'Date' in c or 'Time' in c or 'Start' in c][0]
        dist_col = [c for c in cols if 'Distance' in c][0]
        pace_col = [c for c in cols if 'Pace' in c or 'Speed' in c][0]
        
        df['Date'] = pd.to_datetime(df[date_col])
        df['Year'] = df['Date'].dt.year
        df['Month_Num'] = df['Date'].dt.month
        df['Month_Name'] = df['Date'].dt.strftime('%b')
        df['Distance_KM'] = pd.to_numeric(df[dist_col], errors='coerce').fillna(0)
        
        def parse_pace(x):
            try:
                if ':' in str(x):
                    parts = str(x).split(':')
                    return float(parts[0]) + (float(parts[1]) / 60.0)
                return float(x)
            except:
                return None
                
        df['Pace_Decimal'] = df[pace_col].apply(parse_pace)
        
        def segment_run(km):
            if km >= 42.0: return "Full Marathon 🏆"
            elif km >= 21.2: return "Between Half & Full 📈"
            elif km >= 21.0: return "Half Marathon 🥈"
            elif km > 10.5: return "Between 10K and 21K ⚡"
            elif km >= 9.8: return "10K Runs 🎯"
            else: return "Less than 10K 🌱"
            
        df['Category'] = df['Distance_KM'].apply(segment_run)
        return df
    except Exception as e:
        return None

df = load_garmin_data()

# MAIN HEADER BLOCK
st.markdown("<h1 style='text-align: center; color: #111111;'>🏃‍♂️ Running Journey</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6c757d !important;'>A streamlined dashboard of your lifelong endurance achievements.</p>", unsafe_allow_html=True)

if df is None:
    st.error("Missing 'activities.csv' data file link.")
else:
    # 3. DYNAMIC TARGETED BENCHMARKS TICKER TAPE
    ticker_items = []
    
    # Extract Best 10K
    df_10k = df[(df['Distance_KM'] >= 9.5) & (df['Distance_KM'] <= 11.5) & (df['Pace_Decimal'].notna())]
    if not df_10k.empty:
        best_10k = df_10k.loc[df_10k['Pace_Decimal'].idxmin()]
        p_min = int(best_10k['Pace_Decimal'])
        p_sec = int((best_10k['Pace_Decimal'] % 1) * 60)
        r_date = best_10k['Date'].strftime('%d %b %Y')
        d_val = best_10k['Distance_KM']
        ticker_items.append(f"🎯 BEST 10K: {d_val:.2f}KM @ {p_min}:{p_sec:02d}/km ({r_date})")
        
    # Extract Best 21K Half Marathon
    df_21k = df[(df['Distance_KM'] >= 20.5) & (df['Distance_KM'] <= 22.5) & (df['Pace_Decimal'].notna())]
    if not df_21k.empty:
        best_21k = df_21k.loc[df_21k['Pace_Decimal'].idxmin()]
        p_min = int(best_21k['Pace_Decimal'])
        p_sec = int((best_21k['Pace_Decimal'] % 1) * 60)
        r_date = best_21k['Date'].strftime('%d %b %Y')
        d_val = best_21k['Distance_KM']
        ticker_items.append(f"🥈 BEST HALF MARATHON (21K): {d_val:.2f}KM @ {p_min}:{p_sec:02d}/km ({r_date})")
        
    # Extract Best Full Marathon
    df_42k = df[(df['Distance_KM'] >= 41.0) & (df['Pace_Decimal'].notna())]
    if not df_42k.empty:
        best_42k = df_42k.loc[df_42k['Pace_Decimal'].idxmin()]
        p_min = int(best_42k['Pace_Decimal'])
        p_sec = int((best_42k['Pace_Decimal'] % 1) * 60)
        r_date = best_42k['Date'].strftime('%d %b %Y')
        d_val = best_42k['Distance_KM']
        ticker_items.append(f"🏆 BEST FULL MARATHON: {d_val:.2f}KM @ {p_min}:{p_sec:02d}/km ({r_date})")
        
    if ticker_items:
        spacer = " &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ⚡ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "
        full_ticker_text = spacer.join(ticker_items)
        st.markdown(f"""
            <div class="ticker-wrap">
                <marquee behavior="scroll" direction="left" scrollamount="5" style="color: #0076d6; font-weight: 700; font-family: monospace; font-size: 1.1rem;">
                    🥇 DISTANCE MILESTONE BENCHMARKS &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ⚡ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {full_ticker_text}
                </marquee>
            </div>
        """, unsafe_allow_html=True)

    # 4. CORE METRICS DISPLAY PANEL
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
                <div class="kpi-label">Avg Distance / Run</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">{df['Year'].nunique()}</div>
                <div class="kpi-label">Years Tracked</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 5. VISUALIZATION ROW 1: YEAR-ON-YEAR & REFINED CATEGORIES
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Year-on-Year Training Volume")
        yoy_volume = df.groupby('Year')['Distance_KM'].sum().reset_index()
        yoy_volume['Year'] = yoy_volume['Year'].astype(str)
        
        colors = ['#0076d6', '#10b981', '#ff6b6b']
        fig_yoy = px.bar(
            yoy_volume,
            x='Year',
            y='Distance_KM',
            text_auto='.1f',
            color='Year',
            color_discrete_sequence=colors
        )
        fig_yoy.update_layout(template="plotly_white")
        fig_yoy.update_layout(paper_bgcolor="rgba(0,0,0,0)")
        fig_yoy.update_layout(plot_bgcolor="rgba(0,0,0,0)")
        fig_yoy.update_layout(yaxis_title="Total Distance (KM)")
        fig_yoy.update_layout(showlegend=False)
        st.plotly_chart(fig_yoy, use_container_width=True)

    with col2:
        st.markdown("### 🗂️ Run Count by Category")
        cat_order = ["Full Marathon 🏆", "Between Half & Full 📈", "Half Marathon 🥈", "Between 10K and 21K ⚡", "10K Runs 🎯", "Less than 10K 🌱"]
        cat_counts = df['Category'].value_counts().reindex(cat_order).fillna(0).reset_index()
        cat_counts.columns = ['Category', 'Runs']
        
        fig_cat = px.bar(
            cat_counts,
            x='Runs',
            y='Category',
            orientation='h',
            color_discrete_sequence=['#14b8a6']
        )
        fig_cat.update_layout(template="plotly_white")
        fig_cat.update_layout(paper_bgcolor="rgba(0,0,0,0)")
        fig_cat.update_layout(plot_bgcolor="rgba(0,0,0,0)")
        fig_cat.update_layout(xaxis_title="Number of Activities")
        fig_cat.update_layout(yaxis_title="")
        st.plotly_chart(fig_cat, use_container_width=True)

    st.markdown("<hr style='border-color: #e9ecef; margin-top: 30px; margin-bottom: 30px;'>", unsafe_allow_html=True)

    # 6. VISUALIZATION ROW 2: MONTH-ONLY TIMELINE MATRIX
    st.markdown("### 📅 Monthly Volume Breakdown")
    
    available_years = sorted(df['Year'].unique(), reverse=True)
    selected_year = st.selectbox("Choose Year to View Monthly Splits:", options=available_years)
    
    m_df = df[df['Year'] == selected_year]
    monthly_grouped = m_df.groupby(['Month_Num', 'Month_Name'])['Distance_KM'].sum().reset_index()
    
    all_months = pd.DataFrame({
        'Month_Num': range(1, 13),
        'Month_Name': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    })
    monthly_volume = pd.merge(all_months, monthly_grouped, on=['Month_Num', 'Month_Name'], how='left').fillna(0)
    
    fig_month = px.bar(
        monthly_volume,
        x='Month_Name',
        y='Distance_KM',
        text_auto='.1f',
        color_discrete_sequence=['#4f46e5']
    )
    fig_month.update_layout(template="plotly_white")
    fig_month.update_layout(paper_bgcolor="rgba(0,0,0,0)")
    fig_month.update_layout(plot_bgcolor="rgba(0,0,0,0)")
    fig_month.update_layout(yaxis_title="Distance (KM)")
    fig_month.update_layout(xaxis_title="Months")
    fig_month.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': all_months['Month_Name']})
    st.plotly_chart(fig_month, use_container_width=True)
