import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# ============================================================
# RUNNING JOURNEY // METRIC ENGINE
# Stadium-dark aesthetic preserved; data engine rebuilt on the
# full Strava export (pace, cadence-spm, training load, etc.)
# ============================================================
st.set_page_config(page_title="RUNNING JOURNEY // METRIC ENGINE", layout="wide")

# ---- DESIGN TOKENS (unchanged identity) --------------------
LIME = "#ccff00"; CYAN = "#00f0ff"; RED = "#ff4757"
INK = "#0b0e14"; CARD = "#121721"; LINE = "#1e293b"; MUTE = "#64748b"
YEAR_COLORS = {"2022": "#475569", "2023": "#334155", "2024": CYAN, "2025": RED, "2026": LIME}
CADENCE_TARGET = 174  # spm goal

st.markdown("""
<style>
.stApp { background-color: #0b0e14 !important; color: #e2e8f0 !important;
    font-family: 'Inter', system-ui, sans-serif !important; }
html, body, [data-testid="stMarkdownContainer"] p, p, label, .stSelectbox div { color: #94a3b8 !important; }
h1,h2,h3,h4,h5,h6,strong { color:#fff !important; text-transform:uppercase !important; letter-spacing:1.5px !important; }
div[data-testid="stTabs"] button { font-size:1.05rem !important; font-weight:800 !important; text-transform:uppercase !important;
    letter-spacing:1.2px !important; color:#64748b !important; padding:14px 22px !important; border-bottom:2px solid #1e293b !important; transition:all .3s ease !important; }
div[data-testid="stTabs"] button[aria-selected="true"] { color:#ccff00 !important; border-bottom:3px solid #ccff00 !important; background-color:#121721 !important; }
div[data-testid="stTabs"] button:hover { color:#fff !important; border-bottom-color:#00f0ff !important; }
.ticker-wrap { background:#000; padding:14px; border-radius:4px; margin-bottom:30px; border-left:4px solid #ccff00; box-shadow:0 4px 20px rgba(0,0,0,.5); }
.kpi-container { display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:18px; margin-bottom:30px; }
.kpi-card { background:#121721; padding:22px; border-radius:6px; border:1px solid #1e293b; border-bottom:3px solid #1e293b; }
.kpi-card.accent { border-bottom-color:#ccff00; }
.kpi-value { font-size:2.2rem; font-weight:900; color:#fff !important; line-height:1; font-family:monospace; }
.kpi-label { font-size:.72rem; color:#ccff00 !important; text-transform:uppercase; letter-spacing:1.5px; margin-top:8px; font-weight:700; }
.kpi-sub { font-size:.7rem; color:#64748b !important; font-family:monospace; margin-top:4px; }
.chart-container-box { background:#121721 !important; border:1px solid #1e293b !important; border-radius:8px !important; padding:22px !important; margin-bottom:22px !important; }
.pb-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(210px,1fr)); gap:18px; margin-bottom:26px; }
.pb-card { background:linear-gradient(160deg,#161d2a,#0f1420); border:1px solid #1e293b; border-radius:8px; padding:22px; border-top:3px solid #ccff00; }
.pb-dist { font-size:.75rem; color:#ccff00; font-weight:800; letter-spacing:2px; font-family:monospace; }
.pb-time { font-size:2.3rem; font-weight:900; color:#fff; font-family:monospace; line-height:1.05; margin-top:6px; }
.pb-meta { font-size:.72rem; color:#64748b; font-family:monospace; margin-top:8px; }
.race-row { padding:16px 22px; border-radius:6px; margin-bottom:12px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:14px; }
.flashcard-row-base { border:1px solid #1e293b; border-radius:6px; padding:14px 22px; margin-bottom:10px; display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:15px; }
.flashcard-metrics-group { display:flex; align-items:center; gap:26px; flex-wrap:wrap; }
.flashcard-metric { text-align:center; min-width:64px; }
.flashcard-metric-val { font-size:1.05rem; font-weight:800; color:#fff; font-family:monospace; }
.flashcard-metric-lbl { font-size:.62rem; color:#64748b; text-transform:uppercase; letter-spacing:.5px; margin-top:2px; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# DATA ENGINE
# ============================================================
RACE_REGISTRY = {
    "2023-01-15": {"name": "Tata Mumbai Marathon 5.9K", "bib": "81094", "note": ""},
    "2023-02-12": {"name": "Thane Half Marathon", "bib": "21559", "note": ""},
    "2023-11-19": {"name": "Indian Navy 10K", "bib": "12114", "note": ""},
    "2024-01-21": {"name": "Tata Mumbai Marathon 21K", "bib": "26504", "note": ""},
    "2024-04-28": {"name": "TCS World 10K Bengaluru", "bib": "3970", "note": ""},
    "2024-10-20": {"name": "Vedanta Delhi Half Marathon", "bib": "3258", "note": ""},
    "2024-12-08": {"name": "Indian Navy 21K", "bib": "23781", "note": ""},
    "2024-12-15": {"name": "Tata Steel World 25k Kolkata", "bib": "4653", "note": ""},
    "2025-09-21": {"name": "Berlin Full Marathon", "bib": "76975", "note": ""},
    "2025-10-12": {"name": "Vedanta Delhi Half Marathon", "bib": "5654", "note": ""},
    "2025-12-21": {"name": "Tata Steel World 25k Kolkata", "bib": "4895", "note": ""},
    "2026-01-18": {"name": "Tata Mumbai Full Marathon", "bib": "11435", "note": ""},
    "2026-04-26": {"name": "TCS World 10K Bengaluru", "bib": "32357", "note": "PROCAM SLAM COMPLETED"},
}

DATA_CANDIDATES = ["activities.csv", "Activities.csv", "data/activities.csv"]

def hms_to_label(sec):
    if pd.isna(sec): return "--"
    sec = int(sec); h = sec//3600; m = (sec%3600)//60
    return f"{h}h {m:02d}m" if h else f"{m}m"

@st.cache_data
def load_data():
    path = next((p for p in DATA_CANDIDATES if os.path.exists(p)), None)
    if path is None:
        return None
    df = pd.read_csv(path)
    df["Date_Parsed"] = pd.to_datetime(df["date"])
    # robust numeric coercion (cleaned cells can be blank)
    for c in ["distance_km","moving_time_s","pace_min_per_km","cadence_spm","relative_effort",
              "fatigue_atl","fitness_ctl","form","elevation_gain_m","calories","kudos","hour"]:
        if c in df.columns: df[c] = pd.to_numeric(df[c], errors="coerce")

    def segment_run(km):
        if km >= 42.0: return "Full Marathon"
        elif km >= 21.2: return "Between Half and Full"
        elif km >= 21.0: return "Half Marathon"
        elif km > 10.5: return "Between 10K and 21K"
        elif km >= 9.8: return "10K Runs"
        else: return "Less than 10K"
    df["Category_Custom"] = df["distance_km"].apply(segment_run)

    ds = df["Date_Parsed"].dt.strftime("%Y-%m-%d")
    df["Race_Tag"]  = ds.map(lambda x: RACE_REGISTRY.get(x, {}).get("name"))
    df["Race_Bib"]  = ds.map(lambda x: RACE_REGISTRY.get(x, {}).get("bib"))
    df["Race_Note"] = ds.map(lambda x: RACE_REGISTRY.get(x, {}).get("note"))
    df["weekday"] = df.get("weekday", df["Date_Parsed"].dt.strftime("%a"))

    # ---- merge Garmin FIT metrics (HR, training effect, running dynamics) ----
    fit_path = next((p for p in ["fit_metrics.csv", "data/fit_metrics.csv"] if os.path.exists(p)), None)
    fit_cols = ["avg_hr","max_hr","cadence_spm_fit","aerobic_te","anaerobic_te",
                "gct_ms","vert_osc_mm","vert_ratio","step_len_m"]
    if fit_path:
        fit = pd.read_csv(fit_path)
        keep = ["join_local"] + [c for c in fit_cols if c in fit.columns]
        fit = fit[keep].drop_duplicates("join_local")
        df["join_local"] = df["datetime"].astype(str).str.replace("T", " ").str[:16]
        df = df.merge(fit, on="join_local", how="left")
        for c in fit_cols:
            if c in df.columns: df[c] = pd.to_numeric(df[c], errors="coerce")
    else:
        for c in fit_cols: df[c] = pd.NA
    df["has_hr"] = df["avg_hr"].notna() if "avg_hr" in df.columns else False
    return df

def best_effort(runs, lo, hi):
    """Fastest (min moving_time) run within a distance band."""
    b = runs[(runs["distance_km"] >= lo) & (runs["distance_km"] <= hi) & (runs["moving_time_s"] > 0)]
    if b.empty: return None
    return b.loc[b["moving_time_s"].idxmin()]

PB_BANDS = [("5K",4.9,5.3),("10K",9.7,10.6),("HALF",20.9,21.6),("FULL",41.9,43.5)]

CHART = dict(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
             margin=dict(l=10,r=10,t=20,b=10), font=dict(family="Inter, sans-serif", size=12, color="#94a3b8"),
             showlegend=False)

def grid(fig):
    fig.update_layout(**CHART)
    fig.update_xaxes(showgrid=False, title_text="")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(30,41,59,.45)", zeroline=False, title_text="")
    return fig


df = load_data()
HRMAX = int(df["max_hr"].max()) if ("max_hr" in df.columns and df["max_hr"].notna().any()) else 190

# ---- HEADER ------------------------------------------------
st.markdown("<h1 style='color:#fff;font-size:2.8rem;font-weight:900;margin-bottom:0;'>RUNNING JOURNEY</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#ccff00 !important;font-weight:700;letter-spacing:1px;margin-top:5px;'>ENDURANCE ARCHIVE // PERFORMANCE LOG</p>", unsafe_allow_html=True)
st.markdown("<hr style='border-color:#1e293b;margin:15px 0 25px;'>", unsafe_allow_html=True)

if df is None:
    st.error("No data file found. Add `activities.csv` to the repo root and redeploy.")
    st.stop()

# ---- CONTROL CENTER ---------------------------------------
st.markdown("### CONTROL CENTER")
c1, c2, c3 = st.columns(3)
with c1:
    years = ["ALL TIME"] + [str(y) for y in sorted(df["year"].unique(), reverse=True)]
    sel_year = st.selectbox("YEAR:", years)
with c2:
    cats = ["ALL CATEGORIES","Full Marathon","Between Half and Full","Half Marathon","Between 10K and 21K","10K Runs","Less than 10K"]
    sel_cat = st.selectbox("DISTANCE:", cats)
with c3:
    sports = ["RUNS ONLY","ALL ACTIVITIES"]
    sel_sport = st.selectbox("ACTIVITY TYPE:", sports)

f = df.copy()
if sel_sport == "RUNS ONLY":
    f = f[f["sport_type"] == "Run"]
if sel_year != "ALL TIME":
    f = f[f["year"] == int(sel_year)]
if sel_cat != "ALL CATEGORIES":
    f = f[f["Category_Custom"] == sel_cat]
runs_f = f[f["sport_type"] == "Run"].copy()        # analytics base
runs_all = df[df["sport_type"] == "Run"].copy()     # all-time, for records

st.markdown("<br>", unsafe_allow_html=True)

# ---- STADIUM TICKER (now computed from data) --------------
tick = []
labels = {"5K":"5K","10K":"10K","HALF":"HALF MARATHON","FULL":"FULL MARATHON"}
for key, lo, hi in PB_BANDS:
    r = best_effort(runs_all, lo, hi)
    if r is not None:
        tick.append(f"PR {labels[key]}: {r['moving_time_hms']} @ {r['pace_str']}/KM ({r['Date_Parsed'].strftime('%b %Y')})")
if tick:
    txt = " &nbsp;&nbsp; // &nbsp;&nbsp; ".join(tick)
    st.markdown(f"""<div class="ticker-wrap"><marquee behavior="scroll" direction="left" scrollamount="6"
      style="color:#ccff00;font-weight:800;font-family:monospace;font-size:1.05rem;">ALL-TIME RECORD BENCHMARKS &nbsp;&nbsp; // &nbsp;&nbsp; {txt}</marquee></div>""", unsafe_allow_html=True)

# ============================================================
# NAVIGATION
# ============================================================
t_over, t_trend, t_heart, t_dyn, t_rec, t_pat, t_feed = st.tabs(
    ["Overview", "Trends", "Heart", "Dynamics", "Records", "Patterns", "Activity Feed"])

# ----------------------------- OVERVIEW ---------------------
with t_over:
    tot_km = runs_f["distance_km"].sum()
    n = len(runs_f)
    tot_time = runs_f["moving_time_s"].sum()
    elev = runs_f["elevation_gain_m"].sum()
    avg_pace = runs_f["pace_min_per_km"].mean()
    pace_lbl = f"{int(avg_pace)}:{int(round((avg_pace-int(avg_pace))*60)):02d}" if pd.notna(avg_pace) else "--"
    st.markdown(f"""<div class="kpi-container">
      <div class="kpi-card accent"><div class="kpi-value">{tot_km:,.0f}<span style='font-size:1rem;'> KM</span></div><div class="kpi-label">// TOTAL DISTANCE</div><div class="kpi-sub">runs only</div></div>
      <div class="kpi-card"><div class="kpi-value">{n}</div><div class="kpi-label">// RUNS LOGGED</div></div>
      <div class="kpi-card"><div class="kpi-value">{hms_to_label(tot_time)}</div><div class="kpi-label">// TIME ON FEET</div></div>
      <div class="kpi-card"><div class="kpi-value">{elev:,.0f}<span style='font-size:1rem;'> M</span></div><div class="kpi-label">// ELEVATION GAIN</div></div>
      <div class="kpi-card"><div class="kpi-value">{pace_lbl}</div><div class="kpi-label">// AVG PACE /KM</div></div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="chart-container-box"><h3>Volume By Year</h3>', unsafe_allow_html=True)
        yoy = runs_f.groupby("year")["distance_km"].sum().reset_index(); yoy["year"] = yoy["year"].astype(str)
        fig = px.bar(yoy, x="year", y="distance_km", text_auto=".0f", color="year", color_discrete_map=YEAR_COLORS)
        st.plotly_chart(grid(fig), use_container_width=True); st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="chart-container-box"><h3>Distance Mix</h3>', unsafe_allow_html=True)
        freq = runs_f["Category_Custom"].value_counts().reset_index()
        freq.columns = ["Category_Custom","count"]
        fig = px.bar(freq, x="count", y="Category_Custom", orientation="h", text_auto=".0f")
        fig.update_traces(marker_color=LIME)
        fig = grid(fig); fig.update_yaxes(showgrid=False)
        st.plotly_chart(fig, use_container_width=True); st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="chart-container-box"><h3>Cumulative Distance</h3>', unsafe_allow_html=True)
    cum = runs_f.sort_values("Date_Parsed").copy()
    cum["cum"] = cum["distance_km"].cumsum()
    fig = go.Figure(go.Scatter(x=cum["Date_Parsed"], y=cum["cum"], mode="lines",
                    line=dict(color=LIME, width=2), fill="tozeroy", fillcolor="rgba(204,255,0,.08)"))
    st.plotly_chart(grid(fig), use_container_width=True); st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------- TRENDS -----------------------
with t_trend:
    # Weekly mileage
    st.markdown('<div class="chart-container-box"><h3>Weekly Mileage</h3>', unsafe_allow_html=True)
    wk = runs_f.set_index("Date_Parsed")["distance_km"].resample("W-MON").sum().reset_index()
    if sel_year == "ALL TIME": wk = wk.tail(52)
    fig = px.bar(wk, x="Date_Parsed", y="distance_km")
    fig.update_traces(marker_color=CYAN)
    st.plotly_chart(grid(fig), use_container_width=True); st.markdown("</div>", unsafe_allow_html=True)

    colA, colB = st.columns(2)
    with colA:
        st.markdown('<div class="chart-container-box"><h3>Pace Trend</h3>', unsafe_allow_html=True)
        p = runs_f[(runs_f["pace_min_per_km"].notna()) & (runs_f["distance_km"] >= 3)].sort_values("Date_Parsed")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=p["Date_Parsed"], y=p["pace_min_per_km"], mode="markers",
                       marker=dict(color=MUTE, size=5), name="run"))
        fig.add_trace(go.Scatter(x=p["Date_Parsed"], y=p["pace_min_per_km"].rolling(10, min_periods=3).mean(),
                       mode="lines", line=dict(color=LIME, width=2.5), name="trend"))
        fig = grid(fig); fig.update_yaxes(autorange="reversed", title_text="min/km (faster = up)")
        st.plotly_chart(fig, use_container_width=True); st.markdown("</div>", unsafe_allow_html=True)
    with colB:
        st.markdown('<div class="chart-container-box"><h3>Cadence Trend</h3>', unsafe_allow_html=True)
        cc = runs_f[(runs_f["cadence_spm"].notna()) & (runs_f["cadence_spm"] > 120)].sort_values("Date_Parsed")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=cc["Date_Parsed"], y=cc["cadence_spm"], mode="markers",
                       marker=dict(color=MUTE, size=5)))
        fig.add_trace(go.Scatter(x=cc["Date_Parsed"], y=cc["cadence_spm"].rolling(10, min_periods=3).mean(),
                       mode="lines", line=dict(color=CYAN, width=2.5)))
        fig.add_hline(y=CADENCE_TARGET, line_dash="dash", line_color=RED,
                      annotation_text=f"TARGET {CADENCE_TARGET} SPM", annotation_font_color=RED)
        fig = grid(fig); fig.update_yaxes(title_text="spm")
        st.plotly_chart(fig, use_container_width=True); st.markdown("</div>", unsafe_allow_html=True)

    # Training load model (CTL / ATL / Form)
    st.markdown('<div class="chart-container-box"><h3>Fitness · Fatigue · Form</h3>'
                '<p style="color:#64748b;font-size:.78rem;letter-spacing:0;text-transform:none;margin-top:-6px;">'
                'EWMA model of Strava relative effort — fitness (42-day), fatigue (7-day), form = fitness − fatigue.</p>', unsafe_allow_html=True)
    tl = runs_f.sort_values("Date_Parsed")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=tl["Date_Parsed"], y=tl["fitness_ctl"], mode="lines",
                  line=dict(color=CYAN, width=2), name="Fitness", fill="tozeroy", fillcolor="rgba(0,240,255,.06)"))
    fig.add_trace(go.Scatter(x=tl["Date_Parsed"], y=tl["fatigue_atl"], mode="lines",
                  line=dict(color=RED, width=1.8), name="Fatigue"))
    fig.add_trace(go.Scatter(x=tl["Date_Parsed"], y=tl["form"], mode="lines",
                  line=dict(color=LIME, width=1.5, dash="dot"), name="Form"))
    fig = grid(fig); fig.update_layout(showlegend=True, legend=dict(orientation="h", y=1.12, font=dict(color=MUTE)))
    st.plotly_chart(fig, use_container_width=True); st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------- HEART ------------------------
with t_heart:
    h = runs_f[runs_f["avg_hr"].notna()].sort_values("Date_Parsed") if "avg_hr" in runs_f.columns else runs_f.iloc[0:0]
    if h.empty:
        st.markdown('<p style="color:#64748b;">No heart-rate data in this filter. Commit <code>fit_metrics.csv</code> to the repo to unlock HR analytics.</p>', unsafe_allow_html=True)
    else:
        avg_hr = h["avg_hr"].mean()
        te = h["aerobic_te"].mean() if h["aerobic_te"].notna().any() else float("nan")
        # metres per heartbeat: distance / total beats (higher = more aerobically efficient)
        h = h.copy()
        h["m_per_beat"] = (h["distance_km"]*1000) / (h["avg_hr"] * (h["moving_time_s"]/60.0))
        eff_now = h.sort_values("Date_Parsed")["m_per_beat"].tail(10).mean()
        st.markdown(f"""<div class="kpi-container">
          <div class="kpi-card accent"><div class="kpi-value">{avg_hr:.0f}<span style='font-size:1rem;'> BPM</span></div><div class="kpi-label">// AVG HEART RATE</div><div class="kpi-sub">{int(h['avg_hr'].count())} runs w/ HR</div></div>
          <div class="kpi-card"><div class="kpi-value">{HRMAX}<span style='font-size:1rem;'> BPM</span></div><div class="kpi-label">// MAX HR RECORDED</div></div>
          <div class="kpi-card"><div class="kpi-value">{te:.1f}</div><div class="kpi-label">// AVG AEROBIC TE</div></div>
          <div class="kpi-card"><div class="kpi-value">{eff_now:.2f}<span style='font-size:1rem;'> M/BEAT</span></div><div class="kpi-label">// RECENT EFFICIENCY</div></div>
        </div>""", unsafe_allow_html=True)

        cH1, cH2 = st.columns(2)
        with cH1:
            st.markdown('<div class="chart-container-box"><h3>Heart Rate Trend</h3>', unsafe_allow_html=True)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=h["Date_Parsed"], y=h["max_hr"], mode="markers", marker=dict(color="#3a2230", size=4), name="max"))
            fig.add_trace(go.Scatter(x=h["Date_Parsed"], y=h["avg_hr"], mode="markers", marker=dict(color=MUTE, size=5), name="avg"))
            fig.add_trace(go.Scatter(x=h["Date_Parsed"], y=h["avg_hr"].rolling(10, min_periods=3).mean(), mode="lines", line=dict(color=RED, width=2.5), name="avg trend"))
            st.plotly_chart(grid(fig), use_container_width=True); st.markdown("</div>", unsafe_allow_html=True)
        with cH2:
            st.markdown('<div class="chart-container-box"><h3>Aerobic Efficiency</h3>'
                        '<p style="color:#64748b;font-size:.78rem;letter-spacing:0;text-transform:none;margin-top:-6px;">Metres per heartbeat on runs \u2265 5 km. Rising = same pace at lower effort.</p>', unsafe_allow_html=True)
            e = h[h["distance_km"] >= 5]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=e["Date_Parsed"], y=e["m_per_beat"], mode="markers", marker=dict(color=MUTE, size=5)))
            fig.add_trace(go.Scatter(x=e["Date_Parsed"], y=e["m_per_beat"].rolling(8, min_periods=3).mean(), mode="lines", line=dict(color=LIME, width=2.5)))
            st.plotly_chart(grid(fig), use_container_width=True); st.markdown("</div>", unsafe_allow_html=True)

        cH3, cH4 = st.columns(2)
        with cH3:
            st.markdown('<div class="chart-container-box"><h3>Intensity Mix</h3>'
                        f'<p style="color:#64748b;font-size:.78rem;letter-spacing:0;text-transform:none;margin-top:-6px;">Runs grouped by average HR as % of max ({HRMAX} bpm).</p>', unsafe_allow_html=True)
            pct = h["avg_hr"]/HRMAX*100
            bins = [0,60,70,80,90,200]; labels = ["Z1 Recovery","Z2 Easy","Z3 Aerobic","Z4 Threshold","Z5 Max"]
            zc = pd.cut(pct, bins=bins, labels=labels).value_counts().reindex(labels).fillna(0).reset_index()
            zc.columns = ["zone","runs"]
            fig = px.bar(zc, x="zone", y="runs", text_auto=".0f",
                         color="zone", color_discrete_sequence=["#334155","#00f0ff","#34e5c4","#ffb020","#ff4757"])
            st.plotly_chart(grid(fig), use_container_width=True); st.markdown("</div>", unsafe_allow_html=True)
        with cH4:
            st.markdown('<div class="chart-container-box"><h3>Pace vs Heart Rate</h3>', unsafe_allow_html=True)
            sc = h[h["pace_min_per_km"].notna()]
            fig = px.scatter(sc, x="avg_hr", y="pace_min_per_km", color="year",
                             color_discrete_map=YEAR_COLORS, hover_data=["name"])
            fig = grid(fig); fig.update_yaxes(autorange="reversed", title_text="pace min/km")
            fig.update_xaxes(title_text="avg HR")
            fig.update_layout(showlegend=True, legend=dict(font=dict(color=MUTE)))
            st.plotly_chart(fig, use_container_width=True); st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------- DYNAMICS ---------------------
with t_dyn:
    d = runs_f[runs_f["cadence_spm_fit"].notna()].sort_values("Date_Parsed") if "cadence_spm_fit" in runs_f.columns else runs_f.iloc[0:0]
    if d.empty:
        st.markdown('<p style="color:#64748b;">No running-dynamics data in this filter. These come from the FIT files (HRM-Pro / Run pod).</p>', unsafe_allow_html=True)
    else:
        def dyn_chart(col, title, sub, color, target=None):
            st.markdown(f'<div class="chart-container-box"><h3>{title}</h3>'
                        f'<p style="color:#64748b;font-size:.78rem;letter-spacing:0;text-transform:none;margin-top:-6px;">{sub}</p>', unsafe_allow_html=True)
            s = d[d[col].notna()]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=s["Date_Parsed"], y=s[col], mode="markers", marker=dict(color=MUTE, size=4)))
            fig.add_trace(go.Scatter(x=s["Date_Parsed"], y=s[col].rolling(10, min_periods=3).mean(), mode="lines", line=dict(color=color, width=2.5)))
            if target is not None:
                fig.add_hline(y=target, line_dash="dash", line_color=RED)
            st.plotly_chart(grid(fig), use_container_width=True); st.markdown("</div>", unsafe_allow_html=True)
        cD1, cD2 = st.columns(2)
        with cD1: dyn_chart("cadence_spm_fit", "Cadence (FIT)", f"Steps per minute \u2014 target {CADENCE_TARGET} spm.", CYAN, CADENCE_TARGET)
        with cD2: dyn_chart("gct_ms", "Ground Contact Time", "Milliseconds on the ground per step. Lower is generally better.", LIME)
        cD3, cD4 = st.columns(2)
        with cD3: dyn_chart("vert_osc_mm", "Vertical Oscillation", "Vertical bounce in mm. Lower = less wasted motion.", LIME)
        with cD4: dyn_chart("step_len_m", "Stride Length", "Metres per step.", CYAN)
        dyn_chart("vert_ratio", "Vertical Ratio", "Bounce as a percentage of stride length \u2014 a key efficiency measure. Lower is better.", LIME)

# ----------------------------- RECORDS ----------------------
with t_rec:
    st.markdown("<h3>Personal Bests</h3>", unsafe_allow_html=True)
    cards = ""
    for key, lo, hi in PB_BANDS:
        r = best_effort(runs_all, lo, hi)
        if r is None: continue
        cards += f"""<div class="pb-card"><div class="pb-dist">{key}</div>
          <div class="pb-time">{r['moving_time_hms']}</div>
          <div class="pb-meta">{r['pace_str']} /km<br>{r['Date_Parsed'].strftime('%d %b %Y')}<br>{r['distance_km']:.2f} km recorded</div></div>"""
    st.markdown(f'<div class="pb-grid">{cards}</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748b;font-size:.75rem;">Fastest recorded activity in each distance band (whole-run time, not in-race split).</p>', unsafe_allow_html=True)

    st.markdown('<div class="chart-container-box"><h3>Official Race Registry</h3>', unsafe_allow_html=True)
    # dates that are all-time PRs for a standard distance band -> auto PR badge
    pr_dates = set()
    for _key, lo, hi in PB_BANDS:
        pr = best_effort(runs_all, lo, hi)
        if pr is not None: pr_dates.add(pr["Date_Parsed"].date())
    # one card per race date (keep the longest activity if a day has duplicates)
    races = f[f["Race_Tag"].notna()].copy()
    races["_d"] = races["Date_Parsed"].dt.date
    races = (races.sort_values("distance_km", ascending=False)
                  .drop_duplicates("_d").sort_values("Date_Parsed", ascending=False))
    if races.empty:
        st.markdown('<p style="color:#64748b;">No registered races in this filter.</p>', unsafe_allow_html=True)
    for _, r in races.iterrows():
        full = r["Category_Custom"] == "Full Marathon"
        accent = RED if full else LIME
        chips = ""
        if r["Date_Parsed"].date() in pr_dates:
            chips += "<span style='background:#ccff00;color:#0b0e14;font-family:monospace;font-size:.62rem;font-weight:900;padding:2px 7px;border-radius:3px;letter-spacing:1px;margin-right:6px;'>PR</span>"
        if r["Race_Note"]:
            chips += f"<span style='color:{accent};font-family:monospace;font-size:.7rem;font-weight:800;'>{r['Race_Note']}</span>"
        note = f"<div style='margin-top:4px;'>{chips}</div>" if chips else ""
        st.markdown(f"""<div class="race-row" style="background:{'#1a1215' if full else '#161d2a'};border-left:4px solid {accent};">
          <div><div style="color:#fff;font-weight:800;font-size:1.12rem;">{r['Race_Tag']}</div>
          <div style="color:#64748b;font-size:.74rem;font-family:monospace;">{r['Date_Parsed'].strftime('%B %d, %Y')} &nbsp;·&nbsp; BIB {r['Race_Bib']}</div>{note}</div>
          <div class="flashcard-metrics-group">
            <div class="flashcard-metric"><div class="flashcard-metric-val">{r['distance_km']:.2f}</div><div class="flashcard-metric-lbl">km</div></div>
            <div class="flashcard-metric"><div class="flashcard-metric-val">{r['moving_time_hms']}</div><div class="flashcard-metric-lbl">time</div></div>
            <div class="flashcard-metric"><div class="flashcard-metric-val">{r['pace_str']}</div><div class="flashcard-metric-lbl">/km</div></div>
          </div></div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------- PATTERNS ---------------------
with t_pat:
    # consistency KPIs
    rdates = pd.to_datetime(runs_all["date"]).dt.date.sort_values().unique()
    longest = cur = 1 if len(rdates) else 0
    for i in range(1, len(rdates)):
        cur = cur + 1 if (rdates[i] - rdates[i-1]).days == 1 else 1
        longest = max(longest, cur)
    last30 = sum((pd.Timestamp.now().date() - d).days <= 30 for d in rdates)
    st.markdown(f"""<div class="kpi-container">
      <div class="kpi-card accent"><div class="kpi-value">{len(rdates)}</div><div class="kpi-label">// ACTIVE DAYS</div></div>
      <div class="kpi-card"><div class="kpi-value">{longest}</div><div class="kpi-label">// LONGEST DAY STREAK</div></div>
      <div class="kpi-card"><div class="kpi-value">{last30}</div><div class="kpi-label">// RUNS LAST 30 DAYS</div></div>
    </div>""", unsafe_allow_html=True)

    colC, colD = st.columns(2)
    with colC:
        st.markdown('<div class="chart-container-box"><h3>By Day Of Week</h3>', unsafe_allow_html=True)
        order = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        wd = runs_f.groupby("weekday")["distance_km"].sum().reindex(order).fillna(0).reset_index()
        fig = px.bar(wd, x="weekday", y="distance_km", text_auto=".0f")
        fig.update_traces(marker_color=LIME)
        st.plotly_chart(grid(fig), use_container_width=True); st.markdown("</div>", unsafe_allow_html=True)
    with colD:
        st.markdown('<div class="chart-container-box"><h3>By Hour Of Day</h3>', unsafe_allow_html=True)
        hr = runs_f.groupby("hour").size().reset_index(name="runs")
        fig = px.bar(hr, x="hour", y="runs")
        fig.update_traces(marker_color=CYAN)
        st.plotly_chart(grid(fig), use_container_width=True); st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="chart-container-box"><h3>Monthly Volume Heatmap</h3>', unsafe_allow_html=True)
    hm = runs_f.copy()
    hm["mn"] = hm["Date_Parsed"].dt.month
    piv = hm.pivot_table(index="year", columns="mn", values="distance_km", aggfunc="sum").fillna(0)
    piv = piv.reindex(columns=range(1,13), fill_value=0)
    piv.columns = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    fig = px.imshow(piv, text_auto=".0f", aspect="auto",
                    color_continuous_scale=[[0,"#121721"],[0.5,"#1e6b6b"],[1,LIME]])
    fig.update_layout(**{k:v for k,v in CHART.items() if k!="showlegend"})
    fig.update_coloraxes(showscale=False)
    st.plotly_chart(fig, use_container_width=True); st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------- FEED -------------------------
with t_feed:
    st.markdown("### Activity Feed Log")
    for _, r in f.sort_values("Date_Parsed", ascending=False).head(60).iterrows():
        full = r["Category_Custom"] == "Full Marathon"
        accent = RED if full else CYAN
        cad = f"{r['cadence_spm']:.0f}" if pd.notna(r["cadence_spm"]) else "--"
        eff = f"{r['relative_effort']:.0f}" if pd.notna(r["relative_effort"]) else "--"
        st.markdown(f"""<div class="flashcard-row-base" style="background:{'#1a1215' if full else '#121721'};border-left:4px solid {accent};">
          <div style="min-width:230px;"><div style="color:#fff;font-weight:800;font-size:1.1rem;">{r['name']}</div>
          <div style="color:{accent};font-size:.7rem;letter-spacing:1px;">{r['Category_Custom'].upper()} &nbsp;·&nbsp; {r['Date_Parsed'].strftime('%d %b %Y')}</div></div>
          <div class="flashcard-metrics-group">
            <div class="flashcard-metric"><div class="flashcard-metric-val">{r['distance_km']:.2f}</div><div class="flashcard-metric-lbl">km</div></div>
            <div class="flashcard-metric"><div class="flashcard-metric-val">{r['moving_time_hms']}</div><div class="flashcard-metric-lbl">time</div></div>
            <div class="flashcard-metric"><div class="flashcard-metric-val">{r['pace_str']}</div><div class="flashcard-metric-lbl">/km</div></div>
            <div class="flashcard-metric"><div class="flashcard-metric-val">{cad}</div><div class="flashcard-metric-lbl">spm</div></div>
            <div class="flashcard-metric"><div class="flashcard-metric-val">{eff}</div><div class="flashcard-metric-lbl">effort</div></div>
          </div></div>""", unsafe_allow_html=True)
