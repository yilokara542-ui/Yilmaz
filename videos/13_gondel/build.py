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
t_drei0 = ws("drei"); t_tausend = ws("tausend"); t_luft = ws("Luft")
t_gondel = ws("Gondel"); t_schlucht = ws("Schlucht"); t_bewegt = ws("bewegt")
t_handy = ws("Handy"); t_hoehe = ws("Höhe"); t_luftdruck = ws("Luftdruck")
t_knackt = ws("knackt"); t_achtung = ws("Achtung"); t_ruhe = ws("Ruhe")
t_bestimmt = ws("Bestimmt"); t_fenster = ws("Fenster")
t_ploetz = ws("Plötzlich"); t_kippt = ws("kippt"); t_tief = ws("Tief"); t_blinkt = ws("blinkt"); t_weg = ws("weg", t_blinkt)
t_wieder = ws("Wieder"); t_regeln = ws("Regeln")
t_r1 = ws("Regel", t_regeln + 0.3); t_mitte = ws("Mitte"); t_schritt = ws("Schritt"); t_schaukeln = ws("Schaukeln")
t_r2 = ws("Regel", t_schaukeln); t_tuer = ws("Tür", t_r2); t_ruft = ws("ruft")
t_r3 = ws("Regel", t_ruft); t_warm = ws("warm"); t_sechs = ws("sechs"); t_rettung = ws("Rettung"); t_fuenf = ws("fünf"); t_keine = ws("Keine", t_fuenf)
t_waehlst = ws("wählst"); t_netz = ws("Netz")
t_340 = ws("Drei", t_netz); t_finger = ws("Finger"); t_klopft = ws("klopft")
t_hey = ws("Hey"); t_berg1 = ws("Bergwacht"); t_machauf = ws("Mach", t_berg1)
t_hand = ws("Hand", t_machauf); t_griff = ws("Griff"); t_vibriert = ws("vibriert")
t_berg2 = ws("Bergwacht", t_vibriert); t_tages = ws("Tageslicht"); t_bleib2 = ws("Bleib", t_tages)
t_wer = ws("Wer", t_bleib2); t_vor_tuer = ws("vor", t_wer)
t_du_musst = ws("Du", t_vor_tuer + 0.3); t_dach = ws("Dach", t_du_musst)
t_was = ws("Was", t_dach); t_luke = ws("Dachluke"); t_112b = ws("einhundertzwölf", t_luke)
t_teil2 = ws("Teil", t_112b); t_folge = ws("Folge", t_teil2)

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
# A Hook: du wachst in der Kabine auf
S0, S1 = 0.0, t_tausend - 0.1
scene("sa", S0, S1, interior("sa", dark=True) + figure("sa-fig", 360, 1420, 1.15, eyes="n"))
tw(f'tl.set("#sa-fig-eyes-n",{{opacity:0}},0);')
tw(f'tl.set("#sa-fig-eyes-w",{{opacity:1}},{t_drei0:.3f});')
tw(f'tl.fromTo("#sa-fig",{{y:30}},{{y:0,duration:.5,ease:"power2.out"}},{t_drei0 - 0.3:.3f});')

# B Außen: 1000 Meter Luft unter dir (Überblick: neuer Ort)
S0, S1 = t_tausend - 0.1, t_handy
arrow = (f'<g id="sb-arr" opacity="0"><line x1="900" y1="760" x2="900" y2="1660" stroke="{RED}" stroke-width="6" stroke-dasharray="20 14"/>'
         f'<polygon points="880,780 900,740 920,780" fill="{RED}"/><polygon points="880,1640 900,1680 920,1640" fill="{RED}"/></g>')
scene("sb", S0, S1, night_sky(1) + gorge(2) + cable(470, 640) + gondola_ext("sb-g", 540, 548, 0.8) + arrow
      + label("sb-l", 900, 1240, "1000 M", RED, 54) + label("sb-l2", 540, 1180, "STILLSTAND", "#fff", 40))
pop("#sb-arr", S0 + 0.2, 0.5, 0.95); pop("#sb-l", S0 + 0.4)
tw(f'tl.fromTo("#sb-cam",{{scale:1.5,svgOrigin:"540 760"}},{{scale:1,svgOrigin:"540 760",duration:1.6,ease:"power2.inOut"}},{S0:.3f});')
tw(f'tl.to("#sb-l",{{opacity:0,duration:.3}},{t_gondel - 0.2:.3f});')
tw(f'tl.to("#sb-arr",{{opacity:0,duration:.3}},{t_gondel - 0.2:.3f});')
pop("#sb-l2", t_bewegt)
tw(f'tl.fromTo("#sb-g",{{rotation:-1.5,svgOrigin:"540 548"}},{{rotation:1.5,svgOrigin:"540 548",duration:2.2,yoyo:true,repeat:5,ease:"sine.inOut"}},{S0:.3f});')

# C Handy: Höhenmesser über Luftdruck
S0, S1 = t_handy, t_knackt
alt = (f'<text x="0" y="-380" text-anchor="middle" font-family="Poppins" font-weight="600" font-size="34" fill="#9aa0d0">HÖHENMESSER</text>'
       f'<g id="sc-h" opacity="0"><text x="0" y="-220" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="150" fill="#fff">1000</text>'
       f'<text x="0" y="-150" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="40" fill="{LIME}">METER ÜBER DEM TAL</text></g>'
       f'<circle cx="0" cy="170" r="190" fill="#1d2152" stroke="#3a3f8a" stroke-width="14"/>'
       + "".join(f'<rect x="-3" y="-10" width="6" height="34" fill="#9aa0d0" transform="translate(0,170) rotate({a}) translate(0,-160)"/>' for a in range(-120, 121, 20))
       + f'<g id="sc-needle"><rect x="-6" y="0" width="12" height="150" rx="6" fill="{RED}" transform="translate(0,170) rotate(180)"/></g><circle cx="0" cy="170" r="20" fill="#fff"/>'
       f'<g id="sc-p" opacity="0"><text x="0" y="440" text-anchor="middle" font-family="JetBrains Mono" font-weight="700" font-size="48" fill="#fff">899 hPa</text>'
       f'<text x="0" y="490" text-anchor="middle" font-family="Poppins" font-weight="600" font-size="30" fill="#9aa0d0">Luftdruck</text></g>')
scene("sc", S0, S1, night_sky(3) + f'<rect width="1080" height="1920" fill="#000" opacity=".45"/>' + phone("sc-ph", alt))
tw(f'tl.fromTo("#sc-ph",{{y:200,opacity:0}},{{y:0,opacity:1,duration:.5,ease:"power2.out"}},{S0:.3f});')
pop("#sc-h", t_hoehe); pop("#sc-p", t_luftdruck)
tw(f'tl.fromTo("#sc-needle",{{rotation:-100,svgOrigin:"0 170"}},{{rotation:40,svgOrigin:"0 170",duration:1.0,ease:"power2.out"}},{t_luftdruck:.3f});')

# D Lautsprecher + Sperrbildschirm-Warnung (fiktiver Absender)
S0, S1 = t_knackt, t_bestimmt
lock = (f'<text x="0" y="-380" text-anchor="middle" font-family="Poppins" font-weight="600" font-size="34" fill="#cfd3ff">Mittwoch, 18. November</text>'
        f'<text x="0" y="-250" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="170" fill="#fff">3:13</text>'
        f'<g id="sd-n" opacity="0"><g transform="translate(0,260)"><rect x="-260" y="-160" width="520" height="250" rx="34" fill="#2a1420" stroke="{RED}" stroke-width="5"/>'
        f'<text x="-230" y="-110" font-family="Poppins" font-weight="800" font-size="30" fill="{RED}">⚠ BERGBAHN SÜDWAND</text>'
        f'<text x="-230" y="-60" font-family="Poppins" font-weight="700" font-size="34" fill="#fff">Achtung. Störung.</text>'
        f'<text x="-230" y="-14" font-family="Poppins" font-weight="600" font-size="30" fill="#e8e8ff">Bewahren Sie Ruhe.</text>'
        f'<text x="-230" y="40" font-family="Poppins" font-weight="500" font-size="22" fill="#9aa0d0">Notsystem · Gondel 7</text></g></g>')
waves = "".join(f'<path id="sd-w{i}" d="M {220+i*45} {720-i*30} q {40+i*12} {80+i*30} 0 {160+i*60}" stroke="#fff" stroke-width="9" fill="none" opacity="0"/>' for i in range(3))
scene("sd", S0, S1, interior("sd", dark=True) + f'<rect width="1080" height="1920" fill="#000" opacity=".5"/>'
      + f'<g transform="translate(-660,560)">{waves}</g>' + phone("sd-ph", lock, 540, 1060, 0.86))
tw(f'tl.fromTo("#sd-ph",{{y:240,opacity:0}},{{y:0,opacity:1,duration:.5,ease:"power2.out"}},{t_achtung - 0.5:.3f});')
pop("#sd-n", t_achtung, 0.35, 0.8)
for i in range(3):
    tw(f'tl.fromTo("#sd-w{i}",{{opacity:0}},{{opacity:.9,duration:.25,yoyo:true,repeat:5}},{S0 + i*0.1:.3f});')

# E Zweifel → Fenster → Kabine kippt
S0, S1 = t_bestimmt, t_tief
scene("se", S0, S1, f'<g transform="translate(540,960) scale(1.18) translate(-540,-960)"><g id="se-tilt">{interior("se", dark=True)}{figure("se-fig", 360, 1450, 1.15, eyes="n")}</g></g>', drift=False)
walk_cycle("se-fig", t_fenster - 0.2, t_kippt - 0.1)
tw(f'tl.to("#se-fig",{{x:-120,duration:{max(0.6, t_kippt - t_fenster):.3f},ease:"sine.inOut"}},{t_fenster - 0.2:.3f});')
tw(f'tl.to("#se-tilt",{{rotation:-8,svgOrigin:"540 -400",duration:.6,ease:"power2.out"}},{t_kippt:.3f});')
tw(f'tl.to("#se-tilt",{{rotation:4,svgOrigin:"540 -400",duration:1.1,ease:"sine.inOut"}},{t_kippt + 0.6:.3f});')
tw(f'tl.to("#se-tilt",{{rotation:-2,svgOrigin:"540 -400",duration:1.1,ease:"sine.inOut"}},{t_kippt + 1.7:.3f});')
tw(f'tl.to("#se-fig",{{x:-60,y:-20,duration:.5,ease:"power2.out"}},{t_kippt + 0.05:.3f});')
tw(f'tl.set("#se-fig-eyes-n",{{opacity:0}},{t_kippt:.3f});'); tw(f'tl.set("#se-fig-eyes-w",{{opacity:1}},{t_kippt:.3f});')

# E2 Blick nach unten: ein Licht blinkt – dann weg
S0, S1 = t_tief, t_wieder
scene("se2", S0, S1, f'<rect width="1080" height="1920" fill="#07081c"/>' + gorge(8, lights=False, y_top=200)
      + f'<rect width="1080" height="1920" fill="#000" opacity=".25"/>'
      + f'<g id="se2-l"><circle cx="560" cy="1700" r="10" fill="{WIN}"/><circle cx="560" cy="1700" r="60" fill="url(#moonglow)"/></g>'
      + f'<rect x="0" y="0" width="1080" height="1920" fill="none" stroke="{CAB2}" stroke-width="60"/>')
tw(f'tl.fromTo("#se2-l",{{opacity:0}},{{opacity:1,duration:.2,yoyo:true,repeat:5,ease:"sine.inOut"}},{t_blinkt - 0.2:.3f});')
tw(f'tl.to("#se2-l",{{opacity:0,duration:.15}},{t_weg:.3f});')
tw(f'tl.fromTo("#se2-cam",{{scale:1,svgOrigin:"560 1700"}},{{scale:1.4,svgOrigin:"560 1700",duration:{S1-S0+0.3:.3f},ease:"sine.inOut"}},{S0:.3f});')


# F „Drei Regeln“
def card_bg(cid):
    return (f'<rect width="1080" height="1920" fill="{CARD_BG}"/><circle cx="540" cy="760" r="520" fill="url(#cardglow)"/>'
            + "".join(f'<rect x="{x}" y="0" width="2" height="1920" fill="#fff" opacity=".025"/>' for x in range(0, 1080, 60))
            + "".join(f'<rect x="0" y="{y}" width="1080" height="2" fill="#fff" opacity=".025"/>' for y in range(0, 1920, 60)))


S0, S1 = t_wieder, t_r1
spk = (f'<g id="sf-spk" opacity="0"><circle cx="540" cy="760" r="190" fill="#3c4068"/>' + "".join(f'<circle cx="{540+dx}" cy="{760+dy}" r="16" fill="#20244f"/>' for dx in (-90, -30, 30, 90) for dy in (-60, 0, 60))
       + "".join(f'<path id="sf-w{i}" d="M {770+i*50} {660-i*30} q {50+i*12} {100+i*30} 0 {200+i*60}" stroke="#fff" stroke-width="10" fill="none" opacity="0"/>' for i in range(3)) + '</g>')
scene("sf", S0, S1, card_bg("sf") + spk
      + f'<g id="sf-t" opacity="0"><text x="540" y="1250" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="120" fill="#fff">3 REGELN</text>'
        f'<text x="540" y="1330" text-anchor="middle" font-family="Poppins" font-weight="600" font-size="40" fill="{LIME}" letter-spacing="4">IN 1000 M HÖHE</text></g>')
pop("#sf-spk", S0 + 0.05, 0.4, 0.7); pop("#sf-t", t_regeln - 0.3)
for i in range(3):
    tw(f'tl.fromTo("#sf-w{i}",{{opacity:0}},{{opacity:1,duration:.25,yoyo:true,repeat:5}},{S0 + 0.2 + i*0.1:.3f});')


ICON_DY = {"r1": 60, "r2": 150, "r3": 110}


def rule_card(sid, n, head, sub, icon):
    return (card_bg(sid)
            + f'<g id="{sid}-badge" opacity="0"><rect x="430" y="370" width="220" height="62" rx="12" fill="{RED}"/>'
              f'<text x="540" y="415" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="34" fill="#fff">REGEL #{n}</text></g>'
            + f'<g id="{sid}-head" opacity="0"><text x="540" y="540" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="80" fill="#fff">{head}</text></g>'
            + f'<g id="{sid}-sub" opacity="0"><text x="540" y="615" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="46" fill="{LIME}">{sub}</text></g>'
            + f'<g transform="translate(0,{ICON_DY.get(sid, 0)})">{icon}</g>')


def rule_in(sid, t0, t_sub):
    pop(f"#{sid}-badge", t0 + 0.05); pop(f"#{sid}-head", t0 + 0.25); pop(f"#{sid}-sub", t_sub)


# R1 Bleib in der Mitte
S0, S1 = t_r1, t_r2
icon1 = (f'<g id="r1-gon"><line x1="540" y1="700" x2="540" y2="820" stroke="{CABLE}" stroke-width="10"/><rect x="330" y="820" width="420" height="330" rx="40" fill="{CAB}"/>'
         + "".join(f'<rect x="{360+k*130}" y="850" width="100" height="130" rx="14" fill="#2a2f66"/>' for k in range(3))
         + f'<g id="r1-fig">{figure("r1-f", 540, 1130, 0.42)}</g></g>'
         + f'<line x1="200" y1="700" x2="880" y2="700" stroke="{CABLE}" stroke-width="8"/>'
         + f'<g id="r1-ok" opacity="0"><circle cx="540" cy="1320" r="60" fill="{LIME}"/><path d="M 510 1320 l 22 22 l 40 -44" stroke="#0b0d22" stroke-width="12" fill="none"/></g>')
scene("r1", S0, S1, rule_card("r1", 1, "BLEIB IN DER MITTE", "Jeder Schritt = Schaukeln", icon1) + xmark("r1-x", 700, 1060, 90))
rule_in("r1", S0, t_schritt)
tw(f'tl.to("#r1-fig",{{x:140,duration:.6,ease:"sine.inOut"}},{t_schritt:.3f});')
tw(f'tl.to("#r1-gon",{{rotation:-9,svgOrigin:"540 760",duration:.7,ease:"sine.inOut"}},{t_schritt + 0.2:.3f});')
pop("#r1-x", t_schaukeln, 0.25, 1.4)
tw(f'tl.to("#r1-x",{{opacity:0,duration:.2}},{t_schaukeln + 0.8:.3f});')
tw(f'tl.to("#r1-fig",{{x:0,duration:.6,ease:"sine.inOut"}},{t_schaukeln + 0.8:.3f});')
tw(f'tl.to("#r1-gon",{{rotation:0,svgOrigin:"540 760",duration:1.0,ease:"sine.inOut"}},{t_schaukeln + 0.9:.3f});')
pop("#r1-ok", t_schaukeln + 1.2)

# R2 Öffne nie die Tür
S0, S1 = t_r2, t_r3
icon2 = (f'<rect x="380" y="720" width="320" height="640" rx="20" fill="#c3c7da"/><rect x="405" y="760" width="270" height="260" rx="20" fill="#20244f"/>'
         f'<rect x="410" y="1130" width="110" height="30" rx="15" fill="{STEEL}"/><rect x="380" y="1220" width="320" height="14" fill="#c74545"/>'
         f'<g id="r2-bub" opacity="0"><rect x="560" y="600" width="400" height="130" rx="30" fill="#fff"/><polygon points="640,730 700,730 620,790" fill="#fff"/>'
         f'<text x="760" y="682" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="44" fill="#151a21">„Mach auf!“</text></g>')
scene("r2", S0, S1, rule_card("r2", 2, "ÖFFNE NIE DIE TÜR", "Egal, wer draußen ruft", icon2) + xmark("r2-x", 760, 815, 90))
rule_in("r2", S0, t_ruft - 0.4)
pop("#r2-bub", t_tuer); pop("#r2-x", t_ruft + 0.2, 0.25, 1.4)

# R3 Halte dich warm – Rettung 5:30
S0, S1 = t_r3, t_waehlst
icon3 = (f'<rect x="490" y="660" width="100" height="520" rx="50" fill="#e8ecff"/><circle cx="540" cy="1220" r="90" fill="#e8ecff"/>'
         f'<rect id="r3-merc" x="515" y="740" width="50" height="460" rx="25" fill="{RED}"/><circle cx="540" cy="1220" r="66" fill="{RED}"/>'
         + "".join(f'<rect x="600" y="{720+k*80}" width="40" height="8" fill="#9aa0d0"/>' for k in range(6))
         + label("r3-dt", 800, 900, "−6,5 °C", "#7fd0ff", 52)
         + f'<g id="r3-clock" opacity="0"><rect x="250" y="1380" width="580" height="200" rx="30" fill="#1d2152" stroke="{LIME}" stroke-width="6"/>'
           f'<text x="540" y="1440" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="34" fill="{LIME}" letter-spacing="4">RETTUNG</text>'
           f'<text x="540" y="1545" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="110" fill="#fff">5:30</text></g>'
         + f'<g id="r3-st" opacity="0"><rect x="300" y="1620" width="480" height="90" rx="16" fill="{RED}" transform="rotate(-5 540 1665)"/>'
           f'<text x="540" y="1682" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="46" fill="#fff" transform="rotate(-5 540 1665)">KEINE MINUTE FRÜHER</text></g>')
scene("r3", S0, S1, rule_card("r3", 3, "HALTE DICH WARM", "Oben ist es kälter", icon3))
rule_in("r3", S0, t_sechs - 0.3)
tw(f'tl.fromTo("#r3-merc",{{scaleY:1,transformOrigin:"50% 100%"}},{{scaleY:.45,transformOrigin:"50% 100%",duration:1.2,ease:"power2.inOut"}},{t_sechs - 0.2:.3f});')
pop("#r3-dt", t_sechs + 0.2)
pop("#r3-clock", t_rettung)
tw(f'tl.fromTo("#r3-st",{{opacity:0,scale:1.8,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:.22,ease:"power4.in"}},{t_keine:.3f});')
shake("#r3-cam", t_keine + 0.22, 3, 4)

# G Notruf 112 – auch ohne eigenes Netz
S0, S1 = t_waehlst, t_340
call = (f'<text x="0" y="-380" text-anchor="middle" font-family="Poppins" font-weight="600" font-size="34" fill="#9aa0d0">Notruf</text>'
        f'<text x="0" y="-250" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="170" fill="#fff">112</text>'
        f'<g id="sg-c" opacity="0"><text x="0" y="-150" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="40" fill="{LIME}">verbunden · 00:04</text></g>'
        f'<g id="sg-net" opacity="0"><rect x="-230" y="-60" width="460" height="170" rx="26" fill="#1d2152"/>'
        f'<text x="0" y="0" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="34" fill="#fff">Eigenes Netz: ✕</text>'
        f'<text x="0" y="60" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="34" fill="{LIME}">Fremdes Netz: ✓</text></g>'
        f'<circle cx="0" cy="380" r="70" fill="{RED}"/><rect x="-40" y="366" width="80" height="28" rx="14" fill="#fff"/>')
scene("sg", S0, S1, interior("sg", dark=True) + f'<rect width="1080" height="1920" fill="#000" opacity=".5"/>' + phone("sg-ph", call))
tw(f'tl.fromTo("#sg-ph",{{y:200,opacity:0}},{{y:0,opacity:1,duration:.5,ease:"power2.out"}},{S0:.3f});')
pop("#sg-c", S0 + 0.7); pop("#sg-net", t_netz - 0.6)

# H 3:40 – eiskalt – es klopft
S0, S1 = t_340, t_hand
breath = "".join(f'<ellipse id="sh-br{i}" cx="430" cy="1060" rx="40" ry="26" fill="#fff" opacity="0"/>' for i in range(3))
scene("sh", S0, S1, interior("sh", frost=True, dark=True) + figure("sh-fig", 360, 1420, 1.15, eyes="f") + breath
      + f'<g id="sh-k1" opacity="0"><text x="870" y="760" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="96" fill="{RED}">KLOPF.</text></g>'
      + f'<g id="sh-k2" opacity="0"><text x="870" y="880" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="96" fill="{RED}">KLOPF.</text></g>'
      + quote("sh-q", ["„Hey! Bergwacht!", "Mach auf, ich hol dich raus!“"], y=620, col="#ff8a8a"))
for i in range(3):
    tw(f'tl.fromTo("#sh-br{i}",{{opacity:0,x:0,y:0,scale:.6,transformOrigin:"50% 50%"}},{{opacity:.5,x:60,y:-60,scale:1.4,duration:1.2,ease:"sine.out"}},{S0 + 0.2 + i*1.0:.3f});')
    tw(f'tl.to("#sh-br{i}",{{opacity:0,duration:.6}},{S0 + 1.2 + i*1.0:.3f});')
tw(f'tl.set("#sh-fig-eyes-f",{{opacity:0}},{t_klopft:.3f});'); tw(f'tl.set("#sh-fig-eyes-w",{{opacity:1}},{t_klopft:.3f});')
pop("#sh-k1", t_klopft); pop("#sh-k2", t_klopft + 0.45)
shake("#sh-door", t_klopft, 3, 5); shake("#sh-door", t_klopft + 0.45, 3, 5)
tw(f'tl.to("#sh-k1, #sh-k2",{{opacity:0,duration:.3}},{t_hey - 0.3:.3f});')
pop("#sh-q-lab", t_hey - 0.1); pop("#sh-q-0", t_hey); pop("#sh-q-1", t_machauf)
tw(f'tl.to("#sh-fig",{{x:180,duration:1.0,ease:"sine.inOut"}},{t_machauf + 0.3:.3f});')
walk_cycle("sh-fig", t_machauf + 0.3, t_machauf + 1.3)

# I Hand am Griff → Handy vibriert
S0, S1 = t_hand, t_vibriert + 0.4
hand = (f'<g id="si-hand"><rect x="280" y="1000" width="420" height="150" rx="70" fill="#2f6f73"/><rect x="560" y="990" width="200" height="170" rx="60" fill="{FIG}"/>'
        + "".join(f'<rect x="{620+k*36}" y="1100" width="30" height="90" rx="15" fill="{FIG}"/>' for k in range(4)) + '</g>')
scene("si", S0, S1, f'<rect width="1080" height="1920" fill="#c3c7da"/><rect x="0" y="0" width="1080" height="700" fill="#20244f"/><rect x="0" y="0" width="1080" height="700" fill="{FROST}" opacity=".25"/>'
      + f'<rect x="0" y="700" width="1080" height="30" fill="#aeb3cc"/><g id="si-lever"><rect x="520" y="1050" width="500" height="110" rx="55" fill="{STEEL}"/><circle cx="560" cy="1105" r="80" fill="#3c4068"/></g>'
      + hand + f'<rect x="0" y="1500" width="1080" height="40" fill="#c74545"/>')
tw(f'tl.fromTo("#si-hand",{{x:-300,y:200}},{{x:0,y:0,duration:.8,ease:"power2.out"}},{S0:.3f});')
tw(f'tl.to("#si-lever, #si-hand",{{rotation:6,svgOrigin:"560 1105",duration:.5,ease:"sine.inOut"}},{t_griff:.3f});')
tw(f'tl.to("#si-lever, #si-hand",{{rotation:0,svgOrigin:"560 1105",duration:.3,ease:"power2.out"}},{t_vibriert:.3f});')
shake("#si-cam", t_vibriert, 6, 4)

# J Chat mit der Bergwacht: Gegenbeweis
S0, S1 = t_vibriert + 0.4, t_wer
chat = (f'<rect x="-280" y="-580" width="560" height="150" rx="0" fill="#1a1d47"/><circle cx="-200" cy="-490" r="36" fill="#c74545"/>'
        f'<text x="-200" y="-478" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="30" fill="#fff">BW</text>'
        f'<text x="-140" y="-480" font-family="Poppins" font-weight="700" font-size="36" fill="#fff">Bergwacht</text>'
        f'<text x="0" y="-370" text-anchor="middle" font-family="Poppins" font-weight="600" font-size="24" fill="#8f94c4">Heute 3:21</text>'
        f'<rect x="-250" y="-340" width="420" height="120" rx="26" fill="#262a5e"/><text x="-225" y="-290" font-family="Poppins" font-weight="600" font-size="28" fill="#fff">Notruf erhalten.</text>'
        f'<text x="-225" y="-250" font-family="Poppins" font-weight="600" font-size="28" fill="#fff">Wir melden uns.</text>'
        f'<g id="sj-new" opacity="0"><text x="0" y="-150" text-anchor="middle" font-family="Poppins" font-weight="600" font-size="24" fill="#8f94c4">Heute 3:41</text>'
        f'<rect x="-250" y="-120" width="480" height="210" rx="26" fill="#262a5e" stroke="{LIME}" stroke-width="4"/>'
        f'<text x="-225" y="-66" font-family="Poppins" font-weight="700" font-size="30" fill="#fff">Wir starten erst</text>'
        f'<text x="-225" y="-22" font-family="Poppins" font-weight="700" font-size="30" fill="#fff">bei Tageslicht.</text>'
        f'<text x="-225" y="40" font-family="Poppins" font-weight="700" font-size="30" fill="{LIME}">Bleib, wo du bist.</text></g>')
scene("sj", S0, S1, f'<rect width="1080" height="1920" fill="#0c0d22"/><circle cx="540" cy="900" r="600" fill="url(#cardglow)"/>' + phone("sj-ph", chat))
tw(f'tl.fromTo("#sj-new",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.4,ease:"power2.out"}},{t_berg2:.3f});')

# K Außen: wer hängt da vor der Tür?
S0, S1 = t_wer, t_du_musst
scene("sk", S0, S1, night_sky(9) + gorge(10) + f'<rect width="1080" height="1920" fill="#000" opacity=".35"/>' + cable(380, 520, 7)
      + gondola_ext("sk-g", 540, 440, 1.25, lit=False) + creature("sk-c", 700, 1060, 1.0), drift=False)
tw(f'tl.fromTo("#sk-cam",{{scale:1,svgOrigin:"700 800"}},{{scale:1.35,svgOrigin:"700 800",duration:{S1-S0+0.3:.3f},ease:"sine.in"}},{S0:.3f});')
tw(f'tl.fromTo("#sk-c",{{opacity:0}},{{opacity:1,duration:.8,ease:"sine.inOut"}},{S0 + 0.3:.3f});')
tw(f'tl.fromTo("#sk-c-eyes",{{opacity:0}},{{opacity:1,duration:.2}},{t_vor_tuer:.3f});')

# L Er kommt durchs Dach
S0, S1 = t_du_musst, t_was
scratch = "".join(f'<path id="sl-s{i}" d="M {500+i*60} 120 l 30 160" stroke="#fff" stroke-width="5" opacity="0"/>' for i in range(4))
scene("sl", S0, S1, interior("sl", frost=True, dark=True) + scratch + figure("sl-fig", 450, 1440, 1.15, eyes="w")
      + quote("sl-q", ["„Du musst nicht aufmachen.", "Ich komm durchs Dach.“"], y=640, col="#ff8a8a", label_txt="– ÜBER DIR –"), drift=False)
tw(f'tl.fromTo("#sl-cam",{{y:-80,scale:1.1,svgOrigin:"540 300"}},{{y:0,scale:1,svgOrigin:"540 300",duration:{S1-S0+0.3:.3f},ease:"sine.inOut"}},{S0:.3f});')
pop("#sl-q-lab", S0); pop("#sl-q-0", S0 + 0.1); pop("#sl-q-1", t_dach - 0.6)
for i in range(4):
    tw(f'tl.fromTo("#sl-s{i}",{{opacity:0}},{{opacity:.8,duration:.15,yoyo:true,repeat:1}},{S0 + 0.4 + i*0.25:.3f});')
tw(f'tl.to("#sl-hlever",{{rotation:-35,svgOrigin:"610 209",duration:.9,ease:"power1.inOut"}},{t_dach - 0.3:.3f});')
shake("#sl-hatch", t_dach + 0.5, 4, 4)

# M Wahl
S0, S1 = t_was, t_teil2
scene("sm", S0, S1, interior("sm", frost=True, dark=True) + f'<rect width="1080" height="1920" fill="#000" opacity=".45"/>' + figure("sm-fig", 540, 1500, 1.2, eyes="w")
      + pill("sm-p1", 540, 760, "DACHLUKE ZUHALTEN", RED) + pill("sm-p2", 540, 920, "NOCH MAL 112", BLUE)
      )
pop("#sm-p1", t_luke); pop("#sm-p2", t_112b - 0.3)
tw(f'tl.to("#sm-fig",{{x:-50,duration:.9,ease:"sine.inOut",yoyo:true,repeat:1}},{t_luke:.3f});')

# N Teil-2-Karte
S0, S1 = t_teil2, TOTAL
fog = "".join(f'<ellipse id="sn-f{i}" cx="{RNG.randint(0,1080)}" cy="{RNG.randint(300,1700)}" rx="{RNG.randint(300,520)}" ry="{RNG.randint(90,170)}" fill="#8a8fb8" opacity=".09"/>' for i in range(10))
scene("sn", S0, S1, f'<rect width="1080" height="1920" fill="#14152e"/>{fog}' + cable(1490, 1560, 4) + gondola_ext("sn-g", 540, 1530, 0.5, lit=False)
      + f'<text x="540" y="450" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="36" fill="#cfd3ff" letter-spacing="14">HÖHE</text>'
      + f'<g id="sn-t" opacity="0"><text x="540" y="680" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="230" fill="{RED}" filter="url(#glow)">TEIL 2</text></g>'
      + f'<g id="sn-s" opacity="0"><text x="540" y="1420" text-anchor="middle" font-family="Poppins" font-weight="600" font-size="44" fill="#fff">heute Nacht · 3:12 Uhr</text></g>'
      + f'<g id="sn-b" opacity="0"><rect x="330" y="1560" width="420" height="80" rx="40" fill="none" stroke="#fff" stroke-width="5"/>'
        f'<text x="540" y="1613" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="34" fill="#fff" letter-spacing="3">FOLGE FÜR TEIL 2</text></g>')
pop("#sn-t", S0 + 0.1, 0.5, 1.3); pop("#sn-s", S0 + 0.6); pop("#sn-b", t_folge)
for i in range(10):
    tw(f'tl.fromTo("#sn-f{i}",{{x:0}},{{x:{RNG.choice([-1,1])*RNG.randint(80,200)},duration:{S1-S0:.3f},ease:"sine.inOut"}},{S0:.3f});')

# ================= SERIEN-BRANDING OBEN LINKS (Format B) =================
BRAND = [  # (start, ende, uhrzeit, ort)
    (0.0, t_handy, "3:12", "GONDEL 7 · 1000 M"), (t_handy, t_wieder, "3:13", "GONDEL 7"), (t_wieder, t_waehlst, "3:14", "LAUTSPRECHER"),
    (t_waehlst, t_340, "3:21", "NOTRUF 112"), (t_340, t_vibriert + 0.4, "3:40", "VOR DER TÜR"), (t_vibriert + 0.4, t_wer, "3:41", "HANDY"),
    (t_wer, t_teil2, "3:42", "AUSSEN · 1000 M"),
]
BRAND = [(a, b if i + 1 >= len(BRAND) or BRAND[i+1][0] >= b else BRAND[i+1][0], c, d) for i, (a, b, c, d) in enumerate(BRAND)]
brand_html = []
for i, (a, b, clock, place) in enumerate(BRAND):
    brand_html.append(
        f'<div id="br{i}" class="clip ov" data-start="{a:.3f}" data-duration="{b-a:.3f}" data-track-index="7" style="z-index:12">'
        f'<svg viewBox="0 0 1080 1920" width="1080" height="1920"><rect x="40" y="150" width="400" height="200" rx="24" fill="#0b0d22" opacity=".55"/><g transform="translate(70,190)">'
        f'<circle cx="8" cy="-6" r="8" fill="{RED}"/><text x="26" y="2" font-family="JetBrains Mono, monospace" font-weight="700" font-size="24" fill="#cfd3ff" letter-spacing="4">HÖHE · TEIL 1</text>'
        f'<text x="0" y="96" font-family="JetBrains Mono, monospace" font-weight="800" font-size="96" fill="{RED}" filter="url(#glowsoft)">{clock}</text>'
        f'<text x="{len(clock)*58+10}" y="96" font-family="JetBrains Mono, monospace" font-weight="700" font-size="26" fill="{RED}">UHR</text>'
        f'<text x="2" y="140" font-family="JetBrains Mono, monospace" font-weight="700" font-size="22" fill="#8f94c4" letter-spacing="4">{place}</text></g></svg></div>')

# ================= UNTERTITEL (Skill 7 + Format B: Akzent Neon-Gelbgrün) =================
KEY = {"TAUSEND", "LUFT", "GONDEL", "SCHLUCHT", "HÖHE", "LUFTDRUCK", "LAUTSPRECHER", "ACHTUNG", "STÖRUNG", "FENSTER", "KIPPT", "LICHT",
       "DREI", "REGELN", "MITTE", "SCHRITT", "SCHAUKELN", "TÜR", "RUFT", "WARM", "SECHS", "KÄLTER", "RETTUNG", "112", "NETZ", "EISKALT",
       "KLOPFT", "BERGWACHT", "GRIFF", "VIBRIERT", "TAGESLICHT", "DACH", "DACHLUKE", "TEIL", "ZWEI", "3:12", "3:40", "5:30", "1000", "METERN"}
DISPLAY = {"tausend": "1000", "einhundertzwölf.": "112.", "einhundertzwölf": "112", "einhundertzwölf?": "112?", "zwei": "2", "sechs": "6", "Höhe": "Höhe"}
SKIP = {"zwölf", "zwölf.", "dreißig.", "vierzig.", "Uhr"}


def norm(t):
    return re.sub(r"[^\wÄÖÜäöüß:]", "", t).upper()


words = []
for k, w in enumerate(W):
    nxt2 = " ".join(x["t"] for x in W[k:k+3]).lower()
    if nxt2.startswith("drei uhr zwölf"): words.append({"t": "3:12" + ("." if W[k+2]["t"].endswith(".") else ""), "s": w["s"], "e": W[k+2]["e"]}); continue
    if nxt2.startswith("drei uhr vierzig"): words.append({"t": "3:40.", "s": w["s"], "e": W[k+2]["e"]}); continue
    if nxt2.startswith("fünf uhr dreißig"): words.append({"t": "5:30.", "s": w["s"], "e": W[k+2]["e"]}); continue
    if k >= 1 and W[k-1]["t"].lower() in ("drei", "fünf") and w["t"] == "Uhr": continue
    if k >= 2 and W[k-1]["t"] == "Uhr" and w["t"].lower().rstrip(".") in ("zwölf", "vierzig", "dreißig"): continue
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
<radialGradient id="lampglow"><stop offset="0" stop-color="#fff6d8" stop-opacity=".5"/><stop offset="1" stop-color="#fff6d8" stop-opacity="0"/></radialGradient>
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


danger("ov-d1", t_kippt, t_wieder)
danger("ov-d2", t_klopft, t_hand)
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
    <title>Höhe Teil 1</title>
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
