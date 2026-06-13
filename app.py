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
            "2025-09-21": {"name": "Berlin Full Marathon", "bib": "76975",
