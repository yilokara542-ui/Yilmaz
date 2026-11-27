#!/usr/bin/env python3
"""Video 23 „Katze schnurrt = glücklich?“ – Format D „Strichmännchen-Mythos“ (Skill 11c).

Zeiten aus assets/words.json (wortgenau, inkl. eingefügter Gag-Pausen). Aufruf: python3 build.py
"""
import json, re, html, os, sys, random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../branding/strich"))
from strich import *  # noqa

W = json.load(open(os.path.join(HERE, "assets/words.json"), encoding="utf-8"))
VO_END = W[-1]["e"]
TOTAL = round(VO_END + 2.8, 2)   # kurzer stummer Nachlauf der Schluss-Szene
T = []
SCENES = []


def tw(c):
    T.append(c)


def ws(prefix, after=0.0):
    for w in W:
        if w["s"] >= after - 1e-6 and re.sub(r"[^\wäöüÄÖÜß]", "", w["t"]).lower().startswith(prefix.lower()):
            return w["s"]
    raise KeyError(prefix)


def pop(sel, t, frm=0.8, dur=0.16):
    tw(f'tl.fromTo("{sel}",{{opacity:0,scale:{frm},transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:{dur},ease:"back.out(2)"}},{t:.3f});')


def show(sel, t):
    tw(f'tl.set("{sel}",{{opacity:1}},{t:.3f});')


def hide(sel, t):
    tw(f'tl.set("{sel}",{{opacity:0}},{t:.3f});')


def mood(fid, t, frm, to):
    hide(f"#{fid}-f-{frm}", t); show(f"#{fid}-f-{to}", t)


def g(gid, inner, op=0):
    return f'<g id="{gid}" opacity="{op}">{inner}</g>'


DARK_SCENES = []


def scene(sid, t0, t1, inner, dark=False):
    SCENES.append((sid, t0, t1, inner, dark))
    if dark:
        DARK_SCENES.append((t0, t1))


# ================= CUES =================
t_katze = ws("Katze"); t_streichelst = ws("streichelst"); t_du_f = ws("Du", t_streichelst)
t_ha = [w for w in W if w["s"] == t_streichelst][0]["e"] + 0.15; t_gag = t_du_f - 0.3
t_katzen1 = ws("Katzen", t_du_f); t_angst = ws("Angst"); t_tierarzt = ws("Tierarzt"); t_schmerzen = ws("Schmerzen")
t_schnurren1 = ws("Schnurren", t_schmerzen); t_selbst = ws("Selbstberuhigung")
t_wie = ws("Wie", t_selbst); t_pruefung = ws("Prüfung"); t_panik = ws("Panik")
t_genau = ws("Genau"); t_mathe = ws("Matheklausur")
t_und_es = ws("Und", t_mathe); t_schlimmer = ws("schlimmer")
t_2009 = ws("Zweitausendneun"); t_aufgenommen = ws("aufgenommen")
t_ergebnis = ws("Ergebnis"); t_wenn = ws("Wenn", t_ergebnis); t_ton = ws("Ton"); t_baby = ws("Baby")
t_den = ws("Den", t_baby); t_stehst = ws("stehst"); t_napf = ws("Napf")
t_sie_ist = ws("Sie", t_napf); t_trainiert = ws("trainiert")
t_ob = ws("Ob"); t_schwanz = ws("Schwanz"); t_ohren = ws("Ohren"); t_augen = ws("Augen"); t_nicht_s = ws("Nicht", t_augen)
t_langsam = ws("Langsames"); t_alles = ws("Alles")
t_hoer = ws("Und", t_alles); t_liebe = ws("Liebeserklärung"); t_sie_will = ws("Sie", t_liebe); t_futter_end = ws("Futter", t_sie_will)

# ================= BAUSTEINE =================
def note(nid, x, y, s=1.0, col="#fff", op=0):
    return (f'<g id="{nid}" opacity="{op}"><g transform="translate({x},{y}) scale({s})">'
            f'<ellipse cx="0" cy="0" rx="24" ry="17" fill="{col}" transform="rotate(-20)"/><rect x="16" y="-92" width="9" height="92" fill="{col}"/>'
            f'<path d="M 25 -92 Q 58 -80 50 -40 Q 44 -64 25 -66 Z" fill="{col}"/></g></g>')


CAT = "#F2A65A"


def cat(gid, x, y, s=1.0, eyes="open", col=CAT, tail=True, extra=""):
    """Sitzende Katze im Strich-Stil, (x,y) = Mitte unten. eyes: open | closed | fear | smug."""
    k = s
    e = {"open": f'<circle cx="-22" cy="-215" r="8" fill="{INK}"/><circle cx="22" cy="-215" r="8" fill="{INK}"/>',
         "closed": f'<path d="M -32 -215 Q -22 -205 -12 -215 M 12 -215 Q 22 -205 32 -215" stroke="{INK}" stroke-width="5" fill="none" stroke-linecap="round"/>',
         "fear": f'<circle cx="-22" cy="-215" r="13" fill="#fff" stroke="{INK}" stroke-width="4"/><circle cx="-22" cy="-215" r="7" fill="{INK}"/><circle cx="22" cy="-215" r="13" fill="#fff" stroke="{INK}" stroke-width="4"/><circle cx="22" cy="-215" r="7" fill="{INK}"/>',
         "smug": f'<path d="M -34 -218 L -10 -214 M 10 -214 L 34 -218" stroke="{INK}" stroke-width="6" stroke-linecap="round"/><circle cx="-22" cy="-210" r="5" fill="{INK}"/><circle cx="22" cy="-210" r="5" fill="{INK}"/>'}[eyes]
    t_ = f'<path d="M 70 -20 Q 170 -40 150 -150 Q 140 -200 110 -190" stroke="{INK}" stroke-width="26" fill="none" stroke-linecap="round"/><path d="M 70 -20 Q 170 -40 150 -150 Q 140 -200 110 -190" stroke="{col}" stroke-width="16" fill="none" stroke-linecap="round"/>' if tail else ""
    return (f'<g id="{gid}"><g transform="translate({x},{y}) scale({k})">' + t_
            + f'<ellipse cx="0" cy="-80" rx="95" ry="85" fill="{col}" stroke="{INK}" stroke-width="6"/>'
            + f'<ellipse cx="-45" cy="-6" rx="30" ry="14" fill="{col}" stroke="{INK}" stroke-width="5"/><ellipse cx="45" cy="-6" rx="30" ry="14" fill="{col}" stroke="{INK}" stroke-width="5"/>'
            + f'<polygon points="-60,-250 -50,-310 -12,-268" fill="{col}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/><polygon points="60,-250 50,-310 12,-268" fill="{col}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
            + f'<circle cx="0" cy="-205" r="72" fill="{col}" stroke="{INK}" stroke-width="6"/>'
            + f'<g id="{gid}-e">{e}</g><path d="M -8 -190 L 8 -190 L 0 -180 Z" fill="{PINK}" stroke="{INK}" stroke-width="3"/>'
            + f'<path d="M 0 -180 Q -10 -168 -20 -172 M 0 -180 Q 10 -168 20 -172" stroke="{INK}" stroke-width="4" fill="none" stroke-linecap="round"/>'
            + "".join(f'<line x1="{sx*30}" y1="{-186+dy}" x2="{sx*95}" y2="{-196+dy*2}" stroke="{INK}" stroke-width="3"/>' for sx in (-1, 1) for dy in (-6, 6))
            + extra + '</g></g>')


def purr(gid, x, y, op=0, col=INK):
    return g(gid, text(x, y, "rrrr", 54, col, 900, extra='font-style="italic"') + "".join(
        f'<path d="M {x-70+i*14} {y+20+i*10} q 30 -16 60 0" stroke="#CFC7BC" stroke-width="6" fill="none" stroke-linecap="round"/>' for i in range(2)), op)


def heart(x, y, r=40, col=RED):
    return f'<path d="M {x} {y+r*0.9} C {x-r*1.6} {y-r*0.2} {x-r*0.8} {y-r*1.3} {x} {y-r*0.45} C {x+r*0.8} {y-r*1.3} {x+r*1.6} {y-r*0.2} {x} {y+r*0.9} Z" fill="{col}" stroke="{INK}" stroke-width="4"/>'


def bowl_food(x, y, full=True):
    return (f'<path d="M {x-110} {y-60} L {x+110} {y-60} L {x+80} {y} L {x-80} {y} Z" fill="{BLUE}" stroke="{INK}" stroke-width="5"/>'
            + ("".join(f'<circle cx="{x-70+i*28}" cy="{y-68 - (i%2)*10}" r="14" fill="#A0522D" stroke="{INK}" stroke-width="3"/>' for i in range(6)) if full else ""))


# ================= SZENEN =================
# A1 Hook: Streicheln + Schnurren – HA
A1 = (ground(1290) + stick("a1", 280, 1290, 1.2, "smile", "hold") + cat("a1c", 640, 1290, 1.2, "closed") + purr("a1-p", 860, 840, 1)
      + g("a1-c", cloud(440, 500, 1.1, heart(440, 500, 42)), 0)
      + g("a1-ha", text(800, 560, "HA", 120, RED, 900) + text(920, 470, "HA", 80, RED, 900)))
scene("a1", 0, t_gag, A1)
pop("#a1-c", t_katze); pop("#a1-ha", t_ha, .5, .2)
tw(f'tl.to("#a1-p",{{opacity:.3,duration:.25,yoyo:true,repeat:9,ease:"sine.inOut"}},0.3);')

# A2 Gag (ohne Untertitel)
# spannender (Feedback 27.11.): Ruck-Zoom auf das Gesicht, Wackeln, roter Rand, Figur schrumpft bei „Bastard“
t_dummer = ws("dummer"); t_bastard = ws("Bastard")
A2 = (f'<g id="a2-cam">' + ground(1290) + stick("a2", 330, 1290, 1.25, "shock", "down", stubble=True) + g("a2-fg", finger(470, 760, 1.0), 1) + '</g>'
      + f'<rect id="a2-red" x="0" y="0" width="1080" height="1920" fill="none" stroke="{RED}" stroke-width="60" opacity="0"/>')
scene("a2", t_gag, t_katzen1, A2)
tw(f'tl.fromTo("#a2-cam",{{scale:1,svgOrigin:"330 760"}},{{scale:1.45,svgOrigin:"330 760",duration:.25,ease:"power4.out"}},{t_dummer - 0.05:.3f});')
for k in range(6):
    tw(f'tl.to("#a2-cam",{{x:{(-1)**k * 10},duration:.05}},{t_dummer + 0.25 + k*0.05:.3f});')
tw(f'tl.to("#a2-cam",{{x:0,duration:.05}},{t_dummer + 0.55:.3f});')
tw(f'tl.fromTo("#a2-red",{{opacity:0}},{{opacity:.8,duration:.15,yoyo:true,repeat:1}},{t_bastard:.3f});')
tw(f'tl.to("#a2-cam",{{scale:1.75,svgOrigin:"330 760",duration:.35,ease:"power2.in"}},{t_bastard:.3f});')
tw(f'tl.fromTo("#a2-fg",{{x:700}},{{x:0,duration:.35,ease:"power3.out"}},{t_gag + 0.05:.3f});')
tw(f'tl.to("#a2-fg",{{x:-24,duration:.12,yoyo:true,repeat:3,ease:"sine.inOut"}},{t_gag + 0.5:.3f});')

# B Angst beim Tierarzt – Schmerzen
table = (f'<rect x="200" y="1000" width="680" height="40" rx="10" fill="#C9CED6" stroke="{INK}" stroke-width="6"/>'
         f'<rect x="260" y="1040" width="30" height="250" fill="#C9CED6" stroke="{INK}" stroke-width="5"/><rect x="790" y="1040" width="30" height="250" fill="#C9CED6" stroke="{INK}" stroke-width="5"/>')
syr = (f'<g transform="translate(860,620) rotate(35)"><rect x="-20" y="-110" width="40" height="160" rx="8" fill="#ffffff" stroke="{INK}" stroke-width="5"/>'
       f'<rect x="-20" y="-40" width="40" height="90" fill="#BFE3F5"/><line x1="0" y1="50" x2="0" y2="110" stroke="{INK}" stroke-width="5"/><rect x="-30" y="-125" width="60" height="18" rx="6" fill="{INK}"/></g>')
B = (ground(1290) + table + cat("bc", 540, 1000, 1.1, "fear") + purr("b-p", 760, 700, 1) + pill("b-p1", 540, 420, "Tierarzt", "white", 46)
     + g("b-s", syr, 0) + g("b-ban", f'<rect x="460" y="972" width="70" height="26" rx="8" fill="#ffffff" stroke="{INK}" stroke-width="4"/>' + pill("b-p2", 300, 600, "Schmerzen", "red", 44, 1), 0))
scene("b", t_katzen1, t_schnurren1, B)
pop("#b-p1", t_tierarzt - 0.1); pop("#b-s", t_tierarzt); pop("#b-ban", t_schmerzen)

# C Selbstberuhigung
C = cat("cc", 540, 1150, 1.4, "closed") + purr("c-p", 800, 650, 1) + pill("c-p1", 540, 420, "Selbstberuhigung", "lila", 50)
scene("c", t_schnurren1, t_wie, C)
pop("#c-p1", t_selbst)

# D Prüfung: pfeifen gegen Panik
desk = f'<rect x="420" y="1000" width="560" height="30" fill="#C89A5E" stroke="{INK}" stroke-width="5"/><rect x="450" y="1030" width="24" height="260" fill="#C89A5E" stroke="{INK}" stroke-width="4"/><rect x="926" y="1030" width="24" height="260" fill="#C89A5E" stroke="{INK}" stroke-width="4"/>'
paper = f'<g transform="rotate(-6 700 960)"><rect x="600" y="920" width="200" height="80" fill="#ffffff" stroke="{INK}" stroke-width="4"/>{text(700, 975, "Prüfung", 34, INK, 900)}</g>'
D = (ground(1290) + desk + paper + stick("d", 330, 1290, 1.2, "shock", "hold", stubble=False, extra="".join(drop(x, y, .45) for x, y in ((-62, -460), (64, -440))))
     + "".join(note(f"d-n{k}", 470 + k * 60, 760 - k * 50, .7, INK) for k in range(3)) + pill("d-p", 760, 470, "Panik", "red", 48))
scene("d", t_wie, t_genau, D)
for k in range(3):
    pop(f"#d-n{k}", t_pruefung + 0.2 + k * 0.25, .6)
pop("#d-p", t_panik)

# E (dunkel) Genau wie du vor jeder Matheklausur.
board = f'<rect x="160" y="300" width="760" height="380" rx="12" fill="#2F4A3A" stroke="#ffffff" stroke-width="6"/>' + text(540, 520, "x² + 3x = ???", 80, "#ffffff", 900)
E = (f'<rect width="1080" height="1920" fill="{DARK}"/>' + board + stick("e", 540, 1300, 1.2, "shock", "down", white=True, extra="".join(drop(x, y, .45) for x, y in ((-62, -460), (64, -440), (-70, -400))))
     + text(540, 240, "Mathe – Note: 5", 44, "#ffffff", 800))
scene("e", t_genau, t_und_es, E, dark=True)

# F Und es wird noch schlimmer.
F = cat("fc", 540, 1250, 1.9, "smug")
scene("f", t_und_es, t_2009, F)

# G 2009 – Forscher nehmen Schnurren auf
mic = (f'<g transform="translate(700,760)"><rect x="-26" y="-80" width="52" height="110" rx="26" fill="#3A3A44" stroke="{INK}" stroke-width="5"/>'
       f'<path d="M -46 0 Q -46 60 0 60 Q 46 60 46 0" stroke="{INK}" stroke-width="5" fill="none"/><line x1="0" y1="60" x2="0" y2="120" stroke="{INK}" stroke-width="6"/></g>')
G = polaroid(150, 480, 780, 680, 3, cat("gc", 420, 990, .9, "closed") + mic, "2009") + pill("g-p", 540, 390, "Forscher nehmen auf", "lila", 44)
scene("g", t_2009, t_ergebnis, G)
pop("#g-p", t_aufgenommen - 0.3)

# H Ergebnis? – versteckter Baby-Schrei im Schnurren
scene("h1", t_ergebnis, t_wenn, qmark(540, 860, 300))
low = "M 120 760 " + " ".join(f"Q {150 + i*60} {720 if i%2==0 else 800} {180 + i*60} 760" for i in range(13))
high = "M 120 1000 " + " ".join(f"Q {135 + i*30} {900 if i%2==0 else 1100} {150 + i*30} 1000" for i in range(27))
baby = (f'<circle cx="0" cy="0" r="60" fill="#FCE3D0" stroke="{INK}" stroke-width="5"/>'
        f'<path d="M -30 -12 L -12 -6 M 30 -12 L 12 -6" stroke="{INK}" stroke-width="5" stroke-linecap="round"/><ellipse cx="0" cy="24" rx="18" ry="22" fill="{INK}"/>')
H2 = (text(540, 420, "Schnurren, wenn Futter fällig ist:", 50, INK, 900)
      + f'<path d="{low}" stroke="#9AA3B5" stroke-width="10" fill="none" stroke-linecap="round"/>' + text(540, 860, "normales Schnurren", 36, "#7A8090", 800)
      + g("h-hi", f'<path d="{high}" stroke="{RED}" stroke-width="8" fill="none" stroke-linecap="round"/>' + f'<g transform="translate(880,1170)">{baby}</g>' + pill("h-p", 540, 1170, "Baby-Schrei-Ton", "red", 44, 1), 0))
scene("h2", t_wenn, t_den, H2)
pop("#h-hi", t_ton - 0.1)

# I Du stehst auf und füllst den Napf
I_ = (ground(1290) + stick("i", 300, 1290, 1.2, "neutral", "hold") + cat("ic", 820, 1290, .85, "open") + g("i-b0", bowl_food(600, 1290, False), 1)
      + g("i-b1", bowl_food(600, 1290, True), 0) + purr("i-p", 860, 900, 1, RED))
scene("i", t_den, t_sie_ist, I_)
pop("#i-b1", t_napf - 0.1)

# J Sie hat dich trainiert
clicker = f'<rect x="-34" y="-22" width="68" height="44" rx="14" fill="{YEL}" stroke="{INK}" stroke-width="4"/><circle cx="0" cy="0" r="10" fill="{RED}"/>'
J = (ground(1290) + cat("jc", 300, 1290, 1.0, "smug", extra=f'<g transform="translate(110,-120)">{clicker}</g>')
     + stick("j", 740, 1290, 1.1, "smile", "both") + pill("j-p1", 300, 600, "Trainerin", "lila", 44) + g("j-p2", pill("j-p20", 740, 600, "dressiert", "red", 44, 1), 0))
scene("j", t_sie_ist, t_ob, J)
pop("#j-p1", t_sie_ist + 0.2); pop("#j-p2", t_trainiert)

# K Schwanz, Ohren, Augen – nicht das Schnurren
rows = [("k-r0", "Schwanz", "check", t_schwanz), ("k-r1", "Ohren", "check", t_ohren), ("k-r2", "Augen", "check", t_augen), ("k-r3", "Schnurren", "x", t_nicht_s)]
K = text(540, 420, "Entspannt erkennst du an:", 58, INK, 900)
for k, (rid, t, mk, tt) in enumerate(rows):
    K += listrow(rid, 140, 580 + k * 150, 800, t, mk, 46)
scene("k", t_ob, t_langsam, K)
for rid, t, mk, tt in rows:
    pop(f"#{rid}", tt - 0.05, .85)

# L Langsames Blinzeln = alles gut
L = cat("lc", 540, 1250, 1.9, "open") + g("l-cl", cat("lc2", 540, 1250, 1.9, "closed"), 0) + pill("l-p", 540, 400, "Alles gut", "lila", 56)
scene("l", t_langsam, t_hoer, L)
tw(f'tl.set("#l-cl",{{opacity:1}},{t_langsam + 0.5:.3f});')
tw(f'tl.set("#l-cl",{{opacity:0}},{t_langsam + 1.3:.3f});')
tw(f'tl.set("#l-cl",{{opacity:1}},{t_alles:.3f});')
pop("#l-p", t_alles)

# M Keine Liebeserklärung – sie will nur Futter (+ Nachlauf)
M = (ground(1290) + stick("m", 280, 1290, 1.2, "smile", "hold", moods=("neutral", "sad")) + g("m-h", heart(420, 880, 46), 1)
     + cat("mc", 800, 1290, .95, "open") + bowl_food(620, 1290, False) + g("m-x", xcircle(520, 760, 44), 0)
     + g("m-th", cloud(840, 560, 1.0, f'<g transform="translate(840,600) scale(.7)">{bowl_food(0, 0, True)}</g>'), 0))
scene("m", t_hoer, TOTAL, M)
pop("#m-x", t_liebe); pop("#m-th", t_sie_will); mood("m", t_sie_will, "smile", "neutral"); mood("m", VO_END + 1.2, "neutral", "sad")
tw(f'tl.to("#m-h",{{scale:.6,opacity:.4,transformOrigin:"50% 50%",duration:1.2,ease:"sine.in"}},{VO_END + 0.2:.3f});')

# ================= UNTERTITEL: ganzer Satz (Format D) =================
DISPLAY = {"zweitausendelf": "2011", "Drei-Minuten-YouTube-Workout": "3-Minuten-YouTube-Workout"}
sents = []; cur = []
for w in W:
    cur.append(w)
    if re.search(r"[.?!]$", w["t"]):
        sents.append(cur); cur = []
if cur:
    sents.append(cur)
blocks = []
for s_ in sents:
    txt0 = " ".join(DISPLAY.get(re.sub(r"[^\wäöüß]", "", w["t"]), None) and w["t"].replace(re.sub(r"[^\wäöüß]", "", w["t"]), DISPLAY[re.sub(r"[^\wäöüß]", "", w["t"])]) or w["t"] for w in s_)
    txt = txt0.replace("Zweitausendneun", "2009")
    if blocks and len(blocks[-1]["txt"]) + len(txt) + 1 <= 36 and s_[0]["s"] - blocks[-1]["e"] < 0.6:
        blocks[-1]["txt"] += " " + txt; blocks[-1]["e"] = s_[-1]["e"]
    else:
        blocks.append({"txt": txt, "s": s_[0]["s"], "e": s_[-1]["e"]})
subs = []
for k, b in enumerate(blocks):
    if "Bastard" in b["txt"]:   # Beleidigung nur hörbar
        continue   # Beleidigung nur hörbar, nicht als Untertitel (Feedback 22.11.)
    nxt = blocks[k + 1]["s"] if k + 1 < len(blocks) else TOTAL
    end = nxt if (nxt - b["e"] < 0.8 or k + 1 == len(blocks)) else b["e"] + 0.25
    dark = any(a <= b["s"] < z for a, z in DARK_SCENES)
    subs.append(f'<div id="sub{k}" class="clip sub" data-start="{b["s"]:.3f}" data-duration="{end-b["s"]:.3f}" data-track-index="9" style="color:{"#ffffff" if dark else INK}">{html.escape(b["txt"])}</div>')

# ================= HTML =================
scene_html = []
for sid, t0, t1, inner, dark in SCENES:
    scene_html.append(f'<div id="{sid}" class="clip scene" data-start="{t0:.3f}" data-duration="{max(0.05, min(t1, TOTAL)-t0):.3f}" data-track-index="1">'
                      f'<svg viewBox="0 0 1080 1920" width="1080" height="1920"><rect width="1080" height="1920" fill="{BG}"/>{inner}</svg></div>')
doc_ = f'''<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Katze schnurrt</title>
    <script src="assets/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: {BG}; }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: Nunito, sans-serif; }}
      .scene {{ position: absolute; inset: 0; }}
      .scene svg {{ display: block; }}
      .sub {{ position: absolute; left: 100px; width: 880px; top: 1440px; text-align: center; z-index: 20; font-family: Nunito, sans-serif;
        font-weight: 900; font-size: 58px; line-height: 1.22; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <audio id="vo" class="clip" data-start="0" data-duration="{VO_END:.2f}" data-volume="1" src="assets/voiceover.mp3"></audio>
      <audio id="sfx" class="clip" data-start="0" data-duration="{TOTAL}" data-volume="0.5" src="assets/sfx_bed.wav"></audio>
      {"".join(scene_html)}
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
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(doc_)
cues = {k: v for k, v in globals().items() if k.startswith("t_") and isinstance(v, (int, float))}
cues["TOTAL"] = TOTAL
json.dump(cues, open(os.path.join(HERE, "assets/cues.json"), "w"), indent=1)
print(f"Szenen: {len(SCENES)}, Untertitel: {len(subs)}, Tweens: {len(T)}, Länge: {TOTAL}s")
