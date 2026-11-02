"""NAV iskontosu (piyasa değeri bazlı, yaklaşık) dinamikleri ve ana/yavru oran (spread) ortalamaya dönüşü.
NAV endeksi: referans NAV ağırlıklarıyla al-tut sepeti (yalnız halka açık iştirakler + DOHOL'de USD nakit). Ağırlıklar yaklaşık (kaynak: holding sunumları/R1/aracı kurum notları).
D_t = log P_H - log NAV_t (sabit hariç). Sapma: D_t - MA60(D) ve z250. Tahmin: holding gün-içi t+1, holding cc t+1..t+5 ve göreli (H - NAV) t+1..t+5."""
from gx import *
from statsmodels.tsa.stattools import adfuller
NAVW = {
 'KCHOL': {'TUPRS': .33, 'FROTO': .20, 'YKBNK': .24, 'ARCLK': .07, 'TOASO': .04, 'AYGAZ': .03, 'OTKAR': .02, 'TTRAK': .03},
 'SAHOL': {'AKBNK': .45, 'ENJSA': .10, 'CIMSA': .03, 'BRISA': .03, 'KORDS': .03, 'AKGRT': .03, 'AGESA': .03, 'AKCNS': .02},
 'AGHOL': {'AEFES': .43, 'MGROS': .33, 'ASUZU': .03, 'ADEL': .01},
 'DOHOL': {'GWIND': .12, 'TRY=X': .45},
 'ECZYT': {'ECILC': .70, 'INTEM': .05},
 'ISCTR': {'SISE': .30, 'ISMEN': .25, 'ANHYT': .10, 'ANSGR': .10, 'TSKB': .08, 'ISGYO': .02, 'ISFIN': .02},  # banka: iştirak payı ~%40-50 -> 'yavru sepeti'
 'TRENJ': {'TRMET': 1.0}, 'TRMET': {'TRALT': 1.0}, 'VESTL': {'VESBE': 1.0}, 'BRYAT': {'BRSAN': 1.0}, 'TEHOL': {'TERA': 1.0}, 'ALARK': {'ALCAR': .5, 'ALGYO': .5}, 'AEFES': {'CCOLA': 1.0},
}
def rr(s): return R(s) if s.endswith('=X') is False else ll.ret(s)
def nav_series(h):
    W = NAVW[h]; rets = pd.concat({k: (ll.ret(k) if k.endswith('=X') else R(k)) for k in W}, axis=1)
    rets = rets[rets.index >= pd.Timestamp('2010-01-01')]
    w0 = pd.Series(W, dtype=float); w0 = w0 / w0.sum()
    # al-tut: her bileşen için kümülatif getiri (eksik başlangıçta ağırlık sıfır->yeniden normalize)
    lvl = np.exp(rets.fillna(0).cumsum())
    avail = rets.notna().cumsum() > 0
    val = (lvl * w0).where(avail, 0.0)
    # yeni listelenen bileşen girdiğinde zinciri koru: getiri bazlı birleştir
    wt = val.shift(1).div(val.shift(1).sum(axis=1), axis=0)
    navr = (wt * rets.fillna(0)).sum(axis=1)
    navr[wt.sum(axis=1) == 0] = np.nan
    return navr
def analyze(h):
    navr = nav_series(h); hr = R(h); dh = DC(h)
    df = pd.concat([hr.rename('h'), navr.rename('nav'), R('XU100').rename('m'), dh['intra'].rename('hi'), dh['gap'].rename('hg')], axis=1)
    df = df[df.index >= max(pd.Timestamp('2010-01-01'), navr.dropna().index.min())].dropna(subset=['h', 'nav'])
    df['D'] = (df['h'] - df['nav']).cumsum()                    # log iskonto (sabit hariç)
    df['dev60'] = df['D'] - df['D'].rolling(60, min_periods=40).mean()
    df['z250'] = (df['D'] - df['D'].rolling(250, min_periods=120).mean()) / df['D'].rolling(250, min_periods=120).std()
    b = df['h'].rolling(250, min_periods=120).cov(df['nav']) / df['nav'].rolling(250, min_periods=120).var()
    df['beta_nav'] = b.shift(1)
    f5 = df['h'].shift(-1).rolling(5).sum().shift(-4); n5 = df['nav'].shift(-1).rolling(5).sum().shift(-4)
    df['f_hi1'] = df['hi'].shift(-1); df['f_h5'] = f5; df['f_rel5'] = f5 - df['beta_nav'] * n5
    df['f_rel1i'] = df['hi'].shift(-1)  # gün içi tek bacak
    o = {'holding': h, 'n': len(df), 'start': df.index[0].date(), 'corr_h_nav': df['h'].corr(df['nav']),
         'pc_h_nav': ll.partial_corr(df['h'], df['nav'], [df['m']])[0], 'beta_h_nav': np.polyfit(df['nav'], df['h'], 1)[0]}
    # dev60 AR(1) yarı ömür (günlük) ve ADF (D seviyesi)
    x = df['dev60'].dropna(); phi = np.corrcoef(x[:-1], x[1:])[0, 1]; o['dev60_ar1'] = phi; o['halflife_d'] = np.log(.5) / np.log(phi) if 0 < phi < 1 else np.nan
    try: o['adf_p_D'] = adfuller(df['D'].dropna(), maxlag=10, autolag=None)[1]
    except Exception: o['adf_p_D'] = np.nan
    o['D_range_pct'] = 100 * (np.exp(df['D'].max() - df['D'].min()) - 1)
    for tgt in ['f_hi1', 'f_h5', 'f_rel5']:
        for lab, sub in [('', df), ('_IS', df[df.index < SPLIT]), ('_OOS', df[df.index >= SPLIT])]:
            r = nwreg(sub[tgt], sub[['z250']], lags=5 if tgt == 'f_hi1' else 10)
            o[f'{tgt}_t{lab}'] = r[0].tvalues[1] if r else np.nan; o[f'{tgt}_b{lab}'] = r[0].params[1] * 1e4 if r else np.nan
    df.to_parquet(HERE + f'/nav_{h}.parquet')
    # yıllık iskonto değişimi (yüzde): seviye yaklaşık
    yr = df['D'].groupby(df.index.year).last().diff()
    o['D_chg_2025'] = 100 * yr.get(2025, np.nan); o['D_chg_2026'] = 100 * yr.get(2026, np.nan)
    return o
if __name__ == '__main__':
    rows = [analyze(h) for h in NAVW]
    D = pd.DataFrame(rows); D.to_csv(HERE + '/res_nav.csv', index=False)
    pd.set_option('display.width', 250)
    print(D.round(3).T.to_string())
