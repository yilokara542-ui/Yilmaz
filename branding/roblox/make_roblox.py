"""Blockfigur im Roblox-Stil (eigenes Design, basiert auf unserer Hauptfigur „Senf-Hoodie“). Kein Logo, keine Marken."""
import os
U = 70            # Block-Einheit in px
DX, DY = 34, -24  # Tiefe (3D-Versatz)


def box(x, y, w, h, front, side, top, extra=""):
    """Quader: Vorderseite + rechte Seite + Oberseite."""
    return (f'<polygon points="{x+w},{y} {x+w+DX},{y+DY} {x+w+DX},{y+h+DY} {x+w},{y+h}" fill="{side}"/>'
            f'<polygon points="{x},{y} {x+DX},{y+DY} {x+w+DX},{y+DY} {x+w},{y}" fill="{top}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{front}"/>{extra}')


M, M2, M3 = "#e0a83a", "#b8862a", "#f0c160"
SK, SK2, SK3 = "#e8b08a", "#c98a66", "#f2c4a0"
P, P2, P3 = "#23252e", "#15171e", "#33363f"
HAIR = "#1e1a2e"


def face_decal(cx, cy, mood):
    eyes = ""
    for s in (-1, 1):
        if mood == "happy":
            eyes += f'<path d="M {cx+s*30-14} {cy-6} Q {cx+s*30} {cy-22} {cx+s*30+14} {cy-6}" stroke="#111" stroke-width="7" fill="none" stroke-linecap="round"/>'
        elif mood == "shock":
            eyes += f'<circle cx="{cx+s*30}" cy="{cy-10}" r="15" fill="#fff" stroke="#111" stroke-width="4"/><circle cx="{cx+s*30}" cy="{cy-8}" r="6" fill="#111"/>'
        else:
            eyes += (f'<ellipse cx="{cx+s*30}" cy="{cy-10}" rx="13" ry="16" fill="#111"/><circle cx="{cx+s*30+4}" cy="{cy-16}" r="5" fill="#fff"/>'
                     f'<rect x="{cx+s*30-16}" y="{cy-40}" width="32" height="7" rx="3" fill="#111" transform="rotate({-s*8} {cx+s*30} {cy-36})"/>')
    mouth = {"happy": f'<path d="M {cx-26} {cy+18} Q {cx} {cy+44} {cx+26} {cy+18}" stroke="#111" stroke-width="7" fill="none" stroke-linecap="round"/>',
             "shock": f'<ellipse cx="{cx}" cy="{cy+28}" rx="13" ry="17" fill="#111"/>',
             "cool": f'<path d="M {cx-22} {cy+24} Q {cx+4} {cy+34} {cx+26} {cy+18}" stroke="#111" stroke-width="7" fill="none" stroke-linecap="round"/>'}[mood]
    return eyes + mouth


def avatar(x0, y0, mood="cool", back=False):
    """Oben links = (x0, y0). Kopf 1,2U breit, Rumpf 2x2U, Arme/Beine 1x2U."""
    out = ""
    # Beine
    for i, (f, s) in enumerate(((P, P2), (P3, P2))):
        lx = x0 + i * U
        out += box(lx, y0 + 4.3*U, U, 2*U, f, s, P3)
        out += f'<rect x="{lx+8}" y="{y0+5.0*U}" width="{U-16}" height="{0.45*U}" rx="6" fill="{P2}"/>'          # Cargo-Tasche
        out += box(lx - 4, y0 + 6.05*U, U + 8, 0.35*U, "#f2f3f5", "#cfd3da", "#ffffff") + f'<rect x="{lx-4}" y="{y0+6.32*U}" width="{U+8}" height="8" fill="#1e1a2e"/>'
    # Arme
    out += box(x0 - U, y0 + 2.3*U, U, 2*U, M, M2, M3, f'<rect x="{x0-U}" y="{y0+3.95*U}" width="{U}" height="{0.35*U}" fill="{SK}"/>')
    # Rumpf (Hoodie)
    tor = (f'<rect x="{x0+0.25*U}" y="{y0+3.45*U}" width="{1.5*U}" height="{0.55*U}" rx="10" fill="{M2}"/>' if not back else
           f'<path d="M {x0+0.2*U} {y0+2.3*U} Q {x0+U} {y0+3.1*U} {x0+1.8*U} {y0+2.3*U} Z" fill="{M2}"/>')
    if not back:
        tor += (f'<path d="M {x0+0.8*U} {y0+2.35*U} L {x0+0.75*U} {y0+3.1*U} M {x0+1.2*U} {y0+2.35*U} L {x0+1.25*U} {y0+3.1*U}" stroke="{HAIR}" stroke-width="7" stroke-linecap="round"/>'
                f'<circle cx="{x0+0.75*U}" cy="{y0+3.12*U}" r="7" fill="{HAIR}"/><circle cx="{x0+1.25*U}" cy="{y0+3.12*U}" r="7" fill="{HAIR}"/>')
    out += box(x0, y0 + 2.3*U, 2*U, 2*U, M, M2, M3, tor + f'<rect x="{x0}" y="{y0+4.05*U}" width="{2*U}" height="{0.25*U}" fill="{M2}"/>')
    # Kapuze-Kragen
    out += f'<rect x="{x0+0.3*U}" y="{y0+2.15*U}" width="{1.4*U}" height="{0.3*U}" rx="12" fill="{M2}"/>'
    out += box(x0 + 2*U, y0 + 2.3*U, U, 2*U, M, M2, M3, f'<rect x="{x0+2*U}" y="{y0+3.95*U}" width="{U}" height="{0.35*U}" fill="{SK}"/>')
    out += (f'<rect x="{x0-3}" y="{y0+2.3*U}" width="6" height="{2*U}" fill="#8a6420" opacity=".6"/>'
            f'<rect x="{x0+2*U-3}" y="{y0+2.3*U}" width="6" height="{2*U}" fill="#8a6420" opacity=".6"/>'
            f'<rect x="{x0+U-2}" y="{y0+4.3*U}" width="4" height="{1.75*U}" fill="#0b0c12" opacity=".7"/>')
    # Kopf
    hx, hy, hw = x0 + 0.3*U, y0 + 0.95*U, 1.4*U
    out += box(hx, hy, hw, 1.35*U, SK, SK2, SK3)
    if not back:
        out += face_decal(hx + hw/2, hy + 0.7*U, mood)
        out += f'<rect x="{hx-6}" y="{hy+0.45*U}" width="10" height="24" rx="4" fill="{SK2}"/><rect x="{hx+hw-4}" y="{hy+0.45*U}" width="10" height="24" rx="4" fill="{SK2}"/>'
    # Haar-Accessoire: Stachelfrisur (eckig, Block-Look)
    spikes = [(0, 0.0), (0.25, -0.45), (0.48, -0.2), (0.7, -0.62), (0.92, -0.25), (1.15, -0.5), (1.4, 0.0)]
    pts = " ".join(f"{hx + a*U:.0f},{hy + b*U:.0f}" for a, b in spikes)
    out += f'<polygon points="{hx-10},{hy+0.35*U} {pts} {hx+hw+10},{hy+0.35*U}" fill="{HAIR}"/>'
    out += f'<polygon points="{hx+hw+10},{hy+0.35*U} {hx+hw+10+DX},{hy+0.35*U+DY} {hx+hw+DX},{hy+DY} {hx+hw},{hy}" fill="#151225"/>'
    if back:
        out += f'<rect x="{hx-8}" y="{hy}" width="{hw+16}" height="{0.9*U}" fill="{HAIR}"/>'
    else:
        out += "".join(f'<polygon points="{hx + a*U:.0f},{hy+0.33*U} {hx + (a+0.12)*U:.0f},{hy+0.58*U} {hx + (a+0.24)*U:.0f},{hy+0.33*U}" fill="{HAIR}"/>' for a in (0.05, 0.4, 0.8, 1.1))
    return out


def panel_bg(w, h):
    return (f'<rect width="{w}" height="{h}" fill="url(#bg)"/>'
            + "".join(f'<rect x="{x}" y="0" width="2" height="{h}" fill="#fff" opacity=".04"/>' for x in range(0, w, 60))
            + "".join(f'<rect x="0" y="{y}" width="{w}" height="2" fill="#fff" opacity=".04"/>' for y in range(0, h, 60)))


W, H = 2160, 1100
out = panel_bg(W, H)
out += f'<rect x="40" y="40" width="760" height="70" rx="35" fill="#c8f031"/><text x="75" y="88" font-family="Poppins" font-weight="800" font-size="38" fill="#0b0d22">BLOCK-AVATAR · SENF-HOODIE</text>'
for k, (mood, back, lbl) in enumerate((("cool", False, "VORNE"), ("happy", False, "FREUT SICH"), ("shock", False, "ERSCHROCKEN"), ("cool", True, "HINTEN"))):
    cx = 270 + k * 520
    out += f'<ellipse cx="{cx+35}" cy="815" rx="170" ry="22" fill="#000" opacity=".35"/>'
    out += f'<g transform="translate({cx - U},{240}) scale(1.25)">{avatar(0, 0, mood, back)}</g>'
    out += f'<text x="{cx+35}" y="930" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="40" fill="#cfd3ff">{lbl}</text>'
out += f'<text x="{W/2}" y="1020" text-anchor="middle" font-family="Poppins" font-weight="600" font-size="30" fill="#8f94c4">Senfgelber Hoodie · schwarze Cargo · weiße Sneaker · Stachel-Frisur · Gesichts-Decals</text>'
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs>'
       f'<radialGradient id="bg" cx=".5" cy=".45" r=".8"><stop offset="0" stop-color="#3b8de0"/><stop offset="1" stop-color="#1b3f7a"/></radialGradient></defs>{out}</svg>')
open(os.path.join(os.path.dirname(__file__), "roblox_avatar.svg"), "w", encoding="utf-8").write(svg)
print("ok")
