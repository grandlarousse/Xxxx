"""Hipotez test çalıştırıcısı: bir kuralı dayanaklarda (sentetik kaldıraçlı ETF, 2016+) ve gerçek ETF'lerde (2022+) koşturur,
hisse-düzeyi ve tarih kümelemeli havuz satırlarını kayda (REG) ekler."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import thk, lib

REG = []      # tüm testler (hisse ve havuz düzeyi)
TRADES = {}   # (hipotez, varyant, stock) -> işlem tablosu

_S = {}; _SYN = {}
def S(st):
    if st not in _S: _S[st] = thk.load_stock(st)
    return _S[st]

def SYN(st, L):
    k = (st, L)
    if k not in _SYN: _SYN[k] = thk.synth_for(st, L)
    return _SYN[k]

def _row(base, s):
    r = dict(base)
    for k in ("n", "mean_gross_bp", "mean_net_bp", "median_net_bp", "win", "pf", "t", "maxdd", "worst_bp", "uncond_bp",
              "edge_bp", "t_edge", "is_n", "is_net_bp", "is_t", "oos_n", "oos_net_bp", "oos_t", "years_pos_frac", "n_years"):
        r[k] = s.get(k, np.nan)
    r["p"] = lib.t_to_p(r.get("t", np.nan), r.get("n", 0) or 0)
    return r

def run(hyp, sig_fn, stocks, L=2.0, modes=("C0", "O1", "C1"), hs=(1, 2, 3), exit_fn=None, primary=None,
        cost_etf=None, note="", tradeable=True, max_h_exit=None):
    """sig_fn(st, sdf) -> bool Seri (t kapanışında bilinir). exit_fn(st, sdf) -> bool Seri (opsiyonel).
    primary: (mode, h) ön-kayıtlı ana varyant. cost_etf: {stock: etf} maliyet için (varsayılan PRIMARY)."""
    out = []
    for m in modes:
        for h in hs:
            trs = []
            for st in stocks:
                sdf = S(st); syn = SYN(st, L)
                sig = sig_fn(st, sdf).reindex(sdf.index).fillna(False).astype(bool)
                sig.iloc[:60] = False
                ex = exit_fn(st, sdf) if exit_fn else None
                etf = (cost_etf or {}).get(st, thk.PRIMARY.get(st))
                cost = thk.cost_for(etf)
                s, tr = lib.evaluate(syn, sig, h=h, mode=m, cost=cost, exit_sig=ex, label=hyp)
                var = f"{m}_h{h}"
                is_prim = primary is not None and (m, h) == tuple(primary)
                REG.append(_row({"hipotez": hyp, "duzey": "hisse", "stock": st, "L": L, "mode": m, "h": h, "varyant": var,
                                 "on_kayitli": is_prim, "cost_bp": cost, "not": note}, s))
                if len(tr):
                    u = s.get("uncond_bp", 0.0) / 1e4
                    tr = tr.assign(stock=st, excess=tr["gross"] - u)
                    trs.append(tr)
                TRADES[(hyp, var, st)] = tr
            n, nd, mb, t = thk.pooled_date_t(trs)
            _, _, gb, _ = thk.pooled_date_t(trs, "gross")
            _, _, eb, te = thk.pooled_date_t(trs, "excess")
            isx = [x[x.sig_date <= lib.IS_END] for x in trs]; oos = [x[x.sig_date > lib.IS_END] for x in trs]
            _, ndi, mi, ti = thk.pooled_date_t(isx)
            _, ndo, mo, to = thk.pooled_date_t(oos)
            A = pd.concat(trs, ignore_index=True) if trs else pd.DataFrame(columns=["sig_date", "net", "gross"])
            yp = float((A.groupby(A.sig_date.dt.year)["net"].mean() > 0).mean()) if len(A) else np.nan
            sub = [r for r in REG if r["hipotez"] == hyp and r["duzey"] == "hisse" and r["varyant"] == f"{m}_h{h}" and r["L"] == L]
            row = {"hipotez": hyp, "duzey": "havuz", "stock": "+".join(stocks), "L": L, "mode": m, "h": h, "varyant": f"{m}_h{h}",
                   "on_kayitli": primary is not None and (m, h) == tuple(primary), "n": n, "n_tarih": nd,
                   "mean_gross_bp": gb, "mean_net_bp": mb, "t": t, "edge_bp": eb, "t_edge": te,
                   "is_n": ndi, "is_net_bp": mi, "is_t": ti, "oos_n": ndo, "oos_net_bp": mo, "oos_t": to,
                   "years_pos_frac": yp, "win": float((A.net > 0).mean()) if len(A) else np.nan,
                   "worst_bp": float(A.net.min() * 1e4) if len(A) else np.nan,
                   "hisse_pozitif": sum(1 for r in sub if (r["mean_net_bp"] or -1) > 0), "hisse_k": len(sub), "not": note}
            row["p"] = lib.t_to_p(t, nd) if nd else np.nan
            REG.append(row); out.append(row)
    return pd.DataFrame(out)

def real_check(hyp, sig_fn, etfs, mode, h, exit_fn=None, since=None):
    """Sinyal dayanak hisseden, işlem gerçek ETF verisinde (lib.load). since: kaldıraç geçiş tarihi sonrası alt dönem."""
    rows = []; trs = []
    for e in etfs:
        st = thk.UNDER[e]
        d = lib.load(e)
        sdf = S(st).reindex(d.index)
        sig = sig_fn(st, S(st)).reindex(d.index).fillna(False).astype(bool)
        ex = exit_fn(st, S(st)).reindex(d.index).fillna(False).astype(bool) if exit_fn else None
        if since:
            sig = sig & (d.index >= pd.Timestamp(since.get(e, "1900-01-01")) if isinstance(since, dict) else d.index >= pd.Timestamp(since))
        cost = thk.cost_for(e)
        s, tr = lib.evaluate(d, sig, h=h, mode=mode, cost=cost, exit_sig=ex, label=hyp)
        # aynı işlemlerin 2x (L x) dayanak karşılığı (oynaklık/yol kaybı ölçümü)
        if len(tr):
            sc = S(st)["c"]; so = S(st)["o"]
            ent = so.reindex(tr.entry_date).values if mode == "O1" else sc.reindex(tr.entry_date).values
            ext = sc.reindex(tr.exit_date).values
            Lnom = float(thk.tarama().loc[e, "lev"])
            tr = tr.assign(etf=e, stock_ret=ext / ent - 1)
            tr["Lx_stock"] = Lnom * tr["stock_ret"]
            trs.append(tr)
        r = _row({"hipotez": hyp, "duzey": "gercek_etf", "stock": e, "mode": mode, "h": h, "varyant": f"{mode}_h{h}",
                  "cost_bp": cost, "not": "since" if since else ""}, s)
        if len(tr):
            r["sapma_vs_Lx_bp"] = float((tr["gross"] - tr["Lx_stock"]).mean() * 1e4)
        rows.append(r)
    n, nd, mb, t = thk.pooled_date_t(trs)
    _, _, gb, _ = thk.pooled_date_t(trs, "gross")
    rows.append({"hipotez": hyp, "duzey": "gercek_havuz", "stock": "+".join(etfs), "mode": mode, "h": h, "varyant": f"{mode}_h{h}",
                 "n": n, "n_tarih": nd, "mean_gross_bp": gb, "mean_net_bp": mb, "t": t, "p": lib.t_to_p(t, nd) if nd else np.nan,
                 "not": "since" if since else ""})
    return pd.DataFrame(rows), trs
