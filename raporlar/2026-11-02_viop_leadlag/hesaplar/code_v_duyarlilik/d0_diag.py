"""Tanı: v3->v4 hangi günleri değiştiriyor? (a) hacim0 & h!=l günleri (v3 atar, v4 tutar); (b) 2020-03-13 öncesi %10,5–20,5 bandı (v3 NaN, v4 tutar).
Ayrıca bant içindeki 2020 öncesi negatif sıçramalardan bedelsiz/bölünme şüphelileri (piyasa sakin + hareketin tamamı gap)."""
import vers, numpy as np, pandas as pd
EXTRA = ["XU100", "XBANK", "XU030", "ISDMR", "CCOLA", "HEKTS", "KMPUR", "SMRTG", "AKSA", "KORDS"]
rows = []; susp = []
xu = vers._raw("XU100.IS"); rxu = np.log(xu["adj"]).diff()
for s in vers.VIOP + EXTRA:
    sym = s + ".IS"; d = vers._raw(sym)
    v = d["v"].fillna(0); hl = d["h"] == d["l"]
    volok = v.gt(0).mean() > 0.5
    z = v <= 0
    last1y = d.index >= d.index.max() - pd.DateOffset(years=1); last3y = d.index >= d.index.max() - pd.DateOffset(years=3)
    r = np.log(d["adj"]).diff()  # ham (filtre öncesi) günlük getiri, kendi satır sırasıyla
    pre = d.index < vers.REG
    band = pre & (((r > np.log(1.105)) & (r <= np.log(1.205))) | ((r < np.log(0.895)) & (r >= np.log(0.795))))
    gt20 = pre & ((r > np.log(1.205)) | (r < np.log(0.795)))
    post_bad = (~pre) & ((r > np.log(1.105)) | (r < np.log(0.895)))
    rows.append(dict(stock=s, vol_filter_active=volok, n=len(d), v0=int(z.sum()), v0_hl=int((z & hl).sum()), v0_range=int((z & ~hl).sum()),
                     v0_range_1y=int((z & ~hl & last1y).sum()), n_1y=int(last1y.sum()), v0_range_3y=int((z & ~hl & last3y).sum()),
                     pre_band=int(band.sum()), pre_band_up=int((band & (r > 0)).sum()), pre_band_dn=int((band & (r < 0)).sum()),
                     pre_band_2014_20=int((band & (d.index >= "2014-01-01")).sum()), pre_gt20=int(gt20.sum()), post_bad=int(post_bad.sum())))
    # şüpheli kurumsal işlem: band & r<0 & |XU100|<%3 & açılış zaten önceki kapanışın %9'undan fazla aşağıda & adj/c oranı değişmemiş
    gap_raw = np.log(d["o"] / d["c"].shift(1)); ratio = (d["adj"] / d["c"]); rchg = np.log(ratio).diff().abs()
    for t in d.index[band & (r < 0)]:
        susp.append(dict(stock=s, date=t.date(), r=float(r[t]), xu100=float(rxu.reindex([t]).iloc[0]) if t in rxu.index else np.nan,
                         gap_raw=float(gap_raw[t]), intra=float(np.log(d["c"][t] / d["o"][t])), next5=float(r.shift(-1).rolling(5).sum().shift(-4)[t]) if True else np.nan,
                         adj_c_ratio_chg=float(rchg[t]), v=float(d["v"][t])))
D = pd.DataFrame(rows); D.to_csv(vers.RES + "/d0_diag.csv", index=False)
S = pd.DataFrame(susp); S["calm_mkt"] = S["xu100"].abs() < 0.03; S["all_gap"] = (S["gap_raw"] < -0.09) & (S["intra"].abs() < 0.03)
S["suspect_CA"] = S["calm_mkt"] & S["all_gap"]
S.to_csv(vers.RES + "/d0_band_negative_days.csv", index=False)
pd.set_option("display.width", 250)
print(D.to_string())
print("\nBant içi 2020 öncesi negatif günler:", len(S), " şüpheli kurumsal işlem (piyasa sakin & tamamı gap):", int(S.suspect_CA.sum()))
print(S[S.suspect_CA].to_string())
print(D[["v0_range", "v0_range_1y", "pre_band", "pre_band_2014_20"]].sum())
