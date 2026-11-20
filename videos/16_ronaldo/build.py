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
t_vergleichen = ws("vergleichen"); t_fuenfd = ws("Fünf")
t_d1 = ws("Disziplin"); t_sprung = ws("Sprungkraft"); t_256 = ws("zwei"); t_latte1 = ws("Torlatte"); t_kommst = ws("kommst"); t_10 = ws("Eins", t_kommst)
t_d2 = ws("Disziplin", t_10); t_900 = ws("neunhundert"); t_schaffen = ws("schaffen"); t_jeden = ws("jeden", t_schaffen); t_20 = ws("Zwei", t_jeden + 0.3)
t_d3 = ws("Disziplin", t_20); t_30 = ws("dreißig"); t_bus = ws("Bus"); t_30b = ws("Drei", t_bus)
t_d4 = ws("Disziplin", t_30b); t_alk = ws("Alkohol"); t_cola1 = ws("Cola"); t_hand = ws("Hand"); t_40 = ws("Vier", t_hand)
t_d5 = ws("Disziplin", t_40); t_soll = ws("soll"); t_zockst = ws("zockst"); t_50 = ws("Fünf", t_zockst)
t_chance = ws("Chance"); t_vierzig = ws("vierzig"); t_juenger = ws("jünger"); t_kopieren = ws("kopieren")
t_trainiere = ws("Trainiere"); t_keiner = ws("keiner"); t_schlaf2 = ws("Schlaf", t_keiner); t_wasser = ws("Wasser"); t_hoer = ws("hör"); t_17 = ws("siebzehn")
t_sechzig = ws("sechzig"); t_welcher = ws("welcher"); t_schreib = ws("Schreib")

# ================= SZENEN (Format A · Vergleich, tagsüber) =================
GRASS1 = "#2f8a46"; GRASS2 = "#36994f"; NET = "#ffffff"


def fadein(sel, t, dur=0.45, dy=16):
    tw(f'tl.fromTo("{sel}",{{opacity:0,y:{dy}}},{{opacity:1,y:0,duration:{dur},ease:"sine.out"}},{t:.3f});')


def day_sky():
    return (f'<rect width="1080" height="1920" fill="url(#daysky)"/><circle cx="880" cy="330" r="80" fill="#fff4c2"/><circle cx="880" cy="330" r="220" fill="url(#sunglow)"/>'
            + "".join(f'<g id="cl{i}"><ellipse cx="{x}" cy="{y}" rx="{w}" ry="{w*0.35:.0f}" fill="#fff" opacity=".9"/><ellipse cx="{x+w*0.4:.0f}" cy="{y-w*0.18:.0f}" rx="{w*0.55:.0f}" ry="{w*0.3:.0f}" fill="#fff" opacity=".9"/></g>'
                      for i, (x, y, w) in enumerate(((180, 380, 110), (520, 300, 80), (700, 470, 95)))))


def stadium(prefix, goal=True, gx=560, gw=420, ground=1250, ppm=300):
    """Tagesstadion: Himmel mit Sonne/Wolken, bunte volle Tribünen, Fahnen, Werbebande, gemähter Rasen, Tor."""
    stands = "".join(f'<rect x="0" y="{560+k*70}" width="1080" height="60" fill="{"#c9ced9" if k%2 else "#b7bdcb"}"/>' for k in range(6))
    roof = '<rect x="0" y="520" width="1080" height="40" fill="#8a93a8"/><rect x="0" y="512" width="1080" height="10" fill="#e6e9f0"/>'
    crowd = "".join(f'<circle cx="{(k*41)%1080}" cy="{585+((k*37)%6)*70}" r="{9+(k%3)*2}" fill="{["#e0a83a","#3b6cff","#ff6b6b","#2a9d8f","#f4f1de","#7a5af5"][k%6]}"/>' for k in range(160))
    flags = "".join(f'<rect x="{x}" y="430" width="6" height="90" fill="#e6e9f0"/><path d="M {x+6} 432 l 60 14 l -60 14 Z" fill="{c}"/>' for x, c in ((60, "#e0a83a"), (330, "#3b6cff"), (640, "#ff6b6b"), (930, "#2a9d8f")))
    ads = "".join(f'<rect x="{k*270}" y="960" width="262" height="44" fill="{c}"/><text x="{k*270+131}" y="992" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="26" fill="#fff">{t}</text>'
                  for k, (c, t) in enumerate((("#3b6cff", "SPORT"), ("#e0a83a", "TOR!"), ("#2a9d8f", "FAIRPLAY"), ("#7a5af5", "ARENA"))))
    pitch = (f'<rect x="0" y="1004" width="1080" height="916" fill="{GRASS1}"/>'
             + "".join(f'<rect x="0" y="{1004+k*120}" width="1080" height="60" fill="{GRASS2}"/>' for k in range(8))
             + f'<rect x="0" y="{ground}" width="1080" height="8" fill="#fff" opacity=".8"/>')
    g = ""
    if goal:
        bar_y = ground - 2.44 * ppm
        g = (f'<g id="{prefix}-goal"><rect x="{gx}" y="{bar_y}" width="{gw}" height="{2.44*ppm}" fill="url(#netpat)" opacity=".7"/>'
             f'<rect x="{gx-10}" y="{bar_y-10}" width="{gw+20}" height="16" fill="{NET}"/><rect x="{gx-10}" y="{bar_y}" width="16" height="{2.44*ppm}" fill="{NET}"/>'
             f'<rect x="{gx+gw-6}" y="{bar_y}" width="16" height="{2.44*ppm}" fill="{NET}"/></g>')
    return day_sky() + roof + stands + crowd + flags + ads + pitch + g


def scoreboard(sid, l, r, label="", new=None):
    s = (f'<g id="{sid}"><rect x="200" y="150" width="680" height="120" rx="20" fill="#0b0d22" opacity=".92" stroke="#3a3f8a" stroke-width="4"/>'
         f'<text x="300" y="230" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="44" fill="#e0a83a">DU</text>'
         f'<text id="{sid}-sc" x="540" y="232" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="60" fill="#fff">{l} : {r}</text>'
         f'<text x="745" y="228" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="36" fill="#cfd3ff">RONALDO</text>'
         + (f'<text id="{sid}-new" x="540" y="232" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="60" fill="{RED}" opacity="0">{new[0]} : {new[1]}</text>' if new else "")
         + (f'<rect x="330" y="282" width="420" height="44" rx="22" fill="#0b0d22" opacity=".8"/><text x="540" y="313" text-anchor="middle" font-family="JetBrains Mono" font-weight="700" font-size="24" fill="#fff" letter-spacing="3">{label}</text>' if label else "")
         + '</g>')
    return s


def score_up(sid, t):
    tw(f'tl.to("#{sid}-sc",{{opacity:0,duration:.15}},{t:.3f});')
    tw(f'tl.fromTo("#{sid}-new",{{opacity:0,scale:1.4,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:.35,ease:"power2.out"}},{t + 0.1:.3f});')


def fact_card(cid, x, y, w, title, value, col=RED, op=0):
    return (f'<g id="{cid}" opacity="{op}"><rect x="{x}" y="{y}" width="{w}" height="150" rx="24" fill="#0b0d22" opacity=".9" stroke="{col}" stroke-width="5"/>'
            f'<text x="{x+w/2}" y="{y+52}" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="30" fill="#cfd3ff">{title}</text>'
            f'<text x="{x+w/2}" y="{y+120}" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="56" fill="{col}">{value}</text></g>')


def card_bg(cid):
    return (f'<rect width="1080" height="1920" fill="url(#daysky)"/><rect width="1080" height="1920" fill="#0b1a3a" opacity=".35"/>')


# A Hook
S0, S1 = 0.0, t_d1
scene("sa", S0, S1, stadium("sa") + scoreboard("sa-sb", 0, 0) + figure("sa-fig", 380, 1420, 1.4, eyes="n")
      + pill("sa-p", 540, 700, "5 DISZIPLINEN", RED, "#fff", 56))
fadein("#sa-sb", 0.05, 0.4, -20); pop("#sa-p", t_fuenfd, 0.4, 0.9)
tw(f'tl.set("#sa-fig-eyes-n",{{opacity:0}},{t_vergleichen:.3f});'); tw(f'tl.set("#sa-fig-eyes-f",{{opacity:1}},{t_vergleichen:.3f});')

# B Disziplin 1: Sprungkraft
S0, S1 = t_d1, t_d2
G, PPM = 1250, 300
ruler = (f'<rect x="70" y="{G-2.8*PPM}" width="16" height="{2.8*PPM}" fill="#fff" opacity=".9"/>'
         + "".join(f'<rect x="70" y="{G-m*PPM:.0f}" width="44" height="6" fill="#fff"/><text x="124" y="{G-m*PPM+10:.0f}" font-family="JetBrains Mono" font-weight="700" font-size="28" fill="#0b0d22">{m:.1f} m</text>'
                   for m in (0.5, 1.0, 1.5, 2.0, 2.5)))
r_line = (f'<g id="sb-r" opacity="0"><rect x="60" y="{G-2.56*PPM-3}" width="960" height="6" fill="{RED}"/>'
          f'<rect x="590" y="{G-2.56*PPM-74}" width="400" height="58" rx="12" fill="{RED}"/>'
          f'<text x="790" y="{G-2.56*PPM-33}" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="34" fill="#fff">RONALDO 2,56 m</text></g>')
du_line = (f'<g id="sb-du" opacity="0"><rect x="60" y="{G-2.12*PPM-3}" width="560" height="6" fill="#e0a83a"/>'
           f'<rect x="200" y="{G-2.12*PPM+14}" width="260" height="54" rx="12" fill="#e0a83a"/>'
           f'<text x="330" y="{G-2.12*PPM+52}" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="32" fill="#0b0d22">DU 2,12 m</text></g>')
scene("sb", S0, S1, stadium("sb", gx=560, gw=420, ground=G, ppm=PPM) + ruler + scoreboard("sb-sb", 0, 0, "1 · SPRUNGKRAFT", (0, 1))
      + figure("sb-fig", 380, G, 1.4, eyes="f") + label("sb-bl", 780, G - 2.44 * PPM + 70, "LATTE 2,44 m", "#0b0d22", 30, fill="#ffffff") + r_line + du_line, drift=False)
tw(f'tl.fromTo("#sb-r",{{opacity:0,scaleX:0,transformOrigin:"0% 50%"}},{{opacity:1,scaleX:1,duration:.6,ease:"power2.out"}},{t_256:.3f});')
fadein("#sb-bl", t_latte1 - 0.2, 0.4, 0)
tw(f'tl.to("#sb-fig",{{y:-12,scaleY:.94,transformOrigin:"50% 100%",duration:.18,ease:"sine.in"}},{t_kommst - 0.35:.3f});')
tw(f'tl.to("#sb-fig",{{y:-140,scaleY:1.03,duration:.38,ease:"power2.out"}},{t_kommst - 0.17:.3f});')
tw(f'tl.to("#sb-fig",{{y:0,scaleY:1,duration:.38,ease:"power2.in"}},{t_kommst + 0.21:.3f});')
tw(f'tl.set("#sb-fig-eyes-f",{{opacity:0}},{t_kommst + 0.2:.3f});'); tw(f'tl.set("#sb-fig-eyes-w",{{opacity:1}},{t_kommst + 0.2:.3f});')
fadein("#sb-du", t_kommst + 0.3, 0.4, 0)
score_up("sb-sb", t_10)

# C Disziplin 2: Tore – 900+ vs. 2,5 Jahre jeden Tag
S0, S1 = t_d2, t_d3
balls = "".join(f'<circle id="sc-b{k}" cx="{140+(k%10)*88}" cy="{1060+(k//10)*80}" r="26" fill="#fff" stroke="#0b0d22" stroke-width="4" opacity="0"/>' for k in range(30))
counter = "".join(f'<text id="sc-c{k}" x="540" y="620" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="150" fill="{RED}" opacity="0">{n}</text>' for k, n in enumerate((0, 150, 380, 610, 800, "900+")))
scene("sc", S0, S1, stadium("sc", gx=330, gw=420) + scoreboard("sc-sb", 0, 1, "2 · TORE", (0, 2))
      + f'<rect x="240" y="470" width="600" height="190" rx="30" fill="#0b0d22" opacity=".88"/>' + counter
      + f'<text x="540" y="700" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="34" fill="#0b0d22">RONALDO · TORE IN DER KARRIERE</text>'
      + fact_card("sc-f", 220, 1050, 640, "DU · 1 TOR JEDEN TAG", "≈ 2,5 JAHRE", "#e0a83a") + balls, drift=False)
steps_n = 6
for k in range(steps_n):
    a = t_900 - 0.4 + k * 0.16
    tw(f'tl.set("#sc-c{k}",{{opacity:1}},{a:.3f});')
    if k < steps_n - 1:
        tw(f'tl.set("#sc-c{k}",{{opacity:0}},{a + 0.16:.3f});')
fadein("#sc-f", t_jeden - 0.3, 0.45, 20)
score_up("sc-sb", t_20)

# D Disziplin 3: Tempo – Ronaldo 30+ km/h, du wirst vom Bus überholt
S0, S1 = t_d3, t_d4
bus = (f'<g id="sd-bus"><rect x="-520" y="1110" width="480" height="230" rx="30" fill="#e0a83a"/>'
       + "".join(f'<rect x="{-500+k*92}" y="1140" width="74" height="80" rx="8" fill="#bfe4ff"/>' for k in range(5))
       + f'<rect x="-520" y="1260" width="480" height="18" fill="#b8862a"/><circle cx="-440" cy="1345" r="38" fill="#1b1d25"/><circle cx="-130" cy="1345" r="38" fill="#1b1d25"/>'
       f'<text x="-280" y="1310" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="34" fill="#0b0d22">LINIE 7</text></g>')
bars = (f'<g id="sd-bars"><rect x="140" y="470" width="800" height="70" rx="35" fill="#0b0d22" opacity=".85"/><rect id="sd-rb" x="140" y="470" width="800" height="70" rx="35" fill="{RED}"/>'
        f'<text x="160" y="518" font-family="Poppins" font-weight="800" font-size="34" fill="#fff">RONALDO · 30+ km/h</text>'
        f'<rect x="140" y="570" width="800" height="70" rx="35" fill="#0b0d22" opacity=".85"/><rect id="sd-db" x="140" y="570" width="800" height="70" rx="35" fill="#e0a83a"/>'
        f'<text x="160" y="618" font-family="Poppins" font-weight="800" font-size="34" fill="#0b0d22">DU</text></g>')
scene("sd", S0, S1, stadium("sd", goal=False) + f'<rect x="0" y="1270" width="1080" height="110" fill="#5a5f6e"/>'
      + "".join(f'<rect x="{x}" y="1320" width="80" height="10" fill="#fff"/>' for x in range(0, 1080, 160))
      + scoreboard("sd-sb", 0, 2, "3 · TEMPO", (0, 3)) + bars + bus + figure("sd-fig", 420, 1440, 1.2, eyes="f"), drift=False)
tw(f'tl.fromTo("#sd-rb",{{scaleX:.05,transformOrigin:"0% 50%"}},{{scaleX:1,duration:.8,ease:"power2.out"}},{t_30 - 0.2:.3f});')
tw(f'tl.fromTo("#sd-db",{{scaleX:.05,transformOrigin:"0% 50%"}},{{scaleX:.62,duration:.8,ease:"power2.out"}},{t_30 + 0.3:.3f});')
walk_cycle("sd-fig", S0, S1 + 0.3, period=0.34, bob=12)
tw(f'tl.to("#sd-bus",{{x:1700,duration:1.6,ease:"none"}},{t_bus - 0.6:.3f});')
tw(f'tl.set("#sd-fig-eyes-f",{{opacity:0}},{t_bus:.3f});'); tw(f'tl.set("#sd-fig-eyes-w",{{opacity:1}},{t_bus:.3f});')
score_up("sd-sb", t_30b)

# E Disziplin 4: Ernährung – kein Alkohol, Cola stehen lassen vs. du mit Cola
S0, S1 = t_d4, t_d5
ron_card = (f'<g id="se-r" opacity="0"><rect x="70" y="420" width="420" height="560" rx="30" fill="#0b0d22" opacity=".9" stroke="{RED}" stroke-width="5"/>'
            f'<text x="280" y="490" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="38" fill="#fff">RONALDO</text>'
            f'<rect x="245" y="530" width="70" height="170" rx="20" fill="#bfe4ff"/><rect x="262" y="508" width="36" height="28" rx="6" fill="#3b6cff"/>'
            f'<circle cx="400" cy="590" r="34" fill="{LIME}"/><path d="M 384 590 l 12 12 l 22 -24" stroke="#0b0d22" stroke-width="8" fill="none"/>'
            f'<rect x="140" y="760" width="60" height="120" rx="12" fill="#8b1e1e"/><rect x="330" y="760" width="40" height="130" rx="10" fill="#4a7a3a"/>'
            + xmark("se-x1", 170, 820, 60, 1) + xmark("se-x2", 350, 825, 60, 1)
            + f'<text x="280" y="950" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="28" fill="#cfd3ff">Wasser · kein Alkohol</text></g>')
can = (f'<g id="se-can" opacity="0"><rect x="808" y="1130" width="56" height="96" rx="12" fill="#c8102e"/><rect x="808" y="1160" width="56" height="16" fill="#fff" opacity=".9"/>'
       f'<rect x="814" y="1122" width="44" height="10" rx="4" fill="#c0c0c0"/></g>')
scene("se", S0, S1, stadium("se", goal=False) + scoreboard("se-sb", 0, 3, "4 · ERNÄHRUNG", (0, 4)) + ron_card
      + figure("se-fig", 740, 1420, 1.4, eyes="n") + can, drift=False)
fadein("#se-r", t_alk - 0.4, 0.45, 20)
fadein("#se-can", t_hand - 0.5, 0.4, 10)
tw(f'tl.set("#se-fig-eyes-n",{{opacity:0}},{t_hand:.3f});'); tw(f'tl.set("#se-fig-eyes-f",{{opacity:1}},{t_hand:.3f});')
score_up("se-sb", t_40)

# F Disziplin 5: Schlaf – 5 × 90 min vs. Zocken bis 3 Uhr
S0, S1 = t_d5, t_chance
room = (f'<rect x="0" y="380" width="1080" height="1540" fill="#1c1f45"/><rect x="0" y="1250" width="1080" height="670" fill="#2a2440"/>'
        f'<rect x="560" y="820" width="420" height="250" rx="16" fill="#0b0d22" stroke="#3a3f8a" stroke-width="10"/><rect x="580" y="840" width="380" height="210" fill="#3b6cff" opacity=".85"/>'
        f'<circle cx="770" cy="945" r="200" fill="#3b6cff" opacity=".18"/><rect x="560" y="1070" width="420" height="40" fill="#4a3a5a"/>'
        f'<rect x="80" y="840" width="230" height="110" rx="20" fill="#0b0d22" stroke="#cfd3ff" stroke-width="4"/>'
        f'<text x="195" y="918" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="64" fill="{RED}">3:00</text>')
pad = f'<g id="sf-pad"><rect x="300" y="1150" width="130" height="62" rx="28" fill="#1b1d25"/><circle cx="335" cy="1180" r="9" fill="#e0a83a"/><circle cx="398" cy="1180" r="9" fill="#3b6cff"/></g>'
ron5 = (f'<g id="sf-r" opacity="0"><rect x="60" y="420" width="560" height="170" rx="30" fill="#0b0d22" opacity=".92" stroke="#7a8aff" stroke-width="5"/>'
        f'<text x="340" y="485" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="34" fill="#fff">RONALDO · 5 × 90 MIN</text>'
        + "".join(f'<circle cx="{160+k*90}" cy="545" r="26" fill="{MOON}"/><circle cx="{172+k*90}" cy="537" r="22" fill="#0b0d22"/>' for k in range(5)) + '</g>')
scene("sf", S0, S1, card_bg("sf") + room + scoreboard("sf-sb", 0, 4, "5 · SCHLAF", (0, 5)) + ron5 + figure("sf-fig", 365, 1420, 1.3, eyes="f") + pad, drift=False)
fadein("#sf-r", t_soll - 0.2, 0.45, 20)
tw(f'tl.to("#sf-pad",{{x:6,duration:.12,yoyo:true,repeat:15,ease:"sine.inOut"}},{t_zockst:.3f});')
score_up("sf-sb", t_50)

# G Wendung: deine Chance – Ronaldo über 40, du bist jünger
S0, S1 = t_chance, t_trainiere
scene("sg", S0, S1, stadium("sg", goal=False) + scoreboard("sg-sb", 0, 5, "ENDSTAND?")
      + fact_card("sg-a", 120, 470, 400, "RONALDO", "40+", RED) + fact_card("sg-b", 560, 470, 400, "DU", "JÜNGER", "#e0a83a")
      + pill("sg-p", 540, 760, "SEINE REGELN KOPIEREN", "#0b0d22", "#fff", 46) + figure("sg-fig", 540, 1420, 1.4, eyes="n"))
fadein("#sg-a", t_vierzig - 0.3); fadein("#sg-b", t_juenger - 0.2); pop("#sg-p", t_kopieren - 0.2)

# H Tipps zum Thema: jeden Tag trainieren · Schlaf + Wasser · nie aufhören (Profi mit 17)
S0, S1 = t_trainiere, t_sechzig
tips = (fact_card("sh-t1", 120, 370, 840, "AUCH WENN KEINER ZUSCHAUT", "JEDEN TAG TRAINIEREN", "#e0a83a")
        + fact_card("sh-t2", 120, 535, 840, "WIE EIN PROFI", "SCHLAF + WASSER", "#3b6cff")
        + fact_card("sh-t3", 120, 700, 840, "PROFI MIT 17", "NIE AUFHÖREN", RED))
ball = f'<g id="sh-ball"><circle cx="600" cy="1350" r="30" fill="#fff" stroke="#0b0d22" stroke-width="4"/></g>'
scene("sh", S0, S1, stadium("sh", goal=False) + f'<g transform="translate(0,-20)">' + scoreboard("sh-sb", 0, 5) + '</g>' + tips + figure("sh-fig", 520, 1420, 1.3, eyes="n") + ball, drift=False)
fadein("#sh-t1", t_trainiere, 0.4, 20); fadein("#sh-t2", t_schlaf2 - 0.1, 0.4, 20); fadein("#sh-t3", t_hoer - 0.1, 0.4, 20)
tw(f'tl.to("#sh-ball",{{y:-110,duration:.32,yoyo:true,repeat:{int((S1-S0)/0.32)},ease:"power1.out"}},{S0:.3f});')

# I Ende: Wenn er 60 ist … – in welcher Disziplin schlägst du ihn zuerst?
S0, S1 = t_sechzig, TOTAL
pills = "".join(pill(f"si-p{k}", x, y, t, c, fg, 36) for k, (x, y, t, c, fg) in enumerate(
    ((290, 620, "SPRUNG", "#e0a83a", "#0b0d22"), (790, 620, "TORE", RED, "#fff"), (290, 750, "TEMPO", "#3b6cff", "#fff"),
     (790, 750, "ERNÄHRUNG", "#2a9d8f", "#fff"), (540, 880, "SCHLAF", "#7a5af5", "#fff"))))
scene("si", S0, S1, stadium("si") + scoreboard("si-sb", "?", 5, "IN 20 JAHREN?")
      + f'<g id="si-q" opacity="0"><rect x="100" y="420" width="880" height="110" rx="24" fill="#0b0d22" opacity=".9"/>'
        f'<text x="540" y="495" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="46" fill="#fff">Wo schlägst du ihn zuerst?</text></g>'
      + pills + figure("si-fig", 360, 1420, 1.4, eyes="n"))
fadein("#si-q", t_welcher - 0.2)
for k in range(5):
    pop(f"#si-p{k}", t_welcher + 0.15 + k * 0.18, 0.35, 0.9)
tw(f'tl.to("#si-p4",{{scale:1.08,transformOrigin:"50% 50%",duration:.4,yoyo:true,repeat:5,ease:"sine.inOut"}},{t_schreib:.3f});')

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
KEY = {"RONALDO", "FÜNF", "DISZIPLINEN", "SPRUNGKRAFT", "2,56", "TORLATTE", "LATTE", "1:0", "2:0", "3:0", "4:0", "5:0", "TORE", "900",
       "2,5", "TEMPO", "30", "BUS", "ERNÄHRUNG", "ALKOHOL", "COLA", "SCHLAF", "5×", "90", "ZOCKST", "CHANCE", "40.", "JÜNGER", "KOPIEREN",
       "TRAINIERE", "KEINER", "WASSER", "AUFHÖREN", "HÖR", "17", "PROFI", "60", "KOMMENTARE"}
DISPLAY = {"neunhundert": "900", "dreißig": "30", "zweieinhalb": "2,5", "fünfmal": "5×", "neunzig": "90", "vierzig.": "40.", "siebzehn": "17", "sechzig": "60"}
SKIP = {"zwölf", "zwölf.", "dreißig.", "vierzig.", "Uhr"}


def norm(t):
    return re.sub(r"[^\wÄÖÜäöüß:]", "", t).upper()


words = []
NUMW = {"eins": "1", "zwei": "2", "drei": "3", "vier": "4", "fünf": "5"}
skip = 0
for k, w in enumerate(W):
    if skip: skip -= 1; continue
    nxt2 = " ".join(x["t"] for x in W[k:k+3]).lower()
    if nxt2.startswith("zwei meter sechsundfünfzig"): words.append({"t": "2,56 m.", "s": w["s"], "e": W[k+2]["e"]}); skip = 2; continue
    if nxt2.startswith("drei uhr nachts"): words.append({"t": "3 Uhr nachts.", "s": w["s"], "e": W[k+2]["e"]}); skip = 2; continue
    m = nxt2.split(" ")
    if len(m) == 3 and m[0] in NUMW and m[1] == "zu" and m[2].startswith("null"): words.append({"t": f"{NUMW[m[0]]}:0" + ("." if W[k+2]["t"].endswith(".") else ""), "s": w["s"], "e": W[k+2]["e"]}); skip = 2; continue
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
{FIGC_DEFS}<linearGradient id="daysky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3f8fe0"/><stop offset=".55" stop-color="#8cc6f5"/><stop offset="1" stop-color="#d9efff"/></linearGradient>
<radialGradient id="sunglow"><stop offset="0" stop-color="#fff4c2" stop-opacity=".6"/><stop offset="1" stop-color="#fff4c2" stop-opacity="0"/></radialGradient>
<pattern id="netpat" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M 0 0 L 30 30 M 30 0 L 0 30" stroke="#e8ecff" stroke-width="2"/></pattern>
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


for sbid, tt, txt in []:
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
