# -*- coding: utf-8 -*-
"""B1 (TUR BIST-kapanisi-sonrasi -> ertesi gun banka gap / intra), B3 (ES gece 15:00->06:00 UTC -> banka gap),
ve B4/H3 icin saatlik 15:00 UTC USDTRY ile zamanlama kontrolu. Saatlik veri: bar zaman damgasi = bar BASLANGICI (UTC)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import vb
H1 = vb.D + '/h1'
OUT = os.path.dirname(os.path.abspath(__file__)) + '/res'

def h1(sym):
    x = pd.read_parquet(f'{H1}/{sym}.parquet')
    x = x[~x.index.duplicated(keep='last')].sort_index()
    return x

CAL = vb.CAL
cal = CAL[CAL >= '2023-11-01']
nxt = pd.Series(cal[1:], index=cal[:-1])  # BIST gunu t -> t+1

TGT = ['XBANK.IS', 'GARAN.IS', 'AKBNK.IS', 'YKBNK.IS', 'ISCTR.IS', 'HALKB.IS', 'VAKBN.IS', 'XU100.IS']
dec = {s: vb.bist_rets(s) for s in TGT}

def price_at(x, ts_list, how='open'):
    """ts_list: DatetimeIndex (UTC). 'open' = o of bar starting exactly at ts; yoksa ts'den onceki son barin close'u (en fazla 2 saat)."""
    o = x['o']; c = x['c']
    out = []
    for ts in ts_list:
        if how == 'open' and ts in o.index:
            out.append(o.loc[ts]); continue
        prev = c[(c.index < ts) & (c.index >= ts - pd.Timedelta(hours=2))]
        out.append(prev.iloc[-1] if len(prev) else np.nan)
    return pd.Series(out, index=ts_list)

def corr_t(y, x, Z=None):
    return vb.pc(y, x, Z)

res = []
def rep(tag, y, x, Z=None, extra=''):
    d = corr_t(y, x, Z)
    # iki yari
    df = pd.concat([y.rename('y'), x.rename('x')] + ([Z] if Z is not None else []), axis=1).dropna()
    m = len(df) // 2
    h1_ = vb.pc(df['y'].iloc[:m], df['x'].iloc[:m], df[Z.columns].iloc[:m] if Z is not None else None)
    h2_ = vb.pc(df['y'].iloc[m:], df['x'].iloc[m:], df[Z.columns].iloc[m:] if Z is not None else None)
    res.append(dict(tag=tag, n=d['n'], corr=d['corr'], pc=d['pc'], t=d['t'], beta=d['beta'], h1_pc=h1_['pc'], h2_pc=h2_['pc'], h1_t=h1_['t'], h2_t=h2_['t'], extra=extra))
    print(f"{tag:58s} n={d['n']:4d} corr={d['corr']:+.3f} pc={d['pc']:+.3f} t={d['t']:+.1f} beta={d['beta']:+.3f} | yari1 pc={h1_['pc']:+.3f} (t {h1_['t']:+.1f}) yari2 pc={h2_['pc']:+.3f} (t {h2_['t']:+.1f}) {extra}", flush=True)

# ---------------- B1: TUR post-close ----------------
tur = h1('TUR')
tur_d = vb.load_daily('TUR')
days = [d for d in cal[:-1]]
# baslangic: 14:30 barinin kapanisi (=15:30 UTC fiyati). Alternatif: 14:30 barinin acilisi (=14:30 UTC; BIST kapanisindan ONCE -> kirli)
start1530, start1430, end_h1, end_d, end_full = {}, {}, {}, {}, {}
tur_by_date = {d: g for d, g in tur.groupby(tur.index.normalize().tz_localize(None))}
for d in days:
    g = tur_by_date.get(d)
    if g is None: continue
    b = g[(g.index.hour == 14) & (g.index.minute == 30)]
    if len(b):
        start1530[d] = b['c'].iloc[0]; start1430[d] = b['o'].iloc[0]
    gg = g[g.index.hour <= 21]
    end_h1[d] = gg['c'].iloc[-1]
    if d in tur_d.index: end_d[d] = tur_d.loc[d, 'c']
    # tam pencere: t+1 BIST gununden onceki son ABD kapanisi
    t1 = nxt[d]
    prior = tur_d[(tur_d.index >= d) & (tur_d.index < t1)]
    if len(prior): end_full[d] = prior['c'].iloc[-1]
S = lambda dct: pd.Series(dct)
post = np.log(S(end_h1) / S(start1530)).dropna()
post_d = np.log(S(end_d) / S(start1530)).dropna()
post_full = np.log(S(end_full) / S(start1530)).dropna()
post1430 = np.log(S(end_h1) / S(start1430)).dropna()
def to_next(s):
    s = s[s.index.isin(nxt.index)]
    return pd.Series(s.values, index=nxt[s.index].values)

P = to_next(post); Pd = to_next(post_d); Pf = to_next(post_full); P14 = to_next(post1430)
print('\n=== B1: TUR 15:30 UTC -> ABD kapanisi (t) => BIST t+1 ===')
for s in TGT:
    rep(f'B1 TUR_post->{s} gap', dec[s]['gap'], P)
    rep(f'B1 TUR_post->{s} intra', dec[s]['intra'], P)
xg = dec['XU100.IS']['gap'].rename('XU100gap'); xi = dec['XU100.IS']['intra'].rename('XU100intra')
print('-- varyantlar (XBANK) --')
rep('B1 TUR_post(dailyclose)->XBANK gap', dec['XBANK.IS']['gap'], Pd)
rep('B1 TUR_post(tam pencere, tatiller dahil)->XBANK gap', dec['XBANK.IS']['gap'], Pf)
rep('B1 TUR 14:30->kapanis (KIRLI: BIST kapanisi oncesi 30dk)->XBANK gap', dec['XBANK.IS']['gap'], P14)
rep('B1 TUR_post->XBANK gap | XU100 gap (bankaya ozgu?)', dec['XBANK.IS']['gap'], P, xg.to_frame())
rep('B1 TUR_post->XBANK intra | XBANK gap (gap asiri tepki?)', dec['XBANK.IS']['intra'], P, dec['XBANK.IS']['gap'].rename('g').to_frame())
rep('B1 TUR_post->XBANK intra | XU100 intra', dec['XBANK.IS']['intra'], P, xi.to_frame())
# gun-ici kalinti: sinyal ile gap'in ayni yonde/ters yonde oldugu gunler
df = pd.concat([P.rename('s'), dec['XBANK.IS']['gap'].rename('g'), dec['XBANK.IS']['intra'].rename('i')], axis=1).dropna()
q = df['s'].abs() > df['s'].abs().quantile(0.8)
print(f"  |sinyal| ust %20 gunleri (n={q.sum()}): ort sign(s)*intra = {(np.sign(df.s[q])*df.i[q]).mean()*1e4:+.1f} bps, t={(np.sign(df.s[q])*df.i[q]).mean()/((np.sign(df.s[q])*df.i[q]).std()/np.sqrt(q.sum())):+.2f}; sign(s)*gap = {(np.sign(df.s[q])*df.g[q]).mean()*1e4:+.1f} bps")
# basit backtest: sign(s)*intra, 10 bps
bt = np.sign(df.s) * df.i - 0.0010
print(f"  BT sign(TUR_post)*XBANK intra, 10bps: ort {bt.mean()*1e4:+.1f} bps/gun, t={bt.mean()/(bt.std()/np.sqrt(len(bt))):+.2f}, brut {(bt+0.001).mean()*1e4:+.1f} bps, n={len(bt)}")

# ---------------- B3: ES gece 15:00 -> 06:00 UTC ----------------
es = h1('ES=F')
print('\n=== B3: ES 15:00 UTC (t) -> 06:00 UTC (t+1) => BIST t+1 gap ===')
d0 = [d for d in cal[:-1] if d >= pd.Timestamp('2024-06-10')]
ts15 = pd.DatetimeIndex([pd.Timestamp(d).tz_localize('UTC') + pd.Timedelta(hours=15) for d in d0])
ts21 = pd.DatetimeIndex([pd.Timestamp(d).tz_localize('UTC') + pd.Timedelta(hours=20) for d in d0])  # 20:00 UTC (yaz kapanisi; kis icin 21)
ts06 = pd.DatetimeIndex([pd.Timestamp(nxt[d]).tz_localize('UTC') + pd.Timedelta(hours=6) for d in d0])
ts0655 = pd.DatetimeIndex([pd.Timestamp(nxt[d]).tz_localize('UTC') + pd.Timedelta(hours=7) for d in d0])
p15 = price_at(es, ts15); p06 = price_at(es, ts06); p20 = price_at(es, ts21); p07 = price_at(es, ts0655)
idx_next = pd.DatetimeIndex([nxt[d] for d in d0])
esn = pd.Series(np.log(p06.values / p15.values), index=idx_next)
es_a = pd.Series(np.log(p20.values / p15.values), index=idx_next)  # 15->20 (ABD seansi)
es_b = pd.Series(np.log(p06.values / p20.values), index=idx_next)  # 20->06 (Asya gecesi)
es_c = pd.Series(np.log(p07.values / p06.values), index=idx_next)  # 06->07 (acilis oncesi/acilis)
esn = esn.replace([np.inf, -np.inf], np.nan)
for s in TGT:
    rep(f'B3 ES_night->{s} gap', dec[s]['gap'], esn)
    rep(f'B3 ES_night->{s} intra', dec[s]['intra'], esn)
rep('B3 ES_night->XBANK gap | XU100 gap', dec['XBANK.IS']['gap'], esn, xg.to_frame())
rep('B3 ES 15->20 UTC ->XBANK gap', dec['XBANK.IS']['gap'], es_a)
rep('B3 ES 20->06 UTC ->XBANK gap', dec['XBANK.IS']['gap'], es_b)
rep('B3 ES 06->07 UTC (pencere disi) ->XBANK gap', dec['XBANK.IS']['gap'], es_c)
rep('B3 ES 06->07 UTC ->XBANK intra', dec['XBANK.IS']['intra'], es_c)
rep('B3 ES_night->XBANK intra | XBANK gap', dec['XBANK.IS']['intra'], esn, dec['XBANK.IS']['gap'].rename('g').to_frame())
# TUR ve ES birlikte
Zb = pd.concat([P.rename('TURpost')], axis=1)
rep('B3 ES_night->XBANK gap | TUR_post', dec['XBANK.IS']['gap'], esn, Zb)
rep('B1 TUR_post->XBANK gap | ES_night', dec['XBANK.IS']['gap'], P, esn.rename('ESn').to_frame())
df = pd.concat([esn.rename('s'), dec['XBANK.IS']['intra'].rename('i')], axis=1).dropna()
bt = np.sign(df.s) * df.i - 0.0010
print(f"  BT sign(ES_night)*XBANK intra, 10bps: ort {bt.mean()*1e4:+.1f} bps/gun, t={bt.mean()/(bt.std()/np.sqrt(len(bt))):+.2f}, brut {(bt+0.001).mean()*1e4:+.1f}, n={len(bt)}")

# ---------------- B4/H3 zamanlama: 15:00 UTC USDTRY ----------------
print('\n=== B4/H3: USDTRY 15:00 UTC (saatlik) vs gunluk kaydirilmis ===')
fx = h1('TRY=X')
c2 = CAL[CAL >= '2024-01-16']
ts = pd.DatetimeIndex([pd.Timestamp(d).tz_localize('UTC') + pd.Timedelta(hours=15) for d in c2])
p = price_at(fx, ts)
fx15 = pd.Series(np.log(p.values / np.roll(p.values, 1)), index=c2); fx15.iloc[0] = np.nan
fxd = vb.ret('TRY=X')
x100 = vb.ret('XU100.IS').rename('XU100').to_frame()
both = pd.concat([fx15.rename('fx15'), fxd.rename('fxd')], axis=1).dropna()
print(f"  corr(fx15, gunluk-kaydirilmis) = {both.corr().iloc[0,1]:.3f}; sd fx15={both.fx15.std()*1e4:.1f}bp sd fxd={both.fxd.std()*1e4:.1f}bp n={len(both)}")
for s in ['XBANK.IS', 'AKBNK.IS', 'GARAN.IS', 'YKBNK.IS', 'ENKAI.IS', 'SAHOL.IS', 'XUSIN.IS']:
    y = vb.ret(s)
    rep(f'FX15 {s} ~ USDTRY(15:00) | XU100 2024-01+', y, fx15, x100)
    rep(f'FXd  {s} ~ USDTRY(gunluk) | XU100 2024-01+', vb.per(y, '2024-01-16', '2026-12-31'), vb.per(fxd, '2024-01-16', '2026-12-31'), x100)
    rep(f'FX15+L1 {s} ~ USDTRY(15:00) | XU100+fx15_L1', y, fx15, pd.concat([x100, fx15.shift(1).rename('L1')], axis=1))
pd.DataFrame(res).to_csv(f'{OUT}/hourly_results.csv', index=False)
print('kaydedildi')
