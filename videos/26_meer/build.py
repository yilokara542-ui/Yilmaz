#!/usr/bin/env python3
"""Video 26 „Das Meer ist blau, weil es den Himmel spiegelt?“ – Format D „Strichmännchen-Mythos“ (Skill 11c).

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
t_spiegelt0 = ws("spiegelt"); t_du_f = ws("Du", t_spiegelt0)
t_ha = [w for w in W if w["s"] == t_spiegelt0][0]["e"] + 0.15; t_gag = t_du_f - 0.3
t_wasser = ws("Wasser", t_du_f + 0.5); t_blau1 = ws("blau", t_wasser)
t_es = ws("Es", t_blau1); t_rotes = ws("rotes"); t_tiefer = ws("tiefer"); t_uebrig = ws("Übrig")
t_vollpf = ws("Vollpfosten") - 0.25
t_in = ws("In", t_vollpf + 0.3); t_glas = ws("Glas"); t_wenig = ws("wenig")
t_wie = ws("Wie", t_wenig); t_sonnen = ws("Sonnenbrillen"); t_zehn = ws("Zehn", t_sonnen); t_dunkel = ws("dunkel")
t_genau = ws("Genau"); t_witze = ws("Witze")
t_1921 = ws("Neunzehnhundert"); t_filter = ws("Filter")
t_ergebnis = ws("Ergebnis", t_1921); t_das_m = ws("Das", t_ergebnis); t_blau2 = ws("blau", t_das_m)
t_hohl = ws("Hohlbrot") - 0.25
t_und_d = ws("Und", t_hohl + 0.3); t_algen = ws("Algen"); t_schlamm = ws("Schlamm"); t_sand = ws("Sand")
t_also = ws("Also"); t_obendrauf = ws("obendrauf"); t_farbe = ws("Farbe", t_obendrauf); t_selbst = ws("selbst", t_farbe)
t_hoer = ws("Und", t_selbst); t_urlaub = ws("Urlaub"); t_lauch = ws("Lauch") - 0.25

INSULTS = ("Bastard", "Vollpfosten", "Hohlbrot", "Lauch")   # werden nie untertitelt

# ================= BAUSTEINE =================
SEA = "#3B82C4"; SEA2 = "#1F5F99"; SKY = "#BFE3F5"


def sea_band(y0=900, h=400, col=SEA):
    waves = "".join(f'<path d="M {x} {y0} q 45 -24 90 0" stroke="#ffffff" stroke-width="6" fill="none" opacity=".7"/>' for x in range(0, 1080, 90))
    return f'<rect x="0" y="{y0}" width="1080" height="{h}" fill="{col}"/>' + waves


def sun(x, y, r=70):
    rays = "".join(f'<line x1="{x}" y1="{y}" x2="{x + (r+40)*__import__("math").cos(i*0.785):.0f}" y2="{y + (r+40)*__import__("math").sin(i*0.785):.0f}" stroke="{YEL}" stroke-width="10" stroke-linecap="round"/>' for i in range(8))
    return rays + f'<circle cx="{x}" cy="{y}" r="{r}" fill="{YEL}" stroke="{INK}" stroke-width="5"/>' + face("smile", x, y, INK, .9)


def insult_gag(sid, t0, t1, prop):
    """Kurzer Bild-Gag zu einer Beleidigung (ohne Text): Figur + passendes Objekt."""
    inner = ground(1290) + stick(sid, 320, 1290, 1.25, "shock", "down", stubble=True) + g(f"{sid}-o", prop, 0)
    scene(sid, t0, t1, inner)
    pop(f"#{sid}-o", t0 + 0.1, .5, .2)


# ================= SZENEN =================
# A1 Hook: Strand – „Meer spiegelt Himmel“ – HA
A1 = (f'<rect x="0" y="0" width="1080" height="900" fill="{SKY}"/>' + sun(840, 260) + sea_band(820, 480)
      + f'<rect x="0" y="1180" width="1080" height="120" fill="#F2D8A0"/>' + stick("a1", 300, 1290, 1.2, "smug", "shrug")
      + g("a1-ar", f'<path d="M 600 330 Q 760 520 640 860" stroke="{LILA}" stroke-width="10" fill="none" stroke-dasharray="20 14"/><path d="M 620 840 L 640 880 L 670 845" stroke="{LILA}" stroke-width="10" fill="none" stroke-linecap="round"/>', 0)
      + g("a1-ha", text(260, 560, "HA", 120, RED, 900) + text(140, 470, "HA", 80, RED, 900)))
scene("a1", 0, t_gag, A1)
pop("#a1-ar", t_spiegelt0 - 0.1); pop("#a1-ha", t_ha, .5, .2)

# A2 Gag (ohne Untertitel)
A2 = ground(1290) + stick("a2", 330, 1290, 1.25, "shock", "down", stubble=True) + g("a2-fg", finger(470, 760, 1.0), 1)
scene("a2", t_gag, t_wasser, A2)
tw(f'tl.fromTo("#a2-fg",{{x:700}},{{x:0,duration:.35,ease:"power3.out"}},{t_gag + 0.05:.3f});')
tw(f'tl.to("#a2-fg",{{x:-24,duration:.12,yoyo:true,repeat:3,ease:"sine.inOut"}},{t_gag + 0.5:.3f});')

# B Wasser ist selbst ein bisschen blau
bigdrop = f'<g transform="translate(540,800) scale(9)"><path d="M 0 -30 C 6 -14 20 -2 20 10 A 20 20 0 0 1 -20 10 C -20 -2 -6 -14 0 -30 Z" fill="#9CCBEF" stroke="{INK}" stroke-width=".7"/></g>'
B = bigdrop + face("smile", 540, 860, INK, 2.2) + pill("b-p", 540, 1230, "selbst ein bisschen blau", "lila", 44)
scene("b", t_wasser, t_es, B)
pop("#b-p", t_blau1 - 0.2)

# C Rotes Licht wird geschluckt – Blau bleibt
cols = ((RED, "c-l0"), ("#F28C28", "c-l1"), (YEL, "c-l2"), ("#7BD88F", "c-l3"), (BLUE, "c-l4"))
depth = f'<defs><linearGradient id="dg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9CCBEF"/><stop offset="1" stop-color="{SEA2}"/></linearGradient></defs>'
C = depth + f'<rect x="120" y="520" width="840" height="720" rx="20" fill="url(#dg)" stroke="{INK}" stroke-width="6"/>' + sun(540, 380, 55)
lens = (300, 230, 160, 110, 720)
for k, (c, cid) in enumerate(cols):
    x = 300 + k * 120
    C += f'<g id="{cid}"><rect x="{x-18}" y="520" width="36" height="720" fill="{c}" opacity=".85"/></g>'
C += pill("c-p1", 220, 1170, "Rot weg", "red", 40) + g("c-p2", pill("c-p20", 820, 1170, "Blau bleibt", "lila", 40, 1), 0)
C += "".join(text(975, 560 + i*220, f"{i*10} m", 30, INK, 800, "start") for i in range(4))
scene("c", t_es, t_vollpf, C)
for k, (c, cid) in enumerate(cols):
    tw(f'tl.fromTo("#{cid}",{{scaleY:1,transformOrigin:"50% 0%"}},{{scaleY:{lens[k]/720:.3f},duration:1.0,ease:"sine.inOut"}},{t_rotes + k*0.25:.3f});')
pop("#c-p1", t_rotes + 0.2); pop("#c-p2", t_uebrig)

# D Gag „Du Vollpfosten.“ – Pfosten mit Gesicht
post = f'<rect x="640" y="720" width="120" height="570" fill="#A9773F" stroke="{INK}" stroke-width="6"/><ellipse cx="700" cy="720" rx="60" ry="16" fill="#C8924A" stroke="{INK}" stroke-width="5"/>' + face("neutral", 700, 820, INK, 1.0) + text(560, 900, "=", 90, INK, 900)
insult_gag("d", t_vollpf, t_in, post)

# E Glas: klar – Pool: blau
glass = f'<path d="M 200 700 L 420 700 L 390 1150 L 230 1150 Z" fill="#EAF6FD" stroke="{INK}" stroke-width="6"/><rect x="215" y="800" width="190" height="10" fill="#D6EEF9"/>'
pool = f'<rect x="560" y="760" width="420" height="390" rx="20" fill="{SEA}" stroke="{INK}" stroke-width="6"/>' + "".join(f'<path d="M {x} 800 q 30 -16 60 0" stroke="#ffffff" stroke-width="5" fill="none" opacity=".7"/>' for x in range(580, 960, 70))
E = glass + pool + pill("e-p1", 310, 600, "klar", "white", 44) + g("e-p2", pill("e-p20", 770, 600, "viel Wasser = blau", "lila", 40, 1), 0)
scene("e", t_in, t_wie, E)
pop("#e-p1", t_glas); pop("#e-p2", t_wenig)

# F Sonnenbrillen-Gläser stapeln
F = ""
for k in range(10):
    F += f'<g id="f-g{k}" opacity="{1 if k == 0 else 0}"><ellipse cx="{300 + k*48}" cy="820" rx="150" ry="110" fill="#5A6B7A" opacity=".22" stroke="{INK}" stroke-width="4"/></g>'
F += pill("f-p1", 300, 600, "1 Glas", "white", 44) + g("f-p2", pill("f-p20", 760, 600, "10 Gläser", "lila", 44, 1), 0)
scene("f", t_wie, t_genau, F)
for k in range(1, 10):
    pop(f"#f-g{k}", t_zehn + k * 0.08, .8, .1)
pop("#f-p1", t_sonnen); pop("#f-p2", t_zehn)

# G (dunkel) Genau wie deine Witze
mic = f'<line x1="640" y1="900" x2="640" y2="1290" stroke="#ffffff" stroke-width="8"/><ellipse cx="640" cy="890" rx="22" ry="30" fill="#ffffff"/>'
tumble = f'<g id="g-tw"><circle cx="0" cy="0" r="34" fill="none" stroke="#C8924A" stroke-width="5"/><path d="M -24 -20 L 24 20 M -24 20 L 24 -20 M 0 -34 L 0 34" stroke="#C8924A" stroke-width="4"/></g>'
G = (f'<rect width="1080" height="1920" fill="{DARK}"/>' + f'<polygon points="380,300 700,300 900,1290 180,1290" fill="#ffffff" opacity=".06"/>' + mic
     + stick("g", 500, 1290, 1.15, "smug", "hold", white=True) + text(540, 300, "Witz 10 von 10", 44, "#ffffff", 800)
     + f'<g transform="translate(-100,1250)">{tumble}</g>')
scene("g", t_genau, t_1921, G, dark=True)
tw(f'tl.fromTo("#g-tw",{{x:0,rotation:0}},{{x:1300,rotation:720,duration:{t_1921 - t_genau:.3f},ease:"none"}},{t_genau:.3f});')

# H 1921 – Forscher filtert die Spiegelung weg
ship = (f'<path d="M 300 900 L 780 900 L 720 1000 L 360 1000 Z" fill="#ffffff" stroke="{INK}" stroke-width="5"/><rect x="440" y="820" width="80" height="80" fill="#C9CED6" stroke="{INK}" stroke-width="4"/>'
        f'<rect x="460" y="760" width="26" height="60" fill="{INK}"/>' + f'<rect x="200" y="1000" width="680" height="120" fill="{SEA}"/>'
        + stick("hs", 640, 900, .45, "neutral", "hold") + f'<circle cx="700" cy="790" r="18" fill="#BFE3F5" stroke="{INK}" stroke-width="4"/>')
H = polaroid(150, 480, 780, 680, -3, ship, "1921") + pill("h-p", 540, 390, "Spiegelung weggefiltert", "lila", 44)
scene("h", t_1921, t_ergebnis, H)
pop("#h-p", t_filter)

# I Ergebnis? – immer noch blau
scene("i1", t_ergebnis, t_das_m, qmark(540, 860, 300))
I2 = f'<rect x="120" y="560" width="840" height="560" rx="20" fill="{SEA}" stroke="{INK}" stroke-width="6"/>' + "".join(f'<path d="M {x} 620 q 45 -24 90 0" stroke="#ffffff" stroke-width="6" fill="none" opacity=".7"/>' for x in range(140, 940, 100))
I2 += g("i-c", checkcircle(540, 840, 90), 0) + g("i-p", pill("i-p0", 540, 1230, "immer noch blau", "lila", 50, 1), 0)
scene("i2", t_das_m, t_hohl, I2)
pop("#i-c", t_blau2 - 0.2); pop("#i-p", t_blau2)

# J Gag „Du Hohlbrot.“ – hohles Brot
bread = (f'<path d="M 560 1100 Q 540 860 700 840 Q 860 860 840 1100 Z" fill="#D9A55B" stroke="{INK}" stroke-width="6"/>'
         f'<path d="M 610 1080 Q 600 920 700 905 Q 800 920 790 1080 Z" fill="#F3ECE5" stroke="{INK}" stroke-width="4"/>' + text(520, 990, "=", 90, INK, 900))
insult_gag("j", t_hohl, t_und_d, bread)

# K Algen grün – Schlamm braun – Sand türkis
sw = [("k-s0", "#3E8E5A", "Algen", t_algen), ("k-s1", "#7A5A3A", "Schlamm", t_schlamm), ("k-s2", "#3FC9C0", "heller Sand", t_sand)]
K = text(540, 420, "Nicht überall blau:", 58, INK, 900)
for k, (sid, c, lab, tt) in enumerate(sw):
    K += g(sid, f'<rect x="{110 + k*300}" y="600" width="260" height="440" rx="24" fill="{c}" stroke="{INK}" stroke-width="6"/>' + text(240 + k*300, 1110, lab, 40, INK, 900), 0)
scene("k", t_und_d, t_also, K)
for sid, c, lab, tt in sw:
    pop(f"#{sid}", tt - 0.05, .7)

# L Himmel nur obendrauf – Farbe aus dem Wasser
L = (f'<rect x="120" y="520" width="840" height="720" rx="20" fill="url(#dg2)" stroke="{INK}" stroke-width="6"/>'
     f'<defs><linearGradient id="dg2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9CCBEF"/><stop offset="1" stop-color="{SEA2}"/></linearGradient></defs>'
     + g("l-top", f'<rect x="120" y="520" width="840" height="40" fill="{SKY}" stroke="{LILA}" stroke-width="5" stroke-dasharray="16 10"/>' + pill("l-p10", 540, 450, "Spiegelung: nur obendrauf", "lila", 40, 1), 0)
     + g("l-in", pill("l-p20", 540, 1000, "Farbe: aus dem Wasser", "white", 44, 1), 0))
scene("l", t_also, t_hoer, L)
pop("#l-top", t_obendrauf - 0.3); pop("#l-in", t_farbe)

# M Urlaub: allen erklären – Gag „Du Lauch.“ (+ Nachlauf)
leek = (f'<rect x="820" y="760" width="60" height="460" rx="28" fill="#F4F1E6" stroke="{INK}" stroke-width="5"/>'
        f'<path d="M 830 780 L 780 520 M 850 770 L 850 500 M 870 780 L 930 540" stroke="#3E8E5A" stroke-width="30" stroke-linecap="round"/>'
        + text(740, 1000, "=", 80, INK, 900))
M = (f'<rect x="0" y="0" width="1080" height="900" fill="{SKY}"/>' + sea_band(820, 360) + f'<rect x="0" y="1180" width="1080" height="120" fill="#F2D8A0"/>'
     + stick("m", 260, 1290, 1.1, "smug", "shrug", moods=("neutral", "sad"))
     + stick("m1", 500, 1290, .9, "neutral", "down", moods=("sleep_",)) + stick("m2", 640, 1290, .9, "neutral", "down")
     + g("m-z", text(560, 760, "z z z", 44, INK, 900), 0) + g("m-l", leek, 0))
scene("m", t_hoer, TOTAL, M)
pop("#m-z", t_urlaub + 0.5)
tw(f'tl.set("#m1",{{opacity:0}},{t_lauch:.3f});'); tw(f'tl.set("#m2",{{opacity:0}},{t_lauch:.3f});'); tw(f'tl.set("#m-z",{{opacity:0}},{t_lauch:.3f});')
pop("#m-l", t_lauch, .5, .2); mood("m", t_lauch, "smug", "neutral"); mood("m", VO_END + 1.2, "neutral", "sad")

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
    txt = txt0.replace("Neunzehnhunderteinundzwanzig", "1921")
    if blocks and not any(x in txt or x in blocks[-1]["txt"] for x in INSULTS) and len(blocks[-1]["txt"]) + len(txt) + 1 <= 36 and s_[0]["s"] - blocks[-1]["e"] < 0.6:
        blocks[-1]["txt"] += " " + txt; blocks[-1]["e"] = s_[-1]["e"]
    else:
        blocks.append({"txt": txt, "s": s_[0]["s"], "e": s_[-1]["e"]})
subs = []
for k, b in enumerate(blocks):
    if any(x in b["txt"] for x in INSULTS):   # Beleidigung nur hörbar
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
    <title>Meer blau</title>
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
