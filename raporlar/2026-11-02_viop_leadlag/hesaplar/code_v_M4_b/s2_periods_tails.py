"""s2: Alt donemler (2014-17, 2018-20, 2021-23, 2024-26), uc deger bagimliligi (en iyi 10/20 gun), uzun/kisa, en iyi gunlerin listesi.
Iki kurgu: A = kendi takvim (benim), B = ffill (orijinale benzer)."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vb, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
cA, _ = vb.comp(vb.JP_AU); cB, _ = vb.comp_ffill(vb.JP_AU)
XU = vb.bist("XU100.IS")
P = [("2014-17", "2014-01-01", "2018-01-01"), ("2018-20", "2018-01-01", "2021-01-01"), ("2021-23", "2021-01-01", "2024-01-01"), ("2024-26", "2024-01-01", "2027-01-01")]
rows, tails, best = [], [], []
for cn, c in [("A", cA), ("B", cB)]:
    for s in ["EREGL.IS", "KRDMD.IS", "BRSAN.IS"]:
        b = vb.bist(s); o = vb.bt(c, b.intra, 15, 1.0)
        for pn, a, e in P:
            oo = o[(o.index >= a) & (o.index < e)]; st = vb.stats(oo)
            cc = pd.concat([c.rename("c"), b.intra.rename("y")], axis=1).dropna(); cc = cc[(cc.index >= a) & (cc.index < e)]
            r, t, n = vb.corr_t(cc.c, cc.y)
            rows.append(dict(kurgu=cn, stock=s, period=pn, n_trades=st["n"], net_bps=st["bps"], t=st["t"], corr=r, corr_t=t, n_days=n,
                             long_bps=1e4 * oo[oo.pos > 0].pnl.mean(), short_bps=1e4 * oo[oo.pos < 0].pnl.mean()))
        for lab, msk in [("ALL", o.index == o.index), ("OOS", o.index >= vb.SPLIT), ("IS", o.index < vb.SPLIT)]:
            a = o[msk & (o.pos != 0)].copy()
            tot = a.pnl.sum(); srt = a.pnl.sort_values(ascending=False)
            for k in (0, 5, 10, 20):
                rest = a.drop(srt.index[:k]) if k else a
                tails.append(dict(kurgu=cn, stock=s, sample=lab, drop_best=k, n=len(rest), net_bps=1e4 * rest.pnl.mean(), t=vb.nwt(rest.pnl),
                                  share_of_total=(srt.iloc[:k].sum() / tot) if k else np.nan))
            # simetrik: en iyi k ve en kotu k birlikte atilinca
            for k in (10, 20):
                rest = a.drop(srt.index[:k]).drop(srt.index[-k:])
                tails.append(dict(kurgu=cn, stock=s, sample=lab, drop_best=f"best{k}+worst{k}", n=len(rest), net_bps=1e4 * rest.pnl.mean(), t=vb.nwt(rest.pnl)))
            # winsorize %1/%99 getiri
            y = a.y.clip(a.y.quantile(0.01), a.y.quantile(0.99)); pw = a.pos * y - 15e-4
            tails.append(dict(kurgu=cn, stock=s, sample=lab, drop_best="winsor1-99", n=len(a), net_bps=1e4 * pw.mean(), t=vb.nwt(pw)))
        if cn == "A":
            a = o[o.pos != 0].copy(); a["xu_intra"] = XU.intra.reindex(a.index)
            top = a.sort_values("pnl", ascending=False).head(10)
            for d, r_ in top.iterrows():
                best.append(dict(stock=s, date=d.date(), pos=r_.pos, z=round(r_.z, 2), intra_pct=round(100 * r_.y, 2), xu100_intra_pct=round(100 * r_.xu_intra, 2), pnl_bps=round(1e4 * r_.pnl, 1)))
R = pd.DataFrame(rows); Tt = pd.DataFrame(tails); B = pd.DataFrame(best)
R.to_csv(os.path.join(vb.OUT, "res_s2_periods.csv"), index=False); Tt.to_csv(os.path.join(vb.OUT, "res_s2_tails.csv"), index=False); B.to_csv(os.path.join(vb.OUT, "res_s2_best10.csv"), index=False)
pd.set_option("display.width", 250)
print(R.round(3).to_string()); print(Tt.round(3).to_string()); print(B.to_string())
