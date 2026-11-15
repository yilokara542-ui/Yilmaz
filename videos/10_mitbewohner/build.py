#!/usr/bin/env python3
"""Generator für index.html – Video 10 „Heimlicher Mitbewohner“ (Skill-Format A „Erklär-Story“).

Alle Zeiten kommen aus assets/words.json (wortgenaue Voiceover-Zeitstempel).
Aufruf: python3 build.py → index.html + assets/cues.json
"""
import json, re, html, os, math, random, zlib, struct, base64

HERE = os.path.dirname(os.path.abspath(__file__))
W = json.load(open(os.path.join(HERE, "assets/words.json"), encoding="utf-8"))
VO_END = W[-1]["e"]
TOTAL = round(VO_END + 1.6, 2)          # Schlussfrage steht noch kurz
XF = 0.3                                 # Überblendung zwischen Szenen
RNG = random.Random(10)

# ---------- Farben: Nacht-Palette (Format B) ----------
SKY1 = "#0b0d26"; SKY2 = "#1d1d4f"; VIO = "#2a2360"; BLD = "#141634"; BLD2 = "#1b1d44"
WIN = "#ffd98a"; LAMP = "#ffd98a"; MOON = "#f4e3a1"; STREET = "#191a33"; WALK = "#25264a"
FIG = "#d9dde3"; INK = "#151a21"; RED = "#ff3b3b"; LIME = "#c8f031"; BLUE = "#3b6cff"; WHITE = "#ffffff"
TEAL = "#3fd1c4"; CARD_BG = "#0b0d22"

T = []


def tw(code):
    T.append(code)


def ws(prefix, after=0.0):
    for w in W:
        if w["s"] >= after - 1e-6 and re.sub(r"[^\wäöüÄÖÜß]", "", w["t"]).lower().startswith(prefix.lower()):
            return w["s"]
    raise KeyError(prefix)


def toggle(sel, t_on, t_off=None):
    tw(f'tl.set("{sel}",{{opacity:1}},{t_on:.3f});')
    if t_off is not None:
        tw(f'tl.set("{sel}",{{opacity:0}},{t_off:.3f});')


def pop(sel, t, dur=0.32, frm=0.88):
    tw(f'tl.fromTo("{sel}",{{opacity:0,scale:{frm},transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:{dur},ease:"power3.out"}},{t:.3f});')


def fade_out(sel, t, dur=0.25):
    tw(f'tl.to("{sel}",{{opacity:0,duration:{dur},ease:"sine.inOut"}},{t:.3f});')


def shake(sel, t, n=6, amp=8):
    for i in range(n):
        x = amp * (1 if i % 2 == 0 else -1) * (1 - i / n)
        tw(f'tl.to("{sel}",{{x:{x:.1f},y:{-x/3:.1f},duration:.06,ease:"sine.inOut"}},{t + i*0.06:.3f});')
    tw(f'tl.to("{sel}",{{x:0,y:0,duration:.12,ease:"sine.out"}},{t + n*0.06:.3f});')


def move(sel, t, dur, ease="sine.inOut", **kw):
    vars_ = ",".join(f"{k}:{v}" for k, v in kw.items())
    tw(f'tl.to("{sel}",{{{vars_},duration:{dur:.3f},ease:"{ease}"}},{t:.3f});')


# ---------- Figuren ----------
FIGS = []


def figure(fid, x, y, s=1.0, eyes="n", outfit="hoodie", back=False):
    """Gesichtslose Puppe mit Kleidung (Skill 6). outfit: hoodie | vest (Kassierer)."""
    FIGS.append(fid)
    if outfit == "shirt":   # Mann in Japan: helles Hemd, Krawatte, dunkle Hose
        H, H2, P, SH = "#dfe6ef", "#c9d2de", "#2b2f3a", "#1a1d22"
        extra = '<polygon points="-6,-250 6,-250 10,-150 0,-136 -10,-150" fill="#8b2a2a"/><polygon points="-24,-258 0,-240 24,-258 24,-250 0,-232 -24,-250" fill="#c9d2de"/>'
    elif outfit == "vest":
        H, H2, P, SH = "#c0392b", "#9b2d22", "#2c3a52", "#1a1d22"
        extra = '<rect x="-44" y="-250" width="88" height="140" rx="20" fill="#e6e9ee"/><rect x="-40" y="-250" width="80" height="140" rx="18" fill="#2f7a4a"/><rect x="18" y="-210" width="18" height="10" rx="3" fill="#e6e9ee"/>'
        H = "#e6e9ee"; H2 = "#cfd3da"
    else:
        H, H2, P, SH = "#2f6f73", "#265b5e", "#2c3a52", "#eef0f3"
        extra = ('<ellipse cx="0" cy="-252" rx="46" ry="16" fill="#1f4b4e"/>'
                 '<rect x="-12" y="-248" width="4" height="40" rx="2" fill="#e6e9ee"/><rect x="8" y="-248" width="4" height="40" rx="2" fill="#e6e9ee"/>'
                 '<rect x="-40" y="-178" width="80" height="34" rx="12" fill="#265b5e"/>')
    if back:
        extra = '<ellipse cx="0" cy="-262" rx="52" ry="34" fill="#265b5e"/>'
    def eye(name, op, body):
        return f'<g id="{fid}-eyes-{name}" opacity="{op}">{body}</g>'
    E = INK
    eyes_svg = "" if back else (
        eye("n", 1 if eyes == "n" else 0,
            f'<circle cx="-22" cy="-322" r="9" fill="{E}"/><circle cx="22" cy="-322" r="9" fill="{E}"/>'
            f'<rect x="-36" y="-346" width="26" height="6" rx="3" fill="{E}"/><rect x="10" y="-346" width="26" height="6" rx="3" fill="{E}"/>'
            f'<rect x="-12" y="-290" width="24" height="5" rx="2.5" fill="{E}"/>')
        + eye("w", 1 if eyes == "w" else 0,
              f'<circle cx="-24" cy="-322" r="17" fill="none" stroke="{E}" stroke-width="5"/><circle cx="24" cy="-322" r="17" fill="none" stroke="{E}" stroke-width="5"/>'
              f'<circle cx="-24" cy="-322" r="5" fill="{E}"/><circle cx="24" cy="-322" r="5" fill="{E}"/>'
              f'<rect x="-42" y="-356" width="28" height="6" rx="3" fill="{E}" transform="rotate(-12 -28 -353)"/>'
              f'<rect x="14" y="-356" width="28" height="6" rx="3" fill="{E}" transform="rotate(12 28 -353)"/>'
              f'<ellipse cx="0" cy="-284" rx="9" ry="12" fill="{E}"/>')
        + eye("f", 1 if eyes == "f" else 0,
              f'<circle cx="-22" cy="-322" r="9" fill="{E}"/><circle cx="22" cy="-322" r="9" fill="{E}"/>'
              f'<rect x="-38" y="-350" width="28" height="6" rx="3" fill="{E}" transform="rotate(14 -24 -347)"/>'
              f'<rect x="10" y="-350" width="28" height="6" rx="3" fill="{E}" transform="rotate(-14 24 -347)"/>'
              f'<rect x="-14" y="-290" width="28" height="6" rx="3" fill="{E}"/>'))
    return f'''<g id="{fid}"><g transform="translate({x},{y}) scale({s})">
  <ellipse cx="0" cy="4" rx="78" ry="15" fill="#000" opacity=".4"/>
  <g id="{fid}-body">
  <g id="{fid}-legL"><rect x="-34" y="-128" width="27" height="124" rx="12" fill="{P}"/><ellipse cx="-22" cy="-6" rx="25" ry="12" fill="{SH}"/></g>
  <g id="{fid}-legR"><rect x="7" y="-128" width="27" height="124" rx="12" fill="{P}"/><ellipse cx="22" cy="-6" rx="25" ry="12" fill="{SH}"/></g>
  <rect x="-62" y="-258" width="124" height="152" rx="36" fill="{H}"/>
  <rect x="-62" y="-128" width="124" height="18" rx="9" fill="{H2}"/>
  {extra}
  <rect x="-88" y="-248" width="28" height="112" rx="13" fill="{H}"/>
  <rect x="60" y="-248" width="28" height="112" rx="13" fill="{H}"/>
  <rect x="-88" y="-150" width="28" height="14" rx="6" fill="{H2}"/><rect x="60" y="-150" width="28" height="14" rx="6" fill="{H2}"/>
  <circle cx="-74" cy="-126" r="13" fill="{FIG}"/><circle cx="74" cy="-126" r="13" fill="{FIG}"/>
  <rect x="-12" y="-278" width="24" height="26" rx="8" fill="{FIG}"/>
  <circle cx="0" cy="-320" r="64" fill="{FIG}"/>
  {eyes_svg}
  </g>
</g></g>'''


def stalker(sid, x, y, s=1.0):
    """Dunkle Kapuzen-Silhouette, Hände in den Taschen, kein Gesicht."""
    D, D2 = "#07081a", "#11132e"
    return f'''<g id="{sid}"><g transform="translate({x},{y}) scale({s})">
  <ellipse cx="0" cy="4" rx="80" ry="15" fill="#000" opacity=".5"/>
  <g id="{sid}-body">
  <g id="{sid}-legL"><rect x="-36" y="-130" width="30" height="126" rx="12" fill="{D}"/></g>
  <g id="{sid}-legR"><rect x="6" y="-130" width="30" height="126" rx="12" fill="{D}"/></g>
  <rect x="-66" y="-262" width="132" height="160" rx="38" fill="{D2}"/>
  <rect x="-80" y="-250" width="30" height="96" rx="14" fill="{D2}"/><rect x="50" y="-250" width="30" height="96" rx="14" fill="{D2}"/>
  <rect x="-46" y="-176" width="92" height="40" rx="14" fill="{D}"/>
  <path d="M -76 -300 Q -76 -400 0 -404 Q 76 -400 76 -300 L 70 -256 L -70 -256 Z" fill="{D2}"/>
  <ellipse cx="0" cy="-308" rx="46" ry="52" fill="#000"/>
  <rect x="-66" y="-262" width="132" height="160" rx="38" fill="none" stroke="#3b3f7a" stroke-width="3" opacity=".6"/>
  </g>
</g></g>'''


def walk_cycle(fid, t0, t1, period=0.55, bob=8):
    n = max(1, int((t1 - t0) / period))
    tw(f'tl.fromTo("#{fid}-body",{{y:0}},{{y:-{bob},duration:{period/2:.3f},yoyo:true,repeat:{n*2-1},ease:"sine.inOut"}},{t0:.3f});')
    tw(f'tl.fromTo("#{fid}-legL",{{y:0}},{{y:-14,duration:{period/2:.3f},yoyo:true,repeat:{n*2-1},ease:"sine.inOut"}},{t0:.3f});')
    tw(f'tl.fromTo("#{fid}-legR",{{y:-14}},{{y:0,duration:{period/2:.3f},yoyo:true,repeat:{n*2-1},ease:"sine.inOut"}},{t0:.3f});')


# ---------- Hintergründe ----------
def sky(stars=True):
    st = "".join(f'<circle cx="{RNG.randint(0,1080)}" cy="{RNG.randint(0,700)}" r="{RNG.choice([1.5,2,2.5,3])}" fill="#fff" opacity="{RNG.uniform(.25,.8):.2f}"/>' for _ in range(60)) if stars else ""
    return (f'<rect width="1080" height="1920" fill="url(#skyg)"/>{st}'
            f'<circle cx="820" cy="330" r="70" fill="{MOON}"/><circle cx="820" cy="330" r="150" fill="url(#moonglow)"/>')


def buildings(gid, y_base=1250, width=2400, far=False):
    out = []
    x = -200
    col = BLD2 if far else BLD
    while x < width:
        w = RNG.randint(170, 300); h = RNG.randint(380, 760) if not far else RNG.randint(500, 900)
        out.append(f'<rect x="{x}" y="{y_base-h}" width="{w}" height="{h}" fill="{col}"/>')
        if not far:
            out.append(f'<rect x="{x}" y="{y_base-h}" width="{w}" height="10" fill="#2a2d63"/>')
        for wy in range(y_base - h + 40, y_base - 80, 70):
            for wx in range(x + 24, x + w - 30, 52):
                if RNG.random() < (0.16 if far else 0.24):
                    out.append(f'<rect x="{wx}" y="{wy}" width="26" height="34" rx="3" fill="{WIN}" opacity="{RNG.uniform(.35,.85):.2f}"/>')
                elif not far:
                    out.append(f'<rect x="{wx}" y="{wy}" width="26" height="34" rx="3" fill="#0d0f26"/>')
        x += w + RNG.randint(4, 30)
    return f'<g id="{gid}">{"".join(out)}</g>'


def lamps(gid, y_base=1290, width=2400, step=520):
    out = []
    for x in range(120, width, step):
        out.append(f'<polygon points="{x+40},{y_base-560} {x+60},{y_base-560} {x+230},{y_base+60} {x-130},{y_base+60}" fill="url(#lampcone)"/>'
                   f'<rect x="{x}" y="{y_base-580}" width="14" height="600" fill="#2a2d55"/>'
                   f'<rect x="{x}" y="{y_base-584}" width="70" height="12" rx="6" fill="#2a2d55"/>'
                   f'<ellipse cx="{x+52}" cy="{y_base-566}" rx="26" ry="10" fill="{LAMP}"/>'
                   f'<ellipse cx="{x+50}" cy="{y_base+40}" rx="150" ry="22" fill="{LAMP}" opacity=".12"/>')
    return f'<g id="{gid}">{"".join(out)}</g>'


def street(prefix, parallax=True):
    """Nachtstraße mit Häusern, Laternen, Gehweg. Gruppen {prefix}-far/-near/-lamps lassen sich verschieben."""
    return (sky()
            + buildings(f"{prefix}-far", 1180, far=True)
            + buildings(f"{prefix}-near", 1270)
            + f'<rect x="0" y="1270" width="1080" height="650" fill="{WALK}"/>'
            + f'<g id="{prefix}-tiles">' + "".join(f'<rect x="{x}" y="1270" width="4" height="250" fill="#1d1e3e"/>' for x in range(-200, 2400, 120)) + '</g>'
            + f'<rect x="0" y="1520" width="1080" height="24" fill="#3a3c6a"/><rect x="0" y="1544" width="1080" height="376" fill="{STREET}"/>'
            + f'<g id="{prefix}-mark">' + "".join(f'<rect x="{x}" y="1720" width="120" height="14" rx="5" fill="#d9dbe8" opacity=".55"/>' for x in range(-200, 2600, 240)) + '</g>'
            + lamps(f"{prefix}-lamps"))


def scroll_street(prefix, t0, t1, speed=1.0):
    d = t1 - t0
    move(f"#{prefix}-far", t0, d, "none", x=int(-60 * d * speed))
    move(f"#{prefix}-near", t0, d, "none", x=int(-140 * d * speed))
    move(f"#{prefix}-lamps", t0, d, "none", x=int(-170 * d * speed))
    move(f"#{prefix}-tiles", t0, d, "none", x=int(-170 * d * speed))
    move(f"#{prefix}-mark", t0, d, "none", x=int(-170 * d * speed))


def label(lid, x, y, text, col=RED, size=40, op=0, fill="#0b0d22"):
    w = len(text) * size * 0.66 + 52
    return (f'<g id="{lid}" opacity="{op}"><rect x="{x-w/2:.0f}" y="{y-size*0.95:.0f}" width="{w:.0f}" height="{size*1.42:.0f}" rx="{size*0.71:.0f}" '
            f'fill="{fill}" fill-opacity=".9" stroke="{col}" stroke-width="5"/>'
            f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Poppins, sans-serif" font-weight="700" font-size="{size}" fill="{col}">{html.escape(text)}</text></g>')


def pill(pid, x, y, text, bg, fg="#fff", size=46, op=0):
    w = len(text) * size * 0.64 + 70
    return (f'<g id="{pid}" opacity="{op}"><rect x="{x-w/2:.0f}" y="{y-size*1.05:.0f}" width="{w:.0f}" height="{size*1.6:.0f}" rx="{size*0.8:.0f}" fill="{bg}"/>'
            f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Poppins, sans-serif" font-weight="700" font-size="{size}" fill="{fg}">{html.escape(text)}</text></g>')


def xmark(xid, cx, cy, r=110, op=0):
    return (f'<g id="{xid}" opacity="{op}"><rect x="{cx-16}" y="{cy-r}" width="32" height="{2*r}" rx="16" fill="{RED}" transform="rotate(45 {cx} {cy})"/>'
            f'<rect x="{cx-16}" y="{cy-r}" width="32" height="{2*r}" rx="16" fill="{RED}" transform="rotate(-45 {cx} {cy})"/></g>')


SCENES = []


def scene(sid, t0, t1, inner, drift=True):
    SCENES.append((sid, t0, t1, f'<g id="{sid}-cam">{inner}</g>'))
    if drift:
        tw(f'tl.fromTo("#{sid}-cam",{{scale:1,rotation:-0.4,svgOrigin:"540 960"}},{{scale:1.06,rotation:0.4,duration:{t1-t0+XF:.3f},ease:"sine.inOut"}},{t0:.3f});')


# ================= CUES =================
WALL = "#1c2230"; WALL2 = "#222a3a"; FLOOR = "#141922"; FRIDGE = "#d9dee6"
WOOD = "#5a4130"; WOOD2 = "#6e5038"; PAPER = "#efe6d2"; TATAMI = "#8a8a52"; PLANT = "#3f8f5a"

t_kommst = ws("Du", 4.3); t_kuehl = ws("Kühlschrank"); t_joghurt = ws("Joghurt"); t_merk = ws("Merk", t_joghurt)
t_denkst = ws("denkst"); t_hab = ws("Hab"); t_naechsten = ws("Am", t_hab); t_saft = ws("Saftflasche"); t_halb = ws("halb")
t_nachts = ws("Nachts"); t_knarzen = ws("Knarzen"); t_oben = ws("oben", t_knarzen)
t_doch = ws("Doch"); t_genau = ws("Genau", t_doch); t_japan = ws("Japan"); t_mann = ws("Einem")
t_dabei = ws("Dabei", t_mann); t_ab = ws("ab", t_dabei + 0.5); t_schl = ws("Schlüssel")
t_glaubt = ws("glaubt"); t_verrueckt = ws("verrückt", t_glaubt); t_kamera = ws("Kamera", t_verrueckt); t_handy1 = ws("Handy", t_kamera)
t_paar = ws("Ein", t_handy1); t_vibr = ws("vibriert"); t_arbeit = ws("Arbeit")
t_auf = ws("Auf", t_arbeit); t_fremde = ws("fremde")
t_ruft = ws("ruft"); t_polizei1 = ws("Polizei", t_ruft)
t_beamten = ws("Beamten"); t_tueren = ws("Türen"); t_versch = ws("verschlossen"); t_niemand2 = ws("Niemand", t_versch)
t_bis = ws("Bis"); t_ganz = ws("Ganz", t_bis); t_fach = ws("Fach"); t_schiebt = ws("schiebt")
t_darin = ws("Darin"); t_matratze = ws("Matratze"); t_flaschen = ws("Plastikflaschen")
t_sie = ws("Sie", t_flaschen); t_jahr = ws("Jahr", t_sie); t_wenn = ws("Wenn", t_jahr); t_raus = ws("raus", t_wenn); t_dusch = ws("geduscht")
t_und_kn = ws("Und", t_dusch); t_jetzt = ws("Jetzt", t_und_kn); t_aufgef = ws("Aufgefallen"); t_fehlende = ws("fehlende")
t_also2 = ws("Also", t_fehlende); t_vermisst = ws("vermisst"); t_selbst = ws("selbst", t_vermisst)

SEPIA = set()


# ---------- Deko-Bausteine (Skill 6a: Wohnräume liebevoll eingerichtet) ----------
def frame_pic(x, y, w, h, kind=0):
    inner = {0: f'<polygon points="{x+10},{y+h-10} {x+w*0.4},{y+h*0.35} {x+w*0.62},{y+h*0.6} {x+w*0.78},{y+h*0.45} {x+w-10},{y+h-10}" fill="#4f7a6a"/><circle cx="{x+w*0.75}" cy="{y+h*0.3}" r="{h*0.12}" fill="#ffd98a"/>',
             1: f'<circle cx="{x+w/2}" cy="{y+h*0.42}" r="{h*0.18}" fill="#c98a6a"/><rect x="{x+w*0.3}" y="{y+h*0.6}" width="{w*0.4}" height="{h*0.3}" rx="10" fill="#4a6a9a"/>',
             2: "".join(f'<rect x="{x+12+i*(w-24)/4}" y="{y+h-14-(i%3+1)*h*0.18}" width="{(w-24)/4-6}" height="{(i%3+1)*h*0.18}" fill="{c}"/>' for i, c in enumerate(("#e07a5f", "#f2cc8f", "#81b29a", "#3d405b")))}[kind]
    return (f'<rect x="{x-8}" y="{y-8}" width="{w+16}" height="{h+16}" rx="4" fill="#b08a5a"/><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#e9e1cf"/>{inner}'
            f'<rect x="{x-8}" y="{y+h+8}" width="{w+16}" height="10" fill="#000" opacity=".25"/>')


def wall_clock(x, y, r=56, hid=None):
    hid_attr = f' id="{hid}"' if hid else ""
    return (f'<circle cx="{x}" cy="{y}" r="{r+8}" fill="#6e5038"/><circle cx="{x}" cy="{y}" r="{r}" fill="#f6f1e6"/>'
            + "".join(f'<rect x="{x-2}" y="{y-r+6}" width="4" height="10" fill="#333" transform="rotate({a} {x} {y})"/>' for a in range(0, 360, 30))
            + f'<rect x="{x-3}" y="{y-r*0.5}" width="6" height="{r*0.5}" fill="#222" transform="rotate(40 {x} {y})"/>'
            + f'<rect{hid_attr} x="{x-2}" y="{y-r*0.78}" width="4" height="{r*0.78}" fill="{RED}"/><circle cx="{x}" cy="{y}" r="6" fill="#222"/>')


def plant(x, y, s=1.0):
    leaves = "".join(f'<ellipse cx="{x + math.cos(a)*40*s:.0f}" cy="{y - 70*s + math.sin(a)*34*s:.0f}" rx="{36*s:.0f}" ry="{14*s:.0f}" fill="{PLANT if i%2 else "#4fa86a"}" transform="rotate({math.degrees(a):.0f} {x + math.cos(a)*40*s:.0f} {y - 70*s + math.sin(a)*34*s:.0f})"/>'
                     for i, a in enumerate([-2.8, -2.2, -1.6, -1.0, -0.4, -1.9, -1.3]))
    return (f'{leaves}<path d="M {x-34*s} {y-40*s} L {x+34*s} {y-40*s} L {x+26*s} {y} L {x-26*s} {y} Z" fill="#c26a3d"/>'
            f'<rect x="{x-38*s}" y="{y-48*s}" width="{76*s}" height="{12*s}" rx="4" fill="#a8562f"/>')


def bookshelf(x, y, w=260):
    books = ""
    bx = x + 10
    cols = ["#e07a5f", "#3d405b", "#81b29a", "#f2cc8f", "#6a4c93", "#c9ada7", "#2a9d8f"]
    i = 0
    while bx < x + w - 60:
        bw = 18 + (i * 7) % 14; bh = 70 + (i * 13) % 30
        books += f'<rect x="{bx}" y="{y-bh}" width="{bw}" height="{bh}" rx="2" fill="{cols[i % len(cols)]}"/>'
        bx += bw + 3; i += 1
    return (f'<rect x="{x}" y="{y}" width="{w}" height="14" fill="{WOOD2}"/>{books}'
            f'{plant(x + w - 30, y, 0.5)}<rect x="{x+6}" y="{y+14}" width="10" height="24" fill="{WOOD}"/><rect x="{x+w-16}" y="{y+14}" width="10" height="24" fill="{WOOD}"/>')


def window(x, y, w, h, night=True, curtains=True):
    sky = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#skyg)"/>'
           f'<circle cx="{x+w*0.7}" cy="{y+h*0.3}" r="{min(w,h)*0.12}" fill="{MOON}"/>'
           + "".join(f'<circle cx="{x+10+((i*73)%int(w-20))}" cy="{y+10+((i*41)%int(h*0.6))}" r="2" fill="#fff" opacity=".7"/>' for i in range(10))
           + "".join(f'<rect x="{x+bx}" y="{y+h-bh}" width="{bw}" height="{bh}" fill="#0f1226"/>' for bx, bw, bh in ((0, w*0.25, h*0.35), (w*0.27, w*0.2, h*0.5), (w*0.5, w*0.3, h*0.3), (w*0.82, w*0.18, h*0.45)))) if night else \
          f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#bcd7ef"/>' + "".join(f'<rect x="{x+bx}" y="{y+h-bh}" width="{bw}" height="{bh}" fill="#8aa6c2"/>' for bx, bw, bh in ((0, w*0.3, h*0.5), (w*0.33, w*0.22, h*0.7), (w*0.6, w*0.4, h*0.45)))
    cur = (f'<path d="M {x-40} {y-30} Q {x+30} {y+h/2} {x-10} {y+h+40} L {x-60} {y+h+40} L {x-60} {y-30} Z" fill="#8b3a3a"/>'
           f'<path d="M {x+w+40} {y-30} Q {x+w-30} {y+h/2} {x+w+10} {y+h+40} L {x+w+60} {y+h+40} L {x+w+60} {y-30} Z" fill="#8b3a3a"/>'
           f'<rect x="{x-70}" y="{y-44}" width="{w+140}" height="14" rx="7" fill="#3a2d1f"/>') if curtains else ""
    return (f'<rect x="{x-14}" y="{y-14}" width="{w+28}" height="{h+28}" fill="#e9e1cf"/>{sky}'
            f'<rect x="{x+w/2-5}" y="{y}" width="10" height="{h}" fill="#e9e1cf"/><rect x="{x}" y="{y+h/2-5}" width="{w}" height="10" fill="#e9e1cf"/>'
            f'<rect x="{x-24}" y="{y+h+10}" width="{w+48}" height="18" fill="#d6ccb6"/>{cur}')


def pendant(x, y_len=260, gid=None):
    g = f' id="{gid}"' if gid else ""
    return (f'<g{g}><rect x="{x-2}" y="0" width="4" height="{y_len}" fill="#222"/>'
            f'<path d="M {x-70} {y_len+60} Q {x} {y_len-20} {x+70} {y_len+60} Z" fill="#2a3a4a"/>'
            f'<ellipse cx="{x}" cy="{y_len+60}" rx="70" ry="12" fill="{LAMP}"/>'
            f'<polygon points="{x-60},{y_len+64} {x+60},{y_len+64} {x+260},1300 {x-260},1300" fill="url(#lampcone)" opacity=".55"/></g>')


def rug(cx, cy, w, h, col="#7a3b3b"):
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{w/2}" ry="{h/2}" fill="{col}"/><ellipse cx="{cx}" cy="{cy}" rx="{w/2-24}" ry="{h/2-12}" fill="none" stroke="#e9c46a" stroke-width="6" stroke-dasharray="20 12"/>')


def wallpaper(c1, c2):
    return (f'<rect width="1080" height="1300" fill="{c1}"/>'
            + "".join(f'<rect x="{x}" y="0" width="34" height="1300" fill="{c2}" opacity=".55"/>' for x in range(0, 1080, 90))
            + "".join(f'<circle cx="{x+62}" cy="{y}" r="5" fill="{c2}"/>' for x in range(0, 1080, 90) for y in range(60, 1300, 120)))


def floor(col1="#3a2c22", col2="#33271e"):
    return (f'<rect x="0" y="1300" width="1080" height="620" fill="{col1}"/>'
            + "".join(f'<rect x="{x}" y="{y}" width="236" height="56" fill="{col2 if ((x//240)+(y//60))%2 else col1}"/>' for y in range(1304, 1920, 60) for x in range(-120 * ((y // 60) % 2), 1080, 240))
            + f'<rect x="0" y="1290" width="1080" height="18" fill="#2a1f17"/>')


def kitchen(prefix, sep=False):
    tiles = "".join(f'<rect x="{x}" y="{y}" width="56" height="40" rx="3" fill="#dfe6ee"/>' for x in range(504, 1080, 60) for y in range(880, 1060, 44))
    return (wallpaper("#24324a", "#2b3b57") + floor()
            + f'<rect x="500" y="876" width="580" height="186" fill="#c7cfda"/>{tiles}'
            + window(640, 420, 300, 300)
            + wall_clock(560, 560, 46, f"{prefix}-clk")
            + frame_pic(36, 300, 120, 150, 0) + frame_pic(180, 340, 90, 110, 2)
            + f'<rect x="500" y="1060" width="580" height="240" fill="#6e5038"/><rect x="490" y="1046" width="600" height="20" rx="6" fill="#d9c7a8"/>'
            + "".join(f'<rect x="{x}" y="1080" width="130" height="200" rx="8" fill="#7a5a40"/><rect x="{x+56}" y="1150" width="18" height="6" rx="3" fill="#d9c7a8"/>' for x in (510, 650, 790, 930))
            + f'<rect x="820" y="1010" width="200" height="40" rx="8" fill="#222"/><circle cx="870" cy="1030" r="14" fill="#444"/><circle cx="960" cy="1030" r="14" fill="#444"/>'
            + f'<path d="M 590 1046 L 600 980 Q 640 960 680 980 L 690 1046 Z" fill="#c0392b"/><rect x="620" y="960" width="40" height="14" rx="6" fill="#222"/><path d="M 690 1000 q 20 0 22 20" stroke="#222" stroke-width="6" fill="none"/>'
            + plant(750, 1046, 0.7)
            + "".join(f'<rect x="{x}" y="800" width="8" height="60" fill="#888"/>' for x in (940, 975, 1010)) + '<rect x="920" y="796" width="120" height="8" fill="#555"/>'
            + rug(560, 1700, 700, 170))


def fridge(fid, x, y, items=True):
    shelf = ""
    if items:
        for sy in (y + 120, y + 280, y + 440):
            shelf += f'<rect x="{x+20}" y="{sy+110}" width="300" height="10" fill="#c9d2de"/>'
        shelf += (f'<g id="{fid}-milk"><rect x="{x+40}" y="{y+150}" width="60" height="80" rx="8" fill="#f4f6fa"/><rect x="{x+40}" y="{y+150}" width="60" height="20" fill="{BLUE}"/></g>'
                  f'<g id="{fid}-yog"><rect x="{x+130}" y="{y+180}" width="64" height="50" rx="10" fill="#ffe28a"/><rect x="{x+126}" y="{y+172}" width="72" height="12" rx="6" fill="#ff8fb1"/></g>'
                  f'<rect id="{fid}-gap" x="{x+124}" y="{y+166}" width="76" height="70" rx="12" fill="none" stroke="{RED}" stroke-width="6" stroke-dasharray="12 8" opacity="0"/>'
                  f'<g id="{fid}-cheese"><polygon points="{x+220},{y+230} {x+300},{y+230} {x+300},{y+180}" fill="#ffd34d"/></g>'
                  f'<g id="{fid}-egg">' + "".join(f'<ellipse cx="{x+50+i*36}" cy="{y+370}" rx="15" ry="20" fill="#f6efe2"/>' for i in range(4)) + '</g>'
                  f'<g id="{fid}-juice"><rect x="{x+220}" y="{y+300}" width="70" height="130" rx="10" fill="none" stroke="#e6e9ee" stroke-width="5"/>'
                  f'<rect id="{fid}-jlev" x="{x+224}" y="{y+310}" width="62" height="116" rx="6" fill="#ff9b2f"/></g>'
                  f'<g id="{fid}-veg"><circle cx="{x+80}" cy="{y+530}" r="30" fill="#e74c3c"/><circle cx="{x+150}" cy="{y+530}" r="30" fill="#7ac74f"/><ellipse cx="{x+240}" cy="{y+535}" rx="48" ry="22" fill="#ff9b2f"/></g>')
    magnets = (f'<rect x="{x+40}" y="{y+60}" width="70" height="44" rx="6" fill="#ffcc4d" transform="rotate(-6 {x+75} {y+80})"/>'
               f'<rect x="{x+150}" y="{y+90}" width="90" height="110" fill="#fff" transform="rotate(4 {x+195} {y+145})"/><circle cx="{x+195}" cy="{y+92}" r="8" fill="{RED}"/>'
               + "".join(f'<rect x="{x+160}" y="{y+120+k*20}" width="{60-k*8}" height="5" fill="#9aa" transform="rotate(4 {x+195} {y+145})"/>' for k in range(4))
               + f'<circle cx="{x+90}" cy="{y+260}" r="16" fill="#3b6cff"/><rect x="{x+60}" y="{y+400}" width="100" height="70" fill="#e07a5f" transform="rotate(-3 {x+110} {y+435})"/>')
    return (f'<g id="{fid}"><rect x="{x+12}" y="{y+16}" width="340" height="640" rx="26" fill="#000" opacity=".35"/>'
            f'<rect x="{x}" y="{y}" width="340" height="640" rx="26" fill="{FRIDGE}"/>'
            f'<rect x="{x+16}" y="{y+16}" width="308" height="608" rx="14" fill="#eaf4ff"/><rect x="{x+16}" y="{y+16}" width="308" height="608" rx="14" fill="url(#coldglow)"/>'
            f'{shelf}'
            f'<g id="{fid}-door"><rect x="{x}" y="{y}" width="340" height="640" rx="26" fill="{FRIDGE}" stroke="#aeb6c2" stroke-width="4"/>'
            f'<rect x="{x+290}" y="{y+180}" width="16" height="140" rx="8" fill="#aeb6c2"/>{magnets}</g></g>')


def open_door(fid, x, t, dur=0.45):
    tw(f'tl.to("#{fid}-door",{{scaleX:-0.25,svgOrigin:"{x} 0",duration:{dur},ease:"power2.out"}},{t:.3f});')


def hud_day(hid, day, item, op=1):
    return (f'<g id="{hid}" opacity="{op}"><rect x="200" y="200" width="680" height="170" rx="30" fill="#0b0e12" fill-opacity=".9" stroke="#3a4452" stroke-width="5"/>'
            f'<text x="330" y="255" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="26" fill="#7d8896" letter-spacing="4">TAG</text>'
            f'<text x="330" y="335" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="80" fill="#fff">{day}</text>'
            f'<line x1="430" y1="225" x2="430" y2="345" stroke="#3a4452" stroke-width="4"/>'
            f'<text x="655" y="255" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="26" fill="#7d8896" letter-spacing="4">FEHLT</text>'
            f'<text id="{hid}-it" x="655" y="325" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="52" fill="{RED}" opacity="0">{item}</text></g>')


def phone_frame(inner, x=540, y=960, s=1.0, pid="ph"):
    return (f'<g id="{pid}"><g transform="translate({x},{y}) scale({s}) translate(-540,-960)">'
            f'<rect x="200" y="200" width="680" height="1440" rx="100" fill="#0e0f22"/><rect x="220" y="220" width="640" height="1400" rx="84" fill="#1b2240"/>'
            f'<rect x="440" y="250" width="200" height="46" rx="23" fill="#0e0f22"/>{inner}</g></g>')


def cam_icon(cid, x, y, s=1.0):
    return (f'<g id="{cid}"><g transform="translate({x},{y}) scale({s})">'
            f'<rect x="-30" y="-150" width="60" height="110" rx="12" fill="#c9ccd8"/>'
            f'<rect x="-130" y="-60" width="260" height="150" rx="40" fill="#e6e9ee"/><circle cx="-20" cy="15" r="52" fill="#151a21"/><circle cx="-20" cy="15" r="30" fill="#2b3a6b"/><circle cx="-30" cy="5" r="9" fill="#fff" opacity=".7"/>'
            f'<circle id="{cid}-led" cx="90" cy="50" r="10" fill="{RED}"/></g></g>')


def bedroom(prefix):
    beams = "".join(f'<rect x="0" y="{y}" width="1080" height="34" fill="#3a2d22"/><rect x="0" y="{y+34}" width="1080" height="6" fill="#000" opacity=".3"/>' for y in (40, 210))
    return (wallpaper("#232a45", "#2a3254") + f'<rect width="1080" height="260" fill="#2c2238"/>{beams}'
            + floor("#2e2433", "#28202d")
            + window(660, 460, 280, 300)
            + frame_pic(90, 420, 160, 120, 1) + frame_pic(290, 470, 90, 90, 0)
            + bookshelf(80, 720, 300)
            + f'<rect x="880" y="1180" width="160" height="150" rx="10" fill="{WOOD2}"/><rect x="900" y="1205" width="120" height="10" fill="{WOOD}"/>'
            + f'<rect x="900" y="1130" width="90" height="46" rx="8" fill="#0b0e12"/><text id="{prefix}-clock" x="945" y="1166" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="30" fill="{RED}">03:12</text>'
            + f'<path d="M 940 1060 L 990 1060 L 1000 1110 L 930 1110 Z" fill="#e9c46a"/><rect x="960" y="1110" width="10" height="20" fill="#555"/><circle cx="965" cy="1085" r="80" fill="{LAMP}" opacity=".12"/>'
            + rug(540, 1760, 760, 180, "#4a3b6a"))


def bed_front():
    return (f'<rect x="120" y="1240" width="720" height="70" rx="20" fill="{WOOD}"/>'
            f'<path d="M 140 1330 Q 160 1290 260 1290 L 820 1290 L 840 1600 L 140 1600 Z" fill="#3d5a80"/>'
            + "".join(f'<path d="M {180+i*120} 1300 q 30 140 0 290" stroke="#2f4a6a" stroke-width="6" fill="none"/>' for i in range(6))
            + f'<rect x="120" y="1590" width="740" height="40" rx="10" fill="{WOOD}"/><rect x="130" y="1620" width="30" height="80" fill="{WOOD}"/><rect x="820" y="1620" width="30" height="80" fill="{WOOD}"/>')


def jp_room(prefix, closet=False):
    """Japanisches Zimmer: Shoji-Schiebetüren, Tatami, Rollbild, Bonsai, Laterne."""
    shoji = "".join(f'<rect x="{x}" y="380" width="200" height="900" fill="{PAPER}" stroke="{WOOD}" stroke-width="12"/>'
                    + "".join(f'<rect x="{x}" y="{y}" width="200" height="6" fill="{WOOD}"/>' for y in range(480, 1280, 110))
                    + f'<rect x="{x+97}" y="380" width="6" height="900" fill="{WOOD}"/>' for x in (0,) )
    tat = "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{TATAMI}" stroke="#4a3a22" stroke-width="10"/>' for x, y, w, h in ((0, 1300, 540, 300), (540, 1300, 540, 300), (0, 1600, 360, 320), (360, 1600, 720, 320)))
    scroll = (f'<rect x="300" y="420" width="140" height="440" fill="#efe6d2"/><rect x="290" y="410" width="160" height="16" rx="6" fill="{WOOD}"/><rect x="290" y="860" width="160" height="16" rx="6" fill="{WOOD}"/>'
              f'<path d="M 320 760 L 360 640 L 390 700 L 410 660 L 430 760 Z" fill="#444"/><circle cx="400" cy="520" r="24" fill="{RED}"/>')
    bonsai = (f'<rect x="250" y="1250" width="140" height="40" rx="8" fill="#5a4630"/><path d="M 320 1250 Q 300 1190 330 1150" stroke="#4a3426" stroke-width="12" fill="none"/>'
              f'<ellipse cx="300" cy="1150" rx="60" ry="30" fill="{PLANT}"/><ellipse cx="350" cy="1120" rx="50" ry="26" fill="#4fa86a"/>')
    lantern = (f'<rect x="538" y="0" width="4" height="180" fill="#222"/><rect x="480" y="180" width="120" height="160" rx="50" fill="#f7e3b0"/>'
               + "".join(f'<rect x="480" y="{y}" width="120" height="4" fill="#c9a24b"/>' for y in (210, 250, 290)) + f'<circle cx="540" cy="260" r="160" fill="{LAMP}" opacity=".12"/>')
    clo = ""
    if closet:
        clo = (f'<rect x="560" y="380" width="520" height="900" fill="{WOOD}"/>'
               f'<rect x="580" y="400" width="480" height="160" fill="#1a120a"/>'
               f'<g id="{prefix}-tdoor">' + "".join(f'<rect x="{x}" y="400" width="240" height="160" fill="{PAPER}" stroke="{WOOD2}" stroke-width="8"/>' for x in (580, 820)) + '</g>'
               f'<rect x="560" y="560" width="520" height="20" fill="{WOOD2}"/>'
               + "".join(f'<rect x="{x}" y="590" width="240" height="680" fill="#e9dcc0" stroke="{WOOD2}" stroke-width="8"/><circle cx="{x+30 if x>700 else x+210}" cy="930" r="12" fill="{WOOD}"/>' for x in (580, 820)))
    else:
        clo = window(640, 460, 340, 320, night=True, curtains=False)
    return (f'<rect width="1080" height="1300" fill="#d8c9a8"/><rect width="1080" height="380" fill="#c9b892"/><rect x="0" y="370" width="1080" height="14" fill="{WOOD}"/>'
            + shoji + scroll + bonsai + clo + tat + lantern)


# ================= SZENEN =================
# A Hook: Haus im Querschnitt, liebevoll eingerichtet
S0, S1 = 0.0, t_kommst
roof_tiles = "".join(f'<path d="M {x} {y} q 20 18 40 0" stroke="#3a2a2a" stroke-width="5" fill="none"/>' for y in range(520, 770, 34) for x in range(int(540 - (y - 430) * 1.25) + 20, int(540 + (y - 430) * 1.25) - 40, 40))
house = (f'<polygon points="80,775 540,420 1000,775" fill="#6b3d3d"/>{roof_tiles}'
         f'<rect x="760" y="430" width="70" height="170" fill="#7a5a4a"/><rect x="750" y="420" width="90" height="20" fill="#5a3a2a"/>'
         + "".join(f'<circle id="a-smoke{i}" cx="795" cy="{390-i*40}" r="{20+i*8}" fill="#9aa0b8" opacity="{.35-i*.07:.2f}"/>' for i in range(4))
         + f'<circle cx="540" cy="640" r="56" fill="#e9e1cf"/><circle cx="540" cy="640" r="44" fill="#0a0d14"/>'
         + f'<rect id="a-gap" x="496" y="596" width="88" height="88" rx="44" fill="none" stroke="{RED}" stroke-width="6" stroke-dasharray="12 8" opacity="0"/>'
         f'<rect x="140" y="770" width="800" height="900" fill="#e9dcc4"/>'
         f'<rect x="150" y="780" width="380" height="410" fill="#3a4a6a"/><rect x="550" y="780" width="380" height="410" fill="#4a3a5a"/>'
         f'<rect x="150" y="1210" width="380" height="440" fill="#44536f"/><rect x="550" y="1210" width="380" height="440" fill="#3d4a66"/>'
         # Schlafzimmer oben links
         f'<rect x="180" y="1050" width="240" height="70" rx="16" fill="#3d5a80"/><rect x="180" y="1030" width="70" height="40" rx="12" fill="#e6e9ee"/><rect x="170" y="1120" width="260" height="20" fill="{WOOD}"/>'
         + frame_pic(300, 850, 80, 60, 0) + f'<rect x="440" y="1080" width="60" height="60" fill="{WOOD2}"/><path d="M 450 1040 L 490 1040 L 495 1075 L 445 1075 Z" fill="#e9c46a"/>'
         # Wohnzimmer oben rechts: Sofa, TV-Licht, Regal
         + f'<rect x="580" y="1080" width="220" height="80" rx="20" fill="#8b3a3a"/><rect x="580" y="1050" width="220" height="50" rx="18" fill="#a04848"/>'
         + f'<rect x="830" y="1010" width="80" height="60" rx="6" fill="#111"/><rect x="836" y="1016" width="68" height="48" fill="#5aa0ff" opacity=".7"/><polygon points="836,1064 904,1064 980,1190 760,1190" fill="#5aa0ff" opacity=".1"/>'
         + bookshelf(600, 900, 200) + plant(900, 1190, .6)
         # Küche unten links
         + f'<rect x="170" y="1450" width="110" height="200" rx="10" fill="{FRIDGE}"/><rect x="300" y="1520" width="210" height="130" fill="#7a5a40"/><rect x="292" y="1510" width="226" height="14" fill="#d9c7a8"/>'
         + f'<polygon points="300,1210 380,1210 470,1650 210,1650" fill="url(#lampcone)"/><rect x="320" y="1210" width="40" height="16" fill="{LAMP}"/>' + wall_clock(420, 1300, 30)
         # Flur unten rechts: Tür, Garderobe
         + f'<rect x="760" y="1360" width="140" height="290" rx="6" fill="{WOOD2}"/><circle cx="880" cy="1510" r="9" fill="#c9a24b"/>'
         + f'<rect x="590" y="1300" width="120" height="10" fill="{WOOD}"/>' + "".join(f'<path d="M {610+i*40} 1310 q -10 60 10 120 l 20 0 q 10 -60 -10 -120 z" fill="{c}"/>' for i, c in enumerate(("#2f6f73", "#c0392b", "#e9c46a")))
         + rug(650, 1640, 200, 30, "#6a4c93")
         # Außen: Wände, Fensterläden, Tür, Zaun, Baum, Briefkasten
         + f'<rect x="140" y="1200" width="800" height="14" fill="#c9b892"/><rect x="530" y="770" width="20" height="900" fill="#c9b892"/>'
         + f'<rect x="0" y="1660" width="1080" height="260" fill="#1e3a2a"/><rect x="0" y="1660" width="1080" height="14" fill="#2b4d38"/>'
         + "".join(f'<rect x="{x}" y="1690" width="16" height="120" fill="#e9e1cf"/>' for x in range(20, 1080, 60)) + '<rect x="0" y="1720" width="1080" height="12" fill="#e9e1cf"/><rect x="0" y="1780" width="1080" height="12" fill="#e9e1cf"/>'
         + f'<rect x="990" y="1500" width="16" height="200" fill="#4a3426"/><rect x="960" y="1460" width="76" height="56" rx="10" fill="{RED}"/>'
         + f'<rect x="40" y="1220" width="40" height="460" fill="#3a2a20"/><circle cx="60" cy="1160" r="120" fill="#24563a"/><circle cx="120" cy="1240" r="90" fill="#2d6a46"/>')
scene("sa", S0, S1, f'<rect width="1080" height="1920" fill="url(#skyg)"/>'
      + "".join(f'<circle cx="{RNG.randint(0,1080)}" cy="{RNG.randint(0,500)}" r="2" fill="#fff" opacity="{RNG.uniform(.3,.8):.2f}"/>' for _ in range(50))
      + f'<circle cx="180" cy="230" r="64" fill="{MOON}"/><circle cx="180" cy="230" r="140" fill="url(#moonglow)"/>' + house
      + f'<g id="a-q" opacity="0"><circle cx="150" cy="560" r="70" fill="{RED}"/><text x="150" y="592" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="92" fill="#fff">?</text></g>')
pop("#a-q", 1.0)
tw(f'tl.fromTo("#a-gap",{{opacity:0}},{{opacity:1,duration:.4,yoyo:true,repeat:5,ease:"sine.inOut"}},{1.6:.3f});')
for i in range(4):
    tw(f'tl.fromTo("#a-smoke{i}",{{y:0,x:0}},{{y:-60,x:30,duration:3,ease:"sine.inOut",yoyo:true,repeat:1}},{i*0.3:.3f});')

# B Küche Tag 1: Joghurt fehlt
S0, S1 = t_kommst, t_denkst
scene("sb", S0, S1, kitchen("b") + fridge("b-fr", 120, 640) + figure("b-fig", 740, 1640, 1.25, eyes="n")
      + hud_day("b-hud", "1", "JOGHURT", 0)
      + f'<g id="b-merk" opacity="0"><rect x="560" y="420" width="420" height="96" rx="48" fill="{RED}"/><text x="770" y="484" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="46" fill="#fff">MERK DIR DAS</text></g>')
pop("#b-hud", S0 + 0.2)
open_door("b-fr", 120, t_kuehl)
tw(f'tl.set("#b-fr-yog",{{opacity:0}},{S0:.3f});')
tw(f'tl.fromTo("#b-fr-gap",{{opacity:0}},{{opacity:1,duration:.35,yoyo:true,repeat:{int((S1-t_joghurt)/0.35)},ease:"sine.inOut"}},{t_joghurt:.3f});')
toggle("#b-hud-it", t_joghurt); pop("#b-merk", t_merk)
tw(f'tl.to("#b-fig-eyes-n",{{opacity:0,duration:.15}},{t_joghurt:.3f});'); tw(f'tl.to("#b-fig-eyes-w",{{opacity:1,duration:.15}},{t_joghurt:.3f});')

# C „Hab ich wohl selbst gegessen“
S0, S1 = t_denkst, t_naechsten
scene("sc", S0, S1, kitchen("c") + fridge("c-fr", 120, 640) + figure("c-fig", 760, 1650, 1.3, eyes="n")
      + f'<g id="c-th" opacity="0"><circle cx="680" cy="1180" r="18" fill="#e6e9ee"/><circle cx="640" cy="1090" r="28" fill="#e6e9ee"/>'
        f'<ellipse cx="760" cy="700" rx="240" ry="170" fill="#e6e9ee"/>'
        f'<rect x="700" y="650" width="110" height="90" rx="16" fill="#ffe28a"/><rect x="692" y="636" width="126" height="20" rx="10" fill="#ff8fb1"/>'
        f'<text x="870" y="650" font-family="Poppins" font-weight="800" font-size="90" fill="#2c3a52">?</text></g>')
pop("#c-th", S0 + 0.1, 0.35, 0.6)
tw(f'tl.fromTo("#c-fig",{{rotation:0}},{{rotation:3,svgOrigin:"760 1650",duration:.5,yoyo:true,repeat:3,ease:"sine.inOut"}},{t_hab:.3f});')

# D Tag 2: Saft halb leer
S0, S1 = t_naechsten, t_nachts
scene("sd", S0, S1, kitchen("d") + fridge("d-fr", 370, 640) + hud_day("d-hud", "2", "SAFT", 1)
      + f'<g id="d-half" opacity="0"><circle cx="830" cy="1000" r="74" fill="{RED}"/><text x="830" y="1028" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="76" fill="#fff">½</text></g>')
tw(f'tl.set("#d-fr-yog",{{opacity:0}},{S0:.3f});')
open_door("d-fr", 370, S0 + 0.3)
tw(f'tl.to("#d-fr-cheese",{{opacity:0,duration:.4}},{S0 + 1.0:.3f});')
tw(f'tl.to("#d-fr-jlev",{{scaleY:.5,svgOrigin:"0 1066",duration:.9,ease:"power2.inOut"}},{t_saft:.3f});')
toggle("#d-hud-it", t_saft); pop("#d-half", t_halb)

# D2 Nachts: Knarzen über dir – du wohnst ganz oben
S0, S1 = t_nachts, t_doch
dust = "".join(f'<circle id="d2-p{i}" cx="{420+i*22}" cy="260" r="{3+i%3}" fill="#cfc6b0" opacity="0"/>' for i in range(10))
scene("sd2", S0, S1, bedroom("d2") + figure("d2-fig", 470, 1520, 1.2, eyes="w") + bed_front()
      + f'<rect x="400" y="236" width="300" height="10" fill="#000" opacity=".5"/>' + dust
      + f'<g id="d2-k1" opacity="0"><text x="300" y="380" font-family="Poppins" font-weight="800" font-size="76" fill="{RED}" transform="rotate(-6 300 380)">KNARZ</text></g>'
      + f'<g id="d2-k2" opacity="0"><text x="600" y="330" font-family="Poppins" font-weight="800" font-size="60" fill="{RED}" transform="rotate(5 600 330)">KNARZ…</text></g>'
      + label("d2-l", 540, 640, "ÜBER DIR: NUR DAS DACH", "#e6e9ee", 38), drift=True)
tw(f'tl.set("#d2-fig-eyes-w",{{opacity:0}},{S0:.3f});'); tw(f'tl.set("#d2-fig-eyes-n",{{opacity:1}},{S0:.3f});')
tw(f'tl.to("#d2-fig-eyes-n",{{opacity:0,duration:.1}},{t_knarzen:.3f});'); tw(f'tl.to("#d2-fig-eyes-w",{{opacity:1,duration:.1}},{t_knarzen:.3f});')
pop("#d2-k1", t_knarzen); pop("#d2-k2", t_knarzen + 0.6)
for i in range(10):
    tw(f'tl.fromTo("#d2-p{i}",{{opacity:0,y:0}},{{opacity:.8,y:{300+i*40},duration:1.4,ease:"power1.in",immediateRender:false}},{t_knarzen + 0.1 + i*0.08:.3f});')
shake("#sd2-cam", t_knarzen, 4, 4)
pop("#d2-l", t_oben)

# E „Doch jetzt wird's unheimlich“ – Kalender springt zurück
S0, S1 = t_doch, t_genau
YEARS = ["2026", "2021", "2016", "2012", "2009", "2008"]
scene("se", S0, S1, f'<rect width="1080" height="1920" fill="#000"/>'
      + "".join(f'<rect x="537" y="300" width="6" height="200" fill="{RED}" opacity=".18" transform="rotate({a} 540 960)"/>' for a in range(0, 360, 15))
      + f'<rect id="e-flash" width="1080" height="1920" fill="{RED}" opacity="0"/>'
      + f'<g><rect x="290" y="560" width="500" height="520" rx="30" fill="#f2efe8"/><rect x="290" y="560" width="500" height="130" rx="30" fill="{RED}"/>'
        f'<circle cx="400" cy="560" r="20" fill="#333"/><circle cx="680" cy="560" r="20" fill="#333"/>'
      + "".join(f'<text id="e-y{i}" x="540" y="900" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="150" fill="#151a21" opacity="0">{y}</text>' for i, y in enumerate(YEARS))
      + '</g>')
tw(f'tl.fromTo("#e-flash",{{opacity:0}},{{opacity:.8,duration:.001,immediateRender:false}},{S0:.3f});')
tw(f'tl.fromTo("#e-flash",{{immediateRender:false}},{{opacity:0,duration:.35}},{S0+0.001:.3f});')
for i in range(len(YEARS)):
    a = S0 + (S1 - S0) * i / len(YEARS)
    toggle(f"#e-y{i}", a, S0 + (S1 - S0) * (i + 1) / len(YEARS) if i < len(YEARS) - 1 else None)


# F Japan 2008: japanische Küche, Essen verschwindet
def jp_kitchen():
    noren = "".join(f'<rect x="{620+i*70}" y="380" width="62" height="200" fill="#2a3d6a"/><circle cx="{651+i*70}" cy="470" r="14" fill="{PAPER}"/>' for i in range(5))
    return (f'<rect width="1080" height="1300" fill="#cdbb95"/>' + "".join(f'<rect x="{x}" y="0" width="8" height="1300" fill="{WOOD}" opacity=".4"/>' for x in range(0, 1080, 120))
            + f'<rect x="600" y="360" width="400" height="20" fill="{WOOD}"/>{noren}'
            + f'<rect x="500" y="1060" width="580" height="240" fill="{WOOD}"/><rect x="490" y="1046" width="600" height="20" rx="6" fill="#d9c7a8"/>'
            + f'<rect x="560" y="960" width="110" height="86" rx="30" fill="#f2f2f2"/><rect x="590" y="950" width="50" height="14" rx="6" fill="#bbb"/><circle cx="615" cy="1010" r="8" fill="#2ecc71"/>'
            + f'<path d="M 720 1046 L 730 990 Q 770 970 810 990 L 820 1046 Z" fill="#555"/><rect x="750" y="975" width="40" height="12" rx="5" fill="#222"/>'
            + f'<rect x="870" y="900" width="160" height="140" rx="12" fill="#3a2d1f"/>' + "".join(f'<rect x="{885+i*36}" y="920" width="26" height="100" rx="4" fill="{c}"/>' for i, c in enumerate(("#c0392b", "#e9c46a", "#2a9d8f", "#f4f1de")))
            + f'<rect x="40" y="380" width="150" height="220" fill="{PAPER}" stroke="{WOOD}" stroke-width="10"/><circle cx="115" cy="470" r="40" fill="{RED}"/>'
            + floor("#8a7a52", "#7d6e48") + plant(540, 1300, 0.8))


S0, S1 = t_genau, t_dabei
SEPIA.add("sf")
scene("sf", S0, S1, jp_kitchen() + fridge("f-fr", 120, 640) + figure("f-man", 760, 1640, 1.25, eyes="w", outfit="shirt")
      + f'<g id="f-stamp" opacity="0"><rect x="420" y="160" width="580" height="200" rx="18" fill="#120d08" fill-opacity=".85" stroke="{RED}" stroke-width="10" transform="rotate(-5 710 260)"/>'
        f'<text x="710" y="240" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="42" fill="#e6d2ad" transform="rotate(-5 710 260)" letter-spacing="8">JAPAN</text>'
        f'<text x="710" y="330" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="96" fill="{RED}" transform="rotate(-5 710 260)">2008</text></g>')
open_door("f-fr", 120, S0 + 0.2)
tw(f'tl.fromTo("#f-stamp",{{opacity:0,scale:2.2,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:.22,ease:"power4.in"}},{t_japan:.3f});')
shake("#sf-cam", t_japan + 0.22, 5, 8)
for i, it in enumerate(("milk", "yog", "cheese", "egg", "veg")):
    tw(f'tl.to("#f-fr-{it}",{{opacity:0,y:-20,duration:.35,ease:"sine.in"}},{t_mann + 0.35 + i*0.42:.3f});')

# G Abschließen – nur ein Schlüssel (Eingang „Genkan“)
S0, S1 = t_dabei, t_glaubt
SEPIA.add("sg")
scene("sg", S0, S1, f'<rect width="1080" height="1920" fill="#cdbb95"/>' + "".join(f'<rect x="{x}" y="0" width="8" height="1300" fill="{WOOD}" opacity=".4"/>' for x in range(0, 1080, 120))
      + f'<rect x="300" y="420" width="480" height="880" rx="12" fill="#5a4630" stroke="#3a2d1f" stroke-width="16"/>'
      + "".join(f'<rect x="{x}" y="{y}" width="180" height="340" rx="10" fill="none" stroke="#4a3826" stroke-width="8"/>' for x in (340, 560) for y in (470, 860))
      + f'<circle cx="720" cy="860" r="22" fill="#c9a24b"/><rect x="700" y="900" width="40" height="80" rx="10" fill="#c9a24b"/><circle cx="720" cy="930" r="9" fill="#1a120a"/>'
      + f'<rect x="0" y="1300" width="1080" height="620" fill="#6e6250"/><rect x="0" y="1300" width="1080" height="30" fill="{WOOD}"/>'
      + f'<rect x="830" y="1050" width="200" height="250" fill="{WOOD2}"/>' + "".join(f'<rect x="840" y="{y}" width="180" height="8" fill="{WOOD}"/>' for y in (1110, 1180, 1250))
      + "".join(f'<ellipse cx="{x}" cy="{y}" rx="34" ry="14" fill="{c}"/>' for x, y, c in ((880, 1100, "#2a3d6a"), (960, 1100, "#8b3a3a"), (900, 1170, "#444"), (970, 1240, "#c9a24b")))
      + f'<path d="M 120 1300 L 130 1050 Q 140 1020 150 1050 L 160 1300" fill="#2a3d6a"/><path d="M 140 1050 q -6 -40 10 -50" stroke="#222" stroke-width="6" fill="none"/>'
      + f'<rect x="150" y="1500" width="160" height="60" rx="20" fill="#3a2d1f"/><rect x="340" y="1520" width="160" height="60" rx="20" fill="#5a4630"/>'
      + f'<g id="g-key"><circle cx="880" cy="930" r="40" fill="none" stroke="#e6d2ad" stroke-width="16"/><rect x="740" y="922" width="100" height="16" fill="#e6d2ad"/><rect x="760" y="938" width="14" height="26" fill="#e6d2ad"/></g>'
      + f'<g id="g-lock" opacity="0"><rect x="430" y="1380" width="220" height="170" rx="26" fill="{RED}"/><path d="M 470 1380 L 470 1330 A 70 70 0 0 1 610 1330 L 610 1380" stroke="{RED}" stroke-width="26" fill="none"/>'
        f'<circle cx="540" cy="1455" r="20" fill="#fff"/></g>'
      + label("g-one", 540, 300, "NUR 1 SCHLÜSSEL", "#e6d2ad", 48))
tw(f'tl.fromTo("#g-key",{{x:120,opacity:0}},{{x:0,opacity:1,duration:.4,ease:"power2.out"}},{S0 + 0.1:.3f});')
tw(f'tl.to("#g-key",{{rotation:-90,svgOrigin:"720 930",duration:.35,ease:"power2.inOut"}},{t_ab - 0.2:.3f});')
pop("#g-lock", t_ab); pop("#g-one", t_schl)

# H „Er glaubt, er wird verrückt“ → Kamera, die Bilder aufs Handy schickt
S0, S1 = t_glaubt, t_paar
SEPIA.add("sh")
swirl = "".join(f'<path d="M {760+i*30} 980 q 20 -30 40 0 q 20 30 40 0" stroke="#e6d2ad" stroke-width="6" fill="none" transform="rotate({i*40} 800 960)"/>' for i in range(4))
scene("sh", S0, S1, jp_kitchen() + fridge("h-fr", 120, 640, items=False) + figure("h-man", 760, 1640, 1.25, eyes="w", outfit="shirt")
      + f'<g id="h-sw" opacity="0">{swirl}<text x="900" y="900" font-family="Poppins" font-weight="800" font-size="70" fill="#e6d2ad">?!</text></g>'
      + cam_icon("h-cam", 900, 520, 0.9)
      + "".join(f'<path id="h-w{i}" d="M {760-i*40} {700+i*40} A {80+i*50} {80+i*50} 0 0 1 {900+i*50} {640+i*50}" stroke="{RED}" stroke-width="10" fill="none" opacity="0"/>' for i in range(3))
      + phone_frame('<rect x="260" y="700" width="560" height="420" fill="#4c6a4c"/><circle cx="540" cy="910" r="80" fill="#2b3a2b"/>', 640, 1350, 0.28, "h-ph"))
tw(f'tl.set("#h-cam",{{opacity:0}},{S0:.3f});')
pop("#h-sw", t_verrueckt, 0.3, 0.5)
tw(f'tl.to("#h-sw",{{rotation:360,svgOrigin:"800 960",duration:{t_kamera-t_verrueckt:.3f},ease:"none"}},{t_verrueckt:.3f});')
tw(f'tl.to("#h-sw",{{opacity:0,duration:.2}},{t_kamera:.3f});')
pop("#h-cam", t_kamera, 0.35, 0.6)
for i in range(3):
    tw(f'tl.fromTo("#h-w{i}",{{opacity:0}},{{opacity:.9,duration:.25,yoyo:true,repeat:{max(1,int((S1-t_handy1)/0.5))},ease:"sine.inOut"}},{t_handy1 - 0.4 + i*0.15:.3f});')
pop("#h-ph", t_handy1 - 0.3, 0.35, 0.7)

# M Bei der Arbeit: Handy vibriert → Foto mit fremder Person
S0, S1 = t_paar, t_ruft
SEPIA.add("sm")
notif = (f'<g id="m-n" opacity="0"><rect x="250" y="560" width="580" height="150" rx="30" fill="#2b2f45" fill-opacity=".95"/>'
         f'<text x="290" y="620" font-family="Poppins" font-weight="700" font-size="30" fill="{RED}">● KAMERA · jetzt</text>'
         f'<text x="290" y="675" font-family="Poppins" font-weight="600" font-size="34" fill="#fff">Bewegung erkannt: Küche</text></g>')
camimg = (f'<g id="m-img" opacity="0"><rect x="240" y="760" width="600" height="760" rx="20" fill="#1c2a1c"/>'
          f'<rect x="260" y="780" width="560" height="720" fill="#2f4630"/><rect x="280" y="980" width="180" height="420" rx="10" fill="#4c6a4c"/>'
          f'<rect x="520" y="1200" width="300" height="200" fill="#3a5a3a"/><rect x="560" y="1150" width="90" height="60" rx="20" fill="#4c6a4c"/>'
          f'<rect x="260" y="1380" width="560" height="120" fill="#253a26"/>'
          f'<g id="m-st" opacity="0" transform="translate(680,1420) scale(.6)"><ellipse cx="0" cy="-320" rx="60" ry="72" fill="#0b120b"/><path d="M -60 -330 Q -80 -200 -70 -150 L 70 -150 Q 80 -200 60 -330 Z" fill="#0b120b"/>'
          f'<rect x="-62" y="-262" width="124" height="160" rx="36" fill="#0b120b"/><rect x="-34" y="-110" width="27" height="110" rx="12" fill="#0b120b"/><rect x="7" y="-110" width="27" height="110" rx="12" fill="#0b120b"/></g>'
          f'<text x="280" y="820" font-family="JetBrains Mono" font-weight="700" font-size="28" fill="#cfe8c8">CAM 1 · KÜCHE</text>'
          f'<text x="800" y="820" text-anchor="end" font-family="JetBrains Mono" font-weight="700" font-size="28" fill="#cfe8c8">14:07:33</text><circle cx="790" cy="1470" r="10" fill="{RED}"/></g>')
office = (f'<rect width="1080" height="1920" fill="#3a3f4a"/>' + window(120, 160, 840, 520, night=False, curtains=False)
          + f'<rect x="0" y="1420" width="1080" height="500" fill="{WOOD2}"/><rect x="0" y="1400" width="1080" height="30" fill="{WOOD}"/>'
          + f'<rect x="80" y="1180" width="300" height="200" rx="12" fill="#1a1d22"/><rect x="96" y="1196" width="268" height="168" fill="#4a6a9a"/><rect x="210" y="1380" width="40" height="30" fill="#1a1d22"/>'
          + f'<rect x="780" y="1300" width="80" height="100" rx="10" fill="#e9e1cf"/><path d="M 860 1320 q 40 10 0 50" stroke="#e9e1cf" stroke-width="10" fill="none"/>'
          + plant(960, 1400, 0.9) + "".join(f'<rect x="{420+i*14}" y="{1380-i*6}" width="240" height="14" fill="{c}"/>' for i, c in enumerate(("#f4f1de", "#e9e1cf", "#f4f1de"))))
scene("sm", S0, S1, office + phone_frame(notif + camimg + '<text x="540" y="470" text-anchor="middle" font-family="Poppins" font-weight="300" font-size="120" fill="#fff">14:07</text>', 540, 980, 0.82, "m-ph"))
pop("#m-n", t_vibr)
tw(f'tl.fromTo("#m-ph",{{rotation:-2,svgOrigin:"540 980"}},{{rotation:2,svgOrigin:"540 980",duration:.07,yoyo:true,repeat:9,ease:"none"}},{t_vibr:.3f});')
tw(f'tl.to("#m-ph",{{rotation:0,svgOrigin:"540 980",duration:.1}},{t_vibr + 0.75:.3f});')
pop("#m-img", t_auf); pop("#m-st", t_fremde, 0.5, 1.0)
tw(f'tl.to("#m-img",{{scale:1.08,svgOrigin:"540 1140",duration:{max(.3,S1-t_fremde):.3f},ease:"sine.inOut"}},{t_fremde:.3f});')

# M2 Er ruft sofort die Polizei (110 – auch in Japan)
S0, S1 = t_ruft, t_beamten
SEPIA.add("sm2")
scene("sm2", S0, S1, office + phone_frame('<text x="540" y="480" text-anchor="middle" font-family="Poppins" font-weight="400" font-size="40" fill="#cfd3ff">Polizei</text>'
      '<text x="540" y="640" text-anchor="middle" font-family="Poppins" font-weight="600" font-size="150" fill="#fff">110</text>'
      '<text id="m2-r" x="540" y="760" text-anchor="middle" font-family="Poppins" font-weight="500" font-size="44" fill="#e6d2ad">Verbinden …</text>'
      '<circle cx="540" cy="1400" r="80" fill="#e74c3c"/><rect x="490" y="1390" width="100" height="22" rx="11" fill="#fff"/>', 540, 980, 0.82, "m2-ph"))
tw(f'tl.fromTo("#m2-r",{{opacity:1}},{{opacity:.3,duration:.4,yoyo:true,repeat:{max(1,int((S1-S0)/0.4))},ease:"sine.inOut"}},{S0:.3f});')

# N Beamte durchsuchen das Haus – verschlossen, niemand da
S0, S1 = t_beamten, t_bis
SEPIA.add("sn")
lock = lambda lid, x, y: (f'<g id="{lid}" opacity="0"><rect x="{x-40}" y="{y}" width="80" height="64" rx="12" fill="{RED}"/><path d="M {x-24} {y} L {x-24} {y-24} A 24 24 0 0 1 {x+24} {y-24} L {x+24} {y}" stroke="{RED}" stroke-width="12" fill="none"/></g>')
scene("sn", S0, S1, jp_room("n") + f'<rect width="1080" height="1920" fill="#000" opacity=".45"/>'
      + f'<polygon id="n-beam" points="540,1900 300,500 780,500" fill="#fff4c9" opacity=".2"/>'
      + lock("n-l1", 100, 300) + lock("n-l2", 800, 400)
      + label("n-v", 540, 1500, "VERSCHLOSSEN", RED, 52) + label("n-n", 540, 1640, "NIEMAND DA", "#e6d2ad", 44))
tw(f'tl.fromTo("#n-beam",{{rotation:-30,svgOrigin:"540 1900"}},{{rotation:30,svgOrigin:"540 1900",duration:1.3,yoyo:true,repeat:{max(1,int((S1-S0)/1.3))},ease:"sine.inOut"}},{S0:.3f});')
pop("#n-l1", t_tueren); pop("#n-l2", t_tueren + 0.3); pop("#n-v", t_versch); pop("#n-n", t_niemand2)

# N2 + O „Bis auf einen Ort“ → Wandschrank, oberes Fach, Schiebetür auf, Frau
S0, S1 = t_bis, t_sie
SEPIA.add("so")
inside = (f'<g id="o-in" opacity="0"><rect x="600" y="500" width="440" height="50" rx="16" fill="#c9b79a"/>'
          f'<g transform="translate(780,540) rotate(-90) scale(.4)"><rect x="-34" y="-128" width="27" height="124" rx="12" fill="#4a4a5a"/><rect x="7" y="-128" width="27" height="124" rx="12" fill="#4a4a5a"/>'
          f'<rect x="-62" y="-258" width="124" height="152" rx="36" fill="#7a6a8a"/><rect x="-12" y="-278" width="24" height="26" rx="8" fill="{FIG}"/>'
          f'<circle cx="0" cy="-320" r="64" fill="{FIG}"/><path d="M -60 -330 Q -64 -400 0 -392 Q 64 -400 60 -330 Q 50 -370 0 -372 Q -50 -370 -60 -330 Z" fill="#2a2016"/>'
          f'<rect x="-34" y="-324" width="22" height="6" rx="3" fill="{INK}"/><rect x="12" y="-324" width="22" height="6" rx="3" fill="{INK}"/></g>'
          + "".join(f'<rect x="{x}" y="430" width="26" height="70" rx="8" fill="#cfe7ff" opacity=".85"/><rect x="{x+7}" y="420" width="12" height="12" fill="#3b6cff"/>' for x in (940, 975, 1010))
          + '</g>')
scene("so", S0, S1, jp_room("o", closet=True) + inside
      + f'<rect id="o-dark" width="1080" height="1920" fill="#000" opacity=".55"/>'
      + f'<polygon id="o-beam" points="300,1900 600,380 1080,380 1080,600" fill="#fff4c9" opacity="0"/>'
      + f'<rect id="o-mark" x="574" y="394" width="492" height="172" fill="none" stroke="{RED}" stroke-width="8" stroke-dasharray="20 12" opacity="0"/>'
      + label("o-l1", 300, 220, "MATRATZE", "#e6d2ad", 38) + label("o-l2", 760, 220, "PLASTIKFLASCHEN", "#e6d2ad", 34))
tw(f'tl.to("#so-cam",{{scale:1.12,svgOrigin:"760 640",duration:{t_schiebt-S0:.3f},ease:"sine.inOut"}},{S0:.3f});')
tw(f'tl.fromTo("#o-mark",{{opacity:0}},{{opacity:1,duration:.3,yoyo:true,repeat:5,ease:"sine.inOut"}},{t_fach:.3f});')
tw(f'tl.to("#o-tdoor",{{x:-240,duration:.7,ease:"power2.inOut"}},{t_schiebt + 0.3:.3f});')
tw(f'tl.fromTo("#o-beam",{{opacity:0}},{{opacity:.25,duration:.4}},{t_schiebt + 0.5:.3f});')
tw(f'tl.to("#o-dark",{{opacity:.25,duration:.5}},{t_schiebt + 0.5:.3f});')
tw(f'tl.fromTo("#o-in",{{opacity:0}},{{opacity:1,duration:.5}},{t_darin:.3f});')
pop("#o-l1", t_matratze); pop("#o-l2", t_flaschen)

# P Ein Jahr – sie kam raus, wenn er weg war – sogar geduscht
S0, S1 = t_sie, t_und_kn
SEPIA.add("sp")
DAYS = ["1", "60", "120", "240", "365"]


def card_bg():
    return (f'<rect width="1080" height="1920" fill="#14100c"/><circle cx="540" cy="820" r="560" fill="url(#cardglow)"/>'
            + "".join(f'<rect x="{x}" y="0" width="2" height="1920" fill="#fff" opacity=".025"/>' for x in range(0, 1080, 60)))


drops = "".join(f'<rect id="p-dr{i}" x="{470+i*28}" y="1260" width="6" height="40" rx="3" fill="#8fd3ff" opacity="0"/>' for i in range(6))
scene("sp", S0, S1, card_bg()
      + f'<g id="p-cal"><rect x="290" y="300" width="500" height="480" rx="30" fill="#f2efe8"/><rect x="290" y="300" width="500" height="120" rx="30" fill="{RED}"/>'
        f'<text x="540" y="382" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="52" fill="#fff">TAG</text>'
      + "".join(f'<text id="p-d{i}" x="540" y="660" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="160" fill="#151a21" opacity="0">{d}</text>' for i, d in enumerate(DAYS)) + '</g>'
      + f'<g id="p-out" opacity="0"><rect x="160" y="1140" width="220" height="360" rx="10" fill="{WOOD2}"/><rect x="170" y="1150" width="200" height="340" fill="#1a120a"/>'
        f'<g transform="translate(250,1480) scale(.5)"><rect x="-34" y="-128" width="27" height="124" rx="12" fill="#4a4a5a"/><rect x="7" y="-128" width="27" height="124" rx="12" fill="#4a4a5a"/>'
        f'<rect x="-62" y="-258" width="124" height="152" rx="36" fill="#7a6a8a"/><circle cx="0" cy="-320" r="64" fill="{FIG}"/><path d="M -60 -330 Q -64 -400 0 -392 Q 64 -400 60 -330 Q 50 -370 0 -372 Q -50 -370 -60 -330 Z" fill="#2a2016"/></g></g>'
      + f'<g id="p-sh" opacity="0"><rect x="440" y="1100" width="220" height="30" rx="12" fill="#c9ccd8"/><rect x="540" y="1040" width="20" height="70" fill="#c9ccd8"/><path d="M 550 1040 q 0 -40 60 -40 l 120 0" stroke="#c9ccd8" stroke-width="18" fill="none"/>'
        f'<path d="M 450 1150 L 650 1150 L 700 1520 L 400 1520 Z" fill="#8fd3ff" opacity=".12"/>{drops}'
        + "".join(f'<circle cx="{480+i*60}" cy="1460" r="{40+i*6}" fill="#fff" opacity=".08"/>' for i in range(4)) + '</g>'
      + label("p-l", 760, 1600, "SOGAR GEDUSCHT", RED, 40))
for i in range(len(DAYS)):
    a = S0 + 0.1 + (t_wenn - S0 - 0.1) * i / len(DAYS)
    toggle(f"#p-d{i}", a, S0 + 0.1 + (t_wenn - S0 - 0.1) * (i + 1) / len(DAYS) if i < len(DAYS) - 1 else None)
pop("#p-out", t_raus - 0.2, 0.35, 0.8)
pop("#p-sh", t_dusch - 0.3, 0.35, 0.8); pop("#p-l", t_dusch)
for i in range(6):
    tw(f'tl.fromTo("#p-dr{i}",{{opacity:.9,y:0}},{{y:240,duration:.5,repeat:{max(1,int((S1-t_dusch)/0.5))},ease:"none",immediateRender:false}},{t_dusch + i*0.07:.3f});')

# P2 „Und das Knarzen über dir?“ – Dachluke über deinem Bett öffnet sich einen Spalt
S0, S1 = t_und_kn, t_aufgef
scene("sp2", S0, S1, bedroom("p2") + f'<rect x="400" y="236" width="280" height="24" fill="#120d08"/>'
      + f'<g id="p2-hatch"><rect x="400" y="236" width="280" height="24" fill="#4a3a2a" stroke="#2a1f17" stroke-width="4"/></g>'
      + f'<g id="p2-eyes" opacity="0"><circle cx="510" cy="250" r="7" fill="#f4e3a1"/><circle cx="560" cy="250" r="7" fill="#f4e3a1"/></g>'
      + figure("p2-fig", 470, 1520, 1.2, eyes="w") + bed_front()
      + f'<rect x="0" y="0" width="1080" height="1920" fill="#000" opacity=".25"/>')
tw(f'tl.to("#p2-hatch",{{rotation:-14,svgOrigin:"400 248",duration:1.2,ease:"sine.inOut"}},{S0 + 0.4:.3f});')
tw(f'tl.fromTo("#p2-eyes",{{opacity:0}},{{opacity:1,duration:.5}},{t_jetzt + 0.6:.3f});')
tw(f'tl.to("#sp2-cam",{{scale:1.35,svgOrigin:"540 260",duration:{S1-S0+0.3:.3f},ease:"sine.inOut"}},{S0:.3f});')

# P3 Payoff: das fehlende Essen
S0, S1 = t_aufgef, t_also2
scene("sp3", S0, S1, kitchen("p3") + fridge("p3-fr", 370, 640)
      + label("p3-l", 540, 470, "DAS FEHLENDE ESSEN", RED, 50))
tw(f'tl.set("#p3-fr-yog",{{opacity:0}},{S0:.3f});')
open_door("p3-fr", 370, S0 + 0.1)
tw(f'tl.fromTo("#p3-fr-gap",{{opacity:0}},{{opacity:1,duration:.3,yoyo:true,repeat:{max(1,int((S1-S0)/0.3))},ease:"sine.inOut"}},{S0 + 0.4:.3f});')
tw(f'tl.to("#sp3-cam",{{scale:1.3,svgOrigin:"530 860",duration:{S1-S0:.3f},ease:"sine.inOut"}},{S0:.3f});')
pop("#p3-l", t_fehlende)

# Q Ende: Ja / Nein
S0, S1 = t_also2, TOTAL
scene("sq", S0, S1, kitchen("q") + fridge("q-fr", 120, 640) + figure("q-fig", 760, 1650, 1.25, eyes="w")
      + pill("q-p1", 380, 230, "JA", RED) + pill("q-p2", 700, 230, "NEIN", "#3a4452"))
tw(f'tl.set("#q-fr-yog",{{opacity:0}},{S0:.3f});')
open_door("q-fr", 120, S0 + 0.2)
tw(f'tl.fromTo("#q-fr-gap",{{opacity:0}},{{opacity:1,duration:.35,yoyo:true,repeat:{max(1,int((S1-S0)/0.35))},ease:"sine.inOut"}},{S0 + 0.6:.3f});')
pop("#q-p1", t_vermisst); pop("#q-p2", t_vermisst + 0.3)
tw(f'tl.to("#q-fig",{{y:-12,duration:.6,ease:"sine.inOut",yoyo:true,repeat:3}},{t_selbst:.3f});')

brand_html = []

# ================= UNTERTITEL (Skill 7, Format A: Akzent Rot) =================
KEY = {"JAHRELANG", "HEIMLICH", "JOGHURT", "MERK", "SELBST", "HALB", "LEER", "UNHEIMLICH", "WIRKLICH", "JAPAN", "ZWEITAUSENDACHT",
       "ESSEN", "ABSCHLIESST", "SCHLÜSSEL", "KAMERAS", "HANDY", "BEWEGUNGSMELDER", "LICHT", "WÄRME", "WÄRMEBILD", "FOTO", "DUNKELN",
       "VIBRIERT", "FREMDE", "PERSON", "VERSCHLOSSEN", "SCHRANK", "FRAU", "MATRATZE", "PLASTIKFLASCHEN", "JAHR", "FEHLENDE", "VERMISST",
       "KNARZEN", "OBEN", "VERRÜCKT", "POLIZEI", "NIEMAND", "ORT", "WANDSCHRANK", "FACH", "GEDUSCHT", "KAMERA"}
DISPLAY = {"zweitausendacht.": "2008."}
SKIP = set()


def norm(t):
    return re.sub(r"[^\wÄÖÜäöüß]", "", t).upper().replace("ß", "SS")


words = [w for w in W if w["t"] not in SKIP]
# „A M L“ zu einem Wort
merged = []
for w in words:
    if merged and merged[-1]["t"] in ("A", "A M") and w["t"] in ("M", "L."):
        merged[-1] = {"t": merged[-1]["t"] + " " + w["t"], "s": merged[-1]["s"], "e": w["e"]}
    else:
        merged.append(dict(w))
for w in merged:
    if w["t"] == "A M L.":
        w["t"] = "AML."
chunks, cur = [], []
for i, w in enumerate(merged):
    cur.append(w)
    nxt = merged[i+1] if i + 1 < len(merged) else None
    text = " ".join(x["t"] for x in cur)
    if (re.search(r"[.,:?!]$", w["t"]) or len(cur) >= 3 or (nxt and len(text) + 1 + len(nxt["t"]) > 20)
            or (nxt and nxt["s"] - w["e"] > 0.25) or nxt is None):
        chunks.append(cur); cur = []
changed = True
while changed:
    changed = False
    for k in range(len(chunks) - 1):
        if chunks[k+1][0]["s"] - chunks[k][0]["s"] < 0.45:
            m = chunks[k] + chunks[k+1]
            if len(m) <= 4 and len(" ".join(x["t"] for x in m)) <= 24:
                chunks[k:k+2] = [m]; changed = True; break
subs = []
for k, c in enumerate(chunks):
    s = c[0]["s"]
    e = min(chunks[k+1][0]["s"], c[-1]["e"] + 0.6) if k + 1 < len(chunks) else min(TOTAL, c[-1]["e"] + 1.2)
    parts, plain = [], []
    for w in c:
        t = DISPLAY.get(w["t"], w["t"]); plain.append(t)
        parts.append(f'<span class="k">{html.escape(t)}</span>' if norm(w["t"]) in KEY or norm(t) in KEY else html.escape(t))
    fs = min(62, int(980 / (0.56 * max(len(" ".join(plain)), 1))))
    sid = f"sub{k}"
    subs.append(f'<div id="{sid}" class="clip sub" data-start="{s:.3f}" data-duration="{e-s:.3f}" data-track-index="9" style="font-size:{fs}px">{" ".join(parts)}</div>')
    tw(f'tl.fromTo("#{sid}",{{y:14,opacity:0}},{{y:0,opacity:1,duration:.16,ease:"power2.out"}},{s:.3f});')


# ================= GLOBALE EBENEN (Skill 6a) =================
def noise_png(n=256, seed=3):
    rr = random.Random(seed)
    raw = b"".join(b"\x00" + bytes(v for _ in range(n) for v in (lambda g: (g, g, g, rr.randint(0, 38)))(rr.randint(0, 255))) for _ in range(n))
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", n, n, 8, 6, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
    return base64.b64encode(png).decode()


DEFS = f"""<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<linearGradient id="skyg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{SKY1}"/><stop offset=".6" stop-color="{SKY2}"/><stop offset="1" stop-color="{VIO}"/></linearGradient>
<radialGradient id="moonglow"><stop offset="0" stop-color="{MOON}" stop-opacity=".35"/><stop offset="1" stop-color="{MOON}" stop-opacity="0"/></radialGradient>
<linearGradient id="lampcone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{LAMP}" stop-opacity=".35"/><stop offset="1" stop-color="{LAMP}" stop-opacity="0"/></linearGradient>
<radialGradient id="cardglow"><stop offset="0" stop-color="#3a3d8f" stop-opacity=".55"/><stop offset="1" stop-color="#3a3d8f" stop-opacity="0"/></radialGradient>
<radialGradient id="stationglow" cx=".5" cy="0" r="1"><stop offset="0" stop-color="#fff4c9" stop-opacity=".35"/><stop offset="1" stop-color="#fff4c9" stop-opacity="0"/></radialGradient>
<radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".7"/></radialGradient>
<radialGradient id="sepvig" cx=".5" cy=".5" r=".75"><stop offset=".45" stop-color="#2a1a08" stop-opacity="0"/><stop offset="1" stop-color="#1a0f04" stop-opacity=".85"/></radialGradient>
<radialGradient id="coldglow" cx=".5" cy="0" r="1"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#bfe0ff" stop-opacity=".2"/></radialGradient>
<radialGradient id="heatg"><stop offset="0" stop-color="#fff2a8"/><stop offset=".45" stop-color="#ffb35c"/><stop offset="1" stop-color="{RED}"/></radialGradient>
<radialGradient id="redvig" cx=".5" cy=".5" r=".72"><stop offset=".5" stop-color="{RED}" stop-opacity="0"/><stop offset="1" stop-color="{RED}" stop-opacity=".7"/></radialGradient>
<filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="14" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="glowsoft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs></svg>"""

OVER = []
dust = []
for i in range(40):
    x = RNG.randint(0, 1080); y = RNG.randint(0, 1920); r = RNG.choice([2, 3, 3, 4, 5])
    dust.append(f'<circle id="dust{i}" cx="{x}" cy="{y}" r="{r}" fill="#e8e6ff" opacity="{RNG.uniform(.12,.4):.2f}"/>')
    dur = RNG.uniform(6, 14)
    tw(f'tl.fromTo("#dust{i}",{{x:0,y:0}},{{x:{RNG.randint(-80,80)},y:{-RNG.randint(250,600)},duration:{dur:.2f},ease:"sine.inOut",repeat:{int(TOTAL/dur)+1},yoyo:true}},0);')
OVER.append(f'<div id="ov-dust" class="clip ov" data-start="0" data-duration="{TOTAL}" data-track-index="5" style="z-index:5">'
            f'<svg viewBox="0 0 1080 1920" width="1080" height="1920">{"".join(dust)}<rect width="1080" height="1920" fill="url(#vig)"/></svg></div>')
OVER.append(f'<div id="ov-grain" class="clip ov" data-start="0" data-duration="{TOTAL}" data-track-index="6" '
            f'style="z-index:6;left:-128px;top:-128px;width:1336px;height:2176px;opacity:.25;mix-blend-mode:overlay;'
            f'background-image:url(data:image/png;base64,{noise_png()});background-size:256px 256px"></div>')
t = 0.0
while t < TOTAL:
    tw(f'tl.set("#ov-grain",{{x:{RNG.randint(-120,120)},y:{RNG.randint(-120,120)}}},{t:.2f});'); t += 0.1


def danger(did, t0, t1):
    OVER.append(f'<div id="{did}" class="clip ov" data-start="{t0:.3f}" data-duration="{t1-t0:.3f}" data-track-index="8" style="z-index:8">'
                f'<svg viewBox="0 0 1080 1920" width="1080" height="1920"><rect id="{did}-v" width="1080" height="1920" fill="url(#redvig)" opacity=".3"/></svg></div>')
    tw(f'tl.fromTo("#{did}-v",{{opacity:.2}},{{opacity:.7,duration:.45,yoyo:true,repeat:{int((t1-t0)/0.45)},ease:"sine.inOut"}},{t0:.3f});')


danger("ov-d1", t_fremde, t_ruft)
danger("ov-d2", t_darin, t_sie)


def archive(aid, t0, t1):
    perf = "".join(f'<rect x="14" y="{y}" width="34" height="46" rx="8" fill="#0d0905"/><rect x="1032" y="{y}" width="34" height="46" rx="8" fill="#0d0905"/>' for y in range(10, 1920, 90))
    scr = "".join(f'<rect id="{aid}-sc{i}" x="0" y="0" width="3" height="1920" fill="#f3e2c0" opacity="0"/>' for i in range(3))
    OVER.append(f'<div id="{aid}" class="clip ov" data-start="{t0:.3f}" data-duration="{t1-t0:.3f}" data-track-index="7" style="z-index:7">'
                f'<svg viewBox="0 0 1080 1920" width="1080" height="1920"><rect width="1080" height="1920" fill="url(#sepvig)"/>'
                f'<rect x="0" y="0" width="62" height="1920" fill="#1a120a" opacity=".9"/><rect x="1018" y="0" width="62" height="1920" fill="#1a120a" opacity=".9"/>{perf}{scr}'
                f'<g opacity=".85"><circle cx="110" cy="1820" r="10" fill="{RED}"/><text x="132" y="1832" font-family="JetBrains Mono, monospace" font-weight="800" font-size="30" fill="#e6d2ad">ECHTER FALL · JAPAN 2008</text></g></svg></div>')
    tt = t0
    while tt < t1:
        for i in range(3):
            on = RNG.random() < 0.55
            tw(f'tl.set("#{aid}-sc{i}",{{opacity:{RNG.uniform(.08,.2) if on else 0:.2f},x:{RNG.randint(80, 1000)}}},{tt:.2f});')
        tt += 0.3


archive("ov-arch1", t_genau, t_und_kn)

for fid in FIGS:
    tw(f'tl.fromTo("#{fid}-body",{{scaleY:1}},{{scaleY:1.02,transformOrigin:"50% 100%",duration:1.3,yoyo:true,repeat:{int(TOTAL/1.3)},ease:"sine.inOut"}},0);')
for sid, t0, t1, _ in SCENES[1:]:
    tw(f'tl.fromTo("#{sid}",{{opacity:0}},{{opacity:1,duration:{XF},ease:"sine.inOut"}},{t0:.3f});')

# ================= HTML =================
scene_html = [f'<div id="{sid}" class="clip scene{' sep' if sid in SEPIA else ''}" data-start="{t0:.3f}" data-duration="{min(t1+XF, TOTAL)-t0:.3f}" data-track-index="1">'
              f'<svg viewBox="0 0 1080 1920" width="1080" height="1920">{inner}</svg></div>' for sid, t0, t1, inner in SCENES]

doc = f'''<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Heimlicher Mitbewohner</title>
    <script src="assets/gsap.min.js"></script>
    <style>
      :root {{ --ground: {SKY1}; --ink: #ffffff; --accent: {RED}; --font-display: "Poppins", sans-serif; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: var(--ground); }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: var(--font-display); }}
      .scene, .ov {{ position: absolute; inset: 0; }}
      .ov {{ pointer-events: none; }}
      .scene svg {{ display: block; }}
      .scene.sep {{ filter: sepia(.75) saturate(.85) brightness(.92) contrast(1.05); }}
      .sub {{
        position: absolute; left: 40px; right: 40px; top: 960px; margin-top: -0.6em; text-align: center;
        color: var(--ink); font-weight: 600; line-height: 1.15; white-space: nowrap; z-index: 20;
        -webkit-text-stroke: 7px rgba(0,0,0,.85); paint-order: stroke fill; text-shadow: 0 3px 10px rgba(0,0,0,.6);
      }}
      .sub .k {{ color: var(--accent); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <audio id="vo" class="clip" data-start="0" data-duration="{VO_END:.2f}" data-volume="1" src="assets/voiceover.mp3"></audio>
      <audio id="sfx" class="clip" data-start="0" data-duration="{TOTAL}" data-volume="0.45" src="assets/sfx_bed.wav"></audio>
      {DEFS}
      {"".join(scene_html)}
      {"".join(OVER)}
      {"".join(brand_html)}
      {"".join(subs)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {chr(10).join("      " + x for x in T)}
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
'''
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(doc)
cues = {k: v for k, v in globals().items() if k.startswith("t_") and isinstance(v, (int, float))}
cues["TOTAL"] = TOTAL
json.dump(cues, open(os.path.join(HERE, "assets/cues.json"), "w"), indent=1)
print(f"Szenen: {len(SCENES)}, Untertitel: {len(subs)}, Tweens: {len(T)}, Länge: {TOTAL}s")
