import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. PREMIUM ATHLETIC MINIMALIST PAGE SETUP
st.set_page_config(
    page_title="RUNNING JOURNEY // METRIC ENGINE",
    layout="wide"
)

# Custom typography, prominent navigation tabs, and styled containers
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

/* HIGH-PROMINENCE SPORTS TABS NAVIGATION */
div[data-testid="stTabs"] button {
    font-size: 1.2rem !important;
    font-weight: 800 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
    color: #64748b !important;
    padding: 14px 28px !important;
    border-bottom: 2px solid #1e293b !important;
    transition: all 0.3s ease !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #ccff00 !important;
    border-bottom: 3px solid #ccff00 !important;
    background-color: #121721 !important;
}
div[data-testid="stTabs"] button:hover {
    color: #ffffff !important;
    border-bottom-color: #00f0ff !important;
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
/* Flashcard Base Styling classes */
.flashcard-row-base {
    border: 1px solid #1e293b;
    border-radius: 6px;
    padding: 16px 24px;
    margin-bottom: 12px;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 15px;
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
    if not os.path.exists("Activities.csv"):
        return None
    try:
        df = pd.read_csv("Activities.csv")
        df['Date_Parsed'] = pd.to_datetime(df['date'])
        df['Month_Num'] = df['Date_Parsed'].dt.month
        df['Month_Short'] = df['Date_Parsed'].dt.strftime('%b')
        
        # -----------------------------------------------------------------
        # OFFICIAL COMPETITIVE PROFILE REGISTRY
        # -----------------------------------------------------------------
        RACE_REGISTRY = {
            "2023-01-15": {"name": "Tata Mumbai Marathon 5.9K", "bib": "81094", "note": ""},
            "2023-02-12": {"name": "Thane Half Marathon", "bib": "21559", "note": ""},
            "2023-11-19": {"name": "Indian Navy 10K", "bib": "12114", "note": ""},
            "2024-01-21": {"name": "Tata Mumbai Marathon 21K", "bib": "26504", "note": ""},
            "2024-04-28": {"name": "TCS World 10K Bengaluru", "bib": "3970", "note": "PR EFFORT // 59 MINS"},
            "2024-09-01": {"name": "Satara Half Hill Marathon", "bib": "25051", "note": ""},
            "2024-10-20": {"name": "Vedanta Delhi Half Marathon", "bib": "3258", "note": ""},
            "2024-12-08": {"name": "Indian Navy 21K", "bib": "23781", "note": ""},
            "2024-12-15": {"name": "Tata Steel World 25k Kolkata", "bib": "4653", "note": ""},
            "2025-09-21": {"name": "Berlin Full Marathon", "bib": "76975", "note": "PR EFFORT"},
            "2025-10-12": {"name": "Vedanta Delhi Half Marathon", "bib": "5654", "note": "PR EFFORT"},
            "2025-12-21": {"name": "Tata Steel World 25k Kolkata", "bib": "4895", "note": ""},
            "2026-01-18": {"name": "Tata Mumbai Full Marathon", "bib": "11435", "note": ""},
            "2026-04-26": {"name": "TCS World 10K Bengaluru", "bib": "32357", "note": "PROCAM SLAM COMPLETED"}
        }
        
        date_str_series = df['Date_Parsed'].dt.strftime('%Y-%m-%d')
        df['Race_Tag'] = date_str_series.apply(lambda x: RACE_REGISTRY[x]['name'] if x in RACE_REGISTRY else None)
        df['Race_Bib'] = date_str_series.apply(lambda x: RACE_REGISTRY[x]['bib'] if x in RACE_REGISTRY else None)
        df['Race_Note'] = date_str_series.apply(lambda x: RACE_REGISTRY[x]['note'] if x in RACE_REGISTRY else None)
        
        def segment_run(km):
            if km >= 42.0: return "Full Marathon"
            elif km >= 21.2: return "Between Half and Full"
            elif km >= 21.0: return "Half Marathon"
            elif km > 10.5: return "Between 10K and 21K"
            elif km >= 9.8: return "10K Runs"
            else: return "Less than 10K"
            
        df['Category_Custom'] = df['distance_km'].apply(segment_run)
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
        year_list = ["ALL TIME"] + [str(y) for y in sorted(df['year'].unique(), reverse=True)]
        selected_year = st.selectbox("YEAR:", options=year_list)
    with filter_col2:
        cat_list = ["ALL CATEGORIES"] + ["Full Marathon", "Between Half and Full", "Half Marathon", "Between 10K and 21K", "10K Runs", "Less than 10K"]
        selected_cat = st.selectbox("DISTANCE:", options=cat_list)
        
    f_df = df.copy()
    if selected_year != "ALL TIME": f_df = f_df[f_df['year'] == int(selected_year)]
    if selected_cat != "ALL CATEGORIES": f_df = f_df[f_df['Category_Custom'] == selected_cat]

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. STADIUM LED TICKER
    ticker_items = []
    row_10k = df[df['Date_Parsed'].dt.strftime('%Y-%m-%d') == '2024-04-28']
    row_21k = df[df['Date_Parsed'].dt.strftime('%Y-%m-%d') == '2025-10-12']
    row_42k = df[df['Date_Parsed'].dt.strftime('%Y-%m-%d') == '2025-09-21']
    
    if not row_10k.empty: ticker_items.append(f"PR 10K: TCS BENGALURU ({row_10k.iloc[0]['distance_km']:.2f}KM @ 5:54/KM // TIME: 59:00)")
    else: ticker_items.append("PR 10K: TCS BENGALURU (10.00KM @ 5:54/KM // TIME: 59:00)")
    if not row_21k.empty: r21 = row_21k.iloc[0]; ticker_items.append(f"PR HALF MARATHON: VEDANTA DELHI ({r21['distance_km']:.2f}KM @ {r21['pace_str']}/KM // TIME: {r21['moving_time_hms']})")
    if not row_42k.empty: r42 = row_42k.iloc[0]; ticker_items.append(f"PR FULL MARATHON: BERLIN ({r42['distance_km']:.2f}KM @ {r42['pace_str']}/KM // TIME: {r42['moving_time_hms']})")
        
    if ticker_items:
        full_ticker_text = " &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; // &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ".join(ticker_items)
        st.markdown(f"""<div class="ticker-wrap"><marquee behavior="scroll" direction="left" scrollamount="6" style="color: #ccff00; font-weight: 800; font-family: monospace; font-size: 1.1rem;">ALL-TIME RECORD BENCHMARKS // {full_ticker_text}</marquee></div>""", unsafe_allow_html=True)

    # 5. NAVIGATION
    tab_dashboard, tab_registry, tab_feed = st.tabs(["Overview and Analytics", "Race Registry", "Activity Feed Log"])

    # --- TAB 1 ---
    with tab_dashboard:
        st.markdown(f"""<div class="kpi-container"><div class="kpi-card"><div class="kpi-value">{len(f_df)}</div><div class="kpi-label">// INDEXED ACTIVITIES</div></div><div class="kpi-card"><div class="kpi-value">{f_df['distance_km'].sum():,.1f} KM</div><div class="kpi-label">// TOTAL DISTANCE</div></div><div class="kpi-card"><div class="kpi-value">{f_df['distance_km'].mean() if len(f_df)>0 else 0:.2f} KM</div><div class="kpi-label">// MEAN SESSION</div></div><div class="kpi-card"><div class="kpi-value">{f_df['year'].nunique()}</div><div class="kpi-label">// ACTIVE YEARS</div></div></div>""", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""<div class="chart-container-box"><h3>Volumes</h3>""", unsafe_allow_html=True)
            yoy = f_df.groupby('year')['distance_km'].sum().reset_index(); yoy['year'] = yoy['year'].astype(str)
            fig = px.bar(yoy, x='year', y='distance_km', text_auto='.0f', color='year', color_discrete_map={"2023": "#334155", "2024": "#00f0ff", "2025": "#ff4757", "2026": "#ccff00"})
            fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter, sans-serif", size=12, color="#94a3b8"), showlegend=False, bargap=0.4); fig.update_yaxes(showgrid=True, gridcolor="rgba(30, 41, 59, 0.4)", zeroline=False, title_text=""); st.plotly_chart(fig, use_container_width=True); st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("""<div class="chart-container-box"><h3>Frequency</h3>""", unsafe_allow_html=True)
            freq = f_df['Category_Custom'].value_counts().reset_index()
            fig = px.bar(freq, x='count', y='Category_Custom', orientation='h', text_auto='.0f')
            fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter, sans-serif", size=12, color="#94a3b8"), showlegend=False, bargap=0.4); fig.update_traces(marker_color="#ccff00"); fig.update_yaxes(showgrid=False, title_text=""); st.plotly_chart(fig, use_container_width=True); st.markdown("</div>", unsafe_allow_html=True)

    # --- TAB 2 ---
    with tab_registry:
        races = f_df[f_df['Race_Tag'].notna()].sort_values(by='Date_Parsed', ascending=False)
        for _, row in races.iterrows():
            is_full = row['Category_Custom'] == "Full Marathon"
            st.markdown(f"""<div style='background:{"#1a1215" if is_full else "#161d2a"}; padding:18px 24px; border-radius:6px; margin-bottom:14px; border-left:4px solid {"#ff4757" if is_full else "#ccff00"}; display:flex; justify-content:space-between; align-items:center;'><div><div style='color:{"#ff4757" if is_full else "#ccff00"}; font-size:0.7rem; font-weight:800; font-family:monospace;'>{'// PRESTIGE CLASS: 42.195KM' if is_full else ''}</div><div style='color:#ffffff; font-weight:800; font-size:1.15rem;'>{row['Race_Tag']}</div><div style='color:#64748b; font-size:0.75rem; font-family:monospace;'>{row['Date_Parsed'].strftime('%B %d, %Y')}</div></div><div style='text-align:right;'><div style='color:#ffffff; font-weight:800; font-size:1.2rem;'>{row['distance_km']:.2f} KM</div></div></div>""", unsafe_allow_html=True)

    # --- TAB 3 ---
    with tab_feed:
        st.markdown("### ACTIVITY FEED LOG")
        for _, row in f_df.sort_values(by='Date_Parsed', ascending=False).head(50).iterrows():
            is_full = row['Category_Custom'] == "Full Marathon"
            st.markdown(f"""<div class="flashcard-row-base" style='background:{"#1a1215" if is_full else "#121721"}; border-left: 4px solid {"#ff4757" if is_full else "#00f0ff"};'><div class="flashcard-left"><div><div style='color:#ffffff; font-weight:800; font-size:1.15rem;'>{row['name']}</div><div style='color:{"#ff4757" if is_full else "#ccff00"};'>{row['Category_Custom'].upper()}</div></div></div><div class="flashcard-metrics-group"><div class="flashcard-metric"><div class="flashcard-metric-val">{row['distance_km']:.2f} km</div><div class="flashcard-metric-lbl">Distance</div></div><div class="flashcard-metric"><div class="flashcard-metric-val">{row['moving_time_hms']}</div><div class="flashcard-metric-lbl">Time</div></div></div></div>""", unsafe_allow_html=True)
