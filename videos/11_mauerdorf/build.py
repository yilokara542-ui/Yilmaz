#!/usr/bin/env python3
"""Generator für index.html – Video 11 „Die Welt hinter den Mauern“ (eigene Welt, Mitmach-Video).

Alle Zeiten kommen aus assets/words.json (wortgenaue Voiceover-Zeitstempel).
Aufruf: python3 build.py → index.html + assets/cues.json
"""
import json, re, html, os, math, random, zlib, struct, base64

HERE = os.path.dirname(os.path.abspath(__file__))
W = json.load(open(os.path.join(HERE, "assets/words.json"), encoding="utf-8"))
VO_END = W[-1]["e"]
TOTAL = round(VO_END + 1.6, 2)          # Schlussfrage steht noch kurz
XF = 0.3                                 # Überblendung zwischen Szenen
RNG = random.Random(11)

# ---------- Farben: Nacht-Palette (Format B) ----------
SKY1 = "#0b0d26"; SKY2 = "#1d1d4f"; VIO = "#2a2360"; BLD = "#141634"; BLD2 = "#1b1d44"
WIN = "#ffd98a"; LAMP = "#ffd98a"; MOON = "#f4e3a1"; STREET = "#191a33"; WALK = "#25264a"
FIG = "#d9dde3"; INK = "#151a21"; RED = "#ff3b3b"; LIME = "#c8f031"; BLUE = "#3b6cff"; WHITE = "#ffffff"
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
    tw(f'tl.fromTo("{sel}",{{opacity:0,scale:{frm},transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:{dur},ease:"power3.out"}},{t:.3f});')


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
    if outfit in ("tunic", "tunic2"):   # Dorfbewohner: Leinentunika mit Gürtel
        H, H2, P, SH = (("#8a6a4a", "#6e5038", "#4a3a2a", "#3a2a1a") if outfit == "tunic" else ("#5a7a9a", "#4a6a8a", "#4a3a2a", "#3a2a1a"))
        extra = '<rect x="-62" y="-150" width="124" height="14" fill="#3a2a1a"/><rect x="-10" y="-152" width="20" height="18" rx="3" fill="#c9a24b"/><polygon points="-20,-258 0,-226 20,-258" fill="#efe4cc"/>'
    elif outfit == "apron":   # Bäcker: weiße Schürze, Mütze-artiger Kragen
        H, H2, P, SH = "#c97b4a", "#a8643a", "#4a3a2a", "#3a2a1a"
        extra = '<rect x="-46" y="-236" width="92" height="132" rx="18" fill="#f6f1e6"/><rect x="-46" y="-206" width="92" height="8" fill="#e9e1cf"/>'
    elif outfit == "hunter":  # Jäger: dunkles Wams, Lederriemen kreuzweise
        H, H2, P, SH = "#3a3a44", "#2a2a33", "#e9e1cf", "#3a2a1a"
        extra = '<line x1="-56" y1="-250" x2="56" y2="-120" stroke="#7a4a2a" stroke-width="12"/><line x1="56" y1="-250" x2="-56" y2="-120" stroke="#7a4a2a" stroke-width="12"/>'
    elif outfit == "shirt":   # Mann in Japan: helles Hemd, Krawatte, dunkle Hose
        H, H2, P, SH = "#dfe6ef", "#c9d2de", "#2b2f3a", "#1a1d22"
        extra = '<polygon points="-6,-250 6,-250 10,-150 0,-136 -10,-150" fill="#8b2a2a"/><polygon points="-24,-258 0,-240 24,-258 24,-250 0,-232 -24,-250" fill="#c9d2de"/>'
    elif outfit == "vest":
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
    eyes_svg = "" if back else (
        eye("n", 1 if eyes == "n" else 0,
            f'<circle cx="-22" cy="-322" r="9" fill="{E}"/><circle cx="22" cy="-322" r="9" fill="{E}"/>'
            f'<rect x="-36" y="-346" width="26" height="6" rx="3" fill="{E}"/><rect x="10" y="-346" width="26" height="6" rx="3" fill="{E}"/>'
            f'<rect x="-12" y="-290" width="24" height="5" rx="2.5" fill="{E}"/>')
        + eye("w", 1 if eyes == "w" else 0,
              f'<circle cx="-24" cy="-322" r="17" fill="none" stroke="{E}" stroke-width="5"/><circle cx="24" cy="-322" r="17" fill="none" stroke="{E}" stroke-width="5"/>'
              f'<circle cx="-24" cy="-322" r="5" fill="{E}"/><circle cx="24" cy="-322" r="5" fill="{E}"/>'
              f'<rect x="-42" y="-356" width="28" height="6" rx="3" fill="{E}" transform="rotate(-12 -28 -353)"/>'
              f'<rect x="14" y="-356" width="28" height="6" rx="3" fill="{E}" transform="rotate(12 28 -353)"/>'
              f'<ellipse cx="0" cy="-284" rx="9" ry="12" fill="{E}"/>')
        + eye("c", 1 if eyes == "c" else 0,
              f'<rect x="-34" y="-324" width="22" height="6" rx="3" fill="{E}"/><rect x="12" y="-324" width="22" height="6" rx="3" fill="{E}"/>'
              f'<path d="M -14 -292 Q 0 -282 14 -292" stroke="{E}" stroke-width="5" fill="none" stroke-linecap="round"/>')
        + eye("f", 1 if eyes == "f" else 0,
              f'<circle cx="-22" cy="-322" r="9" fill="{E}"/><circle cx="22" cy="-322" r="9" fill="{E}"/>'
              f'<rect x="-38" y="-350" width="28" height="6" rx="3" fill="{E}" transform="rotate(14 -24 -347)"/>'
              f'<rect x="10" y="-350" width="28" height="6" rx="3" fill="{E}" transform="rotate(-14 24 -347)"/>'
              f'<rect x="-14" y="-290" width="28" height="6" rx="3" fill="{E}"/>'))
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
  <circle cx="-74" cy="-126" r="13" fill="{FIG}"/><circle cx="74" cy="-126" r="13" fill="{FIG}"/>
  <rect x="-12" y="-278" width="24" height="26" rx="8" fill="{FIG}"/>
  <circle cx="0" cy="-320" r="64" fill="{FIG}"/>
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
STONE = "#7d7a74"; STONE2 = "#6a675f"; STONE3 = "#8d8a82"; MOSS = "#4f7a45"; BEAM = "#5a3a24"; PLASTER = "#efe4cc"; ROOF = "#a8432f"; ROOF2 = "#8e3626"
COBBLE = "#8a8377"; GRASS = "#4f8a4a"; GIANT = "#c9a58a"; GIANT2 = "#b08a6e"; GLOW = "#ffb22e"; CLOAK = "#2f4a7a"; CLOAK2 = "#253c64"; GOLD = "#e9c46a"
SEPIA = set()

t_wachst = ws("wachst"); t_riesen0 = ws("Riesen"); t_entsch = ws("entscheidest")
t_vor = ws("Vor", 5); t_fach = ws("Fachwerkhäuser"); t_markt = ws("Marktplatz"); t_brunnen = ws("Brunnen")
t_und1 = ws("Und", t_brunnen); t_mauer1 = ws("Mauer", t_und1); t_fuenfzig = ws("Fünfzig")
t_seit = ws("Seit"); t_hundert = ws("hundert", t_seit)
t_baecker = ws("Bäcker"); t_kinder = ws("Kinder"); t_friedlich = ws("friedlich")
t_doch = ws("Doch"); t_glocke = ws("Glocke"); t_schneller = ws("schneller")
t_erde = ws("Erde"); t_bebt = ws("bebt")
t_langsam = ws("Langsam"); t_kopf = ws("Kopf"); t_augen = ws("leuchtenden")
t_ein_r = ws("Ein", t_augen); t_stirn = ws("Stirn"); t_name1 = ws("Name", t_stirn); t_deiner = ws("deiner")
t_denn = ws("Denn"); t_drei = ws("drei", t_denn)
t_erst = ws("Erstens"); t_folgst = ws("folgst"); t_gross = ws("Groß"); t_zweit = ws("Zweitens"); t_likest = ws("likest"); t_umhang = ws("Umhang"); t_platz = ws("Platz", t_umhang)
t_dritt = ws("Drittens"); t_komm = ws("kommentierst"); t_haeuser = ws("Häuser"); t_tuer = ws("Tür", t_haeuser)
t_hebt = ws("hebt"); t_springen = ws("springen"); t_verr = ws("verriegeln")
t_und_j = ws("Und", t_verr); t_also = ws("Also"); t_wer = ws("Wer", t_also); t_schreib = ws("Schreib")

NAMES = ["@lina.baut", "@jonas.k39", "@mia_nrw", "@tim.zockt", "@emma.vb", "@noah_2011", "@lea.mlk", "@finn.ok"]


# ---------- Bausteine der eigenen Welt ----------
def sky_dawn():
    return (f'<rect width="1080" height="1920" fill="url(#dawn)"/>'
            f'<circle cx="820" cy="560" r="110" fill="#ffd27a"/><circle cx="820" cy="560" r="260" fill="url(#sunglow)"/>'
            + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#fff" opacity=".18"/>' for x, y, rx, ry in ((200, 300, 180, 40), (620, 220, 220, 46), (960, 380, 150, 34))))


def wall(y_top, h, x0=-40, x1=1120, gid="wall", torches=True):
    blocks = ""
    for r, y in enumerate(range(y_top, y_top + h, 70)):
        off = 0 if r % 2 == 0 else 70
        for x in range(x0 - off, x1, 140):
            c = (STONE, STONE2, STONE3)[(x // 140 + r) % 3]
            blocks += f'<rect x="{x}" y="{y}" width="136" height="66" rx="6" fill="{c}"/>'
    moss = "".join(f'<ellipse cx="{x}" cy="{y_top + h - 20}" rx="{60 + (x % 50)}" ry="26" fill="{MOSS}" opacity=".8"/>' for x in range(x0, x1, 170))
    moss += "".join(f'<path d="M {x} {y_top+40} q 10 {80+x%60} -6 {160+x%80}" stroke="{MOSS}" stroke-width="10" fill="none" opacity=".7"/>' for x in range(x0 + 90, x1, 330))
    cren = "".join(f'<rect x="{x}" y="{y_top-60}" width="90" height="64" rx="4" fill="{STONE3}"/>' for x in range(x0, x1, 150))
    tor = ""
    if torches:
        for x in range(x0 + 160, x1, 460):
            tor += (f'<rect x="{x}" y="{y_top+90}" width="12" height="60" fill="#3a2a1a"/><ellipse cx="{x+6}" cy="{y_top+80}" rx="16" ry="26" fill="{GLOW}"/>'
                    f'<circle cx="{x+6}" cy="{y_top+90}" r="90" fill="url(#fireglow)"/>')
    return f'<g id="{gid}">{cren}{blocks}{moss}{tor}<rect x="{x0}" y="{y_top}" width="{x1-x0}" height="{h}" fill="url(#wallshade)"/></g>'


def house(x, y, w=220, h=220, roof=ROOF, door=True, nid=None, name=None, flowers=True, lit=True):
    beams = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{PLASTER}"/>'
             f'<rect x="{x}" y="{y}" width="{w}" height="12" fill="{BEAM}"/><rect x="{x}" y="{y+h-12}" width="{w}" height="12" fill="{BEAM}"/>'
             f'<rect x="{x}" y="{y}" width="12" height="{h}" fill="{BEAM}"/><rect x="{x+w-12}" y="{y}" width="12" height="{h}" fill="{BEAM}"/>'
             f'<rect x="{x}" y="{y+h*0.45}" width="{w}" height="10" fill="{BEAM}"/>'
             f'<line x1="{x+12}" y1="{y+h*0.45}" x2="{x+w*0.35}" y2="{y+12}" stroke="{BEAM}" stroke-width="10"/>'
             f'<line x1="{x+w-12}" y1="{y+h*0.45}" x2="{x+w*0.65}" y2="{y+12}" stroke="{BEAM}" stroke-width="10"/>')
    roof_svg = (f'<polygon points="{x-24},{y+4} {x+w/2},{y-h*0.62} {x+w+24},{y+4}" fill="{roof}"/>'
                + "".join(f'<line x1="{x-10+i*28}" y1="{y-2}" x2="{x+w/2}" y2="{y-h*0.6}" stroke="{ROOF2}" stroke-width="3" opacity=".6"/>' for i in range(int((w+20)/28)+1))
                + f'<rect x="{x+w*0.68}" y="{y-h*0.55}" width="26" height="{h*0.3}" fill="#6e4a3a"/>')
    win = "".join(f'<rect x="{wx}" y="{y+h*0.12}" width="{w*0.2}" height="{h*0.22}" rx="4" fill="{"#ffd98a" if lit else "#3a4a6a"}"/><rect x="{wx+w*0.1-2}" y="{y+h*0.12}" width="4" height="{h*0.22}" fill="{BEAM}"/>'
                  for wx in (x + w * 0.16, x + w * 0.64))
    fl = "".join(f'<rect x="{wx-4}" y="{y+h*0.34}" width="{w*0.2+8}" height="12" fill="{BEAM}"/>' + "".join(f'<circle cx="{wx+6+k*12}" cy="{y+h*0.34-4}" r="7" fill="{c}"/>' for k, c in enumerate(("#e63946", "#f4a261", "#e63946", "#ffd166"))) for wx in (x + w * 0.16, x + w * 0.64)) if flowers else ""
    door_svg = ""
    if door:
        door_svg = (f'<g id="{nid}-door" ><rect x="{x+w*0.38}" y="{y+h*0.58}" width="{w*0.24}" height="{h*0.42-12}" rx="{w*0.12}" fill="#6e4a3a"/></g>'
                    f'<circle cx="{x+w*0.57}" cy="{y+h*0.8}" r="4" fill="{GOLD}"/>' if nid else
                    f'<rect x="{x+w*0.38}" y="{y+h*0.58}" width="{w*0.24}" height="{h*0.42-12}" rx="{w*0.12}" fill="#6e4a3a"/>')
    plate = ""
    if name:
        plate = (f'<g id="{nid}-plate" opacity="0"><rect x="{x+w*0.5-90}" y="{y+h*0.5-6}" width="180" height="40" rx="8" fill="#fff4dc" stroke="{BEAM}" stroke-width="4"/>'
                 f'<text x="{x+w*0.5}" y="{y+h*0.5+22}" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="22" fill="#3a2a1a">{name}</text></g>')
    return f'<g>{roof_svg}{beams}{win}{fl}{door_svg}{plate}</g>'


def village_row(y, start=-60, seed=0, lit=True):
    out = ""; x = start; i = seed
    while x < 1120:
        w = 180 + (i * 37) % 80; h = 170 + (i * 23) % 70
        out += house(x, y - h, w, h, roof=(ROOF, "#7a4a8a", "#b5651d", "#6a7a3a")[i % 4], lit=lit)
        x += w + 26; i += 1
    return out


def fountain(cx, cy, fid="fo"):
    drops = "".join(f'<rect id="{fid}-d{i}" x="{cx-40+i*16}" y="{cy-120}" width="5" height="22" rx="2" fill="#aee3ff" opacity=".8"/>' for i in range(6))
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="170" ry="46" fill="#5e5a52"/><ellipse cx="{cx}" cy="{cy-10}" rx="150" ry="36" fill="#6fb9e0"/>'
            f'<rect x="{cx-20}" y="{cy-140}" width="40" height="130" fill="#8d8a82"/><ellipse cx="{cx}" cy="{cy-140}" rx="70" ry="18" fill="#8d8a82"/>'
            f'<ellipse cx="{cx}" cy="{cy-146}" rx="56" ry="12" fill="#6fb9e0"/>{drops}')


def stall(x, y, col="#e63946", gid=None):
    stripes = "".join(f'<polygon points="{x+i*40},{y} {x+i*40+40},{y} {x+i*40+30},{y+50} {x+i*40-10},{y+50}" fill="{col if i%2==0 else "#fff4dc"}"/>' for i in range(6))
    goods = "".join(f'<circle cx="{x+30+i*34}" cy="{y+118}" r="14" fill="{c}"/>' for i, c in enumerate(("#e63946", "#f4a261", "#9bc53d", "#e63946", "#ffd166", "#9bc53d")))
    g = f' id="{gid}"' if gid else ""
    return (f'<g{g}><rect x="{x}" y="{y+40}" width="8" height="160" fill="{BEAM}"/><rect x="{x+232}" y="{y+40}" width="8" height="160" fill="{BEAM}"/>{stripes}'
            f'<rect x="{x-6}" y="{y+130}" width="252" height="70" fill="#8a5a3a"/>{goods}</g>')


def bell_tower(x, y, bid="bell"):
    return (f'<rect x="{x}" y="{y}" width="200" height="700" fill="{PLASTER}" stroke="{BEAM}" stroke-width="10"/>'
            f'<polygon points="{x-30},{y} {x+100},{y-200} {x+230},{y}" fill="{ROOF}"/>'
            f'<rect x="{x+40}" y="{y+40}" width="120" height="150" rx="60" fill="#2a1f17"/>'
            f'<g id="{bid}"><path d="M {x+70} {y+80} Q {x+100} {y+40} {x+130} {y+80} L {x+140} {y+160} L {x+60} {y+160} Z" fill="{GOLD}"/><circle cx="{x+100}" cy="{y+168}" r="12" fill="#a8842a"/></g>'
            f'<circle cx="{x+100}" cy="{y+300}" r="60" fill="#f6f1e6" stroke="{BEAM}" stroke-width="8"/><rect x="{x+97}" y="{y+256}" width="6" height="44" fill="#222"/><rect x="{x+100}" y="{y+297}" width="34" height="6" fill="#222"/>')


def villager(fid, x, y, s=1.0, eyes="n", kind="tunic"):
    return figure(fid, x, y, s, eyes=eyes, outfit=kind)


def giant_head(gid, cx, cy, s=1.0, name="@dein.name", glow=True):
    cracks = "".join(f'<path d="M {cx+dx} {cy+dy} l {a} {b} l {c} {d}" stroke="{GIANT2}" stroke-width="5" fill="none" opacity=".8"/>' for dx, dy, a, b, c, d in
                     ((-200, -120, 40, 50, -20, 60), (150, -60, -30, 70, 30, 40), (-120, 120, 50, 30, 10, 50), (90, 160, 30, -40, 40, 20)))
    return (f'<g id="{gid}"><g transform="translate({cx},{cy}) scale({s}) translate({-cx},{-cy})">'
            f'<ellipse cx="{cx}" cy="{cy}" rx="300" ry="340" fill="{GIANT}"/>{cracks}'
            f'<ellipse cx="{cx-300}" cy="{cy+20}" rx="40" ry="80" fill="{GIANT2}"/><ellipse cx="{cx+300}" cy="{cy+20}" rx="40" ry="80" fill="{GIANT2}"/>'
            f'<path d="M {cx-280} {cy-160} Q {cx} {cy-420} {cx+280} {cy-160} Q {cx} {cy-260} {cx-280} {cy-160} Z" fill="#3a2a22"/>'
            f'<rect x="{cx-170}" y="{cy-40}" width="120" height="20" rx="10" fill="#6e4a3a" transform="rotate(10 {cx-110} {cy-30})"/>'
            f'<rect x="{cx+50}" y="{cy-40}" width="120" height="20" rx="10" fill="#6e4a3a" transform="rotate(-10 {cx+110} {cy-30})"/>'
            f'<g id="{gid}-eyes"><ellipse cx="{cx-110}" cy="{cy+30}" rx="48" ry="34" fill="#1a120a"/><ellipse cx="{cx+110}" cy="{cy+30}" rx="48" ry="34" fill="#1a120a"/>'
            + (f'<circle cx="{cx-110}" cy="{cy+30}" r="20" fill="{GLOW}"/><circle cx="{cx+110}" cy="{cy+30}" r="20" fill="{GLOW}"/>'
               f'<circle cx="{cx-110}" cy="{cy+30}" r="70" fill="url(#fireglow)"/><circle cx="{cx+110}" cy="{cy+30}" r="70" fill="url(#fireglow)"/>' if glow else "")
            + f'</g><rect x="{cx-70}" y="{cy+170}" width="140" height="14" rx="7" fill="#7a5a4a"/>'
            f'<g id="{gid}-tag"><rect x="{cx-200}" y="{cy-170}" width="400" height="76" rx="14" fill="#1a120a" fill-opacity=".85" stroke="{RED}" stroke-width="6"/>'
            f'<text id="{gid}-name" x="{cx}" y="{cy-118}" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="44" fill="#fff">{name}</text></g>'
            f'</g></g>')


def hunter(hid, x, y, s=1.0, name=None, eyes="f"):
    """Eigener Jäger: blauer Umhang, Gürtel mit Enterhaken, goldenes Pfeil-Stern-Wappen."""
    tag = (f'<rect x="{x-110}" y="{y-470*s-30}" width="220" height="50" rx="12" fill="#0b0e12" fill-opacity=".85" stroke="#5aa0ff" stroke-width="3"/>'
           f'<text x="{x}" y="{y-470*s+4}" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="28" fill="#fff">{name}</text>') if name else ""
    return (f'<g id="{hid}"><g transform="translate({x},{y}) scale({s})">'
            f'<path d="M -70 -250 Q -120 -120 -100 -10 L 100 -10 Q 120 -120 70 -250 Z" fill="{CLOAK}"/>'
            f'<path d="M -70 -250 Q -60 -230 0 -226 Q 60 -230 70 -250 L 60 -262 L -60 -262 Z" fill="{CLOAK2}"/></g>'
            + figure(f"{hid}-f", x, y, s, eyes=eyes, outfit="hunter")
            + f'<g transform="translate({x},{y}) scale({s})"><polygon points="0,-240 10,-214 38,-214 16,-198 24,-172 0,-188 -24,-172 -16,-198 -38,-214 -10,-214" fill="{GOLD}" transform="translate(0,40) scale(.7)"/>'
            f'<rect x="-90" y="-150" width="40" height="70" rx="12" fill="#9aa0a6"/><rect x="50" y="-150" width="40" height="70" rx="12" fill="#9aa0a6"/>'
            f'<rect x="-66" y="-130" width="132" height="14" fill="#3a2a1a"/></g>{tag}</g>')


# ================= SZENEN =================
# S1 Hook: Aufwachen auf dem Hügel, Dorf hinter der Mauer
S0, S1 = 0.0, t_vor
scene("s1", S0, S1, sky_dawn() + wall(820, 420, gid="s1-wall")
      + f'<g opacity=".95">{village_row(1180, seed=1)}</g>'
      + f'<path d="M -50 1500 Q 300 1340 700 1420 T 1130 1380 L 1130 1920 L -50 1920 Z" fill="{GRASS}"/>'
      + "".join(f'<path d="M {x} 1600 l 6 -30 l 6 30" stroke="#3f7a3a" stroke-width="5" fill="none"/>' for x in range(0, 1080, 40))
      + "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="{c}"/>' for x, y, c in ((120, 1640, "#ffd166"), (300, 1700, "#fff"), (880, 1660, "#e63946"), (980, 1740, "#ffd166")))
      + figure("s1-fig", 540, 1760, 1.15, eyes="c", outfit="tunic")
      + f'<g id="s1-q" opacity="0"><circle cx="150" cy="560" r="70" fill="{RED}"/><text x="150" y="592" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="92" fill="#fff">?</text></g>')
tw(f'tl.fromTo("#s1-fig",{{y:120,opacity:.0}},{{y:0,opacity:1,duration:.9,ease:"power2.out"}},{t_wachst:.3f});')
tw(f'tl.set("#s1-fig-eyes-c",{{opacity:0}},{t_riesen0:.3f});'); tw(f'tl.set("#s1-fig-eyes-w",{{opacity:1}},{t_riesen0:.3f});')
pop("#s1-q", t_entsch)

# S2 Dorf: Fachwerk, Markt, Brunnen
S0, S1 = t_vor, t_und1
scene("s2", S0, S1, sky_dawn() + wall(300, 300, gid="s2-wall", torches=False)
      + village_row(980, seed=2) + bell_tower(820, 360, "s2-bell")
      + f'<rect x="0" y="980" width="1080" height="940" fill="{COBBLE}"/>'
      + "".join(f'<ellipse cx="{x + (y//40)%2*30}" cy="{y}" rx="26" ry="12" fill="#7a7368"/>' for y in range(1000, 1920, 40) for x in range(0, 1100, 64))
      + stall(60, 1080, "#e63946", "s2-st1") + stall(760, 1100, "#2a9d8f", "s2-st2")
      + f'<g id="s2-fo">{fountain(540, 1500, "s2fo")}</g>'
      + "".join(f'<g transform="translate({x},1300)"><rect x="-4" y="-200" width="8" height="200" fill="#2a2a2a"/><rect x="-20" y="-230" width="40" height="40" rx="6" fill="#2a2a2a"/><rect x="-14" y="-224" width="28" height="28" fill="{GLOW}"/></g>' for x in (360, 720))
      + label("s2-l1", 270, 920, "FACHWERK", "#3a2a1a", 34, fill="#fff4dc") + label("s2-l2", 540, 1080, "MARKTPLATZ", "#3a2a1a", 34, fill="#fff4dc") + label("s2-l3", 540, 1700, "BRUNNEN", "#3a2a1a", 34, fill="#fff4dc"))
pop("#s2-l1", t_fach); pop("#s2-l2", t_markt); pop("#s2-l3", t_brunnen)
for i in range(6):
    tw(f'tl.fromTo("#s2fo-d{i}",{{y:0,opacity:.8}},{{y:110,opacity:0,duration:.6,repeat:{int((S1-S0)/0.6)},ease:"power1.in"}},{S0 + i*0.1:.3f});')

# S3 Mauer 50 m
S0, S1 = t_und1, t_seit
scene("s3", S0, S1, sky_dawn() + wall(260, 1500, gid="s3-wall")
      + f'<rect x="0" y="1760" width="1080" height="160" fill="{GRASS}"/>' + figure("s3-fig", 300, 1830, 0.35, eyes="w", outfit="tunic")
      + f'<g id="s3-m" opacity="0"><line x1="880" y1="200" x2="880" y2="1830" stroke="{RED}" stroke-width="8" stroke-dasharray="26 14"/>'
        f'<rect x="850" y="196" width="60" height="8" fill="{RED}"/><rect x="850" y="1826" width="60" height="8" fill="{RED}"/>'
        f'<rect x="740" y="960" width="280" height="110" rx="20" fill="#0b0e12" fill-opacity=".85"/><text x="880" y="1040" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="76" fill="{RED}">50 m</text></g>')
tw(f'tl.fromTo("#s3-cam",{{scale:1.35,svgOrigin:"300 1830"}},{{scale:1,svgOrigin:"300 1830",duration:{S1-S0:.3f},ease:"sine.inOut"}},{S0:.3f});')
pop("#s3-m", t_fuenfzig, 0.4, 0.8)

# S4 Seit 100 Jahren – Zähltafel am Markt
S0, S1 = t_seit, t_baecker
scene("s4", S0, S1, sky_dawn() + wall(300, 300, torches=False, gid="s4-wall") + village_row(980, seed=4)
      + f'<rect x="0" y="980" width="1080" height="940" fill="{COBBLE}"/>'
      + '<g transform="translate(0,-260)">' + f'<rect x="250" y="760" width="580" height="420" rx="16" fill="#3a2a1a"/><rect x="270" y="780" width="540" height="380" rx="10" fill="#2a3a2a"/>'
      + f'<text x="540" y="860" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="36" fill="#e6e1c8" letter-spacing="4">TAGE OHNE RIESEN</text>'
      + "".join(f'<text id="s4-n{i}" x="540" y="1060" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="130" fill="#fff4dc" opacity="0">{n}</text>' for i, n in enumerate(("36.517", "36.518", "36.519", "36.520")))
      + f'<rect x="380" y="1180" width="16" height="560" fill="#3a2a1a"/><rect x="684" y="1180" width="16" height="560" fill="#3a2a1a"/></g>'
      + label("s4-l", 540, 1200, "100 JAHRE", RED, 50))
for i in range(4):
    a = S0 + (S1 - S0) * i / 4
    toggle(f"#s4-n{i}", a, S0 + (S1 - S0) * (i + 1) / 4 if i < 3 else None)
pop("#s4-l", t_hundert)

# S5 Friedlich: Bäcker winkt, Kinder rennen
S0, S1 = t_baecker, t_doch
pigeons = "".join(f'<g id="s5-pg{i}"><ellipse cx="{300+i*120}" cy="{1640+i%2*20}" rx="22" ry="14" fill="#9aa0a6"/><circle cx="{318+i*120}" cy="{1628+i%2*20}" r="9" fill="#9aa0a6"/></g>' for i in range(4))
scene("s5", S0, S1, sky_dawn() + wall(260, 260, torches=False, gid="s5-wall") + village_row(960, seed=5)
      + f'<rect x="0" y="960" width="1080" height="960" fill="{COBBLE}"/>'
      + house(560, 640, 400, 330, roof="#b5651d") + f'<rect x="620" y="560" width="280" height="70" rx="10" fill="#3a2a1a"/><text x="760" y="610" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="40" fill="{GOLD}">BÄCKEREI</text>'
      + stall(60, 1080, "#f4a261") + villager("s5-baker", 760, 1560, 1.1, eyes="n", kind="apron")
      + villager("s5-k1", -80, 1760, 0.6, eyes="c", kind="tunic") + villager("s5-k2", -200, 1790, 0.55, eyes="c", kind="tunic2")
      + pigeons)
tw(f'tl.fromTo("#s5-baker",{{rotation:-4,svgOrigin:"760 1560"}},{{rotation:4,svgOrigin:"760 1560",duration:.25,yoyo:true,repeat:7,ease:"sine.inOut"}},{t_baecker:.3f});')
tw(f'tl.to("#s5-k1",{{x:1300,duration:{max(.5,S1-t_kinder):.3f},ease:"none"}},{t_kinder:.3f});')
tw(f'tl.to("#s5-k2",{{x:1320,duration:{max(.5,S1-t_kinder):.3f},ease:"none"}},{t_kinder + 0.2:.3f});')
walk_cycle("s5-k1", t_kinder, S1, 0.3, 10); walk_cycle("s5-k2", t_kinder, S1, 0.3, 10)
for i in range(4):
    tw(f'tl.to("#s5-pg{i}",{{y:-8,duration:.3,yoyo:true,repeat:{int((S1-S0)/0.3)},ease:"sine.inOut"}},{S0 + i*0.1:.3f});')

# S6 Die Glocke läutet – immer schneller
S0, S1 = t_doch, t_erde
scene("s6", S0, S1, f'<rect width="1080" height="1920" fill="url(#dusk)"/>' + bell_tower(440, 520, "s6-bell")
      + f'<g transform="translate(-440,-180) scale(1.8)">{bell_tower(440, 520, "s6-bellbig")}</g>'
      + f'<g id="s6-dong" opacity="0"><text x="120" y="420" font-family="Poppins" font-weight="800" font-size="110" fill="{RED}" transform="rotate(-8 120 420)">DONG</text></g>'
      + f'<g id="s6-dong2" opacity="0"><text x="580" y="300" font-family="Poppins" font-weight="800" font-size="90" fill="{RED}" transform="rotate(6 580 300)">DONG!</text></g>', drift=True)
n = 12
tt = t_glocke
for k in range(n):
    d = max(0.12, 0.45 - k * 0.03)
    tw(f'tl.to("#s6-bellbig",{{rotation:{18 if k%2==0 else -18},svgOrigin:"540 560",duration:{d:.3f},ease:"sine.inOut"}},{tt:.3f});')
    tt += d
pop("#s6-dong", t_glocke + 0.2); pop("#s6-dong2", t_schneller)

# S7 Die Erde bebt
S0, S1 = t_erde, t_langsam
scene("s7", S0, S1, f'<rect width="1080" height="1920" fill="url(#dusk)"/>' + wall(300, 340, gid="s7-wall") + village_row(1000, seed=7)
      + f'<rect x="0" y="1000" width="1080" height="920" fill="{COBBLE}"/>' + stall(400, 1180, "#e63946", "s7-st")
      + "".join(f'<circle id="s7-a{i}" cx="{440+i*34}" cy="1298" r="14" fill="{c}"/>' for i, c in enumerate(("#e63946", "#f4a261", "#9bc53d", "#e63946", "#ffd166", "#9bc53d")))
      + villager("s7-v1", 200, 1700, 0.9, eyes="w", kind="tunic") + villager("s7-v2", 860, 1720, 0.95, eyes="w", kind="apron")
      + "".join(f'<rect id="s7-cr{i}" x="{200+i*170}" y="{1500+i%2*90}" width="6" height="0" fill="#2a2620"/>' for i in range(5)))
for k in range(int((S1 - t_bebt) / 0.12)):
    tw(f'tl.to("#s7-cam",{{x:{(-1)**k * 10},y:{(-1)**(k+1) * 5},duration:.12,ease:"sine.inOut"}},{t_bebt + k*0.12:.3f});')
for i in range(6):
    tw(f'tl.to("#s7-a{i}",{{y:-30,duration:.18,yoyo:true,repeat:3,ease:"power1.out"}},{t_bebt + i*0.05:.3f});')
for i in range(5):
    tw(f'tl.to("#s7-cr{i}",{{attr:{{height:{160+i*30}}},rotation:{(-1)**i*20},transformOrigin:"50% 0%",duration:.6,ease:"power2.out"}},{t_bebt + 0.2 + i*0.1:.3f});')

# S8 Kopf über der Mauer – leuchtende Augen – ein Riese
S0, S1 = t_langsam, t_stirn
scene("s8", S0, S1, f'<rect width="1080" height="1920" fill="url(#dusk)"/>'
      + giant_head("s8-g", 540, 820, 1.0, name="")
      + wall(980, 940, gid="s8-wall")
      + hunter("s8-h1", 200, 980, 0.32) + hunter("s8-h2", 860, 980, 0.32))
tw(f'tl.fromTo("#s8-g",{{y:700}},{{y:0,duration:{t_ein_r-S0+0.3:.3f},ease:"sine.inOut"}},{S0:.3f});')
tw(f'tl.set("#s8-g-tag",{{opacity:0}},{S0:.3f});')
tw(f'tl.fromTo("#s8-g-eyes",{{opacity:.15}},{{opacity:1,duration:.3,ease:"power2.out"}},{t_augen:.3f});')
shake("#s8-cam", t_ein_r, 6, 10)

# S9 Name auf der Stirn – vielleicht deiner
S0, S1 = t_stirn, t_denn
scene("s9", S0, S1, f'<rect width="1080" height="1920" fill="url(#dusk)"/>'
      + giant_head("s9-g", 540, 1060, 1.6, name="")
      + "".join(f'<text id="s9-n{i}" x="540" y="{1060-118*1.6+0:.0f}" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="70" fill="#fff" opacity="0">{n}</text>' for i, n in enumerate(NAMES[:4] + ["@DU?"])))
tw(f'tl.set("#s9-g-name",{{opacity:0}},{S0:.3f});')
seq = NAMES[:4] + ["@DU?"]
step = (S1 - t_name1) / len(seq)
for i in range(len(seq)):
    a = t_name1 + step * i
    toggle(f"#s9-n{i}", a, a + step if i < len(seq) - 1 else None)
tw(f'tl.fromTo("#s9-n4",{{fill:"#fff"}},{{fill:"{RED}",duration:.3}},{t_deiner:.3f});')

# S10 Drei Arten von Menschen
S0, S1 = t_denn, t_erst
cardx = (190, 540, 890)
scene("s10", S0, S1, f'<rect width="1080" height="1920" fill="#120e14"/><circle cx="540" cy="900" r="600" fill="url(#cardglow)"/>'
      + "".join(f'<g id="s10-c{i}" opacity="0"><rect x="{x-150}" y="660" width="300" height="560" rx="30" fill="#1e1822" stroke="{c}" stroke-width="6"/>'
                f'<text x="{x}" y="1190" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="34" fill="{c}">{t}</text></g>'
                for i, (x, c, t) in enumerate(zip(cardx, (GLOW, "#5aa0ff", "#9bc53d"), ("RIESE", "JÄGER", "DORF"))))
      + f'<g transform="translate(190,860) scale(.28) translate(-540,-860)">{giant_head("s10-g", 540, 860, 1.0, name="")}</g>'
      + hunter("s10-h", 540, 1110, 0.62) + villager("s10-v", 890, 1110, 0.62, kind="tunic"))
tw(f'tl.set("#s10-g-tag",{{opacity:0}},{S0:.3f});')
for i in range(3):
    pop(f"#s10-c{i}", t_drei + i * 0.2, 0.35, 0.7)


# Rollen-Karten
def role_card(sid, n, head, sub, icon_svg, accent):
    return (f'<rect width="1080" height="1920" fill="#120e14"/><circle cx="540" cy="900" r="600" fill="url(#cardglow)"/>'
            f'<g id="{sid}-badge" opacity="0"><rect x="410" y="200" width="260" height="62" rx="12" fill="{accent}"/>'
            f'<text x="540" y="245" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="34" fill="#120e14">ROLLE #{n}</text></g>'
            f'<g id="{sid}-head" opacity="0"><text x="540" y="380" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="96" fill="#fff">{head}</text></g>'
            f'<g id="{sid}-sub" opacity="0"><rect x="290" y="420" width="500" height="90" rx="45" fill="{accent}"/>{icon_svg}'
            f'<text x="590" y="480" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="44" fill="#120e14">{sub}</text></g>')


plus_ic = '<circle cx="350" cy="465" r="30" fill="#120e14"/><rect x="336" y="461" width="28" height="8" fill="#fff"/><rect x="346" y="451" width="8" height="28" fill="#fff"/>'
heart_ic = f'<path d="M 350 490 L 324 462 A 15 15 0 0 1 350 444 A 15 15 0 0 1 376 462 Z" fill="{RED}"/>'
bubble_ic = '<rect x="322" y="440" width="58" height="42" rx="12" fill="#120e14"/><polygon points="334,480 350,480 334,496" fill="#120e14"/>'

# R1 Riesen – Folgen
S0, S1 = t_erst, t_zweit
giants = "".join(f'<g transform="translate({x},{y}) scale({s}) translate(-540,-860)">{giant_head(f"r1-g{i}", 540, 860, 1.0, name=NAMES[i])}</g>' for i, (x, y, s) in enumerate(((220, 950, .5), (540, 860, .62), (860, 970, .5))))
scene("r1", S0, S1, role_card("r1", 1, "RIESE", "FOLGEN", plus_ic, GLOW) + giants + wall(1150, 770, gid="r1-wall")
      + label("r1-big", 540, 1560, "DEIN NAME. GROSS. UNÜBERSEHBAR.", GLOW, 36))
pop("#r1-badge", S0); pop("#r1-head", S0 + 0.3); pop("#r1-sub", t_folgst)
for i in range(3):
    tw(f'tl.fromTo("#r1-g{i}",{{y:600}},{{y:0,duration:.8,ease:"back.out(1.4)"}},{t_folgst + 0.2 + i*0.25:.3f});')
pop("#r1-big", t_gross)

# R2 Jäger – Liken
S0, S1 = t_zweit, t_dritt
scene("r2", S0, S1, role_card("r2", 2, "JÄGER", "LIKEN", heart_ic, "#5aa0ff")
      + wall(1150, 770, gid="r2-wall")
      + hunter("r2-h1", 260, 1150, 0.55, name=NAMES[3]) + hunter("r2-h2", 540, 1150, 0.62, name=NAMES[4]) + hunter("r2-h3", 820, 1150, 0.55, name=NAMES[5])
      + f'<g id="r2-hook" opacity="0"><path d="M 540 1000 Q 700 760 980 640" stroke="#c9ccd8" stroke-width="5" fill="none" stroke-dasharray="12 8"/><polygon points="980,620 1010,650 970,660" fill="#c9ccd8"/></g>'
      + label("r2-l1", 300, 700, "UMHANG", "#5aa0ff", 36) + label("r2-l2", 800, 760, "ENTERHAKEN", "#5aa0ff", 36))
pop("#r2-badge", S0); pop("#r2-head", S0 + 0.3); pop("#r2-sub", t_likest)
tw(f'tl.fromTo("#r2-h1",{{y:400}},{{y:0,duration:.6,ease:"back.out(1.6)"}},{t_likest + 0.2:.3f});')
tw(f'tl.fromTo("#r2-h2",{{y:400}},{{y:0,duration:.6,ease:"back.out(1.6)"}},{t_likest + 0.4:.3f});')
tw(f'tl.fromTo("#r2-h3",{{y:400}},{{y:0,duration:.6,ease:"back.out(1.6)"}},{t_likest + 0.6:.3f});')
pop("#r2-l1", t_umhang); pop("#r2-l2", t_umhang + 0.6); pop("#r2-hook", t_umhang + 0.6)

# R3 Dorfbewohner – Kommentieren
S0, S1 = t_dritt, t_hebt
scene("r3", S0, S1, role_card("r3", 3, "DORFBEWOHNER", "KOMMENTIEREN", bubble_ic, "#9bc53d")
      + f'<rect x="0" y="1460" width="1080" height="460" fill="{COBBLE}"/>'
      + house(40, 1180, 300, 280, nid="r3-a", name=NAMES[6]) + house(390, 1140, 300, 320, roof="#7a4a8a", nid="r3-b", name=NAMES[7]) + house(740, 1180, 300, 280, roof="#b5651d", nid="r3-c", name="@du?"))
pop("#r3-badge", S0); pop("#r3-head", S0 + 0.3); pop("#r3-sub", t_komm)
pop("#r3-a-plate", t_tuer - 0.4); pop("#r3-b-plate", t_tuer - 0.2); pop("#r3-c-plate", t_tuer)

# S11 Action: Riese hebt die Hand, Jäger springen, Türen zu
S0, S1 = t_hebt, t_und_j
hand = (f'<g id="s11-hand"><ellipse cx="820" cy="900" rx="170" ry="210" fill="{GIANT}"/>'
        + "".join(f'<rect x="{700+i*62}" y="{560+abs(i-2)*30}" width="54" height="260" rx="27" fill="{GIANT}"/>' for i in range(4))
        + f'<rect x="620" y="840" width="160" height="56" rx="28" fill="{GIANT}" transform="rotate(-30 700 868)"/></g>')
lines = "".join(f'<path id="s11-l{i}" d="M {200+i*220} 1080 Q {300+i*220} 760 {700+i*60} 700" stroke="#c9ccd8" stroke-width="5" fill="none" stroke-dasharray="800" stroke-dashoffset="800"/>' for i in range(3))
scene("s11", S0, S1, f'<rect width="1080" height="1920" fill="url(#dusk)"/>' + hand
      + giant_head("s11-g", 540, 700, 0.8, name=NAMES[1]) + wall(1080, 840, gid="s11-wall") + lines
      + hunter("s11-h1", 200, 1080, 0.35) + hunter("s11-h2", 420, 1080, 0.35) + hunter("s11-h3", 640, 1080, 0.35)
      + f'<g id="s11-doors" opacity="0">' + "".join(f'<g transform="translate({x},1560)"><rect x="-90" y="-200" width="180" height="200" fill="{PLASTER}"/><rect id="s11-d{i}" x="-40" y="-120" width="80" height="120" fill="#6e4a3a"/><rect x="-46" y="-70" width="92" height="12" fill="#3a2a1a"/></g>' for i, x in enumerate((180, 540, 900))) + '</g>'
      + f'<rect x="0" y="1560" width="1080" height="360" fill="{COBBLE}"/>')
tw(f'tl.fromTo("#s11-hand",{{y:700}},{{y:0,duration:.9,ease:"power2.out"}},{t_hebt:.3f});')
for i in range(3):
    tw(f'tl.to("#s11-l{i}",{{attr:{{"stroke-dashoffset":0}},duration:.4,ease:"power2.out"}},{t_springen + i*0.12:.3f});')
    tw(f'tl.to("#s11-h{i+1}",{{x:{300-i*40},y:-420,duration:.8,ease:"power2.out"}},{t_springen + 0.2 + i*0.12:.3f});')
pop("#s11-doors", t_verr - 0.3)
for i in range(3):
    tw(f'tl.fromTo("#s11-d{i}",{{scaleX:.1,transformOrigin:"0% 50%"}},{{scaleX:1,duration:.25,ease:"power2.in"}},{t_verr + i*0.15:.3f});')
shake("#s11-cam", t_verr + 0.5, 5, 6)

# S12 „Und jetzt hängt alles von dir ab“
S0, S1 = t_und_j, t_also
scene("s12", S0, S1, f'<rect width="1080" height="1920" fill="#120e14"/><polygon points="460,0 620,0 900,1920 180,1920" fill="url(#lampcone)" opacity=".6"/>'
      + figure("s12-fig", 540, 1640, 1.6, eyes="f", outfit="tunic")
      + "".join(f'<g id="s12-o{i}"><circle cx="{540+math.cos(a)*360:.0f}" cy="{760+math.sin(a)*200:.0f}" r="70" fill="{c}"/><text x="{540+math.cos(a)*360:.0f}" y="{775+math.sin(a)*200:.0f}" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="40" fill="#120e14">{t}</text></g>'
                for i, (a, c, t) in enumerate(((3.6, GLOW, "+"), (4.7, "#5aa0ff", "♥"), (5.8, "#9bc53d", "💬")))))
for i in range(3):
    pop(f"#s12-o{i}", S0 + 0.2 + i * 0.2, 0.35, 0.5)

# S13 Ende: Wer bist du?
S0, S1 = t_also, TOTAL
scene("s13", S0, S1, sky_dawn() + wall(820, 420, gid="s13-wall") + village_row(1180, seed=9)
      + f'<path d="M -50 1500 Q 300 1340 700 1420 T 1130 1380 L 1130 1920 L -50 1920 Z" fill="{GRASS}"/>'
      + figure("s13-fig", 540, 1760, 1.15, eyes="f", outfit="tunic")
      + pill("s13-p1", 540, 300, "＋  RIESE", GLOW, "#120e14") + pill("s13-p2", 540, 440, "♥  JÄGER", "#5aa0ff", "#120e14") + pill("s13-p3", 540, 580, "💬  DORFBEWOHNER", "#9bc53d", "#120e14"))
pop("#s13-p1", t_wer + 0.4); pop("#s13-p2", t_wer + 0.8); pop("#s13-p3", t_wer + 1.2)
tw(f'tl.fromTo("#s13-p3",{{scale:1}},{{scale:1.1,transformOrigin:"50% 50%",duration:.3,yoyo:true,repeat:3}},{t_schreib:.3f});')

brand_html = []

# ================= UNTERTITEL (Skill 7, Format A: Akzent Rot) =================
KEY = {"RIESEN", "MAUER", "ENTSCHEIDEST", "DORF", "FACHWERKHÄUSER", "MARKTPLATZ", "BRUNNEN", "FÜNFZIG", "HUNDERT", "FRIEDLICH",
       "GLOCKE", "SCHNELLER", "BEBT", "KOPF", "LEUCHTENDEN", "RIESE", "NAME", "DEINER", "DREI", "FOLGST", "GROSS", "UNÜBERSEHBAR",
       "JÄGER", "LIKEST", "UMHANG", "ENTERHAKEN", "DORFBEWOHNER", "KOMMENTIERST", "TÜR", "HAND", "SPRINGEN", "VERRIEGELN", "DIR", "KOMMENTARE"}
DISPLAY = {"Fünfzig": "50"}
SKIP = set()


def norm(t):
    return re.sub(r"[^\wÄÖÜäöüß]", "", t).upper().replace("ß", "SS")


words = [w for w in W if w["t"] not in SKIP]
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
    fs = min(62, int(980 / (0.56 * max(len(" ".join(plain)), 1))))
    sid = f"sub{k}"
    subs.append(f'<div id="{sid}" class="clip sub" data-start="{s:.3f}" data-duration="{e-s:.3f}" data-track-index="9" style="font-size:{fs}px">{" ".join(parts)}</div>')
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
<radialGradient id="cardglow"><stop offset="0" stop-color="#3a3d8f" stop-opacity=".55"/><stop offset="1" stop-color="#3a3d8f" stop-opacity="0"/></radialGradient>
<radialGradient id="stationglow" cx=".5" cy="0" r="1"><stop offset="0" stop-color="#fff4c9" stop-opacity=".35"/><stop offset="1" stop-color="#fff4c9" stop-opacity="0"/></radialGradient>
<radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".7"/></radialGradient>
<radialGradient id="sepvig" cx=".5" cy=".5" r=".75"><stop offset=".45" stop-color="#2a1a08" stop-opacity="0"/><stop offset="1" stop-color="#1a0f04" stop-opacity=".85"/></radialGradient>
<radialGradient id="coldglow" cx=".5" cy="0" r="1"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#bfe0ff" stop-opacity=".2"/></radialGradient>
<radialGradient id="heatg"><stop offset="0" stop-color="#fff2a8"/><stop offset=".45" stop-color="#ffb35c"/><stop offset="1" stop-color="{RED}"/></radialGradient>
<linearGradient id="dawn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b2f6b"/><stop offset=".45" stop-color="#c85a7a"/><stop offset=".8" stop-color="#ffb36b"/></linearGradient>
<linearGradient id="dusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a1430"/><stop offset=".6" stop-color="#5a2a3a"/><stop offset="1" stop-color="#a8432f"/></linearGradient>
<radialGradient id="sunglow"><stop offset="0" stop-color="#ffd27a" stop-opacity=".6"/><stop offset="1" stop-color="#ffd27a" stop-opacity="0"/></radialGradient>
<radialGradient id="fireglow"><stop offset="0" stop-color="#ffb22e" stop-opacity=".55"/><stop offset="1" stop-color="#ffb22e" stop-opacity="0"/></radialGradient>
<linearGradient id="wallshade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".45"/></linearGradient>
<radialGradient id="redvig" cx=".5" cy=".5" r=".72"><stop offset=".5" stop-color="{RED}" stop-opacity="0"/><stop offset="1" stop-color="{RED}" stop-opacity=".7"/></radialGradient>
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


danger("ov-d1", t_glocke, t_stirn)
danger("ov-d2", t_hebt, t_und_j)


def archive(aid, t0, t1):
    perf = "".join(f'<rect x="14" y="{y}" width="34" height="46" rx="8" fill="#0d0905"/><rect x="1032" y="{y}" width="34" height="46" rx="8" fill="#0d0905"/>' for y in range(10, 1920, 90))
    scr = "".join(f'<rect id="{aid}-sc{i}" x="0" y="0" width="3" height="1920" fill="#f3e2c0" opacity="0"/>' for i in range(3))
    OVER.append(f'<div id="{aid}" class="clip ov" data-start="{t0:.3f}" data-duration="{t1-t0:.3f}" data-track-index="7" style="z-index:7">'
                f'<svg viewBox="0 0 1080 1920" width="1080" height="1920"><rect width="1080" height="1920" fill="url(#sepvig)"/>'
                f'<rect x="0" y="0" width="62" height="1920" fill="#1a120a" opacity=".9"/><rect x="1018" y="0" width="62" height="1920" fill="#1a120a" opacity=".9"/>{perf}{scr}'
                f'<g opacity=".85"><circle cx="110" cy="1820" r="10" fill="{RED}"/><text x="132" y="1832" font-family="JetBrains Mono, monospace" font-weight="800" font-size="30" fill="#e6d2ad">ECHTER FALL · JAPAN 2008</text></g></svg></div>')
    tt = t0
    while tt < t1:
        for i in range(3):
            on = RNG.random() < 0.55
            tw(f'tl.set("#{aid}-sc{i}",{{opacity:{RNG.uniform(.08,.2) if on else 0:.2f},x:{RNG.randint(80, 1000)}}},{tt:.2f});')
        tt += 0.3




for fid in FIGS:
    tw(f'tl.fromTo("#{fid}-body",{{scaleY:1}},{{scaleY:1.02,transformOrigin:"50% 100%",duration:1.3,yoyo:true,repeat:{int(TOTAL/1.3)},ease:"sine.inOut"}},0);')
for sid, t0, t1, _ in SCENES[1:]:
    tw(f'tl.fromTo("#{sid}",{{opacity:0}},{{opacity:1,duration:{XF},ease:"sine.inOut"}},{t0:.3f});')

# ================= HTML =================
scene_html = [f'<div id="{sid}" class="clip scene{' sep' if sid in SEPIA else ''}" data-start="{t0:.3f}" data-duration="{min(t1+XF, TOTAL)-t0:.3f}" data-track-index="1">'
              f'<svg viewBox="0 0 1080 1920" width="1080" height="1920">{inner}</svg></div>' for sid, t0, t1, inner in SCENES]

doc = f'''<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Welt hinter den Mauern</title>
    <script src="assets/gsap.min.js"></script>
    <style>
      :root {{ --ground: {SKY1}; --ink: #ffffff; --accent: {RED}; --font-display: "Poppins", sans-serif; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: var(--ground); }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: var(--font-display); }}
      .scene, .ov {{ position: absolute; inset: 0; }}
      .ov {{ pointer-events: none; }}
      .scene svg {{ display: block; }}
      .scene.sep {{ filter: sepia(.75) saturate(.85) brightness(.92) contrast(1.05); }}
      .sub {{
        position: absolute; left: 40px; right: 40px; top: 960px; margin-top: -0.6em; text-align: center;
        color: var(--ink); font-weight: 600; line-height: 1.15; white-space: nowrap; z-index: 20;
        -webkit-text-stroke: 7px rgba(0,0,0,.85); paint-order: stroke fill; text-shadow: 0 3px 10px rgba(0,0,0,.6);
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
