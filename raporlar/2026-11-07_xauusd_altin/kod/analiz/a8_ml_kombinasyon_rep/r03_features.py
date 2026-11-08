"""Adım 3: bağımsız öznitelik kurucu (analistin features.py'si çalıştırılmadı; tanımlar rapordaki tablodan yeniden yazıldı).
Kaynak: base_spot (kendi ham as-of serilerim: spot saatlik, ust, COT, SHFE, CNH07, DXY) + panel_spot/panel_viop'tan Yahoo y_* (avail < t 15:00
doğrulandı; =X kurları gerçekte D 00:00 UTC fiyatı, varsayılandan erken → muhafazakâr) ve dk_*_p15, VİOP t-1 sütunları.
Çıktı: feat_spot.parquet (set A, spot endeksi), feat_viop.parquet (set A as-of + set B, VİOP endeksi), feat_info.csv"""
import numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"; OUT = f"{S}/out/a8_ml_kombinasyon_rep"
b = pd.read_parquet(f"{OUT}/base_spot.parquet"); v = pd.read_parquet(f"{OUT}/base_viop.parquet")
ps = pd.read_parquet(f"{S}/panel/panel_spot.parquet"); ps.index = pd.to_datetime(ps.index)
pv = pd.read_parquet(f"{S}/panel/panel_viop.parquet"); pv.index = pd.to_datetime(pv.index)
ps = ps.reindex(b.index)
F = {}; G = {}
def add(n, x, g, st="A"): F[n] = x; G[n] = (g, st)

lp = np.log(b.p15.ffill(limit=3)); r = lp.diff()
for k in (1, 2, 3, 5, 10, 20, 60, 120, 250): add(f"px_r{k}", lp - lp.shift(k), "fiyat")
s20, s60 = r.rolling(20).std(), r.rolling(60).std()
add("px_vol20", s20, "fiyat"); add("px_vol60", s60, "fiyat"); add("px_volratio", np.log(s20 / s60), "fiyat")
add("px_r1z", r / s60, "fiyat"); add("px_r5z", (lp - lp.shift(5)) / (s60 * np.sqrt(5)), "fiyat")
P = np.exp(lp)
for n in (5, 10, 20, 50, 100, 200): add(f"px_ma{n}", lp - np.log(P.rolling(n).mean()), "fiyat")
def wilder_rsi(p, n):
    d = p.diff(); a = 1.0 / n
    up = d.clip(lower=0).ewm(alpha=a, adjust=False).mean(); dn = (-d).clip(lower=0).ewm(alpha=a, adjust=False).mean()
    return 100 * up / (up + dn)
add("px_rsi2", wilder_rsi(P, 2), "fiyat"); add("px_rsi14", wilder_rsi(P, 14), "fiyat")
add("px_dd250", lp - np.log(P.rolling(250).max()), "fiyat"); add("px_hi20", lp - np.log(P.rolling(20).max()), "fiyat")
# seans
seg = dict(seg_uspm_prev=np.log(b.p20_prev / b.p15_prev), seg_eve=np.log(b.p00 / b.p20_prev), seg_asia=np.log(b.p07 / b.p00),
           seg_london=np.log(b.p12 / b.p07), seg_nyam=np.log(b.p15 / b.p12), seg_last1h=np.log(b.p15 / b.p14))
for k, x in seg.items(): add(k, x, "seans")
asia = seg["seg_eve"] + seg["seg_asia"]; us = seg["seg_nyam"] + seg["seg_uspm_prev"]
add("seg_asia_sum5", asia.rolling(5, min_periods=4).mean() * 5, "seans"); add("seg_asia_sum20", asia.rolling(20, min_periods=15).mean() * 20, "seans")
add("seg_us_sum5", us.rolling(5, min_periods=4).mean() * 5, "seans"); add("seg_us_sum20", us.rolling(20, min_periods=15).mean() * 20, "seans")
# Yahoo t-1
dxy = np.log(b.dxy)
Y = dict(dxy=dxy, spx=np.log(ps.y__GSPC), silver=np.log(ps.y_SI_F), gdx=np.log(ps.y_GDX), oil=np.log(ps.y_CL_F), copper=np.log(ps.y_HG_F),
         tlt=np.log(ps.y_TLT), eem=np.log(ps.y_EEM), aud=np.log(ps.y_AUDUSD_X), btc=np.log(ps.y_BTC_USD))
for k, x in Y.items():
    st = "B" if k == "btc" else "A"
    add(f"xa_{k}_d1", x.diff(), "yahoo", st); add(f"xa_{k}_d5", x - x.shift(5), "yahoo", st)
gld = np.log(ps.y_GLD)
add("xa_gdx_rel1", Y["gdx"].diff() - gld.diff(), "yahoo"); add("xa_gdx_rel5", (Y["gdx"] - Y["gdx"].shift(5)) - (gld - gld.shift(5)), "yahoo")
gs = gld - np.log(ps.y_SLV); add("xa_gsratio_dev60", gs - gs.rolling(60).mean(), "yahoo")
vix, gvz = np.log(ps.y__VIX), np.log(ps.y__GVZ)
add("vol_vix_d1", vix.diff(), "vol"); add("vol_vix_dev60", vix - vix.rolling(60).mean(), "vol")
add("vol_gvz_d1", gvz.diff(), "vol"); add("vol_gvz_dev60", gvz - gvz.rolling(60).mean(), "vol")
add("vol_gvz_vrp", ps.y__GVZ / 100 - s20 * np.sqrt(252), "vol")
# faiz (kendi Treasury as-of)
be10 = b.ust_nom10 - b.ust_real10
for nm, x in dict(nom10=b.ust_nom10, real10=b.ust_real10, be10=be10, nom2=b.ust_nom2).items():
    add(f"rt_{nm}_d1", x.diff(), "faiz"); add(f"rt_{nm}_d5", x.diff(5), "faiz")
add("rt_curve_2s10s_d5", (b.ust_nom10 - b.ust_nom2).diff(5), "faiz")
# COT (kendi zip as-of)
mm = b.cot_mm_net_oi
add("cot_mm_lvl", mm, "cot")
add("cot_mm_z52", (mm - mm.rolling(260, min_periods=150).mean()) / mm.rolling(260, min_periods=150).std(), "cot")
add("cot_mm_chg1w", mm - mm.shift(5), "cot")
sw = ps.cot_gold_swap_net / ps.cot_gold_oi
add("cot_swap_z52", (sw - sw.rolling(260, min_periods=150).mean()) / sw.rolling(260, min_periods=150).std(), "cot")
# Şanghay primi (SHFE aynı gün 07:00 UTC; CNH 07:00, 2016 öncesi Yahoo CNY)
cnh = b.cnh07.where(b.cnh07.notna(), ps.y_CNY_X)
prem = (np.log(b.shfe_c * 31.1035 / cnh) - np.log(b.p07)).where(pd.to_datetime(b.shfe_date) == b.index)
add("sh_prem_dev20", prem - prem.rolling(20, min_periods=10).mean(), "shfe"); add("sh_prem_d1", prem - prem.ffill().shift(1), "shfe")
add("sh_prem_d5", prem - prem.ffill().shift(5), "shfe")
# takvim (spot endeksinde; VİOP'ta yeniden)
def cal(idx):
    idx = pd.DatetimeIndex(idx); out = {}
    dw = idx.dayofweek
    for i, n in enumerate(("mon", "tue", "wed", "thu")): out[f"cal_{n}"] = pd.Series((dw == i).astype(float), index=idx)
    m = pd.Series(idx.month, index=idx); nm = m.shift(-1).fillna(m.iloc[-1] % 12 + 1)
    first = (m != m.shift(1)).astype(int); k = first.groupby(first.cumsum()).cumcount() + 1
    out["cal_tom"] = ((nm != m) | (k <= 3)).astype(float)
    out["cal_msin"] = np.sin(2 * np.pi * m / 12); out["cal_mcos"] = np.cos(2 * np.pi * m / 12)
    return out
for k, x in cal(b.index).items(): add(k, x, "takvim")
# set B: Dukascopy 15:00 24 saatlik değişimler
for nm, sym in dict(dk_dxy="DOLLARIDXUSD", dk_eur="EURUSD", dk_jpy="USDJPY", dk_tbond="USTBONDTRUSD", dk_spx="USA500IDXUSD", dk_silver="XAGUSD",
                    dk_copper="COPPERCMDUSD", dk_btc="BTCUSD", dk_cnh="USDCNH", dk_try="USDTRY").items():
    x = np.log(ps[f"dk_{sym}_p15"]); add(f"{nm}_d1", x.diff(), "dk15", "B")
XS = pd.DataFrame(F).replace([np.inf, -np.inf], np.nan)
info = pd.DataFrame([(k, *G[k]) for k in F], columns=["feature", "group", "set"])
# VİOP endeksine as-of (en fazla 2 satır)
XV = XS.reindex(XS.index.union(v.index)).ffill(limit=2).reindex(v.index)
for k, x in cal(v.index).items(): XV[k] = x
# VİOP t-1
vb = {}
vb["vp_dte"] = pv.v_dte.astype(float)
vb["vp_roll"] = (v.code != v.code.shift(1)).astype(float)
vb["vp_logvol_chg_l1"] = np.log(pv.v_tot_volume.replace(0, np.nan)).diff().shift(1)
vb["vp_logoi_chg_l1"] = np.log(pv.v_tot_oi.replace(0, np.nan)).diff().shift(1)
p15v = XS.index.to_series()  # placeholder
spot_p15_on_v = b.p15.reindex(b.index.union(v.index)).reindex(v.index)  # VİOP gününün kendi 15:00 spotu (yoksa NaN)
vb["vp_basis_l1"] = (np.log(v.settle) - np.log(spot_p15_on_v)).shift(1)
trp = pv.tr_prem_matched.shift(1); vb["tr_prem_dev20_l1"] = trp - trp.rolling(20, min_periods=10).mean()
vb["tr_usdtry_ret_l1"] = pv.vo_usdtry_ret.shift(1)
for k, x in vb.items():
    XV[k] = x; info.loc[len(info)] = (k, "viop_t1", "B")
XS.to_parquet(f"{OUT}/feat_spot.parquet"); XV.to_parquet(f"{OUT}/feat_viop.parquet"); info.to_csv(f"{OUT}/feat_info.csv", index=False)
print("öznitelik sayısı: set A", int((info.set == "A").sum()), " toplam (B)", len(info))
print(info.groupby(["set", "group"]).size().to_string())
print("VİOP 2020+ doluluk en düşük:", XV.loc["2020":].notna().mean().sort_values().head(6).round(3).to_dict())
