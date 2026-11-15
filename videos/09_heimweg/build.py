#!/usr/bin/env python3
"""Generator für index.html – Video 09 „HEIMWEG · Teil 1“ (Skill-Format B „Regel-Serie“).

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
t_was = 0.0
t_23 = ws("Dreiundzwanzig"); t_steigst = ws("steigst"); t_hinter = ws("Hinter", t_23); t_jemand = ws("jemand")
t_hoerst = ws("hörst"); t_schritte = ws("Schritte"); t_leiser = ws("leiser")
t_bestimmt = ws("Bestimmt"); t_biegst = ws("biegst"); t_die_schr = ws("Schritte", t_biegst)
t_gehst = ws("gehst", t_die_schr); t_erauch = ws("Er", t_gehst)
t_schauf = ws("Im", t_erauch); t_kapuze = ws("Kapuze"); t_haende = ws("Hände"); t_zehn = ws("Zehn")
t_dein = ws("Dein", t_zehn); t_rennen = ws("rennen"); t_fehler = ws("Fehler"); t_dann = ws("Dann", t_fehler); t_wohnst = ws("wohnst")
t_polizei = ws("Die", t_wohnst); t_drei = ws("drei", t_polizei)
t_r1 = ws("Regel", t_drei + 0.5); t_teste = ws("Teste"); t_wechsel = ws("Wechsel"); t_folgt = ws("Folgt"); t_ernst = ws("ernst")
t_r2 = ws("Regel", t_ernst); t_licht = ws("Licht", t_r2); t_tanke = ws("Tankstelle", t_r2); t_kiosk = ws("Kiosk"); t_rest = ws("Restaurant"); t_nicht = ws("Nicht", t_rest)
t_r3 = ws("Regel", t_nicht); t_ruf = ws("Ruf"); t_bleib = ws("bleib", t_ruf); t_leitung = ws("Leitung")
t_du_w = ws("Du", t_leitung); t_er2 = ws("Er", t_du_w)
t_vorne = ws("Vorne"); t_rein = ws("rein"); t_laut = ws("laut", t_rein); t_mir = ws("Mir"); t_bitte = ws("Bitte")
t_waehlst = ws("wählst"); t_jetzt = ws("jetzt", t_waehlst); t_kaum = ws("kaum")
t_handy = ws("Handy", t_kaum); t_leitst = ws("Leitstelle"); t_standort = ws("Standort"); t_gps = ws("GPS"); t_wlan = ws("WLAN"); t_ohne = ws("Ohne"); t_nennt = ws("nennt"); t_aml = ws("A", t_nennt + 0.2)
t_draussen = ws("Draußen"); t_scheibe = ws("Scheibe"); t_und_er = ws("Und", t_scheibe); t_weg = ws("weg", t_und_er)
t_also = ws("Also"); t_drinnen = ws("drinnen"); t_abholt = ws("abholt")
t_teil2 = ws("Teil", t_abholt); t_knopf = ws("Notruf")

# ================= SZENEN =================
# S1 Hook: leere Nachtstraße, du unter der Laterne
S0, S1 = 0.0, t_23
scene("s1", S0, S1, street("s1") + figure("s1-fig", 540, 1500, 1.15, eyes="n")
      + f'<g id="s1-q" opacity="0"><circle cx="820" cy="680" r="70" fill="{RED}"/><text x="820" y="712" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="92" fill="#fff">?</text></g>')
pop("#s1-q", 0.4)
scroll_street("s1", S0, S1, 0.3)

# S2 Bus: aussteigen, jemand steigt mit aus
S0, S1 = t_23, t_hoerst
bus = (f'<g id="s2-bus"><rect x="-40" y="980" width="900" height="520" rx="40" fill="#28306b"/>'
       f'<rect x="-40" y="980" width="900" height="70" rx="30" fill="#323b82"/>'
       + "".join(f'<rect x="{x}" y="1080" width="150" height="190" rx="14" fill="{WIN}" opacity=".85"/>' for x in (20, 200, 380))
       + f'<rect x="580" y="1080" width="200" height="400" rx="10" fill="#0d0f26"/><rect id="s2-door" x="580" y="1080" width="200" height="400" rx="10" fill="#4a5396"/>'
       + f'<rect x="40" y="1000" width="170" height="54" rx="10" fill="#0b0d22"/><text x="125" y="1040" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="38" fill="{LIME}">N7</text>'
       + f'<circle cx="160" cy="1500" r="62" fill="#0b0d22"/><circle cx="160" cy="1500" r="26" fill="#3a3c6a"/><circle cx="700" cy="1500" r="62" fill="#0b0d22"/><circle cx="700" cy="1500" r="26" fill="#3a3c6a"/>'
       + f'<rect x="820" y="1220" width="40" height="30" rx="8" fill="{LAMP}"/></g>')
stop = (f'<rect x="900" y="900" width="14" height="620" fill="#3a3c6a"/><circle cx="907" cy="890" r="56" fill="{LIME}"/><text x="907" y="910" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="56" fill="#0b0d22">H</text>')
scene("s2", S0, S1, street("s2") + stop + bus + stalker("s2-st", 680, 1480, 0.95) + figure("s2-fig", 700, 1560, 1.05, eyes="n"))
tw(f'tl.set("#s2-st",{{opacity:0}},{S0:.3f});')
move("#s2-door", t_steigst, 0.4, "power2.out", x=180)
tw(f'tl.fromTo("#s2-fig",{{x:0,y:-40}},{{x:-260,y:0,duration:.9,ease:"sine.out"}},{t_steigst:.3f});')
tw(f'tl.fromTo("#s2-st",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:.6,ease:"sine.out"}},{t_jemand:.3f});')
move("#s2-st", t_jemand + 0.4, 0.8, "sine.out", x=40)
move("#s2-bus", t_jemand + 1.2, 1.6, "power2.in", x=-1300)
tw(f'tl.to("#s2-fig-eyes-n",{{opacity:0,duration:.15}},{t_hinter:.3f});'); tw(f'tl.to("#s2-fig-eyes-w",{{opacity:1,duration:.15}},{t_hinter:.3f});')

# S3 Schritte: du läufst, er hinten
S0, S1 = t_hoerst, t_bestimmt
scene("s3", S0, S1, street("s3") + stalker("s3-st", 200, 1440, 0.55) + figure("s3-fig", 600, 1600, 1.15, eyes="w")
      + f'<g id="s3-tap1" opacity="0"><text x="90" y="1180" font-family="Poppins" font-weight="800" font-size="70" fill="{RED}" transform="rotate(-8 90 1180)">TAPP.</text></g>'
      + f'<g id="s3-tap2" opacity="0"><text x="150" y="1270" font-family="Poppins" font-weight="800" font-size="70" fill="{RED}" transform="rotate(6 150 1270)">TAPP.</text></g>')
scroll_street("s3", S0, S1)
walk_cycle("s3-fig", S0, S1); walk_cycle("s3-st", S0, S1, 0.6, 6)
pop("#s3-tap1", t_schritte); pop("#s3-tap2", t_schritte + 0.45)
fade_out("#s3-tap1", t_leiser + 0.4); fade_out("#s3-tap2", t_leiser + 0.5)
move("#s3-st", t_leiser, 1.0, "sine.inOut", x=60)


# S4 Karte von oben: abbiegen, er folgt
def city_map(mid):
    blocks = "".join(f'<rect x="{x}" y="{y}" width="230" height="230" rx="18" fill="#1a1c40"/>' for x in range(30, 1080, 290) for y in range(220, 1900, 290))
    roof = "".join(f'<rect x="{x+30}" y="{y+30}" width="{RNG.randint(60,170)}" height="{RNG.randint(60,170)}" rx="8" fill="#222452"/>' for x in range(30, 1080, 290) for y in range(220, 1900, 290))
    return (f'<rect width="1080" height="1920" fill="#2b2d58"/>{blocks}{roof}'
            + "".join(f'<rect x="{x}" y="0" width="4" height="1920" fill="#3d3f72" opacity=".6"/>' for x in range(-5, 1080, 290))
            + f'<g opacity=".5">' + "".join(f'<circle cx="{x}" cy="{y}" r="5" fill="{LAMP}"/>' for x in range(-5, 1080, 290) for y in range(200, 1920, 145)) + '</g>')


def dot(did, x, y, col, lab):
    return (f'<g id="{did}"><circle cx="{x}" cy="{y}" r="60" fill="{col}" opacity=".18"/><circle cx="{x}" cy="{y}" r="30" fill="{col}" stroke="#fff" stroke-width="6"/>'
            f'<text x="{x}" y="{y-58}" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="34" fill="{col}">{lab}</text></g>')


S0, S1 = t_bestimmt, t_gehst
scene("s4", S0, S1, city_map("s4") + f'<path id="s4-path" d="M 555 1700 L 555 1080 L 260 1080" stroke="{TEAL}" stroke-width="10" stroke-dasharray="20 16" fill="none" opacity=".7"/>'
      + dot("s4-you", 555, 1500, TEAL, "DU") + dot("s4-him", 555, 1840, RED, "?"))
move("#s4-you", S0 + 0.1, t_biegst - S0, "sine.inOut", y=-420)
move("#s4-you", t_biegst, 1.0, "sine.inOut", x=-295)
move("#s4-him", S0 + 0.3, t_die_schr - S0 - 0.3, "sine.inOut", y=-760)
move("#s4-him", t_die_schr, 0.9, "sine.inOut", x=-120)

# S5 schneller: Tempo, er näher
S0, S1 = t_gehst, t_schauf
scene("s5", S0, S1, street("s5") + stalker("s5-st", 200, 1440, 0.55) + figure("s5-fig", 600, 1600, 1.15, eyes="w")
      + "".join(f'<rect id="s5-sl{i}" x="{1100}" y="{900+i*110}" width="{RNG.randint(120,260)}" height="6" rx="3" fill="#fff" opacity=".35"/>' for i in range(6)))
scroll_street("s5", S0, S1, 2.2)
walk_cycle("s5-fig", S0, S1, 0.36, 10); walk_cycle("s5-st", S0, S1, 0.38, 8)
tw(f'tl.to("#s5-st",{{scale:1.5,x:-60,y:80,svgOrigin:"200 1440",duration:{S1-t_erauch+0.2:.3f},ease:"power2.in"}},{t_erauch:.3f});')
for i in range(6):
    tw(f'tl.fromTo("#s5-sl{i}",{{x:0}},{{x:-1500,duration:.45,repeat:{int((S1-S0)/0.45)},ease:"none"}},{S0 + i*0.07:.3f});')

# S6 Schaufenster-Spiegelung
S0, S1 = t_schauf, t_dein
scene("s6", S0, S1, f'<rect width="1080" height="1920" fill="#0d0f26"/>'
      + f'<rect x="90" y="300" width="900" height="1300" rx="24" fill="#151843" stroke="#3a3c6a" stroke-width="16"/>'
      + f'<rect x="90" y="300" width="900" height="120" fill="#2a2d63"/><text x="540" y="385" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="64" fill="{LIME}" letter-spacing="6">ELEKTRO · MAX</text>'
      + "".join(f'<rect x="{x}" y="1200" width="{w}" height="{h}" rx="12" fill="#22265a"/>' for x, w, h in ((160, 200, 260), (420, 260, 200), (720, 200, 300)))
      + f'<g opacity=".55">{stalker("s6-st", 380, 1360, 1.15)}</g>'
      + f'<g opacity=".45">{figure("s6-fig", 760, 1500, 1.3, eyes="w", back=True)}</g>'
      + f'<polygon points="120,320 360,320 120,900" fill="#fff" opacity=".06"/><polygon points="600,320 760,320 300,1580 140,1580" fill="#fff" opacity=".05"/>'
      + label("s6-l1", 380, 820, "KAPUZE", RED, 40) + label("s6-l2", 380, 1460, "HÄNDE IN DEN TASCHEN", RED, 36)
      + f'<g id="s6-m" opacity="0"><line x1="380" y1="1680" x2="760" y2="1680" stroke="{RED}" stroke-width="6" stroke-dasharray="18 10"/>'
        f'<rect x="372" y="1660" width="8" height="40" fill="{RED}"/><rect x="760" y="1660" width="8" height="40" fill="{RED}"/>'
        f'<text x="570" y="1760" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="64" fill="{RED}">10 m</text></g>')
pop("#s6-l1", t_kapuze); pop("#s6-l2", t_haende); pop("#s6-m", t_zehn)

# S7 Gedanke: nach Hause rennen → Fehler → er weiß, wo du wohnst
S0, S1 = t_dein, t_polizei
house = lambda hid, x, y, s, op=1: (f'<g id="{hid}" opacity="{op}"><g transform="translate({x},{y}) scale({s})"><polygon points="-110,-20 0,-120 110,-20" fill="{LIME}"/>'
                                    f'<rect x="-90" y="-20" width="180" height="150" fill="#e6e9ee"/><rect x="-24" y="40" width="48" height="90" fill="#2c3a52"/>'
                                    f'<rect x="-70" y="10" width="36" height="36" fill="{WIN}"/><rect x="34" y="10" width="36" height="36" fill="{WIN}"/></g></g>')
scene("s7", S0, S1, f'<g id="s7-a">{street("s7")}{figure("s7-fig", 360, 1600, 1.15, eyes="w")}'
      + f'<g id="s7-th" opacity="0"><circle cx="500" cy="1080" r="18" fill="#e6e9ee"/><circle cx="570" cy="930" r="28" fill="#e6e9ee"/>'
        f'<ellipse cx="760" cy="640" rx="250" ry="190" fill="#e6e9ee"/>{house("s7-h1", 760, 660, 1.05)}</g>'
      + xmark("s7-x", 760, 640, 150) + '</g>'
      + f'<g id="s7-b" opacity="0">{city_map("s7m")}{house("s7-h2", 790, 520, 0.9)}'
      + f'<path d="M 230 1700 L 230 1240 L 790 1240 L 790 640" stroke="{TEAL}" stroke-width="10" stroke-dasharray="20 16" fill="none" opacity=".7"/>'
      + dot("s7-you", 230, 1700, TEAL, "DU") + dot("s7-him", 230, 1880, RED, "?")
      + f'<g id="s7-pin" opacity="0"><circle cx="790" cy="420" r="58" fill="{RED}"/><polygon points="750,450 830,450 790,520" fill="{RED}"/><circle cx="790" cy="420" r="22" fill="#fff"/></g></g>')
pop("#s7-th", t_dein + 0.15, 0.35, 0.6)
pop("#s7-x", t_fehler, 0.25, 1.4)
tw(f'tl.to("#s7-a",{{opacity:0,duration:.3}},{t_dann:.3f});'); tw(f'tl.to("#s7-b",{{opacity:1,duration:.3}},{t_dann:.3f});')
tw(f'tl.to("#s7-you",{{keyframes:[{{y:-460,duration:.5}},{{x:560,duration:.6}},{{y:-1060,duration:.5}}],ease:"none"}},{t_dann:.3f});')
tw(f'tl.to("#s7-him",{{keyframes:[{{y:-640,duration:.6}},{{x:560,duration:.6}},{{y:-1180,duration:.55}}],ease:"none"}},{t_dann + 0.2:.3f});')
pop("#s7-pin", t_wohnst)


# S8 „Die Polizei rät dir drei Regeln“
def card_bg(cid):
    return (f'<rect width="1080" height="1920" fill="{CARD_BG}"/><circle cx="540" cy="760" r="520" fill="url(#cardglow)"/>'
            + "".join(f'<rect x="{x}" y="0" width="2" height="1920" fill="#fff" opacity=".025"/>' for x in range(0, 1080, 60))
            + "".join(f'<rect x="0" y="{y}" width="1080" height="2" fill="#fff" opacity=".025"/>' for y in range(0, 1920, 60)))


S0, S1 = t_polizei, t_r1
shield = (f'<g id="s8-sh" opacity="0"><path d="M 540 470 L 760 540 L 740 820 Q 700 980 540 1050 Q 380 980 340 820 L 320 540 Z" fill="#1e2a6b" stroke="{BLUE}" stroke-width="12"/>'
          f'<polygon points="540,620 566,700 650,700 582,748 608,830 540,780 472,830 498,748 430,700 514,700" fill="{LIME}"/></g>')
scene("s8", S0, S1, card_bg("s8") + shield
      + f'<g id="s8-t" opacity="0"><text x="540" y="1460" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="120" fill="#fff">3 REGELN</text>'
        f'<text x="540" y="1540" text-anchor="middle" font-family="Poppins" font-weight="600" font-size="40" fill="{LIME}" letter-spacing="4">FÜR DEN HEIMWEG</text></g>')
pop("#s8-sh", S0 + 0.05, 0.4, 0.7); pop("#s8-t", t_drei)


def rule_card(sid, n, head, sub, icon):
    return (card_bg(sid)
            + f'<g id="{sid}-badge" opacity="0"><rect x="430" y="250" width="220" height="62" rx="12" fill="{RED}"/>'
              f'<text x="540" y="295" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="34" fill="#fff">REGEL #{n}</text></g>'
            + f'<g id="{sid}-head" opacity="0"><text x="540" y="430" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="88" fill="#fff">{head}</text></g>'
            + f'<g id="{sid}-sub" opacity="0"><text x="540" y="510" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="48" fill="{LIME}">{sub}</text></g>'
            + icon)


# R1: Teste es – Straßenseite wechseln
S0, S1 = t_r1, t_r2
road = (f'<rect x="140" y="640" width="800" height="760" rx="30" fill="#151843"/>'
        f'<rect x="140" y="640" width="190" height="760" fill="#25264a"/><rect x="750" y="640" width="190" height="760" fill="#25264a"/>'
        + "".join(f'<rect x="532" y="{y}" width="16" height="70" rx="6" fill="#d9dbe8" opacity=".6"/>' for y in range(670, 1400, 130)))
scene("r1", S0, S1, rule_card("r1", 1, "TESTE ES.", "Straßenseite wechseln", road
      + dot("r1-you", 235, 1150, TEAL, "DU") + dot("r1-him", 235, 1370, RED, "?")
      + f'<g id="r1-warn" opacity="0"><polygon points="840,560 920,700 760,700" fill="{RED}"/><rect x="832" y="600" width="16" height="56" rx="6" fill="#fff"/><circle cx="840" cy="680" r="9" fill="#fff"/></g>'))
pop("#r1-badge", S0); pop("#r1-head", t_teste); pop("#r1-sub", t_wechsel)
tw(f'tl.to("#r1-you",{{x:610,y:-120,duration:.9,ease:"sine.inOut"}},{t_wechsel + 0.2:.3f});')
tw(f'tl.to("#r1-him",{{x:610,y:-120,duration:.9,ease:"sine.inOut"}},{t_folgt:.3f});')
pop("#r1-warn", t_ernst, 0.3, 0.5)

# R2: Licht & Menschen
S0, S1 = t_r2, t_r3
icon = lambda iid, x, inner, lab: (f'<g id="{iid}" opacity="0"><circle cx="{x}" cy="1060" r="120" fill="#151843" stroke="{LIME}" stroke-width="6"/>{inner}'
                                   f'<text x="{x}" y="1240" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="36" fill="#fff">{lab}</text></g>')
pump = '<rect x="160" y="990" width="80" height="130" rx="10" fill="{L}"/><rect x="175" y="1010" width="50" height="34" rx="6" fill="#0b0d22"/><path d="M 240 1010 Q 280 1010 280 1060 L 280 1100" stroke="{L}" stroke-width="10" fill="none"/>'.replace("{L}", LIME)
kiosk = f'<rect x="470" y="1010" width="140" height="100" rx="8" fill="{LIME}"/><polygon points="455,1010 625,1010 600,960 480,960" fill="{RED}"/><rect x="500" y="1040" width="80" height="40" fill="#0b0d22"/>'
rest = f'<rect x="828" y="980" width="12" height="150" rx="6" fill="{LIME}"/><rect x="814" y="980" width="8" height="50" fill="{LIME}"/><rect x="846" y="980" width="8" height="50" fill="{LIME}"/><path d="M 900 980 Q 940 1020 905 1060 L 905 1130" stroke="{LIME}" stroke-width="12" fill="none"/>'
people = "".join(f'<g transform="translate({x},820) scale(.5)"><circle cx="0" cy="-60" r="34" fill="{WIN}"/><rect x="-40" y="-20" width="80" height="90" rx="30" fill="{WIN}"/></g>' for x in (470, 540, 610))
scene("r2", S0, S1, rule_card("r2", 2, "LICHT &amp; MENSCHEN", "da hingehen, wo was los ist",
      f'<g id="r2-ppl" opacity="0"><polygon points="540,600 600,600 700,900 380,900" fill="url(#lampcone)"/><ellipse cx="570" cy="600" rx="40" ry="14" fill="{LAMP}"/>{people}</g>'
      + '<g transform="translate(0,170)">' + icon("r2-i1", 200, pump, "Tankstelle") + icon("r2-i2", 540, kiosk, "Kiosk") + icon("r2-i3", 880, rest, "Restaurant") + '</g>'
      + house("r2-h", 540, 1640, 0.8, 0) + xmark("r2-x", 540, 1620, 120)))
pop("#r2-badge", S0); pop("#r2-head", t_licht - 0.6); pop("#r2-sub", t_licht); pop("#r2-ppl", t_licht)
pop("#r2-i1", t_tanke); pop("#r2-i2", t_kiosk); pop("#r2-i3", t_rest)
pop("#r2-h", t_nicht); pop("#r2-x", t_nicht + 0.3, 0.25, 1.4)

# R3: Ruf 110
S0, S1 = t_r3, t_du_w
phone_ic = (f'<g id="r3-ph" opacity="0"><rect x="400" y="640" width="280" height="520" rx="46" fill="#1e2a6b" stroke="{LIME}" stroke-width="8"/>'
            f'<text x="540" y="900" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="110" fill="#fff">110</text>'
            f'<circle cx="540" cy="1060" r="52" fill="#2ecc71"/><path d="M 515 1045 q 25 40 55 30" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round"/></g>')
wave = "".join(f'<rect id="r3-w{i}" x="{250+i*45}" y="{1360-h/2}" width="22" height="{h}" rx="11" fill="{LIME}" opacity="0"/>' for i, h in enumerate([40, 90, 150, 70, 120, 180, 100, 60, 140, 80, 50, 30]))
scene("r3", S0, S1, rule_card("r3", 3, "RUF 110.", "und bleib in der Leitung", '<g transform="translate(0,400)">' + phone_ic + '</g><g transform="translate(0,360)">' + wave + '</g>'))
pop("#r3-badge", S0); pop("#r3-head", t_ruf); pop("#r3-ph", t_ruf, 0.35, 0.7); pop("#r3-sub", t_bleib)
for i in range(12):
    tw(f'tl.fromTo("#r3-w{i}",{{opacity:.9,scaleY:.3,transformOrigin:"50% 50%"}},{{scaleY:1,duration:.25,yoyo:true,repeat:{int((S1-t_leitung)/0.25)},ease:"sine.inOut"}},{t_leitung + i*0.04:.3f});')

# S9 Test: Straßenseite wechseln, er auch
S0, S1 = t_du_w, t_vorne
scene("s9", S0, S1, city_map("s9") + f'<rect x="440" y="0" width="230" height="1920" fill="#151843"/>'
      + "".join(f'<rect x="547" y="{y}" width="16" height="70" rx="6" fill="#d9dbe8" opacity=".5"/>' for y in range(0, 1920, 130))
      + dot("s9-you", 400, 1300, TEAL, "DU") + dot("s9-him", 400, 1640, RED, "?")
      + label("s9-ok", 540, 520, "REGEL #1  ✓  ER FOLGT DIR", RED, 40))
tw(f'tl.to("#s9-you",{{x:310,y:-160,duration:.9,ease:"sine.inOut"}},{S0 + 0.1:.3f});')
tw(f'tl.to("#s9-him",{{x:310,y:-200,duration:.9,ease:"sine.inOut"}},{t_er2:.3f});')
pop("#s9-ok", t_er2 + 0.3)

# S10 Tankstelle außen → innen, laut um Hilfe bitten
S0, S1 = t_vorne, t_waehlst
station = (f'<g id="s10-out"><rect x="0" y="0" width="1080" height="1920" fill="url(#skyg)"/>'
           f'<rect x="80" y="760" width="920" height="70" rx="12" fill="#e6e9ee"/><rect x="80" y="760" width="920" height="22" fill="{RED}"/>'
           f'<rect x="80" y="830" width="920" height="40" fill="#fff4c9" opacity=".95"/><rect x="0" y="870" width="1080" height="700" fill="url(#stationglow)"/>'
           f'<rect x="150" y="870" width="24" height="560" fill="#c9ccd8"/><rect x="906" y="870" width="24" height="560" fill="#c9ccd8"/>'
           f'<rect x="300" y="1150" width="110" height="280" rx="14" fill="#e6e9ee"/><rect x="320" y="1180" width="70" height="60" rx="8" fill="#0b0d22"/>'
           f'<rect x="640" y="980" width="340" height="450" rx="10" fill="#fff4c9" opacity=".9"/><rect x="640" y="980" width="340" height="60" fill="{LIME}"/>'
           f'<text x="810" y="1022" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="36" fill="#0b0d22">24 h SHOP</text>'
           f'<rect x="760" y="1150" width="110" height="280" fill="#cfe7ff" opacity=".8"/>'
           f'<rect x="0" y="1430" width="1080" height="490" fill="#222452"/>'
           + figure("s10-fig", 540, 1690, 1.1, eyes="w", back=True) + '</g>')
inside = (f'<g id="s10-in" opacity="0"><rect width="1080" height="1920" fill="#2b2f5e"/>'
          + "".join(f'<rect x="{x}" y="{y}" width="150" height="40" rx="6" fill="{c}"/>' for x in (60, 230, 400) for y, c in ((700, LIME), (780, RED), (860, "#3b6cff"), (940, WIN)))
          + f'<rect x="0" y="560" width="1080" height="30" fill="#fff4c9" opacity=".8"/>'
          + figure("s10-cash", 760, 1300, 1.0, eyes="n", outfit="vest")
          + f'<rect x="520" y="1220" width="560" height="320" rx="16" fill="#3b3f7a"/><rect x="520" y="1220" width="560" height="30" fill="#4a4f94"/>'
          + figure("s10-you", 280, 1720, 1.2, eyes="f")
          + f'<g id="s10-q" opacity="0"><rect x="70" y="400" width="940" height="200" rx="40" fill="#fff"/><polygon points="250,600 320,600 260,670" fill="#fff"/>'
            f'<text x="540" y="485" text-anchor="middle" font-family="Poppins" font-weight="700" font-style="italic" font-size="48" fill="#0b0d22">„Mir läuft ein Mann hinterher.</text>'
            f'<text x="540" y="555" text-anchor="middle" font-family="Poppins" font-weight="800" font-style="italic" font-size="52" fill="{RED}">Bitte helfen Sie mir!“</text></g></g>')
scene("s10", S0, S1, station + inside)
walk_cycle("s10-fig", S0, t_rein)
tw(f'tl.to("#s10-fig",{{y:-180,scale:.82,svgOrigin:"540 1690",duration:{t_rein-S0+0.3:.3f},ease:"sine.inOut"}},{S0:.3f});')
tw(f'tl.to("#s10-out",{{opacity:0,duration:.35}},{t_laut - 0.2:.3f});'); tw(f'tl.to("#s10-in",{{opacity:1,duration:.35}},{t_laut - 0.2:.3f});')
pop("#s10-q", t_mir, 0.35, 0.8)

# S11 Handy: 110 wählen
S0, S1 = t_waehlst, t_handy
digits = "".join(f'<g><circle cx="{x}" cy="{y}" r="74" fill="#ffffff" opacity=".12"/><text x="{x}" y="{y+22}" text-anchor="middle" font-family="Poppins" font-weight="500" font-size="64" fill="#fff">{d}</text></g>'
                 for d, (x, y) in zip("123456789", [(330 + 210*(i % 3), 1120 + 170*(i // 3)) for i in range(9)]))
scene("s11", S0, S1, f'<rect width="1080" height="1920" fill="#050611"/>'
      + f'<rect x="140" y="120" width="800" height="1700" rx="110" fill="#2b2470" stroke="#0e0f22" stroke-width="22"/>'
      + f'<rect x="440" y="160" width="200" height="54" rx="27" fill="#050611"/>'
      + f'<text x="540" y="420" text-anchor="middle" font-family="Poppins" font-weight="400" font-size="40" fill="#cfd3ff">Notruf</text>'
      + "".join(f'<text id="s11-d{i}" x="540" y="560" text-anchor="middle" font-family="Poppins" font-weight="600" font-size="140" fill="#fff" opacity="0">{t}</text>' for i, t in enumerate(["1", "11", "110"]))
      + digits
      + f'<g id="s11-call"><circle cx="540" cy="1680" r="80" fill="#2ecc71"/><path d="M 505 1660 q 35 56 78 44" stroke="#fff" stroke-width="16" fill="none" stroke-linecap="round"/></g>'
      + f'<g id="s11-ring" opacity="0"><text x="540" y="700" text-anchor="middle" font-family="Poppins" font-weight="500" font-size="44" fill="{LIME}">Verbinden …</text></g>', drift=False)
toggle("#s11-d0", S0 + 0.1, S0 + 0.35); toggle("#s11-d1", S0 + 0.35, S0 + 0.6); toggle("#s11-d2", S0 + 0.6)
tw(f'tl.fromTo("#s11-call",{{scale:1}},{{scale:1.12,transformOrigin:"50% 50%",duration:.2,yoyo:true,repeat:1}},{S0 + 0.8:.3f});')
pop("#s11-ring", S0 + 1.1)
tw(f'tl.fromTo("#s11-ring",{{opacity:1}},{{opacity:.35,duration:.5,yoyo:true,repeat:{int((S1-S0)/0.5)},ease:"sine.inOut"}},{S0 + 1.4:.3f});')

# S12 AML-Diagramm
S0, S1 = t_handy, t_draussen
sat = lambda sid, x, y: (f'<g id="{sid}" opacity="0"><rect x="{x-30}" y="{y-20}" width="60" height="40" rx="8" fill="#c9ccd8"/>'
                         f'<rect x="{x-110}" y="{y-14}" width="70" height="28" fill="{BLUE}"/><rect x="{x+40}" y="{y-14}" width="70" height="28" fill="{BLUE}"/></g>')
scene("s12", S0, S1, card_bg("s12")
      + sat("s12-s1", 220, 300) + sat("s12-s2", 860, 360)
      + f'<g id="s12-b1" opacity="0"><line x1="220" y1="330" x2="470" y2="1070" stroke="{LIME}" stroke-width="5" stroke-dasharray="14 12"/><line x1="860" y1="390" x2="610" y2="1070" stroke="{LIME}" stroke-width="5" stroke-dasharray="14 12"/></g>'
      + f'<g transform="translate(0,170)"><g id="s12-ph"><rect x="430" y="860" width="220" height="400" rx="36" fill="#2b2470" stroke="#fff" stroke-width="8"/><text x="540" y="1080" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="70" fill="#fff">110</text></g></g>'
      + f'<g transform="translate(0,170)"><g id="s12-wifi" opacity="0">' + "".join(f'<path d="M {170-r} {1050} A {r} {r} 0 0 1 {170+r} 1050" stroke="{LIME}" stroke-width="10" fill="none"/>' for r in (40, 80, 120)) + f'<circle cx="170" cy="1060" r="14" fill="{LIME}"/><text x="170" y="1130" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="34" fill="#fff">WLAN</text></g></g>'
      + f'<text id="s12-gpst" x="540" y="250" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="34" fill="#fff" opacity="0">GPS</text>'
      + f'<g transform="translate(0,150)"><g id="s12-arrow" opacity="0"><line x1="540" y1="1290" x2="540" y2="1420" stroke="{LIME}" stroke-width="10"/><polygon points="510,1410 570,1410 540,1450" fill="{LIME}"/></g></g>'
      + f'<g transform="translate(540,1700) scale(.72) translate(-540,-1625)"><g id="s12-mon" opacity="0"><rect x="250" y="1460" width="580" height="330" rx="22" fill="#151843" stroke="#c9ccd8" stroke-width="8"/>'
        f'<rect x="270" y="1480" width="540" height="250" fill="#2b2d58"/>' + "".join(f'<rect x="{x}" y="{y}" width="110" height="70" rx="6" fill="#1a1c40"/>' for x in range(285, 800, 130) for y in range(1495, 1720, 90))
      + f'<circle id="s12-pin" cx="540" cy="1590" r="22" fill="{RED}"/><circle cx="540" cy="1590" r="46" fill="{RED}" opacity=".25"/>'
        f'<text x="540" y="1772" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="30" fill="{LIME}">LEITSTELLE · Standort empfangen</text></g></g>'
      + label("s12-aml", 540, 600, "AML = Advanced Mobile Location", LIME, 40), drift=True)
pop("#s12-mon", t_leitst); pop("#s12-arrow", t_standort)
tw(f'tl.fromTo("#s12-pin",{{scale:.4,transformOrigin:"50% 50%"}},{{scale:1.3,duration:.4,yoyo:true,repeat:{int((S1-t_standort)/0.4)},ease:"sine.inOut"}},{t_standort:.3f});')
pop("#s12-s1", t_gps); pop("#s12-s2", t_gps + 0.15); pop("#s12-b1", t_gps + 0.3); pop("#s12-gpst", t_gps)
pop("#s12-wifi", t_wlan)
tw(f'tl.fromTo("#s12-ph",{{rotation:-4,svgOrigin:"540 1060"}},{{rotation:4,svgOrigin:"540 1060",duration:.12,yoyo:true,repeat:5}},{t_ohne:.3f});')
pop("#s12-aml", t_aml)

# S13 Er steht draußen hinter der Scheibe
S0, S1 = t_draussen, t_also
scene("s13", S0, S1, f'<rect width="1080" height="1920" fill="#2b2f5e"/>'
      + f'<g><rect x="60" y="240" width="960" height="1100" rx="10" fill="url(#skyg)"/>{lamps("s13-l", 1340, 1080, 600)}'
      + f'<rect x="60" y="1200" width="960" height="140" fill="#1d1e3e"/>{stalker("s13-st", 640, 1300, 1.0)}</g>'
      + f'<polygon points="80,260 300,260 80,700" fill="#fff" opacity=".08"/><polygon points="600,260 700,260 260,1330 160,1330" fill="#fff" opacity=".05"/>'
      + f'<rect x="60" y="240" width="960" height="1100" rx="10" fill="none" stroke="#c9ccd8" stroke-width="22"/><rect x="530" y="240" width="20" height="1100" fill="#c9ccd8"/>'
      + f'<rect x="0" y="1340" width="1080" height="580" fill="#3b3f7a"/>' + figure("s13-you", 300, 1830, 1.25, eyes="w", back=True))
tw(f'tl.fromTo("#s13-st",{{opacity:0,x:200}},{{opacity:1,x:0,duration:.9,ease:"sine.out"}},{S0:.3f});')
tw(f'tl.to("#s13-st",{{scale:1.18,svgOrigin:"640 1300",duration:{S1-t_scheibe:.3f},ease:"sine.inOut"}},{t_scheibe:.3f});')

# S14 Wahl
S0, S1 = t_also, t_teil2
scene("s14", S0, S1, f'<rect width="1080" height="1920" fill="#1d1e44"/><circle cx="540" cy="760" r="560" fill="url(#cardglow)"/>'
      + figure("s14-fig", 540, 1520, 1.3, eyes="w")
      + pill("s14-p1", 540, 640, "DRINNEN WARTEN", LIME, "#0b0d22") + pill("s14-p2", 540, 800, "ABHOLEN LASSEN", BLUE)
      + f'<text x="540" y="520" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="40" fill="#cfd3ff" id="s14-or" opacity="0">Was machst du?</text>')
pop("#s14-or", S0 + 0.1); pop("#s14-p1", t_drinnen); pop("#s14-p2", t_abholt - 0.5)
tw(f'tl.to("#s14-fig",{{x:-60,duration:.9,ease:"sine.inOut",yoyo:true,repeat:1}},{t_drinnen:.3f});')

# S15 Teil-2-Karte
S0, S1 = t_teil2, TOTAL
fog = "".join(f'<ellipse id="s15-f{i}" cx="{RNG.randint(0,1080)}" cy="{RNG.randint(300,1700)}" rx="{RNG.randint(300,520)}" ry="{RNG.randint(90,170)}" fill="#8a8fb8" opacity=".09"/>' for i in range(10))
scene("s15", S0, S1, f'<rect width="1080" height="1920" fill="#14152e"/>{fog}'
      + f'<text x="540" y="450" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="36" fill="#cfd3ff" letter-spacing="14">HEIMWEG</text>'
      + f'<g id="s15-t" opacity="0"><text x="540" y="680" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="230" fill="{RED}" filter="url(#glow)">TEIL 2</text></g>'
      + f'<g id="s15-s" opacity="0"><text x="540" y="1250" text-anchor="middle" font-family="Poppins" font-weight="600" font-size="44" fill="#fff">Der versteckte Notruf-Knopf</text>'
        f'<text x="540" y="1310" text-anchor="middle" font-family="Poppins" font-weight="600" font-size="44" fill="#fff">in deinem Handy</text></g>'
      + f'<g id="s15-b" opacity="0"><rect x="330" y="1400" width="420" height="80" rx="40" fill="none" stroke="#fff" stroke-width="5"/>'
        f'<text x="540" y="1453" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="34" fill="#fff" letter-spacing="3">FOLGE FÜR TEIL 2</text></g>')
pop("#s15-t", S0 + 0.1, 0.5, 1.3); pop("#s15-s", t_knopf); pop("#s15-b", t_knopf + 0.8)
for i in range(10):
    tw(f'tl.fromTo("#s15-f{i}",{{x:0}},{{x:{RNG.choice([-1,1])*RNG.randint(80,200)},duration:{S1-S0:.3f},ease:"sine.inOut"}},{S0:.3f});')

# ================= SERIEN-BRANDING OBEN LINKS (Format B) =================
BRAND = [  # (start, ende, uhrzeit, ort)
    (0.0, t_dein, "23:47", "BUSHALTESTELLE"), (t_bestimmt, t_schauf, "23:48", "HAUPTSTRASSE"), (t_schauf, t_polizei, "23:49", "SCHAUFENSTER"),
    (t_du_w, t_vorne, "23:50", "HAUPTSTRASSE"), (t_vorne, t_waehlst, "23:51", "TANKSTELLE"), (t_waehlst, t_handy, "23:51", "TANKSTELLE · NOTRUF"),
    (t_draussen, t_teil2, "23:52", "TANKSTELLE"),
]
BRAND = [(a, b if i + 1 >= len(BRAND) or BRAND[i+1][0] >= b else BRAND[i+1][0], c, d) for i, (a, b, c, d) in enumerate(BRAND)]
brand_html = []
for i, (a, b, clock, place) in enumerate(BRAND):
    brand_html.append(
        f'<div id="br{i}" class="clip ov" data-start="{a:.3f}" data-duration="{b-a:.3f}" data-track-index="7" style="z-index:12">'
        f'<svg viewBox="0 0 1080 1920" width="1080" height="1920"><g transform="translate(70,190)">'
        f'<circle cx="8" cy="-6" r="8" fill="{RED}"/><text x="26" y="2" font-family="JetBrains Mono, monospace" font-weight="700" font-size="24" fill="#cfd3ff" letter-spacing="4">HEIMWEG · TEIL 1</text>'
        f'<text x="0" y="96" font-family="JetBrains Mono, monospace" font-weight="800" font-size="96" fill="{RED}" filter="url(#glowsoft)">{clock}</text>'
        f'<text x="{len(clock)*58+10}" y="96" font-family="JetBrains Mono, monospace" font-weight="700" font-size="26" fill="{RED}">UHR</text>'
        f'<text x="2" y="140" font-family="JetBrains Mono, monospace" font-weight="700" font-size="22" fill="#8f94c4" letter-spacing="4">{place}</text></g></svg></div>')

# ================= UNTERTITEL (Skill 7 + Format B: Akzent Neon-Gelbgrün) =================
KEY = {"MANN", "HINTERHERLÄUFT", "BUS", "SCHRITTE", "LEISER", "ZUFALL", "SCHNELLER", "KAPUZE", "TASCHEN", "ZEHN", "FEHLER", "WOHNST",
       "DREI", "REGELN", "TESTE", "STRASSENSEITE", "ERNST", "LICHT", "MENSCHEN", "TANKSTELLE", "KIOSK", "RESTAURANT", "HUNDERTZEHN",
       "LEITUNG", "HELFEN", "STANDORT", "GPS", "WLAN", "AML", "SCHEIBE", "WEG", "POLIZEI", "ABHOLT", "NOTRUFKNOPF", "AUTOMATISCH"}
DISPLAY = {"Dreiundzwanzig": "23:47", "hundertzehn.": "110.", "hundertzehn": "110", "Zehn": "10"}
SKIP = {"siebenundvierzig."}


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


danger("ov-d1", t_gehst, t_dein)
danger("ov-d2", t_du_w, t_vorne)
danger("ov-d3", t_draussen, t_also)

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
    <title>Heimweg Teil 1</title>
    <script src="assets/gsap.min.js"></script>
    <style>
      :root {{ --ground: {SKY1}; --ink: #ffffff; --accent: {LIME}; --font-display: "Poppins", sans-serif; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: var(--ground); }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: var(--font-display); }}
      .scene, .ov {{ position: absolute; inset: 0; }}
      .ov {{ pointer-events: none; }}
      .scene svg {{ display: block; }}
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
