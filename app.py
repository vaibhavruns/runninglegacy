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
/* Fact Grid Layout */
.fact-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}
.fact-card {
    background: #121721;
    border: 1px solid #1e293b;
    border-radius: 6px;
    padding: 22px;
    border-top: 3px solid #ccff00;
}
.fact-title {
    font-size: 0.75rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
    font-weight: 700;
}
.fact-value {
    font-size: 1.5rem;
    font-weight: 800;
    color: #ffffff !important;
    font-family: monospace;
    line-height: 1.2;
}
.fact-sub {
    font-size: 0.7rem;
    color: #00f0ff !important;
    text-transform: uppercase;
    margin-top: 6px;
    letter-spacing: 0.5px;
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

# 2. CORE DATA READING ENGINE WITH VERIFIED RACE REGISTRY
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
        
        df['Activity_Title'] = df[title_matches[0]] if title_matches else "Training Run"
        df['Duration_Raw'] = df[time_matches[0]] if time_matches else "--:--"
        df['Heart_Rate'] = df[hr_matches[0]] if hr_matches else None
        
        df['Date'] = pd.to_datetime(df[date_col])
        df['Year'] = df['Date'].dt.year
        df['Month_Num'] = df['Date'].dt.month
        df['Month_Name'] = df['Date'].dt.strftime('%b')
        df['Day_Name'] = df['Date'].dt.day_name()
        df['Distance_KM'] = pd.to_numeric(df[dist_col], errors='coerce').fillna(0)
        
        # -----------------------------------------------------------------
        # EXPLICIT VERIFIED RACE MATRIX
        # -----------------------------------------------------------------
        RACE_REGISTRY = {
            "2024-10-20": {"name": "Vedanta Delhi Half Marathon", "bib": "3258", "note": ""},
            "2024-12-08": {"name": "Indian Navy 21K", "bib": "23781", "note": ""},
            "2024-12-15": {"name": "Tata Steel World 25K Kolkata", "bib": "4653", "note": ""},
            "2025-09-21": {"name": "Berlin Full Marathon", "bib": "76975", "note": ""},
            "2025-10-12": {"name": "Vedanta Delhi Half Marathon", "bib": "5654", "note": ""},
            "2025-12-21": {"name": "Tata Steel World 25K Kolkata", "bib": "4895", "note": ""},
            "2026-01-18": {"name": "Tata Mumbai Full Marathon", "bib": "11435", "note": ""},
            "2026-04-26": {"name": "TCS World 10K Bengaluru", "bib": "32357", "note": "PROCAM SLAM COMPLETED"}
        }
        
        date_str_series = df['Date'].dt.strftime('%Y-%m-%d')
        df['Race_Tag'] = date_str_series.apply(lambda x: RACE_REGISTRY[x]['name'] if x in RACE_REGISTRY else None)
        df['Race_Bib'] = date_str_series.apply(lambda x: RACE_REGISTRY[x]['bib'] if x in RACE_REGISTRY else None)
        df['Race_Note'] = date_str_series.apply(lambda x: RACE_REGISTRY[x]['note'] if x in RACE_REGISTRY else None)
        # -----------------------------------------------------------------
        
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
        st.markdown(f"""<div class="ticker-wrap"><marquee behavior="scroll" direction="left" scrollamount="6" style="color: #ccff00; font-weight: 800; font-family: monospace; font-size: 1.1rem;">ALL-TIME RECORD BENCHMARKS // {full_ticker_text}</marquee></div>""", unsafe_allow_html=True)

    # 5. HIGH-VISIBILITY NAVIGATION ARCHITECTURE
    tab_dashboard, tab_facts, tab_feed = st.tabs(["Overview and Analytics", "System Insights and Milestones", "Activity Feed Log"])

    # --- TAB 1: OVERVIEW & ANALYTICS ---
    with tab_dashboard:
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

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""<div class="chart-container-box"><h2>Annual Training Volume</h2>""", unsafe_allow_html=True)
            yoy_volume = f_df.groupby('Year')['Distance_KM'].sum().reset_index()
            yoy_volume['Year'] = yoy_volume['Year'].astype(str)
            
            fig_yoy = px.bar(
                yoy_volume, x='Year', y='Distance_KM', text_auto='.1f', 
                color='Year', color_discrete_sequence=['#00f0ff', '#ccff00', '#ff4757']
            )
            fig_yoy.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", yaxis_title="VOLUME (KM)", xaxis_title="", showlegend=False)
            st.plotly_chart(fig_yoy, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("""<div class="chart-container-box"><h3>Distribution Matrix</h3>""", unsafe_allow_html=True)
            cat_order = ["Full Marathon", "Between Half and Full", "Half Marathon", "Between 10K and 21K", "10K Runs", "Less than 10K"]
            cat_counts = f_df['Category'].value_counts().reindex(cat_order).fillna(0).reset_index()
            cat_counts.columns = ['Category', 'Runs']
            
            fig_cat = px.bar(cat_counts, x='Runs', y='Category', orientation='h', color_discrete_sequence=['#ccff00'])
            fig_cat.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis_title="FREQUENCY", yaxis_title="")
            st.plotly_chart(fig_cat, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""<div class="chart-container-box"><h3>Intra-Annual Splits Timeline</h3>""", unsafe_allow_html=True)
        if selected_year == "ALL TIME":
            monthly_grouped = f_df.groupby(['Year', 'Month_Num', 'Month_Name'])['Distance_KM'].sum().reset_index()
            monthly_grouped = monthly_grouped.sort_values(['Year', 'Month_Num'])
            monthly_grouped['Timeline'] = monthly_grouped['Month_Name'] + " '" + monthly_grouped['Year'].astype(str).str[-2:]
            
            fig_month = px.bar(
                monthly_grouped, x='Timeline', y='Distance_KM', text_auto='.1f',
                color='Year', color_discrete_sequence=px.colors.qualitative.Safe
            )
            fig_month.update_layout(xaxis={'type': 'category'})
        else:
            monthly_grouped = f_df.groupby(['Month_Num', 'Month_Name'])['Distance_KM'].sum().reset_index()
            all_months = pd.DataFrame({
                'Month_Num': range(1, 13),
                'Month_Name': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            })
            monthly_volume = pd.merge(all_months, monthly_grouped, on=['Month_Num', 'Month_Name'], how='left').fillna(0)
            
            fig_month = px.bar(monthly_volume, x='Month_Name', y='Distance_KM', text_auto='.1f', color_discrete_sequence=['#00f0ff'])
            fig_month.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': all_months['Month_Name']})
            
        fig_month.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", yaxis_title="VOLUME (KM)", xaxis_title="")
        st.plotly_chart(fig_month, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- TAB 2: SYSTEM INSIGHTS & MILESTONES ---
    with tab_facts:
        if f_df.empty:
            st.warning("Insufficient data parameters matching current selection.")
        else:
            # 1. ANCHOR SHOWCASE: OFFICIAL COMPETITIVE HISTORY REGISTRY AT THE TOP
            st.markdown("""<div class="chart-container-box"><h3>Official Competitive History Registry</h3>""", unsafe_allow_html=True)
            
            registered_races = f_df[f_df['Race_Tag'].notna()].sort_values(by='Date', ascending=False)
            
            if not registered_races.empty:
                st.markdown("<p style='color:#94a3b8; font-size:0.9rem; margin-bottom:20px;'>The following verified competitive profiles have been linked and cross-referenced via your secure date registry:</p>", unsafe_allow_html=True)
                
                for _, row in registered_races.iterrows():
                    p_val = row['Pace_Decimal']
                    p_str = f"{int(p_val)}:{int((p_val % 1) * 60):02d} /km" if pd.notna(p_val) else "--:--"
                    r_date = row['Date'].strftime('%B %d, %Y')
                    bib_string = f" // BIB: {row['Race_Bib']}" if row['Race_Bib'] else ""
                    
                    is_full_marathon = row['Category'] == "Full Marathon"
                    card_left_border = "#ff4757" if is_full_marathon else "#ccff00"
                    card_bg_style = "background:#1a1215;" if is_full_marathon else "background:#161d2a;"
                    
                    class_tag = "<div style='color:#ff4757; font-size:0.7rem; font-weight:800; font-family:monospace; margin-bottom:4px;'>// PRESTIGE CLASS: 42.195KM FULL MARATHON</div>" if is_full_marathon else ""
                    
                    note_markup = ""
                    if pd.notna(row['Race_Note']) and row['Race_Note'] != "":
                        note_color = "#ff4757" if is_full_marathon else "#ccff00"
                        note_markup = f"<div style='margin-top: 10px; background: rgba(255, 71, 87, 0.08); border: 1px solid {note_color}; padding: 6px 14px; border-radius: 4px; color: {note_color}; font-size: 0.75rem; font-weight: 800; display: inline-block; letter-spacing: 1px; font-family: monospace;'>// ACCOMPLISHMENT: {row['Race_Note'].upper()}</div>"
                    
                    st.markdown(f"""<div style='{card_bg_style} padding:18px 24px; border-radius:6px; margin-bottom:14px; border-left:4px solid {card_left_border}; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:15px;'>
<div>
{class_tag}
<div style='color:#ffffff; font-weight:800; font-size:1.15rem; text-transform:uppercase;'>{row['Race_Tag']}{bib_string}</div>
<div style='color:#64748b; font-size:0.75rem; font-family:monospace; margin-top:3px;'>CONQUERED: {r_date}</div>
{note_markup}
</div>
<div style='text-align:right; font-family:monospace;'>
<div style='color:#ffffff; font-weight:800; font-size:1.2rem;'>{row['Distance_KM']:.2f} KM</div>
<div style='color:#00f0ff; font-size:0.75rem; text-transform:uppercase; font-weight:700;'>PACE: {p_str}</div>
</div>
</div>""", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#64748b;'>No official verified race dates found within the currently active filter window.</p>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

            # 2. SECONDARY LAYER: EXTRACTED INSIGHT CHARTS & FACTS
            st.markdown("### SYSTEM RUNNING METRIC LOGS")
            
            longest_run_row = f_df.loc[f_df['Distance_KM'].idxmax()]
            longest_dist = longest_run_row['Distance_KM']
            longest_date = longest_run_row['Date'].strftime('%B %d, %Y')
            
            valid_efforts = f_df[(f_df['Distance_KM'] >= 5.0) & (f_df['Pace_Decimal'].notna())]
            if not valid_efforts.empty:
                fastest_row = valid_efforts.loc[valid_efforts['Pace_Decimal'].idxmin()]
                f_pace_dec = fastest_row['Pace_Decimal']
                fastest_pace = f"{int(f_pace_dec)}:{int((f_pace_dec % 1) * 60):02d} /km"
                fastest_meta = f"{fastest_row['Distance_KM']:.2f}KM on {fastest_row['Date'].strftime('%b %d, %Y')}"
            else:
                fastest_pace = "No data"
                fastest_meta = "Minimum distance threshold 5KM"

            monthly_totals = f_df.groupby(['Year', 'Month_Name'])['Distance_KM'].sum().reset_index()
            peak_month_row = monthly_totals.loc[monthly_totals['Distance_KM'].idxmax()]
            peak_month_str = f"{peak_month_row['Month_Name']} {peak_month_row['Year']}"
            peak_month_vol = f"{peak_month_row['Distance_KM']:.1f} KM"

            day_counts = f_df['Day_Name'].value_counts()
            dominant_day = day_counts.index[0]
            dominant_day_count = f"{day_counts.iloc[0]} Sessions"

            st.markdown(f"""<div class="fact-grid">
<div class="fact-card" style="border-top:3px solid #ff4757;">
    <div class="fact-title">Peak Endurance Distance</div>
    <div class="fact-value">{longest_dist:.2f} KM</div>
    <div class="fact-sub">Recorded on {longest_date}</div>
</div>
<div class="fact-card">
    <div class="fact-title">Fastest Pacing Effort</div>
    <div class="fact-value">{fastest_pace}</div>
    <div class="fact-sub">{fastest_meta}</div>
</div>
<div class="fact-card">
    <div class="fact-title">Peak Training Volume Month</div>
    <div class="fact-value">{peak_month_vol}</div>
    <div class="fact-sub">Achieved during {peak_month_str}</div>
</div>
<div class="fact-card">
    <div class="fact-title">Dominant Training Window</div>
    <div class="fact-value">{dominant_day}</div>
    <div class="fact-sub">Accounted for {dominant_day_count}</div>
</div>
</div>""", unsafe_allow_html=True)

    # --- TAB 3: ACTIVITY FEED LOG ---
    with tab_feed:
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
                
                is_full = row['Category'] == "Full Marathon"
                stripe_color = "#ff4757" if is_full else "#00f0ff"
                bg_color = "background: #1a1215;" if is_full else "background: #121721;"
                category_label_color = "#ff4757" if is_full else "#ccff00"
                
                st.markdown(f"""<div class="flashcard-row-base" style="{bg_color} border-left: 4px solid {stripe_color};">
<div class="flashcard-left">
<div class="flashcard-date-block">
<div class="flashcard-date-main">{date_main}</div>
<div class="flashcard-date-sub">{date_sub}</div>
</div>
<div>
<div class="flashcard-title">{row['Activity_Title']}{race_label}</div>
<div class="flashcard-category" style="color: {category_label_color};">{row['Category'].upper()}</div>
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
</div>""", unsafe_allow_html=True)
                
            if len(sorted_cards) > display_limit:
                st.markdown(f"<p style='text-align:center; color:#64748b;'>Truncated loop breakdown at {display_limit} items.</p>", unsafe_allow_html=True)
