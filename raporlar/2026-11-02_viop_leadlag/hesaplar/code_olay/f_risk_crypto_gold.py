"""TR risk primi proxy'leri, kripto (hafta sonu), XAUTRY. Kısa."""
from olib import *
cc, gp, it = comp('cc'), comp('gap'), comp('intra')
X = cc['XU100']; res = []
def pc(a, b): return ll.partial_corr(a, b, [X])[0]
# sanity: ES gün-içi (06:00->15:00 UTC) vs XU030 gün-içi
e6, e15 = ll.snap_daily('ES=F', '07:00'), ll.snap_daily('ES=F', '15:00')
esi = np.log(e15 / e6); print('sanity corr(ES 07-15UTC, XU030 intra)', round(pd.concat([esi, it['XU030']], axis=1).dropna().corr().iloc[0, 1], 3))
# ---- 1) Risk primi proxy'leri: EMB-IEF (EM kredi spreadi), TRY=X (ll düzeltilmiş), CEW, TUR-EEM
P = {'EMB-IEF': ll.ret('EMB') - ll.ret('IEF'), 'TRY=X': ll.ret('TRY=X'), 'TUR-EEM': ll.ret('TUR') - ll.ret('EEM'), 'CEW': ll.ret('CEW')}
P = {k: v.reindex(cc.index) for k, v in P.items()}
for k, v in P.items():
    for s in VIOP + ['XBANK', 'XU100']:
        y = cc[s]; m3 = y.index >= y.index[-1] - pd.DateOffset(years=3)
        dfi = pd.concat([y, v], axis=1).dropna()
        res.append(dict(stock=s, proxy=k, corr_full=dfi.corr().iloc[0, 1], corr_3y=dfi[dfi.index >= dfi.index[-1] - pd.DateOffset(years=3)].corr().iloc[0, 1],
                        corr_1y=dfi[dfi.index >= dfi.index[-1] - pd.DateOffset(years=1)].corr().iloc[0, 1], pc=pc(y, v) if s != 'XU100' else np.nan,
                        gap_l1=pd.concat([gp[s], v.shift(1)], axis=1).dropna().corr().iloc[0, 1], intra_l1=pd.concat([it[s], v.shift(1)], axis=1).dropna().corr().iloc[0, 1],
                        is_c=dfi[dfi.index < '2021-01-01'].corr().iloc[0, 1], oos_c=dfi[dfi.index >= '2021-01-01'].corr().iloc[0, 1], n=len(dfi)))
R = pd.DataFrame(res); R.to_csv('res_riskprem.csv', index=False)
for k in P:
    S = R[R.proxy == k].set_index('stock')
    print(k, 'XU100 c', round(S.at['XU100', 'corr_full'], 2), 'gapL1', round(S.at['XU100', 'gap_l1'], 2), 'intraL1', round(S.at['XU100', 'intra_l1'], 2), '| pc en yüksek', S.pc.dropna().sort_values().tail(4).round(2).to_dict(), 'en düşük', S.pc.dropna().sort_values().head(4).round(2).to_dict())
# XBANK - XU100 spreadi ~ proxy (banka primi)
sp = cc['XBANK'] - cc['XU100']
for k, v in P.items():
    b, t, n = ll.nw_t(sp, v); print('XBANK-XU100 ~', k, 'beta', round(b, 3), 't', round(t, 2))
# ---- 2) Kripto: hafta sonu BTC (Cuma 24:00 -> Pazar 24:00 UTC; BIST ve ES kapalı) -> Pazartesi gap/intra
btc = ll.daily('BTC-USD', on_bist_cal=False); eth = ll.daily('ETH-USD', on_bist_cal=False)
retail = ['ASTOR', 'SASA', 'HEKTS', 'ODAS', 'TRALT', 'PETKM', 'KONTR']
mons = [d for d in cc.index if d.dayofweek == 0]
rows = []
for d in mons:
    fr, su = d - pd.Timedelta(days=3), d - pd.Timedelta(days=1)
    if fr in btc.index and su in btc.index: rows.append((d, np.log(btc[su] / btc[fr])))
W = pd.Series(dict(rows))
kon = decomp2('KONTR') if True else None
out = []
for s in VIOP + ['XU100', 'XBANK', 'KONTR']:
    g = (kon['gap'] if s == 'KONTR' else gp[s]); i_ = (kon['intra'] if s == 'KONTR' else it[s])
    ex_g = g - gp['XU100'] if s != 'XU100' else g
    for nm, y in [('gap', g), ('intra', i_), ('gap_ex', ex_g)]:
        df = pd.concat([y, W], axis=1).dropna()
        if len(df) < 50: continue
        b, t, n = ll.nw_t(df.iloc[:, 0], df.iloc[:, 1], lags=1)
        out.append(dict(stock=s, tgt=nm, corr=df.corr().iloc[0, 1], beta=b, t=t, n=n, is_c=df[df.index < '2021-01-01'].corr().iloc[0, 1], oos_c=df[df.index >= '2021-01-01'].corr().iloc[0, 1]))
C = pd.DataFrame(out); C.to_csv('res_crypto_weekend.csv', index=False)
print('BTC hafta sonu -> Pzt:', C[C.stock.isin(['XU100'] + retail)].round(3).to_string(index=False))
# senkron günlük BTC (BIST takvimi) kısmi korelasyon
bt_ = ll.ret('BTC-USD').reindex(cc.index)
sy = {s: (pd.concat([cc[s], bt_], axis=1).dropna().corr().iloc[0, 1], pc(cc[s], bt_)) for s in VIOP}
sy = pd.DataFrame(sy, index=['corr', 'pc']).T.sort_values('pc'); sy.to_csv('res_crypto_sync.csv'); print('BTC senkron pc en yüksek', sy.tail(5).round(3).to_dict()['pc'])
# ---- 3) XAUTRY: kesin hizalama (h1 snap 15:00 UTC, 2024-06+) ve uzun örneklem (ll.ret GC=F + TRY=X; ~6 saat uyumsuz)
g15, t15 = ll.snap_daily('GC=F', '15:00'), ll.snap_daily('TRY=X', '15:00')
xa_h = np.log(g15 * t15).diff().reindex(cc.index)
xa_d = (ll.ret('GC=F') + ll.ret('TRY=X')).reindex(cc.index)
xo = []
for s in VIOP + ['XBANK', 'XU100']:
    a = pd.concat([cc[s], xa_h], axis=1).dropna(); b_ = pd.concat([cc[s], xa_d], axis=1).dropna()
    xo.append(dict(stock=s, corr_h1=a.corr().iloc[0, 1], pc_h1=pc(cc[s], xa_h) if s != 'XU100' else np.nan, n_h1=len(a), corr_d=b_.corr().iloc[0, 1], pc_d=pc(cc[s], xa_d) if s != 'XU100' else np.nan,
                   is_d=b_[b_.index < '2021-01-01'].corr().iloc[0, 1], oos_d=b_[b_.index >= '2021-01-01'].corr().iloc[0, 1], gap_l1=pd.concat([gp[s], xa_d.shift(1)], axis=1).dropna().corr().iloc[0, 1]))
XO = pd.DataFrame(xo).set_index('stock'); XO.to_csv('res_xautry.csv')
print('XAUTRY XU100', XO.loc['XU100', ['corr_h1', 'corr_d', 'is_d', 'oos_d']].round(3).to_dict(), 'XBANK pc', XO.loc['XBANK', ['pc_h1', 'pc_d']].round(3).to_dict())
print('XAUTRY pc_h1 en yüksek', XO.pc_h1.dropna().sort_values().tail(4).round(2).to_dict(), 'en düşük', XO.pc_h1.dropna().sort_values().head(4).round(2).to_dict())
