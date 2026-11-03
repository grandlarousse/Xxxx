#!/usr/bin/env python3
"""560 Yil Rumeli - final "Muhur" (archive / memory seal) logo.
python3 -I build.py [out.svg] ['alt' | '{"json":"overrides"}']

All type is converted to outlines (HarfBuzz shaping + fontTools), so the SVG is self-contained.
Strings used (do not change): 'RUMELİ' (U+0130), 'YIL' (plain I), '1352–1912' (U+2013), 'روم ایلی'.
"""
import sys, os, json, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_lib import font, shape, f, pol, circle, ring_path, star8, CX, CY  # noqa
from fontTools.pens.recordingPen import DecomposingRecordingPen, RecordingPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.misc.transform import Transform

TXT_RING_TOP = 'RUMELİ'
TXT_RING_BOT = '1352–1912'
TXT_YIL = 'YIL'
TXT_NUM = '560'
TXT_OTT = 'روم ایلی'
assert TXT_RING_TOP[-1] == 'İ' and TXT_YIL == 'Y' + 'I' + 'L' and TXT_RING_BOT[4] == '–'
assert [ord(c) for c in TXT_OTT] == [0x631, 0x648, 0x645, 0x20, 0x627, 0x6CC, 0x644, 0x6CC]


# ------------------------------------------------------------------ glyph outline helpers (font units, y up)
def rec_glyph(fname, gname):
    gs = font(fname)[1]
    p = DecomposingRecordingPen(gs)
    gs[gname].draw(p)
    return p.value


def rec_map(rec, fn):
    out = []
    for op, pts in rec:
        out.append((op, tuple(fn(x, y) for x, y in pts)))
    return out


def rec_contours(rec):
    cs, cur = [], []
    for op, pts in rec:
        cur.append((op, pts))
        if op in ('closePath', 'endPath'):
            cs.append(cur); cur = []
    return cs


def rec_bounds(rec):
    bp = BoundsPen(None)
    replay(rec, bp)
    return bp.bounds


def replay(rec, pen):
    for op, pts in rec:
        getattr(pen, op)(*pts)


def rec_d(rec, t):
    pen = SVGPathPen(None, ntos=lambda v: ('%.2f' % v).rstrip('0').rstrip('.'))
    replay(rec, TransformPen(pen, t))
    return pen.getCommands()


def rec_points(rec, t):
    pts = []
    for op, ps in rec:
        for x, y in ps:
            pts.append(t.transformPoint((x, y)))
    return pts


def slope_map(y_free, y_full, k, side):
    """Smooth 1-D compression: identity on the free side of y_free, slope k beyond y_full,
    slope blended linearly in between (C1 continuous). side=-1 compresses downward tails, +1 upward."""
    a, b = (y_free, y_full)
    def m(y):
        # integral of slope from a to y
        s = side
        u = (y - a) * s           # distance into the compressed side (>0 inside)
        if u <= 0:
            return y
        w = (b - a) * s           # blend width (>0)
        if u <= w:
            val = u - (1 - k) * u * u / (2 * w)
        else:
            val = w - (1 - k) * w / 2 + k * (u - w)
        return a + s * val
    return m


def line_down(rec, bottom_target, y_free=330, y_full=180):
    """Bring a descending figure (Cinzel 3/5/9) up so its lowest point sits at bottom_target (font units, y up)."""
    lo, hi = 0.05, 1.0
    for _ in range(40):
        k = (lo + hi) / 2
        m = slope_map(y_free, y_full, k, -1)
        r = rec_map(rec, lambda x, y: (x, m(y)))
        if rec_bounds(r)[1] < bottom_target:
            hi = k
        else:
            lo = k
    m = slope_map(y_free, y_full, (lo + hi) / 2, -1)
    return rec_map(rec, lambda x, y: (x, m(y)))


def arc_pts(cx, cy, r, a0, a1):
    """cubic bezier segments approximating a circular arc (angles in radians, y up)"""
    n = max(1, int(math.ceil(abs(a1 - a0) / (math.pi / 4))))
    segs = []
    for i in range(n):
        t0 = a0 + (a1 - a0) * i / n
        t1 = a0 + (a1 - a0) * (i + 1) / n
        k = 4 / 3 * math.tan((t1 - t0) / 4)
        p0 = (cx + r * math.cos(t0), cy + r * math.sin(t0))
        p3 = (cx + r * math.cos(t1), cy + r * math.sin(t1))
        c1 = (p0[0] - k * r * math.sin(t0), p0[1] + k * r * math.cos(t0))
        c2 = (p3[0] + k * r * math.sin(t1), p3[1] - k * r * math.cos(t1))
        segs.append(('curveTo', (c1, c2, p3)))
    return segs


def lancet_contour(xl, xr, yb, yt, jamb_half):
    """Counter-clockwise (y up) closed lancet: pointed arch on top, its mirror below, straight jambs.
    = a bridge arch and its reflection in the water."""
    h = (xr - xl) / 2
    xc = (xl + xr) / 2
    yc = (yb + yt) / 2
    ys_t = yc + jamb_half         # springing line (top arch)
    ys_b = yc - jamb_half
    rise = yt - ys_t
    R = (rise * rise + h * h) / (2 * h)
    # left top arc: centre (xl + R, ys_t); from apex down to springing point (xl, ys_t)
    cxl = xl + R
    a_apex_l = math.atan2(yt - ys_t, xc - cxl)          # angle of apex seen from left centre
    cxr = xr - R
    a_apex_r = math.atan2(yt - ys_t, xc - cxr)
    rec = [('moveTo', ((xc, yt),))]
    rec += arc_pts(cxl, ys_t, R, a_apex_l, math.pi)                 # apex -> left springing (ccw)
    rec.append(('lineTo', ((xl, ys_b),)))                           # left jamb
    rec += arc_pts(cxl, ys_b, R, math.pi, 2 * math.pi - a_apex_l)   # -> bottom apex
    rec += arc_pts(cxr, ys_b, R, -a_apex_r, 0.0)                    # bottom apex -> right springing
    rec.append(('lineTo', ((xr, ys_t),)))                           # right jamb
    rec += arc_pts(cxr, ys_t, R, 0.0, a_apex_r)                     # -> apex
    rec.append(('closePath', ()))
    return rec


# ------------------------------------------------------------------ figures for "560"
def figures_560(c):
    F = c['num_font']
    tt, gs, order, hbf, upem = font(F)
    g = shape(F, TXT_NUM)
    recs = []
    for name, adv, xo, yo in g:
        r = rec_glyph(F, name)
        if name == 'five' and c.get('fix5', True):
            r = line_down(r, -c['num_bottom'], y_free=c['f5_free'], y_full=c['f5_full'])
        if name == 'zero':
            b = rec_bounds(r)
            top_t = c['zero_top']
            s0 = (top_t - b[1]) / (b[3] - b[1])
            r = rec_map(r, lambda x, y, s0=s0, y0=b[1]: (x, y0 + (y - y0) * s0))
            if c.get('zero_lancet'):
                cs = rec_contours(r)
                outer = cs[0]
                # original counter extents after scaling
                cb = rec_bounds(cs[1])
                xl, yb, xr, yt = cb
                xl -= c['lancet_widen']; xr += c['lancet_widen']
                yt += c.get('lancet_dy_top', 0); yb -= c.get('lancet_dy_bot', 0)
                jh = c['lancet_jamb'] * (yt - yb) / 2
                cnt = lancet_contour(xl, xr, yb, yt, jh)
                r = [x for x in outer] + cnt
        recs.append((name, r, adv, xo, yo))
    return recs, upem


def layout_line(items, size, upem, x, y, tracking=0.0, anchor='middle'):
    s = size / upem
    w = sum(a for _, _, a, _, _ in items) * s + tracking * (len(items) - 1)
    x0 = x - (w / 2 if anchor == 'middle' else 0)
    out = []
    px = x0
    for name, r, adv, xo, yo in items:
        t = Transform(s, 0, 0, -s, px + xo * s, y - yo * s)
        out.append((name, r, t))
        px += adv * s + tracking
    return out, w


def placed_bounds(placed):
    bb = [1e9, 1e9, -1e9, -1e9]
    for name, r, t in placed:
        bp = BoundsPen(None)
        replay(r, TransformPen(bp, t))
        if bp.bounds:
            b = bp.bounds
            bb = [min(bb[0], b[0]), min(bb[1], b[1]), max(bb[2], b[2]), max(bb[3], b[3])]
    return bb


def simple_items(fname, text, features=None):
    return [(n, rec_glyph(fname, n), a, xo, yo) for n, a, xo, yo in shape(fname, text, features)]


# ------------------------------------------------------------------ text on a circle (custom items)
def arc_items(items, size, upem, r_base, where, tracking, capH, center_deg=0.0):
    s = size / upem
    advs = [a * s for _, _, a, _, _ in items]
    L = sum(advs) + tracking * (len(items) - 1)
    rm = r_base + capH / 2 if where == 'top' else r_base - capH / 2
    span = L / rm
    ds, pts = [], []
    pos = 0.0
    for (name, r, adv, xo, yo), a in zip(items, advs):
        mid = (pos + a / 2) / rm
        if where == 'top':
            th = math.radians(center_deg) - span / 2 + mid
            t = Transform().translate(CX, CY).rotate(th).translate(-a / 2 + xo * s, -r_base - yo * s).scale(s, -s)
        else:
            th = math.radians(center_deg) + span / 2 - mid
            t = Transform().translate(CX, CY).rotate(th).translate(-a / 2 + xo * s, r_base - yo * s).scale(s, -s)
        ds.append(rec_d(r, t))
        pts += rec_points(r, t)
        pos += a + tracking
    return ' '.join(ds), math.degrees(span), pts


def rect_rec(x0, y0, x1, y1):
    return [('moveTo', ((x0, y0),)), ('lineTo', ((x1, y0),)), ('lineTo', ((x1, y1),)), ('lineTo', ((x0, y1),)), ('closePath', ())]


def date_items(c):
    F = c['ring_font']
    left, right = TXT_RING_BOT.split('–')
    items = []
    for part_i, part in enumerate((left, right)):
        for n, a, xo, yo in shape(F, part):
            r = rec_glyph(F, n)
            b = rec_bounds(r)
            if b[1] < -20 and c.get('date_lining', True):
                r = line_down(r, -c['date_bottom'])
            items.append((n, r, a, xo, yo))
        if part_i == 0:
            # custom en dash: ~0.9 x figure width, centred on the figures' optical middle
            # side bearings are asymmetric on purpose: the 2's open diagonal already brings air on the left
            L = c['dash_len']; th = c['dash_th']; ym = c['dash_y']
            sbl = c.get('dash_sb_l', c.get('dash_sb', 40)); sbr = c.get('dash_sb_r', c.get('dash_sb', 40))
            items.append(('endash*', rect_rec(sbl, ym - th / 2, sbl + L, ym + th / 2), L + sbl + sbr, 0, 0))
    return items


def top_items(c):
    F = c['ring_font']
    items = []
    for n, a, xo, yo in shape(F, TXT_RING_TOP):
        r = rec_glyph(F, n)
        if n == 'Idotaccent' and c.get('idot_drop'):
            cs = rec_contours(r)
            new = []
            for cn in cs:
                b = rec_bounds(cn)
                if b[1] > 720:   # the dot
                    cx_, cy_ = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
                    k = c.get('idot_scale', 1.0); dy = c['idot_drop']
                    cn = rec_map(cn, lambda x, y: (cx_ + (x - cx_) * k, cy_ - dy + (y - cy_) * k))
                new += cn
            r = new
        items.append((n, r, a, xo, yo))
    return items


# ------------------------------------------------------------------ arcade: 56 pointed arches, bases out, crowns in
def arcade_windows(n, r_sill, w_frac, jamb, rise, rot=0.0, m=14):
    step = 360.0 / n
    w = 2 * math.pi * r_sill / n * w_frac
    half = w / 2.0
    R = (rise * rise + half * half) / (2 * half)   # each flank: circle of radius R centred on the far springing side
    flank = []
    a_end = math.atan2(rise, half - R)
    for i in range(m + 1):
        a = math.pi + (a_end - math.pi) * i / m
        # left flank centre at (-half + R, jamb); a from pi (springing) to apex
        flank.append((-half + R + R * math.cos(a), jamb + R * math.sin(a)))
    outline = [(-half, 0.0)] + flank + [(-x, y) for x, y in reversed(flank[:-1])] + [(half, 0.0)]
    out = []
    for k in range(n):
        ang = rot + k * step
        pts = []
        for x, y in outline:
            r = r_sill - y                    # crowns point to the centre
            a = ang + math.degrees(x / r_sill)
            pts.append(pol(r, a))
        out.append('M' + 'L'.join(f'{f(px)} {f(py)}' for px, py in pts) + 'Z')
    return ''.join(out), w


def build(c):
    P = []
    BG, BAND, FIELD, GOLD, PARCH = c['bg'], c['band'], c['field'], c['gold'], c['parch']
    P.append(f'<rect width="1080" height="1080" fill="{BG}"/>')
    info = {}

    # ---- arcade ring
    r_out, r_in = c['r_gold_out'], c['r_gold_in']
    P.append(f'<path fill="{c.get("arc_col", GOLD)}" fill-rule="evenodd" d="{ring_path(r_out, r_in)}"/>')
    if BAND != BG:
        P.append(circle(r_in, fill=BAND))
    win_d, win_w = arcade_windows(c['arches'], c['r_sill'], c['arch_wfrac'], c['arch_jamb'], c['arch_rise'], rot=c.get('arch_rot', 0))
    P.append(f'<path fill="{c["win"]}" d="{win_d}"/>')
    info['arch_w'] = win_w
    info['arch_apex_r'] = c['r_sill'] - c['arch_jamb'] - c['arch_rise']

    # ---- seal field + single rule
    P.append(circle(c['r_field'], fill=FIELD))
    P.append(circle(c['r_rule'], fill='none', stroke=c.get('rule_col', GOLD), stroke_width=c['rule_w']))

    # ---- ring text
    F = c['ring_font']; upem = font(F)[4]
    capH = 700 * c['ring_size'] / upem
    top_d, top_span, top_pts = arc_items(top_items(c), c['ring_size'], upem, c['r_top_base'], 'top', c['ring_track'], capH)
    capHb = 714 * c['ring_size_b'] / upem
    bot_d, bot_span, bot_pts = arc_items(date_items(c), c['ring_size_b'], upem, c['r_bot_base'], 'bottom', c['ring_track_b'], capHb)
    P.append(f'<path fill="{c.get("top_col", GOLD)}" d="{top_d}"/>')
    P.append(f'<path fill="{c.get("bot_col", GOLD)}" d="{bot_d}"/>')
    rr = lambda pts: [math.hypot(x - CX, y - CY) for x, y in pts]
    info['top_r'] = (min(rr(top_pts)), max(rr(top_pts)))
    info['bot_r'] = (min(rr(bot_pts)), max(rr(bot_pts)))
    info['top_span'] = top_span; info['bot_span'] = bot_span

    # ---- 8-point stars at 3 and 9 o'clock
    r_mid = c['star_r']
    orn = [star8(*pol(r_mid, ang), c['star_R'], rot=22.5 + ang) for ang in (90, 270)]
    P.append(f'<path fill="{c.get("star_col", GOLD)}" d="{"".join(orn)}"/>')

    # ---- centre stack: (Ottoman) / 560 / YIL, optically centred
    nitems, nupem = figures_560(c)
    placed, _ = layout_line(nitems, c['num_size'], nupem, CX, 0, tracking=c['num_track'])
    nbb0 = placed_bounds(placed)
    yitems = simple_items(c['yil_font'], TXT_YIL)
    yupem = font(c['yil_font'])[4]
    yp0, _ = layout_line(yitems, c['yil_size'], yupem, CX, 0, tracking=c['yil_track'])
    ybb0 = placed_bounds(yp0)
    oitems = simple_items(c['ott_font'], TXT_OTT)
    oupem = font(c['ott_font'])[4]
    op0, _ = layout_line(oitems, c['ott_size'], oupem, CX, 0)
    obb0 = placed_bounds(op0)
    # vertical metrics of each block (relative to its own baseline at 0)
    num_h = nbb0[3] - nbb0[1]
    yil_h = ybb0[3] - ybb0[1]
    # the Ottoman line is measured on its visual core (bowl band), not on alif tops / descender tails
    ott_top, ott_bot = obb0[1], obb0[3]
    stack = [('ott', ott_bot - ott_top), ('gap', c['ott_gap']), ('num', num_h), ('gap', c['gap']), ('yil', yil_h)]
    total = sum(h for _, h in stack)
    top = c['stack_cy'] - total / 2
    y_ott_top = top
    y_num_top = top + (ott_bot - ott_top) + c['ott_gap']
    y_yil_top = y_num_top + num_h + c['gap']
    num_base = y_num_top - nbb0[1]
    yil_base = y_yil_top - ybb0[1]
    ott_base = y_ott_top - ott_top

    placed, _ = layout_line(nitems, c['num_size'], nupem, CX + c.get('num_dx', 0), num_base, tracking=c['num_track'])
    nbb = placed_bounds(placed)
    P.append(f'<path fill="{PARCH}" d="{" ".join(rec_d(r, t) for _, r, t in placed)}"/>')
    npts = [p for _, r, t in placed for p in rec_points(r, t)]
    info['num_bbox'] = nbb
    info['num_r_max'] = max(rr(npts))

    yp, _ = layout_line(yitems, c['yil_size'], yupem, CX, yil_base, tracking=c['yil_track'])
    ybb = placed_bounds(yp)
    P.append(f'<path fill="{c.get("yil_col", GOLD)}" d="{" ".join(rec_d(r, t) for _, r, t in yp)}"/>')
    info['yil_bbox'] = ybb
    ym = (ybb[1] + ybb[3]) / 2
    L = c['yil_rule_len']; g2 = c['yil_rule_gap']; rw = c['yil_rule_w']
    if L > 0:
        rl = []
        for side in (-1, 1):
            x_in = (ybb[0] - g2) if side < 0 else (ybb[2] + g2)
            x_out = x_in + side * L
            x0, x1 = min(x_in, x_out), max(x_in, x_out)
            if c.get('yil_rule_lozenge'):
                # tapered rule ending in a point (outer end) - lighter than a bar
                xo_, xi_ = x_out, x_in
                rl.append(f'M{f(xi_)} {f(ym - rw / 2)}L{f(xo_)} {f(ym)}L{f(xi_)} {f(ym + rw / 2)}Z')
            else:
                rl.append(f'M{f(x0)} {f(ym - rw / 2)}H{f(x1)}V{f(ym + rw / 2)}H{f(x0)}Z')
        P.append(f'<path fill="{c.get("yil_col", GOLD)}" d="{"".join(rl)}"/>')

    if c.get('ottoman'):
        op, _ = layout_line(oitems, c['ott_size'], oupem, CX + c.get('ott_dx', 0), ott_base)
        obb = placed_bounds(op)
        P.append(f'<path fill="{c.get("ott_col", GOLD)}" d="{" ".join(rec_d(r, t) for _, r, t in op)}"/>')
        info['ott_bbox'] = obb

    info['ring_capH_110'] = capH * 110 / 1080
    info['yil_capH_110'] = (ybb[3] - ybb[1]) * 110 / 1080
    info['num_h_110'] = (nbb[3] - nbb[1]) * 110 / 1080
    info['yil_w_over_num_w'] = (ybb[2] - ybb[0]) / (nbb[2] - nbb[0])
    title = '560 Yıl Rumeli — روم ایلی — 1352–1912'
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">\n'
           f'<title>{title}</title>\n' + '\n'.join(P) + '\n</svg>\n')
    return svg, info


# ------------------------------------------------------------------ palette + layout (final)
# palette: deep bordo #2a0a10 / seal bordo #6a1621 / aged brass #c9a66b / parchment #f3e5c8 / Iznik firuze #3f9c92
CFG = {'bg': '#2a0a10',
 'band': '#2a0a10',
 'field': '#6a1621',
 'gold': '#c9a66b',
 'parch': '#f3e5c8',
 'win': '#6a1621',
 'r_gold_out': 505,
 'r_gold_in': 463,
 'arches': 56,
 'r_sill': 499,
 'arch_wfrac': 0.44,
 'arch_jamb': 11,
 'arch_rise': 19,
 'r_field': 337,
 'r_rule': 337,
 'rule_w': 6,
 'ring_font': 'Cinzel-900',
 'ring_size': 106,
 'ring_track': 40,
 'r_top_base': 363,
 'idot_drop': 34,
 'idot_scale': 0.88,
 'ring_size_b': 106,
 'ring_track_b': 20,
 'r_bot_base': 440,
 'date_bottom': 14,
 'dash_len': 470,
 'dash_th': 86,
 'dash_y': 352,
 'star_r': 401,
 'star_R': 30,
 'num_font': 'Cinzel-900',
 'num_size': 300,
 'num_track': -4,
 'num_dx': 0,
 'num_bottom': 15,
 'f5_free': 300,
 'f5_full': 150,
 'zero_top': 740,
 'zero_lancet': True,
 'lancet_widen': 8,
 'lancet_jamb': 0.42,
 'yil_font': 'Cinzel-900',
 'yil_size': 110,
 'yil_track': 50,
 'gap': 34,
 'yil_rule_len': 0,
 'yil_rule_gap': 24,
 'yil_rule_w': 7,
 'yil_rule_lozenge': False,
 'ottoman': True,
 'ott_font': 'Amiri-700',
 'ott_size': 68,
 'ott_gap': 26,
 'stack_cy': 532,
 'top_col': '#f3e5c8',
 'rule_col': '#3f9c92',
 'star_col': '#3f9c92',
 'dash_sb_l': 28,
 'dash_sb_r': 46}
# light "seal on parchment" colorway
ALT = {
 "top_col": "#2a0a10",
 "win": "#f3e5c8",
 "star_col": "#2f8f86",
 "bg": "#f3e5c8",
 "band": "#f3e5c8",
 "arc_col": "#6a1621",
 "bot_col": "#6a1621"
}

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'logo_src.svg')
    cfg = dict(CFG)
    if len(sys.argv) > 2:
        cfg.update(ALT if sys.argv[2] == 'alt' else json.loads(sys.argv[2]))
    svg, info = build(cfg)
    open(out, 'w').write(svg)
    def rnd(v):
        if isinstance(v, float): return round(v, 1)
        if isinstance(v, (list, tuple)): return [rnd(x) for x in v]
        return v
    print(json.dumps({k: rnd(v) for k, v in info.items()}))
