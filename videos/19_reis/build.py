#!/usr/bin/env python3
"""Video 19 „Handy in Reis?“ – Format D „Strichmännchen-Mythos“ (Skill 11c).

Zeiten aus assets/words.json (wortgenau, inkl. eingefügter Gag-Pausen). Aufruf: python3 build.py
"""
import json, re, html, os, sys, random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../branding/strich"))
from strich import *  # noqa

W = json.load(open(os.path.join(HERE, "assets/words.json"), encoding="utf-8"))
VO_END = W[-1]["e"]
TOTAL = round(VO_END + 4.7, 2)   # Schluss-Szene läuft noch nach (Video > 60 s)
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
t_klo = ws("Klo"); t_legst = ws("legst"); t_reis0 = ws("Reis")
t_du_f = ws("Du", t_reis0 + 0.3); t_ha = [w for w in W if w["s"] == t_reis0][0]["e"] + 0.15; t_gag = t_du_f - 0.3; t_saugt = ws("saugt"); t_beruehrt = ws("berührt")
t_das_w = ws("Das", t_beruehrt); t_im = ws("im", t_das_w); t_zwischen = ws("Zwischen")
t_der = ws("Der", t_zwischen); t_wartet = ws("wartet")
t_genau = ws("Genau"); t_antwort = ws("Antwort")
t_reis_ist = ws("Reis", t_antwort); t_handtuch = ws("Handtuch"); t_jacke = ws("Jacke"); t_drunter = ws("drunter")
t_und_w = ws("Und", t_drunter); t_rosten = ws("rosten")
t_dazu = ws("Dazu"); t_kruemeln = ws("krümeln"); t_lade = ws("Ladeanschluss")
t_das_wurde = ws("Das", t_lade); t_2014 = ws("zweitausendvierzehn"); t_sieben = ws("Sieben")
t_ergebnis = ws("Ergebnis"); t_reis_war = ws("Reis", t_ergebnis); t_schlecht = ws("schlechtesten"); t_sogar = ws("Sogar", t_schlecht)
t_besser = ws("besser"); t_apple = ws("Und", t_besser); t_bitte = ws("Bitte")
t_warum = ws("Und", t_bitte); t_funkt = ws("funktioniert")
t_weil = ws("Weil"); t_wdicht = ws("wasserdicht"); t_allein = ws("allein"); t_nicht_w = ws("Nicht", t_allein)
t_also = ws("Also"); t_aus = ws("Ausschalten"); t_nlad = ws("Nicht", t_aus); t_anschl = ws("Anschluss"); t_klopf = ws("abklopfen"); t_luft = ws("Luft")
t_hoer = ws("Und", t_luft); t_einzu = ws("einzupacken"); t_es = ws("Es", t_einzu); t_sushi = ws("Sushi")

# ================= SZENEN =================
# A1 Handy fällt ins Klo
fx, fy, fs = 330, 1290, 1.25
hx, hy = hand_pos(fx, fy, fs, "hold")
A1 = (ground(1290) + toilet(760, 1290, 1.25) + stick("a1", fx, fy, fs, "smile", "hold", moods=("shock",), stubble=False)
      + g("a1-ph", phone(hx + 8, hy - 30, 70, 130), 1)
      + g("a1-sp", "".join(drop(760 + dx, 1030 + dy, .8) for dx, dy in ((-70, -40), (60, -70), (0, -110), (110, -20))), 0))
scene("a1", 0, t_legst, A1)
tw(f'tl.to("#a1-ph",{{x:{760-hx-8},y:{1070-(hy-30)},rotation:200,duration:.5,ease:"power2.in"}},{t_klo - 0.45:.3f});')
hide("#a1-ph", t_klo + 0.06)
pop("#a1-sp", t_klo + 0.05, .4, .2)
mood("a1", t_klo, "smile", "shock")

# A2 … und legst es in Reis? – HA
A2 = (ground(1290) + bowl(640, 1060, 400, 190, inside=rice_pile(640, 1080, 380, 150, 140, 3)
                         + phone(640, 960, 120, 230, rot=-12)) + rice_pile(640, 1070, 360, 60, 60, 5)
      + stick("a2", 270, 1290, 1.25, "smug", "both", moods=("laugh",))
      + g("a2-ha", text(770, 560, "HA", 120, RED, 900) + text(900, 470, "HA", 80, RED, 900)))
scene("a2", t_legst, t_gag, A2)
pop("#a2-ha", t_ha, .5, .2)

# A3 Gag: Zeigefinger – „Du fetter Bastard.“
A3 = ground(1290) + stick("a3", 330, 1290, 1.25, "shock", "down", stubble=True) + g("a3-fg", finger(470, 760, 1.0), 1)
scene("a3", t_gag, t_saugt, A3)
tw(f'tl.fromTo("#a3-fg",{{x:700}},{{x:0,duration:.35,ease:"power3.out"}},{t_gag + 0.05:.3f});')
tw(f'tl.to("#a3-fg",{{x:-24,duration:.12,yoyo:true,repeat:3,ease:"sine.inOut"}},{t_gag + 0.5:.3f});')

# B Reis saugt nur, was er berührt
PX, PY = 540, 720
grains_out = "".join(grain(x, y, r, 3.2) for x, y, r in ((330, 470, 30), (300, 640, 80), (320, 820, 10), (760, 520, 120), (780, 700, 60), (750, 900, 150), (420, 1060, 0), (640, 1070, 170), (560, 380, 90), (250, 980, 40), (830, 1000, 100)))
drops_out = g("b-dr", "".join(drop(x, y, .9) for x, y in ((395, 560), (690, 800), (530, 1010))), 1)
B = (phone(PX, PY, 300, 560, screen="#D7EEF8") + drops_out + grains_out
     + pill("b-p", 860, 380, "Reis", "white", 48) + leader(820, 410, 780, 495))
scene("b", t_saugt, t_das_w, B)
pop("#b-p", t_saugt + 0.05)
for k in range(3):
    tw(f'tl.to("#b-dr > path:nth-child({k+1})",{{scale:0,transformOrigin:"50% 50%",duration:.35,ease:"power2.in"}},{t_beruehrt - 0.1 + k*0.12:.3f});')

# C Das Wasser ist im Handy – zwischen den Bauteilen
inside = (f'<rect x="410" y="470" width="260" height="210" rx="12" fill="#C9CED6" stroke="{INK}" stroke-width="4"/>'
          + text(540, 595, "+  −", 52, "#5a6070", 900)
          + f'<rect x="410" y="720" width="260" height="250" rx="10" fill="#9FD3A8" stroke="{INK}" stroke-width="4"/>'
          + "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#2E3440" stroke="{INK}" stroke-width="3"/>' for x, y, w, h in ((440, 750, 90, 70), (560, 760, 80, 50), (450, 860, 60, 80), (550, 850, 90, 90)))
          + "".join(f'<rect x="{x}" y="955" width="18" height="12" fill="#E8B04A"/>' for x in range(440, 650, 28)))
C = (phone(PX, PY, 300, 560, screen="#F3ECE5", extra=inside)
     + g("c-d1", drop(540, 705, .85) + drop(500, 835, .7), 0) + g("c-d2", drop(625, 905, .75) + drop(430, 700, .6) + drop(600, 470, .6), 0)
     + pill("c-p", 780, 380, "Wasser drinnen", "red", 44))
scene("c", t_das_w, t_der, C)
pop("#c-d1", t_im); pop("#c-p", t_im + 0.1); pop("#c-d2", t_zwischen)

# D Der Reis liegt draußen und wartet
clock = (f'<circle cx="540" cy="360" r="90" fill="#ffffff" stroke="{INK}" stroke-width="6"/>'
         f'<g id="d-mh"><line x1="540" y1="360" x2="540" y2="290" stroke="{INK}" stroke-width="7" stroke-linecap="round"/></g>'
         f'<line x1="540" y1="360" x2="590" y2="360" stroke="{INK}" stroke-width="7" stroke-linecap="round"/><circle cx="540" cy="360" r="8" fill="{INK}"/>')
waiters = "".join(grain(x, y, r, 5.0, "n") for x, y, r in ((300, 820, -8), (780, 820, 8), (330, 1060, 0), (750, 1060, 0)))
D = clock + phone(540, 940, 220, 420) + waiters
scene("d", t_der, t_genau, D)
tw(f'tl.to("#d-mh",{{rotation:360,svgOrigin:"540 360",duration:{t_genau-t_der:.3f},ease:"none"}},{t_der:.3f});')

# E (dunkel) Genau wie du auf ihre Antwort.
bubble = (f'<rect x="560" y="560" width="400" height="150" rx="30" fill="#3A3946" stroke="#ffffff" stroke-width="4"/>'
          + text(760, 630, "hey :)", 44, "#ffffff", 800) + text(900, 690, "gelesen 21:14", 26, "#B9B8C6", 700, "end"))
E = (f'<rect width="1080" height="1920" fill="{DARK}"/>'
     f'<rect x="700" y="230" width="120" height="300" fill="{CURTAIN}"/><rect x="830" y="230" width="120" height="300" fill="{CURTAIN}"/>'
     + text(230, 330, "Tag 3 ohne Antwort", 40, "#ffffff", 800, "middle")
     + f'<polygon points="430,860 700,700 700,1000" fill="#5B8CF0" opacity=".25"/>'
     + stick("e", 330, 1300, 1.25, "sad", "hold", white=True) + phone(460, 920, 70, 130, screen="#7FB2FF") + g("e-bb", bubble, 0))
scene("e", t_genau, t_reis_ist, E, dark=True)
pop("#e-bb", t_genau + 0.2)

# F Reis = Handtuch auf der Jacke, wenn du drunter nass bist
jacket = (f'<path d="M -70 -350 L 70 -350 L 95 -170 L -95 -170 Z" fill="{BLUE}" stroke="{INK}" stroke-width="6"/>'
          f'<line x1="0" y1="-350" x2="0" y2="-170" stroke="{INK}" stroke-width="4"/>')
towel = (f'<path d="M -90 -360 L 90 -360 L 100 -330 L -100 -330 Z" fill="{PINK}" stroke="{INK}" stroke-width="5"/>'
         f'<rect x="60" y="-360" width="40" height="120" fill="{PINK}" stroke="{INK}" stroke-width="5"/>'
         + "".join(f'<line x1="{x}" y1="-358" x2="{x}" y2="-332" stroke="#ffffff" stroke-width="5"/>' for x in (-50, -20, 10)))
wet = "".join(drop(x, y, .45) for x, y in ((-40, -230), (30, -270), (10, -195)))
F = (bowl(220, 900, 260, 120, inside=rice_pile(220, 912, 240, 90, 70, 8) + phone(220, 840, 80, 150, rot=-10))
     + text(420, 900, "=", 90, INK, 900)
     + ground(1290, 480, 1020) + stick("f", 740, 1290, 1.25, "neutral", "down", extra=jacket + g("f-wet", wet, 0) + g("f-tw", towel, 0))
     + pill("f-p1", 900, 420, "Handtuch", "white", 44) + pill("f-p2", 900, 1110, "drunter nass", "red", 42))
scene("f", t_reis_ist, t_und_w, F)
pop("#f-tw", t_handtuch); pop("#f-p1", t_handtuch + 0.1); pop("#f-wet", t_drunter); pop("#f-p2", t_drunter + 0.1)

# G Kontakte rosten weiter
pads = "".join(f'<rect x="{x}" y="640" width="90" height="300" rx="10" fill="#E8B04A" stroke="{INK}" stroke-width="5"/>' for x in (200, 350, 500, 650, 800))
rust = "".join(f'<circle cx="{x + RNG_x}" cy="{y}" r="{r}" fill="#A0522D" opacity=".9"/>'
               for (x, RNG_x, y, r) in ((200, 40, 700, 20), (200, 30, 860, 14), (350, 50, 760, 24), (500, 30, 680, 16), (500, 60, 880, 22), (650, 45, 800, 26), (800, 35, 720, 18), (800, 55, 900, 15)))
G = (f'<rect x="120" y="560" width="840" height="460" rx="20" fill="#9FD3A8" stroke="{INK}" stroke-width="6"/>' + pads
     + g("g-r", rust, 0) + drop(450, 600, .9) + drop(720, 1000, .7) + pill("g-p", 540, 1150, "Rost", "red", 52))
scene("g", t_und_w, t_dazu, G)
tw(f'tl.fromTo("#g-r",{{opacity:0}},{{opacity:1,duration:1.2,ease:"sine.in"}},{t_rosten:.3f});')
pop("#g-p", t_rosten + 0.2)

# H Reisstücke krümeln in den Ladeanschluss
crumbs = "".join(g(f"h-c{k}", grain(x, y, r, 1.6), 0) for k, (x, y, r) in enumerate(((300, 420, 20), (420, 360, 120), (660, 380, 60), (780, 450, 150), (520, 300, 90), (600, 470, 30))))
H = (f'<rect x="140" y="560" width="800" height="560" rx="90" fill="#3A3A44" stroke="{INK}" stroke-width="7"/>'
     f'<rect x="380" y="900" width="320" height="90" rx="45" fill="#15151a" stroke="{INK}" stroke-width="6"/>'
     + "".join(f'<circle cx="{x}" cy="945" r="9" fill="#15151a"/>' for x in (240, 270, 300, 780, 810, 840))
     + crumbs + pill("h-p", 540, 1200, "verstopft", "red", 52) + pill("h-l", 540, 470, "Ladeanschluss", "white", 46).replace('<g id="h-l" opacity="0">','<g id="h-l" opacity="0">'))
scene("h", t_dazu, t_das_wurde, H)
for k in range(6):
    tw(f'tl.fromTo("#h-c{k}",{{opacity:1,x:0,y:0}},{{x:{540-[300,420,660,780,520,600][k]},y:{945-[420,360,380,450,300,470][k]},scale:.6,duration:.6,ease:"power2.in"}},{t_kruemeln + k*0.18:.3f});')
    hide(f"#h-c{k}", t_kruemeln + k * 0.18 + 0.6)
pop("#h-l", t_lade - 0.1); pop("#h-p", t_lade + 0.5)

# J 2014 getestet – sieben Trockenmittel
fills = ("#ffffff", "#9fc6ff", "#d9c2a0", "#e8e0d0", "#c8a77a", "#f0f0f0", "#b8d8b0")
cups = ""
for k in range(7):
    cx = 225 + k * 105
    cups += (f'<path d="M {cx-40} 760 L {cx+40} 760 L {cx+32} 860 L {cx-32} 860 Z" fill="#ffffff" stroke="{INK}" stroke-width="4"/>'
             f'<rect x="{cx-36}" y="760" width="72" height="34" fill="{fills[k]}" stroke="{INK}" stroke-width="3"/>')
J = polaroid(150, 520, 780, 620, -3, cups + f'<circle cx="540" cy="680" r="0"/>', "2014") + pill("j-p", 540, 420, "7 Trockenmittel", "lila", 48)
scene("j", t_das_wurde, t_ergebnis, J)
pop("#j-p", t_sieben)

# K Ergebnis? – Reis am schlechtesten, offene Luft besser
K1 = qmark(540, 860, 300)
scene("k1", t_ergebnis, t_reis_war, K1)
bars = ""
H_ = (520, 440, 380, 330, 260, 210, 120)
labels = {5: "Luft", 6: "Reis"}
for k, hh in enumerate(H_):
    x = 150 + k * 115
    col = "#C9CED6" if k not in labels else ("#ffffff" if k == 6 else LILA_BG)
    st = INK if k != 5 else LILA
    bars += f'<g id="k-b{k}" opacity="0"><rect x="{x}" y="{1100-hh}" width="90" height="{hh}" rx="10" fill="{col}" stroke="{st}" stroke-width="5"/></g>'
bars += text(150 + 5 * 115 + 45, 1160, "Luft", 40, LILA, 800) + text(150 + 6 * 115 + 45, 1160, "Reis", 40, INK, 800)
K2 = (text(540, 420, "Holt Wasser raus:", 56, INK, 900) + ground(1100, 120, 960) + bars
      + g("k-gr", "".join(grain(150 + 6 * 115 + 45 + dx, 960 + dy, r, 1.2) for dx, dy, r in ((-20, 0, 20), (15, -20, 100), (5, 25, 160))), 0)
      + pill("k-p1", 790, 1250, "am schlechtesten", "red", 42) + pill("k-p2", 790, 800, "besser", "lila", 44))
scene("k2", t_reis_war, t_apple, K2)
for k in range(7):
    pop(f"#k-b{k}", t_reis_war + k * 0.06, .6, .14)
pop("#k-gr", t_reis_war + 0.5); pop("#k-p1", t_schlecht); pop("#k-p2", t_besser - 0.3)

# L Hersteller: Bitte keinen Reis.
doc = (f'<rect x="200" y="380" width="680" height="820" rx="30" fill="#ffffff" stroke="{INK}" stroke-width="6"/>'
       f'<rect x="200" y="380" width="680" height="110" rx="30" fill="{LILA_BG}" stroke="{INK}" stroke-width="6"/><rect x="203" y="440" width="674" height="50" fill="{LILA_BG}"/>'
       + text(540, 455, "Hersteller-Tipp", 48, LILA, 900)
       + bowl(540, 700, 300, 140, inside=rice_pile(540, 712, 280, 100, 80, 11)) + g("l-x", xcircle(690, 640, 60), 0)
       + g("l-t", text(540, 1030, "Bitte keinen Reis.", 58, RED, 900), 0))
scene("l", t_apple, t_warum, doc)
pop("#l-x", t_bitte - 0.1, .5); pop("#l-t", t_bitte)

# M Und warum hat es bei dir trotzdem funktioniert?
M = (ground(1290) + stick("m", 400, 1290, 1.25, "smile", "hold", moods=("neutral",)) + phone(545, 965, 80, 150, screen="#BFE3F5")
     + g("m-q", qmark(780, 760, 220), 0))
scene("m", t_warum, t_weil, M)
pop("#m-q", t_funkt - 0.2); mood("m", t_funkt, "smile", "neutral")

# N wasserdicht – trocknet von allein – nicht wegen dem Reis
seal = f'<rect x="355" y="480" width="370" height="640" rx="70" fill="none" stroke="{LILA}" stroke-width="7" stroke-dasharray="22 14"/>'
wind = "".join(f'<path d="M {x} {y} q 60 -30 120 0 t 120 0" stroke="#9AA3B5" stroke-width="7" fill="none" stroke-linecap="round"/>' for x, y in ((90, 560), (60, 700), (110, 840)))
N = (phone(540, 800, 300, 560) + g("n-s", seal + pill("n-p", 540, 410, "wasserdicht", "lila", 48), 0)
     + g("n-d", "".join(drop(x, y, .8) for x, y in ((410, 640), (680, 760), (430, 980))), 1)
     + g("n-w", wind, 0)
     + g("n-r", bowl(860, 1180, 200, 100, inside=rice_pile(860, 1190, 180, 70, 40, 13)) + xcircle(960, 1130, 34), 0))
scene("n", t_weil, t_also, N)
pop("#n-s", t_wdicht - 0.1)
tw(f'tl.to("#n-d",{{y:60,duration:.5,ease:"power2.in"}},{t_wdicht + 0.2:.3f});')
pop("#n-w", t_allein - 0.2)
tw(f'tl.to("#n-d",{{opacity:0,duration:.5}},{t_allein:.3f});')
pop("#n-r", t_nicht_w)

# O So geht's richtig
ic_power = f'<circle cx="235" cy="0" r="26" fill="none" stroke="{INK}" stroke-width="6"/><line x1="235" y1="-34" x2="235" y2="0" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
rows = [("o-r0", "Ausschalten", t_aus), ("o-r1", "Nicht laden", t_nlad), ("o-r2", "Anschluss nach unten", t_anschl), ("o-r3", "Leicht abklopfen", t_klopf), ("o-r4", "An der Luft trocknen", t_luft)]
O = text(540, 420, "So geht's:", 64, INK, 900)
for k, (rid, t, tt) in enumerate(rows):
    O += listrow(rid, 140, 560 + k * 140, 800, t, "check", 42)
scene("o", t_also, t_hoer, O)
for rid, t, tt in rows:
    pop(f"#{rid}", tt - 0.05, .85)

# P Es ist kein Sushi.
sushi = (f'<ellipse cx="730" cy="1050" rx="270" ry="50" fill="#ffffff" stroke="{INK}" stroke-width="6"/>'
         f'<circle cx="730" cy="900" r="150" fill="#2F3B2F" stroke="{INK}" stroke-width="6"/><circle cx="730" cy="900" r="122" fill="#ffffff" stroke="{INK}" stroke-width="3"/>'
         + "".join(grain(730 + dx, 900 + dy, r, 1.2) for dx, dy, r in ((-80, -40, 20), (-60, 50, 100), (70, -60, 60), (80, 40, 140), (0, -95, 0), (0, 95, 90), (-95, 0, 90), (95, 0, 90)))
         + f'<rect x="680" y="830" width="100" height="140" rx="16" fill="#3A3A44" stroke="{INK}" stroke-width="5"/><rect x="690" y="842" width="80" height="116" rx="10" fill="#BFE3F5"/>'
         f'<g id="p-chop"><line x1="900" y1="620" x2="760" y2="830" stroke="#C89A5E" stroke-width="12" stroke-linecap="round"/><line x1="940" y1="640" x2="790" y2="840" stroke="#C89A5E" stroke-width="12" stroke-linecap="round"/></g>')
P = ground(1290) + stick("p", 260, 1290, 1.2, "smile", "both", moods=("neutral", "sad")) + sushi + g("p-x", xcircle(940, 760, 50), 0)
scene("p", t_hoer, TOTAL, P)
mood("p", t_es, "smile", "neutral"); pop("#p-x", t_sushi, .5)
# Nachlauf: Stäbchen heben das Handy-Maki an, Figur wird traurig, ✕ pulsiert
tw(f'tl.to("#p-chop",{{y:-70,duration:.6,ease:"sine.inOut",yoyo:true,repeat:1}},{VO_END + 0.6:.3f});')
tw(f'tl.to("#p-x",{{scale:1.15,transformOrigin:"50% 50%",duration:.35,yoyo:true,repeat:5,ease:"sine.inOut"}},{VO_END + 0.4:.3f});')
mood("p", VO_END + 2.0, "neutral", "sad")

# ================= UNTERTITEL: ganzer Satz (Format D) =================
DISPLAY = {"zweitausendvierzehn": "2014"}
sents = []; cur = []
for w in W:
    cur.append(w)
    if re.search(r"[.?!]$", w["t"]):
        sents.append(cur); cur = []
if cur:
    sents.append(cur)
blocks = []
for s_ in sents:
    txt = " ".join(DISPLAY.get(re.sub(r"[^\wäöüß]", "", w["t"]), None) and w["t"].replace(re.sub(r"[^\wäöüß]", "", w["t"]), DISPLAY[re.sub(r"[^\wäöüß]", "", w["t"])]) or w["t"] for w in s_)
    if blocks and len(blocks[-1]["txt"]) + len(txt) + 1 <= 36 and s_[0]["s"] - blocks[-1]["e"] < 0.6:
        blocks[-1]["txt"] += " " + txt; blocks[-1]["e"] = s_[-1]["e"]
    else:
        blocks.append({"txt": txt, "s": s_[0]["s"], "e": s_[-1]["e"]})
subs = []
for k, b in enumerate(blocks):
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
    <title>Handy in Reis</title>
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
