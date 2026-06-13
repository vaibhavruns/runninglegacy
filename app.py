import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="My Running Legacy", page_icon="⚡", layout="wide")

# Premium UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; font-family: 'Inter', sans-serif; }
    section[data-testid="stSidebar"] { background-color: #161b22 !important; border-right: 1px solid #30363d; }
    .kpi-card { background: linear-gradient(135deg, #1f2937 0%, #111827 100%); padding: 25px; border-radius: 16px; border: 1px solid #374151; text-align: center; }
    .kpi-value { font-size: 2.2rem; font-weight: 800; color: #ffffff; }
    .kpi-label { font-size: 0.9rem; color: #9ca3af; text-transform: uppercase; letter-spacing: 1.5px; }
    </style>
""", unsafe_allow_html=True)

# DIAGNOSTIC DATA LOADING ENGINE
@st.cache_data
def load_premium_data():
    if not os.path.exists("activities.csv"):
        return None, "File Not Found: The server cannot find a file named 'activities.csv' in the main folder."
    try:
        df = pd.read_csv("activities.csv")
        # Find date column dynamically
        date_cols = [c for c in df.columns if 'Date' in c or 'Time' in c or 'Start' in c]
        if not date_cols:
            return None, f"Column Error: Could not find a 'Date' column. Your file columns are: {list(df.columns)}"
        
        df['Date'] = pd.to_datetime(df[date_cols[0]])
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.strftime('%B')
        return df, None
    except Exception as e:
        return None, f"Parsing Error: {str(e)}"

df, error_message = load_premium_data()

st.sidebar.markdown("<h2 style='color:#10b981; text-align:center;'>⚡ LEGACY ENGINE</h2>", unsafe_allow_html=True)
page = st.sidebar.radio("Go to:", ["📊 Performance Analytics", "🌍 Interactive Map"])

if page == "📊 Performance Analytics":
    st.markdown("<h1 style='color: white; font-weight: 800;'>🏃‍♂️ Lifetime Running Monument</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    if df is None:
        st.warning("📊 Awaiting Data Link...")
        st.info("The system is live, but needs a correction on the data file configuration. See details below:")
        st.error(error_message)
        
        # Help block to see what files are actually present
        st.markdown("### 🔍 Current Files Detected in Cloud:")
        st.write(os.listdir("."))
    else:
        # If successfully loaded, show the metrics
        dist_col = [c for c in df.columns if 'Distance' in c][0]
        pace_col = [c for c in df.columns if 'Pace' in c or 'Speed' in c][0]
        hr_col = [c for c in df.columns if 'Heart Rate' in c or 'HR' in c]
        
        st.markdown(f"""
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-bottom: 40px;">
                <div class="kpi-card"><div class="kpi-value">{len(df)}</div><div class="kpi-label">Lifetime Runs</div></div>
                <div class="kpi-card"><div class="kpi-value">{df[dist_col].sum():,.1f} KM</div><div class="kpi-label">Total Volume</div></div>
                <div class="kpi-card"><div class="kpi-value">{df['Year'].nunique()}</div><div class="kpi-label">Years of Discipline</div></div>
            </div>
        """, unsafe_allow_html=True)
        
        st.subheader("📊 Career Progression Data Log")
        st.dataframe(df.sort_values(by='Date', ascending=False), use_container_width=True)

else:
    st.markdown("<h1 style='color: white; font-weight: 800;'>🌍 Geospatial Map</h1>", unsafe_allow_html=True)
    st.map()
