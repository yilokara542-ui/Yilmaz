#!/usr/bin/env python3
"""Generator für index.html – Video 18 „Nach 22 Uhr nicht pfeifen“ (Format C · Block-Stadt, Grusel-Story).

Alle Zeiten kommen aus assets/words.json (wortgenaue Voiceover-Zeitstempel).
Aufruf: python3 build.py → index.html + assets/cues.json
"""
import json, re, html, os, math, random, zlib, struct, base64

HERE = os.path.dirname(os.path.abspath(__file__))
W = json.load(open(os.path.join(HERE, "assets/words.json"), encoding="utf-8"))
VO_END = W[-1]["e"]
TOTAL = round(VO_END + 0.4, 2)          # Teil-2-Karte steht noch gut 3 s
XF = 0.3                                 # Überblendung zwischen Szenen
RNG = random.Random(9)

# ---------- Farben: Nacht-Palette (Format B) ----------
SKY1 = "#0b0d26"; SKY2 = "#1d1d4f"; VIO = "#2a2360"; BLD = "#141634"; BLD2 = "#1b1d44"
WIN = "#ffd98a"; LAMP = "#ffd98a"; MOON = "#f4e3a1"; STREET = "#191a33"; WALK = "#25264a"
FIG = "#e2a982"; SKIN2 = "#c98a66"; HAIR = "#3a2a20"; LIP = "#a85a4a"; INK = "#151a21"; RED = "#ff3b3b"; LIME = "#c8f031"; BLUE = "#3b6cff"; WHITE = "#ffffff"
TEAL = "#3fd1c4"; CARD_BG = "#0b0d22"

T = []


def tw(code):
    T.append(code)


def ws(prefix, after=0.0):
    for w in W:
        if w["s"] >= after - 1e-6 and re.sub(r"[^\wäöüÄÖÜß]", "", w["t"]).lower().startswith(prefix.lower()):
            return w["s"]
    raise KeyError(prefix)


def toggle(sel, t_on, t_off=None):
    tw(f'tl.set("{sel}",{{opacity:1}},{t_on:.3f});')
    if t_off is not None:
        tw(f'tl.set("{sel}",{{opacity:0}},{t_off:.3f});')


def pop(sel, t, dur=0.32, frm=0.88):
    # sauberer: nur leichtes Skalieren + weiches Einblenden (Skill 11a „sauberere Animation“)
    tw(f'tl.fromTo("{sel}",{{opacity:0,scale:{max(frm, .94)},transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:{max(dur, .4)},ease:"sine.out"}},{t:.3f});')


def fade_out(sel, t, dur=0.25):
    tw(f'tl.to("{sel}",{{opacity:0,duration:{dur},ease:"sine.inOut"}},{t:.3f});')


def shake(sel, t, n=6, amp=8):
    for i in range(n):
        x = amp * (1 if i % 2 == 0 else -1) * (1 - i / n)
        tw(f'tl.to("{sel}",{{x:{x:.1f},y:{-x/3:.1f},duration:.06,ease:"sine.inOut"}},{t + i*0.06:.3f});')
    tw(f'tl.to("{sel}",{{x:0,y:0,duration:.12,ease:"sine.out"}},{t + n*0.06:.3f});')


def move(sel, t, dur, ease="sine.inOut", **kw):
    vars_ = ",".join(f"{k}:{v}" for k, v in kw.items())
    tw(f'tl.to("{sel}",{{{vars_},duration:{dur:.3f},ease:"{ease}"}},{t:.3f});')


def label(lid, x, y, text, col=RED, size=40, op=0, fill="#0b0d22"):
    w = len(text) * size * 0.66 + 52
    return (f'<g id="{lid}" opacity="{op}"><rect x="{x-w/2:.0f}" y="{y-size*0.95:.0f}" width="{w:.0f}" height="{size*1.42:.0f}" rx="{size*0.71:.0f}" '
            f'fill="{fill}" fill-opacity=".9" stroke="{col}" stroke-width="5"/>'
            f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Poppins, sans-serif" font-weight="700" font-size="{size}" fill="{col}">{html.escape(text)}</text></g>')


def pill(pid, x, y, text, bg, fg="#fff", size=46, op=0):
    w = len(text) * size * 0.64 + 70
    return (f'<g id="{pid}" opacity="{op}"><rect x="{x-w/2:.0f}" y="{y-size*1.05:.0f}" width="{w:.0f}" height="{size*1.6:.0f}" rx="{size*0.8:.0f}" fill="{bg}"/>'
            f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Poppins, sans-serif" font-weight="700" font-size="{size}" fill="{fg}">{html.escape(text)}</text></g>')


def xmark(xid, cx, cy, r=110, op=0):
    return (f'<g id="{xid}" opacity="{op}"><rect x="{cx-16}" y="{cy-r}" width="32" height="{2*r}" rx="16" fill="{RED}" transform="rotate(45 {cx} {cy})"/>'
            f'<rect x="{cx-16}" y="{cy-r}" width="32" height="{2*r}" rx="16" fill="{RED}" transform="rotate(-45 {cx} {cy})"/></g>')


SCENES = []


def scene(sid, t0, t1, inner, drift=True):
    SCENES.append((sid, t0, t1, f'<g id="{sid}-cam">{inner}</g>'))
    if drift:
        tw(f'tl.fromTo("#{sid}-cam",{{scale:1,rotation:-0.4,svgOrigin:"540 960"}},{{scale:1.06,rotation:0.4,duration:{t1-t0+XF:.3f},ease:"sine.inOut"}},{t0:.3f});')




# ================= CUES =================
t_pf0 = ws("pfeifen"); t_schild = ws("Schild"); t_spiel = ws("Spielplatz"); t_um = ws("Um")
t_fenster = ws("Fenster"); t_baecker = ws("Bäcker"); t_nachb = ws("Nachbarin"); t_buerg = ws("Bürgermeister")
t_kinder = ws("Kinder"); t_mund = ws("Mund")
t_oma = ws("Oma"); t_egal = ws("Egal"); t_pfeif1 = ws("Pfeif", t_egal)
t_aber = ws("Aber"); t_neu = ws("neu", t_aber); t_laech = ws("lächerlich")
t_also = ws("Also"); t_strasse = ws("Straße"); t_turm = ws("Turmuhr"); t_22 = ws("zweiundzwanzig", t_turm)
t_und_pf = ws("Und", t_22); t_pfeifst = ws("pfeifst"); t_stille = ws("Stille"); t_wind = ws("Wind"); t_hund = ws("Hund"); t_gar = ws("Gar")
t_dann1 = ws("Dann", t_gar); t_pfeift2 = ws("pfeift", t_dann1); t_melodie1 = ws("Melodie"); t_wald = ws("Wald")
t_ueber = ws("Überall"); t_nur = ws("Nur", t_ueber); t_du_r = ws("rennst") - 0.1
t_schliesst = ws("schließt"); t_ab = ws("ab", t_schliesst); t_herz = ws("Herz")
t_dann2 = ws("Dann", t_herz); t_klopft = ws("klopft"); t_dreimal = ws("Dreimal")
t_und_d = ws("Und", t_dreimal); t_tuer = ws("Tür"); t_pfeift3 = ws("pfeift", t_tuer); t_leise = ws("leise"); t_melodie2 = ws("Melodie", t_leise)
t_durch = ws("Durch"); t_gelbe = ws("gelbe"); t_laecheln = ws("Lächeln"); t_breit = ws("breit")
t_am = ws("Am", t_breit); t_rathaus = ws("Rathaus"); t_schild2 = ws("Schild", t_rathaus)
t_darauf = ws("Darauf"); t_name = ws("Name"); t_gepf = ws("gepfiffen")
t_oma2 = ws("Oma", t_gepf); t_wald2 = ws("Wald", t_oma2); t_gesagt = ws("gesagt"); t_denn = ws("Denn")

# ================= BAUSTEINE (Format C · Block-Stadt, jetzt bei Nacht) =================
import sys as _s2, math as _m
_s2.path.insert(0, os.path.join(HERE, "../../branding/roblox"))
from block import block, box, shade
YEL = "#d8f53c"; CYAN = "#5ff0d4"; GOLD = "#ffd23f"
DANGER = []
FIGS = []
FIGC_DEFS = ""
brand_html = []

PEOPLE = [  # (shirt, pants, skin, hair, style)
    ("#3b6cff", "#2c3a52", "#e8b08a", "#1e1a2e", "spike"), ("#ff6b6b", "#23252e", "#8d5a3b", "#1a1210", "cap"),
    ("#e98fd0", "#4a6fa5", "#f0c09a", "#6b3a1f", "long"), ("#2a9d8f", "#23252e", "#c68a5e", "#1a1210", "flat"),
    ("#ffd23f", "#3a4a6a", "#f2c7a8", "#c98a3a", "bun"), ("#7a5af5", "#1b1d25", "#e8b896", "#5a3a24", "spike"),
    ("#ffffff", "#2c3a52", "#d9a27a", "#2a1b12", "chef"), ("#ff8a3d", "#23252e", "#e8b08a", "#1e1a2e", "flat")]
OMA = ("#9b6bd6", "#3a4a6a", "#f2c7a8", "#d9d4cf", "bun")


def person(i, bid, x, y, s=1.0, mood="n", back=False, p=None):
    sh, pa, sk, ha, st = p or PEOPLE[i % len(PEOPLE)]
    return block(bid, x, y, s, sh, pa, sk, ha, st, mood, back)


def me(bid, x, y, s=1.0, mood="happy", back=False):
    """Hauptfigur des Accounts als Block-Avatar (Senf-Hoodie)."""
    return block(bid, x, y, s, "#e0a83a", "#23252e", "#e8b08a", "#3a2418", "fringe", mood, back)


def fadein(sel, t, dur=0.35, dy=14):
    tw(f'tl.fromTo("{sel}",{{opacity:0,y:{dy}}},{{opacity:1,y:0,duration:{dur},ease:"sine.out"}},{t:.3f});')


def note(nid, x, y, s=1.0, col="#fff", op=0):
    return (f'<g id="{nid}" opacity="{op}"><g transform="translate({x},{y}) scale({s})">'
            f'<ellipse cx="0" cy="0" rx="24" ry="17" fill="{col}" transform="rotate(-20)"/><rect x="16" y="-92" width="9" height="92" fill="{col}"/>'
            f'<path d="M 25 -92 Q 58 -80 50 -40 Q 44 -64 25 -66 Z" fill="{col}"/></g></g>')


HOUSES = ((-20, 240, 300, "#f4d35e", "#ee6c4d"), (240, 260, 360, "#9bc1ff", "#3d5a80"), (520, 220, 280, "#ffd6e0", "#e56b6f"),
          (760, 340, 330, "#b8e0d2", "#2a9d8f"))


def town(prefix, mode="night", behind="", lit=True, stars=True):
    """Block-Stadt bei Tag/Dämmerung/Nacht. Fenster-IDs: {prefix}-w0 … -w15 (4 Häuser × 2 Reihen × 2)."""
    f = {"day": 1.0, "dusk": .72, "night": .42}[mode]
    if mode == "day":
        sky = (f'<rect width="1080" height="1920" fill="url(#daysky)"/><circle cx="880" cy="300" r="70" fill="#fff4c2"/>'
               + "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="#fff" opacity=".9"/>' for x, y, w, h in ((120, 330, 220, 60), (560, 260, 160, 50))))
    elif mode == "dusk":
        sky = (f'<rect width="1080" height="1920" fill="url(#dusksky)"/><circle cx="200" cy="760" r="120" fill="#ffb36b" opacity=".9"/>'
               f'<circle cx="200" cy="760" r="260" fill="url(#sunglow)"/>'
               + "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="#f6a5a0" opacity=".45"/>' for x, y, w, h in ((420, 330, 260, 46), (700, 470, 200, 40))))
    else:
        st = "".join(f'<circle cx="{RNG.randint(0,1080)}" cy="{RNG.randint(0,650)}" r="{RNG.choice([1.5,2,2.5,3])}" fill="#fff" opacity="{RNG.uniform(.25,.8):.2f}"/>' for _ in range(55)) if stars else ""
        sky = (f'<rect width="1080" height="1920" fill="url(#skyg)"/>{st}'
               f'<circle cx="200" cy="300" r="62" fill="{MOON}"/><circle cx="200" cy="300" r="150" fill="url(#moonglow)"/>')
    out = sky + behind
    n = 0
    for x, w, h, c, roof in HOUSES:
        top = 1000 - h
        cc = shade(c, f)
        out += (box(x, top, w, h, cc, shade(cc, .8), shade(cc, 1.08))
                + f'<polygon points="{x-20},{top} {x+w/2},{top-110} {x+w+20},{top}" fill="{shade(roof, f)}"/>'
                + f'<rect x="{x+w/2-45}" y="{1000-185}" width="90" height="185" fill="{shade("#6b4a32", f)}"/><circle cx="{x+w/2+28}" cy="{1000-90}" r="6" fill="{shade(GOLD, f)}"/>')
        for r in range(2):
            for j in range(2):
                wx = x + 20 + j * (w - 90); wy = top + 40 + r * 120
                if mode == "day":
                    fill = "#bfe4ff"
                else:
                    fill = WIN if lit else "#1a1c3a"
                out += f'<rect id="{prefix}-w{n}" x="{wx}" y="{wy}" width="50" height="60" fill="{fill}" stroke="{shade("#ffffff", f)}" stroke-width="5"/>'
                n += 1
    g = shade("#5cc65a", f); road = shade("#4a4d57", f); walk = shade("#d9d4c7", f)
    out += (f'<rect x="0" y="1000" width="1080" height="920" fill="{g}"/><rect x="0" y="1000" width="1080" height="70" fill="{walk}"/>'
            f'<rect x="0" y="1150" width="1080" height="220" fill="{road}"/>' + "".join(f'<rect x="{x}" y="1252" width="90" height="16" fill="{shade(GOLD, f)}"/>' for x in range(20, 1080, 180))
            + f'<rect x="0" y="1370" width="1080" height="40" fill="{walk}"/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{shade("#3f8f4a", f)}"/><rect x="{x-8}" y="{y}" width="16" height="70" fill="{shade("#6b4a32", f)}"/>' for x, y, r in ((60, 930, 50), (1030, 940, 46))))
    if mode == "night":
        for lx in (180, 900):
            out += (f'<polygon points="{lx-10},{690} {lx+10},{690} {lx+120},{1110} {lx-120},{1110}" fill="url(#lampcone)"/>'
                    f'<rect x="{lx-6}" y="690" width="12" height="380" fill="#2a2d55"/><ellipse cx="{lx}" cy="688" rx="22" ry="10" fill="{LAMP}"/>')
    return out


def sign(gid, cx, top, s=1.0, op=1, post=330):
    """Verbotsschild: NACH 22 UHR – NICHT PFEIFEN (durchgestrichene Note)."""
    w, h = 440, 300
    return (f'<g id="{gid}" opacity="{op}"><g transform="translate({cx},{top}) scale({s})">'
            f'<rect x="-14" y="{h-10}" width="28" height="{post}" fill="#5a5f6e"/>'
            f'<rect x="{-w/2}" y="0" width="{w}" height="{h}" rx="22" fill="#f4f1e6" stroke="#c62828" stroke-width="14"/>'
            f'<text x="0" y="62" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="44" fill="#0b0d22">NACH 22 UHR</text>'
            f'<circle cx="-110" cy="180" r="70" fill="#fff" stroke="#c62828" stroke-width="12"/>'
            f'<g transform="translate(-118,206) scale(.9)"><ellipse cx="0" cy="0" rx="24" ry="17" fill="#0b0d22" transform="rotate(-20)"/>'
            f'<rect x="16" y="-92" width="9" height="92" fill="#0b0d22"/><path d="M 25 -92 Q 58 -80 50 -40 Q 44 -64 25 -66 Z" fill="#0b0d22"/></g>'
            f'<line x1="-160" y1="130" x2="-60" y2="230" stroke="#c62828" stroke-width="12"/>'
            f'<text x="60" y="160" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="50" fill="#c62828">NICHT</text>'
            f'<text x="60" y="222" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="50" fill="#c62828">PFEIFEN!</text>'
            f'</g></g>')


def playground(gid, x, y):
    """Mini-Spielplatz (Schaukel) mit kleinem Schild."""
    return (f'<g id="{gid}"><rect x="{x}" y="{y-200}" width="14" height="200" fill="#c94f4f" transform="rotate(-8 {x} {y})"/>'
            f'<rect x="{x+180}" y="{y-200}" width="14" height="200" fill="#c94f4f" transform="rotate(8 {x+194} {y})"/>'
            f'<rect x="{x-10}" y="{y-210}" width="220" height="16" rx="6" fill="#c94f4f"/>'
            f'<line x1="{x+70}" y1="{y-196}" x2="{x+70}" y2="{y-70}" stroke="#333" stroke-width="4"/><line x1="{x+120}" y1="{y-196}" x2="{x+120}" y2="{y-70}" stroke="#333" stroke-width="4"/>'
            f'<rect x="{x+60}" y="{y-72}" width="70" height="14" rx="4" fill="{GOLD}"/></g>')


# ================= SZENEN =================
CROWD = ((250, 1066, .38), (370, 1068, .38), (720, 1068, .38), (840, 1066, .38))


def hook_scene(sid, t0, t1, loop=False):
    inner = town(sid, "dusk") + sign(f"{sid}-sg", 540, 760, .62, post=225)
    inner += "".join(person(i, f"{sid}-p{i}", x, y, s, "n") for i, (x, y, s) in enumerate(CROWD))
    inner += f'<g id="{sid}-shock" opacity="0">' + "".join(person(i, f"{sid}-q{i}", x, y, s, "shock") for i, (x, y, s) in enumerate(CROWD)) + '</g>'
    if not loop:
        inner += (f'<g id="{sid}-ins" opacity="0"><g transform="translate(-50,0)"><rect x="560" y="80" width="480" height="440" rx="30" fill="#5cc65a" stroke="#fff" stroke-width="10"/>'
                  f'<rect x="560" y="80" width="480" height="200" rx="30" fill="#f6a5a0"/>{playground(f"{sid}-pg", 640, 470)}'
                  f'<g transform="translate(940,250) scale(.38)">{sign(f"{sid}-sg2", 0, 0, 1.0)}</g>'
                  f'<rect x="600" y="100" width="260" height="56" rx="28" fill="#0b0d22"/><text x="730" y="140" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="34" fill="#fff">SPIELPLATZ</text></g></g>')
    scene(sid, t0, t1, inner, drift=False)
    return inner


# A Hook: Dämmerung, Verbotsschild, alle erschrecken bei „pfeifen“
hook_scene("sa", 0.0, t_um)
tw(f'tl.fromTo("#sa-cam",{{scale:1.45,svgOrigin:"540 980"}},{{scale:1.55,svgOrigin:"540 980",duration:{t_schild:.3f},ease:"sine.inOut"}},0);')
tw(f'tl.set("#sa-shock",{{opacity:1}},{t_pf0:.3f});')
shake("#sa-sg", t_pf0, 5, 6)
tw(f'tl.to("#sa-cam",{{scale:2.4,x:0,y:168,duration:.45,ease:"power2.inOut"}},{t_schild - 0.25:.3f});')
tw(f'tl.to("#sa-cam",{{scale:1,x:0,y:0,duration:.4,ease:"power2.inOut"}},{t_spiel - 0.2:.3f});')
pop("#sa-ins", t_spiel - 0.1, 0.35, 0.6)

# B 21:59 – alle machen die Fenster zu
S0, S1 = t_um, t_oma
wall = f'<rect width="1080" height="1920" fill="url(#dusksky)"/>' + box(40, 200, 1000, 1120, "#8a6f9e", "#6e5880", "#a58bb8")
wins = ""
WINS = [(90, 380, "BÄCKER", 6, t_baecker), (580, 380, "NACHBARIN", 2, t_nachb), (90, 820, "BÜRGERMEISTER", 3, t_buerg), (580, 820, "KINDER", None, t_mund)]
for k, (wx, wy, name, pi, tc) in enumerate(WINS):
    W_, H_ = 410, 330
    if pi is not None:
        who = person(pi, f"sb-p{k}", wx + W_/2 - 20, wy + H_ + 360, 1.35, "shock" if k == 2 else "n")
    else:
        who = (person(4, f"sb-p{k}a", wx + 120, wy + H_ + 250, 1.0, "shock", p=("#ff8a3d", "#2c3a52", "#f0c09a", "#c98a3a", "flat"))
               + person(0, f"sb-p{k}b", wx + 290, wy + H_ + 250, 1.0, "shock", p=("#5cc65a", "#2c3a52", "#8d5a3b", "#1a1210", "spike"))
               + "<g id=\"sb-hand\" opacity=\"0\">" + "".join(
                   f'<rect x="{hx-22}" y="{1118}" width="44" height="80" fill="{sh}"/>' + box(hx - 32, 1076, 64, 44, sk, shade(sk, .8), shade(sk, 1.1))
                   + f'<line x1="{hx-12}" y1="1080" x2="{hx-12}" y2="1112" stroke="{shade(sk, .75)}" stroke-width="3"/><line x1="{hx+8}" y1="1080" x2="{hx+8}" y2="1112" stroke="{shade(sk, .75)}" stroke-width="3"/>'
                   for hx, sk, sh in ((wx + 120, "#f0c09a", "#ff8a3d"), (wx + 290, "#8d5a3b", "#5cc65a"))) + "</g>")
    wins += (f'<clipPath id="sb-cl{k}"><rect x="{wx}" y="{wy}" width="{W_}" height="{H_}"/></clipPath>'
             f'<rect x="{wx-14}" y="{wy-14}" width="{W_+28}" height="{H_+28}" fill="#f4f1e6"/><rect x="{wx}" y="{wy}" width="{W_}" height="{H_}" fill="{WIN}"/>'
             f'<g clip-path="url(#sb-cl{k})">{who}</g>'
             f'<g id="sb-sl{k}"><rect x="{wx}" y="{wy}" width="{W_/2}" height="{H_}" fill="#2f5d4a" stroke="#1c3a2e" stroke-width="8"/>'
             + "".join(f'<rect x="{wx+12}" y="{wy+20+j*44}" width="{W_/2-24}" height="10" fill="#1c3a2e"/>' for j in range(7)) + '</g>'
             f'<g id="sb-sr{k}"><rect x="{wx+W_/2}" y="{wy}" width="{W_/2}" height="{H_}" fill="#2f5d4a" stroke="#1c3a2e" stroke-width="8"/>'
             + "".join(f'<rect x="{wx+W_/2+12}" y="{wy+20+j*44}" width="{W_/2-24}" height="10" fill="#1c3a2e"/>' for j in range(7)) + '</g>'
             + label(f"sb-n{k}", wx + W_/2, wy + H_ + 76, name, "#0b0d22", 34, fill="#ffffff"))
clock = (f'<g id="sb-clk"><rect x="330" y="60" width="420" height="150" rx="26" fill="#0b0d22" stroke="{RED}" stroke-width="6"/>'
         f'<text x="540" y="168" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="100" fill="{RED}">21:59</text></g>')
scene("sb", S0, S1, wall + wins + clock, drift=False)
tw(f'tl.fromTo("#sb-cam",{{scale:1.05,svgOrigin:"540 800"}},{{scale:1,svgOrigin:"540 800",duration:{S1-S0+0.3:.3f},ease:"sine.out"}},{S0:.3f});')
pop("#sb-clk", S0 + 0.1, 0.35, 0.7)
for k, (wx, wy, name, pi, tc) in enumerate(WINS):
    pop(f"#sb-n{k}", tc - 0.15, 0.3, 0.8)
    tw(f'tl.set("#sb-sl{k}",{{scaleX:0,transformOrigin:"0% 50%"}},0);')
    tw(f'tl.set("#sb-sr{k}",{{scaleX:0,transformOrigin:"100% 50%"}},0);')
    tc2 = tc + 0.35 if k < 3 else tc + 0.6
    tw(f'tl.to("#sb-sl{k}",{{scaleX:1,duration:.22,ease:"power3.in"}},{tc2:.3f});')
    tw(f'tl.to("#sb-sr{k}",{{scaleX:1,duration:.22,ease:"power3.in"}},{tc2:.3f});')
tw(f'tl.fromTo("#sb-hand",{{opacity:1,y:120}},{{opacity:1,y:0,duration:.3,ease:"back.out(1.6)"}},{t_kinder + 0.25:.3f});')

# C Oma Hilde flüstert: Pfeif nicht.
S0, S1 = t_oma, t_aber
bgC = f'<g opacity=".55">{town("sc", "dusk")}</g><rect width="1080" height="1920" fill="#1a0f2e" opacity=".35"/>'
oma = person(0, "sc-p", 400, 1900, 2.4, "n", p=OMA)
finger = f'<g id="sc-f" opacity="0"><rect x="385" y="1120" width="34" height="120" rx="16" fill="#f2c7a8" stroke="#c99c80" stroke-width="4"/><rect x="350" y="1225" width="110" height="80" rx="18" fill="#f2c7a8" stroke="#c99c80" stroke-width="4"/></g>'
bubble = (f'<g id="sc-bb" opacity="0"><path d="M 500 380 h 520 a 30 30 0 0 1 30 30 v 220 a 30 30 0 0 1 -30 30 h -360 l -90 70 l 10 -70 h -60 a 30 30 0 0 1 -30 -30 v -220 a 30 30 0 0 1 30 -30 z" fill="#fff"/>'
          f'<text x="775" y="470" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="40" fill="#444">psst … egal was passiert:</text>'
          f'<g id="sc-pn" opacity="0"><text x="775" y="590" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="66" fill="{RED}">PFEIF NICHT!</text></g></g>')
scene("sc", S0, S1, bgC + oma + bubble + label("sc-n", 290, 300, "OMA HILDE", "#0b0d22", 46, fill="#ffffff"), drift=False)
tw(f'tl.fromTo("#sc-cam",{{scale:1.1,svgOrigin:"400 1100"}},{{scale:1,svgOrigin:"400 1100",duration:{S1-S0+0.3:.3f},ease:"sine.out"}},{S0:.3f});')
pop("#sc-n", S0 + 0.1, 0.3, 0.8)
pop("#sc-bb", t_egal - 0.1, 0.35, 0.8)
pop("#sc-pn", t_pfeif1, 0.25, 0.6)
shake("#sc-pn", t_pfeif1 + 0.25, 4, 5)

# D Aber du bist neu hier – und findest das lächerlich
S0, S1 = t_aber, t_also
boxes = (box(400, 1000, 90, 66, "#c89a5e", "#a57a44", "#d8b07a") + f'<text x="445" y="1042" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="17" fill="#5a3a1a">UMZUG</text>'
         + box(412, 944, 66, 56, "#c89a5e", "#a57a44", "#d8b07a"))
scene("sd", S0, S1, town("sd", "dusk") + boxes + me("sd-me", 580, 1066, .38, "happy")
      + pill("sd-neu", 560, 700, "NEU HIER", CYAN, "#0b0d22", 40), drift=False)
tw(f'tl.fromTo("#sd-cam",{{scale:1.75,svgOrigin:"520 960"}},{{scale:1.9,svgOrigin:"520 960",duration:{S1-S0+0.3:.3f},ease:"sine.inOut"}},{S0:.3f});')
pop("#sd-neu", t_neu - 0.1, 0.35, 0.7)
tw(f'tl.to("#sd-me-b",{{rotation:4,y:-14,svgOrigin:"0 0",duration:.12,yoyo:true,repeat:7,ease:"sine.inOut"}},{t_laech:.3f});')

# E Nachts raus – Turmuhr springt auf 22:00
S0, S1 = t_also, t_und_pf
tower = (box(800, 120, 200, 900, "#3a3550", "#2a2640", "#4a4566") + f'<polygon points="780,120 900,-20 1020,120" fill="#2a2640"/>'
         f'<circle cx="900" cy="300" r="88" fill="#f4e3a1" stroke="#1a1730" stroke-width="10"/>'
         + "".join(f'<rect x="896" y="218" width="8" height="18" fill="#1a1730" transform="rotate({k*30} 900 300)"/>' for k in range(12))
         + f'<g id="se-hh"><rect x="895" y="252" width="10" height="52" rx="5" fill="#1a1730"/></g>'
         f'<g id="se-mh"><rect x="897" y="228" width="7" height="76" rx="3" fill="#1a1730"/></g><circle cx="900" cy="300" r="9" fill="#1a1730"/>')
dig = f'<g id="se-22" opacity="0"><rect x="700" y="420" width="260" height="100" rx="18" fill="#0b0d22" stroke="{RED}" stroke-width="5"/><text x="830" y="495" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="70" fill="{RED}">22:00</text></g>'
scene("se", S0, S1, town("se", "night", tower) + me("se-me", -60, 1066, .38, "n") + dig
      + f'<rect id="se-fl" width="1080" height="1920" fill="#fff" opacity="0"/>', drift=False)
tw(f'tl.set("#se-hh",{{rotation:-60.5,svgOrigin:"900 300"}},0);')
tw(f'tl.set("#se-mh",{{rotation:-6,svgOrigin:"900 300"}},0);')
move("#se-me", S0, t_turm - S0, "sine.out", x=440)
tw(f'tl.fromTo("#se-me-b",{{y:0}},{{y:-10,duration:.2,yoyo:true,repeat:{int((t_turm-S0)/0.2)},ease:"sine.inOut"}},{S0:.3f});')
tw(f'tl.fromTo("#se-cam",{{scale:1.35,svgOrigin:"400 940"}},{{scale:1.45,svgOrigin:"400 940",duration:{t_turm-S0:.3f},ease:"sine.inOut"}},{S0:.3f});')
tw(f'tl.to("#se-cam",{{scale:1.6,x:-300,y:366,duration:.6,ease:"power2.inOut"}},{t_turm - 0.1:.3f});')
tw(f'tl.to("#se-mh",{{rotation:0,svgOrigin:"900 300",duration:.12,ease:"back.out(3)"}},{t_22:.3f});')
tw(f'tl.to("#se-hh",{{rotation:-60,svgOrigin:"900 300",duration:.12,ease:"back.out(3)"}},{t_22:.3f});')
tw(f'tl.set("#se-fl",{{opacity:.5}},{t_22:.3f});')
tw(f'tl.to("#se-fl",{{opacity:0,duration:.35}},{t_22+0.01:.3f});')
pop("#se-22", t_22 + 0.05, 0.3, 0.6)
shake("#se", t_22, 6, 7)

# F Du pfeifst – Stille. Kein Wind. Kein Hund. Gar nichts.
S0, S1 = t_und_pf, t_dann1
face_me = me("sf-me", 540, 1787, 3.0, "n")
whistle = f'<rect x="470" y="852" width="140" height="66" fill="#e8b08a"/><ellipse cx="540" cy="885" rx="17" ry="21" fill="#111"/>'
notes = "".join(note(f"sf-n{k}", 600, 880, 1.2, "#fff") for k in range(5))
icons = (f'<g id="sf-i0" opacity="0"><g transform="translate(220,330)"><path d="M -70 -30 h 100 a 25 25 0 1 0 -25 -25 M -70 0 h 130 M -70 30 h 90 a 22 22 0 1 1 -22 22" stroke="#cfd3ff" stroke-width="10" fill="none" stroke-linecap="round"/>'
         f'<line x1="-90" y1="-90" x2="90" y2="90" stroke="{RED}" stroke-width="14"/></g></g>'
         f'<g id="sf-i1" opacity="0"><g transform="translate(540,330)"><rect x="-60" y="-20" width="110" height="60" rx="14" fill="#cfd3ff"/><rect x="30" y="-70" width="60" height="60" rx="10" fill="#cfd3ff"/>'
         f'<rect x="34" y="-90" width="16" height="28" rx="4" fill="#cfd3ff"/><rect x="-55" y="38" width="16" height="40" fill="#cfd3ff"/><rect x="25" y="38" width="16" height="40" fill="#cfd3ff"/>'
         f'<line x1="-90" y1="-90" x2="110" y2="90" stroke="{RED}" stroke-width="14"/></g></g>'
         f'<g id="sf-i2" opacity="0"><text x="860" y="370" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="110" fill="#cfd3ff">…</text></g>')
scene("sf", S0, S1, f'<rect width="1080" height="1920" fill="url(#skyg)"/>'
      + f'<g opacity=".5" transform="translate(0,300)">{town("sfb", "night")}</g>'
      + face_me + whistle + notes + icons + f'<rect id="sf-dk" width="1080" height="1920" fill="#000" opacity="0"/>', drift=False)
tw(f'tl.fromTo("#sf-cam",{{scale:1.15,svgOrigin:"540 880"}},{{scale:1,svgOrigin:"540 880",duration:{t_stille-S0:.3f},ease:"sine.out"}},{S0:.3f});')
for k in range(5):
    tt = t_pfeifst + k * 0.28
    tw(f'tl.fromTo("#sf-n{k}",{{opacity:0,x:0,y:0,scale:.6}},{{opacity:1,x:{180+k*40},y:{-240-k*60 + (60 if k%2 else 0)},scale:1,duration:1.1,ease:"sine.out"}},{tt:.3f});')
    tw(f'tl.to("#sf-n{k}",{{opacity:0,duration:.25}},{t_stille - 0.1:.3f});')
tw(f'tl.to("#sf-dk",{{opacity:.45,duration:.4}},{t_stille:.3f});')
tw(f'tl.to("#sf-cam",{{scale:1.18,svgOrigin:"540 820",duration:{S1-t_stille+0.3:.3f},ease:"none"}},{t_stille:.3f});')
for k, tt in enumerate((t_wind, t_hund, t_gar)):
    pop(f"#sf-i{k}", tt - 0.05, 0.3, 0.7)

# ---------- Das Wesen: Schattengestalt mit glühenden Schlitzaugen (eigenes Design) ----------
def m_eyes(eid, cx, cy, s=1.0, op=0):
    """Asymmetrische, schräg stehende Glutaugen mit Schlitzpupillen."""
    L = '<path d="M -82 8 Q -50 -26 -14 -8 Q -46 18 -82 8 Z" fill="url(#meye)" stroke="#2a0600" stroke-width="3"/><ellipse class="pup" cx="-46" cy="-1" rx="3" ry="13" fill="#000"/>'
    R = '<g transform="translate(0,-8) scale(.86)"><path d="M 82 8 Q 50 -26 14 -8 Q 46 18 82 8 Z" fill="url(#meye)" stroke="#2a0600" stroke-width="3"/><ellipse class="pup" cx="46" cy="-1" rx="3" ry="13" fill="#000"/></g>'
    return (f'<g id="{eid}" opacity="{op}"><g transform="translate({cx},{cy}) scale({s})"><circle r="150" fill="url(#mglow)"/>'
            f'<g id="{eid}-lid">{L}{R}</g></g></g>')


def shadow_fig(fid, x, y, s=1.0, op=0):
    """Sehr große, dünne Schattengestalt: Kopf zu lang, Arme bis unter die Knie, lange Finger."""
    C = "#03050a"; RIM = "#2c3160"
    fingers = ""
    for sx in (-1, 1):
        hx, hy = sx * 104, -110
        for k, (dx, dy) in enumerate(((-26, 110), (-10, 128), (6, 122), (20, 100))):
            fingers += f'<path d="M {hx} {hy} Q {hx + sx*dx*0.4:.0f} {hy + dy*0.5:.0f} {hx + sx*dx} {hy + dy}" stroke="{C}" stroke-width="7" fill="none" stroke-linecap="round"/>'
    arms = "".join(f'<path d="M {sx*58} -640 Q {sx*120} -420 {sx*104} -110" stroke="{C}" stroke-width="20" fill="none" stroke-linecap="round"/>' for sx in (-1, 1))
    return (f'<g id="{fid}" opacity="{op}"><g transform="translate({x},{y}) scale({s})">'
            f'<g stroke="{RIM}" stroke-width="5" opacity=".9">'
            f'<path d="M -42 -630 Q -72 -400 -48 -170 L -34 0 L -12 0 L 0 -220 L 12 0 L 34 0 L 48 -170 Q 72 -400 42 -630 Z" fill="{C}"/></g>'
            f'<path d="M -66 -642 Q 0 -690 66 -642 L 44 -598 L -44 -598 Z" fill="{C}"/>{arms}{fingers}'
            f'<rect x="-10" y="-735" width="20" height="100" fill="{C}"/>'
            f'<g id="{fid}-head"><ellipse cx="0" cy="-800" rx="50" ry="84" fill="{C}" stroke="{RIM}" stroke-width="4"/>{m_eyes(f"{fid}-e", 0, -812, .5, 1)}</g>'
            f'</g></g>')


def qpt(p0, c, p1, t):
    return tuple((1-t)**2*a + 2*(1-t)*t*b + t*t*d for a, b, d in zip(p0, c, p1))


def teeth_mouth(gid, op=0):
    """Breiter Mund mit zwei Reihen spitzer Zähne (für das Schlüsselloch)."""
    A, B = (300, 860), (780, 860)
    up, lo = (540, 930), (540, 1060)
    out = f'<g id="{gid}" opacity="{op}"><path d="M 300 860 Q 540 930 780 860 Q 540 1060 300 860 Z" fill="#0a0000"/>'
    n = 16
    for i in range(n):
        t0, t1 = i/n, (i+1)/n
        a, b = qpt(A, up, B, t0), qpt(A, up, B, t1); m = qpt(A, up, B, (t0+t1)/2)
        h = 30 * (1 - abs((t0+t1)/2 - .5) * 1.2)
        out += f'<polygon points="{a[0]:.0f},{a[1]:.0f} {b[0]:.0f},{b[1]:.0f} {m[0]:.0f},{m[1]+h:.0f}" fill="#ece6cf"/>'
        a, b = qpt(A, lo, B, t0), qpt(A, lo, B, t1); m = qpt(A, lo, B, (t0+t1)/2)
        out += f'<polygon points="{a[0]:.0f},{a[1]:.0f} {b[0]:.0f},{b[1]:.0f} {m[0]:.0f},{m[1]-h*.8:.0f}" fill="#d9d2b8"/>'
    return out + '</g>'


# G Jemand pfeift zurück – aus dem Wald
S0, S1 = t_dann1, t_ueber
trees = ""
for row, (col, y0, sc) in enumerate((("#0a1610", 900, 1.0), ("#0f2018", 1000, 1.25), ("#142a1f", 1120, 1.5))):
    for x in range(-60, 1200, int(130 * sc)):
        if row == 2 and 380 < x < 700:
            continue
        hh = 420 * sc + RNG.randint(-40, 40)
        trees += f'<polygon points="{x},{y0-hh} {x-90*sc},{y0} {x+90*sc},{y0}" fill="{col}"/><rect x="{x-10*sc}" y="{y0}" width="{20*sc}" height="{60*sc}" fill="{col}"/>'
fog = "".join(f'<ellipse cx="{x}" cy="{y}" rx="320" ry="60" fill="#8f94c4" opacity=".18" filter="url(#fogblur)"/>' for x, y in ((200, 1080), (800, 1150), (500, 1220)))
eyes = ""
fig_g = shadow_fig("sg-f", 560, 1150, .62)
notes2 = "".join(note(f"sg-n{k}", 540, 940, .7, "#cfd3ff") for k in range(5))
ground = f'<rect x="0" y="1180" width="1080" height="740" fill="#0d1a14"/>'
scene("sg", S0, S1, f'<rect width="1080" height="1920" fill="url(#skyg)"/><circle cx="820" cy="300" r="60" fill="{MOON}"/><circle cx="820" cy="300" r="150" fill="url(#moonglow)"/>'
      + trees + fig_g + ground + fog + notes2 + me("sg-me", 540, 1880, 1.6, "n", back=True), drift=False)
tw(f'tl.fromTo("#sg-cam",{{scale:1,svgOrigin:"540 930"}},{{scale:1.3,svgOrigin:"540 930",duration:{S1-S0+0.3:.3f},ease:"sine.inOut"}},{S0:.3f});')
for k in range(5):
    tt = t_pfeift2 + k * 0.3
    tw(f'tl.fromTo("#sg-n{k}",{{opacity:0,x:0,y:0,scale:.5,transformOrigin:"50% 50%"}},{{opacity:.9,x:{(-260, 200, -120, 280, -20)[k]},y:{(-200, -260, 180, 120, -340)[k]},scale:1.6,duration:1.6,ease:"sine.out"}},{tt:.3f});')
    tw(f'tl.to("#sg-n{k}",{{opacity:0,duration:.4}},{tt + 1.6:.3f});')
tw(f'tl.to("#sg-f",{{opacity:.35,duration:1.2,ease:"sine.in"}},{t_pfeift2:.3f});')
tw(f'tl.set("#sg-f-e",{{opacity:0}},0);')
tw(f'tl.to("#sg-f",{{opacity:1,duration:.4}},{t_wald - 0.1:.3f});')
tw(f'tl.to("#sg-f-e",{{opacity:1,duration:.12}},{t_wald:.3f});')
tw(f'tl.to("#sg-f-head",{{rotation:16,transformOrigin:"50% 100%",duration:.7,ease:"power2.inOut"}},{t_wald + 0.25:.3f});')
tw(f'tl.to("#sg-f-e-lid",{{scaleY:.08,transformOrigin:"50% 50%",duration:.06,yoyo:true,repeat:1}},{t_wald + 0.15:.3f});')
tw(f'tl.to("#sg-me-b",{{y:-12,duration:.1,yoyo:true,repeat:1}},{t_pfeift2:.3f});')

# H Überall gehen die Lichter aus – nur deins nicht
S0, S1 = t_ueber, t_du_r
MYW = 6
scene("sh", S0, S1, town("sh", "night") + f'<g id="sh-ring" opacity="0"><circle cx="265" cy="790" r="80" fill="none" stroke="{CYAN}" stroke-width="10" stroke-dasharray="18 12"/>'
      + f'<rect x="215" y="660" width="100" height="56" rx="28" fill="{CYAN}"/><text x="265" y="702" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="40" fill="#0b0d22">DU</text></g>', drift=False)
order = [k for k in range(16) if k != MYW]
RNG.shuffle(order)
for i, k in enumerate(order):
    tw(f'tl.set("#sh-w{k}",{{fill:"#1a1c3a"}},{t_ueber + 0.2 + i * 0.07:.3f});')
tw(f'tl.fromTo("#sh-cam",{{scale:1,svgOrigin:"540 800"}},{{scale:1.15,svgOrigin:"265 790",duration:{S1-S0+0.3:.3f},ease:"sine.inOut"}},{S0:.3f});')
pop("#sh-ring", t_nur, 0.3, 0.6)

# I1 Du rennst nach Hause
S0, S1 = t_du_r, t_schliesst
strip = ""
for k in range(3):
    strip += f'<g transform="translate({k*1080},0)">{town(f"si{k}", "night", stars=False)}</g>'
scene("si", S0, S1, f'<rect width="1080" height="1920" fill="url(#skyg)"/><g id="si-bg">{strip}</g>'
      + "".join(f'<rect id="si-l{k}" x="{560 + k*30}" y="{900 + k*40}" width="160" height="6" rx="3" fill="#cfd3ff" opacity=".6"/>' for k in range(4))
      + f'<g transform="rotate(8 420 1066)">{me("si-me", 420, 1066, .42, "shock")}</g>', drift=False)
tw(f'tl.set("#si-cam",{{scale:1.6,svgOrigin:"420 960"}},{S0:.3f});')
move("#si-bg", S0, S1 - S0 + 0.3, "none", x=-900)
tw(f'tl.fromTo("#si-me-b",{{y:0}},{{y:-22,duration:.12,yoyo:true,repeat:{int((S1-S0+0.3)/0.12)},ease:"sine.inOut"}},{S0:.3f});')
for k in range(4):
    tw(f'tl.fromTo("#si-l{k}",{{x:0}},{{x:-500,duration:.3,repeat:{int((S1-S0)/0.3)+1},ease:"none"}},{S0 + k*0.07:.3f});')

# I2 Tür abschließen – Herz rast – es klopft dreimal
S0, S1 = t_schliesst, t_und_d
room = (f'<rect width="1080" height="1920" fill="#2a2038"/>' + "".join(f'<rect x="{x}" y="0" width="40" height="1300" fill="#30243f"/>' for x in range(0, 1080, 90))
        + f'<rect x="0" y="1300" width="1080" height="620" fill="#3a2a22"/>' + "".join(f'<rect x="0" y="{y}" width="1080" height="4" fill="#2a1d17"/>' for y in range(1360, 1920, 80)))
door = (f'<g id="sj-door"><rect x="300" y="420" width="480" height="880" fill="#6b4a32" stroke="#4a3020" stroke-width="12"/>'
        f'<rect x="350" y="480" width="170" height="340" fill="#5e4029"/><rect x="560" y="480" width="170" height="340" fill="#5e4029"/>'
        f'<rect x="350" y="880" width="170" height="340" fill="#5e4029"/><rect x="560" y="880" width="170" height="340" fill="#5e4029"/>'
        f'<circle cx="730" cy="870" r="16" fill="{GOLD}"/><rect x="700" y="790" width="50" height="40" rx="6" fill="#9a9a9a"/>'
        f'<g id="sj-bolt"><rect x="640" y="800" width="70" height="20" rx="6" fill="#d0d0d0"/></g></g>'
        f'<rect x="780" y="785" width="40" height="50" fill="#9a9a9a"/>')
heart = f'<g id="sj-ht" opacity="0"><path d="M 540 330 C 540 260 440 250 440 320 C 440 380 520 410 540 450 C 560 410 640 380 640 320 C 640 250 540 260 540 330 Z" fill="{RED}"/></g>'
knocks = "".join(f'<g id="sj-k{k}" opacity="0"><text x="{(250, 830, 540)[k]}" y="{(560, 700, 400)[k]}" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="88" fill="#fff" stroke="#0b0b0b" stroke-width="10" paint-order="stroke" transform="rotate({(-12, 10, -4)[k]} {(250, 830, 540)[k]} {(560, 700, 400)[k]})">KLOPF</text></g>' for k in range(3))
x3 = f'<g id="sj-x3" opacity="0"><text x="540" y="1200" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="150" fill="{RED}" stroke="#0b0b0b" stroke-width="12" paint-order="stroke">3×</text></g>'
scene("sj", S0, S1, room + door + heart + me("sj-me", 170, 1900, 1.5, "shock", back=True) + knocks + x3 + f'<rect id="sj-dk" width="1080" height="1920" fill="#000" opacity="0"/>', drift=False)
tw(f'tl.fromTo("#sj-cam",{{scale:1,svgOrigin:"540 860"}},{{scale:1.12,svgOrigin:"540 860",duration:{S1-S0+0.3:.3f},ease:"sine.inOut"}},{S0:.3f});')
move("#sj-bolt", t_ab - 0.05, 0.15, "power3.in", x=90)
pop("#sj-ht", t_herz - 0.05, 0.25, 0.6)
tw(f'tl.to("#sj-ht",{{scale:1.18,transformOrigin:"50% 50%",duration:.14,yoyo:true,repeat:9,ease:"sine.inOut"}},{t_herz + 0.2:.3f});')
tw(f'tl.to("#sj-ht",{{opacity:0,duration:.2}},{t_dann2:.3f});')
tw(f'tl.to("#sj-dk",{{opacity:.35,duration:.3}},{t_dann2:.3f});')
for k in range(3):
    tk = t_klopft + k * 0.36
    shake("#sj-door", tk, 3, 9)
    pop(f"#sj-k{k}", tk, 0.12, 0.6)
pop("#sj-x3", t_dreimal, 0.25, 0.5)

# K Direkt vor der Tür pfeift es – Noten kriechen unter der Tür durch
S0, S1 = t_und_d, t_durch
gapY = 1110
doorK = (f'<rect width="1080" height="{gapY}" fill="#6b4a32"/><rect x="60" y="120" width="420" height="900" fill="#5e4029"/><rect x="600" y="120" width="420" height="900" fill="#5e4029"/>'
         f'<rect x="0" y="{gapY}" width="1080" height="30" fill="#8fa0ff" opacity=".55"/><rect x="0" y="{gapY+30}" width="1080" height="800" fill="#3a2a22"/>'
         f'<polygon points="0,{gapY+30} 1080,{gapY+30} 1180,{gapY+400} -100,{gapY+400}" fill="#8fa0ff" opacity=".12"/>'
         + "".join(f'<rect x="0" y="{y}" width="1080" height="4" fill="#2a1d17"/>' for y in range(gapY + 110, 1920, 90)))
feet = f'<g id="sk-ft" opacity="0"><rect x="400" y="{gapY}" width="60" height="30" fill="#000"/><rect x="620" y="{gapY}" width="60" height="30" fill="#000"/></g>'
claws = '<g id="sk-cl" opacity="0">' + "".join(
    f'<path d="M {x0 + k*30} {gapY+28} Q {x0 + k*30 + (k-1.5)*14} {gapY+140} {x0 + k*30 + (k-1.5)*34} {gapY+250}" stroke="#000" stroke-width="13" fill="none" stroke-linecap="round" opacity=".85"/>'
    for x0 in (380, 600) for k in range(4)) + '</g>'
feet += claws
notes3 = "".join(note(f"sk-n{k}", 300 + k * 120, gapY + 20, .8, "#cfd3ff") for k in range(5))
scene("sk", S0, S1, doorK + feet + notes3, drift=False)
tw(f'tl.fromTo("#sk-cam",{{scale:1,svgOrigin:"540 {gapY}"}},{{scale:1.25,svgOrigin:"540 {gapY}",duration:{S1-S0+0.3:.3f},ease:"sine.inOut"}},{S0:.3f});')
tw(f'tl.to("#sk-ft",{{opacity:1,duration:.4}},{t_tuer - 0.1:.3f});')
for k in range(5):
    tt = t_pfeift3 + k * 0.35
    tw(f'tl.fromTo("#sk-n{k}",{{opacity:0,y:-10,x:0}},{{opacity:.9,y:{200 + (k%2)*80},x:{(k-2)*60},duration:1.4,ease:"sine.out"}},{tt:.3f});')
tw(f'tl.set("#sk-cl",{{opacity:1}},{t_leise - 0.2:.3f});')
tw(f'tl.fromTo("#sk-cl",{{scaleY:0,transformOrigin:"50% 0%"}},{{scaleY:1,duration:1.6,ease:"sine.inOut"}},{t_leise - 0.2:.3f});')
tw(f'tl.to("#sk-cl",{{scaleY:.15,duration:.25,ease:"power3.in"}},{t_durch - 0.3:.3f});')

# L Durchs Schlüsselloch: zwei gelbe Augen – ein Lächeln, viel zu breit
S0, S1 = t_durch, t_am
kh = "M 540 560 m -150 0 a 150 150 0 1 0 300 0 a 150 150 0 1 0 -300 0 Z M 470 660 L 610 660 L 680 1150 L 400 1150 Z"
grin = teeth_mouth("sl-gr")
eyesL = m_eyes("sl-ey", 540, 575, 1.55)
scene("sl", S0, S1, f'<rect width="1080" height="1920" fill="#3a2618"/>'
      + "".join(f'<rect x="0" y="{y}" width="1080" height="6" fill="#2e1d12"/>' for y in range(0, 1920, 70))
      + f'<clipPath id="sl-kh"><path d="{kh}"/></clipPath>'
      + f'<path d="{kh}" fill="#04050d" stroke="#1a0f08" stroke-width="18"/>'
      + f'<g clip-path="url(#sl-kh)"><rect width="1080" height="1920" fill="#070a1e"/><g id="sl-hd"><ellipse cx="540" cy="760" rx="330" ry="470" fill="#0d1024"/>{eyesL}{grin}</g></g>', drift=False)
tw(f'tl.fromTo("#sl-cam",{{scale:1,svgOrigin:"540 760"}},{{scale:1.45,svgOrigin:"540 760",duration:{S1-S0+0.3:.3f},ease:"sine.in"}},{S0:.3f});')
tw(f'tl.to("#sl-ey",{{opacity:1,duration:.35}},{t_gelbe - 0.1:.3f});')
tw(f'tl.to("#sl-ey-lid",{{scaleY:.08,transformOrigin:"50% 50%",duration:.07,yoyo:true,repeat:1}},{t_gelbe + 0.7:.3f});')
tw(f'tl.fromTo("#sl-hd",{{rotation:0}},{{rotation:-14,svgOrigin:"540 760",duration:{t_am - t_gelbe:.3f},ease:"sine.inOut"}},{t_gelbe:.3f});')
tw(f'tl.to("#sl-ey .pup",{{scaleX:.35,transformOrigin:"50% 50%",duration:.2}},{t_breit:.3f});')
tw(f'tl.fromTo("#sl-gr",{{opacity:0,scaleX:.3,transformOrigin:"50% 50%"}},{{opacity:1,scaleX:1,duration:.45,ease:"power2.out"}},{t_laecheln:.3f});')
tw(f'tl.to("#sl-gr",{{scaleX:1.7,scaleY:1.15,transformOrigin:"50% 50%",duration:.5,ease:"power2.in"}},{t_breit - 0.1:.3f});')
shake("#sl-cam", t_breit + 0.3, 7, 9)
DANGER.append(("dg1", t_gelbe, t_am))

# M Am nächsten Morgen: alles normal – neues Schild am Rathaus
S0, S1 = t_am, t_darauf
rh = (box(200, 430, 680, 570, "#efe4cc", "#d4c6a8", "#fbf3e0") + f'<polygon points="170,430 540,250 910,430" fill="#b85c4a"/>'
      + "".join(f'<rect x="{x}" y="560" width="40" height="440" fill="#ffffff" stroke="#d4c6a8" stroke-width="4"/>' for x in (250, 360, 680, 790))
      + f'<rect x="470" y="780" width="140" height="220" fill="#6b4a32"/>'
      f'<text x="540" y="520" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="56" fill="#6b4a32">RATHAUS</text>'
      f'<circle cx="540" cy="350" r="50" fill="#fff" stroke="#6b4a32" stroke-width="6"/><path d="M 540 350 L 540 315 M 540 350 L 565 360" stroke="#6b4a32" stroke-width="6"/>'
      f'<g id="sm-bd"><rect x="300" y="760" width="150" height="190" fill="#a8743f" stroke="#6b4a32" stroke-width="6"/>'
      f'<rect x="318" y="780" width="114" height="150" fill="#fff"/><rect x="330" y="800" width="90" height="12" fill="{CYAN}"/>'
      f'<rect x="330" y="880" width="90" height="26" fill="{RED}" transform="rotate(-8 375 893)"/></g>')
birds = "".join(f'<g id="sm-b{k}"><path d="M {x} {y} q 18 -16 36 0 q 18 -16 36 0" stroke="#2a2a3a" stroke-width="5" fill="none"/></g>' for k, (x, y) in enumerate(((140, 240), (240, 200), (700, 170))))
scene("sm", S0, S1, f'<rect width="1080" height="1920" fill="url(#daysky)"/><circle cx="900" cy="260" r="70" fill="#fff4c2"/>' + birds
      + f'<rect x="0" y="1000" width="1080" height="920" fill="#5cc65a"/><rect x="0" y="1000" width="1080" height="70" fill="#d9d4c7"/>' + rh
      + "".join(person(i, f"sm-p{i}", x, 1066, .38, "happy") for i, x in ((0, 130), (2, 950), (5, 700))), drift=False)
for k in range(3):
    move(f"#sm-b{k}", S0, S1 - S0 + 0.3, "none", x=160)
tw(f'tl.fromTo("#sm-cam",{{scale:1,svgOrigin:"375 855"}},{{scale:1.08,svgOrigin:"375 855",duration:{t_schild2-S0:.3f},ease:"sine.inOut"}},{S0:.3f});')
tw(f'tl.to("#sm-cam",{{scale:2.6,svgOrigin:"375 855",duration:.6,ease:"power2.inOut"}},{t_schild2 - 0.2:.3f});')

# N Das Schild: DEIN NAME – HAT GEPFIFFEN.
S0, S1 = t_darauf, t_oma2
old = ""
for k, (x, y, r, nm) in enumerate(((60, 160, -9, "TOM"), (700, 130, 7, "LENA"), (40, 1060, 6, "MAX"), (760, 1030, -6, "OLE"))):
    old += (f'<g transform="rotate({r} {x+150} {y+170})" opacity=".55"><rect x="{x}" y="{y}" width="300" height="340" fill="#e9e1cc"/>'
            f'<circle cx="{x+150}" cy="{y+18}" r="12" fill="{RED}"/><text x="{x+150}" y="{y+130}" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="52" fill="#555">{nm}</text>'
            f'<text x="{x+150}" y="{y+230}" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="30" fill="#a33">HAT GEPFIFFEN</text></g>')
paper = (f'<g id="sn-pp"><rect x="200" y="380" width="680" height="700" fill="#ffffff" stroke="#ddd" stroke-width="4"/><circle cx="540" cy="410" r="18" fill="{RED}"/>'
         f'<text x="540" y="520" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="40" fill="#777">NEUER BEWOHNER:</text>'
         f'<g id="sn-nm"><text x="540" y="660" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="96" fill="{CYAN}" stroke="#0b0d22" stroke-width="6" paint-order="stroke">DEIN NAME</text></g>'
         f'<g id="sn-st" opacity="0"><g transform="rotate(-9 540 880)"><rect x="250" y="800" width="580" height="160" rx="16" fill="none" stroke="{RED}" stroke-width="12"/>'
         f'<text x="540" y="910" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="72" fill="{RED}">HAT GEPFIFFEN.</text></g></g></g>')
scene("sn", S0, S1, f'<rect width="1080" height="1920" fill="#a8743f"/>' + "".join(f'<circle cx="{RNG.randint(0,1080)}" cy="{RNG.randint(0,1920)}" r="{RNG.randint(3,8)}" fill="#8c5e30" opacity=".6"/>' for _ in range(120))
      + old + paper, drift=False)
tw(f'tl.fromTo("#sn-cam",{{scale:1.15,svgOrigin:"540 700"}},{{scale:1,svgOrigin:"540 700",duration:{S1-S0+0.3:.3f},ease:"sine.out"}},{S0:.3f});')
tw(f'tl.fromTo("#sn-nm",{{scale:.7,opacity:0,transformOrigin:"50% 50%"}},{{scale:1,opacity:1,duration:.35,ease:"back.out(2)"}},{t_name - 0.25:.3f});')
tw(f'tl.fromTo("#sn-st",{{scale:2.2,opacity:0,transformOrigin:"50% 50%"}},{{scale:1,opacity:1,duration:.18,ease:"power4.in"}},{t_gepf - 0.1:.3f});')
shake("#sn-cam", t_gepf + 0.1, 6, 10)

# O Oma Hilde schaut zum Wald: Ich hab's dir gesagt.
S0, S1 = t_oma2, t_denn
forest = "".join(f'<polygon points="{x},{1000-h} {x-80},1000 {x+80},1000" fill="#1d3324"/>' for x, h in ((640, 420), (760, 520), (880, 460), (1000, 540), (1100, 480)))
eyesO = shadow_fig("so-ey", 860, 1010, .42)
scene("so", S0, S1, f'<rect width="1080" height="1920" fill="url(#daysky)"/><circle cx="160" cy="260" r="70" fill="#fff4c2"/>'
      + f'<rect x="0" y="1000" width="1080" height="920" fill="#5cc65a"/>' + forest + eyesO
      + f'<rect x="560" y="990" width="520" height="40" fill="#3f6b3f" opacity=".6"/>'
      + person(0, "so-p", 330, 1900, 2.2, "n", p=OMA), drift=False)
tw(f'tl.fromTo("#so-cam",{{scale:1,svgOrigin:"700 900"}},{{scale:1.12,svgOrigin:"760 900",duration:{S1-S0+0.3:.3f},ease:"sine.inOut"}},{S0:.3f});')
tw(f'tl.to("#so-ey",{{opacity:.85,duration:.4}},{t_wald2:.3f});')
tw(f'tl.to("#so-ey",{{opacity:0,duration:.1}},{t_wald2 + 1.2:.3f});')
tw(f'tl.to("#so-p-b",{{rotation:3,svgOrigin:"0 -300",duration:.18,yoyo:true,repeat:3,ease:"sine.inOut"}},{t_gesagt - 0.3:.3f});')

# P Loop: zurück an den Anfang – „Denn in dieser Stadt …“
hook_scene("sp", t_denn, TOTAL, loop=True)
tw(f'tl.fromTo("#sp-cam",{{scale:1.7,svgOrigin:"540 980"}},{{scale:1.45,svgOrigin:"540 980",duration:{TOTAL-t_denn:.3f},ease:"sine.out"}},{t_denn:.3f});')

# ================= UNTERTITEL (Format C: ein Wort, groß, Gelbgrün) =================
KEY = {"DU", "DIR", "DEIN", "DEINE", "DEINER", "DEINS"}
DISPLAY = {"zweiundzwanzig": "22", "einundzwanzig": "21:59"}
words = [dict(w) for w in W]
chunks = []
skip_next = 0
for k, w in enumerate(words):
    if skip_next:
        skip_next -= 1
        continue
    chunks.append(w)
    if w["t"] == "einundzwanzig":
        skip_next = 2          # „Uhr neunundfünfzig“ steckt in „21:59“
subs = []
for k, w in enumerate(chunks):
    s = w["s"]
    e = chunks[k+1]["s"] if k + 1 < len(chunks) else min(TOTAL, w["e"] + 0.4)
    t = DISPLAY.get(re.sub(r"[^\wäöüß]", "", w["t"]), w["t"]).upper()
    core = re.sub(r"[^\wÄÖÜß:]", "", t)
    col = CYAN if core in KEY else (RED if ("PFEIF" in core or "PFIFF" in core) else YEL)
    fs = min(116, int(940 / (0.62 * max(len(t), 1))))
    sid = f"sub{k}"
    subs.append(f'<div id="{sid}" class="clip sub" data-start="{s:.3f}" data-duration="{max(0.05, e-s):.3f}" data-track-index="9" style="font-size:{fs}px;color:{col}">{html.escape(t)}</div>')
    tw(f'tl.fromTo("#{sid}",{{scale:.7,opacity:0}},{{scale:1,opacity:1,duration:.12,ease:"back.out(2)"}},{s:.3f});')

# ================= GLOBALE EBENEN (Skill 6a) =================
def noise_png(n=256, seed=3):
    rr = random.Random(seed)
    raw = b"".join(b"\x00" + bytes(v for _ in range(n) for v in (lambda g: (g, g, g, rr.randint(0, 38)))(rr.randint(0, 255))) for _ in range(n))
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", n, n, 8, 6, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
    return base64.b64encode(png).decode()


DEFS = f"""<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<linearGradient id="skyg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{SKY1}"/><stop offset=".6" stop-color="{SKY2}"/><stop offset="1" stop-color="{VIO}"/></linearGradient>
<radialGradient id="moonglow"><stop offset="0" stop-color="{MOON}" stop-opacity=".35"/><stop offset="1" stop-color="{MOON}" stop-opacity="0"/></radialGradient>
<linearGradient id="lampcone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{LAMP}" stop-opacity=".35"/><stop offset="1" stop-color="{LAMP}" stop-opacity="0"/></linearGradient>
<radialGradient id="lampglow"><stop offset="0" stop-color="#fff6d8" stop-opacity=".5"/><stop offset="1" stop-color="#fff6d8" stop-opacity="0"/></radialGradient>
<radialGradient id="cardglow"><stop offset="0" stop-color="#3a3d8f" stop-opacity=".55"/><stop offset="1" stop-color="#3a3d8f" stop-opacity="0"/></radialGradient>
<radialGradient id="stationglow" cx=".5" cy="0" r="1"><stop offset="0" stop-color="#fff4c9" stop-opacity=".35"/><stop offset="1" stop-color="#fff4c9" stop-opacity="0"/></radialGradient>
<radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".7"/></radialGradient>
<radialGradient id="redvig" cx=".5" cy=".5" r=".72"><stop offset=".5" stop-color="{RED}" stop-opacity="0"/><stop offset="1" stop-color="{RED}" stop-opacity=".7"/></radialGradient>
<radialGradient id="yelglow"><stop offset="0" stop-color="#ffd23f" stop-opacity=".55"/><stop offset="1" stop-color="#ffd23f" stop-opacity="0"/></radialGradient>
{FIGC_DEFS}<linearGradient id="daysky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3f8fe0"/><stop offset=".55" stop-color="#8cc6f5"/><stop offset="1" stop-color="#d9efff"/></linearGradient>
<radialGradient id="sunglow"><stop offset="0" stop-color="#fff4c2" stop-opacity=".6"/><stop offset="1" stop-color="#fff4c2" stop-opacity="0"/></radialGradient>
<linearGradient id="thumbshade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".18"/></linearGradient>
<radialGradient id="namglow"><stop offset="0" stop-color="#fff4c2" stop-opacity=".7"/><stop offset="1" stop-color="#fff4c2" stop-opacity="0"/></radialGradient>
<pattern id="netpat" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M 0 0 L 30 30 M 30 0 L 0 30" stroke="#e8ecff" stroke-width="2"/></pattern>
<linearGradient id="dusksky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a1f4f"/><stop offset=".55" stop-color="#9a4a78"/><stop offset="1" stop-color="#f0a060"/></linearGradient>
<radialGradient id="meye"><stop offset="0" stop-color="#fff6c0"/><stop offset=".45" stop-color="#ffc21a"/><stop offset="1" stop-color="#d63a00"/></radialGradient>
<radialGradient id="mglow"><stop offset="0" stop-color="#ff7a1a" stop-opacity=".45"/><stop offset="1" stop-color="#ff7a1a" stop-opacity="0"/></radialGradient>
<filter id="softblur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="10"/></filter>
<filter id="softedge" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3"/></filter>
<radialGradient id="eyeglow"><stop offset="0" stop-color="#f6f4ff" stop-opacity=".45"/><stop offset="1" stop-color="#f6f4ff" stop-opacity="0"/></radialGradient>
<filter id="fogblur" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="40"/></filter>
<filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="14" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="glowsoft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs></svg>"""

OVER = []
dust = []
for i in range(40):
    x = RNG.randint(0, 1080); y = RNG.randint(0, 1920); r = RNG.choice([2, 3, 3, 4, 5])
    dust.append(f'<circle id="dust{i}" cx="{x}" cy="{y}" r="{r}" fill="#e8e6ff" opacity="{RNG.uniform(.12,.4):.2f}"/>')
    dur = RNG.uniform(6, 14)
    tw(f'tl.fromTo("#dust{i}",{{x:0,y:0}},{{x:{RNG.randint(-80,80)},y:{-RNG.randint(250,600)},duration:{dur:.2f},ease:"sine.inOut",repeat:{int(TOTAL/dur)+1},yoyo:true}},0);')
OVER.append(f'<div id="ov-dust" class="clip ov" data-start="0" data-duration="{TOTAL}" data-track-index="5" style="z-index:5">'
            f'<svg viewBox="0 0 1080 1920" width="1080" height="1920">{"".join(dust)}<rect width="1080" height="1920" fill="url(#vig)"/></svg></div>')
OVER.append(f'<div id="ov-grain" class="clip ov" data-start="0" data-duration="{TOTAL}" data-track-index="6" '
            f'style="z-index:6;left:-128px;top:-128px;width:1336px;height:2176px;opacity:.25;mix-blend-mode:overlay;'
            f'background-image:url(data:image/png;base64,{noise_png()});background-size:256px 256px"></div>')
t = 0.0
while t < TOTAL:
    tw(f'tl.set("#ov-grain",{{x:{RNG.randint(-120,120)},y:{RNG.randint(-120,120)}}},{t:.2f});'); t += 0.1


def danger(did, t0, t1):
    OVER.append(f'<div id="{did}" class="clip ov" data-start="{t0:.3f}" data-duration="{t1-t0:.3f}" data-track-index="8" style="z-index:8">'
                f'<svg viewBox="0 0 1080 1920" width="1080" height="1920"><rect id="{did}-v" width="1080" height="1920" fill="url(#redvig)" opacity=".3"/></svg></div>')
    tw(f'tl.fromTo("#{did}-v",{{opacity:.2}},{{opacity:.7,duration:.45,yoyo:true,repeat:{int((t1-t0)/0.45)},ease:"sine.inOut"}},{t0:.3f});')


for _d in DANGER:
    danger(*_d)
for fid in FIGS:
    tw(f'tl.fromTo("#{fid}-body",{{scaleY:1}},{{scaleY:1.02,transformOrigin:"50% 100%",duration:1.3,yoyo:true,repeat:{int(TOTAL/1.3)},ease:"sine.inOut"}},0);')
for sid, t0, t1, _ in SCENES[1:]:
    tw(f'tl.fromTo("#{sid}",{{opacity:0}},{{opacity:1,duration:{XF},ease:"sine.inOut"}},{t0:.3f});')

# ================= HTML =================
scene_html = [f'<div id="{sid}" class="clip scene" data-start="{t0:.3f}" data-duration="{min(t1+XF, TOTAL)-t0:.3f}" data-track-index="1">'
              f'<svg viewBox="0 0 1080 1920" width="1080" height="1920">{inner}</svg></div>' for sid, t0, t1, inner in SCENES]

doc = f'''<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Nicht pfeifen</title>
    <script src="assets/gsap.min.js"></script>
    <style>
      :root {{ --ground: {SKY1}; --ink: #ffffff; --accent: {RED}; --font-display: "Poppins", sans-serif; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: var(--ground); }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: var(--font-display); }}
      .scene, .ov {{ position: absolute; inset: 0; }}
      .ov {{ pointer-events: none; }}
      .scene svg {{ display: block; }}
      .sub {{ position: absolute; left: 0; right: 0; top: 1330px; text-align: center; z-index: 20; font-weight: 800; letter-spacing: 1px;
        -webkit-text-stroke: 14px #0b0b0b; paint-order: stroke fill; text-shadow: 0 6px 0 #0b0b0b; line-height: 1; transform-origin: 50% 50%; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <audio id="vo" class="clip" data-start="0" data-duration="{VO_END:.2f}" data-volume="1" src="assets/voiceover.mp3"></audio>
      <audio id="sfx" class="clip" data-start="0" data-duration="{TOTAL}" data-volume="0.45" src="assets/sfx_bed.wav"></audio>
      {DEFS}
      {"".join(scene_html)}
      {"".join(OVER)}
      {"".join(brand_html)}
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
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(doc)
cues = {k: v for k, v in globals().items() if k.startswith("t_") and isinstance(v, (int, float))}
cues["TOTAL"] = TOTAL
json.dump(cues, open(os.path.join(HERE, "assets/cues.json"), "w"), indent=1)
print(f"Szenen: {len(SCENES)}, Untertitel: {len(subs)}, Tweens: {len(T)}, Länge: {TOTAL}s")
