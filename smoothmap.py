"""Smooth district map for Streamlit (components v2, no external JS libraries).

The SVG with every district path is built once. On each rerun Python only sends
colours, opacities, tooltips and the target view box, and the browser:
  * glides the camera (view box) to the selected state with an ease-in-out zoom,
  * cross-fades district colours when the colour mode or filters change,
so nothing snaps or pops.
"""
import json
import math

import streamlit as st

CSS = """
:host { display: block; width: 100%; }
.mapbox { position: relative; width: 100%; }
.modes { display: flex; flex-wrap: wrap; gap: 6px; margin: 0 0 10px; position: relative; z-index: 3; }
.modes button {
  font: 600 13.5px 'Plus Jakarta Sans', system-ui, sans-serif; color: #334155; cursor: pointer;
  padding: 8px 16px; border-radius: 999px; border: 1px solid rgba(255,255,255,.9); background: rgba(255,255,255,.65);
  transition: background .25s cubic-bezier(.22,1,.36,1), color .25s, box-shadow .25s, transform .15s;
}
.modes button:hover { transform: translateY(-1px); box-shadow: 0 6px 14px -8px rgba(79,70,229,.5); }
.modes button:active { transform: scale(.96); }
.modes button.on { background: linear-gradient(135deg,#4f46e5,#0d9488); color: #fff; border-color: transparent;
  box-shadow: 0 8px 18px -8px rgba(79,70,229,.6); }
/* clip zoomed-in districts to the map area so they never cover the buttons above */
.wrap { position: relative; width: 100%; height: 500px; overflow: hidden;
  /* soft fade at the clipped edges so zoomed-in neighbours dissolve instead of ending in a hard box */
  -webkit-mask-image: linear-gradient(to right, transparent 0, #000 5%, #000 95%, transparent 100%),
                      linear-gradient(to bottom, transparent 0, #000 6%, #000 94%, transparent 100%);
  -webkit-mask-composite: source-in; mask-composite: intersect;
  mask-image: linear-gradient(to right, transparent 0, #000 5%, #000 95%, transparent 100%),
              linear-gradient(to bottom, transparent 0, #000 6%, #000 94%, transparent 100%); }
svg { width: 100%; height: 100%; display: block; overflow: visible; }
path {
  fill: #e2e8f0; stroke: rgba(255,255,255,.95); stroke-width: .7; vector-effect: non-scaling-stroke;
  transition: fill .6s cubic-bezier(.22,1,.36,1), opacity .6s cubic-bezier(.22,1,.36,1), stroke-width .25s;
  cursor: pointer;
}
path:hover { stroke: #0f172a; stroke-width: 1.6; }
.tip {
  position: absolute; pointer-events: none; opacity: 0; transform: translateY(6px);
  transition: opacity .2s ease, transform .2s ease;
  background: rgba(255,255,255,.85); backdrop-filter: blur(14px) saturate(170%); -webkit-backdrop-filter: blur(14px);
  border: 1px solid rgba(255,255,255,.9); border-radius: 14px; padding: 10px 12px; font-size: 12.5px;
  box-shadow: 0 12px 30px -12px rgba(30,41,99,.35); color: #0f172a; min-width: 180px; z-index: 5;
}
.tip.on { opacity: 1; transform: none; }
.tip b { font-size: 13.5px; }
.tip .row { display: flex; justify-content: space-between; gap: 14px; color: #475569; margin-top: 2px; }
.tip .row span:last-child { color: #0f172a; font-weight: 600; }
.legend { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-top: 6px; font-size: 12.5px; color: #475569;
          min-height: 28px; }
.chip { display: inline-flex; align-items: center; gap: 6px; padding: 4px 10px; border-radius: 999px;
        background: rgba(255,255,255,.7); border: 1px solid rgba(255,255,255,.9); transition: opacity .4s; }
.chip i { width: 10px; height: 10px; border-radius: 3px; display: inline-block; }
.bar { width: 220px; height: 10px; border-radius: 999px; }
"""

JS = """
export default function (c) {
  const root = c.parentElement;
  const wrap = root.querySelector('.wrap');
  const svg = root.querySelector('svg');
  const tip = root.querySelector('.tip');
  const paths = Array.from(svg.querySelectorAll('path'));
  const d = c.data || {};
  const ease = t => (t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);

  if (!root.__ready) {
    root.__ready = true;
    root.__vb = d.bbox.slice();
    svg.setAttribute('viewBox', d.bbox.join(' '));
    paths.forEach((p, i) => {
      p.addEventListener('mousemove', e => {
        const r = wrap.getBoundingClientRect();
        tip.innerHTML = (root.__tips || [])[i] || '';
        let x = e.clientX - r.left + 14, y = e.clientY - r.top + 14;
        if (x + 220 > r.width) x -= 240;
        if (y + 190 > r.height) y -= 200;
        tip.style.left = x + 'px'; tip.style.top = y + 'px';
        tip.classList.add('on');
      });
      p.addEventListener('mouseleave', () => tip.classList.remove('on'));
    });
  }
  root.__tips = d.tip || [];

  // colour mode is switched entirely in the browser: all modes arrive at once, so a click recolours instantly
  root.__d = d;
  if (!root.__mode || !(root.__mode in d.fills)) root.__mode = d.mode || Object.keys(d.fills)[0];
  const paint = () => {
    const D = root.__d, m = root.__mode, f = D.fills[m];
    paths.forEach((p, i) => { p.style.fill = f[i]; p.style.opacity = D.op[i]; });
    const lg = root.querySelector('.legend');
    if (lg.__html !== D.legends[m]) { lg.__html = D.legends[m]; lg.innerHTML = D.legends[m]; }
    bar.querySelectorAll('button').forEach(b => b.classList.toggle('on', b.dataset.m === m));
  };
  const bar = root.querySelector('.modes');
  const sig = JSON.stringify(d.labels);
  if (bar.__sig !== sig) {
    bar.__sig = sig;
    bar.innerHTML = Object.entries(d.labels).map(([k, v]) => `<button type="button" data-m="${k}">${v}</button>`).join('');
    bar.querySelectorAll('button').forEach(b => b.addEventListener('click', () => { root.__mode = b.dataset.m; paint(); }));
  }
  requestAnimationFrame(paint);

  // camera glide to the target view box
  const from = root.__vb.slice(), to = d.bbox, dur = d.dur || 1100;
  if (from.some((v, i) => Math.abs(v - to[i]) > 0.01)) {
    cancelAnimationFrame(root.__raf);
    const t0 = performance.now();
    const step = now => {
      const t = Math.min(1, (now - t0) / dur), k = ease(t);
      root.__vb = from.map((v, i) => v + (to[i] - v) * k);
      svg.setAttribute('viewBox', root.__vb.join(' '));
      if (t < 1) root.__raf = requestAnimationFrame(step);
    };
    root.__raf = requestAnimationFrame(step);
  }

}
"""

# Mercator projection into a ~1000-unit wide canvas around Malaysia
_LON0, _K = 99.0, 62.0


def _proj(lon, lat):
    y = math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
    return (lon - _LON0) * _K, (0.13 - y) * _K * 57.2958


def _rings(geom):
    if geom["type"] == "Polygon":
        return geom["coordinates"]
    return [r for poly in geom["coordinates"] for r in poly]


@st.cache_resource
def build(geo_json_text: str):
    """Return (component, ids, state_bbox) — paths are projected once per server."""
    geo = json.loads(geo_json_text)
    ids, paths, boxes = [], [], {}
    for f in geo["features"]:
        pid = f["id"]
        st_name = f["properties"]["state"]
        parts, xs, ys = [], [], []
        for ring in _rings(f["geometry"]):
            pts = [_proj(lon, lat) for lon, lat in ring]
            xs += [p[0] for p in pts]; ys += [p[1] for p in pts]
            parts.append("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z")
        ids.append(pid)
        paths.append(f'<path d="{"".join(parts)}"/>')
        b = boxes.setdefault(st_name, [1e9, 1e9, -1e9, -1e9])
        boxes[st_name] = [min(b[0], min(xs)), min(b[1], min(ys)), max(b[2], max(xs)), max(b[3], max(ys))]
    allb = [min(b[0] for b in boxes.values()), min(b[1] for b in boxes.values()),
            max(b[2] for b in boxes.values()), max(b[3] for b in boxes.values())]
    boxes["All Malaysia"] = allb
    html = ('<div class="modes"></div><div class="mapbox"><div class="wrap"><svg preserveAspectRatio="xMidYMid meet">' + "".join(paths) +
            '</svg></div><div class="tip"></div></div><div class="legend"></div>')
    comp = st.components.v2.component("decentwork_smoothmap", html=html, css=CSS, js=JS)
    return comp, ids, boxes


def view_box(b, pad=0.06, aspect=1.45):
    """Padded view box [x, y, w, h], widened to the panel's aspect so zoom feels centred."""
    x0, y0, x1, y1 = b
    w, h = (x1 - x0) * (1 + 2 * pad), (y1 - y0) * (1 + 2 * pad)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    if w / h < aspect:
        w = h * aspect
    else:
        h = w / aspect
    return [round(cx - w / 2, 2), round(cy - h / 2, 2), round(w, 2), round(h, 2)]
