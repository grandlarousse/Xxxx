"""Ek sağlamlık: (1) NAV için alternatif ağırlıklar (eşit, ilk-3, kayan regresyon - look-ahead yok)
(2) 2023-11+ ilk 30 dk ayrıştırması (NAVgap vs Kgap)  (3) TUR alternatif hiza (iddia tarzı <= t_prev) ve TKC
(4) (b)/(c) eşik ızgarası ve en büyük katkı günleri."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vlib as V, numpy as np, pandas as pd
pd.set_option('display.width', 250)
W = {'TUPRS': .33, 'FROTO': .20, 'YKBNK': .24, 'ARCLK': .07, 'TOASO': .04, 'AYGAZ': .03, 'OTKAR': .02, 'TTRAK': .03}
K = V.decomp('KCHOL'); D = {s: V.decomp(s) for s in W}


def bgap(w):
    G = pd.DataFrame({s: D[s]['gap'] for s in w}); ws = pd.Series(w); M = G.notna().mul(ws, axis=1)
    return ((G.fillna(0) * ws).sum(axis=1) / M.sum(axis=1)).where(M.sum(axis=1) >= 0.6 * ws.sum())


def rollw(win=250, step=21):
    """KCHOL cc ~ iştirak cc (geçmiş 250 gün, aylık yeniden tahmin); ağırlıklar yalnız t'den önceki veriyle."""
    Y = K['cc']; X = pd.DataFrame({s: D[s]['cc'] for s in W})
    df = pd.concat([Y.rename('y'), X], axis=1).loc['2012':]
    idx = df.index; Wt = {}
    for i in range(win, len(idx), step):
        g = df.iloc[i - win:i].dropna()
        if len(g) < 150: continue
        b = np.linalg.lstsq(np.column_stack([np.ones(len(g)), g[list(W)].values]), g['y'].values, rcond=None)[0][1:]
        Wt[idx[i]] = pd.Series(b, index=list(W))
    Wd = pd.DataFrame(Wt).T.reindex(idx).ffill()
    G = pd.DataFrame({s: D[s]['gap'] for s in W}).reindex(idx)
    return (G.fillna(0) * Wd).sum(axis=1).where(G[['TUPRS', 'FROTO', 'YKBNK']].notna().all(axis=1) & Wd.notna().all(axis=1)) / Wd.sum(axis=1)


print('=== (1) NAV ağırlık alternatifleri: sig -> KCHOL intra; ve Kintra ~ Bgap + Kgap; BT z>0.5 8 bps ===')
for lab, bg in [('iddia ağırlıkları', bgap(W)), ('eşit ağırlık (8)', bgap({s: 1 for s in W})), ('ilk-3 (TUPRS,FROTO,YKBNK eşit)', bgap({'TUPRS': 1, 'FROTO': 1, 'YKBNK': 1})),
                ('kayan regresyon ağırlığı (look-ahead yok)', rollw())]:
    s = bg - K['gap']
    c, t, n = V.corr_t(K['intra'], s); _, ti, _ = V.corr_t(K['intra'], s, V.IS0, V.SPLIT); _, to, _ = V.corr_t(K['intra'], s, V.SPLIT)
    r = V.ols(K['intra'], [bg, K['gap']], names=['B', 'K'])
    o, _ = V.bt(V.zpos(s, 0.5), K['intra'], 8)
    print(f"  {lab:42s} corr {c:+.3f} t {t:+.2f} (IS {ti:+.2f}, OOS {to:+.2f}) | Bgap {r['b']['B']:+.3f} (t {r['t']['B']:+.2f}) Kgap {r['b']['K']:+.3f} | BT8 IS {o['IS']['mean_bps']:+.1f} OOS {o['OOS']['mean_bps']:+.1f} (t {o['OOS']['t']:.2f})")

print('\n=== (2) 2023-11+ : KCHOL o->07:30 ve 07:30->kapanış ~ NAVgap + Kgap ===')
h = V.raw('KCHOL.IS', 'h1').copy(); h['d'] = h.index.tz_convert(None).normalize()
p0730 = h[h.index.strftime('%H:%M') == '06:30'].set_index('d')['c'].reindex(K.index)
a = np.log(p0730 / K['o']); b = np.log(K['c'] / p0730)
nav = bgap(W)
for lab, y in [('o->07:30', a), ('07:30->c', b), ('o->c', K['intra'])]:
    y = y[y.index >= '2023-11-30']
    r = V.ols(y, [nav, K['gap']], names=['NAVgap', 'Kgap'])
    print(f"  {lab:9s} n={r['n']} NAVgap {r['b']['NAVgap']:+.3f} (t {r['t']['NAVgap']:+.2f})  Kgap {r['b']['Kgap']:+.3f} (t {r['t']['Kgap']:+.2f})")

print('\n=== (3) TUR hiza alternatifleri -> ENKAI intra ===')
E = V.decomp('ENKAI'); cal = V.bist_cal()
for sym in ['TUR', 'TKC']:
    d = V.raw(sym); p = d['adj'].astype(float)
    # iddia tarzı: BIST takvimine 'yerel tarih <= t' ffill, getiri, shift(1)
    s = p.reindex(p.index.union(cal)).ffill().reindex(cal); r_cl = np.log(s).diff().shift(1)
    r_me, _ = V.us_prev(sym)
    for lab, x in [('<= t_prev (iddia tarzı)', r_cl), ('< t (bu çalışma)', r_me)]:
        c, t, n = V.corr_t(E['intra'], x); _, ti, _ = V.corr_t(E['intra'], x, V.IS0, V.SPLIT); _, to, _ = V.corr_t(E['intra'], x, V.SPLIT)
        print(f'  {sym} {lab:24s} corr {c:+.3f} t {t:+.2f} IS {ti:+.2f} OOS {to:+.2f} n {n}')

print('\n=== (4) Eşik ızgarası (8 bps) ve en büyük katkılar ===')
TUR, _ = V.us_prev('TUR'); USD = V.fx_prev('TRY=X')
for nm, sig in [('-TUR', -TUR), ('USD', USD)]:
    for thr in [0.5, 1.0, 1.5, 2.0, 2.5]:
        o, pnl = V.bt(V.zpos(sig, thr), E['intra'], 8)
        f = lambda k: f"{o[k]['mean_bps']:+6.1f} (t {o[k]['t']:+.2f}, n {o[k]['n']})" if 'mean_bps' in o[k] else f"n {o[k]['n']}"
        print(f'  {nm:5s} z>{thr}: IS {f("IS")} | OOS {f("OOS")}')
    o, pnl = V.bt(V.zpos(sig, 1.0), E['intra'], 8)
    pnl = pnl[pnl.index >= V.SPLIT]
    act = pnl[V.zpos(sig, 1.0).reindex(pnl.index) != 0]
    top = act.abs().sort_values(ascending=False).head(10).index
    print(f'  {nm} z>1 OOS en büyük 10 |pnl| günü (bps):', {str(k.date()): round(1e4 * act[k], 0) for k in top})
    print(f'  {nm} z>1 OOS toplam {1e4 * act.sum():+.0f} bps; bu 10 gün hariç toplam {1e4 * act.drop(top).sum():+.0f} bps; n={len(act)}')
