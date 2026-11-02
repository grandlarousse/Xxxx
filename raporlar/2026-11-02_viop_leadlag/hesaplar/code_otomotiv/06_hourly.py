"""Saatlik kesin hizalama (2023-11+; h1 bar zaman damgası = bar başlangıcı UTC, kapanış = başlangıç+60dk).
Her BIST günü t için:
  r_in(t)  = ln P_X(15:00 UTC, t) / P_X(15:00 UTC, t-1)  -> BIST cc_t ile GERÇEK senkron getiri
  r_ovn(t) = ln P_X(06:30 UTC, t) / P_X(15:00 UTC, t-1)  -> BIST kapanışı(t-1) ile açılışı(t) arasındaki sürücü hareketi (açılıştan önce bilinir)
  (ABD hissesi için r_ovn = BIST kapanışından sonraki ABD seansı; FX/ES için Asya gecesi dahil)
Testler: corr(cc_t, r_in) vs günlük lag0 corr; r_ovn -> gap_t (fiyatlanma), r_ovn -> intra_t (işlenebilir), XU100 gap ve kendi gap kontrollü.
Çıktı: res/hourly_align.csv"""
from common import *
H1 = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data/h1/'

def snap(sym, hh, mm):
    """BIST günü t için hh:mm UTC anına kadar kapanmış son h1 barın kapanışı (bayatlık filtresi YOK, 20 saat sınırı)."""
    h = pd.read_parquet(H1 + sym + '.parquet').sort_index()
    end = h.index + pd.Timedelta(minutes=60)
    s = pd.Series(h['c'].values, index=end)
    cal = ll.bist_cal(); cal = cal[cal >= s.index.tz_convert(None).min().normalize()]
    tg = pd.DatetimeIndex(cal + pd.Timedelta(hours=hh, minutes=mm)).tz_localize('UTC')
    pos = s.index.searchsorted(tg, side='right') - 1
    v = np.where(pos >= 0, s.values[np.clip(pos, 0, None)], np.nan)
    age = (tg - s.index[np.clip(pos, 0, None)]).total_seconds() / 3600
    v = np.where(age > 20, np.nan, v)
    return pd.Series(v, index=cal)

DRV = ['F', 'STLA', 'WHR', 'ETN', 'VRT', 'HUBB', 'PCAR', 'VOW3.DE', 'STLAM.MI', 'RNO.PA', 'EXV5.DE', 'ELUX-B.ST', 'ENR.DE', 'SU.PA',
       'ABBN.SW', 'IVG.MI', 'DTG.DE', 'EURUSD=X', 'EURTRY=X', 'TRY=X', 'ES=F', 'HG=F', 'BTC-USD']
xg = D('XU100')['gap']
rows = []
for x in DRV:
    try:
        p15 = snap(x, 15, 0); p0630 = snap(x, 6, 30)
    except Exception as e: print('skip', x, e); continue
    r_in = np.log(p15).diff(); r_ovn = np.log(p0630 / p15.shift(1))
    r_in = r_in.where(r_in != 0); r_ovn = r_ovn.where(r_ovn != 0)
    for st in STOCKS:
        d = D(st); d = d[d.index >= r_in.dropna().index.min()]
        o = {'stock': st, 'driver': x}
        o['sync_h1_c'], o['sync_h1_t'], o['n'] = corr_t(d['cc'], r_in)
        o['sync_daily_c'], _, _ = corr_t(d['cc'], R(x), start=str(r_in.dropna().index.min().date()))
        o['sync_h1_pc'], o['sync_h1_pc_t'], _ = pcorr(d['cc'], r_in, [R('XU100')])
        o['ovn_gap_c'], o['ovn_gap_t'], _ = corr_t(d['gap'], r_ovn)
        o['ovn_intra_c'], o['ovn_intra_t'], _ = corr_t(d['intra'], r_ovn)
        o['ovn_intra_pc'], o['ovn_intra_pc_t'], _ = pcorr(d['intra'], r_ovn, [xg, d['gap']])
        rows.append(o)
Hh = pd.DataFrame(rows); Hh.to_csv(os.path.join(RES, 'hourly_align.csv'), index=False)
print('çift:', len(Hh), '| medyan ovn->gap t:', Hh.ovn_gap_t.median().round(2), '| |ovn->intra_pc t|>2:', int((Hh.ovn_intra_pc_t.abs() > 2).sum()))
print(Hh.sort_values('sync_h1_pc', key=abs, ascending=False).head(12)[['stock', 'driver', 'n', 'sync_daily_c', 'sync_h1_c', 'sync_h1_pc', 'ovn_gap_t', 'ovn_intra_t', 'ovn_intra_pc_t']].round(3).to_string(index=False))
print(Hh[Hh.ovn_intra_pc_t.abs() > 2][['stock', 'driver', 'n', 'ovn_gap_t', 'ovn_intra_c', 'ovn_intra_pc_t']].round(3).to_string(index=False))
