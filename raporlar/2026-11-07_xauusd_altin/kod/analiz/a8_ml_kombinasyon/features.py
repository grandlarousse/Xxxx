"""a8_ml_kombinasyon — öznitelik kurucu.
Bütün öznitelikler gün t 15:00 UTC karar anından ÖNCE (ya da tam 15:00'te kapanan Dukascopy saatlik barıyla) bilinir.
Spot türevli öznitelikler 2010'dan başlayan spot panel endeksinde (Dukascopy iş günleri) hesaplanır, sonra VİOP günlerine
as-of (ffill: yalnız geçmiş bilgi) taşınır. VİOP'a özgü öznitelikler yalnızca t-1 değerlerinden kurulur.
Çıktı: build() -> (X_spot, X_viop, info DataFrame); info: öznitelik, grup, kaynak, bilgi zamanı (UTC), set (A=2010+, B=VİOP).
"""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/code")
from lib_altin import load_viop, load_spot

T15 = "gün t 15:00 UTC (Dukascopy saatlik bar 14:00–15:00 kapanışı)"
YUS = "ABD kapanışı t-1 (≈20:00–21:15 UTC t-1; y_*_avail < t 15:00 doğrulandı)"
UST = "ABD Hazinesi t-1 değeri (t-1 22:00 UTC)"
COT = "CFTC Salı pozisyonu, Cuma 21:00 UTC (gün t'den ≥1 gün önce; kapanma dönemleri hariç)"
SHF = "SHFE gündüz kapanışı gün t 07:00 UTC + Dukascopy 07:00 UTC"


def rsi(p, n):
    d = p.diff(); up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean(); dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    return 100 - 100 / (1 + up / dn)


def spot_features(s):
    F, info = {}, []

    def add(name, x, group, src, t, fset="A"):
        F[name] = x; info.append(dict(feature=name, group=group, source=src, info_time_utc=t, set=fset))

    p = s.xau_p15.ffill(limit=3); lp = np.log(p); r1 = lp.diff()
    # (i) fiyat
    for k in [1, 2, 3, 5, 10, 20, 60, 120, 250]:
        add(f"px_r{k}", lp - lp.shift(k), "fiyat", "xau_p15", T15)
    v20 = r1.rolling(20).std(); v60 = r1.rolling(60).std()
    add("px_vol20", v20, "fiyat", "xau_p15", T15); add("px_vol60", v60, "fiyat", "xau_p15", T15)
    add("px_volratio", np.log(v20 / v60), "fiyat", "xau_p15", T15)
    add("px_r1z", r1 / v60, "fiyat", "xau_p15", T15); add("px_r5z", (lp - lp.shift(5)) / (v60 * np.sqrt(5)), "fiyat", "xau_p15", T15)
    for n in [5, 10, 20, 50, 100, 200]:
        add(f"px_ma{n}", lp - np.log(p.rolling(n).mean()), "fiyat", "xau_p15", T15)
    add("px_rsi2", rsi(p, 2), "fiyat", "xau_p15", T15); add("px_rsi14", rsi(p, 14), "fiyat", "xau_p15", T15)
    add("px_dd250", lp - np.log(p.rolling(250).max()), "fiyat", "xau_p15", T15)
    add("px_hi20", lp - np.log(p.rolling(20).max()), "fiyat", "xau_p15", T15)
    # (iv) seans segmentleri (spot saatlik, hepsi <= t 15:00)
    seg = {
        "seg_uspm_prev": (np.log(s.xau_p20_prev / s.xau_p15_prev), "xau_p15_prev→xau_p20_prev", "t-1 20:00 UTC"),
        "seg_eve": (np.log(s.xau_p00 / s.xau_p20_prev), "xau_p20_prev→xau_p00", "t 00:00 UTC"),
        "seg_asia": (np.log(s.xau_p07 / s.xau_p00), "xau_p00→xau_p07", "t 07:00 UTC"),
        "seg_london": (np.log(s.xau_p12 / s.xau_p07), "xau_p07→xau_p12", "t 12:00 UTC"),
        "seg_nyam": (np.log(s.xau_p15 / s.xau_p12), "xau_p12→xau_p15", T15),
        "seg_last1h": (np.log(s.xau_p15 / s.xau_p14), "xau_p14→xau_p15", T15),
    }
    for k, (x, src, t) in seg.items():
        add(k, x, "seans", src, t)
    asia_like = seg["seg_eve"][0] + seg["seg_asia"][0]  # 20:00 t-1 → 07:00 t
    us_like = seg["seg_nyam"][0] + seg["seg_uspm_prev"][0]  # t 12-15 + (t-1 15-20)
    add("seg_asia_sum20", asia_like.rolling(20, min_periods=15).mean() * 20, "seans", "xau_p20_prev→xau_p07 20g toplam", "t 07:00 UTC")
    add("seg_us_sum20", us_like.rolling(20, min_periods=15).mean() * 20, "seans", "(t-1 15→20)+(t 12→15) 20g toplam", T15)
    add("seg_asia_sum5", asia_like.rolling(5, min_periods=4).mean() * 5, "seans", "xau_p20_prev→xau_p07 5g toplam", "t 07:00 UTC")
    add("seg_us_sum5", us_like.rolling(5, min_periods=4).mean() * 5, "seans", "(t-1 15→20)+(t 12→15) 5g toplam", T15)
    # (ii) çapraz varlık, Yahoo t-1 kapanış değişimleri
    yl = {"dxy": "y_DX_Y_NYB", "spx": "y__GSPC", "silver": "y_SI_F", "gdx": "y_GDX", "oil": "y_CL_F", "copper": "y_HG_F",
          "tlt": "y_TLT", "eem": "y_EEM", "gld": "y_GLD", "aud": "y_AUDUSD_X", "btc": "y_BTC_USD"}
    for nm, col in yl.items():
        ly = np.log(s[col])
        fs = "B" if nm == "btc" else "A"
        if nm != "gld":
            add(f"xa_{nm}_d1", ly.diff(), "capraz_yahoo", col, YUS if nm not in ("aud", "btc") else "Yahoo t-1 24:00 UTC bar sonu (+1s) → t-1", fs)
            add(f"xa_{nm}_d5", ly - ly.shift(5), "capraz_yahoo", col, YUS if nm not in ("aud", "btc") else "Yahoo t-1 24:00 UTC bar sonu (+1s) → t-1", fs)
    add("xa_gdx_rel1", np.log(s.y_GDX).diff() - np.log(s.y_GLD).diff(), "capraz_yahoo", "y_GDX,y_GLD", YUS)
    add("xa_gdx_rel5", np.log(s.y_GDX / s.y_GDX.shift(5)) - np.log(s.y_GLD / s.y_GLD.shift(5)), "capraz_yahoo", "y_GDX,y_GLD", YUS)
    gsr = np.log(s.y_GLD / s.y_SLV)
    add("xa_gsratio_dev60", gsr - gsr.rolling(60).mean(), "capraz_yahoo", "y_GLD/y_SLV", YUS)
    # oynaklık endeksleri
    lv = np.log(s.y__VIX); lg = np.log(s.y__GVZ)
    add("vol_vix_d1", lv.diff(), "oynaklik", "y__VIX", "VIX kapanışı t-1 (16:15 ET)")
    add("vol_vix_dev60", lv - lv.rolling(60).mean(), "oynaklik", "y__VIX", "VIX kapanışı t-1 (16:15 ET)")
    add("vol_gvz_d1", lg.diff(), "oynaklik", "y__GVZ", "GVZ kapanışı t-1 (16:15 ET)")
    add("vol_gvz_dev60", lg - lg.rolling(60).mean(), "oynaklik", "y__GVZ", "GVZ kapanışı t-1 (16:15 ET)")
    add("vol_gvz_vrp", s.y__GVZ / 100 - v20 * np.sqrt(252), "oynaklik", "y__GVZ, xau_p15", "GVZ t-1 / spot t 15:00")
    # faizler
    for c in ["nom10", "real10", "be10", "nom2"]:
        add(f"rt_{c}_d1", s[f"ust_{c}"].diff(), "faiz", f"ust_{c}", UST)
        add(f"rt_{c}_d5", s[f"ust_{c}"].diff(5), "faiz", f"ust_{c}", UST)
    add("rt_curve_2s10s_d5", (s.ust_nom10 - s.ust_nom2).diff(5), "faiz", "ust_nom10-ust_nom2", UST)
    # (iii) COT
    mm = s.cot_gold_mm_net_oi
    add("cot_mm_lvl", mm, "cot", "cot_gold_mm_net_oi", COT)
    add("cot_mm_z52", (mm - mm.rolling(260, min_periods=150).mean()) / mm.rolling(260, min_periods=150).std(), "cot", "cot_gold_mm_net_oi", COT)
    add("cot_mm_chg1w", mm - mm.shift(5), "cot", "cot_gold_mm_net_oi", COT)
    sw = s.cot_gold_swap_net / s.cot_gold_oi
    add("cot_swap_z52", (sw - sw.rolling(260, min_periods=150).mean()) / sw.rolling(260, min_periods=150).std(), "cot", "cot_gold_swap_net/oi", COT)
    # Şanghay primi
    cnh = s.dk_USDCNH_p07.where(s.dk_USDCNH_p07.notna(), s.y_CNY_X)
    same = pd.to_datetime(s.shfe_AU0_date) == s.index
    prem = (np.log(s.shfe_AU0_c * 31.1035 / cnh) - np.log(s.xau_p07)).where(same)
    add("sh_prem_dev20", prem - prem.rolling(20, min_periods=10).mean(), "shfe", "shfe_AU0_c, USDCNH 07:00, xau_p07", SHF)
    add("sh_prem_d1", prem - prem.ffill().shift(1), "shfe", "shfe_AU0_c, USDCNH 07:00, xau_p07", SHF)
    add("sh_prem_d5", prem - prem.ffill().shift(5), "shfe", "shfe_AU0_c, USDCNH 07:00, xau_p07", SHF)
    # takvim
    idx = s.index
    dow = pd.Series(idx.dayofweek, index=idx)
    for i, nm in enumerate(["mon", "tue", "wed", "thu"]):
        add(f"cal_{nm}", (dow == i).astype(float), "takvim", "takvim", "önceden bilinir")
    mon = pd.Series(idx.month, index=idx)
    nxt_mon = mon.shift(-1).fillna(mon.iloc[-1] % 12 + 1)  # sonraki işlem gününün ayı (takvim, önceden bilinir)
    first = (mon != mon.shift(1)).astype(int)
    pos_in_m = first.groupby(first.cumsum()).cumcount() + 1  # ay içindeki işlem günü sırası (1 = ilk gün)
    add("cal_tom", (((nxt_mon != mon)) | (pos_in_m <= 3)).astype(float), "takvim", "takvim (ay sonu son gün + ilk 3 gün)", "önceden bilinir")
    add("cal_msin", np.sin(2 * np.pi * mon / 12), "takvim", "ay", "önceden bilinir")
    add("cal_mcos", np.cos(2 * np.pi * mon / 12), "takvim", "ay", "önceden bilinir")
    # jeopolitik risk (DÜŞÜK güven)
    add("gpr_ma7_30", np.log(s.gpr_GPRD_MA7 / s.gpr_GPRD_MA30), "gpr", "gpr_GPRD_MA7/MA30", "D+1 23:00 UTC (as-of)")  # NOT: panelde gpr_* sabit (veri hatası) → standardize aşamasında düşer
    # (ii-b) Dukascopy 15:00 UTC 24 saatlik değişimler (2016+; set B)
    dk = {"dk_dxy": "DOLLARIDXUSD", "dk_eur": "EURUSD", "dk_jpy": "USDJPY", "dk_tbond": "USTBONDTRUSD", "dk_spx": "USA500IDXUSD",
          "dk_silver": "XAGUSD", "dk_copper": "COPPERCMDUSD", "dk_btc": "BTCUSD", "dk_cnh": "USDCNH", "dk_try": "USDTRY"}
    for nm, sym in dk.items():
        x = np.log(s[f"dk_{sym}_p15"]); add(f"{nm}_d1", x - x.shift(1), "capraz_dk15", f"dk_{sym}_p15", T15, "B")
    X = pd.DataFrame(F); X = X.replace([np.inf, -np.inf], np.nan)
    return X, pd.DataFrame(info)


def viop_features(d):
    F, info = {}, []

    def add(name, x, src, t):
        F[name] = x; info.append(dict(feature=name, group="viop_t1", source=src, info_time_utc=t, set="B"))
    add("vp_dte", d.v_dte.astype(float), "v_dte (vade takvimi)", "önceden bilinir")
    add("vp_roll", (d.v_code != d.v_code.shift(1)).astype(float), "v_code (aktif = t-1 en büyük AP)", "t-1 bülteni")
    add("vp_logvol_chg_l1", np.log(d.v_tot_volume.replace(0, np.nan)).diff().shift(1), "v_tot_volume t-1", "t-1 15:15 UTC")
    add("vp_logoi_chg_l1", np.log(d.v_tot_oi.replace(0, np.nan)).diff().shift(1), "v_tot_oi t-1", "t-1 bülten")
    add("vp_basis_l1", (np.log(d.v_settle) - np.log(d.xau_p15)).shift(1), "v_settle t-1 − xau_p15 t-1", "t-1 15:10 UTC")
    trp = d.tr_prem_matched.shift(1)
    add("tr_prem_dev20_l1", trp - trp.rolling(20, min_periods=10).mean(), "tr_prem_matched t-1", "t-1 15:10 UTC")
    add("tr_usdtry_ret_l1", d.vo_usdtry_ret.shift(1), "vo_usdtry_ret t-1", "t-1 15:10 UTC")
    X = pd.DataFrame(F).replace([np.inf, -np.inf], np.nan)
    return X, pd.DataFrame(info)


def build():
    s = load_spot(); d = load_viop()
    Xs, info_s = spot_features(s)
    # VİOP günlerine as-of taşı (Paskalya/Noel gibi spotun olmadığı VİOP günlerinde son spot gününün öznitelikleri)
    Xs_v = Xs.reindex(Xs.index.union(d.index)).ffill(limit=2).reindex(d.index)
    # takvim özniteliklerini VİOP endeksinde yeniden hesapla
    Xv, info_v = viop_features(d)
    Xs_v = Xs_v.copy()
    idx = d.index; dow = pd.Series(idx.dayofweek, index=idx)
    for i, nm in enumerate(["mon", "tue", "wed", "thu"]):
        Xs_v[f"cal_{nm}"] = (dow == i).astype(float)
    mon = pd.Series(idx.month, index=idx); nxt = mon.shift(-1).fillna(mon.iloc[-1] % 12 + 1)
    first = (mon != mon.shift(1)).astype(int); pim = first.groupby(first.cumsum()).cumcount() + 1
    Xs_v["cal_tom"] = ((nxt != mon) | (pim <= 3)).astype(float)
    XV = pd.concat([Xs_v, Xv], axis=1)
    info = pd.concat([info_s, info_v], ignore_index=True)
    return Xs, XV, info, s, d


FSET_A = None
def feature_sets(info):
    A = info.loc[info.set == "A", "feature"].tolist()
    B = info.feature.tolist()
    return A, B


if __name__ == "__main__":
    Xs, XV, info, s, d = build()
    out = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a8_ml_kombinasyon"
    # Yahoo bilgi zamanı doğrulaması: kullanılan her y_* sütununun _avail damgası < gün t 15:00 UTC
    chk = []
    for c in ["y_DX_Y_NYB", "y__GSPC", "y_SI_F", "y_GDX", "y_CL_F", "y_HG_F", "y_TLT", "y_EEM", "y_GLD", "y_SLV", "y_AUDUSD_X", "y_BTC_USD", "y__VIX", "y__GVZ", "y_CNY_X"]:
        av = pd.to_datetime(s[f"{c}_avail"]); m_ = av.notna(); ok = (av[m_] < (s.index + pd.Timedelta(hours=15))[m_.values]).mean()
        lag_h = ((s.index + pd.Timedelta(hours=15)) - av).dt.total_seconds().div(3600)
        chk.append(dict(col=c, frac_before_cutoff=round(float(ok), 4), min_lead_hours=round(float(lag_h.min()), 1), median_lead_hours=round(float(lag_h.median()), 1)))
    cot_ok = ((pd.to_datetime(s.cot_gold_reportdate) + pd.Timedelta(days=3, hours=21)) < s.index + pd.Timedelta(hours=15)).mean()
    sh_ok = (pd.to_datetime(s.shfe_AU0_date) <= s.index).mean()
    chk.append(dict(col="cot_gold_reportdate+3g 21:00", frac_before_cutoff=round(float(cot_ok), 4)))
    chk.append(dict(col="shfe_AU0_date<=t (07:00 UTC)", frac_before_cutoff=round(float(sh_ok), 4)))
    pd.DataFrame(chk).to_csv(f"{out}/bilgi_zamani_kontrol.csv", index=False)
    info.to_csv(f"{out}/oznitelik_bilgi_zamani.csv", index=False)
    print(pd.DataFrame(chk).to_string())
    print(info.groupby(["set", "group"]).size())
    print(XV.loc["2020":].notna().mean().sort_values().head(15))
    print(Xs.loc["2011":"2016", [f for f in info.feature if info.set[info.feature == f].iloc[0] == "A"]].notna().mean().sort_values().head(10))
