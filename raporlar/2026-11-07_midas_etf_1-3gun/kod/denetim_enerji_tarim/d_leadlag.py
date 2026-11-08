"""Denetim lead-lag (enerji_tarim hedefleri): leadlag_sweep FDR satırlarının taranması + bağımsız yeniden hesap
(kendi gecikmesi kontrollü, Newey-West), ekonomik büyüklük vs maliyet, bayat fiyat kontrolü (CANE).
Çalıştırma: python3 -I kod/denetim_enerji_tarim/d_leadlag.py"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import dsim as D, lib

pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
FAM = "USO BNO USL UCO SCO UNG UNL BOIL KOLD UGA DBO XLE DBC PDBC GSG DBA CORN WEAT SOYB CANE COMT BCI XOP OIH GUSH DRIP ERX ERY".split()
KEEP = ["USO", "XLE", "KOLD", "BNO", "UCO", "SCO", "UNG", "BOIL", "XOP", "DRIP", "PDBC"]
ll = pd.read_csv(os.path.join(D.ROOT, "sonuclar", "leadlag_sweep.csv"))
f = ll[ll["target"].isin(FAM)].copy()
flags = [c for c in f.columns if c.startswith("fdr10_")]
print("Aile hedefli satır:", len(f), "| FDR bayrağı olan satır:", int(f[flags].any(axis=1).sum()))
hit = f[f[flags].any(axis=1)]
cols = ["target", "leader", "corr_1y", "lag_t_h1", "lag_t_h1_is", "lag_t_h1_oos", "lag_bp_per_sd_h1", "lag_t_h3", "lag_t_h3_is", "lag_t_h3_oos", "lag_bp_per_sd_h3",
        "catch_t_h1", "catch_t_h1_is", "catch_t_h1_oos", "catch_bp_per_sd_h1", "catch_t_h3", "catch_t_h3_is", "catch_t_h3_oos", "catch_bp_per_sd_h3"] + flags
print(hit[cols].round(2).to_string(index=False))
tar = pd.read_csv(os.path.join(D.ROOT, "sonuclar", "tarama.csv")).set_index("sym")

# Kabul/yedek hedefler için: FDR + IS/OOS aynı işaret + |bp/sd| > maliyet ölçütünü yeniden uygula
rows = []
for _, r in f[f["target"].isin(KEEP)].iterrows():
    cst = tar.loc[r["target"], "cost_rt_bp"]
    for kind in ("lag", "catch"):
        for h in ("h1", "h3"):
            fl = r.get(f"fdr10_{kind}_t_{h}", False)
            same = np.sign(r[f"{kind}_t_{h}_is"]) == np.sign(r[f"{kind}_t_{h}_oos"]) == np.sign(r[f"{kind}_t_{h}"])
            big = abs(r[f"{kind}_bp_per_sd_{h}"]) > cst
            if fl and same and big:
                rows.append({"target": r["target"], "leader": r["leader"], "tur": kind, "h": h, "t": r[f"{kind}_t_{h}"], "bp_sd": r[f"{kind}_bp_per_sd_{h}"], "maliyet": cst})
print("\nKabul/yedek hedeflerde ölçütü geçen gecikmeli öncü satırı:", len(rows)); print(pd.DataFrame(rows).to_string(index=False) if rows else "  (yok)")


# Bağımsız yeniden hesap: r_T(t+1..t+h) ~ r_L(t) + r_T(t) + r_T(t-1); NW t
def nw(y, X, L):
    xtx = np.linalg.inv(X.T @ X); b = xtx @ X.T @ y; e = y - X @ b; u = X * e[:, None]; S = u.T @ u
    for l in range(1, L + 1):
        w = 1 - l / (L + 1); G = u[l:].T @ u[:-l]; S += w * (G + G.T)
    V = xtx @ S @ xtx; return b, b / np.sqrt(np.diag(V))


def lr(sym):
    return np.log(lib.load(sym)["c"]).diff()


def test(target, leader, h, lab=""):
    rt, rl = lr(target), lr(leader)
    d = pd.DataFrame({"rt": rt, "rl": rl}).dropna()
    d["y"] = d["rt"][::-1].rolling(h).sum()[::-1].shift(-1)
    d["rt1"] = d["rt"].shift(1); d = d.dropna()
    out = {}
    for nm, m in (("tum", slice(None)), ("is", d.index <= D.IS_END), ("oos", d.index > D.IS_END)):
        dd = d[m] if nm != "tum" else d
        X = np.column_stack([np.ones(len(dd)), dd["rl"], dd["rt"], dd["rt1"]])
        b, t = nw(dd["y"].to_numpy(), X, h + 2)
        out[nm + "_t"] = t[1]; out[nm + "_bp_sd"] = b[1] * dd["rl"].std() * 1e4
    return {"hedef": target, "oncu": leader, "h": h, **out}


print("\nBağımsız yeniden hesap (kendi 2 gecikmesi kontrollü, NW):")
pairs = [("CANE", "BNO"), ("CANE", "USO"), ("XOP", "UNG"), ("XLE", "KWEB"), ("UNG", "KWEB"), ("BNO", "VVIX"), ("UCO", "CPER"), ("PDBC", "KWEB"), ("USO", "SPY"), ("XLE", "SPY"), ("KOLD", "SPY")]
res = []
for tgt, ld in pairs:
    for h in (1, 3):
        try:
            if ld == "VVIX":
                v = np.log(lib.vol_index("VVIX")).diff()
                rt = lr(tgt); d = pd.DataFrame({"rt": rt, "rl": v.reindex(rt.index)}).dropna()
                d["y"] = d["rt"][::-1].rolling(h).sum()[::-1].shift(-1); d["rt1"] = d["rt"].shift(1); d = d.dropna()
                X = np.column_stack([np.ones(len(d)), d["rl"], d["rt"], d["rt1"]]); b, t = nw(d["y"].to_numpy(), X, h + 2)
                o = {"hedef": tgt, "oncu": "VVIX(16:15 ET)", "h": h, "tum_t": t[1], "tum_bp_sd": b[1] * d["rl"].std() * 1e4}
                for nm, m in (("is", d.index <= D.IS_END), ("oos", d.index > D.IS_END)):
                    dd = d[m]; X = np.column_stack([np.ones(len(dd)), dd["rl"], dd["rt"], dd["rt1"]]); b2, t2 = nw(dd["y"].to_numpy(), X, h + 2)
                    o[nm + "_t"] = t2[1]; o[nm + "_bp_sd"] = b2[1] * dd["rl"].std() * 1e4
                res.append(o)
            else:
                res.append(test(tgt, ld, h))
        except Exception as e:
            print("hata", tgt, ld, e)
res = pd.DataFrame(res); print(res.round(2).to_string(index=False))
res.to_csv(os.path.join(D.OUT, "leadlag_yeniden.csv"), index=False)

# Bayat fiyat kontrolü (CANE): sıfır hacimli gün oranı, kapanış=önceki kapanış oranı, düşük hacim günlerinde öncü etkisi
c = lib.load("CANE"); raw = c["raw_c"]
print("\nCANE: hacmi 0 olan gün oranı %.3f | kapanış değişmeyen gün oranı %.3f | medyan günlük hacim (adet) %.0f" % ((c["v"] == 0).mean(), (raw.diff() == 0).mean(), c["v"].median()))
rt, rl = lr("CANE"), lr("BNO")
d = pd.DataFrame({"rt": rt, "rl": rl, "v": c["v"]}).dropna(); d["y"] = d["rt"].shift(-1); d["rt1"] = d["rt"].shift(1); d = d.dropna()
q = d["v"].rolling(60).median()
for nm, m in (("düşük hacimli gün (< 60g medyan)", d["v"] < q), ("yüksek hacimli gün", d["v"] >= q)):
    dd = d[m.fillna(False)]; X = np.column_stack([np.ones(len(dd)), dd["rl"], dd["rt"], dd["rt1"]]); b, t = nw(dd["y"].to_numpy(), X, 3)
    print(f"  CANE<-BNO h1 {nm}: n={len(dd)} t={t[1]:.2f} bp/sd={b[1]*dd['rl'].std()*1e4:.1f}")
# Açılış boşluğu mu gün içi mi? CANE(t+1) = gap + intraday
o = c["o"]; cc = c["c"]
gap = np.log(o / cc.shift(1)); intr = np.log(cc / o)
d2 = pd.DataFrame({"gap1": gap.shift(-1), "intr1": intr.shift(-1), "rl": rl, "rt": rt}).dropna()
for col in ("gap1", "intr1"):
    X = np.column_stack([np.ones(len(d2)), d2["rl"], d2["rt"]]); b, t = nw(d2[col].to_numpy(), X, 3)
    print(f"  CANE {col} ~ r_BNO(t): t={t[1]:.2f} bp/sd={b[1]*d2['rl'].std()*1e4:.1f}")
