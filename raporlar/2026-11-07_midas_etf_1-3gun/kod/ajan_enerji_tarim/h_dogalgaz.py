"""Doğalgaz hipotezleri (EN01 EIA depolama günü, EN02 kontango vekili UNG/UNL, EN03 UNG ve BOIL/KOLD roll,
NG vade günü, mevsimsellik, haftanın günü, büyük gün sonrası).  Çalıştırma: python3 -I kod/ajan_enerji_tarim/h_dogalgaz.py
Çıktı: sonuclar/aile_enerji_tarim/dogalgaz_*.csv ve testler_dogalgaz.csv (FDR için test kaydı)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import ortak as O, lib

pd.set_option("display.width", 250)
ung = lib.load("UNG"); idx = ung.index
r = {s: O.logret(s) for s in ["UNG", "UNL", "BOIL", "KOLD"]}
desc_rows = []

def describe(name, mask, series_name="UNG", r_=None):
    x = (r_ if r_ is not None else r[series_name]).reindex(idx)
    m = mask.reindex(idx).fillna(False)
    a, b = x[m].dropna(), x[~m].dropna()
    t, p = O.ttest_diff(a, b)
    ai, bi = a[a.index <= lib.IS_END], b[b.index <= lib.IS_END]
    ao, bo = a[a.index > lib.IS_END], b[b.index > lib.IS_END]
    ti, _ = O.ttest_diff(ai, bi); to, _ = O.ttest_diff(ao, bo)
    va, vb = a.abs().mean(), b.abs().mean()
    tv, pv = O.ttest_diff(a.abs(), b.abs())
    rec = {"test": name, "seri": series_name, "n_olay": len(a), "ort_olay_bp": a.mean() * 1e4, "ort_diger_bp": b.mean() * 1e4,
           "t_fark": t, "p_fark": p, "t_fark_is": ti, "t_fark_oos": to, "ort_olay_is_bp": ai.mean() * 1e4, "ort_olay_oos_bp": ao.mean() * 1e4,
           "abs_olay_bp": va * 1e4, "abs_diger_bp": vb * 1e4, "abs_oran": va / vb, "t_abs": tv, "p_abs": pv}
    desc_rows.append(rec)
    # tanımlayıcı testler de FDR sayımına girer (iki yönlü p -> tek yönlü eşdeğeri olarak p/2 değil, p kullanılır)
    O.REG.append({"hyp": name, "sym": series_name, "desc": "olay günü ort. fark (tanımlayıcı)", "mode": "-", "h": 0, "kind": "tanimlayici",
                  "sign": 0, "n": len(a), "net_bp": a.mean() * 1e4, "t": t, "p1": p, "is_t": ti, "oos_t": to})
    return rec

# ---------- EN01: EIA depolama raporu günü ----------
eia = O.events("eia_ng_storage")["date"]
rep_day = O.on_dates(idx, eia)
for s in ["UNG", "BOIL", "KOLD"]:
    describe("EN01_EIA_gunu", rep_day, s)
pre = O.day_before(idx, eia)          # t = rapor gününden önceki işlem günü (genelde Çarşamba)
res = []
res.append(O.grid("EN01_EIA_KOLD", "KOLD", pre, "rapor öncesi gün kapanışı KOLD long", hs=(1, 2)))
res.append(O.grid("EN01_EIA_UNG", "UNG", pre, "rapor öncesi gün UNG long (beklenen -)", hs=(1, 2), sign=-1))
res.append(O.grid("EN01_EIA_BOIL", "BOIL", pre, "rapor öncesi gün BOIL long (beklenen -)", hs=(1, 2), sign=-1))
# mevsim ayrımı (enjeksiyon Nis-Eki / çekiş Kas-Mar) -- yalnız tanımlayıcı
win = pd.Series(idx.month.isin([11, 12, 1, 2, 3]), index=idx)
describe("EN01_EIA_gunu_kis", rep_day & win, "UNG")
describe("EN01_EIA_gunu_kis_KOLD", rep_day & win, "KOLD")
res.append(O.grid("EN01k_EIA_kis_KOLD", "KOLD", pre & win.shift(-1).fillna(False).astype(bool), "Kas-Mar: rapor öncesi gün KOLD long", hs=(1, 2)))
describe("EN01_EIA_gunu_yaz", rep_day & ~win, "UNG")

# ---------- EN02: kontango vekili (UNG'nin 12 aylık şeride göre 20 g performansı) ----------
k20 = (np.log(lib.load("UNL")["c"]).diff(20) - np.log(ung["c"]).diff(20)).reindex(idx)
kpos = k20 > 0
res.append(O.grid("EN02_k20_KOLD", "KOLD", kpos, "k20=Δ20ln(UNL)-Δ20ln(UNG)>0 -> KOLD long"))
# komşu pencereler (parametre duyarlılığı; 20 önceden seçildi) ve saf momentum karşılaştırması
for L in (10, 40, 60):
    kL = (np.log(lib.load("UNL")["c"]).diff(L) - np.log(ung["c"]).diff(L)).reindex(idx)
    res.append(O.grid(f"EN02_k{L}_KOLD", "KOLD", kL > 0, f"k{L}>0 -> KOLD long", hs=(3,), modes=("C0", "O1", "C1")))
mom = np.log(ung["c"]).diff(20) < 0
res.append(O.grid("EN02_mom20_KOLD", "KOLD", mom, "Δ20ln(UNG)<0 (saf momentum) -> KOLD long", hs=(3,), modes=("C0", "O1", "C1")))
res.append(O.grid("EN02_k20neg_KOLD", "KOLD", ~kpos & k20.notna(), "k20<=0 -> KOLD long (tamamlayıcı, beklenen -)", hs=(3,), modes=("C0",), sign=-1))
res.append(O.grid("EN02_k20_UNG", "UNG", kpos, "k20>0 -> UNG long (beklenen -)", hs=(3,), modes=("C0",), sign=-1))
# regresyon: UNG ileri getirisi ~ k20 + kendi gecikmesi
reg_rows = []
for h in (1, 3):
    y = O.fwd(r["UNG"], h)
    d = pd.DataFrame({"y": y, "own": r["UNG"], "k": k20}).dropna()
    for nm, m in (("tum", d.index == d.index), ("is", d.index <= lib.IS_END), ("oos", d.index > lib.IS_END)):
        dd = d[m]
        b, t = O.nw_t(dd["y"].values, np.column_stack([np.ones(len(dd)), dd["own"].values, dd["k"].values]), h)
        reg_rows.append({"test": "EN02_k20_reg", "h": h, "donem": nm, "n": len(dd), "b_k": b[2], "t_k": t[2],
                         "bp_per_sd": b[2] * dd["k"].std() * 1e4})
        if nm == "tum":
            O.REG.append({"hyp": "EN02_k20_reg", "sym": "UNG", "desc": f"fwd{h} ~ k20 (NW)", "mode": "-", "h": h, "kind": "regresyon",
                          "sign": -1, "n": len(dd), "t": t[2], "p1": O.p_one(t[2], len(dd), -1)})
# koşulsuz sürüklenme
for s in ["UNG", "BOIL", "KOLD", "UNL"]:
    x = r[s].dropna()
    desc_rows.append({"test": "EN02_kosulsuz", "seri": s, "n_olay": len(x), "ort_olay_bp": x.mean() * 1e4,
                      "t_fark": x.mean() / (x.std() / np.sqrt(len(x))), "ort_olay_is_bp": x[x.index <= lib.IS_END].mean() * 1e4,
                      "ort_olay_oos_bp": x[x.index > lib.IS_END].mean() * 1e4})

# ---------- EN03: UNG roll penceresi ve BOIL/KOLD roll ----------
roll = O.events("ung_uso_roll")
ung_roll = O.on_dates(idx, roll[roll.event == "UNG_roll"]["date"])
describe("EN03_UNG_roll_gunu", ung_roll, "UNG")
describe("EN03_UNG_roll_gunu_UNG-UNL", ung_roll, "UNG-UNL", r["UNG"] - r["UNL"])
r1 = roll[(roll.event == "UNG_roll") & roll.detail.str.startswith("gün 1/4")]["date"]
pre_r1 = O.day_before(idx, r1)
res.append(O.grid("EN03_roll_KOLD", "KOLD", pre_r1, "UNG roll 1. gününden önceki kapanış KOLD long"))
bk_roll = O.on_dates(idx, roll[roll.event == "BOIL_KOLD_roll"]["date"])
describe("EN03_BOIL_roll_gunu", bk_roll, "BOIL")
describe("EN03_BOIL_roll_gunu_BOIL-2UNG", bk_roll, "BOIL-2UNG", r["BOIL"] - 2 * r["UNG"])

# ---------- NG son işlem günü ----------
ngv = O.events("vadeler", "NG_vade")["date"]
describe("NG_vade_gunu", O.on_dates(idx, ngv), "UNG")
describe("NG_vade_ertesi", O.on_dates(idx, ngv).shift(1).fillna(False).astype(bool), "UNG")

# ---------- mevsimsellik ----------
describe("NG_mevsim_KasMar", win, "UNG")
describe("NG_mevsim_KasMar_KOLD", win, "KOLD")
mon = r["UNG"].groupby(r["UNG"].index.month).agg(["mean", "std", "count"])
mon["t"] = mon["mean"] / (mon["std"] / np.sqrt(mon["count"])); mon["mean_bp"] = mon["mean"] * 1e4
mon.to_csv(os.path.join(O.OUT, "dogalgaz_ay_ortalamalari.csv"))

D = pd.DataFrame(desc_rows); D.to_csv(os.path.join(O.OUT, "dogalgaz_tanimlayici.csv"), index=False)
G = pd.concat(res); G.to_csv(os.path.join(O.OUT, "dogalgaz_stratejiler.csv"), index=False)
pd.DataFrame(reg_rows).to_csv(os.path.join(O.OUT, "dogalgaz_k20_regresyon.csv"), index=False)
O.save_registry("dogalgaz")

print("== Tanımlayıcı (olay günü vs diğer günler; günlük log getiri bp)")
print(D.round(3).to_string(index=False))
print("\n== Strateji ızgaraları (2.500 $ maliyetli)")
for hyp, g in G.groupby("hyp", sort=False):
    print("--", hyp, g["desc"].iloc[0]); print(O.fmt(g, ["mode", "h", "n", "mean_gross_bp", "mean_net_bp", "t", "win", "pf", "is_net_bp", "oos_net_bp", "years_pos_frac", "worst_bp", "edge_bp"]))
print("\n== k20 regresyon"); print(pd.DataFrame(reg_rows).round(3).to_string(index=False))
print("\n== UNG ay ortalamaları (bp)"); print(mon[["mean_bp", "t", "count"]].round(2).T.to_string())
