#!/usr/bin/env python3
"""Generator für index.html – Video „Was passiert, wenn das Seil deines Aufzugs reißt?“

Alle Zeiten kommen aus assets/words.json (wortgenaue ElevenLabs-Zeitstempel des Voiceovers).
Aufruf:  python3 build.py   → schreibt index.html
"""
import json, re, html, os

HERE = os.path.dirname(os.path.abspath(__file__))
W = json.load(open(os.path.join(HERE, "assets/words.json"), encoding="utf-8"))
TOTAL = 80.8

# ---------- Farben (Skill: dunkle Grundpalette + eine Signalfarbe) ----------
BG = "#10141a"; SHAFT = "#1a2029"; WALL = "#232b36"; RAIL = "#4a5563"
ROPE = "#9aa4b1"; CAB = "#2b3442"; CAB_LINE = "#5d6b7d"; FIG = "#d9dde3"; INK = "#151a21"
RED = "#ff3b3b"; GREEN = "#3ddc84"; WHITE = "#ffffff"; LAMP = "#ffe9a8"
SEP_BG = "#221a12"; SEP_MID = "#3a2d1f"; SEP_LINE = "#8a6f4e"; SEP_FIG = "#e6d2ad"; SEP_LIGHT = "#c9a77c"


def ws(word_prefix, after=0.0):
    """Startzeit des ersten Wortes (nach Zeit `after`), das mit word_prefix beginnt."""
    for w in W:
        if w["s"] >= after - 1e-6 and w["t"].lower().strip(".,:?!").startswith(word_prefix.lower()):
            return w["s"]
    raise KeyError(word_prefix)


T = []  # GSAP-Tweens


def tw(code):
    T.append(code)


def toggle(sel, t_on, t_off=None):
    tw(f'tl.set("{sel}",{{opacity:1}},{t_on:.3f});')
    if t_off is not None:
        tw(f'tl.set("{sel}",{{opacity:0}},{t_off:.3f});')


def pop(sel, t, dur=0.18, frm=0.6):
    tw(f'tl.fromTo("{sel}",{{opacity:0,scale:{frm},transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:{dur},ease:"back.out(2)"}},{t:.3f});')


def shake(sel, t, n=8, amp=18, step=0.035):
    for i in range(n):
        x = amp * (1 if i % 2 == 0 else -1) * (1 - i / n)
        tw(f'tl.to("{sel}",{{x:{x:.1f},y:{-x/2:.1f},duration:{step}}},{t + i*step:.3f});')
    tw(f'tl.to("{sel}",{{x:0,y:0,duration:{step}}},{t + n*step:.3f});')


def drift(sel, t0, t1, s0=1.0, s1=1.07):
    tw(f'tl.fromTo("{sel}",{{scale:{s0},svgOrigin:"540 960"}},{{scale:{s1},duration:{t1-t0:.3f},ease:"none"}},{t0:.3f});')


# ---------- SVG-Bausteine ----------
def figure(fid, x, y, s=1.0, sep=False, cap=False, eyes="n"):
    """Gesichtslose Gliederpuppe (Skill: Emotion nur über Augen/Brauen). Füße bei (x,y)."""
    F = SEP_FIG if sep else FIG
    E = "#2a2016" if sep else INK
    capsvg = ""
    if cap:
        capsvg = (f'<rect x="-58" y="-392" width="116" height="36" rx="8" fill="#5a4630"/>'
                  f'<rect x="-70" y="-362" width="140" height="12" rx="6" fill="#4a3826"/>')
    o_n = 1 if eyes == "n" else 0
    o_w = 1 if eyes == "w" else 0
    o_c = 1 if eyes == "c" else 0
    return f'''
<g id="{fid}"><g transform="translate({x},{y}) scale({s})">
  <g id="{fid}-body">
  <rect x="-34" y="-125" width="26" height="125" rx="13" fill="{F}"/>
  <rect x="8" y="-125" width="26" height="125" rx="13" fill="{F}"/>
  <rect x="-58" y="-255" width="116" height="145" rx="34" fill="{F}"/>
  <rect x="-84" y="-245" width="24" height="120" rx="12" fill="{F}" id="{fid}-armL"/>
  <rect x="60" y="-245" width="24" height="120" rx="12" fill="{F}" id="{fid}-armR"/>
  <rect x="-12" y="-275" width="24" height="26" rx="8" fill="{F}"/>
  <circle cx="0" cy="-320" r="64" fill="{F}"/>
  {capsvg}
  <g id="{fid}-eyes-n" opacity="{o_n}">
    <circle cx="-22" cy="-322" r="9" fill="{E}"/><circle cx="22" cy="-322" r="9" fill="{E}"/>
    <rect x="-36" y="-346" width="26" height="6" rx="3" fill="{E}"/><rect x="10" y="-346" width="26" height="6" rx="3" fill="{E}"/>
    <rect x="-12" y="-290" width="24" height="5" rx="2.5" fill="{E}"/>
  </g>
  <g id="{fid}-eyes-w" opacity="{o_w}">
    <circle cx="-24" cy="-322" r="17" fill="none" stroke="{E}" stroke-width="5"/><circle cx="24" cy="-322" r="17" fill="none" stroke="{E}" stroke-width="5"/>
    <circle cx="-24" cy="-322" r="5" fill="{E}"/><circle cx="24" cy="-322" r="5" fill="{E}"/>
    <rect x="-42" y="-356" width="28" height="6" rx="3" fill="{E}" transform="rotate(-12 -28 -353)"/>
    <rect x="14" y="-356" width="28" height="6" rx="3" fill="{E}" transform="rotate(12 28 -353)"/>
    <ellipse cx="0" cy="-284" rx="9" ry="12" fill="{E}"/>
  </g>
  <g id="{fid}-eyes-c" opacity="{o_c}">
    <rect x="-34" y="-324" width="22" height="6" rx="3" fill="{E}"/><rect x="12" y="-324" width="22" height="6" rx="3" fill="{E}"/>
    <path d="M -14 -292 Q 0 -282 14 -292" stroke="{E}" stroke-width="5" fill="none" stroke-linecap="round"/>
  </g>
  </g>
</g></g>'''


def cabin(cid, cx, cy, w=440, h=580, sep=False, fig=None, lamp_id=None):
    C = SEP_MID if sep else CAB
    L = SEP_LINE if sep else CAB_LINE
    lamp = SEP_LIGHT if sep else LAMP
    inner = fig or ""
    lid = f' id="{lamp_id}"' if lamp_id else ""
    return f'''
<g id="{cid}"><g transform="translate({cx},{cy})">
  <rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" rx="18" fill="{C}" stroke="{L}" stroke-width="8"/>
  <rect x="{-w/2+24}" y="{-h/2+24}" width="{w-48}" height="{h-48}" rx="8" fill="{'#2d241a' if sep else '#222a35'}"/>
  <rect{lid} x="-90" y="{-h/2+30}" width="180" height="16" rx="8" fill="{lamp}"/>
  <line x1="0" y1="{-h/2+60}" x2="0" y2="{h/2-24}" stroke="{L}" stroke-width="4" opacity=".55"/>
  <rect x="{-w/2+24}" y="{h/2-60}" width="{w-48}" height="8" rx="4" fill="{L}" opacity=".7"/>
  <circle cx="0" cy="{-h/2-6}" r="16" fill="{L}"/>
  {inner}
</g></g>'''


def ropes(rid, xs, y0, y1, col=ROPE, width=9):
    lines = "".join(
        f'<line id="{rid}-{i}" x1="{x}" y1="{y0}" x2="{x}" y2="{y1}" stroke="{col}" stroke-width="{width}" stroke-linecap="round"/>'
        for i, x in enumerate(xs))
    return f'<g id="{rid}">{lines}</g>'


def shaft_bg(sep=False):
    bg = SEP_BG if sep else BG
    sh = "#2a2118" if sep else SHAFT
    rl = SEP_LINE if sep else RAIL
    return f'''
<rect width="1080" height="1920" fill="{bg}"/>
<rect x="250" y="0" width="580" height="1920" fill="{sh}"/>
<rect x="286" y="0" width="16" height="1920" fill="{rl}"/>
<rect x="778" y="0" width="16" height="1920" fill="{rl}"/>'''


def rail_marks(mid, sep=False, span=9000):
    rl = SEP_LINE if sep else RAIL
    marks = "".join(f'<rect x="250" y="{y}" width="580" height="10" fill="{rl}" opacity=".35"/>'
                    f'<rect x="270" y="{y+120}" width="50" height="6" fill="{rl}" opacity=".6"/>'
                    f'<rect x="760" y="{y+120}" width="50" height="6" fill="{rl}" opacity=".6"/>'
                    for y in range(-200, span, 300))
    return f'<g id="{mid}">{marks}</g>'


def label(lid, x, y, text, col=RED, size=40, anchor="middle", op=0, fill_bg=True):
    tw_ = len(text) * size * 0.64 + 44
    if anchor == "middle":
        rx = x - tw_/2
    elif anchor == "start":
        rx = x - 22
    else:
        rx = x - tw_ + 22
    bg = (f'<rect x="{rx:.0f}" y="{y-size*0.95:.0f}" width="{tw_:.0f}" height="{size*1.4:.0f}" rx="{size*0.7:.0f}" '
          f'fill="#0b0e12" fill-opacity=".85" stroke="{col}" stroke-width="5"/>') if fill_bg else ""
    return (f'<g id="{lid}" opacity="{op}" style="transform-box:fill-box;transform-origin:center">{bg}'
            f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Inter, sans-serif" '
            f'font-weight="800" font-size="{size}" fill="{col}">{html.escape(text)}</text></g>')


def hud(hid, floor_vals, speed_vals):
    """Diegetische Anzeige oben: Etage + Geschwindigkeit. *_vals: [(t, text, color)]"""
    out = [f'<g id="{hid}" transform="translate(0,90)">',
           '<rect x="190" y="110" width="700" height="210" rx="34" fill="#0b0e12" stroke="#3a4452" stroke-width="6"/>',
           '<text x="365" y="165" text-anchor="middle" font-family="Inter, sans-serif" font-weight="700" font-size="30" fill="#7d8896" letter-spacing="4">ETAGE</text>',
           '<text x="715" y="165" text-anchor="middle" font-family="Inter, sans-serif" font-weight="700" font-size="30" fill="#7d8896" letter-spacing="4">TEMPO M/S</text>',
           '<line x1="540" y1="140" x2="540" y2="290" stroke="#3a4452" stroke-width="4"/>']
    for i, (t, txt, col) in enumerate(floor_vals):
        out.append(f'<text id="{hid}-f{i}" x="365" y="282" text-anchor="middle" font-family="JetBrains Mono, monospace" '
                   f'font-weight="800" font-size="104" fill="{col}" opacity="0">{txt}</text>')
    for i, (t, txt, col) in enumerate(speed_vals):
        out.append(f'<text id="{hid}-s{i}" x="715" y="272" text-anchor="middle" font-family="JetBrains Mono, monospace" '
                   f'font-weight="800" font-size="76" fill="{col}" opacity="0">{txt}</text>')
    out.append('</g>')
    return "".join(out)


def hud_anim(hid, floor_vals, speed_vals, t_end):
    for arr, k in ((floor_vals, "f"), (speed_vals, "s")):
        for i, (t, txt, col) in enumerate(arr):
            t_off = arr[i+1][0] if i + 1 < len(arr) else t_end
            toggle(f"#{hid}-{k}{i}", t, t_off)


SCENES = []


def scene(sid, t0, t1, svg_inner, extra_html=""):
    SCENES.append((sid, t0, t1, svg_inner, extra_html))
    drift(f"#{sid}-cam", t0, t1)


def cam(sid, inner):
    return f'<g id="{sid}-cam" style="transform-origin:540px 960px">{inner}</g>'


# ================= SZENEN =================
t_was = ws("Was"); t_seil = ws("Seil"); t_reisst = ws("reißt")
t_zwei = ws("Zweiunddreißigster"); t_du = ws("Du", 4)
t_ploetz = ws("Plötzlich"); t_knall = ws("Knall"); t_licht = ws("Licht")
t_dein = ws("Dein", 9); t_hoch = ws("hochspringen"); t_bringt = ws("Bringt"); t_faellst = ws("fällst")
t_doch = ws("Doch", 15); t_genau = ws("Genau", 16); t_1945 = ws("Neunzehn")
t_bomber = ws("Bomber"); t_building = ws("Building"); t_durch = ws("durchtrennt"); t_seile1 = ws("Seile", 23)
t_inder = ws("In", 25.5); t_lift = ws("Liftführerin"); t_betty = ws("Betty", 26)
t_sie = ws("Sie", 28.5); t_75 = ws("fünfundsiebzig"); t_tiefe = ws("Tiefe")
t_und_ueb = ws("Und", 31.7); t_ueberlebt = ws("überlebt")
t_wie = ws("Wie", 33); t_heute = ws("heute")
t_erst = ws("Erstens"); t_einem = ws("einem", 38); t_sondern = ws("sondern"); t_vier1 = ws("vier", 40); t_acht = ws("acht")
t_jedes = ws("Jedes"); t_allein = ws("allein", 43)
t_zweit = ws("Zweitens"); t_duenne = ws("dünne", 45); t_traegt = ws("trägt"); t_laeuft = ws("läuft")
t_doch2 = ws("Doch", 49.5); t_reissen = ws("reißen"); t_kab_f = ws("Kabine", 52); t_faellt = ws("fällt", 52)
t_2ms = ws("Zwei", 53); t_3ms = ws("Drei", 54); t_4ms = ws("Vier", 55)
t_und_g = ws("Und", 56); t_duenne2 = ws("dünne", 57); t_dreht = ws("dreht"); t_rad = ws("Rad", 59); t_gesch = ws("Geschwindigkeits")
t_wird = ws("Wird", 60); t_blockiert = ws("blockiert"); t_reisst2 = ws("reißt", 63.9); t_keile = ws("Stahlkeile"); t_schienen = ws("Schienen")
t_krallt = ws("krallt"); t_fest = ws("fest", 67); t_nach = ws("Nach", 68); t_still = ws("Stillstand")
t_bei = ws("Bei", 70); t_einschlag = ws("Einschlag"); t_gerettet = ws("Gerettet"); t_seile3 = ws("Seile", 74.5); t_feder = ws("Feder"); t_auf = ws("aufrollten")
t_also = ws("Also"); t_aufzug_end = ws("Aufzug", 79)

# --- A: Hook – Seil-Nahaufnahme reißt (0 – Zweiunddreißigster) ---
A0, A1 = 0.0, t_zwei
strands = ""
for i in range(7):
    x = 400 + i * 40
    strands += (f'<g id="a-st{i}"><rect x="{x}" y="-100" width="30" height="1060" rx="15" fill="#8e98a5"/>'
                f'<rect x="{x+6}" y="-100" width="8" height="1060" fill="#c3cad3" opacity=".6"/></g>')
    strands += (f'<g id="a-sb{i}"><rect x="{x}" y="960" width="30" height="1060" rx="15" fill="#8e98a5"/>'
                f'<rect x="{x+6}" y="960" width="8" height="1060" fill="#c3cad3" opacity=".6"/></g>')
bands = "".join(f'<rect x="390" y="{y}" width="300" height="14" fill="#5f6976" opacity=".7" transform="skewY(-14)" style="transform-origin:540px {y}px"/>'
                for y in range(-60, 1960, 90))
sparks = "".join(f'<rect id="a-spk{i}" x="530" y="950" width="22" height="6" rx="3" fill="{LAMP}" opacity="0" '
                 f'style="transform-origin:540px 960px" transform="rotate({i*36} 540 960)"/>' for i in range(10))
scene("sa", A0, A1, cam("sa", f'''
<rect width="1080" height="1920" fill="{BG}"/>
<radialGradient id="ga" cx=".5" cy=".5" r=".6"><stop offset="0" stop-color="#26303d"/><stop offset="1" stop-color="{BG}"/></radialGradient>
<rect width="1080" height="1920" fill="url(#ga)"/>
<g id="a-rope">{strands}{bands}</g>{sparks}
''') + hud("ha", [(A0, "32", WHITE)], [(A0, "0,0", WHITE)]))
hud_anim("ha", [(A0, "32", WHITE)], [(A0, "0,0", WHITE)], A1)
tw(f'tl.fromTo("#a-rope",{{scale:1,svgOrigin:"540 960"}},{{scale:1.18,duration:{t_reisst-A0:.3f},ease:"power1.in"}},0);')
for i in range(7):
    d = 0.06 * (i % 3)
    tw(f'tl.to("#a-st{i}",{{y:{-260 - 40*(i%4)},rotation:{(-1)**i*8},transformOrigin:"50% 50%",duration:.45,ease:"power3.out"}},{t_reisst + d:.3f});')
    tw(f'tl.to("#a-sb{i}",{{y:{260 + 40*(i%3)},rotation:{(-1)**(i+1)*8},transformOrigin:"50% 50%",duration:.45,ease:"power3.out"}},{t_reisst + d:.3f});')
for i in range(10):
    tw(f'tl.fromTo("#a-spk{i}",{{opacity:0}},{{opacity:1,duration:0.001,immediateRender:false}},{t_reisst:.3f});'); tw(f'tl.fromTo("#a-spk{i}",{{immediateRender:false,x:0,y:0}},{{opacity:0,x:{int(300*__import__("math").cos(i*0.628))},y:{int(300*__import__("math").sin(i*0.628))},duration:.5}},{t_reisst:.3f});')
shake("#sa-cam", t_reisst, amp=22)

# --- B: Kabine 32. Stock, allein (Zweiunddreißigster – Plötzlich) ---
B0, B1 = t_zwei, t_ploetz
rope_xs = [490, 515, 540, 565, 590]
scene("sb", B0, B1, cam("sb", shaft_bg() + ropes("b-r", rope_xs, 0, 1060)
      + cabin("b-cab", 540, 1350, fig=figure("b-fig", 0, 270, 0.95)))
      + hud("hb", [(B0, "32", WHITE)], [(B0, "0,0", WHITE)])
      + label("b-l", 540, 1750, "ALLEIN", WHITE, 44))
hud_anim("hb", [(B0, "32", WHITE)], [(B0, "0,0", WHITE)], B1)
pop("#hb", B0, .25, .8)
tw(f'tl.fromTo("#b-fig",{{opacity:0}},{{opacity:1,duration:.3}},{t_du:.3f});')
pop("#b-l", ws("allein"))

# --- C: Knall + Licht flackert (Plötzlich – Dein) ---
C0, C1 = t_ploetz, t_dein
burst = "".join(f'<polygon points="540,40 {540+int(170*__import__("math").cos(a))},{40+int(170*__import__("math").sin(a))} {540+int(60*__import__("math").cos(a+0.3))},{40+int(60*__import__("math").sin(a+0.3))}" fill="{LAMP}"/>'
                for a in [i*0.785 for i in range(8)])
scene("sc", C0, C1, cam("sc", shaft_bg() + ropes("c-r", rope_xs, 0, 1060)
      + cabin("c-cab", 540, 1350, fig=figure("c-fig", 0, 270, 0.95), lamp_id="c-lamp")
      + f'<g id="c-burst" opacity="0" style="transform-origin:540px 40px">{burst}'
        f'<text x="540" y="560" text-anchor="middle" font-family="Inter" font-weight="900" font-size="120" fill="{RED}">KNALL!</text></g>'
      + f'<rect id="c-dark" width="1080" height="1920" fill="#000" opacity="0"/>')
      + hud("hc", [(C0, "32", WHITE)], [(C0, "0,0", WHITE)]))
hud_anim("hc", [(C0, "32", WHITE)], [(C0, "0,0", WHITE)], C1)
tw(f'tl.fromTo("#c-burst",{{opacity:0}},{{opacity:1,duration:0.001,immediateRender:false}},{t_knall:.3f});'); tw(f'tl.fromTo("#c-burst",{{immediateRender:false,scale:.3,svgOrigin:"540 470"}},{{scale:1.1,duration:.25,ease:"back.out(3)"}},{t_knall:.3f});')
tw(f'tl.to("#c-burst",{{opacity:0,duration:.4}},{t_knall+0.9:.3f});')
shake("#sc-cam", t_knall, n=10, amp=26)
toggle("#c-fig-eyes-n", C0, t_knall + 0.05); toggle("#c-fig-eyes-w", t_knall + 0.05)
fl = [0, .08, .16, .30, .38, .55, .62, .80]
for i, d in enumerate(fl):
    tw(f'tl.set("#c-dark",{{opacity:{0.72 if i%2==0 else 0}}},{t_licht + d:.3f});')
    tw(f'tl.set("#c-lamp",{{opacity:{0.1 if i%2==0 else 1}}},{t_licht + d:.3f});')

# --- D: Gedanke hochspringen → bringt nichts → du fällst mit (Dein – Doch) ---
D0, D1 = t_dein, t_doch
arrow = lambda aid, x, txt: (f'<g id="{aid}" opacity="0"><rect x="{x-14}" y="1120" width="28" height="330" fill="{RED}"/>'
                             f'<polygon points="{x-50},1440 {x+50},1440 {x},1530" fill="{RED}"/>'
                             f'<text x="{x}" y="1600" text-anchor="middle" font-family="Inter" font-weight="900" font-size="46" fill="{WHITE}">{txt}</text></g>')
scene("sd", D0, D1, cam("sd", f'<rect width="1080" height="1920" fill="{BG}"/>'
      + cabin("d-cab", 540, 1450, 600, 760, fig=figure("d-fig", 0, 360, 1.25, eyes="w"))
      + f'<g id="d-think" opacity="0" style="transform-origin:760px 520px">'
        f'<circle cx="640" cy="760" r="18" fill="{FIG}"/><circle cx="690" cy="680" r="28" fill="{FIG}"/>'
        f'<ellipse cx="800" cy="520" rx="210" ry="130" fill="{FIG}"/>'
        f'<text x="800" y="505" text-anchor="middle" font-family="Inter" font-weight="900" font-size="54" fill="{INK}">HOCH-</text>'
        f'<text x="800" y="565" text-anchor="middle" font-family="Inter" font-weight="900" font-size="54" fill="{INK}">SPRINGEN?</text></g>'
      + f'<g id="d-x" opacity="0" style="transform-origin:540px 1250px"><rect x="490" y="900" width="100" height="700" rx="40" fill="{RED}" transform="rotate(45 540 1250)"/>'
        f'<rect x="490" y="900" width="100" height="700" rx="40" fill="{RED}" transform="rotate(-45 540 1250)"/></g>'
      + arrow("d-a1", 120, "KABINE") + arrow("d-a2", 960, "DU")))
pop("#d-think", t_dein + 0.1, .3, .4)
tw(f'tl.to("#d-think",{{opacity:0,duration:.2}},{t_bringt:.3f});')
tw(f'tl.to("#d-fig",{{y:-170,duration:.28,ease:"power2.out"}},{t_hoch:.3f});')
tw(f'tl.to("#d-fig",{{y:0,duration:.28,ease:"power2.in"}},{t_hoch+0.28:.3f});')
pop("#d-x", t_bringt, .2, 1.6)
tw(f'tl.to("#d-x",{{opacity:0,duration:.2}},{t_faellst - 0.1:.3f});')
tw(f'tl.fromTo("#d-a1",{{opacity:0,y:-80}},{{opacity:1,y:0,duration:.3}},{t_faellst:.3f});')
tw(f'tl.fromTo("#d-a2",{{opacity:0,y:-80}},{{opacity:1,y:0,duration:.3}},{t_faellst:.3f});')
tw(f'tl.to("#d-cab",{{y:"+=60",duration:{D1-t_faellst:.3f},ease:"power1.in"}},{t_faellst:.3f});')

# --- E: „Doch jetzt wird's verrückt“ – Uhr dreht zurück ---
E0, E1 = t_doch, t_genau
ticks = "".join(f'<rect x="535" y="700" width="10" height="40" fill="{SEP_LIGHT}" transform="rotate({i*30} 540 960)"/>' for i in range(12))
scene("se", E0, E1, cam("se", f'<rect width="1080" height="1920" fill="#000"/>'
      + f'<rect id="e-flash" width="1080" height="1920" fill="{RED}" opacity="0"/>'
      + f'<g id="e-clock" opacity="0" style="transform-origin:540px 960px"><circle cx="540" cy="960" r="280" fill="#1a140e" stroke="{SEP_LIGHT}" stroke-width="14"/>{ticks}'
        f'<rect id="e-h1" x="532" y="800" width="16" height="170" rx="8" fill="{SEP_FIG}" style="transform-origin:540px 960px"/>'
        f'<rect id="e-h2" x="534" y="740" width="12" height="230" rx="6" fill="{RED}" style="transform-origin:540px 960px"/></g>'))
tw(f'tl.fromTo("#e-flash",{{opacity:0}},{{opacity:.85,duration:0.001,immediateRender:false}},{E0:.3f});'); tw(f'tl.fromTo("#e-flash",{{immediateRender:false}},{{opacity:0,duration:.35}},{E0:.3f});')
pop("#e-clock", E0 + 0.15, .3, .5)
tw(f'tl.to("#e-h2",{{rotation:-1440,svgOrigin:"540 960",duration:{E1-E0:.3f},ease:"power2.in"}},{E0:.3f});')
tw(f'tl.to("#e-h1",{{rotation:-360,svgOrigin:"540 960",duration:{E1-E0:.3f},ease:"power2.in"}},{E0:.3f});')

# --- F/G/H: Sepia-Skyline, 1945, Bomber + Einschlag (Genau – durchtrennt) ---
F0, F1 = t_genau, t_durch
tower = (f'<g id="f-tower"><rect x="470" y="420" width="140" height="1500" fill="#4a3a28"/>'
         f'<rect x="430" y="700" width="220" height="1220" fill="#433423"/><rect x="390" y="1000" width="300" height="920" fill="#3d2f20"/>'
         f'<rect x="520" y="250" width="40" height="180" fill="#4a3a28"/><rect x="535" y="120" width="10" height="140" fill="#4a3a28"/>'
         + "".join(f'<rect x="{x}" y="{y}" width="14" height="22" fill="{SEP_LIGHT}" opacity=".35"/>' for x in range(410, 680, 34) for y in range(1040, 1900, 60))
         + '</g>')
city = "".join(f'<rect x="{x}" y="{1920-h}" width="{w}" height="{h}" fill="#2e2318"/>' for x, w, h in
               [(0, 160, 600), (150, 120, 820), (700, 150, 700), (840, 120, 900), (950, 130, 640)])
fog = "".join(f'<rect id="f-fog{i}" x="-400" y="{y}" width="1900" height="90" rx="45" fill="{SEP_LIGHT}" opacity=".12"/>' for i, y in enumerate([520, 860, 1180, 1500]))
plane = (f'<g id="f-plane" opacity="0"><rect x="-150" y="-18" width="300" height="36" rx="18" fill="#1d1610"/>'
         f'<polygon points="-30,-10 40,-10 -20,-160 -70,-160" fill="#1d1610"/><polygon points="-30,10 40,10 -20,160 -70,160" fill="#1d1610"/>'
         f'<polygon points="-150,-10 -110,-10 -150,-70" fill="#1d1610"/></g>')
boom = "".join(f'<circle cx="{540+dx}" cy="{900+dy}" r="{r}" fill="{c}"/>' for dx, dy, r, c in
               [(0, 0, 200, "#ff8a3b"), (-90, 50, 130, "#ffb35c"), (100, -40, 140, "#ff6a2b"), (0, 0, 90, "#fff2c4")])
scene("sf", F0, F1, cam("sf", f'<rect width="1080" height="1920" fill="{SEP_BG}"/>'
      + f'<radialGradient id="gf" cx=".5" cy=".3" r=".7"><stop offset="0" stop-color="#4a3926"/><stop offset="1" stop-color="{SEP_BG}"/></radialGradient>'
      + f'<rect width="1080" height="1920" fill="url(#gf)"/>' + tower + city + fog + plane
      + f'<g id="f-boom" opacity="0" style="transform-origin:540px 900px">{boom}</g>'
      + f'<rect id="f-white" width="1080" height="1920" fill="#fff4dc" opacity="0"/>')
      + f'<g id="f-stamp" opacity="0" style="transform-origin:540px 560px">'
        f'<rect x="210" y="440" width="660" height="230" rx="20" fill="#120d08" fill-opacity=".8" stroke="{RED}" stroke-width="10" transform="rotate(-6 540 555)"/>'
        f'<text x="540" y="535" text-anchor="middle" font-family="Inter, sans-serif" font-weight="800" font-size="44" fill="{SEP_FIG}" transform="rotate(-6 540 555)" letter-spacing="6">28. JULI</text>'
        f'<text x="540" y="640" text-anchor="middle" font-family="Inter" font-weight="900" font-size="120" fill="{RED}" transform="rotate(-6 540 555)">1945</text></g>')
for i in range(4):
    tw(f'tl.fromTo("#f-fog{i}",{{x:{-150 if i%2 else 150}}},{{x:{150 if i%2 else -150},duration:{F1-F0:.3f},ease:"none"}},{F0:.3f});')
tw(f'tl.fromTo("#f-stamp",{{opacity:0,scale:2.4,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:.22,ease:"power4.in"}},{t_1945:.3f});')
shake("#sf-cam", t_1945 + 0.22, n=6, amp=14)
tw(f'tl.to("#f-stamp",{{opacity:0,duration:.25}},{t_bomber - 0.15:.3f});')
tw(f'tl.fromTo("#f-plane",{{opacity:0}},{{opacity:1,duration:0.001,immediateRender:false}},{t_bomber - 0.1:.3f});'); tw(f'tl.fromTo("#f-plane",{{immediateRender:false,x:-200,y:700,rotation:6}},{{x:540,y:900,duration:{t_building+0.15-t_bomber:.3f},ease:"power1.in"}},{t_bomber - 0.1:.3f});')
tw(f'tl.set("#f-plane",{{opacity:0}},{t_building + 0.05:.3f});')
tw(f'tl.fromTo("#f-white",{{opacity:0}},{{opacity:.95,duration:0.001,immediateRender:false}},{t_building + 0.05:.3f});'); tw(f'tl.fromTo("#f-white",{{immediateRender:false}},{{opacity:0,duration:.4}},{t_building + 0.05:.3f});')
tw(f'tl.fromTo("#f-boom",{{opacity:0}},{{opacity:1,duration:0.001,immediateRender:false}},{t_building + 0.05:.3f});'); tw(f'tl.fromTo("#f-boom",{{immediateRender:false,scale:.2,svgOrigin:"540 900"}},{{scale:1.25,duration:.5,ease:"power3.out"}},{t_building + 0.05:.3f});')
shake("#sf-cam", t_building + 0.05, n=12, amp=30)

# --- I: Querschnitt Sepia – Seile werden durchtrennt (durchtrennt – In der Kabine) ---
I0, I1 = t_durch, t_inder
scene("si", I0, I1, cam("si", shaft_bg(True)
      + f'<g id="i-top">{ropes("i-rt", rope_xs, 0, 600, SEP_LIGHT)}</g>'
      + f'<g id="i-bot">{ropes("i-rb", rope_xs, 600, 1060, SEP_LIGHT)}</g>'
      + cabin("i-cab", 540, 1350, sep=True)
      + f'<g id="i-cut" opacity="0"><rect x="430" y="585" width="220" height="30" rx="15" fill="{RED}"/></g>'))
tw(f'tl.fromTo("#i-cut",{{opacity:0,scaleX:0}},{{opacity:1,scaleX:1,duration:.15,svgOrigin:"540 600"}},{t_seile1 - 0.1:.3f});')
tw(f'tl.to("#i-top",{{y:-260,duration:.5,ease:"power3.out"}},{t_seile1:.3f});')
tw(f'tl.to("#i-bot",{{y:120,rotation:4,duration:.5,ease:"power3.out",svgOrigin:"540 1060"}},{t_seile1:.3f});')
tw(f'tl.to("#i-cut",{{opacity:0,duration:.3}},{t_seile1 + 0.3:.3f});')
shake("#si-cam", t_seile1, amp=16)
tw(f'tl.to("#i-cab",{{y:"+=40",duration:{I1-t_seile1:.3f},ease:"power2.in"}},{t_seile1:.3f});')

# --- J: Betty Lou Oliver in der Kabine (In der Kabine – Sie stürzt) ---
J0, J1 = t_inder, t_sie
scene("sj", J0, J1, cam("sj", f'<rect width="1080" height="1920" fill="{SEP_BG}"/>'
      + cabin("j-cab", 540, 1300, 620, 800, sep=True, fig=figure("j-fig", 0, 380, 1.3, sep=True, cap=True)))
      + label("j-l1", 540, 300, "LIFTFÜHRERIN", SEP_FIG, 46)
      + label("j-l2", 540, 420, "BETTY LOU OLIVER", RED, 60))
pop("#j-cab", J0, .3, .85)
pop("#j-l1", t_lift)
pop("#j-l2", t_betty)

# --- K: Sturz 75 Stockwerke (Sie stürzt – Und sie überlebt) ---
K0, K1 = t_sie, t_und_ueb
scene("sk", K0, K1, cam("sk", shaft_bg(True) + rail_marks("k-marks", True)
      + cabin("k-cab", 540, 1180, sep=True, fig=figure("k-fig", 0, 270, 0.95, sep=True, cap=True, eyes="w"))
      + "".join(f'<rect id="k-sl{i}" x="{300+i*110}" y="300" width="8" height="260" fill="{SEP_LIGHT}" opacity=".35"/>' for i in range(5))))
floors = list(range(75, 0, -5)) + [1]
fl_t0, fl_t1 = t_75, t_tiefe + 0.5
fv = []
for i, f in enumerate(floors):
    fv.append((fl_t0 + (fl_t1 - fl_t0) * i / len(floors), str(f), RED if i > 0 else SEP_FIG))
SCENES[-1] = (SCENES[-1][0], SCENES[-1][1], SCENES[-1][2], SCENES[-1][3],
              hud("hk", [(K0, "75", SEP_FIG)] + fv[1:], [(K0, "!!", RED)]))
hud_anim("hk", [(K0, "75", SEP_FIG)] + fv[1:], [(K0, "!!", RED)], K1)
tw(f'tl.fromTo("#k-marks",{{y:0}},{{y:-7000,duration:{K1-K0:.3f},ease:"power2.in"}},{K0:.3f});')
for i in range(5):
    tw(f'tl.fromTo("#k-sl{i}",{{y:1400}},{{y:-600,duration:.35,repeat:{int((K1-K0)/0.35)},ease:"none"}},{K0 + i*0.07:.3f});')
for k in range(int((K1 - K0) / 0.12)):
    tw(f'tl.set("#k-cab",{{x:{(-1)**k * 6}}},{K0 + k*0.12:.3f});')

# --- L: „Und sie überlebt.“ ---
L0, L1 = t_und_ueb, t_wie
scene("sl", L0, L1, cam("sl", f'<rect width="1080" height="1920" fill="#000"/>'
      + figure("l-fig", 540, 1000, 1.6, sep=True, eyes="c")
      + f'<path id="l-ecg" d="M 60 1350 L 330 1350 L 380 1250 L 440 1470 L 500 1350 L 620 1350 L 660 1280 L 700 1420 L 740 1350 L 1020 1350" '
        f'fill="none" stroke="{RED}" stroke-width="12" stroke-linejoin="round" style="transform-origin:60px 1350px"/>'))
tw(f'tl.fromTo("#l-fig",{{opacity:0}},{{opacity:1,duration:.5}},{L0:.3f});')
tw(f'tl.fromTo("#l-fig-eyes-c",{{scaleY:.1,transformOrigin:"50% 50%"}},{{scaleY:1,duration:.2}},{t_ueberlebt + 0.3:.3f});')
tw(f'tl.fromTo("#l-ecg",{{scaleX:0,transformOrigin:"0% 50%"}},{{scaleX:1,duration:.8,ease:"none"}},{t_ueberlebt:.3f});')

# --- M: Heute – zurück in deine Kabine (Wie – Erstens) ---
M0, M1 = t_wie, t_erst
scene("sm", M0, M1, cam("sm", shaft_bg() + ropes("m-r", rope_xs, 0, 1060)
      + cabin("m-cab", 540, 1350, fig=figure("m-fig", 0, 270, 0.95, eyes="w"))
      + f'<g id="m-q" opacity="0" style="transform-origin:840px 560px"><circle cx="840" cy="560" r="110" fill="{RED}"/>'
        f'<text x="840" y="610" text-anchor="middle" font-family="Inter" font-weight="900" font-size="150" fill="{WHITE}">?</text></g>')
      + hud("hm", [(M0, "32", WHITE)], [(M0, "0,0", WHITE)])
      + label("m-heute", 300, 560, "HEUTE", RED, 56))
hud_anim("hm", [(M0, "32", WHITE)], [(M0, "0,0", WHITE)], M1)
pop("#m-q", t_wie + 0.05, .3, .3)
pop("#m-heute", t_heute)

# --- N/O: Erstens – 4 bis 8 Tragseile, jedes hält allein (Erstens – Zweitens) ---
N0, N1 = t_erst, t_zweit
six = [465, 495, 525, 555, 585, 615]
glow = "".join(f'<line id="n-g{i}" x1="{x}" y1="0" x2="{x}" y2="1060" stroke="{LAMP}" stroke-width="18" stroke-linecap="round" opacity="0"/>' for i, x in enumerate(six))
scene("sn", N0, N1, cam("sn", shaft_bg() + glow + ropes("n-r", six, 0, 1060)
      + cabin("n-cab", 540, 1350, fig=figure("n-fig", 0, 270, 0.95)))
      + label("n-l", 540, 250, "1  TRAGSEILE", RED, 56)
      + label("n-cnt", 540, 380, "4 – 8", WHITE, 60)
      + label("n-ok", 540, 380, "✓ HÄLT ALLEIN", GREEN, 52))
pop("#n-l", N0)
for i in range(6):
    if i != 2:
        tw(f'tl.set("#n-r-{i}",{{opacity:0}},{N0:.3f});')
        tw(f'tl.fromTo("#n-r-{i}",{{opacity:0}},{{opacity:1,duration:.15}},{t_sondern + 0.12*i:.3f});')
for i in range(6):
    tw(f'tl.fromTo("#n-g{i}",{{opacity:0}},{{opacity:.8,duration:0.001,immediateRender:false}},{t_vier1 + 0.17*i:.3f});'); tw(f'tl.fromTo("#n-g{i}",{{immediateRender:false}},{{opacity:0,duration:.35}},{t_vier1 + 0.17*i:.3f});')
pop("#n-cnt", t_vier1)
tw(f'tl.to("#n-cnt",{{opacity:0,duration:.2}},{t_jedes:.3f});')
for i in range(6):
    if i != 2:
        tw(f'tl.to("#n-r-{i}",{{opacity:0,duration:.25}},{t_jedes + 0.25 + 0.12*i:.3f});')
tw(f'tl.to("#n-g2",{{opacity:.7,duration:.3}},{t_allein:.3f});')
pop("#n-ok", t_allein)

# --- P: Zweitens – das dünne Seil (Zweitens – Doch jetzt reißen) ---
P0, P1 = t_zweit, t_doch2
gov = (f'<g id="p-wheel" style="transform-origin:880px 120px"><circle cx="880" cy="120" r="70" fill="#2b3442" stroke="{ROPE}" stroke-width="10"/>'
       + "".join(f'<rect x="876" y="60" width="8" height="120" fill="{ROPE}" transform="rotate({a} 880 120)"/>' for a in (0, 60, 120))
       + '</g>')
scene("sp", P0, P1, cam("sp", shaft_bg() + ropes("p-r", rope_xs, 0, 1060)
      + f'<line id="p-thin" x1="950" y1="120" x2="950" y2="1920" stroke="{ROPE}" stroke-width="5" stroke-dasharray="40 18"/>'
      + f'<line x1="810" y1="120" x2="810" y2="1200" stroke="{ROPE}" stroke-width="5"/>'
      + f'<rect x="760" y="1185" width="190" height="14" rx="7" fill="{ROPE}"/>' + gov
      + cabin("p-cab", 540, 1350, fig=figure("p-fig", 0, 270, 0.95))
      + f'<ellipse id="p-circ" cx="900" cy="760" rx="120" ry="330" fill="none" stroke="{RED}" stroke-width="9" stroke-dasharray="26 18" opacity="0" style="transform-origin:900px 760px"/>')
      + label("p-l", 540, 250, "2  ???", RED, 60)
      + label("p-kg", 760, 520, "TRÄGT: 0 KG", WHITE, 44))
pop("#p-l", P0)
tw(f'tl.fromTo("#p-circ",{{opacity:0}},{{opacity:1,duration:0.001,immediateRender:false}},{t_duenne:.3f});'); tw(f'tl.fromTo("#p-circ",{{immediateRender:false,scale:.6,transformOrigin:"50% 50%"}},{{scale:1,duration:.3,ease:"back.out(2)"}},{t_duenne:.3f});')
pop("#p-kg", t_traegt)
tw(f'tl.to("#p-kg",{{opacity:0,duration:.2}},{t_laeuft - 0.1:.3f});')
tw(f'tl.to("#p-cab",{{y:-120,duration:{P1-t_laeuft:.3f},ease:"sine.inOut"}},{t_laeuft:.3f});')
tw(f'tl.to("#p-thin",{{attr:{{"stroke-dashoffset":-240}},duration:{P1-t_laeuft:.3f},ease:"sine.inOut"}},{t_laeuft:.3f});')
tw(f'tl.to("#p-wheel",{{rotation:-200,svgOrigin:"880 120",duration:{P1-t_laeuft:.3f},ease:"sine.inOut"}},{t_laeuft:.3f});')

# --- Q: Alle Seile reißen, Kabine fällt, 2-3-4 m/s (Doch – Und genau jetzt) ---
Q0, Q1 = t_doch2, t_und_g
scene("sq", Q0, Q1, cam("sq", shaft_bg() + rail_marks("q-marks")
      + f'<g id="q-top">{ropes("q-rt", rope_xs, 0, 520)}</g>'
      + f'<g id="q-bot">{ropes("q-rb", rope_xs, 520, 1060)}</g>'
      + f'<line id="q-thin" x1="950" y1="0" x2="950" y2="1920" stroke="{ROPE}" stroke-width="5" stroke-dasharray="40 18"/>'
      + f'<g id="q-cut" opacity="0"><rect x="430" y="505" width="220" height="30" rx="15" fill="{RED}"/></g>'
      + cabin("q-cab", 540, 1350, fig=figure("q-fig", 0, 270, 0.95, eyes="w"))))
qs = [(Q0, "0,0", WHITE), (t_kab_f, "1", RED), (t_2ms, "2", RED), (t_3ms, "3", RED), (t_4ms, "4", RED)]
qf = [(Q0, "32", WHITE), (t_kab_f + 0.3, "31", RED), (t_2ms + 0.2, "30", RED), (t_3ms + 0.1, "28", RED), (t_4ms + 0.05, "26", RED)]
SCENES[-1] = (*SCENES[-1][:4], hud("hq", qf, qs))
hud_anim("hq", qf, qs, Q1)
tw(f'tl.fromTo("#q-cut",{{opacity:0,scaleX:0}},{{opacity:1,scaleX:1,duration:.15,svgOrigin:"540 520"}},{t_reissen - 0.1:.3f});')
tw(f'tl.to("#q-top",{{y:-300,duration:.5,ease:"power3.out"}},{t_reissen:.3f});')
tw(f'tl.to("#q-bot",{{y:160,rotation:-5,duration:.5,ease:"power3.out",svgOrigin:"540 1060"}},{t_reissen:.3f});')
tw(f'tl.to("#q-cut",{{opacity:0,duration:.3}},{t_reissen + 0.3:.3f});')
shake("#sq-cam", t_reissen, amp=20)
tw(f'tl.fromTo("#q-marks",{{y:0}},{{y:-6500,duration:{Q1-t_kab_f:.3f},ease:"power2.in"}},{t_kab_f:.3f});')
tw(f'tl.to("#q-bot",{{y:-1600,duration:{Q1-t_kab_f:.3f},ease:"power2.in"}},{t_kab_f:.3f});')
tw(f'tl.to("#q-thin",{{attr:{{"stroke-dashoffset":2400}},duration:{Q1-t_kab_f:.3f},ease:"power2.in"}},{t_kab_f:.3f});')

# --- R: Geschwindigkeitsbegrenzer (Und genau jetzt – Wird die Kabine) ---
R0, R1 = t_und_g, t_wird
big_wheel = (f'<g id="r-wheel" style="transform-origin:540px 620px"><circle cx="540" cy="620" r="270" fill="#2b3442" stroke="{ROPE}" stroke-width="22"/>'
             f'<circle cx="540" cy="620" r="60" fill="{ROPE}"/>'
             + "".join(f'<rect x="530" y="370" width="20" height="500" rx="10" fill="{ROPE}" transform="rotate({a} 540 620)"/>' for a in (0, 45, 90, 135))
             + "".join(f'<circle id="r-fw{i}" cx="{540+150*__import__("math").cos(i*3.1416)}" cy="620" r="34" fill="{LAMP}"/>' for i in range(2))
             + '</g>')
scene("sr", R0, R1, cam("sr", f'<rect width="1080" height="1920" fill="{BG}"/>' + big_wheel
      + f'<line id="r-rope" x1="810" y1="620" x2="810" y2="1920" stroke="{RED}" stroke-width="16" stroke-dasharray="60 26"/>'
      + f'<line x1="270" y1="620" x2="270" y2="1920" stroke="{ROPE}" stroke-width="16"/>')
      + label("r-l1", 540, 1260, "DAS DÜNNE SEIL", RED, 50)
      + label("r-l2", 540, 1400, "2  GESCHWINDIGKEITSBEGRENZER", RED, 40))
tw(f'tl.to("#r-wheel",{{rotation:{360*4},svgOrigin:"540 620",duration:{R1-R0:.3f},ease:"none"}},{R0:.3f});')
tw(f'tl.to("#r-rope",{{attr:{{"stroke-dashoffset":-2600}},duration:{R1-R0:.3f},ease:"none"}},{R0:.3f});')
pop("#r-l1", t_duenne2)
tw(f'tl.to("#r-l1",{{opacity:0,duration:.2}},{t_gesch - 0.2:.3f});')
pop("#r-l2", t_gesch)

# --- S: Rad blockiert → Stahlkeile an die Schienen (Wird – Die Kabine krallt) ---
S0, S1 = t_wird, t_krallt
wedge = lambda wid, x, flip: (f'<polygon id="{wid}" points="{x},1180 {x+flip*90},1220 {x+flip*90},1420 {x},1460" fill="{RED}"/>')
sparks2 = "".join(f'<rect id="s-spk{i}" x="{300 if i<6 else 770}" y="1320" width="30" height="6" rx="3" fill="{LAMP}" opacity="0"/>' for i in range(12))
scene("ss", S0, S1, cam("ss", f'<rect width="1080" height="1920" fill="{BG}"/>'
      + f'<g id="s-top"><g id="s-wheel" style="transform-origin:540px 420px"><circle cx="540" cy="420" r="220" fill="#2b3442" stroke="{ROPE}" stroke-width="20"/>'
        + "".join(f'<rect x="531" y="215" width="18" height="410" rx="9" fill="{ROPE}" transform="rotate({a} 540 420)"/>' for a in (0, 45, 90, 135))
        + f'</g><g id="s-lock" opacity="0" style="transform-origin:540px 420px"><circle cx="540" cy="420" r="250" fill="none" stroke="{RED}" stroke-width="16"/>'
        f'<rect x="760" y="380" width="120" height="80" rx="14" fill="{RED}"/></g></g>'
      + f'<g id="s-bottom" opacity="0">' + shaft_bg().replace('<rect width="1080" height="1920" fill="#10141a"/>', '')
        + cabin("s-cab", 540, 1500, 440, 580)
        + wedge("s-w1", 400, -1) + wedge("s-w2", 680, 1) + sparks2 + '</g>'))
tw(f'tl.to("#s-wheel",{{rotation:720,svgOrigin:"540 420",duration:{t_blockiert-S0:.3f},ease:"none"}},{S0:.3f});')
tw(f'tl.to("#s-wheel",{{rotation:740,svgOrigin:"540 420",duration:.12,ease:"power4.out"}},{t_blockiert:.3f});')
pop("#s-lock", t_blockiert, .15, 1.3)
tw(f'tl.to("#s-top",{{y:-260,scale:.7,duration:.35,ease:"power2.inOut",svgOrigin:"540 0"}},{t_reisst2 - 0.1:.3f});')
tw(f'tl.to("#s-bottom",{{opacity:1,duration:.3}},{t_reisst2 - 0.1:.3f});')
tw(f'tl.fromTo("#s-w1",{{x:120}},{{x:-60,duration:.25,ease:"power4.in"}},{t_keile:.3f});')
tw(f'tl.fromTo("#s-w2",{{x:-120}},{{x:60,duration:.25,ease:"power4.in"}},{t_keile:.3f});')
import math
for i in range(12):
    a = (i % 6) * 0.5 - 1.2
    side = -1 if i < 6 else 1
    tw(f'tl.fromTo("#s-spk{i}",{{opacity:0}},{{opacity:1,duration:0.001,immediateRender:false}},{t_schienen + 0.04*(i%6):.3f});'); tw(f'tl.fromTo("#s-spk{i}",{{immediateRender:false,x:0,y:0}},{{opacity:0,x:{int(side*220*math.cos(a))},y:{int(-220*math.sin(a))},duration:.45}},{t_schienen + 0.04*(i%6):.3f});')
    tw(f'tl.fromTo("#s-spk{i}",{{opacity:0}},{{opacity:1,duration:0.001,immediateRender:false}},{t_schienen + 0.35 + 0.04*(i%6):.3f});'); tw(f'tl.fromTo("#s-spk{i}",{{immediateRender:false,x:0,y:0}},{{opacity:0,x:{int(side*200*math.cos(a+0.3))},y:{int(-200*math.sin(a+0.3))},duration:.45}},{t_schienen + 0.35 + 0.04*(i%6):.3f});')
shake("#ss-cam", t_schienen, n=10, amp=14)

# --- T: Stillstand (Die Kabine krallt – Bei Betty Lou) ---
T0, T1 = t_krallt, t_bei
scene("st", T0, T1, cam("st", shaft_bg() + rail_marks("t-marks")
      + f'<line x1="950" y1="0" x2="950" y2="1920" stroke="{ROPE}" stroke-width="5" stroke-dasharray="40 18"/>'
      + cabin("t-cab", 540, 1350, fig=figure("t-fig", 0, 270, 0.95, eyes="w"))
      + wedge("t-w1", 340, -1).replace("1180", "1050").replace("1220", "1090").replace("1420", "1290").replace("1460", "1330")
      + wedge("t-w2", 740, 1).replace("1180", "1050").replace("1220", "1090").replace("1420", "1290").replace("1460", "1330"))
      + hud("ht", [(T0, "26", RED), (t_still, "25", GREEN)], [(T0, "4", RED), (t_fest, "1,2", RED), (t_nach, "0,4", RED), (t_still, "0,0", GREEN)]))
hud_anim("ht", [(T0, "26", RED), (t_still, "25", GREEN)], [(T0, "4", RED), (t_fest, "1,2", RED), (t_nach, "0,4", RED), (t_still, "0,0", GREEN)], T1)
tw(f'tl.fromTo("#t-marks",{{y:0}},{{y:-900,duration:{t_fest+0.3-T0:.3f},ease:"power3.out"}},{T0:.3f});')
tw(f'tl.fromTo("#t-cab",{{y:0}},{{y:24,duration:.12,yoyo:true,repeat:1}},{t_fest:.3f});')
toggle("#t-fig-eyes-w", T0, t_still + 0.2); toggle("#t-fig-eyes-c", t_still + 0.2)
tw(f'tl.set("#t-fig-eyes-n",{{opacity:0}},{T0:.3f});')
tw(f'tl.set("#t-fig-eyes-c",{{opacity:0}},{T0:.3f});')
tw(f'tl.set("#t-fig-eyes-c",{{opacity:1}},{t_still + 0.2:.3f});')

# --- U: Betty Lou – Seile rollen sich wie eine Feder auf (Bei – Also) ---
U0, U1 = t_bei, t_also
coil = "".join(f'<ellipse cx="540" cy="{1800-i*36}" rx="{230-i*6}" ry="30" fill="none" stroke="{SEP_LIGHT}" stroke-width="12"/>' for i in range(10))
fall_ropes = "".join(f'<path id="u-fr{i}" d="M {470+i*35} -200 C {430+i*35} 200 {560+i*35} 500 {500+i*35} 900" stroke="{SEP_LIGHT}" stroke-width="12" fill="none"/>' for i in range(5))
scene("su", U0, U1, cam("su", shaft_bg(True)
      + f'<g id="u-ropes" opacity="0">{fall_ropes}</g>'
      + f'<g id="u-coil" opacity="0" style="transform-origin:540px 1830px">{coil}</g>'
      + cabin("u-cab", 540, 330, sep=True, fig=figure("u-fig", 0, 270, 0.95, sep=True, cap=True, eyes="w"))
      + f'<rect id="u-dmg" x="390" y="140" width="300" height="70" rx="35" fill="{RED}" opacity="0"/>')
      + label("u-l1", 540, 1250, "BREMSE ZERSTÖRT", RED, 50)
      + label("u-l2", 540, 300, "SEILE = FEDER", SEP_FIG, 56))
pop("#u-l1", t_einschlag)
tw(f'tl.to("#u-l1",{{opacity:0,duration:.2}},{t_gerettet:.3f});')
tw(f'tl.fromTo("#u-ropes",{{opacity:0}},{{opacity:1,duration:0.001,immediateRender:false}},{t_gerettet:.3f});'); tw(f'tl.fromTo("#u-ropes",{{immediateRender:false,y:-900}},{{y:700,duration:1.0,ease:"power2.in"}},{t_gerettet:.3f});')
tw(f'tl.to("#u-ropes",{{opacity:0,duration:.2}},{t_seile3 + 0.5:.3f});')
tw(f'tl.fromTo("#u-coil",{{opacity:0}},{{opacity:1,duration:0.001,immediateRender:false}},{t_seile3 + 0.3:.3f});'); tw(f'tl.fromTo("#u-coil",{{immediateRender:false,scaleY:.1,svgOrigin:"540 1830"}},{{scaleY:1,duration:.6,ease:"power2.out"}},{t_seile3 + 0.3:.3f});')
tw(f'tl.to("#u-cab",{{y:856,duration:.6,ease:"power2.in"}},{t_feder - 0.6:.3f});')
tw(f'tl.to("#u-coil",{{scaleY:.45,svgOrigin:"540 1830",duration:.18,ease:"power2.out"}},{t_feder:.3f});')
tw(f'tl.to("#u-cab",{{y:"+=150",duration:.18,ease:"power2.out"}},{t_feder:.3f});')
tw(f'tl.to("#u-coil",{{scaleY:.8,svgOrigin:"540 1830",duration:.5,ease:"elastic.out(1,.4)"}},{t_feder + 0.18:.3f});')
tw(f'tl.to("#u-cab",{{y:"-=90",duration:.5,ease:"elastic.out(1,.4)"}},{t_feder + 0.18:.3f});')
pop("#u-l2", t_feder)

# --- V: Ende – Aufzug oder Treppe? (Also – Ende) ---
V0, V1 = t_also, TOTAL
stairs = "".join(f'<rect x="{640+i*55}" y="{1500-i*60}" width="{440-i*55}" height="60" fill="#3a4452"/>' for i in range(8))
scene("sv", V0, V1, cam("sv", f'<rect width="1080" height="1920" fill="{BG}"/>'
      + f'<rect x="80" y="1080" width="420" height="540" rx="12" fill="#2b3442" stroke="{CAB_LINE}" stroke-width="8"/>'
      + f'<g id="v-doorL"><rect x="100" y="1100" width="188" height="500" fill="#566173"/></g>'
      + f'<g id="v-doorR"><rect x="292" y="1100" width="188" height="500" fill="#566173"/></g>'
            + stairs + f'<rect x="0" y="1620" width="1080" height="300" fill="#181d25"/>'
      + figure("v-fig", 560, 1700, 1.05, eyes="w"))
      + label("v-l1", 290, 1780, "1  AUFZUG", RED, 50)
      + label("v-l2", 830, 1780, "2  TREPPE", WHITE, 50))
tw(f'tl.to("#v-doorL",{{x:-90,duration:.6,ease:"power2.out"}},{V0 + 0.2:.3f});')
tw(f'tl.to("#v-doorR",{{x:90,duration:.6,ease:"power2.out"}},{V0 + 0.2:.3f});')
pop("#v-l1", t_also + 0.2); pop("#v-l2", t_also + 0.45)
tw(f'tl.fromTo("#v-l1",{{scale:1,transformOrigin:"50% 50%"}},{{scale:1.15,duration:.25,yoyo:true,repeat:3}},{t_aufzug_end:.3f});')
tw(f'tl.to("#v-fig",{{x:-40,duration:.8,ease:"sine.inOut",yoyo:true,repeat:1}},{V0 + 0.8:.3f});')

# ================= UNTERTITEL =================
KEY = {"SEIL", "REISST", "ZWEIUNDDREISSIGSTER", "KNALL", "NICHTS", "VERRÜCKT", "NEUNZEHNHUNDERTFÜNFUNDVIERZIG",
       "BUILDING", "DURCHTRENNT", "OLIVER", "FÜNFUNDSIEBZIG", "ÜBERLEBT", "HEUTE", "VIER", "ACHT", "ALLEIN",
       "DÜNNE", "REISSEN", "FÄLLT", "ZWEI", "DREI", "GESCHWINDIGKEITSBEGRENZER", "BLOCKIERT", "STAHLKEILE",
       "SCHIENEN", "STILLSTAND", "FEDER", "AUFZUG", "EINEM", "BOMBER", "ZERSTÖRT"}
DISPLAY = {"Zweiunddreißigster": "32.", "Neunzehnhundertfünfundvierzig.": "1945.", "fünfundsiebzig": "75"}


def norm(t):
    return re.sub(r"[^\wÄÖÜäöüß]", "", t).upper().replace("ß", "SS")


chunks, cur = [], []
for i, w in enumerate(W):
    cur.append(w)
    text = " ".join(x["t"] for x in cur)
    nxt = W[i+1] if i + 1 < len(W) else None
    end_punct = bool(re.search(r"[.,:?!]$", w["t"]))
    too_long = nxt is not None and len(text) + 1 + len(nxt["t"]) > 18
    gap = nxt is not None and nxt["s"] - w["e"] > 0.25
    if end_punct or len(cur) >= 3 or too_long or gap or nxt is None:
        chunks.append(cur); cur = []

def dur_of(k):
    return (chunks[k+1][0]["s"] if k + 1 < len(chunks) else TOTAL) - chunks[k][0]["s"]
changed = True
while changed:
    changed = False
    for k in range(len(chunks)):
        if dur_of(k) < 0.45:
            j = k + 1 if k + 1 < len(chunks) else k - 1
            a, b = (k, j) if j > k else (j, k)
            merged = chunks[a] + chunks[b]
            if len(merged) <= 4 and len(" ".join(x["t"] for x in merged)) <= 24:
                chunks[a:b+1] = [merged]; changed = True; break
subs = []
for k, c in enumerate(chunks):
    s = c[0]["s"]
    e = chunks[k+1][0]["s"] if k + 1 < len(chunks) else TOTAL
    e = min(e, c[-1]["e"] + 0.6) if k + 1 < len(chunks) else TOTAL
    parts, plain = [], []
    for w in c:
        t = DISPLAY.get(w["t"], w["t"])
        up = t.upper()
        plain.append(up)
        if norm(w["t"]) in KEY:
            parts.append(f'<span class="k">{html.escape(up)}</span>')
        else:
            parts.append(html.escape(up))
    ln = len(" ".join(plain))
    fs = min(104, int(1000 / (0.66 * max(ln, 1))))
    sid = f"sub{k}"
    subs.append(f'<div id="{sid}" class="clip sub" data-start="{s:.3f}" data-duration="{e-s:.3f}" data-track-index="9" '
                f'style="font-size:{fs}px">{" ".join(parts)}</div>')
    tw(f'tl.fromTo("#{sid}",{{scale:.82,opacity:0}},{{scale:1,opacity:1,duration:.09,ease:"power2.out"}},{s:.3f});')

# ================= HTML =================
scene_html = []
for sid, t0, t1, svg_inner, extra in SCENES:
    scene_html.append(
        f'<div id="{sid}" class="clip scene" data-start="{t0:.3f}" data-duration="{t1-t0:.3f}" data-track-index="1">'
        f'<svg viewBox="0 0 1080 1920" width="1080" height="1920" xmlns="http://www.w3.org/2000/svg">{svg_inner}{extra}</svg></div>')

doc = f'''<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Aufzugseil reißt</title>
    <script src="assets/gsap.min.js"></script>
    <style>
      :root {{ --ground: {BG}; --ink: #ffffff; --signal: {RED}; --font-display: "Inter", sans-serif; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: var(--ground); }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: var(--font-display); }}
      .scene {{ position: absolute; inset: 0; }}
      .scene svg {{ display: block; }}
      .scene svg g, .scene svg rect, .scene svg circle, .scene svg path, .scene svg ellipse, .scene svg polygon, .scene svg line {{ transform-box: view-box; }}
      .sub {{
        position: absolute; left: 40px; right: 40px; top: 960px; transform-origin: 50% 50%;
        margin-top: -0.6em; text-align: center; color: var(--ink); font-weight: 900; line-height: 1.1;
        letter-spacing: -0.01em; white-space: nowrap; z-index: 10;
        -webkit-text-stroke: 14px #000; paint-order: stroke fill;
        text-shadow: 0 6px 0 #000, 0 0 30px rgba(0,0,0,.65);
      }}
      .sub .k {{ color: var(--signal); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <audio id="vo" class="clip" data-start="0" data-duration="80.24" data-volume="1" src="assets/voiceover.mp3"></audio>
      <audio id="sfx" class="clip" data-start="0" data-duration="{TOTAL}" data-volume="0.45" src="assets/sfx_bed.wav"></audio>
      {"".join(scene_html)}
      {"".join(subs)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {chr(10).join("      " + t for t in T)}
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
'''
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(doc)
json.dump({k: v for k, v in globals().items() if k.startswith("t_") and isinstance(v, float)},
          open(os.path.join(HERE, "assets/cues.json"), "w"), indent=1)
print(f"Szenen: {len(SCENES)}, Untertitel: {len(subs)}, Tweens: {len(T)}")
