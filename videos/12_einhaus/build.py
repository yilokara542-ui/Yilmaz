#!/usr/bin/env python3
"""Generator für index.html – Video 12 „In diesem Haus lebt nur eine Person“ (Mitmach-Video).

Alle Zeiten kommen aus assets/words.json (wortgenaue Voiceover-Zeitstempel).
Aufruf: python3 build.py → index.html + assets/cues.json
"""
import json, re, html, os, math, random, zlib, struct, base64

HERE = os.path.dirname(os.path.abspath(__file__))
W = json.load(open(os.path.join(HERE, "assets/words.json"), encoding="utf-8"))
VO_END = W[-1]["e"]
TOTAL = round(max(VO_END + 1.6, 61.2), 2)   # Skill: mind. 61 s          # Schlussfrage steht noch kurz
XF = 0.3                                 # Überblendung zwischen Szenen
RNG = random.Random(12)

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
    if outfit in ("tunic", "tunic2"):   # Dorfbewohner: Leinentunika mit Gürtel
        H, H2, P, SH = (("#8a6a4a", "#6e5038", "#4a3a2a", "#3a2a1a") if outfit == "tunic" else ("#5a7a9a", "#4a6a8a", "#4a3a2a", "#3a2a1a"))
        extra = '<rect x="-62" y="-150" width="124" height="14" fill="#3a2a1a"/><rect x="-10" y="-152" width="20" height="18" rx="3" fill="#c9a24b"/><polygon points="-20,-258 0,-226 20,-258" fill="#efe4cc"/>'
    elif outfit == "apron":   # Bäcker: weiße Schürze, Mütze-artiger Kragen
        H, H2, P, SH = "#c97b4a", "#a8643a", "#4a3a2a", "#3a2a1a"
        extra = '<rect x="-46" y="-236" width="92" height="132" rx="18" fill="#f6f1e6"/><rect x="-46" y="-206" width="92" height="8" fill="#e9e1cf"/>'
    elif outfit == "hunter":  # Jäger: dunkles Wams, Lederriemen kreuzweise
        H, H2, P, SH = "#3a3a44", "#2a2a33", "#e9e1cf", "#3a2a1a"
        extra = '<line x1="-56" y1="-250" x2="56" y2="-120" stroke="#7a4a2a" stroke-width="12"/><line x1="56" y1="-250" x2="-56" y2="-120" stroke="#7a4a2a" stroke-width="12"/>'
    elif outfit == "shirt":   # Mann in Japan: helles Hemd, Krawatte, dunkle Hose
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
        + eye("c", 1 if eyes == "c" else 0,
              f'<rect x="-34" y="-324" width="22" height="6" rx="3" fill="{E}"/><rect x="12" y="-324" width="22" height="6" rx="3" fill="{E}"/>'
              f'<path d="M -14 -292 Q 0 -282 14 -292" stroke="{E}" stroke-width="5" fill="none" stroke-linecap="round"/>')
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
GRASS = "#5fae5a"; GRASS2 = "#4f9a4c"; ROAD = "#4a4f5c"; WALLC = "#f3e9d6"; WOODC = "#7a5236"; ROOFC = "#3d4a6b"; ROOFC2 = "#33405e"
GLOWC = "#ffd98a"; WATER = "#5fb4e0"; GOLD = "#e9c46a"; PLANT = "#3f8f5a"
SEPIA = set()

t_ich = ws("Ich"); t_zumindest = ws("Zumindest")
t_es = ws("Es", 5); t_wiese = ws("Wiese"); t_ringsum = ws("Ringsum"); t_strassen = ws("Straßen"); t_baeume = ws("Bäume"); t_see = ws("See")
HAS_INNEN = any(w["t"].lower().startswith("innen") for w in W)
t_innen = ws("Und", t_see) if HAS_INNEN else ws("Eine", t_see)
t_matr = ws("Matratze"); t_lampe = ws("Lampe"); t_fenster1 = ws("Fenster", t_lampe); t_mehr = ws("Mehr")
t_aber = ws("Aber"); t_dunklen = ws("leere", t_aber) if any(w["t"].lower().startswith("leere") for w in W) else ws("dunklen"); t_platz = ws("Platz", t_aber)
t_also1 = ws("Also"); t_regel = ws("Regel"); t_laut = ws("Laut")
t_jeder = ws("Jeder"); t_komm1 = ws("Kommentare"); t_genau = ws("genau", t_komm1)
t_gaming = ws("Gaming"); t_baue1 = ws("baue", t_gaming); t_pflanzen = ws("Pflanzen"); t_baue2 = ws("baue", t_pflanzen)
t_bett = ws("Bett"); t_sterne = ws("Sterne"); t_baue3 = ws("baue", t_sterne)
t_jeder2 = ws("Jeder", t_baue3); t_namen = ws("Namen", t_jeder2); t_tuer = ws("Tür")
t_wenn = ws("wenn", t_tuer); t_stock = ws("Stockwerk")
t_heute = ws("Heute"); t_morgen = ws("Morgen"); t_hundert = ws("hundert")
t_also2 = ws("Also", t_hundert); t_wie = ws("Wie", t_also2); t_schreib = ws("Schreib")

NAMES = ["@lina.baut", "@jonas.k39", "@mia_nrw", "@tim.zockt", "@emma.vb", "@noah_2011", "@lea.mlk", "@finn.ok", "@sara.art", "@ben_gg", "@ida.moon"]


def plant(x, y, s=1.0):
    leaves = "".join(f'<ellipse cx="{x + math.cos(a)*40*s:.0f}" cy="{y - 70*s + math.sin(a)*34*s:.0f}" rx="{36*s:.0f}" ry="{14*s:.0f}" fill="{PLANT if i%2 else "#4fa86a"}" transform="rotate({math.degrees(a):.0f} {x + math.cos(a)*40*s:.0f} {y - 70*s + math.sin(a)*34*s:.0f})"/>'
                     for i, a in enumerate([-2.8, -2.2, -1.6, -1.0, -0.4, -1.9, -1.3]))
    return (f'{leaves}<path d="M {x-34*s} {y-40*s} L {x+34*s} {y-40*s} L {x+26*s} {y} L {x-26*s} {y} Z" fill="#c26a3d"/>'
            f'<rect x="{x-38*s}" y="{y-48*s}" width="{76*s}" height="{12*s}" rx="4" fill="#a8562f"/>')



# ---------- Umgebung (Skill 6a: liebevoll, detailreich) ----------
def sky_sunset():
    return (f'<rect width="1080" height="1920" fill="url(#sunset)"/><circle cx="820" cy="640" r="120" fill="#ffd27a"/><circle cx="820" cy="640" r="300" fill="url(#sunglow)"/>'
            + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#fff" opacity=".22"/>' for x, y, rx, ry in ((180, 280, 190, 44), (640, 200, 240, 50), (960, 420, 150, 34), (360, 480, 140, 30)))
            + "".join(f'<path id="bird{i}" d="M {x} {y} q 14 -12 28 0 q 14 -12 28 0" stroke="#3a3048" stroke-width="5" fill="none"/>' for i, (x, y) in enumerate(((300, 360), (380, 320), (460, 380)))))


def sky_night():
    return (f'<rect width="1080" height="1920" fill="url(#nightsky)"/>'
            + "".join(f'<circle cx="{RNG.randint(0,1080)}" cy="{RNG.randint(0,900)}" r="{RNG.choice([1.5,2,2.5,3])}" fill="#fff" opacity="{RNG.uniform(.3,.9):.2f}"/>' for _ in range(90))
            + f'<circle cx="840" cy="300" r="70" fill="{MOON}"/><circle cx="840" cy="300" r="170" fill="url(#moonglow)"/>')


def tree(x, y, s=1.0, col=GRASS2):
    return (f'<ellipse cx="{x}" cy="{y+4}" rx="{60*s}" ry="{14*s}" fill="#000" opacity=".2"/><rect x="{x-10*s}" y="{y-110*s}" width="{20*s}" height="{110*s}" fill="#6b4a32"/>'
            f'<circle cx="{x}" cy="{y-150*s}" r="{70*s}" fill="{col}"/><circle cx="{x-45*s}" cy="{y-120*s}" r="{50*s}" fill="{col}"/><circle cx="{x+48*s}" cy="{y-118*s}" r="{52*s}" fill="{col}"/>'
            f'<circle cx="{x-20*s}" cy="{y-175*s}" r="{30*s}" fill="#7cc46f" opacity=".6"/>')


def lantern(x, y, gid=None):
    g = f' id="{gid}"' if gid else ""
    return (f'<g{g}><rect x="{x-5}" y="{y-260}" width="10" height="260" fill="#2a2f3a"/><rect x="{x-24}" y="{y-300}" width="48" height="50" rx="10" fill="#2a2f3a"/>'
            f'<rect x="{x-16}" y="{y-292}" width="32" height="34" rx="6" fill="{GLOWC}"/><circle cx="{x}" cy="{y-276}" r="70" fill="url(#lampglow2)"/></g>')


def flowers(x, y, n=8, seed=1):
    rr = random.Random(seed)
    return "".join(f'<circle cx="{x+rr.randint(-80,80)}" cy="{y+rr.randint(-20,20)}" r="{rr.choice([6,7,8])}" fill="{rr.choice(("#ff6b8a","#ffd166","#ffffff","#c77dff","#ff8c42"))}"/>' for _ in range(n))


def fence(y, x0=0, x1=1080):
    return ("".join(f'<rect x="{x}" y="{y-60}" width="14" height="66" rx="4" fill="#f6efe2"/>' for x in range(x0, x1, 46))
            + f'<rect x="{x0}" y="{y-44}" width="{x1-x0}" height="10" fill="#f6efe2"/><rect x="{x0}" y="{y-20}" width="{x1-x0}" height="10" fill="#f6efe2"/>')


# ---------- Das Haus: 3 Etagen × 4 Zimmer = 12 ----------
HX, HY, RW, RH = 90, 760, 225, 300          # links, Oberkante oberste Etage, Zimmerbreite/-höhe


def room_xy(i):
    return HX + (i % 4) * RW, HY + (i // 4) * RH


def room_inner(i, kind, prefix, name=None):
    x, y = room_xy(i); w, h = RW, RH
    out = ""
    if kind == "empty":
        out += (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#dccdb2"/>' + "".join(f'<rect x="{x}" y="{y+h-40+k*0}" width="{w}" height="40" fill="#b08a62"/>' for k in range(1))
                + f'<line x1="{x+w/2}" y1="{y}" x2="{x+w/2}" y2="{y+60}" stroke="#555" stroke-width="3"/><circle cx="{x+w/2}" cy="{y+66}" r="9" fill="#cfcfcf"/>'
                + f'<g id="{prefix}-free{i}"><rect x="{x+w/2-50}" y="{y+120}" width="100" height="44" rx="8" fill="#fff" stroke="#2a9d8f" stroke-width="4"/>'
                f'<text x="{x+w/2}" y="{y+151}" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="24" fill="#2a9d8f">FREI</text></g>')
    elif kind == "mine":
        out += (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#f2d8b4"/><rect x="{x}" y="{y+h-40}" width="{w}" height="40" fill="#b08a62"/>'
                f'<circle cx="{x+60}" cy="{y+130}" r="110" fill="url(#lampglow2)"/>'
                f'<g id="{prefix}-win"><rect x="{x+120}" y="{y+40}" width="80" height="100" fill="url(#nightsky)" stroke="#fff" stroke-width="6"/><circle cx="{x+178}" cy="{y+64}" r="10" fill="{MOON}"/></g>'
                f'<g id="{prefix}-lamp"><rect x="{x+46}" y="{y+150}" width="8" height="100" fill="#444"/><path d="M {x+28} {y+150} L {x+72} {y+150} L {x+62} {y+120} L {x+38} {y+120} Z" fill="#ffcc66"/></g>'
                f'<g id="{prefix}-mat"><rect x="{x+70}" y="{y+226}" width="140" height="34" rx="10" fill="#e9e6f2"/><rect x="{x+76}" y="{y+216}" width="44" height="20" rx="8" fill="#fff"/></g>')
    elif kind == "gaming":
        out += (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#2a1f4a"/><rect x="{x}" y="{y+h-40}" width="{w}" height="40" fill="#3a2a5a"/>'
                f'<rect x="{x}" y="{y+10}" width="{w}" height="8" fill="#ff4fd8" opacity=".9"/><rect x="{x}" y="{y+18}" width="{w}" height="6" fill="#4fd8ff" opacity=".7"/>'
                + "".join(f'<rect x="{x+18+k*66}" y="{y+100}" width="60" height="44" rx="4" fill="{c}"/><rect x="{x+44+k*66}" y="{y+144}" width="8" height="18" fill="#222"/>' for k, c in enumerate(("#4fd8ff", "#ff4fd8", "#7cff6b")))
                + f'<rect x="{x+10}" y="{y+160}" width="205" height="14" fill="#111"/><rect x="{x+20}" y="{y+174}" width="10" height="86" fill="#111"/><rect x="{x+195}" y="{y+174}" width="10" height="86" fill="#111"/>'
                f'<path d="M {x+90} {y+260} L {x+90} {y+190} Q {x+112} {y+170} {x+134} {y+190} L {x+134} {y+260}" fill="#e63946"/><circle cx="{x+112}" cy="{y+130}" r="90" fill="#4fd8ff" opacity=".1"/>')
    elif kind == "plants":
        out += (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#dfeedd"/><rect x="{x}" y="{y+h-40}" width="{w}" height="40" fill="#b08a62"/>'
                + "".join(f'<path d="M {x+20+k*45} {y} q 10 60 -6 {90+k*14}" stroke="#3f8f5a" stroke-width="6" fill="none"/>' + "".join(f'<ellipse cx="{x+18+k*45+(j%2)*10}" cy="{y+20+j*24}" rx="10" ry="6" fill="#4fa86a"/>' for j in range(3 + k % 2)) for k in range(5))
                + plant(x + 50, y + 260, 0.8) + plant(x + 120, y + 262, 1.0) + plant(x + 185, y + 260, 0.7)
                + f'<rect x="{x+150}" y="{y+120}" width="60" height="10" fill="{WOODC}"/>' + plant(x + 180, y + 120, 0.45))
    elif kind == "stars":
        out += (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#1c2340"/><rect x="{x}" y="{y}" width="{w}" height="120" fill="url(#nightsky)"/>'
                + "".join(f'<circle cx="{x+15+(k*37)%200}" cy="{y+12+(k*23)%100}" r="2.5" fill="#fff"/>' for k in range(14))
                + "".join(f'<rect x="{x+k*56}" y="{y}" width="4" height="120" fill="#cfd8ff" opacity=".6"/>' for k in range(5))
                + f'<rect x="{x}" y="{y+118}" width="{w}" height="6" fill="#cfd8ff" opacity=".7"/><rect x="{x}" y="{y+h-40}" width="{w}" height="40" fill="#3a3f6a"/>'
                f'<rect x="{x+30}" y="{y+200}" width="170" height="60" rx="12" fill="#e9e6f2"/><rect x="{x+30}" y="{y+180}" width="50" height="34" rx="10" fill="#fff"/><rect x="{x+90}" y="{y+204}" width="110" height="56" rx="12" fill="#7a8aff"/>')
    if name:
        out += (f'<g id="{prefix}-np{i}" opacity="0"><rect x="{x+w/2-92}" y="{y+h-82}" width="184" height="38" rx="8" fill="#fff4dc" stroke="{WOODC}" stroke-width="4"/>'
                f'<text x="{x+w/2}" y="{y+h-55}" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="20" fill="#3a2a1a">{name}</text></g>')
    return f'<g id="{prefix}-r{i}">{out}</g>'


def house_cut(prefix, kinds, names=None, extra_floor=False):
    names = names or {}
    rooms = "".join(room_inner(i, kinds.get(i, "empty"), prefix, names.get(i)) for i in range(12))
    grid = ("".join(f'<rect x="{HX}" y="{HY + k*RH - 6}" width="{4*RW}" height="12" fill="{WOODC}"/>' for k in range(4))
            + "".join(f'<rect x="{HX + k*RW - 6}" y="{HY}" width="12" height="{3*RH}" fill="{WOODC}"/>' for k in range(5)))
    roof = (f'<polygon points="{HX-50},{HY} {HX+2*RW},{HY-300} {HX+4*RW+50},{HY}" fill="{ROOFC}"/>'
            + "".join(f'<line x1="{HX-30+k*60}" y1="{HY}" x2="{HX+2*RW}" y2="{HY-290}" stroke="{ROOFC2}" stroke-width="4"/>' for k in range(17))
            + f'<rect x="{HX+3*RW}" y="{HY-260}" width="60" height="140" fill="#8a5a42"/>')
    ef = ""
    if extra_floor:
        ef = (f'<g id="{prefix}-ef"><rect x="{HX}" y="{HY-RH}" width="{4*RW}" height="{RH}" fill="#e9dcc4"/>'
              + "".join(f'<rect x="{HX + k*RW - 6}" y="{HY-RH}" width="12" height="{RH}" fill="{WOODC}"/>' for k in range(5))
              + "".join(f'<g><rect x="{HX+k*RW+62}" y="{HY-RH+110}" width="100" height="44" rx="8" fill="#fff" stroke="#2a9d8f" stroke-width="4"/>'
                        f'<text x="{HX+k*RW+112}" y="{HY-RH+141}" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="24" fill="#2a9d8f">FREI</text></g>' for k in range(4))
              + f'<polygon points="{HX-50},{HY-RH} {HX+2*RW},{HY-RH-300} {HX+4*RW+50},{HY-RH}" fill="{ROOFC}"/></g>')
    return f'<g id="{prefix}-house">{"" if extra_floor else f'<g id="{prefix}-roof">{roof}</g>'}{rooms}{grid}{ef}<rect x="{HX-20}" y="{HY+3*RH}" width="{4*RW+40}" height="24" fill="#8a7a6a"/></g>'


def house_ext(prefix, lit, night=False):
    win = ""
    for i in range(12):
        x, y = room_xy(i)
        on = i in lit
        win += (f'<g id="{prefix}-w{i}"><rect x="{x+62}" y="{y+70}" width="100" height="130" rx="6" fill="{GLOWC if on else ("#1d2440" if night else "#9fb4cc")}" stroke="#fff" stroke-width="8"/>'
                f'<rect x="{x+108}" y="{y+70}" width="8" height="130" fill="#fff"/><rect x="{x+62}" y="{y+130}" width="100" height="8" fill="#fff"/>'
                + (f'<circle cx="{x+112}" cy="{y+135}" r="110" fill="url(#lampglow2)"/>' if on else "")
                + f'<rect x="{x+52}" y="{y+200}" width="120" height="16" fill="{WOODC}"/>' + flowers(x + 112, y + 196, 5, i) + '</g>')
    body = (f'<polygon points="{HX-50},{HY} {HX+2*RW},{HY-300} {HX+4*RW+50},{HY}" fill="{ROOFC}"/>'
            + "".join(f'<line x1="{HX-30+k*60}" y1="{HY}" x2="{HX+2*RW}" y2="{HY-290}" stroke="{ROOFC2}" stroke-width="4"/>' for k in range(17))
            + f'<rect x="{HX+3*RW}" y="{HY-260}" width="60" height="140" fill="#8a5a42"/><circle cx="{HX+2*RW}" cy="{HY-150}" r="50" fill="#e9e1cf"/><circle cx="{HX+2*RW}" cy="{HY-150}" r="38" fill="{"#1d2440" if night else "#9fb4cc"}"/>'
            f'<rect x="{HX}" y="{HY}" width="{4*RW}" height="{3*RH}" fill="{WALLC}"/>'
            + "".join(f'<rect x="{HX}" y="{HY+k*RH-6}" width="{4*RW}" height="12" fill="{WOODC}"/>' for k in range(1, 3))
            + win
            + f'<rect x="{HX+2*RW-70}" y="{HY+3*RH-200}" width="140" height="200" rx="70" fill="{WOODC}"/><circle cx="{HX+2*RW+45}" cy="{HY+3*RH-100}" r="8" fill="{GOLD}"/>'
            + lantern(HX + 2 * RW - 130, HY + 3 * RH) + lantern(HX + 2 * RW + 130, HY + 3 * RH))
    return f'<g id="{prefix}-hx">{body}</g>'


def meadow(prefix, y0=1660):
    return (f'<rect x="0" y="{y0-220}" width="1080" height="{1920-y0+220}" fill="{GRASS}"/>'
            f'<path d="M -50 {y0-200} Q 300 {y0-280} 700 {y0-220} T 1130 {y0-240} L 1130 {y0} L -50 {y0} Z" fill="#6fbb66"/>'
            f'<path d="M 540 {y0} L 470 1920 L 610 1920 Z" fill="#e2d2b0"/>'
            + "".join(f'<path d="M {x} {y0+40+(x*7)%120} l 5 -24 l 5 24" stroke="#3f8a3a" stroke-width="4" fill="none"/>' for x in range(10, 1080, 34))
            + flowers(150, y0 + 120, 12, 3) + flowers(900, y0 + 160, 12, 4) + flowers(300, y0 + 230, 10, 5) + flowers(780, y0 + 60, 10, 6)
            + fence(y0 + 20, 0, 380) + fence(y0 + 20, 700, 1080)
            + tree(80, y0 - 30, 1.1) + tree(1000, y0 - 40, 1.2) + tree(200, y0 + 10, 0.7, "#5aa85a"))


def hud(hid, day, count, op=1):
    return (f'<g id="{hid}" opacity="{op}"><rect x="390" y="140" width="300" height="50" rx="25" fill="#1a1f2e" fill-opacity=".85"/>'
            f'<text x="540" y="174" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="26" fill="#fff" letter-spacing="4">TAG {day}</text>'
            f'<text x="540" y="270" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="74" fill="#fff" stroke="#1a1f2e" stroke-width="10" paint-order="stroke">BEWOHNER: {count}</text></g>')



CX0, CY0, CW, CH = 360, 1180, 360, 480     # Häuschen: links, oben, Breite, Höhe (Unterkante 1660)


def cottage(prefix, night=False, me=True, cutaway=False):
    x, y, w, h = CX0, CY0, CW, CH
    roof = (f'<polygon points="{x-50},{y} {x+w/2},{y-260} {x+w+50},{y}" fill="{ROOFC}"/>'
            + "".join(f'<line x1="{x-30+k*44}" y1="{y}" x2="{x+w/2}" y2="{y-250}" stroke="{ROOFC2}" stroke-width="4"/>' for k in range(11))
            + f'<rect x="{x+w-90}" y="{y-200}" width="46" height="120" fill="#8a5a42"/>'
            + "".join(f'<circle id="{prefix}-sm{k}" cx="{x+w-67}" cy="{y-220-k*40}" r="{16+k*7}" fill="#e9e6f2" opacity="{.45-k*.1:.2f}"/>' for k in range(3)))
    if cutaway:
        inner = (f'<g transform="translate({x},{y}) scale({w/RW:.4f},{h/RH:.4f}) translate({-room_xy(8)[0]},{-room_xy(8)[1]})">{room_inner(8, "mine", prefix)}</g>'
                 + f'<rect x="{x-8}" y="{y}" width="16" height="{h}" fill="{WOODC}"/><rect x="{x+w-8}" y="{y}" width="16" height="{h}" fill="{WOODC}"/>'
                 + f'<rect x="{x-8}" y="{y-8}" width="{w+16}" height="16" fill="{WOODC}"/><rect x="{x-20}" y="{y+h}" width="{w+40}" height="20" fill="#8a7a6a"/>')
        return f'<g id="{prefix}-cot">{roof}{inner}</g>'
    win_fill = GLOWC
    body = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{WALLC}"/>'
            + "".join(f'<rect x="{x}" y="{y+k*60}" width="{w}" height="3" fill="#000" opacity=".05"/>' for k in range(8))
            + f'<rect x="{x+24}" y="{y+h-230}" width="110" height="230" rx="55" fill="{WOODC}"/><circle cx="{x+118}" cy="{y+h-110}" r="8" fill="{GOLD}"/>'
            + f'<g id="{prefix}-win"><rect x="{x+170}" y="{y+90}" width="160" height="190" rx="8" fill="{win_fill}" stroke="#fff" stroke-width="10"/>'
            + f'<circle cx="{x+250}" cy="{y+185}" r="160" fill="url(#lampglow2)"/></g>'
            + (figure(f"{prefix}-me", x + 250, y + 280, 0.5, eyes="n") if me else "")
            + f'<rect x="{x+246}" y="{y+90}" width="8" height="190" fill="#fff"/><rect x="{x+170}" y="{y+180}" width="160" height="8" fill="#fff"/>'
            + f'<rect x="{x+160}" y="{y+280}" width="180" height="20" fill="{WOODC}"/>' + flowers(x + 250, y + 276, 8, 21)
            + lantern(x + 160, y + h) + f'<rect x="{x-20}" y="{y+h}" width="{w+40}" height="20" fill="#8a7a6a"/>')
    mailbox = f'<rect x="{x+w+90}" y="{y+h-120}" width="12" height="120" fill="#6b4a32"/><rect x="{x+w+66}" y="{y+h-160}" width="60" height="44" rx="10" fill="{RED}"/>'
    return f'<g id="{prefix}-cot">{roof}{body}{mailbox}</g>'


# ================= SZENEN =================
# A Hook: kleines Ein-Zimmer-Häuschen, ein Licht
S0, S1 = 0.0, t_es
scene("sa", S0, S1, sky_sunset() + meadow("sa") + cottage("sa") + hud("sa-hud", 1, 1)
      + f'<g id="sa-q" opacity="0"><circle cx="880" cy="230" r="46" fill="{RED}"/><text x="880" y="252" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="60" fill="#fff">?</text></g>')
tw(f'tl.fromTo("#sa-cam",{{scale:1.08,svgOrigin:"540 1400"}},{{scale:1,svgOrigin:"540 1400",duration:{S1-S0:.3f},ease:"sine.out"}},{S0:.3f});')
tw(f'tl.fromTo("#sa-win",{{opacity:.6}},{{opacity:1,duration:.4,yoyo:true,repeat:3}},{t_ich:.3f});')
pop("#sa-q", t_zumindest + 0.3, 0.3, 0.5)
for k in range(3):
    tw(f'tl.to("#sa-sm{k}",{{y:-50,x:20,duration:2.5,yoyo:true,repeat:1,ease:"sine.inOut"}},{k*0.3:.3f});')

# B Wiese von oben (Skill 6a: neuer Ort → Überblick)
S0, S1 = t_es, t_ringsum


def aerial():
    out = f'<rect x="-600" y="-600" width="2280" height="3120" fill="{GRASS}"/>'
    out += "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}" opacity=".5"/>' for x, y, rx, ry, c in ((200, 400, 260, 160, "#7cc46f"), (850, 1500, 300, 180, "#7cc46f"), (300, 1600, 200, 120, "#c9e07a"), (900, 300, 200, 140, "#c9e07a")))
    out += f'<rect x="-600" y="920" width="2280" height="120" fill="{ROAD}"/><rect x="480" y="-600" width="120" height="3120" fill="{ROAD}"/>'
    out += "".join(f'<rect x="{x}" y="976" width="60" height="8" fill="#f6efe2"/>' for x in range(-600, 1700, 120)) + "".join(f'<rect x="536" y="{y}" width="8" height="60" fill="#f6efe2"/>' for y in range(-600, 2600, 120))
    out += f'<rect x="680" y="700" width="120" height="120" fill="#6fbb66"/><rect x="690" y="710" width="100" height="90" fill="{ROOFC}"/><line x1="690" y1="755" x2="790" y2="755" stroke="{ROOFC2}" stroke-width="6"/><rect x="770" y="714" width="16" height="22" fill="#8a5a42"/>'
    out += f'<path d="M 740 820 L 740 920" stroke="#e2d2b0" stroke-width="20"/>'
    out += f'<ellipse cx="260" cy="1360" rx="200" ry="130" fill="{WATER}"/><ellipse cx="240" cy="1340" rx="120" ry="60" fill="#8fd0f0" opacity=".6"/>'
    out += "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#3f8f4a"/><circle cx="{x-8}" cy="{y-8}" r="{r*0.6}" fill="#5aa85a"/>' for x, y, r in ((120, 700, 50), (200, 760, 40), (380, 1250, 44), (900, 1200, 56), (980, 1280, 44), (880, 400, 48), (150, 1700, 52), (700, 1650, 40), (960, 760, 42)))
    out += flowers(300, 500, 20, 9) + flowers(820, 1350, 20, 10) + flowers(600, 1500, 14, 11)
    return out


scene("sb", S0, S1, aerial() + label("sb-l", 540, 380, "DIE GROSSE WIESE", "#1a1f2e", 44, fill="#fff4dc"))
tw(f'tl.fromTo("#sb-cam",{{scale:1.0,rotation:-4,svgOrigin:"740 700"}},{{scale:1.35,rotation:0,svgOrigin:"740 700",duration:{S1-S0+0.3:.3f},ease:"sine.inOut"}},{S0:.3f});')
pop("#sb-l", S0 + 0.2)

# C Straßen, Bäume, See
S0, S1 = t_ringsum, (t_innen if HAS_INNEN else t_matr - 0.2)
ducks = "".join(f'<g id="sc-duck{i}"><ellipse cx="{180+i*70}" cy="{1590+i%2*16}" rx="22" ry="12" fill="#fff"/><circle cx="{196+i*70}" cy="{1576+i%2*16}" r="9" fill="#fff"/><polygon points="{204+i*70},{1576+i%2*16} {214+i*70},{1580+i%2*16} {204+i*70},{1582+i%2*16}" fill="#ffb02e"/></g>' for i in range(3))
scene("sc", S0, S1, sky_sunset() + f'<rect x="0" y="1000" width="1080" height="920" fill="{GRASS}"/>'
      + f'<path d="M 724 1146 L 704 1236 L 768 1236 L 748 1146 Z" fill="#e2d2b0"/>'
      + f'<g transform="translate(560,470) scale(.4)">{cottage("scx")}</g>'
      + tree(120, 1040, .6) + tree(980, 1060, .7) + tree(860, 1040, .5)
      + f'<path d="M -50 1220 Q 540 1160 1130 1240 L 1130 1330 Q 540 1250 -50 1310 Z" fill="{ROAD}"/>'
      + "".join(f'<rect x="{x}" y="{1262 - abs(540-x)*0.02:.0f}" width="50" height="8" fill="#f6efe2"/>' for x in range(0, 1080, 110))
      + lantern(240, 1220) + lantern(470, 1218)
      + f'<ellipse cx="300" cy="1620" rx="300" ry="120" fill="{WATER}"/><ellipse cx="280" cy="1600" rx="180" ry="50" fill="#8fd0f0" opacity=".6"/>' + ducks
      + tree(900, 1800, 1.3) + flowers(700, 1700, 14, 12)
      + label("sc-l1", 540, 1400, "STRASSEN", "#1a1f2e", 36, fill="#fff4dc") + label("sc-l2", 900, 820, "BÄUME", "#1a1f2e", 36, fill="#fff4dc") + label("sc-l3", 300, 1480, "SEE", "#1a1f2e", 36, fill="#fff4dc"))
pop("#sc-l1", t_strassen); pop("#sc-l2", t_baeume); pop("#sc-l3", t_see)
for i in range(3):
    tw(f'tl.to("#sc-duck{i}",{{x:{60+i*10},duration:{S1-S0:.3f},ease:"sine.inOut"}},{S0:.3f});')

if HAS_INNEN:
    SCENES_C_END = t_innen
    S0, S1 = t_innen, t_matr - 0.2
    scene("sd", S0, S1, sky_sunset() + meadow("sd") + cottage("sd", cutaway=True)
          + label("sd-l", 540, 360, "1 ZIMMER", "#1a1f2e", 50, fill="#fff4dc"))
    pop("#sd-l", ws("einziges", t_innen))
    tw(f'tl.fromTo("#sd-cam",{{scale:1,svgOrigin:"540 1400"}},{{scale:1.12,svgOrigin:"540 1400",duration:{S1-S0+0.3:.3f},ease:"sine.inOut"}},{S0:.3f});')

# E Mein Zimmer: Matratze, Lampe, Fenster – mehr nicht
S0, S1 = t_matr - 0.2, t_aber
x3, y3 = room_xy(8)
scene("se", S0, S1, f'<rect width="1080" height="1920" fill="#2a2030"/><g transform="translate({540-(x3+RW/2)*4},{1000-(y3+RH/2)*4}) scale(4)">{room_inner(8, "mine", "se")}</g>'
      + figure("se-me", 760, 1560, 1.0, eyes="n") + label("se-l", 540, 360, "MEHR NICHT.", "#fff4dc", 50, fill="#1a1f2e"))
for sel, t in (("#se-mat", t_matr), ("#se-lamp", t_lampe)):
    tw(f'tl.fromTo("{sel}",{{opacity:0,y:-14}},{{opacity:1,y:0,duration:.5,ease:"power2.out"}},{t:.3f});')
tw(f'tl.fromTo("#se-win",{{opacity:.25}},{{opacity:1,duration:.6,ease:"sine.inOut"}},{t_fenster1:.3f});')
pop("#se-l", t_mehr)

# F Nacht: leere Wiese – so viel Platz (Geister-Zimmer als Vorausdeutung)
S0, S1 = t_aber, t_also1
ghosts = "".join(f'<g id="sf-g{i}" opacity="0"><rect x="{gx}" y="{gy}" width="200" height="160" rx="10" fill="#cfe0ff" fill-opacity=".06" stroke="#cfe0ff" stroke-width="5" stroke-dasharray="18 12"/>'
                 f'<rect x="{gx+60}" y="{gy+40}" width="80" height="80" rx="4" fill="#0b1030" stroke="#cfe0ff" stroke-width="4"/></g>'
                 for i, (gx, gy) in enumerate(((60, 1500), (820, 1500), (60, 1340), (820, 1340))))
scene("sf", S0, S1, sky_night() + f'<g opacity=".6">{meadow("sf")}</g>' + cottage("sf", night=True) + ghosts
      + f'<rect width="1080" height="1920" fill="#0a0f2a" opacity=".2"/>')
for i in range(4):
    tw(f'tl.fromTo("#sf-g{i}",{{opacity:0}},{{opacity:.85,duration:.4,ease:"sine.out"}},{t_dunklen + i*0.15:.3f});')
tw(f'tl.to("#sf-g0, #sf-g1, #sf-g2, #sf-g3",{{opacity:.4,duration:.3,yoyo:true,repeat:3,ease:"sine.inOut"}},{t_platz:.3f});')
tw(f'tl.to("#sf-cam",{{scale:1.08,svgOrigin:"540 1400",duration:{S1-S0:.3f},ease:"sine.inOut"}},{S0:.3f});')


# G Regel – laut und deutlich
def card(extra=""):
    return f'<rect width="1080" height="1920" fill="#16213a"/><circle cx="540" cy="900" r="600" fill="url(#cardglow)"/>{extra}'


S0, S1 = t_also1, t_jeder
mega = (f'<g id="sg-mega" opacity="0"><path d="M 380 900 L 620 780 L 620 1100 L 380 980 Z" fill="{GOLD}"/><rect x="330" y="880" width="60" height="120" rx="12" fill="{GOLD}"/>'
        + "".join(f'<path id="sg-w{i}" d="M {660+i*50} {860-i*30} q {40+i*10} {80+i*30} 0 {160+i*60}" stroke="#fff" stroke-width="10" fill="none" opacity="0"/>' for i in range(3)) + '</g>')
scene("sg", S0, S1, card(mega) + f'<g id="sg-b" opacity="0"><rect x="400" y="380" width="280" height="64" rx="14" fill="{RED}"/><text x="540" y="425" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="34" fill="#fff">DIE REGEL</text></g>'
      + f'<g id="sg-t" opacity="0"><text x="540" y="1380" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="76" fill="#fff">LAUT &amp; DEUTLICH</text></g>')
pop("#sg-b", t_regel); pop("#sg-mega", t_regel + 0.2, 0.35, 0.6); pop("#sg-t", t_laut)
for i in range(3):
    tw(f'tl.fromTo("#sg-w{i}",{{opacity:0}},{{opacity:1,duration:.2,yoyo:true,repeat:3}},{t_laut + i*0.12:.3f});')

# H Kommentar = dein Zimmer
S0, S1 = t_jeder, t_gaming
bubble = (f'<g id="sh-bub"><rect x="150" y="560" width="780" height="200" rx="40" fill="#fff"/><polygon points="250,760 330,760 260,830" fill="#fff"/>'
          f'<circle cx="230" cy="660" r="44" fill="#ffd166"/><text x="300" y="640" font-family="Poppins" font-weight="700" font-size="32" fill="#555">@dein.name</text>'
          f'<text x="300" y="700" font-family="Poppins" font-weight="600" font-size="38" fill="#1a1f2e">Ich will ein Zimmer mit …</text></g>')
scene("sh", S0, S1, card(bubble) + f'<g transform="translate(540,1300) scale(.7) translate(-540,-1420)">{cottage("shc")}'
      f'<g id="sh-new"><g id="sh-nw"><rect x="{CX0+CW}" y="{CY0+180}" width="240" height="300" fill="{WALLC}" stroke="{WOODC}" stroke-width="10"/>'
      f'<rect id="sh-nwin" x="{CX0+CW+70}" y="{CY0+260}" width="100" height="120" rx="6" fill="#9fb4cc" stroke="#fff" stroke-width="8"/></g>'
      f'<polygon id="sh-nr" points="{CX0+CW-10},{CY0+180} {CX0+CW+120},{CY0+60} {CX0+CW+250},{CY0+180}" fill="{ROOFC}"/>'
      + "".join(f'<ellipse id="sh-d{k}" cx="{CX0+CW+40+k*80}" cy="{CY0+CH}" rx="50" ry="22" fill="#e9dcc4" opacity="0"/>' for k in range(3)) + '</g></g>'
      + label("sh-l", 540, 380, "KOMMENTAR = DEIN ZIMMER", GOLD, 44, fill="#1a1f2e")
      + label("sh-l2", 540, 1780, "GENAU SO, WIE DU WILLST", "#fff", 40, fill="#1a1f2e"))
pop("#sh-l", S0 + 0.1)
tw(f'tl.fromTo("#sh-bub",{{opacity:0,y:60}},{{opacity:1,y:0,duration:.4,ease:"back.out(1.6)"}},{t_komm1 - 0.6:.3f});')
tw(f'tl.to("#sh-bub",{{scale:.25,x:260,y:700,svgOrigin:"540 660",duration:.6,ease:"power2.in"}},{t_komm1 + 0.5:.3f});')
tw(f'tl.to("#sh-bub",{{opacity:0,duration:.2}},{t_komm1 + 1.1:.3f});')
tb = t_komm1 + 1.1
tw(f'tl.set("#sh-nw",{{scaleY:0,transformOrigin:"50% 100%"}},{S0:.3f});')
tw(f'tl.set("#sh-nr",{{opacity:0}},{S0:.3f});')
tw(f'tl.fromTo("#sh-nw",{{scaleY:0,transformOrigin:"50% 100%"}},{{scaleY:1,duration:.7,ease:"power2.out"}},{tb:.3f});')
tw(f'tl.fromTo("#sh-nr",{{opacity:0,y:-90}},{{opacity:1,y:0,duration:.5,ease:"power2.inOut"}},{tb + 0.65:.3f});')
tw(f'tl.to("#sh-nwin",{{attr:{{fill:"{GLOWC}"}},duration:.3}},{tb + 1.2:.3f});')
for k in range(3):
    tw(f'tl.fromTo("#sh-d{k}",{{opacity:0,scale:.4,transformOrigin:"50% 50%"}},{{opacity:.8,scale:1.4,duration:.4,ease:"power1.out"}},{tb + k*0.08:.3f});')
    tw(f'tl.to("#sh-d{k}",{{opacity:0,duration:.6}},{tb + 0.45 + k*0.08:.3f});')
pop("#sh-l2", t_genau)


# I/J/K Wunschzimmer: Gaming, Pflanzen, Sternenbett – „Ich baue es“
def wish_scene(sid, t0, t1, idx, kind, name, t_stamp, title):
    xi, yi = room_xy(idx)
    scene(sid, t0, t1, f'<rect width="1080" height="1920" fill="#16213a"/><circle cx="540" cy="900" r="600" fill="url(#cardglow)"/>'
          + f'<g transform="translate({540-(xi+RW/2)*3.6},{1000-(yi+RH/2)*3.6}) scale(3.6)">{room_inner(idx, "empty", sid+"e")}<clipPath id="{sid}-clip"><rect id="{sid}-cr" x="{xi}" y="{yi+RH}" width="{RW}" height="0"/></clipPath><g clip-path="url(#{sid}-clip)">{room_inner(idx, kind, sid, name)}</g>'
          + f'<rect id="{sid}-line" x="{xi}" y="{yi+RH-3}" width="{RW}" height="3" fill="{GOLD}" opacity="0"/></g>'
          + label(f"{sid}-t", 540, 380, title, "#fff4dc", 48, fill="#1a1f2e")
          + f'<g id="{sid}-st" opacity="0"><rect x="250" y="1520" width="580" height="130" rx="20" fill="{RED}" transform="rotate(-6 540 1585)"/>'
            f'<text x="540" y="1610" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="70" fill="#fff" transform="rotate(-6 540 1585)">ICH BAUE ES!</text></g>')
    pop(f"#{sid}-t", t0 + 0.1)
    tb = t0 + 0.5; db = max(0.6, min(1.2, t_stamp - tb - 0.15))
    tw(f'tl.to("#{sid}-cr",{{attr:{{y:{yi}, height:{RH}}},duration:{db:.3f},ease:"power1.inOut"}},{tb:.3f});')
    tw(f'tl.set("#{sid}-line",{{opacity:.9}},{tb:.3f});')
    tw(f'tl.to("#{sid}-line",{{y:{-RH+3},duration:{db:.3f},ease:"power1.inOut"}},{tb:.3f});')
    tw(f'tl.to("#{sid}-line",{{opacity:0,duration:.15}},{tb + db:.3f});')
    tw(f'tl.set("#{sid}-np{idx}",{{opacity:1}},{t_stamp:.3f});')
    tw(f'tl.fromTo("#{sid}-st",{{opacity:0,scale:2.2,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:.22,ease:"power4.in"}},{t_stamp:.3f});')
    shake(f"#{sid}-cam", t_stamp + 0.22, 4, 6)


wish_scene("si", t_gaming, t_pflanzen, 0, "gaming", NAMES[3], t_baue1 - 0.1, "GAMING-ZIMMER")
wish_scene("sj", t_pflanzen, t_bett, 5, "plants", NAMES[0], t_baue2 - 0.1, "PFLANZEN-ZIMMER")
wish_scene("sk", t_bett, t_jeder2, 1, "stars", NAMES[10], t_baue3 - 0.1, "STERNEN-ZIMMER")

# L Jeder Kommentar ein Zimmer – Name an der Tür
S0, S1 = t_jeder2, t_wenn
kinds = {8: "mine", 3: "gaming", 0: "gaming", 5: "plants", 1: "stars", 2: "plants", 4: "gaming", 6: "stars", 7: "plants", 9: "stars", 10: "plants", 11: "gaming"}
nm = {i: NAMES[i % len(NAMES)] for i in range(12) if i != 8}
door = (f'<g id="sl-door" opacity="0"><rect width="1080" height="1920" fill="#16213a"/><rect x="320" y="520" width="440" height="900" rx="20" fill="{WOODC}"/>'
        f'<rect x="350" y="560" width="380" height="380" rx="12" fill="none" stroke="#5a3a24" stroke-width="10"/><circle cx="700" cy="1000" r="20" fill="{GOLD}"/>'
        f'<rect x="380" y="640" width="320" height="90" rx="12" fill="#fff4dc" stroke="{GOLD}" stroke-width="6"/>'
        f'<text x="540" y="700" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="44" fill="#3a2a1a">@DEIN.NAME</text></g>')
sl_dust = "".join(f'<ellipse id="sl-d{r}-{k}" cx="{HX+40+k*150}" cy="{HY+(r+1)*RH}" rx="70" ry="26" fill="#e9dcc4" opacity="0"/>' for r in range(3) for k in range(6))
scene("sl", S0, S1, sky_sunset() + meadow("sl") + house_cut("sl", kinds, nm) + sl_dust + door)
tw(f'tl.set("#sl-house > polygon, #sl-house > line, #sl-house > rect",{{opacity:1}},{S0:.3f});')
rows = [[9, 10, 11], [4, 5, 6, 7], [0, 1, 2, 3]]
tw(f'tl.set("#sl-r9, #sl-r10, #sl-r11, #sl-r4, #sl-r5, #sl-r6, #sl-r7, #sl-r0, #sl-r1, #sl-r2, #sl-r3",{{scaleY:0,transformOrigin:"50% 100%"}},{S0:.3f});')
tw(f'tl.set("#sl-roof",{{opacity:0}},{S0:.3f});')
span = max(1.0, t_namen - 0.35 - S0)
rd = span / 3.4
for r, row in enumerate(rows):
    tr = S0 + 0.05 + r * rd
    for k, i in enumerate(row):
        tw(f'tl.fromTo("#sl-r{i}",{{scaleY:0,transformOrigin:"50% 100%"}},{{scaleY:1,duration:{rd*0.95:.3f},ease:"power2.out"}},{tr + k*0.04:.3f});')
        tw(f'tl.fromTo("#sl-np{i}",{{opacity:0}},{{opacity:1,duration:.15}},{tr + rd*0.8:.3f});')
    for k in range(6):
        tw(f'tl.fromTo("#sl-d{2-r}-{k}",{{opacity:0,scale:.4,transformOrigin:"50% 50%"}},{{opacity:.75,scale:1.3,duration:{rd*0.6:.3f},ease:"power1.out"}},{tr:.3f});')
        tw(f'tl.to("#sl-d{2-r}-{k}",{{opacity:0,duration:.4}},{tr + rd*0.6:.3f});')
tw(f'tl.fromTo("#sl-roof",{{opacity:0,y:-160}},{{opacity:1,y:0,duration:{rd*0.9:.3f},ease:"power2.inOut"}},{S0 + 0.05 + 3*rd - 0.1:.3f});')
tw(f'tl.fromTo("#sl-door",{{opacity:0,scale:.8,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:.35,ease:"power3.out"}},{t_namen - 0.1:.3f});')

# M Neues Stockwerk wird aufgesetzt
S0, S1 = t_wenn, t_heute
scene("sm", S0, S1, sky_sunset() + meadow("sm") + f'<g transform="translate(0,200)">{house_cut("sm", kinds, nm, extra_floor=True)}</g>'
      + f'<g id="sm-crane"><rect x="1000" y="0" width="20" height="1700" fill="#e9c46a"/>'
        + "".join(f'<line x1="1000" y1="{k*80}" x2="1020" y2="{k*80+80}" stroke="#b8963e" stroke-width="4"/>' for k in range(21))
        + f'<rect x="440" y="0" width="600" height="22" fill="#e9c46a"/><rect x="520" y="18" width="40" height="24" fill="#555"/></g>'
      + f'<g transform="translate(0,200)"><g id="sm-oroof"><line x1="540" y1="-1500" x2="540" y2="{HY-300}" stroke="#333" stroke-width="4"/><circle cx="540" cy="{HY-300}" r="10" fill="none" stroke="#333" stroke-width="5"/>'
        + f'<polygon points="{HX-50},{HY} {HX+2*RW},{HY-300} {HX+4*RW+50},{HY}" fill="{ROOFC}"/>'
        + "".join(f'<line x1="{HX-30+k*60}" y1="{HY}" x2="{HX+2*RW}" y2="{HY-290}" stroke="{ROOFC2}" stroke-width="4"/>' for k in range(17)) + '</g>'
        + f'<g id="sm-cable"><line x1="540" y1="-1500" x2="540" y2="{HY-RH-300}" stroke="#333" stroke-width="4"/><circle cx="540" cy="{HY-RH-300}" r="10" fill="none" stroke="#333" stroke-width="5"/></g>'
        + "".join(f'<ellipse id="sm-d{k}" cx="{HX+40+k*150}" cy="{HY}" rx="70" ry="24" fill="#e9dcc4" opacity="0"/>' for k in range(6)) + '</g>'
      + label("sm-l", 540, 220, "+1 STOCKWERK", GOLD, 50, fill="#1a1f2e"))
for i in range(12):
    tw(f'tl.set("#sm-np{i}",{{opacity:1}},{S0:.3f});')
t_lift = S0 + 0.1
tw(f'tl.set("#sm-ef, #sm-cable",{{y:-1100}},{S0:.3f});')
tw(f'tl.to("#sm-oroof",{{y:-1100,duration:1.1,ease:"power2.in"}},{t_lift:.3f});')
t_low = max(t_lift + 0.9, t_stock - 0.6); d_low = max(1.0, min(1.8, S1 - 0.6 - t_low))
for sel in ("#sm-ef", "#sm-cable"):
    tw(f'tl.fromTo("{sel}",{{y:-1100}},{{y:0,duration:{d_low:.3f},ease:"power2.out"}},{t_low:.3f});')
tw(f'tl.fromTo("#sm-ef",{{rotation:-1.2,svgOrigin:"540 {HY-RH-300}"}},{{rotation:0,svgOrigin:"540 {HY-RH-300}",duration:{d_low:.3f},ease:"sine.out"}},{t_low:.3f});')
t_land = t_low + d_low
tw(f'tl.to("#sm-cable",{{y:-1200,duration:.8,ease:"power2.in"}},{t_land + 0.1:.3f});')
for k in range(6):
    tw(f'tl.fromTo("#sm-d{k}",{{opacity:0,scale:.4,transformOrigin:"50% 50%"}},{{opacity:.8,scale:1.4,duration:.35,ease:"power1.out"}},{t_land - 0.05:.3f});')
    tw(f'tl.to("#sm-d{k}",{{opacity:0,duration:.5}},{t_land + 0.3:.3f});')
pop("#sm-l", t_stock)
shake("#sm-cam", t_land - 0.02, 3, 3)

# N Heute 1 – morgen vielleicht hundert
S0, S1 = t_heute, t_also2
COUNTS = ["1", "1", "7", "23", "48", "100"]
scene("sn", S0, S1, sky_night() + f'<g opacity=".6">{meadow("sn")}</g>' + house_ext("sn", set(), night=True)
      + f'<g><rect x="390" y="140" width="300" height="50" rx="25" fill="#1a1f2e" fill-opacity=".85"/><text x="540" y="174" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="26" fill="#fff" letter-spacing="4">BEWOHNER</text></g>'
      + "".join(f'<text id="sn-c{i}" x="540" y="330" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="130" fill="{GOLD}" stroke="#1a1f2e" stroke-width="12" paint-order="stroke" opacity="0">{c}</text>' for i, c in enumerate(COUNTS)))
tw(f'tl.set("#sn-w8 rect:first-child",{{attr:{{fill:"{GLOWC}"}}}},{S0:.3f});')
toggle("#sn-c0", S0, t_morgen)
steps = len(COUNTS) - 1
for i in range(1, len(COUNTS)):
    a = t_morgen + (t_hundert + 0.4 - t_morgen) * (i - 1) / steps
    toggle(f"#sn-c{i}", a, t_morgen + (t_hundert + 0.4 - t_morgen) * i / steps if i < len(COUNTS) - 1 else None)
lit_order = [8, 9, 10, 11, 4, 5, 6, 7, 0, 1, 2, 3]
for k, i in enumerate(lit_order):
    tw(f'tl.to("#sn-w{i} rect:first-child",{{attr:{{fill:"{GLOWC}"}},duration:.15}},{t_morgen + k*0.12:.3f});')

# O Ende: Wie sieht dein Zimmer aus?
S0, S1 = t_also2, TOTAL
scene("so", S0, S1, sky_sunset() + meadow("so") + house_ext("so", set(range(12)))
      + pill("so-p", 540, 330, "💬  DEIN WUNSCHZIMMER?", GOLD, "#1a1f2e", 50))
pop("#so-p", t_wie, 0.35, 0.6)
tw(f'tl.fromTo("#so-p",{{scale:1}},{{scale:1.08,transformOrigin:"50% 50%",duration:.3,yoyo:true,repeat:3}},{t_schreib:.3f});')
for i in range(3):
    tw(f'tl.to("#bird{i}",{{x:200,y:-30,duration:4,ease:"sine.inOut"}},0);')
for k in range(12):
    tw(f'tl.to("#so-w{k}",{{opacity:.7,duration:.4,yoyo:true,repeat:5,ease:"sine.inOut"}},{VO_END + 0.2 + (k%4)*0.15:.3f});')
OUT_NAMES = "".join(f'<g id="so-n{k}" opacity="0"><rect x="{nx-90}" y="{ny-30}" width="180" height="44" rx="10" fill="#fff4dc" stroke="{WOODC}" stroke-width="4"/>'
                    f'<text x="{nx}" y="{ny}" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="22" fill="#3a2a1a">{NAMES[k]}</text></g>'
                    for k, (nx, ny) in enumerate(((180, 520), (900, 560), (200, 1720), (880, 1760), (540, 480))))
SCENES[-1] = (SCENES[-1][0], SCENES[-1][1], SCENES[-1][2], SCENES[-1][3].replace("</g>", "", 0) + OUT_NAMES)
for k in range(5):
    tw(f'tl.fromTo("#so-n{k}",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.4,ease:"back.out(1.6)"}},{VO_END + 0.4 + k*0.4:.3f});')
tw(f'tl.to("#so-p",{{scale:1.08,transformOrigin:"50% 50%",duration:.35,yoyo:true,repeat:{int((TOTAL-VO_END)/0.35)}}},{VO_END:.3f});')

brand_html = []

# ================= UNTERTITEL (Skill 7, Format A: Akzent Rot) =================
KEY = {"EINZIGE", "ICH", "NOCH", "WIESE", "STRASSEN", "BÄUME", "SEE", "ZWÖLF", "ELF", "LEER", "OBEN", "MATRATZE", "LAMPE", "FENSTER",
       "DUNKLEN", "PLATZ", "REGEL", "LAUT", "DEUTLICH", "EIGENES", "KOMMENTARE", "WÜNSCHT", "BILDSCHIRMEN", "PFLANZEN", "STERNE",
       "BAUE", "KOMMENTAR", "NAMEN", "TÜR", "STOCKWERK", "HUNDERT", "ZIMMER"}
DISPLAY = {"Zwölf": "12", "Elf": "11", "hundert.": "100."}
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
<linearGradient id="dawn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b2f6b"/><stop offset=".45" stop-color="#c85a7a"/><stop offset=".8" stop-color="#ffb36b"/></linearGradient>
<linearGradient id="dusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a1430"/><stop offset=".6" stop-color="#5a2a3a"/><stop offset="1" stop-color="#a8432f"/></linearGradient>
<radialGradient id="sunglow"><stop offset="0" stop-color="#ffd27a" stop-opacity=".6"/><stop offset="1" stop-color="#ffd27a" stop-opacity="0"/></radialGradient>
<radialGradient id="fireglow"><stop offset="0" stop-color="#ffb22e" stop-opacity=".55"/><stop offset="1" stop-color="#ffb22e" stop-opacity="0"/></radialGradient>
<linearGradient id="wallshade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".45"/></linearGradient>
<radialGradient id="giantshade" cx=".5" cy=".75" r=".8"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/></radialGradient>
<linearGradient id="underlight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".35"/><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#ff5a1f" stop-opacity=".18"/></linearGradient>
<filter id="emberglow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<linearGradient id="bodyshade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset=".7" stop-color="#000" stop-opacity=".15"/><stop offset="1" stop-color="#000" stop-opacity=".6"/></linearGradient>
<filter id="steamblur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="22"/></filter>
<linearGradient id="sunset" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a6ad0"/><stop offset=".5" stop-color="#f29ab5"/><stop offset=".8" stop-color="#ffcf8a"/></linearGradient>
<linearGradient id="nightsky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b1030"/><stop offset="1" stop-color="#2a2a6a"/></linearGradient>
<radialGradient id="lampglow2"><stop offset="0" stop-color="#ffd98a" stop-opacity=".45"/><stop offset="1" stop-color="#ffd98a" stop-opacity="0"/></radialGradient>
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
    <title>Ein Haus, eine Person</title>
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
