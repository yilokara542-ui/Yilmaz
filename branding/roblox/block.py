"""Block-Avatar-Bausteine (eigener Stil) für Format-C-Videos. Füße bei y=0, Höhe ≈ 6,7 U."""
DX, DY = 34, -24


def box(x, y, w, h, front, side, top, extra=""):
    return (f'<polygon points="{x+w},{y} {x+w+DX},{y+DY} {x+w+DX},{y+h+DY} {x+w},{y+h}" fill="{side}"/>'
            f'<polygon points="{x},{y} {x+DX},{y+DY} {x+w+DX},{y+DY} {x+w},{y}" fill="{top}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{front}"/>{extra}')


def shade(c, f):
    c = c.lstrip("#"); r, g, b = (int(c[i:i+2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(v * f))) for v in (r, g, b))


def face(cx, cy, mood, U):
    k = U / 70
    e = ""
    for s in (-1, 1):
        ex = cx + s * 30 * k
        if mood == "happy":
            e += f'<path d="M {ex-14*k} {cy-6*k} Q {ex} {cy-22*k} {ex+14*k} {cy-6*k}" stroke="#111" stroke-width="{7*k}" fill="none" stroke-linecap="round"/>'
        elif mood == "shock":
            e += f'<circle cx="{ex}" cy="{cy-10*k}" r="{15*k}" fill="#fff" stroke="#111" stroke-width="{4*k}"/><circle cx="{ex}" cy="{cy-8*k}" r="{6*k}" fill="#111"/>'
        elif mood == "sleep":
            e += f'<path d="M {ex-14*k} {cy-10*k} L {ex+14*k} {cy-10*k}" stroke="#111" stroke-width="{6*k}" stroke-linecap="round"/>'
        else:
            e += f'<ellipse cx="{ex}" cy="{cy-10*k}" rx="{12*k}" ry="{15*k}" fill="#111"/><circle cx="{ex+4*k}" cy="{cy-16*k}" r="{4.5*k}" fill="#fff"/>'
    m = {"happy": f'<path d="M {cx-26*k} {cy+18*k} Q {cx} {cy+44*k} {cx+26*k} {cy+18*k}" stroke="#111" stroke-width="{7*k}" fill="none" stroke-linecap="round"/>',
         "shock": f'<ellipse cx="{cx}" cy="{cy+28*k}" rx="{13*k}" ry="{17*k}" fill="#111"/>',
         "sleep": f'<path d="M {cx-10*k} {cy+24*k} L {cx+10*k} {cy+24*k}" stroke="#111" stroke-width="{6*k}" stroke-linecap="round"/>'}.get(
        mood, f'<path d="M {cx-20*k} {cy+22*k} Q {cx} {cy+34*k} {cx+20*k} {cy+22*k}" stroke="#111" stroke-width="{6*k}" fill="none" stroke-linecap="round"/>')
    return f'<g class="bf">{e}{m}</g>'


HAIRS = ("spike", "flat", "bun", "cap", "bald", "long", "chef")


def block(bid, x, y, s=1.0, shirt="#e0a83a", pants="#23252e", skin="#e8b08a", hair="#1e1a2e", hstyle="spike", mood="n",
          back=False, U=70, extra=""):
    """Block-Figur; (x,y) = Mitte unten zwischen den Füßen."""
    x0 = -U; y0 = -6.4 * U
    o = ""
    for i in range(2):
        lx = x0 + i * U
        o += box(lx, y0 + 4.3*U, U, 2*U, pants if i == 0 else shade(pants, 1.15), shade(pants, .7), shade(pants, 1.25))
        o += box(lx - 4, y0 + 6.05*U, U + 8, 0.35*U, "#f2f3f5", "#cfd3da", "#ffffff")
    S1, S2, S3 = shirt, shade(shirt, .78), shade(shirt, 1.12)
    o += box(x0 - U, y0 + 2.3*U, U, 2*U, S1, S2, S3, f'<rect x="{x0-U}" y="{y0+3.95*U}" width="{U}" height="{0.35*U}" fill="{skin}"/>')
    o += box(x0, y0 + 2.3*U, 2*U, 2*U, S1, S2, S3)
    o += box(x0 + 2*U, y0 + 2.3*U, U, 2*U, S1, S2, S3, f'<rect x="{x0+2*U}" y="{y0+3.95*U}" width="{U}" height="{0.35*U}" fill="{skin}"/>')
    o += (f'<rect x="{x0-3}" y="{y0+2.3*U}" width="6" height="{2*U}" fill="#000" opacity=".25"/>'
          f'<rect x="{x0+2*U-3}" y="{y0+2.3*U}" width="6" height="{2*U}" fill="#000" opacity=".25"/>')
    hx, hy, hw = x0 + 0.3*U, y0 + 0.95*U, 1.4*U
    o += box(hx, hy, hw, 1.35*U, skin, shade(skin, .82), shade(skin, 1.08))
    if not back:
        o += face(hx + hw/2, hy + 0.75*U, mood, U)
    H2 = shade(hair, .7)
    if hstyle == "spike":
        pts = " ".join(f"{hx + a*U:.0f},{hy + b*U:.0f}" for a, b in ((0, 0), (0.25, -0.45), (0.48, -0.2), (0.7, -0.62), (0.92, -0.25), (1.15, -0.5), (1.4, 0)))
        o += f'<polygon points="{hx-10},{hy+0.35*U} {pts} {hx+hw+10},{hy+0.35*U}" fill="{hair}"/>'
    elif hstyle == "flat":
        o += box(hx - 6, hy - 0.2*U, hw + 12, 0.45*U, hair, H2, shade(hair, 1.2))
    elif hstyle == "bun":
        o += box(hx - 6, hy - 0.15*U, hw + 12, 0.4*U, hair, H2, shade(hair, 1.2)) + box(hx + 0.45*U, hy - 0.55*U, 0.5*U, 0.4*U, hair, H2, shade(hair, 1.2))
    elif hstyle == "cap":
        o += box(hx - 6, hy - 0.25*U, hw + 12, 0.45*U, hair, H2, shade(hair, 1.2)) + f'<rect x="{hx-0.35*U}" y="{hy+0.12*U}" width="{0.6*U}" height="{0.12*U}" fill="{H2}"/>'
    elif hstyle == "long":
        o += box(hx - 8, hy - 0.2*U, hw + 16, 0.45*U, hair, H2, shade(hair, 1.2)) + f'<rect x="{hx-8}" y="{hy}" width="{0.22*U}" height="{1.5*U}" fill="{hair}"/><rect x="{hx+hw-0.22*U+8}" y="{hy}" width="{0.22*U}" height="{1.5*U}" fill="{hair}"/>'
    elif hstyle == "chef":
        o += box(hx - 4, hy - 0.7*U, hw + 8, 0.85*U, "#ffffff", "#d9dde6", "#ffffff")
    if back:
        o += f'<rect x="{hx-8}" y="{hy}" width="{hw+16}" height="{0.95*U}" fill="{hair}"/>'
    return f'<g id="{bid}"><g transform="translate({x},{y}) scale({s})"><ellipse cx="{0.25*U}" cy="6" rx="{1.9*U}" ry="{0.28*U}" fill="#000" opacity=".25"/><g id="{bid}-b">{o}{extra}</g></g></g>'
