"""Animated, scroll-driven infographic for the About / Maklumat tab (components v2, no external libraries).

Python builds the HTML (so it follows the selected language and live numbers); the JS:
  * reveals blocks as they scroll into view (fade + rise, staggered),
  * counts numbers up when they appear,
  * grows comparison bars to their value,
  * fills the pipeline timeline line in step with the scroll position.
"""
import streamlit as st

CSS = """
:host { display: block; }
.ig { --ink:#0f172a; --ink2:#475569; --ink3:#94a3b8; --g:rgba(255,255,255,.55); --gb:rgba(255,255,255,.8);
      --ease:cubic-bezier(.22,1,.36,1); color: var(--ink); font-family: inherit; }
.glass { background: var(--g); border: 1px solid var(--gb); border-radius: 22px;
         backdrop-filter: blur(20px) saturate(170%); -webkit-backdrop-filter: blur(20px) saturate(170%);
         box-shadow: 0 1px 0 rgba(255,255,255,.9) inset, 0 12px 34px -14px rgba(30,41,99,.2); }
section { margin: 0 0 56px; }
.kicker { font-size: 12px; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: #6366f1; }
h2 { font-size: clamp(22px, 2.6vw, 30px); font-weight: 800; letter-spacing: -.02em; margin: 6px 0 6px; line-height: 1.15; }
.lead { color: var(--ink2); font-size: 15px; max-width: 760px; margin: 0 0 22px; line-height: 1.6; }

/* reveal on scroll */
.rv { opacity: 0; transform: translateY(42px) scale(.98); filter: blur(6px);
      transition: opacity .9s var(--ease), transform .9s var(--ease), filter .9s var(--ease);
      transition-delay: calc(var(--d, 0) * 110ms); }
.rv.in { opacity: 1; transform: none; filter: none; }
.rv:not(.in) { transition-duration: .6s; transition-delay: 0ms; }
.rv.left { transform: translateX(-46px); } .rv.right { transform: translateX(46px); }
.rv.left.in, .rv.right.in { transform: none; }

/* hero */
.hero { position: relative; overflow: hidden; padding: 38px 36px; }
.hero h1 { font-size: clamp(30px, 4.4vw, 52px); font-weight: 800; letter-spacing: -.035em; margin: 8px 0 10px; line-height: 1.02;
  background: linear-gradient(100deg,#1e1b4b,#4f46e5 40%,#0d9488 70%,#1e1b4b); background-size: 220% auto;
  -webkit-background-clip: text; background-clip: text; color: transparent; animation: sheen 9s linear infinite; }
.hero p { color: var(--ink2); max-width: 680px; font-size: 16px; line-height: 1.6; margin: 0; }
.orb { position: absolute; border-radius: 50%; filter: blur(40px); opacity: .55; pointer-events: none; }
.orb.a { width: 260px; height: 260px; right: -40px; top: -80px; background: #a5b4fc; animation: float 9s ease-in-out infinite; }
.orb.b { width: 200px; height: 200px; right: 160px; bottom: -110px; background: #99f6e4; animation: float 11s ease-in-out infinite reverse; }
.scrollhint { margin-top: 22px; display: inline-flex; gap: 10px; align-items: center; font-size: 13px; color: var(--ink3); }
.mouse { width: 18px; height: 28px; border: 2px solid var(--ink3); border-radius: 10px; position: relative; }
.mouse::after { content: ""; position: absolute; left: 50%; top: 5px; width: 3px; height: 6px; margin-left: -1.5px;
  border-radius: 2px; background: var(--ink3); animation: wheel 1.6s ease-in-out infinite; }

/* stats band */
.stats { display: grid; grid-template-columns: repeat(5, minmax(0,1fr)); gap: 14px; }
.stat { padding: 20px 18px; text-align: left; }
.stat .n { font-size: 34px; font-weight: 800; letter-spacing: -.03em; line-height: 1;
  background: linear-gradient(135deg,#4f46e5,#0d9488); -webkit-background-clip: text; background-clip: text; color: transparent; }
.stat .l { font-size: 13px; color: var(--ink2); margin-top: 8px; line-height: 1.4; }

/* data sources */
.sources { display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 14px; }
.src { padding: 20px; position: relative; overflow: hidden; transition: transform .4s var(--ease), box-shadow .4s var(--ease); }
.src:hover { transform: translateY(-5px); box-shadow: 0 1px 0 #fff inset, 0 22px 44px -18px rgba(79,70,229,.4); }
.ico { width: 44px; height: 44px; border-radius: 14px; display: grid; place-items: center; margin-bottom: 14px; color: #fff; }
.ico svg { width: 22px; height: 22px; }
.src b { display: block; font-size: 15px; margin-bottom: 4px; }
.src .id { font-family: ui-monospace, monospace; font-size: 11.5px; color: #6366f1; background: rgba(99,102,241,.08);
  padding: 2px 7px; border-radius: 6px; display: inline-block; margin: 4px 0 8px; }
.src .y { font-size: 12.5px; color: var(--ink2); }
.years { display: flex; gap: 3px; margin-top: 10px; }
.years i { flex: 1; height: 6px; border-radius: 3px; background: rgba(148,163,184,.25); transition: background .6s var(--ease);
  transition-delay: calc(var(--k) * 70ms + 300ms); }
.in .years i.on { background: var(--c); }

/* pipeline timeline */
.pipe { position: relative; padding-left: 64px; }
.rail { position: absolute; left: 25px; top: 10px; bottom: 10px; width: 3px; border-radius: 3px; background: rgba(148,163,184,.25); }
.rail .fill { position: absolute; left: 0; top: 0; width: 100%; height: 0; border-radius: 3px;
  background: linear-gradient(#4f46e5, #0d9488); box-shadow: 0 0 12px rgba(79,70,229,.45); }
.step { position: relative; padding: 18px 22px; margin-bottom: 16px; }
.step .dot { position: absolute; left: -52px; top: 18px; width: 30px; height: 30px; border-radius: 50%;
  display: grid; place-items: center; font-weight: 800; font-size: 13px; color: #fff;
  background: linear-gradient(135deg,#4f46e5,#0d9488); box-shadow: 0 0 0 6px rgba(255,255,255,.7), 0 8px 18px -6px rgba(79,70,229,.6);
  transform: scale(.4); transition: transform .7s var(--ease) .15s; }
.step.in .dot { transform: scale(1); }
.step b { font-size: 16px; } .step p { margin: 4px 0 0; color: var(--ink2); font-size: 14px; line-height: 1.55; }
.step .tag { display: inline-block; font-size: 11.5px; font-weight: 600; padding: 3px 9px; border-radius: 999px;
  background: rgba(20,184,166,.12); color: #0f766e; margin-top: 8px; }

/* district types */
.types { display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 14px; }
.type { padding: 20px; border-top: 4px solid var(--c); }
.type .nm { font-weight: 800; font-size: 15.5px; } .type .ct { font-size: 12.5px; color: var(--ink3); margin-bottom: 12px; }
.mrow { margin: 10px 0; } .mrow .lab { display: flex; justify-content: space-between; font-size: 12.5px; color: var(--ink2); }
.mrow .lab span:last-child { color: var(--ink); font-weight: 700; }
.track { height: 8px; border-radius: 999px; background: rgba(148,163,184,.2); overflow: hidden; margin-top: 5px; }
.track i { display: block; height: 100%; width: 0; border-radius: 999px; background: var(--c);
  transition: width 1.3s var(--ease); transition-delay: calc(var(--d, 0) * 110ms + 250ms); }

/* the finding */
.finding { padding: 30px 32px; }
.vs { display: grid; grid-template-columns: 1fr 1fr; gap: 28px; margin-top: 14px; }
.vs h3 { font-size: 15px; margin: 0 0 4px; } .vs .note { font-size: 13px; color: var(--ink2); margin-bottom: 12px; }
.bar2 { display: grid; grid-template-columns: 130px 1fr 74px; align-items: center; gap: 10px; margin: 10px 0; font-size: 13px; }
.bar2 .t { height: 26px; border-radius: 10px; background: rgba(148,163,184,.16); overflow: hidden; }
.bar2 .t i { display: block; height: 100%; width: 0; border-radius: 10px; background: var(--c);
  transition: width 1.5s var(--ease) .3s; }
.bar2 .v { font-weight: 800; text-align: right; }
.verdict { margin-top: 18px; padding: 14px 18px; border-radius: 16px; font-size: 15px; line-height: 1.5;
  background: linear-gradient(135deg, rgba(79,70,229,.1), rgba(13,148,136,.1)); }

/* SDG + limits */
.sdg { display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 14px; }
.target { padding: 20px; display: flex; gap: 14px; align-items: flex-start; }
.badge { flex: none; width: 54px; height: 54px; border-radius: 16px; background: #a21942; color: #fff;
  display: grid; place-items: center; font-weight: 800; font-size: 16px; box-shadow: 0 10px 20px -10px #a21942; }
.target b { display: block; margin-bottom: 4px; } .target span { font-size: 13.5px; color: var(--ink2); line-height: 1.5; }
.limits { display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 12px; }
.lim { padding: 16px 18px; display: flex; gap: 12px; font-size: 14px; color: var(--ink2); line-height: 1.5; }
.lim .i { flex: none; width: 28px; height: 28px; border-radius: 10px; display: grid; place-items: center;
  background: rgba(245,158,11,.14); color: #b45309; font-weight: 800; }

@keyframes sheen { to { background-position: 220% center; } }
@keyframes float { 50% { transform: translate(-24px, 18px) scale(1.08); } }
@keyframes wheel { 0% { opacity: 0; transform: translateY(0); } 40% { opacity: 1; } 100% { opacity: 0; transform: translateY(8px); } }
@media (max-width: 1000px) { .stats { grid-template-columns: repeat(2,1fr); } .sources, .types { grid-template-columns: repeat(2,1fr); }
  .sdg, .vs, .limits { grid-template-columns: 1fr; } }
@media (prefers-reduced-motion: reduce) { .rv, .track i, .bar2 .t i, .years i, .step .dot { transition: none !important; }
  .rv { opacity: 1; transform: none; filter: none; } * { animation: none !important; } }
"""

JS = """
export default function (c) {
  const root = c.parentElement;
  let host = root.querySelector('.ig');
  if (!host) { host = document.createElement('div'); host.className = 'ig'; root.appendChild(host); }
  const html = (c.data || {}).html || '';
  if (host.__html === html) return;          // nothing changed: keep current animation state
  host.__html = html;
  host.innerHTML = html;
  if (root.__io) root.__io.disconnect();

  const countUp = el => {
    const to = parseFloat(el.dataset.to), dec = +(el.dataset.dec || 0), pre = el.dataset.pre || '', suf = el.dataset.suf || '';
    const t0 = performance.now(), dur = 1600;
    const fmt = v => pre + v.toLocaleString('en-US', { minimumFractionDigits: dec, maximumFractionDigits: dec }) + suf;
    const step = now => {
      const t = Math.min(1, (now - t0) / dur), k = 1 - Math.pow(1 - t, 4);
      el.textContent = fmt(to * k);
      if (t < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };

  const reveal = el => {
    el.classList.add('in');
    el.querySelectorAll('[data-to]').forEach(countUp);
    el.querySelectorAll('[data-w]').forEach(b => { b.style.width = b.dataset.w; });
  };
  const hide = el => {
    el.classList.remove('in');
    el.querySelectorAll('[data-to]').forEach(n => { n.textContent = '0'; });
    el.querySelectorAll('[data-w]').forEach(b => { b.style.width = '0'; });
  };
  // Blocks appear when scrolled into view. When the reader scrolls back up, blocks that drop below
  // the viewport dissolve away again (and replay when scrolled to once more).
  root.__io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) reveal(e.target);
    else if (e.boundingClientRect.top > 0) hide(e.target);
  }), { threshold: 0.12, rootMargin: '0px 0px -10% 0px' });
  host.querySelectorAll('.rv').forEach(el => root.__io.observe(el));

  // pipeline rail fills as the reader scrolls through it
  const rail = host.querySelector('.rail'), fill = host.querySelector('.rail .fill');
  if (rail && fill) {
    const onScroll = () => {
      const r = rail.getBoundingClientRect(), vh = window.innerHeight;
      const p = Math.min(1, Math.max(0, (vh * 0.7 - r.top) / r.height));
      fill.style.height = (p * 100) + '%';
    };
    if (root.__onScroll) document.removeEventListener('scroll', root.__onScroll, true);
    root.__onScroll = onScroll;
    document.addEventListener('scroll', onScroll, { capture: true, passive: true });
    onScroll();
  }
}
"""

ICONS = {
    "income": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21V10l9-6 9 6v11"/><path d="M9 21v-6h6v6"/></svg>',
    "poverty": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 17l6-6 4 4 8-8"/><path d="M14 7h7v7"/></svg>',
    "labour": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="7" r="3"/><path d="M3 21v-2a5 5 0 0 1 5-5h2a5 5 0 0 1 5 5v2"/><path d="M16 3.5a3 3 0 0 1 0 6M21 21v-2a4 4 0 0 0-3-3.9"/></svg>',
    "gdp": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/></svg>',
}


@st.cache_resource
def component():
    return st.components.v2.component("mywajarscope_infographic", css=CSS, js=JS)


def build_html(I, s, CL, CLR):
    """I: infographic text (current language). s: live numbers from the app."""
    yrs = lambda on, col: "".join(f'<i style="--k:{k};--c:{col}" class="{"on" if y in on else ""}"></i>'
                                  for k, y in enumerate(range(2015, 2025)))
    src_specs = [("income", "#6366f1", "hh_income_district", {2019, 2022, 2024}),
                 ("poverty", "#f43f5e", "hh_poverty_district", {2019, 2022, 2024}),
                 ("labour", "#14b8a6", "lfs_district", set(range(2018, 2025))),
                 ("gdp", "#f59e0b", "gdp_district_real_supply", set(range(2015, 2021)))]
    sources = "".join(
        f'<div class="glass src rv" style="--d:{i}"><div class="ico" style="background:{col}">{ICONS[k]}</div>'
        f'<b>{I["src"][k][0]}</b><span class="id">{did}</span><div class="y">{I["src"][k][1]}</div>'
        f'<div class="years">{yrs(on, col)}</div></div>'
        for i, (k, col, did, on) in enumerate(src_specs))

    stats = [(s["n"], 0, "", "", I["st"][0]), (19, 0, "", "", I["st"][1]), (8, 0, "", "", I["st"][2]),
             (4, 0, "", "", I["st"][3]), (s["r2"], 2, "", "", I["st"][4])]
    stats_html = "".join(f'<div class="glass stat rv" style="--d:{i}"><div class="n" data-to="{v}" data-dec="{d}" '
                         f'data-pre="{p}" data-suf="{u}">0</div><div class="l">{lab}</div></div>'
                         for i, (v, d, p, u, lab) in enumerate(stats))

    steps = "".join(f'<div class="glass step rv"><div class="dot">{i + 1}</div><b>{t}</b><p>{d}</p>'
                    f'<span class="tag">{tag}</span></div>' for i, (t, d, tag) in enumerate(I["steps"]))

    P = s["prof"]
    imax = max(p["inc"] for p in P.values())
    pmax = max(p["pov"] for p in P.values())
    types = "".join(
        f'<div class="glass type rv" style="--d:{i};--c:{CLR[c]}"><div class="nm">{CL(c)}</div>'
        f'<div class="ct">{P[c]["n"]} {I["districts"]}</div>'
        f'<div class="mrow"><div class="lab"><span>{I["m_inc"]}</span><span>RM{P[c]["inc"]:,.0f}</span></div>'
        f'<div class="track"><i data-w="{P[c]["inc"] / imax * 100:.0f}%"></i></div></div>'
        f'<div class="mrow"><div class="lab"><span>{I["m_pov"]}</span><span>{P[c]["pov"]:.1f}%</span></div>'
        f'<div class="track"><i data-w="{P[c]["pov"] / pmax * 100:.0f}%"></i></div></div>'
        f'<div class="mrow"><div class="lab"><span>{I["m_u"]}</span><span>{P[c]["u"]:.1f}%</span></div>'
        f'<div class="track"><i data-w="{P[c]["u"] / 10 * 100:.0f}%"></i></div></div></div>'
        for i, c in enumerate(P))

    hub, wpr = P["Industrial hub"], P["Working-poor rural"]
    bar = lambda lab, v, mx, col, txt: (f'<div class="bar2"><span>{lab}</span><div class="t"><i style="--c:{col}" '
                                        f'data-w="{v / mx * 100:.0f}%"></i></div><span class="v">{txt}</span></div>')
    finding = (
        f'<div class="glass finding rv"><div class="kicker">{I["f_k"]}</div><h2>{I["f_t"]}</h2>'
        f'<div class="vs"><div><h3>{I["f_u"]}</h3><div class="note">{I["f_un"]}</div>'
        + bar(CL("Industrial hub"), hub["u"], 5, CLR["Industrial hub"], f'{hub["u"]:.1f}%')
        + bar(CL("Working-poor rural"), wpr["u"], 5, CLR["Working-poor rural"], f'{wpr["u"]:.1f}%')
        + f'</div><div><h3>{I["f_i"]}</h3><div class="note">{I["f_in"]}</div>'
        + bar(CL("Industrial hub"), hub["inc"], hub["inc"], CLR["Industrial hub"], f'RM{hub["inc"]:,.0f}')
        + bar(CL("Working-poor rural"), wpr["inc"], hub["inc"], CLR["Working-poor rural"], f'RM{wpr["inc"]:,.0f}')
        + f'</div></div><div class="verdict">{I["f_v"]}</div></div>')

    sdg = "".join(f'<div class="glass target rv" style="--d:{i}"><div class="badge">{n}</div><div><b>{t}</b>'
                  f'<span>{d}</span></div></div>' for i, (n, t, d) in enumerate(I["sdg"]))
    limits = "".join(f'<div class="glass lim rv {"left" if i % 2 == 0 else "right"}"><div class="i">!</div>'
                     f'<div>{t}</div></div>' for i, t in enumerate(I["lim"]))

    return f"""
<section><div class="glass hero rv"><div class="orb a"></div><div class="orb b"></div>
  <div class="kicker">{I['h_k']}</div><h1>MyWajarScope</h1><p>{I['h_p']}</p></div></section>
<section><div class="stats">{stats_html}</div></section>
<section><div class="rv"><div class="kicker">01</div><h2>{I['s1_t']}</h2><p class="lead">{I['s1_p']}</p></div>
  <div class="sources">{sources}</div></section>
<section><div class="rv"><div class="kicker">02</div><h2>{I['s2_t']}</h2><p class="lead">{I['s2_p']}</p></div>
  <div class="pipe"><div class="rail"><div class="fill"></div></div>{steps}</div></section>
<section><div class="rv"><div class="kicker">03</div><h2>{I['s3_t']}</h2><p class="lead">{I['s3_p']}</p></div>
  <div class="types">{types}</div></section>
<section>{finding}</section>
<section><div class="rv"><div class="kicker">04</div><h2>{I['s4_t']}</h2></div><div class="sdg">{sdg}</div></section>
<section><div class="rv"><div class="kicker">05</div><h2>{I['s5_t']}</h2></div><div class="limits">{limits}</div></section>
"""
