"""2) Diebold–Yilmaz spillover (Pesaran–Shin genelleştirilmiş FEVD, H=10), VAR(1) OLS.
Düğümler: 47 VİOP hissesi + XU100 + 10 sürücü (ES, EEM, Stoxx50, VIX, DXY, Brent, Altın, ABD10y, USDTRY, TUR).
Hizalama: A = ham BIST takvimi (sürücü_t BIST kapanışından sonra biter); B = ABD/FX kapanışlı sürücüler 1 gün ileri
(sürücü_{t-1} BIST_t satırında = 'BIST t+1 ile hizalı'); C = saatlik 15:00 UTC anlık fiyat (gerçek senkron, 2024-06+).
Çalıştır: nice -n 10 python3 dy.py
"""
import numpy as np, pandas as pd, time
from common import *
import ll
DRV = ["ES=F", "EEM", "^STOXX50E", "^VIX", "DX-Y.NYB", "BZ=F", "GC=F", "^TNX", "TRY=X", "TUR"]
SHORT = {"ES=F": "ES", "EEM": "EEM", "^STOXX50E": "SX5E", "^VIX": "VIX", "DX-Y.NYB": "DXY", "BZ=F": "BRENT", "GC=F": "ALTIN",
         "^TNX": "US10Y", "TRY=X": "USDTRY", "TUR": "TUR", "XU100.IS": "XU100"}

def matrix(stocks, drivers=DRV, align="A"):
    P = panel(); cols = [s + ".IS" for s in stocks] + ["XU100.IS"]
    M = P[cols].rename(columns=lambda c: c[:-3])
    for d in drivers:
        x = P[d]
        if align == "B" and d in US_CLOSE: x = x.shift(1)
        M[SHORT[d]] = x
    if align == "C":
        cal = P.index
        for d in drivers:
            try:
                s = ll.snap_daily(d, "15:00"); s.index = pd.DatetimeIndex(s.index)
                s = s.reindex(cal); r = np.log(s).diff()
                M[SHORT[d]] = r
            except Exception as e:
                print("snap fail", d, e); M[SHORT[d]] = np.nan
    return M

def var_fit(Y, p=1, ridge=0.0):
    T, N = Y.shape
    X = np.hstack([np.ones((T - p, 1))] + [Y[p - k - 1:T - k - 1] for k in range(p)])
    Yt = Y[p:]
    if ridge > 0:
        Xs = X.copy(); XtX = Xs.T @ Xs; pen = ridge * (T - p) * np.eye(XtX.shape[0]); pen[0, 0] = 0
        B = np.linalg.solve(XtX + pen, Xs.T @ Yt)
    else:
        B = np.linalg.lstsq(X, Yt, rcond=None)[0]
    E = Yt - X @ B; S = E.T @ E / (len(E) - X.shape[1])
    A = [B[1 + k * N:1 + (k + 1) * N].T for k in range(p)]  # A_k: N×N, y_t = c + Σ A_k y_{t-k}
    return A, S

def gfevd(A, S, H=10):
    N = S.shape[0]; p = len(A)
    Psi = [np.eye(N)]
    for h in range(1, H):
        acc = np.zeros((N, N))
        for k in range(1, min(h, p) + 1): acc += A[k - 1] @ Psi[h - k]
        Psi.append(acc)
    num = np.zeros((N, N)); den = np.zeros(N); sd = np.diag(S)
    for P_ in Psi:
        PS = P_ @ S; num += PS ** 2; den += np.einsum("ij,ij->i", PS, P_)
    th = num / sd[None, :] / den[:, None]
    return th / th.sum(1, keepdims=True)  # satır i: i'nin FEV'sinin j'den gelen payı

def summarize(th, names):
    N = len(names); off = th - np.diag(np.diag(th))
    frm = off.sum(1); to = off.sum(0); net = to - frm
    total = off.sum() / N
    return total, pd.DataFrame({"to": to, "from": frm, "net": net, "own": np.diag(th)}, index=names)

def fit_window(M, p=1, ridge=0.0, H=10, minfrac=0.9):
    ok = M.notna().mean() >= minfrac; X = M.loc[:, ok].fillna(0.0)
    X = X.loc[:, X.std() > 0]
    A, S = var_fit(X.values, p, ridge); th = gfevd(A, S, H)
    return th, list(X.columns)

def rolling(M, w=250, step=5, label="", ridge=0.0):
    idx = M.index; rows = []; node_rows = []
    for e in range(w, len(idx) + 1, step):
        W = M.iloc[e - w:e]
        th, names = fit_window(W, ridge=ridge)
        tot, tab = summarize(th, names)
        dt = idx[e - 1]
        stocks = [n for n in names if n in STOCKS]; drv = [n for n in names if n in SHORT.values() and n != "XU100"]
        si = [names.index(n) for n in stocks]; di = [names.index(n) for n in drv]
        # bloklar arası: hisselerin FEV'sinin küresel/TR sürücülerden, XU100'den, diğer hisselerden gelen payı
        glob = [names.index(n) for n in drv if n not in ("USDTRY", "TUR")]; trm = [names.index(n) for n in drv if n in ("USDTRY", "TUR")]
        xu = names.index("XU100") if "XU100" in names else None
        sub = th[np.ix_(si, range(len(names)))]
        from_glob = sub[:, glob].sum(1).mean(); from_tr = sub[:, trm].sum(1).mean()
        from_xu = sub[:, [xu]].sum(1).mean() if xu is not None else np.nan
        from_oth = (sub[:, si].sum(1) - np.diag(th)[si]).mean()
        to_glob_from_bist = th[np.ix_(glob, si + ([xu] if xu is not None else []))].sum(1).mean()
        rows.append({"date": dt, "label": label, "N": len(names), "total": 100 * tot, "stk_from_global": 100 * from_glob,
                     "stk_from_tr": 100 * from_tr, "stk_from_xu100": 100 * from_xu, "stk_from_otherstk": 100 * from_oth,
                     "stk_own": 100 * np.diag(th)[si].mean(), "glob_from_bist": 100 * to_glob_from_bist})
        t2 = tab.copy(); t2["date"] = dt; t2["label"] = label; node_rows.append(t2.reset_index().rename(columns={"index": "node"}))
    return pd.DataFrame(rows), pd.concat(node_rows, ignore_index=True)

def static(M, a, b, label, p=1, ridge=0.0):
    W = M[(M.index >= a) & (M.index <= b)]
    th, names = fit_window(W, p=p, ridge=ridge)
    tot, tab = summarize(th, names)
    return tot, tab, th, names

if __name__ == "__main__":
    t0 = time.time()
    fixed = [s for s in STOCKS if s not in ("ASTOR", "SOKM", "ENJSA")]
    res_tot = []; res_node = []
    for al in ["A", "B"]:
        M = matrix(fixed, align=al); M = M[(M.index >= START)]
        tt, nn = rolling(M, label=f"fixed44_{al}"); res_tot.append(tt); res_node.append(nn)
        print("rolling", al, round(time.time() - t0, 1), flush=True)
    # ridge sağlamlık (A)
    M = matrix(fixed, align="A"); M = M[M.index >= START]
    tt, _ = rolling(M, step=10, label="fixed44_A_ridge", ridge=0.05); res_tot.append(tt)
    # tam set (47) 2023+
    for al in ["A", "B"]:
        M = matrix(STOCKS, align=al); M = M[M.index >= "2023-01-20"]
        tt, nn = rolling(M, label=f"full47_{al}"); res_tot.append(tt); res_node.append(nn)
    pd.concat(res_tot).to_csv(os.path.join(CACHE, "dy_rolling_total.csv"), index=False)
    pd.concat(res_node).to_csv(os.path.join(CACHE, "dy_rolling_nodes.csv.gz"), index=False)
    print("rolling done", round(time.time() - t0, 1), flush=True)
    # statik dönemler (A ve B), tüm mevcut düğümler
    st_rows = []; pair_rows = []
    for al in ["A", "B"]:
        M = matrix(STOCKS, align=al)
        for pn, (a, b) in PERIODS.items():
            tot, tab, th, names = static(M, a, b, pn)
            tab = tab.reset_index().rename(columns={"index": "node"}); tab["period"] = pn; tab["align"] = al; tab["total"] = 100 * tot
            st_rows.append(tab)
            N = len(names)
            for i in range(N):
                for j in range(N):
                    if i < j:
                        pair_rows.append({"align": al, "period": pn, "a": names[i], "b": names[j], "a_to_b": th[j, i], "b_to_a": th[i, j], "net_a_to_b": th[j, i] - th[i, j]})
    pd.concat(st_rows).to_csv(os.path.join(CACHE, "dy_static_nodes.csv"), index=False)
    pd.DataFrame(pair_rows).to_csv(os.path.join(CACHE, "dy_static_pairs.csv.gz"), index=False)
    # VAR(2) sağlamlık, tam dönem A
    M = matrix(STOCKS, align="A"); tot2, tab2, _, _ = static(M, "2014-01-01", "2026-10-30", "tam", p=2)
    tab2.to_csv(os.path.join(CACHE, "dy_static_tam_A_var2.csv")); print("VAR2 total", 100 * tot2)
    # C hizalaması karşılaştırması (2024-06-11 .. 2026-10-30), EEM/TUR hariç (15:00 UTC'de ABD nakit seansı kapalı/eksik)
    drvC = ["ES=F", "^STOXX50E", "^VIX", "DX-Y.NYB", "BZ=F", "GC=F", "^TNX", "TRY=X"]
    cmp_rows = []
    for al in ["A", "B", "C"]:
        M = matrix(STOCKS, drivers=drvC, align=al)
        W = M[(M.index >= "2024-06-12") & (M.index <= "2026-10-30")]
        tot, tab, th, names = static(W, "2024-06-12", "2026-10-30", "C-pencere")
        tab = tab.reset_index().rename(columns={"index": "node"}); tab["align"] = al; tab["total"] = 100 * tot
        # sürücü -> hisse ortalama, hisse -> sürücü ortalama
        si = [names.index(n) for n in names if n in STOCKS]
        for dname in [SHORT[d] for d in drvC]:
            if dname in names:
                j = names.index(dname)
                tab.loc[tab.node == dname, "to_stocks_mean"] = 100 * th[si, j].mean()
                tab.loc[tab.node == dname, "from_stocks_sum"] = 100 * th[j, si].sum()
                tab.loc[tab.node == dname, "n_obs"] = len(W.dropna(subset=[dname]))
        cmp_rows.append(tab)
        print("C-cmp", al, round(100 * tot, 2), flush=True)
    pd.concat(cmp_rows).to_csv(os.path.join(CACHE, "dy_align_compare.csv"), index=False)
    print("done", round(time.time() - t0, 1))
