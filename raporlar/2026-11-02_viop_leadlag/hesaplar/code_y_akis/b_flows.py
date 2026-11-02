"""2) TCMB haftalık menkul kıymet istatistikleri: yurt dışı yerleşiklerin hisse senedi net alımı (milyon $, fiyat/kur etkisinden arındırılmış).
Kaynak: EVDS3 (evds3.tcmb.gov.tr, halka açık web arayüzünün /igmevdsms-dis/fe uç noktası) seriler TP.PYUK3 (arşiv 2005-01..2021-08) +
TP.MKNETHAR.M7 (2020-09..), stok TP.PYUK1 / TP.MKNETHAR.M1; örtüşen 48 haftada corr 0,99999. Kayıt: data/akis/tcmb_foreign_equity_weekly.csv
Zamanlama: hafta w = Pzt..Cuma (Cuma tarihli). Yayın = izleyen Perşembe 14:30 TSİ (11:30 UTC) -> D_w = Cuma_w + 6 gün (tatilse sonraki iş günü).
Testler: senkron (akış_w ~ getiri_w), ters (getiri_{w-k} -> akış_w), öncülük (akış_w -> yayın SONRASI getiri: D_w kapanış -> D_w+5 iş günü kapanış),
yayın öncesi (akış_w -> hafta w+1 Pzt..Çar, işlenemez), 47 hisse kesiti, backtest.
"""
import numpy as np, pandas as pd, alib, json
from alib import ll
F = pd.read_csv(alib.SCR + '/data/akis/tcmb_foreign_equity_weekly.csv', parse_dates=['date']).set_index('date')
F['fz'] = F.flow_eq_musd / F.flow_eq_musd.rolling(52, min_periods=26).std().shift(1)  # geçmiş 52h std ile ölçek (look-ahead yok)
F['fs'] = F.flow_eq_musd / F.stock_eq_musd.shift(1) * 100  # stok yüzdesi
cal = ll.bist_cal(); cal = cal[cal >= '2005-01-01']
r_tl = ll.ret('XU100'); r_usd = ll.bist_usd('XU100'); r30 = ll.ret('XU030'); rbank = ll.ret('XBANK')
def wsum(r, a, b):  # (a, b] aralığı toplam log getiri
    s = r[(r.index > a) & (r.index <= b)]; return s.sum() if len(s) else np.nan
def nth_after(d, n):  # d'den sonraki n'inci BIST günü (d dahil değil)
    i = cal.searchsorted(d, side='right') + n - 1
    return cal[i] if i < len(cal) else pd.NaT
rows = []
for fri in F.index:
    D = cal[cal.searchsorted(fri + pd.Timedelta(days=6), side='left')] if cal.searchsorted(fri + pd.Timedelta(days=6)) < len(cal) else pd.NaT
    prev_fri = fri - pd.Timedelta(days=7)
    r = dict(fri=fri, D=D)
    for nm, ser in [('usd', r_usd), ('tl', r_tl), ('x30', r30), ('bank', rbank)]:
        r[nm + '_w'] = wsum(ser, prev_fri, fri)
        r[nm + '_wm1'] = wsum(ser, prev_fri - pd.Timedelta(days=7), prev_fri)
        if pd.notna(D):
            r[nm + '_pre'] = wsum(ser, fri, cal[cal.searchsorted(D) - 1])  # hafta w+1 Pzt..yayın öncesi gün (işlenemez)
            r[nm + '_D'] = ser.get(D, np.nan)  # yayın günü tamamı (14:30 öncesi kısmı işlenemez)
            e5 = nth_after(D, 5); e20 = nth_after(D, 20)
            r[nm + '_post5'] = wsum(ser, D, e5) if pd.notna(e5) else np.nan
            r[nm + '_post20'] = wsum(ser, D, e20) if pd.notna(e20) else np.nan
    rows.append(r)
W = pd.DataFrame(rows).set_index('fri').join(F)
W.to_csv('res_flow_weekly.csv')
res = {}
def reg(y, xs, dfm):
    import statsmodels.api as sm
    d = dfm[[y] + xs].dropna()
    m = sm.OLS(d[y], sm.add_constant(d[xs])).fit(cov_type='HAC', cov_kwds={'maxlags': 4})
    return {x: (round(m.params[x], 5), round(m.tvalues[x], 2)) for x in xs} | {'n': len(d), 'r2': round(m.rsquared, 3)}
out = []
for per, a, b in [('ALL', '2005', '2026-12'), ('IS_05_20', '2005', '2020-12'), ('OOS_21_26', '2021', '2026-12'), ('last3y', '2023-10', '2026-12')]:
    d = W.loc[a:b]
    o = {'per': per, 'n': len(d)}
    o['corr_sync_usd'] = d[['fz', 'usd_w']].corr().iloc[0, 1]
    o['corr_rev_usd_wm1'] = d[['fz', 'usd_wm1']].corr().iloc[0, 1]   # geçen haftanın getirisi -> bu hafta akış
    o['corr_pre_usd'] = d[['fz', 'usd_pre']].corr().iloc[0, 1]       # akış -> sonraki hafta yayın öncesi (işlenemez)
    o['corr_post5_usd'] = d[['fz', 'usd_post5']].corr().iloc[0, 1]   # akış -> yayın sonrası 5 gün
    o['corr_post5_x30'] = d[['fz', 'x30_post5']].corr().iloc[0, 1]
    o['corr_post20_usd'] = d[['fz', 'usd_post20']].corr().iloc[0, 1]
    o['flow_ac1'] = d.fz.autocorr(1)
    rr = reg('usd_post5', ['fz', 'usd_w', 'usd_pre'], d); o['b_post5_fz'], o['t_post5_fz'] = rr['fz']; o['t_post5_usdw'] = rr['usd_w'][1]
    rr = reg('fz', ['usd_wm1'], d.assign(fzn=d.fz)); o['t_rev'] = rr['usd_wm1'][1]
    rr = reg('fz', ['usd_w'], d); o['t_sync'] = rr['usd_w'][1]
    out.append(o)
S = pd.DataFrame(out).round(3); print(S.to_string()); S.to_csv('res_flow_summary.csv', index=False)
# yıllara göre
yr = W.groupby(W.index.year).apply(lambda d: pd.Series({'sync': d[['fz', 'usd_w']].corr().iloc[0, 1], 'rev': d[['fz', 'usd_wm1']].corr().iloc[0, 1], 'post5': d[['fz', 'usd_post5']].corr().iloc[0, 1], 'pre': d[['fz', 'usd_pre']].corr().iloc[0, 1]}))
print(yr.round(2).T.to_string())
yr.to_csv('res_flow_byyear.csv')
# Yayın günü tepkisi (saatlik, 2023-11+): XU030 11:30->15:10 UTC getirisi vs fz
try:
    h = ll.intraday('XU030.IS'); h = h.copy(); h['d'] = h.index.tz_convert(None).normalize()
    p1130 = ll.snap_daily('XU030.IS', '11:30'); p1500 = ll.snap_daily('XU030.IS', '15:15')
    rD = np.log(p1500 / p1130)
    W2 = W.dropna(subset=['D']).copy(); W2['rD_after'] = rD.reindex(W2.D).values
    d = W2.dropna(subset=['rD_after', 'fz'])
    print('Yayın günü 11:30->kapanış XU030: corr(fz)=%.3f n=%d' % (d[['fz', 'rD_after']].corr().iloc[0, 1], len(d)))
    res['release_day_corr'] = float(d[['fz', 'rD_after']].corr().iloc[0, 1]); res['release_day_n'] = len(d)
except Exception as e: print('h1 hata', e)
# 47 hisse kesiti: akış_w -> hisse post5 (XU100 TL'ye göre fazla getiri) ve senkron kısmi
rows = []
for s in alib.VIOP:
    try: rs = ll.ret(s)
    except Exception: continue
    ex = rs - r_tl
    a5, sw, pre = [], [], []
    for fri, w in W.iterrows():
        if pd.isna(w.D): a5.append(np.nan); sw.append(np.nan); continue
        e5 = nth_after(w.D, 5)
        a5.append(wsum(ex, w.D, e5) if pd.notna(e5) else np.nan); sw.append(wsum(ex, fri - pd.Timedelta(days=7), fri))
    d = W[['fz']].assign(post5x=a5, syncx=sw).dropna()
    d = d[d.index >= '2010-01-01']
    _, t5, n = ll.nw_t((d.post5x - d.post5x.mean()) / d.post5x.std(), (d.fz - d.fz.mean()) / d.fz.std(), lags=4)
    _, ts, _ = ll.nw_t((d.syncx - d.syncx.mean()) / d.syncx.std(), (d.fz - d.fz.mean()) / d.fz.std(), lags=4)
    dis, doo = d[d.index < '2021'], d[d.index >= '2021']
    rows.append(dict(stock=s, corr_sync_x=d[['fz', 'syncx']].corr().iloc[0, 1], t_sync=ts, corr_post5_x=d[['fz', 'post5x']].corr().iloc[0, 1], t_post5=t5, n=n,
                     c_is=dis[['fz', 'post5x']].corr().iloc[0, 1], c_oos=doo[['fz', 'post5x']].corr().iloc[0, 1]))
X = pd.DataFrame(rows); X['p5'] = ll.t_to_p(X.t_post5); X['ps'] = ll.t_to_p(X.t_sync)
X['fdr_post5'], _ = ll.fdr(X.p5.values); X['fdr_sync'], _ = ll.fdr(X.ps.values)
X = X.sort_values('corr_sync_x'); print(X.round(3).to_string()); X.to_csv('res_flow_xsec.csv', index=False)
# Backtest: sign(fz) -> XU030 D kapanış -> D+5 kapanış (VİOP F_XU030 ile işlenebilir; yayın 14:30, kapanış 18:10)
bt = {}
d = W.dropna(subset=['fz', 'x30_post5']).copy()
for thr in [0.0, 0.5, 1.0]:
    for cost in [8, 15]:
        sig = d.fz.where(d.fz.abs() > thr, 0); pos = np.sign(sig)
        pnl = pos * d.x30_post5 - cost / 1e4 * pos.abs()
        for per, a, b in [('ALL', '2005', '2027'), ('IS', '2005', '2020-12'), ('OOS', '2021', '2027')]:
            p = pnl.loc[a:b]; ps = pos.loc[a:b]; act = p[ps != 0]
            m, t, n = alib.nw(act, 4) if len(act) > 30 else (np.nan, np.nan, len(act))
            bt[f'thr{thr}_c{cost}_{per}'] = dict(n=int((ps != 0).sum()), mean_bps=round(1e4 * act.mean(), 1), t=round(t, 2) if t == t else None,
                                                 hit=round((act > 0).mean(), 3), sharpe_ann=round(act.mean() / act.std() * np.sqrt(52) * np.sqrt((ps != 0).mean()), 2) if len(act) > 5 else None)
# kontrarian versiyon (işaret ters) sadece raporlamak için zaten simetrik: mean_bps işareti
for k, v in bt.items(): print(k, v)
res['bt'] = bt
json.dump(res, open('res_flow_bt.json', 'w'), indent=1, default=str)
