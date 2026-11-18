"""Profilbild 1080x1080 (TikTok schneidet rund zu) – Figur aus den Videos + Glühbirne mit Zahnrad."""
import ast, os, subprocess, math
SRC = os.path.join(os.path.dirname(__file__), "../videos/13_gondel/build.py")
tree = ast.parse(open(SRC, encoding="utf-8").read())
code = "FIGS=[]\n"
for node in tree.body:
    seg = ast.get_source_segment(open(SRC, encoding="utf-8").read(), node)
    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in ("FIG", "SKIN2", "HAIR", "LIP", "INK") for t in node.targets): code += seg + "\n"
    if isinstance(node, ast.Assign) and seg.startswith("FIG ="): code += seg + "\n"
    if isinstance(node, ast.FunctionDef) and node.name == "figure": code += seg + "\n"
g = {}; exec(code, g)
fig = g["figure"]("p-fig", 540, 1420, 2.6, eyes="w")

LIME = "#c8f031"; RED = "#ff3b3b"; GOLD = "#ffd98a"
teeth = "".join(f'<rect x="-9" y="-62" width="18" height="22" rx="4" fill="#20244f" transform="rotate({a})"/>' for a in range(0, 360, 45))
bulb = (f'<g transform="translate(770,330) rotate(14) scale(.85)">'
        f'<circle r="190" fill="url(#bulbglow)"/>'
        f'<path d="M -78 20 Q -110 -40 -98 -80 Q -80 -150 0 -158 Q 80 -150 98 -80 Q 110 -40 78 20 Q 52 52 50 92 L -50 92 Q -52 52 -78 20 Z" fill="{GOLD}" stroke="#fff6d8" stroke-width="8"/>'
        f'<rect x="-48" y="96" width="96" height="22" rx="8" fill="#9aa0c8"/><rect x="-44" y="122" width="88" height="20" rx="8" fill="#7b81a8"/><rect x="-26" y="146" width="52" height="16" rx="8" fill="#5a5f86"/>'
        f'<g transform="translate(0,-60)">{teeth}<circle r="44" fill="#20244f"/><circle r="17" fill="{GOLD}"/></g>'
        f'<path d="M -120 -190 l -26 -30 M 0 -215 l 0 -40 M 120 -190 l 26 -30 M 175 -90 l 38 -12 M -175 -90 l -38 -12" stroke="{LIME}" stroke-width="14" stroke-linecap="round"/></g>')
stars = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" opacity="{o}"/>' for x, y, r, o in
                ((160, 220, 4, .7), (260, 140, 3, .5), (120, 420, 3, .5), (930, 620, 4, .6), (980, 520, 3, .4), (200, 600, 2.5, .4)))
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080">
<defs>
<radialGradient id="bg" cx=".45" cy=".4" r=".75"><stop offset="0" stop-color="#2e2f7a"/><stop offset=".6" stop-color="#15163e"/><stop offset="1" stop-color="#0b0d26"/></radialGradient>
<radialGradient id="bulbglow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".55"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>
<radialGradient id="faceglow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{GOLD}" stop-opacity=".25"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>
</defs>
<rect width="1080" height="1080" fill="url(#bg)"/>{stars}
<circle cx="560" cy="560" r="470" fill="none" stroke="{LIME}" stroke-width="10" opacity=".35"/>
<circle cx="760" cy="330" r="420" fill="url(#faceglow)"/>
{bulb}
<g transform="translate(-30,0)">{fig}</g>
</svg>'''
open(os.path.join(os.path.dirname(__file__), "profilbild.svg"), "w", encoding="utf-8").write(svg)
print("svg ok")
