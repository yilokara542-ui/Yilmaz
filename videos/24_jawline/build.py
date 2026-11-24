#!/usr/bin/env python3
"""Video 24 „Kaugummi = Jawline?“ – Format D „Strichmännchen-Mythos“ (Skill 11c).

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
t_kaust = ws("kaust"); t_jaw0 = ws("Jawline"); t_machen = ws("machen", t_jaw0); t_du_f = ws("Du", t_machen)
t_ha = [w for w in W if w["s"] == t_machen][0]["e"] + 0.15; t_gag = t_du_f - 0.3
t_deine = ws("Deine", t_du_f + 0.5); t_knochen1 = ws("Knochen"); t_fett1 = ws("Fett")
t_den = ws("Den", t_fett1); t_eltern = ws("Eltern"); t_fertig = ws("fertig")
t_und_das = ws("Und", t_fertig); t_kaust2 = ws("kaust", t_und_das)
t_kauen = ws("Kauen", t_kaust2); t_kaumuskel = ws("Kaumuskel"); t_breiter = ws("breiter"); t_schaerfer = ws("schärfer")
t_das_ist = ws("Das", t_schaerfer); t_bizeps = ws("Bizeps"); t_bauch = ws("Bauch")
t_genau = ws("Genau"); t_null = ws("null")
t_1999 = ws("Neunzehnhundert"); t_elf = ws("elf")
t_ergebnis = ws("Ergebnis", t_1999); t_kg = ws("Kaugummi", t_ergebnis); t_k2 = ws("Knochen", t_kg); t_f2 = ws("Fett", t_k2); t_kinn2 = ws("Kinnlinie", t_f2)
t_dafuer = ws("Dafür"); t_kiefer = ws("Kiefer", t_dafuer)
t_und_auf = ws("Und", t_kiefer); t_packung = ws("Packung"); t_abfuehrend = ws("abführend")
t_also = ws("Also"); t_kfett = ws("Körperfett"); t_gerade = ws("gerade"); t_kopf = ws("Kopf", t_gerade)
t_hoer = ws("Und", t_kopf); t_kuh = ws("Kuh"); t_deine2 = ws("Deine", t_kuh); t_brei = ws("Kartoffelbrei")

# ================= BAUSTEINE =================
def note(nid, x, y, s=1.0, col="#fff", op=0):
    return (f'<g id="{nid}" opacity="{op}"><g transform="translate({x},{y}) scale({s})">'
            f'<ellipse cx="0" cy="0" rx="24" ry="17" fill="{col}" transform="rotate(-20)"/><rect x="16" y="-92" width="9" height="92" fill="{col}"/>'
            f'<path d="M 25 -92 Q 58 -80 50 -40 Q 44 -64 25 -66 Z" fill="{col}"/></g></g>')


CAT = "#F2A65A"


FAT = "#FBE7B0"; BONE = "#F7F3EA"


def profile(gid, x, y, s=1.0, fat=True, wide=False, extra=""):
    """Kopf im Profil (Blick nach rechts) mit Kieferknochen und optionaler Fettschicht. (x,y)=Kinn."""
    fat_ = (f'<path d="M -150 -70 Q -60 60 40 30 Q 80 20 90 -10 L 70 -40 Q 0 0 -110 -110 Z" fill="{FAT}" stroke="{INK}" stroke-width="4"/>' if fat else "")
    return (f'<g id="{gid}"><g transform="translate({x},{y}) scale({s})">'
            f'<path d="M -170 -380 Q -40 -470 70 -360 Q 110 -300 100 -230 L 120 -180 L 95 -170 Q 100 -120 80 -60 L 70 -40 Q 0 0 -110 -110 Q -150 -150 -170 -250 Z" fill="#ffffff" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M -120 -150 L -110 -110 Q 0 0 70 -40 L 60 -70 Q -10 -40 -90 -150 Z" fill="{BONE}" stroke="{INK}" stroke-width="4"/>'
            + fat_ + f'<circle cx="30" cy="-260" r="9" fill="{INK}"/>' + extra + '</g></g>')


def gum_bubble(gid, x, y, r=40, op=1):
    return g(gid, f'<circle cx="{x}" cy="{y}" r="{r}" fill="{PINK}" stroke="{INK}" stroke-width="4"/><path d="M {x-r*0.5} {y-r*0.4} Q {x-r*0.3} {y-r*0.7} {x} {y-r*0.75}" stroke="#ffffff" stroke-width="5" fill="none" stroke-linecap="round"/>', op)


def jaw_face(gid, x, y, s=1.0, sharp=False):
    """Gesicht frontal: rund (Kartoffel) oder kantig (Jawline)."""
    if sharp:
        shape = f'<path d="M -70 -110 L 70 -110 L 80 10 L 30 80 L -30 80 L -80 10 Z" fill="#ffffff" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
    else:
        shape = f'<ellipse cx="0" cy="-10" rx="85" ry="95" fill="#ffffff" stroke="{INK}" stroke-width="6"/>'
    return f'<g id="{gid}"><g transform="translate({x},{y}) scale({s})">{shape}{face("neutral", 0, -20, INK, 1.0)}</g></g>'


# ================= SZENEN =================
# A1 Hook: Kaugummi vor dem Spiegel – träumt von Jawline – HA
A1 = (ground(1290) + stick("a1", 300, 1290, 1.25, "smug", "down", extra=gum_bubble("a1-gum", 20, -385, 18))
      + mirror(760, 900, 280, 520, f'<g>{jaw_face("a1m", 760, 860, .9)}</g>')
      + g("a1-c", cloud(640, 430, 1.1, jaw_face("a1j", 640, 440, .5, True)), 0)
      + g("a1-ha", text(260, 560, "HA", 120, RED, 900) + text(140, 470, "HA", 80, RED, 900)))
scene("a1", 0, t_gag, A1)
tw(f'tl.fromTo("#a1-gum",{{scale:.4,transformOrigin:"50% 50%"}},{{scale:1.8,duration:.5,yoyo:true,repeat:3,ease:"sine.inOut"}},0.2);')
pop("#a1-c", t_jaw0 - 0.2); pop("#a1-ha", t_ha, .5, .2)

# A2 Gag (ohne Untertitel)
A2 = ground(1290) + stick("a2", 330, 1290, 1.25, "shock", "down", stubble=True) + g("a2-fg", finger(470, 760, 1.0), 1)
scene("a2", t_gag, t_deine, A2)
tw(f'tl.fromTo("#a2-fg",{{x:700}},{{x:0,duration:.35,ease:"power3.out"}},{t_gag + 0.05:.3f});')
tw(f'tl.to("#a2-fg",{{x:-24,duration:.12,yoyo:true,repeat:3,ease:"sine.inOut"}},{t_gag + 0.5:.3f});')

# B Knochen + Fett
B = (profile("bp", 560, 1050, 1.5) + pill("b-p1", 300, 1200, "Knochen", "white", 44) + leader(360, 1170, 470, 1000)
     + pill("b-p2", 840, 1200, "Fett", "red", 46) + leader(800, 1170, 640, 1040))
scene("b", t_deine, t_den, B)
pop("#b-p1", t_knochen1); pop("#b-p2", t_fett1)

# C Knochen von den Eltern – fertig
C = (ground(1290) + stick("cm", 220, 1290, 1.0, "neutral", "down") + stick("cv", 420, 1290, 1.0, "neutral", "down")
     + stick("ck", 760, 1290, 1.0, "neutral", "down") + text(590, 1000, "=", 90, INK, 900)
     + pill("c-p1", 320, 600, "Eltern", "white", 44) + g("c-p2", pill("c-p20", 760, 600, "fertig gewachsen", "lila", 42, 1), 0))
scene("c", t_den, t_und_das, C)
pop("#c-p1", t_eltern - 0.1); pop("#c-p2", t_fertig)

# D Kauen – Fett bleibt
D = profile("dp", 560, 1050, 1.5) + gum_bubble("d-b", 720, 860, 26) + g("d-p", pill("d-p0", 840, 1200, "Fett bleibt", "red", 46, 1), 0)
scene("d", t_und_das, t_kauen, D)
tw(f'tl.to("#d-b",{{scale:1.6,transformOrigin:"50% 50%",duration:.3,yoyo:true,repeat:5,ease:"sine.inOut"}},{t_und_das:.3f});')
pop("#d-p", t_kaust2)

# E Kaumuskel → Gesicht breiter, nicht schärfer
E = (jaw_face("ef", 540, 900, 2.6) + g("e-m", f'<ellipse cx="330" cy="960" rx="40" ry="70" fill="{PINK}" stroke="{INK}" stroke-width="4" opacity=".8"/><ellipse cx="750" cy="960" rx="40" ry="70" fill="{PINK}" stroke="{INK}" stroke-width="4" opacity=".8"/>', 0)
     + pill("e-p0", 540, 430, "Kaumuskel", "white", 44) + g("e-p1", pill("e-p10", 300, 1220, "breiter ✓", "red", 44, 1), 0) + g("e-p2", pill("e-p20", 780, 1220, "schärfer ✕", "lila", 44, 1), 0))
scene("e", t_kauen, t_das_ist, E)
pop("#e-m", t_kaumuskel); pop("#e-p0", t_kaumuskel)
tw(f'tl.to("#ef",{{scaleX:1.22,transformOrigin:"50% 50%",duration:.6,ease:"power2.out"}},{t_breiter - 0.2:.3f});')
pop("#e-p1", t_breiter); pop("#e-p2", t_schaerfer)

# F wie Bizeps trainieren für flachen Bauch
bic = f'<ellipse cx="80" cy="-290" rx="40" ry="28" fill="#ffffff" stroke="{INK}" stroke-width="6"/>'
F = (ground(1290) + stick("f", 400, 1290, 1.3, "smug", "shrug", extra=bic + belly(0, -270, .95))
     + g("f-x", xcircle(620, 960, 50) + pill("f-p0", 760, 640, "Bauch bleibt", "red", 44, 1), 0) + pill("f-p", 420, 400, "Bizeps-Training", "white", 44))
scene("f", t_das_ist, t_genau, F)
pop("#f-p", t_bizeps); pop("#f-x", t_bauch)

# G (dunkel) Genau wie deine Beziehung
msgs = "".join(f'<rect x="{560}" y="{330 + i*95}" width="360" height="70" rx="26" fill="#5B8CF0"/>' + text(740, 378 + i*95, t, 32, "#ffffff", 800) for i, t in enumerate(("hey", "hey?", "bist du da", "????", "ok")))
G = (f'<rect width="1080" height="1920" fill="{DARK}"/>' + msgs + stick("g", 300, 1300, 1.2, "sad", "hold", white=True) + phone(430, 940, 70, 130, screen="#7FB2FF")
     + text(540, 250, "gesendet: 47 · Antworten: 0", 38, "#ffffff", 800))
scene("g", t_genau, t_1999, G, dark=True)

# H 1999: ~11 kcal pro Stunde
gumpack = f'<rect x="-140" y="-60" width="280" height="120" rx="20" fill="#7BD88F" stroke="{INK}" stroke-width="5"/>' + text(0, 18, "KAUGUMMI", 40, INK, 900)
flame = f'<path d="M 0 -90 Q 50 -30 30 20 Q 15 50 0 50 Q -15 50 -30 20 Q -50 -30 0 -90 Z" fill="#F28C28" stroke="{INK}" stroke-width="5"/>'
H = polaroid(150, 480, 780, 680, -3, f'<g transform="translate(400,800)">{gumpack}</g><g transform="translate(720,800)">{flame}</g>', "1999") + pill("h-p", 540, 390, "≈ 11 kcal pro Stunde", "lila", 46)
scene("h", t_1999, t_ergebnis, H)
pop("#h-p", t_elf)

# I Ergebnis? – gar nichts
scene("i1", t_ergebnis, t_kg, qmark(540, 860, 300))
rows = [("i-r0", "Knochen", t_k2), ("i-r1", "Fett", t_f2), ("i-r2", "Kinnlinie", t_kinn2)]
I2 = text(540, 420, "Kaugummi ändert:", 60, INK, 900)
for k, (rid, t, tt) in enumerate(rows):
    I2 += listrow(rid, 140, 600 + k * 150, 800, t, "x", 46)
I2 += g("i-gn", text(540, 1180, "gar nichts", 80, RED, 900), 0)
scene("i2", t_kg, t_dafuer, I2)
pop("#i-gn", ws("gar", t_kg))
for rid, t, tt in rows:
    pop(f"#{rid}", tt - 0.05, .85)

# J Kiefer überlastet
bolt = f'<path d="M 0 -60 L -24 6 L 4 6 L -12 64 L 30 -10 L 2 -10 L 16 -60 Z" fill="{RED}" stroke="{INK}" stroke-width="4"/>'
J = profile("jp", 560, 1050, 1.5) + g("j-b", f'<g transform="translate(400,780)">{bolt}</g><g transform="translate(470,700)">{bolt}</g>', 0) + pill("j-p", 540, 1250, "Kiefer überlastet", "red", 48)
scene("j", t_dafuer, t_und_auf, J)
pop("#j-b", t_kiefer - 0.1); pop("#j-p", t_kiefer)
tw(f'tl.to("#j-b",{{opacity:.3,duration:.18,yoyo:true,repeat:5}},{t_kiefer + 0.3:.3f});')

# K Packung: abführend
pack = (f'<rect x="240" y="480" width="600" height="300" rx="30" fill="#7BD88F" stroke="{INK}" stroke-width="6"/>' + text(540, 600, "KAUGUMMI", 70, INK, 900)
        + f'<rect x="270" y="650" width="540" height="100" rx="12" fill="#ffffff" stroke="{INK}" stroke-width="3"/>'
        + text(540, 692, "Kann bei übermäßigem Verzehr", 28, INK, 800) + text(540, 732, "abführend wirken.", 28, RED, 900))
K = pack + g("k-t", toilet(540, 1250, 1.0), 0)
scene("k", t_und_auf, t_also, K)
pop("#k-t", t_abfuehrend)

# L So geht's
rows2 = [("l-r0", "Körperfett runter", t_kfett), ("l-r1", "Gerade stehen", t_gerade), ("l-r2", "Kopf nicht nach vorne", t_kopf)]
L = text(540, 420, "So geht's:", 64, INK, 900)
for k, (rid, t, tt) in enumerate(rows2):
    L += listrow(rid, 140, 600 + k * 150, 800, t, "check", 46)
scene("l", t_also, t_hoer, L)
for rid, t, tt in rows2:
    pop(f"#{rid}", tt - 0.05, .85)

# M Kuh – Kartoffelbrei (+ Nachlauf)
cow = (f'<ellipse cx="0" cy="0" rx="90" ry="80" fill="#ffffff" stroke="{INK}" stroke-width="6"/><ellipse cx="-30" cy="-20" rx="26" ry="20" fill="{INK}"/>'
       f'<ellipse cx="0" cy="40" rx="60" ry="34" fill="{PINK}" stroke="{INK}" stroke-width="5"/><circle cx="-18" cy="40" r="6" fill="{INK}"/><circle cx="18" cy="40" r="6" fill="{INK}"/>'
       f'<circle cx="-35" cy="-15" r="7" fill="#ffffff"/><circle cx="35" cy="-15" r="7" fill="{INK}"/>'
       f'<path d="M -70 -60 L -100 -100 M 70 -60 L 100 -100" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>')
mash = (f'<path d="M 640 1000 Q 700 880 780 930 Q 830 860 900 940 Q 960 920 960 1000 Z" fill="#F4DFA0" stroke="{INK}" stroke-width="5"/>'
        + bowl(800, 1000, 380, 160, "#ffffff", BLUE))
M = (ground(1290) + stick("m", 280, 1290, 1.2, "smug", "down", moods=("neutral", "sad"), extra=gum_bubble("m-gum", 20, -385, 16))
     + g("m-cow", f'<g transform="translate(820,560)">{cow}</g>', 0) + g("m-mash", mash + text(560, 960, "=", 80, INK, 900), 0))
scene("m", t_hoer, TOTAL, M)
pop("#m-cow", t_kuh - 0.1)
tw(f'tl.to("#m-cow",{{rotation:6,svgOrigin:"820 560",duration:.15,yoyo:true,repeat:7}},{t_kuh:.3f});')
tw(f'tl.set("#m-cow",{{opacity:0}},{t_deine2:.3f});'); pop("#m-mash", t_brei - 0.2)
mood("m", t_deine2, "smug", "neutral"); mood("m", VO_END + 1.2, "neutral", "sad")
tw(f'tl.to("#m-gum",{{scale:2.4,transformOrigin:"50% 50%",duration:.8,ease:"power1.in"}},{VO_END + 0.3:.3f});')
tw(f'tl.set("#m-gum",{{opacity:0}},{VO_END + 1.1:.3f});')

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
    txt = txt0.replace("Neunzehnhundertneunundneunzig", "1999").replace("elf Kalorien", "11 Kalorien")   # „Du Opfer“ bleibt hier im Untertitel (User-Wunsch)
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
    <title>Jawline</title>
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
