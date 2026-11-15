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


def pop(sel, t, dur=0.32, frm=0.88):
    tw(f'tl.fromTo("{sel}",{{opacity:0,scale:{frm},transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:{dur},ease:"power3.out"}},{t:.3f});')


def shake(sel, t, n=8, amp=18, step=0.035):
    n = min(n, 6); amp = amp * 0.45; step = 0.06
    for i in range(n):
        x = amp * (1 if i % 2 == 0 else -1) * (1 - i / n)
        tw(f'tl.to("{sel}",{{x:{x:.1f},y:{-x/3:.1f},duration:{step},ease:"sine.inOut"}},{t + i*step:.3f});')
    tw(f'tl.to("{sel}",{{x:0,y:0,duration:.12,ease:"sine.out"}},{t + n*step:.3f});')


def drift(sel, t0, t1, s0=1.0, s1=1.07):
    tw(f'tl.fromTo("{sel}",{{scale:{s0},svgOrigin:"540 960"}},{{scale:{s1},duration:{t1-t0:.3f},ease:"none"}},{t0:.3f});')


# ---------- SVG-Bausteine ----------
FIGS = []
import random as _r
RNG = _r.Random(42)  # fester Seed → deterministisch
def figure(fid, x, y, s=1.0, sep=False, cap=False, eyes="n"):
    """Gesichtslose Gliederpuppe (Skill: Emotion nur über Augen/Brauen). Füße bei (x,y)."""
    F = SEP_FIG if sep else FIG
    E = "#2a2016" if sep else INK
    capsvg = ""
    if cap:
        capsvg = (f'<rect x="-58" y="-392" width="116" height="36" rx="8" fill="#5a4630"/>'
                  f'<rect x="-70" y="-362" width="140" height="12" rx="6" fill="#4a3826"/>')
    FIGS.append(fid)
    if cap:   # Liftführerin 1945: Uniformjacke, Messingknöpfe, dunkle Hose
        H, H2, P, SH = ("#6e3b2a", "#57301f", "#2e241b", "#1d1610")
        jacket = ('<rect x="-3" y="-250" width="6" height="128" fill="#57301f"/>'
                  + "".join(f'<circle cx="0" cy="{y}" r="6" fill="#c9a24b"/>' for y in (-228, -198, -168, -138))
                  + '<rect x="-62" y="-150" width="124" height="12" fill="#2a1d13"/><rect x="-10" y="-152" width="20" height="16" rx="3" fill="#c9a24b"/>')
        collar = '<polygon points="-30,-262 0,-228 -8,-262" fill="#e6d2ad"/><polygon points="30,-262 0,-228 8,-262" fill="#e6d2ad"/>'
    else:     # Standard-Outfit: Petrol-Hoodie, Jeans, helle Sneaker
        H, H2, P, SH = (("#4f6a5c", "#3f5649", "#2f3a4a", "#d8ccb0") if sep else ("#2f6f73", "#265b5e", "#2c3a52", "#eef0f3"))
        jacket = ('<ellipse cx="0" cy="-252" rx="46" ry="16" fill="#1f4b4e"/>'
                  '<rect x="-12" y="-248" width="4" height="40" rx="2" fill="#e6e9ee"/><rect x="8" y="-248" width="4" height="40" rx="2" fill="#e6e9ee"/>'
                  '<rect x="-40" y="-178" width="80" height="34" rx="12" fill="#265b5e"/>')
        collar = ""
    o_n = 1 if eyes == "n" else 0
    o_w = 1 if eyes == "w" else 0
    o_c = 1 if eyes == "c" else 0
    return f'''
<g id="{fid}"><g transform="translate({x},{y}) scale({s})">
  <ellipse cx="0" cy="4" rx="78" ry="15" fill="#000" opacity=".38"/>
  <g id="{fid}-body">
  <rect x="-34" y="-128" width="27" height="124" rx="12" fill="{P}"/>
  <rect x="7" y="-128" width="27" height="124" rx="12" fill="{P}"/>
  <rect x="-28" y="-60" width="4" height="50" rx="2" fill="#000" opacity=".18"/><rect x="24" y="-60" width="4" height="50" rx="2" fill="#000" opacity=".18"/>
  <ellipse cx="-22" cy="-6" rx="25" ry="12" fill="{SH}"/><ellipse cx="22" cy="-6" rx="25" ry="12" fill="{SH}"/>
  <rect x="-44" y="-12" width="44" height="6" rx="3" fill="#000" opacity=".25"/><rect x="0" y="-12" width="44" height="6" rx="3" fill="#000" opacity=".25"/>
  <rect x="-62" y="-258" width="124" height="152" rx="36" fill="{H}"/>
  <rect x="-62" y="-128" width="124" height="18" rx="9" fill="{H2}"/>
  {jacket}
  <rect x="-88" y="-248" width="28" height="112" rx="13" fill="{H}" id="{fid}-armL"/>
  <rect x="60" y="-248" width="28" height="112" rx="13" fill="{H}" id="{fid}-armR"/>
  <rect x="-88" y="-150" width="28" height="14" rx="6" fill="{H2}"/><rect x="60" y="-150" width="28" height="14" rx="6" fill="{H2}"/>
  <circle cx="-74" cy="-126" r="13" fill="{F}"/><circle cx="74" cy="-126" r="13" fill="{F}"/>
  <rect x="-12" y="-278" width="24" height="26" rx="8" fill="{F}"/>
  {collar}
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
  <rect x="{-w/2+18}" y="{-h/2+26}" width="{w}" height="{h}" rx="18" fill="#000" opacity=".35"/>
  <rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" rx="18" fill="{C}" stroke="{L}" stroke-width="8"/>
  <rect x="{-w/2+24}" y="{-h/2+24}" width="{w-48}" height="{h-48}" rx="8" fill="{'#2d241a' if sep else '#222a35'}"/>
  <rect x="{-w/2+24}" y="{-h/2+24}" width="{w-48}" height="{h-48}" rx="8" fill="url(#cabshade)"/>
  {"".join(f'<rect x="{-w/2+40+i*((w-80)/6):.0f}" y="{-h/2+70}" width="3" height="{h-150}" fill="#000" opacity=".18"/>' for i in range(7))}
  <ellipse cx="0" cy="{-h/2+60}" rx="{w*0.42:.0f}" ry="{h*0.38:.0f}" fill="url({'#lampglowS' if sep else '#lampglow'})"/>
  <rect{lid} x="-90" y="{-h/2+30}" width="180" height="16" rx="8" fill="{lamp}"/>
  <rect x="{w/2-74}" y="{-h/2+140}" width="34" height="110" rx="8" fill="{'#4a3a28' if sep else '#3a4555'}"/>
  <circle cx="{w/2-57}" cy="{-h/2+165}" r="8" fill="{RED}"/><circle cx="{w/2-57}" cy="{-h/2+195}" r="8" fill="{'#2a2016' if sep else '#1a2029'}"/><circle cx="{w/2-57}" cy="{-h/2+225}" r="8" fill="{'#2a2016' if sep else '#1a2029'}"/>
  <rect x="{-w/2+30}" y="{h/2-200}" width="{w-60}" height="10" rx="5" fill="{L}" opacity=".85"/>
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
    pan = "#2a2118" if sep else "#171c24"
    seam = "#3a2d1f" if sep else "#252d39"
    bolt = "#5a4630" if sep else "#3a4452"
    walls = ""
    for x0, w in ((0, 250), (830, 250)):
        for y in range(0, 1920, 320):
            walls += (f'<rect x="{x0+8}" y="{y+8}" width="{w-16}" height="304" rx="6" fill="{pan}" stroke="{seam}" stroke-width="4"/>'
                      + "".join(f'<circle cx="{x0+cx}" cy="{y+cy}" r="6" fill="{bolt}"/>' for cx in (26, w-26) for cy in (26, 290)))
    # Etagenschilder an der Schachtwand
    plates = "".join(f'<g opacity=".55" data-layout-ignore="true"><rect x="36" y="{y}" width="150" height="70" rx="10" fill="{seam}"/>'
                     f'<text x="111" y="{y+52}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-weight="800" font-size="46" fill="{"#8a6f4e" if sep else "#5d6b7d"}">{n}</text></g>'
                     for y, n in ((260, "33"), (900, "32"), (1540, "31")))
    # Kabel mit Halterungen
    cables = (f'<path d="M 920 0 C 940 400 900 800 930 1200 S 910 1700 925 1920" stroke="#0b0e12" stroke-width="14" fill="none" opacity=".9"/>'
              f'<path d="M 960 0 C 975 500 945 900 968 1300 S 950 1750 962 1920" stroke="{RED if not sep else "#7a3a1e"}" stroke-width="7" fill="none" opacity=".55"/>'
              + "".join(f'<rect x="900" y="{y}" width="80" height="14" rx="4" fill="{bolt}"/>' for y in range(150, 1920, 420)))
    # Schachttür-Rahmen + Warnstreifen
    door = (f'<rect x="842" y="700" width="60" height="420" fill="{bg}" stroke="{seam}" stroke-width="6"/>'
            + "".join(f'<rect x="842" y="{700+i*42}" width="60" height="20" fill="{RED if not sep else "#7a3a1e"}" opacity=".35" transform="skewY(-30)" style="transform-origin:842px {700+i*42}px"/>' for i in range(10)))
    beam = f'<polygon points="470,0 610,0 760,1920 320,1920" fill="url(#beam{"S" if sep else ""})" opacity=".55"/>'
    return f'''
<rect width="1080" height="1920" fill="{bg}"/>
{walls}{plates}{cables}{door}
<rect x="250" y="0" width="580" height="1920" fill="{sh}"/>
{"".join(f'<rect x="{x}" y="0" width="2" height="1920" fill="#000" opacity=".25"/>' for x in range(330, 760, 70))}
{beam}
<rect x="286" y="0" width="16" height="1920" fill="{rl}"/>
<rect x="778" y="0" width="16" height="1920" fill="{rl}"/>
{"".join(f'<rect x="280" y="{y}" width="28" height="10" fill="{bolt}"/><rect x="772" y="{y}" width="28" height="10" fill="{bolt}"/>' for y in range(60, 1920, 240))}
<rect x="250" y="0" width="580" height="1920" fill="url(#shaftshade)"/>'''


def machine_bg():
    """Maschinenraum: Wandpaneele, Rohre, Motor, Warnstreifen."""
    pan = "".join(f'<rect x="{x+8}" y="{y+8}" width="344" height="464" rx="8" fill="#151a21" stroke="#232b36" stroke-width="4"/>'
                  + "".join(f'<circle cx="{x+cx}" cy="{y+cy}" r="7" fill="#3a4452"/>' for cx in (30, 330) for cy in (30, 450))
                  for x in (0, 360, 720) for y in (0, 480, 960, 1440))
    pipes = ('<rect x="0" y="1060" width="1080" height="34" fill="#2b3442"/><rect x="0" y="1112" width="1080" height="20" fill="#232b36"/>'
             + "".join(f'<rect x="{x}" y="1050" width="20" height="54" rx="4" fill="#4a5563"/>' for x in range(60, 1080, 200)))
    stripes = '<g opacity=".8">' + "".join(f'<polygon points="{x},1840 {x+60},1840 {x+20},1920 {x-40},1920" fill="{RED}"/>' for x in range(-40, 1120, 120)) + '</g>'
    motor = ('<rect x="340" y="1500" width="400" height="260" rx="22" fill="#232b36" stroke="#3a4452" stroke-width="8"/>'
             + "".join(f'<rect x="380" y="{y}" width="320" height="10" rx="5" fill="#151a21"/>' for y in range(1540, 1720, 30))
             + f'<circle id="led-{len(FIGS)}-{RNG.randint(0,9999)}" class="blink" cx="710" cy="1530" r="10" fill="{RED}"/>'
             + '<rect x="380" y="1470" width="320" height="30" rx="8" fill="#151a21"/>'
             '<text x="540" y="1494" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="22" fill="#7d8896" letter-spacing="5">MASCHINENRAUM</text>')
    return (f'<rect width="1080" height="1920" fill="{BG}"/>{pan}'
            f'<rect width="1080" height="1920" fill="url(#roomshade)"/>{pipes}{motor}<rect x="0" y="1840" width="1080" height="80" fill="#0b0e12"/>{stripes}')


def rail_marks(mid, sep=False, span=9000):
    rl = SEP_LINE if sep else RAIL
    marks = "".join(f'<rect x="250" y="{y}" width="580" height="10" fill="{rl}" opacity=".35"/>'
                    f'<rect x="270" y="{y+120}" width="50" height="6" fill="{rl}" opacity=".6"/>'
                    f'<rect x="760" y="{y+120}" width="50" height="6" fill="{rl}" opacity=".6"/>'
                    for y in range(-200, span, 300))
    return f'<g id="{mid}">{marks}</g>'


def label(lid, x, y, text, col=RED, size=40, anchor="middle", op=0, fill_bg=True):
    tw_ = len(text) * size * 0.68 + 48
    if anchor == "middle":
        rx = x - tw_/2
    elif anchor == "start":
        rx = x - 22
    else:
        rx = x - tw_ + 22
    bg = (f'<rect x="{rx:.0f}" y="{y-size*0.95:.0f}" width="{tw_:.0f}" height="{size*1.4:.0f}" rx="{size*0.7:.0f}" '
          f'fill="#0b0e12" fill-opacity=".85" stroke="{col}" stroke-width="5"/>') if fill_bg else ""
    return (f'<g id="{lid}" opacity="{op}" style="transform-box:fill-box;transform-origin:center">{bg}'
            f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Poppins, sans-serif" '
            f'font-weight="700" font-size="{size}" fill="{col}">{html.escape(text)}</text></g>')


def hud(hid, floor_vals, speed_vals):
    """Diegetische Anzeige oben: Etage + Geschwindigkeit. *_vals: [(t, text, color)]"""
    out = [f'<g id="{hid}" transform="translate(0,90)">',
           '<rect x="190" y="110" width="700" height="210" rx="34" fill="#0b0e12" stroke="#3a4452" stroke-width="6"/>',
           '<text x="365" y="165" text-anchor="middle" font-family="Poppins, sans-serif" font-weight="700" font-size="30" fill="#7d8896" letter-spacing="4">ETAGE</text>',
           '<text x="715" y="165" text-anchor="middle" font-family="Poppins, sans-serif" font-weight="700" font-size="30" fill="#7d8896" letter-spacing="4">TEMPO M/S</text>',
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
XF = 0.3  # Überblendung zwischen Szenen (s)


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
        f'<text x="540" y="560" text-anchor="middle" font-family="Poppins" font-weight="900" font-size="120" fill="{RED}">KNALL!</text></g>'
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
                             f'<text x="{x}" y="1600" text-anchor="middle" font-family="Poppins" font-weight="900" font-size="46" fill="{WHITE}">{txt}</text></g>')
scene("sd", D0, D1, cam("sd", shaft_bg()
      + cabin("d-cab", 540, 1450, 600, 760, fig=figure("d-fig", 0, 360, 1.25, eyes="w"))
      + f'<g id="d-think" opacity="0" style="transform-origin:760px 520px">'
        f'<circle cx="640" cy="760" r="18" fill="{FIG}"/><circle cx="690" cy="680" r="28" fill="{FIG}"/>'
        f'<ellipse cx="800" cy="520" rx="210" ry="130" fill="{FIG}"/>'
        f'<text x="800" y="505" text-anchor="middle" font-family="Poppins" font-weight="900" font-size="54" fill="{INK}">HOCH-</text>'
        f'<text x="800" y="565" text-anchor="middle" font-family="Poppins" font-weight="900" font-size="54" fill="{INK}">SPRINGEN?</text></g>'
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
YEARS = ["2026", "2003", "1987", "1971", "1958", "19??"]
scene("se", E0, E1, cam("se", f'<rect width="1080" height="1920" fill="#000"/>'
      + "".join(f'<rect x="537" y="300" width="6" height="200" fill="{SEP_LIGHT}" opacity=".18" transform="rotate({a} 540 960)"/>' for a in range(0, 360, 15))
      + f'<circle id="e-ring" cx="540" cy="960" r="360" fill="none" stroke="{RED}" stroke-width="6" stroke-dasharray="30 22" opacity=".7"/>'
      + "".join(f'<text id="e-y{i}" x="540" y="1440" text-anchor="middle" font-family="JetBrains Mono, monospace" font-weight="800" font-size="110" fill="{SEP_FIG if i < 5 else RED}" opacity="0">{y}</text>' for i, y in enumerate(YEARS))
      + f'<rect id="e-flash" width="1080" height="1920" fill="{RED}" opacity="0"/>'
      + f'<g id="e-clock" opacity="0" style="transform-origin:540px 960px"><circle cx="540" cy="960" r="280" fill="#1a140e" stroke="{SEP_LIGHT}" stroke-width="14"/>{ticks}'
        f'<rect id="e-h1" x="532" y="800" width="16" height="170" rx="8" fill="{SEP_FIG}" style="transform-origin:540px 960px"/>'
        f'<rect id="e-h2" x="534" y="740" width="12" height="230" rx="6" fill="{RED}" style="transform-origin:540px 960px"/></g>'))
tw(f'tl.fromTo("#e-flash",{{opacity:0}},{{opacity:.85,duration:0.001,immediateRender:false}},{E0:.3f});'); tw(f'tl.fromTo("#e-flash",{{immediateRender:false}},{{opacity:0,duration:.35}},{E0:.3f});')
pop("#e-clock", E0 + 0.15, .3, .5)
tw(f'tl.to("#e-h2",{{rotation:-1440,svgOrigin:"540 960",duration:{E1-E0:.3f},ease:"power2.in"}},{E0:.3f});')
tw(f'tl.to("#e-ring",{{rotation:-180,svgOrigin:"540 960",duration:{E1-E0:.3f},ease:"power1.in"}},{E0:.3f});')
for i in range(len(YEARS)):
    a = E0 + (E1 - E0) * i / len(YEARS)
    toggle(f"#e-y{i}", a, E0 + (E1 - E0) * (i + 1) / len(YEARS) if i < len(YEARS) - 1 else None)
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
      + f'<rect width="1080" height="1920" fill="url(#gf)"/>' + f'<polygon id="f-sl1" points="200,1920 230,1920 -200,200 -60,160" fill="{SEP_LIGHT}" opacity=".12"/>'
      + f'<polygon id="f-sl2" points="880,1920 910,1920 1300,260 1140,200" fill="{SEP_LIGHT}" opacity=".12"/>'
      + tower + city + fog + plane
      + f'<g id="f-boom" opacity="0" style="transform-origin:540px 900px">{boom}</g>'
      + f'<rect id="f-white" width="1080" height="1920" fill="#fff4dc" opacity="0"/>')
      + f'<g id="f-stamp" opacity="0" style="transform-origin:540px 560px">'
        f'<rect x="210" y="440" width="660" height="230" rx="20" fill="#120d08" fill-opacity=".8" stroke="{RED}" stroke-width="10" transform="rotate(-6 540 555)"/>'
        f'<text x="540" y="535" text-anchor="middle" font-family="Poppins, sans-serif" font-weight="800" font-size="44" fill="{SEP_FIG}" transform="rotate(-6 540 555)" letter-spacing="6">28. JULI</text>'
        f'<text x="540" y="640" text-anchor="middle" font-family="Poppins" font-weight="900" font-size="120" fill="{RED}" transform="rotate(-6 540 555)">1945</text></g>')
tw(f'tl.fromTo("#f-sl1",{{rotation:-8}},{{rotation:10,svgOrigin:"215 1920",duration:{F1-F0:.3f},ease:"sine.inOut"}},{F0:.3f});')
tw(f'tl.fromTo("#f-sl2",{{rotation:9}},{{rotation:-12,svgOrigin:"895 1920",duration:{F1-F0:.3f},ease:"sine.inOut"}},{F0:.3f});')
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
      + "".join(f'<rect x="{x}" y="0" width="6" height="1920" fill="{SEP_LINE}" opacity=".25"/>' for x in range(30, 1080, 70))
      + "".join(f'<polygon points="{x},520 {x+35},470 {x+70},520" fill="none" stroke="{SEP_LINE}" stroke-width="4" opacity=".4"/>' for x in range(0, 1080, 70))
      + f'<g><path d="M 400 760 A 140 140 0 0 1 680 760" fill="#1a140e" stroke="{SEP_LIGHT}" stroke-width="10"/>'
      + "".join(f'<rect x="537" y="630" width="6" height="22" fill="{SEP_LIGHT}" transform="rotate({a} 540 760)"/>' for a in range(-80, 81, 20))
      + f'<rect id="j-needle" x="536" y="650" width="8" height="112" rx="4" fill="{RED}" transform="rotate(62 540 760)"/><circle cx="540" cy="760" r="14" fill="{SEP_LIGHT}"/></g>'
      + cabin("j-cab", 540, 1300, 620, 800, sep=True, fig=figure("j-fig", 0, 380, 1.3, sep=True, cap=True)))
      + label("j-l1", 540, 300, "LIFTFÜHRERIN", SEP_FIG, 46)
      + label("j-l2", 540, 420, "BETTY LOU OLIVER", RED, 60))
pop("#j-cab", J0, .3, .85)
pop("#j-l1", t_lift)
tw(f'tl.fromTo("#j-needle",{{rotation:0}},{{rotation:-6,svgOrigin:"540 760",duration:.15,yoyo:true,repeat:{int((J1-J0)/0.15)},ease:"sine.inOut"}},{J0:.3f});')
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
    tw(f'tl.to("#k-cab",{{x:{(-1)**k * 3},duration:.12,ease:"sine.inOut"}},{K0 + k*0.12:.3f});')

# --- L: „Und sie überlebt.“ ---
L0, L1 = t_und_ueb, t_wie
scene("sl", L0, L1, cam("sl", f'<rect width="1080" height="1920" fill="#000"/>'
      + f'<polygon points="470,0 610,0 900,1100 180,1100" fill="url(#beamS)" opacity=".8"/><ellipse cx="540" cy="1010" rx="260" ry="40" fill="{SEP_LIGHT}" opacity=".18"/>'
      + figure("l-fig", 540, 1000, 1.6, sep=True, cap=True, eyes="c")
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
        f'<text x="840" y="610" text-anchor="middle" font-family="Poppins" font-weight="900" font-size="150" fill="{WHITE}">?</text></g>')
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
scene("sr", R0, R1, cam("sr", machine_bg() + big_wheel
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
scene("ss", S0, S1, cam("ss", machine_bg()
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
      + "".join(f'<rect x="{x}" y="{y}" width="116" height="116" rx="6" fill="#151a21" stroke="#1d232c" stroke-width="4"/>' for x in range(0, 1080, 120) for y in range(0, 1620, 120))
      + f'<polygon points="500,0 580,0 860,1620 220,1620" fill="url(#beam)" opacity=".5"/><rect x="470" y="0" width="140" height="26" rx="10" fill="{LAMP}"/>'
      + f'<rect x="510" y="1260" width="44" height="80" rx="10" fill="#0b0e12" stroke="#3a4452" stroke-width="4"/><circle id="v-btn" cx="532" cy="1300" r="12" fill="{RED}"/>'
      + "".join(f'<rect x="{x}" y="1620" width="236" height="300" fill="{"#1a2029" if (x//240)%2 else "#161b22"}"/>' for x in range(0, 1080, 240))
      + f'<rect x="100" y="1630" width="380" height="120" fill="#566173" opacity=".08"/>'
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
        up = t
        plain.append(up)
        if norm(w["t"]) in KEY:
            parts.append(f'<span class="k">{html.escape(up)}</span>')
        else:
            parts.append(html.escape(up))
    ln = len(" ".join(plain))
    fs = min(62, int(980 / (0.56 * max(ln, 1))))
    sid = f"sub{k}"
    subs.append(f'<div id="{sid}" class="clip sub" data-start="{s:.3f}" data-duration="{e-s:.3f}" data-track-index="9" '
                f'style="font-size:{fs}px">{" ".join(parts)}</div>')
    tw(f'tl.fromTo("#{sid}",{{y:14,opacity:0}},{{y:0,opacity:1,duration:.16,ease:"power2.out"}},{s:.3f});')


# ================= GLOBALE EBENEN (Skill 6a) =================
import zlib, struct, base64


def noise_png(n=256, seed=3):
    rr = _r.Random(seed)
    raw = b"".join(b"\x00" + bytes(v for _ in range(n) for v in (lambda g: (g, g, g, rr.randint(0, 38)))(rr.randint(0, 255))) for _ in range(n))
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", n, n, 8, 6, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
    return base64.b64encode(png).decode()


DEFS = f"""<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<radialGradient id="lampglow" cx=".5" cy="0" r="1"><stop offset="0" stop-color="{LAMP}" stop-opacity=".45"/><stop offset="1" stop-color="{LAMP}" stop-opacity="0"/></radialGradient>
<radialGradient id="lampglowS" cx=".5" cy="0" r="1"><stop offset="0" stop-color="{SEP_LIGHT}" stop-opacity=".45"/><stop offset="1" stop-color="{SEP_LIGHT}" stop-opacity="0"/></radialGradient>
<linearGradient id="cabshade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".06"/><stop offset="1" stop-color="#000" stop-opacity=".35"/></linearGradient>
<linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{LAMP}" stop-opacity=".22"/><stop offset="1" stop-color="{LAMP}" stop-opacity="0"/></linearGradient>
<linearGradient id="beamS" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{SEP_LIGHT}" stop-opacity=".3"/><stop offset="1" stop-color="{SEP_LIGHT}" stop-opacity="0"/></linearGradient>
<linearGradient id="shaftshade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".55"/><stop offset=".3" stop-color="#000" stop-opacity="0"/><stop offset=".75" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".6"/></linearGradient>
<radialGradient id="roomshade" cx=".5" cy=".35" r=".8"><stop offset="0" stop-color="#2b3442" stop-opacity=".5"/><stop offset="1" stop-color="#000" stop-opacity=".6"/></radialGradient>
<radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".7"/></radialGradient>
<radialGradient id="redvig" cx=".5" cy=".5" r=".72"><stop offset=".5" stop-color="{RED}" stop-opacity="0"/><stop offset="1" stop-color="{RED}" stop-opacity=".75"/></radialGradient>
<radialGradient id="sepvig" cx=".5" cy=".5" r=".75"><stop offset=".45" stop-color="#2a1a08" stop-opacity="0"/><stop offset="1" stop-color="#1a0f04" stop-opacity=".85"/></radialGradient>
</defs></svg>"""

OVER = []  # zusätzliche Clip-Ebenen über den Szenen (unter den Untertiteln)

# Staub + Vignette über dem ganzen Video
dust = []
for i in range(46):
    x = RNG.randint(0, 1080); y = RNG.randint(0, 1920); r = RNG.choice([2, 3, 3, 4, 5, 7])
    op = RNG.uniform(.15, .45)
    dust.append(f'<circle id="dust{i}" cx="{x}" cy="{y}" r="{r}" fill="#fff4dc" opacity="{op:.2f}"/>')
    dur = RNG.uniform(6, 14); dx = RNG.randint(-80, 80)
    tw(f'tl.fromTo("#dust{i}",{{x:0,y:0}},{{x:{dx},y:{-RNG.randint(250, 600)},duration:{dur:.2f},ease:"none",repeat:{int(TOTAL/dur)+1},yoyo:true}},0);')
OVER.append(f'<div id="ov-dust" class="clip ov" data-start="0" data-duration="{TOTAL}" data-track-index="5" style="z-index:5">'
            f'<svg viewBox="0 0 1080 1920" width="1080" height="1920">{"".join(dust)}<rect width="1080" height="1920" fill="url(#vig)"/></svg></div>')

# Filmkorn (gekachelte Rauschtextur, ruckelt alle 0,1 s)
OVER.append(f'<div id="ov-grain" class="clip ov" data-start="0" data-duration="{TOTAL}" data-track-index="6" '
            f'style="z-index:6;left:-128px;top:-128px;width:1336px;height:2176px;opacity:.28;mix-blend-mode:overlay;'
            f'background-image:url(data:image/png;base64,{noise_png()});background-size:256px 256px"></div>')
k = 0
t = 0.0
while t < TOTAL:
    tw(f'tl.set("#ov-grain",{{x:{RNG.randint(-120, 120)},y:{RNG.randint(-120, 120)}}},{t:.2f});')
    t += 0.1; k += 1

# Archiv-Look für die Rückblenden (Filmrand, Kratzer, Sepia-Vignette, Flackern)
def archive(aid, t0, t1):
    perf = "".join(f'<rect x="14" y="{y}" width="34" height="46" rx="8" fill="#0d0905"/><rect x="1032" y="{y}" width="34" height="46" rx="8" fill="#0d0905"/>' for y in range(10, 1920, 90))
    scr = "".join(f'<rect id="{aid}-sc{i}" x="0" y="0" width="3" height="1920" fill="#f3e2c0" opacity="0"/>' for i in range(3))
    OVER.append(f'<div id="{aid}" class="clip ov" data-start="{t0:.3f}" data-duration="{t1-t0:.3f}" data-track-index="7" style="z-index:7">'
                f'<svg viewBox="0 0 1080 1920" width="1080" height="1920"><rect width="1080" height="1920" fill="url(#sepvig)"/>'
                f'<rect x="0" y="0" width="62" height="1920" fill="#1a120a" opacity=".9"/><rect x="1018" y="0" width="62" height="1920" fill="#1a120a" opacity=".9"/>{perf}{scr}'
                f'<rect id="{aid}-fl" width="1080" height="1920" fill="#fff1d0" opacity="0"/>'
                f'<g opacity=".85"><circle cx="110" cy="1820" r="10" fill="{RED}"/><text x="132" y="1832" font-family="JetBrains Mono, monospace" font-weight="800" font-size="32" fill="{SEP_FIG}">ARCHIV · 1945</text></g></svg></div>')
    tt = t0; j = 0
    while tt < t1:
        for i in range(3):
            on = RNG.random() < 0.55
            tw(f'tl.set("#{aid}-sc{i}",{{opacity:{RNG.uniform(.08,.2) if on else 0:.2f},x:{RNG.randint(80, 1000)}}},{tt:.2f});')
        tw(f'tl.to("#{aid}-fl",{{opacity:{RNG.choice([0, .02, .04]):.2f},duration:.3,ease:"sine.inOut"}},{tt:.2f});')
        tt += 0.3; j += 1

archive("ov-arch1", t_genau, t_wie)
archive("ov-arch2", t_bei, t_also)

# Gefahr: rot pulsierende Vignette + Warnsymbole
def danger(did, t0, t1):
    tri = lambda x: (f'<g transform="translate({x},560)"><polygon points="0,-60 62,48 -62,48" fill="{RED}"/>'
                     f'<rect x="-7" y="-28" width="14" height="46" rx="6" fill="#fff"/><circle cx="0" cy="32" r="8" fill="#fff"/></g>')
    OVER.append(f'<div id="{did}" class="clip ov" data-start="{t0:.3f}" data-duration="{t1-t0:.3f}" data-track-index="8" style="z-index:8">'
                f'<svg viewBox="0 0 1080 1920" width="1080" height="1920"><rect id="{did}-v" width="1080" height="1920" fill="url(#redvig)" opacity=".3"/>'
                f'<g id="{did}-w">{tri(110)}{tri(970)}</g></svg></div>')
    tw(f'tl.fromTo("#{did}-v",{{opacity:.25}},{{opacity:.85,duration:.32,yoyo:true,repeat:{int((t1-t0)/0.32)},ease:"sine.inOut"}},{t0:.3f});')
    tw(f'tl.fromTo("#{did}-w",{{opacity:1}},{{opacity:.15,duration:.32,yoyo:true,repeat:{int((t1-t0)/0.32)},ease:"sine.inOut"}},{t0:.3f});')

danger("ov-d1", t_sie, t_und_ueb)
danger("ov-d2", t_reissen, t_und_g)
danger("ov-d3", t_knall, t_dein)

# Blitz-Übergang bei jedem Szenenwechsel
for sid, t0, t1, *_ in SCENES[1:]:
    tw(f'tl.fromTo("#{sid}",{{opacity:0}},{{opacity:1,duration:{XF},ease:"sine.inOut"}},{t0:.3f});')

# Figuren atmen, LEDs blinken, Kamera wiegt leicht
for fid in FIGS:
    tw(f'tl.fromTo("#{fid}-body",{{scaleY:1}},{{scaleY:1.022,transformOrigin:"50% 100%",duration:1.3,yoyo:true,repeat:{int(TOTAL/1.3)},ease:"sine.inOut"}},0);')
tw(f'tl.fromTo(".blink",{{opacity:1}},{{opacity:.2,duration:.8,yoyo:true,repeat:{int(TOTAL/.8)},ease:"sine.inOut"}},0);')
tw(f'tl.fromTo("#v-btn",{{opacity:1}},{{opacity:.3,duration:.4,yoyo:true,repeat:10,ease:"sine.inOut"}},{t_also:.3f});')
for sid, t0, t1, *_ in SCENES:
    tw(f'tl.fromTo("#{sid}-cam",{{rotation:-0.6}},{{rotation:0.6,svgOrigin:"540 960",duration:{max(t1-t0,0.2):.3f},ease:"sine.inOut"}},{t0:.3f});')

# ================= HTML =================
scene_html = []
for sid, t0, t1, svg_inner, extra in SCENES:
    scene_html.append(
        f'<div id="{sid}" class="clip scene" data-start="{t0:.3f}" data-duration="{(min(t1+XF, TOTAL) if t1 < TOTAL else t1)-t0:.3f}" data-track-index="1">'
        f'<svg viewBox="0 0 1080 1920" width="1080" height="1920" xmlns="http://www.w3.org/2000/svg">{svg_inner}{extra}</svg></div>')

doc = f'''<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Aufzugseil reißt</title>
    <script src="assets/gsap.min.js"></script>
    <style>
      :root {{ --ground: {BG}; --ink: #ffffff; --signal: {RED}; --font-display: "Poppins", sans-serif; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: var(--ground); }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: var(--font-display); }}
      .scene {{ position: absolute; inset: 0; }}
      .scene svg {{ display: block; }}
      .scene svg g, .scene svg rect, .scene svg circle, .scene svg path, .scene svg ellipse, .scene svg polygon, .scene svg line {{ transform-box: view-box; }}
      .ov {{ position: absolute; inset: 0; pointer-events: none; }}
      .sub {{
        position: absolute; left: 40px; right: 40px; top: 960px; transform-origin: 50% 50%;
        margin-top: -0.6em; text-align: center; color: var(--ink); font-weight: 600; line-height: 1.15;
        letter-spacing: 0; white-space: nowrap; z-index: 20;
        -webkit-text-stroke: 7px rgba(0,0,0,.85); paint-order: stroke fill;
        text-shadow: 0 3px 10px rgba(0,0,0,.6);
      }}
      .sub .k {{ color: var(--signal); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <audio id="vo" class="clip" data-start="0" data-duration="80.24" data-volume="1" src="assets/voiceover.mp3"></audio>
      <audio id="sfx" class="clip" data-start="0" data-duration="{TOTAL}" data-volume="0.45" src="assets/sfx_bed.wav"></audio>
      {DEFS}
      {"".join(scene_html)}
      {"".join(OVER)}
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
