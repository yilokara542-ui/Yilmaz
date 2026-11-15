#!/usr/bin/env python3
"""Generator für index.html – Video 10 „Heimlicher Mitbewohner“ (Skill-Format A „Erklär-Story“).

Alle Zeiten kommen aus assets/words.json (wortgenaue Voiceover-Zeitstempel).
Aufruf: python3 build.py → index.html + assets/cues.json
"""
import json, re, html, os, math, random, zlib, struct, base64

HERE = os.path.dirname(os.path.abspath(__file__))
W = json.load(open(os.path.join(HERE, "assets/words.json"), encoding="utf-8"))
VO_END = W[-1]["e"]
TOTAL = round(VO_END + 1.6, 2)          # Schlussfrage steht noch kurz
XF = 0.3                                 # Überblendung zwischen Szenen
RNG = random.Random(10)

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
    if outfit == "shirt":   # Mann in Japan: helles Hemd, Krawatte, dunkle Hose
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
WALL = "#1c2230"; WALL2 = "#222a3a"; FLOOR = "#141922"; WOOD = "#3a2f2a"; FRIDGE = "#d9dee6"
SEPB = "#2a2118"

t_kommst = ws("Du", 4.3); t_alles = ws("Alles"); t_kuehl = ws("Kühlschrank"); t_joghurt = ws("Joghurt"); t_merk = ws("Merk", t_joghurt)
t_denkst = ws("denkst"); t_hab = ws("Hab"); t_naechsten = ws("Am", t_hab); t_saft = ws("Saftflasche"); t_halb = ws("halb")
t_doch = ws("Doch"); t_genau = ws("Genau", t_doch); t_japan = ws("Japan"); t_2008 = ws("zweitausendacht"); t_mann = ws("Einem")
t_essen = ws("Essen", t_mann); t_dabei = ws("Dabei"); t_ab = ws("ab", t_dabei + 0.5); t_niemand = ws("Niemand"); t_schl = ws("Schlüssel")
t_also1 = ws("Also"); t_kameras = ws("Kameras"); t_handy1 = ws("Handy", t_kameras)
t_aber = ws("Aber"); t_wann = ws("wann", t_aber)
t_erst = ws("Erstens"); t_bew = ws("Bewegungsmelder"); t_licht = ws("Licht", t_bew); t_waerme1 = ws("Wärme", t_licht)
t_zweit = ws("Zweitens"); t_mensch = ws("Mensch"); t_laeuft = ws("Läuft"); t_aendert = ws("ändert"); t_wbild = ws("Wärmebild")
t_dritt = ws("Drittens"); t_wacht = ws("wacht"); t_foto1 = ws("Foto", t_wacht); t_dunkel = ws("Dunkeln")
t_paar = ws("Ein", t_dunkel); t_vibr = ws("vibriert"); t_arbeit = ws("Arbeit")
t_auf = ws("Auf", t_arbeit); t_kueche2 = ws("Küche", t_auf); t_fremde = ws("fremde")
t_polizei = ws("Polizei"); t_tueren = ws("Türen"); t_versch = ws("verschlossen")
t_dann = ws("Dann", t_versch); t_oeffnen = ws("öffnen"); t_schrank = ws("Schrank", t_oeffnen)
t_darin = ws("Darin"); t_frau = ws("Frau"); t_matratze = ws("Matratze"); t_flaschen = ws("Plastikflaschen")
t_sie = ws("Sie", t_flaschen); t_jahr = ws("Jahr", t_sie); t_aufgef = ws("Aufgefallen"); t_fehlende = ws("fehlende")
t_also2 = ws("Also", t_fehlende); t_vermisst = ws("vermisst"); t_selbst = ws("selbst", t_vermisst)

SEPIA = set()   # Szenen im Archiv-Look (echter Fall 2008)


# ---------- Bausteine Innenraum ----------
def room(prefix, sep=False):
    w1 = "#2e2519" if sep else WALL; w2 = "#3a2d1f" if sep else WALL2; fl = "#1f170f" if sep else FLOOR
    tiles = "".join(f'<rect x="{x}" y="{y}" width="88" height="88" rx="4" fill="{w2}"/>' for x in range(30, 1080, 96) for y in range(700, 1300, 96))
    return (f'<rect width="1080" height="1920" fill="{w1}"/>{tiles}'
            f'<rect x="0" y="1300" width="1080" height="620" fill="{fl}"/>'
            + "".join(f'<rect x="0" y="{y}" width="1080" height="3" fill="#000" opacity=".25"/>' for y in range(1360, 1920, 80))
            + f'<rect x="0" y="1290" width="1080" height="14" fill="#000" opacity=".35"/>'
            + f'<polygon points="470,0 610,0 900,1300 180,1300" fill="url(#lampcone)" opacity=".7"/><rect x="480" y="0" width="120" height="22" rx="10" fill="{LAMP}"/>')


def fridge(fid, x, y, open_=False, items=True):
    """Kühlschrank: Tür (Gruppe {fid}-door) klappt per scaleX auf; Fächer mit Lebensmitteln."""
    shelf = ""
    if items:
        for k, sy in enumerate((y + 120, y + 280, y + 440)):
            shelf += f'<rect x="{x+20}" y="{sy+110}" width="300" height="10" fill="#c9d2de"/>'
        shelf += (f'<g id="{fid}-milk"><rect x="{x+40}" y="{y+150}" width="60" height="80" rx="8" fill="#f4f6fa"/><rect x="{x+40}" y="{y+150}" width="60" height="20" fill="{BLUE}"/></g>'
                  f'<g id="{fid}-yog"><rect x="{x+130}" y="{y+180}" width="64" height="50" rx="10" fill="#ffe28a"/><rect x="{x+126}" y="{y+172}" width="72" height="12" rx="6" fill="#ff8fb1"/></g>'
                  f'<rect id="{fid}-gap" x="{x+124}" y="{y+166}" width="76" height="70" rx="12" fill="none" stroke="{RED}" stroke-width="6" stroke-dasharray="12 8" opacity="0"/>'
                  f'<g id="{fid}-cheese"><polygon points="{x+220},{y+230} {x+300},{y+230} {x+300},{y+180}" fill="#ffd34d"/></g>'
                  f'<g id="{fid}-egg">' + "".join(f'<ellipse cx="{x+50+i*36}" cy="{y+370}" rx="15" ry="20" fill="#f6efe2"/>' for i in range(4)) + '</g>'
                  f'<g id="{fid}-juice"><rect x="{x+220}" y="{y+300}" width="70" height="130" rx="10" fill="none" stroke="#e6e9ee" stroke-width="5"/>'
                  f'<rect id="{fid}-jlev" x="{x+224}" y="{y+310}" width="62" height="116" rx="6" fill="#ff9b2f"/></g>'
                  f'<g id="{fid}-veg"><circle cx="{x+80}" cy="{y+530}" r="30" fill="#e74c3c"/><circle cx="{x+150}" cy="{y+530}" r="30" fill="#7ac74f"/><ellipse cx="{x+240}" cy="{y+535}" rx="48" ry="22" fill="#ff9b2f"/></g>')
    return (f'<g id="{fid}"><rect x="{x+12}" y="{y+16}" width="340" height="640" rx="26" fill="#000" opacity=".35"/>'
            f'<rect x="{x}" y="{y}" width="340" height="640" rx="26" fill="{FRIDGE}"/>'
            f'<rect x="{x+16}" y="{y+16}" width="308" height="608" rx="14" fill="#eaf4ff"/><rect x="{x+16}" y="{y+16}" width="308" height="608" rx="14" fill="url(#coldglow)"/>'
            f'{shelf}'
            f'<g id="{fid}-door"><rect x="{x}" y="{y}" width="340" height="640" rx="26" fill="{FRIDGE}" stroke="#aeb6c2" stroke-width="4"/>'
            f'<rect x="{x+290}" y="{y+180}" width="16" height="140" rx="8" fill="#aeb6c2"/>'
            f'<rect x="{x+40}" y="{y+60}" width="70" height="40" rx="6" fill="#ffcc4d" transform="rotate(-6 {x+75} {y+80})"/></g></g>')


def open_door(fid, x, t, dur=0.45):
    tw(f'tl.to("#{fid}-door",{{scaleX:-0.25,svgOrigin:"{x} 0",duration:{dur},ease:"power2.out"}},{t:.3f});')


def phone_frame(inner, x=540, y=960, s=1.0, pid="ph"):
    return (f'<g id="{pid}"><g transform="translate({x},{y}) scale({s}) translate(-540,-960)">'
            f'<rect x="200" y="200" width="680" height="1440" rx="100" fill="#0e0f22"/><rect x="220" y="220" width="640" height="1400" rx="84" fill="#1b2240"/>'
            f'<rect x="440" y="250" width="200" height="46" rx="23" fill="#0e0f22"/>{inner}</g></g>')


def cam_icon(cid, x, y, s=1.0, led=True):
    return (f'<g id="{cid}"><g transform="translate({x},{y}) scale({s})">'
            f'<rect x="-30" y="-150" width="60" height="110" rx="12" fill="#c9ccd8"/>'
            f'<rect x="-130" y="-60" width="260" height="150" rx="40" fill="#e6e9ee"/><circle cx="-20" cy="15" r="52" fill="#151a21"/><circle cx="-20" cy="15" r="30" fill="#2b3a6b"/><circle cx="-30" cy="5" r="9" fill="#fff" opacity=".7"/>'
            f'<path d="M 60 -10 A 36 36 0 0 1 132 -10 L 132 30 L 60 30 Z" fill="#f6f7fb" stroke="#aeb6c2" stroke-width="3"/>'
            + "".join(f'<line x1="{60+i*12}" y1="-6" x2="{60+i*12}" y2="30" stroke="#aeb6c2" stroke-width="2"/>' for i in range(1, 6))
            + (f'<circle id="{cid}-led" cx="100" cy="60" r="10" fill="{RED}" opacity=".25"/>' if led else "")
            + '</g></g>')


def house_icon(hid, x, y, s=1.0, op=1):
    return (f'<g id="{hid}" opacity="{op}"><g transform="translate({x},{y}) scale({s})"><polygon points="-110,-20 0,-120 110,-20" fill="{RED}"/>'
            f'<rect x="-90" y="-20" width="180" height="150" fill="#e6e9ee"/><rect x="-24" y="40" width="48" height="90" fill="#2c3a52"/>'
            f'<rect x="-70" y="10" width="36" height="36" fill="{WIN}"/><rect x="34" y="10" width="36" height="36" fill="{WIN}"/></g></g>')


def hud_day(hid, day, item, op=1):
    return (f'<g id="{hid}" opacity="{op}"><rect x="200" y="200" width="680" height="170" rx="30" fill="#0b0e12" fill-opacity=".9" stroke="#3a4452" stroke-width="5"/>'
            f'<text x="330" y="255" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="26" fill="#7d8896" letter-spacing="4">TAG</text>'
            f'<text x="330" y="335" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="80" fill="#fff">{day}</text>'
            f'<line x1="430" y1="225" x2="430" y2="345" stroke="#3a4452" stroke-width="4"/>'
            f'<text x="655" y="255" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="26" fill="#7d8896" letter-spacing="4">FEHLT</text>'
            f'<text id="{hid}-it" x="655" y="325" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="52" fill="{RED}" opacity="0">{item}</text></g>')


# ================= SZENEN =================
# A Hook: Haus im Querschnitt bei Nacht
S0, S1 = 0.0, t_kommst
rooms = (f'<rect x="140" y="760" width="800" height="900" fill="#262f42"/>'
         f'<polygon points="100,770 540,430 980,770" fill="#1a2030" stroke="#3a4452" stroke-width="10"/>'
         f'<rect x="140" y="1200" width="800" height="16" fill="#3a4452"/><rect x="530" y="770" width="16" height="890" fill="#3a4452"/>'
         f'<rect x="150" y="780" width="370" height="410" fill="#2d3850"/><rect x="556" y="780" width="374" height="410" fill="#1f2738"/>'
         f'<rect x="150" y="1226" width="370" height="424" fill="#33405c"/><rect x="556" y="1226" width="374" height="424" fill="#2a3349"/>'
         f'<polygon points="300,1226 380,1226 470,1650 210,1650" fill="url(#lampcone)"/><rect x="320" y="1226" width="40" height="16" fill="{LAMP}"/>'
         f'<rect x="200" y="1430" width="150" height="220" rx="12" fill="{FRIDGE}"/>'
         f'<rect x="620" y="1520" width="260" height="70" rx="20" fill="#5a6a8a"/><rect x="600" y="1060" width="300" height="90" rx="16" fill="#4a5a7a"/>'
         f'<rect x="200" y="840" width="120" height="300" fill="#151a24"/><rect x="200" y="840" width="120" height="70" fill="#0a0d14"/>'
         f'<rect id="a-gap" x="200" y="840" width="120" height="70" fill="none" stroke="{RED}" stroke-width="5" stroke-dasharray="10 8" opacity="0"/>'
         f'<rect x="420" y="600" width="240" height="150" fill="#0a0d14"/><rect x="0" y="1660" width="1080" height="260" fill="#10141a"/>')
scene("sa", S0, S1, f'<rect width="1080" height="1920" fill="url(#skyg)"/>'
      + "".join(f'<circle cx="{RNG.randint(0,1080)}" cy="{RNG.randint(0,600)}" r="2" fill="#fff" opacity="{RNG.uniform(.3,.8):.2f}"/>' for _ in range(50))
      + f'<circle cx="860" cy="260" r="64" fill="{MOON}"/><circle cx="860" cy="260" r="140" fill="url(#moonglow)"/>' + rooms
      + f'<g id="a-q" opacity="0"><circle cx="820" cy="560" r="70" fill="{RED}"/><text x="820" y="592" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="92" fill="#fff">?</text></g>')
pop("#a-q", 1.0)
tw(f'tl.fromTo("#a-gap",{{opacity:0}},{{opacity:1,duration:.4,yoyo:true,repeat:5,ease:"sine.inOut"}},{1.6:.3f});')

# B Kühlschrank Tag 1: Joghurt fehlt, „Merk dir das“
S0, S1 = t_kommst, t_denkst
scene("sb", S0, S1, room("sb") + fridge("b-fr", 120, 640) + figure("b-fig", 740, 1620, 1.25, eyes="n")
      + hud_day("b-hud", "1", "JOGHURT", 0)
      + f'<g id="b-merk" opacity="0"><rect x="560" y="420" width="420" height="96" rx="48" fill="{RED}"/><text x="770" y="484" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="46" fill="#fff">MERK DIR DAS</text></g>')
pop("#b-hud", S0 + 0.2)
open_door("b-fr", 120, t_kuehl)
tw(f'tl.set("#b-fr-yog",{{opacity:0}},{S0:.3f});')
tw(f'tl.fromTo("#b-fr-gap",{{opacity:0}},{{opacity:1,duration:.35,yoyo:true,repeat:{int((S1-t_joghurt)/0.35)},ease:"sine.inOut"}},{t_joghurt:.3f});')
toggle("#b-hud-it", t_joghurt)
pop("#b-merk", t_merk)
tw(f'tl.to("#b-fig-eyes-n",{{opacity:0,duration:.15}},{t_joghurt:.3f});'); tw(f'tl.to("#b-fig-eyes-w",{{opacity:1,duration:.15}},{t_joghurt:.3f});')

# C „Hab ich wohl selbst gegessen“
S0, S1 = t_denkst, t_naechsten
scene("sc", S0, S1, room("sc") + figure("c-fig", 420, 1640, 1.3, eyes="n")
      + f'<g id="c-th" opacity="0"><circle cx="560" cy="1060" r="18" fill="#e6e9ee"/><circle cx="620" cy="960" r="28" fill="#e6e9ee"/>'
        f'<ellipse cx="760" cy="700" rx="240" ry="190" fill="#e6e9ee"/>'
        f'<rect x="700" y="640" width="110" height="90" rx="16" fill="#ffe28a"/><rect x="692" y="626" width="126" height="20" rx="10" fill="#ff8fb1"/>'
        f'<text x="880" y="640" font-family="Poppins" font-weight="800" font-size="90" fill="#2c3a52">?</text></g>')
pop("#c-th", S0 + 0.1, 0.35, 0.6)
tw(f'tl.fromTo("#c-fig",{{rotation:0}},{{rotation:3,svgOrigin:"420 1640",duration:.5,yoyo:true,repeat:3,ease:"sine.inOut"}},{t_hab:.3f});')

# D Tag 2: Saft halb leer
S0, S1 = t_naechsten, t_doch
scene("sd", S0, S1, room("sd") + fridge("d-fr", 370, 640) + hud_day("d-hud", "2", "SAFT", 1)
      + f'<g id="d-half" opacity="0"><circle cx="830" cy="1000" r="74" fill="{RED}"/><text x="830" y="1028" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="76" fill="#fff">½</text></g>')
tw(f'tl.set("#d-fr-yog",{{opacity:0}},{S0:.3f});')
open_door("d-fr", 370, S0 + 0.3)
tw(f'tl.to("#d-fr-cheese",{{opacity:0,duration:.4}},{S0 + 1.0:.3f});')
tw(f'tl.to("#d-fr-jlev",{{scaleY:.5,svgOrigin:"0 1066",duration:.9,ease:"power2.inOut"}},{t_saft:.3f});')
toggle("#d-hud-it", t_saft); pop("#d-half", t_halb)

# E „Doch jetzt wird's unheimlich“ – Kalender springt zurück
S0, S1 = t_doch, t_genau
YEARS = ["2026", "2021", "2016", "2012", "2009", "2008"]
scene("se", S0, S1, f'<rect width="1080" height="1920" fill="#000"/>'
      + "".join(f'<rect x="537" y="300" width="6" height="200" fill="{RED}" opacity=".18" transform="rotate({a} 540 960)"/>' for a in range(0, 360, 15))
      + f'<rect id="e-flash" width="1080" height="1920" fill="{RED}" opacity="0"/>'
      + f'<g><rect x="290" y="560" width="500" height="520" rx="30" fill="#f2efe8"/><rect x="290" y="560" width="500" height="130" rx="30" fill="{RED}"/>'
        f'<circle cx="400" cy="560" r="20" fill="#333"/><circle cx="680" cy="560" r="20" fill="#333"/>'
      + "".join(f'<text id="e-y{i}" x="540" y="900" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="150" fill="#151a21" opacity="0">{y}</text>' for i, y in enumerate(YEARS))
      + '</g>')
tw(f'tl.fromTo("#e-flash",{{opacity:0}},{{opacity:.8,duration:.001,immediateRender:false}},{S0:.3f});')
tw(f'tl.fromTo("#e-flash",{{immediateRender:false}},{{opacity:0,duration:.35}},{S0+0.001:.3f});')
for i in range(len(YEARS)):
    a = S0 + (S1 - S0) * i / len(YEARS)
    toggle(f"#e-y{i}", a, S0 + (S1 - S0) * (i + 1) / len(YEARS) if i < len(YEARS) - 1 else None)

# F Japan 2008: Essen verschwindet (Archiv)
S0, S1 = t_genau, t_dabei
SEPIA.add("sf")
scene("sf", S0, S1, room("sf", True) + fridge("f-fr", 120, 640) + figure("f-man", 760, 1620, 1.25, eyes="w", outfit="shirt")
      + f'<g id="f-stamp" opacity="0"><rect x="420" y="380" width="580" height="200" rx="18" fill="#120d08" fill-opacity=".85" stroke="{RED}" stroke-width="10" transform="rotate(-5 710 480)"/>'
        f'<text x="710" y="460" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="42" fill="#e6d2ad" transform="rotate(-5 710 480)" letter-spacing="8">JAPAN</text>'
        f'<text x="710" y="550" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="96" fill="{RED}" transform="rotate(-5 710 480)">2008</text></g>')
open_door("f-fr", 120, S0 + 0.2)
tw(f'tl.fromTo("#f-stamp",{{opacity:0,scale:2.2,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:.22,ease:"power4.in"}},{t_japan:.3f});')
shake("#sf-cam", t_japan + 0.22, 5, 8)
for i, it in enumerate(("milk", "yog", "cheese", "egg", "veg")):
    tw(f'tl.to("#f-fr-{it}",{{opacity:0,y:-20,duration:.35,ease:"sine.in"}},{t_mann + 0.35 + i*0.42:.3f});')

# G Abschließen, nur ein Schlüssel
S0, S1 = t_dabei, t_also1
SEPIA.add("sg")
scene("sg", S0, S1, room("sg", True)
      + f'<rect x="300" y="420" width="480" height="880" rx="12" fill="#5a4630" stroke="#3a2d1f" stroke-width="16"/>'
      + "".join(f'<rect x="{x}" y="{y}" width="180" height="340" rx="10" fill="none" stroke="#4a3826" stroke-width="8"/>' for x in (340, 560) for y in (470, 860))
      + f'<circle cx="720" cy="860" r="22" fill="#c9a24b"/><rect x="700" y="900" width="40" height="80" rx="10" fill="#c9a24b"/><circle cx="720" cy="930" r="9" fill="#1a120a"/>'
      + f'<g id="g-key"><circle cx="880" cy="930" r="40" fill="none" stroke="#e6d2ad" stroke-width="16"/><rect x="740" y="922" width="100" height="16" fill="#e6d2ad"/><rect x="760" y="938" width="14" height="26" fill="#e6d2ad"/></g>'
      + f'<g id="g-lock" opacity="0"><rect x="430" y="1380" width="220" height="170" rx="26" fill="{RED}"/><path d="M 470 1380 L 470 1330 A 70 70 0 0 1 610 1330 L 610 1380" stroke="{RED}" stroke-width="26" fill="none"/>'
        f'<circle cx="540" cy="1455" r="20" fill="#fff"/></g>'
      + label("g-one", 540, 300, "NUR 1 SCHLÜSSEL", "#e6d2ad", 48))
tw(f'tl.fromTo("#g-key",{{x:120,opacity:0}},{{x:0,opacity:1,duration:.4,ease:"power2.out"}},{S0 + 0.1:.3f});')
tw(f'tl.to("#g-key",{{rotation:-90,svgOrigin:"720 930",duration:.35,ease:"power2.inOut"}},{t_ab - 0.2:.3f});')
pop("#g-lock", t_ab); pop("#g-one", t_schl)

# H Kameras, die Bilder aufs Handy schicken
S0, S1 = t_also1, t_aber
SEPIA.add("sh")
scene("sh", S0, S1, room("sh", True) + fridge("h-fr", 120, 640, items=False) + cam_icon("h-cam", 820, 520, 1.1)
      + "".join(f'<path id="h-w{i}" d="M {700-i*60} {760+i*60} A {90+i*60} {90+i*60} 0 0 1 {880+i*60} {700+i*60}" stroke="{RED}" stroke-width="10" fill="none" opacity="0"/>' for i in range(3))
      + phone_frame('<text x="540" y="900" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="90" fill="#fff">📷</text>', 760, 1450, 0.32, "h-ph"))
pop("#h-cam", t_kameras, 0.35, 0.6)
for i in range(3):
    tw(f'tl.fromTo("#h-w{i}",{{opacity:0}},{{opacity:.9,duration:.25,yoyo:true,repeat:{int((S1-t_handy1)/0.5)},ease:"sine.inOut"}},{t_handy1 - 0.4 + i*0.15:.3f});')
pop("#h-ph", t_handy1 - 0.3, 0.35, 0.7)


# I Frage: Woher weiß die Kamera …?
def card_bg(cid):
    return (f'<rect width="1080" height="1920" fill="#0b0e14"/><circle cx="540" cy="820" r="560" fill="url(#cardglow)"/>'
            + "".join(f'<rect x="{x}" y="0" width="2" height="1920" fill="#fff" opacity=".025"/>' for x in range(0, 1080, 60))
            + "".join(f'<rect x="0" y="{y}" width="1080" height="2" fill="#fff" opacity=".025"/>' for y in range(0, 1920, 60)))


S0, S1 = t_aber, t_erst
scene("si", S0, S1, card_bg("si") + cam_icon("i-cam", 540, 620, 2.0)
      + f'<g id="i-q" opacity="0"><circle cx="860" cy="1300" r="110" fill="{RED}"/><text x="860" y="1352" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="150" fill="#fff">?</text></g>'
      + f'<g id="i-ph">{phone_frame("", 300, 1360, 0.3, "i-ph2")}</g>')
pop("#i-q", t_wann, 0.35, 0.5)

# J Erstens: Bewegungsmelder – kein Licht, sondern Wärme
S0, S1 = t_erst, t_zweit
lens = "".join(f'<polygon points="{540+math.cos(a)*r1:.0f},{760+math.sin(a)*r1:.0f} {540+math.cos(a+0.5)*r1:.0f},{760+math.sin(a+0.5)*r1:.0f} {540+math.cos(a+0.5)*r2:.0f},{760+math.sin(a+0.5)*r2:.0f} {540+math.cos(a)*r2:.0f},{760+math.sin(a)*r2:.0f}" fill="#f6f7fb" stroke="#aeb6c2" stroke-width="3"/>'
               for r1, r2 in ((60, 140), (140, 220)) for a in [i*0.5 - 3.14 for i in range(7)])
scene("sj", S0, S1, card_bg("sj")
      + f'<g id="j-dome"><path d="M 300 760 A 240 240 0 0 1 780 760 Z" fill="#f6f7fb"/>{lens}<rect x="300" y="760" width="480" height="40" rx="10" fill="#c9ccd8"/>'
        f'<rect x="490" y="820" width="100" height="70" rx="10" fill="#2b3442"/><rect x="510" y="835" width="60" height="40" rx="6" fill="#ff6a3b"/></g>'
      + label("j-l", 540, 380, "1  BEWEGUNGSMELDER (PIR)", RED, 40)
      + f'<g id="j-sun" opacity="0"><circle cx="300" cy="1420" r="70" fill="{WIN}"/>' + "".join(f'<rect x="296" y="1310" width="8" height="40" fill="{WIN}" transform="rotate({a} 300 1420)"/>' for a in range(0, 360, 45)) + '</g>'
      + xmark("j-x", 300, 1420, 110)
      + f'<g id="j-heat" opacity="0"><path d="M 780 1500 Q 740 1440 780 1380 Q 820 1320 780 1270" stroke="#ff6a3b" stroke-width="16" fill="none" stroke-linecap="round"/>'
        f'<path d="M 840 1500 Q 800 1440 840 1380 Q 880 1320 840 1270" stroke="#ffb35c" stroke-width="16" fill="none" stroke-linecap="round"/>'
        f'<path d="M 720 1500 Q 680 1440 720 1380 Q 760 1320 720 1270" stroke="{RED}" stroke-width="16" fill="none" stroke-linecap="round"/>'
        f'<circle cx="780" cy="1580" r="40" fill="#2ecc71"/><path d="M 760 1580 l 14 14 l 26 -30" stroke="#fff" stroke-width="10" fill="none"/></g>'
      + f'<text x="300" y="1590" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="40" fill="#fff" id="j-t1" opacity="0">Licht</text>'
      + f'<text x="780" y="1690" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="40" fill="#fff" id="j-t2" opacity="0">Wärme</text>')
pop("#j-l", S0 + 0.05); tw(f'tl.fromTo("#j-dome",{{scale:.6,transformOrigin:"50% 100%"}},{{scale:1,duration:.5,ease:"power3.out"}},{S0:.3f});')
pop("#j-sun", t_licht - 0.2); pop("#j-t1", t_licht - 0.2); pop("#j-x", t_licht + 0.25, 0.25, 1.4)
pop("#j-heat", t_waerme1); pop("#j-t2", t_waerme1)

# K Zweitens: Wärmebild – Zonen leuchten auf, wenn jemand durchläuft
S0, S1 = t_zweit, t_dritt
zones = "".join(f'<polygon id="k-z{i}" points="540,300 {60+i*160},1800 {200+i*160},1800" fill="#3a3dff" opacity=".18"/>' for i in range(6))
heatman = (f'<g id="k-p"><defs></defs><ellipse cx="0" cy="-320" rx="70" ry="70" fill="url(#heatg)"/>'
           f'<rect x="-70" y="-260" width="140" height="170" rx="40" fill="url(#heatg)"/>'
           f'<rect x="-40" y="-100" width="30" height="120" rx="14" fill="url(#heatg)"/><rect x="10" y="-100" width="30" height="120" rx="14" fill="url(#heatg)"/></g>')
scene("sk", S0, S1, f'<rect width="1080" height="1920" fill="#070a2a"/>{zones}'
      + "".join(f'<rect x="0" y="{y}" width="1080" height="2" fill="#3a3dff" opacity=".2"/>' for y in range(320, 1900, 80))
      + cam_icon("k-cam", 540, 300, 0.8) + f'<g transform="translate(-200,1500)">{heatman}</g>'
      + label("k-l", 540, 560, "WÄRMEBILD", "#ffb35c", 40)
      + f'<text id="k-c" x="540" y="1760" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="40" fill="#ffb35c" opacity="0">36,5 °C</text>')
pop("#k-l", S0 + 0.1)
tw(f'tl.fromTo("#k-p",{{x:0}},{{x:1460,duration:{S1-t_laeuft:.3f},ease:"none"}},{t_laeuft:.3f});')
pop("#k-c", t_mensch)
for i in range(6):
    tc = t_laeuft + (S1 - t_laeuft) * (i + 0.6) / 6.6
    tw(f'tl.fromTo("#k-z{i}",{{opacity:.18}},{{opacity:.75,duration:.15,yoyo:true,repeat:1,ease:"sine.inOut"}},{tc:.3f});')

# L Drittens: Kamera wacht auf, Foto ans Handy – auch im Dunkeln
S0, S1 = t_dritt, t_paar
scene("sl", S0, S1, card_bg("sl") + cam_icon("l-cam", 540, 640, 1.8)
      + f'<rect id="l-flash" width="1080" height="1920" fill="#fff" opacity="0"/>'
      + f'<g id="l-photo" opacity="0"><rect x="380" y="1040" width="320" height="240" rx="12" fill="#e6e9ee"/><rect x="396" y="1056" width="288" height="180" fill="#2b3a6b"/>'
        f'<circle cx="540" cy="1130" r="26" fill="#ff6a3b" opacity=".8"/><rect x="520" y="1158" width="40" height="70" rx="12" fill="#ff6a3b" opacity=".8"/></g>'
      + phone_frame("", 860, 1560, 0.26, "l-ph")
      + f'<g id="l-moon" opacity="0"><circle cx="200" cy="1500" r="70" fill="{MOON}"/><circle cx="230" cy="1475" r="64" fill="#0b0e14"/></g>')
tw(f'tl.fromTo("#l-cam-led",{{opacity:.25}},{{opacity:1,duration:.2}},{t_wacht:.3f});')
tw(f'tl.fromTo("#l-flash",{{opacity:0}},{{opacity:.85,duration:.001,immediateRender:false}},{t_foto1:.3f});')
tw(f'tl.fromTo("#l-flash",{{immediateRender:false}},{{opacity:0,duration:.3}},{t_foto1+0.001:.3f});')
tw(f'tl.fromTo("#l-photo",{{opacity:0}},{{opacity:1,duration:.15,immediateRender:false}},{t_foto1 + 0.1:.3f});')
tw(f'tl.to("#l-photo",{{x:320,y:330,scale:.35,svgOrigin:"540 1160",duration:.6,ease:"power2.in"}},{t_foto1 + 0.5:.3f});')
pop("#l-moon", t_dunkel)

# M Handy vibriert bei der Arbeit → Foto: Küche + fremde Person
S0, S1 = t_paar, t_polizei
SEPIA.add("sm")
notif = (f'<g id="m-n" opacity="0"><rect x="250" y="560" width="580" height="150" rx="30" fill="#2b2f45" fill-opacity=".95"/>'
         f'<text x="290" y="620" font-family="Poppins" font-weight="700" font-size="30" fill="{RED}">● KAMERA · jetzt</text>'
         f'<text x="290" y="675" font-family="Poppins" font-weight="600" font-size="34" fill="#fff">Bewegung erkannt: Küche</text></g>')
camimg = (f'<g id="m-img" opacity="0"><rect x="240" y="760" width="600" height="760" rx="20" fill="#1c2a1c"/>'
          f'<rect x="260" y="780" width="560" height="720" fill="#2f4630"/><rect x="280" y="980" width="180" height="420" rx="10" fill="#4c6a4c"/>'
          f'<rect x="260" y="1380" width="560" height="120" fill="#253a26"/>'
          f'<g id="m-st" opacity="0" transform="translate(640,1420) scale(.6)"><ellipse cx="0" cy="-320" rx="60" ry="72" fill="#0b120b"/><path d="M -60 -330 Q -80 -200 -70 -150 L 70 -150 Q 80 -200 60 -330 Z" fill="#0b120b"/>'
          f'<rect x="-62" y="-262" width="124" height="160" rx="36" fill="#0b120b"/><rect x="-34" y="-110" width="27" height="110" rx="12" fill="#0b120b"/><rect x="7" y="-110" width="27" height="110" rx="12" fill="#0b120b"/></g>'
          f'<text x="280" y="820" font-family="JetBrains Mono" font-weight="700" font-size="28" fill="#cfe8c8">CAM 1 · KÜCHE</text>'
          f'<text x="800" y="820" text-anchor="end" font-family="JetBrains Mono" font-weight="700" font-size="28" fill="#cfe8c8">14:07:33</text>'
          f'<circle cx="790" cy="1470" r="10" fill="{RED}"/></g>')
scene("sm", S0, S1, f'<rect width="1080" height="1920" fill="#1a140e"/>'
      + "".join(f'<rect x="{x}" y="1500" width="200" height="420" fill="#2e2519"/>' for x in (0, 880))
      + f'<rect x="0" y="1400" width="1080" height="40" fill="#3a2d1f"/>'
      + phone_frame(notif + camimg + '<text x="540" y="470" text-anchor="middle" font-family="Poppins" font-weight="300" font-size="120" fill="#fff">14:07</text>', 540, 960, 0.92, "m-ph"), drift=True)
pop("#m-n", t_vibr)
tw(f'tl.fromTo("#m-ph",{{rotation:-2,svgOrigin:"540 960"}},{{rotation:2,svgOrigin:"540 960",duration:.07,yoyo:true,repeat:9,ease:"none"}},{t_vibr:.3f});')
tw(f'tl.to("#m-ph",{{rotation:0,svgOrigin:"540 960",duration:.1}},{t_vibr + 0.75:.3f});')
pop("#m-img", t_auf); pop("#m-st", t_fremde, 0.5, 1.0)
tw(f'tl.to("#m-img",{{scale:1.08,svgOrigin:"540 1140",duration:{S1-t_fremde:.3f},ease:"sine.inOut"}},{t_fremde:.3f});')

# N Polizei durchsucht das Haus – Türen & Fenster verschlossen
S0, S1 = t_polizei, t_dann
SEPIA.add("sn")
lock = lambda lid, x, y: (f'<g id="{lid}" opacity="0"><rect x="{x-40}" y="{y}" width="80" height="64" rx="12" fill="{RED}"/><path d="M {x-24} {y} L {x-24} {y-24} A 24 24 0 0 1 {x+24} {y-24} L {x+24} {y}" stroke="{RED}" stroke-width="12" fill="none"/></g>')
scene("sn", S0, S1, f'<rect width="1080" height="1920" fill="#0d0a07"/>'
      + f'<rect x="80" y="620" width="340" height="700" rx="10" fill="#2e2519" stroke="#4a3826" stroke-width="12"/><circle cx="380" cy="980" r="16" fill="#c9a24b"/>'
      + f'<rect x="560" y="640" width="420" height="380" fill="#151a2a" stroke="#4a3826" stroke-width="14"/><rect x="764" y="640" width="12" height="380" fill="#4a3826"/><rect x="560" y="824" width="420" height="12" fill="#4a3826"/>'
      + f'<rect x="0" y="1320" width="1080" height="600" fill="#1f170f"/>'
      + f'<polygon id="n-beam" points="540,1900 300,600 780,600" fill="#fff4c9" opacity=".18"/>'
      + lock("n-l1", 250, 520) + lock("n-l2", 770, 540)
      + label("n-v", 540, 1500, "VERSCHLOSSEN", RED, 52))
tw(f'tl.fromTo("#n-beam",{{rotation:-25,svgOrigin:"540 1900"}},{{rotation:25,svgOrigin:"540 1900",duration:1.4,yoyo:true,repeat:2,ease:"sine.inOut"}},{S0:.3f});')
pop("#n-l1", t_tueren); pop("#n-l2", t_tueren + 0.3); pop("#n-v", t_versch)

# O Der oberste Schrank: Matratze, Flaschen, eine Frau
S0, S1 = t_dann, t_sie
SEPIA.add("so")
inside = (f'<rect x="210" y="430" width="660" height="300" fill="#120d08"/>'
          f'<g id="o-in" opacity="0"><rect x="230" y="640" width="620" height="70" rx="20" fill="#c9b79a"/>'
          f'<g transform="translate(560,690) rotate(-90) scale(.55)"><ellipse cx="0" cy="4" rx="78" ry="15" fill="#000" opacity=".3"/>'
          f'<rect x="-34" y="-128" width="27" height="124" rx="12" fill="#4a4a5a"/><rect x="7" y="-128" width="27" height="124" rx="12" fill="#4a4a5a"/>'
          f'<rect x="-62" y="-258" width="124" height="152" rx="36" fill="#7a6a8a"/><rect x="-12" y="-278" width="24" height="26" rx="8" fill="{FIG}"/>'
          f'<circle cx="0" cy="-320" r="64" fill="{FIG}"/><path d="M -60 -330 Q -64 -400 0 -392 Q 64 -400 60 -330 Q 50 -370 0 -372 Q -50 -370 -60 -330 Z" fill="#2a2016"/>'
          f'<rect x="-34" y="-324" width="22" height="6" rx="3" fill="{INK}"/><rect x="12" y="-324" width="22" height="6" rx="3" fill="{INK}"/></g>'
          + "".join(f'<rect x="{x}" y="540" width="34" height="96" rx="10" fill="#cfe7ff" opacity=".85"/><rect x="{x+9}" y="528" width="16" height="16" fill="#3b6cff"/>' for x in (720, 770, 820))
          + '</g>')
scene("so", S0, S1, f'<rect width="1080" height="1920" fill="#1a140e"/>'
      + f'<rect x="180" y="400" width="720" height="1460" fill="#5a4630" stroke="#3a2d1f" stroke-width="14"/>{inside}'
      + f'<rect x="180" y="750" width="720" height="16" fill="#3a2d1f"/>'
      + "".join(f'<rect x="{x}" y="790" width="340" height="1050" rx="8" fill="none" stroke="#4a3826" stroke-width="8"/>' for x in (200, 540))
      + f'<g id="o-door"><rect x="190" y="410" width="700" height="330" fill="#6a5438" stroke="#3a2d1f" stroke-width="8"/><circle cx="540" cy="700" r="14" fill="#c9a24b"/></g>'
      + f'<polygon id="o-beam" points="540,1920 160,420 920,420" fill="#fff4c9" opacity="0"/>'
      + label("o-l1", 310, 300, "MATRATZE", "#e6d2ad", 38) + label("o-l2", 760, 300, "PLASTIKFLASCHEN", "#e6d2ad", 34))
tw(f'tl.to("#o-door",{{scaleY:.05,svgOrigin:"540 410",duration:.5,ease:"power2.inOut"}},{t_oeffnen:.3f});')
tw(f'tl.fromTo("#o-beam",{{opacity:0}},{{opacity:.22,duration:.4}},{t_oeffnen + 0.3:.3f});')
tw(f'tl.fromTo("#o-in",{{opacity:0}},{{opacity:1,duration:.5}},{t_darin:.3f});')
pop("#o-l1", t_matratze); pop("#o-l2", t_flaschen)

# P Ein Jahr – und das fehlende Essen (Payoff)
S0, S1 = t_sie, t_also2
SEPIA.add("sp")
DAYS = ["1", "30", "90", "180", "270", "365"]
scene("sp", S0, S1, card_bg("sp")
      + f'<g id="p-cal"><rect x="290" y="420" width="500" height="520" rx="30" fill="#f2efe8"/><rect x="290" y="420" width="500" height="130" rx="30" fill="{RED}"/>'
        f'<text x="540" y="510" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="56" fill="#fff">TAG</text>'
      + "".join(f'<text id="p-d{i}" x="540" y="800" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="170" fill="#151a21" opacity="0">{d}</text>' for i, d in enumerate(DAYS)) + '</g>'
      + f'<g id="p-yog" opacity="0"><rect x="400" y="1180" width="280" height="220" rx="40" fill="#ffe28a"/><rect x="380" y="1150" width="320" height="50" rx="25" fill="#ff8fb1"/>'
        f'<rect x="380" y="1140" width="320" height="270" rx="40" fill="none" stroke="{RED}" stroke-width="10" stroke-dasharray="22 14"/></g>'
      + label("p-l", 540, 1560, "DAS FEHLENDE ESSEN", RED, 48))
for i in range(len(DAYS)):
    a = S0 + 0.2 + (t_aufgef - S0 - 0.2) * i / len(DAYS)
    toggle(f"#p-d{i}", a, S0 + 0.2 + (t_aufgef - S0 - 0.2) * (i + 1) / len(DAYS) if i < len(DAYS) - 1 else None)
pop("#p-yog", t_aufgef + 0.4, 0.4, 0.6); pop("#p-l", t_fehlende)

# Q Ende: zurück in deiner Küche – Ja / Nein
S0, S1 = t_also2, TOTAL
scene("sq", S0, S1, room("sq") + fridge("q-fr", 120, 640) + figure("q-fig", 760, 1640, 1.25, eyes="w")
      + pill("q-p1", 380, 470, "JA", RED) + pill("q-p2", 700, 470, "NEIN", "#3a4452"))
tw(f'tl.set("#q-fr-yog",{{opacity:0}},{S0:.3f});')
open_door("q-fr", 120, S0 + 0.2)
tw(f'tl.fromTo("#q-fr-gap",{{opacity:0}},{{opacity:1,duration:.35,yoyo:true,repeat:{int((S1-S0)/0.35)},ease:"sine.inOut"}},{S0 + 0.6:.3f});')
pop("#q-p1", t_vermisst); pop("#q-p2", t_vermisst + 0.3)
tw(f'tl.to("#q-fig",{{y:-12,duration:.6,ease:"sine.inOut",yoyo:true,repeat:3}},{t_selbst:.3f});')

brand_html = []

# ================= UNTERTITEL (Skill 7, Format A: Akzent Rot) =================
KEY = {"JAHRELANG", "HEIMLICH", "JOGHURT", "MERK", "SELBST", "HALB", "LEER", "UNHEIMLICH", "WIRKLICH", "JAPAN", "ZWEITAUSENDACHT",
       "ESSEN", "ABSCHLIESST", "SCHLÜSSEL", "KAMERAS", "HANDY", "BEWEGUNGSMELDER", "LICHT", "WÄRME", "WÄRMEBILD", "FOTO", "DUNKELN",
       "VIBRIERT", "FREMDE", "PERSON", "VERSCHLOSSEN", "SCHRANK", "FRAU", "MATRATZE", "PLASTIKFLASCHEN", "JAHR", "FEHLENDE", "VERMISST"}
DISPLAY = {"zweitausendacht.": "2008."}
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


danger("ov-d1", t_fremde, t_polizei)
danger("ov-d2", t_darin, t_sie)


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


archive("ov-arch1", t_genau, t_aber)
archive("ov-arch2", t_paar, t_also2)

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
    <title>Heimlicher Mitbewohner</title>
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
