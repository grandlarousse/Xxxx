"""Alternatif giriş zamanları (h1: 2023-11-30+, m5: son ~60 gün) ve FX'in seans/seans-sonrası ayrıştırması (h1 TRY=X 2024-01+).
Yahoo günlük 'o' = açılış müzayedesi (06:55-07:00 UTC). Sinyal (a) müzayede fiyatlarından sonra bilinir -> müzayede fiyatından
dolum İMKÂNSIZ; gerçekçi giriş 07:00 sonrası sürekli işlem. Burada 07:30 (h1 ilk bar kapanışı) ve 08:30 girişleri test edilir."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vlib as V, numpy as np, pandas as pd
pd.set_option('display.width', 250)
W = {'TUPRS': .33, 'FROTO': .20, 'YKBNK': .24, 'ARCLK': .07, 'TOASO': .04, 'AYGAZ': .03, 'OTKAR': .02, 'TTRAK': .03}


def hday(code):
    """günlük tablo: o (müzayede), p0730 (06:30 barı kapanışı), p0830, cc, intra, ve önceki kapanıştan 07:30'a getiri (temettü düzeltmeli)."""
    D = V.decomp(code)
    h = V.raw(code + '.IS', 'h1').copy(); h['d'] = h.index.tz_convert(None).normalize(); h['hm'] = h.index.strftime('%H:%M')
    p0730 = h[h.hm == '06:30'].set_index('d')['c']; p0830 = h[h.hm == '07:30'].set_index('d')['c']
    p1230 = h[h.hm == '11:30'].set_index('d')['c']
    T = pd.DataFrame({'p0730': p0730, 'p0830': p0830, 'p1230': p1230}).reindex(D.index)
    D = D.join(T)
    D['r_o_0730'] = np.log(D.p0730 / D.o); D['r_0730_c'] = np.log(D.c / D.p0730); D['r_0830_c'] = np.log(D.c / D.p0830)
    D['r_o_1230'] = np.log(D.p1230 / D.o); D['r_1230_c'] = np.log(D.c / D.p1230)
    D['r_pc_0730'] = D.cc - D.r_0730_c
    for k in ['r_o_0730', 'r_0730_c', 'r_0830_c', 'r_pc_0730', 'r_o_1230', 'r_1230_c']:
        D.loc[D.intra.isna(), k] = np.nan
    return D[D.index >= '2023-11-30']


def basket(Ds, col):
    G = pd.DataFrame({s: Ds[s][col] for s in W}); ws = pd.Series(W); M = G.notna().mul(ws, axis=1)
    return ((G.fillna(0) * ws).sum(axis=1) / M.sum(axis=1)).where(M.sum(axis=1) >= 0.6 * ws.sum())


def row(lab, y, x):
    c, t, n = V.corr_t(y, x)
    yr = V.by_year(y, x, 40)
    print(f'  {lab:62s} corr {c:+.3f} t {t:+.2f} n {n}  yıllar ' + ' '.join(f'{k}:{v:+.2f}' for k, v in yr.items()))
    return {'test': lab, 'c': c, 't': t, 'n': n}


rows = []
print('=== (a) KCHOL: aynı sinyal (müzayede bazlı), farklı giriş zamanları, 2023-11-30 .. 2026-10-30 ===')
K = hday('KCHOL'); Ds = {s: hday(s) for s in W}; X30 = V.decomp('XU030')
sig = basket(Ds, 'gap') - K['gap']
for lab, tgt in [('müzayede(o) -> kapanış [iddia, dolum imkânsız]', K['intra']), ('o -> 07:30 (ilk 30 dk)', K['r_o_0730']),
                 ('07:30 -> kapanış [gerçekçi giriş]', K['r_0730_c']), ('08:30 -> kapanış', K['r_0830_c']),
                 ('o -> 12:30', K['r_o_1230']), ('12:30 -> kapanış', K['r_1230_c'])]:
    rows.append(row('sig_open -> KCHOL ' + lab, tgt, sig))
sig730 = basket(Ds, 'r_pc_0730') - K['r_pc_0730']
rows.append(row('sig_0730 (07:30 itibarıyla NAV-KCHOL) -> KCHOL 07:30->kapanış', K['r_0730_c'], sig730))
print('  Backtest (z>0.5, geçmiş 250 gün; ilk 60 gün min) — pay vadelisi 8 / 15 bps; aynı pozisyonlar, farklı giriş:')
# z-skor için tam geçmiş (2014+) sinyali kullan ki 2023-11'de pencere dolu olsun
Kfull = V.decomp('KCHOL'); Dfull = {s: V.decomp(s) for s in W}
G = pd.DataFrame({s: Dfull[s]['gap'] for s in W}); ws = pd.Series(W); M = G.notna().mul(ws, axis=1)
navfull = ((G.fillna(0) * ws).sum(axis=1) / M.sum(axis=1)).where((M.sum(axis=1) >= 0.6) & G[['TUPRS', 'FROTO', 'YKBNK']].notna().all(axis=1))
pos = V.zpos(navfull - Kfull['gap'], 0.5)
for lab, tgt in [('o->c', K['intra']), ('07:30->c', K['r_0730_c']), ('08:30->c', K['r_0830_c'])]:
    for cost in [0, 8, 15]:
        o, _ = V.bt(pos.reindex(tgt.index), tgt, cost)
        a = o['ALL']
        if 'mean_bps' in a:
            print(f'    giriş {lab:9s} maliyet {cost:2d}: n={a["n"]} ort {a["mean_bps"]:+.1f} bps t={a["t"]:.2f} isabet {a["hit"]:.2f} | yıllar {o["by_year"]}')
            rows.append({'test': f'BT a giriş {lab} cost {cost}', 'n': a['n'], 'mean_bps': a['mean_bps'], 't': a['t']})

print('\n=== (b)/(c) ENKAI: TUR_{t-1}, USD_{t-1} -> farklı pencereler (2023-11-30+) ===')
E = hday('ENKAI'); TUR, _ = V.us_prev('TUR'); USD = V.fx_prev('TRY=X')
for nm, x, sg in [('TUR', TUR, -1), ('USD', USD, 1)]:
    for lab, tgt in [('o->c (intra)', E['intra']), ('o->07:30', E['r_o_0730']), ('07:30->c', E['r_0730_c']), ('gap', E['gap'])]:
        rows.append(row(f'{nm}_(t-1) -> ENKAI {lab}', tgt, x))

print('\n=== (c) USDTRY seans içi vs seans sonrası ayrıştırması (h1 TRY=X, 2024-01-15+) ===')
h = V.raw('TRY=X', 'h1'); px = pd.Series(h['c'].values, index=h.index + pd.Timedelta(hours=1)).sort_index()  # bar bitişi
def snap(days, hh):
    t = pd.DatetimeIndex(days).tz_localize('UTC') + pd.Timedelta(hours=hh)
    p = px.index.searchsorted(t, side='right') - 1
    v = np.where(p >= 0, px.values[np.clip(p, 0, None)], np.nan)
    age = t - px.index[np.clip(p, 0, None)]
    v[age > pd.Timedelta(hours=3)] = np.nan
    return pd.Series(v, index=days)
cal = V.bist_cal(); cal = cal[cal >= '2024-01-17']
prev = pd.Series(cal[:-1], index=cal[1:])
cal = cal[1:]
P00_t = snap(cal, 0); P00_p = snap(pd.DatetimeIndex(prev.values), 0).set_axis(cal)
P15_p = snap(pd.DatetimeIndex(prev.values), 15).set_axis(cal); P06_t = snap(cal, 6.5)
U_day = np.log(P00_t / P00_p)            # = günlük USD_{t-1} (kontrol)
U_sess = np.log(P15_p / P00_p)           # t-1 BIST seansı dahil 00:00-15:00 UTC (ENKAI t-1 kapanışında görüldü)
U_post = np.log(P00_t / P15_p)           # t-1 15:00 -> t 00:00 (BIST kapandıktan sonra)
U_pre = np.log(P06_t / P15_p)            # t-1 15:00 -> t 06:30 (açılıştan hemen önce bilinen tüm seans-sonrası)
print('  kontrol: corr(h1 U_day, günlük USD_{t-1}) =', round(pd.concat([U_day, USD], axis=1).dropna().corr().iloc[0, 1], 3))
Ef = V.decomp('ENKAI')
for lab, x in [('U_day (00-00)', U_day), ('U_sess (t-1 00:00-15:00)', U_sess), ('U_post (t-1 15:00 - t 00:00)', U_post), ('U_pre (t-1 15:00 - t 06:30)', U_pre)]:
    rows.append(row(f'{lab} -> ENKAI intra_t', Ef['intra'], x))
    rows.append(row(f'{lab} -> ENKAI gap_t', Ef['gap'], x))
    rows.append(row(f'{lab} -> ENKAI cc_(t-1)', Ef['cc'].shift(1), x))
r = V.ols(Ef['intra'], [U_sess, U_post], names=['sess', 'post'])
print(f"  Eintra ~ U_sess + U_post: sess {r['b']['sess']:+.3f} (t {r['t']['sess']:+.2f}), post {r['b']['post']:+.3f} (t {r['t']['post']:+.2f}), n={r['n']}")

print('\n=== m5 (son ~60 gün): KCHOL sig_open -> giriş 07:05 / 07:15 / 07:30 ===')
def m5day(code):
    m = V.raw(code + '.IS', 'm5').copy(); m['d'] = m.index.tz_convert(None).normalize(); m['hm'] = m.index.strftime('%H:%M')
    return pd.DataFrame({k: m[m.hm == hm].set_index('d')['c'] for k, hm in [('p0705', '07:00'), ('p0715', '07:10'), ('p0730', '07:25')]})
Km = m5day('KCHOL').join(V.decomp('KCHOL')[['c', 'o', 'intra']], how='left')
sgm = sig.reindex(Km.index)
for k in ['p0705', 'p0715', 'p0730']:
    y = np.log(Km.c / Km[k]); c, t, n = V.corr_t(y, sgm)
    print(f'  giriş {k}: corr {c:+.3f} t {t:+.2f} n {n}')
c, t, n = V.corr_t(Km['intra'], sgm); print(f'  müzayede girişi: corr {c:+.3f} t {t:+.2f} n {n}')
pd.DataFrame(rows).to_csv(os.path.join(V.CODE, 'res_hourly.csv'), index=False)
