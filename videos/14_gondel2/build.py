#!/usr/bin/env python3
"""Generator für index.html – Video 13 „HÖHE · Teil 1“ (Skill-Format B „Regel-Serie“).

Alle Zeiten kommen aus assets/words.json (wortgenaue Voiceover-Zeitstempel).
Aufruf: python3 build.py → index.html + assets/cues.json
"""
import json, re, html, os, math, random, zlib, struct, base64

HERE = os.path.dirname(os.path.abspath(__file__))
W = json.load(open(os.path.join(HERE, "assets/words.json"), encoding="utf-8"))
VO_END = W[-1]["e"]
TOTAL = round(VO_END + 3.2, 2)          # Teil-2-Karte steht noch gut 3 s
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


# ---------- Figuren ----------
FIGS = []


def figure(fid, x, y, s=1.0, eyes="n", outfit="hoodie", back=False):
    """Gesichtslose Puppe mit Kleidung (Skill 6). outfit: hoodie | vest (Kassierer)."""
    FIGS.append(fid)
    if outfit == "vest":
        H, H2, P, SH = "#c0392b", "#9b2d22", "#2c3a52", "#1a1d22"
        extra = '<rect x="-44" y="-250" width="88" height="140" rx="20" fill="#e6e9ee"/><rect x="-40" y="-250" width="80" height="140" rx="18" fill="#2f7a4a"/><rect x="18" y="-210" width="18" height="10" rx="3" fill="#e6e9ee"/>'
        H = "#e6e9ee"; H2 = "#cfd3da"
    else:
        H, H2, P, SH = "#2f6f73", "#265b5e", "#2c3a52", "#eef0f3"
        extra = ('<ellipse cx="0" cy="-252" rx="46" ry="16" fill="#1f4b4e"/>'
                 '<rect x="-12" y="-248" width="4" height="40" rx="2" fill="#e6e9ee"/><rect x="8" y="-248" width="4" height="40" rx="2" fill="#e6e9ee"/>'
                 '<rect x="-40" y="-178" width="80" height="34" rx="12" fill="#265b5e"/>')
    if back:
        extra = '<ellipse cx="0" cy="-262" rx="52" ry="34" fill="#265b5e"/>'
    def eye(name, op, body):
        return f'<g id="{fid}-eyes-{name}" opacity="{op}">{body}</g>'
    E = INK
    E = INK
    brow = lambda x, y, r: f'<rect x="{x}" y="{y}" width="26" height="7" rx="3.5" fill="{HAIR}" transform="rotate({r} {x+13} {y+3})"/>'
    eyes_svg = "" if back else (
        eye("n", 1 if eyes == "n" else 0,
            f'<ellipse cx="-22" cy="-326" rx="12" ry="9" fill="#fff"/><ellipse cx="22" cy="-326" rx="12" ry="9" fill="#fff"/>'
            f'<circle cx="-20" cy="-326" r="6" fill="#4a3426"/><circle cx="24" cy="-326" r="6" fill="#4a3426"/><circle cx="-20" cy="-326" r="2.6" fill="{E}"/><circle cx="24" cy="-326" r="2.6" fill="{E}"/>'
            + brow(-36, -348, -4) + brow(10, -348, 4)
            + f'<path d="M -13 -284 Q 0 -277 13 -284" stroke="{LIP}" stroke-width="5" fill="none" stroke-linecap="round"/>')
        + eye("w", 1 if eyes == "w" else 0,
              f'<ellipse cx="-22" cy="-326" rx="15" ry="13" fill="#fff"/><ellipse cx="22" cy="-326" rx="15" ry="13" fill="#fff"/>'
              f'<circle cx="-22" cy="-326" r="5.5" fill="#4a3426"/><circle cx="22" cy="-326" r="5.5" fill="#4a3426"/><circle cx="-22" cy="-326" r="2.4" fill="{E}"/><circle cx="22" cy="-326" r="2.4" fill="{E}"/>'
              + brow(-38, -360, -12) + brow(12, -360, 12)
              + f'<ellipse cx="0" cy="-282" rx="9" ry="12" fill="#5a2a24"/><ellipse cx="0" cy="-276" rx="5" ry="4" fill="#c46a6a"/>')
        + eye("f", 1 if eyes == "f" else 0,
              f'<ellipse cx="-22" cy="-325" rx="12" ry="6" fill="#fff"/><ellipse cx="22" cy="-325" rx="12" ry="6" fill="#fff"/>'
              f'<circle cx="-21" cy="-325" r="5" fill="#4a3426"/><circle cx="23" cy="-325" r="5" fill="#4a3426"/>'
              + brow(-38, -346, 14) + brow(12, -346, -14)
              + f'<path d="M -13 -282 L 13 -282" stroke="{LIP}" stroke-width="5" stroke-linecap="round"/>')
        + eye("s", 1 if eyes == "s" else 0,
              f'<path d="M -34 -324 Q -22 -316 -10 -324" stroke="#5a3a2a" stroke-width="5" fill="none" stroke-linecap="round"/>'
              f'<path d="M 10 -324 Q 22 -316 34 -324" stroke="#5a3a2a" stroke-width="5" fill="none" stroke-linecap="round"/>'
              + brow(-36, -346, 0) + brow(10, -346, 0)
              + f'<path d="M -8 -284 Q 0 -280 8 -284" stroke="{LIP}" stroke-width="5" fill="none" stroke-linecap="round"/>'))
    face = "" if back else (
        f'<path d="M 2 -320 Q 10 -302 -2 -296" stroke="{SKIN2}" stroke-width="5" fill="none" stroke-linecap="round"/>'
        f'<circle cx="-34" cy="-300" r="11" fill="#e98f7a" opacity=".35"/><circle cx="34" cy="-300" r="11" fill="#e98f7a" opacity=".35"/>')
    hair = (f'<path d="M -60 -322 Q -70 -398 0 -404 Q 70 -400 60 -322 Q 56 -356 30 -366 Q 10 -352 -20 -370 Q -48 -360 -60 -322 Z" fill="{HAIR}"/>'
            f'<path d="M -20 -370 Q -6 -352 18 -360" stroke="#4d382b" stroke-width="5" fill="none"/>') if not back else \
           f'<ellipse cx="0" cy="-330" rx="60" ry="66" fill="{HAIR}"/>'
    return f'''<g id="{fid}"><g transform="translate({x},{y}) scale({s})">
  <ellipse cx="0" cy="4" rx="78" ry="15" fill="#000" opacity=".4"/>
  <g id="{fid}-body">
  <g id="{fid}-legL"><rect x="-34" y="-128" width="27" height="124" rx="12" fill="{P}"/><ellipse cx="-22" cy="-6" rx="25" ry="12" fill="{SH}"/></g>
  <g id="{fid}-legR"><rect x="7" y="-128" width="27" height="124" rx="12" fill="{P}"/><ellipse cx="22" cy="-6" rx="25" ry="12" fill="{SH}"/></g>
  <rect x="-62" y="-258" width="124" height="152" rx="36" fill="{H}"/>
  <rect x="-62" y="-128" width="124" height="18" rx="9" fill="{H2}"/>
  {extra}
  <rect x="-88" y="-248" width="28" height="112" rx="13" fill="{H}"/>
  <rect x="60" y="-248" width="28" height="112" rx="13" fill="{H}"/>
  <rect x="-88" y="-150" width="28" height="14" rx="6" fill="{H2}"/><rect x="60" y="-150" width="28" height="14" rx="6" fill="{H2}"/>
  <rect x="40" y="-258" width="22" height="150" rx="10" fill="#000" opacity=".12"/>
  <circle cx="-74" cy="-126" r="14" fill="{FIG}"/><circle cx="74" cy="-126" r="14" fill="{FIG}"/>
  <circle cx="-80" cy="-122" r="6" fill="{SKIN2}" opacity=".5"/><circle cx="80" cy="-122" r="6" fill="{SKIN2}" opacity=".5"/>
  <rect x="-14" y="-280" width="28" height="30" rx="8" fill="{SKIN2}"/>
  <ellipse cx="-56" cy="-318" rx="10" ry="16" fill="{SKIN2}"/><ellipse cx="56" cy="-318" rx="10" ry="16" fill="{SKIN2}"/>
  <ellipse cx="0" cy="-322" rx="56" ry="66" fill="{FIG}"/>
  <path d="M 30 -380 Q 62 -330 34 -266 Q 56 -300 56 -330 Q 54 -370 30 -380 Z" fill="{SKIN2}" opacity=".35"/>
  {hair}{face}
  {eyes_svg}
  </g>
</g></g>'''


def stalker(sid, x, y, s=1.0):
    """Dunkle Kapuzen-Silhouette, Hände in den Taschen, kein Gesicht."""
    D, D2 = "#07081a", "#11132e"
    return f'''<g id="{sid}"><g transform="translate({x},{y}) scale({s})">
  <ellipse cx="0" cy="4" rx="80" ry="15" fill="#000" opacity=".5"/>
  <g id="{sid}-body">
  <g id="{sid}-legL"><rect x="-36" y="-130" width="30" height="126" rx="12" fill="{D}"/></g>
  <g id="{sid}-legR"><rect x="6" y="-130" width="30" height="126" rx="12" fill="{D}"/></g>
  <rect x="-66" y="-262" width="132" height="160" rx="38" fill="{D2}"/>
  <rect x="-80" y="-250" width="30" height="96" rx="14" fill="{D2}"/><rect x="50" y="-250" width="30" height="96" rx="14" fill="{D2}"/>
  <rect x="-46" y="-176" width="92" height="40" rx="14" fill="{D}"/>
  <path d="M -76 -300 Q -76 -400 0 -404 Q 76 -400 76 -300 L 70 -256 L -70 -256 Z" fill="{D2}"/>
  <ellipse cx="0" cy="-308" rx="46" ry="52" fill="#000"/>
  <rect x="-66" y="-262" width="132" height="160" rx="38" fill="none" stroke="#3b3f7a" stroke-width="3" opacity=".6"/>
  </g>
</g></g>'''


def walk_cycle(fid, t0, t1, period=0.55, bob=8):
    n = max(1, int((t1 - t0) / period))
    tw(f'tl.fromTo("#{fid}-body",{{y:0}},{{y:-{bob},duration:{period/2:.3f},yoyo:true,repeat:{n*2-1},ease:"sine.inOut"}},{t0:.3f});')
    tw(f'tl.fromTo("#{fid}-legL",{{y:0}},{{y:-14,duration:{period/2:.3f},yoyo:true,repeat:{n*2-1},ease:"sine.inOut"}},{t0:.3f});')
    tw(f'tl.fromTo("#{fid}-legR",{{y:-14}},{{y:0,duration:{period/2:.3f},yoyo:true,repeat:{n*2-1},ease:"sine.inOut"}},{t0:.3f});')



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
t_entsch = ws("entschieden"); t_luke = ws("Dachluke"); t_342 = ws("Drei"); t_kratzt = ws("kratzt"); t_finger = ws("Fingernägel")
t_drueckst = ws("drückst"); t_dreht = ws("dreht"); t_zenti = ws("Zentimeter")
t_rammst = ws("rammst"); t_stoppt = ws("stoppt"); t_kratzen = ws("Kratzen")
t_stille = ws("Stille"); t_atem = ws("Atem"); t_akku = ws("Akku"); t_23 = ws("dreiundzwanzig")
t_knackt = ws("knackt"); t_atmet = ws("atmet"); t_ruhig = ws("ruhig")
t_fahrgast = ws("Fahrgast"); t_links_f = ws("linken")
t_regel = ws("Regel"); t_mitte = ws("Mitte"); t_ruehrst = ws("rührst")
t_vibriert = ws("vibriert"); t_berg = ws("Bergwacht"); t_strom = ws("Strom")
t_wer = ws("Wer"); t_kippt = ws("kippt"); t_haengen = ws("hängen")
t_410 = ws("Vier"); t_hand1 = ws("Handabdruck"); t_aussen = ws("außen"); t_noch1 = ws("noch", t_aussen); t_noch2 = ws("noch", t_noch1 + 0.05); t_hoeher = ws("höher")
t_punkte = ws("Punkte"); t_blinzeln = ws("blinzeln")
t_fluestert = ws("flüstert"); t_stimme = ws("Stimme"); t_licht = ws("Licht", t_stimme); t_sehen = ws("sehen", t_licht)
t_was = ws("Was", t_sehen); t_lampe = ws("Taschenlampe"); t_dunkel = ws("dunkel", t_lampe)
t_teil3 = ws("Teil", t_dunkel); t_folge = ws("Folge", t_teil3)

ROCK = "#151735"; ROCK2 = "#1e2148"; CABLE = "#9aa0c8"; CAB = "#d8dbe8"; CAB2 = "#b9bdd2"; STEEL = "#5a5f86"; FROST = "#cfe6ff"


# ---------- Umgebung (Skill 6a: Tiefe, Licht, Details) ----------
def night_sky(seed=1):
    rr = random.Random(seed)
    return (f'<rect width="1080" height="1920" fill="url(#skyg)"/><circle cx="830" cy="330" r="70" fill="{MOON}"/><circle cx="830" cy="330" r="260" fill="url(#moonglow)"/>'
            + "".join(f'<circle cx="{rr.randint(0,1080)}" cy="{rr.randint(0,1100)}" r="{rr.choice([1.5,2,2.5,3])}" fill="#fff" opacity="{rr.uniform(.3,.9):.2f}"/>' for _ in range(70)))


def gorge(seed=2, lights=True, y_top=900):
    """Felswände links/rechts, tief unten das Tal mit winzigen Lichtern."""
    rr = random.Random(seed)
    far = (f'<path d="M 0 {y_top+120} L 160 {y_top-40} L 300 {y_top+60} L 470 {y_top-120} L 640 {y_top+40} L 820 {y_top-80} L 1080 {y_top+80} L 1080 1920 L 0 1920 Z" fill="#191b45"/>'
           f'<path d="M 470 {y_top-120} L 520 {y_top-60} L 500 {y_top-50} L 440 {y_top-80} Z" fill="#e8ecff" opacity=".5"/>')
    valley = f'<rect x="0" y="1650" width="1080" height="270" fill="#0d0e2a"/><path d="M 0 1700 Q 540 1640 1080 1710" stroke="#2b3a7a" stroke-width="10" fill="none" opacity=".7"/>'
    lts = "".join(f'<circle cx="{rr.randint(320,760)}" cy="{rr.randint(1660,1760)}" r="{rr.choice([2,3,3,4])}" fill="{WIN}" opacity=".85"/>' for _ in range(18)) if lights else ""
    walls = (f'<path d="M 0 {y_top-200} L 120 {y_top-60} L 90 {y_top+200} L 230 {y_top+420} L 200 1300 L 330 1650 L 0 1920 Z" fill="{ROCK}"/>'
             f'<path d="M 1080 {y_top-260} L 960 {y_top-40} L 1010 {y_top+260} L 860 {y_top+480} L 900 1350 L 760 1650 L 1080 1920 Z" fill="{ROCK}"/>'
             f'<path d="M 0 {y_top-200} L 120 {y_top-60} L 90 {y_top+200} L 60 {y_top+220} Z" fill="{ROCK2}"/>'
             f'<path d="M 1080 {y_top-260} L 960 {y_top-40} L 1000 {y_top+200} L 1040 {y_top+220} Z" fill="{ROCK2}"/>'
             + "".join(f'<path d="M {x} {y} l 14 -36 l 14 36 Z" fill="#0f1130"/>' for x, y in ((40, y_top - 160), (70, y_top - 120), (1000, y_top - 200), (1030, y_top - 170), (150, 1280), (880, 1320))))
    mist = "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="40" fill="#8a8fb8" opacity=".08"/>' for x, y, rx in ((300, 1400, 380), (760, 1500, 420), (540, 1600, 500)))
    return far + valley + lts + mist + walls


def gondola_ext(gid, cx, top, s=1.0, lit=True):
    """Gondel außen: Laufwerk am Seil, Gehänge, Kabine mit Fenstern, Tür, Dachluke."""
    g = (f'<rect x="-70" y="-26" width="140" height="40" rx="10" fill="{STEEL}"/><circle cx="-40" cy="-20" r="16" fill="#2c2f55"/><circle cx="40" cy="-20" r="16" fill="#2c2f55"/>'
         f'<rect x="-10" y="10" width="20" height="200" fill="{STEEL}"/><path d="M -10 200 Q -150 210 -150 260 L 150 260 Q 150 210 10 200 Z" fill="{STEEL}"/>'
         f'<rect x="-170" y="250" width="340" height="40" rx="14" fill="{CAB2}"/><rect x="-40" y="238" width="80" height="16" rx="5" fill="#8a8fb0"/>'
         f'<rect x="-170" y="280" width="340" height="300" rx="34" fill="{CAB}"/>'
         + "".join(f'<rect x="{-150+k*104}" y="310" width="92" height="150" rx="14" fill="{"#ffe2a8" if lit else "#2a2f66"}" opacity="{.85 if lit else 1}"/>' for k in range(3))
         + f'<rect x="58" y="300" width="96" height="260" rx="10" fill="none" stroke="{CAB2}" stroke-width="6"/><rect x="66" y="430" width="22" height="8" rx="4" fill="#555a80"/>'
         f'<rect x="-170" y="490" width="340" height="16" fill="#c74545"/><rect x="-170" y="540" width="340" height="40" rx="18" fill="{CAB2}"/>'
         f'<text x="-100" y="530" font-family="JetBrains Mono" font-weight="800" font-size="26" fill="#3a3f6a">7</text>')
    return f'<g id="{gid}"><g transform="translate({cx},{top}) scale({s})">{g}</g></g>'


def cable(y0, y1, w=6):
    return f'<line x1="-40" y1="{y0}" x2="1120" y2="{y1}" stroke="{CABLE}" stroke-width="{w}"/><line x1="-40" y1="{y0+40}" x2="1120" y2="{y1+40}" stroke="{CABLE}" stroke-width="{w*0.6:.1f}" opacity=".5"/>'


def interior(gid, frost=False, dark=False):
    """Kabine innen: Decke mit Lautsprecher + Dachluke, große Fenster mit Tiefblick, Bank, Tür rechts."""
    win = ""
    for k, x in enumerate((90, 390)):
        win += (f'<clipPath id="{gid}-wc{k}"><rect x="{x}" y="520" width="280" height="560" rx="30"/></clipPath>'
                f'<g clip-path="url(#{gid}-wc{k})"><g id="{gid}-view{k}" transform="translate({-x*0.4:.0f},-180) scale(1.1)">{night_sky(5+k)}{gorge(6+k, y_top=700)}</g>'
                + (f'<circle cx="{x+190}" cy="640" r="34" fill="{MOON}"/><circle cx="{x+190}" cy="640" r="120" fill="url(#moonglow)"/>' if k == 1 else "")
                + f'<path d="M {x+40} 1080 L {x+200} 520 L {x+240} 520 L {x+80} 1080 Z" fill="#fff" opacity=".06"/>'
                + (f'<rect x="{x}" y="520" width="280" height="560" fill="{FROST}" opacity=".28"/>' + "".join(f'<path d="M {x+dx} {1080} q 20 -60 0 -120 q -20 -40 10 -90" stroke="#fff" stroke-width="4" fill="none" opacity=".5"/>' for dx in (30, 120, 220)) if frost else "")
                + f'</g><rect x="{x}" y="520" width="280" height="560" rx="30" fill="none" stroke="{CAB2}" stroke-width="18"/>')
    door = (f'<g id="{gid}-door"><rect x="720" y="470" width="300" height="1060" rx="20" fill="#c3c7da"/><rect x="745" y="520" width="250" height="420" rx="22" fill="#20244f"/>'
            f'<rect x="745" y="520" width="250" height="420" rx="22" fill="none" stroke="#aeb3cc" stroke-width="10"/>'
            + (f'<rect x="745" y="520" width="250" height="420" fill="{FROST}" opacity=".3"/>' if frost else "")
            + f'<g id="{gid}-handle"><rect x="750" y="1040" width="110" height="34" rx="17" fill="{STEEL}"/><circle cx="760" cy="1057" r="24" fill="#3c4068"/></g>'
            f'<rect x="740" y="1180" width="260" height="14" rx="7" fill="#c74545"/><text x="870" y="1250" text-anchor="middle" font-family="JetBrains Mono" font-weight="700" font-size="24" fill="#5a5f86">NICHT ÖFFNEN</text></g>')
    ceil = (f'<rect x="0" y="0" width="1080" height="440" fill="{"#5d6288" if dark else "#b3b7cc"}"/><rect x="0" y="400" width="1080" height="70" fill="{"#50557a" if dark else "#9ea3bd"}"/>'
            f'<g id="{gid}-hatch"><rect x="470" y="110" width="300" height="200" rx="16" fill="#7a7fa0" stroke="#4d5276" stroke-width="10"/>'
            f'<g id="{gid}-hlever"><rect x="600" y="196" width="120" height="26" rx="13" fill="#2c3157"/><circle cx="610" cy="209" r="18" fill="#20244f"/></g></g>'
            f'<g id="{gid}-spk"><circle cx="930" cy="210" r="80" fill="#3c4068"/>' + "".join(f'<circle cx="{930+dx}" cy="{210+dy}" r="7" fill="#20244f"/>' for dx in (-36, -12, 12, 36) for dy in (-24, 0, 24)) + '</g>'
            f'<rect x="250" y="40" width="160" height="40" rx="20" fill="#fff6d8" opacity="{.25 if dark else .9}"/><circle cx="330" cy="60" r="160" fill="url(#lampglow)" opacity="{.2 if dark else .6}"/>')
    walls = (f'<rect x="0" y="440" width="1080" height="1480" fill="{"#5c6290" if dark else "#7a80ad"}"/>'
             f'<rect x="0" y="1100" width="720" height="40" fill="#686e9c"/>')
    bench = (f'<rect x="40" y="1330" width="660" height="70" rx="20" fill="#3d5a8a"/><rect x="60" y="1400" width="30" height="180" fill="#2c3157"/><rect x="640" y="1400" width="30" height="180" fill="#2c3157"/>'
             f'<rect x="40" y="1230" width="660" height="100" rx="24" fill="#456aa0"/>'
             f'<rect x="80" y="1290" width="120" height="40" rx="12" fill="#c74545"/><text x="140" y="1318" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="22" fill="#fff">SOS</text>')
    floor = f'<rect x="0" y="1580" width="1080" height="340" fill="#2c3157"/>' + "".join(f'<rect x="0" y="{1600+k*60}" width="1080" height="4" fill="#3a4070"/>' for k in range(6))
    return walls + win + ceil + door + bench + floor


def phone(pid, inner, x=540, y=980, s=1.0):
    return (f'<g id="{pid}"><g transform="translate({x},{y}) scale({s})"><rect x="-300" y="-600" width="600" height="1200" rx="70" fill="#0c0d1c"/>'
            f'<rect x="-280" y="-580" width="560" height="1160" rx="56" fill="#13163a"/><rect x="-70" y="-566" width="140" height="30" rx="15" fill="#0c0d1c"/>{inner}</g></g>')


def quote(qid, lines, y=430, col=RED, label_txt="– VOR DER TÜR –"):
    out = f'<g id="{qid}-lab" opacity="0"><text x="540" y="{y-90}" text-anchor="middle" font-family="JetBrains Mono" font-weight="700" font-size="28" fill="#cfd3ff" letter-spacing="4">{label_txt}</text></g>'
    for i, ln in enumerate(lines):
        out += f'<g id="{qid}-{i}" opacity="0"><text x="540" y="{y+i*72}" text-anchor="middle" font-family="Poppins" font-style="italic" font-weight="700" font-size="54" fill="{col}">{html.escape(ln)}</text></g>'
    return out


def creature(cid, x, y, s=1.0):
    """Eigenes Design: hagere, überlange Schattengestalt mit bleichen Lichtpunkt-Augen, klammert sich an die Kabine."""
    D = "#05061a"
    return (f'<g id="{cid}"><g transform="translate({x},{y}) scale({s})">'
            f'<path d="M -40 -260 Q 0 -300 40 -260 L 50 40 Q 0 70 -50 40 Z" fill="{D}"/>'
            f'<ellipse cx="0" cy="-300" rx="46" ry="60" fill="{D}"/>'
            f'<path d="M -40 -220 Q -160 -260 -230 -380 L -250 -420 M -230 -380 L -270 -390 M -230 -380 L -220 -430" stroke="{D}" stroke-width="18" fill="none" stroke-linecap="round"/>'
            f'<path d="M 40 -220 Q 160 -200 220 -120 L 250 -100 M 220 -120 L 240 -150 M 220 -120 L 260 -120" stroke="{D}" stroke-width="18" fill="none" stroke-linecap="round"/>'
            f'<path d="M -30 30 Q -60 160 -40 300 M 30 30 Q 70 160 50 300" stroke="{D}" stroke-width="20" fill="none" stroke-linecap="round"/>'
            f'<g id="{cid}-eyes"><circle cx="-16" cy="-306" r="7" fill="#f2f0ff"/><circle cx="16" cy="-306" r="7" fill="#f2f0ff"/>'
            f'<circle cx="-16" cy="-306" r="22" fill="#f2f0ff" opacity=".15"/><circle cx="16" cy="-306" r="22" fill="#f2f0ff" opacity=".15"/></g></g></g>')


# ================= SZENEN =================
def card_bg(cid):
    return (f'<rect width="1080" height="1920" fill="{CARD_BG}"/><circle cx="540" cy="760" r="520" fill="url(#cardglow)"/>'
            + "".join(f'<rect x="{x}" y="0" width="2" height="1920" fill="#fff" opacity=".025"/>' for x in range(0, 1080, 60))
            + "".join(f'<rect x="0" y="{y}" width="1080" height="2" fill="#fff" opacity=".025"/>' for y in range(0, 1920, 60)))


def fadein(sel, t, dur=0.45, dy=16):
    """Saubere Einblendung: weiches Einblenden + leichtes Hochgleiten (kein Aufploppen)."""
    tw(f'tl.fromTo("{sel}",{{opacity:0,y:{dy}}},{{opacity:1,y:0,duration:{dur},ease:"sine.out"}},{t:.3f});')


def hands(hid):
    one = lambda dx: (f'<rect x="{dx-55}" y="300" width="110" height="420" rx="50" fill="#2f6f73"/><rect x="{dx-58}" y="300" width="116" height="40" rx="18" fill="#265b5e"/>'
                      f'<rect x="{dx-52}" y="190" width="104" height="130" rx="44" fill="{FIG}"/>'
                      + "".join(f'<rect x="{dx-50+k*26}" y="140" width="24" height="80" rx="12" fill="{FIG}"/>' for k in range(4))
                      + f'<rect x="{dx-52}" y="250" width="104" height="20" rx="10" fill="{SKIN2}" opacity=".4"/>')
    return f'<g id="{hid}">{one(-120)}{one(120)}</g>'


def hatch_close(hid, with_bar=False):
    bar = (f'<g id="{hid}-bar"><rect x="560" y="738" width="560" height="44" rx="10" fill="#e9c46a"/>'
           + "".join(f'<rect x="{600+k*80}" y="738" width="34" height="44" fill="#1a1d22" opacity=".8"/>' for k in range(7)) + '</g>') if with_bar else ""
    return (f'<rect width="1080" height="1920" fill="#4d527a"/><rect x="0" y="1300" width="1080" height="620" fill="#3d4268"/>'
            f'<rect x="160" y="420" width="760" height="680" rx="40" fill="#2f3358" stroke="#20244f" stroke-width="24"/>'
            f'<rect x="210" y="470" width="660" height="580" rx="24" fill="#6f7499"/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="12" fill="#3c4068"/>' for x in (240, 840) for y in (500, 1020))
            + f'<g id="{hid}-lever"><rect x="520" y="735" width="340" height="50" rx="25" fill="#2c3157"/>{bar}<circle cx="540" cy="760" r="56" fill="#20244f"/><circle cx="540" cy="760" r="22" fill="#9aa0c8"/></g>')


def claw_marks(sid, x0, y0, n=4, length=220):
    """Kratzspuren wie Fingernägel – werden langsam gezogen (stroke-dashoffset)."""
    out = ""
    for i in range(n):
        out += (f'<path id="{sid}{i}" d="M {x0+i*34} {y0} q 14 {length*0.5:.0f} 6 {length}" stroke="#e6e9ff" stroke-width="5" stroke-linecap="round" fill="none" '
                f'stroke-dasharray="{length+20}" stroke-dashoffset="{length+20}" opacity=".75"/>')
    return out


def draw(sel, t, dur, length):
    tw(f'tl.fromTo("{sel}",{{attr:{{"stroke-dashoffset":{length+20}}}}},{{attr:{{"stroke-dashoffset":0}},duration:{dur:.3f},ease:"sine.inOut"}},{t:.3f});')


# A Hook: du hast entschieden – über dir kratzt etwas, wie Fingernägel
S0, S1 = 0.0, t_drueckst - 0.05
scene("sa", S0, S1, interior("sa", frost=True, dark=True) + claw_marks("sa-c", 520, 125, 4, 150)
      + figure("sa-fig", 610, 1440, 1.15, eyes="w")
      + f'<g id="sa-badge" opacity="0"><rect x="300" y="560" width="480" height="64" rx="32" fill="{LIME}"/>'
        f'<text x="540" y="604" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="32" fill="#0b0d22" letter-spacing="2">DU HAST GEWÄHLT</text></g>'
      + pill("sa-p", 540, 760, "A · DACHLUKE ZUHALTEN", RED), drift=False)
fadein("#sa-badge", S0 + 0.05); fadein("#sa-p", t_luke)
tw(f'tl.to("#sa-badge, #sa-p",{{opacity:0,duration:.4,ease:"sine.in"}},{t_kratzt - 0.4:.3f});')
for i in range(4):
    draw(f"#sa-c{i}", t_kratzt + i * 0.25, 1.2, 150)
tw(f'tl.fromTo("#sa-cam",{{scale:1,svgOrigin:"620 220"}},{{scale:1.18,svgOrigin:"620 220",duration:{S1-S0+0.3:.3f},ease:"sine.inOut"}},{S0:.3f});')
tw(f'tl.set("#sa-fig-eyes-w",{{opacity:1}},0);')

# B Hände gegen den Hebel – er dreht sich trotzdem, Zentimeter für Zentimeter
S0, S1 = t_drueckst - 0.05, t_rammst - 0.05
scene("sb", S0, S1, hatch_close("sb") + claw_marks("sb-c", 330, 500, 4, 300) + f'<g transform="translate(700,600)">{hands("sb-h")}</g>', drift=False)
tw(f'tl.fromTo("#sb-h",{{y:300}},{{y:0,duration:.6,ease:"sine.out"}},{S0:.3f});')
for k, (t0, ang) in enumerate(((t_dreht, -7), (t_zenti, -14), (t_zenti + 0.8, -21))):
    tw(f'tl.to("#sb-lever, #sb-h",{{rotation:{ang},svgOrigin:"540 760",duration:.7,ease:"power1.inOut"}},{t0:.3f});')
for i in range(4):
    draw(f"#sb-c{i}", S0 + 0.2 + i * 0.3, 1.4, 300)
tw(f'tl.fromTo("#sb-cam",{{scale:1,svgOrigin:"540 760"}},{{scale:1.06,svgOrigin:"540 760",duration:{S1-S0+0.3:.3f},ease:"sine.inOut"}},{S0:.3f});')

# C Notfall-Stange gleitet in den Griff – Hebel stoppt, Kratzen hört auf
S0, S1 = t_rammst - 0.05, t_stille
scene("sc", S0, S1, hatch_close("sc", with_bar=True) + claw_marks("sc-c", 330, 500, 4, 300) + f'<g transform="translate(700,600)">{hands("sc-h")}</g>', drift=False)
tw(f'tl.set("#sc-lever, #sc-h",{{rotation:-21,svgOrigin:"540 760"}},{S0:.3f});')
for i in range(4):
    tw(f'tl.set("#sc-c{i}",{{attr:{{"stroke-dashoffset":0}}}},{S0:.3f});')
tw(f'tl.fromTo("#sc-bar",{{x:700}},{{x:0,duration:.55,ease:"power3.out"}},{t_rammst + 0.15:.3f});')
shake("#sc-cam", t_rammst + 0.7, 3, 4)
tw(f'tl.to("#sc-c0, #sc-c1, #sc-c2, #sc-c3",{{opacity:0,duration:1.0,ease:"sine.inOut"}},{t_kratzen:.3f});')

# D Stille – nur dein Atem – Akku 23 %
S0, S1 = t_stille, t_knackt
breath = "".join(f'<ellipse id="sd-br{i}" cx="560" cy="1050" rx="44" ry="28" fill="#fff" opacity="0" filter="url(#softblur)"/>' for i in range(3))
bat = (f'<g id="sd-bat" opacity="0"><rect x="700" y="420" width="300" height="100" rx="24" fill="#0b0d22" opacity=".75"/>'
       f'<rect x="730" y="448" width="110" height="44" rx="8" fill="none" stroke="#fff" stroke-width="5"/><rect x="842" y="460" width="8" height="20" rx="3" fill="#fff"/>'
       f'<rect id="sd-lvl" x="736" y="454" width="98" height="32" rx="5" fill="{RED}"/>'
       f'<text x="930" y="486" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="40" fill="{RED}">23 %</text></g>')
scene("sd", S0, S1, interior("sd", frost=True, dark=True) + f'<rect width="1080" height="1920" fill="#000" opacity=".3"/>'
      + figure("sd-fig", 540, 1440, 1.15, eyes="f") + breath + bat, drift=False)
for i in range(3):
    tw(f'tl.fromTo("#sd-br{i}",{{opacity:0,x:0,y:0,scale:.6,transformOrigin:"50% 50%"}},{{opacity:.45,x:40,y:-70,scale:1.5,duration:1.3,ease:"sine.out"}},{t_atem - 0.2 + i*0.9:.3f});')
    tw(f'tl.to("#sd-br{i}",{{opacity:0,duration:.7,ease:"sine.in"}},{t_atem + 1.1 + i*0.9:.3f});')
fadein("#sd-bat", t_akku - 0.1)
tw(f'tl.fromTo("#sd-lvl",{{scaleX:1,transformOrigin:"0% 50%"}},{{scaleX:.23,transformOrigin:"0% 50%",duration:1.0,ease:"sine.inOut"}},{t_akku + 0.2:.3f});')
tw(f'tl.fromTo("#sd-cam",{{scale:1,svgOrigin:"540 1100"}},{{scale:1.08,svgOrigin:"540 1100",duration:{S1-S0+0.3:.3f},ease:"sine.inOut"}},{S0:.3f});')

# E Lautsprecher: jemand atmet hinein … „Gehen Sie zum linken Fenster.“
S0, S1 = t_knackt, t_regel
spk = (f'<g id="se-spk"><circle cx="540" cy="1010" r="260" fill="#2c3157" stroke="#3c4068" stroke-width="22"/>'
       + "".join(f'<circle cx="{540+dx}" cy="{1010+dy}" r="20" fill="#14163a"/>' for dx in (-130, -65, 0, 65, 130) for dy in (-130, -65, 0, 65, 130) if dx*dx + dy*dy <= 140**2 + 10) + '</g>')
rings = "".join(f'<circle id="se-r{i}" cx="540" cy="1010" r="270" fill="none" stroke="#cfd3ff" stroke-width="4" opacity="0"/>' for i in range(3))
scene("se", S0, S1, f'<rect width="1080" height="1920" fill="#3d4268"/><rect width="1080" height="1920" fill="#000" opacity=".5"/>' + rings + spk
      + quote("se-q", ["„Fahrgast in Gondel 7.", "Gehen Sie zum linken Fenster.“"], y=520, col="#ff8a8a", label_txt="– LAUTSPRECHER –"), drift=False)
for i in range(3):   # langsames Atmen: Ringe dehnen sich aus
    tw(f'tl.fromTo("#se-r{i}",{{opacity:.5,scale:1,transformOrigin:"50% 50%"}},{{opacity:0,scale:1.35,duration:1.6,ease:"sine.out"}},{t_atmet + i*0.8:.3f});')
tw(f'tl.to("#se-spk",{{scale:1.03,transformOrigin:"50% 50%",duration:.8,yoyo:true,repeat:3,ease:"sine.inOut"}},{t_atmet:.3f});')
fadein("#se-q-lab", t_fahrgast - 0.2); fadein("#se-q-0", t_fahrgast); fadein("#se-q-1", ws("Gehen", t_fahrgast))
tw(f'tl.fromTo("#se-cam",{{scale:1,svgOrigin:"540 1010"}},{{scale:1.12,svgOrigin:"540 1010",duration:{S1-S0+0.3:.3f},ease:"sine.inOut"}},{S0:.3f});')

# F Regel 1 – du rührst dich nicht
S0, S1 = t_regel, t_vibriert
icon = (f'<line x1="200" y1="760" x2="880" y2="760" stroke="{CABLE}" stroke-width="8"/><line x1="540" y1="760" x2="540" y2="880" stroke="{CABLE}" stroke-width="10"/>'
        f'<rect x="330" y="880" width="420" height="330" rx="40" fill="{CAB}"/>' + "".join(f'<rect x="{360+k*130}" y="910" width="100" height="130" rx="14" fill="#2a2f66"/>' for k in range(3))
        + figure("sf-f", 540, 1190, 0.42)
        + f'<g id="sf-ok" opacity="0"><circle cx="860" cy="1060" r="60" fill="{LIME}"/><path d="M 830 1060 l 22 22 l 40 -44" stroke="#0b0d22" stroke-width="12" fill="none"/></g>')
scene("sf", S0, S1, card_bg("sf")
      + f'<g id="sf-badge" opacity="0"><rect x="430" y="370" width="220" height="62" rx="12" fill="{RED}"/>'
        f'<text x="540" y="415" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="34" fill="#fff">REGEL #1</text></g>'
      + f'<g id="sf-head" opacity="0"><text x="540" y="540" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="80" fill="#fff">BLEIB IN DER MITTE</text></g>' + icon)
fadein("#sf-badge", S0 + 0.05); fadein("#sf-head", t_mitte - 0.3); fadein("#sf-ok", t_ruehrst, 0.4, 0)

# G Handy: Bergwacht – Strom aus, kein Lautsprecher
S0, S1 = t_vibriert, t_wer
chat = (f'<rect x="-280" y="-580" width="560" height="150" rx="0" fill="#1a1d47"/><circle cx="-200" cy="-490" r="36" fill="#c74545"/>'
        f'<text x="-200" y="-478" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="30" fill="#fff">BW</text>'
        f'<text x="-140" y="-480" font-family="Poppins" font-weight="700" font-size="36" fill="#fff">Bergwacht</text>'
        f'<text x="0" y="-370" text-anchor="middle" font-family="Poppins" font-weight="600" font-size="24" fill="#8f94c4">Heute 3:41</text>'
        f'<rect x="-250" y="-340" width="440" height="120" rx="26" fill="#262a5e"/><text x="-225" y="-290" font-family="Poppins" font-weight="600" font-size="28" fill="#fff">Wir starten erst</text>'
        f'<text x="-225" y="-250" font-family="Poppins" font-weight="600" font-size="28" fill="#fff">bei Tageslicht.</text>'
        f'<g id="sg-new" opacity="0"><text x="0" y="-150" text-anchor="middle" font-family="Poppins" font-weight="600" font-size="24" fill="#8f94c4">Heute 3:52</text>'
        f'<rect x="-250" y="-120" width="480" height="210" rx="26" fill="#262a5e" stroke="{LIME}" stroke-width="4"/>'
        f'<text x="-225" y="-66" font-family="Poppins" font-weight="700" font-size="30" fill="#fff">Der Strom ist</text>'
        f'<text x="-225" y="-22" font-family="Poppins" font-weight="700" font-size="30" fill="#fff">komplett aus.</text>'
        f'<text x="-225" y="40" font-family="Poppins" font-weight="700" font-size="30" fill="{LIME}">Kein Lautsprecher</text>'
        f'<text x="-225" y="80" font-family="Poppins" font-weight="700" font-size="30" fill="{LIME}">funktioniert.</text></g>')
scene("sg", S0, S1, f'<rect width="1080" height="1920" fill="#0c0d22"/><circle cx="540" cy="900" r="600" fill="url(#cardglow)"/>' + phone("sg-ph", chat))
tw(f'tl.fromTo("#sg-ph",{{y:120,opacity:0}},{{y:0,opacity:1,duration:.5,ease:"sine.out"}},{S0:.3f});')
fadein("#sg-new", t_strom - 0.3, 0.5, 24)

# H Wer spricht dann mit dir?
S0, S1 = t_wer, t_kippt
scene("sh", S0, S1, f'<rect width="1080" height="1920" fill="#3d4268"/><rect width="1080" height="1920" fill="#000" opacity=".6"/>'
      + spk.replace('id="se-spk"', 'id="sh-spk"')
      + f'<g id="sh-q" opacity="0"><text x="540" y="560" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="72" fill="#ff8a8a" font-style="italic">Wer spricht da?</text></g>', drift=False)
tw(f'tl.fromTo("#sh-cam",{{scale:1,svgOrigin:"540 1010"}},{{scale:1.3,svgOrigin:"540 1010",duration:{S1-S0+0.3:.3f},ease:"sine.in"}},{S0:.3f});')
fadein("#sh-q", S0 + 0.3, 0.8, 0)

# I Gondel kippt langsam nach links – als würde sich etwas an die Seite hängen
S0, S1 = t_kippt, t_410
grip = (f'<g id="si-grip" opacity="0"><g transform="translate(140,1090)">'
        + "".join(f'<path d="M {dx} 40 Q {dx-6} -10 {dx+10} -40" stroke="#05061a" stroke-width="22" stroke-linecap="round" fill="none"/>' for dx in (0, 36, 72, 108))
        + f'<rect x="-20" y="30" width="150" height="120" rx="40" fill="#05061a"/></g></g>')
shadow = f'<g id="si-sh" opacity="0"><ellipse cx="220" cy="780" rx="100" ry="230" fill="#05061a" opacity=".85" filter="url(#softblur)"/></g>'
scene("si", S0, S1, f'<g transform="translate(540,960) scale(1.18) translate(-540,-960)"><g id="si-tilt">{interior("si", frost=True, dark=True)}{shadow}{grip}'
      f'<g id="si-up">{figure("si-fig", 540, 1450, 1.15, eyes="w")}</g></g></g>', drift=False)
PIV = "540 150"; FEET = "540 1450"
for t0, dd, ang in ((S0, 1.6, -5.0), (S0 + 1.6, 1.4, -3.6), (S0 + 3.0, 1.4, -4.4), (S0 + 4.4, 1.4, -4.0)):
    if t0 >= S1 + XF: break
    tw(f'tl.to("#si-tilt",{{rotation:{ang},svgOrigin:"{PIV}",duration:{dd:.3f},ease:"sine.inOut"}},{t0:.3f});')
    tw(f'tl.to("#si-up",{{rotation:{-ang},svgOrigin:"{FEET}",duration:{dd:.3f},ease:"sine.inOut"}},{t0:.3f});')
tw(f'tl.fromTo("#si-sh",{{opacity:0,y:-160}},{{opacity:1,y:0,duration:1.6,ease:"sine.inOut"}},{S0 + 0.2:.3f});')
tw(f'tl.fromTo("#si-grip",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.9,ease:"sine.out"}},{t_haengen - 0.4:.3f});')

# J 4:10 – Handabdrücke von außen, immer höher – zwei helle Punkte, die nicht blinzeln
S0, S1 = t_410, t_fluestert


def handprint(hid, x, y, s=1.0, r=0):
    return (f'<g id="{hid}" opacity="0"><g transform="translate({x},{y}) rotate({r}) scale({s})" filter="url(#softedge)">'
            f'<ellipse cx="0" cy="40" rx="62" ry="72" fill="#e6eeff"/>'
            + "".join(f'<rect x="{fx-12}" y="{fy}" width="24" height="{fh}" rx="12" fill="#e6eeff" transform="rotate({fr} {fx} {fy+fh})"/>' for fx, fy, fh, fr in
                      ((-48, -60, 70, -18), (-20, -96, 96, -6), (10, -102, 100, 4), (38, -84, 86, 14), (54, 8, 56, 52)))
            + '</g></g>')


prints = [handprint("sj-p0", 400, 1260, 1.0, -8), handprint("sj-p1", 660, 1060, 1.0, 10), handprint("sj-p2", 420, 840, 1.05, -4), handprint("sj-p3", 650, 620, 1.1, 6)]
eyes = (f'<g id="sj-eyes" opacity="0"><circle cx="470" cy="900" r="70" fill="url(#eyeglow)"/><circle cx="610" cy="900" r="70" fill="url(#eyeglow)"/>'
        f'<circle cx="470" cy="900" r="13" fill="#f6f4ff"/><circle cx="610" cy="900" r="13" fill="#f6f4ff"/></g>')
win = (f'<rect width="1080" height="1920" fill="#7a80ad"/><rect x="120" y="300" width="840" height="1200" rx="60" fill="#14163a"/>'
       f'<clipPath id="sj-clip"><rect x="120" y="300" width="840" height="1200" rx="60"/></clipPath>'
       f'<g clip-path="url(#sj-clip)"><g transform="translate(-200,-300) scale(1.6)">{night_sky(21)}{gorge(22, y_top=700)}</g>'
       f'<rect x="120" y="300" width="840" height="1200" fill="#05061a" opacity=".35"/>{eyes}'
       f'<g id="sj-fog" opacity="0"><ellipse cx="540" cy="900" rx="320" ry="230" fill="#dfe8ff" opacity=".28" filter="url(#fogblur)"/></g>'
       + "".join(prints) + '</g>'
       f'<rect x="120" y="300" width="840" height="1200" rx="60" fill="none" stroke="{CAB2}" stroke-width="40"/>')
scene("sj", S0, S1, win, drift=False)
for k, t0 in enumerate((t_hand1, t_noch1, t_noch2, t_hoeher)):
    tw(f'tl.fromTo("#sj-p{k}",{{opacity:0,scale:1.06,transformOrigin:"50% 50%"}},{{opacity:.5,scale:1,duration:.5,ease:"sine.out"}},{t0:.3f});')
tw(f'tl.fromTo("#sj-fog",{{opacity:0}},{{opacity:1,duration:1.2,ease:"sine.inOut"}},{t_punkte - 0.8:.3f});')
tw(f'tl.fromTo("#sj-eyes",{{opacity:0}},{{opacity:1,duration:1.0,ease:"sine.in"}},{t_punkte - 0.2:.3f});')
tw(f'tl.fromTo("#sj-cam",{{scale:1,svgOrigin:"540 900"}},{{scale:1.25,svgOrigin:"540 900",duration:{S1-S0+0.3:.3f},ease:"sine.inOut"}},{S0:.3f});')

# K Der Lautsprecher flüstert mit deiner eigenen Stimme
S0, S1 = t_fluestert, t_was
scene("sk", S0, S1, interior("sk", frost=True, dark=True) + f'<rect width="1080" height="1920" fill="#2a0008" opacity=".35"/>'
      + figure("sk-fig", 540, 1440, 1.15, eyes="w")
      + quote("sk-q", ["„Licht an.", "Ich will dich sehen.“"], y=640, col="#ff8a8a", label_txt="– DEINE EIGENE STIMME –"), drift=False)
fadein("#sk-q-lab", t_stimme - 0.3); fadein("#sk-q-0", t_licht); fadein("#sk-q-1", ws("Ich", t_licht))
tw(f'tl.fromTo("#sk-cam",{{scale:1,svgOrigin:"540 1100"}},{{scale:1.15,svgOrigin:"540 1100",duration:{S1-S0+0.3:.3f},ease:"sine.inOut"}},{S0:.3f});')


# N Wahl als Abstimmung (Skill 11a)
S0, S1 = t_was, t_folge - 0.3


def vote_card(cid, x, col, letter, l1, l2, icon):
    return (f'<g id="{cid}" opacity="0"><g id="{cid}-in"><rect x="{x}" y="640" width="420" height="440" rx="36" fill="#14163a" stroke="{col}" stroke-width="8"/>'
            f'<rect id="{cid}-hl" x="{x}" y="640" width="420" height="440" rx="36" fill="{col}" opacity="0"/>'
            f'<circle cx="{x+60}" cy="700" r="38" fill="{col}"/><text x="{x+60}" y="716" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="44" fill="#fff">{letter}</text>'
            f'{icon}'
            f'<text x="{x+210}" y="985" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="40" fill="#fff">{l1}</text>'
            f'<text x="{x+210}" y="1035" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="40" fill="#fff">{l2}</text>'
            f'<rect x="{x+20}" y="1110" width="380" height="34" rx="17" fill="#262a5e"/><rect id="{cid}-bar" x="{x+20}" y="1110" width="380" height="34" rx="17" fill="{col}"/>'
            f'</g></g>')


icon_a = (f'<polygon points="330,790 470,730 470,890 330,830" fill="{GOLD if "GOLD" in globals() else "#ffd98a"}" opacity=".55"/>'
          f'<rect x="190" y="785" width="150" height="50" rx="14" fill="#3c4068"/><rect x="330" y="780" width="30" height="60" rx="8" fill="#9aa0c8"/><circle cx="345" cy="810" r="12" fill="#fff6d8"/>')
icon_b = (f'<circle cx="780" cy="810" r="70" fill="#0b0d22" stroke="#3c4068" stroke-width="6"/>'
          f'<path d="M 745 815 Q 780 840 815 815" stroke="#9aa0c8" stroke-width="7" fill="none" stroke-linecap="round"/>'
          f'<circle cx="840" cy="760" r="26" fill="{MOON}"/><circle cx="852" cy="752" r="22" fill="#14163a"/>')
ring_len = 2 * math.pi * 70
finger = (f'<g id="sn-tap"><g transform="translate(540,1200)"><circle id="sn-ripple" cx="0" cy="-40" r="30" fill="none" stroke="#fff" stroke-width="5" opacity="0"/>'
          f'<rect x="-14" y="-40" width="28" height="80" rx="14" fill="{FIG}"/><rect x="-34" y="10" width="68" height="80" rx="26" fill="{FIG}"/>'
          f'<rect x="-34" y="70" width="68" height="40" rx="12" fill="#2f6f73"/></g></g>')
scene("sn", S0, S1, interior("sn", frost=True, dark=True) + f'<rect width="1080" height="1920" fill="#05061a" opacity=".72"/>'
      + f'<g id="sn-badge" opacity="0"><rect x="370" y="390" width="340" height="60" rx="30" fill="{LIME}"/>'
        f'<text x="540" y="432" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="30" fill="#0b0d22" letter-spacing="3">DU ENTSCHEIDEST</text></g>'
      + f'<g id="sn-q" opacity="0"><text x="540" y="560" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="74" fill="#fff">Was machst du?</text></g>'
      + vote_card("sn-a", 70, RED, "A", "TASCHENLAMPE", "AN", icon_a) + vote_card("sn-b", 590, BLUE, "B", "ALLES", "DUNKEL LASSEN", icon_b)
      + f'<g id="sn-or" opacity="0"><circle cx="540" cy="860" r="70" fill="#0b0d22" stroke="#33376e" stroke-width="10"/>'
        f'<circle id="sn-ring" cx="540" cy="860" r="70" fill="none" stroke="{LIME}" stroke-width="10" stroke-dasharray="{ring_len:.1f}" stroke-dashoffset="0" transform="rotate(-90 540 860)"/>'
        f'<text x="540" y="876" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="44" fill="#fff">ODER</text></g>'
      + finger
      + f'<g id="sn-cta" opacity="0"><rect x="250" y="1215" width="580" height="80" rx="40" fill="#fff"/>'
        f'<text x="540" y="1268" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="36" fill="#0b0d22">💬 Schreib A oder B</text></g>', drift=False)
tw(f'tl.fromTo("#sn-badge",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:.35,ease:"power2.out"}},{S0:.3f});')
pop("#sn-q", S0 + 0.1, 0.35, 0.8)
tw(f'tl.fromTo("#sn-a",{{opacity:0,x:-260}},{{opacity:1,x:0,duration:.45,ease:"power3.out"}},{t_lampe - 0.25:.3f});')
tw(f'tl.fromTo("#sn-b",{{opacity:0,x:260}},{{opacity:1,x:0,duration:.45,ease:"power3.out"}},{t_dunkel - 0.5:.3f});')
pop("#sn-or", t_lampe + 0.2, 0.3, 0.6)
tw(f'tl.fromTo("#sn-ring",{{attr:{{"stroke-dashoffset":0}}}},{{attr:{{"stroke-dashoffset":{ring_len:.1f}}},duration:{max(1.0, S1 - t_lampe):.3f},ease:"none"}},{t_lampe + 0.2:.3f});')
tw(f'tl.set("#sn-a-bar, #sn-b-bar",{{scaleX:0,transformOrigin:"0% 50%"}},{S0:.3f});')
va = [0.42, 0.66, 0.51, 0.6, 0.55]; t_v = t_lampe + 0.3
for k, a in enumerate(va):
    tv = t_v + k * max(0.35, (S1 - t_v) / len(va))
    tw(f'tl.to("#sn-a-bar",{{scaleX:{a},duration:.35,ease:"power2.out"}},{tv:.3f});')
    tw(f'tl.to("#sn-b-bar",{{scaleX:{1-a:.2f},duration:.35,ease:"power2.out"}},{tv:.3f});')
tw(f'tl.set("#sn-tap",{{opacity:0}},{S0:.3f});')
tw(f'tl.fromTo("#sn-tap",{{opacity:0,y:200}},{{opacity:1,y:0,duration:.4,ease:"power2.out"}},{t_lampe + 0.1:.3f});')
seq = [(-260, "a"), (260, "b"), (-260, "a"), (260, "b")]
step = max(0.45, (S1 - t_lampe - 0.5) / len(seq))
for k, (dx, c) in enumerate(seq):
    tk = t_lampe + 0.4 + k * step
    tw(f'tl.to("#sn-tap",{{x:{dx},y:-60,duration:{step*0.5:.3f},ease:"power2.inOut"}},{tk:.3f});')
    tw(f'tl.fromTo("#sn-ripple",{{opacity:.9,scale:.5,transformOrigin:"50% 50%"}},{{opacity:0,scale:2.2,duration:.4,ease:"power1.out"}},{tk + step*0.5:.3f});')
    tw(f'tl.fromTo("#sn-{c}-hl",{{opacity:.35}},{{opacity:0,duration:.45,ease:"sine.out"}},{tk + step*0.5:.3f});')
    tw(f'tl.fromTo("#sn-{c}-in",{{scale:.96,transformOrigin:"50% 50%"}},{{scale:1,duration:.3,ease:"power2.out"}},{tk + step*0.5:.3f});')
tw(f'tl.fromTo("#sn-cta",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.35,ease:"power2.out"}},{max(t_dunkel, S1 - 1.2):.3f});')

# O Teil-3-Karte
S0, S1 = t_folge - 0.3, TOTAL
fog = "".join(f'<ellipse id="so-f{i}" cx="{RNG.randint(0,1080)}" cy="{RNG.randint(300,1700)}" rx="{RNG.randint(300,520)}" ry="{RNG.randint(90,170)}" fill="#8a8fb8" opacity=".09"/>' for i in range(10))
scene("so", S0, S1, f'<rect width="1080" height="1920" fill="#14152e"/>{fog}' + cable(1040, 1100, 4) + gondola_ext("so-g", 540, 1070, 0.5, lit=False)
      + f'<text x="540" y="450" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="36" fill="#cfd3ff" letter-spacing="14">HÖHE</text>'
      + f'<g id="so-t" opacity="0"><text x="540" y="680" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="230" fill="{RED}" filter="url(#glow)">TEIL 3</text></g>'
      + f'<g id="so-s" opacity="0"><text x="540" y="850" text-anchor="middle" font-family="Poppins" font-weight="600" font-size="44" fill="#fff">heute Nacht · 4:10 Uhr</text></g>'
      + f'<g id="so-b" opacity="0"><rect x="330" y="1560" width="420" height="80" rx="40" fill="none" stroke="#fff" stroke-width="5"/>'
        f'<text x="540" y="1613" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="34" fill="#fff" letter-spacing="3">FOLGE FÜR TEIL 3</text></g>')
pop("#so-t", S0 + 0.1, 0.5, 1.3); pop("#so-s", S0 + 0.4); pop("#so-b", S0 + 0.9)
for i in range(10):
    tw(f'tl.fromTo("#so-f{i}",{{x:0}},{{x:{RNG.choice([-1,1])*RNG.randint(80,200)},duration:{S1-S0:.3f},ease:"sine.inOut"}},{S0:.3f});')

# ================= SERIEN-BRANDING OBEN LINKS (Format B) =================
BRAND = [  # (start, ende, uhrzeit, ort)
    (0.0, t_stille, "3:42", "GONDEL 7 · DACHLUKE"), (t_stille, t_knackt, "3:47", "AKKU 23 %"), (t_knackt, t_vibriert, "3:51", "LAUTSPRECHER"),
    (t_vibriert, t_wer, "3:52", "HANDY"), (t_wer, t_410, "3:58", "GONDEL 7"), (t_410, t_teil3, "4:10", "LINKES FENSTER"),
]
BRAND = [(a, b if i + 1 >= len(BRAND) or BRAND[i+1][0] >= b else BRAND[i+1][0], c, d) for i, (a, b, c, d) in enumerate(BRAND)]
brand_html = []
for i, (a, b, clock, place) in enumerate(BRAND):
    brand_html.append(
        f'<div id="br{i}" class="clip ov" data-start="{a:.3f}" data-duration="{b-a:.3f}" data-track-index="7" style="z-index:12">'
        f'<svg viewBox="0 0 1080 1920" width="1080" height="1920"><rect x="40" y="150" width="400" height="200" rx="24" fill="#0b0d22" opacity=".55"/><g transform="translate(70,190)">'
        f'<circle cx="8" cy="-6" r="8" fill="{RED}"/><text x="26" y="2" font-family="JetBrains Mono, monospace" font-weight="700" font-size="24" fill="#cfd3ff" letter-spacing="4">HÖHE · TEIL 2</text>'
        f'<text x="0" y="96" font-family="JetBrains Mono, monospace" font-weight="800" font-size="96" fill="{RED}" filter="url(#glowsoft)">{clock}</text>'
        f'<text x="{len(clock)*58+10}" y="96" font-family="JetBrains Mono, monospace" font-weight="700" font-size="26" fill="{RED}">UHR</text>'
        f'<text x="2" y="140" font-family="JetBrains Mono, monospace" font-weight="700" font-size="22" fill="#8f94c4" letter-spacing="4">{place}</text></g></svg></div>')

# ================= UNTERTITEL (Skill 7 + Format B: Akzent Neon-Gelbgrün) =================
KEY = {"DACHLUKE", "ZUHALTEN", "KRATZT", "FINGERNÄGEL", "HEBEL", "ZENTIMETER", "NOTFALLSTANGE", "STOPPT", "STILLE", "ATEM", "AKKU", "23",
       "LAUTSPRECHER", "ATMET", "LINKEN", "MITTE", "VIBRIERT", "BERGWACHT", "STROM", "WER", "KIPPT", "LINKS", "HÄNGEN", "HANDABDRUCK", "AUSSEN",
       "AUßEN", "HÖHER", "PUNKTE", "BLINZELN", "STIMME", "LICHT", "SEHEN", "TASCHENLAMPE", "DUNKEL", "TEIL", "3", "3:42.", "4:10.", "7."}
DISPLAY = {"dreiundzwanzig": "23", "sieben.": "7.", "drei": "3"}
SKIP = {"zwölf", "zwölf.", "dreißig.", "vierzig.", "Uhr"}


def norm(t):
    return re.sub(r"[^\wÄÖÜäöüß:]", "", t).upper()


words = []
for k, w in enumerate(W):
    nxt2 = " ".join(x["t"] for x in W[k:k+3]).lower()
    if nxt2.startswith("drei uhr zweiundvierzig"): words.append({"t": "3:42.", "s": w["s"], "e": W[k+2]["e"]}); continue
    if nxt2.startswith("vier uhr zehn"): words.append({"t": "4:10.", "s": w["s"], "e": W[k+2]["e"]}); continue
    if k >= 1 and W[k-1]["t"].lower() in ("drei", "vier") and w["t"] == "Uhr": continue
    if k >= 2 and W[k-1]["t"] == "Uhr" and w["t"].lower().rstrip(".") in ("zweiundvierzig", "zehn"): continue
    words.append(dict(w))
# „A M L“ zu einem Wort
merged = []
for w in words:
    if merged and merged[-1]["t"] in ("A", "A M") and w["t"] in ("M", "L."):
        merged[-1] = {"t": merged[-1]["t"] + " " + w["t"], "s": merged[-1]["s"], "e": w["e"]}
    else:
        merged.append(dict(w))
for w in merged:
    if w["t"] == "A M L.":
        w["t"] = "AML."
chunks, cur = [], []
for i, w in enumerate(merged):
    cur.append(w)
    nxt = merged[i+1] if i + 1 < len(merged) else None
    text = " ".join(x["t"] for x in cur)
    if (re.search(r"[.,:?!]$", w["t"]) or len(cur) >= 3 or (nxt and len(text) + 1 + len(nxt["t"]) > 20)
            or (nxt and nxt["s"] - w["e"] > 0.25) or nxt is None):
        chunks.append(cur); cur = []
changed = True
while changed:
    changed = False
    for k in range(len(chunks) - 1):
        if chunks[k+1][0]["s"] - chunks[k][0]["s"] < 0.45:
            m = chunks[k] + chunks[k+1]
            if len(m) <= 4 and len(" ".join(x["t"] for x in m)) <= 24:
                chunks[k:k+2] = [m]; changed = True; break
subs = []
for k, c in enumerate(chunks):
    s = c[0]["s"]
    e = min(chunks[k+1][0]["s"], c[-1]["e"] + 0.6) if k + 1 < len(chunks) else min(TOTAL, c[-1]["e"] + 1.2)
    parts, plain = [], []
    for w in c:
        t = DISPLAY.get(w["t"], w["t"]); plain.append(t)
        parts.append(f'<span class="k">{html.escape(t)}</span>' if norm(w["t"]) in KEY or norm(t) in KEY else html.escape(t))
    fs = min(60, int(760 / (0.56 * max(len(" ".join(plain)), 1))))
    sid = f"sub{k}"
    subs.append(f'<div id="{sid}" class="clip sub" data-start="{s:.3f}" data-duration="{e-s:.3f}" data-track-index="9" style="font-size:{fs}px"><span class="box">{" ".join(parts)}</span></div>')
    tw(f'tl.fromTo("#{sid}",{{y:14,opacity:0}},{{y:0,opacity:1,duration:.16,ease:"power2.out"}},{s:.3f});')


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


danger("ov-d1", t_kratzt, t_rammst)
danger("ov-d2", t_wer, t_410)
danger("ov-d3", t_punkte, t_was)

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
    <title>Höhe Teil 2</title>
    <script src="assets/gsap.min.js"></script>
    <style>
      :root {{ --ground: {SKY1}; --ink: #ffffff; --accent: {LIME}; --font-display: "Poppins", sans-serif; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: var(--ground); }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: var(--font-display); }}
      .scene, .ov {{ position: absolute; inset: 0; }}
      .ov {{ pointer-events: none; }}
      .scene svg {{ display: block; }}
      .sub {{ position: absolute; left: 0; right: 0; top: 1385px; text-align: center; z-index: 20; }}
      .sub .box {{
        display: inline-block; max-width: 820px; padding: 10px 28px 14px; border-radius: 24px;
        background: rgba(8,9,26,.78); box-shadow: 0 6px 24px rgba(0,0,0,.45);
        color: var(--ink); font-weight: 600; line-height: 1.2; white-space: nowrap;
        text-shadow: 0 2px 6px rgba(0,0,0,.5);
      }}
      .sub .k {{ color: var(--accent); }}
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
