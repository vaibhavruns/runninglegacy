import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. 2026 PREMIUM ATHLETIC MINIMALIST PAGE SETUP
st.set_page_config(
    page_title="RUNNING JOURNEY // METRIC ENGINE",
    layout="wide"
)

# Custom typography and styled container boxes (Emoji-free modern sports look)
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0e14 !important;
        color: #e2e8f0 !important;
        font-family: 'Inter', system-ui, sans-serif !important;
    }
    html, body, [data-testid="stMarkdownContainer"] p, p, label, .stSelectbox div {
        color: #94a3b8 !important;
    }
    h1, h2, h3, h4, h5, h6, strong {
        color: #ffffff !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
    }
    /* Stadium Style Ticker */
    .ticker-wrap {
        background: #000000;
        padding: 14px;
        border-radius: 4px;
        margin-bottom: 30px;
        border-left: 4px solid #ccff00;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    /* KPI Metric Containers */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 20px;
        margin-bottom: 35px;
    }
    .kpi-card {
        background: #121721;
        padding: 24px;
        border-radius: 6px;
        border: 1px solid #1e293b;
        text-align: left;
        border-bottom: 3px solid #1e293b;
    }
    .kpi-value {
        font-size: 2.4rem;
        font-weight: 900;
        color: #ffffff !important;
        line-height: 1;
        font-family: monospace;
    }
    .kpi-label {
        font-size: 0.75rem;
        color: #ccff00 !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 8px;
        font-weight: 700;
    }
    /* Modern Content Box Container Wrapper */
    .chart-container-box {
        background-color: #121721 !important;
        border: 1px solid #1e293b !important;
        border-radius: 8px !important;
        padding: 24px !important;
        margin-bottom: 25px !important;
    }
    /* Flashcard Row Systems */
    .flashcard-row {
        background: #121721;
        border: 1px solid #1e293b;
        border-radius: 6px;
        padding: 16px 24px;
        margin-bottom: 12px;
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: 15px;
        border-left: 4px solid #00f0ff;
    }
    .flashcard-left {
        display: flex;
        align-items: center;
        gap: 25px;
        min-width: 250px;
    }
    .flashcard-date-block {
        line-height: 1.2;
    }
    .flashcard-date-main {
        color: #ffffff;
        font-weight: 800;
        font-size: 1.05rem;
    }
    .flashcard-date-sub {
        color: #64748b;
        font-size: 0.75rem;
        font-family: monospace;
    }
    .flashcard-title {
        font-size: 1.1rem;
        font-weight: 800;
        color: #ffffff;
    }
    .flashcard-category {
        font-size: 0.7rem;
        color: #ccff00;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .flashcard-metrics-group {
        display: flex;
        align-items: center;
        gap: 30px;
        flex-wrap: wrap;
    }
    .flashcard-metric {
        text-align: center;
        min-width: 80px;
    }
    .flashcard-metric-val {
        font-size: 1.15rem;
        font-weight: 800;
        color: #ffffff;
        font-family: monospace;
    }
    .flashcard-metric-lbl {
        font-size: 0.65rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 2px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. CORE DATA READING ENGINE
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
        
        title_matches = [c for c in cols if 'Title' in c or 'Name' in c]
        time_matches = [c for c in cols if 'Duration' in c or 'Time' in c]
        hr_matches = [c for c in cols if 'Heart' in c or 'HR' in c or 'bpm' in c]
        tag_matches = [c for c in cols if 'Tag' in c or 'Race' in c]
        
        df['Race_Tag'] = df[tag_matches[0]] if tag_matches else None
        df['Activity_Title'] = df[title_matches[0]] if title_matches else "Training Run"
        df['Duration_Raw'] = df[time_matches[0]] if time_matches else "--:--"
        df['Heart_Rate'] = df[hr_matches[0]] if hr_matches else None
        
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
            if km >= 42.0: return "Full Marathon"
            elif km >= 21.2: return "Between Half and Full"
            elif km >= 21.0: return "Half Marathon"
            elif km > 10.5: return "Between 10K and 21K"
            elif km >= 9.8: return "10K Runs"
            else: return "Less than 10K"
            
        df['Category'] = df['Distance_KM'].apply(segment_run)
        return df
    except Exception as e:
        return None

df = load_garmin_data()

# HEADER TERMINAL
st.markdown("<h1 style='text-align: left; color: #ffffff; font-size: 2.8rem; font-weight: 900; margin-bottom:0px;'>RUNNING JOURNEY</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: left; color: #ccff00 !important; font-weight:700; letter-spacing:1px; margin-top:5px;'>ENDURANCE ARCHIVE // PERFORMANCE LOG</p>", unsafe_allow_html=True)
st.markdown("<hr style='border-color: #1e293b; margin-top: 15px; margin-bottom: 25px;'>", unsafe_allow_html=True)

if df is None:
    st.error("Missing data sheet reference linking parameters.")
else:
    # 3. GLOBAL CONTROL ROOM FILTERS
    st.markdown("### CONTROL CENTER")
    filter_col1, filter_col2 = st.columns(2)
    
    with filter_col1:
        year_list = ["ALL TIME"] + [str(y) for y in sorted(df['Year'].unique(), reverse=True)]
        selected_year = st.selectbox("ISOLATE REGISTRATION YEAR:", options=year_list)
        
    with filter_col2:
        cat_list = ["ALL CATEGORIES"] + ["Full Marathon", "Between Half and Full", "Half Marathon", "Between 10K and 21K", "10K Runs", "Less than 10K"]
        selected_cat = st.selectbox("ISOLATE DISTANCE THRESHOLD:", options=cat_list)
        
    # Isolate global dataframe parameters
    f_df = df.copy()
    if selected_year != "ALL TIME":
        f_df = f_df[f_df['Year'] == int(selected_year)]
    if selected_cat != "ALL CATEGORIES":
        f_df = f_df[f_df['Category'] == selected_cat]

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. STADIUM LED TICKER (ALL-TIME PR BENCHMARKS)
    ticker_items = []
    df_10k = df[(df['Distance_KM'] >= 9.5) & (df['Distance_KM'] <= 11.5) & (df['Pace_Decimal'].notna())]
    if not df_10k.empty:
        best_10k = df_10k.loc[df_10k['Pace_Decimal'].idxmin()]
        p_min, p_sec = int(best_10k['Pace_Decimal']), int((best_10k['Pace_Decimal'] % 1) * 60)
        ticker_items.append(f"PR 10K: {best_10k['Distance_KM']:.2f}KM @ {p_min}:{p_sec:02d}/KM")
        
    df_21k = df[(df['Distance_KM'] >= 20.5) & (df['Distance_KM'] <= 22.5) & (df['Pace_Decimal'].notna())]
    if not df_21k.empty:
        best_21k = df_21k.loc[df_21k['Pace_Decimal'].idxmin()]
        p_min, p_sec = int(best_21k['Pace_Decimal']), int((best_21k['Pace_Decimal'] % 1) * 60)
        ticker_items.append(f"PR 21K: {best_21k['Distance_KM']:.2f}KM @ {p_min}:{p_sec:02d}/KM")
        
    df_42k = df[(df['Distance_KM'] >= 41.0) & (df['Pace_Decimal'].notna())]
    if not df_42k.empty:
        best_42k = df_42k.loc[df_42k['Pace_Decimal'].idxmin()]
        p_min, p_sec = int(best_42k['Pace_Decimal']), int((best_42k['Pace_Decimal'] % 1) * 60)
        ticker_items.append(f"PR FULL MARATHON: {best_42k['Distance_KM']:.2f}KM @ {p_min}:{p_sec:02d}/KM")
        
    if ticker_items:
        spacer = " &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; // &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "
        full_ticker_text = spacer.join(ticker_items)
        st.markdown(f"""
            <div class="ticker-wrap">
                <marquee behavior="scroll" direction="left" scrollamount="6" style="color: #ccff00; font-weight: 800; font-family: monospace; font-size: 1.1rem;">
                    ALL-TIME RECORD BENCHMARKS // {full_ticker_text}
                </marquee>
            </div>
        """, unsafe_allow_html=True)

    # 5. TABBED ARCHITECTURE DEPLOYMENT
    tab_dashboard, tab_feed = st.tabs(["Overview and Analytics", "Activity Feed Log"])

    with tab_dashboard:
        # KPI Core Summary Blocks
        total_runs = len(f_df)
        total_km = f_df['Distance_KM'].sum()
        avg_run_dist = f_df['Distance_KM'].mean() if total_runs > 0 else 0
        tracked_years = f_df['Year'].nunique()
        
        st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-card">
                    <div class="kpi-value">{total_runs}</div>
                    <div class="kpi-label">// INDEXED ACTIVITIES</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">{total_km:,.1f} KM</div>
                    <div class="kpi-label">// TOTAL DISTANCE CONQUERED</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">{avg_run_dist:.2f} KM</div>
                    <div class="kpi-label">// MEAN SESSION VOLUME</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">{tracked_years}</div>
                    <div class="kpi-label">// ACTIVE VOLUME YEARS</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # ROW 1 CONTAINERS: VOLUME AND CATEGORIES
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""<div class="chart-container-box"><h3>Annual Training Volume</h3>""", unsafe_allow_html=True)
            yoy_volume = f_df.groupby('Year')['Distance_KM'].sum().reset_index()
            yoy_volume['Year'] = yoy_volume['Year'].astype(str)
            
            fig_yoy = px.bar(
                yoy_volume, x='Year', y='Distance_KM', text_auto='.1f', 
                color='Year', color_discrete_sequence=['#00f0ff', '#ccff00', '#ff4757']
            )
            fig_yoy.update_layout(template="plotly_dark")
            fig_yoy.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            fig_yoy.update_layout(yaxis_title="VOLUME (KM)", xaxis_title="")
            fig_yoy.update_layout(showlegend=False)
            st.plotly_chart(fig_yoy, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("""<div class="chart-container-box"><h3>Distribution Matrix</h3>""", unsafe_allow_html=True)
            cat_order = ["Full Marathon", "Between Half and Full", "Half Marathon", "Between 10K and 21K", "10K Runs", "Less than 10K"]
            cat_counts = f_df['Category'].value_counts().reindex(cat_order).fillna(0).reset_index()
            cat_counts.columns = ['Category', 'Runs']
            
            fig_cat = px.bar(cat_counts, x='Runs', y='Category', orientation='h', color_discrete_sequence=['#ccff00'])
            fig_cat.update_layout(template="plotly_dark")
            fig_cat.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            fig_cat.update_layout(xaxis_title="FREQUENCY", yaxis_title="")
            st.plotly_chart(fig_cat, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # ROW 2 CONTAINER: NON-MERGED INTRA-ANNUAL TIMELINE SEQUENCING
        st.markdown("""<div class="chart-container-box"><h3>Intra-Annual Splits Timeline</h3>""", unsafe_allow_html=True)
        
        if selected_year == "ALL TIME":
            # Group chronologically across all tracked months and years sequentially
            monthly_grouped = f_df.groupby(['Year', 'Month_Num', 'Month_Name'])['Distance_KM'].sum().reset_index()
            monthly_grouped = monthly_grouped.sort_values(['Year', 'Month_Num'])
            # Build continuous chronological labels: e.g., Jan '24, Feb '24
            monthly_grouped['Timeline'] = monthly_grouped['Month_Name'] + " '" + monthly_grouped['Year'].astype(str).str[-2:]
            
            fig_month = px.bar(
                monthly_grouped, x='Timeline', y='Distance_KM', text_auto='.1f',
                color='Year', color_discrete_sequence=px.colors.qualitative.Safe
            )
            fig_month.update_layout(xaxis={'type': 'category'})
        else:
            # Traditional 12-month fixed grid for a single standalone year target
            monthly_grouped = f_df.groupby(['Month_Num', 'Month_Name'])['Distance_KM'].sum().reset_index()
            all_months = pd.DataFrame({
                'Month_Num': range(1, 13),
                'Month_Name': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            })
            monthly_volume = pd.merge(all_months, monthly_grouped, on=['Month_Num', 'Month_Name'], how='left').fillna(0)
            
            fig_month = px.bar(
                monthly_volume, x='Month_Name', y='Distance_KM', 
                text_auto='.1f', color_discrete_sequence=['#00f0ff']
            )
            fig_month.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': all_months['Month_Name']})
            
        fig_month.update_layout(template="plotly_dark")
        fig_month.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        fig_month.update_layout(yaxis_title="VOLUME (KM)", xaxis_title="")
        st.plotly_chart(fig_month, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_feed:
        # FEED ARCHITECTURE LAYER
        st.markdown("### ACTIVITY FEED LOG")
        
        if f_df.empty:
            st.warning("No performance records match your active filtering configuration.")
        else:
            sorted_cards = f_df.sort_values(by='Date', ascending=False)
            display_limit = 50
            
            for idx, (_, row) in enumerate(sorted_cards.head(display_limit).iterrows()):
                date_main = row['Date'].strftime('%b %d')
                date_sub = row['Date'].strftime('%Y')
                
                p_val = row['Pace_Decimal']
                p_str = f"{int(p_val)}:{int((p_val % 1) * 60):02d} /km" if pd.notna(p_val) else "--:--"
                
                hr_val = row['Heart_Rate']
                hr_str = f"{int(hr_val)} bpm" if pd.notna(hr_val) and hr_val > 0 else "--"
                race_label = f" // {row['Race_Tag']}" if pd.notna(row['Race_Tag']) else ""
                
                st.markdown(f"""
                    <div class="flashcard-row">
                        <div class="flashcard-left">
                            <div class="flashcard-date-block">
                                <div class="flashcard-date-main">{date_main}</div>
                                <div class="flashcard-date-sub">{date_sub}</div>
                            </div>
                            <div>
                                <div class="flashcard-title">{row['Activity_Title']}{race_label}</div>
                                <div class="flashcard-category">{row['Category']}</div>
                            </div>
                        </div>
                        <div class="flashcard-metrics-group">
                            <div class="flashcard-metric">
                                <div class="flashcard-metric-val">{row['Distance_KM']:.2f} km</div>
                                <div class="flashcard-metric-lbl">Distance</div>
                            </div>
                            <div class="flashcard-metric">
                                <div class="flashcard-metric-val">{row['Duration_Raw']}</div>
                                <div class="flashcard-metric-lbl">Time</div>
                            </div>
                            <div class="flashcard-metric">
                                <div class="flashcard-metric-val">{p_str}</div>
                                <div class="flashcard-metric-lbl">Avg Pace</div>
                            </div>
                            <div class="flashcard-metric">
                                <div class="flashcard-metric-val" style="color: #ff4757;">{hr_str}</div>
                                <div class="flashcard-metric-lbl">Avg HR</div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
            if len(sorted_cards) > display_limit:
                st.markdown(f"<p style='text-align:center; color:#64748b;'>Truncated loop breakdown at {display_limit} items.</p>", unsafe_allow_html=True)
