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

# 2. CORE DATA READING ENGINE WITH OFFICIAL RACE REGISTRY
@st.cache_data
def load_garmin_data():
    if not os.path.exists("Activities.csv"):
        return None
    try:
        # Load from native schema layout
        df = pd.read_csv("Activities.csv")
        
        # Enforce exact datetime type indexing 
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
        # -----------------------------------------------------------------
        
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
    if selected_year != "ALL TIME":
        f_df = f_df[f_df['year'] == int(selected_year)]
    if selected_cat != "ALL CATEGORIES":
        f_df = f_df[f_df['Category_Custom'] == selected_cat]

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. STADIUM LED TICKER (ISOLATED RACE-ONLY BENCHMARKS)
    ticker_items = []
    
    row_10k = df[df['Date_Parsed'].dt.strftime('%Y-%m-%d') == '2024-04-28']
    row_21k = df[df['Date'].dt.strftime('%Y-%m-%d') == '2025-10-12']
    row_42k = df[df['Date'].dt.strftime('%Y-%m-%d') == '2025-09-21']
    
    if not row_10k.empty:
        r10 = row_10k.iloc[0]
        ticker_items.append(f"PR 10K: TCS BENGALURU ({r10['distance_km']:.2f}KM @ 5:54/KM // TIME: 59:00)")
    else:
        ticker_items.append("PR 10K: TCS BENGALURU (10.00KM @ 5:54/KM // TIME: 59:00)")
        
    if not row_21k.empty:
        r21 = row_21k.iloc[0]
        p_str = f"{r21['pace_str']}/KM" if pd.notna(r21['pace_str']) else "--:--"
        t_str = f" // TIME: {r21['moving_time_hms']}" if pd.notna(r21['moving_time_hms']) else ""
        ticker_items.append(f"PR HALF MARATHON: VEDANTA DELHI ({r21['distance_km']:.2f}KM @ {p_str}{t_str})")
        
    if not row_42k.empty:
        r42 = row_42k.iloc[0]
        p_str = f"{r42['pace_str']}/KM" if pd.notna(r42['pace_str']) else "--:--"
        t_str = f" // TIME: {r42['moving_time_hms']}" if pd.notna(r42['moving_time_hms']) else ""
        ticker_items.append(f"PR FULL MARATHON: BERLIN ({r42['distance_km']:.2f}KM @ {p_str}{t_str})")
        
    if ticker_items:
        spacer = " &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; // &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "
        full_ticker_text = spacer.join(ticker_items)
        st.markdown(f"""<div class="ticker-wrap"><marquee behavior="scroll" direction="left" scrollamount="6" style="color: #ccff00; font-weight: 800; font-family: monospace; font-size: 1.1rem;">ALL-TIME RECORD BENCHMARKS // {full_ticker_text}</marquee></div>""", unsafe_allow_html=True)

    # 5. HIGH-VISIBILITY NAVIGATION ARCHITECTURE
    tab_dashboard, tab_facts, tab_feed = st.tabs(["Overview and Analytics", "System Insights and Milestones", "Activity Feed Log"])

    # Define a clean, master layout configuration dict for uniform modern charts
    premium_chart_layout = dict(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=15, b=10),
        font=dict(family="Inter, sans-serif", size=12, color="#94a3b8"),
        showlegend=False,
        bargap=0.4
    )
    
    # Secure fixed color variables across years to look unified
    athletic_color_map = {
        "2023": "#334155",  # Deep Subdued Slate
        "2024": "#00f0ff",  # Electric Cyan
        "2025": "#ff4757",  # Racing Crimson
        "2026": "#ccff00"   # Volt Green
    }

    # --- TAB 1: OVERVIEW & ANALYTICS ---
    with tab_dashboard:
        total_runs = len(f_df)
        total_km = f_df['distance_km'].sum()
        avg_run_dist = f_df['distance_km'].mean() if total_runs > 0 else 0
        tracked_years = f_df['year'].nunique()
        
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
            st.markdown("""<div class="chart-container-box"><h3>Volumes</h3>""", unsafe_allow_html=True)
            yoy_volume = f_df.groupby('year')['distance_km'].sum().reset_index()
            yoy_volume['year'] = yoy_volume['year'].astype(str)
            
            fig_yoy = px.bar(
                yoy_volume, x='year', y='distance_km', text_auto='.0f',
                color='year', color_discrete_map=athletic_color_map
            )
            fig_yoy.update_layout(**premium_chart_layout)
            fig_yoy.update_xaxes(showgrid=False, zeroline=False, title_text="")
            fig_yoy.update_yaxes(showgrid=True, gridcolor="rgba(30, 41, 59, 0.4)", zeroline=False, title_text="")
            fig_yoy.update_traces(textposition="outside", textfont=dict(family="monospace", weight="bold"))
            st.plotly_chart(fig_yoy, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("""<div class="chart-container-box"><h3>Frequency</h3>""", unsafe_allow_html=True)
            cat_order = ["Full Marathon", "Between Half and Full", "Half Marathon", "Between 10K and 21K", "10K Runs", "Less than 10K"]
            cat_counts = f_df['Category_Custom'].value_counts().reindex(cat_order).fillna(0).reset_index()
            cat_counts.columns = ['Category_Custom', 'Runs']
            
            fig_cat = px.bar(cat_counts, x='Runs', y='Category_Custom', orientation='h', text_auto='.0f')
            fig_cat.update_layout(**premium_chart_layout)
            fig_cat.update_traces(marker_color="#ccff00", textposition="outside", textfont=dict(family="monospace", weight="bold"))
            fig_cat.update_xaxes(showgrid=True, gridcolor="rgba(30, 41, 59, 0.4)", zeroline=False, title_text="")
            fig_cat.update_yaxes(showgrid=False, zeroline=False, title_text="", categoryorder="array", categoryarray=cat_order[::-1])
            st.plotly_chart(fig_cat, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""<div class="chart-container-box"><h3>Timeline</h3>""", unsafe_allow_html=True)
        if selected_year == "ALL TIME":
            # Extract month string cleanly using internal structures
            monthly_grouped = f_df.groupby(['year', 'Month_Num', 'Month_Short'])['distance_km'].sum().reset_index()
            monthly_grouped = monthly_grouped.sort_values(['year', 'Month_Num'])
            monthly_grouped['Timeline'] = monthly_grouped['Month_Short'] + " '" + monthly_grouped['year'].astype(str).str[-2:]
            monthly_grouped['year'] = monthly_grouped['year'].astype(str)
            
            fig_month = px.bar(
                monthly_grouped, x='Timeline', y='distance_km', text_auto='.0f',
                color='year', color_discrete_map=athletic_color_map
            )
            fig_month.update_layout(**premium_chart_layout)
            fig_month.update_xaxes(type='category', showgrid=False, zeroline=False, title_text="")
        else:
            monthly_grouped = f_df.groupby(['Month_Num', 'Month_Short'])['distance_km'].sum().reset_index()
            all_months = pd.DataFrame({
                'Month_Num': range(1, 13),
                'Month_Short': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            })
            monthly_volume = pd.merge(all_months, monthly_grouped, on=['Month_Num', 'Month_Short'], how='left').fillna(0)
            
            fig_month = px.bar(monthly_volume, x='Month_Short', y='distance_km', text_auto='.0f')
            fig_month.update_layout(**premium_chart_layout)
            fig_month.update_traces(marker_color="#00f0ff")
            fig_month.update_xaxes(categoryorder='array', categoryarray=all_months['Month_Short'], showgrid=False, zeroline=False, title_text="")
            
        fig_month.update_yaxes(showgrid=True, gridcolor="rgba(30, 41, 59, 0.4)", zeroline=False, title_text="")
        fig_month.update_traces(textposition="outside", textfont=dict(family="monospace", weight="bold"))
        st.plotly_chart(fig_month, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- TAB 2: SYSTEM INSIGHTS & MILESTONES ---
    with tab_facts:
        if f_df.empty:
            st.warning("Insufficient data parameters matching current selection.")
        else:
            # OFFICIAL COMPETITIVE HISTORY REGISTRY SHOWCASE AS THE PRIMARY ANCHOR
            st.markdown("""<div class="chart-container-box"><h3>Official Competitive History Registry</h3>""", unsafe_allow_html=True)
            
            registered_races = f_df[f_df['Race_Tag'].notna()].sort_values(by='Date_Parsed', ascending=False)
            
            if not registered_races.empty:
                st.markdown("<p style='color:#94a3b8; font-size:0.9rem; margin-bottom:20px;'>The following verified competitive profiles have been linked and cross-referenced via your secure date registry:</p>", unsafe_allow_html=True)
                
                for _, row in registered_races.iterrows():
                    p_str = "5:54 /km" if row['Date_Parsed'].strftime('%Y-%m-%d') == '2024-04-28' else f"{row['pace_str']} /km" if pd.notna(row['pace_str']) else "--:--"
                    r_date_formatted = row['Date_Parsed'].strftime('%B %d, %Y')
                    bib_string = f" // BIB: {row['Race_Bib']}" if row['Race_Bib'] else ""
                    
                    is_full_marathon = row['Category_Custom'] == "Full Marathon"
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
<div style='color:#64748b; font-size:0.75rem; font-family:monospace; margin-top:3px;'>CONQUERED: {r_date_formatted}</div>
{note_markup}
</div>
<div style='text-align:right; font-family:monospace;'>
<div style='color:#ffffff; font-weight:800; font-size:1.2rem;'>{row['distance_km']:.2f} KM</div>
<div style='color:#00f0ff; font-size:0.75rem; text-transform:uppercase; font-weight:700;'>PACE: {p_str}</div>
</div>
</div>""", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#64748b;'>No official verified race dates found within the currently active filter window.</p>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

    # --- TAB 3: ACTIVITY FEED LOG ---
    with tab_feed:
        st.markdown("### ACTIVITY FEED LOG")
        if f_df.empty:
            st.warning("No performance records match your active filtering configuration.")
        else:
            sorted_cards = f_df.sort_values(by='Date_Parsed', ascending=False)
            display_limit = 50
            
            for idx, (_, row) in enumerate(sorted_cards.head(display_limit).iterrows()):
                date_main = row['Date_Parsed'].strftime('%b %d')
                date_sub = row['Date_Parsed'].strftime('%Y')
                
                card_date_str = row['Date_Parsed'].strftime('%Y-%m-%d')
                p_str = "5:54 /km" if card_date_str == '2024-04-28' else f"{row['pace_str']} /km" if pd.notna(row['pace_str']) else "--:--"
                
                # Dynamic matching using row column parameters from native strava definitions
                hr_val = row['relative_effort']  # Default backup if heartrate field omitted 
                if 'calories' in row and pd.notna(row['calories']):
                    hr_str = f"{int(row['calories'])} cal"
                else:
                    hr_str = "--"
                
                race_label = f" // {row['Race_Tag']}" if pd.notna(row['Race_Tag']) else ""
                
                is_full = row['Category_Custom'] == "Full Marathon"
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
<div class="flashcard-title">{row['name']}{race_label}</div>
<div class="flashcard-category" style="color: {category_label_color};">{row['Category_Custom'].upper()}</div>
</div>
</div>
<div class="flashcard-metrics-group">
<div class="flashcard-metric">
<div class="flashcard-metric-val">{row['distance_km']:.2f} km</div>
<div class="flashcard-metric-lbl">Distance</div>
</div>
<div class="flashcard-metric">
<div class="flashcard-metric-val">{row['moving_time_hms'] if card_date_str != '2024-04-28' else "59:00"}</div>
<div class="flashcard-metric-lbl">Time</div>
</div>
<div class="flashcard-metric">
<div class="flashcard-metric-val">{p_str}</div>
<div class="flashcard-metric-lbl">Avg Pace</div>
</div>
<div class="flashcard-metric">
<div class="flashcard-metric-val" style="color: #ff4757;">{int(row['kudos'])} ★</div>
<div class="flashcard-metric-lbl">Kudos</div>
</div>
</div>
</div>""", unsafe_allow_html=True)
                
            if len(sorted_cards) > display_limit:
                st.markdown(f"<p style='text-align:center; color:#64748b;'>Truncated loop breakdown at {display_limit} items.</p>", unsafe_allow_html=True)
