import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="RUNNING JOURNEY // METRIC ENGINE", layout="wide",
                   initial_sidebar_state="collapsed")

# ---- DESIGN TOKENS -----------------------------------------
LIME="#ccff00"; CYAN="#00f0ff"; RED="#ff4757"; MINT="#34e5c4"
INK="#0b0e14"; CARD="#121721"; LINE="#1e293b"; MUTE="#64748b"
YEAR_COLORS={"2022":"#475569","2023":"#334155","2024":CYAN,"2025":RED,"2026":LIME}
CADENCE_TARGET=174

st.markdown("""
<style>
.stApp { background:#0b0e14 !important; color:#e2e8f0 !important; font-family:'Inter',system-ui,sans-serif !important; }
html, body, [data-testid="stMarkdownContainer"] p, p, label, .stSelectbox div { color:#94a3b8 !important; }
h1,h2,h3,h4,h5,h6,strong { color:#fff !important; text-transform:uppercase !important; letter-spacing:1.5px !important; }
div[data-testid="stTabs"] div[role="tablist"] { gap:4px; flex-wrap:wrap; }
div[data-testid="stTabs"] button { font-size:1.05rem !important; font-weight:800 !important; text-transform:uppercase !important;
    letter-spacing:1.2px !important; color:#64748b !important; padding:14px 22px !important; border-bottom:2px solid #1e293b !important; }
div[data-testid="stTabs"] button[aria-selected="true"] { color:#ccff00 !important; border-bottom:3px solid #ccff00 !important; background:#121721 !important; }
.ticker-wrap { background:#000; padding:14px; border-radius:4px; margin-bottom:26px; border-left:4px solid #ccff00; box-shadow:0 4px 20px rgba(0,0,0,.5); }
.kpi-container { display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:16px; margin-bottom:26px; }
.kpi-card { background:#121721; padding:20px; border-radius:6px; border:1px solid #1e293b; border-bottom:3px solid #1e293b; }
.kpi-card.accent { border-bottom-color:#ccff00; }
.kpi-value { font-size:2rem; font-weight:900; color:#fff !important; line-height:1; font-family:monospace; }
.kpi-label { font-size:.7rem; color:#ccff00 !important; text-transform:uppercase; letter-spacing:1.5px; margin-top:8px; font-weight:700; }
.kpi-sub { font-size:.68rem; color:#64748b !important; font-family:monospace; margin-top:4px; }
.chart-container-box { background:#121721 !important; border:1px solid #1e293b !important; border-radius:8px !important; padding:20px !important; margin-bottom:20px !important; }
.section-h { color:#fff; font-weight:900; letter-spacing:2px; font-size:1.3rem; margin:8px 0 14px; }
/* timeline */
.timeline { border-left:2px solid #1e293b; margin:6px 0 24px 10px; padding-left:26px; }
.tl-item { position:relative; margin-bottom:24px; }
.tl-item:before { content:''; position:absolute; left:-33px; top:3px; width:13px; height:13px; border-radius:50%; background:#ccff00; box-shadow:0 0 0 5px rgba(204,255,0,.10); }
.tl-item.full:before { background:#ff4757; box-shadow:0 0 0 5px rgba(255,71,87,.12); }
.tl-year { color:#ccff00; font-family:monospace; font-weight:800; font-size:.78rem; letter-spacing:2px; }
.tl-title { color:#fff; font-weight:800; font-size:1.18rem; margin:1px 0 3px; }
.tl-desc { color:#94a3b8; font-size:.86rem; line-height:1.5; }
/* blurb */
.blurb { background:linear-gradient(160deg,#161d2a,#0f1420); border-left:4px solid #ccff00; border-radius:8px;
    padding:24px 26px; margin:4px 0 24px; font-size:1.04rem; line-height:1.75; color:#cbd5e1; font-style:italic; }
.blurb b { color:#fff; font-style:normal; }
/* PB + race */
.pb-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(190px,1fr)); gap:16px; margin-bottom:24px; }
.pb-card { background:linear-gradient(160deg,#161d2a,#0f1420); border:1px solid #1e293b; border-radius:8px; padding:20px; border-top:3px solid #ccff00; }
.pb-dist { font-size:.72rem; color:#ccff00; font-weight:800; letter-spacing:2px; font-family:monospace; }
.pb-time { font-size:2.1rem; font-weight:900; color:#fff; font-family:monospace; line-height:1.05; margin-top:6px; }
.pb-meta { font-size:.7rem; color:#64748b; font-family:monospace; margin-top:8px; }
.race-row { padding:15px 20px; border-radius:6px; margin-bottom:11px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; }
.flashcard-row-base { border:1px solid #1e293b; border-radius:6px; padding:13px 18px; margin-bottom:10px; display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:12px; }
.fm-group { display:flex; align-items:center; gap:22px; flex-wrap:wrap; }
.fm { text-align:center; min-width:58px; }
.fm-val { font-size:1rem; font-weight:800; color:#fff; font-family:monospace; }
.fm-lbl { font-size:.6rem; color:#64748b; text-transform:uppercase; letter-spacing:.5px; margin-top:2px; }
@media (max-width:640px){
  h1 { font-size:2rem !important; }
  div[data-testid="stTabs"] button { font-size:.82rem !important; padding:9px 12px !important; letter-spacing:.6px !important; }
  .kpi-value { font-size:1.7rem; } .pb-time { font-size:1.8rem; }
}
</style>
""", unsafe_allow_html=True)

# ---- static chart rendering (no zoom/pan on touch) ---------
STATIC = {"staticPlot": True, "displayModeBar": False, "responsive": True}
def SHOW(fig, height=320):
    fig.update_layout(height=height)
    st.plotly_chart(fig, use_container_width=True, config=STATIC)

CHART = dict(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
             margin=dict(l=10,r=10,t=20,b=10), font=dict(family="Inter, sans-serif", size=12, color="#94a3b8"),
             showlegend=False)
def grid(fig):
    fig.update_layout(**CHART)
    fig.update_xaxes(showgrid=False, title_text="")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(30,41,59,.45)", zeroline=False, title_text="")
    return fig

# ---- race registry -----------------------------------------
RACE_REGISTRY = {
    "2023-11-19": {"name": "Indian Navy 10K", "bib": "12114", "note": ""},
    "2024-01-21": {"name": "Tata Mumbai Marathon 21K", "bib": "26504", "note": ""},
    "2024-04-28": {"name": "TCS World 10K Bengaluru", "bib": "3970", "note": ""},
    "2024-09-01": {"name": "Satara Hill Half Marathon", "bib": "25051", "note": ""},
    "2024-10-20": {"name": "Vedanta Delhi Half Marathon", "bib": "3258", "note": ""},
    "2024-12-08": {"name": "Indian Navy 21K", "bib": "23781", "note": ""},
    "2024-12-15": {"name": "Tata Steel World 25K Kolkata", "bib": "4653", "note": ""},
    "2025-09-21": {"name": "Berlin Full Marathon", "bib": "76975", "note": ""},
    "2025-10-12": {"name": "Vedanta Delhi Half Marathon", "bib": "5654", "note": ""},
    "2025-12-21": {"name": "Tata Steel World 25K Kolkata", "bib": "4895", "note": ""},
    "2026-01-18": {"name": "Tata Mumbai Full Marathon", "bib": "11435", "note": ""},
    "2026-04-26": {"name": "TCS World 10K Bengaluru", "bib": "32357", "note": "PROCAM SLAM COMPLETED"},
}

# ---- city footprint (home + race cities) -------------------
CITY_CENTROIDS = {
    "Mumbai": (19.05, 72.85), "Delhi": (28.60, 77.21), "Kolkata": (22.57, 88.36),
    "Bengaluru": (12.97, 77.59), "Satara": (17.69, 73.99), "Berlin": (52.51, 13.40),
}
CITY_BY_DATE = {
    "2025-09-20": "Berlin", "2025-09-21": "Berlin",
    "2024-12-15": "Kolkata", "2025-12-21": "Kolkata",
    "2024-10-20": "Delhi", "2025-10-12": "Delhi",
    "2024-04-28": "Bengaluru", "2026-04-26": "Bengaluru",
    "2024-09-01": "Satara",
}
def assign_city(date_str): return CITY_BY_DATE.get(date_str, "Mumbai")

DATA_CANDIDATES = ["activities.csv", "Activities.csv", "data/activities.csv"]

def hms_label(sec):
    if pd.isna(sec): return "--"
    sec=int(sec); h=sec//3600; m=(sec%3600)//60
    return f"{h}h {m:02d}m" if h else f"{m}m"

@st.cache_data(show_spinner=False)
def load_data():
    path = next((p for p in DATA_CANDIDATES if os.path.exists(p)), None)
    if path is None: return None
    df = pd.read_csv(path)
    df["Date_Parsed"] = pd.to_datetime(df["date"])
    for c in ["distance_km","moving_time_s","pace_min_per_km","cadence_spm","relative_effort",
              "fatigue_atl","fitness_ctl","form","elevation_gain_m","calories","kudos","hour"]:
        if c in df.columns: df[c] = pd.to_numeric(df[c], errors="coerce")
    def seg(km):
        if km>=42.0: return "Full Marathon"
        if km>=21.2: return "Between Half and Full"
        if km>=21.0: return "Half Marathon"
        if km>10.5:  return "Between 10K and 21K"
        if km>=9.8:  return "10K Runs"
        return "Less than 10K"
    df["Category_Custom"] = df["distance_km"].apply(seg)
    ds = df["Date_Parsed"].dt.strftime("%Y-%m-%d")
    df["Race_Tag"]=ds.map(lambda x: RACE_REGISTRY.get(x,{}).get("name"))
    df["Race_Bib"]=ds.map(lambda x: RACE_REGISTRY.get(x,{}).get("bib"))
    df["Race_Note"]=ds.map(lambda x: RACE_REGISTRY.get(x,{}).get("note"))
    df["weekday"]=df.get("weekday", df["Date_Parsed"].dt.strftime("%a"))
    df["city"]=ds.map(assign_city)
    # merge FIT metrics
    fit_path=next((p for p in ["fit_metrics.csv","data/fit_metrics.csv"] if os.path.exists(p)), None)
    fitcols=["avg_hr","max_hr","cadence_spm_fit","aerobic_te","anaerobic_te","gct_ms","vert_osc_mm","vert_ratio","step_len_m"]
    if fit_path:
        fit=pd.read_csv(fit_path); keep=["join_local"]+[c for c in fitcols if c in fit.columns]
        fit=fit[keep].drop_duplicates("join_local")
        df["join_local"]=df["datetime"].astype(str).str.replace("T"," ").str[:16]
        df=df.merge(fit,on="join_local",how="left")
        for c in fitcols:
            if c in df.columns: df[c]=pd.to_numeric(df[c],errors="coerce")
    else:
        for c in fitcols: df[c]=np.nan
    return df

def best_effort(runs, lo, hi):
    b=runs[(runs["distance_km"]>=lo)&(runs["distance_km"]<=hi)&(runs["moving_time_s"]>0)]
    return None if b.empty else b.loc[b["moving_time_s"].idxmin()]
PB_BANDS=[("5K",4.9,5.3),("10K",9.7,10.6),("HALF",20.9,21.6),("FULL",41.9,43.5)]

df = load_data()
HRMAX = int(df["max_hr"].max()) if (df is not None and "max_hr" in df.columns and df["max_hr"].notna().any()) else 190

# ---- header ------------------------------------------------
st.markdown("<h1 style='color:#fff;font-size:2.8rem;font-weight:900;margin-bottom:0;'>RUNNING JOURNEY</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#ccff00 !important;font-weight:700;letter-spacing:1px;margin-top:5px;'>ENDURANCE ARCHIVE // PERFORMANCE LOG</p>", unsafe_allow_html=True)
st.markdown("<hr style='border-color:#1e293b;margin:14px 0 22px;'>", unsafe_allow_html=True)

if df is None:
    st.error("No data file found. Add activities.csv to the repo root."); st.stop()

# ---- filters ----------------------------------------------
with st.expander("CONTROL CENTER  //  FILTERS", expanded=False):
    c1,c2,c3 = st.columns(3)
    with c1:
        years=["ALL TIME"]+[str(y) for y in sorted(df["year"].unique(),reverse=True)]
        sel_year=st.selectbox("YEAR", years)
    with c2:
        cats=["ALL CATEGORIES","Full Marathon","Between Half and Full","Half Marathon","Between 10K and 21K","10K Runs","Less than 10K"]
        sel_cat=st.selectbox("DISTANCE", cats)
    with c3:
        sel_sport=st.selectbox("ACTIVITY TYPE", ["RUNS ONLY","ALL ACTIVITIES"])

f=df.copy()
if sel_sport=="RUNS ONLY": f=f[f["sport_type"]=="Run"]
if sel_year!="ALL TIME": f=f[f["year"]==int(sel_year)]
if sel_cat!="ALL CATEGORIES": f=f[f["Category_Custom"]==sel_cat]
runs_f=f[f["sport_type"]=="Run"].copy()
runs_all=df[df["sport_type"]=="Run"].copy()

# ---- ticker (computed PRs) --------------------------------
tick=[]; labmap={"5K":"5K","10K":"10K","HALF":"HALF MARATHON","FULL":"FULL MARATHON"}
for k,lo,hi in PB_BANDS:
    r=best_effort(runs_all,lo,hi)
    if r is not None: tick.append(f"PR {labmap[k]}: {r['moving_time_hms']} @ {r['pace_str']}/KM ({r['Date_Parsed'].strftime('%b %Y')})")
if tick:
    st.markdown(f"""<div class="ticker-wrap"><marquee behavior="scroll" direction="left" scrollamount="6"
      style="color:#ccff00;font-weight:800;font-family:monospace;font-size:1.05rem;">ALL-TIME RECORD BENCHMARKS &nbsp;&nbsp; // &nbsp;&nbsp; {" &nbsp;&nbsp; // &nbsp;&nbsp; ".join(tick)}</marquee></div>""", unsafe_allow_html=True)

t_over, t_data, t_rec, t_log = st.tabs(["Overview", "Data", "Race Registry", "Activity Log"])

# ============================================================ OVERVIEW
with t_over:
    tot=runs_f["distance_km"].sum(); n=len(runs_f); tt=runs_f["moving_time_s"].sum()
    elev=runs_f["elevation_gain_m"].sum(); ap=runs_f["pace_min_per_km"].mean()
    apl=f"{int(ap)}:{int(round((ap-int(ap))*60)):02d}" if pd.notna(ap) else "--"
    st.markdown(f"""<div class="kpi-container">
      <div class="kpi-card accent"><div class="kpi-value">{tot:,.0f}<span style='font-size:.9rem;'> KM</span></div><div class="kpi-label">// DISTANCE</div><div class="kpi-sub">runs only</div></div>
      <div class="kpi-card"><div class="kpi-value">{n}</div><div class="kpi-label">// RUNS</div></div>
      <div class="kpi-card"><div class="kpi-value">{hms_label(tt)}</div><div class="kpi-label">// TIME ON FEET</div></div>
      <div class="kpi-card"><div class="kpi-value">{elev:,.0f}<span style='font-size:.9rem;'> M</span></div><div class="kpi-label">// CLIMBED</div></div>
      <div class="kpi-card"><div class="kpi-value">{apl}</div><div class="kpi-label">// AVG PACE</div></div>
    </div>""", unsafe_allow_html=True)

    # blurb (editable)
    st.markdown("""<div class="blurb">
    I started running in 2022 with no real plan \u2014 just shoes, a road, and the quiet that comes about twenty minutes in.
    What began as a way to clear my head slowly turned into something I build my weeks around. The numbers grew on their own:
    a first long run, then a first half, then a start line in <b>Berlin</b> and one back home in <b>Mumbai</b>.
    A knee injury taught me that consistency beats heroics, and that coming back patiently is its own kind of progress.
    Running is where I keep my discipline honest \u2014 the one part of the day that is fully mine.
    </div>""", unsafe_allow_html=True)

    # running timeline (data-derived stats)
    st.markdown('<div class="section-h">RUNNING TIMELINE</div>', unsafe_allow_html=True)
    yr = runs_all.groupby("year").agg(runs=("distance_km","size"), km=("distance_km","sum"),
                                      longest=("distance_km","max")).round(0)
    def ys(y, key): return int(yr.loc[y, key]) if y in yr.index else 0
    MILE = [
        (2022, False, "Where It Began",
         f"First logged run in May. {ys(2022,'runs')} runs, {ys(2022,'km')} km \u2014 and already a 26 km push by August."),
        (2023, False, "Finding Rhythm",
         f"{ys(2023,'runs')} runs, {ys(2023,'km')} km. The first race bibs start appearing."),
        (2024, False, "The Big Leap",
         f"{ys(2024,'runs')} runs, {ys(2024,'km')} km. Half marathons, the Satara hills, and the Kolkata 25K."),
        (2025, True,  "Berlin \u2014 First Marathon",
         f"{ys(2025,'runs')} runs, {ys(2025,'km')} km. 42.2 km in 4:48:48, plus a 2:01 half-marathon PR."),
        (2026, True,  "Mumbai & The Comeback",
         f"Tata Mumbai Marathon in January \u2014 then rebuilding patiently from a knee injury."),
    ]
    rows="".join(
        f"""<div class="tl-item {'full' if full else ''}"><div class="tl-year">{y}</div>
            <div class="tl-title">{title}</div><div class="tl-desc">{desc}</div></div>"""
        for y,full,title,desc in MILE)
    st.markdown(f'<div class="timeline">{rows}</div>', unsafe_allow_html=True)

    # journey trendline
    st.markdown('<div class="chart-container-box"><h3>The Journey \u2014 Cumulative Distance</h3>', unsafe_allow_html=True)
    cum=runs_all.sort_values("Date_Parsed").copy(); cum["c"]=cum["distance_km"].cumsum()
    fig=go.Figure(go.Scatter(x=cum["Date_Parsed"], y=cum["c"], mode="lines",
                  line=dict(color=LIME,width=2.5), fill="tozeroy", fillcolor="rgba(204,255,0,.08)"))
    SHOW(grid(fig), 300); st.markdown("</div>", unsafe_allow_html=True)

# ============================================================ DATA
with t_data:
    def c_weekly():
        st.markdown('<div class="chart-container-box"><h3>Weekly Mileage</h3>', unsafe_allow_html=True)
        wk=runs_f.set_index("Date_Parsed")["distance_km"].resample("W-MON").sum().reset_index()
        if sel_year=="ALL TIME": wk=wk.tail(52)
        fig=px.bar(wk,x="Date_Parsed",y="distance_km"); fig.update_traces(marker_color=CYAN); SHOW(grid(fig)); st.markdown("</div>",unsafe_allow_html=True)
    def c_pace():
        st.markdown('<div class="chart-container-box"><h3>Pace Trend</h3>', unsafe_allow_html=True)
        p=runs_f[(runs_f["pace_min_per_km"].notna())&(runs_f["distance_km"]>=3)].sort_values("Date_Parsed")
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=p["Date_Parsed"],y=p["pace_min_per_km"],mode="markers",marker=dict(color=MUTE,size=5)))
        fig.add_trace(go.Scatter(x=p["Date_Parsed"],y=p["pace_min_per_km"].rolling(10,min_periods=3).mean(),mode="lines",line=dict(color=LIME,width=2.5)))
        fig=grid(fig); fig.update_yaxes(autorange="reversed", title_text="min/km (faster=up)"); SHOW(fig); st.markdown("</div>",unsafe_allow_html=True)
    def c_cad():
        st.markdown('<div class="chart-container-box"><h3>Cadence Trend</h3>', unsafe_allow_html=True)
        cc=runs_f[(runs_f["cadence_spm"].notna())&(runs_f["cadence_spm"]>120)].sort_values("Date_Parsed")
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=cc["Date_Parsed"],y=cc["cadence_spm"],mode="markers",marker=dict(color=MUTE,size=5)))
        fig.add_trace(go.Scatter(x=cc["Date_Parsed"],y=cc["cadence_spm"].rolling(10,min_periods=3).mean(),mode="lines",line=dict(color=CYAN,width=2.5)))
        fig.add_hline(y=CADENCE_TARGET,line_dash="dash",line_color=RED,annotation_text=f"TARGET {CADENCE_TARGET}",annotation_font_color=RED)
        SHOW(grid(fig)); st.markdown("</div>",unsafe_allow_html=True)
    def c_form():
        st.markdown('<div class="chart-container-box"><h3>Fitness \u00b7 Fatigue \u00b7 Form</h3><p style="color:#64748b;font-size:.78rem;letter-spacing:0;text-transform:none;margin-top:-6px;">EWMA model of relative effort. Fitness 42-day, Fatigue 7-day, Form = the gap.</p>', unsafe_allow_html=True)
        tl=runs_f.sort_values("Date_Parsed")
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=tl["Date_Parsed"],y=tl["fitness_ctl"],mode="lines",line=dict(color=CYAN,width=2),name="Fitness",fill="tozeroy",fillcolor="rgba(0,240,255,.06)"))
        fig.add_trace(go.Scatter(x=tl["Date_Parsed"],y=tl["fatigue_atl"],mode="lines",line=dict(color=RED,width=1.8),name="Fatigue"))
        fig.add_trace(go.Scatter(x=tl["Date_Parsed"],y=tl["form"],mode="lines",line=dict(color=LIME,width=1.5,dash="dot"),name="Form"))
        fig=grid(fig); fig.update_layout(showlegend=True,legend=dict(orientation="h",y=1.15,font=dict(color=MUTE))); SHOW(fig,360); st.markdown("</div>",unsafe_allow_html=True)
    def c_yoy():
        st.markdown('<div class="chart-container-box"><h3>Volume By Year</h3>', unsafe_allow_html=True)
        yoy=runs_f.groupby("year")["distance_km"].sum().reset_index(); yoy["year"]=yoy["year"].astype(str)
        fig=px.bar(yoy,x="year",y="distance_km",text_auto=".0f",color="year",color_discrete_map=YEAR_COLORS); SHOW(grid(fig)); st.markdown("</div>",unsafe_allow_html=True)
    def c_mix():
        st.markdown('<div class="chart-container-box"><h3>Distance Mix</h3>', unsafe_allow_html=True)
        fr=runs_f["Category_Custom"].value_counts().reset_index(); fr.columns=["Category_Custom","count"]
        fig=px.bar(fr,x="count",y="Category_Custom",orientation="h",text_auto=".0f"); fig.update_traces(marker_color=LIME)
        fig=grid(fig); fig.update_yaxes(showgrid=False); SHOW(fig); st.markdown("</div>",unsafe_allow_html=True)
    def c_map():
        st.markdown('<div class="chart-container-box"><h3>Where I\'ve Run</h3><p style="color:#64748b;font-size:.78rem;letter-spacing:0;text-transform:none;margin-top:-6px;">Every run mapped to home base or a race city. Bubble size = total distance there (all-time).</p>', unsafe_allow_html=True)
        cv=runs_all.groupby("city").agg(runs=("distance_km","size"),km=("distance_km","sum")).reset_index()
        cv=cv[cv["city"].isin(CITY_CENTROIDS)]
        cv["lat"]=cv["city"].map(lambda c: CITY_CENTROIDS[c][0]); cv["lon"]=cv["city"].map(lambda c: CITY_CENTROIDS[c][1])
        cv["size"]=12+ (cv["km"]**0.5)*1.6
        cv["label"]=cv.apply(lambda r:f"{r['city']}  \u2022  {int(r['runs'])} runs \u2022 {int(r['km'])} km",axis=1)
        fig=go.Figure(go.Scattergeo(lon=cv["lon"],lat=cv["lat"],text=cv["label"],hoverinfo="text",
            mode="markers", marker=dict(size=cv["size"],color=LIME,opacity=.85,line=dict(width=1,color="#0b0e14"))))
        fig.update_geos(projection_type="natural earth", showland=True, landcolor="#121721",
            showcountries=True, countrycolor="#1e293b", showocean=True, oceancolor="#0b0e14",
            showcoastlines=True, coastlinecolor="#1e293b", bgcolor="rgba(0,0,0,0)", lakecolor="#0b0e14",
            lataxis_range=[5,58], lonaxis_range=[5,95])
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0,r=0,t=0,b=0), height=420)
        st.plotly_chart(fig,use_container_width=True,config=STATIC)
        chips="".join(f"<span style='display:inline-block;background:#161d2a;border:1px solid #1e293b;border-radius:20px;padding:5px 13px;margin:4px 6px 0 0;font-size:.74rem;'><b style='color:#ccff00;'>{r['city']}</b> <span style='color:#64748b;font-family:monospace;'>{int(r['km'])} km</span></span>" for _,r in cv.sort_values('km',ascending=False).iterrows())
        st.markdown(f"<div style='margin-top:10px;'>{chips}</div></div>", unsafe_allow_html=True)
    def c_dow():
        st.markdown('<div class="chart-container-box"><h3>By Day Of Week</h3>', unsafe_allow_html=True)
        order=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        wd=runs_f.groupby("weekday")["distance_km"].sum().reindex(order).fillna(0).reset_index()
        fig=px.bar(wd,x="weekday",y="distance_km",text_auto=".0f"); fig.update_traces(marker_color=LIME); SHOW(grid(fig)); st.markdown("</div>",unsafe_allow_html=True)
    def c_hour():
        st.markdown('<div class="chart-container-box"><h3>By Hour Of Day</h3>', unsafe_allow_html=True)
        hr=runs_f.groupby("hour").size().reset_index(name="runs")
        fig=px.bar(hr,x="hour",y="runs"); fig.update_traces(marker_color=CYAN); SHOW(grid(fig)); st.markdown("</div>",unsafe_allow_html=True)
    def c_heat():
        st.markdown('<div class="chart-container-box"><h3>Monthly Volume Heatmap</h3>', unsafe_allow_html=True)
        hm=runs_f.copy(); hm["mn"]=hm["Date_Parsed"].dt.month
        piv=hm.pivot_table(index="year",columns="mn",values="distance_km",aggfunc="sum").fillna(0).reindex(columns=range(1,13),fill_value=0)
        piv.columns=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        fig=px.imshow(piv,text_auto=".0f",aspect="auto",color_continuous_scale=[[0,"#121721"],[.5,"#1e6b6b"],[1,LIME]])
        fig.update_layout(**{k:v for k,v in CHART.items() if k!="showlegend"}); fig.update_coloraxes(showscale=False); SHOW(fig,300); st.markdown("</div>",unsafe_allow_html=True)
    def c_hrtrend():
        h=runs_f[runs_f["avg_hr"].notna()].sort_values("Date_Parsed")
        if h.empty: st.info("No HR data in this filter."); return
        st.markdown('<div class="chart-container-box"><h3>Heart Rate Trend</h3>', unsafe_allow_html=True)
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=h["Date_Parsed"],y=h["max_hr"],mode="markers",marker=dict(color="#3a2230",size=4)))
        fig.add_trace(go.Scatter(x=h["Date_Parsed"],y=h["avg_hr"],mode="markers",marker=dict(color=MUTE,size=5)))
        fig.add_trace(go.Scatter(x=h["Date_Parsed"],y=h["avg_hr"].rolling(10,min_periods=3).mean(),mode="lines",line=dict(color=RED,width=2.5)))
        SHOW(grid(fig)); st.markdown("</div>",unsafe_allow_html=True)
    def c_eff():
        h=runs_f[runs_f["avg_hr"].notna()].copy()
        if h.empty: st.info("No HR data in this filter."); return
        h["mpb"]=(h["distance_km"]*1000)/(h["avg_hr"]*(h["moving_time_s"]/60.0)); e=h[h["distance_km"]>=5].sort_values("Date_Parsed")
        st.markdown('<div class="chart-container-box"><h3>Aerobic Efficiency</h3><p style="color:#64748b;font-size:.78rem;letter-spacing:0;text-transform:none;margin-top:-6px;">Metres per heartbeat on 5 km+ runs. Rising = same pace at lower effort.</p>', unsafe_allow_html=True)
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=e["Date_Parsed"],y=e["mpb"],mode="markers",marker=dict(color=MUTE,size=5)))
        fig.add_trace(go.Scatter(x=e["Date_Parsed"],y=e["mpb"].rolling(8,min_periods=3).mean(),mode="lines",line=dict(color=LIME,width=2.5)))
        SHOW(grid(fig)); st.markdown("</div>",unsafe_allow_html=True)
    def c_intensity():
        h=runs_f[runs_f["avg_hr"].notna()]
        if h.empty: st.info("No HR data in this filter."); return
        st.markdown(f'<div class="chart-container-box"><h3>Intensity Mix</h3><p style="color:#64748b;font-size:.78rem;letter-spacing:0;text-transform:none;margin-top:-6px;">Runs grouped by avg HR as % of max ({HRMAX} bpm).</p>', unsafe_allow_html=True)
        z=pd.cut(h["avg_hr"]/HRMAX*100,bins=[0,60,70,80,90,200],labels=["Z1","Z2","Z3","Z4","Z5"]).value_counts().reindex(["Z1","Z2","Z3","Z4","Z5"]).fillna(0).reset_index()
        z.columns=["zone","runs"]
        fig=px.bar(z,x="zone",y="runs",text_auto=".0f",color="zone",color_discrete_sequence=["#334155",CYAN,MINT,"#ffb020",RED]); SHOW(grid(fig)); st.markdown("</div>",unsafe_allow_html=True)
    def c_pacehr():
        h=runs_f[(runs_f["avg_hr"].notna())&(runs_f["pace_min_per_km"].notna())]
        if h.empty: st.info("No HR data in this filter."); return
        st.markdown('<div class="chart-container-box"><h3>Pace vs Heart Rate</h3>', unsafe_allow_html=True)
        fig=px.scatter(h,x="avg_hr",y="pace_min_per_km",color="year",color_discrete_map=YEAR_COLORS)
        fig=grid(fig); fig.update_yaxes(autorange="reversed",title_text="pace min/km"); fig.update_xaxes(title_text="avg HR")
        fig.update_layout(showlegend=True,legend=dict(font=dict(color=MUTE))); SHOW(fig); st.markdown("</div>",unsafe_allow_html=True)
    def dyn(col,title,sub,color,target=None):
        d=runs_f[runs_f[col].notna()].sort_values("Date_Parsed")
        if d.empty: st.info("No running-dynamics data in this filter."); return
        st.markdown(f'<div class="chart-container-box"><h3>{title}</h3><p style="color:#64748b;font-size:.78rem;letter-spacing:0;text-transform:none;margin-top:-6px;">{sub}</p>', unsafe_allow_html=True)
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=d["Date_Parsed"],y=d[col],mode="markers",marker=dict(color=MUTE,size=4)))
        fig.add_trace(go.Scatter(x=d["Date_Parsed"],y=d[col].rolling(10,min_periods=3).mean(),mode="lines",line=dict(color=color,width=2.5)))
        if target is not None: fig.add_hline(y=target,line_dash="dash",line_color=RED)
        SHOW(grid(fig)); st.markdown("</div>",unsafe_allow_html=True)

    CHARTS={
        "Map \u00b7 Where I've Run (World)": c_map,
        "Trends \u00b7 Weekly Mileage": c_weekly,
        "Trends \u00b7 Pace Trend": c_pace,
        "Trends \u00b7 Cadence Trend": c_cad,
        "Trends \u00b7 Fitness / Fatigue / Form": c_form,
        "Trends \u00b7 Volume by Year": c_yoy,
        "Trends \u00b7 Distance Mix": c_mix,
        "Patterns \u00b7 Day of Week": c_dow,
        "Patterns \u00b7 Hour of Day": c_hour,
        "Patterns \u00b7 Monthly Heatmap": c_heat,
        "Heart \u00b7 Heart Rate Trend": c_hrtrend,
        "Heart \u00b7 Aerobic Efficiency": c_eff,
        "Heart \u00b7 Intensity Mix": c_intensity,
        "Heart \u00b7 Pace vs Heart Rate": c_pacehr,
        "Dynamics \u00b7 Cadence (FIT)": lambda: dyn("cadence_spm_fit","Cadence (FIT)",f"Steps per minute \u2014 target {CADENCE_TARGET} spm.",CYAN,CADENCE_TARGET),
        "Dynamics \u00b7 Ground Contact Time": lambda: dyn("gct_ms","Ground Contact Time","Milliseconds on the ground per step. Lower is better.",LIME),
        "Dynamics \u00b7 Vertical Oscillation": lambda: dyn("vert_osc_mm","Vertical Oscillation","Vertical bounce in mm. Lower = less wasted motion.",LIME),
        "Dynamics \u00b7 Stride Length": lambda: dyn("step_len_m","Stride Length","Metres per step.",CYAN),
        "Dynamics \u00b7 Vertical Ratio": lambda: dyn("vert_ratio","Vertical Ratio","Bounce as % of stride length. Lower is better.",LIME),
    }
    pick=st.selectbox("SELECT CHART", list(CHARTS.keys()))
    CHARTS[pick]()

# ============================================================ RACE REGISTRY
with t_rec:
    st.markdown("<div class='section-h'>PERSONAL BESTS</div>", unsafe_allow_html=True)
    cards=""
    for k,lo,hi in PB_BANDS:
        r=best_effort(runs_all,lo,hi)
        if r is None: continue
        cards+=f"""<div class="pb-card"><div class="pb-dist">{k}</div><div class="pb-time">{r['moving_time_hms']}</div>
          <div class="pb-meta">{r['pace_str']} /km<br>{r['Date_Parsed'].strftime('%d %b %Y')}</div></div>"""
    st.markdown(f'<div class="pb-grid">{cards}</div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-container-box"><h3>Official Race Registry</h3>', unsafe_allow_html=True)
    pr_dates={best_effort(runs_all,lo,hi)["Date_Parsed"].date() for _,lo,hi in PB_BANDS if best_effort(runs_all,lo,hi) is not None}
    races=f[f["Race_Tag"].notna()].copy(); races["_d"]=races["Date_Parsed"].dt.date
    races=races.sort_values("distance_km",ascending=False).drop_duplicates("_d").sort_values("Date_Parsed",ascending=False)
    if races.empty: st.markdown('<p style="color:#64748b;">No registered races in this filter.</p>', unsafe_allow_html=True)
    for _,r in races.iterrows():
        full=r["Category_Custom"]=="Full Marathon"; acc=RED if full else LIME
        chips=""
        if r["Date_Parsed"].date() in pr_dates: chips+="<span style='background:#ccff00;color:#0b0e14;font-family:monospace;font-size:.6rem;font-weight:900;padding:2px 7px;border-radius:3px;letter-spacing:1px;margin-right:6px;'>PR</span>"
        if r["Race_Note"]: chips+=f"<span style='color:{acc};font-family:monospace;font-size:.68rem;font-weight:800;'>{r['Race_Note']}</span>"
        note=f"<div style='margin-top:4px;'>{chips}</div>" if chips else ""
        st.markdown(f"""<div class="race-row" style="background:{'#1a1215' if full else '#161d2a'};border-left:4px solid {acc};">
          <div><div style="color:#fff;font-weight:800;font-size:1.08rem;">{r['Race_Tag']}</div>
          <div style="color:#64748b;font-size:.72rem;font-family:monospace;">{r['Date_Parsed'].strftime('%B %d, %Y')} &nbsp;\u00b7&nbsp; BIB {r['Race_Bib']}</div>{note}</div>
          <div class="fm-group">
            <div class="fm"><div class="fm-val">{r['distance_km']:.2f}</div><div class="fm-lbl">km</div></div>
            <div class="fm"><div class="fm-val">{r['moving_time_hms']}</div><div class="fm-lbl">time</div></div>
            <div class="fm"><div class="fm-val">{r['pace_str']}</div><div class="fm-lbl">/km</div></div>
          </div></div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================ ACTIVITY LOG
with t_log:
    st.markdown("<div class='section-h'>ACTIVITY LOG</div>", unsafe_allow_html=True)
    for _,r in f.sort_values("Date_Parsed",ascending=False).head(60).iterrows():
        full=r["Category_Custom"]=="Full Marathon"; acc=RED if full else CYAN
        cad=f"{r['cadence_spm']:.0f}" if pd.notna(r["cadence_spm"]) else "--"
        hr=f"{r['avg_hr']:.0f}" if pd.notna(r.get("avg_hr")) else "--"
        st.markdown(f"""<div class="flashcard-row-base" style="background:{'#1a1215' if full else '#121721'};border-left:4px solid {acc};">
          <div style="min-width:210px;"><div style="color:#fff;font-weight:800;font-size:1.05rem;">{r['name']}</div>
          <div style="color:{acc};font-size:.68rem;letter-spacing:1px;">{r['Category_Custom'].upper()} &nbsp;\u00b7&nbsp; {r['Date_Parsed'].strftime('%d %b %Y')}</div></div>
          <div class="fm-group">
            <div class="fm"><div class="fm-val">{r['distance_km']:.2f}</div><div class="fm-lbl">km</div></div>
            <div class="fm"><div class="fm-val">{r['moving_time_hms']}</div><div class="fm-lbl">time</div></div>
            <div class="fm"><div class="fm-val">{r['pace_str']}</div><div class="fm-lbl">/km</div></div>
            <div class="fm"><div class="fm-val">{cad}</div><div class="fm-lbl">spm</div></div>
            <div class="fm"><div class="fm-val">{hr}</div><div class="fm-lbl">hr</div></div>
          </div></div>""", unsafe_allow_html=True)
