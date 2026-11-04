"""(g) KCHOL NAV iskontosu (uzlaşmadan), (h) Koza grubu (TRALT/TRMET/TRENJ) kapanıştan kapanışa.
(g) Girdi: out/code_y_grup/nav_KCHOL.parquet (D = log KCHOL − log NAV sepeti (TUPRS .33, YKBNK .24, FROTO .20, ARCLK .07, TOASO .04, AYGAZ .03, TTRAK .03, OTKAR .02),
    kümülatif; z250 = 250g z-skoru; dev60 = D − 60g ortalaması). Sinyal t kapanışında bilinir. İskonto genişse (z<−thr) KCHOL al, darsa sat.
    Hedef: KCHOL vadelisi, β·XU030 vadelisiyle hedge'li (uygulanabilir) ve NAV sepeti vadelileriyle hedge'li (bilgi amaçlı; 5 bacak).
(h) TRMET'in grup-içi artığı u = r_TRMET − β·ort(r_TRALT, r_TRENJ) (spot, 250g β). REV1/REV3 |z|>thr -> TRMET'te ters yön, TRALT vadelisiyle hedge'li
    ya da XU030 hedge'li. Ayrıca grup sinyali: ort(TRALT,TRENJ) artığı (TRMET'e göre) -> TRMET (önceki gün-içi bulgunun kapanıştan kapanışa versiyonu).
"""
from klib import *
C = ctx(); vcal = C['vcal']; scal = C['scal']; r_s = C['r']
F = C['F']; SF = C['SF']
out = []
# ---------- (g) KCHOL NAV ----------
nv = pd.read_parquet(S + '/out/code_y_grup/nav_KCHOL.parquet'); nv.index = pd.to_datetime(nv.index)
nv['zdev'] = nv['dev60'] / nv['dev60'].rolling(250, min_periods=120).std().shift(1)
W = {'TUPRS': .33, 'YKBNK': .24, 'FROTO': .20, 'ARCLK': .07, 'TOASO': .04}
wsum = sum(W.values())
for sig in ['z250', 'zdev']:
    for thr in [0.5, 1.0, 1.5]:
        z = nv[sig]; on = z.abs() > thr; dts = z.index[on.fillna(False)]
        for h in H:
            for inst in ['VIOP_xu', 'VIOP_nav', 'SPOT_xu']:
                cal = vcal if inst.startswith('VIOP') else scal
                ed = shift_date(dts, 0, cal); ok = ~pd.isna(ed); ed = ed[ok]; sd_ = -np.sign(z.loc[dts[ok]].values)
                if inst == 'VIOP_xu':
                    b = C['beta']['KCHOL'].reindex(ed, method='ffill').fillna(1).values
                    ret = sd_ * (F[f'f0_{h}']['KCHOL'].reindex(ed).values - b * F[f'f0_{h}']['XU030'].reindex(ed).values) / (1 + b)
                    legs = 1
                elif inst == 'VIOP_nav':
                    bn = nv['beta_nav'].reindex(ed, method='ffill').fillna(1).values
                    navf = sum(F[f'f0_{h}'][k].reindex(ed).values * w for k, w in W.items()) / wsum
                    ret = sd_ * (F[f'f0_{h}']['KCHOL'].reindex(ed).values - bn * navf) / (1 + bn)
                    legs = 1
                else:
                    b = C['beta']['KCHOL'].reindex(ed, method='ffill').fillna(1).values
                    ret = sd_ * (SF[h]['KCHOL'].reindex(ed).values - b * SF[h]['XU030'].reindex(ed).values) / (1 + b)
                    legs = 1
                tr = pd.DataFrame({'date': ed, 'ret': ret}).dropna()
                st = trade_stats(tr, 'ret', h=h, is_end=V_IS_END if inst.startswith('VIOP') else S_IS_END, legs=legs)
                newe = int((on & ~on.shift(1, fill_value=False)).sum()); st['new_entries_per_yr'] = round(newe / max((nv.index[-1] - nv.index[0]).days / 365.25, 1), 1)
                reg('g_kchol_nav', f'KCHOL NAV {sig}>{thr}', inst, 'E0', h, st, dict(sig=sig, thr=thr))
                out.append(f'KCHOL NAV {sig}>{thr} {inst:8s} h{h} {fmt(st)}')
# uzun ufuk (bilgi): spot, h=10/20
for sig in ['z250']:
    for thr in [1.0, 1.5]:
        z = nv[sig]; dts = z.index[(z.abs() > thr).fillna(False)]
        for h in [10, 20]:
            ed = shift_date(dts, 0, scal); ok = ~pd.isna(ed); ed = ed[ok]; sd_ = -np.sign(z.loc[dts[ok]].values)
            b = C['beta']['KCHOL'].reindex(ed, method='ffill').fillna(1).values
            ret = sd_ * (SF[h]['KCHOL'].reindex(ed).values - b * SF[h]['XU030'].reindex(ed).values) / (1 + b)
            tr = pd.DataFrame({'date': ed, 'ret': ret}).dropna(); st = trade_stats(tr, 'ret', h=h, is_end=S_IS_END)
            reg('g_kchol_nav', f'KCHOL NAV {sig}>{thr} uzun', 'SPOT_xu', 'E0', h, st, dict(sig=sig, thr=thr))
            out.append(f'KCHOL NAV {sig}>{thr} SPOT_xu  h{h} {fmt(st)}')
# ---------- (h) Koza grubu ----------
grp = r_s[['TRALT', 'TRENJ']].mean(axis=1)
def resid(y, x):
    b = (y.rolling(250, min_periods=120).cov(x) / x.rolling(250, min_periods=120).var()).shift(1).clip(0.2, 2.0)
    return y - b * x, b
u_met, b_met = resid(r_s['TRMET'], grp)            # TRMET'in gruba göre artığı
grp2 = r_s[['TRMET', 'TRENJ']].mean(axis=1)
u_alt, b_alt = resid(r_s['TRALT'], grp2)           # TRALT'ın gruba göre artığı
bTA = (r_s['TRMET'].rolling(250, min_periods=120).cov(r_s['TRALT']) / r_s['TRALT'].rolling(250, min_periods=120).var()).shift(1).clip(0.3, 2.0)
def zrev(u, k):
    sd = u.rolling(60, min_periods=40).std()
    return u.rolling(k, min_periods=k).sum() / (sd * np.sqrt(k))
for tgt, u in [('TRMET', u_met), ('TRALT', u_alt)]:
    for k in [1, 3]:
        z = zrev(u, k)
        for thr in [1.0, 1.5, 2.0]:
            on = z.abs() > thr; dts = z.index[on.fillna(False)]
            for h in H:
                for inst in ['VIOP_pair', 'VIOP_xu', 'SPOT_xu']:
                    for entry in (['E0', 'E2'] if inst.startswith('VIOP') else ['E0']):
                        cal = vcal if inst.startswith('VIOP') else scal
                        ed = shift_date(dts, 1 if entry == 'E2' else 0, cal); ok = ~pd.isna(ed); ed = ed[ok]; sd_ = -np.sign(z.loc[dts[ok]].values)
                        other = 'TRALT' if tgt == 'TRMET' else 'TRMET'
                        if inst == 'VIOP_pair':
                            bb = (bTA if tgt == 'TRMET' else 1 / bTA).reindex(ed, method='ffill').fillna(1).values
                            ret = sd_ * (F[f'f0_{h}'][tgt].reindex(ed).values - bb * F[f'f0_{h}'][other].reindex(ed).values) / (1 + bb)
                        elif inst == 'VIOP_xu':
                            b = C['beta'][tgt].reindex(ed, method='ffill').fillna(1).values
                            ret = sd_ * (F[f'f0_{h}'][tgt].reindex(ed).values - b * F[f'f0_{h}']['XU030'].reindex(ed).values) / (1 + b)
                        else:
                            b = C['beta'][tgt].reindex(ed, method='ffill').fillna(1).values
                            ret = sd_ * (SF[h][tgt].reindex(ed).values - b * SF[h]['XU030'].reindex(ed).values) / (1 + b)
                        tr = pd.DataFrame({'date': ed, 'ret': ret}).dropna()
                        st = trade_stats(tr, 'ret', h=h, is_end=V_IS_END if inst.startswith('VIOP') else S_IS_END)
                        reg('h_koza', f'{tgt} grup artığı REV{k}>{thr} (dönüş)', inst, entry, h, st, dict(k=k, thr=thr))
                        if entry == 'E0' and h in (1, 3): out.append(f'{tgt} grup artığı REV{k}>{thr} {inst:9s} {entry} h{h} {fmt(st)}')
for o in out: print(o)
D1 = save_registry('g_kchol_nav'); D2 = save_registry('h_koza'); print('test sayısı', len(D1), len(D2))
