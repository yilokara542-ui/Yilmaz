"""Figuren-Blatt der neuen Hauptfigur: 4 Gesichtsausdrücke + Rückansicht."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from figur_c import make_figure, DEFS
FIGS = []; figure = make_figure(FIGS)
labels = [("n", "NEUTRAL"), ("w", "ERSCHROCKEN"), ("f", "ANGESPANNT"), ("s", "SCHLAFEND")]
out = "".join(f'{figure(f"f{i}", 200 + i*420, 1180, 2.0, eyes=e)}<text x="{200+i*420}" y="1260" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="38" fill="#cfd3ff">{t}</text>' for i, (e, t) in enumerate(labels))
out += f'{figure("fb", 1880, 1180, 2.0, back=True)}<text x="1880" y="1260" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="38" fill="#cfd3ff">RÜCKEN</text>'
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="2160" height="1350" viewBox="0 0 2160 1350"><defs>{DEFS}'
       f'<radialGradient id="bgs" cx=".5" cy=".4" r=".8"><stop offset="0" stop-color="#1d2a4f"/><stop offset="1" stop-color="#0b1226"/></radialGradient></defs>'
       f'<rect width="2160" height="1350" fill="url(#bgs)"/>'
       f'<rect x="40" y="40" width="720" height="70" rx="35" fill="#c8f031"/><text x="75" y="88" font-family="Poppins" font-weight="800" font-size="38" fill="#0b0d22">NEUE HAUPTFIGUR · SENF-HOODIE</text>{out}</svg>')
open(os.path.join(os.path.dirname(__file__), "figur_c_sheet.svg"), "w", encoding="utf-8").write(svg); print("ok")
