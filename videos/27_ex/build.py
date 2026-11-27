#!/usr/bin/env python3
"""Video 27 „Ex bereut die Trennung?“ – Format D „Strichmännchen-Mythos“ (Skill 11c).

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
t_ex = ws("Ex"); t_haben = ws("haben"); t_werd = ws("Werd"); t_mann = ws("Mann", t_werd); t_bastard = ws("Bastard")
t_ha = [w for w in W if w["s"] == t_haben][0]["e"] + 0.15; t_gag = t_werd - 0.3
t_digga1 = ws("Digga"); t_wochen = ws("Wochen"); t_innerlich = ws("innerlich"); t_abgeschl = ws("abgeschlossen")
t_die_tr = ws("Die", t_abgeschl); t_letzte = ws("letzte")
t_wie = ws("Wie", t_letzte); t_neues = ws("neues"); t_alte = ws("alte", t_neues)
t_und_du = ws("Und", t_alte); t_drei = ws("drei", t_und_du); t_zwanzig = ws("zwanzigsten"); t_profil1 = ws("Profil")
t_2015 = ws("Zweitausendfünfzehn"); t_6000 = ws("sechstausend"); t_laender = ws("Ländern"); t_befragt = ws("befragt")
t_ergebnis = ws("Ergebnis"); t_frauen = ws("Frauen"); t_aber = ws("Aber", t_frauen); t_komplett = ws("komplett")
t_und_m = ws("Und", t_komplett); t_digga2 = ws("Digga", t_und_m); t_nie = ws("nie", t_digga2)
t_was = ws("Was", t_nie); t_ausreden = ws("Ausreden"); t_zocker = ws("Zockernächte"); t_sprach = ws("Sprachnachrichten"); t_gar = ws("Gar", t_sprach)
t_so = ws("So", t_gar); t_kein = ws("Kein", t_so); t_profil2 = ws("Profil", t_kein); t_raus = ws("Raus")
t_digga3 = ws("Digga", t_raus); t_zurueck = ws("zurückschreibt"); t_sie_b = ws("Sie", t_zurueck); t_sie_h = ws("Sie", t_sie_b + 0.1); t_blockiert = ws("blockiert")


# ================= BAUSTEINE =================
def hair():
    """Lange Haare + Pony für die Ex (in Figur-Koordinaten, Kopf bei 0,-418)."""
    return (f'<path d="M -62 -430 Q -66 -490 0 -484 Q 66 -490 62 -430 Q 50 -468 0 -466 Q -50 -468 -62 -430 Z" fill="{HAIR}" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M -60 -440 Q -86 -380 -70 -300 L -48 -300 Q -60 -380 -52 -430 Z" fill="{HAIR}" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M 60 -440 Q 86 -380 70 -300 L 48 -300 Q 60 -380 52 -430 Z" fill="{HAIR}" stroke="{INK}" stroke-width="4"/>')


def woman(fid, x, y, s=1.0, mood="smile", pose="down", moods=(), white=False, extra=""):
    return stick(fid, x, y, s, mood, pose, moods, white, extra=hair() + extra)


def tears(col=WATER):
    return drop(-24, -380, .35, col) + drop(26, -370, .35, col)


def calsheet(x, y, top, big, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})"><rect x="-110" y="-120" width="220" height="240" rx="16" fill="#ffffff" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M -110 -64 L -110 -104 Q -110 -120 -94 -120 L 94 -120 Q 110 -120 110 -104 L 110 -64 Z" fill="{RED}" stroke="{INK}" stroke-width="6"/>'
            + text(0, -78, top, 34, "#ffffff", 900) + text(0, 60, big, 96, INK, 900) + '</g>')


def screen_txt(x, y, t, size=34, col=INK):
    return text(x, y, t, size, col, 900)


# ================= SZENEN =================
# A1 Hook: Du denkst, sie bereut es – Gedankenblase: Ex weint – HA HA
A1 = (ground(1290) + stick("a1", 300, 1290, 1.2, "smile", "down")
      + g("a1-c", cloud(640, 560, 1.25, f'<g transform="translate(650,720) scale(.48)">{woman("a1w", 0, 0, 1.0, "sad", "down", extra=tears())}</g>'), 0)
      + g("a1-ha", text(780, 980, "HA", 120, RED, 900) + text(900, 890, "HA", 80, RED, 900)))
scene("a1", 0, t_gag, A1)
pop("#a1-c", t_ex); pop("#a1-ha", t_ha, .5, .2)

# A2 Gag – „Werd Mann, du Bastard.“ (ohne Untertitel; ernst & herablassend, Zoom/Wackeln/roter Blitz)
A2 = (f'<g id="a2-cam">' + ground(1290) + stick("a2", 330, 1290, 1.25, "shock", "down", stubble=True) + g("a2-fg", finger(470, 760, 1.0), 1) + '</g>'
      + f'<rect id="a2-red" x="0" y="0" width="1080" height="1920" fill="none" stroke="{RED}" stroke-width="60" opacity="0"/>')
scene("a2", t_gag, t_digga1, A2)
tw(f'tl.fromTo("#a2-fg",{{x:700}},{{x:0,duration:.35,ease:"power3.out"}},{t_gag + 0.05:.3f});')
tw(f'tl.to("#a2-fg",{{x:-24,duration:.12,yoyo:true,repeat:3,ease:"sine.inOut"}},{t_gag + 0.5:.3f});')
tw(f'tl.fromTo("#a2-cam",{{scale:1,svgOrigin:"330 760"}},{{scale:1.45,svgOrigin:"330 760",duration:.25,ease:"power4.out"}},{t_mann - 0.05:.3f});')
for k in range(6):
    tw(f'tl.to("#a2-cam",{{x:{(-1)**k * 10},duration:.05}},{t_mann + 0.25 + k*0.05:.3f});')
tw(f'tl.to("#a2-cam",{{x:0,duration:.05}},{t_mann + 0.55:.3f});')
tw(f'tl.fromTo("#a2-red",{{opacity:0}},{{opacity:.8,duration:.15,yoyo:true,repeat:1}},{t_bastard:.3f});')
tw(f'tl.to("#a2-cam",{{scale:1.75,svgOrigin:"330 760",duration:.35,ease:"power2.in"}},{t_bastard:.3f});')

# B Wer Schluss macht, hat Wochen vorher abgeschlossen – Kalender blättert
B = (ground(1290) + woman("b", 260, 1290, 1.15, "neutral", "down")
     + "".join(g(f"b-c{k}", calsheet(720, 640, f"Woche {k+1}", "✓" if k == 2 else f"{k+1}", 1.25), 0) for k in range(3))
     + pill("b-p", 720, 870, "innerlich: fertig", "lila", 46))
scene("b", t_digga1, t_die_tr, B)
for k in range(3):
    pop(f"#b-c{k}", t_wochen + k * 0.35, .8)
pop("#b-p", t_innerlich)

# C Die Trennung = nur noch der letzte Schritt – Treppe
steps = "".join(f'<rect x="{140 + i*170}" y="{1290 - (i+1)*90}" width="{820 - i*170}" height="90" fill="{"#ffffff" if i < 3 else RED_BG}" stroke="{INK}" stroke-width="5"/>' for i in range(4))
C = (ground(1290) + steps + woman("c", 880, 925, .75, "smile", "down") + text(540, 430, "Schritt für Schritt raus", 56, INK, 900)
     + pill("c-p", 805, 978, "Trennung", "red", 34, 0) + pill("c-p2", 540, 560, "letzter Schritt", "red", 52))
scene("c", t_die_tr, t_wie, C)
tw(f'tl.fromTo("#c",{{x:-510,y:270}},{{x:0,y:0,duration:1.2,ease:"steps(3)"}},{t_die_tr:.3f});')
pop("#c-p", t_die_tr + 0.4); pop("#c-p2", t_letzte)

# D Vergleich: altes Handy vs. neues Handy
crack = f'<path d="M -40 -120 L -10 -60 L -40 -10 L 10 40 L -20 110" stroke="{INK}" stroke-width="5" fill="none"/>'
bin_ = (f'<path d="M 120 1290 L 100 1060 L 320 1060 L 300 1290 Z" fill="#9AA3B5" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
        f'<rect x="88" y="1036" width="244" height="30" rx="10" fill="#9AA3B5" stroke="{INK}" stroke-width="6"/>')
D = (ground(1290) + bin_ + g("d-old", phone(210, 760, 180, 340, "#C9CED6", "#6A6A74", f'<g transform="translate(210,760)">{crack}</g>', -8), 1)
     + woman("d", 700, 1290, 1.15, "smile", "hold", extra=f'<g transform="translate(110,-300)">{phone(0, 0, 110, 200, "#BFE3F5")}</g>')
     + pill("d-p1", 210, 520, "alt", "red", 46, 1) + pill("d-p2", 820, 640, "neu", "lila", 46, 0))
scene("d", t_wie, t_und_du, D)
pop("#d-p2", t_neues)
tw(f'tl.to("#d-old",{{y:330,rotation:25,svgOrigin:"210 760",duration:.45,ease:"power2.in"}},{t_alte - 0.2:.3f});')
tw(f'tl.to("#d-p1",{{opacity:0,duration:.1}},{t_alte - 0.2:.3f});')

# E (dunkel) Roast: 3 Uhr nachts, 20. Mal ihr Profil
cone = '<polygon points="760,660 380,1200 1000,1200" fill="#6FB6FF" opacity=".16"/>'
prof = (f'<g transform="translate(760,660)">{phone(0, 0, 150, 270, "#BFE3F5")}'
        f'<circle cx="0" cy="-40" r="30" fill="#ffffff" stroke="{INK}" stroke-width="4"/><path d="M -30 -50 Q 0 -90 30 -50" fill="{HAIR}"/>'
        f'<rect x="-46" y="10" width="92" height="12" rx="6" fill="#9AA3B5"/><rect x="-36" y="34" width="72" height="12" rx="6" fill="#9AA3B5"/></g>')
E = (f'<rect width="1080" height="1920" fill="{DARK}"/>' + cone
     + f'<rect x="0" y="180" width="140" height="1110" fill="{CURTAIN}"/><rect x="940" y="180" width="140" height="1110" fill="{CURTAIN}"/>'
     + stick("e", 470, 1290, 1.2, "sad", "hold", white=True) + prof
     + text(540, 340, "03:00", 110, "#ffffff", 900) + g("e-n", pill("e-p", 540, 450, "Profil-Besuch Nr. 20", "red", 44, 1), 0))
scene("e", t_und_du, t_2015, E, dark=True)
pop("#e-n", t_zwanzig)

# F Beweis 2015 – 5705 Menschen, 96 Länder
crowd = "".join(f'<g transform="translate({250 + c*95},{780 + r*170}) scale(.28)">'
                + (woman(f"fw{r}{c}", 0, 0, 1.0, "neutral") if (r + c) % 2 else stick(f"fm{r}{c}", 0, 0, 1.0, "neutral")) + '</g>'
                for r in range(3) for c in range(7))
F = polaroid(150, 520, 780, 700, -3, crowd, "2015") + pill("f-p1", 330, 400, "5.705 Menschen", "lila", 42) + pill("f-p2", 790, 400, "96 Länder", "lila", 42)
scene("f", t_2015, t_ergebnis, F)
pop("#f-p1", t_6000); pop("#f-p2", t_laender)

# G1 Ergebnis?
scene("g1", t_ergebnis, t_frauen, qmark(540, 860, 300))

# G2 Kurve: Frauen erst stärker, dann komplett erholt – Männer nie ganz
ax = (f'<path d="M 150 420 L 150 1100 L 960 1100" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
      + text(130, 400, "Schmerz", 40, INK, 900, "start") + text(950, 1160, "Zeit", 40, INK, 900, "end"))
fcurve = '<path id="g2-fc" d="M 160 1090 C 220 460 300 450 380 640 S 560 1080 940 1090" stroke="#6A4BD0" stroke-width="14" fill="none" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>'
mcurve = '<path id="g2-mc" d="M 160 1090 C 240 760 320 740 420 800 S 700 840 940 830" stroke="#E3454C" stroke-width="14" fill="none" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>'
G2 = (ax + fcurve + mcurve + pill("g2-p1", 640, 560, "Frauen: erst schlimmer", "lila", 38)
      + pill("g2-p2", 700, 1010, "dann komplett erholt", "lila", 38) + pill("g2-p3", 640, 730, "Männer: nie ganz drüber", "red", 38)
)
scene("g2", t_frauen, t_was, G2)
tw(f'tl.to("#g2-fc",{{strokeDashoffset:0.55,duration:.6,ease:"none"}},{t_frauen:.3f});')
pop("#g2-p1", t_frauen + 0.2)
tw(f'tl.to("#g2-fc",{{strokeDashoffset:0,duration:.9,ease:"none"}},{t_aber:.3f});')
pop("#g2-p2", t_komplett)
tw(f'tl.to("#g2-mc",{{strokeDashoffset:0,duration:1.4,ease:"none"}},{t_und_m:.3f});')
pop("#g2-p3", t_nie)

# H Was sie vermisst – ✕-Liste – „gar nichts“
rows = [("h-r0", "Deine Ausreden", t_ausreden), ("h-r1", "Deine Zockernächte", t_zocker), ("h-r2", "Deine Sprachnachrichten", t_sprach)]
H = text(540, 420, "Was sie von dir vermisst:", 58, INK, 900)
for k, (rid, t, tt) in enumerate(rows):
    H += listrow(rid, 110, 600 + k * 160, 860, t, "x", 44)
H += g("h-gn", text(540, 1220, "gar nichts", 120, RED, 900), 0)
scene("h", t_was, t_so, H)
for rid, t, tt in rows:
    pop(f"#{rid}", tt - 0.05, .85)
pop("#h-gn", t_gar, .5, .2)

# I So geht's – Checkliste
rows2 = [("i-r0", "Kein Kontakt", t_kein), ("i-r1", "Profil nicht checken", t_profil2), ("i-r2", "Raus mit Freunden", t_raus)]
I_ = text(540, 420, "So kommst du drüber weg:", 58, INK, 900)
for k, (rid, t, tt) in enumerate(rows2):
    I_ += listrow(rid, 110, 600 + k * 160, 860, t, "check", 46)
scene("i", t_so, t_digga3, I_)
for rid, t, tt in rows2:
    pop(f"#{rid}", tt - 0.05, .85)

# J Schluss: wartet aufs Zurückschreiben – „blockiert“ (+ Nachlauf)
dots = "".join(f'<circle id="j-d{i}" cx="{-40 + i*40}" cy="0" r="14" fill="{INK}"/>' for i in range(3))
J = (ground(1290) + stick("j", 300, 1290, 1.2, "neutral", "hold", moods=("shock", "sad"))
     + f'<g transform="translate(640,720)">{phone(0, 0, 300, 540, "#BFE3F5")}'
     + g("j-wait", f'<rect x="-110" y="-60" width="220" height="90" rx="40" fill="#ffffff" stroke="{INK}" stroke-width="4"/><g transform="translate(0,-15)">{dots}</g>', 1)
     + g("j-blk", f'<rect x="-128" y="-238" width="256" height="476" rx="28" fill="{RED_BG}"/><circle cx="0" cy="-40" r="70" fill="none" stroke="{RED}" stroke-width="14"/>'
         f'<line x1="-50" y1="10" x2="50" y2="-90" stroke="{RED}" stroke-width="14" stroke-linecap="round"/>' + text(0, 110, "blockiert", 44, RED, 900), 0) + '</g>'
     + pill("j-p", 640, 360, "bereut: nichts", "red", 48))
scene("j", t_digga3, TOTAL, J)
for i in range(3):
    tw(f'tl.to("#j-d{i}",{{opacity:.25,duration:.3,yoyo:true,repeat:5,ease:"sine.inOut"}},{t_digga3 + i*0.15:.3f});')
pop("#j-p", t_sie_b + 0.3)
show("#j-blk", t_blockiert); hide("#j-wait", t_blockiert); mood("j", t_blockiert, "neutral", "shock"); mood("j", VO_END + 0.8, "shock", "sad")

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
    txt = txt0.replace("Zweitausendfünfzehn", "2015").replace("sechstausend", "6000").replace("sechsundneunzig", "96")
    if blocks and "Bastard" not in txt and "Bastard" not in blocks[-1]["txt"] and len(blocks[-1]["txt"]) + len(txt) + 1 <= 36 and s_[0]["s"] - blocks[-1]["e"] < 0.6:
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
    <title>Ex bereut es</title>
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
