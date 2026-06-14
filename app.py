import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="RUNNING JOURNEY", layout="wide")

# --- DESIGN TOKENS ---
LIME, CYAN, RED = "#ccff00", "#00f0ff", "#ff4757"
INK, CARD, MUTE = "#0b0e14", "#121721", "#64748b"
YEAR_COLORS = {"2022": "#475569", "2023": "#334155", "2024": CYAN, "2025": RED, "2026": LIME}
CADENCE_TARGET = 174
CHART = dict(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
             margin=dict(l=10,r=10,t=20,b=10), font=dict(family="Inter, sans-serif", size=12, color="#94a3b8"),
             showlegend=False)

st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
.stApp { background-color: #0b0e14; color: #e2e8f0; font-family: 'Inter', system-ui, sans-serif; }
.js-plotly-plot .plotly .main-svg { touch-action: none; }
h1,h2,h3 { color:#fff !important; text-transform:uppercase; letter-spacing:1.5px; }
div[data-testid="stTabs"] button { font-weight:800; text-transform:uppercase; color:#64748b !important; }
div[data-testid="stTabs"] button[aria-selected="true"] { color:#ccff00 !important; border-bottom:3px solid #ccff00 !important; }
.chart-container-box { background:#121721 !important; border:1px solid #1e293b !important; border-radius:8px !important; padding:20px !important; }
.kpi-card { background:#121721; padding:22px; border-radius:6px; border:1px solid #1e293b; border-bottom:3px solid #1e293b; }
.kpi-value { font-size:2.2rem; font-weight:900; color:#fff; font-family:monospace; }
</style>
""", unsafe_allow_html=True)

# --- DATA ENGINE ---
@st.cache_data
def load_data():
    if not os.path.exists("activities.csv"): return None
    df = pd.read_csv("activities.csv")
    df["Date_Parsed"] = pd.to_datetime(df["date"])
    for c in ["distance_km","moving_time_s","pace_min_per_km","cadence_spm"]:
        if c in df.columns: df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

def grid(fig):
    fig.update_layout(**CHART, dragmode=False)
    return fig

df = load_data()
runs_f = df[df["sport_type"] == "Run"]

# --- NAVIGATION ---
tabs = st.tabs(["Overview", "Data", "Race Registry", "Activity Log"])

with tabs[0]: # OVERVIEW
    st.markdown("### RUNNING TIMELINE")
    st.markdown("""
    - 2022 — Started Running
    - 2023 — First Organized Race
    - 2024 — First Half Marathon
    - 2025 — Berlin Marathon
    - 2026 — Mumbai Marathon
    
    *Running is my rhythm and my discipline. Every mile is a reminder of what is possible when I just keep moving forward.*
    """)

with tabs[1]: # DATA (Merged Trends, Heart, Dynamics, Patterns)
    st.markdown("### ANALYTICAL SUITE")
    view = st.selectbox("CHOOSE CHART:", ["Volume Trends", "Pace Trend", "Global Map"])
    
    if view == "Global Map":
        if os.path.exists("race_locations.csv"):
            locs = pd.read_csv("race_locations.csv")
            fig = px.scatter_mapbox(locs, lat="lat", lon="lon", hover_name="race_name", zoom=1)
            fig.update_layout(mapbox_style="carto-darkmatter", margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(grid(fig), use_container_width=True)
        else:
            st.warning("Upload 'race_locations.csv' (race_name, lat, lon) to see map.")
    elif view == "Volume Trends":
        st.markdown("### WEEKLY MILEAGE")
        wk = runs_f.set_index("Date_Parsed")["distance_km"].resample("W-MON").sum().reset_index()
        fig = px.bar(wk, x="Date_Parsed", y="distance_km")
        st.plotly_chart(grid(fig), use_container_width=True)

with tabs[2]: # RACE REGISTRY
    st.markdown("### RACE REGISTRY")
    st.info("Upload race photos to assets/races/ named YYYY-MM-DD.png to populate this view.")
    # Add your registry loop here

with tabs[3]: # ACTIVITY LOG
    st.markdown("### ACTIVITY FEED LOG")
    st.dataframe(df.sort_values("Date_Parsed", ascending=False), use_container_width=True)
