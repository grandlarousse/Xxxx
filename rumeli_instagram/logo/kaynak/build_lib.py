#!/usr/bin/env python3
"""Generator for the "Muhur" (Ottoman seal) logo of 560 Yil Rumeli.
All type is converted to outlines (HarfBuzz shaping + fontTools), so logo.svg is self-contained.
Run:  python3 -I build.py   (writes logo.svg next to this file)
"""
import math, os, json
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.misc.transform import Transform

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, '..', 'fonts')
CX = CY = 540.0

# ---------------------------------------------------------------- palette
INK = '#3d0a12'        # deepest crimson (outer field / ring band)
CRIMSON = '#7a1823'    # seal field
GOLD = '#d1a95a'       # antique gold
PARCH = '#f4e6c6'      # parchment

_cache = {}
def font(name):
    if name not in _cache:
        path = os.path.join(FONTS, name + '.ttf')
        tt = TTFont(path)
        blob = hb.Blob.from_file_path(path)
        face = hb.Face(blob)
        _cache[name] = (tt, tt.getGlyphSet(), tt.getGlyphOrder(), hb.Font(face), face.upem)
    return _cache[name]

def shape(fname, text, features=None):
    tt, gs, order, hbf, upem = font(fname)
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    feats = {'kern': True, 'liga': True}; feats.update(features or {})
    hb.shape(hbf, buf, feats)
    return [(order[i.codepoint], p.x_advance, p.x_offset, p.y_offset) for i, p in zip(buf.glyph_infos, buf.glyph_positions)]

def glyph_d(fname, gname, t):
    tt, gs, order, hbf, upem = font(fname)
    pen = SVGPathPen(gs, ntos=lambda v: ('%.2f' % v).rstrip('0').rstrip('.'))
    gs[gname].draw(TransformPen(pen, t))
    return pen.getCommands()

def glyph_bounds(fname, gname, t):
    tt, gs, order, hbf, upem = font(fname)
    bp = BoundsPen(gs); gs[gname].draw(TransformPen(bp, t))
    return bp.bounds

def line_text(fname, text, size, x, y, anchor='middle', tracking=0.0, features=None, per_glyph=False):
    """Straight text; returns (d or list of d, bbox[xmin,ymin,xmax,ymax])"""
    upem = font(fname)[4]; s = size / upem
    g = shape(fname, text, features)
    w = sum(a for _, a, _, _ in g) * s + tracking * (len(g) - 1)
    x0 = x - (w / 2 if anchor == 'middle' else (w if anchor == 'end' else 0))
    ds, bb = [], [1e9, 1e9, -1e9, -1e9]
    px = x0
    for name, adv, xo, yo in g:
        t = Transform(s, 0, 0, -s, px + xo * s, y - yo * s)
        d = glyph_d(fname, name, t)
        b = glyph_bounds(fname, name, t)
        if b:
            bb = [min(bb[0], b[0]), min(bb[1], b[1]), max(bb[2], b[2]), max(bb[3], b[3])]
        ds.append(d)
        px += adv * s + tracking
    return (ds if per_glyph else ' '.join(ds)), bb, w

def arc_text(fname, text, size, r_base, where='top', tracking=0.0, center_deg=0.0, features=None, cap=None):
    """Text set on a circle. Spacing is measured at the mid-cap radius for optical evenness.
    top: reads clockwise over the top, baseline at r_base, letters point outward.
    bottom: reads left->right under the bottom, baseline at r_base, letters point inward."""
    tt, gs, order, hbf, upem = font(fname)
    s = size / upem
    capH = (cap if cap is not None else tt['OS/2'].sCapHeight) * s
    g = shape(fname, text, features)
    advs = [a * s for _, a, _, _ in g]
    L = sum(advs) + tracking * (len(g) - 1)
    rm = r_base + capH / 2 if where == 'top' else r_base - capH / 2
    span = L / rm
    ds = []
    pos = 0.0
    for (name, adv, xo, yo), a in zip(g, advs):
        mid = (pos + a / 2) / rm
        if where == 'top':
            th = math.radians(center_deg) - span / 2 + mid
            t = Transform().translate(CX, CY).rotate(th).translate(-a / 2 + xo * s, -r_base - yo * s).scale(s, -s)
        else:
            th = math.radians(center_deg) + span / 2 - mid
            t = Transform().translate(CX, CY).rotate(th).translate(-a / 2 + xo * s, r_base - yo * s).scale(s, -s)
        ds.append(glyph_d(fname, name, t))
        pos += a + tracking
    return ' '.join(ds), math.degrees(span)

# ---------------------------------------------------------------- geometry helpers
def f(v):
    return ('%.2f' % v).rstrip('0').rstrip('.')

def pol(r, deg):
    a = math.radians(deg)
    return CX + r * math.sin(a), CY - r * math.cos(a)   # 0deg = 12 o'clock, clockwise

def circle(r, **attrs):
    a = ' '.join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return f'<circle cx="{f(CX)}" cy="{f(CY)}" r="{f(r)}" {a}/>'

def ring_path(r_out, r_in):
    """annulus as a single path (even-odd)"""
    def c(r):
        return (f'M{f(CX - r)} {f(CY)}A{f(r)} {f(r)} 0 1 1 {f(CX + r)} {f(CY)}'
                f'A{f(r)} {f(r)} 0 1 1 {f(CX - r)} {f(CY)}Z')
    return c(r_out) + c(r_in)

def star8(cx, cy, R, ratio=0.7654, rot=22.5):
    """8-point star; ratio 0.7654 = two overlapping squares (Seljuk/Ottoman star)."""
    pts = []
    for i in range(16):
        r = R if i % 2 == 0 else R * ratio
        a = math.radians(rot + i * 22.5)
        pts.append((cx + r * math.sin(a), cy - r * math.cos(a)))
    return 'M' + 'L'.join(f'{f(x)} {f(y)}' for x, y in pts) + 'Z'

def pointed_arch_crown(n, r_valley, r_tip, r_base, rot=0.0):
    """Outer contour: n pointed (ogee-ish) arches pointing outward, closed with an inner circle r_base."""
    d = []
    step = 360.0 / n
    for i in range(n):
        a0 = rot + i * step
        a1 = a0 + step
        am = a0 + step / 2
        p0 = pol(r_valley, a0)
        tip = pol(r_tip, am)
        # two quadratic-ish curves using cubic beziers -> pointed arch with convex flanks
        c1 = pol(r_valley + (r_tip - r_valley) * 0.78, a0 + step * 0.06)
        c2 = pol(r_tip - (r_tip - r_valley) * 0.10, am - step * 0.20)
        c3 = pol(r_tip - (r_tip - r_valley) * 0.10, am + step * 0.20)
        c4 = pol(r_valley + (r_tip - r_valley) * 0.78, a1 - step * 0.06)
        p1 = pol(r_valley, a1)
        if i == 0:
            d.append(f'M{f(p0[0])} {f(p0[1])}')
        d.append(f'C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(tip[0])} {f(tip[1])}')
        d.append(f'C{f(c3[0])} {f(c3[1])} {f(c4[0])} {f(c4[1])} {f(p1[0])} {f(p1[1])}')
    d.append('Z')
    r = r_base
    d.append(f'M{f(CX - r)} {f(CY)}A{f(r)} {f(r)} 0 1 0 {f(CX + r)} {f(CY)}A{f(r)} {f(r)} 0 1 0 {f(CX - r)} {f(CY)}Z')
    return ''.join(d)

def dots_ring(n, r, rad, rot=0.0):
    out = []
    for i in range(n):
        x, y = pol(r, rot + i * 360.0 / n)
        out.append(f'M{f(x - rad)} {f(y)}a{f(rad)} {f(rad)} 0 1 0 {f(2 * rad)} 0a{f(rad)} {f(rad)} 0 1 0 {f(-2 * rad)} 0Z')
    return ''.join(out)


def arcade_ring(n, r_base, w_deg_frac, h_jamb, rise, rot=0.0):
    """n pointed-arch windows arranged radially, bases on r_base, pointing outward."""
    out = []
    step = 360.0 / n
    w = 2 * math.pi * r_base / n * w_deg_frac
    # build symmetric outline
    half = w / 2.0
    c = (rise * rise - half * half) / (2 * half)
    R = half + c
    m = 16
    left = []
    for i in range(m + 1):
        # left flank centred at (c, h_jamb): angle from pi (point (-half,h)) to apex angle
        a_start = math.pi
        a_end = math.atan2(rise, -c)
        a = a_start + (a_end - a_start) * i / m
        left.append((c + R * math.cos(a), h_jamb + R * math.sin(a)))
    outline = [(-half, 0.0)] + left + [(-x, y) for x, y in reversed(left[:-1])] + [(half, 0.0)]
    for k in range(n):
        ang = rot + k * step
        pts = []
        for x, y in outline:
            r = r_base + y
            a = ang + math.degrees(x / r_base)
            pts.append(pol(r, a))
        out.append('M' + 'L'.join(f'{f(px)} {f(py)}' for px, py in pts) + 'Z')
    return ''.join(out)

