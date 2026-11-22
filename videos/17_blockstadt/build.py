#!/usr/bin/env python3
"""Generator für index.html – Video 13 „HÖHE · Teil 1“ (Skill-Format B „Regel-Serie“).

Alle Zeiten kommen aus assets/words.json (wortgenaue Voiceover-Zeitstempel).
Aufruf: python3 build.py → index.html + assets/cues.json
"""
import json, re, html, os, math, random, zlib, struct, base64

HERE = os.path.dirname(os.path.abspath(__file__))
W = json.load(open(os.path.join(HERE, "assets/words.json"), encoding="utf-8"))
VO_END = W[-1]["e"]
TOTAL = round(VO_END + 0.4, 2)          # Teil-2-Karte steht noch gut 3 s
XF = 0.3                                 # Überblendung zwischen Szenen
RNG = random.Random(9)

# ---------- Farben: Nacht-Palette (Format B) ----------
SKY1 = "#0b0d26"; SKY2 = "#1d1d4f"; VIO = "#2a2360"; BLD = "#141634"; BLD2 = "#1b1d44"
WIN = "#ffd98a"; LAMP = "#ffd98a"; MOON = "#f4e3a1"; STREET = "#191a33"; WALK = "#25264a"
FIG = "#e2a982"; SKIN2 = "#c98a66"; HAIR = "#3a2a20"; LIP = "#a85a4a"; INK = "#151a21"; RED = "#ff3b3b"; LIME = "#c8f031"; BLUE = "#3b6cff"; WHITE = "#ffffff"
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
    # sauberer: nur leichtes Skalieren + weiches Einblenden (Skill 11a „sauberere Animation“)
    tw(f'tl.fromTo("{sel}",{{opacity:0,scale:{max(frm, .94)},transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:{max(dur, .4)},ease:"sine.out"}},{t:.3f});')


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


# ---------- Figuren: feste Hauptfigur „C · Anime mit Senf-Hoodie“ (Skill 6) ----------
import sys as _sys
_sys.path.insert(0, os.path.join(HERE, "../../branding/figur"))
from figur_c import make_figure, DEFS as FIGC_DEFS
FIGS = []
figure = make_figure(FIGS)


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




# ================= CUES =================
t_warte = ws("Warte"); t_schaut2 = ws("schaut", t_warte)
t_weiss = ws("weiß"); t_videos = ws("Videos"); t_keiner = ws("keiner"); t_dich = ws("dich", t_keiner)
t_oma = ws("Oma"); t_zwei = ws("zwei"); t_bett = ws("Bett")
t_baecker = ws("Bäcker"); t_chips = ws("Chips"); t_tuete = ws("Tüte")
t_hm = ws("Hausmeister"); t_schule = ws("Schule"); t_scrollen = ws("scrollen")
t_opa = ws("Opa", t_hm + 0.5); t_leiser = ws("leiser"); t_lina = ws("Lina"); t_wisch = ws("weggewischt"); t_zweimal = ws("Zweimal"); t_geblieben = ws("geblieben")
t_papa = ws("Papa"); t_tafel = ws("Tafel"); t_drei = ws("Drei"); t_acht = ws("Acht"); t_weg2 = ws("weg", t_acht); t_unddu = ws("du", t_weg2); t_immer = ws("Immer")
t_nicht = ws("Nicht", t_immer); t_dreissig = ws("dreißig")
t_daumen = ws("Daumen"); t_fest = ws("festhalten"); t_bleibt = ws("bleibt"); t_jubelt = ws("jubelt")
t_papa2 = ws("Papa", t_bleibt); t_zoom = ws("Zoom"); t_handy = ws("Handy"); t_zimmer = ws("Zimmer"); t_stadt2 = ws("Stadt", t_zimmer)
t_ende = ws("Ende"); t_haus2 = ws("Haus", t_ende); t_namen = ws("Namen"); t_tuer = ws("Tür")
t_schaust = ws("schaust"); t_wohnst = ws("wohnst"); t_und_in = ws("Und", t_wohnst)

# ================= SZENEN (Format C · Block-Stadt) =================
import sys as _s2
_s2.path.insert(0, os.path.join(HERE, "../../branding/roblox"))
from block import block, box, shade
YEL = "#d8f53c"; CYAN = "#5ff0d4"
GR = "#5cc65a"; GR2 = "#4fb34e"; ROADC = "#4a4d57"


def fadein(sel, t, dur=0.35, dy=14):
    tw(f'tl.fromTo("{sel}",{{opacity:0,y:{dy}}},{{opacity:1,y:0,duration:{dur},ease:"sine.out"}},{t:.3f});')


PEOPLE = [  # (shirt, pants, skin, hair, style)
    ("#3b6cff", "#2c3a52", "#e8b08a", "#1e1a2e", "spike"), ("#ff6b6b", "#23252e", "#8d5a3b", "#1a1210", "cap"),
    ("#e98fd0", "#4a6fa5", "#f0c09a", "#6b3a1f", "long"), ("#2a9d8f", "#23252e", "#c68a5e", "#1a1210", "flat"),
    ("#ffd23f", "#3a4a6a", "#f2c7a8", "#c98a3a", "bun"), ("#7a5af5", "#1b1d25", "#e8b896", "#5a3a24", "spike"),
    ("#ffffff", "#2c3a52", "#d9a27a", "#2a1b12", "chef"), ("#ff8a3d", "#23252e", "#e8b08a", "#1e1a2e", "flat")]


def person(i, bid, x, y, s=1.0, mood="n", back=False):
    sh, pa, sk, ha, st = PEOPLE[i % len(PEOPLE)]
    return block(bid, x, y, s, sh, pa, sk, ha, st, mood, back)


def town_bg(prefix):
    sky = (f'<rect width="1080" height="1920" fill="url(#daysky)"/><circle cx="880" cy="300" r="70" fill="#fff4c2"/>'
           + "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="#fff" opacity=".9"/>' for x, y, w, h in ((120, 330, 220, 60), (560, 260, 160, 50), (700, 420, 200, 56))))
    houses = ""
    for k, (x, w, h, c, roof) in enumerate(((-20, 240, 300, "#f4d35e", "#ee6c4d"), (240, 260, 360, "#9bc1ff", "#3d5a80"), (520, 220, 280, "#ffd6e0", "#e56b6f"),
                                              (760, 340, 330, "#b8e0d2", "#2a9d8f"))):
        top = 1000 - h
        houses += (box(x, top, w, h, c, shade(c, .8), shade(c, 1.08))
                   + f'<polygon points="{x-20},{top} {x+w/2},{top-110} {x+w+20},{top}" fill="{roof}"/>'
                   + f'<rect x="{x+w/2-35}" y="{1000-120}" width="70" height="120" fill="#6b4a32"/>'
                   + "".join(f'<rect x="{x+30+j*(w-110)}" y="{top+50}" width="60" height="60" fill="#bfe4ff" stroke="#fff" stroke-width="6"/>' for j in range(2)))
    ground = (f'<rect x="0" y="1000" width="1080" height="920" fill="{GR}"/><rect x="0" y="1000" width="1080" height="70" fill="#d9d4c7"/>'
              f'<rect x="0" y="1150" width="1080" height="220" fill="{ROADC}"/>' + "".join(f'<rect x="{x}" y="1252" width="90" height="16" fill="#ffd23f"/>' for x in range(20, 1080, 180))
              + f'<rect x="0" y="1370" width="1080" height="40" fill="#d9d4c7"/>'
              + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#3f8f4a"/><rect x="{x-8}" y="{y}" width="16" height="70" fill="#6b4a32"/>' for x, y, r in ((60, 930, 50), (1030, 940, 46))))
    return sky + houses + ground


def board_live(bid, x, y, w, t_rows, t_live_from, t_live_to):
    rows = [("0:03", "WEG", RED), ("0:08", "WEG", RED)]
    out = (f'<g id="{bid}"><rect x="{x}" y="{y}" width="{w}" height="560" rx="24" fill="#6b4a32"/><rect x="{x+20}" y="{y+20}" width="{w-40}" height="520" rx="16" fill="#0b0d22"/>'
           + "".join(f'<circle cx="{x+14+k*((w-28)/14):.0f}" cy="{y+10}" r="8" fill="#fff4c2"/><circle cx="{x+14+k*((w-28)/14):.0f}" cy="{y+550}" r="8" fill="#fff4c2"/>' for k in range(15))
           + "".join(f'<circle cx="{x+10}" cy="{y+40+k*48}" r="8" fill="#fff4c2"/><circle cx="{x+w-10}" cy="{y+40+k*48}" r="8" fill="#fff4c2"/>' for k in range(10))
           + f'<text x="{x+w/2}" y="{y+90}" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="46" fill="#ffd23f">ZUSCHAUER JETZT</text>')
    for k, (tm, st, col) in enumerate(rows):
        yy = y + 170 + k * 120
        out += (f'<g id="{bid}-r{k}" opacity="0"><rect x="{x+60}" y="{yy-50}" width="70" height="70" rx="10" fill="#ffd23f"/>'
                f'<path d="M {x+60} {yy-50} l 70 70 M {x+130} {yy-50} l -70 70" stroke="{RED}" stroke-width="12"/>'
                f'<text x="{x+170}" y="{yy+5}" font-family="JetBrains Mono" font-weight="800" font-size="58" fill="{col}">{tm} {st}</text></g>')
    yy = y + 170 + 2 * 120
    out += (f'<g id="{bid}-r2" opacity="0"><rect x="{x+60}" y="{yy-50}" width="70" height="70" rx="10" fill="#7fb0ff"/>'
            f'<circle cx="{x+82}" cy="{yy-22}" r="6" fill="#111"/><circle cx="{x+108}" cy="{yy-22}" r="6" fill="#111"/>'
            f'<text x="{x+170}" y="{yy+5}" font-family="Poppins" font-weight="800" font-size="58" fill="{CYAN}">DU</text>')
    for sec in range(int(t_live_from), int(t_live_to) + 2):
        out += f'<text id="{bid}-s{sec}" x="{x+290}" y="{yy+5}" font-family="JetBrains Mono" font-weight="800" font-size="58" fill="{CYAN}" opacity="0">0:{sec:02d}</text>'
    out += '</g></g>'
    for sec in range(int(t_live_from), int(t_live_to) + 2):
        tw(f'tl.set("#{bid}-s{sec}",{{opacity:1}},{max(sec, t_live_from):.3f});')
        tw(f'tl.set("#{bid}-s{sec}",{{opacity:0}},{sec + 1:.3f});')
    for k, tr in enumerate(t_rows):
        tw(f'tl.fromTo("#{bid}-r{k}",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:.3,ease:"power2.out"}},{tr:.3f});')
    return out


# A Hook: Straße voller Block-Bewohner – alle schauen zu
S0, S1 = 0.0, t_weiss
crowd = "".join(person(i, f"sa-p{i}", x, y, s, "n") for i, (x, y, s) in enumerate(((150, 1150, .9), (380, 1160, .95), (620, 1150, .9), (870, 1160, .95), (260, 1400, 1.15), (760, 1400, 1.15))))
scene("sa", S0, S1, town_bg("sa") + crowd, drift=False)
for i in range(6):
    tw(f'tl.to("#sa-p{i} .bf",{{opacity:0,duration:.05}},{t_warte:.3f});')
tw(f'tl.fromTo("#sa-cam",{{scale:1,svgOrigin:"540 1200"}},{{scale:1.12,svgOrigin:"540 1200",duration:{S1-S0+0.3:.3f},ease:"sine.inOut"}},{S0:.3f});')
tw(f'tl.to("#sa-cam",{{scale:1.6,svgOrigin:"760 1100",duration:.5,ease:"power2.inOut"}},{t_schaut2 - 0.2:.3f});')
shocked = "".join(person(i, f"sa-q{i}", x, y, s, "shock") for i, (x, y, s) in enumerate(((150, 1150, .9), (380, 1160, .95), (620, 1150, .9), (870, 1160, .95), (260, 1400, 1.15), (760, 1400, 1.15))))
SCENES[-1] = (SCENES[-1][0], SCENES[-1][1], SCENES[-1][2], SCENES[-1][3][:-4] + f'<g id="sa-shock" opacity="0">{shocked}</g></g>')
tw(f'tl.set("#sa-shock",{{opacity:1}},{t_warte:.3f});')


# B Draufsicht: Bewohner-Kreis um den Zuschauer
def top_person(i, cx, cy, ang, mood="n"):
    sh, pa, sk, ha, st = PEOPLE[i % len(PEOPLE)]
    import math as _m
    deg = _m.degrees(ang) + 90
    return (f'<g transform="translate({cx:.0f},{cy:.0f}) rotate({deg:.0f})">'
            f'<rect x="-75" y="-10" width="150" height="80" rx="8" fill="{sh}"/><rect x="-105" y="0" width="34" height="60" rx="8" fill="{shade(sh,.8)}"/><rect x="71" y="0" width="34" height="60" rx="8" fill="{shade(sh,.8)}"/>'
            f'<rect x="-48" y="-92" width="96" height="92" rx="6" fill="{sk}"/><rect x="-48" y="-92" width="96" height="22" fill="{ha}"/>'
            f'<ellipse cx="-20" cy="-50" rx="9" ry="11" fill="#111"/><ellipse cx="20" cy="-50" rx="9" ry="11" fill="#111"/>'
            + (f'<ellipse cx="0" cy="-22" rx="10" ry="12" fill="#111"/>' if mood == "shock" else f'<path d="M -14 -24 Q 0 -14 14 -24" stroke="#111" stroke-width="5" fill="none"/>') + '</g>')


import math as _m
S0, S1 = t_weiss, t_oma
ring = "".join(top_person(i, 540 + 330 * _m.cos(2*_m.pi*i/14), 960 + 330 * _m.sin(2*_m.pi*i/14), 2*_m.pi*i/14 + _m.pi) for i in range(14))
topbg = (f'<rect width="1080" height="1920" fill="{GR}"/><rect x="340" y="0" width="400" height="1920" fill="{ROADC}"/>'
         + "".join(f'<rect x="530" y="{y}" width="20" height="90" fill="#ffd23f"/>' for y in range(0, 1920, 180))
         + f'<rect x="300" y="0" width="40" height="1920" fill="#d9d4c7"/><rect x="740" y="0" width="40" height="1920" fill="#d9d4c7"/>'
         + "".join(f'<circle cx="{x}" cy="{y}" r="60" fill="#3f8f4a"/><circle cx="{x-15}" cy="{y-15}" r="30" fill="#5aa85a"/>' for x, y in ((120, 300), (960, 420), (130, 1600), (950, 1500))))
center = (f'<g id="sb-c" opacity="0"><circle cx="540" cy="960" r="90" fill="none" stroke="{CYAN}" stroke-width="10" stroke-dasharray="20 14"/>'
          f'<text x="540" y="985" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="70" fill="{CYAN}">DU</text></g>')
scene("sb", S0, S1, topbg + ring + center, drift=False)
tw(f'tl.fromTo("#sb-cam",{{rotation:0,svgOrigin:"540 960",scale:1}},{{rotation:25,svgOrigin:"540 960",scale:1.12,duration:{S1-S0+0.3:.3f},ease:"sine.inOut"}},{S0:.3f});')
pop("#sb-c", t_dich, 0.4, 0.6)
tw(f'tl.to("#sb-c",{{scale:1.12,transformOrigin:"50% 50%",duration:.35,yoyo:true,repeat:5,ease:"sine.inOut"}},{t_dich + 0.4:.3f});')


# C Ertappt-Momente: Oma Hilde, Bäcker Ben, Hausmeister Kurt, Lina
def callout(sid, t0, t1, pi, name, icon, mood="shock", sky=True):
    bg = (f'<rect width="1080" height="1920" fill="url(#daysky)"/><rect x="0" y="1150" width="1080" height="770" fill="{GR}"/>' if sky else
          f'<rect width="1080" height="1920" fill="#14163a"/>')
    scene(sid, t0, t1, bg + person(pi, f"{sid}-p", 420, 1900, 2.4, mood)
          + f'<g id="{sid}-i" opacity="0">{icon}</g>' + label(f"{sid}-n", 760, 380, name, "#0b0d22", 46, fill="#ffffff"), drift=False)
    pop(f"#{sid}-n", t0 + 0.1, 0.3, 0.8)
    tw(f'tl.fromTo("#{sid}-cam",{{scale:1.08,svgOrigin:"420 1100"}},{{scale:1,svgOrigin:"420 1100",duration:{t1-t0+0.3:.3f},ease:"sine.out"}},{t0:.3f});')


PEOPLE[4] = ("#9b6bd6", "#3a4a6a", "#f2c7a8", "#d9d4cf", "bun")     # Oma Hilde: graue Haare
icon_oma = (f'<rect x="640" y="520" width="380" height="300" rx="24" fill="#0b0d22" stroke="#7a8aff" stroke-width="6"/>'
            f'<circle cx="720" cy="590" r="34" fill="#f4e3a1"/><circle cx="736" cy="580" r="30" fill="#0b0d22"/>'
            f'<text x="880" y="610" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="64" fill="{RED}">2:00</text>'
            f'<rect x="680" y="690" width="300" height="70" rx="14" fill="#3b6cff"/><rect x="680" y="660" width="90" height="50" rx="14" fill="#fff"/><rect x="900" y="640" width="50" height="80" rx="8" fill="#bfe4ff"/>')
callout("sc1", t_oma, t_baecker, 4, "OMA HILDE", icon_oma)
tw(f'tl.fromTo("#sc1-i",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.4,ease:"power2.out"}},{t_zwei - 0.2:.3f});')
icon_chips = (f'<g transform="rotate(10 830 680)"><path d="M 720 540 L 940 540 L 960 820 L 700 820 Z" fill="#ffd23f"/><rect x="700" y="530" width="260" height="30" fill="#ff8a3d"/>'
              f'<text x="830" y="700" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="56" fill="{RED}">CHIPS</text></g>'
              + "".join(f'<ellipse cx="{cx}" cy="{cy}" rx="26" ry="16" fill="#f4c35e"/>' for cx, cy in ((660, 880), (720, 930), (600, 950))))
callout("sc2", t_baecker, t_hm, 6, "BÄCKER BEN", icon_chips)
tw(f'tl.fromTo("#sc2-i",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.4,ease:"power2.out"}},{t_chips - 0.2:.3f});')
PEOPLE[1] = ("#3b6cff", "#2c3a52", "#8d5a3b", "#2f57d4", "cap")      # Hausmeister Kurt: blaue Latzhose + Kappe
icon_desk = (f'<rect x="620" y="700" width="420" height="40" fill="#b07a4a"/><rect x="640" y="740" width="20" height="160" fill="#8a5a32"/><rect x="1000" y="740" width="20" height="160" fill="#8a5a32"/>'
             f'<rect x="780" y="760" width="90" height="150" rx="14" fill="#0b0d22"/><rect x="790" y="772" width="70" height="120" rx="8" fill="#7fb0ff"/>'
             f'<path d="M 825 880 L 825 800 M 805 820 L 825 800 L 845 820" stroke="#fff" stroke-width="7" fill="none"/>'
             f'<rect x="640" y="520" width="360" height="140" rx="10" fill="#2f5d3a" stroke="#b07a4a" stroke-width="10"/><text x="820" y="605" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="40" fill="#fff">MATHE</text>')
callout("sc3", t_hm, t_opa, 1, "HAUSMEISTER KURT", icon_desk)
tw(f'tl.fromTo("#sc3-i",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.4,ease:"power2.out"}},{t_schule - 0.2:.3f});')
icon_vol = (f'<rect x="640" y="560" width="360" height="300" rx="30" fill="#0b0d22" stroke="#ffd23f" stroke-width="6"/>'
            f'<path d="M 700 680 L 750 680 L 810 630 L 810 790 L 750 740 L 700 740 Z" fill="#fff"/>'
            + "".join(f'<rect id="sc3b-v{k}" x="{850+k*40}" y="{760-k*40}" width="26" height="{40+k*40}" rx="6" fill="#ffd23f"/>' for k in range(3)))
PEOPLE[3] = ("#8d6e63", "#3a4a6a", "#e8c4a8", "#d9d4cf", "flat")     # Opa Fritz: graue Haare
callout("sc3b", t_opa, t_lina, 3, "OPA FRITZ", icon_vol, mood="happy")
tw(f'tl.fromTo("#sc3b-i",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.4,ease:"power2.out"}},{t_opa + 0.3:.3f});')
for k in range(3):
    tw(f'tl.to("#sc3b-v{2-k}",{{opacity:.15,duration:.15}},{t_leiser + k*0.2:.3f});')
icon_swipe = (f'<rect x="700" y="500" width="260" height="460" rx="40" fill="#0b0d22"/><rect x="718" y="520" width="224" height="420" rx="26" fill="url(#daysky)"/>'
              f'<rect x="760" y="640" width="140" height="140" rx="10" fill="#ffd23f"/><circle cx="800" cy="690" r="10" fill="#111"/><circle cx="860" cy="690" r="10" fill="#111"/>'
              f'<g id="sc4-sw"><path d="M 830 900 L 830 560 M 790 600 L 830 560 L 870 600" stroke="#fff" stroke-width="14" fill="none" stroke-linecap="round"/></g>'
              f'<text id="sc4-x2" x="990" y="560" font-family="Poppins" font-weight="800" font-size="80" fill="{RED}" opacity="0">2×</text>')
callout("sc4", t_lina, t_papa, 2, "LINA", icon_swipe)
tw(f'tl.fromTo("#sc4-i",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.4,ease:"power2.out"}},{t_lina + 0.2:.3f});')
tw(f'tl.fromTo("#sc4-sw",{{y:60,opacity:0}},{{y:-60,opacity:1,duration:.45,repeat:1,repeatDelay:.15,ease:"power2.in"}},{t_wisch - 0.2:.3f});')
tw(f'tl.to("#sc4-x2",{{opacity:1,duration:.2}},{t_zweimal:.3f});')
tw(f'tl.set("#sc4-p .bf",{{opacity:1}},{t_lina:.3f});')

# D Papas Tafel: ZUSCHAUER JETZT – 0:03 WEG, 0:08 WEG, DU live
S0, S1 = t_papa, t_daumen
papa = block("sd-papa", 860, 1400, 1.0, "#e0a83a", "#23252e", "#e8b08a", "#1e1a2e", "spike", "happy")
scene("sd", S0, S1, town_bg("sd") + board_live("sd-bd", 110, 420, 720, (t_drei, t_acht, t_unddu), t_unddu, t_daumen + 1)
      + "".join(person(i, f"sd-p{i}", x, 1560, 1.05, "shock", back=True) for i, x in enumerate((120, 330, 540, 750)))
      + papa, drift=False)
fadein("#sd-bd", S0 + 0.05, 0.4, -20)
tw(f'tl.fromTo("#sd-cam",{{scale:1,svgOrigin:"470 700"}},{{scale:1.18,svgOrigin:"470 700",duration:{t_nicht-S0:.3f},ease:"sine.inOut"}},{S0:.3f});')
tw(f'tl.to("#sd-cam",{{scale:1.45,svgOrigin:"470 850",duration:{max(1.0, S1-t_nicht):.3f},ease:"sine.inOut"}},{t_nicht:.3f});')

# E Der Daumen kommt – alle festhalten – er bleibt
S0, S1 = t_daumen, t_papa2
thumb = (f'<g id="se-th"><rect x="300" y="-1100" width="480" height="1300" rx="220" fill="#e8b08a"/><rect x="300" y="-1100" width="480" height="1300" rx="220" fill="url(#thumbshade)"/>'
         f'<rect x="370" y="-40" width="340" height="200" rx="90" fill="#f6d3bd"/>'
         + "".join(f'<path d="M 380 {y} Q 540 {y+30} 700 {y}" stroke="#c98a66" stroke-width="6" fill="none" opacity=".6"/>' for y in (-300, -260)) + '</g>')
scene("se", S0, S1, f'<rect width="1080" height="1920" fill="url(#daysky)"/>' + thumb + f'<rect x="0" y="1250" width="1080" height="670" fill="{GR}"/>'
      + "".join(person(i, f"se-p{i}", x, 1560, 1.0, "shock") for i, x in enumerate((140, 400, 680, 940))), drift=False)
tw(f'tl.fromTo("#se-th",{{y:-500}},{{y:200,duration:{max(0.8, t_fest - S0):.3f},ease:"power1.in"}},{S0:.3f});')
for i in range(4):
    tw(f'tl.to("#se-p{i}-b",{{scaleY:.86,transformOrigin:"50% 100%",duration:.2,ease:"power2.out"}},{t_fest:.3f});')
    tw(f'tl.to("#se-p{i}-b",{{scaleY:1,duration:.3,ease:"power2.out"}},{t_bleibt + 0.2:.3f});')
shake("#se-cam", t_fest, 6, 6)
tw(f'tl.to("#se-th",{{y:-1200,duration:.8,ease:"power2.in"}},{t_bleibt - 0.1:.3f});')
for i in range(4):
    tw(f'tl.to("#se-p{i}",{{y:-90,duration:.25,yoyo:true,repeat:3,ease:"power1.out"}},{t_jubelt + i*0.06:.3f});')
happy = "".join(person(i, f"se-h{i}", x, 1560, 1.0, "happy") for i, x in enumerate((140, 400, 680, 940)))

# F Zoom rein: ins Handy, ins Zimmer, in unsere Stadt
S0, S1 = t_papa2, t_ende
room = (f'<rect x="-400" y="-300" width="1880" height="2520" fill="#2a2440"/><rect x="200" y="500" width="680" height="520" fill="#1c1f45"/>'
        f'<rect x="560" y="580" width="260" height="300" fill="url(#daysky)" stroke="#fff" stroke-width="12"/>'
        f'<rect x="240" y="860" width="320" height="120" rx="20" fill="#3b6cff"/><rect x="240" y="830" width="110" height="60" rx="16" fill="#fff"/>')
mini_town = f'<g transform="translate(616,632) scale(.15)">{town_bg("sf-mini")}</g>'
phone_fr = (f'<g id="sf-ph"><rect x="300" y="300" width="480" height="900" rx="60" fill="#0b0d22"/><rect x="320" y="320" width="440" height="860" rx="44" fill="url(#daysky)"/>'
            f'<g transform="translate(320,320) scale(.4074)">{town_bg("sf-ph")}</g></g>')
scene("sf", S0, S1, f'<g id="sf-z">{room}{mini_town}{phone_fr}</g>', drift=False)
tw(f'tl.fromTo("#sf-z",{{scale:.6,svgOrigin:"540 750"}},{{scale:1,svgOrigin:"540 750",duration:.6,ease:"sine.out"}},{S0:.3f});')
tw(f'tl.to("#sf-z",{{scale:2.6,svgOrigin:"540 750",duration:.9,ease:"power2.in"}},{t_handy - 0.2:.3f});')
tw(f'tl.to("#sf-ph",{{opacity:0,duration:.3}},{t_zimmer - 0.3:.3f});')
tw(f'tl.set("#sf-z",{{scale:1,svgOrigin:"540 750"}},{t_zimmer - 0.3:.3f});')
tw(f'tl.to("#sf-z",{{scale:7,svgOrigin:"690 730",duration:1.0,ease:"power2.in"}},{t_stadt2 - 0.6:.3f});')

# G Am Ende der Straße: ein Haus mit deinem Namen
S0, S1 = t_ende, t_schaust
house = (box(330, 560, 420, 460, "#ffd6e0", "#e8b4c2", "#ffe3ea") + f'<polygon points="300,560 540,400 780,560" fill="#e56b6f"/>'
         f'<rect x="480" y="820" width="120" height="200" fill="#6b4a32"/><circle cx="580" cy="925" r="8" fill="#ffd23f"/>'
         f'<rect x="370" y="620" width="90" height="90" fill="#bfe4ff" stroke="#fff" stroke-width="8"/><rect x="620" y="620" width="90" height="90" fill="#bfe4ff" stroke="#fff" stroke-width="8"/>'
         f'<g id="sg-np" opacity="0"><rect x="420" y="740" width="240" height="64" rx="12" fill="#fff4c2" stroke="#ffd23f" stroke-width="6"/>'
         f'<text x="540" y="784" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="34" fill="#0b0d22">DEIN NAME</text></g>'
         f'<circle id="sg-glow" cx="540" cy="772" r="200" fill="url(#namglow)" opacity="0"/>')
carpet = f'<polygon points="480,1020 600,1020 760,1920 320,1920" fill="#c62828"/><polygon points="500,1020 580,1020 700,1920 380,1920" fill="#e53935"/>'
scene("sg", S0, S1, f'<rect width="1080" height="1920" fill="url(#daysky)"/><rect x="0" y="1020" width="1080" height="900" fill="{GR}"/>'
      + f'<polygon points="420,1020 660,1020 1080,1920 0,1920" fill="{ROADC}"/>' + carpet + house
      + "".join(person(i, f"sg-p{i}", x, y, s, "happy") for i, (x, y, s) in enumerate(((150, 1300, .9), (930, 1300, .9), (90, 1650, 1.1), (990, 1650, 1.1)))), drift=False)
tw(f'tl.fromTo("#sg-cam",{{scale:1,svgOrigin:"540 900"}},{{scale:1.45,svgOrigin:"540 780",duration:{S1-S0+0.3:.3f},ease:"sine.inOut"}},{S0:.3f});')
pop("#sg-np", t_namen - 0.1, 0.4, 0.7)
tw(f'tl.fromTo("#sg-glow",{{opacity:0}},{{opacity:1,duration:.5,yoyo:true,repeat:3,ease:"sine.inOut"}},{t_namen:.3f});')

# H Loop: zurück auf die Straße – exakt wie der Anfang
S0, S1 = t_schaust, TOTAL
crowd2 = "".join(person(i, f"sh-p{i}", x, y, s, "happy") for i, (x, y, s) in enumerate(((150, 1150, .9), (380, 1160, .95), (620, 1150, .9), (870, 1160, .95), (260, 1400, 1.15), (760, 1400, 1.15))))
scene("sh", S0, S1, town_bg("sh") + crowd2, drift=False)
tw(f'tl.fromTo("#sh-cam",{{scale:1.25,svgOrigin:"540 1200"}},{{scale:1,svgOrigin:"540 1200",duration:{S1-S0+0.3:.3f},ease:"sine.inOut"}},{S0:.3f});')

# ================= SERIEN-BRANDING OBEN LINKS (Format B) =================
BRAND = []
BRAND = [(a, b if i + 1 >= len(BRAND) or BRAND[i+1][0] >= b else BRAND[i+1][0], c, d) for i, (a, b, c, d) in enumerate(BRAND)]
brand_html = []
for i, (a, b, clock, place) in enumerate(BRAND):
    brand_html.append(
        f'<div id="br{i}" class="clip ov" data-start="{a:.3f}" data-duration="{b-a:.3f}" data-track-index="7" style="z-index:12">'
        f'<svg viewBox="0 0 1080 1920" width="1080" height="1920"><rect x="40" y="150" width="400" height="200" rx="24" fill="#0b0d22" opacity=".55"/><g transform="translate(70,190)">'
        f'<circle cx="8" cy="-6" r="8" fill="{RED}"/><text x="26" y="2" font-family="JetBrains Mono, monospace" font-weight="700" font-size="24" fill="#cfd3ff" letter-spacing="4">GULLY · TEIL 1</text>'
        f'<text x="0" y="96" font-family="JetBrains Mono, monospace" font-weight="800" font-size="96" fill="{RED}" filter="url(#glowsoft)">{clock}</text>'
        f'<text x="{len(clock)*58+10}" y="96" font-family="JetBrains Mono, monospace" font-weight="700" font-size="26" fill="{RED}">UHR</text>'
        f'<text x="2" y="140" font-family="JetBrains Mono, monospace" font-weight="700" font-size="22" fill="#8f94c4" letter-spacing="4">{place}</text></g></svg></div>')

# ================= UNTERTITEL (Skill 7 + Format B: Akzent Neon-Gelbgrün) =================
KEY = {"DU", "DICH", "DEIN", "DEINEM", "DU?"}
RED_W = {"WEG", "WEG!"}
DISPLAY = {"zwei": "2", "dreißig": "30", "Drei": "3", "Acht": "8"}
SKIP = {"zwölf", "zwölf.", "dreißig.", "vierzig.", "Uhr"}


def norm(t):
    return re.sub(r"[^\wÄÖÜäöüß:]", "", t).upper()


words = [dict(w) for w in W]
for k, w in enumerate(words):
    if w["t"].lower().startswith("uhr") and k and words[k-1]["t"].lower() == "zwei":
        pass
chunks = [[w] for w in words]
subs = []
for k, c in enumerate(chunks):
    w = c[0]
    s = w["s"]
    e = chunks[k+1][0]["s"] if k + 1 < len(chunks) else min(TOTAL, w["e"] + 0.4)
    t = DISPLAY.get(w["t"], w["t"]).upper()
    core = re.sub(r"[^\wÄÖÜß:]", "", t)
    col = "#5ff0d4" if core in KEY else (RED if core.startswith("WEG") else "#d8f53c")
    fs = min(116, int(940 / (0.62 * max(len(t), 1))))
    sid = f"sub{k}"
    subs.append(f'<div id="{sid}" class="clip sub" data-start="{s:.3f}" data-duration="{max(0.05, e-s):.3f}" data-track-index="9" style="font-size:{fs}px;color:{col}">{html.escape(t)}</div>')
    tw(f'tl.fromTo("#{sid}",{{scale:.7,opacity:0}},{{scale:1,opacity:1,duration:.12,ease:"back.out(2)"}},{s:.3f});')


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
<radialGradient id="lampglow"><stop offset="0" stop-color="#fff6d8" stop-opacity=".5"/><stop offset="1" stop-color="#fff6d8" stop-opacity="0"/></radialGradient>
<radialGradient id="cardglow"><stop offset="0" stop-color="#3a3d8f" stop-opacity=".55"/><stop offset="1" stop-color="#3a3d8f" stop-opacity="0"/></radialGradient>
<radialGradient id="stationglow" cx=".5" cy="0" r="1"><stop offset="0" stop-color="#fff4c9" stop-opacity=".35"/><stop offset="1" stop-color="#fff4c9" stop-opacity="0"/></radialGradient>
<radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".7"/></radialGradient>
<radialGradient id="redvig" cx=".5" cy=".5" r=".72"><stop offset=".5" stop-color="{RED}" stop-opacity="0"/><stop offset="1" stop-color="{RED}" stop-opacity=".7"/></radialGradient>
<radialGradient id="yelglow"><stop offset="0" stop-color="#ffd23f" stop-opacity=".55"/><stop offset="1" stop-color="#ffd23f" stop-opacity="0"/></radialGradient>
{FIGC_DEFS}<linearGradient id="daysky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3f8fe0"/><stop offset=".55" stop-color="#8cc6f5"/><stop offset="1" stop-color="#d9efff"/></linearGradient>
<radialGradient id="sunglow"><stop offset="0" stop-color="#fff4c2" stop-opacity=".6"/><stop offset="1" stop-color="#fff4c2" stop-opacity="0"/></radialGradient>
<linearGradient id="thumbshade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".18"/></linearGradient>
<radialGradient id="namglow"><stop offset="0" stop-color="#fff4c2" stop-opacity=".7"/><stop offset="1" stop-color="#fff4c2" stop-opacity="0"/></radialGradient>
<pattern id="netpat" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M 0 0 L 30 30 M 30 0 L 0 30" stroke="#e8ecff" stroke-width="2"/></pattern>
<filter id="softblur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="10"/></filter>
<filter id="softedge" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3"/></filter>
<radialGradient id="eyeglow"><stop offset="0" stop-color="#f6f4ff" stop-opacity=".45"/><stop offset="1" stop-color="#f6f4ff" stop-opacity="0"/></radialGradient>
<filter id="fogblur" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="40"/></filter>
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


for sbid, tt, txt in []:
    pass
for fid in FIGS:
    tw(f'tl.fromTo("#{fid}-body",{{scaleY:1}},{{scaleY:1.02,transformOrigin:"50% 100%",duration:1.3,yoyo:true,repeat:{int(TOTAL/1.3)},ease:"sine.inOut"}},0);')
for sid, t0, t1, _ in SCENES[1:]:
    tw(f'tl.fromTo("#{sid}",{{opacity:0}},{{opacity:1,duration:{XF},ease:"sine.inOut"}},{t0:.3f});')

# ================= HTML =================
scene_html = [f'<div id="{sid}" class="clip scene" data-start="{t0:.3f}" data-duration="{min(t1+XF, TOTAL)-t0:.3f}" data-track-index="1">'
              f'<svg viewBox="0 0 1080 1920" width="1080" height="1920">{inner}</svg></div>' for sid, t0, t1, inner in SCENES]

doc = f'''<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Block-Stadt</title>
    <script src="assets/gsap.min.js"></script>
    <style>
      :root {{ --ground: {SKY1}; --ink: #ffffff; --accent: {RED}; --font-display: "Poppins", sans-serif; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: var(--ground); }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: var(--font-display); }}
      .scene, .ov {{ position: absolute; inset: 0; }}
      .ov {{ pointer-events: none; }}
      .scene svg {{ display: block; }}
      .sub {{ position: absolute; left: 0; right: 0; top: 1330px; text-align: center; z-index: 20; font-weight: 800; letter-spacing: 1px;
        -webkit-text-stroke: 14px #0b0b0b; paint-order: stroke fill; text-shadow: 0 6px 0 #0b0b0b; line-height: 1; transform-origin: 50% 50%; }}
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
