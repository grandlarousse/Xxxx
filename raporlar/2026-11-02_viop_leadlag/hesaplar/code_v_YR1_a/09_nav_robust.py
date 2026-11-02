"""YR1-B sağlamlık: temizlik kuralı, NAV ağırlıkları/başlangıç/yeniden dengeleme, z penceresi×eşik ızgarası, plasebolar (REL, rastgele sepet)."""
import sys; HERE = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_YR1_a'; sys.path.insert(0, HERE)
exec(open(HERE + '/07_nav.py').read().split("if __name__ == '__main__':")[0])
import vlib
pd.set_option('display.width', 260); pd.set_option('display.max_rows', 300)
def quick(navr, win=250, thr=1.0, cost=8, entry='open', Kser=None):
    pos, z = signal(navr, win, thr)
    sim = simulate(pos, tg, ti, tc, lw, entry, cost)
    o = {}
    for per, lo, hi in [('IS', '2014-01-01', SPLIT), ('OOS', SPLIT, '2027-01-01')]:
        st = summarize(sim, lo, hi); o[f'{per}_m'] = st['mean_bps']; o[f'{per}_t'] = st['t_all']
    yb = by_year(sim[sim.index >= '2014-01-01']); o['yrs'] = f'{int((yb > 0).sum())}/{len(yb)}'
    return o
rows = []
rows.append(dict(var='temel (rejim temizliği, W0, 2010 al-tut)', **quick(nav_ret(W0))))
# eski simetrik ±%10,5 kuralı: bileşenlerde bayrak
def nav_ret_sym(W, start='2010-01-01'):
    rr = {}
    for k in W:
        d = raw(k); r = np.log(d['adj']).diff(); r[(r > np.log(1.105)) | (r < np.log(0.895))] = np.nan; rr[k] = r.reindex(cal)
    rr = pd.DataFrame(rr); rr = rr[rr.index >= start]
    w0 = pd.Series(W, dtype=float); w0 /= w0.sum(); avail = rr.notna().cumsum() > 0
    val = (np.exp(rr.fillna(0).cumsum()) * w0).where(avail, 0.0); wt = val.shift(1).div(val.shift(1).sum(axis=1), axis=0)
    o = (wt * rr.fillna(0)).sum(axis=1); o[wt.sum(axis=1) == 0] = np.nan; return o.reindex(cal)
rows.append(dict(var='eski simetrik ±%10,5 temizliği (bileşenler)', **quick(nav_ret_sym(W0))))
Wx = dict(W0); Wx.pop('AYGAZ'); rows.append(dict(var='AYGAZ hariç (Yahoo adj temettü hatası)', **quick(nav_ret(Wx))))
rows.append(dict(var='al-tut başlangıcı 2014', **quick(nav_ret(W0, '2014-01-01'))))
rows.append(dict(var='al-tut başlangıcı 2012', **quick(nav_ret(W0, '2012-01-01'))))
rows.append(dict(var='yıllık yeniden dengeleme', **quick(nav_ret(W0, rebal='Y'))))
rows.append(dict(var='eşit ağırlık 8 bileşen', **quick(nav_ret({k: 1 for k in W0}))))
rows.append(dict(var='yalnız TUPRS/FROTO/YKBNK (.4/.25/.35)', **quick(nav_ret({'TUPRS': .4, 'FROTO': .25, 'YKBNK': .35}))))
rows.append(dict(var='YKBNK ağırlığı .12 (2020 öncesi efektif pay)', **quick(nav_ret({**W0, 'YKBNK': .12}))))
rows.append(dict(var='ağırlıklar ±%30 karıştırılmış (ort. 20 çekiliş)', **pd.DataFrame([quick(nav_ret({k: v * np.random.default_rng(s).uniform(.7, 1.3) for k, v in W0.items()})) for s in range(20)]).drop(columns='yrs').mean().to_dict()))
print(pd.DataFrame(rows).round(2).to_string())
# ızgara
G = []
navr = nav_ret(W0)
for win in [60, 120, 250, 500]:
    for thr in [0.5, 1.0, 1.5, 2.0]:
        G.append(dict(win=win, thr=thr, **quick(navr, win, thr)))
G = pd.DataFrame(G); G.to_csv(HERE + '/res_nav_grid.csv', index=False); print(G.round(2).to_string())
print('ızgara (16): OOS t>2 oranı', (G.OOS_t > 2).mean().round(2), 'OOS t aralığı', G.OOS_t.min().round(2), G.OOS_t.max().round(2), ' IS t aralığı', G.IS_t.min().round(2), G.IS_t.max().round(2))
# Plasebo 1: KCHOL'ün XU030'a göre kendi göreli z'si (REL)
rel = K['cc'] - bm * X['cc']
P1 = []
for win in [60, 250]:
    S = rel.fillna(0).cumsum(); z = zscore(S, win); pos = positions(z, 1.0)
    sim = simulate(pos, tg, ti, tc, lw, 'open', 8)
    P1.append(dict(sig=f'REL z{win}', **{f'{p}_t': summarize(sim, lo, hi)['t_all'] for p, lo, hi in [('IS', '2014-01-01', SPLIT), ('OOS', SPLIT, '2027-01-01')]}))
    # NAV ile aynı XU030-beta'lı sepet: NAV yerine XU030
    pos2, _ = signal(X['cc'], win, 1.0); sim = simulate(pos2, tg, ti, tc, lw, 'open', 8)
    P1.append(dict(sig=f'KCHOL vs XU030 cumsum(h-x) z{win}', **{f'{p}_t': summarize(sim, lo, hi)['t_all'] for p, lo, hi in [('IS', '2014-01-01', SPLIT), ('OOS', SPLIT, '2027-01-01')]}))
print(pd.DataFrame(P1).round(2).to_string())
# Plasebo 2: rastgele Koç dışı 8 hisselik sepet (aynı ağırlıklar), 300 çekiliş
NONKOC = ['AEFES','AKBNK','AKSEN','ALARK','ASELS','BIMAS','CIMSA','DOAS','DOHOL','EKGYO','ENJSA','ENKAI','EREGL','GARAN','GUBRF','HALKB','HEKTS','ISCTR','KRDMD','MGROS','PETKM','PGSUS','SAHOL','SASA','SISE','TAVHL','TCELL','THYAO','TKFEN','TSKB','TTKOM','ULKER','VAKBN','VESTL','SOKM','ODAS']
rng = np.random.default_rng(7); PL = []
wv = list(W0.values())
for b in range(300):
    names = list(rng.choice(NONKOC, 8, replace=False))
    o = quick(nav_ret(dict(zip(names, wv))))
    PL.append(dict(b=b, names=','.join(names), **o))
PL = pd.DataFrame(PL); PL.to_csv(HERE + '/res_nav_placebo_random.csv', index=False)
base = rows[0]
print('rastgele sepet plasebosu (300): IS t ort %.2f sd %.2f | OOS t ort %.2f sd %.2f | OOS t >= gerçek (%.2f) oranı %.3f | IS t >= gerçek (%.2f) oranı %.3f | ikisi birden %.3f' % (
    PL.IS_t.mean(), PL.IS_t.std(), PL.OOS_t.mean(), PL.OOS_t.std(), base['OOS_t'], (PL.OOS_t >= base['OOS_t']).mean(), base['IS_t'], (PL.IS_t >= base['IS_t']).mean(), ((PL.OOS_t >= base['OOS_t']) & (PL.IS_t >= base['IS_t'])).mean()))
print('kaynağın OOS t 2,98 değerini aşan plasebo oranı', (PL.OOS_t >= 2.98).mean().round(3))
