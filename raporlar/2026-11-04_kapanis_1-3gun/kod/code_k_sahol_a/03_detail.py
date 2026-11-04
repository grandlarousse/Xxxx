"""3) Önerilen kuralların ayrıntısı: olay profili (giriş sonrası gün gün), tutma dağılımı, yıllara göre, stop, eşik/pencere duyarlılığı,
hedge/kontrat oranı (β, eşit TL, tam sayı kontrat), 1 kontrat çifti TL, ardışık kayıp, devir sayısı, likidite. IS = spot vekili 2014–20, OOS = VİOP 2021–26."""
import sys; sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_k_sahol_a')
import kl, numpy as np, pandas as pd
import importlib.util
spec = importlib.util.spec_from_file_location('c2', kl.HERE + '/02_c2c.py'); c2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)
K, FA, FB = c2.K, c2.FA[1], c2.FB[1]
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 300)
RULES = {'A_bant_ici': dict(exit_z=1.5), 'z<1': dict(exit_z=1.0), 'B_z<0,5': dict(exit_z=0.5), 'B2_z<0,5|max20': dict(exit_z=0.5, maxN=20)}
IS = ('2014-01-01', '2021-01-01'); OOS = ('2021-01-01', '2027-01-01')
def both(c=8, **kw):
    """IS spot + OOS VİOP birleşik: iki ayrı koşum, dönemlerine göre birleştirilir."""
    Ds, Ts = kl.run_rule(*c2.spot_inputs(c)[:6], roll=None, **kw)
    z, ra, rb, beta, cA, cB, rl = c2.fut_inputs(c, 1)
    if 'beta_override' in kw: pass
    Df, Tf = kl.run_rule(z, ra, rb, beta, cA, cB, roll=rl, **kw)
    return Ds, Ts, Df, Tf
def fmt(s): return {k: (round(v, 2) if isinstance(v, float) else v) for k, v in s.items()}
out = []
print('=== Kural özetleri (8 bps + tik; IS spot / OOS VİOP) ===')
RES = {}
for nm, kw in RULES.items():
    for c in [8, 15, 30]:
        Ds, Ts, Df, Tf = both(c, **kw); RES[(nm, c)] = (Ds, Ts, Df, Tf)
        si, so = kl.summ(Ds, Ts, *IS), kl.summ(Df, Tf, *OOS)
        out.append(dict(rule=nm, cost=c, per='IS spot', **si)); out.append(dict(rule=nm, cost=c, per='OOS VIOP', **so))
O = pd.DataFrame(out); O.to_csv(kl.HERE + '/res_rules.csv', index=False)
print(O[['rule', 'cost', 'per', 'n', 'per_yr', 'hold_mean', 'hold_med', 'gross_bps', 'net_bps', 'med_bps', 'hit', 't_trade', 't_daily', 'ann_bps', 'sh', 'mdd_bps', 'worst_bps', 'p5_bps', 'max_lstreak', 'frac_exp']].round(2).to_string())
# tutma dağılımı
print('\n=== Tutma süresi dağılımı (iş günü), OOS VİOP 8 bps ===')
for nm in RULES:
    T = RES[(nm, 8)][3]; T = T[(T.entry_date >= OOS[0]) & ~T.open]
    print(nm, T.days.quantile([.1, .25, .5, .75, .9, 1]).to_dict(), ' çıkış nedeni:', T.why.value_counts().to_dict(), ' devirli işlem payı:', round((T.nroll > 0).mean(), 2))
# olay profili: giriş sonrası h gün kümülatif BRÜT spread getirisi (giriş = sinyal günü uzlaşması/kapanışı)
print('\n=== Olay profili: bölüm başlangıcında giriş, h gün sonra kümülatif brüt getiri (bps), ort (t) ===')
def profile(z, ra, rb, beta, lo, hi, H=(1, 2, 3, 4, 5, 7, 10, 15, 20)):
    zz = z.values; ep = np.where(np.abs(zz) > 1.5, np.sign(zz), 0.0); ep[np.isnan(zz)] = 0
    st = np.where((ep != 0) & (np.r_[0, ep[:-1]] != ep))[0]
    st = [i for i in st if lo <= z.index[i] < hi]
    a = np.nan_to_num(ra.values); b_ = np.nan_to_num(rb.values); bb = beta.ffill().values
    res = {}
    for h in H:
        x = np.array([-ep[i] * (a[i + 1:i + 1 + h].sum() - bb[i] * b_[i + 1:i + 1 + h].sum()) for i in st if i + h < len(zz)])
        res[h] = f'{1e4 * x.mean():.0f} ({x.mean() / x.std() * np.sqrt(len(x)):.1f})'
    # ayrıca: gün gün marjinal
    return len(st), res
n1, p1 = profile(K.z, K.rA, K.rB, K.beta, pd.Timestamp(IS[0]), pd.Timestamp(IS[1]))
z, ra, rb, beta, cA, cB, rl = c2.fut_inputs(8, 1)
n2, p2 = profile(z, ra, rb, beta, pd.Timestamp(OOS[0]), pd.Timestamp(OOS[1]))
n3, p3 = profile(K.z, K.rA, K.rB, K.beta, pd.Timestamp(OOS[0]), pd.Timestamp(OOS[1]))
print(pd.DataFrame({f'IS spot (n={n1})': p1, f'OOS VİOP (n={n2})': p2, f'OOS spot (n={n3})': p3}).T.to_string())
# yıllara göre
print('\n=== Yıllara göre (8 bps + tik; 2014–20 spot, 2021+ VİOP): işlem, net bps ort., yıl toplamı bps, isabet ===')
for nm in ['A_bant_ici', 'B_z<0,5']:
    Ds, Ts, Df, Tf = RES[(nm, 8)]
    T = pd.concat([Ts[Ts.entry_date < OOS[0]], Tf[Tf.entry_date >= OOS[0]]]); T = T[~T.open & (T.entry_date >= IS[0])]
    D = pd.concat([Ds[(Ds.index >= IS[0]) & (Ds.index < OOS[0])], Df[Df.index >= OOS[0]]])
    y = T.groupby(T.entry_date.dt.year).agg(n=('net', 'size'), ort_bps=('net', lambda x: 1e4 * x.mean()), isabet=('net', lambda x: (x > 0).mean()), en_kotu=('net', lambda x: 1e4 * x.min()))
    y['yil_toplam_bps'] = 1e4 * D.net.groupby(D.index.year).sum()
    print(nm); print(y.round(1).T.to_string())
# stop
print('\n=== Stop (kümülatif brüt spread kaybı) — 8 bps + tik: net bps (t_işlem) IS / OOS ===')
for nm in ['A_bant_ici', 'B_z<0,5']:
    row = {}
    for stp in [None, 0.03, 0.05, 0.08]:
        Ds, Ts, Df, Tf = both(8, stop=stp, **RULES[nm]); si, so = kl.summ(Ds, Ts, *IS), kl.summ(Df, Tf, *OOS)
        row[str(stp)] = f"IS {si['net_bps']:.0f} ({si['t_trade']:.2f}) worst {si['worst_bps']:.0f} | OOS {so['net_bps']:.0f} ({so['t_trade']:.2f}) worst {so['worst_bps']:.0f} mdd {so['mdd_bps']:.0f}"
    print(nm); [print('  stop', k, v) for k, v in row.items()]
# eşik/pencere duyarlılığı (OOS VİOP ve IS spot, 8 bps + tik)
print('\n=== Eşik × pencere duyarlılığı: t_işlem IS spot / OOS VİOP ===')
rows = []
for win in [40, 60, 90]:
    Kw = kl.signal(win=win)
    for thr in [1.25, 1.5, 1.75, 2.0]:
        for nm, ex in [('A', thr), ('B', 0.5)]:
            idx = Kw.index; cs = c2.spot_inputs(8)
            Ds, Ts = kl.run_rule(Kw.z, Kw.rA, Kw.rB, Kw.beta, cs[4], cs[5], thr=thr, exit_z=ex)
            zf = Kw.z.reindex(z.index)
            Df, Tf = kl.run_rule(zf, ra, rb, Kw.beta.reindex(z.index), cA, cB, roll=rl, thr=thr, exit_z=ex)
            si, so = kl.summ(Ds, Ts, *IS), kl.summ(Df, Tf, *OOS)
            rows.append(dict(win=win, thr=thr, rule=nm, IS_t=si.get('t_trade'), IS_bps=si.get('net_bps'), OOS_t=so.get('t_trade'), OOS_bps=so.get('net_bps'), OOS_n=so.get('n'), OOS_tday=so.get('t_daily')))
W = pd.DataFrame(rows); W.to_csv(kl.HERE + '/res_sens.csv', index=False)
print(W.pivot_table(index=['rule', 'win'], columns='thr', values=['IS_t', 'OOS_t']).round(2).to_string())
print(W.pivot_table(index=['rule', 'win'], columns='thr', values=['OOS_bps']).round(0).to_string())
# hedge / kontrat oranı
print('\n=== Hedge/kontrat oranı (OOS VİOP 8 bps + tik): net bps (t_işlem), günlük spread vol (bps) ===')
FAF = FA.F.reindex(z.index).ffill(); FBF = FB.F.reindex(z.index).ffill()
variants = {'β250 (sürekli)': beta, 'eşit TL (β=1)': pd.Series(1.0, index=z.index)}
for NA in [1, 3, 10, 30]:
    nb = (NA * beta * FAF / FBF).round().clip(lower=1)
    variants[f'tam sayı N_A={NA}'] = nb / NA * FBF / FAF
for vn, bv in variants.items():
    for nm in ['A_bant_ici', 'B_z<0,5']:
        Df, Tf = kl.run_rule(z, ra, rb, bv, cA, cB, roll=rl, **RULES[nm]); so = kl.summ(Df, Tf, *OOS)
        vol = 1e4 * Df.gross[Df.pos.shift(1).fillna(0) != 0].std()
        print(f'  {vn:22s} {nm:12s} {so["net_bps"]:6.1f} ({so["t_trade"]:.2f})  günlük vol {vol:.0f}  worst {so["worst_bps"]:.0f}')
# 1 kontrat çifti TL: N_A=1, N_B=round(β F_A/F_B); TL = side*100*(ΣdF_A − N_B ΣdF_B) − maliyet
print('\n=== 1 kontrat çifti (1 SAHOL + N_B AKBNK) TL, OOS VİOP, 8 bps + 1 tik ===')
dFA = FA.dF.reindex(z.index).fillna(0).values; dFB = FB.dF.reindex(z.index).fillna(0).values; rlv = rl.values
for nm in ['A_bant_ici', 'B_z<0,5']:
    Df, Tf = kl.run_rule(z, ra, rb, beta, cA, cB, roll=rl, **RULES[nm]); Tf = Tf[(Tf.entry_date >= OOS[0]) & ~Tf.open].copy()
    tl = []
    for _, t in Tf.iterrows():
        i0, i1 = int(t.entry), int(t.exit); fa0, fb0 = FAF.iloc[i0], FBF.iloc[i0]; nb = max(1, round(t.beta * fa0 / fb0))
        g = t.side * 100 * (dFA[i0 + 1:i1 + 1].sum() - nb * dFB[i0 + 1:i1 + 1].sum())
        side_cost = lambda fa, fb: 8e-4 / 2 * 100 * (fa + nb * fb) + 0.5 * 0.01 * 100 * (1 + nb)
        cst = side_cost(fa0, fb0) + side_cost(FAF.iloc[i1], FBF.iloc[i1]) + 2 * side_cost(FAF.iloc[i0], FBF.iloc[i0]) * rlv[i0 + 1:i1 + 1].sum()
        tl.append(dict(year=t.entry_date.year, nb=nb, tl_net=g - cst, notionalA=100 * fa0))
    TL = pd.DataFrame(tl)
    print(nm, 'işlem başı net TL ort.:', round(TL.tl_net.mean(), 1), ' medyan', round(TL.tl_net.median(), 1), ' N_B dağılımı', TL.nb.value_counts().to_dict())
    print('   yıllara göre (TL/işlem ort., yıl toplamı):', TL.groupby('year').tl_net.agg(['mean', 'sum']).round(0).to_dict('index'))
# likidite: pozisyon günlerinde tutulan sözleşmenin günlük işlem değeri
v = FA.value_tl.reindex(z.index); w = FB.value_tl.reindex(z.index)
Df = RES[('A_bant_ici', 8)][2]; m = (Df.pos != 0) & (Df.index >= '2025-01-01')
print('\nlikidite 2025+: pozisyon günlerinde tutulan sözleşme günlük işlem değeri medyan (mn TL) SAHOL', round(v[m].median() / 1e6), ' AKBNK', round(w[m].median() / 1e6))
