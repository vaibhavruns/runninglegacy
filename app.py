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
@import url('https://fonts.googleapis.com/css2?family=Saira:wght@500;600;700;800;900&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap');
:root{
  --bg:#0a0d13; --surface:#10151e; --line:#1c2634; --line-hi:#2a3647;
  --ink:#f3f6fa; --ink-2:#9aa7b8; --muted:#5f6b7e;
  --accent:#ccff00; --cyan:#00f0ff; --mint:#34e5c4; --red:#ff4757;
  --r:10px; --r-sm:6px;
}
.stApp{ background:var(--bg)!important; color:var(--ink-2)!important; font-family:'Inter',system-ui,sans-serif!important; animation:fadeUp .5s ease both; }
html,body,[data-testid="stMarkdownContainer"] p,p,label,.stSelectbox div{ color:var(--ink-2)!important; }
.block-container{ padding-top:2.4rem!important; max-width:1180px; }

h1,h2,h3,h4,h5,h6{ font-family:'Saira',system-ui,sans-serif!important; color:var(--ink)!important; }
h1{ font-weight:900!important; text-transform:uppercase!important; letter-spacing:-.5px!important; line-height:.98!important; }
h2,h3{ font-weight:700!important; letter-spacing:.2px!important; text-transform:none!important; }
strong{ color:var(--ink)!important; }

div[data-testid="stTabs"] div[role="tablist"]{ gap:2px; flex-wrap:wrap; border-bottom:1px solid var(--line); }
div[data-testid="stTabs"] button{ font-family:'Saira',sans-serif!important; font-size:.9rem!important; font-weight:700!important; text-transform:uppercase!important; letter-spacing:1px!important; color:var(--muted)!important; padding:13px 20px!important; border-bottom:2px solid transparent!important; transition:color .18s ease,border-color .18s ease; }
div[data-testid="stTabs"] button:hover{ color:var(--ink-2)!important; }
div[data-testid="stTabs"] button[aria-selected="true"]{ color:var(--accent)!important; border-bottom:2px solid var(--accent)!important; background:transparent!important; }

.ticker-wrap{ background:#06080c; padding:13px 16px; border-radius:var(--r-sm); margin-bottom:28px; border-left:3px solid var(--accent); }

.kpi-container{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:14px; margin-bottom:30px; }
.kpi-card{ background:var(--surface); padding:22px; border-radius:var(--r); border:1px solid var(--line); transition:transform .18s ease,border-color .18s ease; }
.kpi-card:hover{ transform:translateY(-2px); border-color:var(--line-hi); }
.kpi-card.accent{ border-color:rgba(204,255,0,.35); }
.kpi-value{ font-family:'JetBrains Mono',ui-monospace,monospace; font-size:2rem; font-weight:700; color:var(--ink)!important; line-height:1; font-feature-settings:"tnum" 1; letter-spacing:-1px; }
.kpi-card.accent .kpi-value{ color:var(--accent)!important; }
.kpi-label{ font-size:.68rem; color:var(--muted)!important; text-transform:uppercase; letter-spacing:1.6px; margin-top:10px; font-weight:600; }
.kpi-sub{ font-size:.66rem; color:var(--muted)!important; font-family:'JetBrains Mono',ui-monospace,monospace; margin-top:5px; }

.chart-container-box{ background:var(--surface)!important; border:1px solid var(--line)!important; border-radius:var(--r)!important; padding:22px!important; margin-bottom:14px!important; transition:border-color .18s ease; }
.chart-container-box:hover{ border-color:var(--line-hi)!important; }
.chart-container-box h3{ font-size:1.12rem!important; margin:0 0 4px!important; }

.section-h{ font-family:'Saira',sans-serif; color:var(--ink); font-weight:800; letter-spacing:.3px; font-size:1.35rem; margin:10px 0 16px; }

.timeline{ border-left:1px solid var(--line); margin:6px 0 24px 10px; padding-left:26px; }
.tl-item{ position:relative; margin-bottom:24px; }
.tl-item:before{ content:''; position:absolute; left:-32px; top:4px; width:11px; height:11px; border-radius:50%; background:var(--muted); }
.tl-item.full:before{ background:var(--accent); box-shadow:0 0 0 4px rgba(204,255,0,.12); }
.tl-year{ color:var(--muted); font-family:'JetBrains Mono',ui-monospace,monospace; font-weight:700; font-size:.74rem; letter-spacing:1.5px; }
.tl-title{ font-family:'Saira',sans-serif; color:var(--ink); font-weight:700; font-size:1.16rem; margin:2px 0 4px; }
.tl-desc{ color:var(--ink-2); font-size:.86rem; line-height:1.55; }

.blurb{ background:var(--surface); border-left:3px solid var(--accent); border-radius:var(--r); padding:22px 24px; margin:4px 0 26px; line-height:1.7; color:#cbd5e1; }
.blurb b{ color:var(--ink); }

.pb-grid{ display:grid; grid-template-columns:repeat(auto-fit,minmax(190px,1fr)); gap:14px; margin-bottom:26px; }
.pb-card{ background:var(--surface); border:1px solid var(--line); border-radius:var(--r); padding:22px; transition:transform .18s ease,border-color .18s ease; }
.pb-card:hover{ transform:translateY(-2px); border-color:var(--line-hi); }
.pb-dist{ font-size:.7rem; color:var(--accent); font-weight:700; letter-spacing:2px; font-family:'JetBrains Mono',ui-monospace,monospace; }
.pb-time{ font-size:2.1rem; font-weight:700; color:var(--ink); font-family:'JetBrains Mono',ui-monospace,monospace; line-height:1.05; margin-top:8px; font-feature-settings:"tnum" 1; letter-spacing:-1px; }
.pb-meta{ font-size:.68rem; color:var(--muted); font-family:'JetBrains Mono',ui-monospace,monospace; margin-top:9px; }

.race-row{ padding:15px 20px; border-radius:var(--r-sm); margin-bottom:10px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; }
.flashcard-row-base{ border:1px solid var(--line); border-radius:var(--r-sm); padding:14px 18px; margin-bottom:10px; display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:12px; background:var(--surface); transition:border-color .18s ease; }
.flashcard-row-base:hover{ border-color:var(--line-hi); }
.fm-group{ display:flex; align-items:center; gap:22px; flex-wrap:wrap; }
.fm{ text-align:center; min-width:58px; }
.fm-val{ font-size:1rem; font-weight:700; color:var(--ink); font-family:'JetBrains Mono',ui-monospace,monospace; font-feature-settings:"tnum" 1; }
.fm-lbl{ font-size:.58rem; color:var(--muted); text-transform:uppercase; letter-spacing:.6px; margin-top:3px; }

@keyframes fadeUp{ from{opacity:0; transform:translateY(8px);} to{opacity:1; transform:none;} }
*:focus-visible{ outline:2px solid var(--accent)!important; outline-offset:2px; }
@media (prefers-reduced-motion:reduce){ *{ animation:none!important; transition:none!important; } }

@media (max-width:640px){
  h1{ font-size:2rem!important; }
  .block-container{ padding-top:1.6rem!important; }
  div[data-testid="stTabs"] button{ font-size:.78rem!important; padding:9px 11px!important; letter-spacing:.5px!important; }
  .kpi-value{ font-size:1.7rem; } .pb-time{ font-size:1.8rem; }
  .kpi-card,.pb-card,.chart-container-box{ padding:17px!important; }
  .flashcard-row-base,.race-row{ gap:10px!important; }
  .flashcard-row-base > div:first-child,.race-row > div:first-child{ min-width:100%!important; }
  .fm-group{ gap:14px!important; width:100%; justify-content:flex-start; }
  .fm{ min-width:46px; }
}
</style>
""", unsafe_allow_html=True)

STATIC={"staticPlot":True,"displayModeBar":False,"responsive":True}
def SHOW(fig,height=320):
    fig.update_layout(height=height); st.plotly_chart(fig,use_container_width=True,config=STATIC)
CHART=dict(template="plotly_dark",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=8,r=12,t=22,b=8),font=dict(family="Inter, sans-serif",size=12,color="#9aa7b8"),
    showlegend=False,colorway=[LIME,CYAN,MINT,RED,"#9aa7b8","#7c5cff"])
def grid(fig):
    fig.update_layout(**CHART)
    fig.update_xaxes(showgrid=False,title_text="",tickfont=dict(color="#5f6b7e"),linecolor="rgba(28,38,52,.8)")
    fig.update_yaxes(showgrid=True,gridcolor="rgba(28,38,52,.55)",zeroline=False,title_text="",tickfont=dict(color="#5f6b7e")); return fig
DISCLAIMER=("Yearly volume &amp; the monthly heatmap blend a <b style='color:#94a3b8;'>Nike Run Club archive (2021\u20132023)</b> "
            "with <b style='color:#94a3b8;'>per-run Strava &amp; Garmin (2024+)</b> \u2014 never summed for the same period. "
            "Detailed per-run charts use Strava/Garmin only, so they thin out before 2024.")
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
    "Chandigarh":(30.73,76.78),"Berlin":(52.51,13.40),"Plitvicka jezera":(44.88,15.62),"Dubrovnik":(42.64,18.11),
    "Chennai":(13.08,80.27),"Pune":(18.52,73.86),"Hyderabad":(17.39,78.49),"Ahmedabad":(23.02,72.57),
    "Jaipur":(26.91,75.79),"Goa":(15.30,74.12),"Nashik":(19.99,73.79),"Lonavala":(18.75,73.41),
    "Rishikesh":(30.09,78.27),"Dehradun":(30.32,78.03),"Shimla":(31.10,77.17),"Manali":(32.24,77.19),
    "Nainital":(29.38,79.46),"Kochi":(9.93,76.27),"Thane":(19.22,72.97),"Navi Mumbai":(19.03,73.03),
    "Lucknow":(26.85,80.95),"Indore":(22.72,75.86),"Nagpur":(21.15,79.09),"Coimbatore":(11.02,76.96),
    "London":(51.51,-0.13),"Dubai":(25.20,55.27),"Singapore":(1.35,103.82)}
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
    # richer Garmin per-activity (location by DATE = robust; power/load by minute key)
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
    # user-controlled overrides (locations.csv: date,city) win over everything
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
    # Nike Run Club monthly archive (2021-2023). Kept SEPARATE from the Strava
    # activities.csv spine - monthly summaries only, never merged per-run.
    p=next((x for x in ["nrc_monthly.csv","data/nrc_monthly.csv"] if os.path.exists(x)),None)
    if not p: return None
    n=pd.read_csv(p); n["year"]=n["year"].astype(int)
    n["mn"]=pd.to_datetime(n["month_start"]).dt.month
    return n

def best_effort(runs,lo,hi):
    b=runs[(runs["distance_km"]>=lo)&(runs["distance_km"]<=hi)&(runs["moving_time_s"]>0)]
    return None if b.empty else b.loc[b["moving_time_s"].idxmin()]
PB_BANDS=[("5K",4.9,5.3),("10K",9.7,10.6),("HALF",20.9,21.6),("FULL",41.9,43.5)]

df=load_data(); daily=load_daily(_sig=(os.path.getmtime("daily_metrics.csv") if os.path.exists("daily_metrics.csv") else 0)); PROFILE=load_profile(); ZONES=load_zones(); NRC=load_nrc()
NRC_CUTOFF=2024  # NRC monthly archive authoritative before this year; Strava per-run from this year on
def annual_volume(runs):
    # Blended TRUE yearly volume: NRC archive for pre-2024, Strava per-run for 2024+.
    # Each year is sourced from exactly one layer, so the two are never double-counted.
    sv=runs.groupby("year")["distance_km"].sum(); svn=runs.groupby("year").size()
    years=set(int(y) for y in sv.index)
    if NRC is not None: years|=set(int(y) for y in NRC["year"].unique())
    rows=[]
    for y in sorted(years):
        if y<NRC_CUTOFF and NRC is not None and (NRC["year"]==y).any():
            sub=NRC[NRC["year"]==y]; rows.append({"year":y,"km":float(sub["total_km"].sum()),"runs":int(sub["num_runs"].sum()),"source":"NRC"})
        else:
            rows.append({"year":y,"km":float(sv.get(y,0.0)),"runs":int(svn.get(y,0)),"source":"Strava"})
    return pd.DataFrame(rows)
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
_last=df["Date_Parsed"].max(); _nr=int((df["sport_type"]=="Run").sum())
st.markdown(f"<p style='color:#475569;font-size:.72rem;font-family:monospace;letter-spacing:1px;margin:-10px 0 16px;'>DATA CURRENT THROUGH {_last.strftime('%d %b %Y').upper()} &nbsp;\u00b7&nbsp; {_nr} RUNS LOADED</p>", unsafe_allow_html=True)

with st.expander("CONTROL CENTER  //  FILTERS", expanded=False):
    c1,c2,c3=st.columns(3)
    with c1:
        years=["ALL TIME"]+[str(y) for y in sorted(df["year"].unique(),reverse=True)]; sel_year=st.selectbox("YEAR",years,index=1 if len(years)>1 else 0)
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
      <div class="kpi-card"><div class="kpi-value">{int(annual_volume(runs_all)['km'].sum()):,}<span style='font-size:.9rem;'> KM</span></div><div class="kpi-label">// LIFETIME DISTANCE</div><div class="kpi-sub">NRC + Strava</div></div>
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
        fig.update_geos(projection_type="equirectangular",showland=True,landcolor="#1a2230",showcountries=True,countrycolor="#5a6b85",
            countrywidth=0.8,showocean=True,oceancolor="#0b0e14",showcoastlines=True,coastlinecolor="#5a6b85",coastlinewidth=0.8,
            bgcolor="rgba(0,0,0,0)",lakecolor="#0b0e14",framecolor="#2b3850",lataxis_range=[6,60],lonaxis_range=[5,98])
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",margin=dict(l=0,r=0,t=0,b=0),height=440)
        st.plotly_chart(fig,use_container_width=True,config=STATIC)
        chips="".join(f"<span style='display:inline-block;background:#161d2a;border:1px solid #1e293b;border-radius:20px;padding:5px 13px;margin:4px 6px 0 0;font-size:.74rem;'><b style='color:#ccff00;'>{x['loc']}</b> <span style='color:#64748b;font-family:monospace;'>{int(x['km'])} km</span></span>" for _,x in cv.sort_values('km',ascending=False).iterrows())
        st.markdown(f"<div style='margin-top:10px;'>{chips}</div></div>", unsafe_allow_html=True)
    def _fd(cols):
        if daily is None: return None
        d=daily.dropna(subset=cols)
        if sel_year!="ALL TIME": d=d[d["year"]==int(sel_year)]
        return d.sort_values("date")
    def _scope(key,default=0):
        # compact per-chart distance filter for run-based charts (mobile-friendly single row)
        opt=st.radio("Distance filter",["All","5K+","10K+","HM+"],horizontal=True,index=default,key="scope_"+key)
        return {"All":0.0,"5K+":5.0,"10K+":10.0,"HM+":21.0}[opt]
    def _smooth(key,base=14):
        opt=st.radio("Smoothing",["Raw","Smooth","Smoother"],horizontal=True,index=1,key="sm_"+key)
        return {"Raw":1,"Smooth":int(base),"Smoother":int(base*2)}[opt]
    def _rmean(s,w):
        mp=1 if w<=1 else max(2,w//4); return s.rolling(w,min_periods=mp).mean()
    def _trend(d,col,color,title,hline=None,hlbl=""):
        st.markdown(f'<div class="chart-container-box"><h3>{title}</h3>', unsafe_allow_html=True)
        w=_smooth("trend_"+col)
        fig=go.Figure(); fig.add_trace(go.Scatter(x=d["date"],y=d[col],mode="markers",marker=dict(color=MUTE,size=4)))
        fig.add_trace(go.Scatter(x=d["date"],y=_rmean(d[col],w),mode="lines",line=dict(color=color,width=2.5)))
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
        w=_smooth("hrv")
        fig=go.Figure(); fig.add_trace(go.Scatter(x=d["date"],y=d["hrv_overnight_ms"],mode="markers",marker=dict(color=MUTE,size=4)))
        fig.add_trace(go.Scatter(x=d["date"],y=_rmean(d["hrv_overnight_ms"],w),mode="lines",line=dict(color=LIME,width=2.5)))
        SHOW(grid(fig)); st.markdown("</div>",unsafe_allow_html=True)
    def c_sleep():
        d=_fd(["sleep_total_min"]);
        if d is None or d.empty: st.info("No sleep data in this filter."); return
        # ---- Chart 1: Sleep Score (single axis, 7-night rolling average) ----
        if "sleep_score" in d and d["sleep_score"].notna().any():
            s=d.dropna(subset=["sleep_score"])
            st.markdown('<div class="chart-container-box"><h3>Sleep Score</h3>', unsafe_allow_html=True)
            fig=go.Figure()
            fig.add_trace(go.Scatter(x=s["date"],y=s["sleep_score"],mode="markers",marker=dict(color=MUTE,size=3,opacity=.35),hovertemplate="%{y:.0f}<extra></extra>"))
            fig.add_trace(go.Scatter(x=s["date"],y=s["sleep_score"].rolling(7,min_periods=3).mean(),mode="lines",line=dict(color=LIME,width=2.5),hovertemplate="%{y:.0f}<extra></extra>"))
            fig.add_hrect(y0=80,y1=100,fillcolor="rgba(204,255,0,.06)",line_width=0)
            fig=grid(fig); fig.update_yaxes(range=[0,100]); SHOW(fig,300); st.markdown("</div>",unsafe_allow_html=True)
        # ---- Chart 2: Sleep stage composition in hours (stacked, 7-night avg) ----
        st.markdown('<div class="chart-container-box"><h3>Sleep Stages (hrs)</h3>', unsafe_allow_html=True)
        fig=go.Figure()
        for col,nm,clr in [("sleep_deep_min","Deep","#1e40af"),("sleep_rem_min","REM",CYAN),("sleep_light_min","Light","#334155")]:
            if col in d:
                hrs=(d[col]/60).rolling(7,min_periods=3).mean()
                fig.add_trace(go.Scatter(x=d["date"],y=hrs,mode="lines",stackgroup="s",name=nm,
                    line=dict(width=0,color=clr),fillcolor=clr,hovertemplate=nm+": %{y:.1f}h<extra></extra>"))
        fig=grid(fig); fig.update_layout(showlegend=True,legend=dict(orientation="h",y=1.18,x=0,font=dict(color=MUTE)))
        fig.update_yaxes(title_text="hours"); SHOW(fig,300); st.markdown("</div>",unsafe_allow_html=True)
    def c_ready():
        d=_fd(["readiness_score"]);
        if d is None or d.empty: st.info("No readiness data in this filter."); return
        _trend(d,"readiness_score",MINT,"Training Readiness")
    def c_acwr():
        # Rebuild ACWR on a CONTINUOUS daily timeline so rest-day gaps don't
        # collapse the ratio to ~0 and create false spikes. Prefer recomputing
        # from acute/chronic load; fall back to smoothing the raw acwr column.
        if daily is None: st.info("No load data in this filter."); return
        base=daily.copy()
        if sel_year!="ALL TIME": base=base[base["year"]==int(sel_year)]
        if base.empty: st.info("No load data in this filter."); return
        g=base[["date","acute_load","chronic_load","acwr"]].dropna(subset=["date"]).sort_values("date").set_index("date")
        g=g.resample("D").mean()
        if g[["acute_load","chronic_load"]].notna().any().all():
            ac=g["acute_load"].ffill(); ch=g["chronic_load"].ffill()
            ratio=(ac/ch).replace([float("inf"),float("-inf")],pd.NA)
        else:
            ratio=g["acwr"].ffill()
        ratio=ratio.rolling(7,min_periods=3).mean()
        d=ratio.dropna().reset_index(); d.columns=["date","acwr"]
        if d.empty: st.info("No load data in this filter."); return
        st.markdown('<div class="chart-container-box"><h3>Acute : Chronic Load (ACWR)</h3>', unsafe_allow_html=True)
        fig=go.Figure(); fig.add_hrect(y0=0.8,y1=1.3,fillcolor="rgba(52,229,196,.10)",line_width=0)
        fig.add_trace(go.Scatter(x=d["date"],y=d["acwr"],mode="lines",line=dict(color=LIME,width=2.5),hovertemplate="%{y:.2f}<extra></extra>"))
        fig.add_hline(y=1.5,line_dash="dash",line_color=RED,annotation_text="injury-risk 1.5",annotation_font_color=RED)
        fig=grid(fig); fig.update_yaxes(range=[0,2]); SHOW(fig); st.markdown("</div>",unsafe_allow_html=True)
    def c_preds():
        d=_fd(["pred_marathon_s"]);
        if d is None or d.empty: st.info("No race-prediction data in this filter."); return
        st.markdown('<div class="chart-container-box"><h3>Garmin Race Predictions</h3>', unsafe_allow_html=True)
        alld=[("pred_5k_s","5K","#64748b"),("pred_10k_s","10K",CYAN),("pred_half_s","Half",MINT),("pred_marathon_s","Marathon",LIME)]
        pick=st.multiselect("Distances",[nm for _,nm,_ in alld],default=[nm for _,nm,_ in alld],key="preds_pick")
        fig=go.Figure()
        for col,nm,clr in alld:
            if nm in pick and col in d:
                fig.add_trace(go.Scatter(x=d["date"],y=_rmean(d[col]/60,7),mode="lines",name=nm,line=dict(color=clr,width=2.5),
                    hovertemplate=nm+": %{y:.0f} min<extra></extra>"))
        fig=grid(fig); fig.update_yaxes(title_text="predicted minutes")
        fig.update_layout(showlegend=True,legend=dict(orientation="h",y=1.15,font=dict(color=MUTE))); SHOW(fig,360); st.markdown("</div>",unsafe_allow_html=True)
    def c_power():
        base=runs_f[runs_f["avg_power"].notna()] if "avg_power" in runs_f.columns else runs_f.iloc[0:0]
        if base.empty: st.info("No running-power data in this filter."); return
        st.markdown('<div class="chart-container-box"><h3>Running Power</h3>', unsafe_allow_html=True)
        lo=_scope("power")
        d=base[base["distance_km"]>=lo].sort_values("Date_Parsed")
        if d.empty: st.info("No runs match this distance filter."); st.markdown("</div>",unsafe_allow_html=True); return
        fig=go.Figure(); fig.add_trace(go.Scatter(x=d["Date_Parsed"],y=d["avg_power"],mode="markers",marker=dict(color=MUTE,size=4)))
        fig.add_trace(go.Scatter(x=d["Date_Parsed"],y=_rmean(d["avg_power"],10),mode="lines",line=dict(color="#ffb020",width=2.5)))
        SHOW(grid(fig)); st.markdown("</div>",unsafe_allow_html=True)
    def c_weekly():
        st.markdown('<div class="chart-container-box"><h3>Weekly Mileage</h3>', unsafe_allow_html=True)
        wk=runs_f.set_index("Date_Parsed")["distance_km"].resample("W-MON").sum().reset_index()
        if sel_year=="ALL TIME": wk=wk.tail(52)
        fig=px.bar(wk,x="Date_Parsed",y="distance_km"); fig.update_traces(marker_color=CYAN); SHOW(grid(fig)); st.markdown("</div>",unsafe_allow_html=True)
    def c_pace():
        st.markdown('<div class="chart-container-box"><h3>Pace Trend</h3>', unsafe_allow_html=True)
        lo=_scope("pace")
        p=runs_f[(runs_f["pace_min_per_km"].notna())&(runs_f["distance_km"]>=max(3.0,lo))].sort_values("Date_Parsed")
        if p.empty: st.info("No runs match this distance filter."); st.markdown("</div>",unsafe_allow_html=True); return
        fig=go.Figure(); fig.add_trace(go.Scatter(x=p["Date_Parsed"],y=p["pace_min_per_km"],mode="markers",marker=dict(color=MUTE,size=5)))
        fig.add_trace(go.Scatter(x=p["Date_Parsed"],y=_rmean(p["pace_min_per_km"],10),mode="lines",line=dict(color=LIME,width=2.5)))
        fig=grid(fig); fig.update_yaxes(autorange="reversed",title_text="min/km (faster=up)"); SHOW(fig); st.markdown("</div>",unsafe_allow_html=True)
    def c_cad():
        st.markdown('<div class="chart-container-box"><h3>Cadence Trend</h3>', unsafe_allow_html=True)
        lo=_scope("cad")
        cc=runs_f[(runs_f["cadence_spm"].notna())&(runs_f["cadence_spm"]>120)&(runs_f["distance_km"]>=lo)].sort_values("Date_Parsed")
        if cc.empty: st.info("No runs match this distance filter."); st.markdown("</div>",unsafe_allow_html=True); return
        fig=go.Figure(); fig.add_trace(go.Scatter(x=cc["Date_Parsed"],y=cc["cadence_spm"],mode="markers",marker=dict(color=MUTE,size=5)))
        fig.add_trace(go.Scatter(x=cc["Date_Parsed"],y=_rmean(cc["cadence_spm"],10),mode="lines",line=dict(color=CYAN,width=2.5)))
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
        av=annual_volume(runs_all)
        if sel_year!="ALL TIME": av=av[av["year"]==int(sel_year)]
        if av.empty: st.info("No volume data in this filter."); st.markdown("</div>",unsafe_allow_html=True); return
        av["yr"]=av["year"].astype(str)
        fig=px.bar(av,x="yr",y="km",text_auto=".0f",color="yr",color_discrete_map=YEAR_COLORS)
        nrc_years=set(av[av["source"]=="NRC"]["yr"])
        for tr in fig.data:
            if tr.name in nrc_years: tr.marker.pattern=dict(shape="/",solidity=0.55,fgcolor="#0a0d13")
        fig=grid(fig); fig.update_layout(showlegend=False); fig.update_yaxes(title_text="km"); fig.update_xaxes(title_text="")
        SHOW(fig); st.markdown("</div>",unsafe_allow_html=True)
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
        sv=runs_all.copy(); sv["mn"]=sv["Date_Parsed"].dt.month
        piv=sv[sv["year"]>=NRC_CUTOFF].pivot_table(index="year",columns="mn",values="distance_km",aggfunc="sum")
        if NRC is not None:
            npv=NRC[NRC["year"]<NRC_CUTOFF].pivot_table(index="year",columns="mn",values="total_km",aggfunc="sum")
            piv=pd.concat([piv,npv])
        piv=piv.groupby(level=0).sum().reindex(columns=range(1,13)).fillna(0).sort_index()
        if sel_year!="ALL TIME": piv=piv[piv.index==int(sel_year)]
        if piv.empty: st.info("No volume data in this filter."); st.markdown("</div>",unsafe_allow_html=True); return
        piv.index=piv.index.astype(int); piv.columns=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        fig=px.imshow(piv,text_auto=".0f",aspect="auto",color_continuous_scale=[[0,"#121721"],[.5,"#1e6b6b"],[1,LIME]])
        fig.update_layout(**{k:v for k,v in CHART.items() if k!="showlegend"}); fig.update_coloraxes(showscale=False); SHOW(fig,300); st.markdown("</div>",unsafe_allow_html=True)
    def c_hrtrend():
        if runs_f[runs_f["avg_hr"].notna()].empty: st.info("No HR data in this filter."); return
        st.markdown('<div class="chart-container-box"><h3>Heart Rate Trend</h3>', unsafe_allow_html=True)
        lo=_scope("hrtrend")
        h=runs_f[(runs_f["avg_hr"].notna())&(runs_f["distance_km"]>=lo)].sort_values("Date_Parsed")
        if h.empty: st.info("No runs match this distance filter."); st.markdown("</div>",unsafe_allow_html=True); return
        fig=go.Figure(); fig.add_trace(go.Scatter(x=h["Date_Parsed"],y=h["max_hr"],mode="markers",marker=dict(color="#3a2230",size=4)))
        fig.add_trace(go.Scatter(x=h["Date_Parsed"],y=h["avg_hr"],mode="markers",marker=dict(color=MUTE,size=5)))
        fig.add_trace(go.Scatter(x=h["Date_Parsed"],y=_rmean(h["avg_hr"],10),mode="lines",line=dict(color=RED,width=2.5)))
        SHOW(grid(fig)); st.markdown("</div>",unsafe_allow_html=True)
    def c_eff():
        h=runs_f[runs_f["avg_hr"].notna()].copy()
        if h.empty: st.info("No HR data in this filter."); return
        st.markdown('<div class="chart-container-box"><h3>Aerobic Efficiency</h3>', unsafe_allow_html=True)
        lo=_scope("eff",default=1)
        h["mpb"]=(h["distance_km"]*1000)/(h["avg_hr"]*(h["moving_time_s"]/60.0)); e=h[h["distance_km"]>=max(1.0,lo)].sort_values("Date_Parsed")
        if e.empty: st.info("No runs match this distance filter."); st.markdown("</div>",unsafe_allow_html=True); return
        fig=go.Figure(); fig.add_trace(go.Scatter(x=e["Date_Parsed"],y=e["mpb"],mode="markers",marker=dict(color=MUTE,size=5)))
        fig.add_trace(go.Scatter(x=e["Date_Parsed"],y=_rmean(e["mpb"],8),mode="lines",line=dict(color=LIME,width=2.5)))
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
        if runs_f[(runs_f["avg_hr"].notna())&(runs_f["pace_min_per_km"].notna())].empty: st.info("No HR data in this filter."); return
        st.markdown('<div class="chart-container-box"><h3>Pace vs Heart Rate</h3>', unsafe_allow_html=True)
        lo=_scope("pacehr")
        h=runs_f[(runs_f["avg_hr"].notna())&(runs_f["pace_min_per_km"].notna())&(runs_f["distance_km"]>=lo)]
        if h.empty: st.info("No runs match this distance filter."); st.markdown("</div>",unsafe_allow_html=True); return
        fig=px.scatter(h,x="avg_hr",y="pace_min_per_km",color="year",color_discrete_map=YEAR_COLORS)
        fig=grid(fig); fig.update_yaxes(autorange="reversed",title_text="pace min/km"); fig.update_xaxes(title_text="avg HR")
        fig.update_layout(showlegend=True,legend=dict(orientation="h",y=1.15,font=dict(color=MUTE))); SHOW(fig); st.markdown("</div>",unsafe_allow_html=True)
    def dyn(col,title,color,target=None):
        if runs_f[runs_f[col].notna()].empty: st.info("No running-dynamics data in this filter."); return
        st.markdown(f'<div class="chart-container-box"><h3>{title}</h3>', unsafe_allow_html=True)
        lo=_scope("dyn_"+col)
        d=runs_f[(runs_f[col].notna())&(runs_f["distance_km"]>=lo)].sort_values("Date_Parsed")
        if d.empty: st.info("No runs match this distance filter."); st.markdown("</div>",unsafe_allow_html=True); return
        fig=go.Figure(); fig.add_trace(go.Scatter(x=d["Date_Parsed"],y=d[col],mode="markers",marker=dict(color=MUTE,size=4)))
        fig.add_trace(go.Scatter(x=d["Date_Parsed"],y=_rmean(d[col],10),mode="lines",line=dict(color=color,width=2.5)))
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
        "Trends \u00b7 Volume by Year": c_yoy,
        "Trends \u00b7 Weekly Mileage": c_weekly,
        "Trends \u00b7 Pace Trend": c_pace,
        "Trends \u00b7 Distance Mix": c_mix,
        "Patterns \u00b7 Day of Week": c_dow,
        "Patterns \u00b7 Monthly Heatmap": c_heat,
        "Heart \u00b7 Heart Rate Trend": c_hrtrend,
        "Heart \u00b7 Aerobic Efficiency": c_eff,
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
        "Engine \u00b7 Sleep":"Two views, both smoothed as a 7-night average. <b>Sleep Score</b> is Garmin's nightly 0\u2013100 rating (80+ band shaded) \u2014 the recovery foundation everything else sits on. <b>Sleep Stages</b> breaks each night into deep, REM and light hours, stacked to show total sleep and its composition.",
        "Engine \u00b7 Training Readiness":"Garmin's daily 0\u2013100 readiness score \u2014 how prepared your body is to train hard, blending sleep, HRV, recovery time and recent load.",
        "Load \u00b7 Garmin ACWR":"Recent (acute) load versus your baseline (chronic) load, computed on a continuous daily timeline and 7-day smoothed so rest days don't create false spikes. The green 0.8\u20131.3 band builds fitness safely; sustained time above ~1.5 (red line) is the classic injury-risk zone \u2014 worth watching given your knee history.",
        "Performance \u00b7 Race Predictions":"Garmin's predicted finish times over two years, each a 7-day average so the daily noise drops out. Watch the marathon line \u2014 fitness gained into Berlin and the dip through the knee rebuild.",
        "Performance \u00b7 Running Power":"Running power in watts per run \u2014 effort that's independent of pace, hills and wind. Steady or rising output at the same feel signals improving strength.",
        "Trends \u00b7 Weekly Mileage":"Total distance run each week. Training blocks, taper weeks and breaks all show up at a glance.",
        "Trends \u00b7 Pace Trend":"Average pace of every run over time (faster sits higher). The line is a 10-run rolling average showing the direction of your speed.",
        "Trends \u00b7 Volume by Year":"Total kilometres per calendar year. 2021\u20132023 come from your Nike Run Club archive (hatched bars); 2024 on is per-run Strava/Garmin. Strava badly under-counted the early years, so this is the truer growth curve \u2014 2022 was a ~770 km year, not the ~340 Strava alone showed.",
        "Trends \u00b7 Distance Mix":"How your runs split across distance buckets \u2014 how much is short and easy versus long efforts.",
        "Patterns \u00b7 Day of Week":"Which days you run most, by distance \u2014 your weekly rhythm and long-run day.",
        "Patterns \u00b7 Monthly Heatmap":"Distance per month across the years; brighter cells are bigger months. Pre-2024 months come from the Nike Run Club archive, 2024+ from Strava/Garmin \u2014 so your real 2022 base block finally shows.",
        "Heart \u00b7 Heart Rate Trend":"Average and max HR per run over time. The average trending down at similar paces is a clean sign of improving fitness.",
        "Heart \u00b7 Aerobic Efficiency":"Metres covered per heartbeat on 5 km+ runs. Rising = the same speed at lower cardiac cost \u2014 pure aerobic gains.",
        "Heart \u00b7 Pace vs Heart Rate":"Each run plotted as pace against heart rate, coloured by year. Points drifting down-and-left over the years mean faster at the same effort.",
        "Dynamics \u00b7 Cadence (FIT)":"Garmin's measured steps per minute against the 174 target \u2014 a cleaner signal than the Strava-derived cadence.",
        "Dynamics \u00b7 Ground Contact Time":"How long each foot stays on the ground (ms). Quicker contact is generally more economical.",
        "Dynamics \u00b7 Vertical Oscillation":"How much you bounce vertically each stride (mm). Less bounce means less energy wasted going up instead of forward.",
        "Dynamics \u00b7 Stride Length":"Average distance covered per step \u2014 tends to grow as fitness and speed improve.",
        "Dynamics \u00b7 Vertical Ratio":"Vertical bounce as a percentage of stride length \u2014 the single best running-economy number. Lower is better.",
    }
    cats=[]
    for k in CHARTS:
        c=k.split(" \u00b7 ")[0]
        if c not in cats: cats.append(c)
    cat=st.selectbox("SELECT CATEGORY", cats)
    for k in CHARTS:
        if k.split(" \u00b7 ")[0]!=cat: continue
        CHARTS[k]()
        st.markdown(f"<p style='color:#64748b;font-size:.82rem;line-height:1.6;letter-spacing:0;text-transform:none;margin:2px 0 22px;'><b style='color:#94a3b8;'>What this shows \u2014 </b>{CAPTIONS.get(k,'')}</p>", unsafe_allow_html=True)

# ===== ACTIVITY LOG =====
with t_log:
    st.markdown("<div class='section-h'>ACTIVITY LOG</div>", unsafe_allow_html=True)
    log_df=f.sort_values("Date_Parsed",ascending=False)
    show_all=st.checkbox(f"Show all {len(log_df)} activities",value=False) if len(log_df)>20 else True
    rows=log_df if show_all else log_df.head(20)
    for _,r in rows.iterrows():
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
