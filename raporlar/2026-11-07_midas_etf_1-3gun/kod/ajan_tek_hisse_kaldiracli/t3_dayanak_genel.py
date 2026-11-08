"""Görev 2b/3: Genel kütüphane (strategies.LIB, 31 sinyal; parametreler literatür varsayılanı, ayarlanmadı) DAYANAK HİSSELERDE
2016-11..2026-11 boyunca, sentetik 2x günlük sıfırlamalı ETF üzerinden (sinyal hissenin kendi verisinden) test edilir.
Maliyet: dayanağın birincil ETF'inin 2.500$ maliyeti (thk.cost_for). IS = <=2021, OOS = 2022+.
Aile havuzu: 9 dayanak, tarih kümelemeli havuz t (aynı sinyal günündeki işlemler tek gözlem).
Çalıştırma: python3 -I kod/ajan_tek_hisse_kaldiracli/t3_dayanak_genel.py
Çıktılar: dayanak_genel_satirlar.csv, dayanak_genel_havuz.csv"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import thk, lib, strategies as S

pd.set_option("display.width", 260); pd.set_option("display.max_columns", 40); pd.set_option("display.max_rows", 200)
X = thk.ctx()

def build(stock):
    sdf = thk.load_stock(stock)
    syn = thk.synth_for(stock, 2.0)
    return sdf, syn

rows = []; pool = {}
for st in thk.STOCKS:
    sdf, syn = build(st)
    cost = thk.cost_for(thk.PRIMARY[st])
    for name, fn in S.LIB.items():
        sig = fn(sdf, X).reindex(sdf.index).fillna(False).astype(bool)
        sig.iloc[:200] = False
        variants = [(m, h, "sabit", None) for m in ("C0", "O1", "C1") for h in (1, 2, 3)]
        if name in S.EXITS:
            ex = S.EXITS[name](sdf)
            variants += [(m, 3, "kural_max3", ex) for m in ("C0", "O1", "C1")]
        for m, h, exn, ex in variants:
            s, tr = thk.full_stats(syn, sig, h, m, cost, exit_sig=ex, label=name)
            s.update({"stock": st, "sig": name, "exit": exn})
            rows.append(s)
            u = s.get("uncond_bp", np.nan) / 1e4 if s.get("n", 0) else np.nan
            if len(tr):
                # koşulsuz kayma (aynı tutuş yapısı, hayatta kalma yanlılığı içeren sürüklenme) düşülmüş fazla getiri;
                # erken çıkışlı varyantta tutuş süresiyle orantılı ölçeklenir
                tr = tr.assign(stock=st, excess=tr["gross"] - u * (tr["days"] / (h if m != "O1" else h)).clip(upper=1.0))
            pool.setdefault((name, m, h, exn), []).append(tr)
R = pd.DataFrame(rows)
R["fdr"] = lib.bh_fdr(R["p"].values, 0.10)
R.to_csv(os.path.join(thk.OUT, "dayanak_genel_satirlar.csv"), index=False)

hv = []
for (name, m, h, exn), trs in pool.items():
    trs = [t for t in trs if len(t)]
    if not trs: continue
    A = pd.concat(trs, ignore_index=True)
    n, nd, mbp, t = thk.pooled_date_t(trs)
    isx = [t_[t_.sig_date <= lib.IS_END] for t_ in trs]; oos = [t_[t_.sig_date > lib.IS_END] for t_ in trs]
    _, ndi, mi, ti = thk.pooled_date_t([x for x in isx if len(x)])
    _, ndo, mo, to = thk.pooled_date_t([x for x in oos if len(x)])
    sub = R[(R.sig == name) & (R["mode"] == m) & (R.h == h) & (R.exit == exn)]
    yrs = A.groupby(A.sig_date.dt.year)["net"].mean()
    _, _, gbp, _ = thk.pooled_date_t(trs, "gross")
    _, _, ebp, te = thk.pooled_date_t(trs, "excess")
    hv.append({"sig": name, "mode": m, "h": h, "exit": exn, "n": n, "n_tarih": nd, "brut_bp": gbp, "brut_islem_ort_bp": A.gross.mean() * 1e4,
               "net_bp": mbp, "t_havuz": t, "is_net_bp": mi, "is_t": ti, "oos_net_bp": mo, "oos_t": to,
               "hisse_pozitif": int((sub.mean_net_bp > 0).sum()), "hisse_k": len(sub),
               "hisse_is_poz": int((sub.is_net_bp > 0).sum()), "hisse_oos_poz": int((sub.oos_net_bp > 0).sum()),
               "edge_ort_bp": sub.edge_bp.mean(), "edge_havuz_bp": ebp, "t_edge_havuz": te, "yil_poz": float((yrs > 0).mean()), "kazanma": float((A.net > 0).mean())})
H = pd.DataFrame(hv)
H["p_havuz"] = [lib.t_to_p(t, n) for t, n in zip(H.t_havuz, H.n_tarih)]
H["fdr_havuz"] = lib.bh_fdr(H["p_havuz"].values, 0.10)
H = H.sort_values("t_havuz", ascending=False)
H.to_csv(os.path.join(thk.OUT, "dayanak_genel_havuz.csv"), index=False)
print("satır:", len(R), "hisse-düzeyi FDR geçen:", int(R.fdr.sum()), "| havuz testleri:", len(H), "havuz FDR geçen:", int(H.fdr_havuz.sum()))
print(H.head(40).round(2).to_string())
print(H.tail(12).round(2).to_string())
ok = H[(H.net_bp > 0) & (H.t_havuz >= 2.5) & (H.is_net_bp > 0) & (H.oos_net_bp > 0) & (H.yil_poz >= 0.6)]
print("\nZamanlama değeri (koşulsuz sürüklenme düşülmüş) en yüksek 20:")
print(H.sort_values("t_edge_havuz", ascending=False).head(20)[["sig","mode","h","exit","n","n_tarih","brut_bp","net_bp","t_havuz","edge_havuz_bp","t_edge_havuz","is_net_bp","oos_net_bp","hisse_pozitif","yil_poz"]].round(2).to_string())
print("\nHavuz ön eleme (net>0, t>=2.5, IS>0, OOS>0, yıl>=0.6):"); print(ok.round(2).to_string())
