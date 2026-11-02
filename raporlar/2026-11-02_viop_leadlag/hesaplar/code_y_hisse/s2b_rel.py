"""Adım 2c: Piyasa-göreli (çifte özgü) lead-lag. Bağımlı: hedef getirisi - β_IS·XU100 getirisi (aynı bileşen: cc/gap/intra).
Böylece 'lider -> tüm piyasa' (piyasa zamanlaması) etkileri ayıklanır, yalnız çifte özgü öncülük kalır; VİOP'ta hedef vadeli - XU030 vadeli ile işlenebilir.
Kontroller: hedef cc_{t-1}, XU100_{t-1}, sektör_{t-1}, EW177_{t-1} (küçük/bireysel faktör); lag k>1 ve c5 için aynı değişkenlerin _{t-k}/Σ'ı.
Null: 10 dairesel kaydırma (lag1). Çıktı: res/scan_rel.parquet, res/null_rel.npz
"""
import sys, os, time, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hdata, hreg
D = hdata.load(); cc, gap, intra = D["cc"], D["gap"], D["intra"]
LEAD = [c for c in cc.columns if c not in hdata.IDX]; TGT = hdata.VIOP
idx = cc.index; T = len(idx); SPLIT = pd.Timestamp(hdata.SPLIT)
EW = cc[LEAD].mean(axis=1)
per = {"FULL": np.ones(T, bool), "IS": idx < SPLIT, "OOS": idx >= SPLIT}
def beta(j):
    d = pd.concat([cc[j], cc["XU100"]], axis=1).dropna(); dI = d[d.index < SPLIT]
    if len(dI) < 250: dI = d.iloc[:250]
    return np.cov(dI.iloc[:, 0], dI.iloc[:, 1])[0, 1] / dI.iloc[:, 1].var()
B = {j: beta(j) for j in TGT}
pd.Series(B).to_csv(os.path.join(hdata.RES, "beta_is.csv"))
def ctrl(j, k):
    s = hdata.sector_index(j); base = [cc[j].shift(1), cc["XU100"].shift(1), EW.shift(1)] + ([cc[s].shift(1)] if s else [])
    if k == 1: return pd.concat(base, axis=1)
    src = [cc[j], cc["XU100"], EW] + ([cc[s]] if s else [])
    add = [x.rolling(5, min_periods=5).sum().shift(1) for x in src] if k == "c5" else [x.shift(k) for x in src]
    return pd.concat(base + add, axis=1)
def lagX(M, k): return M.rolling(5, min_periods=5).sum().shift(1) if k == "c5" else M.shift(k)
deps = {"cc_rel": (cc, "XU100"), "gap_rel": (gap, "XU100"), "intra_rel": (intra, "XU100")}
def yrel(dn, j):
    dd, m = deps[dn]; return dd[j] - B[j] * dd[m]
if __name__ == "__main__":
    rows = []; t0 = time.time()
    Xk = {k: lagX(cc[LEAD], k).values for k in [1, 2, "c5"]}
    for j in TGT:
        si = LEAD.index(j)
        for k in [1, 2, "c5"]:
            C = ctrl(j, k).values
            for dn in deps:
                yv = yrel(dn, j).values
                for pn, pm in per.items():
                    r = hreg.nw_batch(np.where(pm, yv, np.nan), Xk[k], C); r["t"][si] = np.nan
                    rows.append(pd.DataFrame({"target": j, "leader": LEAD, "dep": dn, "lag": str(k), "period": pn, "b": r["b"], "t": r["t"], "pc": r["pc"], "n": r["n"]}))
        print(j, round(time.time() - t0, 1), flush=True)
    out = pd.concat(rows, ignore_index=True); out.to_parquet(os.path.join(hdata.RES, "scan_rel.parquet"))
    # null
    rng = np.random.default_rng(11); offs = rng.integers(250, T - 250, 10)
    NT = np.full((len(offs), len(TGT), 3, 3, len(LEAD)), np.nan, np.float32)
    Lv = cc[LEAD].values; Cs = {j: ctrl(j, 1).values for j in TGT}; Ys = {(j, dn): yrel(dn, j).values for j in TGT for dn in deps}
    for si_, o in enumerate(offs):
        X = pd.DataFrame(np.roll(Lv, o, axis=0), index=idx).shift(1).values
        for jj, j in enumerate(TGT):
            for di, dn in enumerate(deps):
                for pi, (pn, pm) in enumerate(per.items()):
                    NT[si_, jj, di, pi] = hreg.nw_batch(np.where(pm, Ys[(j, dn)], np.nan), X, Cs[j])["t"]
        print("null", si_, round(time.time() - t0, 1), flush=True)
    np.savez_compressed(os.path.join(hdata.RES, "null_rel.npz"), t=NT, offs=offs, targets=np.array(TGT), leaders=np.array(LEAD), deps=np.array(list(deps)), periods=np.array(list(per)))
