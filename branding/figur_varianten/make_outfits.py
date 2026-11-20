"""Figur C (Anime) mit 4 neuen Outfits/Farben – Vorschau 2x2 (2160x2160)."""
import importlib.util, os
spec = importlib.util.spec_from_file_location("v", os.path.join(os.path.dirname(__file__), "make_varianten.py"))
SK = "#e8b08a"; SK2 = "#c98a66"; LIME = "#c8f031"


def head(x, y):
    return (f'<path d="M {x-70} {y+90} Q {x-75} {y+215} {x} {y+235} Q {x+75} {y+215} {x+70} {y+90} Q {x} {y+20} {x-70} {y+90} Z" fill="url(#face1)"/>'
            f'<ellipse cx="{x-72}" cy="{y+150}" rx="11" ry="18" fill="{SK2}"/><ellipse cx="{x+72}" cy="{y+150}" rx="11" ry="18" fill="{SK2}"/>'
            f'<path d="M {x-95} {y+130} L {x-110} {y+40} L {x-60} {y+70} L {x-50} {y-10} L {x-5} {y+45} L {x+30} {y-20} L {x+45} {y+50} L {x+100} {y+10} L {x+85} {y+90} L {x+115} {y+120} L {x+70} {y+115} '
            f'L {x+40} {y+80} L {x+20} {y+120} L {x-5} {y+85} L {x-30} {y+125} L {x-50} {y+90} L {x-75} {y+140} Z" fill="#1e1a2e"/>'
            + "".join(f'<path d="M {x+sx*15} {y+148} Q {x+sx*38} {y+135} {x+sx*58} {y+150} L {x+sx*55} {y+170} Q {x+sx*37} {y+182} {x+sx*18} {y+168} Z" fill="#fff"/>'
                      f'<ellipse cx="{x+sx*36}" cy="{y+160}" rx="12" ry="14" fill="#3b6cff"/><circle cx="{x+sx*36}" cy="{y+161}" r="5" fill="#0b0d22"/><circle cx="{x+sx*40}" cy="{y+155}" r="3" fill="#fff"/>'
                      f'<path d="M {x+sx*12} {y+140} L {x+sx*62} {y+142}" stroke="#1e1a2e" stroke-width="6" stroke-linecap="round"/>' for sx in (-1, 1))
            + f'<path d="M {x} {y+180} L {x+6} {y+195}" stroke="{SK2}" stroke-width="4" stroke-linecap="round"/><path d="M {x-14} {y+212} Q {x} {y+218} {x+14} {y+212}" stroke="#a85a4a" stroke-width="5" fill="none" stroke-linecap="round"/>'
            f'<circle cx="{x-45}" cy="{y+195}" r="11" fill="#e98f7a" opacity=".3"/><circle cx="{x+45}" cy="{y+195}" r="11" fill="#e98f7a" opacity=".3"/>')


def legs(x, y, c1, c2, shoe="#f2f3f5", shoe2="#e3e5ea", sole="#1e1a2e", cargo=False):
    out = (f'<path d="M {x-62} {y+500} L {x-72} {y+870} L {x-18} {y+870} L {x-6} {y+540} Z" fill="{c1}"/><path d="M {x+62} {y+500} L {x+72} {y+870} L {x+18} {y+870} L {x+6} {y+540} Z" fill="{c2}"/>'
           f'<path d="M {x-100} {y+868} Q {x-100} {y+840} {x-60} {y+842} L {x-12} {y+848} L {x-10} {y+885} L {x-102} {y+885} Z" fill="{shoe}"/>'
           f'<path d="M {x+100} {y+868} Q {x+100} {y+840} {x+60} {y+842} L {x+12} {y+848} L {x+10} {y+885} L {x+102} {y+885} Z" fill="{shoe2}"/>'
           f'<rect x="{x-104}" y="{y+880}" width="96" height="14" rx="6" fill="{sole}"/><rect x="{x+8}" y="{y+880}" width="96" height="14" rx="6" fill="{sole}"/>')
    if cargo:
        out += f'<rect x="{x-82}" y="{y+660}" width="40" height="60" rx="8" fill="{c2}"/><rect x="{x+44}" y="{y+660}" width="40" height="60" rx="8" fill="{c1}"/>'
    return out


def arms(x, y, c1, c2, cuff=None):
    out = (f'<path d="M {x-120} {y+265} Q {x-190} {y+380} {x-175} {y+510} L {x-130} {y+510} Q {x-140} {y+390} {x-100} {y+300} Z" fill="{c1}"/>'
           f'<path d="M {x+120} {y+265} Q {x+190} {y+380} {x+175} {y+510} L {x+130} {y+510} Q {x+140} {y+390} {x+100} {y+300} Z" fill="{c2}"/>')
    if cuff:
        out += f'<rect x="{x-178}" y="{y+490}" width="50" height="26" rx="10" fill="{cuff}"/><rect x="{x+128}" y="{y+490}" width="50" height="26" rx="10" fill="{cuff}"/>'
    return out + f'<ellipse cx="{x-152}" cy="{y+535}" rx="22" ry="26" fill="{SK}"/><ellipse cx="{x+152}" cy="{y+535}" rx="22" ry="26" fill="{SK2}"/>'


def neck(x, y):
    return f'<rect x="{x-24}" y="{y+215}" width="48" height="55" rx="14" fill="{SK2}"/>'


# 1 Senf-Oversize-Hoodie + schwarze Cargo
def o1(x, y):
    M, M2 = "#e0a83a", "#b8862a"
    return (legs(x, y, "#23252e", "#1b1d25", cargo=True) + arms(x, y, M, M2, cuff=M2)
            + f'<path d="M {x-135} {y+255} Q {x-160} {y+400} {x-130} {y+560} L {x+130} {y+560} Q {x+160} {y+400} {x+135} {y+255} Q {x} {y+215} {x-135} {y+255} Z" fill="{M}"/>'
            + f'<path d="M {x+60} {y+260} Q {x+150} {y+400} {x+130} {y+560} L {x+90} {y+560} Q {x+110} {y+400} {x+40} {y+265} Z" fill="{M2}" opacity=".6"/>'
            + f'<rect x="{x-128}" y="{y+520}" width="256" height="45" rx="16" fill="{M2}"/><path d="M {x-75} {y+420} L {x+75} {y+420} L {x+65} {y+495} L {x-65} {y+495} Z" fill="{M2}"/>'
            + f'<path d="M {x-90} {y+250} Q {x} {y+300} {x+90} {y+250} Q {x+100} {y+215} {x+70} {y+205} Q {x} {y+240} {x-70} {y+205} Q {x-100} {y+215} {x-90} {y+250} Z" fill="{M2}"/>'
            + f'<path d="M {x-22} {y+275} L {x-26} {y+370} M {x+22} {y+275} L {x+26} {y+370}" stroke="#1e1a2e" stroke-width="6" stroke-linecap="round"/>'
            + neck(x, y) + head(x, y))


# 2 Schwarze Bomberjacke mit Neon-Bündchen + graues Shirt
def o2(x, y):
    B, B2 = "#22253a", "#181a2b"
    return (legs(x, y, "#2c3a52", "#26324a") + arms(x, y, B, B2, cuff=LIME)
            + f'<rect x="{x-80}" y="{y+260}" width="160" height="270" rx="16" fill="#8e95a8"/>'
            + f'<path d="M {x-130} {y+255} Q {x-150} {y+400} {x-128} {y+530} L {x-25} {y+530} L {x-40} {y+262} Z" fill="{B}"/>'
            + f'<path d="M {x+130} {y+255} Q {x+150} {y+400} {x+128} {y+530} L {x+25} {y+530} L {x+40} {y+262} Z" fill="{B2}"/>'
            + f'<rect x="{x-130}" y="{y+515}" width="105" height="30" rx="10" fill="{LIME}"/><rect x="{x+25}" y="{y+515}" width="105" height="30" rx="10" fill="{LIME}"/>'
            + f'<path d="M {x-75} {y+245} Q {x} {y+280} {x+75} {y+245}" stroke="{LIME}" stroke-width="16" fill="none" stroke-linecap="round"/>'
            + f'<rect x="{x-110}" y="{y+330}" width="40" height="8" rx="4" fill="{LIME}" opacity=".8"/>'
            + f'<path d="M {x-25} {y+262} L {x-25} {y+530} M {x+25} {y+262} L {x+25} {y+530}" stroke="#0f1020" stroke-width="4"/>'
            + neck(x, y) + head(x, y))


# 3 Lila Windbreaker mit weißem Keil + schwarze Jogger
def o3(x, y):
    P, P2 = "#6c4bd1", "#5538ad"
    return (legs(x, y, "#1e1f2b", "#181922", shoe="#f2f3f5", sole="#6c4bd1") + arms(x, y, P, P2, cuff=P2)
            + f'<path d="M {x-135} {y+255} Q {x-155} {y+400} {x-125} {y+545} L {x+125} {y+545} Q {x+155} {y+400} {x+135} {y+255} Q {x} {y+215} {x-135} {y+255} Z" fill="{P}"/>'
            + f'<path d="M {x-140} {y+330} L {x} {y+410} L {x+140} {y+330} L {x+142} {y+380} L {x} {y+460} L {x-142} {y+380} Z" fill="#f2f3f5"/>'
            + f'<rect x="{x-6}" y="{y+250}" width="12" height="160" fill="#c9c2ef"/><rect x="{x-125}" y="{y+520}" width="250" height="30" rx="12" fill="{P2}"/>'
            + f'<path d="M {x-80} {y+250} Q {x} {y+200} {x+80} {y+250} L {x+60} {y+270} Q {x} {y+240} {x-60} {y+270} Z" fill="{P2}"/>'
            + neck(x, y) + head(x, y))


# 4 Olivgrüner Parka mit Fellkapuze + beiger Schal
def o4(x, y):
    O, O2 = "#5f6b3a", "#4b552d"
    return (legs(x, y, "#23252e", "#1b1d25", shoe="#6b4a32", shoe2="#5a3d29", sole="#2a1d14")
            + arms(x, y, O, O2, cuff=O2)
            + f'<path d="M {x-140} {y+255} Q {x-165} {y+430} {x-140} {y+600} L {x+140} {y+600} Q {x+165} {y+430} {x+140} {y+255} Q {x} {y+215} {x-140} {y+255} Z" fill="{O}"/>'
            + f'<path d="M {x} {y+262} L {x} {y+600}" stroke="{O2}" stroke-width="6"/>'
            + "".join(f'<rect x="{x+sx*60-24}" y="{y+430}" width="48" height="56" rx="8" fill="{O2}"/>' for sx in (-1, 1))
            + f'<path d="M {x-125} {y+265} Q {x-150} {y+60} {x} {y+40} Q {x+150} {y+60} {x+125} {y+265}" stroke="#d9cbb0" stroke-width="30" fill="none" stroke-linecap="round" opacity=".95"/>'
            + f'<path d="M {x-82} {y+235} Q {x} {y+290} {x+82} {y+235} L {x+78} {y+285} Q {x} {y+325} {x-78} {y+285} Z" fill="#cdb48a"/><path d="M {x-50} {y+290} L {x-70} {y+400} L {x-28} {y+395} Z" fill="#b89c70"/>'
            + neck(x, y) + head(x, y))


DEFS = f'''<defs><radialGradient id="face1" cx=".4" cy=".4" r=".7"><stop offset="0" stop-color="#f2c4a0"/><stop offset=".75" stop-color="{SK}"/><stop offset="1" stop-color="{SK2}"/></radialGradient></defs>'''


def panel(px, py, title, sub, inner, bg1, bg2):
    gid = f"bg{px}{py}"
    return (f'<g transform="translate({px},{py})"><defs><radialGradient id="{gid}" cx=".5" cy=".38" r=".8"><stop offset="0" stop-color="{bg1}"/><stop offset="1" stop-color="{bg2}"/></radialGradient></defs>'
            f'<rect width="1080" height="1080" fill="url(#{gid})"/><ellipse cx="540" cy="932" rx="130" ry="18" fill="#000" opacity=".35"/>{inner}'
            f'<rect x="40" y="40" width="{len(title)*27+70}" height="70" rx="35" fill="{LIME}"/><text x="75" y="88" font-family="Poppins" font-weight="800" font-size="38" fill="#0b0d22">{title}</text>'
            f'<text x="540" y="1045" text-anchor="middle" font-family="Poppins" font-weight="600" font-size="32" fill="#cfd3ff">{sub}</text></g>')


g = lambda f: f'<g transform="translate(70,105) scale(.87)">{f(540, 60)}</g>'
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="2160" height="2160" viewBox="0 0 2160 2160">{DEFS}'
       + panel(0, 0, "1 · SENF-HOODIE", "Oversize-Hoodie Senfgelb · schwarze Cargo", g(o1), "#1d2a4f", "#0b1226")
       + panel(1080, 0, "2 · BOMBERJACKE", "Schwarz mit Neon-Bündchen · graues Shirt", g(o2), "#1d2a4f", "#0b1226")
       + panel(0, 1080, "3 · WINDBREAKER", "Lila mit weißem Keil · schwarze Jogger", g(o3), "#1d2a4f", "#0b1226")
       + panel(1080, 1080, "4 · PARKA", "Olivgrün mit Fellkapuze · beiger Schal", g(o4), "#1d2a4f", "#0b1226")
       + '<rect x="1078" y="0" width="4" height="2160" fill="#000"/><rect x="0" y="1078" width="2160" height="4" fill="#000"/></svg>')
open(os.path.join(os.path.dirname(__file__), "figur_c_outfits.svg"), "w", encoding="utf-8").write(svg)
print("ok")
