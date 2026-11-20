"""Feste Hauptfigur „C · Anime mit Senf-Hoodie“ (gewählt am 20.11.).

Drop-in-Ersatz für figure() in den build.py-Dateien: gleiche Signatur und gleiche IDs
({fid}, {fid}-body, {fid}-legL, {fid}-legR, {fid}-eyes-n/-w/-f/-s), Füße bei y=0, Höhe ≈ 385 px bei s=1.
Benutzung in build.py:
    import sys; sys.path.insert(0, "../../branding/figur"); from figur_c import make_figure
    FIGS = []; figure = make_figure(FIGS)
"""
SK = "#e8b08a"; SK2 = "#c98a66"; HAIR = "#1e1a2e"; IRIS = "#3b6cff"; LIP = "#a85a4a"
M = "#e0a83a"; M2 = "#b8862a"; PANTS = "#23252e"; PANTS2 = "#1b1d25"; SHOE = "#f2f3f5"; SHOE2 = "#e3e5ea"; SOLE = "#1e1a2e"
DEFS = (f'<radialGradient id="figc-face" cx=".4" cy=".4" r=".7"><stop offset="0" stop-color="#f2c4a0"/><stop offset=".75" stop-color="{SK}"/>'
        f'<stop offset="1" stop-color="{SK2}"/></radialGradient>')
K = 0.43            # Skalierung: Zeichnung ist ~900 px hoch → ~385 px wie die alte Figur
Y0 = -888           # Kopf-Oberkante in Zeichnungs-Koordinaten, Füße bei ~0


def _eyes(fid, mode, show):
    x, y = 0, Y0
    def g(name, body):
        return f'<g id="{fid}-eyes-{name}" opacity="{1 if name == show else 0}">{body}</g>'
    sx_ = (-1, 1)
    n = "".join(f'<path d="M {x+s*15} {y+148} Q {x+s*38} {y+135} {x+s*58} {y+150} L {x+s*55} {y+170} Q {x+s*37} {y+182} {x+s*18} {y+168} Z" fill="#fff"/>'
                f'<ellipse cx="{x+s*36}" cy="{y+160}" rx="12" ry="14" fill="{IRIS}"/><circle cx="{x+s*36}" cy="{y+161}" r="5" fill="#0b0d22"/><circle cx="{x+s*40}" cy="{y+155}" r="3" fill="#fff"/>'
                f'<path d="M {x+s*12} {y+140} L {x+s*62} {y+142}" stroke="{HAIR}" stroke-width="6" stroke-linecap="round"/>' for s in sx_) \
        + f'<path d="M {x-14} {y+212} Q {x} {y+218} {x+14} {y+212}" stroke="{LIP}" stroke-width="5" fill="none" stroke-linecap="round"/>'
    w = "".join(f'<ellipse cx="{x+s*37}" cy="{y+158}" rx="22" ry="20" fill="#fff"/>'
                f'<circle cx="{x+s*37}" cy="{y+160}" r="9" fill="{IRIS}"/><circle cx="{x+s*37}" cy="{y+160}" r="4" fill="#0b0d22"/><circle cx="{x+s*40}" cy="{y+156}" r="2.5" fill="#fff"/>'
                f'<path d="M {x+s*14} {y+128} Q {x+s*38} {y+116} {x+s*62} {y+126}" stroke="{HAIR}" stroke-width="6" fill="none" stroke-linecap="round"/>' for s in sx_) \
        + f'<ellipse cx="{x}" cy="{y+214}" rx="11" ry="14" fill="#5a2a24"/><ellipse cx="{x}" cy="{y+221}" rx="6" ry="4" fill="#c46a6a"/>'
    f = "".join(f'<path d="M {x+s*16} {y+154} Q {x+s*38} {y+148} {x+s*58} {y+156} L {x+s*55} {y+166} Q {x+s*37} {y+172} {x+s*18} {y+164} Z" fill="#fff"/>'
                f'<ellipse cx="{x+s*36}" cy="{y+160}" rx="9" ry="7" fill="{IRIS}"/><circle cx="{x+s*36}" cy="{y+160}" r="4" fill="#0b0d22"/>'
                f'<path d="M {x+s*14} {y+138} L {x+s*62} {y+148}" stroke="{HAIR}" stroke-width="7" stroke-linecap="round"/>' for s in sx_) \
        + f'<path d="M {x-14} {y+214} L {x+14} {y+214}" stroke="{LIP}" stroke-width="5" stroke-linecap="round"/>'
    sl = "".join(f'<path d="M {x+s*16} {y+160} Q {x+s*37} {y+170} {x+s*58} {y+160}" stroke="{HAIR}" stroke-width="5" fill="none" stroke-linecap="round"/>'
                 f'<path d="M {x+s*14} {y+142} L {x+s*62} {y+142}" stroke="{HAIR}" stroke-width="6" stroke-linecap="round"/>' for s in sx_) \
        + f'<path d="M {x-8} {y+212} Q {x} {y+216} {x+8} {y+212}" stroke="{LIP}" stroke-width="5" fill="none" stroke-linecap="round"/>'
    return g("n", n) + g("w", w) + g("f", f) + g("s", sl)


def _head(fid, eyes):
    x, y = 0, Y0
    return (f'<rect x="{x-24}" y="{y+215}" width="48" height="55" rx="14" fill="{SK2}"/>'
            f'<path d="M {x-70} {y+90} Q {x-75} {y+215} {x} {y+235} Q {x+75} {y+215} {x+70} {y+90} Q {x} {y+20} {x-70} {y+90} Z" fill="url(#figc-face)"/>'
            f'<ellipse cx="{x-72}" cy="{y+150}" rx="11" ry="18" fill="{SK2}"/><ellipse cx="{x+72}" cy="{y+150}" rx="11" ry="18" fill="{SK2}"/>'
            f'<path d="M {x-95} {y+130} L {x-110} {y+40} L {x-60} {y+70} L {x-50} {y-10} L {x-5} {y+45} L {x+30} {y-20} L {x+45} {y+50} L {x+100} {y+10} L {x+85} {y+90} L {x+115} {y+120} L {x+70} {y+115} '
            f'L {x+40} {y+80} L {x+20} {y+120} L {x-5} {y+85} L {x-30} {y+125} L {x-50} {y+90} L {x-75} {y+140} Z" fill="{HAIR}"/>'
            f'<path d="M {x} {y+180} L {x+6} {y+195}" stroke="{SK2}" stroke-width="4" stroke-linecap="round"/>'
            f'<circle cx="{x-45}" cy="{y+195}" r="11" fill="#e98f7a" opacity=".3"/><circle cx="{x+45}" cy="{y+195}" r="11" fill="#e98f7a" opacity=".3"/>'
            + _eyes(fid, None, eyes))


def _back_head():
    x, y = 0, Y0
    return (f'<rect x="{x-24}" y="{y+215}" width="48" height="55" rx="14" fill="{SK2}"/>'
            f'<path d="M {x-75} {y+150} Q {x-80} {y+30} {x} {y+20} Q {x+80} {y+30} {x+75} {y+150} Q {x+60} {y+235} {x} {y+238} Q {x-60} {y+235} {x-75} {y+150} Z" fill="{HAIR}"/>'
            f'<path d="M {x-95} {y+130} L {x-110} {y+40} L {x-50} {y-10} L {x+30} {y-20} L {x+100} {y+10} L {x+115} {y+120} Z" fill="{HAIR}"/>')


def _legs(fid):
    x, y = 0, Y0
    L = (f'<g id="{fid}-legL"><path d="M {x-62} {y+500} L {x-72} {y+870} L {x-18} {y+870} L {x-6} {y+540} Z" fill="{PANTS}"/>'
         f'<rect x="{x-82}" y="{y+660}" width="40" height="60" rx="8" fill="{PANTS2}"/>'
         f'<path d="M {x-100} {y+868} Q {x-100} {y+840} {x-60} {y+842} L {x-12} {y+848} L {x-10} {y+885} L {x-102} {y+885} Z" fill="{SHOE}"/>'
         f'<rect x="{x-104}" y="{y+880}" width="96" height="14" rx="6" fill="{SOLE}"/></g>')
    R = (f'<g id="{fid}-legR"><path d="M {x+62} {y+500} L {x+72} {y+870} L {x+18} {y+870} L {x+6} {y+540} Z" fill="{PANTS2}"/>'
         f'<rect x="{x+44}" y="{y+660}" width="40" height="60" rx="8" fill="{PANTS}"/>'
         f'<path d="M {x+100} {y+868} Q {x+100} {y+840} {x+60} {y+842} L {x+12} {y+848} L {x+10} {y+885} L {x+102} {y+885} Z" fill="{SHOE2}"/>'
         f'<rect x="{x+8}" y="{y+880}" width="96" height="14" rx="6" fill="{SOLE}"/></g>')
    return L + R


def _torso(back=False):
    x, y = 0, Y0
    return (f'<path d="M {x-120} {y+265} Q {x-190} {y+380} {x-175} {y+510} L {x-130} {y+510} Q {x-140} {y+390} {x-100} {y+300} Z" fill="{M}"/>'
            f'<path d="M {x+120} {y+265} Q {x+190} {y+380} {x+175} {y+510} L {x+130} {y+510} Q {x+140} {y+390} {x+100} {y+300} Z" fill="{M2}"/>'
            f'<rect x="{x-178}" y="{y+490}" width="50" height="26" rx="10" fill="{M2}"/><rect x="{x+128}" y="{y+490}" width="50" height="26" rx="10" fill="{M2}"/>'
            f'<ellipse cx="{x-152}" cy="{y+535}" rx="22" ry="26" fill="{SK}"/><ellipse cx="{x+152}" cy="{y+535}" rx="22" ry="26" fill="{SK2}"/>'
            f'<path d="M {x-135} {y+255} Q {x-160} {y+400} {x-130} {y+560} L {x+130} {y+560} Q {x+160} {y+400} {x+135} {y+255} Q {x} {y+215} {x-135} {y+255} Z" fill="{M}"/>'
            f'<path d="M {x+60} {y+260} Q {x+150} {y+400} {x+130} {y+560} L {x+90} {y+560} Q {x+110} {y+400} {x+40} {y+265} Z" fill="{M2}" opacity=".6"/>'
            f'<rect x="{x-128}" y="{y+520}" width="256" height="45" rx="16" fill="{M2}"/>'
            + ("" if back else f'<path d="M {x-75} {y+420} L {x+75} {y+420} L {x+65} {y+495} L {x-65} {y+495} Z" fill="{M2}"/>'
               f'<path d="M {x-90} {y+250} Q {x} {y+300} {x+90} {y+250} Q {x+100} {y+215} {x+70} {y+205} Q {x} {y+240} {x-70} {y+205} Q {x-100} {y+215} {x-90} {y+250} Z" fill="{M2}"/>'
               f'<path d="M {x-22} {y+275} L {x-26} {y+370} M {x+22} {y+275} L {x+26} {y+370}" stroke="{HAIR}" stroke-width="6" stroke-linecap="round"/>')
            + (f'<path d="M {x-110} {y+250} Q {x} {y+220} {x+110} {y+250} Q {x+90} {y+330} {x} {y+340} Q {x-90} {y+330} {x-110} {y+250} Z" fill="{M2}"/>' if back else ""))


def make_figure(FIGS):
    def figure(fid, x, y, s=1.0, eyes="n", outfit="hoodie", back=False):
        FIGS.append(fid)
        head = _back_head() if back else _head(fid, eyes)
        return (f'<g id="{fid}"><g transform="translate({x},{y}) scale({s})">'
                f'<ellipse cx="0" cy="4" rx="78" ry="15" fill="#000" opacity=".4"/>'
                f'<g id="{fid}-body"><g transform="scale({K})">{_legs(fid)}{_torso(back)}{head}</g></g></g></g>')
    return figure
