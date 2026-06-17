import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

st.set_page_config(page_title="STRIDE", layout="wide", initial_sidebar_state="collapsed")

# ============================================================ IDENTITY
INK="#0B0D10"; SURF="#14171C"; LINE="#1E232B"; LINE2="#2A313B"
TXT="#ECF0F4"; TXT2="#9BA6B2"; MUTE="#5A6472"
VOLT="#D6FB4F"   # you / progress / live
SIGNAL="#FF5A3C" # effort / alert / the race
DETAIL_FLOOR=pd.Timestamp("2024-01-01")  # per-run detail begins when Garmin+Strava synced
RACE_NAME="Sydney Marathon"; RACE_DATE=pd.Timestamp("2026-08-30")
CADENCE_TARGET=174

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Saira:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap');
html{ scroll-behavior:smooth; }
.stApp{ background:#0B0D10!important; color:#9BA6B2!important; font-family:'Saira',system-ui,sans-serif!important; }
.block-container{ padding-top:3.6rem!important; max-width:1180px; }
header[data-testid="stHeader"]{ background:rgba(11,13,16,0.85)!important; backdrop-filter:blur(4px); }
.nav{ margin-top:6px; }
[data-testid="stMarkdownContainer"] p,p,label,.stSelectbox div{ color:#9BA6B2!important; }
h1,h2,h3,h4{ font-family:'Saira',sans-serif!important; color:#ECF0F4!important; }
.mono{ font-family:'JetBrains Mono',ui-monospace,monospace; }
.eyebrow{ font-family:'JetBrains Mono',monospace; font-size:.72rem; letter-spacing:2px; color:#5A6472; text-transform:uppercase; }
.reveal{ animation:fadeUp .6s ease both; }
@keyframes fadeUp{ from{opacity:0; transform:translateY(10px);} to{opacity:1; transform:none;} }
/* nav */
.nav{ display:flex; align-items:center; justify-content:space-between; padding:4px 0 16px; border-bottom:.5px solid #1E232B; margin-bottom:28px; }
.wordmark{ font-family:'Saira',sans-serif; font-weight:800; font-size:1.7rem; letter-spacing:3px; color:#ECF0F4; }
.wordmark b{ color:#D6FB4F; }
.navlinks a{ font-family:'JetBrains Mono',monospace; font-size:.72rem; letter-spacing:1.5px; color:#5A6472; text-decoration:none; margin-left:22px; text-transform:uppercase; }
.navlinks a:hover{ color:#9BA6B2; }
/* hero */
.statement{ font-family:'Saira',sans-serif; font-weight:800; font-size:4rem; line-height:.96; color:#ECF0F4; letter-spacing:.5px; margin:6px 0 4px; }
.statement .dot{ color:#D6FB4F; }
.herostat{ font-family:'JetBrains Mono',monospace; font-weight:700; font-size:3rem; color:#D6FB4F; line-height:1; }
.herostat small{ font-size:1rem; color:#9BA6B2; font-weight:500; }
.cd-card{ background:#14171C; border:.5px solid #1E232B; border-radius:14px; padding:22px 24px; }
.cd-num{ font-family:'JetBrains Mono',monospace; font-weight:700; font-size:3.6rem; color:#FF5A3C; line-height:1; }
/* section */
.sec{ margin:54px 0 6px; }
.sec h2{ font-family:'Saira',sans-serif; font-weight:700; font-size:1.7rem; color:#ECF0F4; margin:2px 0 2px; }
.rule{ border:0; border-top:.5px solid #1E232B; margin:10px 0 22px; }
/* stat cards */
.cards{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:14px; margin:6px 0 8px; }
.card{ background:#14171C; border:.5px solid #1E232B; border-radius:12px; padding:18px 20px; transition:border-color .18s ease; }
.card:hover{ border-color:#2A313B; }
.card .v{ font-family:'JetBrains Mono',monospace; font-weight:700; font-size:1.9rem; color:#ECF0F4; line-height:1; }
.card .v.volt{ color:#D6FB4F; }
.card .l{ font-family:'JetBrains Mono',monospace; font-size:.68rem; letter-spacing:1.4px; color:#5A6472; text-transform:uppercase; margin-top:9px; }
/* timeline */
.tl{ border-left:.5px solid #2A313B; margin:8px 0 8px 8px; padding-left:26px; }
.tl-item{ position:relative; margin-bottom:22px; }
.tl-item:before{ content:''; position:absolute; left:-33px; top:3px; width:11px; height:11px; border-radius:50%; background:#5A6472; }
.tl-item.volt:before{ background:#D6FB4F; }
.tl-item.signal:before{ background:#FF5A3C; }
.tl-item.now:before{ background:#D6FB4F; box-shadow:0 0 0 5px rgba(214,251,79,.14); }
.tl-yr{ font-family:'JetBrains Mono',monospace; font-size:.7rem; letter-spacing:1.5px; color:#9BA6B2; text-transform:uppercase; }
.tl-t{ font-family:'Saira',sans-serif; font-weight:600; font-size:1.05rem; color:#ECF0F4; margin:1px 0 2px; }
.tl-s{ font-family:'JetBrains Mono',monospace; font-size:.74rem; color:#5A6472; }
/* chart heads + empty */
.ch{ margin:24px 0 6px; }
.ch-t{ font-family:'Saira',sans-serif; font-weight:600; font-size:1.12rem; color:#ECF0F4; }
.ch-s{ font-family:'JetBrains Mono',monospace; font-size:.72rem; color:#5A6472; margin-top:2px; }
.empty{ background:#14171C; border:.5px dashed #2A313B; border-radius:12px; padding:30px; text-align:center;
  font-family:'JetBrains Mono',monospace; font-size:.82rem; color:#5A6472; letter-spacing:1px; margin:4px 0 8px; }
.note{ font-family:'JetBrains Mono',monospace; font-size:.74rem; color:#5A6472; line-height:1.6; margin:2px 0 6px; }
.footer{ border-top:.5px solid #1E232B; margin-top:54px; padding-top:18px; display:flex; justify-content:space-between;
  font-family:'JetBrains Mono',monospace; font-size:.7rem; letter-spacing:1px; color:#5A6472; }
*:focus-visible{ outline:2px solid #D6FB4F!important; outline-offset:2px; }
@media (prefers-reduced-motion:reduce){ *{ animation:none!important; transition:none!important; } }
@media (max-width:640px){
  .statement{ font-size:2.6rem; } .herostat{ font-size:2.2rem; } .cd-num{ font-size:2.6rem; }
  .footer{ flex-direction:column; gap:6px; }
}
/* tabs */
div[data-testid="stTabs"] div[role="tablist"]{ gap:2px; flex-wrap:wrap; border-bottom:.5px solid #1E232B; margin-bottom:16px; }
div[data-testid="stTabs"] button{ font-family:'JetBrains Mono',monospace!important; font-size:.78rem!important; font-weight:500!important; letter-spacing:1.5px!important; text-transform:uppercase!important; color:#5A6472!important; padding:12px 18px!important; border-bottom:2px solid transparent!important; }
div[data-testid="stTabs"] button:hover{ color:#9BA6B2!important; }
div[data-testid="stTabs"] button[aria-selected="true"]{ color:#D6FB4F!important; border-bottom:2px solid #D6FB4F!important; }
/* registry + log rows */
.row{ background:#14171C; border:.5px solid #1E232B; border-radius:10px; padding:14px 18px; margin-bottom:10px; display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:12px; }
.row .nm{ font-family:'Saira',sans-serif; font-weight:600; font-size:1.05rem; color:#ECF0F4; min-width:200px; }
.row .meta{ font-family:'JetBrains Mono',monospace; font-size:.68rem; color:#5A6472; margin-top:3px; letter-spacing:.5px; }
.stats{ display:flex; gap:20px; }
.stat{ text-align:center; min-width:46px; }
.stat .n{ font-family:'JetBrains Mono',monospace; font-weight:700; color:#ECF0F4; font-size:.95rem; }
.stat .u{ font-family:'JetBrains Mono',monospace; font-size:.56rem; color:#5A6472; letter-spacing:.5px; margin-top:2px; }
.chip{ display:inline-block; font-family:'JetBrains Mono',monospace; font-size:.56rem; font-weight:700; padding:2px 7px; border-radius:4px; letter-spacing:1px; margin-right:6px; margin-top:4px; }
.chip.pr{ background:#D6FB4F; color:#0B0D10; }
@media (max-width:640px){ .row .nm{ min-width:100%; } .stats{ width:100%; justify-content:flex-start; gap:16px; } }

</style>
""", unsafe_allow_html=True)

STATIC={"staticPlot":True,"displayModeBar":False,"responsive":True}
CHART=dict(template="plotly_dark",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=8,r=12,t=20,b=8),font=dict(family="'JetBrains Mono', monospace",size=12,color="#9BA6B2"),
    showlegend=False,colorway=[VOLT,SIGNAL,"#9BA6B2","#5DCAA5","#85B7EB"])
def grid(fig):
    fig.update_layout(**CHART)
    fig.update_xaxes(showgrid=False,title_text="",tickfont=dict(color="#5A6472"),linecolor="rgba(30,35,43,.9)")
    fig.update_yaxes(showgrid=True,gridcolor="rgba(30,35,43,.7)",zeroline=False,title_text="",tickfont=dict(color="#5A6472"))
    return fig
def SHOW(fig,h=320):
    fig.update_layout(height=h); st.plotly_chart(fig,use_container_width=True,config=STATIC)
def chart_head(title,sub=""):
    s=f"<div class='ch-s'>{sub}</div>" if sub else ""
    st.markdown(f"<div class='ch'><div class='ch-t'>{title}</div>{s}</div>",unsafe_allow_html=True)
def detail_empty():
    st.markdown("<div class='empty'>Detailed data starts Jan 2024</div>",unsafe_allow_html=True)
def _rmean(s,w):
    mp=1 if w<=1 else max(2,w//4); return s.rolling(w,min_periods=mp).mean()

# ============================================================ DATA LAYER (reused, proven)
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
    "Chandigarh":(30.73,76.78),"Berlin":(52.51,13.40),"Plitvicka jezera":(44.88,15.62),"Dubrovnik":(42.64,18.11),
    "Chennai":(13.08,80.27),"Pune":(18.52,73.86),"Hyderabad":(17.39,78.49),"Ahmedabad":(23.02,72.57),
    "Jaipur":(26.91,75.79),"Goa":(15.30,74.12),"Nashik":(19.99,73.79),"Lonavala":(18.75,73.41),
    "London":(51.51,-0.13),"Dubai":(25.20,55.27),"Singapore":(1.35,103.82)}
NON_INDIA={"Berlin":"Germany","Plitvicka jezera":"Croatia","Dubrovnik":"Croatia",
    "London":"United Kingdom","Dubai":"UAE","Singapore":"Singapore"}
def country_of(city): return NON_INDIA.get(city,"India")
DATA_CANDIDATES_OV=["locations.csv","data/locations.csv"]
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
    df=df[df["Date_Parsed"].notna()].copy()
    for c in ["distance_km","moving_time_s","pace_min_per_km","cadence_spm","relative_effort",
              "elevation_gain_m","calories","kudos","hour"]:
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
    fit_path=next((p for p in ["fit_metrics.csv","data/fit_metrics.csv"] if os.path.exists(p)),None)
    fitcols=["avg_hr","max_hr","cadence_spm_fit","aerobic_te","anaerobic_te","gct_ms","vert_osc_mm","vert_ratio","step_len_m"]
    if fit_path:
        fit=pd.read_csv(fit_path); keep=["join_local"]+[c for c in fitcols if c in fit.columns]
        fit=fit[keep].drop_duplicates("join_local"); df=df.merge(fit,on="join_local",how="left")
        for c in fitcols:
            if c in df.columns: df[c]=pd.to_numeric(df[c],errors="coerce")
    else:
        for c in fitcols: df[c]=np.nan
    gpath=next((p for p in ["garmin_activities.csv","data/garmin_activities.csv"] if os.path.exists(p)),None)
    if gpath:
        g=pd.read_csv(gpath)
        gdate=pd.to_datetime(g["date"],errors="coerce").dt.strftime("%Y-%m-%d")
        locmap=(g.assign(_d=gdate).dropna(subset=["location"])
                  .groupby("_d")["location"].agg(lambda s: s.mode().iat[0] if not s.mode().empty else s.iloc[0]))
        df["location"]=df["Date_Parsed"].dt.strftime("%Y-%m-%d").map(locmap)
        g["jl"]=g["datetime_local"].astype(str).str.replace("T"," ").str[:16]
        gm=g[["jl","avg_power","training_load"]].rename(columns={"training_load":"gar_load"}).drop_duplicates("jl")
        df=df.merge(gm,left_on="join_local",right_on="jl",how="left")
        for c in ["avg_power","gar_load"]:
            if c in df.columns: df[c]=pd.to_numeric(df[c],errors="coerce")
    else:
        df["location"]=np.nan; df["avg_power"]=np.nan; df["gar_load"]=np.nan
    ovp=next((p for p in DATA_CANDIDATES_OV if os.path.exists(p)),None)
    if ovp:
        try:
            ov=pd.read_csv(ovp)
            ov["d"]=pd.to_datetime(ov["date"],errors="coerce").dt.strftime("%Y-%m-%d")
            om=ov.dropna(subset=["d","city"]).set_index("d")["city"].to_dict()
            dkey=df["Date_Parsed"].dt.strftime("%Y-%m-%d")
            df["location"]=dkey.map(om).fillna(df["location"])
        except Exception:
            pass
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
def load_nrc():
    p=next((x for x in ["nrc_monthly.csv","data/nrc_monthly.csv"] if os.path.exists(x)),None)
    if not p: return None
    n=pd.read_csv(p); n["year"]=n["year"].astype(int)
    n["mn"]=pd.to_datetime(n["month_start"]).dt.month
    return n

def best_effort(runs,lo,hi):
    b=runs[(runs["distance_km"]>=lo)&(runs["distance_km"]<=hi)&(runs["moving_time_s"]>0)]
    return None if b.empty else b.loc[b["moving_time_s"].idxmin()]
PB_BANDS=[("5K",4.9,5.3),("10K",9.7,10.6),("HALF",20.9,21.6),("FULL",41.9,43.5)]

df=load_data()
daily=load_daily(_sig=(os.path.getmtime("daily_metrics.csv") if os.path.exists("daily_metrics.csv") else 0))
PROFILE=load_profile(); ZONES=load_zones(); NRC=load_nrc()

def annual_volume(runs):
    # ADDITIVE: Strava per-run + NRC monthly archive summed per year (distinct runs across apps).
    sv=runs.groupby("year")["distance_km"].sum(); svn=runs.groupby("year").size()
    years=set(int(y) for y in sv.index)
    if NRC is not None: years|=set(int(y) for y in NRC["year"].unique())
    rows=[]
    for y in sorted(years):
        nk=nr=0.0
        if NRC is not None and (NRC["year"]==y).any():
            sub=NRC[NRC["year"]==y]; nk=float(sub["total_km"].sum()); nr=int(sub["num_runs"].sum())
        km=float(sv.get(y,0.0))+nk; rn=int(svn.get(y,0))+int(nr)
        rows.append({"year":y,"km":km,"runs":rn,"has_nrc":nk>0})
    return pd.DataFrame(rows)

if df is None:
    st.markdown("<div class='nav'><span class='wordmark'>STRIDE<b>.</b></span></div>",unsafe_allow_html=True)
    st.markdown("<div class='empty'>No data file found. Add activities.csv to the repo root.</div>",unsafe_allow_html=True)
    st.stop()

HRMAX=int(PROFILE.get("max_hr")) if PROFILE.get("max_hr") else (int(df["max_hr"].max()) if ("max_hr" in df.columns and df["max_hr"].notna().any()) else 190)
RHR_BASE=int(PROFILE.get("resting_hr")) if PROFILE.get("resting_hr") else None
VO2_BASE=PROFILE.get("vo2max_running")

runs_all=df[df["sport_type"]=="Run"].copy()
av=annual_volume(runs_all)
life_km=int(av["km"].sum()); life_runs=int(av["runs"].sum())
n_full=int((runs_all["distance_km"]>=42.0).sum())
n_half=int(((runs_all["distance_km"]>=21.0)&(runs_all["distance_km"]<42.0)).sum())
years_running=pd.Timestamp.today().year-2021
days_to=(RACE_DATE - pd.Timestamp.today().normalize()).days
bf=best_effort(runs_all,41.9,43.5); marathon_pb=bf["moving_time_hms"] if bf is not None else "—"

st.markdown("""
<div class="nav">
  <span class="wordmark">STRIDE<b>.</b></span>
  <span class="eyebrow" style="letter-spacing:2px;">A running record · since 2021</span>
</div>""", unsafe_allow_html=True)

t_over,t_lab,t_reg,t_log=st.tabs(["Overview","Data Lab","Race Registry","Activity Log"])

with t_over:
    # ============================================================ 1 · HERO
    hero_l,hero_r=st.columns([1.55,1])
    with hero_l:
        st.markdown(f"""<div class="reveal">
          <div class="eyebrow">A running record · since 2021</div>
          <div class="statement">Five years.<br>On foot<span class="dot">.</span></div>
          <div style="font-family:'Saira';font-size:1.05rem;color:#9BA6B2;margin:6px 0 22px;">Building toward the next start line.</div>
          <div class="herostat">{life_km:,}<small> KM</small></div>
          <div class="eyebrow" style="margin-top:8px;">Lifetime distance · {life_runs:,} runs</div>
        </div>""", unsafe_allow_html=True)
    with hero_r:
        st.markdown(f"""<div class="reveal cd-card">
          <div class="eyebrow">Next race</div>
          <div style="font-family:'Saira';font-weight:600;font-size:1.25rem;color:#ECF0F4;margin:4px 0 14px;">{RACE_NAME}</div>
          <div class="cd-num">{days_to}</div>
          <div class="eyebrow" style="margin-top:8px;">Days to go</div>
          <div class="eyebrow" style="color:#9BA6B2;margin-top:10px;">{RACE_DATE.strftime('%d %B %Y').upper()}</div>
        </div>""", unsafe_allow_html=True)

    # ============================================================ 2 · THE JOURNEY
    st.markdown("<div id='journey'></div>",unsafe_allow_html=True)
    st.markdown("""<div class="sec reveal"><div class="eyebrow" style="color:#D6FB4F;">The journey</div>
      <h2>The long arc</h2></div><div class="note">2021 — present · NRC archive + Strava, combined</div>
      <hr class="rule">""", unsafe_allow_html=True)

    st.markdown(f"""<div class="cards">
      <div class="card"><div class="v volt">{life_km:,}</div><div class="l">Lifetime km</div></div>
      <div class="card"><div class="v">{life_runs:,}</div><div class="l">Total runs</div></div>
      <div class="card"><div class="v">{n_full}</div><div class="l">Marathons run</div></div>
      <div class="card"><div class="v">{years_running}</div><div class="l">Years running</div></div>
    </div>""", unsafe_allow_html=True)

    # Volume by year — columns, additive, NRC years hatched, in-progress year hollow
    chart_head("Volume by year", "Kilometres per year · NRC + Strava, additive · 2026 in progress")
    avc=av.copy(); avc["yr"]=avc["year"].astype(str)
    this_year=pd.Timestamp.today().year
    bar_colors=["rgba(214,251,79,.35)" if int(y)==this_year else VOLT for y in avc["year"]]
    fig=go.Figure()
    fig.add_trace(go.Bar(x=avc["yr"],y=avc["km"],marker_color=bar_colors,
        text=[f"{k:,.0f}" for k in avc["km"]],textposition="outside",
        textfont=dict(family="'JetBrains Mono', monospace",color="#9BA6B2",size=11),
        hovertemplate="%{x}: %{y:,.0f} km<extra></extra>"))
    fig=grid(fig); fig.update_yaxes(title_text="km"); fig.update_layout(margin=dict(l=8,r=12,t=28,b=8))
    SHOW(fig,300)

    # Where I've run (map)
    chart_head("Where I've run", "Every recorded run placed at its city · bubble size = total distance")
    r=runs_all.copy(); r["loc"]=r["location"].where(r["location"].notna() & r["location"].astype(str).ne("nan"),"Mumbai")
    r["loc"]=r["loc"].apply(lambda c: c if c in CITY_GEO else "Mumbai")
    cv=r.groupby("loc").agg(runs=("distance_km","size"),km=("distance_km","sum")).reset_index()
    cv["lat"]=cv["loc"].map(lambda c: CITY_GEO[c][0]); cv["lon"]=cv["loc"].map(lambda c: CITY_GEO[c][1])
    cv["sz"]=8+ (cv["km"]/cv["km"].max()*22)
    cv["label"]=cv.apply(lambda x:f"{x['loc']} · {int(x['runs'])} runs · {int(x['km'])} km",axis=1)
    mp=go.Figure(go.Scattergeo(lon=cv["lon"],lat=cv["lat"],text=cv["label"],hoverinfo="text",mode="markers",
        marker=dict(size=cv["sz"],color=VOLT,opacity=.9,line=dict(width=1,color=INK))))
    mp.update_geos(projection_type="natural earth",showland=True,landcolor="#11151B",showcountries=True,countrycolor="#2A313B",
        countrywidth=0.5,showocean=True,oceancolor="#0B0D10",showcoastlines=True,coastlinecolor="#2A313B",coastlinewidth=0.5,
        bgcolor="rgba(0,0,0,0)",lakecolor="#0B0D10",lataxis_range=[5,58],lonaxis_range=[-12,100])
    mp.update_layout(paper_bgcolor="rgba(0,0,0,0)",margin=dict(l=0,r=0,t=0,b=0),height=420)
    st.plotly_chart(mp,use_container_width=True,config=STATIC)

    # Cities & countries (below the map)
    cvc=cv.copy(); cvc["country"]=cvc["loc"].map(country_of)
    n_cities=int(cvc["loc"].nunique()); countries=sorted(cvc["country"].unique().tolist()); n_countries=len(countries)
    st.markdown(f"""<div class="cards" style="margin-top:14px;">
      <div class="card"><div class="v volt">{n_cities}</div><div class="l">Cities run in</div></div>
      <div class="card"><div class="v">{n_countries}</div><div class="l">Countries run in</div></div>
    </div>""", unsafe_allow_html=True)
    city_chips="".join(
        f"<span style='display:inline-block;background:#14171C;border:.5px solid #1E232B;border-radius:20px;padding:5px 12px;margin:5px 6px 0 0;font-family:JetBrains Mono,monospace;font-size:.72rem;'>"
        f"<b style='color:#D6FB4F;'>{x['loc']}</b> <span style='color:#5A6472;'>{int(x['km'])} km</span></span>"
        for _,x in cvc.sort_values('km',ascending=False).iterrows())
    st.markdown(f"<div style='margin:6px 0 8px;'>{city_chips}</div>", unsafe_allow_html=True)
    country_chips="".join(
        f"<span style='display:inline-block;border:.5px solid #2A313B;border-radius:20px;padding:4px 12px;margin:5px 6px 0 0;font-family:JetBrains Mono,monospace;font-size:.7rem;color:#9BA6B2;'>{c}</span>"
        for c in countries)
    st.markdown(f"<div class='eyebrow' style='margin-top:10px;'>Countries</div><div style='margin-top:4px;'>{country_chips}</div>", unsafe_allow_html=True)

    # Milestones (last in Overview, just before Outlook)
    chart_head("Milestones", "")
    items=[
        ("2021","First logged runs","Nike Run Club era — monthly archive","steel"),
        ("2022",f"Base year — {int(av[av['year']==2022]['km'].sum()) if (av['year']==2022).any() else 0:,} km","Highest-volume year on record","volt"),
        ("Sep 2025","Berlin Marathon",f"First full marathon — {marathon_pb}","signal"),
        ("Early 2026","Knee injury","Managed conservatively, no surgery","signal"),
        ("May 2026","Comeback","Cleared to run","volt"),
        ("Now","Building for Sydney","Detailed training data from Jan 2024","now"),
    ]
    rows="".join(f"<div class='tl-item {c}'><div class='tl-yr'>{yr}</div><div class='tl-t'>{t}</div><div class='tl-s'>{s}</div></div>" for yr,t,s,c in items)
    st.markdown(f"<div class='tl'>{rows}</div>", unsafe_allow_html=True)

    # ============================================================ 4 · OUTLOOK
    st.markdown("<div id='outlook'></div>",unsafe_allow_html=True)
    st.markdown("""<div class="sec reveal"><div class="eyebrow" style="color:#FF5A3C;">Outlook</div>
      <h2>The road to Sydney</h2></div><hr class="rule">""", unsafe_allow_html=True)

    # current form readouts (last 28 days vs prior 28)
    recent=runs_all[runs_all["Date_Parsed"]>=pd.Timestamp.today().normalize()-pd.Timedelta(days=28)]
    prior=runs_all[(runs_all["Date_Parsed"]<pd.Timestamp.today().normalize()-pd.Timedelta(days=28))&(runs_all["Date_Parsed"]>=pd.Timestamp.today().normalize()-pd.Timedelta(days=56))]
    km28=recent["distance_km"].sum(); kmprev=prior["distance_km"].sum()
    delta=("+" if km28>=kmprev else "")+f"{(km28-kmprev):.0f}"
    cur_acwr=cur_ready=cur_vo2=None
    if daily is not None:
        dd=daily.dropna(subset=["acute_load","chronic_load"]).sort_values("date")
        if not dd.empty:
            rr=dd.set_index("date")[["acute_load","chronic_load"]].resample("D").mean()
            rser=(rr["acute_load"].ffill()/rr["chronic_load"].ffill()).rolling(7,min_periods=3).mean().dropna()
            if not rser.empty: cur_acwr=rser.iloc[-1]
        dr2=daily.dropna(subset=["readiness_score"]).sort_values("date")
        if not dr2.empty: cur_ready=float(dr2["readiness_score"].iloc[-1])
        dv2=daily.dropna(subset=["vo2max_running"]).sort_values("date")
        if not dv2.empty: cur_vo2=float(dv2["vo2max_running"].iloc[-1])
    acwr_txt=f"{cur_acwr:.2f}" if cur_acwr is not None else "--"
    acwr_col=VOLT if (cur_acwr is not None and 0.8<=cur_acwr<=1.3) else (SIGNAL if (cur_acwr is not None and cur_acwr>1.5) else "#ECF0F4")
    ready_txt=f"{cur_ready:.0f}" if cur_ready is not None else "--"
    vo2_txt=f"{cur_vo2:.0f}" if cur_vo2 is not None else "--"

    st.markdown(f"""<div class="cards">
      <div class="card"><div class="v" style="color:#FF5A3C;">{days_to}</div><div class="l">Days to {RACE_NAME}</div></div>
      <div class="card"><div class="v volt">{km28:.0f}<small style="font-size:.9rem;color:#9BA6B2;"> km</small></div><div class="l">Last 28 days · {delta} vs prior</div></div>
      <div class="card"><div class="v" style="color:{acwr_col};">{acwr_txt}</div><div class="l">Current load (ACWR)</div></div>
      <div class="card"><div class="v">{ready_txt}</div><div class="l">Readiness today</div></div>
      <div class="card"><div class="v">{vo2_txt}</div><div class="l">VO\u2082 max</div></div>
    </div>
    <div class="note" style="margin-top:10px;">Momentum readout — not a prediction. The plan is the plan; the body has the veto.</div>""", unsafe_allow_html=True)

with t_lab:
    # ===================== TRENDS (trivia · full history · per-chart filters) =====================
    st.markdown("""<div class="sec"><div class="eyebrow" style="color:#D6FB4F;">Trends</div>
      <h2>Patterns &amp; trivia</h2></div>
      <div class="note">Full-history patterns across every recorded run. Each chart carries its own filter.</div>
      <hr class="rule">""", unsafe_allow_html=True)
    tr_years=["All time"]+[str(y) for y in sorted(runs_all["year"].dropna().astype(int).unique(),reverse=True)]
    def tr_scope(key,r):
        yr=st.selectbox("Year",tr_years,index=0,key=key)
        return r if yr=="All time" else r[r["year"]==int(yr)]

    # Day of week
    chart_head("Day of week", "Which days carry the miles")
    dow_metric=st.radio("Measure",["Distance","Runs"],horizontal=True,index=0,key="dow_m")
    d=tr_scope("dow_y",runs_all.copy())
    order=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    if dow_metric=="Distance":
        wd=d.groupby("weekday")["distance_km"].sum().reindex(order).fillna(0); ylab="km"
    else:
        wd=d.groupby("weekday").size().reindex(order).fillna(0); ylab="runs"
    fig=go.Figure(go.Bar(x=order,y=wd.values,marker_color=VOLT,text=[f"{v:.0f}" for v in wd.values],
        textposition="outside",textfont=dict(family="'JetBrains Mono', monospace",color="#9BA6B2",size=11)))
    fig=grid(fig); fig.update_yaxes(title_text=ylab); SHOW(fig,260)

    # Hour of day
    chart_head("Time of day", "When the runs start")
    d=tr_scope("hour_y",runs_all.copy())
    if "hour" in d.columns and d["hour"].notna().any():
        hr=d.groupby(d["hour"].astype("Int64")).size().reindex(range(0,24)).fillna(0)
        fig=go.Figure(go.Bar(x=list(range(0,24)),y=hr.values,marker_color="#85B7EB"))
        fig=grid(fig); fig.update_yaxes(title_text="runs"); fig.update_xaxes(title_text="hour"); SHOW(fig,240)
    else:
        st.markdown("<div class='empty'>No start-hour data in this filter.</div>",unsafe_allow_html=True)

    # Distance mix
    chart_head("Distance mix", "How the runs break down by length")
    d=tr_scope("mix_y",runs_all.copy())
    order2=["Less than 10K","10K Runs","Between 10K and 21K","Half Marathon","Between Half and Full","Full Marathon"]
    fr=d["Category_Custom"].value_counts().reindex(order2).fillna(0)
    fr=fr[fr>0]
    fig=go.Figure(go.Bar(x=fr.values,y=fr.index,orientation="h",marker_color=VOLT,
        text=[f"{v:.0f}" for v in fr.values],textposition="outside",textfont=dict(family="'JetBrains Mono', monospace",color="#9BA6B2",size=11)))
    fig=grid(fig); fig.update_xaxes(title_text="runs"); fig.update_yaxes(showgrid=False); SHOW(fig,260)

    # Monthly consistency (moved from Overview · full history · additive)
    chart_head("Monthly consistency", "Distance per month · brighter = bigger month · NRC + Strava, additive")
    sv=runs_all.copy(); sv["mn"]=sv["Date_Parsed"].dt.month
    piv=sv.pivot_table(index="year",columns="mn",values="distance_km",aggfunc="sum")
    if NRC is not None:
        npv=NRC.pivot_table(index="year",columns="mn",values="total_km",aggfunc="sum")
        piv=pd.concat([piv,npv])
    piv=piv.groupby(level=0).sum().reindex(columns=range(1,13)).fillna(0).sort_index()
    piv.index=piv.index.astype(int); piv.columns=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    hm=px.imshow(piv,text_auto=".0f",aspect="auto",color_continuous_scale=[[0,"#0F1318"],[.5,"#5a7a1e"],[1,VOLT]])
    hm.update_layout(**{k:v for k,v in CHART.items() if k!="showlegend"}); hm.update_coloraxes(showscale=False)
    hm.update_traces(textfont=dict(family="'JetBrains Mono', monospace",size=10))
    SHOW(hm,300)

    # ============================================================ 3 · THE BUILD
    st.markdown("<div id='build'></div>",unsafe_allow_html=True)
    st.markdown("""<div class="sec reveal"><div class="eyebrow" style="color:#D6FB4F;">The build</div>
      <h2>The current block</h2></div>
      <div class="note">Per-run detail begins Jan 2024, when Garmin and Strava came into sync. Earlier years live in the Journey tab.</div>
      <hr class="rule">""", unsafe_allow_html=True)

    det_years=[str(y) for y in sorted(df[df["Date_Parsed"]>=DETAIL_FLOOR]["year"].unique(),reverse=True)]
    with st.expander("Filters", expanded=False):
        fc1,fc2=st.columns(2)
        with fc1:
            yopts=["2024 — now"]+det_years
            sel_year=st.selectbox("Window",yopts,index=0)
        with fc2:
            sel_scope=st.radio("Distance",["All","5K+","10K+","HM+"],horizontal=True,index=0)
    SCOPE={"All":0.0,"5K+":5.0,"10K+":10.0,"HM+":21.0}[sel_scope]

    def bruns():
        r=runs_all[runs_all["Date_Parsed"]>=DETAIL_FLOOR].copy()
        if sel_year!="2024 — now": r=r[r["year"]==int(sel_year)]
        if SCOPE>0: r=r[r["distance_km"]>=SCOPE]
        return r.sort_values("Date_Parsed")
    def bdaily(cols):
        if daily is None: return None
        d=daily.dropna(subset=cols); d=d[d["date"]>=DETAIL_FLOOR]
        if sel_year!="2024 — now": d=d[d["year"]==int(sel_year)]
        return d.sort_values("date")

    # --- Load & safety: weekly km bars + ACWR line + safe band ---
    chart_head("Weekly load & safety", "Bars = weekly km · line = acute:chronic ratio · green band 0.8–1.3 builds safely")
    rb=bruns()
    if rb.empty:
        detail_empty()
    else:
        wk=rb.set_index("Date_Parsed")["distance_km"].resample("W-MON").sum().reset_index()
        fig=make_subplots(specs=[[{"secondary_y":True}]])
        fig.add_trace(go.Bar(x=wk["Date_Parsed"],y=wk["distance_km"],marker_color="#3a4a12",
            hovertemplate="%{y:.0f} km<extra></extra>"),secondary_y=False)
        if daily is not None:
            base=daily[daily["date"]>=DETAIL_FLOOR]
            if sel_year!="2024 — now": base=base[base["year"]==int(sel_year)]
            g=base[["date","acute_load","chronic_load"]].dropna(subset=["date"]).sort_values("date").set_index("date").resample("D").mean()
            if g[["acute_load","chronic_load"]].notna().any().all():
                ratio=(g["acute_load"].ffill()/g["chronic_load"].ffill()).rolling(7,min_periods=3).mean().dropna()
                if not ratio.empty:
                    fig.add_hrect(y0=0.8,y1=1.3,fillcolor="rgba(93,202,165,.10)",line_width=0,secondary_y=True)
                    fig.add_trace(go.Scatter(x=ratio.index,y=ratio.values,mode="lines",line=dict(color=TXT2,width=2),
                        hovertemplate="ACWR %{y:.2f}<extra></extra>"),secondary_y=True)
                    hot=ratio.where(ratio>1.5)
                    fig.add_trace(go.Scatter(x=ratio.index,y=hot.values,mode="lines",line=dict(color=SIGNAL,width=2.5),
                        hovertemplate="ACWR %{y:.2f}<extra></extra>"),secondary_y=True)
                    fig.add_hline(y=1.5,line_dash="dash",line_color=SIGNAL,secondary_y=True)
                    fig.update_yaxes(range=[0,2],secondary_y=True,title_text="ACWR",showgrid=False,tickfont=dict(color="#5A6472"))
        fig=grid(fig); fig.update_yaxes(title_text="km / week",secondary_y=False); SHOW(fig,330)

    # --- Pace trend ---
    chart_head("Pace trend", "Every run · faster sits higher · 10-run rolling average")
    rb=bruns(); p=rb[(rb["pace_min_per_km"].notna())&(rb["distance_km"]>=max(2.0,SCOPE))]
    if p.empty: detail_empty()
    else:
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=p["Date_Parsed"],y=p["pace_min_per_km"],mode="markers",marker=dict(color=MUTE,size=5)))
        fig.add_trace(go.Scatter(x=p["Date_Parsed"],y=_rmean(p["pace_min_per_km"],10),mode="lines",line=dict(color=VOLT,width=2.5)))
        fig=grid(fig); fig.update_yaxes(autorange="reversed",title_text="min/km"); SHOW(fig)

    # --- Cadence trend ---
    chart_head("Cadence", f"Steps per minute · target {CADENCE_TARGET} · 10-run rolling average")
    rb=bruns(); cc=rb[(rb["cadence_spm"].notna())&(rb["cadence_spm"]>120)]
    if cc.empty: detail_empty()
    else:
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=cc["Date_Parsed"],y=cc["cadence_spm"],mode="markers",marker=dict(color=MUTE,size=5)))
        fig.add_trace(go.Scatter(x=cc["Date_Parsed"],y=_rmean(cc["cadence_spm"],10),mode="lines",line=dict(color=VOLT,width=2.5)))
        fig.add_hline(y=CADENCE_TARGET,line_dash="dash",line_color=SIGNAL,annotation_text=f"target {CADENCE_TARGET}",annotation_font_color=SIGNAL)
        fig=grid(fig); fig.update_yaxes(title_text="spm"); SHOW(fig)

    # --- Aerobic efficiency (signature) ---
    chart_head("Aerobic efficiency", "Effort vs pace · bubble = distance · brighter = more recent · down-left over time = base building")
    rb=bruns(); e=rb[(rb["relative_effort"].notna())&(rb["pace_min_per_km"].notna())]
    if e.empty: detail_empty()
    else:
        e=e.sort_values("Date_Parsed"); days=(e["Date_Parsed"]-e["Date_Parsed"].min()).dt.days
        fig=go.Figure(go.Scatter(x=e["relative_effort"],y=e["pace_min_per_km"],mode="markers",
            marker=dict(size=6+(e["distance_km"]/e["distance_km"].max()*22),
                color=days,colorscale=[[0,"#2A313B"],[1,VOLT]],showscale=False,line=dict(width=0.5,color=INK)),
            hovertemplate="effort %{x:.0f} · %{y:.2f} min/km<extra></extra>"))
        fig=grid(fig); fig.update_yaxes(autorange="reversed",title_text="pace min/km"); fig.update_xaxes(title_text="relative effort"); SHOW(fig)

    # --- Recovery: HRV + RHR ---
    chart_head("Recovery", "Overnight HRV & resting HR · faint dots raw, bold 7-day rolling · gaps = unsynced days")
    dr=bdaily(["hrv_overnight_ms"])
    if dr is None or dr.empty: detail_empty()
    else:
        fig=make_subplots(specs=[[{"secondary_y":True}]])
        fig.add_trace(go.Scatter(x=dr["date"],y=dr["hrv_overnight_ms"],mode="markers",marker=dict(color="rgba(214,251,79,.30)",size=4),hovertemplate="HRV %{y:.0f} ms<extra></extra>"),secondary_y=False)
        fig.add_trace(go.Scatter(x=dr["date"],y=_rmean(dr["hrv_overnight_ms"],7),mode="lines",line=dict(color=VOLT,width=2.5),hovertemplate="HRV %{y:.0f} ms<extra></extra>"),secondary_y=False)
        drh=bdaily(["rhr"])
        if drh is not None and not drh.empty:
            fig.add_trace(go.Scatter(x=drh["date"],y=drh["rhr"],mode="markers",marker=dict(color="rgba(133,183,235,.30)",size=4),hovertemplate="RHR %{y:.0f} bpm<extra></extra>"),secondary_y=True)
            fig.add_trace(go.Scatter(x=drh["date"],y=_rmean(drh["rhr"],7),mode="lines",line=dict(color="#85B7EB",width=2),hovertemplate="RHR %{y:.0f} bpm<extra></extra>"),secondary_y=True)
            if RHR_BASE: fig.add_hline(y=RHR_BASE,line_dash="dot",line_color="#85B7EB",secondary_y=True)
        fig=grid(fig); fig.update_yaxes(title_text="HRV ms",secondary_y=False)
        fig.update_yaxes(title_text="RHR bpm",secondary_y=True,showgrid=False,tickfont=dict(color="#5A6472"))
        SHOW(fig,330)

    # --- Economy small multiples ---
    chart_head("Running economy", "Ground contact · vertical ratio · stride — each annotated with the good direction")
    rb=bruns()
    econ=[("gct_ms","Ground contact (ms)","lower is better"),("vert_ratio","Vertical ratio (%)","lower is better"),("step_len_m","Stride (m)","higher is better")]
    if rb[[c for c,_,_ in econ if c in rb.columns]].dropna(how="all").empty:
        detail_empty()
    else:
        cols=st.columns(3)
        for (col,lbl,good),cc in zip(econ,cols):
            with cc:
                if col not in rb.columns or rb[col].notna().sum()==0:
                    st.markdown(f"<div class='ch-s'>{lbl}</div><div class='empty' style='padding:18px'>no data</div>",unsafe_allow_html=True); continue
                d=rb[rb[col].notna()]
                st.markdown(f"<div class='ch-s'>{lbl} · <span style='color:#9BA6B2'>{good}</span></div>",unsafe_allow_html=True)
                fig=go.Figure()
                fig.add_trace(go.Scatter(x=d["Date_Parsed"],y=d[col],mode="markers",marker=dict(color=MUTE,size=3)))
                fig.add_trace(go.Scatter(x=d["Date_Parsed"],y=_rmean(d[col],10),mode="lines",line=dict(color=VOLT,width=2)))
                fig=grid(fig); fig.update_xaxes(showticklabels=False); SHOW(fig,200)

    # --- Fitness: VO2 stepped ---
    chart_head("Fitness", "VO\u2082 max trend (stepped)")
    dv=bdaily(["vo2max_running"])
    if dv is None or dv.empty: detail_empty()
    else:
        fig=go.Figure(go.Scatter(x=dv["date"],y=dv["vo2max_running"],mode="lines",line=dict(color=VOLT,width=2.5,shape="hv"),hovertemplate="VO2 %{y:.1f}<extra></extra>"))
        fig=grid(fig); fig.update_yaxes(title_text="VO\u2082 max"); SHOW(fig,280)

    # --- Fitness / Fatigue / Form (Garmin load — never Strava CTL) ---
    chart_head("Fitness \u00b7 Fatigue \u00b7 Form", "Garmin load \u00b7 fitness = chronic load, fatigue = acute load, form = chronic \u2212 acute (fresh when positive)")
    dff=bdaily(["acute_load","chronic_load"])
    if dff is None or dff.empty: detail_empty()
    else:
        dff=dff.sort_values("date"); form=dff["chronic_load"]-dff["acute_load"]
        fig=make_subplots(specs=[[{"secondary_y":True}]])
        fig.add_trace(go.Scatter(x=dff["date"],y=dff["chronic_load"],mode="lines",line=dict(color=VOLT,width=2.5),name="Fitness",hovertemplate="Fitness %{y:.0f}<extra></extra>"),secondary_y=False)
        fig.add_trace(go.Scatter(x=dff["date"],y=dff["acute_load"],mode="lines",line=dict(color=SIGNAL,width=1.8),name="Fatigue",hovertemplate="Fatigue %{y:.0f}<extra></extra>"),secondary_y=False)
        fig.add_trace(go.Scatter(x=dff["date"],y=form,mode="lines",line=dict(color="#85B7EB",width=1.5),name="Form",hovertemplate="Form %{y:.0f}<extra></extra>"),secondary_y=True)
        fig.add_hline(y=0,line_dash="dot",line_color="#5A6472",secondary_y=True)
        fig=grid(fig); fig.update_yaxes(title_text="load",secondary_y=False)
        fig.update_yaxes(title_text="form",secondary_y=True,showgrid=False,tickfont=dict(color="#5A6472"))
        fig.update_layout(showlegend=True,legend=dict(orientation="h",y=1.18,x=0,font=dict(color="#9BA6B2"))); SHOW(fig,300)

    # --- Heart rate footnote ---
    chart_head("Heart rate", "Wrist HR — indicative only · pace and effort are the trusted signals")
    rb=bruns(); h=rb[rb["avg_hr"].notna()] if "avg_hr" in rb.columns else rb.iloc[0:0]
    if h.empty: detail_empty()
    else:
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=h["Date_Parsed"],y=h["avg_hr"],mode="markers",marker=dict(color=MUTE,size=4)))
        fig.add_trace(go.Scatter(x=h["Date_Parsed"],y=_rmean(h["avg_hr"],10),mode="lines",line=dict(color="#85B7EB",width=2)))
        fig=grid(fig); fig.update_yaxes(title_text="avg HR (wrist)"); SHOW(fig,240)

with t_reg:
    st.markdown("<div class='sec'><div class='eyebrow' style='color:#FF5A3C;'>Race registry</div><h2>Official races</h2></div><hr class='rule'>", unsafe_allow_html=True)
    # Personal bests by distance + race counts
    pb_cards=""
    for lbl,lo,hi in PB_BANDS:
        b=best_effort(runs_all,lo,hi)
        if b is not None:
            tt=b["moving_time_hms"]; pc=b["pace_str"]; dt=b["Date_Parsed"].strftime("%b %Y")
            pb_cards+=f"<div class='card'><div class='l' style='color:#D6FB4F;margin:0 0 6px;'>{lbl}</div><div class='v'>{tt}</div><div class='l'>{pc}/km · {dt}</div></div>"
        else:
            pb_cards+=f"<div class='card'><div class='l' style='color:#5A6472;margin:0 0 6px;'>{lbl}</div><div class='v' style='color:#5A6472;'>—</div><div class='l'>no effort yet</div></div>"
    st.markdown(f"<div class='eyebrow'>Personal bests</div><div class='cards' style='margin-top:6px;'>{pb_cards}</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class="cards" style="margin-top:6px;">
      <div class="card"><div class="v" style="color:#FF5A3C;">{n_full}</div><div class="l">Marathons (42 km+)</div></div>
      <div class="card"><div class="v">{n_half}</div><div class="l">Half+ (21–42 km)</div></div>
    </div><hr class='rule'>""", unsafe_allow_html=True)
    pr_dates={best_effort(runs_all,lo,hi)["Date_Parsed"].date() for _,lo,hi in PB_BANDS if best_effort(runs_all,lo,hi) is not None}
    races=runs_all[runs_all["Race_Tag"].notna()].copy(); races["_d"]=races["Date_Parsed"].dt.date
    races=races.sort_values("distance_km",ascending=False).drop_duplicates("_d").sort_values("Date_Parsed",ascending=False)
    if races.empty:
        st.markdown("<div class='empty'>No registered races.</div>", unsafe_allow_html=True)
    for _,rr in races.iterrows():
        full=rr["Category_Custom"]=="Full Marathon"; acc=SIGNAL if full else VOLT
        chips="<span class='chip pr'>PR</span>" if rr["Date_Parsed"].date() in pr_dates else ""
        if rr["Race_Note"]: chips+=f"<span class='chip' style='color:{acc};background:#1E232B;'>{rr['Race_Note']}</span>"
        note=f"<div>{chips}</div>" if chips else ""
        st.markdown(f"<div class='row' style='border-left:3px solid {acc};'><div><div class='nm'>{rr['Race_Tag']}</div><div class='meta'>{rr['Date_Parsed'].strftime('%d %b %Y')} · BIB {rr['Race_Bib']}</div>{note}</div><div class='stats'><div class='stat'><div class='n'>{rr['distance_km']:.2f}</div><div class='u'>KM</div></div><div class='stat'><div class='n'>{rr['moving_time_hms']}</div><div class='u'>TIME</div></div><div class='stat'><div class='n'>{rr['pace_str']}</div><div class='u'>/KM</div></div></div></div>", unsafe_allow_html=True)

with t_log:
    st.markdown("<div class='sec'><div class='eyebrow' style='color:#D6FB4F;'>Activity log</div><h2>Recent runs</h2></div><hr class='rule'>", unsafe_allow_html=True)
    log_df=runs_all.sort_values("Date_Parsed",ascending=False)
    show_all=st.checkbox(f"Show all {len(log_df)} runs", value=False) if len(log_df)>20 else True
    rows_=log_df if show_all else log_df.head(20)
    for _,rr in rows_.iterrows():
        full=rr["Category_Custom"]=="Full Marathon"; acc=SIGNAL if full else "#85B7EB"
        cad=f"{rr['cadence_spm']:.0f}" if pd.notna(rr.get('cadence_spm')) else "--"
        hr=f"{rr['avg_hr']:.0f}" if ('avg_hr' in rr.index and pd.notna(rr.get('avg_hr'))) else "--"
        st.markdown(f"<div class='row' style='border-left:3px solid {acc};'><div><div class='nm'>{rr['name']}</div><div class='meta'>{rr['Category_Custom'].upper()} · {rr['Date_Parsed'].strftime('%d %b %Y')}</div></div><div class='stats'><div class='stat'><div class='n'>{rr['distance_km']:.2f}</div><div class='u'>KM</div></div><div class='stat'><div class='n'>{rr['moving_time_hms']}</div><div class='u'>TIME</div></div><div class='stat'><div class='n'>{rr['pace_str']}</div><div class='u'>/KM</div></div><div class='stat'><div class='n'>{cad}</div><div class='u'>SPM</div></div><div class='stat'><div class='n'>{hr}</div><div class='u'>HR</div></div></div></div>", unsafe_allow_html=True)

st.markdown(f"""<div class="footer">
  <span>STRIDE · STRAVA · GARMIN · NIKE RUN CLUB</span>
  <span>DETAIL — JAN 2024 ONWARD · DATA THROUGH {df['Date_Parsed'].max().strftime('%d %b %Y').upper()}</span>
</div>""", unsafe_allow_html=True)
