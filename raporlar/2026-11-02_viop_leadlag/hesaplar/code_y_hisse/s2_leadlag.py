"""Adım 2: Günlük lead-lag taraması. lider_{t-k} (cc) -> hedef_t (cc | gap | intra), 177 aday lider x 47 VİOP hedef.
Kontroller: hedefin kendi cc_{t-1}, XU100_{t-1}, (varsa) sektör endeksi_{t-1} (XBANK / XUSIN); k>1 için ayrıca kendi/XU100/sektör _{t-k};
'c5' (kümülatif): lider Σ_{t-5..t-1}, kontroller kendi/XU100/sektör Σ_{t-5..t-1} + _{t-1}.
Ek varyant 'intra_g' (lag1): gün-içi_t | hedef gap_t + XU100 gap_t (açılışta bilinen bilgi) kontrollü.
Dönemler: FULL 2014–2026, IS 2014–2020, OOS 2021–2026, PRE 2005–2013 (yalnız cc lag1/c5), Y<yıl> (yalnız lag1 cc/intra).
Null: lider paneli dairesel kaydırma (20 ofset, tüm liderler aynı ofset -> liderler arası bağımlılık korunur), lag1, cc/gap/intra, FULL/IS/OOS.
Hacim filtresi: düşük hacimli günler (TL hacim < 0,3 x geçmiş 60g medyan) hedefte t ve t-1, liderde t-1 maskelenir (lag1).
Çıktı: res/scan_long.parquet, res/null_t.npz, res/volfilt.parquet
"""
import sys, os, time, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hdata, hreg
D = hdata.load(); cc, gap, intra = D["cc"], D["gap"], D["intra"]
ccL = pd.read_parquet(os.path.join(hdata.CACHE, "cc_long.parquet"))
LEAD = [c for c in cc.columns if c not in hdata.IDX]
TGT = hdata.VIOP
idx = cc.index; T = len(idx)
SPLIT = pd.Timestamp(hdata.SPLIT)
per_masks = {"FULL": np.ones(T, bool), "IS": idx < SPLIT, "OOS": idx >= SPLIT}

def ctrl(df, j, k):
    sec = hdata.sector_index(j)
    base = [df[j].shift(1), df["XU100"].shift(1)] + ([df[sec].shift(1)] if sec else [])
    if k == 1: return pd.concat(base, axis=1)
    if k == "c5":
        add = [df[x].rolling(5, min_periods=5).sum().shift(1) for x in [j, "XU100"] + ([sec] if sec else [])]
    else:
        add = [df[x].shift(k) for x in [j, "XU100"] + ([sec] if sec else [])]
    return pd.concat(base + add, axis=1)

def lagX(Lm, k):
    if k == "c5": return Lm.rolling(5, min_periods=5).sum().shift(1)
    return Lm.shift(k)

def run_main():
    rows = []
    Lcc = cc[LEAD]
    Xk = {k: lagX(Lcc, k).values for k in [1, 2, 3, 4, 5, "c5"]}
    deps = {"cc": cc, "gap": gap, "intra": intra}
    t0 = time.time()
    for jj, j in enumerate(TGT):
        self_i = LEAD.index(j)
        for k in [1, 2, 3, 4, 5, "c5"]:
            C = ctrl(cc, j, k).values
            for dn, dd in deps.items():
                for pn, pm in per_masks.items():
                    y = np.where(pm, dd[j].values, np.nan)
                    r = hreg.nw_batch(y, Xk[k], C)
                    for key in r: r[key] = np.asarray(r[key], float).copy()
                    r["b"][self_i] = np.nan; r["t"][self_i] = np.nan
                    rows.append(pd.DataFrame({"target": j, "leader": LEAD, "dep": dn, "lag": str(k), "period": pn,
                                              "b": r["b"], "t": r["t"], "pc": r["pc"], "n": r["n"]}))
            if k == 1:  # intra | gap_t
                C2 = np.column_stack([C, gap[j].values, gap["XU100"].values])
                for pn, pm in per_masks.items():
                    y = np.where(pm, intra[j].values, np.nan)
                    r = hreg.nw_batch(y, Xk[1], C2); r["t"][self_i] = np.nan
                    rows.append(pd.DataFrame({"target": j, "leader": LEAD, "dep": "intra_g", "lag": "1", "period": pn,
                                              "b": r["b"], "t": r["t"], "pc": r["pc"], "n": r["n"]}))
                # yıllık (asimetri istikrarı)
                for yr in range(2014, 2027):
                    pm = idx.year == yr
                    for dn in ["cc", "intra"]:
                        y = np.where(pm, deps[dn][j].values, np.nan)
                        r = hreg.nw_batch(y, Xk[1], C, min_n=120); r["t"][self_i] = np.nan
                        rows.append(pd.DataFrame({"target": j, "leader": LEAD, "dep": dn, "lag": "1", "period": f"Y{yr}",
                                                  "b": r["b"], "t": r["t"], "pc": r["pc"], "n": r["n"]}))
        print(jj, j, round(time.time() - t0, 1), flush=True)
    # PRE 2005–2013 (yalnız cc)
    pre = ccL.loc[ccL.index < pd.Timestamp("2014-01-01")]
    LccP = pre[LEAD]
    for j in TGT:
        self_i = LEAD.index(j)
        for k in [1, "c5"]:
            C = ctrl(pre, j, k).values
            r = hreg.nw_batch(pre[j].values, lagX(LccP, k).values, C); r["t"][self_i] = np.nan
            rows.append(pd.DataFrame({"target": j, "leader": LEAD, "dep": "cc", "lag": str(k), "period": "PRE",
                                      "b": r["b"], "t": r["t"], "pc": r["pc"], "n": r["n"]}))
    out = pd.concat(rows, ignore_index=True)
    out["n"] = out["n"].astype("int32")
    for c in ["target", "leader", "dep", "lag", "period"]: out[c] = out[c].astype("category")
    out.to_parquet(os.path.join(hdata.RES, "scan_long.parquet"))
    print("ana tarama bitti", out.shape, round(time.time() - t0, 1))

def run_null(nshift=20, seed=7):
    rng = np.random.default_rng(seed)
    offs = rng.integers(250, T - 250, nshift)
    Lv = cc[LEAD].values
    deps = {"cc": cc, "gap": gap, "intra": intra}
    res = np.full((nshift, len(TGT), 3, 3, len(LEAD)), np.nan, dtype=np.float32)
    t0 = time.time()
    Cs = {j: ctrl(cc, j, 1).values for j in TGT}
    for si, o in enumerate(offs):
        X = pd.DataFrame(np.roll(Lv, o, axis=0), index=idx).shift(1).values
        for jj, j in enumerate(TGT):
            for di, (dn, dd) in enumerate(deps.items()):
                for pi, (pn, pm) in enumerate(per_masks.items()):
                    y = np.where(pm, dd[j].values, np.nan)
                    r = hreg.nw_batch(y, X, Cs[j])
                    res[si, jj, di, pi] = r["t"]
        print("null", si, o, round(time.time() - t0, 1), flush=True)
    np.savez_compressed(os.path.join(hdata.RES, "null_t.npz"), t=res, offs=offs, targets=np.array(TGT), leaders=np.array(LEAD),
                        deps=np.array(list(deps)), periods=np.array(list(per_masks)))

def run_volfilt():
    tov = D["tov"].reindex(idx)
    med = tov.rolling(60, min_periods=20).median().shift(1)
    low = (tov.fillna(0) < 0.3 * med) | (tov.fillna(0) <= 0)
    lowv = low.values
    LI = [cc.columns.get_loc(c) for c in LEAD]
    X = cc[LEAD].shift(1).values.copy()
    lowL1 = pd.DataFrame(lowv[:, LI], index=idx).shift(1).fillna(True).values.astype(bool)
    X[lowL1] = np.nan
    deps = {"cc": cc, "gap": gap, "intra": intra}
    rows = []
    for j in TGT:
        self_i = LEAD.index(j)
        C = ctrl(cc, j, 1).values
        lj = low[j].values; lj1 = low[j].shift(1).fillna(True).values.astype(bool)
        for dn, dd in deps.items():
            for pn, pm in per_masks.items():
                y = np.where(pm & ~lj & ~lj1, dd[j].values, np.nan)
                r = hreg.nw_batch(y, X, C); r["t"][self_i] = np.nan
                rows.append(pd.DataFrame({"target": j, "leader": LEAD, "dep": dn, "lag": "1", "period": pn,
                                          "b": r["b"], "t": r["t"], "pc": r["pc"], "n": r["n"]}))
    out = pd.concat(rows, ignore_index=True); out.to_parquet(os.path.join(hdata.RES, "volfilt.parquet"))
    print("hacim filtresi bitti; maskelenen gün oranı (hedef medyan):", float(low[TGT].mean().median()))

if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("main", "all"): run_main()
    if what in ("vol", "all"): run_volfilt()
    if what in ("null", "all"): run_null()
