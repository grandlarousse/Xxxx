"""5) Sektör ajanlarının 1. tur iddialarını (master_findings_r1 + f_kimya/f_metal/f_otomotiv/f_tarama) ortak-faktör çerçevesinde yeniden test et.
SENKRON iddia: hisse_t ~ [küresel 8×(t,t-1) + USDTRY(t,t-1) + TUR_{t-1} + XU100_t + sektör akranı_t] + sürücü_t + sürücü_{t-1};
   sürücünün kendisi kontrol setindeyse kontrolden çıkarılır. Ölçüt: sürücü_t kısmi korelasyonu + (t, t-1) ortak HC1 Wald.
ÖNCÜLÜK iddiası: hedef (gap/intra/cc)_t ~ [hisse_{t-1}, XU100_{t-1}, küresel 8_{t-1}, USDTRY_{t-1}, TUR_{t-1}] + sürücü_{t-k}.
Dönemler: tam (2014–2026) ve OOS (2021–2026). BH-FDR ilişki sınıfı içinde.
"""
import re, numpy as np, pandas as pd
from common import *
import ll
from scipy import stats
from common import *

def load_claims():
    m = pd.read_csv(os.path.join(OUT, "master_findings_r1.csv")); ex = []
    for f in ["kimya", "metal", "otomotiv", "tarama"]:
        x = pd.read_csv(os.path.join(OUT, f"f_{f}.csv")); x["agent"] = f; ex.append(x)
    A = pd.concat([m] + ex, ignore_index=True); A["cid"] = np.arange(len(A)); return A

def parse(row):
    rel = row["relation"]; lag = str(row["lag"]).strip().lower()
    if rel == "sync": return ("sync", 0)
    if rel in ("lead_gap", "lead_intra", "lead_multiday"):
        if "2-5" in lag: return ("multi25", 2)
        if "->" in lag and "gece" not in lag:  # gün-içi segment iddiaları (r1, rest, saatlik) günlük çerçevede test edilemez
            seg = lag.split("->")[-1].strip()
            if seg not in ("gap", "intra", "cc"): return (None, None)
        if "gece" in lag: k = 1
        elif "aynı gün" in lag or lag in ("0", "0.0"): k = 0
        else:
            try: k = int(float(lag))
            except Exception: return (None, None)
        tgt = {"lead_gap": "gap", "lead_intra": "intra", "lead_multiday": "cc"}[rel]
        if "rest" in lag: return (None, None)
        return (tgt, k)
    return (None, None)

def hc1(y, X, j):
    """y ~ X (sabit dahil); j: test edilen sütun indeksleri. Dönüş: b_j0, t_j0, p_joint, pc_j0."""
    n, k = X.shape; XtX = X.T @ X
    b = np.linalg.solve(XtX, X.T @ y); e = y - X @ b
    inv = np.linalg.inv(XtX); V = inv @ ((X * e[:, None] ** 2).T @ X) @ inv * n / (n - k)
    bj = b[j]; Vj = V[np.ix_(j, j)]; W = float(bj @ np.linalg.solve(Vj, bj)); p = stats.chi2.sf(W, len(j))
    # kısmi korelasyon (ilk test sütunu | diğer tüm sütunlar)
    others = [i for i in range(k) if i != j[0]]
    Xo = X[:, others]; bo = np.linalg.lstsq(Xo, np.column_stack([y, X[:, j[0]]]), rcond=None)[0]
    R = np.column_stack([y, X[:, j[0]]]) - Xo @ bo; pc = np.corrcoef(R[:, 0], R[:, 1])[0, 1]
    return b[j[0]], b[j[0]] / np.sqrt(V[j[0], j[0]]), p, pc

if __name__ == "__main__":
    A = load_claims(); P = panel(); F = factors(); DEC = pd.read_parquet(os.path.join(SCR, "data", "panel_decomp_bist.parquet"))
    A["test"], A["k"] = zip(*A.apply(parse, axis=1))
    A["dcol"] = A["driver_yahoo"].map(lambda d: col(str(d)) if isinstance(d, str) else None)
    T = A[A["stock"].isin(STOCKS) & A["dcol"].notna() & A["test"].notna()].copy()
    keys = T[["stock", "dcol", "test", "k"]].drop_duplicates().values.tolist()
    print("iddia:", len(A), "test edilebilir:", len(T), "tekil test:", len(keys), flush=True)
    G0 = [g for g in GLOBAL]; res = []
    REUSE = os.environ.get("REUSE") == "1" and os.path.exists(os.path.join(CACHE, "claims_tests.csv"))
    for st, dc, test, k in ([] if REUSE else keys):
        d = P[dc]; own_ctrl = [g for g in G0 + ["TRY=X", "TUR"] if g != dc]
        for pn, (a, b) in [("tam", ("2014-01-01", "2026-10-30")), ("OOS", ("2021-01-01", "2026-10-30"))]:
            if test == "sync":
                y = P[st + ".IS"]
                C = [F[g] for g in own_ctrl if g in GLOBAL] + [F[g + "_l1"] for g in own_ctrl if g in GLOBAL]
                C += [F["TRY=X"], F["TRY=X_l1"]] if dc != "TRY=X" else []
                C += [F["TUR_l1"]] if dc != "TUR" else []
                C += [F["XU100"]] if dc != "XU100.IS" else []
                peers = [col(p) for p in CL[SECT[st]] if p != st]
                C += [peer_factor(st)] if dc not in peers else []
                X = [d, d.shift(1)]
            else:
                y = P[st + ".IS"] if test in ("cc", "multi25") else DEC[(st, test)].reindex(P.index)
                C = [P[st + ".IS"].shift(1), F["XU100_l1"]] + [F[g + "_l1"] for g in own_ctrl]
                if test == "multi25": X = [sum(d.shift(j) for j in range(2, 6))]
                else: X = [d.shift(int(k))]
            Dm = pd.concat([y.rename("y")] + [c.rename(f"c{i}") for i, c in enumerate(C)] + [x.rename(f"x{i}") for i, x in enumerate(X)], axis=1)
            Dm = Dm[(Dm.index >= a) & (Dm.index <= b)].dropna()
            if len(Dm) < 150: continue
            xc = [c for c in Dm if c.startswith("x")]; cc_ = [c for c in Dm if c.startswith("c")]
            M = np.column_stack([np.ones(len(Dm)), Dm[xc].values, Dm[cc_].values])
            try: b1, t1, pj, pc = hc1(Dm["y"].values, M, list(range(1, 1 + len(xc))))
            except Exception: continue
            # karşılaştırma: yalnız XU100 kontrollü (senkron) / yalnız kendi lag + XU100 lag (öncülük)
            if test == "sync":
                D2 = pd.concat([y.rename("y"), F["XU100"].rename("m"), d.rename("x")], axis=1); D2 = D2[(D2.index >= a) & (D2.index <= b)].dropna()
                pc_xu, _ = ll.partial_corr(D2["y"], D2["x"], [D2["m"]]) if dc != "XU100.IS" else (np.nan, 0)
                raw = D2["y"].corr(D2["x"])
            else:
                D2 = pd.concat([y.rename("y"), X[0].rename("x"), P[st + ".IS"].shift(1).rename("o"), F["XU100_l1"].rename("m")], axis=1)
                D2 = D2[(D2.index >= a) & (D2.index <= b)].dropna()
                pc_xu, _ = ll.partial_corr(D2["y"], D2["x"], [D2["o"], D2["m"]]); raw = D2["y"].corr(D2["x"])
            res.append({"stock": st, "dcol": dc, "test": test, "k": k, "period": pn, "n": len(Dm), "raw_corr": raw, "pc_light": pc_xu,
                        "pc_full": pc, "b": b1, "t": t1, "p_joint": pj})
    R = pd.DataFrame(res) if not REUSE else pd.read_csv(os.path.join(CACHE, "claims_tests.csv")).drop(columns=["q"])
    R["q"] = np.nan
    for (pn, tst), g in R.groupby(["period", R["test"].eq("sync")]):
        rej, q = ll.fdr(g["p_joint"].values); R.loc[g.index, "q"] = q
    R.to_csv(os.path.join(CACHE, "claims_tests.csv"), index=False)
    # iddialarla birleştir
    W = R.pivot_table(index=["stock", "dcol", "test", "k"], columns="period", values=["raw_corr", "pc_light", "pc_full", "t", "q", "n"]).reset_index()
    W.columns = ["_".join([c for c in col_ if c]) if isinstance(col_, tuple) else col_ for col_ in W.columns]
    T = T.merge(W, on=["stock", "dcol", "test", "k"], how="left")
    def sgn(r):
        for c in (["pcorr_xu100", "corr_full"] if r["test"] == "sync" else (["gap_corr", "corr_full", "t_stat"] if r["test"] == "gap" else ["intra_corr", "corr_full", "t_stat"])):
            v = pd.to_numeric(r.get(c), errors="coerce")
            if pd.notna(v) and v != 0: return np.sign(v)
        return np.nan
    T["claim_sign"] = T.apply(sgn, axis=1)
    def verdict(r):
        if pd.isna(r.get("pc_full_tam")): return "test edilemedi"
        s = np.sign(r["pc_full_tam"]); same = (pd.isna(r["claim_sign"]) or s == r["claim_sign"])
        # OOS = önceden belirlenmiş hipotezin replikasyonu: tekil t (sürücü_t / sürücü_{t-k}) aynı işaret ve |t|>=2
        oos_ok = pd.notna(r.get("pc_full_OOS")) and np.sign(r["pc_full_OOS"]) == s and abs(r.get("t_OOS", 0)) >= 2
        if r["q_tam"] < 0.05 and same and abs(r["pc_full_tam"]) >= 0.05 and oos_ok: return "AYAKTA (faktör-sonrası, OOS tutarlı)"
        if r["q_tam"] < 0.05 and same and oos_ok: return "AYAKTA ama küçük (|pc|<0,05)"
        if r["q_tam"] < 0.05 and same: return "ZAYIF (tam dönemde var, OOS'ta yok/zayıf)"
        if r["q_tam"] < 0.05 and not same: return "İŞARET TERS"
        if abs(r.get("raw_corr_tam", 0)) >= 0.1 or (pd.notna(r.get("pc_light_tam")) and abs(r["pc_light_tam"]) >= 0.05): return "SADECE ORTAK FAKTÖR"
        return "ZATEN ZAYIF / GÜRÜLTÜ"
    T["verdict"] = T.apply(verdict, axis=1)
    MIR = ["TKC", "AKBTY", "TKGBY", "TYIDY", "YKBNY", "TUR", "TURKF", "HALKF", "TRYUSD=X"]
    def cls(d):
        if d in GLOBAL + ["TRY=X", "TUR", "XU100.IS"]: return "ORTAK"
        if d in MIR: return "AYNA"
        if str(d).endswith(".IS"): return "BIST"
        return "DIS"
    T["dclass"] = T["dcol"].map(cls)
    T.loc[(T.dclass == "ORTAK") & T.verdict.isin(["SADECE ORTAK FAKTÖR", "ZATEN ZAYIF / GÜRÜLTÜ"]), "verdict"] = "ORTAK FAKTÖRÜN KENDİSİ (küresel blok içinde ikame)"
    T.loc[(T.dclass == "AYNA") & T.verdict.str.startswith("AYAKTA"), "verdict"] = "AYNA (ADR/ETF; mekanik)"
    T.loc[(T.dclass == "BIST") & T.verdict.str.startswith("AYAKTA"), "verdict"] = "AYAKTA = yerli küme/sektör faktörü"
    # 'ikiz' sürücü: kontrol setimdeki bir faktörle |r|>0,8 (ör. GLD~GC=F, CL=F~BZ=F, NQ=F~ES=F) -> o faktörün kendi testine bak
    FAC = GLOBAL + ["TRY=X", "TUR", "XU100.IS"]; Pp = P[P.index >= START]
    twin = {}
    for dc in T["dcol"].dropna().unique():
        if dc in FAC: continue
        cc = Pp[FAC].corrwith(Pp[dc]).abs()
        if cc.max() > 0.8: twin[dc] = cc.idxmax()
    T["twin"] = T["dcol"].map(twin)
    own_v = T[T.dclass == "ORTAK"].set_index(["stock", "dcol", "test", "k"])["verdict"].to_dict()
    def tw(r):
        if pd.isna(r["twin"]) or not (r["verdict"] in ("SADECE ORTAK FAKTÖR", "ZATEN ZAYIF / GÜRÜLTÜ")): return r["verdict"]
        v = own_v.get((r["stock"], r["twin"], r["test"], r["k"]))
        if v is not None and str(v).startswith("AYAKTA"): return f"AYAKTA (faktör ikizi: {r['twin']})"
        return f"ORTAK FAKTÖRÜN İKİZİ ({r['twin']})"
    T["verdict"] = T.apply(tw, axis=1)
    T["short_sample"] = T["n_tam"] < 1200
    T.loc[T.short_sample & T.verdict.str.startswith("AYAKTA"), "verdict"] = T.loc[T.short_sample & T.verdict.str.startswith("AYAKTA"), "verdict"] + " [kısa örneklem]"
    def nc(x):
        x = str(x).upper()
        if x.startswith(("YÜKSEK", "YUKSEK")): return "YÜKSEK"
        if x.startswith("ORTA"): return "ORTA"
        if x.startswith(("ÇOK", "COK")): return "ÇOK DÜŞÜK"
        if x.startswith(("DÜŞÜK", "DUSUK")): return "DÜŞÜK"
        return "?"
    T["conf_orig"] = T["confidence"].map(nc)
    T.to_csv(os.path.join(CACHE, "claims_verdicts.csv"), index=False)
    print(T.groupby(["test", "verdict"]).size().to_string())
    print(pd.crosstab(T["conf_orig"], T["verdict"]).to_string())
