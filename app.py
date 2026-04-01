"""
app.py — RiskLab USTA
"""

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.DARKLY,
        "https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css",
    ],
    suppress_callback_exceptions=True,
    title="RiskLab · USTA",
)
server = app.server

C = {
    "bg"     : "#0A0E1A",
    "surface": "#111827",
    "border" : "#2A3347",
    "accent" : "#6C63FF",
    "accent2": "#00D4AA",
    "text"   : "#E8EDF5",
    "muted"  : "#8892A4",
    "gold"   : "#FFD166",
}

CSS = f"""
* {{ box-sizing: border-box; }}
body {{ background:{C['bg']}; font-family:'DM Mono',monospace; color:{C['text']}; margin:0; }}
#sidebar {{
    position:fixed; top:0; left:0; width:240px; height:100vh;
    background:{C['surface']}; border-right:1px solid {C['border']};
    display:flex; flex-direction:column; z-index:1000; overflow-y:auto;
}}
#content {{ margin-left:240px; padding:2rem 2.5rem; min-height:100vh; }}
.logo {{ padding:1.6rem 1.4rem; border-bottom:1px solid {C['border']}; }}
.logo-title {{ font-family:Syne,sans-serif; font-size:1.4rem; font-weight:800; letter-spacing:-0.02em; }}
.logo-sub {{ font-size:0.62rem; color:{C['muted']}; letter-spacing:0.15em; text-transform:uppercase; margin-top:3px; }}
.nav-label {{ font-size:0.58rem; letter-spacing:0.18em; text-transform:uppercase; color:{C['muted']}; padding:1rem 1.4rem 0.3rem; }}
.nav-link {{
    display:flex; align-items:center; gap:9px; padding:0.6rem 1.4rem;
    color:{C['muted']}; font-size:0.8rem; text-decoration:none;
    border-left:3px solid transparent; transition:all .18s;
}}
.nav-link:hover {{ color:{C['text']}; background:rgba(255,255,255,.04); text-decoration:none; }}
.nav-link.active {{ color:{C['text']}; border-left-color:{C['accent']}; background:rgba(108,99,255,.08); }}
.badge-pct {{ margin-left:auto; font-size:0.58rem; color:{C['accent']}; background:rgba(108,99,255,.15); padding:2px 6px; border-radius:20px; }}
.badge-new {{ margin-left:auto; font-size:0.58rem; color:{C['accent2']}; background:rgba(0,212,170,.12); padding:2px 6px; border-radius:20px; }}
::-webkit-scrollbar {{ width:4px; }}
::-webkit-scrollbar-thumb {{ background:{C['border']}; border-radius:2px; }}
"""

NAV = [
    ("PANEL",   None),
    ("overview","fa-house",                "Vista General",       None),
    ("MÓDULOS", None),
    ("m1",      "fa-chart-line",           "Análisis Técnico",    "12%"),
    ("m2",      "fa-wave-square",          "Rendimientos",        "8%"),
    ("m3",      "fa-fire",                 "ARCH / GARCH",        "12%"),
    ("m4",      "fa-shield-halved",        "CAPM & Beta",         "8%"),
    ("m5",      "fa-triangle-exclamation", "VaR & CVaR",          "12%"),
    ("m6",      "fa-bullseye",             "Markowitz",           "12%"),
    ("m7",      "fa-bolt",                 "Señales & Alertas",   "new"),
    ("m8",      "fa-globe",                "Macro & Benchmark",   "new"),
]

def sidebar(active="overview"):
    items = []
    for entry in NAV:
        if len(entry) == 2:
            items.append(html.Div(entry[0], className="nav-label"))
            continue
        page_id, icon, label, badge = entry
        badge_el = None
        if badge == "new":
            badge_el = html.Span("NEW", className="badge-new")
        elif badge:
            badge_el = html.Span(badge, className="badge-pct")
        items.append(html.A(
            [
                html.I(className=f"fa-solid {icon}",
                       style={"width": "16px", "textAlign": "center", "color": C["accent"]}),
                html.Span(label),
                badge_el,
            ],
            href=f"/{page_id}",
            className="nav-link" + (" active" if page_id == active else ""),
        ))
    return html.Div([
        html.Div([
            html.Div([
                html.Span("Risk", style={"color": C["accent"]}),
                html.Span("Lab"),
            ], className="logo-title"),
            html.Div("USTA · Teoría del Riesgo", className="logo-sub"),
        ], className="logo"),
        html.Nav(items),
    ], id="sidebar")


app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Style(CSS),
    html.Div(id="sidebar-wrap"),
    html.Div(id="content"),
])


@app.callback(
    Output("sidebar-wrap", "children"),
    Output("content", "children"),
    Input("url", "pathname"),
)
def route(path):
    page = (path or "/").lstrip("/") or "overview"

    try:
        if page == "overview":
            from pages.overview import layout
        elif page == "m1":
            from pages.m1_technical import layout
        elif page == "m2":
            from pages.m2_returns import layout
        elif page == "m3":
            from pages.m3_garch import layout
        elif page == "m4":
            from pages.m4_capm import layout
        elif page == "m5":
            from pages.m5_var import layout
        elif page == "m6":
            from pages.m6_markowitz import layout
        elif page == "m7":
            from pages.m7_signals import layout
        elif page == "m8":
            from pages.m8_macro import layout
        else:
            layout = html.Div("Página no encontrada",
                              style={"color": C["muted"], "padding": "3rem"})
    except ImportError:
        layout = html.Div(
            "🔧 Módulo en construcción",
            style={"color": C["accent"], "fontSize": "1.2rem",
                   "fontFamily": "Syne,sans-serif", "padding": "3rem"},
        )

    return sidebar(active=page), layout


if __name__ == "__main__":
    app.run(debug=True, port=8050)
