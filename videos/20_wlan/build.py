#!/usr/bin/env python3
"""Video 20 „Volle WLAN-Balken = schnelles Internet?“ – Format D „Strichmännchen-Mythos“ (Skill 11c).

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
t_volle = ws("volle"); t_schnell = ws("schnell"); t_du_f = ws("Du", t_schnell)
t_ha = [w for w in W if w["s"] == t_schnell][0]["e"] + 0.15; t_gag = t_du_f - 0.3
t_die_b = ws("Die", t_du_f); t_hoert = ws("hört"); t_nicht1 = ws("Nicht", t_hoert); t_dahinter = ws("dahinter")
t_der_r = ws("Der", t_dahinter); t_einfahrt = ws("Einfahrt"); t_und_d = ws("Und", t_einfahrt); t_stau = ws("Stau")
t_volle2 = ws("Volle", t_stau); t_nichts = ws("Nichts", t_volle2); t_genau = ws("Genau")
t_das_i = ws("Das", t_genau); t_anbieter = ws("Anbieter"); t_ist = ws("Ist", t_anbieter); t_langsam = ws("langsam"); t_gar1 = ws("gar", t_langsam)
t_und_s = ws("Und", t_gar1); t_familie = ws("Familie"); t_teilt = ws("teilt"); t_leitung2 = ws("Leitung", t_teilt)
t_wlan = ws("WLAN", t_leitung2); t_1997 = ws("neunzehnhundert"); t_funkt = ws("funkt"); t_zwischen = ws("zwischen")
t_ergebnis = ws("Ergebnis"); t_die_b2 = ws("Die", t_ergebnis); t_laden = ws("Laden"); t_streamen = ws("Streamen", t_laden); t_zocken = ws("Zocken")
t_willst = ws("Willst"); t_speed = ws("Speedtest")
t_hoer = ws("Und", t_speed); t_luft = ws("Luft", t_hoer); t_du_fang = ws("Du", t_luft); t_internet_end = ws("Internet", t_du_fang)

# ================= SZENEN =================
# A1 Volle Balken – denkst, dein Internet ist schnell?
A1 = (ground(1290) + stick("a1", 300, 1290, 1.25, "smile", "hold", moods=("laugh",)) + phone(440, 960, 80, 150)
      + g("a1-w", wifi(640, 700, 1.4, 3, LILA), 1)
      + g("a1-c", cloud(780, 960, 1.2, "".join(f'<line x1="{690+i*8}" y1="{930+i*24}" x2="{740+i*8}" y2="{930+i*24}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>' for i in range(3)) + car(830, 980, RED, .8)), 0)
      + g("a1-ha", text(780, 470, "HA", 120, RED, 900) + text(910, 380, "HA", 80, RED, 900)))
scene("a1", 0, t_gag, A1)
pop("#a1-c", t_schnell - 0.4)
pop("#a1-ha", t_ha, .5, .2)

# A2 Gag: Zeigefinger – „Du fetter Bastard.“ (ohne Untertitel)
A2 = ground(1290) + stick("a2", 330, 1290, 1.25, "shock", "down", stubble=True) + g("a2-fg", finger(470, 760, 1.0), 1)
scene("a2", t_gag, t_die_b, A2)
tw(f'tl.fromTo("#a2-fg",{{x:700}},{{x:0,duration:.35,ease:"power3.out"}},{t_gag + 0.05:.3f});')
tw(f'tl.to("#a2-fg",{{x:-24,duration:.12,yoyo:true,repeat:3,ease:"sine.inOut"}},{t_gag + 0.5:.3f});')

# B Die Balken zeigen nur, wie gut dein Handy den Router hört
waves = "".join(f'<path d="M {380+i*90} 760 q 20 -40 0 -80" stroke="{LILA}" stroke-width="10" fill="none" stroke-linecap="round" transform="rotate(90 {380+i*90} 720)"/>' for i in range(4))
B = (phone(220, 800, 180, 340, extra=wifi(220, 760, .45, 3, LILA)) + router(820, 900, 1.2) + g("b-wv", waves, 0)
     + pill("b-p", 540, 520, "Funk zum Router", "lila", 44))
scene("b", t_die_b, t_nicht1, B)
pop("#b-p", t_die_b + 0.2)
tw(f'tl.fromTo("#b-wv",{{opacity:0}},{{opacity:1,duration:.3}},{t_die_b + 0.1:.3f});')
tw(f'tl.to("#b-wv",{{opacity:.3,duration:.4,yoyo:true,repeat:5,ease:"sine.inOut"}},{t_die_b + 0.5:.3f});')

# C Nicht, wie schnell das Internet dahinter ist
globe = (f'<circle cx="860" cy="760" r="120" fill="#BFE3F5" stroke="{INK}" stroke-width="6"/>'
         f'<path d="M 740 760 L 980 760 M 860 640 Q 800 760 860 880 M 860 640 Q 920 760 860 880" stroke="{INK}" stroke-width="5" fill="none"/>')
C = (router(260, 900, 1.1) + f'<path d="M 390 860 Q 560 980 740 800" stroke="{INK}" stroke-width="10" fill="none"/>' + globe
     + text(860, 580, "Internet", 50, INK, 900) + g("c-q", qmark(560, 700, 180), 0) + pill("c-p", 560, 1110, "Tempo?", "red", 48))
scene("c", t_nicht1, t_der_r, C)
pop("#c-q", t_dahinter - 0.2); pop("#c-p", t_dahinter)

# D Router = breite Einfahrt
drive = (f'<rect x="560" y="560" width="400" height="560" fill="#CFC7BC" stroke="{INK}" stroke-width="6"/>'
         f'<rect x="540" y="540" width="40" height="80" fill="#ffffff" stroke="{INK}" stroke-width="5"/><rect x="940" y="540" width="40" height="80" fill="#ffffff" stroke="{INK}" stroke-width="5"/>'
         + "".join(f'<line x1="760" y1="{y}" x2="760" y2="{y+50}" stroke="#ffffff" stroke-width="10"/>' for y in range(620, 1100, 110)))
D = router(250, 930, 1.1) + text(450, 860, "=", 100, INK, 900) + g("d-dr", drive, 0) + pill("d-p", 760, 470, "breite Einfahrt", "white", 44)
scene("d", t_der_r, t_und_d, D)
pop("#d-dr", t_einfahrt - 0.3); pop("#d-p", t_einfahrt)

# E Dahinter die Autobahn im Stau
lanes = "".join(f'<rect x="0" y="{y}" width="1080" height="150" fill="#CFC7BC"/>' for y in (560, 730, 900)) + "".join(f'<line x1="{x}" y1="{y}" x2="{x+70}" y2="{y}" stroke="#ffffff" stroke-width="8"/>' for x in range(20, 1080, 140) for y in (718, 888))
cars = "".join(car(90 + i * 150, y, c, 1.0) for i in range(7) for y, c in ((650, RED), (820, YEL), (990, BLUE)))
E = lanes + cars + pill("e-p", 540, 1180, "Stau", "red", 56)
scene("e", t_und_d, t_volle2, E)
pop("#e-p", t_stau)

# F Volle Balken. Nichts lädt.
F = phone(540, 820, 360, 680, screen="#ffffff", extra=wifi(650, 560, .3, 3, INK) + spinner(540, 860, 80, INK, "f-sp")) + g("f-p", pill("f-p0", 540, 1250, "lädt …", "red", 48, 1), 0)
scene("f", t_volle2, t_genau, F)
tw(f'tl.to("#f-sp",{{rotation:720,svgOrigin:"540 860",duration:{t_genau - t_volle2:.3f},ease:"none"}},{t_volle2:.3f});')
pop("#f-p", t_nichts)

# G (dunkel) Genau wie dein Kopf.
G = (f'<rect width="1080" height="1920" fill="{DARK}"/>' + text(540, 330, "lädt seit 2009", 44, "#ffffff", 800)
     + stick("g", 540, 1300, 1.25, "neutral", "down", white=True)
     + g("g-sp", spinner(540, 600, 50, "#ffffff", "g-spr"), 0) + wifi(540, 500, .6, 3, "#ffffff", "#55545e"))
scene("g", t_genau, t_das_i, G, dark=True)
pop("#g-sp", t_genau + 0.1)
tw(f'tl.to("#g-spr",{{rotation:540,svgOrigin:"540 600",duration:{t_das_i - t_genau:.3f},ease:"none"}},{t_genau:.3f});')

# H Leitung vom Anbieter
house = (f'<polygon points="90,760 260,620 430,760" fill="{RED}" stroke="{INK}" stroke-width="6"/><rect x="120" y="760" width="280" height="300" fill="#ffffff" stroke="{INK}" stroke-width="6"/>'
         + router(260, 1040, .7))
box_ = f'<rect x="800" y="760" width="180" height="300" rx="16" fill="#C9CED6" stroke="{INK}" stroke-width="6"/>' + text(890, 900, "⚡", 60, INK, 900)
H = (house + box_ + ground(1060, 60, 1020) + g("h-c", f'<path d="M 400 1040 L 800 1040" stroke="{LILA}" stroke-width="16" stroke-linecap="round"/>', 0)
     + pill("h-p", 890, 690, "Anbieter", "white", 42) + pill("h-l", 600, 1150, "Leitung", "lila", 42))
scene("h", t_das_i, t_ist, H)
pop("#h-c", t_das_i + 0.3); pop("#h-l", t_das_i + 0.5); pop("#h-p", t_anbieter)

# I Langsame Leitung – bester Empfang hilft gar nichts
snail = (f'<ellipse cx="600" cy="1015" rx="60" ry="20" fill="#E8C9A0" stroke="{INK}" stroke-width="4"/>'
         f'<circle cx="590" cy="985" r="32" fill="#F4C23E" stroke="{INK}" stroke-width="4"/><path d="M 590 985 m -14 0 a 14 14 0 1 1 14 14" stroke="{INK}" stroke-width="4" fill="none"/>'
         f'<line x1="650" y1="1000" x2="665" y2="970" stroke="{INK}" stroke-width="4"/><line x1="660" y1="1002" x2="680" y2="975" stroke="{INK}" stroke-width="4"/>')
I_ = (house + box_ + ground(1060, 60, 1020) + f'<path d="M 400 1040 L 800 1040" stroke="{LILA}" stroke-width="6" stroke-linecap="round"/>' + g("i-sn", snail, 1)
      + g("i-w", wifi(260, 560, .8, 3, LILA), 0) + g("i-gn", text(540, 1260, "gar nichts", 72, RED, 900), 0))
scene("i", t_ist, t_und_s, I_)
tw(f'tl.fromTo("#i-sn",{{x:-150}},{{x:60,duration:{t_und_s - t_ist:.3f},ease:"none"}},{t_ist:.3f});')
pop("#i-w", t_ist + 0.6); pop("#i-gn", t_gar1)

# J Ganze Familie streamt – eine Leitung
fam = "".join(stick(f"j{i}", x, 1150, s, "smile", "hold") + phone(x + 130 * s, 1150 - 258 * s, 70 * s, 120 * s) for i, (x, s) in enumerate(((150, .85), (380, .85), (610, .65), (790, .55))))
J = (router(540, 640, 1.0) + "".join(f'<line x1="540" y1="640" x2="{x}" y2="820" stroke="{LILA}" stroke-width="5" stroke-dasharray="14 10"/>' for x in (230, 470, 680, 860))
     + fam + ground(1150, 60, 1020) + f'<line x1="540" y1="550" x2="540" y2="330" stroke="{INK}" stroke-width="8"/>'
     + pill("j-p", 540, 290, "eine Leitung", "red", 44))
scene("j", t_und_s, t_wlan, J)
pop("#j-p", t_leitung2)

# K Seit 1997 – funkt nur zwischen Handy und Router
oldpc = (f'<rect x="340" y="660" width="400" height="300" rx="14" fill="#E8E0D0" stroke="{INK}" stroke-width="5"/><rect x="370" y="690" width="340" height="220" fill="#9FB8A8" stroke="{INK}" stroke-width="4"/>'
         f'<rect x="300" y="960" width="480" height="40" rx="8" fill="#E8E0D0" stroke="{INK}" stroke-width="5"/>')
K1 = polaroid(150, 480, 780, 680, 3, oldpc + router(620, 1040, .5), "1997")
scene("k1", t_wlan, t_funkt - 0.3, K1)
K2 = (phone(220, 800, 180, 340) + router(820, 900, 1.2) + "".join(f'<path d="M {380+i*90} 760 q 20 -40 0 -80" stroke="{LILA}" stroke-width="10" fill="none" stroke-linecap="round" transform="rotate(90 {380+i*90} 720)"/>' for i in range(4))
      + pill("k-p", 540, 520, "nur bis hier", "lila", 46) + f'<line x1="980" y1="700" x2="1060" y2="700" stroke="{RED}" stroke-width="8" stroke-dasharray="12 10"/>')
scene("k2", t_funkt - 0.3, t_ergebnis, K2)
pop("#k-p", t_zwischen)

# L Ergebnis? – Balken sagen gar nichts übers Tempo
scene("l1", t_ergebnis, t_die_b2, qmark(540, 860, 300))
rows = [("l-r0", "Laden", t_laden), ("l-r1", "Streamen", t_streamen), ("l-r2", "Zocken", t_zocken)]
L2 = text(540, 420, "Balken sagen etwas über:", 56, INK, 900)
for k, (rid, t, tt) in enumerate(rows):
    L2 += listrow(rid, 140, 600 + k * 150, 800, t, "x", 46)
L2 += g("l-gn", text(540, 1180, "gar nichts", 80, RED, 900), 0)
scene("l2", t_die_b2, t_willst, L2)
pop("#l-gn", ws("gar", t_die_b2))
for rid, t, tt in rows:
    pop(f"#{rid}", tt - 0.05, .85)

# M Speedtest
gauge = (f'<path d="M 340 900 A 200 200 0 0 1 740 900" stroke="#CFC7BC" stroke-width="34" fill="none" stroke-linecap="round"/>'
         f'<path d="M 340 900 A 200 200 0 0 1 470 714" stroke="{LILA}" stroke-width="34" fill="none" stroke-linecap="round"/>'
         f'<g id="m-nd"><line x1="540" y1="900" x2="540" y2="740" stroke="{INK}" stroke-width="12" stroke-linecap="round"/></g><circle cx="540" cy="900" r="20" fill="{INK}"/>')
M = phone(540, 860, 520, 900, screen="#ffffff", extra=gauge + text(540, 1050, "Mbit/s", 44, INK, 800)) + pill("m-p", 540, 360, "Speedtest", "lila", 52)
scene("m", t_willst, t_hoer, M)
pop("#m-p", t_speed - 0.1)
tw(f'tl.fromTo("#m-nd",{{rotation:-90,svgOrigin:"540 900"}},{{rotation:35,svgOrigin:"540 900",duration:.9,ease:"elastic.out(1,0.5)"}},{t_speed:.3f});')

# N Handy in die Luft – du fängst da oben kein Internet (+ Nachlauf)
hx2, hy2 = hand_pos(480, 1290, 1.25, "up")
N = (ground(1290) + stick("n", 480, 1290, 1.25, "smile", "up", moods=("neutral", "sad")) + g("n-ph", phone(hx2 + 10, hy2 - 60, 80, 150), 1)
     + "".join(f'<path d="M {hx2 + 70 + i*30} {hy2 - 120 - i*25} q 25 25 0 50" stroke="#CFC7BC" stroke-width="8" fill="none" stroke-linecap="round"/>' for i in range(3))
     + g("n-x", xcircle(820, 420, 56), 0))
scene("n", t_hoer, TOTAL, N)
mood("n", t_du_fang, "smile", "neutral"); pop("#n-x", t_internet_end, .5)
tw(f'tl.to("#n",{{y:-40,duration:.25,yoyo:true,repeat:3,ease:"power1.out"}},{VO_END + 0.4:.3f});')
tw(f'tl.to("#n-x",{{scale:1.15,transformOrigin:"50% 50%",duration:.35,yoyo:true,repeat:3,ease:"sine.inOut"}},{VO_END + 0.4:.3f});')
mood("n", VO_END + 1.4, "neutral", "sad")

# ================= UNTERTITEL: ganzer Satz (Format D) =================
DISPLAY = {"neunzehnhundertsiebenundneunzig": "1997"}
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
    if "Bastard" in b["txt"]:
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
    <title>WLAN-Balken</title>
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
