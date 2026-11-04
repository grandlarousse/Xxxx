"""(a) Temettü: ex-gün öncesi yükseliş / sonrası geri veriş — kapanıştan kapanışa, VİOP uzlaşması ve spot ayrı.
Olaylar: out/code_y_akis/res_div_events.csv (Yahoo adj/c sıçraması; ex-gün; verim dy). Tarihler önceden ilan edilir -> sinyal geçerli.
Pencereler (E = ex-gün):
  PRE_k: giriş E-k kapanış/uzlaşma, çıkış E-1 (hak kullanım öncesi son gün), uzun.  h = k-1.
  PRE_kE: giriş E-k, çıkış E (ex günü dahil), uzun. h = k.
  EX: giriş E-1, çıkış E (ex günü), kısa (spotta toplam getiri = adj).
  POST_h: giriş E (ex kapanışı), çıkış E+h, kısa.
  POSTc_h: giriş E-1, çıkış E-1+h, kısa (ex günü dahil).
"""
from klib import *
C = ctx(); vcal = C['vcal']; scal = C['scal']
ev = pd.read_csv(S + '/out/code_y_akis/res_div_events.csv', parse_dates=['date'])
ev = ev.rename(columns={'stock': 'und'})
print('olay', len(ev), 'VİOP47', ev.und.isin(VIOP47).sum())
# vadeli ex-gün davranışı: vadeli uzlaşma getirisi ex gününde spot fiyat mı düzeltilmiş mi izliyor?
W = C['W']
rows = []
for _, e in ev[ev.und.isin(VIOP47)].iterrows():
    d = e.date
    if d not in vcal or e.und not in C['raw_r'].columns: continue
    fr = C['raw_r'].at[d, e.und]
    try:
        c = W['c'][e.und]; a = W['adj'][e.und]; i = c.index.get_loc(d)
        pr = np.log(c.iloc[i] / c.iloc[i - 1]); ar = np.log(a.iloc[i] / a.iloc[i - 1])
    except Exception: continue
    rows.append(dict(und=e.und, date=d, dy=e.dy, fut=fr, spot_px=pr, spot_adj=ar))
X = pd.DataFrame(rows).dropna()
print('\nVadeli ex-gün kontrolü (n=%d): vadeli−düzeltilmiş spot medyan %.1f bps; vadeli−fiyat spot medyan %.1f bps; ort. verim %.1f bps' % (
    len(X), 1e4 * (X.fut - X.spot_adj).median(), 1e4 * (X.fut - X.spot_px).median(), 1e4 * X.dy.mean()))
print('  -> vadeli temettüde düşmüyor (temettü bazda fiyatlanmış); vadeli getirisi düzeltilmiş spot getirisine yakın' if abs((X.fut - X.spot_adj).median()) < abs((X.fut - X.spot_px).median()) else '  -> vadeli fiyat düşüşünü izliyor!')

def build(evs, cal, k, side, base_shift):
    """giriş = E + base_shift (takvimde), döner DataFrame und,date,side,dy"""
    d = shift_date(evs['date'], base_shift, cal)
    o = pd.DataFrame({'und': evs['und'].values, 'date': d, 'side': side, 'dy': evs['dy'].values, 'ex': evs['date'].values})
    return o.dropna(subset=['date'])

specs = []
for k, h in [(2, 1), (3, 2), (4, 3), (6, 5)]: specs.append((f'PRE_{k}->E-1', -k, h, +1))
for k, h in [(1, 1), (2, 2), (3, 3), (5, 5)]: specs.append((f'PRE_{k}->E', -k, h, +1))
for h in [1, 2, 3, 5]: specs.append((f'POST E->E+{h}', 0, h, -1))
for h in [2, 3, 5]: specs.append((f'POSTc E-1->E-1+{h}', -1, h, -1))
specs.append(('EX E-1->E', -1, 1, -1))

out = []
for name, sh, h, side in specs:
    # VİOP: dayanak vadeli varsa (tarih kontrolü vadeli panelde NaN ile)
    for univ in ['VIOP47']:
        e = ev[ev.und.isin(VIOP47)]
        b = build(e, vcal, 0, side, sh)
        for hedge in [False, True]:
            b['ret'] = vectorized_fut(b, h, 'E0', hedge=hedge)
            st = trade_stats(b, 'ret', h=h, is_end=V_IS_END)
            reg('a_temettu', name, 'VIOP' + ('_hedge' if hedge else ''), 'E0', h, st, dict(univ=univ, side=side))
            out.append((name, 'VIOP' + ('_h' if hedge else ''), h, fmt(st)))
        b['ret'] = vectorized_fut(b, h, 'E1'); st = trade_stats(b, 'ret', h=h, is_end=V_IS_END)
        reg('a_temettu', name, 'VIOP', 'E1', h, st, dict(univ=univ, side=side)); out.append((name, 'VIOP_E1', h, fmt(st)))
    # Spot: VİOP47 ve tüm evren, XU100'e göre fazla getiri (toplam getiri)
    for univ, e in [('VIOP47', ev[ev.und.isin(VIOP47)]), ('ALL', ev)]:
        b = build(e, scal, 0, side, sh)
        b['ret'] = vectorized_spot(b, h, excess='XU100'); st = trade_stats(b, 'ret', h=h, is_end=S_IS_END)
        reg('a_temettu', name, 'SPOT_x', 'C', h, st, dict(univ=univ, side=side)); out.append((name, f'SPOTx_{univ}', h, fmt(st)))
        # VİOP döneminde spot (aynı olaylar, 2017+) — kıyas için
        if univ == 'VIOP47':
            b2 = b[b.date >= '2017-03-06'].copy(); st = trade_stats(b2, 'ret', h=h, is_end=V_IS_END)
            reg('a_temettu', name, 'SPOT_x_2017+', 'C', h, st, dict(univ=univ, side=side)); out.append((name, 'SPOTx_V47_2017+', h, fmt(st)))
for o in out: print(f'{o[0]:22s} {o[1]:16s} h{o[2]} {o[3]}')
# verim büyüklüğüne göre (VİOP, PRE_4->E-1)
print('\nVerim tercili — PRE_4->E-1 (h3), VİOP E0 ham ve spot fazla getiri:')
e = ev[ev.und.isin(VIOP47)].copy(); e['q'] = pd.qcut(e.dy, 3, labels=['düşük', 'orta', 'yüksek'])
for q, g in e.groupby('q'):
    b = build(g, vcal, 0, 1, -4); b['ret'] = vectorized_fut(b, 3, 'E0'); s1 = trade_stats(b, 'ret', h=3)
    b2 = build(g, scal, 0, 1, -4); b2['ret'] = vectorized_spot(b2, 3); s2 = trade_stats(b2, 'ret', h=3, is_end=S_IS_END)
    print(f'  {q:7s} verim medyan {1e4*g.dy.median():.0f} bps | VİOP {fmt(s1)}\n          spot {fmt(s2)}')
D = save_registry('a_temettu'); print('\ntest sayısı', len(D))
# ---- yüksek verimli temettüler (verim ≥ %4; temettü tutarı ilan edildiği için ex-ante bilinir) ----
print('\nYüksek verim (dy ≥ %4):')
hi = ev[ev.dy >= 0.04]
for univ, e in [('VIOP47', hi[hi.und.isin(VIOP47)]), ('ALL', hi)]:
    for k, h in [(3, 2), (4, 3), (6, 5)]:
        b = build(e, scal, 0, 1, -k); b['ret'] = vectorized_spot(b, h, excess='XU100'); st = trade_stats(b, 'ret', h=h, is_end=S_IS_END)
        reg('a_temettu', f'yüksek verim PRE_{k}->E-1', 'SPOT_x', 'C', h, st, dict(univ=univ, side=1)); print(f'  spot {univ:6s} PRE_{k}->E-1 h{h} {fmt(st)} | {st["by_year"]}')
        if univ == 'VIOP47':
            b = build(e, vcal, 0, 1, -k); b['ret'] = vectorized_fut(b, h, 'E0'); st = trade_stats(b, 'ret', h=h, is_end=V_IS_END)
            reg('a_temettu', f'yüksek verim PRE_{k}->E-1', 'VIOP', 'E0', h, st, dict(univ=univ, side=1)); print(f'  VİOP {univ:6s} PRE_{k}->E-1 h{h} {fmt(st)}')
D = save_registry('a_temettu'); print('test sayısı', len(D))
