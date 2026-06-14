import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="RUNNING JOURNEY", layout="wide")

# --- DESIGN TOKENS ---
LIME = "#ccff00"; CYAN = "#00f0ff"; RED = "#ff4757"
INK = "#0b0e14"; CARD = "#121721"; MUTE = "#64748b"
YEAR_COLORS = {"2022": "#475569", "2023": "#334155", "2024": CYAN, "2025": RED, "2026": LIME}
CADENCE_TARGET = 174

st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
.stApp { background-color: #0b0e14; color: #e2e8f0; font-family: 'Inter', system-ui, sans-serif; }
.js-plotly-plot .plotly .main-svg { touch-action: none; }
h1,h2,h3 { color:#fff !important; text-transform:uppercase; letter-spacing:1.5px; }
div[data-testid="stTabs"] button { font-weight:800; text-transform:uppercase; color:#64748b !important; }
div[data-testid="stTabs"] button[aria-selected="true"] { color:#ccff00 !important; border-bottom:3px solid #ccff00 !important; }
.chart-container-box { background:#121721 !important; border:1px solid #1e293b !important; border-radius:8px !important; padding:20px !important; }
</style>
""", unsafe_allow_html=True)

# --- DATA ENGINE ---
@st.cache_data
def load_data():
    # Place your existing load_data() logic here
    return df # Assuming df is loaded

# --- HELPER GRID (Fixed for Mobile) ---
def grid(fig):
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", 
                      margin=dict(l=10,r=10,t=20,b=10), dragmode=False) # dragmode=False fixes touch-zoom
    fig.update_xaxes(showgrid=False); fig.update_yaxes(showgrid=True, gridcolor="rgba(30,41,59,.45)")
    return fig

df = load_data()
tabs = st.tabs(["Overview", "Data", "Race Registry", "Activity Log"])

# --- TAB 1: OVERVIEW ---
with tabs[0]:
    st.markdown("### RUNNING TIMELINE")
    st.markdown("""
    - **2022** — Started Running
    - **2023** — First Organized Race
    - **2024** — First Half Marathon
    - **2025** — Berlin Marathon
    - **2026** — Mumbai Marathon
    
    Running is the rhythm of my discipline. It is where I find clarity, push boundaries, and transform effort into progress. Each step is a deliberate move towards a stronger, more focused version of myself.
    """)
    # (Insert your existing KPI grid and summary charts here)

# --- TAB 2: DATA (Consolidated) ---
with tabs[1]:
    st.markdown("### ANALYTICAL SUITE")
    view = st.selectbox("SELECT VIEW:", ["Volume Trends", "Heart Rate Analysis", "Running Dynamics", "Global Map"])
    
    if view == "Global Map":
        if os.path.exists("race_locations.csv"):
            locs = pd.read_csv("race_locations.csv")
            fig = px.scatter_mapbox(locs, lat="lat", lon="lon", hover_name="race_name", zoom=1)
            fig.update_layout(mapbox_style="carto-darkmatter", margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(grid(fig), use_container_width=True)
        else:
            st.warning("Upload 'race_locations.csv' (race_name, lat, lon) to see map.")
    else:
        st.info(f"Rendering: {view} charts...")
        # (Insert your existing Trends/Heart/Dynamics chart logic here)

# --- TAB 3: RACE REGISTRY (Formerly Records) ---
with tabs[2]:
    st.markdown("### RACE REGISTRY")
    # (Insert your existing Records loop and race card code here)

# --- TAB 4: ACTIVITY LOG ---
with tabs[3]:
    st.markdown("### ACTIVITY FEED LOG")
    # (Insert your existing activity log loop code here)
