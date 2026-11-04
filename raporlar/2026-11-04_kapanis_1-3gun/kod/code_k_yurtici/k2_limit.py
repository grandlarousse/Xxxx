"""(b) Taban/tavan sonrası 1–3 gün — kapanıştan kapanışa, dolum kısıtıyla.
Olay günü t (yalnız ±%10 rejimi, 2020-03-13+): spot TC (tavan kapanış: adj oranı ≥1,0925 ve c ≥ 0,999·h), BC (taban kapanış: ≤0,9075 ve c ≤ 1,001·l).
Kilit: spotta h==l (gün boyu kilitli); VİOP'ta uzlaşma limitte (lock_up/lock_dn: uzlaşma/önceki uzlaşma ≥ +%9,7 / ≤ −%9,7).
Dolum kuralı (VİOP uzlaşmasından): limitte kilitli vadelide limit yönünde (tavanda alım, tabanda satım) dolum YOK; ters yönde var.
Stratejiler: CONT (devam), REV (dönüş); E0 = t uzlaşması, E2 = t+1 uzlaşması (t+1'de de dolum kontrolü).
"""
from klib import *
C = ctx(); vcal = C['vcal']; scal = C['scal']; W = C['W']
a, c, h, l = W['adj'], W['c'], W['h'], W['l']
R = a / a.ffill().shift(1)
stocks = [s for s in a.columns if s not in ['XU100', 'XU030', 'XBANK', 'XHOLD']]
P10 = a.index >= REG
TC = (R >= 1.0925) & (c >= 0.999 * h) & P10[:, None]
BC = (R <= 0.9075) & (c <= 1.001 * l) & P10[:, None]
TCL = TC & (l >= 0.999 * h); BCL = BC & (l >= 0.999 * h)
TC, BC, TCL, BCL = [x[stocks] for x in (TC, BC, TCL, BCL)]
def events(M, lab):
    s = M.stack(); s = s[s]; return pd.DataFrame({'date': s.index.get_level_values(0), 'und': s.index.get_level_values(1), 'ev': lab})
E = pd.concat([events(TC, 'TC'), events(BC, 'BC')], ignore_index=True)
E['locked_spot'] = [bool(TCL.at[d, u]) if e == 'TC' else bool(BCL.at[d, u]) for d, u, e in zip(E.date, E.und, E.ev)]
E['v47'] = E.und.isin(VIOP47)
print('olay sayısı', E.groupby(['ev', 'v47']).size().to_dict())
# VİOP durumu (t ve t+1)
LU, LD = C['lock_up'], C['lock_dn']
def lk(M, d, u):
    try: v = M.at[d, u]; return bool(v) if pd.notna(v) else None
    except KeyError: return None
E['d1'] = shift_date(E['date'], 1, vcal)
E['fut_has'] = [ (u in LU.columns) and (d in LU.index) and pd.notna(LU.at[d, u]) for d, u in zip(E.date, E.und)]
E['flock_t'] = [lk(LU, d, u) if e == 'TC' else lk(LD, d, u) for d, u, e in zip(E.date, E.und, E.ev)]
E['flock_t1'] = [lk(LU, d, u) if e == 'TC' else lk(LD, d, u) for d, u, e in zip(E.d1, E.und, E.ev)]
V = E[E.v47 & E.fut_has].copy()
print('VİOP47 + vadeli var:', V.groupby('ev').size().to_dict(), '| t günü vadeli kilitli oranı:', V.groupby('ev').flock_t.mean().round(3).to_dict(),
      '| t+1 kilitli:', V.groupby('ev').flock_t1.mean().round(3).to_dict())
out = []
def run(name, ev, h, entry, hedge, inst='VIOP'):
    ev = ev.copy()
    if inst == 'VIOP':
        ev['ret'] = vectorized_fut(ev, h, 'E0', hedge=hedge)
        st = trade_stats(ev, 'ret', h=h, is_end=V_IS_END)
    else:
        ev['ret'] = vectorized_spot(ev, h, excess='XU100')
        st = trade_stats(ev, 'ret', h=h, is_end=V_IS_END)
    reg('b_limit', name, inst + ('_hedge' if hedge else ''), entry, h, st)
    out.append(f"{name:42s} {inst+('_h' if hedge else ''):8s} {entry} h{h} {fmt(st)}")
for evn in ['TC', 'BC']:
    sgn_cont = 1 if evn == 'TC' else -1
    base = V[V.ev == evn]
    for h in H:
        for hedge in [False, True]:
            # E0 devam: yalnız vadeli limitte kilitli değilse
            e0c = base[base.flock_t == False].assign(side=sgn_cont)
            run(f'{evn} DEVAM E0 (vadeli kilitsiz)', e0c, h, 'E0', hedge)
            e0r = base.assign(side=-sgn_cont)
            run(f'{evn} DÖNÜŞ E0 (tümü)', e0r, h, 'E0', hedge)
            # E2: t+1 uzlaşması, devam yönünde t+1 kilitsizse
            e2c = base[base.flock_t1 == False].assign(side=sgn_cont, date=lambda x: x.d1)
            run(f'{evn} DEVAM E2 (t+1 kilitsiz)', e2c, h, 'E2', hedge)
            e2r = base.assign(side=-sgn_cont, date=lambda x: x.d1)
            run(f'{evn} DÖNÜŞ E2', e2r, h, 'E2', hedge)
        # spot kıyas (XU100 fazla getiri), tüm evren, E2 (t+1 kapanış; dolum-uygun: t+1 kilitli değilse)
        sb = E[(E.ev == evn)].copy()
        sb['d1s'] = shift_date(sb['date'], 1, scal)
        lockmat = TCL if evn == 'TC' else BCL
        sb['slock1'] = [bool(lockmat.at[d, u]) if (pd.notna(d) and d in lockmat.index) else True for d, u in zip(sb.d1s, sb.und)]
        e2s = sb[~sb.slock1].assign(side=sgn_cont, date=lambda x: x.d1s)
        run(f'{evn} DEVAM E2 spot tüm evren (t+1 kilitsiz)', e2s, h, 'E2', False, inst='SPOT')
        e2s47 = e2s[e2s.v47]
        run(f'{evn} DEVAM E2 spot VİOP47', e2s47, h, 'E2', False, inst='SPOT')
for o in out: print(o)
# Kilitsiz TC günlerinde vadeli uzlaşması spot kapanışın ne kadar altında? (vadeli 'gerçek fiyatı' gösteriyor mu)
Vt = V[(V.ev == 'TC')]
print('\nTC: vadeli t günü uzlaşma getirisi medyan (kilitsiz):', 1e4 * np.nanmedian([C['raw_r'].at[d, u] for d, u in zip(Vt[Vt.flock_t == False].date, Vt[Vt.flock_t == False].und)]))
D = save_registry('b_limit'); print('test sayısı', len(D))
