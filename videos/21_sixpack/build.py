#!/usr/bin/env python3
"""Video 21 „3-Minuten-Workout = Sixpack?“ – Format D „Strichmännchen-Mythos“ (Skill 11c).

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
t_workout = ws("DreiMinuten"); t_sixpack0 = ws("Sixpack"); t_du_f = ws("Du", t_sixpack0)
t_ha = [w for w in W if w["s"] == t_sixpack0][0]["e"] + 0.15; t_gag = t_du_f - 0.3
t_du_hast = ws("Du", t_du_f + 0.3); t_jeder = ws("Jeder"); t_deiner = ws("Deiner"); t_pizza = ws("Pizza")
t_bauch1 = ws("Bauchübungen"); t_staerker = ws("stärker"); t_aber = ws("Aber"); t_bleibt = ws("bleibt")
t_das_ist = ws("Das", t_bleibt); t_bild = ws("Bild"); t_decke = ws("Decke")
t_und_drei = ws("Und", t_decke); t_keks = ws("Keks"); t_den = ws("Den", t_keks); t_belohnung = ws("Belohnung")
t_genau = ws("Genau"); t_das_w = ws("Das", t_genau); t_2011 = ws("zweitausendelf"); t_sechs = ws("Sechs")
t_ergebnis = ws("Ergebnis"); t_das_b = ws("Das", t_ergebnis); t_nicht_am = ws("Nicht", t_das_b); t_koerper = ws("Körper"); t_gar = ws("Gar", t_koerper)
t_fett = ws("Fett", t_gar); t_sondern = ws("Sondern"); t_ueber = ws("Über", t_sondern); t_ernaehrung = ws("Ernährung")
t_also = ws("Also"); t_weniger = ws("Weniger"); t_mehr = ws("mehr", t_weniger); t_genug = ws("genug"); t_geduld = ws("Geduld")
t_hoer = ws("Und", t_geduld); t_spiegel = ws("Spiegel"); t_da_ist = ws("Da", t_spiegel); t_nichts_end = ws("nichts", t_da_ist)

# ================= SZENEN =================
# A1 Hook: 3-Minuten-Workout → Sixpack? – HA
A1 = (ground(1290) + stick("a1", 260, 1290, 1.2, "smile", "both") + player(720, 980, 440, 260, "3:00")
      + g("a1-c", cloud(720, 520, 1.3, sixpack(720, 520, .55)), 0)
      + g("a1-ha", text(330, 520, "HA", 120, RED, 900) + text(200, 430, "HA", 80, RED, 900)))
scene("a1", 0, t_gag, A1)
pop("#a1-c", t_sixpack0 - 0.2); pop("#a1-ha", t_ha, .5, .2)

# A2 Gag – „Du fetter Bastard.“ (ohne Untertitel)
A2 = ground(1290) + stick("a2", 330, 1290, 1.25, "shock", "down", stubble=True, extra=belly(0, -270, .95)) + g("a2-fg", finger(470, 760, 1.0), 1)
scene("a2", t_gag, t_du_hast, A2)
tw(f'tl.fromTo("#a2-fg",{{x:700}},{{x:0,duration:.35,ease:"power3.out"}},{t_gag + 0.05:.3f});')
tw(f'tl.to("#a2-fg",{{x:-24,duration:.12,yoyo:true,repeat:3,ease:"sine.inOut"}},{t_gag + 0.5:.3f});')

# B Du hast schon einen Sixpack. Jeder hat einen.
B1 = (ground(1290) + stick("b", 540, 1290, 1.6, "smile", "down") + sixpack(540, 1290 - 270 * 1.6, .55)
      + pill("b-p", 860, 560, "Bauchmuskel", "white", 42) + leader(800, 590, 600, 830))
B2 = ground(1290) + "".join(stick(f"b2{i}", x, 1290, 1.0, "neutral", "down") + sixpack(x, 1290 - 270, .34) for i, x in enumerate((200, 420, 660, 880)))
scene("b1", t_du_hast, t_jeder, B1); pop("#b-p", t_du_hast + 0.4)
scene("b2", t_jeder, t_deiner, B2)

# C Deiner liegt unter einer Schicht Pizza – Querschnitt
slices = "".join(f'<g transform="rotate({r} {x} {y})"><polygon points="{x},{y-40} {x-34},{y+30} {x+34},{y+30}" fill="{YEL}" stroke="{INK}" stroke-width="4"/>'
                 f'<circle cx="{x-8}" cy="{y+8}" r="7" fill="{RED}"/><circle cx="{x+10}" cy="{y+16}" r="6" fill="{RED}"/></g>' for x, y, r in ((300, 610, 10), (520, 640, -20), (760, 600, 25), (420, 700, 180), (680, 710, 160)))
C = (f'<rect x="120" y="520" width="840" height="260" rx="30" fill="#FBE7B0" stroke="{INK}" stroke-width="6"/>' + slices
     + f'<rect x="120" y="780" width="840" height="320" rx="30" fill="{UNDER}" stroke="{INK}" stroke-width="6"/>' + sixpack(540, 940, .9)
     + pill("c-p1", 900, 450, "Fett", "red", 46) + pill("c-p2", 900, 1170, "Sixpack", "white", 42))
scene("c", t_deiner, t_bauch1, C)
pop("#c-p1", t_pizza); pop("#c-p2", t_deiner + 0.3)

# D Bauchübungen: Muskel stärker – Fett bleibt
D = (f'<rect x="120" y="520" width="840" height="260" rx="30" fill="#FBE7B0" stroke="{INK}" stroke-width="6"/>' + slices
     + f'<rect x="120" y="780" width="840" height="320" rx="30" fill="{UNDER}" stroke="{INK}" stroke-width="6"/>' + sixpack(540, 940, .9, "#D9706F", "d-sp")
     + pill("d-p1", 270, 1170, "stärker", "lila", 44) + pill("d-p2", 900, 450, "bleibt", "red", 46))
scene("d", t_bauch1, t_das_ist, D)
tw(f'tl.to("#d-sp",{{scale:1.12,transformOrigin:"50% 50%",duration:.25,yoyo:true,repeat:3,ease:"sine.inOut"}},{t_staerker - 0.3:.3f});')
pop("#d-p1", t_staerker); pop("#d-p2", t_bleibt)

# E Bild an die Wand malen – Decke drüber
frame_ = f'<rect x="290" y="470" width="500" height="560" fill="#ffffff" stroke="{INK}" stroke-width="8"/>' + sixpack(540, 750, .9)
blanket = (f'<path d="M 250 430 L 830 430 L 860 1080 Q 760 1050 680 1090 Q 580 1050 500 1090 Q 400 1050 320 1090 Q 270 1060 220 1080 Z" fill="{PINK}" stroke="{INK}" stroke-width="6"/>'
           + "".join(f'<line x1="{x}" y1="440" x2="{x+10}" y2="1060" stroke="#ffffff" stroke-width="10" opacity=".7"/>' for x in (330, 450, 570, 690)))
E = f'<rect x="0" y="0" width="1080" height="1300" fill="#EFE6DA"/>' + frame_ + g("e-bl", blanket, 0) + pill("e-p", 540, 1200, "Decke = Fett", "red", 44)
scene("e", t_das_ist, t_und_drei, E)
tw(f'tl.fromTo("#e-bl",{{opacity:1,y:-1300}},{{y:0,duration:.45,ease:"bounce.out"}},{t_decke - 0.1:.3f});')
pop("#e-p", t_decke + 0.4)

# F 3 Minuten Workout = ein Keks
F = (player(300, 860, 360, 220, "3:00") + text(560, 880, "=", 110, INK, 900) + cookie(800, 860, 110) + pill("f-p", 540, 1140, "≈ 25 kcal", "lila", 48))
scene("f", t_und_drei, t_den, F)
pop("#f-p", t_keks)

# G … den du danach als Belohnung isst
G = (ground(1290) + stick("g", 420, 1290, 1.3, "laugh", "hold") + cookie(560, 935, 45)
     + "".join(f'<circle cx="{x}" cy="{y}" r="6" fill="#D9A55B"/>' for x, y in ((520, 1000), (545, 1040), (500, 1080)))
     + pill("g-p", 760, 560, "Belohnung", "red", 46))
scene("g", t_den, t_genau, G)
pop("#g-p", t_belohnung)

# H (dunkel) Genau wie gestern.
couch = (f'<rect x="240" y="1060" width="620" height="120" rx="30" fill="{CURTAIN}" stroke="#ffffff" stroke-width="4"/>'
         f'<rect x="240" y="940" width="620" height="140" rx="30" fill="#4A3060" stroke="#ffffff" stroke-width="4"/>')
H = (f'<rect width="1080" height="1920" fill="{DARK}"/>' + text(540, 330, "Tag 1 (schon wieder)", 44, "#ffffff", 800)
     + couch + stick("h", 540, 1180, 1.0, "neutral", "hold", white=True, extra=belly(0, -270, .9)) + cookie(650, 920, 32)
     + f'<rect x="700" y="1000" width="110" height="70" rx="10" fill="#D9A55B" stroke="#ffffff" stroke-width="3"/>' + text(755, 1046, "KEKSE", 24, "#3a2410", 900))
scene("h", t_genau, t_das_w, H, dark=True)

# I 2011 getestet – sechs Wochen nur Bauchübungen
crunchers = "".join(f'<g transform="translate({x},880)"><line x1="-50" y1="0" x2="20" y2="-50" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
                    f'<circle cx="34" cy="-64" r="22" fill="#ffffff" stroke="{INK}" stroke-width="5"/><path d="M -50 0 L -10 -40 L 20 0" stroke="{INK}" stroke-width="8" fill="none" stroke-linecap="round"/></g>' for x in (300, 480, 660, 840))
I_ = polaroid(150, 500, 780, 640, -3, crunchers, "2011") + pill("i-p", 540, 410, "6 Wochen Bauchübungen", "lila", 40)
scene("i", t_das_w, t_ergebnis, I_)
pop("#i-p", t_sechs)

# J Ergebnis? – Bauchfett gleich – gar nichts
scene("j1", t_ergebnis, t_das_b, qmark(540, 860, 300))
rows = [("j-r0", "Bauchfett weniger", t_das_b + 0.3), ("j-r1", "am Bauch", t_nicht_am), ("j-r2", "am Körper", t_koerper)]
J2 = text(540, 420, "Bauchübungen ändern:", 58, INK, 900)
for k, (rid, t, tt) in enumerate(rows):
    J2 += listrow(rid, 140, 600 + k * 150, 800, t, "x", 46)
J2 += g("j-gn", text(540, 1180, "gar nichts", 80, RED, 900), 0)
scene("j2", t_das_b, t_fett, J2)
for rid, t, tt in rows:
    pop(f"#{rid}", tt - 0.05, .85)
pop("#j-gn", t_gar)

# K Fett verlierst du überall ein bisschen – über die Ernährung
dots = "".join(f'<circle cx="{x}" cy="{y}" r="16" fill="#FBE7B0" stroke="{INK}" stroke-width="3"/>' for x, y in ((470, 640), (610, 650), (430, 820), (650, 830), (540, 760), (500, 1000), (590, 1000), (540, 560)))
K1 = (ground(1290) + stick("k", 540, 1290, 1.6, "neutral", "down") + g("k-d", dots, 1)
      + pill("k-p", 540, 380, "überall ein bisschen", "lila", 44))
scene("k1", t_fett, t_ueber, K1)
pop("#k-p", t_sondern)
tw(f'tl.to("#k-d > circle",{{scale:.4,transformOrigin:"50% 50%",duration:1.2,ease:"sine.inOut"}},{t_sondern:.3f});')
plate = (f'<ellipse cx="540" cy="860" rx="300" ry="90" fill="#ffffff" stroke="{INK}" stroke-width="6"/><ellipse cx="540" cy="850" rx="220" ry="58" fill="#F3ECE5" stroke="{INK}" stroke-width="3"/>'
         f'<circle cx="470" cy="830" r="40" fill="#7BD88F" stroke="{INK}" stroke-width="4"/><rect x="530" y="805" width="110" height="50" rx="20" fill="#E8A07A" stroke="{INK}" stroke-width="4"/>'
         f'<line x1="200" y1="760" x2="200" y2="960" stroke="{INK}" stroke-width="10" stroke-linecap="round"/><line x1="880" y1="760" x2="880" y2="960" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>')
K2 = plate + pill("k2-p", 540, 600, "Ernährung", "lila", 52)
scene("k2", t_ueber, t_also, K2)
pop("#k2-p", t_ernaehrung)

# L So geht's
rows2 = [("l-r0", "Weniger futtern", t_weniger), ("l-r1", "Mehr bewegen", t_mehr), ("l-r2", "Genug schlafen", t_genug), ("l-r3", "Geduld", t_geduld)]
L = text(540, 420, "So geht's:", 64, INK, 900)
for k, (rid, t, tt) in enumerate(rows2):
    L += listrow(rid, 140, 580 + k * 150, 800, t, "check", 46)
scene("l", t_also, t_hoer, L)
for rid, t, tt in rows2:
    pop(f"#{rid}", tt - 0.05, .85)

# M Spiegel – da ist noch nichts (+ Nachlauf)
M = (ground(1290) + stick("m", 330, 1290, 1.25, "smile", "down", moods=("neutral", "sad"), extra=belly(0, -270, .95))
     + mirror(780, 900, 300, 560, f'<g>{stick("mm", 780, 1150, .75, "neutral", "down", extra=belly(0, -270, .95))}</g>')
     + g("m-x", xcircle(940, 560, 50), 0))
scene("m", t_hoer, TOTAL, M)
mood("m", t_da_ist, "smile", "neutral"); pop("#m-x", t_nichts_end, .5)
tw(f'tl.to("#m-x",{{scale:1.15,transformOrigin:"50% 50%",duration:.35,yoyo:true,repeat:3,ease:"sine.inOut"}},{VO_END + 0.3:.3f});')
mood("m", VO_END + 1.2, "neutral", "sad")

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
    txt = txt0.replace("Drei-Minuten", "3-Minuten").replace("zweitausendelf", "2011")
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
    <title>Sixpack</title>
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
