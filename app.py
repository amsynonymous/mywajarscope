"""MyWajarScope — MDIT 2026 (SDG 8) district dashboard, bilingual (English / Bahasa Melayu).
Run locally:  streamlit run app.py
Data: OpenDOSM (household income, poverty, labour force, district GDP) — see About tab.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.model_selection import KFold, cross_val_predict, cross_val_score

from analytics import (brief_html, entropy_topsis, group_profile, peers, percentile_profile,
                       recommend, spearman)
from i18n import TEXT
from smoothmap import build as build_map, view_box

st.set_page_config(page_title="MyWajarScope", page_icon=str(Path(__file__).parent / "assets" / "favicon.png"),
                   layout="wide")

HERE = Path(__file__).parent
DATA = HERE / "data"
st.markdown(f"<style>{(HERE / 'style.css').read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
st.logo(str(HERE / "assets" / "logo_mark.png"), icon_image=str(HERE / "assets" / "icon.png"), size="large")
ICON_B64 = __import__("base64").b64encode((HERE / "assets" / "icon.png").read_bytes()).decode()

CLUSTERS = ["Industrial hub", "Mid-tier town", "Working-poor rural", "Low-income trap"]
CLR = {"Industrial hub": "#14B8A6", "Mid-tier town": "#6366F1",
       "Working-poor rural": "#F59E0B", "Low-income trap": "#F43F5E"}
X_COLS = ["u_rate", "p_rate", "agri_share", "mining_share", "mfg_share",
          "constr_share", "services_share", "log_gdp_per_worker"]
ALL = "All Malaysia"  # internal value for "no state filter"

# ---------- language (top-right toggle) ----------
st.session_state.setdefault("lang_w", "en")
st.session_state.setdefault("lang_last", "en")


def _keep_lang():
    # clicking the already-active flag would clear the choice; keep the last language instead
    if st.session_state.lang_w is None:
        st.session_state.lang_w = st.session_state.lang_last
    st.session_state.lang_last = st.session_state.lang_w


_, lang_col = st.columns([5, 1])
with lang_col:
    st.segmented_control("Language", ["ms", "en"], key="lang_w", label_visibility="collapsed",
                         on_change=_keep_lang, format_func=lambda c: {"ms": "BM", "en": "EN"}[c])
L = TEXT[st.session_state.lang_w or st.session_state.lang_last]
LABELS = L["labels"]


def CL(c):
    """Display name of a cluster in the current language."""
    return L["clusters"][c]


CLR_D = {CL(c): CLR[c] for c in CLUSTERS}
ORDER_D = {"cluster": [CL(c) for c in CLUSTERS]}


def disp(d):
    """Copy of a frame with cluster names translated for charts/tables."""
    return d.assign(cluster=d.cluster.map(CL))


# glass-friendly Plotly theme: transparent canvas, soft grid, app font
pio.templates["glass"] = go.layout.Template(layout=dict(
    font=dict(family="Plus Jakarta Sans, system-ui, sans-serif", color="#334155", size=13),
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    title=dict(font=dict(size=15, color="#0f172a"), x=0, xanchor="left"),
    colorway=list(CLR.values()),
    xaxis=dict(gridcolor="rgba(148,163,184,.18)", zeroline=False, linecolor="rgba(148,163,184,.35)"),
    yaxis=dict(gridcolor="rgba(148,163,184,.18)", zeroline=False, linecolor="rgba(148,163,184,.35)"),
    legend=dict(orientation="h", y=-0.18, title_text="", font=dict(size=12)),
    hoverlabel=dict(bgcolor="rgba(255,255,255,.95)", bordercolor="rgba(99,102,241,.35)",
                    font=dict(family="Plus Jakarta Sans", color="#0f172a")),
    margin=dict(l=10, r=10, t=50, b=10)))
pio.templates.default = "plotly_white+glass"


def card(name, container=st):
    """Glass card: a bordered container tagged with a CSS class via its (stable) key."""
    return container.container(border=True, key=f"glass_{name}")


def chart(fig, name, container=st, animate=True):
    """Plotly chart with a stable key, so Streamlit updates it in place and Plotly
    animates bars/points/lines smoothly to their new values instead of redrawing."""
    fig.update_layout(legend_title_text="", uirevision=name)
    if animate:
        fig.update_layout(transition=dict(duration=700, easing="cubic-in-out"))
    container.plotly_chart(fig, width="stretch", theme=None, key=f"chart_{name}",
                           config={"displayModeBar": False})


def title(text, sub=None):
    st.markdown(f'<div class="section-title">{text}</div>' + (f'<div class="section-sub">{sub}</div>' if sub else ""),
                unsafe_allow_html=True)


def insight(text, icon="💡"):
    st.markdown(f'<div class="glass insight"><div class="icon">{icon}</div><div>{text}</div></div>',
                unsafe_allow_html=True)


def stat(container, label, value):
    container.markdown(f'<div class="glass stat"><div class="label">{label}</div><div class="value pop">{value}</div></div>',
                       unsafe_allow_html=True)


# ---------- data ----------
@st.cache_data
def load():
    df = pd.read_csv(DATA / "dashboard_district_2022.csv")
    df["id"] = df["state"] + "|" + df["district"]
    return df


@st.cache_resource
def train_rf(df):
    X, y = df[X_COLS], np.log(df["inc_med_2022"])
    rf = RandomForestRegressor(n_estimators=400, min_samples_leaf=3, random_state=42)
    kf = KFold(5, shuffle=True, random_state=42)
    cv = cross_val_score(rf, X, y, cv=kf, scoring="r2")
    oof = np.exp(cross_val_predict(rf, X, y, cv=kf))
    rf.fit(X, y)
    pi = permutation_importance(rf, X, y, n_repeats=20, random_state=42)
    return rf, float(cv.mean()), pd.Series(pi.importances_mean, index=X_COLS), oof


def dwgi(d, w):
    if sum(w.values()) == 0:          # every slider at 0: fall back to equal weights instead of dividing by zero
        w = {k: 1.0 for k in w}
    z = lambda s: (s - s.mean()) / s.std()
    raw = (w["income"] * -z(np.log(d.inc_med_2022)) + w["poverty"] * z(d.pov_abs_2022)
           + w["unemp"] * z(d.u_rate) + w["particip"] * -z(d.p_rate)) / max(sum(w.values()), 1e-9)
    span = raw.max() - raw.min()
    return (((raw - raw.min()) / span * 100) if span else raw * 0).round(1)


df_all = load().copy()
rf, cv_r2, importance_raw, oof_pred = train_rf(df_all)

# ---------- sidebar ----------
with st.sidebar:
    st.header(L["filters"])
    # option labels are translated, so each language gets its own widget key; the chosen values
    # live in session_state and carry over when the language is switched
    lang = st.session_state.lang_last
    st.session_state.setdefault("sel_state", ALL)
    st.session_state.setdefault("sel_clusters", list(CLUSTERS))
    states = [ALL] + sorted(df_all.state.unique())
    state = st.selectbox(L["state"], states, index=states.index(st.session_state.sel_state),
                         key=f"f_state_{lang}", format_func=lambda s: L["all_my"] if s == ALL else s,
                         on_change=lambda: st.session_state.update(sel_state=st.session_state[f"f_state_{lang}"]))
    clusters = st.multiselect(L["dtype"], CLUSTERS, default=st.session_state.sel_clusters,
                              key=f"f_clusters_{lang}", format_func=CL,
                              on_change=lambda: st.session_state.update(
                                  sel_clusters=st.session_state[f"f_clusters_{lang}"]))
    st.divider()
    st.header(L["weights"])
    st.caption(L["weights_cap"])
    def _level(v):
        return 0 if v == 0 else 1 if v < 0.8 else 2 if v <= 1.2 else 3 if v < 2 else 4

    w = {}
    for k in ["income", "poverty", "unemp", "particip"]:
        # slider + its explanation live in one box so the explanation can appear on hover only
        with st.container(key=f"wbox_{k}"):
            w[k] = st.slider(L[f"w_{k}"], 0.0, 2.0, 1.0, 0.1, key=f"w_{k}", help=L[f"h_{k}"])
            lv = _level(w[k])
            st.markdown(f'<div class="wlevel"><span class="lvl lvl{lv}">{L["levels"][lv]}</span>'
                        f'<span class="up">↑ {L[f"up_{k}"]}</span></div>', unsafe_allow_html=True)

if sum(w.values()) == 0:
    st.sidebar.warning(L["all_zero"])
df_all["dwgi"] = dwgi(df_all, w)
df_all["dwgi_rank"] = df_all.dwgi.rank(ascending=False, method="min").astype(int)
df_all["topsis"], TOPSIS_W = entropy_topsis(df_all)
df_all["topsis_rank"] = df_all.topsis.rank(ascending=False, method="min").astype(int)
df = df_all[df_all.cluster.isin(clusters)]
if state != ALL:
    df = df[df.state == state]
state_disp = L["all_my"] if state == ALL else state

# ---------- hero + KPIs ----------
hub = df_all[df_all.cluster == "Industrial hub"]
trap = df_all[df_all.cluster == "Low-income trap"]
wpr = df_all[df_all.cluster == "Working-poor rural"]
gap = hub.inc_med_2022.median() - trap.inc_med_2022.median()

st.markdown(f"""
<div class="glass hero">
  <div class="eyebrow">
    <span class="pill live">{L['pill_data']}</span><span class="pill">{L['pill_sdg']}</span>
    <span class="pill">{L['pill_n'].format(n=len(df_all))}</span>
  </div>
  <div class="brand"><img src="data:image/png;base64,{ICON_B64}" alt=""><h1>MyWajarScope</h1></div>
  <p><b>{L['hero_q']}</b> {L['hero_p']}</p>
</div>
<div class="kpis">
  <div class="glass kpi"><div class="label">{L['k1']}</div>
    <div class="value"><span class="count" style="--to:{len(df_all)}"></span></div>
    <div class="sub">{L['k1s']}</div></div>
  <div class="glass kpi"><div class="label"><span class="dot" style="background:{CLR['Low-income trap']}"></span>{L['k2']}</div>
    <div class="value"><span class="count" style="--to:{len(trap)}"></span> {L['k2u']}</div>
    <div class="sub">{L['k2s'].format(n=(trap.state == 'Sabah').sum())}</div></div>
  <div class="glass kpi"><div class="label">{L['k3']}</div>
    <div class="value">RM{gap:,.0f}</div>
    <div class="sub">{L['k3s']}</div></div>
  <div class="glass kpi"><div class="label"><span class="dot" style="background:{CLR['Working-poor rural']}"></span>{L['k4']}</div>
    <div class="value">{wpr.u_rate.mean() - hub.u_rate.mean():+.1f} pp</div>
    <div class="sub">{L['k4s']}</div></div>
</div>
""", unsafe_allow_html=True)

tab_map, tab_profile, tab_types, tab_priority, tab_trend, tab_ai, tab_about = st.tabs(L["tabs"])

# ---------- map ----------
MAP_COMP, MAP_IDS, MAP_BOXES = build_map((DATA / "district.geojson").read_text(encoding="utf-8"))
RED = ["#ffe4e6", "#fda4af", "#f43f5e", "#881337"]
BLUE = ["#e0e7ff", "#a5b4fc", "#6366f1", "#312e81"]
SCALES = {"dwgi": RED, "pov_abs_2022": RED, "u_rate": RED, "inc_med_2022": BLUE, "p_rate": BLUE}


def _ramp(stops, t):
    t = min(max(t, 0.0), 1.0) * (len(stops) - 1)
    i = min(int(t), len(stops) - 2)
    a, b = stops[i].lstrip("#"), stops[i + 1].lstrip("#")
    ca, cb = [int(a[j:j + 2], 16) for j in (0, 2, 4)], [int(b[j:j + 2], 16) for j in (0, 2, 4)]
    f = t - i
    return "#" + "".join(f"{round(x + (y - x) * f):02x}" for x, y in zip(ca, cb))


def map_panel(df_all, state, clusters):
    """Builds colours for every mode at once; the map switches modes in the browser with no server round trip."""
    with card("map"):
        rows = df_all.set_index("id")
        scope = df_all if state == ALL else df_all[df_all.state == state]
        fills = {m: [] for m in L["modes"]}
        op, tips = [], []
        rng = {m: (float(scope[m].min()), float(scope[m].max())) for m in SCALES}
        for pid in MAP_IDS:
            if pid not in rows.index:
                for m in fills:
                    fills[m].append("#e2e8f0")
                op.append(0.45)
                tips.append(f"<b>{pid.split('|')[1]}</b><div class='row'><span>{L['tip_none']}</span></div>")
                continue
            r = rows.loc[pid]
            in_type = r.cluster in clusters
            in_state = state == ALL or r.state == state
            for m in fills:
                if not in_type:
                    fills[m].append("#e2e8f0")
                elif m == "cluster":
                    fills[m].append(CLR[r.cluster])
                else:
                    lo, hi = rng[m]
                    fills[m].append(_ramp(SCALES[m], (float(r[m]) - lo) / (hi - lo or 1)))
            op.append(1.0 if (in_type and in_state) else (0.28 if in_type else 0.35))
            tips.append(
                f"<b>{r.district}</b> <span style='color:#64748b'>· {r.state}</span>"
                f"<div class='row'><span><i style='display:inline-block;width:8px;height:8px;border-radius:2px;"
                f"background:{CLR[r.cluster]};margin-right:5px'></i>{CL(r.cluster)}</span></div>"
                f"<div class='row'><span>{L['tip_gap']}</span><span>{r.dwgi:.0f}</span></div>"
                f"<div class='row'><span>{L['tip_inc']}</span><span>RM{r.inc_med_2022:,.0f}</span></div>"
                f"<div class='row'><span>{L['tip_pov']}</span><span>{r.pov_abs_2022:.1f}%</span></div>"
                f"<div class='row'><span>{L['tip_u']}</span><span>{r.u_rate:.1f}%</span></div>"
                f"<div class='row'><span>{L['tip_p']}</span><span>{r.p_rate:.1f}%</span></div>")
        legends = {"cluster": "".join(f"<span class='chip' style='opacity:{1 if c in clusters else .4}'>"
                                      f"<i style='background:{CLR[c]}'></i>{CL(c)}</span>" for c in CLUSTERS)}
        for m in SCALES:
            lo, hi = rng[m]
            if m == "inc_med_2022":
                fmt = lambda v: f"RM{v:,.0f}"
            elif m == "dwgi":
                fmt = lambda v: f"{v:.0f}"
            else:
                fmt = lambda v: f"{v:.1f}%"
            legends[m] = (f"<span>{LABELS[m]}</span><span>{fmt(lo)}</span>"
                          f"<span class='bar' style='background:linear-gradient(90deg,{','.join(SCALES[m])})'></span>"
                          f"<span>{fmt(hi)}</span>")
        MAP_COMP(data={"fills": fills, "legends": legends, "labels": L["modes"], "mode": "cluster",
                       "op": op, "tip": tips, "dur": 1200,
                       "bbox": view_box(MAP_BOXES.get(state, MAP_BOXES[ALL]))}, key="smooth_map")


with tab_map:
    c1, c2 = st.columns([3.2, 1], gap="large")
    with c1:
        map_panel(df_all, state, clusters)
    with c2:
        st.markdown(f'<div class="section-title">{L["sel_area"]}</div>'
                    f'<div class="section-sub">{state_disp}</div>', unsafe_allow_html=True)
        stat(st, L["s_shown"], f"{len(df)}")
        if len(df):
            stat(st, L["s_inc"], f"RM{df.inc_med_2022.median():,.0f}")
            stat(st, L["s_pov"], f"{df.pov_abs_2022.mean():.1f}%")
            worst = df.sort_values("dwgi", ascending=False).iloc[0]
            stat(st, L["s_gap"], f"{worst.district} · {worst.dwgi:.0f}")

# ---------- district profile ----------
with tab_profile:
    title(L["prof_t"], L["prof_s"])
    pool = (df if not df.empty else df_all).sort_values("dwgi", ascending=False)
    pid = st.selectbox(L["pick"], pool.id, key="profile_district", format_func=lambda i: i.replace("|", " — "))
    row = df_all.set_index("id").loc[pid]
    row.name = df_all.index[df_all.id == pid][0]
    nat = df_all[["inc_med_2022", "pov_abs_2022", "u_rate", "p_rate"]].median()
    n_all = len(df_all)

    st.markdown(f"""
<div class="glass profile-head">
  <div><div class="ph-name">{row.district}</div>
  <div class="ph-sub">{row.state} · <span class="ph-chip" style="--c:{CLR[row.cluster]}">{CL(row.cluster)}</span></div></div>
  <div class="ph-score"><div class="ph-big">{row.dwgi:.0f}<span>/100</span></div>
  <div class="ph-sub">DWGI · {L['rank_of'].format(r=row.dwgi_rank, n=n_all)} · {L['topsis_rank'].format(r=row.topsis_rank)}</div></div>
</div>""", unsafe_allow_html=True)

    k = st.columns(4)
    for col, (lab, v, m, fmt, good_high) in zip(k, [
            (L["tip_inc"], row.inc_med_2022, nat.inc_med_2022, "RM{:,.0f}", True),
            (L["tip_pov"], row.pov_abs_2022, nat.pov_abs_2022, "{:.1f}%", False),
            (L["tip_u"], row.u_rate, nat.u_rate, "{:.1f}%", False),
            (L["tip_p"], row.p_rate, nat.p_rate, "{:.1f}%", True)]):
        diff = v - m
        dtxt = (f"{'+' if diff >= 0 else '-'}RM{abs(diff):,.0f}" if fmt.startswith("RM") else f"{diff:+.1f} pp")
        col.metric(lab, fmt.format(v), f"{dtxt} {L['vs_nat']}", delta_color="normal" if good_high else "inverse")

    c1, c2 = st.columns([1.1, 1], gap="large")
    with card("radar", c1):
        dims = L["radar_dims"]
        series = [(L["radar_series"][0], percentile_profile(df_all, row), "#4F46E5", .25),
                  (L["radar_series"][1], group_profile(df_all, df_all[df_all.cluster == row.cluster]),
                   CLR[row.cluster], .12),
                  (L["radar_series"][2], [50] * len(dims), "#94A3B8", 0)]
        fig = go.Figure()
        for name, vals, colr, alpha in series:
            r_, g_, b_ = (int(colr[i:i + 2], 16) for i in (1, 3, 5))
            fig.add_trace(go.Scatterpolar(r=vals + vals[:1], theta=dims + dims[:1], name=name, mode="lines",
                                          line=dict(color=colr, width=3 if alpha else 1.5,
                                                    dash=None if alpha else "dot"),
                                          fill="toself" if alpha else None,
                                          fillcolor=f"rgba({r_},{g_},{b_},{alpha})"))
        fig.update_layout(title=L["radar_t"], height=430, showlegend=True, margin=dict(l=70, r=70, t=60, b=10),
                          polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(range=[0, 100], showticklabels=False,
                                     gridcolor="rgba(148,163,184,.25)"),
                                     angularaxis=dict(gridcolor="rgba(148,163,184,.25)")))
        chart(fig, "radar")
    with card("ptrend", c2):
        yrs = [2019, 2022, 2024]
        inc = [row.get(f"inc_med_{y}") for y in yrs]
        pov = [row.get(f"pov_abs_{y}") for y in yrs]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=yrs, y=inc, name=L["tip_inc"] + " (RM)", mode="lines+markers",
                                 line=dict(color="#6366F1", width=3, shape="spline"), marker=dict(size=9)))
        fig.add_trace(go.Scatter(x=yrs, y=pov, name=L["tip_pov"] + " (%)", mode="lines+markers", yaxis="y2",
                                 line=dict(color="#F43F5E", width=3, shape="spline", dash="dot"), marker=dict(size=9)))
        fig.update_layout(title=L["trend_mini"], height=430, xaxis=dict(tickvals=yrs),
                          yaxis=dict(title="RM"), yaxis2=dict(title="%", overlaying="y", side="right", showgrid=False))
        chart(fig, "ptrend")

    recs = recommend(df_all, row)
    pr = peers(df_all, row)
    c1, c2 = st.columns([1.3, 1], gap="large")
    with c1:
        st.markdown(f'<div class="section-title">{L["recs_t"]}</div><div class="section-sub">{L["recs_s"]}</div>',
                    unsafe_allow_html=True)
        st.markdown('<div class="recs">' + "".join(
            f'<div class="glass rec"><div class="rec-t">{L["recs"][r][0]}<span class="rec-tag">{L["recs"][r][2]}</span>'
            f'</div><div class="rec-d">{L["recs"][r][1]}</div></div>' for r in recs) + "</div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="section-title">{L["peers_t"]}</div><div class="section-sub">{L["peers_s"]}</div>',
                    unsafe_allow_html=True)
        if pr.empty:
            insight(L["peers_none"], "🏅")
        else:
            st.markdown('<div class="peers">' + "".join(
                f'<div class="glass peer"><span class="dot" style="background:{CLR[p.cluster]}"></span>'
                f'<div><b>{p.district}</b><span>{p.state} · RM{p.inc_med_2022:,.0f}</span></div>'
                f'<div class="peer-s">{p.dwgi:.0f}</div></div>' for p in pr.itertuples()) + "</div>",
                unsafe_allow_html=True)
    st.download_button(L["dl_brief"], brief_html(row, L, CL, recs, pr, n_all),
                       f"MyWajarScope_{row.district.replace(' ', '_')}.html", "text/html", key="dl_brief")

# ---------- district types ----------
with tab_types:
    title(L["types_t"], L["types_s"])
    prof = df_all.groupby("cluster").agg(
        a=("district", "size"), b=("inc_med_2022", "median"), c=("pov_abs_2022", "mean"), d=("u_rate", "mean"),
        e=("p_rate", "mean"), f=("agri_share", "mean"), g=("mfg_share", "mean")).loc[CLUSTERS].round(1)
    prof.columns = L["prof_cols"]
    prof.index = [CL(c) for c in prof.index]
    st.dataframe(prof, width="stretch")
    insight(L["insight"])
    c1, c2 = st.columns(2, gap="medium")
    for col, x, ttl in [(c1, "u_rate", L["sc1"]), (c2, "p_rate", L["sc2"])]:
        with card(f"scatter_{x}", col):
            fig = px.scatter(disp(df), x=x, y="inc_med_2022", color="cluster", color_discrete_map=CLR_D,
                             category_orders=ORDER_D, hover_name="district",
                             hover_data={"state": True}, labels=LABELS, title=ttl, height=420)
            fig.update_traces(marker=dict(size=10, opacity=.85, line=dict(width=1, color="white")))
            chart(fig, f"scatter_{x}")
    with card("mix"):
        mix = disp(df_all).groupby(["state", "cluster"]).size().reset_index(name="n")
        fig = px.bar(mix, x="state", y="n", color="cluster", color_discrete_map=CLR_D, category_orders=ORDER_D,
                     labels={"n": L["n_districts"], "state": ""}, title=L["mix_t"], height=400)
        fig.update_traces(marker_line_width=0)
        fig.update_layout(bargap=.35)
        chart(fig, "mix")

# ---------- priority ----------
with tab_priority:
    title(L["prio_t"], L["prio_s"])
    c1, c2 = st.columns([1.4, 1], gap="large")
    with c1:
        method = st.segmented_control("method", ["dwgi", "topsis"], default="dwgi", key="prio_method",
                                      label_visibility="collapsed", format_func=L["method"].get) or "dwgi"
        st.caption(L["method_note"][method])
    with c2:
        n = st.slider(L["topn"], 5, 50, 20, key="topn")
    score_col, rank_col = ("dwgi", "dwgi_rank") if method == "dwgi" else ("topsis", "topsis_rank")
    if df.empty:
        st.info(L["empty"])
    else:
        top = df.sort_values(score_col, ascending=False).head(n)
        with card("priority"):
            fig = px.bar(disp(top).iloc[::-1], x=score_col, y="district", color="cluster", orientation="h",
                         color_discrete_map=CLR_D, category_orders=ORDER_D, hover_data={"state": True},
                         labels={**LABELS, "topsis": L["score"], "dwgi": L["score"]}, height=max(340, 26 * n))
            fig.update_traces(marker_line_width=0)
            fig.update_layout(yaxis_title="", margin=dict(l=0, r=10, t=10, b=10), bargap=.3,
                              legend=dict(y=1.02, x=0, yanchor="bottom"),
                              yaxis=dict(categoryorder="array", categoryarray=list(top.district[::-1])))
            chart(fig, "priority")
        P = L["pcols"]
        show = disp(top)[[rank_col, "state", "district", "cluster", score_col, "inc_med_2022", "pov_abs_2022",
                          "u_rate", "p_rate", "agri_share"]].rename(columns={
            rank_col: P["Rank"], "state": P["state"], "district": P["district"], "cluster": P["cluster"],
            score_col: P["DWGI"] if method == "dwgi" else "TOPSIS", "inc_med_2022": P["inc"],
            "pov_abs_2022": P["pov"], "u_rate": P["u"], "p_rate": P["p"], "agri_share": P["agri"]})
        sc = P["DWGI"] if method == "dwgi" else "TOPSIS"
        st.dataframe(show.round(1), hide_index=True, width="stretch",
                     column_config={sc: st.column_config.ProgressColumn(sc, min_value=0, max_value=100, format="%.0f")})
        st.download_button(L["dl_prio"], show.to_csv(index=False), f"priority_{method}.csv", "text/csv", key="dl_prio")

    # robustness: do the two ranking methods agree?
    with card("agree"):
        st.markdown(f'<div class="section-title">{L["agree_t"]}</div>', unsafe_allow_html=True)
        rho = spearman(df_all.dwgi, df_all.topsis)
        top_d = set(df_all.nlargest(20, "dwgi").id)
        top_t = set(df_all.nlargest(20, "topsis").id)
        a, b, cw = st.columns([1, 1, 2])
        a.metric(L["agree_rho"], f"{rho:.2f}")
        b.metric(L["agree_top"], f"{len(top_d & top_t)} / 20")
        wdf = pd.DataFrame({"k": [L["w_names"][k] for k in TOPSIS_W.index], "w": TOPSIS_W.values * 100})
        fig = px.bar(wdf, x="w", y="k", orientation="h", text="w", height=190, title=L["agree_w"],
                     color_discrete_sequence=["#6366F1"])
        fig.update_traces(texttemplate="%{x:.0f}%", textposition="outside", marker_line_width=0)
        fig.update_layout(xaxis=dict(visible=False, range=[0, wdf.w.max() * 1.3]), yaxis_title="",
                          margin=dict(l=0, r=0, t=34, b=0), bargap=.35)
        chart(fig, "topsis_w", cw)

# ---------- trend ----------
with tab_trend:
    title(L["trend_t"], L["trend_s"])
    if df.empty:
        st.info(L["empty"])
    t = df.dropna(subset=["inc_growth_pct"])
    g = t.groupby("cluster")[["inc_growth_pct", "pov_change_pp"]].median().reindex(CLUSTERS).dropna().reset_index()
    g = disp(g)
    c1, c2 = st.columns(2, gap="medium")
    for col, y, ylab, ttl in [(c1, "inc_growth_pct", L["tr_inc_y"], L["tr_inc"]),
                              (c2, "pov_change_pp", L["tr_pov_y"], L["tr_pov"])]:
        with card(f"trend_{y}", col):
            fig = px.bar(g, x="cluster", y=y, color="cluster", color_discrete_map=CLR_D, category_orders=ORDER_D,
                         labels={y: ylab, "cluster": ""}, title=ttl, text_auto=".1f", height=380)
            fig.update_traces(marker_line_width=0, textposition="outside")
            fig.update_layout(showlegend=False, bargap=.45)
            chart(fig, f"trend_{y}")
    pick = st.multiselect(L["compare"], sorted(df.district.unique()), key="compare",
                          default=[d for d in ["Pitas", "Tongod", "Petaling", "Kuching"] if d in set(df.district)])
    long = (df[df.district.isin(pick)]
            .melt(id_vars=["district"], value_vars=["inc_med_2019", "inc_med_2022", "inc_med_2024"],
                  var_name="year", value_name="income"))
    long["year"] = long.year.str[-4:].astype(int)
    if len(long.dropna()):
        with card("paths"):
            fig = px.line(long.dropna(), x="year", y="income", color="district", markers=True,
                          labels={"income": L["paths_y"], "year": ""}, title=L["paths"], height=400,
                          color_discrete_sequence=["#6366F1", "#14B8A6", "#F43F5E", "#F59E0B", "#0EA5E9", "#A855F7"])
            fig.update_traces(line=dict(width=3, shape="spline"), marker=dict(size=9, line=dict(width=2, color="white")))
            fig.update_xaxes(tickvals=[2019, 2022, 2024])
            chart(fig, "paths")
    st.caption(L["trend_cap"])


# ---------- AI ----------
@st.fragment
def simulator():
    """Runs on its own: moving a slider only re-runs this card, and the bar glides to the new estimate."""
    with card("sim"):
        st.markdown(f'<div class="section-title">{L["sim_t"]}</div><div class="section-sub">{L["sim_s"]}</div>',
                    unsafe_allow_html=True)
        opts = df_all.sort_values("dwgi", ascending=False)
        name = st.selectbox(L["sim_d"], opts.id, format_func=lambda i: i.replace("|", " — "), key="sim_district")
        row = df_all[df_all.id == name].iloc[0]
        new_p = st.slider(LABELS["p_rate"], 35.0, 85.0, float(row.p_rate), 0.5, key=f"sim_p_{name}")
        new_a = st.slider(LABELS["agri_share"], 0.0, 95.0, float(round(row.agri_share, 1)), 0.5, key=f"sim_a_{name}")
        new_m = st.slider(LABELS["mfg_share"], 0.0, 70.0, float(round(row.mfg_share, 1)), 0.5, key=f"sim_m_{name}")
        base = row[X_COLS].to_frame().T.astype(float)
        sim = base.copy()
        sim["p_rate"], sim["agri_share"], sim["mfg_share"] = new_p, new_a, new_m
        sim["services_share"] = max(0.0, row.services_share + (row.agri_share - new_a) + (row.mfg_share - new_m))
        est0, est1 = np.exp(rf.predict(base)[0]), np.exp(rf.predict(sim)[0])
        a, b = st.columns(2)
        a.metric(L["sim_now"], f"RM{est0:,.0f}")
        b.metric(L["sim_new"], f"RM{est1:,.0f}", f"{(est1 / est0 - 1) * 100:+.1f}%")
        hub_med = float(df_all[df_all.cluster == "Industrial hub"].inc_med_2022.median())
        comp = pd.DataFrame({"what": L["sim_bars"], "income": [est0, est1, hub_med]})
        fig = px.bar(comp, x="income", y="what", orientation="h", text="income", height=200,
                     color="what", color_discrete_sequence=["#94A3B8", "#6366F1", "#14B8A6"])
        fig.update_traces(texttemplate="RM%{x:,.0f}", textposition="inside", marker_line_width=0,
                          insidetextanchor="end")
        fig.update_layout(showlegend=False, xaxis=dict(range=[0, max(hub_med, est1) * 1.08], visible=False),
                          yaxis=dict(title="", autorange="reversed"), margin=dict(l=0, r=0, t=6, b=0), bargap=.35)
        chart(fig, "sim")
        st.caption(L["sim_actual"].format(v=row.inc_med_2022))


with tab_ai:
    title(L["ai_t"], L["ai_s"].format(r2=cv_r2))
    c1, c2 = st.columns(2, gap="large")
    with card("drivers", c1):
        importance = importance_raw.rename(LABELS).sort_values()
        fig = px.bar(importance, orientation="h", labels={"value": L["imp_x"], "index": ""},
                     title=L["imp_t"], height=430)
        fig.update_traces(marker=dict(color=importance.values, colorscale=[[0, "#c7d2fe"], [1, "#4f46e5"]],
                                      line_width=0))
        fig.update_layout(showlegend=False, bargap=.35, yaxis_title="")
        chart(fig, "drivers")
        st.caption(L["imp_cap"])
    with card("valid", c1):
        vd = disp(df_all.assign(pred=oof_pred))
        mx = float(max(vd.inc_med_2022.max(), vd.pred.max())) * 1.05
        fig = px.scatter(vd, x="inc_med_2022", y="pred", color="cluster", color_discrete_map=CLR_D,
                         category_orders=ORDER_D, hover_name="district", title=L["val_t"], height=400,
                         labels={"inc_med_2022": L["val_x"], "pred": L["val_y"]})
        fig.add_shape(type="line", x0=0, y0=0, x1=mx, y1=mx, line=dict(color="#94A3B8", dash="dash"))
        fig.update_traces(marker=dict(size=8, opacity=.85, line=dict(width=1, color="white")), selector=dict(mode="markers"))
        fig.update_layout(showlegend=False, xaxis=dict(range=[1500, mx], autorange=False),
                          yaxis=dict(range=[1500, mx], autorange=False))
        chart(fig, "valid", animate=False)
        st.caption(L["val_cap"])
    with c2:
        simulator()

# ---------- about (animated infographic) ----------
with tab_about:
    from infographic import build_html, component as info_component
    prof = {c: {"n": int((df_all.cluster == c).sum()),
                "inc": float(df_all.loc[df_all.cluster == c, "inc_med_2022"].median()),
                "pov": float(df_all.loc[df_all.cluster == c, "pov_abs_2022"].mean()),
                "u": float(df_all.loc[df_all.cluster == c, "u_rate"].mean())} for c in CLUSTERS}
    info_component()(data={"html": build_html(L["info"], {"n": len(df_all), "r2": round(cv_r2, 2), "prof": prof},
                                              CL, CLR)}, key="infographic")
    st.download_button(L["dl_all"], df_all.drop(columns="id").to_csv(index=False),
                       "mywajarscope_districts.csv", "text/csv", key="dl_all")

st.markdown(f'<div class="footer">{L["foot"]}</div>', unsafe_allow_html=True)
