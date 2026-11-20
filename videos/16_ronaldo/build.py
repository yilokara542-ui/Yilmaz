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


# ---------- Figuren: feste Hauptfigur „C · Anime mit Senf-Hoodie“ (Skill 6) ----------
import sys as _sys
_sys.path.insert(0, os.path.join(HERE, "../../branding/figur"))
from figur_c import make_figure, DEFS as FIGC_DEFS
FIGS = []
figure = make_figure(FIGS)


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
t_ronaldo1 = ws("Ronaldo"); t_finden = ws("Finden")
t_d1 = ws("Erste"); t_sprung = ws("Sprungkraft"); t_kopfball = ws("Kopfball"); t_256 = ws("zwei"); t_latte = ws("Latte")
t_du_spr = ws("springst"); t_nicht_mal = ws("nicht", t_du_spr)
t_d2 = ws("Zweite"); t_trainierst = ws("trainierst"); t_er_auch = ws("Er", t_trainierst); t_zwanzig = ws("zwanzig")
t_doch = ws("Doch"); t_platz = ws("Platz"); t_bett = ws("Bett")
t_soll = ws("soll"); t_fuenf = ws("fünfmal"); t_warum = ws("Warum"); t_zyklus = ws("Schlafzyklus"); t_wer = ws("Wer", t_zyklus); t_fit = ws("fit")
t_messen = ws("messen"); t_watch = ws("Smartwatch"); t_spuert = ws("spürt"); t_puls = ws("Puls"); t_gruen = ws("grünem"); t_daraus = ws("Daraus"); t_tief = ws("tief")
t_wecker = ws("Wecker"); t_woche1 = ws("Woche"); t_wacher = ws("wacher"); t_woche4 = ws("Woche", t_wacher); t_sprintest = ws("sprintest")
t_soweit = ws("weit"); t_d3 = ws("Dritte"); t_elf = ws("Elfmeter"); t_torwart = ws("Torwart"); t_laeufst = ws("läufst")
t_wirst = ws("Wirst"); t_ehrlich = ws("Ehrlich"); t_aber = ws("Aber", t_ehrlich); t_schlaefst = ws("schläfst")
t_was = ws("Was", t_schlaefst); t_schuss = ws("Schuss"); t_schlaf = ws("Schlaf", t_schuss); t_schreib = ws("Schreib")

# ================= SZENEN (Format A „Erklär-Story“) =================
GRASS1 = "#1f6b3a"; GRASS2 = "#237a42"; NET = "#e8ecff"; GREEN_LED = "#3cff8a"


def fadein(sel, t, dur=0.45, dy=16):
    tw(f'tl.fromTo("{sel}",{{opacity:0,y:{dy}}},{{opacity:1,y:0,duration:{dur},ease:"sine.out"}},{t:.3f});')


def stadium(prefix, goal=True, gx=560, gw=420, ground=1250, ppm=300):
    """Nachtstadion: Tribünen mit Lichtpunkten, Flutlichter, Rasen mit Streifen, Tor (Latte 2,44 m)."""
    stands = "".join(f'<rect x="0" y="{560+k*70}" width="1080" height="60" fill="{"#191b3d" if k%2 else "#1d2048"}"/>' for k in range(6))
    crowd = "".join(f'<circle cx="{(k*53)%1080}" cy="{575+((k*37)%6)*70}" r="{4+(k%3)}" fill="{["#ffd98a","#cfd3ff","#ff8a8a","#9ad0ff"][k%4]}" opacity=".5"/>' for k in range(120))
    lights = "".join(f'<rect x="{x}" y="300" width="14" height="300" fill="#2a2d55"/><rect x="{x-50}" y="270" width="114" height="44" rx="8" fill="#e8ecff"/>'
                     f'<polygon points="{x-50},{314} {x+64},{314} {x+260},{900} {x-250},{900}" fill="url(#lampcone)" opacity=".5"/>' for x in (120, 940))
    pitch = (f'<rect x="0" y="960" width="1080" height="960" fill="{GRASS1}"/>'
             + "".join(f'<rect x="0" y="{960+k*120}" width="1080" height="60" fill="{GRASS2}"/>' for k in range(8))
             + f'<rect x="0" y="{ground}" width="1080" height="8" fill="#e8ecff" opacity=".7"/>')
    g = ""
    if goal:
        bar_y = ground - 2.44 * ppm
        g = (f'<g id="{prefix}-goal"><rect x="{gx}" y="{bar_y}" width="{gw}" height="{2.44*ppm}" fill="url(#netpat)" opacity=".55"/>'
             f'<rect x="{gx-10}" y="{bar_y-10}" width="{gw+20}" height="16" fill="{NET}"/><rect x="{gx-10}" y="{bar_y}" width="16" height="{2.44*ppm}" fill="{NET}"/>'
             f'<rect x="{gx+gw-6}" y="{bar_y}" width="16" height="{2.44*ppm}" fill="{NET}"/></g>')
    return f'<rect width="1080" height="1920" fill="url(#skyg)"/>{stands}{crowd}{lights}{pitch}{g}'


def scoreboard(sid, l, r, label="DISZIPLIN"):
    return (f'<g id="{sid}"><rect x="200" y="150" width="680" height="120" rx="20" fill="#0b0d22" opacity=".9" stroke="#3a3f8a" stroke-width="4"/>'
            f'<text x="300" y="230" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="44" fill="#e0a83a">DU</text>'
            f'<text id="{sid}-sc" x="540" y="232" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="60" fill="#fff">{l} : {r}</text>'
            f'<text x="745" y="228" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="36" fill="#cfd3ff">RONALDO</text>'
            f'<text x="540" y="300" text-anchor="middle" font-family="JetBrains Mono" font-weight="700" font-size="24" fill="#8f94c4" letter-spacing="4">{label}</text></g>')


def card_bg(cid):
    return (f'<rect width="1080" height="1920" fill="{CARD_BG}"/><circle cx="540" cy="860" r="560" fill="url(#cardglow)"/>'
            + "".join(f'<rect x="{x}" y="0" width="2" height="1920" fill="#fff" opacity=".025"/>' for x in range(0, 1080, 60)))


def bed(prefix, sleeping_fig=True):
    """Schlafzimmer bei Nacht: Bett, Nachttisch mit Lampe, Fenster mit Mond, Poster, Pflanze."""
    room = (f'<rect width="1080" height="1920" fill="#1c1f45"/><rect x="0" y="1240" width="1080" height="680" fill="#2a2440"/>'
            f'<rect x="620" y="420" width="300" height="360" rx="14" fill="#0b0d26" stroke="#3a3f8a" stroke-width="14"/><circle cx="820" cy="520" r="44" fill="{MOON}"/>'
            f'<rect x="120" y="440" width="220" height="300" rx="8" fill="#e0a83a" opacity=".8"/><circle cx="230" cy="560" r="60" fill="#fff" opacity=".9"/>'
            + "".join(f'<path d="M {170+k*30} 560 l 30 -50" stroke="#1e1a2e" stroke-width="6"/>' for k in range(3))
            + f'<rect x="860" y="1060" width="150" height="190" rx="10" fill="#4a3a5a"/><rect x="905" y="980" width="12" height="80" fill="#888"/><path d="M 870 980 L 950 980 L 935 940 L 885 940 Z" fill="#ffd98a"/>'
            f'<circle cx="910" cy="960" r="140" fill="url(#moonglow)" opacity=".6"/>'
            f'<rect x="40" y="1120" width="80" height="120" rx="10" fill="#c26a3d"/><ellipse cx="80" cy="1100" rx="70" ry="40" fill="#3f8f5a"/>')
    frame = (f'<rect x="140" y="1080" width="700" height="200" rx="20" fill="#5a3a24"/><rect x="140" y="980" width="40" height="300" rx="10" fill="#5a3a24"/>'
             f'<rect x="170" y="1050" width="660" height="80" rx="20" fill="#e9e6f2"/><rect x="190" y="1010" width="180" height="70" rx="26" fill="#fff"/>')
    fig = f'<g transform="rotate(-90 490 1050)">{figure(f"{prefix}-fig", 490, 1050 + 30, 0.75, eyes="s")}</g>' if sleeping_fig else ""
    blanket = f'<path d="M 330 1030 Q 560 990 830 1040 L 830 1130 L 330 1130 Z" fill="#3b6cff"/><path d="M 330 1030 Q 560 990 830 1040" stroke="#5a86ff" stroke-width="10" fill="none"/>'
    return room + frame + fig + blanket


# A Hook: Kannst du besser werden als Ronaldo?
S0, S1 = 0.0, t_d1
scene("sa", S0, S1, stadium("sa") + scoreboard("sa-sb", 0, 0, "DISZIPLIN – / 3") + figure("sa-fig", 380, 1420, 1.4, eyes="n")
      + f'<g id="sa-q" opacity="0"><circle cx="540" cy="760" r="90" fill="{RED}"/><text x="540" y="800" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="120" fill="#fff">?</text></g>')
fadein("#sa-sb", 0.05, 0.4, -20); pop("#sa-q", t_ronaldo1, 0.4, 0.8)
tw(f'tl.set("#sa-fig-eyes-n",{{opacity:0}},{t_finden:.3f});'); tw(f'tl.set("#sa-fig-eyes-f",{{opacity:1}},{t_finden:.3f});')

# B Disziplin 1: Sprungkraft – 2,56 m vs. Latte 2,44 m
S0, S1 = t_d1, t_d2
G, PPM = 1250, 300
ruler = (f'<rect x="70" y="{G-2.8*PPM}" width="16" height="{2.8*PPM}" fill="#e8ecff" opacity=".8"/>'
         + "".join(f'<rect x="70" y="{G-m*PPM:.0f}" width="44" height="6" fill="#e8ecff"/><text x="124" y="{G-m*PPM+10:.0f}" font-family="JetBrains Mono" font-weight="700" font-size="28" fill="#e8ecff">{m:.1f} m</text>'
                   for m in (0.5, 1.0, 1.5, 2.0, 2.5)))
r_line = (f'<g id="sb-r" opacity="0"><rect x="60" y="{G-2.56*PPM-3}" width="960" height="6" fill="{RED}"/>'
          f'<rect x="590" y="{G-2.56*PPM-74}" width="400" height="58" rx="12" fill="{RED}"/>'
          f'<text x="790" y="{G-2.56*PPM-33}" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="34" fill="#fff">RONALDO 2,56 m</text></g>')
bar_lbl = label("sb-bl", 780, G - 2.44 * PPM + 70, "LATTE 2,44 m", "#e8ecff", 30)
du_line = (f'<g id="sb-du" opacity="0"><rect x="60" y="{G-2.12*PPM-3}" width="560" height="6" fill="#e0a83a"/>'
           f'<rect x="200" y="{G-2.12*PPM+14}" width="260" height="54" rx="12" fill="#e0a83a"/>'
           f'<text x="330" y="{G-2.12*PPM+52}" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="32" fill="#0b0d22">DU 2,12 m</text></g>')
scene("sb", S0, S1, stadium("sb", gx=560, gw=420, ground=G, ppm=PPM) + ruler + scoreboard("sb-sb", 0, 0, "DISZIPLIN 1 / 3 · SPRUNG")
      + figure("sb-fig", 380, G, 1.4, eyes="f") + bar_lbl + r_line + du_line
      + f'<text id="sb-s2" x="540" y="232" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="60" fill="{RED}" opacity="0">0 : 1</text>', drift=False)
fadein("#sb-bl", t_latte - 0.2, 0.4, 0)
tw(f'tl.fromTo("#sb-r",{{opacity:0,scaleX:0,transformOrigin:"0% 50%"}},{{opacity:1,scaleX:1,duration:.6,ease:"power2.out"}},{t_256:.3f});')
tw(f'tl.to("#sb-fig",{{y:-12,scaleY:.94,transformOrigin:"50% 100%",duration:.18,ease:"sine.in"}},{t_du_spr - 0.15:.3f});')
tw(f'tl.to("#sb-fig",{{y:-140,scaleY:1.03,duration:.38,ease:"power2.out"}},{t_du_spr + 0.03:.3f});')
tw(f'tl.to("#sb-fig",{{y:0,scaleY:1,duration:.38,ease:"power2.in"}},{t_du_spr + 0.41:.3f});')
tw(f'tl.set("#sb-fig-eyes-f",{{opacity:0}},{t_du_spr:.3f});'); tw(f'tl.set("#sb-fig-eyes-w",{{opacity:1}},{t_du_spr:.3f});')
fadein("#sb-du", t_du_spr + 0.4, 0.4, 0)
tw(f'tl.to("#sb-sb-sc",{{opacity:0,duration:.15}},{t_nicht_mal:.3f});')
fadein("#sb-s2", t_nicht_mal + 0.15, 0.3, 0)
SCORE_SWAP = []

# C Disziplin 2: Training – jeden Tag, er seit über 20 Jahren
S0, S1 = t_d2, t_doch
cal = (f'<g id="sc-cal"><rect x="700" y="420" width="260" height="280" rx="18" fill="#fff"/><rect x="700" y="420" width="260" height="70" rx="18" fill="{RED}"/>'
       + "".join(f'<text id="sc-d{k}" x="830" y="640" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="120" fill="#1e1a2e" opacity="0">{d}</text>' for k, d in enumerate((1, 2, 3, 4, 5, 6, 7)))
       + '</g>')
yrs = (f'<g id="sc-y" opacity="0"><rect x="560" y="760" width="440" height="120" rx="20" fill="#0b0d22" opacity=".9" stroke="#cfd3ff" stroke-width="4"/>'
       f'<text x="780" y="840" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="52" fill="#cfd3ff">RONALDO: 20+ J.</text></g>')
scene("sc", S0, S1, stadium("sc", goal=False) + scoreboard("sc-sb", 0, 1, "DISZIPLIN 2 / 3 · TRAINING") + cal + yrs
      + f'<g id="sc-cones">' + "".join(f'<polygon points="{x},1300 {x+30},1240 {x+60},1300" fill="#ff8a3d"/>' for x in range(-100, 2200, 260)) + '</g>'
      + figure("sc-fig", 420, 1420, 1.3, eyes="f"), drift=False)
walk_cycle("sc-fig", S0, S1 + 0.3, period=0.36, bob=12)
tw(f'tl.to("#sc-cones",{{x:-900,duration:{S1-S0+0.3:.3f},ease:"none"}},{S0:.3f});')
for k in range(7):
    a = t_trainierst + k * max(0.25, (t_er_auch - t_trainierst) / 7)
    tw(f'tl.set("#sc-d{k}",{{opacity:1}},{a:.3f});')
    if k < 6:
        tw(f'tl.set("#sc-d{k}",{{opacity:0}},{a + max(0.25, (t_er_auch - t_trainierst) / 7):.3f});')
fadein("#sc-y", t_zwanzig - 0.2, 0.45, 20)

# D Wendung: nicht auf dem Platz – im Bett
S0, S1 = t_doch, t_soll
scene("sd", S0, S1, bed("sd") + f'<g id="sd-x" opacity="0"><rect x="250" y="250" width="580" height="90" rx="20" fill="#0b0d22" opacity=".9"/>'
      f'<text x="540" y="312" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="44" fill="#8f94c4">NICHT AUF DEM PLATZ</text>'
      f'<rect x="270" y="290" width="540" height="10" fill="{RED}"/></g>'
      + pill("sd-p", 540, 450, "SONDERN IM BETT", RED, "#fff", 54))
fadein("#sd-x", t_platz - 0.3); pop("#sd-p", t_bett, 0.4, 0.9)
tw(f'tl.fromTo("#sd-cam",{{scale:1.15,svgOrigin:"500 1060"}},{{scale:1,svgOrigin:"500 1060",duration:{S1-S0+0.3:.3f},ease:"sine.out"}},{S0:.3f});')

# E 5 × 90 Minuten – Schlafzyklen
S0, S1 = t_soll, t_messen
R0 = 300; CXE, CYE = 540, 760
import math as _m
def arc(a0, a1, r=R0):
    x0, y0 = CXE + r*_m.sin(a0), CYE - r*_m.cos(a0); x1, y1 = CXE + r*_m.sin(a1), CYE - r*_m.cos(a1)
    return f'M {x0:.1f} {y0:.1f} A {r} {r} 0 {1 if a1-a0>_m.pi else 0} 1 {x1:.1f} {y1:.1f}'
segs = [(22.5, 24.0), (3.0, 4.5), (7.5, 9.0), (13.0, 14.5), (17.0, 18.5)]
ring = (f'<circle cx="{CXE}" cy="{CYE}" r="{R0}" fill="none" stroke="#262a5e" stroke-width="60"/>'
        + "".join(f'<path id="se-s{k}" d="{arc(a/24*2*_m.pi, b/24*2*_m.pi)}" stroke="#7a8aff" stroke-width="60" fill="none" opacity="0"/>' for k, (a, b) in enumerate(segs))
        + "".join(f'<text x="{CXE + 390*_m.sin(h/24*2*_m.pi):.0f}" y="{CYE - 390*_m.cos(h/24*2*_m.pi) + 12:.0f}" text-anchor="middle" font-family="JetBrains Mono" font-weight="700" font-size="30" fill="#8f94c4">{h}</text>' for h in (0, 6, 12, 18))
        + f'<text id="se-n" x="{CXE}" y="{CYE+30}" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="110" fill="#fff" opacity="0">5 × 90</text>'
        + f'<text x="{CXE}" y="{CYE+90}" text-anchor="middle" font-family="Poppins" font-weight="600" font-size="34" fill="#9aa0d0">Minuten Schlaf</text>')
hyp_pts = []
for c in range(4):
    for i, d in enumerate((0, 1, 2, 3, 2, 1, 0)):
        hyp_pts.append((120 + c*210 + i*35, 1150 + d*45))
hyp = (f'<g id="se-h" opacity="0"><polyline points="{" ".join(f"{x},{y}" for x, y in hyp_pts)}" fill="none" stroke="#7a8aff" stroke-width="8" stroke-linejoin="round"/>'
       + "".join(f'<rect x="{120+c*210-2}" y="1110" width="4" height="190" fill="#3a3f8a"/><text x="{225+c*210}" y="1340" text-anchor="middle" font-family="JetBrains Mono" font-size="24" fill="#8f94c4">90 min</text>' for c in range(4))
       + f'<text x="100" y="1140" font-family="Poppins" font-weight="600" font-size="24" fill="#9aa0d0">wach</text><text x="100" y="1310" font-family="Poppins" font-weight="600" font-size="24" fill="#9aa0d0">tief</text></g>'
       + f'<g id="se-ok" opacity="0">' + "".join(f'<circle cx="{330+c*210}" cy="1150" r="22" fill="{LIME}"/>' for c in range(4)) + '</g>')
scene("se", S0, S1, card_bg("se") + ring + hyp)
for k in range(5):
    tw(f'tl.fromTo("#se-s{k}",{{opacity:0}},{{opacity:1,duration:.3,ease:"sine.out"}},{t_fuenf - 0.3 + k*0.18:.3f});')
fadein("#se-n", t_fuenf, 0.4, 10)
fadein("#se-h", t_zyklus - 0.2, 0.5, 20)
tw(f'tl.to("#se-n",{{opacity:.15,duration:.4}},{t_zyklus - 0.2:.3f});')
fadein("#se-ok", t_fit - 0.3, 0.4, 0)

# F Smartwatch: Bewegung + Puls mit grünem Licht durch die Haut
S0, S1 = t_messen, t_wecker
watch = (f'<g id="sf-w"><rect x="300" y="430" width="480" height="560" rx="110" fill="#14163a" stroke="#3a3f8a" stroke-width="16"/>'
         f'<rect x="340" y="470" width="400" height="480" rx="80" fill="#0b0d22"/>'
         f'<text x="540" y="560" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="34" fill="#9aa0d0">SCHLAF</text>'
         f'<g id="sf-hr"><path d="M 380 700 L 450 700 L 475 640 L 505 770 L 530 680 L 555 700 L 700 700" stroke="{RED}" stroke-width="8" fill="none"/></g>'
         f'<text id="sf-bpm" x="540" y="830" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="60" fill="#fff">52 bpm</text>'
         f'<g id="sf-deep" opacity="0"><rect x="380" y="860" width="320" height="56" rx="28" fill="#7a8aff"/><text x="540" y="899" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="30" fill="#0b0d22">TIEFSCHLAF</text></g></g>')
strap = f'<rect x="380" y="0" width="320" height="440" fill="#262a5e"/><rect x="380" y="980" width="320" height="380" fill="#262a5e"/>'
xsec = (f'<g id="sf-x" opacity="0"><rect x="120" y="1000" width="840" height="300" rx="30" fill="{FIG}"/><rect x="120" y="1000" width="840" height="40" fill="#c98a66"/>'
        f'<path id="sf-vein" d="M 120 1180 Q 540 1140 960 1190" stroke="#b03030" stroke-width="34" fill="none"/>'
        + "".join(f'<rect x="{430+k*110}" y="980" width="40" height="22" rx="6" fill="{GREEN_LED}"/>'
                  f'<polygon id="sf-b{k}" points="{432+k*110},1000 {468+k*110},1000 {500+k*110},1170 {400+k*110},1170" fill="{GREEN_LED}" opacity=".25"/>' for k in range(3))
        + f'<text x="540" y="1260" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="30" fill="#5a2a24">grünes Licht · Blut schluckt es im Pulsschlag</text></g>')
move_ic = (f'<g id="sf-acc" opacity="0"><rect x="800" y="560" width="200" height="120" rx="20" fill="#0b0d22" stroke="#cfd3ff" stroke-width="4"/>'
           f'<text x="900" y="610" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="26" fill="#cfd3ff">BEWEGUNG</text>'
           f'<path d="M 830 650 q 20 -20 40 0 t 40 0 t 40 0 t 40 0" stroke="#e0a83a" stroke-width="6" fill="none"/></g>')
scene("sf", S0, S1, f'<rect width="1080" height="1920" fill="#0c0d22"/><circle cx="540" cy="700" r="600" fill="url(#cardglow)"/>' + strap + watch + move_ic + xsec)
tw(f'tl.fromTo("#sf-w",{{scale:.9,opacity:0,transformOrigin:"50% 50%"}},{{scale:1,opacity:1,duration:.5,ease:"sine.out"}},{S0:.3f});')
fadein("#sf-acc", t_spuert, 0.4, 10)
tw(f'tl.to("#sf-hr",{{x:-20,duration:.4,yoyo:true,repeat:9,ease:"sine.inOut"}},{t_puls:.3f});')
fadein("#sf-x", t_gruen - 0.2, 0.5, 30)
for k in range(3):
    tw(f'tl.fromTo("#sf-b{k}",{{opacity:.1}},{{opacity:.55,duration:.4,yoyo:true,repeat:7,ease:"sine.inOut"}},{t_gruen + k*0.1:.3f});')
tw(f'tl.fromTo("#sf-vein",{{attr:{{"stroke-width":30}}}},{{attr:{{"stroke-width":40}},duration:.45,yoyo:true,repeat:7,ease:"sine.inOut"}},{t_puls:.3f});')
fadein("#sf-deep", t_tief - 0.2, 0.4, 10)

# G Smart-Wecker am Ende eines Zyklus
S0, S1 = t_wecker, t_woche1
alarm = (f'<g id="sg-al" opacity="0"><rect x="560" y="300" width="420" height="200" rx="30" fill="#0b0d22" opacity=".92" stroke="{LIME}" stroke-width="5"/>'
         f'<text x="770" y="370" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="30" fill="{LIME}">SMART-WECKER</text>'
         f'<text x="770" y="455" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="64" fill="#fff">6:58</text></g>')
scene("sg", S0, S1, bed("sg") + alarm, drift=False)
fadein("#sg-al", S0 + 0.2, 0.4, -16)
shake("#sg-al", t_zyklus if False else S0 + 0.9, 4, 4)
tw(f'tl.set("#sg-fig-eyes-s",{{opacity:0}},{S0 + 1.2:.3f});'); tw(f'tl.set("#sg-fig-eyes-n",{{opacity:1}},{S0 + 1.2:.3f});')

# H Woche 1 → Woche 4: wacher, schneller
S0, S1 = t_woche1, t_soweit
meter = (f'<g id="sh-m"><rect x="140" y="420" width="800" height="70" rx="35" fill="#262a5e"/><rect id="sh-bar" x="140" y="420" width="800" height="70" rx="35" fill="#e0a83a"/>'
         f'<text x="540" y="400" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="40" fill="#fff">ENERGIE</text></g>'
         f'<g id="sh-w1" opacity="0">{pill("sh-p1", 300, 600, "WOCHE 1 · WACHER", "#3b6cff", "#fff", 36).replace("opacity=\"0\"", "")}</g>'
         f'<g id="sh-w4" opacity="0">{pill("sh-p4", 760, 600, "WOCHE 4 · SCHNELLER", RED, "#fff", 36).replace("opacity=\"0\"", "")}</g>')
speed = "".join(f'<rect id="sh-l{k}" x="{-200}" y="{1150+k*60}" width="{160+k*40}" height="8" rx="4" fill="#e8ecff" opacity=".6"/>' for k in range(4))
scene("sh", S0, S1, stadium("sh", goal=False) + meter + speed + figure("sh-fig", 560, 1420, 1.3, eyes="n"), drift=False)
tw(f'tl.fromTo("#sh-bar",{{scaleX:.3,transformOrigin:"0% 50%"}},{{scaleX:.6,transformOrigin:"0% 50%",duration:.8,ease:"sine.out"}},{t_woche1:.3f});')
fadein("#sh-w1", t_wacher - 0.3)
tw(f'tl.to("#sh-bar",{{scaleX:.95,duration:.8,ease:"sine.out"}},{t_woche4:.3f});')
fadein("#sh-w4", t_sprintest - 0.3)
walk_cycle("sh-fig", t_woche4, S1 + 0.3, period=0.28, bob=14)
for k in range(4):
    tw(f'tl.fromTo("#sh-l{k}",{{x:1300}},{{x:-300,duration:.5,repeat:5,ease:"none"}},{t_sprintest - 0.3 + k*0.08:.3f});')

# I Disziplin 3: Elfmeter – du läufst an
S0, S1 = t_soweit, t_wirst
keeper = (f'<g id="si-k"><rect x="505" y="760" width="70" height="120" rx="20" fill="#3cff8a"/><circle cx="540" cy="730" r="34" fill="{FIG}"/>'
          f'<rect x="460" y="770" width="40" height="22" rx="10" fill="#3cff8a"/><rect x="580" y="770" width="40" height="22" rx="10" fill="#3cff8a"/>'
          f'<circle cx="452" cy="780" r="16" fill="#fff"/><circle cx="628" cy="780" r="16" fill="#fff"/><rect x="515" y="880" width="20" height="60" fill="#1b1d25"/><rect x="545" y="880" width="20" height="60" fill="#1b1d25"/></g>')
goalI = (f'<rect x="300" y="640" width="480" height="300" fill="url(#netpat)" opacity=".55"/><rect x="290" y="630" width="500" height="14" fill="{NET}"/>'
         f'<rect x="290" y="630" width="14" height="310" fill="{NET}"/><rect x="776" y="630" width="14" height="310" fill="{NET}"/>')
ball = f'<g id="si-ball"><circle cx="540" cy="1230" r="34" fill="#fff"/><path d="M 528 1220 l 12 -8 l 12 8 l -5 14 l -14 0 Z" fill="#1e1a2e"/></g>'
scene("si", S0, S1, f'<rect width="1080" height="1920" fill="url(#skyg)"/><rect x="0" y="940" width="1080" height="980" fill="{GRASS1}"/>'
      + "".join(f'<rect x="0" y="{940+k*120}" width="1080" height="60" fill="{GRASS2}"/>' for k in range(8))
      + f'<rect x="200" y="940" width="680" height="8" fill="#e8ecff" opacity=".6"/><ellipse cx="540" cy="1250" rx="14" ry="5" fill="#e8ecff"/>'
      + goalI + keeper + ball + figure("si-fig", 430, 1560, 1.2, back=True) + scoreboard("si-sb", 0, 1, "DISZIPLIN 3 / 3 · ELFMETER"), drift=False)
tw(f'tl.to("#si-k",{{x:-30,duration:.5,yoyo:true,repeat:7,ease:"sine.inOut"}},{t_torwart:.3f});')
walk_cycle("si-fig", t_laeufst, t_laeufst + 1.0, period=0.32, bob=10)
tw(f'tl.to("#si-fig",{{x:60,y:-180,scale:.85,transformOrigin:"50% 100%",duration:1.0,ease:"power1.in"}},{t_laeufst:.3f});')
tw(f'tl.to("#si-cam",{{scale:1.12,svgOrigin:"540 1000",duration:1.2,ease:"sine.in"}},{t_laeufst:.3f});')

# J Auflösung + Frage
S0, S1 = t_wirst, TOTAL
scene("sj", S0, S1, bed("sj", sleeping_fig=True)
      + f'<g id="sj-q" opacity="0"><rect x="160" y="250" width="760" height="110" rx="24" fill="#0b0d22" opacity=".9"/>'
        f'<text x="540" y="325" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="50" fill="#fff">Was trainierst du zuerst?</text></g>'
      + pill("sj-p1", 290, 480, "SPRUNGKRAFT", "#e0a83a", "#0b0d22", 40) + pill("sj-p2", 700, 480, "SCHUSS", RED, "#fff", 40)
      + pill("sj-p3", 540, 620, "SCHLAF", "#7a8aff", "#0b0d22", 46)
      + f'<g id="sj-z">' + "".join(f'<text id="sj-z{k}" x="{380+k*40}" y="{900-k*50}" font-family="Poppins" font-weight="800" font-size="{40+k*14}" fill="#cfd3ff" opacity="0">z</text>' for k in range(3)) + '</g>')
for k in range(3):
    tw(f'tl.fromTo("#sj-z{k}",{{opacity:0,y:0}},{{opacity:.8,y:-60,duration:1.4,repeat:4,ease:"sine.out"}},{S0 + 0.3 + k*0.4:.3f});')
fadein("#sj-q", t_was - 0.2)
pop("#sj-p1", ws("Sprungkraft", t_was)); pop("#sj-p2", t_schuss); pop("#sj-p3", t_schlaf)
tw(f'tl.to("#sj-p3",{{scale:1.08,transformOrigin:"50% 50%",duration:.4,yoyo:true,repeat:5,ease:"sine.inOut"}},{t_schreib:.3f});')

# ================= SERIEN-BRANDING OBEN LINKS (Format B) =================
BRAND = []
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
KEY = {"RONALDO", "SPRUNGKRAFT", "KOPFBALL", "2,56", "LATTE", "TRAINING", "ZWANZIG", "20", "VERRÜCKT", "BETT", "SCHLAFEN", "5×", "90",
       "SCHLAFZYKLUS", "FIT", "SMARTWATCH", "BEWEGUNG", "PULS", "GRÜNEM", "LICHT", "TIEF", "WECKER", "ZYKLUS", "WACHER", "SCHNELLER",
       "ELFMETER", "TORWART", "WAHRSCHEINLICH", "SCHLÄFST", "SCHUSS", "SCHLAF", "KOMMENTARE"}
DISPLAY = {"fünfmal": "5×", "neunzig": "90", "neunzig?": "90?", "zwanzig": "20"}
SKIP = {"zwölf", "zwölf.", "dreißig.", "vierzig.", "Uhr"}


def norm(t):
    return re.sub(r"[^\wÄÖÜäöüß:]", "", t).upper()


words = []
for k, w in enumerate(W):
    nxt2 = " ".join(x["t"] for x in W[k:k+3]).lower()
    if nxt2.startswith("zwei meter sechsundfünfzig"): words.append({"t": "2,56 m", "s": w["s"], "e": W[k+2]["e"]}); continue
    if k >= 1 and W[k-1]["t"].lower() == "zwei" and w["t"] == "Meter": continue
    if k >= 2 and W[k-1]["t"] == "Meter" and w["t"].lower().startswith("sechsundfünfzig"): continue
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
{FIGC_DEFS}<pattern id="netpat" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M 0 0 L 30 30 M 30 0 L 0 30" stroke="#e8ecff" stroke-width="2"/></pattern>
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


danger("ov-d1", t_laeufst, t_wirst)

for sbid, tt, txt in SCORE_SWAP:
    pass
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
    <title>Besser als Ronaldo</title>
    <script src="assets/gsap.min.js"></script>
    <style>
      :root {{ --ground: {SKY1}; --ink: #ffffff; --accent: {RED}; --font-display: "Poppins", sans-serif; }}
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
