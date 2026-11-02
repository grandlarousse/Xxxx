"""V1 bağımsız doğrulama: Kredi notu değişikliği sonrası kontraryen (haberi sat) stratejisi.
ll.py / olib.py KULLANILMAZ. Ham parquet -> kendi hizalama.
Çalıştır: nice -n 10 python3 -I v1.py
"""
import numpy as np, pandas as pd, json, os, sys
SC = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad'
OUT = SC + '/out/code_v_V1_a'
D = SC + '/data'
rng = np.random.default_rng(12345)
pd.set_option('display.width', 220); pd.set_option('display.max_columns', 40)

# ---------------------------------------------------------------- veri
def load_daily(sym):
    d = pd.read_parquet(f'{D}/daily/{sym}.parquet')
    li = pd.DatetimeIndex(pd.to_datetime(d['ldate'].astype(str)))
    d.index = li.normalize()
    d = d[~d.index.duplicated(keep='last')].sort_index()
    return d[['o', 'h', 'l', 'c', 'v']].astype(float)

IDX = ['XU100.IS', 'XBANK.IS', 'XU030.IS']
DLY = {s: load_daily(s) for s in IDX}
CAL = DLY['XU100.IS'].index[DLY['XU100.IS'].index >= '2010-01-01']
for s in IDX:
    DLY[s] = DLY[s].reindex(CAL)
# FX: Yahoo '=X' bar etiketi D'nin kapanışı aslında D 00:00 UTC (= D-1 sonu) -> etiketi 1 gün geri al
fx = load_daily('TRY=X')
fx_fixed = fx['c'].copy(); fx_fixed.index = fx_fixed.index - pd.Timedelta(days=1)
fx_fixed = fx_fixed[~fx_fixed.index.duplicated(keep='last')]
FXC = fx_fixed.reindex(CAL, method='ffill')   # BIST günü D için ~D sonu (24:00 UTC) USDTRY

def load_h1(sym):
    f = f'{D}/h1/{sym}.parquet'
    if not os.path.exists(f): return None
    h = pd.read_parquet(f); h.index = pd.DatetimeIndex(h.index).tz_convert('UTC')
    return h
H1 = {s: load_h1(s) for s in IDX}

def first_hour_close(sym, day):
    """06:30 UTC barının kapanışı (≈07:30 UTC = 10:30 TSİ)."""
    h = H1[sym]
    if h is None: return np.nan
    t = pd.Timestamp(day.date()).tz_localize('UTC') + pd.Timedelta(hours=6, minutes=30)
    return float(h.at[t, 'c']) if t in h.index else np.nan

# ---------------------------------------------------------------- olaylar (birincil/ikincil kaynaklardan doğrulandı; bkz. v_V1_a.md)
# ann: açıklama tarihi (yerel); hepsi BIST kapanışından SONRA (S&P 20.07.2016 hariç belirsiz: ~15-16 UTC)
EVENTS = [
 # date, agency, kind, dir, weekday-note, src
 ('2016-07-20', 'SP', 'rating', -1, 'Çar, takvim dışı (darbe sonrası); aynı akşam OHAL ilanı', 'Garanti BBVA KAP/IR, CNBC 20.07.2016 11:58 EDT'),
 ('2016-09-23', 'MOODYS', 'rating', -1, 'Cum', 'Bloomberg 23.09.2016, countryeconomy'),
 ('2017-01-27', 'FITCH', 'rating', -1, 'Cum (aynı gün S&P görünüm negatif)', 'Hurriyet DN, countryeconomy'),
 ('2018-03-07', 'MOODYS', 'rating', -1, 'Çar gece, takvim dışı', 'Reuters/Business Standard 08.03.2018, countryeconomy'),
 ('2018-05-01', 'SP', 'rating', -1, 'Sal gece (1 Mayıs tatil), takvim dışı', 'tradingeconomics, countryeconomy'),
 ('2018-07-13', 'FITCH', 'rating', -1, 'Cum', 'Arab Times 15.07.2018, ING'),
 ('2018-08-17', 'SP+MOODYS', 'rating', -1, 'Cum; Pzt 20.08 arife yarım gün, sonra 4 gün bayram', 'intellinews, tradingeconomics, countryeconomy'),
 ('2019-06-14', 'MOODYS', 'rating', -1, 'Cum', 'countryeconomy, Gulf News'),
 ('2019-07-12', 'FITCH', 'rating', -1, 'Cum; 15.07 tatil', 'Al Arabiya/Turkish Minute 13.07.2019'),
 ('2020-09-11', 'MOODYS', 'rating', -1, 'Cum', 'countryeconomy, Gulf News'),
 ('2022-02-11', 'FITCH', 'rating', -1, 'Cum  ** 1. TUR LİSTESİNDE YOK **', 'Bloomberg 11.02.2022, Garanti BBVA IR, bianet'),
 ('2022-07-08', 'FITCH', 'rating', -1, 'Cum (arife); 13.07 açılış. Not B+->B (1. tur BB-->B yazmış)', 'Bloomberg 08.07.2022, Garanti BBVA IR'),
 ('2022-08-12', 'MOODYS', 'rating', -1, 'Cum', 'countryeconomy'),
 ('2022-09-30', 'SP', 'rating', -1, 'Cum', 'tradingeconomics, countryeconomy'),
 ('2024-03-08', 'FITCH', 'rating', +1, 'Cum', 'Bloomberg 08.03.2024, invest.gov.tr'),
 ('2024-05-03', 'SP', 'rating', +1, 'Cum', 'tradingeconomics, countryeconomy'),
 ('2024-07-19', 'MOODYS', 'rating', +1, 'Cum', 'countryeconomy, intellinews'),
 ('2024-09-06', 'FITCH', 'rating', +1, 'Cum', 'Bloomberg 06.09.2024, Garanti BBVA IR'),
 ('2024-11-01', 'SP', 'rating', +1, 'Cum', 'tradingeconomics, countryeconomy'),
 ('2025-07-25', 'MOODYS', 'rating', +1, 'Cum', 'countryeconomy, Reuters/TradingView'),
 # --- görünüm / izleme (alternatif tanım)
 ('2014-02-07', 'SP', 'outlook', -1, 'Cum', 'tradingeconomics'),
 ('2014-04-11', 'MOODYS', 'outlook', -1, 'Cum', 'countryeconomy'),
 ('2016-05-06', 'SP', 'outlook', +1, 'Cum (neg->durağan)  ** 1. turda yok **', 'tradingeconomics, countryeconomy'),
 ('2016-07-18', 'MOODYS', 'review', -1, 'Pzt (izlemeye alma)', 'countryeconomy'),
 ('2016-08-19', 'FITCH', 'outlook', -1, 'Cum', 'CNBC 20.08.2016'),
 ('2016-11-04', 'SP', 'outlook', +1, 'Cum (neg->durağan)  ** 1. turda yok **', 'tradingeconomics, countryeconomy'),
 ('2017-03-17', 'MOODYS', 'outlook', -1, 'Cum', 'countryeconomy'),
 ('2018-06-01', 'MOODYS', 'review', -1, 'Cum', 'countryeconomy'),
 ('2019-11-01', 'FITCH', 'outlook', +1, 'Cum (neg->durağan)  ** 1. turda yok **', 'Duvar English, bianet'),
 ('2020-08-21', 'FITCH', 'outlook', -1, 'Cum', 'Bloomberg 21.08.2020'),
 ('2021-02-19', 'FITCH', 'outlook', +1, 'Cum (neg->durağan)  ** 1. turda yok **', 'Hurriyet DN'),
 ('2021-12-02', 'FITCH', 'outlook', -1, 'Per gece  ** 1. turda yok **', 'Garanti BBVA IR, fxstreet 02.12.2021 22:19'),
 ('2021-12-10', 'SP', 'outlook', -1, 'Cum  ** 1. turda yok **', 'S&P notu, capital.com.tr'),
 ('2023-03-31', 'SP', 'outlook', -1, 'Cum', 'tradingeconomics'),
 ('2023-09-08', 'FITCH', 'outlook', +1, 'Cum', 'countryeconomy'),
 ('2023-09-29', 'SP', 'outlook', +1, 'Cum', 'tradingeconomics'),
 ('2023-11-30', 'SP', 'outlook', +1, 'Per', 'tradingeconomics'),
 ('2024-01-12', 'MOODYS', 'outlook', +1, 'Cum', 'countryeconomy'),
 ('2026-01-23', 'FITCH', 'outlook', +1, 'Cum', 'ntv, intellinews'),
 ('2026-04-10', 'FITCH', 'outlook', -1, 'Cum, takvim dışı (poz->durağan)  ** 1. turda yok **', 'evrensel 11.04.2026, QNB Invest, BloombergHT'),
]
EV = pd.DataFrame(EVENTS, columns=['ann', 'agency', 'kind', 'dir', 'note', 'src'])
EV['ann'] = pd.to_datetime(EV['ann'])
EV['wd'] = EV['ann'].dt.day_name().str[:3]
pos = CAL.searchsorted(EV['ann'], side='right')         # açıklama BIST kapanışından sonra -> ilk BIST günü > ann
EV['react'] = [CAL[p] if p < len(CAL) else pd.NaT for p in pos]
EV['react_i'] = pos
# 1. turun 19 olayı (karşılaştırma)
R1 = ['2016-07-21', '2016-09-26', '2017-01-30', '2018-03-08', '2018-05-02', '2018-07-16', '2018-08-20', '2019-06-17', '2019-07-16',
      '2020-09-14', '2022-07-13', '2022-08-15', '2022-10-03', '2024-03-11', '2024-05-06', '2024-07-22', '2024-09-09', '2024-11-04', '2025-07-28']
R1 = pd.to_datetime(R1)

# ---------------------------------------------------------------- getiri motoru
def px(sym, i, field):
    if i < 0 or i >= len(CAL): return np.nan
    return DLY[sym][field].iloc[i]

def trade(sym, i0, entry='open', exit_k=2):
    """i0 = react gün indeksi. entry: 'open' (t0 açılış), 'h1' (t0 ilk saat kapanışı), 'close0' (t0 kapanış),
       'open1' (t+1 açılış), 'prevclose' (olay öncesi kapanış; İŞLENEBİLİR DEĞİL, toplam tepki).
       Çıkış: t+exit_k kapanışı. Log getiri döner (yönsüz)."""
    if entry == 'open': p0 = px(sym, i0, 'o')
    elif entry == 'h1': p0 = first_hour_close(sym, CAL[i0])
    elif entry == 'close0': p0 = px(sym, i0, 'c')
    elif entry == 'open1': p0 = px(sym, i0 + 1, 'o')
    elif entry == 'prevclose': p0 = px(sym, i0 - 1, 'c')
    p1 = px(sym, i0 + exit_k, 'c')
    return np.log(p1 / p0)

def fx_leg(i0, exit_k):  # USDTRY ~ (t0-1 sonu) -> (t+k sonu), yaklaşık
    return np.log(FXC.iloc[i0 + exit_k] / FXC.iloc[i0 - 1])

def tstat(x):
    x = np.asarray(pd.Series(x).dropna()); n = len(x)
    if n < 3 or x.std(ddof=1) == 0: return np.nan, n
    return x.mean() / (x.std(ddof=1) / np.sqrt(n)), n

def summarize(v, cost_bps=15):
    v = pd.Series(v).dropna() - cost_bps / 1e4
    t, n = tstat(v)
    return dict(n=n, mean_bps=round(1e4 * v.mean(), 1), med_bps=round(1e4 * v.median(), 1), t=round(t, 2), hit=round((v > 0).mean(), 2))

def signed_returns(ev, sym='XU100.IS', entry='open', exit_k=2, usd=False, excess=None):
    out = {}
    for _, e in ev.iterrows():
        i0 = int(e.react_i)
        r = trade(sym, i0, entry, exit_k)
        if usd: r = r - fx_leg(i0, exit_k)
        if excess: r = r - trade(excess, i0, entry, exit_k)
        out[e.react] = -e.dir * r     # KONTRARYEN
    return pd.Series(out)

if __name__ == '__main__':
    res = {}
    print('=== OLAY LİSTESİ (not değişiklikleri) ===')
    rat = EV[EV.kind == 'rating'].copy()
    print(rat[['ann', 'wd', 'agency', 'dir', 'react', 'note']].to_string(index=False))
    print('1. tur reaksiyon günleri benim listemde mi?', R1.isin(rat.react).all(), '| benim listemde fazladan:', sorted(set(rat.react) - set(R1)))
    EV.to_csv(OUT + '/events_verified.csv', index=False)

    # (a) 1. tur listesi ile birebir yeniden üretim
    r1ev = rat[rat.react.isin(R1)]
    print('\n=== (a) YENİDEN ÜRETİM: 1. tur 19 olay, Pzt açılış -> t+2 kapanış, kontraryen, 15 bps ===')
    rows = []
    for sym in IDX:
        v = signed_returns(r1ev, sym)
        for lab, m in [('ALL', v.index.notna()), ('IS', v.index < '2021-01-01'), ('OOS', v.index >= '2021-01-01')]:
            rows.append(dict(set='R1_19', sym=sym, sample=lab, **summarize(v[m])))
    # (a2) düzeltilmiş liste (n=20)
    for sym in IDX:
        v = signed_returns(rat, sym)
        for lab, m in [('ALL', v.index.notna()), ('IS', v.index < '2021-01-01'), ('OOS', v.index >= '2021-01-01')]:
            rows.append(dict(set='DUZ_20', sym=sym, sample=lab, **summarize(v[m])))
    A = pd.DataFrame(rows); print(A.to_string(index=False)); A.to_csv(OUT + '/res_a_replication.csv', index=False)

    # olay bazında tablo
    tb = rat[['ann', 'wd', 'agency', 'dir', 'react']].copy()
    for sym, nm in [('XU100.IS', 'xu100'), ('XBANK.IS', 'xbank')]:
        tb[nm + '_pre5'] = [np.log(px(sym, int(i) - 1, 'c') / px(sym, int(i) - 6, 'c')) for i in rat.react_i]
        tb[nm + '_gap'] = [np.log(px(sym, int(i), 'o') / px(sym, int(i) - 1, 'c')) for i in rat.react_i]
        tb[nm + '_intra0'] = [np.log(px(sym, int(i), 'c') / px(sym, int(i), 'o')) for i in rat.react_i]
        tb[nm + '_o_t2'] = [trade(sym, int(i), 'open', 2) for i in rat.react_i]
        tb[nm + '_strat'] = -tb['dir'] * tb[nm + '_o_t2']
    tb['xu100_h1_t2'] = [trade('XU100.IS', int(i), 'h1', 2) for i in rat.react_i]
    tb['days_t0_t2'] = [(CAL[int(i) + 2] - CAL[int(i)]).days for i in rat.react_i]
    print('\n=== olay bazında (log getiri, %) ===')
    show = tb.copy()
    for c in show.columns:
        if c.startswith('xu') or c.startswith('xb'): show[c] = (100 * show[c]).round(2)
    print(show.to_string(index=False)); tb.to_csv(OUT + '/res_event_table.csv', index=False)
    # olay öncesi 5 gün (t-6 kapanış -> t-1 kapanış, yani olay haftası Cuma kapanışına kadar) not yönünde?
    for nm in ['xu100', 'xbank']:
        s = tb['dir'] * tb[nm + '_pre5']
        print(f'pre5 not yönünde {nm}:', summarize(s, 0), '| 1. tur 19:', summarize(s[tb.react.isin(R1)], 0))
    print('sign(pre5)==dir oranı:', (np.sign(tb.xu100_pre5) == tb.dir).mean().round(2))
    json.dump({'n_rating': int(len(rat))}, open(OUT + '/meta.json', 'w'))
