"""Backtestler (look-ahead yok; sinyal pozisyondan ÖNCE bilinir). Maliyet: tek bacak 8 / 15 bps gidiş-dönüş; çift bacak 16 / 30.
IS 2014–2020 (veri yoksa başlangıçtan), OOS 2021–2026. Yön kuralı önceden (mekanizmadan) sabit; IS'ten seçilmez (aksi belirtilmedikçe).
BT1  Zımni TL faizi şoku (VİOP USDTRY 1-2 ay takvim yayılımı, uzlaşma ~15:00 UTC t-1) -> banka sepeti / XBANK gün-içi t (faiz ↑ -> short).
BT1b DİBS 2y getiri şoku (BAP kapanış ~14:30 UTC t-1) -> banka sepeti gün-içi t ; EKGYO, holdingler.
BT2  Gram altın gece hareketi (GC=F x TRY=X, 15:00 UTC t-1 -> 06:00 UTC t) -> TRALT / TRMET gün-içi t (devam: +, geri dönüş: −; her ikisi raporlanır).
BT2b Uzun geçmiş: Yahoo gram altın_{t-1} (ons ~18 UTC x kur ~24 UTC) -> TRALT gün-içi t.
BT3  USDTRY_{t-1} (Yahoo, ~24 UTC) -> 'dolar hisseleri − bankalar' gün-içi çift (TL zayıfladıysa long ihracatçı / short banka), tüm günler vs yüksek kur-vol rejimi.
BT3b Aynı, sadece banka sepeti tek bacak (USDTRY ↑ -> banka short) ve rejim filtresi.
Çıktı: res/bt.csv, res/bt_years.csv"""
import numpy as np, pandas as pd, json
import mlib as M, ll
mac = pd.read_parquet(M.RES + "/macro_daily.parquet")
reg = pd.read_parquet(M.RES + "/fx_regime.parquet")["reg"]
EXP = ["ENKAI", "TUPRS", "THYAO", "PGSUS", "FROTO", "TOASO", "BRSAN", "EREGL", "KRDMD", "ARCLK", "VESTL", "SISE", "CIMSA", "TAVHL", "TKFEN", "AEFES", "ASELS", "PETKM", "SASA"]
def basket(names, col):
    return pd.concat([M.dec(s, col) for s in names], axis=1).mean(axis=1, skipna=True)
BK = basket(M.BANKS, "intra"); EXi = basket(EXP, "intra")
def z(x, w=250):
    mu = x.rolling(w, min_periods=60).mean().shift(1); sd = x.rolling(w, min_periods=60).std().shift(1); return (x - mu) / sd
def run(name, sig, tgt, sign=+1, thr=0.0, cost=(8, 15), legs=1, mask=None, mode="z", split="2021-01-01"):
    s = sig.copy()
    if mask is not None: s = s.where(mask.reindex(s.index).fillna(False), 0.0)
    out = []
    for c in cost:
        res, pnl = ll.backtest(sign * s, tgt, cost_bps=c * legs, mode="sign", thr=thr, split=split)
        r = {"bt": name, "cost_bps": c * legs, "thr": thr, "sign": sign, "split": split}
        for k in ["IS", "OOS", "ALL"]:
            for m in ["n", "mean_bps", "t", "hit", "sharpe"]: r[f"{k}_{m}"] = res[k].get(m, np.nan)
        r["by_year"] = json.dumps(res["by_year_bps"]); out.append(r)
        # brüt
    res0, p0 = ll.backtest(sign * s, tgt, cost_bps=0, mode="sign", thr=thr, split=split)
    # kıyas: aynı günlerde 'hep long' hedef ortalaması ve pozisyonun long oranı (sürüklenme/kur kayması artefaktı kontrolü)
    df = pd.concat([(sign * s).rename("s"), tgt.rename("y")], axis=1).dropna(); act = df[df["s"].abs() > thr]
    sp = pd.Timestamp(split)
    for r in out:
        r["OOS_gross_bps"] = res0["OOS"].get("mean_bps", np.nan); r["IS_gross_bps"] = res0["IS"].get("mean_bps", np.nan)
        r["long_share"] = float((act["s"] > 0).mean()) if len(act) else np.nan
        r["OOS_target_mean_bps"] = 1e4 * act.loc[act.index >= sp, "y"].mean() if len(act) else np.nan
        r["IS_target_mean_bps"] = 1e4 * act.loc[act.index < sp, "y"].mean() if len(act) else np.nan
    return out
R = []
SPH = "2025-08-01"  # saatlik (2024+) sinyaller için 1. yarı / 2. yarı bölünmesi
# ---- BT1: zımni faiz şoku -> banka gün-içi
for v in ["d_ir12", "d_ir13"]:
    zz = z(mac[v].clip(-10, 10)).shift(1)
    for tgt_nm, tgt in [("BANKA7_intra", BK), ("XBANK_intra", M.dec("XBANK", "intra")), ("EKGYO_intra", M.dec("EKGYO", "intra")),
                        ("HOLD4_intra", basket(["KCHOL", "SAHOL", "ALARK", "DOHOL"], "intra")), ("BANKA7_cc(ref: gap dahil, işlenemez)", basket(M.BANKS, "cc"))]:
        for thr in [1.0, 2.0]:
            R += run(f"BT1 {v}_z(t-1)->{tgt_nm}", zz, tgt, sign=-1, thr=thr)
    # rejim filtresi
    for thr in [1.0]:
        R += run(f"BT1 {v}_z(t-1)->BANKA7_intra [vol_H]", zz, BK, sign=-1, thr=thr, mask=(reg == "H"))
# ---- BT1b: DİBS 2y / 10y / TLREF
for v in ["d_dibs2", "d_dibs10", "d_tlref"]:
    if v not in mac or mac[v].notna().sum() < 300: continue
    zz = z(mac[v].clip(-8, 8)).shift(1)
    for tgt_nm, tgt in [("BANKA7_intra", BK), ("EKGYO_intra", M.dec("EKGYO", "intra")), ("HOLD4_intra", basket(["KCHOL", "SAHOL", "ALARK", "DOHOL"], "intra")),
                        ("XU030_intra", M.dec("XU030", "intra"))]:
        for thr in ([0.0, 1.0] if tgt_nm in ("XU030_intra", "BANKA7_intra") else [1.0]):
            R += run(f"BT1b {v}_z(t-1)->{tgt_nm}", zz, tgt, sign=-1, thr=thr)
    R += run(f"BT1b {v}_z(t-1)->BANKA7_intra [vol_H]", zz, BK, sign=-1, thr=1.0, mask=(reg == "H"))
# ---- BT2: gram altın gece hareketi -> TRALT / TRMET gün-içi (saatlik, 2024-06+)
for s in ["TRALT", "TRMET"]:
    it = M.dec(s, "intra")
    for sign, lab in [(+1, "devam"), (-1, "geri_donus")]:
        for thr in [0.0, 0.01]:
            R += run(f"BT2 n_xau(gece)->{s}_intra {lab} [ham]", mac["n_xau"], it, sign=sign, thr=thr, split=SPH)
        for thr in [0.0, 1.0]:
            R += run(f"BT2 z(n_xau,120g)->{s}_intra {lab}", z(mac["n_xau"], 120), it, sign=sign, thr=thr, split=SPH)
    # gap'e göre: gece altın hareketinin açılışta ne kadarı fiyatlandı? fazla gap -> fade
    g = M.dec(s, "gap"); beta = 0.6
    resid = g - beta * mac["n_xau"]
    # sinyal açılışta bilinir (gap + gece altın) -> gün-içi
    R += run(f"BT2c ({s} gap − 0,6·n_xau) fade ->{s}_intra", resid, it, sign=-1, thr=0.01, split=SPH)
# ---- BT2b: uzun geçmiş Yahoo gram altın_{t-1}
for s in ["TRALT", "TRMET"]:
    R += run(f"BT2b z(y_xau)(t-1)->{s}_intra devam", z(mac["y_xau"]).shift(1), M.dec(s, "intra"), sign=+1, thr=0.0)
    R += run(f"BT2b z(y_xau)(t-1)->{s}_intra devam |z|>1", z(mac["y_xau"]).shift(1), M.dec(s, "intra"), sign=+1, thr=1.0)
    R += run(f"BT2b z(y_xau)(t-1)->{s}_intra geri_donus |z|>1", z(mac["y_xau"]).shift(1), M.dec(s, "intra"), sign=-1, thr=1.0)
# ---- BT3: USDTRY_{t-1} -> ihracatçı − banka gün-içi çift
pair = EXi - BK
zz = z(mac["y_usd"].clip(-0.1, 0.1)).shift(1)
for thr in [0.0, 1.0]:
    R += run(f"BT3 y_usd_z(t-1)->ihracatci−banka intra", zz, pair, sign=+1, thr=thr, legs=2)
    R += run(f"BT3 y_usd_z(t-1)->ihracatci−banka intra [vol_H]", zz, pair, sign=+1, thr=thr, legs=2, mask=(reg == "H"))
    R += run(f"BT3 y_usd_z(t-1)->ihracatci−banka intra [vol_L+M]", zz, pair, sign=+1, thr=thr, legs=2, mask=(reg != "H"))
R += run("BT3 n_usd(gece)->ihracatci−banka intra [ham]", mac["n_usd"], pair, sign=+1, thr=0.0, legs=2, split=SPH)
R += run("BT3 z(n_usd,120g)->ihracatci−banka intra", z(mac["n_usd"], 120), pair, sign=+1, thr=0.0, legs=2, split=SPH)
R += run("BT3 z(n_usd,120g)->ihracatci−banka intra |z|>1", z(mac["n_usd"], 120), pair, sign=+1, thr=1.0, legs=2, split=SPH)
R += run("BT3 n_usd(gece)->XU100 intra short [ham; kur kayması = hep short]", mac["n_usd"], M.dec("XU100", "intra"), sign=-1, thr=0.0, split=SPH)
R += run("BT3 z(n_usd,120g)->XU100 intra short", z(mac["n_usd"], 120), M.dec("XU100", "intra"), sign=-1, thr=0.0, split=SPH)
R += run("BT3 z(n_usd,120g)->XU100 intra short |z|>1", z(mac["n_usd"], 120), M.dec("XU100", "intra"), sign=-1, thr=1.0, split=SPH)
R += run("BT3 z(n_usd,120g)->BANKA7 intra short |z|>1", z(mac["n_usd"], 120), BK, sign=-1, thr=1.0, split=SPH)
# BT3b: banka tek bacak
for thr in [1.0, 2.0]:
    R += run(f"BT3b y_usd_z(t-1)->BANKA7_intra", zz, BK, sign=-1, thr=thr)
    R += run(f"BT3b y_usd_z(t-1)->BANKA7_intra [vol_H]", zz, BK, sign=-1, thr=thr, mask=(reg == "H"))
# ---- BT4: VİOP kur (15:00 UTC hizalı) t-1 -> ihracatçı−banka (gerçek öncülük; senkron bilgi değil)
zz = z(mac["v_usd"].clip(-0.1, 0.1)).shift(1)
for thr in [0.0, 1.0]:
    R += run("BT4 v_usd_z(t-1)->ihracatci−banka intra", zz, pair, sign=+1, thr=thr, legs=2)
    R += run("BT4 v_usd_z(t-1)->ihracatci−banka cc(t)", zz, basket(EXP, "cc") - basket(M.BANKS, "cc"), sign=+1, thr=thr, legs=2)
# ---- BT5: taramada FDR'den geçen tek kur->gün-içi bağı: USDTRY_{t-1} (Yahoo) -> ENKAI gün-içi (devam: TL zayıfladıysa long)
zz = z(mac["y_usd"].clip(-0.1, 0.1)).shift(1)
for thr in [0.0, 1.0]:
    R += run("BT5 y_usd_z(t-1)->ENKAI_intra", zz, M.dec("ENKAI", "intra"), sign=+1, thr=thr)
B = pd.DataFrame(R); B.to_csv(M.RES + "/bt.csv", index=False)
pd.set_option("display.width", 260); pd.set_option("display.max_colwidth", 70)
print(B[["bt", "cost_bps", "thr", "split", "IS_n", "IS_mean_bps", "IS_t", "OOS_n", "OOS_mean_bps", "OOS_t", "OOS_sharpe", "OOS_gross_bps", "IS_gross_bps", "long_share", "OOS_target_mean_bps"]].round(2).to_string(index=False))
