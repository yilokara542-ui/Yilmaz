#!/usr/bin/env python3
"""Video 22 „Heizung auf 5 = schneller warm?“ – Format D „Strichmännchen-Mythos“ (Skill 11c).

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
t_fuenf0 = ws("fünf"); t_warm = ws("warm"); t_du_f = ws("Du", t_warm)
t_ha = [w for w in W if w["s"] == ws("wird", t_warm)][0]["e"] + 0.15; t_gag = t_du_f - 0.3
t_die_z = ws("Die", t_du_f + 0.5); t_turbo = ws("Turbo"); t_ziel = ws("Zieltemperatur")
t_drei = ws("Drei", t_ziel); t_zwanzig = ws("zwanzig"); t_fuenf2 = ws("Fünf", t_zwanzig); t_28a = ws("achtundzwanzig", t_fuenf2)
t_ist = ws("Ist", t_28a); t_ventil = ws("Ventil"); t_genauso = ws("genauso")
t_das_a = ws("Das", t_genauso); t_aufzug = ws("Aufzug"); t_knopf = ws("Knopf"); t_er = ws("Er", t_knopf); t_nicht_s = ws("nicht", t_er)
t_genau = ws("Genau", t_nicht_s); t_mama = ws("Mama")
t_der_u = ws("Der", t_mama); t_28b = ws("achtundzwanzig", t_der_u)
t_dann = ws("Dann", t_28b); t_sauna = ws("Sauna"); t_fenster = ws("Fenster")
t_thermo = ws("Thermostatventil"); t_1943 = ws("neunzehnhundert")
t_jedes = ws("Und", t_1943); t_sechs = ws("sechs", t_jedes); t_kosten = ws("Heizkosten")
t_ergebnis = ws("Ergebnis"); t_fuenf3 = ws("Fünf", t_ergebnis); t_wohn = ws("Wohnzimmer"); t_bad = ws("Bad", t_wohn); t_kinder = ws("Kinderzimmer"); t_gar = ws("Gar", t_kinder)
t_also = ws("Also"); t_stell = ws("Stell"); t_warte = ws("warte")
t_hoer = ws("Und", t_warte); t_gas = ws("Gaspedal")

# ================= BAUSTEINE =================
def radiator(x, y, w=420, h=300):
    """Heizkörper, (x,y) = links oben."""
    fins = "".join(f'<rect x="{x + 14 + i*(w-28)/8:.0f}" y="{y}" width="{(w-28)/8 - 10:.0f}" height="{h}" rx="14" fill="#ffffff" stroke="{INK}" stroke-width="5"/>' for i in range(8))
    return fins + f'<rect x="{x-20}" y="{y+h-40}" width="30" height="22" fill="#C9CED6" stroke="{INK}" stroke-width="4"/>'


def knob(gid, x, y, r=90, val=3):
    """Thermostatkopf mit Zahlen 1–5 (Zeiger als drehbare Gruppe {gid}-p)."""
    nums = "".join(text(x + (r + 38) * __import__("math").cos(__import__("math").radians(-210 + i * 60)), y + (r + 38) * __import__("math").sin(__import__("math").radians(-210 + i * 60)) + 14, str(i + 1), 40, INK, 900) for i in range(5))
    ang = -210 + (val - 1) * 60
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ffffff" stroke="{INK}" stroke-width="7"/>' + nums
            + f'<g id="{gid}-p"><g transform="rotate({ang + 90} {x} {y})"><rect x="{x-9}" y="{y-r+12}" width="18" height="{r*0.55:.0f}" rx="9" fill="{RED}"/></g></g>'
            + f'<circle cx="{x}" cy="{y}" r="14" fill="{INK}"/>')


def thermometer(x, y, h=420, level=.5, gid=None, label=None):
    """Thermometer, (x,y) = Kugel unten; level 0..1."""
    fill_h = (h - 60) * level
    g_ = f'<g id="{gid}">' if gid else '<g>'
    return (f'<rect x="{x-30}" y="{y-h}" width="60" height="{h}" rx="30" fill="#ffffff" stroke="{INK}" stroke-width="6"/>'
            + g_ + f'<rect x="{x-16}" y="{y-40-fill_h:.0f}" width="32" height="{fill_h + 40:.0f}" rx="16" fill="{RED}"/></g>'
            + f'<circle cx="{x}" cy="{y}" r="52" fill="{RED}" stroke="{INK}" stroke-width="6"/>'
            + (text(x + 110, y - h + 60, label, 64, RED, 900) if label else ""))


# ================= SZENEN =================
# A1 Hook: Heizung auf 5 – HA
A1 = (ground(1290) + radiator(560, 860, 420, 300) + g("a1-k", knob("a1k", 460, 1000, 60, 3), 1)
      + stick("a1", 260, 1290, 1.2, "smile", "hold") + g("a1-ha", text(780, 600, "HA", 120, RED, 900) + text(900, 510, "HA", 80, RED, 900)))
scene("a1", 0, t_gag, A1)
tw(f'tl.to("#a1k-p",{{rotation:120,svgOrigin:"460 1000",duration:.5,ease:"power2.out"}},{t_fuenf0 - 0.2:.3f});')
pop("#a1-ha", t_ha, .5, .2)

# A2 Gag – „Du dummer eingeschränkter Bastard.“ (ohne Untertitel)
A2 = ground(1290) + stick("a2", 330, 1290, 1.25, "shock", "down", stubble=True) + g("a2-fg", finger(470, 760, 1.0), 1)
scene("a2", t_gag, t_die_z, A2)
tw(f'tl.fromTo("#a2-fg",{{x:700}},{{x:0,duration:.35,ease:"power3.out"}},{t_gag + 0.05:.3f});')
tw(f'tl.to("#a2-fg",{{x:-24,duration:.12,yoyo:true,repeat:3,ease:"sine.inOut"}},{t_gag + 0.5:.3f});')

# B Kein Turbo – Zieltemperatur
rocket = (f'<g transform="translate(820,560)"><path d="M 0 -90 Q 40 -40 40 40 L -40 40 Q -40 -40 0 -90 Z" fill="#ffffff" stroke="{INK}" stroke-width="5"/>'
          f'<circle cx="0" cy="-20" r="16" fill="#BFE3F5" stroke="{INK}" stroke-width="4"/><path d="M -20 40 L 0 90 L 20 40 Z" fill="{YEL}" stroke="{INK}" stroke-width="4"/></g>')
B = (knob("bk", 400, 820, 170, 5) + g("b-r", rocket + xcircle(900, 470, 40), 0)
     + g("b-t", thermometer(820, 1150, 380, .55) , 0) + pill("b-p", 540, 1230, "Zieltemperatur", "lila", 50))
scene("b", t_die_z, t_drei, B)
pop("#b-r", t_turbo - 0.1); tw(f'tl.set("#b-r",{{opacity:0}},{t_ziel - 0.2:.3f});'); pop("#b-t", t_ziel - 0.2); pop("#b-p", t_ziel)

# C 3 ≈ 20 °C, 5 ≈ 28 °C
C = (text(540, 420, "Was die Zahl bedeutet:", 58, INK, 900)
     + g("c-r1", knob("c1", 330, 680, 90, 3) + text(560, 700, "=", 90, INK, 900) + text(780, 720, "≈ 20 °C", 80, INK, 900), 0)
     + g("c-r2", knob("c2", 330, 1020, 90, 5) + text(560, 1040, "=", 90, INK, 900) + text(780, 1060, "≈ 28 °C", 80, RED, 900), 0))
scene("c", t_drei, t_ist, C)
pop("#c-r1", t_drei); pop("#c-r2", t_fuenf2)

# D Ventil bei 3 genauso offen wie bei 5
def valve(cx, lab):
    return (f'<rect x="{cx-170}" y="780" width="340" height="90" fill="#C9CED6" stroke="{INK}" stroke-width="6"/>'
            f'<rect x="{cx-30}" y="650" width="60" height="130" fill="#ffffff" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="{cx-26}" y="660" width="52" height="40" fill="{INK}"/>'
            + "".join(f'<path d="M {cx-150+i*70} 825 l 40 0 m -14 -12 l 14 12 l -14 12" stroke="{RED}" stroke-width="7" fill="none" stroke-linecap="round"/>' for i in range(4))
            + knob(f"dk{lab}", cx, 540, 70, lab))
D = valve(290, 3) + valve(790, 5) + text(540, 990, "=", 100, INK, 900) + pill("d-p", 540, 1150, "gleich weit offen", "lila", 48)
scene("d", t_ist, t_das_a, D)
pop("#d-p", t_genauso)

# E Aufzug: 5× drücken – kommt nicht schneller
elev = (f'<rect x="560" y="420" width="400" height="760" fill="#C9CED6" stroke="{INK}" stroke-width="6"/><line x1="760" y1="420" x2="760" y2="1180" stroke="{INK}" stroke-width="5"/>'
        f'<rect x="660" y="330" width="200" height="70" rx="10" fill="{INK}"/>' + g("e-n", text(760, 384, "7", 54, "#7BD88F", 900), 1)
        + f'<rect x="440" y="760" width="70" height="120" rx="12" fill="#ffffff" stroke="{INK}" stroke-width="5"/><circle cx="475" cy="820" r="20" fill="{YEL}" stroke="{INK}" stroke-width="4"/>')
E = ground(1290) + elev + stick("e", 240, 1290, 1.2, "neutral", "hold") + g("e-5", text(380, 700, "5×", 90, RED, 900), 0)
scene("e", t_das_a, t_genau, E)
pop("#e-5", t_knopf)
for k in range(5):
    tw(f'tl.to("#e",{{x:12,duration:.07,yoyo:true,repeat:1}},{t_knopf + k*0.16:.3f});')

# F (dunkel) Genau wie du, wenn deine Mama ruft.
bed = (f'<rect x="160" y="1060" width="760" height="110" rx="20" fill="{CURTAIN}" stroke="#ffffff" stroke-width="4"/>'
       f'<rect x="160" y="980" width="200" height="90" rx="30" fill="#ffffff"/><rect x="340" y="1000" width="560" height="80" rx="20" fill="#4A3060" stroke="#ffffff" stroke-width="3"/>')
door = f'<rect x="830" y="420" width="190" height="560" fill="#3A3946" stroke="#ffffff" stroke-width="4"/>'
F = (f'<rect width="1080" height="1920" fill="{DARK}"/>' + door + bed
     + f'<circle cx="260" cy="950" r="52" fill="#ffffff"/>' + face("neutral", 260, 950, INK) + phone(380, 920, 60, 110, screen="#7FB2FF")
     + g("f-b", f'<rect x="560" y="330" width="320" height="120" rx="30" fill="#ffffff"/>' + text(720, 412, "ESSEN!", 64, RED, 900), 0)
     + text(540, 1300 - 60, "„komme gleich“ – seit 40 Min.", 38, "#ffffff", 800))
scene("f", t_genau, t_der_u, F, dark=True)
pop("#f-b", t_mama - 0.2)

# G Bei 5 erst bei 28 °C Schluss
G = knob("gk", 330, 820, 150, 5) + thermometer(780, 1150, 600, .2, "g-th") + g("g-l", pill("g-p0", 780, 420, "erst bei 28 °C aus", "red", 44, 1), 0)
scene("g", t_der_u, t_dann, G)
tw(f'tl.fromTo("#g-th",{{scaleY:1,transformOrigin:"50% 100%"}},{{scaleY:4,transformOrigin:"50% 100%",duration:{t_dann - t_der_u - 0.4:.3f},ease:"sine.inOut"}},{t_der_u + 0.2:.3f});')
pop("#g-l", t_28b)

# H Sauna – Fenster auf
wood = "".join(f'<rect x="0" y="{y}" width="1080" height="70" fill="{"#D9A55B" if (y//70)%2 else "#C8924A"}"/>' for y in range(0, 1300, 70))
sweat = "".join(drop(x, y, .5) for x, y in ((-50, -470), (55, -450), (-70, -390), (70, -380)))
win = (f'<g id="h-w" opacity="0"><rect x="640" y="420" width="320" height="420" fill="#BFE3F5" stroke="{INK}" stroke-width="8"/>'
       f'<line x1="800" y1="420" x2="800" y2="840" stroke="{INK}" stroke-width="6"/>'
       + "".join(f'<path d="M {660+i*40} {500+i*90} q 60 -30 120 0 t 120 0" stroke="#ffffff" stroke-width="8" fill="none" stroke-linecap="round"/>' for i in range(3))
       + "".join(f'<g transform="translate({x},{y})"><circle r="34" fill="{YEL}" stroke="{INK}" stroke-width="4"/>{text(0, 14, "€", 40, INK, 900)}</g>' for x, y in ((700, 900), (830, 880), (940, 910))) + '</g>')
H = wood + text(540, 300, "28 °C", 90, RED, 900) + ground(1290) + stick("h", 330, 1290, 1.25, "sad", "down", extra=sweat) + win
scene("h", t_dann, t_thermo - 0.3, H)
pop("#h-w", t_fenster - 0.1)
tw(f'tl.to("#h-w g",{{y:"-=380",duration:.9,ease:"sine.out"}},{t_fenster + 0.2:.3f});')

# I Thermostatventil seit 1943
oldrad = radiator(280, 640, 380, 300) + knob("ik", 250, 780, 50, 3)
I_ = polaroid(150, 480, 780, 680, -3, oldrad, "1943") + pill("i-p", 540, 390, "über 80 Jahre alt", "lila", 44)
scene("i", t_thermo - 0.3, t_jedes, I_)
pop("#i-p", t_1943 + 0.4)

# J Jedes Grad ≈ 6 % mehr Heizkosten
stacks = ""
for k in range(4):
    x = 230 + k * 200; n = 3 + k
    stacks += f'<g id="j-s{k}" opacity="0">' + "".join(f'<ellipse cx="{x}" cy="{1080 - i*34}" rx="70" ry="22" fill="{YEL}" stroke="{INK}" stroke-width="4"/>' for i in range(n)) + text(x, 1170, f"{20 + k*2} °C", 40, INK, 900) + '</g>'
J = stacks + pill("j-p", 540, 470, "+6 % pro Grad", "red", 56)
scene("j", t_jedes, t_ergebnis, J)
for k in range(4):
    pop(f"#j-s{k}", t_jedes + 0.3 + k * 0.35, .7)
pop("#j-p", t_sechs)

# K Ergebnis? – 5 heizt nicht schneller
scene("k1", t_ergebnis, t_fuenf3, qmark(540, 860, 300))
rows = [("k-r0", "im Wohnzimmer", t_wohn), ("k-r1", "im Bad", t_bad), ("k-r2", "im Kinderzimmer", t_kinder)]
K2 = text(540, 420, "Stufe 5 heizt schneller:", 58, INK, 900)
for k, (rid, t, tt) in enumerate(rows):
    K2 += listrow(rid, 140, 600 + k * 150, 800, t, "x", 46)
K2 += g("k-gn", text(540, 1180, "gar nicht", 80, RED, 900), 0)
scene("k2", t_fuenf3, t_also, K2)
for rid, t, tt in rows:
    pop(f"#{rid}", tt - 0.05, .85)
pop("#k-gn", t_gar)

# L Temperatur einstellen und warten
hour = (f'<g id="l-h"><path d="M 760 640 L 920 640 L 840 780 Z M 760 920 L 920 920 L 840 780 Z" fill="#FBE7B0" stroke="{INK}" stroke-width="6"/>'
        f'<rect x="740" y="620" width="200" height="24" rx="8" fill="#C89A5E" stroke="{INK}" stroke-width="4"/><rect x="740" y="916" width="200" height="24" rx="8" fill="#C89A5E" stroke="{INK}" stroke-width="4"/></g>')
L = knob("lk", 340, 780, 150, 3) + g("l-c", checkcircle(480, 640, 40), 0) + g("l-hg", hour, 0) + pill("l-p", 540, 1120, "einstellen & warten", "lila", 48)
scene("l", t_also, t_hoer, L)
pop("#l-c", t_stell + 0.3); pop("#l-hg", t_warte - 0.1)
tw(f'tl.to("#l-h",{{rotation:180,svgOrigin:"840 780",duration:.6,ease:"power2.inOut"}},{t_warte + 0.3:.3f});')

# M Kein Gaspedal (+ Nachlauf)
pedal = (f'<g transform="translate(860,560) rotate(-15)"><rect x="-60" y="-90" width="120" height="180" rx="20" fill="#3A3A44" stroke="{INK}" stroke-width="5"/>'
         + "".join(f'<line x1="-40" y1="{y}" x2="40" y2="{y}" stroke="#77777f" stroke-width="6"/>' for y in (-50, -15, 20, 55)) + '</g>')
M = (ground(1290) + radiator(500, 860, 420, 300) + g("m-k", knob("mk", 390, 1000, 60, 5), 1)
     + stick("m", 230, 1290, 1.15, "smug", "hold", moods=("neutral", "sad")) + g("m-pd", pedal + xcircle(950, 460, 46), 0))
scene("m", t_hoer, TOTAL, M)
tw(f'tl.to("#mk-p",{{rotation:-120,svgOrigin:"390 1000",duration:.35,yoyo:true,repeat:5,ease:"sine.inOut"}},{t_hoer + 0.3:.3f});')
pop("#m-pd", t_gas - 0.1); mood("m", t_gas, "smug", "neutral"); mood("m", VO_END + 1.2, "neutral", "sad")
tw(f'tl.to("#m-pd",{{scale:1.1,transformOrigin:"50% 50%",duration:.35,yoyo:true,repeat:3,ease:"sine.inOut"}},{VO_END + 0.3:.3f});')

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
    txt = txt0.replace("neunzehnhundertdreiundvierzig", "1943").replace("auf fünf", "auf 5").replace("bei fünf", "bei 5").replace("Fünf heißt", "5 heißt").replace("Drei heißt", "3 heißt").replace("bei drei", "bei 3").replace("Fünf heizt", "5 heizt").replace("achtundzwanzig Grad", "28 °C").replace(" zwanzig Grad", " 20 °C").replace("Bei fünf", "Bei 5").replace("achtundzwanzig.", "28 °C.").replace("sechs Prozent", "6 %").replace("fünfmal", "5-mal")
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
    <title>Heizung auf 5</title>
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
