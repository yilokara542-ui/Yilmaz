"""Neue Hauptfigur – 4 Stil-Varianten als Vorschau (2x2-Raster, 2160x2160)."""
import os
SK = "#e8b08a"; SK2 = "#c98a66"; HAIR = "#2e2118"; TEAL = "#2f6f73"; TEAL2 = "#245a5d"; JEANS = "#2c3a52"; LIME = "#c8f031"

def panel(px, py, title, sub, inner, bg1="#1d1d4f", bg2="#0b0d26"):
    gid = f"bg{px}{py}"
    return (f'<g transform="translate({px},{py})"><defs><radialGradient id="{gid}" cx=".5" cy=".38" r=".8"><stop offset="0" stop-color="{bg1}"/><stop offset="1" stop-color="{bg2}"/></radialGradient></defs>'
            f'<rect width="1080" height="1080" fill="url(#{gid})"/>{inner}'
            f'<rect x="40" y="40" width="{len(title)*30+70}" height="70" rx="35" fill="{LIME}"/><text x="75" y="88" font-family="Poppins" font-weight="800" font-size="40" fill="#0b0d22">{title}</text>'
            f'<text x="540" y="1040" text-anchor="middle" font-family="Poppins" font-weight="600" font-size="32" fill="#cfd3ff">{sub}</text></g>')

def shadow(x, y, w=170):
    return f'<ellipse cx="{x}" cy="{y}" rx="{w}" ry="26" fill="#000" opacity=".35"/>'

# ---------- 1: Kapuzen-Held (halb-realistisch, schattiert) ----------
def v1(x, y):
    return (shadow(x, y + 900) +
        # Beine + Schuhe
        f'<path d="M {x-70} {y+520} L {x-80} {y+870} L {x-20} {y+870} L {x-5} {y+560} Z" fill="{JEANS}"/>'
        f'<path d="M {x+70} {y+520} L {x+80} {y+870} L {x+20} {y+870} L {x+5} {y+560} Z" fill="#26324a"/>'
        f'<path d="M {x-110} {y+870} Q {x-110} {y+840} {x-60} {y+845} L {x-10} {y+850} L {x-8} {y+895} L {x-110} {y+895} Z" fill="#f2f3f5"/>'
        f'<path d="M {x+110} {y+870} Q {x+110} {y+840} {x+60} {y+845} L {x+10} {y+850} L {x+8} {y+895} L {x+110} {y+895} Z" fill="#e3e5ea"/>'
        # Hoodie
        f'<path d="M {x-150} {y+260} Q {x-170} {y+400} {x-130} {y+560} L {x+130} {y+560} Q {x+170} {y+400} {x+150} {y+260} Q {x} {y+210} {x-150} {y+260} Z" fill="url(#hood1)"/>'
        f'<rect x="{x-135}" y="{y+520}" width="270" height="45" rx="18" fill="{TEAL2}"/>'
        f'<path d="M {x-80} {y+420} L {x+80} {y+420} L {x+70} {y+500} L {x-70} {y+500} Z" fill="{TEAL2}"/>'
        f'<path d="M {x-150} {y+270} Q {x-215} {y+380} {x-200} {y+520} L {x-150} {y+520} Q {x-160} {y+400} {x-120} {y+320} Z" fill="{TEAL}"/>'
        f'<path d="M {x+150} {y+270} Q {x+215} {y+380} {x+200} {y+520} L {x+150} {y+520} Q {x+160} {y+400} {x+120} {y+320} Z" fill="{TEAL2}"/>'
        f'<ellipse cx="{x-178}" cy="{y+545}" rx="28" ry="32" fill="{SK}"/><ellipse cx="{x+178}" cy="{y+545}" rx="28" ry="32" fill="{SK2}"/>'
        f'<path d="M {x-25} {y+280} L {x-30} {y+380} M {x+25} {y+280} L {x+30} {y+380}" stroke="#e6e9ee" stroke-width="7" stroke-linecap="round"/>'
        # Kapuze hinter dem Kopf
        f'<path d="M {x-125} {y+275} Q {x-150} {y+40} {x} {y+20} Q {x+150} {y+40} {x+125} {y+275} Q {x} {y+240} {x-125} {y+275} Z" fill="{TEAL2}"/>'
        # Hals, Kopf
        f'<rect x="{x-28}" y="{y+215} " width="56" height="60" rx="16" fill="{SK2}"/>'
        f'<path d="M {x-85} {y+120} Q {x-90} {y+250} {x} {y+262} Q {x+90} {y+250} {x+85} {y+120} Q {x+80} {y+30} {x} {y+28} Q {x-80} {y+30} {x-85} {y+120} Z" fill="url(#face1)"/>'
        f'<ellipse cx="{x-86}" cy="{y+150}" rx="13" ry="22" fill="{SK2}"/><ellipse cx="{x+86}" cy="{y+150}" rx="13" ry="22" fill="{SK2}"/>'
        # Haare (Undercut + Strähne)
        f'<path d="M {x-88} {y+130} Q {x-100} {y+30} {x-10} {y+18} Q {x+80} {y+10} {x+92} {y+110} Q {x+60} {y+60} {x+10} {y+78} Q {x-40} {y+50} {x-88} {y+130} Z" fill="{HAIR}"/>'
        f'<path d="M {x-10} {y+30} Q {x+30} {y+70} {x+70} {y+80}" stroke="#4a3528" stroke-width="6" fill="none"/>'
        # Gesicht
        f'<path d="M {x-55} {y+128} Q {x-38} {y+120} {x-20} {y+128}" stroke="{HAIR}" stroke-width="8" stroke-linecap="round" fill="none"/>'
        f'<path d="M {x+20} {y+128} Q {x+38} {y+120} {x+55} {y+128}" stroke="{HAIR}" stroke-width="8" stroke-linecap="round" fill="none"/>'
        f'<ellipse cx="{x-37}" cy="{y+155}" rx="15" ry="11" fill="#fff"/><ellipse cx="{x+37}" cy="{y+155}" rx="15" ry="11" fill="#fff"/>'
        f'<circle cx="{x-35}" cy="{y+156}" r="8" fill="#5a3b26"/><circle cx="{x+39}" cy="{y+156}" r="8" fill="#5a3b26"/>'
        f'<circle cx="{x-35}" cy="{y+156}" r="3.5" fill="#111"/><circle cx="{x+39}" cy="{y+156}" r="3.5" fill="#111"/><circle cx="{x-32}" cy="{y+152}" r="2.5" fill="#fff"/><circle cx="{x+42}" cy="{y+152}" r="2.5" fill="#fff"/>'
        f'<path d="M {x-52} {y+146} Q {x-37} {y+140} {x-22} {y+146} M {x+22} {y+146} Q {x+37} {y+140} {x+52} {y+146}" stroke="#7a5a48" stroke-width="3" fill="none"/>'
        f'<path d="M {x+2} {y+165} Q {x+12} {y+195} {x-6} {y+200}" stroke="{SK2}" stroke-width="5" fill="none" stroke-linecap="round"/>'
        f'<path d="M {x-22} {y+222} Q {x} {y+232} {x+22} {y+222}" stroke="#a85a4a" stroke-width="6" fill="none" stroke-linecap="round"/>'
        f'<circle cx="{x-55}" cy="{y+200}" r="14" fill="#e98f7a" opacity=".3"/><circle cx="{x+55}" cy="{y+200}" r="14" fill="#e98f7a" opacity=".3"/>')

# ---------- 2: Chibi (großer Kopf, große glänzende Augen) ----------
def v2(x, y):
    return (shadow(x, y + 900, 150) +
        f'<rect x="{x-60}" y="{y+760}" width="50" height="110" rx="20" fill="{JEANS}"/><rect x="{x+10}" y="{y+760}" width="50" height="110" rx="20" fill="#26324a"/>'
        f'<ellipse cx="{x-40}" cy="{y+875}" rx="50" ry="26" fill="#f2f3f5"/><ellipse cx="{x+40}" cy="{y+875}" rx="50" ry="26" fill="#e3e5ea"/>'
        f'<path d="M {x-130} {y+580} Q {x-140} {y+700} {x-110} {y+790} L {x+110} {y+790} Q {x+140} {y+700} {x+130} {y+580} Q {x} {y+540} {x-130} {y+580} Z" fill="{TEAL}"/>'
        f'<rect x="{x-60}" y="{y+690} " width="120" height="60" rx="20" fill="{TEAL2}"/>'
        f'<ellipse cx="{x-150}" cy="{y+700}" rx="42" ry="85" fill="{TEAL}" transform="rotate(15 {x-150} {y+700})"/><ellipse cx="{x+150}" cy="{y+700}" rx="42" ry="85" fill="{TEAL2}" transform="rotate(-15 {x+150} {y+700})"/>'
        f'<circle cx="{x-165}" cy="{y+780}" r="30" fill="{SK}"/><circle cx="{x+165}" cy="{y+780}" r="30" fill="{SK2}"/>'
        # Riesiger Kopf
        f'<ellipse cx="{x}" cy="{y+330}" rx="250" ry="235" fill="url(#face2)"/>'
        f'<ellipse cx="{x-245}" cy="{y+350}" rx="30" ry="45" fill="{SK2}"/><ellipse cx="{x+245}" cy="{y+350}" rx="30" ry="45" fill="{SK2}"/>'
        f'<path d="M {x-260} {y+330} Q {x-280} {y+70} {x} {y+60} Q {x+280} {y+70} {x+260} {y+330} Q {x+220} {y+190} {x+120} {y+170} Q {x+60} {y+230} {x-20} {y+170} Q {x-90} {y+220} {x-170} {y+180} Q {x-240} {y+230} {x-260} {y+330} Z" fill="{HAIR}"/>'
        f'<path d="M {x+30} {y+62} Q {x+70} {y+10} {x+50} {y-20}" stroke="{HAIR}" stroke-width="22" fill="none" stroke-linecap="round"/>'
        + "".join(f'<ellipse cx="{x+sx*95}" cy="{y+350}" rx="62" ry="78" fill="#2a1a12"/><ellipse cx="{x+sx*95}" cy="{y+365}" rx="50" ry="60" fill="#6b4226"/>'
                  f'<ellipse cx="{x+sx*95}" cy="{y+372}" rx="28" ry="34" fill="#140c08"/><circle cx="{x+sx*95+18}" cy="{y+330}" r="20" fill="#fff"/><circle cx="{x+sx*95-20}" cy="{y+395}" r="9" fill="#fff"/>' for sx in (-1, 1))
        + f'<ellipse cx="{x-170}" cy="{y+440}" rx="40" ry="22" fill="#ff8a8a" opacity=".45"/><ellipse cx="{x+170}" cy="{y+440}" rx="40" ry="22" fill="#ff8a8a" opacity=".45"/>'
        f'<path d="M {x-30} {y+460} Q {x} {y+490} {x+30} {y+460}" stroke="#7a3a30" stroke-width="9" fill="#c44" stroke-linecap="round"/>'
        f'<path d="M {x-150} {y+260} Q {x-95} {y+240} {x-45} {y+262} M {x+45} {y+262} Q {x+95} {y+240} {x+150} {y+260}" stroke="{HAIR}" stroke-width="10" fill="none" stroke-linecap="round"/>')

# ---------- 3: Anime-Stil (Stachelhaar, Jacke, Schal) ----------
def v3(x, y):
    return (shadow(x, y + 900, 140) +
        f'<path d="M {x-60} {y+500} L {x-70} {y+870} L {x-20} {y+870} L {x-8} {y+540} Z" fill="#1f2433"/><path d="M {x+60} {y+500} L {x+70} {y+870} L {x+20} {y+870} L {x+8} {y+540} Z" fill="#1a1e2c"/>'
        f'<path d="M {x-90} {y+870} L {x-10} {y+870} L {x-10} {y+895} L {x-100} {y+895} Z" fill="#f2f3f5"/><path d="M {x+90} {y+870} L {x+10} {y+870} L {x+10} {y+895} L {x+100} {y+895} Z" fill="#e3e5ea"/>'
        f'<rect x="{x-75}" y="{y+270}" width="150" height="250" rx="20" fill="#e9ecf2"/>'
        f'<path d="M {x-120} {y+260} L {x-75} {y+260} L {x-60} {y+540} L {x-125} {y+540} Q {x-140} {y+400} {x-120} {y+260} Z" fill="{TEAL}"/>'
        f'<path d="M {x+120} {y+260} L {x+75} {y+260} L {x+60} {y+540} L {x+125} {y+540} Q {x+140} {y+400} {x+120} {y+260} Z" fill="{TEAL2}"/>'
        f'<path d="M {x-120} {y+265} Q {x-185} {y+380} {x-170} {y+500} L {x-130} {y+500} Q {x-140} {y+390} {x-100} {y+300} Z" fill="{TEAL}"/>'
        f'<path d="M {x+120} {y+265} Q {x+185} {y+380} {x+170} {y+500} L {x+130} {y+500} Q {x+140} {y+390} {x+100} {y+300} Z" fill="{TEAL2}"/>'
        f'<ellipse cx="{x-152}" cy="{y+520}" rx="22" ry="26" fill="{SK}"/><ellipse cx="{x+152}" cy="{y+520}" rx="22" ry="26" fill="{SK2}"/>'
        f'<path d="M {x-80} {y+240} Q {x} {y+290} {x+80} {y+240} L {x+75} {y+290} Q {x} {y+330} {x-75} {y+290} Z" fill="#c74545"/><path d="M {x+40} {y+290} L {x+60} {y+400} L {x+20} {y+395} Z" fill="#a93a3a"/>'
        f'<path d="M {x-70} {y+90} Q {x-75} {y+215} {x} {y+235} Q {x+75} {y+215} {x+70} {y+90} Q {x} {y+20} {x-70} {y+90} Z" fill="url(#face1)"/>'
        f'<path d="M {x-95} {y+130} L {x-110} {y+40} L {x-60} {y+70} L {x-50} {y-10} L {x-5} {y+45} L {x+30} {y-20} L {x+45} {y+50} L {x+100} {y+10} L {x+85} {y+90} L {x+115} {y+120} L {x+70} {y+115} '
        f'L {x+40} {y+80} L {x+20} {y+120} L {x-5} {y+85} L {x-30} {y+125} L {x-50} {y+90} L {x-75} {y+140} Z" fill="#1e1a2e"/>'
        + "".join(f'<path d="M {x+sx*15} {y+148} Q {x+sx*38} {y+135} {x+sx*58} {y+150} L {x+sx*55} {y+170} Q {x+sx*37} {y+182} {x+sx*18} {y+168} Z" fill="#fff"/>'
                  f'<ellipse cx="{x+sx*36}" cy="{y+160}" rx="12" ry="14" fill="#3b6cff"/><circle cx="{x+sx*36}" cy="{y+161}" r="5" fill="#0b0d22"/><circle cx="{x+sx*40}" cy="{y+155}" r="3" fill="#fff"/>'
                  f'<path d="M {x+sx*12} {y+140} L {x+sx*62} {y+142}" stroke="#1e1a2e" stroke-width="6" stroke-linecap="round"/>' for sx in (-1, 1))
        + f'<path d="M {x} {y+180} L {x+6} {y+195}" stroke="{SK2}" stroke-width="4" stroke-linecap="round"/><path d="M {x-14} {y+212} L {x+14} {y+212}" stroke="#a85a4a" stroke-width="5" stroke-linecap="round"/>')

# ---------- 4: Mystery (Silhouette, nur Handylicht im Gesicht) ----------
def v4(x, y):
    D = "#0a0b1e"
    return (shadow(x, y + 900) +
        f'<path d="M {x-70} {y+520} L {x-80} {y+880} L {x-15} {y+880} L {x-5} {y+560} Z" fill="{D}"/><path d="M {x+70} {y+520} L {x+80} {y+880} L {x+15} {y+880} L {x+5} {y+560} Z" fill="{D}"/>'
        f'<path d="M {x-150} {y+260} Q {x-170} {y+400} {x-130} {y+560} L {x+130} {y+560} Q {x+170} {y+400} {x+150} {y+260} Q {x} {y+210} {x-150} {y+260} Z" fill="{D}"/>'
        f'<path d="M {x-125} {y+275} Q {x-150} {y+30} {x} {y+15} Q {x+150} {y+30} {x+125} {y+275} Q {x} {y+240} {x-125} {y+275} Z" fill="{D}"/>'
        f'<path d="M {x-125} {y+275} Q {x-150} {y+30} {x} {y+15} Q {x+150} {y+30} {x+125} {y+275}" stroke="{LIME}" stroke-width="5" fill="none" opacity=".7"/>'
        f'<path d="M {x+150} {y+260} Q {x+170} {y+400} {x+130} {y+560}" stroke="{LIME}" stroke-width="5" fill="none" opacity=".6"/>'
        f'<path d="M {x-80} {y+110} Q {x-85} {y+240} {x} {y+252} Q {x+85} {y+240} {x+80} {y+110} Q {x} {y+40} {x-80} {y+110} Z" fill="#141530"/>'
        f'<path d="M {x-80} {y+170} Q {x-85} {y+240} {x} {y+252} Q {x+85} {y+240} {x+80} {y+170} Q {x} {y+200} {x-80} {y+170} Z" fill="url(#phoneglow)"/>'
        f'<ellipse cx="{x-34}" cy="{y+160}" rx="14" ry="9" fill="#e8f0ff"/><ellipse cx="{x+34}" cy="{y+160}" rx="14" ry="9" fill="#e8f0ff"/>'
        f'<circle cx="{x-34}" cy="{y+161}" r="5" fill="#0b0d22"/><circle cx="{x+34}" cy="{y+161}" r="5" fill="#0b0d22"/>'
        f'<rect x="{x-45}" y="{y+330}" width="90" height="150" rx="16" fill="#0b0d22" stroke="#3a3f8a" stroke-width="4"/><rect x="{x-38}" y="{y+338}" width="76" height="134" rx="10" fill="#bfe4ff"/>'
        f'<polygon points="{x-38},{y+338} {x+38},{y+338} {x+90},{y+150} {x-90},{y+150}" fill="#bfe4ff" opacity=".12"/>'
        f'<ellipse cx="{x-60}" cy="{y+430}" rx="30" ry="34" fill="#2a2b4a"/><ellipse cx="{x+60}" cy="{y+430}" rx="30" ry="34" fill="#2a2b4a"/>')

DEFS = f'''<defs>
<linearGradient id="hood1" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3a8286"/><stop offset=".6" stop-color="{TEAL}"/><stop offset="1" stop-color="{TEAL2}"/></linearGradient>
<radialGradient id="face1" cx=".4" cy=".4" r=".7"><stop offset="0" stop-color="#f2c4a0"/><stop offset=".75" stop-color="{SK}"/><stop offset="1" stop-color="{SK2}"/></radialGradient>
<radialGradient id="face2" cx=".42" cy=".4" r=".7"><stop offset="0" stop-color="#f6d0b0"/><stop offset=".8" stop-color="{SK}"/><stop offset="1" stop-color="{SK2}"/></radialGradient>
<linearGradient id="phoneglow" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#bfe4ff" stop-opacity=".55"/><stop offset="1" stop-color="#bfe4ff" stop-opacity="0"/></linearGradient>
</defs>'''
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="2160" height="2160" viewBox="0 0 2160 2160">{DEFS}'
       + panel(0, 0, "A · KAPUZEN-HELD", "halb-realistisch, Schatten, Kapuze", f'<g transform="translate(70,110) scale(.87)">{v1(540, 40)}</g>')
       + panel(1080, 0, "B · CHIBI", "großer Kopf, große Augen – sehr niedlich", f'<g transform="translate(70,95) scale(.87)">{v2(540, 40)}</g>', "#2a2360", "#120f30")
       + panel(0, 1080, "C · ANIME", "Stachelhaar, Jacke, roter Schal", f'<g transform="translate(70,95) scale(.87)">{v3(540, 60)}</g>', "#1d2a4f", "#0b1226")
       + panel(1080, 1080, "D · MYSTERY", "Silhouette, nur Handylicht – passt zu Horror", f'<g transform="translate(70,110) scale(.87)">{v4(540, 40)}</g>', "#14152e", "#05061a")
       + '<rect x="1078" y="0" width="4" height="2160" fill="#000"/><rect x="0" y="1078" width="2160" height="4" fill="#000"/></svg>')
open("figur_varianten.svg", "w", encoding="utf-8").write(svg)
print("ok")
