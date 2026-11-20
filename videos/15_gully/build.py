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



# ---------- Hintergründe ----------
def sky(stars=True):
    st = "".join(f'<circle cx="{RNG.randint(0,1080)}" cy="{RNG.randint(0,700)}" r="{RNG.choice([1.5,2,2.5,3])}" fill="#fff" opacity="{RNG.uniform(.25,.8):.2f}"/>' for _ in range(60)) if stars else ""
    return (f'<rect width="1080" height="1920" fill="url(#skyg)"/>{st}'
            f'<circle cx="820" cy="330" r="70" fill="{MOON}"/><circle cx="820" cy="330" r="150" fill="url(#moonglow)"/>')


def buildings(gid, y_base=1250, width=2400, far=False):
    out = []
    x = -200
    col = BLD2 if far else BLD
    while x < width:
        w = RNG.randint(170, 300); h = RNG.randint(380, 760) if not far else RNG.randint(500, 900)
        out.append(f'<rect x="{x}" y="{y_base-h}" width="{w}" height="{h}" fill="{col}"/>')
        if not far:
            out.append(f'<rect x="{x}" y="{y_base-h}" width="{w}" height="10" fill="#2a2d63"/>')
        for wy in range(y_base - h + 40, y_base - 80, 70):
            for wx in range(x + 24, x + w - 30, 52):
                if RNG.random() < (0.16 if far else 0.24):
                    out.append(f'<rect x="{wx}" y="{wy}" width="26" height="34" rx="3" fill="{WIN}" opacity="{RNG.uniform(.35,.85):.2f}"/>')
                elif not far:
                    out.append(f'<rect x="{wx}" y="{wy}" width="26" height="34" rx="3" fill="#0d0f26"/>')
        x += w + RNG.randint(4, 30)
    return f'<g id="{gid}">{"".join(out)}</g>'


def lamps(gid, y_base=1290, width=2400, step=520):
    out = []
    for x in range(120, width, step):
        out.append(f'<polygon points="{x+40},{y_base-560} {x+60},{y_base-560} {x+230},{y_base+60} {x-130},{y_base+60}" fill="url(#lampcone)"/>'
                   f'<rect x="{x}" y="{y_base-580}" width="14" height="600" fill="#2a2d55"/>'
                   f'<rect x="{x}" y="{y_base-584}" width="70" height="12" rx="6" fill="#2a2d55"/>'
                   f'<ellipse cx="{x+52}" cy="{y_base-566}" rx="26" ry="10" fill="{LAMP}"/>'
                   f'<ellipse cx="{x+50}" cy="{y_base+40}" rx="150" ry="22" fill="{LAMP}" opacity=".12"/>')
    return f'<g id="{gid}">{"".join(out)}</g>'


def street(prefix, parallax=True):
    """Nachtstraße mit Häusern, Laternen, Gehweg. Gruppen {prefix}-far/-near/-lamps lassen sich verschieben."""
    return (sky()
            + buildings(f"{prefix}-far", 1180, far=True)
            + buildings(f"{prefix}-near", 1270)
            + f'<rect x="0" y="1270" width="1080" height="650" fill="{WALK}"/>'
            + f'<g id="{prefix}-tiles">' + "".join(f'<rect x="{x}" y="1270" width="4" height="250" fill="#1d1e3e"/>' for x in range(-200, 2400, 120)) + '</g>'
            + f'<rect x="0" y="1520" width="1080" height="24" fill="#3a3c6a"/><rect x="0" y="1544" width="1080" height="376" fill="{STREET}"/>'
            + f'<g id="{prefix}-mark">' + "".join(f'<rect x="{x}" y="1720" width="120" height="14" rx="5" fill="#d9dbe8" opacity=".55"/>' for x in range(-200, 2600, 240)) + '</g>'
            + lamps(f"{prefix}-lamps"))


def scroll_street(prefix, t0, t1, speed=1.0):
    d = t1 - t0
    move(f"#{prefix}-far", t0, d, "none", x=int(-60 * d * speed))
    move(f"#{prefix}-near", t0, d, "none", x=int(-140 * d * speed))
    move(f"#{prefix}-lamps", t0, d, "none", x=int(-170 * d * speed))
    move(f"#{prefix}-tiles", t0, d, "none", x=int(-170 * d * speed))
    move(f"#{prefix}-mark", t0, d, "none", x=int(-170 * d * speed))




# ================= CUES =================
t_23 = ws("dreiundzwanzig"); t_allein = ws("allein"); t_gully1 = ws("Gully"); t_pfeift = ws("pfeift")
t_melodie = ws("Melodie"); t_spieluhr = ws("Spieluhr")
t_vibriert = ws("vibriert"); t_warnung = ws("Warnung"); t_achtung = ws("Achtung"); t_strasse = ws("Straße")
t_bestimmt = ws("Bestimmt"); t_weiter = ws("weiter")
t_doch = ws("Doch"); t_hebt = ws("hebt"); t_spalt = ws("Spalt"); t_finger = ws("Finger"); t_asphalt = ws("Asphalt")
t_neue = ws("Neue"); t_regeln = ws("Regeln")
t_r1 = ws("Regel", t_regeln + 0.3); t_tritt = ws("Tritt"); t_r2 = ws("Regel", t_tritt); t_pfeifen = ws("pfeifen"); t_dreh = ws("dreh", t_pfeifen)
t_r3 = ws("Regel", t_dreh); t_licht = ws("Licht", t_r3); t_insl = ws("Ins", t_licht)
t_laeufst = ws("läufst", t_insl); t_laterne2 = ws("Laterne", t_laeufst)
t_dann_aus = ws("Dann", t_laterne2); t_hinter = ws("Hinter", t_dann_aus)
t_ruft = ws("ruft", t_hinter); t_bruder = ws("Bruders"); t_hilf = ws("Hilf"); t_rein = ws("reingefallen")
t_willst = ws("willst"); t_vibr2 = ws("vibriert", t_willst); t_mama = ws("Mama"); t_schlaeft = ws("schläft"); t_geschaut = ws("geschaut")
t_wer = ws("Wer", t_geschaut); t_nur = ws("Nur", t_wer); t_flackert = ws("flackert"); t_direkt = ws("direkt", t_flackert); t_hoert = ws("hört", t_direkt)
t_was = ws("Was", t_hoert); t_rennen = ws("rennen"); t_stehen = ws("stehen", t_rennen); t_teil2 = ws("Teil", t_stehen); t_folge = ws("Folge", t_teil2)

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
    tw(f'tl.fromTo("{sel}",{{opacity:0,y:{dy}}},{{opacity:1,y:0,duration:{dur},ease:"sine.out"}},{t:.3f});')


GULLY = "#2a2c4a"; YEL = "#ffd23f"
PORC = "#d9d2c3"; PORC2 = "#b9b0a0"; COAT = "#6b6a3a"; COAT2 = "#4c5a58"; COAT3 = "#7a5a3a"


def clown(cid, x, y, s=1.0, dark=False):
    """Eigenes Design „Herr Pfiff“: überlang & hager, Flickenmantel (Senf/Graugrün/Braun), rissiges Porzellangesicht
    mit senkrechten schwarzen Tränenstrichen, genähtes breites Grinsen, gelb glimmende Augen, schiefe Zipfelmütze mit
    einer Messingglocke, lange Finger. Kein roter Ballon, keine orangen Haare, keine rote Nase."""
    op = ' opacity=".0"' if False else ""
    body = (f'<path d="M -70 -520 Q -110 -200 -120 0 L -40 0 L -20 -300 L 20 -300 L 40 0 L 120 0 Q 110 -200 70 -520 Z" fill="{COAT2}"/>'
            f'<path d="M -70 -520 L 0 -540 L 70 -520 L 60 -380 L -60 -380 Z" fill="{COAT}"/>'
            f'<rect x="-50" y="-360" width="46" height="60" fill="{COAT3}" transform="rotate(-8 -27 -330)"/><rect x="10" y="-250" width="50" height="70" fill="{COAT}" transform="rotate(6 35 -215)"/>'
            + "".join(f'<path d="M {px} {py} l 10 6" stroke="#2b2a1a" stroke-width="3"/>' for px, py in ((-46, -356), (-10, -300), (12, -246), (56, -184)))
            + f'<path d="M -70 -500 Q -170 -420 -190 -250 Q -196 -200 -180 -170" stroke="{COAT2}" stroke-width="44" fill="none" stroke-linecap="round"/>'
            f'<path d="M 70 -500 Q 170 -420 190 -250 Q 196 -200 180 -170" stroke="{COAT2}" stroke-width="44" fill="none" stroke-linecap="round"/>'
            + "".join(f'<path d="M {sx*180} -170 q {sx*(6+k*4)} 50 {sx*(2+k*6)} {90+k*8}" stroke="{PORC2}" stroke-width="9" fill="none" stroke-linecap="round"/>' for sx in (-1, 1) for k in range(4))
            + f'<path d="M -60 -560 Q -80 -500 -54 -470 L 54 -470 Q 80 -500 60 -560 Z" fill="#e9e3d6"/>'
            + "".join(f'<path d="M {-60+k*24} -560 l 12 34 l 12 -34" fill="#cfc6b4"/>' for k in range(5)))
    head = (f'<g id="{cid}-head"><ellipse cx="0" cy="-660" rx="74" ry="98" fill="{PORC}"/>'
            f'<path d="M 30 -740 l -16 40 l 22 26 l -10 30" stroke="#8a8270" stroke-width="3" fill="none"/>'
            f'<path d="M -90 -720 Q -40 -830 40 -800 Q 120 -780 150 -860 Q 140 -760 90 -720 Z" fill="{COAT}"/>'
            f'<path d="M 150 -860 Q 175 -880 180 -850" stroke="{COAT}" stroke-width="10" fill="none"/><circle cx="182" cy="-842" r="16" fill="#c9a24a"/><circle cx="178" cy="-846" r="5" fill="#fff3c0"/>'
            f'<path d="M -78 -725 Q 0 -700 90 -725" stroke="{COAT3}" stroke-width="16" fill="none"/>'
            f'<g id="{cid}-eyes"><ellipse cx="-30" cy="-668" rx="20" ry="14" fill="#0b0b10"/><ellipse cx="30" cy="-668" rx="20" ry="14" fill="#0b0b10"/>'
            f'<circle cx="-30" cy="-668" r="7" fill="{YEL}"/><circle cx="30" cy="-668" r="7" fill="{YEL}"/>'
            f'<circle cx="-30" cy="-668" r="34" fill="url(#yelglow)"/><circle cx="30" cy="-668" r="34" fill="url(#yelglow)"/></g>'
            f'<path d="M -30 -650 L -30 -600 M 30 -650 L 30 -600" stroke="#141414" stroke-width="5"/>'
            f'<path d="M -50 -612 Q 0 -585 50 -612" stroke="#5a1f22" stroke-width="7" fill="none"/>'
            + "".join(f'<path d="M {-46+k*13} -618 l 0 16" stroke="#141414" stroke-width="3"/>' for k in range(8))
            + f'<path d="M -50 -612 Q -66 -630 -60 -650 M 50 -612 Q 66 -630 60 -650" stroke="#5a1f22" stroke-width="5" fill="none"/></g>')
    shade = f'<rect x="-200" y="-880" width="400" height="900" fill="#05061a" opacity="{.55 if dark else .15}"/>'
    return f'<g id="{cid}"><g transform="translate({x},{y}) scale({s})">{body}{head}{shade}</g></g>'


def manhole(mid, cx, cy, rx=120, ry=36):
    return (f'<g id="{mid}"><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{GULLY}" stroke="#3c3f68" stroke-width="6"/>'
            + "".join(f'<line x1="{cx-rx*0.7+k*rx*0.28:.0f}" y1="{cy-ry*0.6:.0f}" x2="{cx-rx*0.7+k*rx*0.28:.0f}" y2="{cy+ry*0.6:.0f}" stroke="#15162e" stroke-width="5"/>' for k in range(6))
            + '</g>')


def notes(nid, x, y, n=4):
    return "".join(f'<text id="{nid}{i}" x="{x+i*26}" y="{y}" font-family="Poppins" font-weight="700" font-size="{44+i*6}" fill="#e8e3ff" opacity="0">{"♪" if i%2==0 else "♫"}</text>' for i in range(n))


def float_notes(nid, t0, n=4, rep=2):
    for i in range(n):
        tw(f'tl.fromTo("#{nid}{i}",{{opacity:0,x:0,y:0}},{{opacity:.8,x:{(-1)**i*60},y:-260,duration:2.2,ease:"sine.out",repeat:{rep},repeatDelay:.4}},{t0 + i*0.45:.3f});')


def street_lamps(prefix, xs, y_base=1290):
    out = []
    for k, x in enumerate(xs):
        out.append(f'<g id="{prefix}-l{k}"><g id="{prefix}-c{k}"><polygon points="{x+40},{y_base-560} {x+60},{y_base-560} {x+230},{y_base+60} {x-130},{y_base+60}" fill="url(#lampcone)"/>'
                   f'<ellipse cx="{x+50}" cy="{y_base+40}" rx="150" ry="22" fill="{LAMP}" opacity=".14"/></g>'
                   f'<rect x="{x}" y="{y_base-580}" width="14" height="600" fill="#2a2d55"/><rect x="{x}" y="{y_base-584}" width="70" height="12" rx="6" fill="#2a2d55"/>'
                   f'<ellipse id="{prefix}-b{k}" cx="{x+52}" cy="{y_base-566}" rx="26" ry="10" fill="{LAMP}"/></g>')
    return "".join(out)


def street_static(prefix, lamp_xs=(), extra=""):
    return (sky() + buildings(f"{prefix}-far", 1180, far=True) + buildings(f"{prefix}-near", 1270)
            + f'<rect x="0" y="1270" width="1080" height="650" fill="{WALK}"/>'
            + "".join(f'<rect x="{x}" y="1270" width="4" height="250" fill="#1d1e3e"/>' for x in range(0, 1080, 120))
            + f'<rect x="0" y="1520" width="1080" height="24" fill="#3a3c6a"/><rect x="0" y="1544" width="1080" height="376" fill="{STREET}"/>'
            + "".join(f'<rect x="{x}" y="1720" width="120" height="14" rx="5" fill="#d9dbe8" opacity=".55"/>' for x in range(0, 1080, 240))
            + extra + street_lamps(f"{prefix}", lamp_xs))


# A Hook: 23:58, allein nach Hause – aus dem Gully pfeift jemand
S0, S1 = 0.0, t_melodie
scene("sa", S0, S1, street("sa") + manhole("sa-m", 760, 1320, 110, 30) + notes("sa-n", 740, 1290) + figure("sa-fig", 420, 1500, 1.0, eyes="n"), drift=False)
walk_cycle("sa-fig", 0, t_pfeift + 0.1); scroll_street("sa", 0, t_pfeift + 0.1, 1.0)
tw(f'tl.to("#sa-m",{{x:-200,duration:{t_pfeift + 0.1:.3f},ease:"none"}},0);')
tw(f'tl.set("#sa-fig-eyes-n",{{opacity:0}},{t_pfeift:.3f});'); tw(f'tl.set("#sa-fig-eyes-w",{{opacity:1}},{t_pfeift:.3f});')
float_notes("sa-n", t_pfeift, 4, 1)
tw(f'tl.set("#sa-n0, #sa-n1, #sa-n2, #sa-n3",{{x:-200}},{t_pfeift + 0.1:.3f});')

# B Gullydeckel von oben: Melodie wie aus einer Spieluhr
S0, S1 = t_melodie, t_vibriert
grate = (f'<rect width="1080" height="1920" fill="{STREET}"/>' + "".join(f'<rect x="{x}" y="0" width="2" height="1920" fill="#22234a" opacity=".6"/>' for x in range(0, 1080, 90))
         + f'<circle cx="540" cy="900" r="360" fill="#3c3f68"/><circle cx="540" cy="900" r="330" fill="{GULLY}"/>'
         + "".join(f'<rect x="{300+k*70}" y="640" width="34" height="520" rx="12" fill="#07081a"/>' for k in range(7))
         + f'<g id="sb-glint" opacity="0"><circle cx="505" cy="930" r="8" fill="{YEL}"/><circle cx="575" cy="930" r="8" fill="{YEL}"/>'
           f'<circle cx="505" cy="930" r="30" fill="url(#yelglow)"/><circle cx="575" cy="930" r="30" fill="url(#yelglow)"/></g>'
         + notes("sb-n", 470, 820, 5))
scene("sb", S0, S1, grate, drift=False)
float_notes("sb-n", S0 + 0.1, 5, 2)
tw(f'tl.fromTo("#sb-glint",{{opacity:0}},{{opacity:.9,duration:.8,ease:"sine.inOut",yoyo:true,repeat:1}},{t_spieluhr:.3f});')
tw(f'tl.fromTo("#sb-cam",{{scale:1,svgOrigin:"540 900"}},{{scale:1.18,svgOrigin:"540 900",duration:{S1-S0+0.3:.3f},ease:"sine.inOut"}},{S0:.3f});')

# C Warnung auf dem Sperrbildschirm (fiktiver Absender)
S0, S1 = t_vibriert, t_bestimmt
lock = (f'<text x="0" y="-380" text-anchor="middle" font-family="Poppins" font-weight="600" font-size="34" fill="#cfd3ff">Freitag, 20. November</text>'
        f'<text x="0" y="-250" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="170" fill="#fff">23:58</text>'
        f'<g id="sc-n" opacity="0"><g transform="translate(0,260)"><rect x="-260" y="-170" width="520" height="270" rx="34" fill="#2a1420" stroke="{RED}" stroke-width="5"/>'
        f'<text x="-230" y="-120" font-family="Poppins" font-weight="800" font-size="28" fill="{RED}">⚠ STADTWERKE NORDHAFEN</text>'
        f'<text x="-230" y="-70" font-family="Poppins" font-weight="700" font-size="32" fill="#fff">Achtung. Bleiben Sie</text>'
        f'<text x="-230" y="-28" font-family="Poppins" font-weight="700" font-size="32" fill="#fff">heute Nacht nicht</text>'
        f'<text x="-230" y="14" font-family="Poppins" font-weight="700" font-size="32" fill="#fff">auf der Straße.</text>'
        f'<text x="-230" y="62" font-family="Poppins" font-weight="500" font-size="22" fill="#9aa0d0">Warnsystem · jetzt</text></g></g>')
scene("sc", S0, S1, street_static("sc") + f'<rect width="1080" height="1920" fill="#000" opacity=".55"/>' + phone("sc-ph", lock, 540, 1000, 0.86))
tw(f'tl.fromTo("#sc-ph",{{y:200,opacity:0}},{{y:0,opacity:1,duration:.5,ease:"sine.out"}},{S0:.3f});')
fadein("#sc-n", t_warnung - 0.1, 0.5, 20)

# D Fehlalarm – du gehst weiter
S0, S1 = t_bestimmt, t_doch
scene("sd", S0, S1, street("sd") + figure("sd-fig", 540, 1500, 1.0, eyes="n"), drift=False)
walk_cycle("sd-fig", S0, S1 + 0.3); scroll_street("sd", S0, S1 + 0.3, 1.0)

# E Ein Gullydeckel hebt sich – lange, dünne Finger tasten über den Asphalt
S0, S1 = t_doch, t_neue
fingers = (f'<g id="se-fing" opacity="0">' + "".join(
    f'<path id="se-f{k}" d="M {420+k*30} {1462+k*3} Q {330+k*24} {1430-k*8} {250+k*30} {1470+k*6} Q {200+k*30} {1500+k*6} {170+k*34} {1478+k*8}" stroke="{PORC}" stroke-width="13" fill="none" stroke-linecap="round"/>'
    f'<circle cx="{170+k*34}" cy="{1478+k*8}" r="7" fill="#8a8270"/>' for k in range(4))
    + '</g>')
scene("se", S0, S1, f'<rect width="1080" height="1920" fill="{STREET}"/><g transform="translate(0,-380)">' + street_static("se", (880,)) + f'<rect width="1080" height="1920" fill="#000" opacity=".25"/>'
      + f'<ellipse cx="540" cy="1460" rx="200" ry="52" fill="#000"/>' + fingers
      + f'<g id="se-lid"><ellipse cx="540" cy="1450" rx="200" ry="56" fill="{GULLY}" stroke="#3c3f68" stroke-width="8"/>'
        + "".join(f'<line x1="{420+k*48}" y1="1420" x2="{420+k*48}" y2="1480" stroke="#15162e" stroke-width="6"/>' for k in range(6)) + '</g>'
      + f'<g id="se-eyes" opacity="0"><circle cx="520" cy="1478" r="6" fill="{YEL}"/><circle cx="560" cy="1478" r="6" fill="{YEL}"/></g></g>', drift=False)
tw(f'tl.to("#se-lid",{{y:-40,rotation:-6,svgOrigin:"740 1450",duration:1.2,ease:"sine.inOut"}},{t_hebt:.3f});')
tw(f'tl.fromTo("#se-eyes",{{opacity:0}},{{opacity:.9,duration:.6}},{t_spalt:.3f});')
tw(f'tl.fromTo("#se-fing",{{opacity:0,x:60}},{{opacity:1,x:0,duration:1.6,ease:"sine.inOut"}},{t_finger - 0.2:.3f});')
for k in range(4):
    tw(f'tl.to("#se-f{k}",{{x:-30,duration:.7,yoyo:true,repeat:2,ease:"sine.inOut"}},{t_finger + 0.4 + k*0.12:.3f});')
tw(f'tl.fromTo("#se-cam",{{scale:1,svgOrigin:"540 1070"}},{{scale:1.3,svgOrigin:"540 1070",duration:{S1-S0+0.3:.3f},ease:"sine.inOut"}},{S0:.3f});')

# F „Drei Regeln“
S0, S1 = t_neue, t_r1
msg = (f'<rect x="-280" y="-580" width="560" height="150" fill="#2a1420"/><text x="-240" y="-480" font-family="Poppins" font-weight="800" font-size="30" fill="{RED}">⚠ STADTWERKE NORDHAFEN</text>'
       f'<g id="sf-m" opacity="0"><rect x="-250" y="-340" width="480" height="150" rx="26" fill="#262a5e" stroke="{RED}" stroke-width="4"/>'
       f'<text x="-225" y="-280" font-family="Poppins" font-weight="700" font-size="32" fill="#fff">Hören Sie genau zu.</text>'
       f'<text x="-225" y="-228" font-family="Poppins" font-weight="800" font-size="36" fill="{LIME}">Drei Regeln.</text></g>')
scene("sf", S0, S1, f'<rect width="1080" height="1920" fill="#0c0d22"/><circle cx="540" cy="900" r="600" fill="url(#cardglow)"/>' + phone("sf-ph", msg))
fadein("#sf-m", t_neue + 0.2, 0.5, 20)


def rule_card(sid, n, head, sub, icon):
    return (card_bg(sid)
            + f'<g id="{sid}-badge" opacity="0"><rect x="430" y="370" width="220" height="62" rx="12" fill="{RED}"/>'
              f'<text x="540" y="415" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="34" fill="#fff">REGEL #{n}</text></g>'
            + f'<g id="{sid}-head" opacity="0"><text x="540" y="540" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="74" fill="#fff">{head}</text></g>'
            + f'<g id="{sid}-sub" opacity="0"><text x="540" y="615" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="44" fill="{LIME}">{sub}</text></g>'
            + icon)


def rule_in(sid, t0, t_sub):
    fadein(f"#{sid}-badge", t0 + 0.05); fadein(f"#{sid}-head", t0 + 0.25); fadein(f"#{sid}-sub", t_sub)


# R1 Tritt niemals auf einen Gullydeckel
S0, S1 = t_r1, t_r2
shoe = f'<g id="r1-shoe"><rect x="600" y="820" width="200" height="90" rx="40" fill="#eef0f3"/><rect x="600" y="880" width="210" height="30" rx="12" fill="#cfd3da"/><rect x="640" y="700" width="80" height="140" rx="20" fill="#2c3a52"/></g>'
icon1 = manhole("r1-m", 540, 1050, 260, 90) + shoe
scene("r1", S0, S1, rule_card("r1", 1, "NIE AUF EINEN GULLY", "Kein einziger Schritt", icon1) + xmark("r1-x", 540, 1000, 110))
rule_in("r1", S0, t_tritt + 0.2)
tw(f'tl.fromTo("#r1-shoe",{{x:200,y:-120}},{{x:-60,y:60,duration:.8,ease:"sine.inOut"}},{t_tritt:.3f});')
tw(f'tl.fromTo("#r1-x",{{opacity:0}},{{opacity:1,duration:.3,ease:"sine.out"}},{t_tritt + 0.7:.3f});')
tw(f'tl.to("#r1-shoe",{{x:200,y:-120,duration:.6,ease:"sine.inOut"}},{t_tritt + 1.0:.3f});')

# R2 Wenn er pfeift: dreh dich nicht um
S0, S1 = t_r2, t_r3
icon2 = (f'<g transform="translate(540,1120)"><circle cx="0" cy="-200" r="120" fill="{FIG}"/><path d="M -120 -220 Q -120 -330 0 -330 Q 120 -330 120 -220 Q 90 -280 0 -285 Q -90 -280 -120 -220 Z" fill="{HAIR}"/>'
         f'<rect x="-130" y="-80" width="260" height="240" rx="60" fill="#2f6f73"/></g>'
         f'<path id="r2-arr" d="M 760 900 A 240 120 0 1 1 330 900" stroke="#fff" stroke-width="12" fill="none" opacity=".8"/><polygon points="310,870 330,930 360,880" fill="#fff"/>'
         + notes("r2-n", 820, 820, 3))
scene("r2", S0, S1, rule_card("r2", 2, "DREH DICH NICHT UM", "wenn du ihn pfeifen hörst", icon2) + xmark("r2-x", 540, 900, 110))
rule_in("r2", S0, t_pfeifen - 0.3)
float_notes("r2-n", t_pfeifen - 0.2, 3, 1)
tw(f'tl.fromTo("#r2-x",{{opacity:0}},{{opacity:1,duration:.3,ease:"sine.out"}},{t_dreh + 0.1:.3f});')

# R3 Bleib im Licht der Laternen
S0, S1 = t_r3, t_laeufst
icon3 = (f'<polygon points="560,740 590,740 760,1260 380,1260" fill="url(#lampcone)" opacity="1"/><rect x="520" y="700" width="16" height="560" fill="#2a2d55"/>'
         f'<rect x="520" y="696" width="80" height="14" rx="7" fill="#2a2d55"/><ellipse cx="580" cy="716" rx="30" ry="11" fill="{LAMP}"/>'
         + figure("r3-f", 580, 1250, 0.6, eyes="n")
         + f'<g id="r3-ok" opacity="0"><circle cx="860" cy="1000" r="60" fill="{LIME}"/><path d="M 830 1000 l 22 22 l 40 -44" stroke="#0b0d22" stroke-width="12" fill="none"/></g>'
         + f'<g id="r3-sh" opacity="0"><ellipse cx="200" cy="1100" rx="60" ry="170" fill="#05061a"/><circle cx="185" cy="980" r="6" fill="{YEL}"/><circle cx="215" cy="980" r="6" fill="{YEL}"/></g>')
scene("r3", S0, S1, rule_card("r3", 3, "BLEIB IM LICHT", "Ins Licht kommt er nicht", icon3))
rule_in("r3", S0, t_insl - 0.2)
fadein("#r3-sh", t_insl, 0.8, 0); fadein("#r3-ok", t_insl + 0.6, 0.4, 0)

# G Du läufst – von Laterne zu Laterne
S0, S1 = t_laeufst, t_dann_aus
scene("sg", S0, S1, street("sg") + figure("sg-fig", 540, 1500, 1.0, eyes="f"), drift=False)
walk_cycle("sg-fig", S0, S1 + 0.3, period=0.38, bob=12); scroll_street("sg", S0, S1 + 0.3, 1.8)

# H Die Laternen gehen aus – eine nach der anderen, hinter dir
S0, S1 = t_dann_aus, t_ruft
LX = (40, 300, 560, 820)
scene("sh", S0, S1, street_static("sh", LX) + f'<rect id="sh-dark" width="1080" height="1920" fill="#02030c" opacity="0"/>'
      + figure("sh-fig", 900, 1500, 1.0, eyes="w"), drift=False)
for k in range(3):
    t0 = t_dann_aus + 0.5 + k * 0.7
    tw(f'tl.to("#sh-c{k}, #sh-b{k}",{{opacity:.2,duration:.08,yoyo:true,repeat:3}},{t0:.3f});')
    tw(f'tl.to("#sh-c{k}, #sh-b{k}",{{opacity:0,duration:.2}},{t0 + 0.35:.3f});')
    tw(f'tl.to("#sh-dark",{{opacity:{0.15 + k*0.15:.2f},duration:.4}},{t0 + 0.35:.3f});')

# I Aus dem Gully ruft die Stimme deines kleinen Bruders
S0, S1 = t_ruft, t_willst
small_hand = (f'<g id="si-hand" opacity="0"><rect x="565" y="880" width="30" height="110" rx="14" fill="#e2a982"/>'
              + "".join(f'<rect x="{560+k*11}" y="{830+abs(k-1.5)*6:.0f}" width="10" height="60" rx="5" fill="#e2a982"/>' for k in range(4)) + '</g>')
scene("si", S0, S1, grate.replace('id="sb-', 'id="si-').replace('id="sb-n', 'id="si-n') + small_hand
      + quote("si-q", ["„Hilf mir!", "Ich bin reingefallen!“"], y=520, col="#ff8a8a", label_txt="– AUS DEM GULLY –").replace('y="380"', 'y="430"'), drift=False)
fadein("#si-q-lab", t_bruder - 0.2); fadein("#si-q-0", t_hilf); fadein("#si-q-1", t_rein)
tw(f'tl.fromTo("#si-hand",{{opacity:0,y:80}},{{opacity:1,y:0,duration:.8,ease:"sine.out"}},{t_hilf:.3f});')
tw(f'tl.to("#si-hand",{{x:10,duration:.25,yoyo:true,repeat:5,ease:"sine.inOut"}},{t_hilf + 0.8:.3f});')
tw(f'tl.fromTo("#si-cam",{{scale:1,svgOrigin:"540 900"}},{{scale:1.15,svgOrigin:"540 900",duration:{S1-S0+0.3:.3f},ease:"sine.inOut"}},{S0:.3f});')

# J Mama: „Dein Bruder schläft.“
S0, S1 = t_willst, t_wer
chat = (f'<rect x="-280" y="-580" width="560" height="150" rx="0" fill="#1a1d47"/><circle cx="-200" cy="-490" r="36" fill="#e98fb0"/>'
        f'<text x="-200" y="-478" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="30" fill="#fff">M</text>'
        f'<text x="-140" y="-480" font-family="Poppins" font-weight="700" font-size="36" fill="#fff">Mama ♥</text>'
        f'<text x="0" y="-370" text-anchor="middle" font-family="Poppins" font-weight="600" font-size="24" fill="#8f94c4">Heute 21:40</text>'
        f'<rect x="-250" y="-340" width="420" height="80" rx="26" fill="#262a5e"/><text x="-225" y="-290" font-family="Poppins" font-weight="600" font-size="28" fill="#fff">Komm nicht zu spät!</text>'
        f'<g id="sj-new" opacity="0"><text x="0" y="-190" text-anchor="middle" font-family="Poppins" font-weight="600" font-size="24" fill="#8f94c4">Heute 00:07</text>'
        f'<rect x="-250" y="-160" width="480" height="170" rx="26" fill="#262a5e" stroke="{LIME}" stroke-width="4"/>'
        f'<text x="-225" y="-106" font-family="Poppins" font-weight="700" font-size="30" fill="#fff">Dein Bruder schläft.</text>'
        f'<text x="-225" y="-62" font-family="Poppins" font-weight="700" font-size="30" fill="#fff">Ich habe gerade</text>'
        f'<text x="-225" y="-18" font-family="Poppins" font-weight="700" font-size="30" fill="{LIME}">nach ihm geschaut.</text></g>')
scene("sj", S0, S1, street_static("sj") + f'<rect width="1080" height="1920" fill="#000" opacity=".6"/>' + phone("sj-ph", chat))
tw(f'tl.fromTo("#sj-ph",{{y:160,opacity:0}},{{y:0,opacity:1,duration:.5,ease:"sine.out"}},{t_vibr2 - 0.2:.3f});')
fadein("#sj-new", t_mama, 0.5, 24)

# K Wer ruft dann nach dir? – im Dunkeln hinter dir: Herr Pfiff
S0, S1 = t_wer, t_nur
scene("sk", S0, S1, street_static("sk") + f'<rect width="1080" height="1920" fill="#02030c" opacity=".7"/>'
      + clown("sk-cl", 330, 1520, 1.1, dark=True) + f'<rect width="1080" height="1920" fill="url(#vig)"/>', drift=False)
tw(f'tl.fromTo("#sk-cl",{{opacity:0}},{{opacity:1,duration:1.6,ease:"sine.in"}},{S0 + 0.2:.3f});')
tw(f'tl.fromTo("#sk-cam",{{scale:1,svgOrigin:"330 800"}},{{scale:1.25,svgOrigin:"330 800",duration:{S1-S0+0.3:.3f},ease:"sine.in"}},{S0:.3f});')

# L Letzte Laterne vor der Haustür flackert – direkt hinter dir hört das Pfeifen auf
S0, S1 = t_nur, t_was
house = (f'<rect x="760" y="900" width="320" height="620" fill="#232650"/><rect x="840" y="1220" width="120" height="300" rx="10" fill="#5a3a24"/>'
         f'<circle cx="940" cy="1370" r="7" fill="{GOLD if "GOLD" in globals() else "#e9c46a"}"/><rect x="800" y="980" width="90" height="110" rx="6" fill="{WIN}" opacity=".85"/>'
         f'<rect x="940" y="980" width="90" height="110" rx="6" fill="#0d0f26"/>')
scene("sl", S0, S1, street_static("sl", (500,), extra=house) + f'<rect width="1080" height="1920" fill="#02030c" opacity=".35"/>'
      + clown("sl-cl", 380, 1530, 1.0, dark=True) + figure("sl-fig", 590, 1500, 1.0, eyes="w") + notes("sl-n", 340, 820, 3), drift=False)
tw(f'tl.set("#sl-cl",{{opacity:0}},{S0:.3f});')
for k in range(5):
    tw(f'tl.to("#sl-c0, #sl-b0",{{opacity:.25,duration:.07,yoyo:true,repeat:1}},{t_flackert + k*0.55:.3f});')
float_notes("sl-n", S0, 3, 1)
tw(f'tl.to("#sl-n0, #sl-n1, #sl-n2",{{opacity:0,duration:.2}},{t_hoert:.3f});')
tw(f'tl.to("#sl-cl",{{opacity:1,duration:1.4,ease:"sine.in"}},{t_direkt - 0.4:.3f});')
tw(f'tl.fromTo("#sl-cam",{{scale:1,svgOrigin:"520 1100"}},{{scale:1.2,svgOrigin:"520 1100",duration:{S1-S0+0.3:.3f},ease:"sine.inOut"}},{S0:.3f});')


# M Wahl als Abstimmung
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


icon_a = (f'<rect x="230" y="730" width="120" height="180" rx="8" fill="#5a3a24"/><circle cx="330" cy="825" r="7" fill="#e9c46a"/>'
          + "".join(f'<path d="M {170-k*22} {790+k*30} l -40 0" stroke="#fff" stroke-width="6" stroke-linecap="round" opacity=".7"/>' for k in range(3)))
icon_b = (f'<polygon points="790,740 810,740 880,920 720,920" fill="url(#lampcone)"/><rect x="772" y="720" width="10" height="200" fill="#9aa0c8"/>'
          f'<ellipse cx="800" cy="736" rx="22" ry="8" fill="{LAMP}"/>')
ring_len = 2 * math.pi * 70
finger_tap = (f'<g id="sm-tap"><g transform="translate(540,1200)"><circle id="sm-ripple" cx="0" cy="-40" r="30" fill="none" stroke="#fff" stroke-width="5" opacity="0"/>'
              f'<rect x="-14" y="-40" width="28" height="80" rx="14" fill="{FIG}"/><rect x="-34" y="10" width="68" height="80" rx="26" fill="{FIG}"/>'
              f'<rect x="-34" y="70" width="68" height="40" rx="12" fill="#2f6f73"/></g></g>')
scene("sm", S0, S1, street_static("sm", (500,)) + f'<rect width="1080" height="1920" fill="#05061a" opacity=".75"/>'
      + f'<g id="sm-badge" opacity="0"><rect x="370" y="390" width="340" height="60" rx="30" fill="{LIME}"/>'
        f'<text x="540" y="432" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="30" fill="#0b0d22" letter-spacing="3">DU ENTSCHEIDEST</text></g>'
      + f'<g id="sm-q" opacity="0"><text x="540" y="560" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="74" fill="#fff">Was machst du?</text></g>'
      + vote_card("sm-a", 70, RED, "A", "ZUR HAUSTÜR", "RENNEN", icon_a) + vote_card("sm-b", 590, BLUE, "B", "IM LICHT", "STEHEN BLEIBEN", icon_b)
      + f'<g id="sm-or" opacity="0"><circle cx="540" cy="860" r="70" fill="#0b0d22" stroke="#33376e" stroke-width="10"/>'
        f'<circle id="sm-ring" cx="540" cy="860" r="70" fill="none" stroke="{LIME}" stroke-width="10" stroke-dasharray="{ring_len:.1f}" stroke-dashoffset="0" transform="rotate(-90 540 860)"/>'
        f'<text x="540" y="876" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="44" fill="#fff">ODER</text></g>'
      + finger_tap
      + f'<g id="sm-cta" opacity="0"><rect x="250" y="1215" width="580" height="80" rx="40" fill="#fff"/>'
        f'<text x="540" y="1268" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="36" fill="#0b0d22">💬 Schreib A oder B</text></g>', drift=False)
fadein("#sm-badge", S0, 0.35, -20); fadein("#sm-q", S0 + 0.1)
tw(f'tl.fromTo("#sm-a",{{opacity:0,x:-260}},{{opacity:1,x:0,duration:.5,ease:"power2.out"}},{t_rennen - 0.6:.3f});')
tw(f'tl.fromTo("#sm-b",{{opacity:0,x:260}},{{opacity:1,x:0,duration:.5,ease:"power2.out"}},{t_stehen - 0.6:.3f});')
fadein("#sm-or", t_rennen, 0.4, 0)
tw(f'tl.fromTo("#sm-ring",{{attr:{{"stroke-dashoffset":0}}}},{{attr:{{"stroke-dashoffset":{ring_len:.1f}}},duration:{max(1.0, S1 - t_rennen):.3f},ease:"none"}},{t_rennen:.3f});')
tw(f'tl.set("#sm-a-bar, #sm-b-bar",{{scaleX:0,transformOrigin:"0% 50%"}},{S0:.3f});')
va = [0.38, 0.61, 0.47, 0.56, 0.52]; t_v = t_rennen + 0.2
for k, a in enumerate(va):
    tv = t_v + k * max(0.35, (S1 - t_v) / len(va))
    tw(f'tl.to("#sm-a-bar",{{scaleX:{a},duration:.35,ease:"power2.out"}},{tv:.3f});')
    tw(f'tl.to("#sm-b-bar",{{scaleX:{1-a:.2f},duration:.35,ease:"power2.out"}},{tv:.3f});')
tw(f'tl.set("#sm-tap",{{opacity:0}},{S0:.3f});')
tw(f'tl.fromTo("#sm-tap",{{opacity:0,y:200}},{{opacity:1,y:0,duration:.4,ease:"sine.out"}},{t_rennen:.3f});')
seq = [(-260, "a"), (260, "b"), (-260, "a"), (260, "b")]
step = max(0.45, (S1 - t_rennen - 0.4) / len(seq))
for k, (dx, c) in enumerate(seq):
    tk = t_rennen + 0.3 + k * step
    tw(f'tl.to("#sm-tap",{{x:{dx},y:-60,duration:{step*0.5:.3f},ease:"power2.inOut"}},{tk:.3f});')
    tw(f'tl.fromTo("#sm-ripple",{{opacity:.9,scale:.5,transformOrigin:"50% 50%"}},{{opacity:0,scale:2.2,duration:.4,ease:"power1.out"}},{tk + step*0.5:.3f});')
    tw(f'tl.fromTo("#sm-{c}-hl",{{opacity:.35}},{{opacity:0,duration:.45,ease:"sine.out"}},{tk + step*0.5:.3f});')
fadein("#sm-cta", max(t_stehen, S1 - 1.2), 0.35, 30)

# N Teil-2-Karte
S0, S1 = t_folge - 0.3, TOTAL
fog = "".join(f'<ellipse id="sn-f{i}" cx="{RNG.randint(0,1080)}" cy="{RNG.randint(300,1700)}" rx="{RNG.randint(300,520)}" ry="{RNG.randint(90,170)}" fill="#8a8fb8" opacity=".09"/>' for i in range(10))
scene("sn", S0, S1, f'<rect width="1080" height="1920" fill="#14152e"/>{fog}' + manhole("sn-m", 540, 1150, 220, 66)
      + f'<g id="sn-e"><circle cx="515" cy="1150" r="7" fill="{YEL}"/><circle cx="565" cy="1150" r="7" fill="{YEL}"/></g>'
      + f'<text x="540" y="450" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="36" fill="#cfd3ff" letter-spacing="14">GULLY</text>'
      + f'<g id="sn-t" opacity="0"><text x="540" y="680" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="230" fill="{RED}" filter="url(#glow)">TEIL 2</text></g>'
      + f'<g id="sn-s" opacity="0"><text x="540" y="850" text-anchor="middle" font-family="Poppins" font-weight="600" font-size="44" fill="#fff">heute Nacht · 23:58 Uhr</text></g>'
      + f'<g id="sn-b" opacity="0"><rect x="330" y="1560" width="420" height="80" rx="40" fill="none" stroke="#fff" stroke-width="5"/>'
        f'<text x="540" y="1613" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="34" fill="#fff" letter-spacing="3">FOLGE FÜR TEIL 2</text></g>')
fadein("#sn-t", S0 + 0.1, 0.6, 0); fadein("#sn-s", S0 + 0.4); fadein("#sn-b", S0 + 0.9)
tw(f'tl.to("#sn-e",{{opacity:.2,duration:.15,yoyo:true,repeat:1}},{S0 + 1.6:.3f});')
for i in range(10):
    tw(f'tl.fromTo("#sn-f{i}",{{x:0}},{{x:{RNG.choice([-1,1])*RNG.randint(80,200)},duration:{S1-S0:.3f},ease:"sine.inOut"}},{S0:.3f});')

# ================= SERIEN-BRANDING OBEN LINKS (Format B) =================
BRAND = [  # (start, ende, uhrzeit, ort)
    (0.0, t_vibriert, "23:58", "HAUPTSTRASSE"), (t_vibriert, t_doch, "23:59", "HANDY"), (t_doch, t_neue, "00:01", "GULLY"),
    (t_neue, t_laeufst, "00:02", "REGELN"), (t_laeufst, t_ruft, "00:04", "LATERNEN"), (t_ruft, t_willst, "00:06", "GULLY"),
    (t_willst, t_wer, "00:07", "HANDY"), (t_wer, t_teil2, "00:08", "LETZTE LATERNE"),
]
BRAND = [(a, b if i + 1 >= len(BRAND) or BRAND[i+1][0] >= b else BRAND[i+1][0], c, d) for i, (a, b, c, d) in enumerate(BRAND)]
brand_html = []
for i, (a, b, clock, place) in enumerate(BRAND):
    brand_html.append(
        f'<div id="br{i}" class="clip ov" data-start="{a:.3f}" data-duration="{b-a:.3f}" data-track-index="7" style="z-index:12">'
        f'<svg viewBox="0 0 1080 1920" width="1080" height="1920"><rect x="40" y="150" width="400" height="200" rx="24" fill="#0b0d22" opacity=".55"/><g transform="translate(70,190)">'
        f'<circle cx="8" cy="-6" r="8" fill="{RED}"/><text x="26" y="2" font-family="JetBrains Mono, monospace" font-weight="700" font-size="24" fill="#cfd3ff" letter-spacing="4">GULLY · TEIL 1</text>'
        f'<text x="0" y="96" font-family="JetBrains Mono, monospace" font-weight="800" font-size="96" fill="{RED}" filter="url(#glowsoft)">{clock}</text>'
        f'<text x="{len(clock)*58+10}" y="96" font-family="JetBrains Mono, monospace" font-weight="700" font-size="26" fill="{RED}">UHR</text>'
        f'<text x="2" y="140" font-family="JetBrains Mono, monospace" font-weight="700" font-size="22" fill="#8f94c4" letter-spacing="4">{place}</text></g></svg></div>')

# ================= UNTERTITEL (Skill 7 + Format B: Akzent Neon-Gelbgrün) =================
KEY = {"23:58.", "ALLEIN", "GULLY", "PFEIFT", "MELODIE", "SPIELUHR", "VIBRIERT", "WARNUNG", "STRASSE", "STRAßE", "FEHLALARM", "GULLYDECKEL",
       "SPALT", "FINGER", "ASPHALT", "DREI", "REGELN", "NIEMALS", "PFEIFEN", "UM", "LICHT", "LATERNEN", "LATERNE", "AUS", "HINTER", "BRUDERS",
       "HILF", "REINGEFALLEN", "MAMA", "SCHLÄFT", "WER", "FLACKERT", "PFEIFEN", "HAUSTÜR", "RENNEN", "STEHEN", "TEIL", "2"}
DISPLAY = {"zwei": "2"}
SKIP = {"zwölf", "zwölf.", "dreißig.", "vierzig.", "Uhr"}


def norm(t):
    return re.sub(r"[^\wÄÖÜäöüß:]", "", t).upper()


words = []
for k, w in enumerate(W):
    nxt2 = " ".join(x["t"] for x in W[k:k+3]).lower()
    if nxt2.startswith("dreiundzwanzig uhr achtundfünfzig"): words.append({"t": "23:58.", "s": w["s"], "e": W[k+2]["e"]}); continue
    if k >= 1 and W[k-1]["t"].lower() == "dreiundzwanzig" and w["t"] == "Uhr": continue
    if k >= 2 and W[k-1]["t"] == "Uhr" and w["t"].lower().startswith("achtundfünfzig"): continue
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
<radialGradient id="yelglow"><stop offset="0" stop-color="#ffd23f" stop-opacity=".55"/><stop offset="1" stop-color="#ffd23f" stop-opacity="0"/></radialGradient>
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


danger("ov-d1", t_hebt, t_neue)
danger("ov-d2", t_ruft, t_willst)
danger("ov-d3", t_wer, t_was)

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
    <title>Gully Teil 1</title>
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
