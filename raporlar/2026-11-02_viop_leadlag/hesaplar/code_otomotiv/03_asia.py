"""Asya (Kore/Japonya/Tayvan) aynı gün (lag0) -> BIST gap_t ve intra_t.
Kore kapanışı 06:30 UTC, Tokyo 06:00 UTC (Kasım 2024'ten beri 06:30), Tayvan 05:30 UTC; BIST açılış müzayedesi ~06:40-07:00 UTC.
=> Asya_t BIST t açılışından ÖNCE bilinir: intra_t (açılış->kapanış) testi işlenebilirdir.
Kontroller: XU100 gap_t, hissenin kendi gap_t (ikisi de açılışta bilinir), ^GSPC_{t-1} (ABD önceki seans), ayrıca KOSPI/N225_t (emsal mi piyasa mı?).
Saatlik (2023-11+): ilk saat (açılış->07:30 UTC bar kapanışı) ve gün geri kalanı ayrımı.
Çıktı: res/asia_pairs.csv, res/asia_hourly.csv, res/asia_bt.csv"""
from common import *

ASIA = ['^KS11','005930.KS','000660.KS','005380.KS','000270.KS','066570.KS','034220.KS','267260.KS','298040.KS','010120.KS','103590.KS','006260.KS',
        '^N225','7203.T','7267.T','7201.T','7270.T','7269.T','6752.T','6758.T','6501.T','6503.T','6504.T','5108.T',
        '^TWII','2330.TW','2317.TW','2409.TW','3481.TW']
xg = D('XU100')['gap']; spx1 = R('^GSPC').shift(1)
rows = []
for st in STOCKS:
    d = D(st)
    for a in ASIA:
        try: A = R(a)
        except Exception as e: print('skip', a, e); continue
        idx_ctrl = R('^KS11') if a.endswith('.KS') else (R('^N225') if a.endswith('.T') else R('^TWII'))
        o = {'stock': st, 'asia': a}
        o['gap_c'], o['gap_t'], _ = corr_t(d['gap'], A)
        o['intra_c'], o['intra_t'], o['n'] = corr_t(d['intra'], A)
        o['pc'], o['pc_t'], _ = pcorr(d['intra'], A, [xg, d['gap'], spx1])
        sp, is0 = split_for(d['intra'], A)
        o['split'] = str(sp.date())
        o['pc_IS'], o['pc_t_IS'], _ = pcorr(d['intra'], A, [xg, d['gap'], spx1], start=is0, end=sp)
        o['pc_OOS'], o['pc_t_OOS'], _ = pcorr(d['intra'], A, [xg, d['gap'], spx1], start=sp)
        if a not in ('^KS11', '^N225', '^TWII'):
            o['pc_exidx'], o['pc_exidx_t'], _ = pcorr(d['intra'], A, [xg, d['gap'], spx1, idx_ctrl])
        # Asya'ya özgü kısım (ABD önceki seansından arındırılmış) -> gap
        o['gap_pc_spx'], o['gap_pc_spx_t'], _ = pcorr(d['gap'], A, [spx1])
        # yıllık işaret tutarlılığı (intra ham)
        df = pd.concat([d['intra'].rename('y'), A.rename('x')], axis=1).dropna()
        g = df.groupby(df.index.year).apply(lambda x: x['y'].corr(x['x']) if len(x) > 60 else np.nan).dropna()
        o['yr_pos_share'] = float((g > 0).mean()) if len(g) else np.nan; o['n_years'] = len(g)
        o['p'] = ll.t_to_p(o['pc_t'])
        rows.append(o)
A_ = pd.DataFrame(rows)
rej, pa = ll.fdr(A_['p'].values); A_['fdr'] = rej; A_['p_bh'] = pa
A_.to_csv(os.path.join(RES, 'asia_pairs.csv'), index=False)
print('Asya test sayısı:', len(A_), '| FDR geçen:', int(A_.fdr.sum()))
c = ['stock', 'asia', 'n', 'gap_t', 'intra_c', 'intra_t', 'pc', 'pc_t', 'pc_t_IS', 'pc_t_OOS', 'pc_exidx_t', 'yr_pos_share', 'p_bh']
print(A_.sort_values('pc_t', key=abs, ascending=False).head(14)[c].round(3).to_string(index=False))
print('gap_t medyan (|.|):', A_.gap_t.abs().median().round(2), '| intra_t medyan:', A_.intra_t.abs().median().round(2))

# ---- saatlik: ilk saat vs geri kalan ----
H1 = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data/h1/'
def bist_parts(st):
    h = pd.read_parquet(H1 + st + '.IS.parquet'); h = h[h.index.hour.isin([6, 7, 8, 9, 10, 11, 12, 13, 14, 15])]
    day = h.index.tz_convert(None).normalize()
    g = h.groupby(day)
    o = g['o'].first(); first_close = g.apply(lambda x: x['c'].iloc[0]); last = g['c'].last()
    return pd.DataFrame({'first': np.log(first_close / o), 'rest': np.log(last / first_close)})
def asia_daily_h1(a):
    h = pd.read_parquet(H1 + a + '.parquet'); day = h.index.tz_convert(None).normalize()
    c = h.groupby(day)['c'].last(); return np.log(c).diff()
hrows = []
for st in STOCKS:
    try: P_ = bist_parts(st)
    except Exception as e: print('h1 skip', st, e); continue
    for a in ['^KS11', '005930.KS', '066570.KS', '034220.KS', '000270.KS', '005380.KS', '267260.KS', '298040.KS', '010120.KS', '7203.T', '6752.T', '6758.T', '^N225', '^TWII']:
        try: A = asia_daily_h1(a)
        except Exception: continue
        o = {'stock': st, 'asia': a}
        o['first_c'], o['first_t'], o['n'] = corr_t(P_['first'], A)
        o['rest_c'], o['rest_t'], _ = corr_t(P_['rest'], A)
        hrows.append(o)
HH = pd.DataFrame(hrows); HH.to_csv(os.path.join(RES, 'asia_hourly.csv'), index=False)
print('saatlik (2023-11+): |first_t|>2:', int((HH.first_t.abs() > 2).sum()), '/', len(HH), '| |rest_t|>2:', int((HH.rest_t.abs() > 2).sum()))
print(HH.sort_values('rest_t', key=abs, ascending=False).head(6).round(3).to_string(index=False))

# ---- backtest: en iyi Asya çiftleri (sign ve |z|>1) ----
brows = []
top = A_[A_.fdr].sort_values('pc_t', key=abs, ascending=False).head(6)
pairs = [(r.stock, r.asia) for r in top.itertuples()] + [('ASTOR', '298040.KS'), ('ARCLK', '066570.KS'), ('VESTL', '034220.KS'), ('FROTO', '000270.KS')]
for st, a in dict.fromkeys(pairs):
    for mode, thr in [('sign', 0.0), ('z', 1.0)]:
        sp, _ = split_for(D(st)['intra'], R(a))
        res = bt(R(a), D(st)['intra'], costs=(8, 15), mode=mode, thr=thr, split=str(sp.date()))
        for cst in (8, 15):
            r = bt_row(f'{a} lag0 -> {st} intra [{mode}{thr}]', res, cst); r['split'] = str(sp.date()); brows.append(r)
BB = pd.DataFrame(brows); BB.to_csv(os.path.join(RES, 'asia_bt.csv'), index=False)
print(BB[BB.cost_bps == 8][['test', 'IS_n', 'IS_mean_bps', 'IS_t', 'OOS_n', 'OOS_mean_bps', 'OOS_t', 'OOS_sharpe']].round(2).to_string(index=False))
