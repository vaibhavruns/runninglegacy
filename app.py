import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="RUNNING JOURNEY // METRIC ENGINE", layout="wide",
                   initial_sidebar_state="collapsed")

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
.chart-container-box { background:#121721 !important; border:1px solid #1e293b !important; border-radius:8px !important; padding:20px !important; margin-bottom:10px !important; }
.section-h { color:#fff; font-weight:900; letter-spacing:2px; font-size:1.3rem; margin:8px 0 14px; }
.timeline { border-left:2px solid #1e293b; margin:6px 0 24px 10px; padding-left:26px; }
.tl-item { position:relative; margin-bottom:24px; }
.tl-item:before { content:''; position:absolute; left:-33px; top:3px; width:13px; height:13px; border-radius:50%; background:#ccff00; box-shadow:0 0 0 5px rgba(204,255,0,.10); }
.tl-item.full:before { background:#ff4757; box-shadow:0 0 0 5px rgba(255,71,87,.12); }
.tl-year { color:#ccff00; font-family:monospace; font-weight:800; font-size:.78rem; letter-spacing:2px; }
.tl-title { color:#fff; font-weight:800; font-size:1.18rem; margin:1px 0 3px; }
.tl-desc { color:#94a3b8; font-size:.86rem; line-height:1.5; }
.blurb { background:linear-gradient(160deg,#161d2a,#0f1420); border-left:4px solid #ccff00; border-radius:8px; padding:22px 24px; margin:4px 0 24px; line-height:1.7; color:#cbd5e1; }
.blurb b { color:#fff; }
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

STATIC={"staticPlot":True,"displayModeBar":False,"responsive":True}
def SHOW(fig,height=320):
    fig.update_layout(height=height); st.plotly_chart(fig,use_container_width=True,config=STATIC)
CHART=dict(template="plotly_dark",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=10,r=10,t=20,b=10),font=dict(family="Inter, sans-serif",size=12,color="#94a3b8"),showlegend=False)
def grid(fig):
    fig.update_layout(**CHART); fig.update_xaxes(showgrid=False,title_text="")
    fig.update_yaxes(showgrid=True,gridcolor="rgba(30,41,59,.45)",zeroline=False,title_text=""); return fig
DISCLAIMER=("Shows only runs recorded on Garmin &amp; Strava \u2014 actual mileage is higher. "
            "I\u2019ve run <b style='color:#94a3b8;'>1,000+ km every year since 2022</b>.")
def disclaimer():
    st.markdown(f"<p style='color:#64748b;font-size:.72rem;font-style:italic;letter-spacing:0;text-transform:none;margin:-4px 0 18px;'>{DISCLAIMER}</p>", unsafe_allow_html=True)

RACE_REGISTRY={
    "2023-11-19":{"name":"Indian Navy 10K","bib":"12114","note":""},
    "2024-01-21":{"name":"Tata Mumbai Marathon 21K","bib":"26504","note":""},
    "2024-04-28":{"name":"TCS World 10K Bengaluru","bib":"3970","note":""},
    "2024-09-01":{"name":"Satara Hill Half Marathon","bib":"25051","note":""},
    "2024-10-20":{"name":"Vedanta Delhi Half Marathon","bib":"3258","note":""},
    "2024-12-08":{"name":"Indian Navy 21K","bib":"23781","note":""},
    "2024-12-15":{"name":"Tata Steel World 25K Kolkata","bib":"4653","note":""},
    "2025-09-21":{"name":"Berlin Full Marathon","bib":"76975","note":""},
    "2025-10-12":{"name":"Vedanta Delhi Half Marathon","bib":"5654","note":""},
    "2025-12-21":{"name":"Tata Steel World 25K Kolkata","bib":"4895","note":""},
    "2026-01-18":{"name":"Tata Mumbai Full Marathon","bib":"11435","note":""},
    "2026-04-26":{"name":"TCS World 10K Bengaluru","bib":"32357","note":"PROCAM SLAM COMPLETED"},
}
CITY_GEO={"Mumbai":(19.05,72.85),"Surat":(21.17,72.83),"Gurgaon":(28.46,77.03),"Satara":(17.69,73.99),
    "New Delhi":(28.61,77.21),"Delhi":(28.61,77.21),"Bengaluru":(12.97,77.59),"Ujjain":(23.18,75.78),
    "Kolkata":(22.57,88.36),"Mussoorie":(30.46,78.07),"Mori":(30.78,78.18),"Puraula":(30.88,78.08),
    "Chandigarh":(30.73,76.78),"Berlin":(52.51,13.40),"Plitvicka jezera":(44.88,15.62),"Dubrovnik":(42.64,18.11)}
DATA_CANDIDATES=["activities.csv","Activities.csv","data/activities.csv"]

def hms_label(sec):
    if pd.isna(sec): return "--"
    sec=int(sec); h=sec//3600; m=(sec%3600)//60
    return f"{h}h {m:02d}m" if h else f"{m}m"

@st.cache_data(show_spinner=False)
def load_data():
    path=next((p for p in DATA_CANDIDATES if os.path.exists(p)),None)
    if path is None: return None
    df=pd.read_csv(path)
    _src=df["datetime"] if "datetime" in df.columns else df["date"]
    dt=pd.to_datetime(_src, errors="coerce")
    if dt.isna().mean()>0.3: dt=pd.to_datetime(_src, errors="coerce", dayfirst=True)
    dcol=pd.to_datetime(df["date"], errors="coerce")
    if dcol.isna().mean()>0.3: dcol=pd.to_datetime(df["date"], errors="coerce", dayfirst=True)
    df["Date_Parsed"]=dt.fillna(dcol)
    df=df[df["Date_Parsed"].notna()].copy()   # never let an unparseable date crash the app
    for c in ["distance_km","moving_time_s","pace_min_per_km","cadence_spm","relative_effort",
              "fatigue_atl","fitness_ctl","form","elevation_gain_m","calories","kudos","hour"]:
        if c in df.columns: df[c]=pd.to_numeric(df[c],errors="coerce")
    def seg(km):
        if km>=42.0: return "Full Marathon"
        if km>=21.2: return "Between Half and Full"
        if km>=21.0: return "Half Marathon"
        if km>10.5:  return "Between 10K and 21K"
        if km>=9.8:  return "10K Runs"
        return "Less than 10K"
    df["Category_Custom"]=df["distance_km"].apply(seg)
    ds=df["Date_Parsed"].dt.strftime("%Y-%m-%d")
    df["Race_Tag"]=ds.map(lambda x: RACE_REGISTRY.get(x,{}).get("name"))
    df["Race_Bib"]=ds.map(lambda x: RACE_REGISTRY.get(x,{}).get("bib"))
    df["Race_Note"]=ds.map(lambda x: RACE_REGISTRY.get(x,{}).get("note"))
    df["weekday"]=df.get("weekday",df["Date_Parsed"].dt.strftime("%a"))
    df["join_local"]=df["Date_Parsed"].dt.strftime("%Y-%m-%d %H:%M")
    # FIT per-run metrics
    fit_path=next((p for p in ["fit_metrics.csv","data/fit_metrics.csv"] if os.path.exists(p)),None)
    fitcols=["avg_hr","max_hr","cadence_spm_fit","aerobic_te","anaerobic_te","gct_ms","vert_osc_mm","vert_ratio","step_len_m"]
    if fit_path:
        fit=pd.read_csv(fit_path); keep=["join_local"]+[c for c in fitcols if c in fit.columns]
        fit=fit[keep].drop_duplicates("join_local"); df=df.merge(fit,on="join_local",how="left")
        for c in fitcols:
            if c in df.columns: df[c]=pd.to_numeric(df[c],errors="coerce")
    else:
        for c in fitcols: df[c]=np.nan
    # richer Garmin per-activity (location, power, training load)
    gpath=next((p for p in ["garmin_activities.csv","data/garmin_activities.csv"] if os.path.exists(p)),None)
    if gpath:
        g=pd.read_csv(gpath); g["jl"]=g["datetime_local"].astype(str).str.replace("T"," ").str[:16]
        g=g[["jl","location","avg_power","training_load"]].rename(columns={"training_load":"gar_load"}).drop_duplicates("jl")
        df=df.merge(g,left_on="join_local",right_on="jl",how="left")
        for c in ["avg_power","gar_load"]:
            if c in df.columns: df[c]=pd.to_numeric(df[c],errors="coerce")
    else:
        df["location"]=np.nan; df["avg_power"]=np.nan; df["gar_load"]=np.nan
    return df

@st.cache_data(show_spinner=False)
def load_daily(_sig=0):
    p=next((x for x in ["daily_metrics.csv","data/daily_metrics.csv"] if os.path.exists(x)),None)
    if not p: return None
    d=pd.read_csv(p,encoding="utf-8-sig"); d.columns=[c.strip() for c in d.columns]
    d["date"]=pd.to_datetime(d["date"],errors="coerce"); d["year"]=d["date"].dt.year; return d
@st.cache_data(show_spinner=False)
def load_profile():
    p=next((x for x in ["athlete_profile.csv","data/athlete_profile.csv"] if os.path.exists(x)),None)
    return pd.read_csv(p).iloc[0].to_dict() if p else {}
@st.cache_data(show_spinner=False)
def load_zones():
    p=next((x for x in ["zones.csv","data/zones.csv"] if os.path.exists(x)),None)
    return pd.read_csv(p) if p else None

def best_effort(runs,lo,hi):
    b=runs[(runs["distance_km"]>=lo)&(runs["distance_km"]<=hi)&(runs["moving_time_s"]>0)]
    return None if b.empty else b.loc[b["moving_time_s"].idxmin()]
PB_BANDS=[("5K",4.9,5.3),("10K",9.7,10.6),("HALF",20.9,21.6),("FULL",41.9,43.5)]

df=load_data(); daily=load_daily(_sig=(os.path.getmtime("daily_metrics.csv") if os.path.exists("daily_metrics.csv") else 0)); PROFILE=load_profile(); ZONES=load_zones()
HRMAX=int(PROFILE.get("max_hr")) if PROFILE.get("max_hr") else (int(df["max_hr"].max()) if (df is not None and "max_hr" in df.columns and df["max_hr"].notna().any()) else 190)
RHR_BASE=int(PROFILE.get("resting_hr")) if PROFILE.get("resting_hr") else None
if ZONES is not None and "hr_floor" in ZONES.columns:
    ZFLOORS=list(ZONES.sort_values("zone")["hr_floor"].astype(float))
else:
    ZFLOORS=[HRMAX*r for r in (0.50,0.60,0.70,0.80,0.90)]

st.markdown("<h1 style='color:#fff;font-size:2.8rem;font-weight:900;margin-bottom:0;'>RUNNING JOURNEY</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#ccff00 !important;font-weight:700;letter-spacing:1px;margin-top:5px;'>ENDURANCE ARCHIVE // PERFORMANCE LOG</p>", unsafe_allow_html=True)
st.markdown("<hr style='border-color:#1e293b;margin:14px 0 22px;'>", unsafe_allow_html=True)
if df is None:
    st.error("No data file found. Add activities.csv to the repo root."); st.stop()

with st.expander("CONTROL CENTER  //  FILTERS", expanded=False):
    c1,c2,c3=st.columns(3)
    with c1:
        years=["ALL TIME"]+[str(y) for y in sorted(df["year"].unique(),reverse=True)]; sel_year=st.selectbox("YEAR",years)
    with c2:
        cats=["ALL CATEGORIES","Full Marathon","Between Half and Full","Half Marathon","Between 10K and 21K","10K Runs","Less than 10K"]; sel_cat=st.selectbox("DISTANCE",cats)
    with c3:
        sel_sport=st.selectbox("ACTIVITY TYPE",["RUNS ONLY","ALL ACTIVITIES"])
f=df.copy()
if sel_sport=="RUNS ONLY": f=f[f["sport_type"]=="Run"]
if sel_year!="ALL TIME": f=f[f["year"]==int(sel_year)]
if sel_cat!="ALL CATEGORIES": f=f[f["Category_Custom"]==sel_cat]
runs_f=f[f["sport_type"]=="Run"].copy(); runs_all=df[df["sport_type"]=="Run"].copy()

tick=[]; labmap={"5K":"5K","10K":"10K","HALF":"HALF MARATHON","FULL":"FULL MARATHON"}
for k,lo,hi in PB_BANDS:
    r=best_effort(runs_all,lo,hi)
    if r is not None:
        _ds=r['Date_Parsed'].strftime('%b %Y') if pd.notna(r['Date_Parsed']) else ''
        tick.append(f"PR {labmap[k]}: {r['moving_time_hms']} @ {r['pace_str']}/KM ({_ds})")
if tick:
    st.markdown(f"""<div class="ticker-wrap"><marquee behavior="scroll" direction="left" scrollamount="6"
      style="color:#ccff00;font-weight:800;font-family:monospace;font-size:1.05rem;">ALL-TIME RECORD BENCHMARKS &nbsp;&nbsp; // &nbsp;&nbsp; {" &nbsp;&nbsp; // &nbsp;&nbsp; ".join(tick)}</marquee></div>""", unsafe_allow_html=True)

t_over,t_rec,t_data,t_log=st.tabs(["Overview","Race Registry","Data","Activity Log"])

# ===== OVERVIEW =====
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
    disclaimer()
    st.markdown("""<div class="blurb">
      <div style="font-size:1.2rem;color:#ccff00;font-weight:800;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;">Welcome to my running journey</div>
      <p style="margin:0 0 11px;">In 2022 I could barely run 2 km. A public promise\u2014to run <b>1,000 km in a year</b>\u2014turned into a habit, and I've crossed 1,000 km <b>every year since</b>.</p>
      <p style="margin:0 0 11px;">The medals and PBs were never the point\u2014it was showing up: the friendships, the new cities, the ordinary mornings. Four years of that quietly added up at the finish of the <b>2025 Berlin Marathon</b>, where I became a marathoner.</p>
      <p style="margin:0;">This is my running archive. Progress isn't dramatic\u2014it's lacing up and heading out the door. Thanks for being part of it. \U0001F3C3\u200D\u2642\uFE0F</p>
    </div>""", unsafe_allow_html=True)
    st.markdown('<div class="section-h">RUNNING TIMELINE</div>', unsafe_allow_html=True)
    yr=runs_all.groupby("year").agg(runs=("distance_km","size"),km=("distance_km","sum"),longest=("distance_km","max")).round(0)
    def ys(y,key): return int(yr.loc[y,key]) if y in yr.index else 0
    MILE=[(2022,False,"Where It Began",f"First logged run in May. {ys(2022,'runs')} runs, {ys(2022,'km')} km \u2014 and already a 26 km push by August."),
          (2023,False,"Finding Rhythm",f"{ys(2023,'runs')} runs, {ys(2023,'km')} km. The first race bibs start appearing."),
          (2024,False,"The Big Leap",f"{ys(2024,'runs')} runs, {ys(2024,'km')} km. Half marathons, the Satara hills, and the Kolkata 25K."),
          (2025,True,"Berlin \u2014 First Marathon",f"{ys(2025,'runs')} runs, {ys(2025,'km')} km. 42.2 km in 4:48:48, plus a 2:01 half-marathon PR."),
          (2026,True,"Mumbai & The Comeback","Tata Mumbai Marathon in January \u2014 then rebuilding patiently from a knee injury.")]
    rows="".join(f'<div class="tl-item {"full" if full else ""}"><div class="tl-year">{y}</div><div class="tl-title">{t}</div><div class="tl-desc">{d}</div></div>' for y,full,t,d in MILE)
    st.markdown(f'<div class="timeline">{rows}</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container-box"><h3>The Journey \u2014 Cumulative Distance</h3>', unsafe_allow_html=True)
    cum=runs_all.sort_values("Date_Parsed").copy(); cum["c"]=cum["distance_km"].cumsum()
    fig=go.Figure(go.Scatter(x=cum["Date_Parsed"],y=cum["c"],mode="lines",line=dict(color=LIME,width=2.5),fill="tozeroy",fillcolor="rgba(204,255,0,.08)"))
    SHOW(grid(fig),300); st.markdown("</div>", unsafe_allow_html=True)

# ===== RACE REGISTRY =====
with t_rec:
    disclaimer()
    st.markdown("<div class='section-h'>PERSONAL BESTS</div>", unsafe_allow_html=True)
    cards=""
    for k,lo,hi in PB_BANDS:
        r=best_effort(runs_all,lo,hi)
        if r is None: continue
        cards+=f'<div class="pb-card"><div class="pb-dist">{k}</div><div class="pb-time">{r["moving_time_hms"]}</div><div class="pb-meta">{r["pace_str"]} /km<br>{r["Date_Parsed"].strftime("%d %b %Y")}</div></div>'
    st.markdown(f'<div class="pb-grid">{cards}</div>', unsafe_allow_html=True)
    n_full=int((runs_all["distance_km"]>=42.0).sum()); n_half=int(((runs_all["distance_km"]>=21.0)&(runs_all["distance_km"]<42.0)).sum())
    lr=runs_all.loc[runs_all["distance_km"].idxmax()]; bf=best_effort(runs_all,41.9,43.5); bh=best_effort(runs_all,20.9,21.6)
    fs=f"best {bf['moving_time_hms']}" if bf is not None else "42 km +"; hs=f"best {bh['moving_time_hms']}" if bh is not None else "21\u201342 km"
    st.markdown(f"""<div class="section-h">DISTANCE MILESTONES</div><div class="kpi-container">
      <div class="kpi-card accent"><div class="kpi-value">{n_full}</div><div class="kpi-label">// FULL MARATHONS</div><div class="kpi-sub">42 km \u00b7 {fs}</div></div>
      <div class="kpi-card accent"><div class="kpi-value">{n_half}</div><div class="kpi-label">// HALF MARATHON OR LONGER</div><div class="kpi-sub">21\u201342 km \u00b7 {hs}</div></div>
      <div class="kpi-card"><div class="kpi-value">{lr['distance_km']:.1f}<span style='font-size:.9rem;'> KM</span></div><div class="kpi-label">// LONGEST RUN</div><div class="kpi-sub">{lr['Date_Parsed'].strftime('%d %b %Y')}</div></div>
      <div class="kpi-card"><div class="kpi-value">{int(runs_all['distance_km'].sum()):,}<span style='font-size:.9rem;'> KM</span></div><div class="kpi-label">// LIFETIME DISTANCE</div><div class="kpi-sub">recorded</div></div>
    </div>""", unsafe_allow_html=True)
    st.markdown('<div class="chart-container-box"><h3>Official Race Registry</h3>', unsafe_allow_html=True)
    pr_dates={best_effort(runs_all,lo,hi)["Date_Parsed"].date() for _,lo,hi in PB_BANDS if best_effort(runs_all,lo,hi) is not None}
    races=f[f["Race_Tag"].notna()].copy(); races["_d"]=races["Date_Parsed"].dt.date
    races=races.sort_values("distance_km",ascending=False).drop_duplicates("_d").sort_values("Date_Parsed",ascending=False)
    if races.empty: st.markdown('<p style="color:#64748b;">No registered races in this filter.</p>', unsafe_allow_html=True)
    for _,r in races.iterrows():
        full=r["Category_Custom"]=="Full Marathon"; acc=RED if full else LIME; chips=""
        if r["Date_Parsed"].date() in pr_dates: chips+="<span style='background:#ccff00;color:#0b0e14;font-family:monospace;font-size:.6rem;font-weight:900;padding:2px 7px;border-radius:3px;letter-spacing:1px;margin-right:6px;'>PR</span>"
        if r["Race_Note"]: chips+=f"<span style='color:{acc};font-family:monospace;font-size:.68rem;font-weight:800;'>{r['Race_Note']}</span>"
        note=f"<div style='margin-top:4px;'>{chips}</div>" if chips else ""
        st.markdown(f"""<div class="race-row" style="background:{'#1a1215' if full else '#161d2a'};border-left:4px solid {acc};">
          <div><div style="color:#fff;font-weight:800;font-size:1.08rem;">{r['Race_Tag']}</div>
          <div style="color:#64748b;font-size:.72rem;font-family:monospace;">{r['Date_Parsed'].strftime('%B %d, %Y')} &nbsp;\u00b7&nbsp; BIB {r['Race_Bib']}</div>{note}</div>
          <div class="fm-group"><div class="fm"><div class="fm-val">{r['distance_km']:.2f}</div><div class="fm-lbl">km</div></div>
            <div class="fm"><div class="fm-val">{r['moving_time_hms']}</div><div class="fm-lbl">time</div></div>
            <div class="fm"><div class="fm-val">{r['pace_str']}</div><div class="fm-lbl">/km</div></div></div></div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ===== DATA =====
with t_data:
    disclaimer()
    _ds = "daily_metrics: " + (f"loaded {len(daily)} rows" if daily is not None else "NOT FOUND")
    _ds += " \u00b7 garmin power: " + ("yes" if ("avg_power" in df.columns and df["avg_power"].notna().any()) else "no")
    _ds += " \u00b7 profile: " + ("yes" if PROFILE else "no") + " \u00b7 zones: " + ("yes" if ZONES is not None else "no")
    st.caption(_ds)
    def c_map():
        st.markdown('<div class="chart-container-box"><h3>Where I\'ve Run</h3>', unsafe_allow_html=True)
        r=runs_all.copy(); r["loc"]=r["location"].where(r["location"].notna() & r["location"].astype(str).ne("nan"),"Mumbai")
        r["loc"]=r["loc"].apply(lambda c: c if c in CITY_GEO else "Mumbai")
        cv=r.groupby("loc").agg(runs=("distance_km","size"),km=("distance_km","sum")).reset_index()
        cv["lat"]=cv["loc"].map(lambda c: CITY_GEO[c][0]); cv["lon"]=cv["loc"].map(lambda c: CITY_GEO[c][1])
        cv["label"]=cv.apply(lambda x:f"{x['loc']}  \u2022  {int(x['runs'])} runs \u2022 {int(x['km'])} km",axis=1)
        fig=go.Figure(go.Scattergeo(lon=cv["lon"],lat=cv["lat"],text=cv["label"],hoverinfo="text",mode="markers",
            marker=dict(size=9,color=LIME,opacity=.95,symbol="circle",line=dict(width=1.6,color="#0b0e14"))))
        fig.update_geos(projection_type="natural earth",showland=True,landcolor="#1a2230",showcountries=True,countrycolor="#5a6b85",
            countrywidth=0.8,showocean=True,oceancolor="#0b0e14",showcoastlines=True,coastlinecolor="#5a6b85",coastlinewidth=0.8,
            bgcolor="rgba(0,0,0,0)",lakecolor="#0b0e14",framecolor="#2b3850",lataxis_range=[8,56],lonaxis_range=[8,95])
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",margin=dict(l=0,r=0,t=0,b=0),height=440)
        st.plotly_chart(fig,use_container_width=True,config=STATIC)
        chips="".join(f"<span style='display:inline-block;background:#161d2a;border:1px solid #1e293b;border-radius:20px;padding:5px 13px;margin:4px 6px 0 0;font-size:.74rem;'><b style='color:#ccff00;'>{x['loc']}</b> <span style='color:#64748b;font-family:monospace;'>{int(x['km'])} km</span></span>" for _,x in cv.sort_values('km',ascending=False).iterrows())
        st.markdown(f"<div style='margin-top:10px;'>{chips}</div></div>", unsafe_allow_html=True)
    def _fd(cols):
        if daily is None: return None
        d=daily.dropna(subset=cols)
        if sel_year!="ALL TIME": d=d[d["year"]==int(sel_year)]
        return d.sort_values("date")
    def _trend(d,col,color,title,hline=None,hlbl=""):
        st.markdown(f'<div class="chart-container-box"><h3>{title}</h3>', unsafe_allow_html=True)
        fig=go.Figure(); fig.add_trace(go.Scatter(x=d["date"],y=d[col],mode="markers",marker=dict(color=MUTE,size=4)))
        fig.add_trace(go.Scatter(x=d["date"],y=d[col].rolling(14,min_periods=4).mean(),mode="lines",line=dict(color=color,width=2.5)))
        if hline is not None: fig.add_hline(y=hline,line_dash="dash",line_color=RED,annotation_text=hlbl,annotation_font_color=RED)
        SHOW(grid(fig)); st.markdown("</div>",unsafe_allow_html=True)
    def c_vo2():
        d=_fd(["vo2max_running"]);
        if d is None or d.empty: st.info("No VO\u2082 max data in this filter."); return
        _trend(d,"vo2max_running",LIME,"VO\u2082 Max (Running)")
    def c_rhr():
        d=_fd(["rhr"]);
        if d is None or d.empty: st.info("No resting-HR data in this filter."); return
        _trend(d,"rhr",CYAN,"Resting Heart Rate",RHR_BASE,f"baseline {RHR_BASE}" if RHR_BASE else "")
    def c_hrv():
        d=_fd(["hrv_overnight_ms"]);
        if d is None or d.empty: st.info("No HRV data in this filter."); return
        st.markdown('<div class="chart-container-box"><h3>Overnight HRV</h3>', unsafe_allow_html=True)
        fig=go.Figure(); fig.add_trace(go.Scatter(x=d["date"],y=d["hrv_overnight_ms"],mode="markers",marker=dict(color=MUTE,size=4)))
        wk=d["hrv_weekly_avg"] if ("hrv_weekly_avg" in d and d["hrv_weekly_avg"].notna().any()) else d["hrv_overnight_ms"].rolling(14,min_periods=4).mean()
        fig.add_trace(go.Scatter(x=d["date"],y=wk,mode="lines",line=dict(color=LIME,width=2.5)))
        SHOW(grid(fig)); st.markdown("</div>",unsafe_allow_html=True)
    def c_sleep():
        d=_fd(["sleep_total_min"]);
        if d is None or d.empty: st.info("No sleep data in this filter."); return
        st.markdown('<div class="chart-container-box"><h3>Sleep Stages &amp; Score</h3>', unsafe_allow_html=True)
        fig=go.Figure()
        for col,nm,clr in [("sleep_deep_min","Deep","#1e40af"),("sleep_rem_min","REM",CYAN),("sleep_light_min","Light","#334155")]:
            if col in d: fig.add_trace(go.Scatter(x=d["date"],y=d[col]/60,mode="lines",stackgroup="s",name=nm,line=dict(width=0.4,color=clr)))
        if "sleep_score" in d: fig.add_trace(go.Scatter(x=d["date"],y=d["sleep_score"],mode="lines",name="Score",yaxis="y2",line=dict(color=LIME,width=1.4)))
        fig=grid(fig); fig.update_layout(showlegend=True,legend=dict(orientation="h",y=1.15,font=dict(color=MUTE)),
            yaxis2=dict(overlaying="y",side="right",showgrid=False,range=[0,100],title="")); SHOW(fig,360); st.markdown("</div>",unsafe_allow_html=True)
    def c_ready():
        d=_fd(["readiness_score"]);
        if d is None or d.empty: st.info("No readiness data in this filter."); return
        _trend(d,"readiness_score",MINT,"Training Readiness")
    def c_acwr():
        d=_fd(["acwr"]);
        if d is None or d.empty: st.info("No load data in this filter."); return
        st.markdown('<div class="chart-container-box"><h3>Acute : Chronic Load (ACWR)</h3>', unsafe_allow_html=True)
        fig=go.Figure(); fig.add_hrect(y0=0.8,y1=1.3,fillcolor="rgba(52,229,196,.10)",line_width=0)
        fig.add_trace(go.Scatter(x=d["date"],y=d["acwr"],mode="lines",line=dict(color=LIME,width=2)))
        fig.add_hline(y=1.5,line_dash="dash",line_color=RED,annotation_text="injury-risk 1.5",annotation_font_color=RED)
        fig=grid(fig); fig.update_yaxes(range=[0,2]); SHOW(fig); st.markdown("</div>",unsafe_allow_html=True)
    def c_preds():
        d=_fd(["pred_marathon_s"]);
        if d is None or d.empty: st.info("No race-prediction data in this filter."); return
        st.markdown('<div class="chart-container-box"><h3>Garmin Race Predictions</h3>', unsafe_allow_html=True)
        fig=go.Figure()
        for col,nm,clr in [("pred_5k_s","5K","#334155"),("pred_10k_s","10K",CYAN),("pred_half_s","Half",MINT),("pred_marathon_s","Marathon",LIME)]:
            if col in d: fig.add_trace(go.Scatter(x=d["date"],y=d[col]/60,mode="lines",name=nm,line=dict(color=clr,width=2)))
        fig=grid(fig); fig.update_yaxes(type="log",title_text="predicted minutes (log)")
        fig.update_layout(showlegend=True,legend=dict(orientation="h",y=1.15,font=dict(color=MUTE))); SHOW(fig,360); st.markdown("</div>",unsafe_allow_html=True)
    def c_power():
        d=runs_f[runs_f["avg_power"].notna()].sort_values("Date_Parsed") if "avg_power" in runs_f.columns else runs_f.iloc[0:0]
        if d.empty: st.info("No running-power data in this filter."); return
        st.markdown('<div class="chart-container-box"><h3>Running Power</h3>', unsafe_allow_html=True)
        fig=go.Figure(); fig.add_trace(go.Scatter(x=d["Date_Parsed"],y=d["avg_power"],mode="markers",marker=dict(color=MUTE,size=4)))
        fig.add_trace(go.Scatter(x=d["Date_Parsed"],y=d["avg_power"].rolling(10,min_periods=3).mean(),mode="lines",line=dict(color="#ffb020",width=2.5)))
        SHOW(grid(fig)); st.markdown("</div>",unsafe_allow_html=True)
    def c_weekly():
        st.markdown('<div class="chart-container-box"><h3>Weekly Mileage</h3>', unsafe_allow_html=True)
        wk=runs_f.set_index("Date_Parsed")["distance_km"].resample("W-MON").sum().reset_index()
        if sel_year=="ALL TIME": wk=wk.tail(52)
        fig=px.bar(wk,x="Date_Parsed",y="distance_km"); fig.update_traces(marker_color=CYAN); SHOW(grid(fig)); st.markdown("</div>",unsafe_allow_html=True)
    def c_pace():
        st.markdown('<div class="chart-container-box"><h3>Pace Trend</h3>', unsafe_allow_html=True)
        p=runs_f[(runs_f["pace_min_per_km"].notna())&(runs_f["distance_km"]>=3)].sort_values("Date_Parsed")
        fig=go.Figure(); fig.add_trace(go.Scatter(x=p["Date_Parsed"],y=p["pace_min_per_km"],mode="markers",marker=dict(color=MUTE,size=5)))
        fig.add_trace(go.Scatter(x=p["Date_Parsed"],y=p["pace_min_per_km"].rolling(10,min_periods=3).mean(),mode="lines",line=dict(color=LIME,width=2.5)))
        fig=grid(fig); fig.update_yaxes(autorange="reversed",title_text="min/km (faster=up)"); SHOW(fig); st.markdown("</div>",unsafe_allow_html=True)
    def c_cad():
        st.markdown('<div class="chart-container-box"><h3>Cadence Trend</h3>', unsafe_allow_html=True)
        cc=runs_f[(runs_f["cadence_spm"].notna())&(runs_f["cadence_spm"]>120)].sort_values("Date_Parsed")
        fig=go.Figure(); fig.add_trace(go.Scatter(x=cc["Date_Parsed"],y=cc["cadence_spm"],mode="markers",marker=dict(color=MUTE,size=5)))
        fig.add_trace(go.Scatter(x=cc["Date_Parsed"],y=cc["cadence_spm"].rolling(10,min_periods=3).mean(),mode="lines",line=dict(color=CYAN,width=2.5)))
        fig.add_hline(y=CADENCE_TARGET,line_dash="dash",line_color=RED,annotation_text=f"TARGET {CADENCE_TARGET}",annotation_font_color=RED)
        SHOW(grid(fig)); st.markdown("</div>",unsafe_allow_html=True)
    def c_form():
        st.markdown('<div class="chart-container-box"><h3>Fitness \u00b7 Fatigue \u00b7 Form</h3>', unsafe_allow_html=True)
        tl=runs_f.sort_values("Date_Parsed"); fig=go.Figure()
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
        fig=go.Figure(); fig.add_trace(go.Scatter(x=h["Date_Parsed"],y=h["max_hr"],mode="markers",marker=dict(color="#3a2230",size=4)))
        fig.add_trace(go.Scatter(x=h["Date_Parsed"],y=h["avg_hr"],mode="markers",marker=dict(color=MUTE,size=5)))
        fig.add_trace(go.Scatter(x=h["Date_Parsed"],y=h["avg_hr"].rolling(10,min_periods=3).mean(),mode="lines",line=dict(color=RED,width=2.5)))
        SHOW(grid(fig)); st.markdown("</div>",unsafe_allow_html=True)
    def c_eff():
        h=runs_f[runs_f["avg_hr"].notna()].copy()
        if h.empty: st.info("No HR data in this filter."); return
        h["mpb"]=(h["distance_km"]*1000)/(h["avg_hr"]*(h["moving_time_s"]/60.0)); e=h[h["distance_km"]>=5].sort_values("Date_Parsed")
        st.markdown('<div class="chart-container-box"><h3>Aerobic Efficiency</h3>', unsafe_allow_html=True)
        fig=go.Figure(); fig.add_trace(go.Scatter(x=e["Date_Parsed"],y=e["mpb"],mode="markers",marker=dict(color=MUTE,size=5)))
        fig.add_trace(go.Scatter(x=e["Date_Parsed"],y=e["mpb"].rolling(8,min_periods=3).mean(),mode="lines",line=dict(color=LIME,width=2.5)))
        SHOW(grid(fig)); st.markdown("</div>",unsafe_allow_html=True)
    def c_intensity():
        h=runs_f[runs_f["avg_hr"].notna()]
        if h.empty: st.info("No HR data in this filter."); return
        st.markdown('<div class="chart-container-box"><h3>Intensity Mix</h3>', unsafe_allow_html=True)
        edges=[0,ZFLOORS[1],ZFLOORS[2],ZFLOORS[3],ZFLOORS[4],300]
        z=pd.cut(h["avg_hr"],bins=edges,labels=["Z1","Z2","Z3","Z4","Z5"],right=False).value_counts().reindex(["Z1","Z2","Z3","Z4","Z5"]).fillna(0).reset_index()
        z.columns=["zone","runs"]
        fig=px.bar(z,x="zone",y="runs",text_auto=".0f",color="zone",color_discrete_sequence=["#334155",CYAN,MINT,"#ffb020",RED]); SHOW(grid(fig)); st.markdown("</div>",unsafe_allow_html=True)
    def c_pacehr():
        h=runs_f[(runs_f["avg_hr"].notna())&(runs_f["pace_min_per_km"].notna())]
        if h.empty: st.info("No HR data in this filter."); return
        st.markdown('<div class="chart-container-box"><h3>Pace vs Heart Rate</h3>', unsafe_allow_html=True)
        fig=px.scatter(h,x="avg_hr",y="pace_min_per_km",color="year",color_discrete_map=YEAR_COLORS)
        fig=grid(fig); fig.update_yaxes(autorange="reversed",title_text="pace min/km"); fig.update_xaxes(title_text="avg HR")
        fig.update_layout(showlegend=True,legend=dict(font=dict(color=MUTE))); SHOW(fig); st.markdown("</div>",unsafe_allow_html=True)
    def dyn(col,title,color,target=None):
        d=runs_f[runs_f[col].notna()].sort_values("Date_Parsed")
        if d.empty: st.info("No running-dynamics data in this filter."); return
        st.markdown(f'<div class="chart-container-box"><h3>{title}</h3>', unsafe_allow_html=True)
        fig=go.Figure(); fig.add_trace(go.Scatter(x=d["Date_Parsed"],y=d[col],mode="markers",marker=dict(color=MUTE,size=4)))
        fig.add_trace(go.Scatter(x=d["Date_Parsed"],y=d[col].rolling(10,min_periods=3).mean(),mode="lines",line=dict(color=color,width=2.5)))
        if target is not None: fig.add_hline(y=target,line_dash="dash",line_color=RED)
        SHOW(grid(fig)); st.markdown("</div>",unsafe_allow_html=True)

    CHARTS={
        "Map \u00b7 Where I've Run (World)": c_map,
        "Engine \u00b7 VO\u2082 Max": c_vo2,
        "Engine \u00b7 Resting HR": c_rhr,
        "Engine \u00b7 Overnight HRV": c_hrv,
        "Engine \u00b7 Sleep": c_sleep,
        "Engine \u00b7 Training Readiness": c_ready,
        "Load \u00b7 Garmin ACWR": c_acwr,
        "Performance \u00b7 Race Predictions": c_preds,
        "Performance \u00b7 Running Power": c_power,
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
        "Dynamics \u00b7 Cadence (FIT)": lambda: dyn("cadence_spm_fit","Cadence (FIT)",CYAN,CADENCE_TARGET),
        "Dynamics \u00b7 Ground Contact Time": lambda: dyn("gct_ms","Ground Contact Time",LIME),
        "Dynamics \u00b7 Vertical Oscillation": lambda: dyn("vert_osc_mm","Vertical Oscillation",LIME),
        "Dynamics \u00b7 Stride Length": lambda: dyn("step_len_m","Stride Length",CYAN),
        "Dynamics \u00b7 Vertical Ratio": lambda: dyn("vert_ratio","Vertical Ratio",LIME),
    }
    CAPTIONS={
        "Map \u00b7 Where I've Run (World)":"Every recorded run placed at its real city. Bigger bubble = more total distance there \u2014 from your Mumbai home base out to race trips across India and Europe.",
        "Engine \u00b7 VO\u2082 Max":"Garmin's estimate of your aerobic capacity over time. The headline endurance-fitness number \u2014 higher and more sustained means a stronger engine.",
        "Engine \u00b7 Resting HR":"Your daily resting heart rate (with your baseline marked). A falling trend signals improving fitness and recovery; spikes usually mean fatigue, stress, or illness.",
        "Engine \u00b7 Overnight HRV":"Overnight heart-rate variability in milliseconds. Higher and stable means well-recovered; a sustained drop is an early warning of stress or overtraining.",
        "Engine \u00b7 Sleep":"Each night split into deep, REM and light hours (stacked), with Garmin's sleep score as the green line \u2014 the recovery foundation everything else sits on.",
        "Engine \u00b7 Training Readiness":"Garmin's daily 0\u2013100 readiness score \u2014 how prepared your body is to train hard, blending sleep, HRV, recovery time and recent load.",
        "Load \u00b7 Garmin ACWR":"Recent (acute) load versus your baseline (chronic) load. The green 0.8\u20131.3 band builds fitness safely; spiking above ~1.5 (red line) is the classic injury-risk zone \u2014 worth watching given your knee history.",
        "Performance \u00b7 Race Predictions":"Garmin's predicted finish times over two years (log scale, so all four distances fit). Watch the marathon line \u2014 fitness gained into Berlin and the dip through the knee rebuild.",
        "Performance \u00b7 Running Power":"Running power in watts per run \u2014 effort that's independent of pace, hills and wind. Steady or rising output at the same feel signals improving strength.",
        "Trends \u00b7 Weekly Mileage":"Total distance run each week. Training blocks, taper weeks and breaks all show up at a glance.",
        "Trends \u00b7 Pace Trend":"Average pace of every run over time (faster sits higher). The line is a 10-run rolling average showing the direction of your speed.",
        "Trends \u00b7 Cadence Trend":"Steps per minute per run against your 174 target. Higher cadence usually means shorter, springier, lower-impact strides.",
        "Trends \u00b7 Fitness / Fatigue / Form":"A load model from effort: Fitness (42-day) is your built-up base, Fatigue (7-day) is recent tiredness, Form is the gap \u2014 positive = fresh, negative = loaded.",
        "Trends \u00b7 Volume by Year":"Total kilometres per calendar year \u2014 the clearest view of your year-on-year growth.",
        "Trends \u00b7 Distance Mix":"How your runs split across distance buckets \u2014 how much is short and easy versus long efforts.",
        "Patterns \u00b7 Day of Week":"Which days you run most, by distance \u2014 your weekly rhythm and long-run day.",
        "Patterns \u00b7 Hour of Day":"The time of day you start runs \u2014 confirms you're a committed morning runner.",
        "Patterns \u00b7 Monthly Heatmap":"Distance per month across the years; brighter cells are bigger months. Surfaces seasonality and your heaviest blocks.",
        "Heart \u00b7 Heart Rate Trend":"Average and max HR per run over time. The average trending down at similar paces is a clean sign of improving fitness.",
        "Heart \u00b7 Aerobic Efficiency":"Metres covered per heartbeat on 5 km+ runs. Rising = the same speed at lower cardiac cost \u2014 pure aerobic gains.",
        "Heart \u00b7 Intensity Mix":"How many runs fall in each of your real Garmin HR zones. A base built mostly on Z2 is the healthy endurance pattern; heavy Z4/Z5 means lots of hard running.",
        "Heart \u00b7 Pace vs Heart Rate":"Each run plotted as pace against heart rate, coloured by year. Points drifting down-and-left over the years mean faster at the same effort.",
        "Dynamics \u00b7 Cadence (FIT)":"Garmin's measured steps per minute against the 174 target \u2014 a cleaner signal than the Strava-derived cadence.",
        "Dynamics \u00b7 Ground Contact Time":"How long each foot stays on the ground (ms). Quicker contact is generally more economical.",
        "Dynamics \u00b7 Vertical Oscillation":"How much you bounce vertically each stride (mm). Less bounce means less energy wasted going up instead of forward.",
        "Dynamics \u00b7 Stride Length":"Average distance covered per step \u2014 tends to grow as fitness and speed improve.",
        "Dynamics \u00b7 Vertical Ratio":"Vertical bounce as a percentage of stride length \u2014 the single best running-economy number. Lower is better.",
    }
    pick=st.selectbox("SELECT CHART",list(CHARTS.keys()))
    CHARTS[pick]()
    st.markdown(f"<p style='color:#64748b;font-size:.82rem;line-height:1.6;letter-spacing:0;text-transform:none;margin-top:2px;'><b style='color:#94a3b8;'>What this shows \u2014 </b>{CAPTIONS.get(pick,'')}</p>", unsafe_allow_html=True)

# ===== ACTIVITY LOG =====
with t_log:
    st.markdown("<div class='section-h'>ACTIVITY LOG</div>", unsafe_allow_html=True)
    for _,r in f.sort_values("Date_Parsed",ascending=False).head(60).iterrows():
        full=r["Category_Custom"]=="Full Marathon"; acc=RED if full else CYAN
        cad=f"{r['cadence_spm']:.0f}" if pd.notna(r["cadence_spm"]) else "--"
        hr=f"{r['avg_hr']:.0f}" if pd.notna(r.get("avg_hr")) else "--"
        st.markdown(f"""<div class="flashcard-row-base" style="background:{'#1a1215' if full else '#121721'};border-left:4px solid {acc};">
          <div style="min-width:210px;"><div style="color:#fff;font-weight:800;font-size:1.05rem;">{r['name']}</div>
          <div style="color:{acc};font-size:.68rem;letter-spacing:1px;">{r['Category_Custom'].upper()} &nbsp;\u00b7&nbsp; {r['Date_Parsed'].strftime('%d %b %Y')}</div></div>
          <div class="fm-group"><div class="fm"><div class="fm-val">{r['distance_km']:.2f}</div><div class="fm-lbl">km</div></div>
            <div class="fm"><div class="fm-val">{r['moving_time_hms']}</div><div class="fm-lbl">time</div></div>
            <div class="fm"><div class="fm-val">{r['pace_str']}</div><div class="fm-lbl">/km</div></div>
            <div class="fm"><div class="fm-val">{cad}</div><div class="fm-lbl">spm</div></div>
            <div class="fm"><div class="fm-val">{hr}</div><div class="fm-lbl">hr</div></div></div></div>""", unsafe_allow_html=True)
