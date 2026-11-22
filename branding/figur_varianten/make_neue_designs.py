"""6 neue Hauptfiguren-Designs (verschiedene Typen, Hauttöne, Outfits) – 3x2-Raster, 2160x2160."""
import os


def face(x, y, sk, sk2, iris, brow, mood="n", lashes=False, glasses=False):
    out = (f'<rect x="{x-24}" y="{y+215}" width="48" height="55" rx="14" fill="{sk2}"/>'
           f'<path d="M {x-72} {y+95} Q {x-78} {y+215} {x} {y+238} Q {x+78} {y+215} {x+72} {y+95} Q {x} {y+20} {x-72} {y+95} Z" fill="{sk}"/>'
           f'<path d="M {x+30} {y+60} Q {x+78} {y+120} {x+60} {y+200} Q {x+76} {y+150} {x+72} {y+95} Z" fill="{sk2}" opacity=".35"/>'
           f'<ellipse cx="{x-74}" cy="{y+150}" rx="11" ry="18" fill="{sk2}"/><ellipse cx="{x+74}" cy="{y+150}" rx="11" ry="18" fill="{sk2}"/>')
    for s in (-1, 1):
        out += (f'<ellipse cx="{x+s*34}" cy="{y+158}" rx="18" ry="15" fill="#fff"/>'
                f'<circle cx="{x+s*34}" cy="{y+160}" r="10" fill="{iris}"/><circle cx="{x+s*34}" cy="{y+161}" r="5" fill="#0b0d22"/><circle cx="{x+s*38}" cy="{y+155}" r="3" fill="#fff"/>'
                f'<path d="M {x+s*14} {y+134} Q {x+s*34} {y+124} {x+s*56} {y+134}" stroke="{brow}" stroke-width="7" fill="none" stroke-linecap="round"/>')
        if lashes:
            out += f'<path d="M {x+s*16} {y+150} Q {x+s*34} {y+140} {x+s*54} {y+150} l {s*8} -6" stroke="#1a1414" stroke-width="5" fill="none" stroke-linecap="round"/>'
    if glasses:
        out += (f'<circle cx="{x-34}" cy="{y+158}" r="27" fill="none" stroke="#1e1a2e" stroke-width="6"/><circle cx="{x+34}" cy="{y+158}" r="27" fill="none" stroke="#1e1a2e" stroke-width="6"/>'
                f'<path d="M {x-7} {y+156} L {x+7} {y+156}" stroke="#1e1a2e" stroke-width="6"/>')
    out += (f'<path d="M {x} {y+178} Q {x+8} {y+194} {x-2} {y+198}" stroke="{sk2}" stroke-width="4" fill="none" stroke-linecap="round"/>'
            f'<circle cx="{x-46}" cy="{y+196}" r="11" fill="#e98f7a" opacity=".28"/><circle cx="{x+46}" cy="{y+196}" r="11" fill="#e98f7a" opacity=".28"/>')
    out += (f'<path d="M {x-16} {y+212} Q {x} {y+224} {x+16} {y+212}" stroke="#8a3a30" stroke-width="5" fill="none" stroke-linecap="round"/>' if mood == "n"
            else f'<path d="M {x-18} {y+208} Q {x} {y+232} {x+18} {y+208} Z" fill="#7a2a24"/>')
    return out


def legs(x, y, p1, p2, shoe, sole="#1e1a2e", wide=False, shorts=False, sk=None):
    w = 14 if wide else 0
    out = ""
    if shorts:
        out += (f'<path d="M {x-62} {y+500} L {x-70} {y+640} L {x-10} {y+640} L {x-6} {y+540} Z" fill="{p1}"/><path d="M {x+62} {y+500} L {x+70} {y+640} L {x+10} {y+640} L {x+6} {y+540} Z" fill="{p2}"/>'
                f'<rect x="{x-62}" y="{y+640}" width="44" height="230" rx="18" fill="{sk}"/><rect x="{x+18}" y="{y+640}" width="44" height="230" rx="18" fill="{sk}"/>'
                f'<rect x="{x-64}" y="{y+800}" width="48" height="50" rx="10" fill="#fff"/><rect x="{x+16}" y="{y+800}" width="48" height="50" rx="10" fill="#fff"/>')
    else:
        out += (f'<path d="M {x-62-w} {y+500} L {x-74-w} {y+870} L {x-14} {y+870} L {x-6} {y+540} Z" fill="{p1}"/>'
                f'<path d="M {x+62+w} {y+500} L {x+74+w} {y+870} L {x+14} {y+870} L {x+6} {y+540} Z" fill="{p2}"/>')
    out += (f'<path d="M {x-102} {y+868} Q {x-102} {y+838} {x-60} {y+840} L {x-12} {y+846} L {x-10} {y+885} L {x-104} {y+885} Z" fill="{shoe}"/>'
            f'<path d="M {x+102} {y+868} Q {x+102} {y+838} {x+60} {y+840} L {x+12} {y+846} L {x+10} {y+885} L {x+104} {y+885} Z" fill="{shoe}"/>'
            f'<rect x="{x-106}" y="{y+880}" width="98" height="14" rx="6" fill="{sole}"/><rect x="{x+8}" y="{y+880}" width="98" height="14" rx="6" fill="{sole}"/>')
    return out


def arms(x, y, c1, c2, sk, sk2, cuff=None):
    out = (f'<path d="M {x-120} {y+265} Q {x-190} {y+380} {x-175} {y+510} L {x-130} {y+510} Q {x-140} {y+390} {x-100} {y+300} Z" fill="{c1}"/>'
           f'<path d="M {x+120} {y+265} Q {x+190} {y+380} {x+175} {y+510} L {x+130} {y+510} Q {x+140} {y+390} {x+100} {y+300} Z" fill="{c2}"/>')
    if cuff:
        out += f'<rect x="{x-178}" y="{y+490}" width="50" height="24" rx="10" fill="{cuff}"/><rect x="{x+128}" y="{y+490}" width="50" height="24" rx="10" fill="{cuff}"/>'
    return out + f'<ellipse cx="{x-152}" cy="{y+535}" rx="22" ry="26" fill="{sk}"/><ellipse cx="{x+152}" cy="{y+535}" rx="22" ry="26" fill="{sk2}"/>'


def torso(x, y, c1, c2, h=560):
    return (f'<path d="M {x-135} {y+255} Q {x-158} {y+400} {x-128} {y+h} L {x+128} {y+h} Q {x+158} {y+400} {x+135} {y+255} Q {x} {y+215} {x-135} {y+255} Z" fill="{c1}"/>'
            f'<path d="M {x+60} {y+260} Q {x+150} {y+400} {x+128} {y+h} L {x+90} {y+h} Q {x+110} {y+400} {x+40} {y+265} Z" fill="{c2}" opacity=".55"/>')


# 1 · STREET-KID: Afro, dunkler Hautton, Varsity-Jacke Navy/Creme, Cap rückwärts
def d1(x, y):
    SK, SK2 = "#8d5a3b", "#6e4329"
    jacket = (torso(x, y, "#1f2d5c", "#16214a") + f'<rect x="{x-60}" y="{y+262}" width="120" height="290" fill="#f1e6cf"/>'
              f'<path d="M {x} {y+262} L {x} {y+552}" stroke="#c9b48a" stroke-width="4"/>'
              + "".join(f'<circle cx="{x-14}" cy="{y+300+k*55}" r="6" fill="#c9b48a"/>' for k in range(5))
              + f'<rect x="{x-128}" y="{y+530}" width="256" height="30" fill="#f1e6cf"/><rect x="{x-128}" y="{y+537}" width="256" height="8" fill="#1f2d5c"/>'
              f'<text x="{x-95}" y="{y+360}" font-family="Poppins" font-weight="800" font-size="56" fill="#f1e6cf">7</text>')
    afro = (f'<circle cx="{x}" cy="{y+80}" r="104" fill="#1a1210"/>' + "".join(f'<circle cx="{x+dx}" cy="{y+dy}" r="40" fill="#1a1210"/>' for dx, dy in ((-92, 120), (92, 120), (-62, 20), (62, 20), (0, -6), (-100, 70), (100, 70))))
    cap = (f'<path d="M {x-80} {y+92} Q {x} {y+30} {x+80} {y+92} L {x+84} {y+108} L {x-84} {y+108} Z" fill="#f1e6cf"/>'
           f'<rect x="{x-118}" y="{y+96}" width="70" height="16" rx="8" fill="#f1e6cf"/><rect x="{x-12}" y="{y+56}" width="24" height="10" rx="5" fill="#1f2d5c"/>')
    return (afro + legs(x, y, "#3a4a6a", "#2f3d5a", "#f2f3f5", "#c74545") + arms(x, y, "#f1e6cf", "#d9cdb4", SK, SK2, cuff="#1f2d5c") + jacket
            + face(x, y, SK, SK2, "#5a3b26", "#1a1210") + cap)


# 2 · SPORTY GIRL: Pferdeschwanz, Trainingsjacke Türkis, schwarze Leggings
def d2(x, y):
    SK, SK2 = "#f0c09a", "#d39c78"
    top = (torso(x, y, "#2a9d8f", "#21877b", 540) + f'<path d="M {x-135} {y+340} L {x+135} {y+340}" stroke="#fff" stroke-width="12"/>'
           f'<path d="M {x} {y+262} L {x} {y+540}" stroke="#e9f5f2" stroke-width="6"/><path d="M {x-40} {y+250} L {x} {y+290} L {x+40} {y+250}" stroke="#e9f5f2" stroke-width="10" fill="none"/>')
    hair = (f'<path d="M {x-80} {y+150} Q {x-95} {y+30} {x} {y+22} Q {x+95} {y+30} {x+80} {y+150} Q {x+70} {y+70} {x} {y+66} Q {x-70} {y+70} {x-80} {y+150} Z" fill="#6b3a1f"/>'
            f'<path d="M {x+70} {y+60} Q {x+170} {y+80} {x+150} {y+260} Q {x+140} {y+150} {x+90} {y+110} Z" fill="#6b3a1f"/><rect x="{x+72}" y="{y+56}" width="26" height="22" rx="8" fill="#ff8a3d"/>'
            f'<path d="M {x-30} {y+40} Q {x+10} {y+70} {x+60} {y+60}" stroke="#8a5030" stroke-width="6" fill="none"/>')
    return (legs(x, y, "#1b1d25", "#15171e", "#ff8a3d") + arms(x, y, "#2a9d8f", "#21877b", SK, SK2, cuff="#fff") + top
            + face(x, y, SK, SK2, "#2a9d8f", "#6b3a1f", lashes=True) + hair)


# 3 · TECH-NERD: Brille, wuschelige braune Haare, grauer Hoodie, Kopfhörer um den Hals, Rucksack
def d3(x, y):
    SK, SK2 = "#e8b896", "#cc977a"
    pack = f'<rect x="{x-150}" y="{y+280}" width="300" height="300" rx="50" fill="#3b6cff"/><rect x="{x-110}" y="{y+420}" width="220" height="110" rx="24" fill="#2f57d4"/>'
    top = (torso(x, y, "#7b8194", "#646a7c") + f'<path d="M {x-75} {y+420} L {x+75} {y+420} L {x+65} {y+495} L {x-65} {y+495} Z" fill="#646a7c"/>'
           f'<rect x="{x-128}" y="{y+520}" width="256" height="40" rx="16" fill="#646a7c"/>'
           f'<path d="M {x-118} {y+265} L {x-90} {y+520} M {x+118} {y+265} L {x+90} {y+520}" stroke="#2f57d4" stroke-width="22" stroke-linecap="round"/>'
           f'<path d="M {x-70} {y+255} Q {x} {y+330} {x+70} {y+255}" stroke="#1e1a2e" stroke-width="14" fill="none"/>'
           f'<circle cx="{x-72}" cy="{y+262}" r="26" fill="#1e1a2e"/><circle cx="{x+72}" cy="{y+262}" r="26" fill="#1e1a2e"/><circle cx="{x-72}" cy="{y+262}" r="12" fill="{LIME}"/><circle cx="{x+72}" cy="{y+262}" r="12" fill="{LIME}"/>')
    hair = "".join(f'<circle cx="{x+dx}" cy="{y+dy}" r="{r}" fill="#5a3a24"/>' for dx, dy, r in ((-60, 70, 40), (-20, 45, 44), (25, 45, 44), (62, 70, 38), (-75, 110, 26), (78, 110, 26), (0, 70, 40)))
    return (pack + legs(x, y, "#2c3a52", "#26324a", "#f2f3f5", "#3b6cff") + arms(x, y, "#7b8194", "#646a7c", SK, SK2, cuff="#646a7c") + top
            + face(x, y, SK, SK2, "#3a8a5a", "#5a3a24", glasses=True) + hair)


# 4 · SKATER: Bucket Hat, offenes Karohemd (Grün) über weißem Shirt, weite Jeans
def d4(x, y):
    SK, SK2 = "#d9a27a", "#bb825e"
    shirt = (torso(x, y, "#f4f1e8", "#dcd6c8", 540)
             + f'<path d="M {x-135} {y+255} Q {x-158} {y+400} {x-128} {y+560} L {x-30} {y+560} L {x-45} {y+262} Z" fill="#3f7f4a"/>'
             f'<path d="M {x+135} {y+255} Q {x+158} {y+400} {x+128} {y+560} L {x+30} {y+560} L {x+45} {y+262} Z" fill="#356e40"/>'
             + "".join(f'<path d="M {x+s*(40+k*30)} {y+262} L {x+s*(36+k*30)} {y+560}" stroke="#1f4a28" stroke-width="5" opacity=".7"/>' for s in (-1, 1) for k in range(3))
             + "".join(f'<path d="M {x-135} {y+320+k*70} L {x-35} {y+320+k*70} M {x+35} {y+320+k*70} L {x+135} {y+320+k*70}" stroke="#1f4a28" stroke-width="5" opacity=".6"/>' for k in range(4))
             + f'<text x="{x}" y="{y+420}" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="40" fill="#e0a83a">☺</text>')
    hat = (f'<path d="M {x-120} {y+95} Q {x} {y+70} {x+120} {y+95} L {x+100} {y+115} Q {x} {y+95} {x-100} {y+115} Z" fill="#2b2b33"/>'
           f'<path d="M {x-80} {y+95} Q {x-70} {y+10} {x} {y+8} Q {x+70} {y+10} {x+80} {y+95} Z" fill="#33333d"/><rect x="{x-80}" y="{y+80}" width="160" height="14" fill="#e0a83a"/>'
           f'<path d="M {x-75} {y+110} Q {x-85} {y+150} {x-70} {y+175}" stroke="#2a1b12" stroke-width="14" fill="none"/><path d="M {x+75} {y+110} Q {x+85} {y+150} {x+70} {y+175}" stroke="#2a1b12" stroke-width="14" fill="none"/>')
    return (legs(x, y, "#4a6fa5", "#3f5f8f", "#2b2b33", "#f2f3f5", wide=True) + arms(x, y, "#3f7f4a", "#356e40", SK, SK2, cuff="#2a5e34") + shirt
            + face(x, y, SK, SK2, "#5a3b26", "#2a1b12") + hat)


# 5 · COZY: Beanie (Lila), oranger Puffer-Weste über Longsleeve, Cargo beige
def d5(x, y):
    SK, SK2 = "#f2c7a8", "#d6a585"
    vest = (torso(x, y, "#e8e4f2", "#cfc9de", 560)
            + f'<path d="M {x-135} {y+255} Q {x-158} {y+400} {x-128} {y+560} L {x-8} {y+560} L {x-8} {y+258} Z" fill="#ff8a3d"/>'
            f'<path d="M {x+135} {y+255} Q {x+158} {y+400} {x+128} {y+560} L {x+8} {y+560} L {x+8} {y+258} Z" fill="#e8762f"/>'
            + "".join(f'<path d="M {x-140} {y+320+k*60} Q {x-70} {y+335+k*60} {x-8} {y+320+k*60} M {x+8} {y+320+k*60} Q {x+70} {y+335+k*60} {x+140} {y+320+k*60}" stroke="#c9601f" stroke-width="5" fill="none"/>' for k in range(4)))
    beanie = (f'<path d="M {x-82} {y+110} Q {x-90} {y+10} {x} {y+4} Q {x+90} {y+10} {x+82} {y+110} Z" fill="#7a5af5"/>'
              f'<rect x="{x-88}" y="{y+86}" width="176" height="34" rx="14" fill="#6446d8"/>'
              + "".join(f'<path d="M {x-70+k*22} {y+90} L {x-70+k*22} {y+118}" stroke="#5638c0" stroke-width="5"/>' for k in range(7))
              + f'<circle cx="{x}" cy="{y-4}" r="24" fill="#e8e4f2"/>'
              f'<path d="M {x-80} {y+118} Q {x-90} {y+170} {x-76} {y+190} L {x-66} {y+130} Z" fill="#c98a3a"/><path d="M {x+80} {y+118} Q {x+90} {y+170} {x+76} {y+190} L {x+66} {y+130} Z" fill="#c98a3a"/>')
    return (legs(x, y, "#c9b48a", "#b8a37a", "#6b4a32", "#2a1d14") + arms(x, y, "#e8e4f2", "#cfc9de", SK, SK2, cuff="#cfc9de") + vest
            + face(x, y, SK, SK2, "#3b6cff", "#c98a3a", lashes=True) + beanie)


# 6 · ATHLET: kurze Haare (Fade), Trikot (Blau/Weiß) mit Nummer, Shorts, Stutzen
def d6(x, y):
    SK, SK2 = "#c68a5e", "#a86f47"
    shirt = (torso(x, y, "#3b6cff", "#2f57d4", 540) + f'<rect x="{x-30}" y="{y+262}" width="60" height="278" fill="#fff" opacity=".9"/>'
             f'<text x="{x+70}" y="{y+420}" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="70" fill="#fff">10</text>'
             f'<path d="M {x-45} {y+255} L {x} {y+300} L {x+45} {y+255}" stroke="#fff" stroke-width="12" fill="none"/>')
    hair = (f'<path d="M {x-76} {y+120} Q {x-82} {y+30} {x} {y+26} Q {x+82} {y+30} {x+76} {y+120} Q {x+60} {y+60} {x} {y+58} Q {x-60} {y+60} {x-76} {y+120} Z" fill="#1a1210"/>'
            f'<path d="M {x-76} {y+120} L {x-74} {y+150} M {x+76} {y+120} L {x+74} {y+150}" stroke="#3a2a20" stroke-width="10" opacity=".6"/>')
    return (legs(x, y, "#f2f3f5", "#dcdfe6", "#e0a83a", "#1e1a2e", shorts=True, sk=SK) + arms(x, y, "#3b6cff", "#2f57d4", SK, SK2) + shirt
            + face(x, y, SK, SK2, "#3a2a1a", "#1a1210", mood="w") + hair)


LIME = "#c8f031"
PANELS = [("1 · STREET-KID", "Afro · Varsity-Jacke · Cap", d1), ("2 · SPORTY GIRL", "Zopf · Trainingsjacke Türkis", d2),
          ("3 · TECH-NERD", "Brille · Kopfhörer · Rucksack", d3), ("4 · SKATER", "Bucket Hat · Karohemd · Baggy", d4),
          ("5 · COZY", "Beanie · Puffer-Weste Orange", d5), ("6 · ATHLET", "Trikot Nr. 10 · Shorts", d6)]
out = ""
for k, (t, sub, fn) in enumerate(PANELS):
    px, py = (k % 3) * 720, (k // 3) * 1080
    out += (f'<g transform="translate({px},{py})"><rect width="720" height="1080" fill="url(#bgp)"/>'
            f'<ellipse cx="360" cy="878" rx="110" ry="16" fill="#000" opacity=".35"/>'
            f'<g transform="translate(360,150) scale(.78) translate(-540,0)">{fn(540, 40)}</g>'
            f'<rect x="30" y="30" width="{len(t)*24+60}" height="62" rx="31" fill="{LIME}"/><text x="60" y="74" font-family="Poppins" font-weight="800" font-size="32" fill="#0b0d22">{t}</text>'
            f'<text x="360" y="1040" text-anchor="middle" font-family="Poppins" font-weight="600" font-size="28" fill="#cfd3ff">{sub}</text></g>')
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="2160" height="2160" viewBox="0 0 2160 2160"><defs>'
       f'<radialGradient id="bgp" cx=".5" cy=".4" r=".8"><stop offset="0" stop-color="#22306a"/><stop offset="1" stop-color="#0b1226"/></radialGradient></defs>'
       f'{out}<rect x="718" y="0" width="4" height="2160" fill="#000"/><rect x="1438" y="0" width="4" height="2160" fill="#000"/><rect x="0" y="1078" width="2160" height="4" fill="#000"/></svg>')
open(os.path.join(os.path.dirname(__file__), "neue_designs.svg"), "w", encoding="utf-8").write(svg)
print("ok")
