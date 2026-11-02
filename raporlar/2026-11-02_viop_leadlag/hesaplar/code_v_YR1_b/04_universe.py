"""47 hissenin tüm yönlü çiftlerinde aynı kural (β250, z60>1,5, t+1 açılış, 8 bps) -> null dağılım, SAHOL/AKBNK sırası, korelasyon-eşli plasebo,
grup (holding–iştirak) çiftleri. Vektörize."""
import vb, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
U = 'AEFES AKBNK AKSEN ALARK ARCLK ASELS ASTOR BIMAS BRSAN CIMSA DOAS DOHOL EKGYO ENJSA ENKAI EREGL FROTO GARAN GUBRF HALKB HEKTS ISCTR KCHOL KRDMD MGROS ODAS OYAKC PETKM PGSUS SAHOL SASA SISE SOKM TAVHL TCELL THYAO TKFEN TOASO TRALT TRMET TSKB TTKOM TUPRS ULKER VAKBN VESTL YKBNK'.split()
idx = vb.cal(); idx = idx[idx >= '2010-01-01']
C = pd.DataFrame({s: vb.load(s)['cc'] for s in U}).reindex(idx)
G = pd.DataFrame({s: vb.load(s)['gap'] for s in U}).reindex(idx)
I = pd.DataFrame({s: vb.load(s)['intra'] for s in U}).reindex(idx)
isd = (idx >= '2014-01-01') & (idx < '2021-01-01'); osd = idx >= '2021-01-01'
def nwt_cols(X, lags=5):
    X = np.where(np.isnan(X), 0, X); n = X.shape[0]; m = X.mean(0); E = X - m; s = (E * E).sum(0) / n
    for L in range(1, lags + 1): s += 2 * (1 - L / (lags + 1)) * (E[L:] * E[:-L]).sum(0) / n
    return m, m / np.sqrt(s / n)
def run(a, win=60, thr=1.5, cost=8, bwin=250):
    ca = C[a]; others = [b for b in U if b != a]
    Cb = C[others]
    cov = Cb.rolling(bwin, min_periods=bwin // 2).cov(ca); var = Cb.rolling(bwin, min_periods=bwin // 2).var()
    beta = (cov / var).shift(1)
    s = (-(beta.mul(1.0)).mul(Cb)).add(ca, axis=0)
    S = s.fillna(0).cumsum()
    z = (S - S.rolling(win, min_periods=win // 2).mean()) / S.rolling(win, min_periods=win // 2).std()
    pos = (-np.sign(z)).where(z.abs() > thr, 0.0).fillna(0.0)
    Pg = pos.shift(2).fillna(0); Pi = pos.shift(1).fillna(0); bi = beta.shift(1)
    sg = (-bi * G[others]).add(G[a], axis=0); si = (-bi * I[others]).add(I[a], axis=0)
    net = Pg * sg.fillna(0) + Pi * si.fillna(0) - cost / 1e4 / 2 * (1 + bi.abs().fillna(1)) * (Pi - Pg).abs()
    exp = (Pg != 0) | (Pi != 0)
    out = []
    for lab, m in [('IS', isd), ('OOS', osd)]:
        X = net.values[m]; mm, tt = nwt_cols(X); e = exp.values[m]
        bps = 1e4 * np.where(e, net.values[m], 0).sum(0) / np.maximum(e.sum(0), 1)
        out.append(pd.DataFrame({'b': others, f'{lab}_t': tt, f'{lab}_bps': bps}).set_index('b'))
    o = pd.concat(out, axis=1); o['a'] = a
    return o.reset_index()
if __name__ == '__main__':
    R = pd.concat([run(a) for a in U], ignore_index=True)
    corr = C[(idx >= '2014')].corr()
    R['corr'] = [corr.loc[a, b] for a, b in zip(R.a, R.b)]
    R.to_csv('res_universe.csv', index=False)
    print('çift sayısı', len(R), ' IS t ort/sd', R.IS_t.mean().round(2), R.IS_t.std().round(2), ' OOS t ort/sd', R.OOS_t.mean().round(2), R.OOS_t.std().round(2), ' corr(IS_t,OOS_t)', R[['IS_t', 'OOS_t']].corr().iloc[0, 1].round(2))
    R['mn'] = R[['IS_t', 'OOS_t']].min(axis=1, skipna=False); R = R.sort_values('mn', ascending=False)
    print(R.head(15).round(2).to_string())
    sa = R[(R.a == 'SAHOL') & (R.b == 'AKBNK')].iloc[0]
    print('SAHOL/AKBNK:', sa.to_dict(), ' sıra (min t):', int((R.mn > sa.mn).sum()) + 1, '/', int(R.mn.notna().sum()))
    print('IS t>=3 & OOS t>=3 olan çift:', int(((R.IS_t >= 3) & (R.OOS_t >= 3)).sum()), ' IS>=2 & OOS>=2:', int(((R.IS_t >= 2) & (R.OOS_t >= 2)).sum()), ' beklenen (bağımsız N(ort,sd)):',
          round(len(R) * (1 - __import__('scipy').stats.norm.cdf(2, R.IS_t.mean(), R.IS_t.std())) * (1 - __import__('scipy').stats.norm.cdf(2, R.OOS_t.mean(), R.OOS_t.std())), 2))
    # korelasyon eşli
    cs = corr.loc['SAHOL', 'AKBNK']; M = R[(R['corr'] > cs - 0.1) & (R['corr'] < cs + 0.1)]
    print(f'korelasyon eşli (SAHOL/AKBNK corr {cs:.2f} ±0,1): n={len(M)}  IS t ort {M.IS_t.mean():.2f}, OOS t ort {M.OOS_t.mean():.2f}; ikisi de >2: {int(((M.IS_t > 2) & (M.OOS_t > 2)).sum())}')
    print(M.sort_values('mn', ascending=False).head(8).round(2).to_string())
    # holding–iştirak / grup çiftleri (47 içinde)
    GR = [('KCHOL', 'YKBNK'), ('KCHOL', 'TUPRS'), ('KCHOL', 'FROTO'), ('KCHOL', 'ARCLK'), ('KCHOL', 'TOASO'), ('SAHOL', 'ENJSA'), ('SAHOL', 'CIMSA'), ('SAHOL', 'AKBNK'), ('ISCTR', 'SISE'), ('ISCTR', 'TSKB'),
          ('DOHOL', 'AKBNK'), ('TRMET', 'TRALT'), ('ALARK', 'ENJSA'), ('FROTO', 'TOASO'), ('EREGL', 'KRDMD'), ('OYAKC', 'CIMSA'), ('AEFES', 'MGROS'), ('TKFEN', 'EREGL'), ('HEKTS', 'OYAKC')]
    print('a-bacağına göre ortalama t (ilk 10, OOS):'); ag = R.groupby('a')[['IS_t', 'OOS_t']].mean().sort_values('OOS_t', ascending=False); print(ag.head(10).round(2).to_string()); print('SAHOL sırası', list(ag.index).index('SAHOL') + 1, '/', len(ag))
    bg = R.groupby('b')[['IS_t', 'OOS_t']].mean().sort_values('OOS_t', ascending=False); print('b-bacağı ilk 5'); print(bg.head(5).round(2).to_string())
    sx = R[R.a == 'SAHOL'].sort_values('OOS_t', ascending=False); print('SAHOL/x en iyi 10:'); print(sx.head(10)[['b','IS_t','OOS_t','corr']].round(2).to_string()); print('SAHOL/x (AKBNK hariç) ort IS/OOS', sx[sx.b!='AKBNK'][['IS_t','OOS_t']].mean().round(2).to_dict(), ' banka b:', sx[sx.b.isin(['GARAN','YKBNK','ISCTR','HALKB','VAKBN','TSKB'])][['IS_t','OOS_t']].mean().round(2).to_dict())
    Gp = pd.concat([R[(R.a == a) & (R.b == b)] for a, b in GR])
    print('grup/benzer çiftler:'); print(Gp.round(2).to_string())
