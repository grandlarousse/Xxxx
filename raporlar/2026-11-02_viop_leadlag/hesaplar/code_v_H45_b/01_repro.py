"""01: bağımsız yeniden üretim (H45 a/b/c) + veri/zamanlama denetimi."""
import sys; sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_H45_b')
from blib import *

W = {'TUPRS': .33, 'YKBNK': .24, 'FROTO': .20, 'ARCLK': .07, 'TOASO': .04, 'AYGAZ': .03, 'TTRAK': .03, 'OTKAR': .02}


def basket_gap(w, legacy=False, strict=False, col='gap'):
    G = pd.concat({k: bist(k, legacy, strict)[col] for k in w}, axis=1)
    wv = pd.Series(w)
    m = G.notna()
    num = (G.fillna(0) * wv).sum(1)
    den = (m * wv).sum(1)
    out = num / den
    out[den < 0.7] = np.nan  # ağırlığın %70'i yoksa NaN
    return out


if __name__ == '__main__':
    for legacy in (True, False):
        print(f'\n===== temizlik: {"LEGACY ±10,5" if legacy else "REJİM (2020-03 öncesi ±20,5)"} =====')
        K = bist('KCHOL', legacy)
        nav = basket_gap(W, legacy)
        sig = nav - K['gap']
        print('(a) sig=NAVgap-Kgap -> Kintra :', ct3(K['intra'], sig))
        yr = yearly(K['intra'], sig)
        print('    yıllar:', yr.round(3).to_dict())
        r = reg(K['intra'], {'nav': nav, 'kgap': K['gap']}, T0)
        print('    Kintra ~ NAVgap + Kgap: b', {k: round(v, 3) for k, v in r['b'].items()}, 't', {k: round(v, 2) for k, v in r['t'].items()})
        E = bist('ENKAI', legacy)
        tur, tui, tun = us_lag('TUR')
        usd, usd_same = fx_lag('TRY=X')
        print('(b) TUR_{t-1} -> Eintra      :', ct3(E['intra'], tur))
        print('    TUR_{t-1} -> Egap        :', ct3(E['gap'], tur))
        print('(c) USD_{t-1} -> Eintra      :', ct3(E['intra'], usd))
        tur12, _, _ = us_lag('TUR', clip_sd=12)
        print('    (b) 12σ kırpılmış TUR     :', ct3(E['intra'], tur12))
        # 12σ kırpılmış USD (iddia benzeri)
        sd = usd.rolling(250, min_periods=60).std().shift(1)
        usd12 = usd.where(~((usd.abs() > 12 * sd) & sd.notna()))
        print('    (c) 12σ kırpılmış USD     :', ct3(E['intra'], usd12))
        print('        kırpılan günler:', list(usd[(usd.abs() > 12 * sd) & sd.notna() & (usd.index >= T0)].index.date))
    # zaman denetimi: TRY=X günlük c ile h1 00:00 / 15:00 karşılaştırma
    h = load('TRY=X', 'h1')['c']
    d = load('TRY=X')['c']
    h00 = h[h.index.hour == 0]; h00.index = h00.index.tz_localize(None).normalize()
    h15 = h[h.index.hour == 15]; h15.index = h15.index.tz_localize(None).normalize()
    j = pd.concat([d.rename('d'), h00.rename('h00'), h15.rename('h15')], axis=1).dropna()
    print('\nTRY=X günlük c vs h1 00:00 medyan |fark| bps:', round(1e4 * np.median(np.abs(np.log(j.d / j.h00))), 2),
          ' vs 15:00:', round(1e4 * np.median(np.abs(np.log(j.d / j.h15))), 2), ' n', len(j))
    # TUR günlük o: ABD seans açılışı mı? h1 ilk bar ile karşılaştır
    th = load('TUR', 'h1')
    first = th.groupby(th.index.tz_convert('America/New_York').date)['o'].first()
    first.index = pd.DatetimeIndex(first.index)
    td = load('TUR')['o']
    jj = pd.concat([td.rename('d'), first.rename('h')], axis=1).dropna()
    print('TUR günlük o vs h1 ilk bar o: medyan |fark| bps', round(1e4 * np.median(np.abs(np.log(jj.d / jj.h))), 2), 'n', len(jj))
