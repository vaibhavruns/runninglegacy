import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# 1. PREMIUM PAGE SETUP & CUSTOM CSS INJECTION
st.set_page_config(page_title="The Running Legacy", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

# Inject Custom CSS for a high-end, premium Dark Mode SaaS aesthetic
st.markdown("""
    <style>
    /* Main background and font styling */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #30363d;
    }
    /* Premium KPI Card Design */
    .kpi-card {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        padding: 25px;
        border-radius: 16px;
        border: 1px solid #374151;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        text-align: center;
        transition: transform 0.3s ease;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
        border-color: #10b981;
    }
    .kpi-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 5px;
        font-family: 'Monospace', Courier;
    }
    .kpi-label {
        font-size: 0.9rem;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    /* Photo Card Styling */
    .photo-card {
        background-color: #1f2937;
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #374151;
        margin-bottom: 20px;
    }
    .photo-caption {
        padding: 12px;
        font-size: 0.9rem;
        color: #e5e7eb;
        background-color: #111827;
    }
    </style>
""", unsafe_allow_html=True)

# 2. DATA PROCESSING ENGINE
@st.cache_data
def load_premium_data():
    try:
        df = pd.read_csv("activities.csv")
        date_col = [c for c in df.columns if 'Date' in c or 'Time' in c][0]
        df['Date'] = pd.to_datetime(df[date_col])
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.strftime('%B')
        return df
    except:
        return None

df = load_premium_data()

# Navigation
st.sidebar.markdown("<h2 style='color:#10b981; text-align:center;'>⚡ LEGACY ENGINE</h2>", unsafe_allow_html=True)
page = st.sidebar.radio("Go to:", ["📊 Performance Analytics", "🌍 Interactive Map", "🖼️ Race Wall & Memory Gallery"])

# Core Variables
if df is not None:
    dist_col = [c for c in df.columns if 'Distance' in c][0]
    pace_col = [c for c in df.columns if 'Pace' in c or 'Speed' in c][0]
    hr_col = [c for c in df.columns if 'Heart Rate' in c or 'HR' in c]

# ==========================================
# PAGE 1: PERFORMANCE ANALYTICS (UPGRADED)
# ==========================================
if page == "📊 Performance Analytics":
    st.markdown("<h1 style='color: white; font-weight: 800;'>🏃‍♂️ Lifetime Running Monument</h1>", unsafe_allow_html=True)
    st.markdown("A deep-dive data visualization of career endurance progression.")
    st.markdown("---")
    
    if df is None:
        st.info("👋 Upload your `activities.csv` to GitHub to populate your live metrics.")
    else:
        # Premium KPI Metric Row using HTML Grid
        total_runs = len(df)
        total_km = df[dist_col].sum()
        avg_hr = int(df[hr_col[0]].mean()) if hr_col else 145
        
        st.markdown(f"""
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-bottom: 40px;">
                <div class="kpi-card">
                    <div class="kpi-value">{total_runs}</div>
                    <div class="kpi-label">Lifetime Runs</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">{total_km:,.1f} KM</div>
                    <div class="kpi-label">Total Volume</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">{avg_hr} BPM</div>
                    <div class="kpi-label">Avg Cardiovascular HR</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">{df['Year'].nunique()}</div>
                    <div class="kpi-label">Years of Discipline</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Advanced Plotly Chart: Volume Progression over Time
        st.subheader("📈 Monthly Volume & Pacing Architecture")
        
        monthly_data = df.groupby(['Year', 'Month'])[dist_col].sum().reset_index()
        
        # High-end Area Chart
        fig_vol = px.area(
            monthly_data, x="Month", y=dist_col, color="Year",
            line_group="Year", pattern_shape_sequence=[""],
            color_discrete_sequence=["#10b981", "#3b82f6", "#6366f1"]
        )
        fig_vol.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis_title="Total Distance (KM)",
            xaxis_title="",
            hovermode="x unified"
        )
        st.plotly_chart(fig_vol, use_container_width=True)

# ==========================================
# PAGE 2: INTERACTIVE MAP (UPGRADED)
# ==========================================
elif page == "🌍 Interactive Map":
    st.markdown("<h1 style='color: white; font-weight: 800;'>🌍 Geospatial Running Trails</h1>", unsafe_allow_html=True)
    st.markdown("Every street, training corridor, and race route conquered.")
    st.markdown("---")
    
    # Premium Mapbox Styling configuration
    # To use high-end satellite or custom map styles, you can grab a free Mapbox token later
    st.markdown("💡 *Pro Tip: We can hook this up to Mapbox Studio for stunning custom dark-glow or 3D terrain backgrounds.*")
    
    # Mocking high-density coordinates based on typical Mumbai running routes (Marine Drive, Bandra, etc.)
    mock_coordinates = pd.DataFrame({
        'lat': [18.944, 18.955, 18.931, 19.056, 19.068],
        'lon': [72.822, 72.815, 72.834, 72.825, 72.831],
        'size': [20, 10, 15, 30, 25]
    })
    
    fig_map = px.scatter_mapbox(
        mock_coordinates, lat="lat", lon="lon", size="size",
        color_discrete_sequence=["#10b981"], zoom=11, height=600
    )
    fig_map.update_layout(
        mapbox_style="carto-darkmatter", # Premium clean dark base map
        margin={"r":0,"t":0,"l":0,"b":0},
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_map, use_container_width=True)

# ==========================================
# PAGE 3: RACE WALL & MEMORY GALLERY
# ==========================================
elif page == "🖼️ Race Wall & Memory Gallery":
    st.markdown("<h1 style='color: white; font-weight: 800;'>🖼️ The Race Wall & Journey Chronicles</h1>", unsafe_allow_html=True)
    st.markdown("Where raw metrics meet real-world sweat and medals. Your visual running legacy.")
    st.markdown("---")
    
    # Setting up a clean responsive 3-column photo grid
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="photo-card">', unsafe_allow_html=True)
        # Placeholder image - you can replace these URLs with your actual Cloudinary/Supabase image links
        st.image("https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?auto=format&fit=crop&w=500&q=80", use_container_width=True)
        st.markdown('<div class="photo-caption"><b>🏆 Milestone Marathon Finish</b><br>Pushed through the wall at KM 35. Official Time: 04:12:15. Feel the legacy.</div></div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="photo-card">', unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1502224562085-639556652f33?auto=format&fit=crop&w=500&q=80", use_container_width=True)
        st.markdown('<div class="photo-caption"><b>🏃‍♂️ Early Morning Speedwork</b><br>Rainy intervals. Pacing steady at 4:45/km. Consistency beats talent every single day.</div></div>', unsafe_allow_html=True)
        
    with col3:
        st.markdown('<div class="photo-card">', unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1486218119243-13883505764c?auto=format&fit=crop&w=500&q=80", use_container_width=True)
        st.markdown('<div class="photo-caption"><b>🥇 The Medal Rack</b><br>Two years of discipline hanging on a single wall. The journey doesn\'t end here.</div></div>', unsafe_allow_html=True)

    # Simple workflow instruction for adding images
    st.markdown("---")
    st.markdown("### 📸 How to add your own photos to this page:")
    st.markdown("""
    1. Upload your running images to a free cloud host like **Cloudinary.com** or **Supabase**.
    2. Copy the direct image URL link they give you.
    3. Update the `st.image("YOUR_LINK_HERE")` parts in your GitHub code. 
    """)
