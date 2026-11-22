"""Format D „Strichmännchen-Mythos“ – Zeichen-Baukasten (eigener Stil nach Referenz 22.11.).

Alle Funktionen liefern SVG-Strings im 1080×1920-Raster. Farben exakt aus der Referenz gemessen.
"""
import html as _html
import random as _random

INK = "#140F0C"; BG = "#F3ECE5"; SKIN = "#F4D5B6"; UNDER = "#F2C8C9"; HAIR = "#3D2922"
YEL = "#F4C23E"; PINK = "#F1A1A4"; RED = "#E3454C"; RED_BG = "#FDE3E2"; LILA = "#6A4BD0"; LILA_BG = "#ECE6FF"
GROUND = "#D8CFC2"; BLUE = "#3B82F6"; WATER = "#5BA8F5"; DARK = "#22212A"; CURTAIN = "#5C396F"; SEPIA = "#E6D9C2"
FONT = "Nunito, 'Nunito Black', Poppins, sans-serif"
LW = 12  # Linienstärke Körper

_R = _random.Random(4)


def esc(t):
    return _html.escape(t)


# ---------------------------------------------------------------- Gesicht & Figur
def face(mood, cx=0, cy=0, col=INK, k=1.0):
    e = ""
    ex = 19 * k; ey = cy - 8 * k
    if mood == "shock":
        e = (f'<circle cx="{cx-ex}" cy="{ey}" r="{9*k}" fill="#fff" stroke="{col}" stroke-width="{3.5*k}"/><circle cx="{cx-ex}" cy="{ey}" r="{3.5*k}" fill="{col}"/>'
             f'<circle cx="{cx+ex}" cy="{ey}" r="{9*k}" fill="#fff" stroke="{col}" stroke-width="{3.5*k}"/><circle cx="{cx+ex}" cy="{ey}" r="{3.5*k}" fill="{col}"/>')
    elif mood in ("laugh", "smug"):
        e = "".join(f'<path d="M {cx+s*ex-9*k} {ey+2*k} Q {cx+s*ex} {ey-9*k} {cx+s*ex+9*k} {ey+2*k}" stroke="{col}" stroke-width="{4.5*k}" fill="none" stroke-linecap="round"/>' for s in (-1, 1))
    elif mood == "dumb":
        e = (f'<circle cx="{cx-ex}" cy="{ey}" r="{7*k}" fill="#fff" stroke="{col}" stroke-width="{3*k}"/><circle cx="{cx-ex+4*k}" cy="{ey+1*k}" r="{3*k}" fill="{col}"/>'
             f'<circle cx="{cx+ex}" cy="{ey-2*k}" r="{9.5*k}" fill="#fff" stroke="{col}" stroke-width="{3*k}"/><circle cx="{cx+ex-5*k}" cy="{ey}" r="{3*k}" fill="{col}"/>')
    else:
        e = f'<circle cx="{cx-ex}" cy="{ey}" r="{5.5*k}" fill="{col}"/><circle cx="{cx+ex}" cy="{ey}" r="{5.5*k}" fill="{col}"/>'
    m = {
        "smile": f'<path d="M {cx-20*k} {cy+12*k} Q {cx} {cy+30*k} {cx+20*k} {cy+12*k}" stroke="{col}" stroke-width="{4.5*k}" fill="none" stroke-linecap="round"/>',
        "laugh": f'<path d="M {cx-24*k} {cy+8*k} Q {cx} {cy+46*k} {cx+24*k} {cy+8*k} Z" fill="{col}"/>',
        "smug": f'<path d="M {cx-16*k} {cy+18*k} Q {cx+6*k} {cy+26*k} {cx+22*k} {cy+10*k}" stroke="{col}" stroke-width="{4.5*k}" fill="none" stroke-linecap="round"/>',
        "sad": f'<path d="M {cx-17*k} {cy+26*k} Q {cx} {cy+12*k} {cx+17*k} {cy+26*k}" stroke="{col}" stroke-width="{4.5*k}" fill="none" stroke-linecap="round"/>',
        "shock": f'<ellipse cx="{cx}" cy="{cy+22*k}" rx="{8*k}" ry="{11*k}" fill="none" stroke="{col}" stroke-width="{4*k}"/>',
        "dumb": f'<path d="M {cx-18*k} {cy+20*k} Q {cx-8*k} {cy+28*k} {cx} {cy+20*k} Q {cx+8*k} {cy+12*k} {cx+18*k} {cy+22*k}" stroke="{col}" stroke-width="{4*k}" fill="none" stroke-linecap="round"/>',
    }.get(mood, f'<line x1="{cx-15*k}" y1="{cy+20*k}" x2="{cx+15*k}" y2="{cy+20*k}" stroke="{col}" stroke-width="{4.5*k}" stroke-linecap="round"/>')
    return e + m


ARMS = {
    "down": ((-56, -170), (-36, -262), (36, -262), (56, -170)),
    "hold": ((-56, -170), (-36, -262), (62, -292), (104, -258)),      # rechte Hand vorne auf Brusthöhe
    "ear": ((-56, -170), (-36, -262), (70, -300), (52, -404)),        # rechte Hand am Ohr/Gesicht
    "both": ((-104, -258), (-62, -292), (62, -292), (104, -258)),     # beide Hände vorne
    "shrug": ((-110, -330), (-70, -280), (70, -280), (110, -330)),
}


def stick(fid, x, y, s=1.0, mood="smile", pose="down", moods=(), white=False, stubble=False, extra=""):
    """Strichmännchen, Füße bei (x,y). Höhe ≈ 480·s. Gesichter für alle `moods` werden mitgezeichnet (umschaltbar)."""
    col = "#ffffff" if white else INK
    head_fill = "#ffffff"
    (lh, le, re, rh) = ARMS[pose]
    body = (f'<path d="M -34 0 L -16 -100 L 0 -200 L 16 -100 L 34 0" stroke="{col}" stroke-width="{LW}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<line x1="0" y1="-200" x2="0" y2="-358" stroke="{col}" stroke-width="{LW}" stroke-linecap="round"/>'
            f'<path d="M {lh[0]} {lh[1]} L {le[0]} {le[1]} L 0 -340 L {re[0]} {re[1]} L {rh[0]} {rh[1]}" stroke="{col}" stroke-width="{LW}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            + "".join(f'<circle cx="{px}" cy="{py}" r="7" fill="{col}"/>' for px, py in (lh, rh, (-34, 0), (34, 0))))
    head = f'<circle cx="0" cy="-418" r="58" fill="{head_fill}" stroke="{col}" stroke-width="7"/>'
    if stubble:
        head += "".join(f'<circle cx="{_R.uniform(-40,40):.0f}" cy="{_R.uniform(-392,-368):.0f}" r="2.6" fill="{INK}"/>' for _ in range(14))
    allm = [mood] + [m for m in moods if m != mood]
    faces = "".join(f'<g id="{fid}-f-{m}" opacity="{1 if m == mood else 0}">{face(m, 0, -418, INK)}</g>' for m in allm)
    return f'<g id="{fid}"><g transform="translate({x},{y}) scale({s})"><g id="{fid}-b">{body}{head}{faces}{extra}</g></g></g>'


def hand_pos(x, y, s, pose="hold", side="r"):
    lh, le, re, rh = ARMS[pose]
    p = rh if side == "r" else lh
    return x + p[0] * s, y + p[1] * s


# ---------------------------------------------------------------- Bausteine
def ground(y=1300, x0=60, x1=1020):
    return f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{GROUND}" stroke-width="5" stroke-linecap="round"/>'


def text(x, y, t, size=56, col=INK, weight=900, anchor="middle", extra=""):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{FONT}" font-weight="{weight}" font-size="{size}" fill="{col}" {extra}>{esc(t)}</text>'


def pill(pid, x, y, t, kind="white", size=42, op=0):
    w = len(t) * size * 0.6 + 52; h = size * 1.7
    fill, stroke, tc = {"white": ("#ffffff", INK, INK), "red": (RED_BG, RED, RED), "lila": (LILA_BG, LILA, LILA)}[kind]
    return (f'<g id="{pid}" opacity="{op}"><rect x="{x-w/2:.0f}" y="{y-h/2:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{h*0.32:.0f}" fill="{fill}" stroke="{stroke}" stroke-width="4"/>'
            + text(x, y + size * 0.36, t, size, tc, 800) + '</g>')


def leader(x1, y1, x2, y2, col=INK):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="3.5"/>'


def xcircle(x, y, r=30):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{RED_BG}" stroke="{RED}" stroke-width="4"/>'
            f'<path d="M {x-r*.42} {y-r*.42} L {x+r*.42} {y+r*.42} M {x+r*.42} {y-r*.42} L {x-r*.42} {y+r*.42}" stroke="{RED}" stroke-width="5" stroke-linecap="round"/>')


def checkcircle(x, y, r=30):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{LILA_BG}" stroke="{LILA}" stroke-width="4"/>'
            f'<path d="M {x-r*.45} {y} L {x-r*.1} {y+r*.38} L {x+r*.48} {y-r*.36}" stroke="{LILA}" stroke-width="5.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')


def listrow(rid, x, y, w, t, mark="x", size=44, op=0, icon=""):
    h = size * 2.0
    m = xcircle(x + w - 50, y, 26) if mark == "x" else checkcircle(x + w - 50, y, 26)
    return (f'<g id="{rid}" opacity="{op}"><rect x="{x}" y="{y-h/2}" width="{w}" height="{h}" rx="22" fill="#ffffff" stroke="{INK}" stroke-width="5"/>'
            + icon + text(x + (110 if icon else 34), y + size * 0.36, t, size, INK, 800, "start") + m + '</g>')


def phone(x, y, w=200, h=380, screen="#BFE3F5", body="#3A3A44", extra="", rot=0):
    """Handy, (x,y) = Mitte. Flach mit schwarzer Kontur."""
    r = w * 0.16
    return (f'<g transform="rotate({rot} {x} {y})"><rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="{r}" fill="{body}" stroke="{INK}" stroke-width="6"/>'
            f'<rect x="{x-w/2+w*0.08}" y="{y-h/2+h*0.06}" width="{w*0.84}" height="{h*0.88}" rx="{r*0.6}" fill="{screen}"/>'
            f'<line x1="{x-w/2+w*0.2}" y1="{y-h/2+h*0.12}" x2="{x-w/2+w*0.32}" y2="{y-h/2+h*0.2}" stroke="#ffffff" stroke-width="5" stroke-linecap="round" opacity=".8"/>'
            f'{extra}</g>')


def drop(x, y, s=1.0, col=WATER):
    return (f'<path d="M {x} {y-30*s} C {x+6*s} {y-14*s} {x+20*s} {y-2*s} {x+20*s} {y+10*s} A {20*s} {20*s} 0 0 1 {x-20*s} {y+10*s} '
            f'C {x-20*s} {y-2*s} {x-6*s} {y-14*s} {x} {y-30*s} Z" fill="{col}" stroke="{INK}" stroke-width="{3.5*s:.1f}"/>')


def grain(x, y, rot=0, s=1.0, faced=None):
    g = f'<ellipse cx="{x}" cy="{y}" rx="{13*s}" ry="{6.5*s}" fill="#ffffff" stroke="{INK}" stroke-width="{2.6*min(s,2):.1f}" transform="rotate({rot} {x} {y})"/>'
    if faced:
        g += face(faced, x, y - 2 * s, INK, s * 0.22)
    return g


def rice_pile(cx, cy, w, h, n=120, seed=1):
    rr = _random.Random(seed)
    out = ""
    for _ in range(n):
        gx = rr.uniform(-1, 1); gy = rr.uniform(0, 1)
        if gx * gx + (1 - gy) ** 2 * 0.0 > 1:
            continue
        x = cx + gx * w / 2 * (1 - gy * 0.15); y = cy - gy * h * (1 - abs(gx) ** 2)
        out += grain(round(x), round(y), rr.randint(0, 180))
    return out


def bowl(cx, cy, w=420, h=170, col="#ffffff", rim=BLUE, inside=""):
    """Schüssel, (cx,cy) = Mitte Oberkante."""
    return (inside + f'<path d="M {cx-w/2} {cy} Q {cx-w/2+10} {cy+h} {cx} {cy+h} Q {cx+w/2-10} {cy+h} {cx+w/2} {cy} Z" fill="{col}" stroke="{INK}" stroke-width="6"/>'
            f'<rect x="{cx-w/2-8}" y="{cy-8}" width="{w+16}" height="18" rx="9" fill="{rim}" stroke="{INK}" stroke-width="5"/>')


def toilet(x, y, s=1.0):
    """Klo seitlich, (x,y) = Boden-Mitte."""
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<rect x="40" y="-330" width="90" height="170" rx="14" fill="#ffffff" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M -130 -170 L 130 -170 Q 120 -60 30 -40 L 40 0 L -60 0 L -50 -40 Q -125 -70 -130 -170 Z" fill="#ffffff" stroke="{INK}" stroke-width="6"/>'
            f'<ellipse cx="0" cy="-170" rx="130" ry="20" fill="#ffffff" stroke="{INK}" stroke-width="6"/>'
            f'<ellipse cx="0" cy="-168" rx="100" ry="11" fill="{WATER}" opacity=".85"/></g>')


def cloud(x, y, s=1.0, inner=""):
    """Gedankenblase, (x,y)=Mitte; zwei kleine Kreise nach unten links."""
    pts = ((-70, 0, 55), (-20, -40, 62), (45, -30, 58), (80, 15, 48), (20, 40, 55), (-45, 38, 48))
    st = "".join(f'<circle cx="{x+a*s}" cy="{y+b*s}" r="{r*s}" fill="#ffffff" stroke="{INK}" stroke-width="5"/>' for a, b, r in pts)
    fi = "".join(f'<circle cx="{x+a*s}" cy="{y+b*s}" r="{(r-5)*s}" fill="#ffffff"/>' for a, b, r in pts)
    tail = (f'<circle cx="{x-90*s}" cy="{y+95*s}" r="{14*s}" fill="#ffffff" stroke="{INK}" stroke-width="4"/>'
            f'<circle cx="{x-118*s}" cy="{y+130*s}" r="{8*s}" fill="#ffffff" stroke="{INK}" stroke-width="4"/>')
    return st + fi + tail + inner


def polaroid(x, y, w, h, rot, inner, caption=""):
    return (f'<g transform="rotate({rot} {x+w/2} {y+h/2})"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#ffffff" stroke="{INK}" stroke-width="6"/>'
            f'<rect x="{x+26}" y="{y+26}" width="{w-52}" height="{h-120}" fill="{SEPIA}" stroke="{INK}" stroke-width="3"/>{inner}'
            + (text(x + w / 2, y + h - 38, caption, 52, INK, 900) if caption else "") + '</g>')


def qmark(x, y, size=260, col=LILA):
    return text(x, y, "?", size, col, 900)


def finger(x, y, s=1.0, flip=False):
    """Großer Zeigefinger von rechts (zeigt nach links), (x,y) = Fingerspitze."""
    f = -1 if flip else 1
    return (f'<g transform="translate({x},{y}) scale({s*f},{s})">'
            f'<rect x="0" y="-26" width="240" height="52" rx="26" fill="{SKIN}" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="200" y="-56" width="420" height="112" rx="40" fill="{SKIN}" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M 20 -18 Q 8 0 20 18" stroke="{INK}" stroke-width="3" fill="none"/>'
            + "".join(f'<line x1="{xx}" y1="-50" x2="{xx}" y2="50" stroke="#d8b494" stroke-width="3"/>' for xx in (260, 290)) + '</g>')
