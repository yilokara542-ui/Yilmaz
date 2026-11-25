#!/usr/bin/env python3
"""Video 25 „Nasenbluten: Kopf in den Nacken?“ – Format D „Strichmännchen-Mythos“ (Skill 11c).

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
t_nacken0 = ws("Nacken"); t_du_f = ws("Du", t_nacken0)
t_ha = [w for w in W if w["s"] == t_nacken0][0]["e"] + 0.15; t_gag = t_du_f - 0.3
t_das_b = ws("Das", t_du_f + 0.5); t_hinten = ws("hinten"); t_hals = ws("Hals")
t_und_s = ws("Und", t_hals); t_schluckst = ws("schluckst")
t_blut_m = ws("Blut", t_schluckst); t_uebel = ws("übel"); t_brechen = ws("brechen")
t_das_l = ws("Das", t_brechen); t_leck = ws("Leck"); t_umdrehst = ws("umdrehst")
t_genau = ws("Genau"); t_sieht = ws("sieht")
t_fast = ws("Fast"); t_vorne = ws("vorne", t_fast); t_aederchen = ws("Äderchen")
t_1884 = ws("achtzehnhundert"); t_locus = ws("Locus")
t_ergebnis = ws("Ergebnis"); t_kopf2 = ws("Kopf", t_ergebnis); t_nase2 = ws("Nase", t_kopf2); t_magen2 = ws("Magen", t_nase2); t_blutung = ws("Blutung")
t_also = ws("Also"); t_hinsetzen = ws("Hinsetzen"); t_kopf3 = ws("Kopf", t_hinsetzen); t_zudruecken = ws("zudrücken"); t_kaltes = ws("Kaltes")
t_hoert = ws("Hört", t_kaltes); t_arzt = ws("Arzt")
t_hoer = ws("Und", t_arzt); t_wolf = ws("Wolf"); t_du_s = ws("Du", t_wolf); t_blut_end = ws("Blut", t_du_s)

# ================= BAUSTEINE =================
BONE = "#F7F3EA"


def profile(gid, x, y, s=1.0, rot=0, extra=""):
    """Kopf im Profil (Blick nach rechts), (x,y)=Kinn; rot dreht den Kopf (negativ = nach hinten)."""
    return (f'<g id="{gid}"><g transform="translate({x},{y}) rotate({rot}) scale({s})">'
            f'<path d="M -170 -380 Q -40 -470 70 -360 Q 110 -300 100 -230 L 120 -180 L 95 -170 Q 100 -120 80 -60 L 70 -40 Q 0 0 -110 -110 Q -150 -150 -170 -250 Z" fill="#ffffff" stroke="{INK}" stroke-width="6"/>'
            f'<rect x="-120" y="-120" width="80" height="200" fill="#ffffff" stroke="{INK}" stroke-width="6"/>'
            f'<circle cx="30" cy="-260" r="9" fill="{INK}"/>' + extra + '</g></g>')


def blood(x, y, s=1.0):
    return drop(x, y, s, RED)


def stomach(x, y, s=1.0, fill_id=None):
    path = "M -80 -120 Q -120 -20 -60 60 Q 20 120 110 60 Q 150 20 110 -30 Q 60 -60 20 -40 Q -10 -80 -20 -140 Z"
    fid = f' id="{fill_id}"' if fill_id else ""
    return (f'<g transform="translate({x},{y}) scale({s})"><clipPath id="stc-{fill_id}"><path d="{path}"/></clipPath>'
            f'<path d="{path}" fill="{PINK}" stroke="{INK}" stroke-width="6"/>'
            f'<g clip-path="url(#stc-{fill_id})"><rect{fid} x="-150" y="40" width="320" height="200" fill="{RED}" opacity=".85"/></g>'
            f'<path d="{path}" fill="none" stroke="{INK}" stroke-width="6"/></g>')


# ================= SZENEN =================
# A1 Hook: Nasenbluten – Kopf in den Nacken – HA
A1 = (ground(1290) + f'<line x1="430" y1="1290" x2="470" y2="1010" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>'
      + profile("a1h", 470, 1000, .8, -35, blood(110, -150, .6) + blood(130, -95, .45))
      + g("a1-ha", text(780, 560, "HA", 120, RED, 900) + text(900, 470, "HA", 80, RED, 900)))
scene("a1", 0, t_gag, A1)
pop("#a1-ha", t_ha, .5, .2)

# A2 Gag (ohne Untertitel)
A2 = ground(1290) + stick("a2", 330, 1290, 1.25, "shock", "down", stubble=True) + g("a2-fg", finger(470, 760, 1.0), 1)
scene("a2", t_gag, t_das_b, A2)
tw(f'tl.fromTo("#a2-fg",{{x:700}},{{x:0,duration:.35,ease:"power3.out"}},{t_gag + 0.05:.3f});')
tw(f'tl.to("#a2-fg",{{x:-24,duration:.12,yoyo:true,repeat:3,ease:"sine.inOut"}},{t_gag + 0.5:.3f});')

# B Blut läuft nach hinten in den Hals
flow = f'<path id="b-fl" d="M 120 -190 Q 0 -200 -60 -170 Q -90 -120 -80 -40 L -80 80" stroke="{RED}" stroke-width="22" fill="none" stroke-linecap="round" stroke-dasharray="600" stroke-dashoffset="600"/>'
B = profile("bp", 560, 1000, 1.4, -25, flow) + pill("b-p1", 300, 450, "nach hinten", "red", 44) + g("b-p2", pill("b-p20", 560, 1250, "in den Hals", "red", 46, 1), 0)
scene("b", t_das_b, t_und_s, B)
tw(f'tl.to("#b-fl",{{strokeDashoffset:0,duration:1.4,ease:"sine.inOut"}},{t_hinten - 0.4:.3f});')
pop("#b-p1", t_hinten); pop("#b-p2", t_hals)

# C … schluckst du runter – Magen füllt sich
C = stomach(540, 820, 2.2, "c-f") + pill("c-p", 540, 1250, "runtergeschluckt", "red", 44)
scene("c", t_und_s, t_blut_m, C)
tw(f'tl.fromTo("#c-f",{{y:200}},{{y:0,duration:1.2,ease:"sine.out"}},{t_schluckst - 0.1:.3f});')
pop("#c-p", t_schluckst)

# D Übel – brechen
bucket = (f'<path d="M 600 1080 L 820 1080 L 790 1290 L 630 1290 Z" fill="#C9CED6" stroke="{INK}" stroke-width="6"/>'
          f'<path d="M 600 1080 Q 710 1010 820 1080" stroke="{INK}" stroke-width="5" fill="none"/>')
green = f'<circle cx="0" cy="-418" r="52" fill="#B8E0B0"/>' + face("sad", 0, -418, INK)
D = ground(1290) + stick("d", 330, 1290, 1.25, "sad", "both", extra=green) + g("d-bk", bucket, 0) + pill("d-p", 760, 520, "übel", "lila", 52)
scene("d", t_blut_m, t_das_l, D)
pop("#d-p", t_uebel); pop("#d-bk", t_brechen)
tw(f'tl.to("#d",{{x:10,duration:.08,yoyo:true,repeat:7}},{t_uebel + 0.1:.3f});')

# E Leck im Boot – Boot umdrehen
boat = (f'<g id="e-bt"><path d="M 200 900 L 880 900 L 780 1060 L 300 1060 Z" fill="#C89A5E" stroke="{INK}" stroke-width="7"/>'
        f'<line x1="540" y1="900" x2="540" y2="600" stroke="{INK}" stroke-width="10"/><path d="M 550 610 L 760 860 L 550 860 Z" fill="#ffffff" stroke="{INK}" stroke-width="6"/>'
        + "".join(drop(x, y, .6) for x, y in ((440, 1040), (470, 990))) + '</g>')
waterE = f'<rect x="0" y="1040" width="1080" height="260" fill="#BFE3F5"/>' + "".join(f'<path d="M {x} 1040 q 45 -26 90 0" stroke="{BLUE}" stroke-width="7" fill="none"/>' for x in range(0, 1080, 90))
E = waterE + boat + pill("e-p", 540, 450, "Leck", "red", 50)
scene("e", t_das_l, t_genau, E)
pop("#e-p", t_leck)
tw(f'tl.to("#e-bt",{{rotation:180,svgOrigin:"540 900",duration:.6,ease:"power2.inOut"}},{t_umdrehst - 0.2:.3f});')

# F (dunkel) Probleme unter den Teppich
rug = (f'<path d="M 140 1180 Q 300 1080 420 1160 Q 520 1060 620 1150 Q 760 1050 940 1180 L 940 1240 L 140 1240 Z" fill="{CURTAIN}" stroke="#ffffff" stroke-width="5"/>'
       + text(540, 1215, "Probleme", 40, "#ffffff", 900))
broom = f'<line x1="300" y1="960" x2="200" y2="1230" stroke="#C89A5E" stroke-width="12" stroke-linecap="round"/><path d="M 160 1230 L 240 1230 L 230 1280 L 170 1280 Z" fill="#E8D9B5"/>'
F = f'<rect width="1080" height="1920" fill="{DARK}"/>' + rug + broom + stick("f", 380, 1300, 1.1, "smug", "hold", white=True) + text(540, 300, "Hauptsache, keiner sieht's", 44, "#ffffff", 800)
scene("f", t_genau, t_fast, F, dark=True)

# G Vorne in der Nase – kleine Stelle voller Äderchen
noseF = (f'<path d="M 540 420 Q 470 700 380 900 Q 360 990 450 1000 Q 500 960 540 990 Q 580 960 630 1000 Q 720 990 700 900 Q 610 700 540 420 Z" fill="#ffffff" stroke="{INK}" stroke-width="8"/>'
         f'<ellipse cx="470" cy="960" rx="34" ry="22" fill="{INK}"/><ellipse cx="610" cy="960" rx="34" ry="22" fill="{INK}"/>')
vessels = g("g-v", f'<circle cx="540" cy="880" r="70" fill="{RED}" opacity=".18"/>' + "".join(f'<path d="M 540 880 q {dx} {dy} {dx*2} {dy*0.5}" stroke="{RED}" stroke-width="5" fill="none"/>' for dx, dy in ((30, -40), (-30, -40), (35, 20), (-35, 20), (0, -60))), 0)
G = noseF + vessels + pill("g-p", 800, 600, "vorne", "red", 48) + leader(760, 630, 580, 850)
scene("g", t_fast, t_1884, G)
pop("#g-p", t_vorne); pop("#g-v", t_aederchen - 0.2)

# H 1884 – Locus Kiesselbach
book = (f'<rect x="300" y="640" width="480" height="340" rx="10" fill="#E8D9B5" stroke="{INK}" stroke-width="5"/><line x1="540" y1="640" x2="540" y2="980" stroke="{INK}" stroke-width="4"/>'
        + f'<g transform="translate(420,810) scale(.25)">{noseF.replace("540", "540")}</g>'
        + "".join(f'<line x1="570" y1="{y}" x2="750" y2="{y}" stroke="#9A8A70" stroke-width="5"/>' for y in range(700, 960, 40)))
H = polaroid(150, 480, 780, 680, -3, book, "1884") + pill("h-p", 540, 390, "Locus Kiesselbach", "lila", 46)
scene("h", t_1884, t_ergebnis, H)
pop("#h-p", t_locus)

# I Ergebnis? – gar nichts
scene("i1", t_ergebnis, t_kopf2, qmark(540, 860, 300))
rows = [("i-r0", "für die Nase", t_nase2), ("i-r1", "für den Magen", t_magen2), ("i-r2", "für die Blutung", t_blutung)]
I2 = text(540, 420, "Kopf nach hinten hilft:", 58, INK, 900)
for k, (rid, t, tt) in enumerate(rows):
    I2 += listrow(rid, 140, 600 + k * 150, 800, t, "x", 46)
I2 += g("i-gn", text(540, 1180, "gar nichts", 80, RED, 900), 0)
scene("i2", t_kopf2, t_also, I2)
pop("#i-gn", ws("gar", t_kopf2))
for rid, t, tt in rows:
    pop(f"#{rid}", tt - 0.05, .85)

# J So geht's richtig
rows2 = [("j-r0", "Hinsetzen", t_hinsetzen), ("j-r1", "Kopf leicht nach vorne", t_kopf3), ("j-r2", "10 Min. zudrücken", t_zudruecken), ("j-r3", "Kaltes Tuch in den Nacken", t_kaltes)]
J = text(540, 420, "So geht's:", 64, INK, 900)
for k, (rid, t, tt) in enumerate(rows2):
    J += listrow(rid, 140, 580 + k * 150, 800, t, "check", 44)
scene("j", t_also, t_hoert, J)
for rid, t, tt in rows2:
    pop(f"#{rid}", tt - 0.05, .85)

# K > 20 Minuten – Arzt
clockK = (f'<circle cx="330" cy="820" r="170" fill="#ffffff" stroke="{INK}" stroke-width="8"/><path d="M 330 820 L 330 690" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
          f'<path d="M 330 820 L 330 650 A 170 170 0 0 1 477 905 Z" fill="{RED}" opacity=".25"/>' + text(330, 1060, "20 Min.", 56, INK, 900))
cross = f'<rect x="700" y="660" width="80" height="240" rx="12" fill="{RED}"/><rect x="620" y="740" width="240" height="80" rx="12" fill="{RED}"/>'
K = clockK + text(560, 840, "→", 100, INK, 900) + g("k-c", cross + text(740, 1060, "Arzt", 56, INK, 900), 0)
scene("k", t_hoert, t_hoer, K)
pop("#k-c", t_arzt - 0.2)

# L Wolf – den Himmel anschauen (+ Nachlauf)
night = f'<rect width="1080" height="1300" fill="#2A2D55"/><circle cx="820" cy="300" r="90" fill="#F4E3A1"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="#ffffff"/>' for x, y in ((120, 200), (300, 120), (480, 260), (640, 160), (960, 520), (200, 480)))
wolf = (f'<g transform="translate(760,1290)"><path d="M -120 0 L -100 -160 L -40 -260 L -10 -360 L 30 -300 L 60 -360 L 70 -250 L 140 -230 L 60 -180 L 80 0 Z" fill="#4A4A55" stroke="{INK}" stroke-width="5"/></g>')
L = (night + ground(1290) + f'<line x1="300" y1="1290" x2="330" y2="1010" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>'
     + profile("lh", 330, 1000, .75, -40, blood(110, -150, .55)) + g("l-w", wolf + text(700, 860, "AUUUU", 64, "#ffffff", 900), 0)
     + g("l-x", xcircle(540, 560, 56), 0))
scene("l", t_hoer, TOTAL, L)
pop("#l-w", t_wolf - 0.1); pop("#l-x", t_blut_end - 0.2)
tw(f'tl.to("#l-x",{{scale:1.15,transformOrigin:"50% 50%",duration:.35,yoyo:true,repeat:3,ease:"sine.inOut"}},{VO_END + 0.3:.3f});')
tw(f'tl.to("#l-w",{{opacity:0,duration:.5}},{VO_END + 1.0:.3f});')

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
    txt = txt0.replace("achtzehnhundertvierundachtzig", "1884").replace("zehn Minuten", "10 Minuten").replace("zwanzig Minuten", "20 Minuten")
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
    <title>Nasenbluten</title>
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
