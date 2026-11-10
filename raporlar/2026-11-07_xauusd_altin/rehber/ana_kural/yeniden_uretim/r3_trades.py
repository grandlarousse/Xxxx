"""r3: sade islem (yalniz uzun; sinyal gunu uzlasmada AL, son sinyalden H gun sonra uzlasmada SAT)."""
import json
from rep_lib import *
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 60); pd.set_option("display.max_rows", 400)
D = pd.read_parquet(f"{OUT}/rep_signal_viop.parquet")
thr = json.load(open(f"{OUT}/rep_esik.json"))
TH = {"A": thr["A_2008_2017_w250"], "C": thr["C_tum_<=2017_min60 (ana ajan)"]}
r = D.ret
bh = (np.exp(r) - 1)
print("B&H (her gun uzun, maliyetsiz): Sharpe tam %.2f | 2017-21 %.2f | 2022-26 %.2f | 2018-26 %.2f | yillik %%%.1f | vol %%%.1f | maks dusus %%%.1f | toplam %%%.0f" % (
    sharpe(bh), sharpe(bh[:"2021"]), sharpe(bh["2022":]), sharpe(bh["2018":]), bh.mean() * 252 * 100, bh.std() * np.sqrt(252) * 100, maxdd(bh) * 100, ((1 + bh).prod() - 1) * 100))
rows = []
TR = {}
for tn, th in TH.items():
    sig = (D.x > th).astype(float)
    for H in (3, 5):
        for c in (5, 22):
            T, net, pos = run_trades(r, sig, H, c)
            Tc = T[T.closed]
            al = alpha_vs_bh(net, bh); al18 = alpha_vs_bh(net["2018":], bh["2018":]); al22 = alpha_vs_bh(net["2022":], bh["2022":]); al1721 = alpha_vs_bh(net[:"2021"], bh[:"2021"])
            alx = alpha_vs_bh(net[:"2024"], bh[:"2024"])
            row = dict(esik=tn, H=H, maliyet=c, islem=len(Tc), acik=int((~T.closed).sum()), ort_sure=Tc.days.mean(), ort_net=Tc.net.mean() * 100, med_net=Tc.net.median() * 100,
                       ort_brut=Tc.gross.mean() * 100, kazanan=(Tc.net > 0).mean() * 100, enkotu=Tc.net.min() * 100, eniyi=Tc.net.max() * 100,
                       sharpe=sharpe(net), sh_1721=sharpe(net[:"2021"]), sh_2226=sharpe(net["2022":]), sh_1826=sharpe(net["2018":]), sh_1724=sharpe(net[:"2024"]),
                       yillik=net.mean() * 252 * 100, piyasada=pos.mean() * 100, alfa=al["alpha_ann"], alfa_t=al["t"], beta=al["beta"],
                       alfa1826=al18["alpha_ann"], alfa1826_t=al18["t"], alfa1721_t=al1721["t"], alfa2226_t=al22["t"], alfa1724=alx["alpha_ann"], alfa1724_t=alx["t"], maxdd=maxdd(net) * 100,
                       islem_t=Tc.net.mean() / Tc.net.std() * np.sqrt(len(Tc)))
            rows.append(row); TR[(tn, H, c)] = (T, net, pos)
RES = pd.DataFrame(rows)
print("\nSADE ISLEM OZETI"); print(RES.round(2).T.to_string())
RES.to_csv(f"{OUT}/rep_islem_ozet.csv", index=False)

for key in [("C", 3, 5), ("C", 5, 5), ("A", 3, 5), ("A", 5, 5)]:
    T, net, pos = TR[key]; Tc = T[T.closed].copy()
    print(f"\n--- islem dagilimi esik {key[0]} H={key[1]} {key[2]} bps: n {len(Tc)}; sure dagilimi", Tc.days.describe()[["mean", "50%", "max"]].round(1).to_dict())
    y = Tc.groupby(Tc.entry.dt.year).net.agg(["size", "mean", "sum", lambda z: (z > 0).mean()]); y.columns = ["n", "ort%", "toplam%", "kazanan"]; y[["ort%", "toplam%", "kazanan"]] *= 100
    print(y.round(2).T.to_string())
    print("  en kotu 5:", [(a.date().isoformat(), b.date().isoformat(), round(v * 100, 2)) for a, b, v in Tc.nsmallest(5, "net")[["entry", "exit", "net"]].values])
    print("  en iyi 5 :", [(a.date().isoformat(), b.date().isoformat(), round(v * 100, 2)) for a, b, v in Tc.nlargest(5, "net")[["entry", "exit", "net"]].values])
    tot = Tc.net.sum(); top5 = Tc.nlargest(5, "net").net.sum()
    print(f"  toplam net (basit toplam) %{tot*100:.1f}; en iyi 5 islemin payi %{top5/tot*100:.0f}; 2025-26 payi %{Tc[Tc.entry >= '2025-01-01'].net.sum()/tot*100:.0f}; 2017 payi %{Tc[Tc.entry < '2018-01-01'].net.sum()/tot*100:.0f}")
    # yil yil gunluk pnl: strateji vs (piyasada kalma orani x B&H)
    yy = pd.DataFrame({"strateji%": net.groupby(net.index.year).sum() * 100, "B&H%": bh.groupby(bh.index.year).sum() * 100, "piyasada": pos.groupby(pos.index.year).mean()})
    yy["beklenen(rastgele)%"] = yy["B&H%"] * yy["piyasada"]; yy["fazla%"] = yy["strateji%"] - yy["beklenen(rastgele)%"]
    print(yy.round(2).T.to_string()); print("  fazla>0 yil:", int((yy["fazla%"] > 0).sum()), "/ 10")
    T.to_csv(f"{OUT}/rep_islemler_{key[0]}_H{key[1]}.csv", index=False)

# plasebo: ayni blok yapisiyla rastgele zamanlama (dairesel kaydirma) -> Sharpe ve alfa dagilimi
print("\nPLASEBO (sinyal dizisi dairesel kaydirilir; 2000 tekrar), 5 bps:")
rng = np.random.default_rng(11)
for tn in ("A", "C"):
    sig = (D.x > TH[tn]).astype(float)
    for H in (3, 5):
        T, net, pos = TR[(tn, H, 5)]
        obs_sh = sharpe(net); obs_al = alpha_vs_bh(net, bh)["alpha_ann"]; obs_mean = T[T.closed].net.mean()
        shs, als, mns = [], [], []
        for k in range(2000):
            s2 = pd.Series(np.roll(sig.values, rng.integers(30, len(sig) - 30)), index=sig.index)
            T2, n2, p2 = run_trades(r, s2, H, 5)
            shs.append(sharpe(n2)); mns.append(T2[T2.closed].net.mean())
            d = np.column_stack([np.ones(len(n2)), bh.fillna(0).values]); als.append(np.linalg.lstsq(d, n2.values, rcond=None)[0][0] * 252 * 100)
        shs, als, mns = np.array(shs), np.array(als), np.array(mns)
        print(f"  esik {tn} H={H}: Sharpe {obs_sh:.2f} (plasebo ort {shs.mean():.2f}, %95 {np.quantile(shs, .95):.2f}, p {np.mean(shs >= obs_sh):.3f}) | alfa %{obs_al:.1f} (plasebo ort {als.mean():.1f}, p {np.mean(als >= obs_al):.3f}) | islem ort %{obs_mean*100:.2f} (plasebo ort {mns.mean()*100:.2f}, p {np.mean(mns >= obs_mean):.3f})")
