"""Analytics used by the dashboard: Entropy-weight TOPSIS, percentile profiles, peer districts,
rule-based action suggestions and a downloadable district brief."""
import numpy as np
import pandas as pd

# indicators and their direction: +1 = higher value means a bigger decent-work gap, -1 = lower value means a bigger gap
GAP_DIRECTION = {"inc_med_2022": -1, "pov_abs_2022": +1, "u_rate": +1, "p_rate": -1}


def entropy_topsis(d: pd.DataFrame):
    """Entropy-weight TOPSIS deprivation score (0–100, higher = bigger gap) and the data-driven weights.

    1. Orient every indicator so larger = more deprived and min-max scale to [0, 1].
    2. Entropy weights: indicators that vary more across districts carry more information, so get more weight.
    3. TOPSIS: distance to the best and worst virtual district; score = closeness to the worst.
    """
    cols = list(GAP_DIRECTION)
    X = d[cols].astype(float).copy()
    for c, s in GAP_DIRECTION.items():
        lo, hi = X[c].min(), X[c].max()
        X[c] = (X[c] - lo) / (hi - lo) if s > 0 else (hi - X[c]) / (hi - lo)
    B = X.values + 1e-9
    P = B / B.sum(axis=0)
    e = -(P * np.log(P)).sum(axis=0) / np.log(len(B))
    w = (1 - e) / (1 - e).sum()
    V = (B / np.sqrt((B ** 2).sum(axis=0))) * w
    worst, best = V.max(axis=0), V.min(axis=0)
    d_worst = np.sqrt(((V - worst) ** 2).sum(axis=1))
    d_best = np.sqrt(((V - best) ** 2).sum(axis=1))
    score = d_best / (d_best + d_worst)
    score = (score - score.min()) / (score.max() - score.min()) * 100
    return pd.Series(score.round(1), index=d.index), pd.Series(w, index=cols)


def spearman(a: pd.Series, b: pd.Series) -> float:
    return float(a.rank().corr(b.rank()))


# radar dimensions: (column, higher_is_better)
RADAR_DIMS = [("inc_med_2022", True), ("pov_abs_2022", False), ("u_rate", False), ("p_rate", True),
              ("agri_share", False), ("gdp_per_worker", True)]


def percentile_profile(d: pd.DataFrame, row: pd.Series):
    """0–100 percentile for each radar dimension, oriented so 100 = best in Malaysia."""
    out = []
    for c, good_high in RADAR_DIMS:
        pct = (d[c] < row[c]).mean() * 100 + (d[c] == row[c]).mean() * 50
        out.append(pct if good_high else 100 - pct)
    return out


def group_profile(d: pd.DataFrame, sub: pd.DataFrame):
    med = sub[[c for c, _ in RADAR_DIMS]].median()
    return percentile_profile(d, med)


STRUCTURE = ["agri_share", "mining_share", "mfg_share", "constr_share", "services_share", "log_gdp_per_worker"]


def peers(d: pd.DataFrame, row: pd.Series, k: int = 8):
    """Districts with the most similar economic structure that achieve a smaller decent-work gap."""
    Z = (d[STRUCTURE] - d[STRUCTURE].mean()) / d[STRUCTURE].std()
    z0 = (row[STRUCTURE].astype(float) - d[STRUCTURE].mean()) / d[STRUCTURE].std()
    dist = np.sqrt(((Z - z0) ** 2).sum(axis=1).astype(float))
    near = d.assign(_dist=dist).drop(index=row.name, errors="ignore").nsmallest(k, "_dist")
    return near[near.dwgi < row.dwgi].sort_values("dwgi").head(4)


def recommend(d: pd.DataFrame, row: pd.Series):
    """Rule-based action areas from the district's weakest dimensions (keys looked up in i18n)."""
    med = d[["p_rate", "u_rate", "pov_abs_2022", "gdp_per_worker"]].median()
    recs = []
    if row.p_rate < med.p_rate - 3:
        recs.append("participation")
    if row.u_rate > med.u_rate + 1.5:
        recs.append("jobs")
    if row.agri_share > 40:
        recs.append("agri")
    if row.pov_abs_2022 > 15:
        recs.append("poverty")
    if row.gdp_per_worker < d.gdp_per_worker.quantile(.25):
        recs.append("productivity")
    if pd.notna(row.get("inc_growth_pct")) and row.inc_growth_pct < 0:
        recs.append("falling")
    return recs or ["sustain"]


def brief_html(row, L, CL, recs, peer_rows, n_total):
    """Self-contained one-page district brief (HTML) for download / printing to PDF."""
    B = L["brief"]
    rec_html = "".join(f"<li><b>{L['recs'][r][0]}</b> <span class='t'>{L['recs'][r][2]}</span><br>{L['recs'][r][1]}</li>"
                       for r in recs)
    peer_html = "".join(f"<li>{p.district} ({p.state}) · DWGI {p.dwgi:.0f}</li>" for p in peer_rows.itertuples()) \
        or f"<li>{B['no_peers']}</li>"
    g = row.get("inc_growth_pct")
    growth = "—" if pd.isna(g) else f"{g:+.1f}%"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>{row.district} · MyWajarScope</title>
<style>body{{font-family:'Segoe UI',system-ui,sans-serif;color:#0f172a;max-width:780px;margin:32px auto;padding:0 20px}}
h1{{margin:0;font-size:28px}} .sub{{color:#64748b;margin:4px 0 20px}} .grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}}
.k{{border:1px solid #e2e8f0;border-radius:12px;padding:12px}} .k b{{display:block;font-size:20px}} .k span{{color:#64748b;font-size:12px}}
h2{{font-size:16px;margin:24px 0 8px;color:#4f46e5}} li{{margin:6px 0;line-height:1.5}} .t{{font-size:11px;background:#eef2ff;color:#4f46e5;
padding:1px 7px;border-radius:999px}} .foot{{margin-top:28px;font-size:11px;color:#94a3b8;border-top:1px solid #e2e8f0;padding-top:10px}}
.chip{{display:inline-block;padding:3px 10px;border-radius:999px;background:#eef2ff;font-size:12px;font-weight:600}}</style></head><body>
<div class="chip">MyWajarScope · {B['title']}</div><h1>{row.district}</h1>
<div class="sub">{row.state} · {CL(row.cluster)} · DWGI {row.dwgi:.0f}/100 · {B['rank']} {row.dwgi_rank}/{n_total}</div>
<div class="grid"><div class="k"><b>RM{row.inc_med_2022:,.0f}</b><span>{L['tip_inc']} 2022</span></div>
<div class="k"><b>{row.pov_abs_2022:.1f}%</b><span>{L['tip_pov']} 2022</span></div>
<div class="k"><b>{row.u_rate:.1f}%</b><span>{L['tip_u']} 2022</span></div>
<div class="k"><b>{row.p_rate:.1f}%</b><span>{L['tip_p']} 2022</span></div></div>
<p>{B['growth']}: <b>{growth}</b></p>
<h2>{B['actions']}</h2><ul>{rec_html}</ul>
<h2>{B['peers']}</h2><ul>{peer_html}</ul>
<div class="foot">{B['foot']}</div></body></html>"""
