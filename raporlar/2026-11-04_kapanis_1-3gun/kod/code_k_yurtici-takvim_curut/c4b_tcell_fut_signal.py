"""TCELL–TTKOM: tarayıcının VİOP testi sinyali VADELİ uzlaşma getirilerinden kuruyor (u = r_F,A − β r_F,B) ve E0'da AYNI uzlaşmadan giriyor.
Uzlaşma seans sonunda (VWAP) belirlenir; aynı fiyatla hem sinyal hem giriş = ileriye bakma/gürültü dönüşü. Burada: vadeli-sinyal vs spot-sinyal, E0 vs E2."""
from curlib import *
cal = vcal(); FW = pd.read_parquet(RES + '/_fwd_cache.parquet')
def fw(u, h, e): return FW[f'{u}|{h}|{e}']
def beta(y, x, w=250, mp=120): return (y.rolling(w, min_periods=mp).cov(x) / x.rolling(w, min_periods=mp).var()).shift(1)
ra_s = spot_ret('TCELL').reindex(cal); rb_s = spot_ret('TTKOM').reindex(cal)
bb = beta(ra_s, rb_s).clip(0.3, 2.0)
ra_f = FW['TCELL|0|r_front']; rb_f = FW['TTKOM|0|r_front']
out = []
for src, ra, rb in [('VADELİ-sinyal', ra_f, rb_f), ('SPOT-sinyal', ra_s, rb_s)]:
    u = ra - bb * rb
    Sx = u.fillna(0).cumsum().where(u.notna())
    for L, thr in [(20, 2.0), (20, 1.5), (60, 2.0)]:
        z = (Sx - Sx.rolling(L, min_periods=int(L * .8)).mean()) / Sx.rolling(L, min_periods=int(L * .8)).std()
        on = (z.abs() > thr).fillna(False).values; d = cal[on]; sd = -np.sign(z.values[on]); bv = bb.reindex(d).fillna(1).values
        for h in [2, 3]:
            for e in ['E0', 'E2']:
                x = sd * (fw('TCELL', h, e).reindex(d).values - bv * fw('TTKOM', h, e).reindex(d).values) / (1 + bv)
                o = summary(d, x, h); reg('tcell2', f'{src} Z{L}>{thr}', h, e, o)
                out.append(f'{src:14s} Z{L}>{thr} {e} h{h}: n={o["n"]} brüt {o["gross"]:+.1f} t {o["t"]:.2f} | IS {o["IS"]:+.1f} (t {o["IS_t"]:.2f}) OOS {o["OOS"]:+.1f} (t {o["OOS_t"]:.2f}) | 17-19 {o["2017-19"]:+.0f} 20-21 {o["2020-21"]:+.0f} 22-23 {o["2022-23"]:+.0f} 24-26 {o["2024-26"]:+.0f} | top10 hariç {o.get("ex_top10", np.nan):+.1f} (t {o.get("ex_top10_t", np.nan):.2f})')
for o in out: print(o)
# 2017-19 vadeli likiditesi: işlem yapılmayan (trades=0) ön vade günleri payı
for u_ in ['TCELL', 'TTKOM']:
    F = fut(u_); tr, _ = F.front_series('trades', min_dte=3)
    print(u_, 'ön vade işlem=0 gün payı yıllara göre:', (tr.fillna(0) == 0).groupby(tr.index.year).mean().round(2).to_dict())
save('tcell2')
