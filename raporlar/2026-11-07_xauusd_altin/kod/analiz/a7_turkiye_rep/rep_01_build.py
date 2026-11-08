"""Adım 1: ham bültenden sürekli seriler + Dukascopy 15:00 USDTRY; panel ile karşılaştırma; ham zaman damgası kontrolleri."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a7_turkiye_rep")
from rep_lib import *
C = {r: continuous(r) for r in ["XAUUSD", "XAUTRYM", "USDTRY", "XU030"]}
days = C["XAUUSD"].index
for r, c in C.items():
    bad = (np.abs(c.settle_prev_own - c.prev_settle_bull) / c.settle_prev_own > 1e-6).sum()
    print(f"{r}: n={len(c)} {c.index.min().date()}..{c.index.max().date()}  prev_settle(bülten) != kendi t-1 settle: {bad} gün; roll günü: {(c.code != c.code.shift()).sum()-1}")
fx15, fx15_ts = duka_at("USDTRY", days, 15, 1)
fx07, _ = duka_at("USDTRY", days, 7, 1)
print("Dukascopy USDTRY 15:00: NaN gün", int(fx15.isna().sum()), "; son geçerli", fx15.dropna().index.max().date())
print("fiyat damgası 15:00 dışı (stale) gün sayısı:", int(((fx15_ts.dt.hour != 15) & fx15.notna()).sum()))
D = pd.DataFrame(index=days)
for r, nm in [("XAUUSD", "x"), ("XAUTRYM", "g"), ("USDTRY", "u"), ("XU030", "xu")]:
    c = C[r].reindex(days)
    for col in ["code", "expiry", "settle", "ret", "oi", "volume", "dte"]:
        D[f"{nm}_{col}"] = c[col]
D["fx15"] = fx15; D["fx07"] = fx07
# matched premium: aynı vade ayı; ay seçimi = t günü XAUTRYM hacmi en büyük (panel ile aynı tanım) ve alternatif: t-1 OI'ye göre aktif XAUTRYM ayı
V = viop_long(); V = V.assign(ym=V.expiry.dt.to_period("M"))
g1 = V[V.root == "XAUTRYM"][["date", "ym", "settle", "volume", "oi"]].rename(columns={"settle": "gs", "volume": "gv", "oi": "goi"})
g2 = V[V.root == "XAUUSD"][["date", "ym", "settle"]].rename(columns={"settle": "xsx"})
g3 = V[V.root == "USDTRY"][["date", "ym", "settle"]].rename(columns={"settle": "us"})
m = g1.merge(g2, on=["date", "ym"]).merge(g3, on=["date", "ym"])
m = m[(m.gs > 0) & (m.xsx > 0) & (m.us > 0)]
m["prem"] = np.log(m.gs) - np.log(m.xsx * m.us / 31.1035)
mv = m.sort_values(["date", "gv"], ascending=[True, False]).drop_duplicates("date").set_index("date")
D["prem_vol"] = mv.prem.reindex(days); D["prem_vol_ym"] = mv.ym.astype(str).reindex(days)
# alternatif: aktif XAUTRYM kontratının ayı (t-1 OI ile seçilmiş; ileriye bakmasız)
D["g_ym"] = pd.to_datetime(D.g_expiry).dt.to_period("M").astype(str)
ma = m.assign(ym=m.ym.astype(str)).set_index(["date", "ym"]).prem
D["prem_act"] = [ma.get((d, y), np.nan) for d, y in zip(D.index, D.g_ym)]
D.to_parquet(f"{OUT}/rep_series.parquet")
# ---- panel ile karşılaştırma
p = pd.read_parquet(f"{P}/panel_viop.parquet"); p.index = pd.to_datetime(p.index)
p = p.reindex(days)
for a, b in [("x_ret", "v_ret"), ("g_ret", "vo_xautry_ret"), ("u_ret", "vo_usdtry_ret"), ("xu_ret", "vo_xu030_ret"), ("u_settle", "vo_usdtry_settle"), ("u_dte", "vo_usdtry_dte"),
             ("g_oi", "vo_xautry_oi"), ("fx15", "dk_USDTRY_p15"), ("prem_vol", "tr_prem_matched")]:
    dd = (D[a].astype(float) - p[b].astype(float)).abs()
    print(f"  {a:9s} vs panel {b:18s}: max|fark| {dd.max():.3g}, >1e-9 gün {(dd>1e-9).sum()}, NaN uyumsuz {(D[a].isna() != p[b].isna()).sum()}")
print("kod uyumu x/u/g:", (D.x_code == p.v_code).mean(), (D.u_code == p.vo_usdtry_code).mean(), (D.g_code == p.vo_xautry_code).mean())
print("prem_vol ile prem_act aynı ay oranı:", (D.prem_vol_ym == D.g_ym).mean(), " corr:", D.prem_vol.corr(D.prem_act))
