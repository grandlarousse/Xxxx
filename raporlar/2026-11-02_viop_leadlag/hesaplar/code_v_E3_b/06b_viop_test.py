import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_E3_b")
"""06b: Gerçek enstrüman testi — VİOP F_TUPRS (en yüksek hacimli vade) açılış->kapanış getirisi; Yahoo açılışından BAĞIMSIZ.
Ayrıca likidite ve açılış seansı istatistikleri (2023+ bülten sütunları)."""
import vb, numpy as np, pandas as pd
V = pd.read_parquet(vb.RES + "/viop_rows.parquet")
V = V[(V["TRADE COUNT"] > 0) & (V["OPENING PRICE"] > 0) & (V["CLOSING PRICE"] > 0)]
def front(g):
    return g.sort_values("TRADE VOLUME", ascending=False).iloc[0]
TU = V[V.und == "TUPRS"].groupby("date").apply(front); XU = V[V.und == "XU030"].groupby("date").apply(front)
F = pd.read_parquet(vb.RES + "/F.parquet")
cal = F.index
tu = vb.bist_dec("TUPRS.IS", cal); x30 = vb.bist_dec("XU030.IS", cal)
W = pd.DataFrame(index=TU.index)
W["f_intra"] = np.log(TU["CLOSING PRICE"] / TU["OPENING PRICE"]); W["f_intra_set"] = np.log(TU["SETTLEMENT PRICE"] / TU["OPENING PRICE"])
W["x_intra"] = np.log(XU["CLOSING PRICE"] / XU["OPENING PRICE"]).reindex(W.index)
W["f_h"] = W.f_intra - W.x_intra
W["trades"] = TU["TRADE COUNT"]; W["val_mn"] = TU["TRADED VALUE"] / 1e6; W["oi"] = TU["OPEN POSITION"]
W["os_px"] = TU.get("OPENING SESSION PRICE"); W["os_val"] = TU.get("TRADED VALUE AT OPENING SESSION"); W["os_n"] = TU.get("TRADE COUNT AT OPENING SESSION")
W["os_open_eq"] = (W.os_px == TU["OPENING PRICE"]).where(W.os_px.notna() & (W.os_px > 0))
W["s_intra"] = tu.intra.reindex(W.index); W["s_open"] = tu.o.reindex(W.index); W["s_close"] = tu.c.reindex(W.index)
W["sig"] = F["A_USREF"].reindex(W.index)
W["y_h30"] = (tu.intra - x30.intra).reindex(W.index)
# temizlik: |f_intra|>0,2 veya bariz hatalı
W.loc[W.f_intra.abs() > 0.2, ["f_intra", "f_h"]] = np.nan
W = W[W.index >= "2017-01-01"]
W.to_parquet(vb.RES + "/06_viop_daily.parquet")
pd.set_option("display.width", 220)
Y = W.groupby(W.index.year)
print("Yıllık: gün, corr(vadeli gün-içi, spot gün-içi), medyan|fark| bps, medyan işlem sayısı, medyan işlem değeri mn TL, medyan AP")
print(pd.DataFrame({"n": Y.f_intra.count(), "corr_f_s": Y.apply(lambda g: g.f_intra.corr(g.s_intra)), "med_absdiff_bps": Y.apply(lambda g: 1e4 * (g.f_intra - g.s_intra).abs().median()),
                    "med_trades": Y.trades.median(), "med_val_mnTL": Y.val_mn.median(), "med_oi": Y.oi.median(),
                    "os_med_val_TL": Y.os_val.median(), "os_med_n": Y.os_n.median(), "os_open_eq_frac": Y.os_open_eq.mean()}).round(3).to_string())
# İmza testi: vadeli gün-içi ~ sinyal
s = F["A_USREF"]
rows = []
for nm in ["f_intra", "f_intra_set", "f_h", "s_intra", "y_h30"]:
    for pk, a, b in [("2017-18", "2017", "2019"), ("2020-22", "2020", "2023"), ("2023-26", "2023", "2027"), ("tüm bülten günleri", "2017", "2027"), ("2020-26", "2020", "2027")]:
        g = W[(W.index >= a) & (W.index < b)]
        if g[nm].notna().sum() < 100: continue
        p, t, n = vb.nw(g[nm], g[["sig"]]); rows.append(dict(y=nm, per=pk, b_bps_per1pct=100 * p["sig"], t=t["sig"], n=n))
print("\nRegresyon (NW t): hedef ~ A_USREF"); print(pd.DataFrame(rows).pivot_table(index="y", columns="per", values="t").round(2).to_string())
print(pd.DataFrame(rows).pivot_table(index="y", columns="per", values="n").to_string())
# BT: z F'nin tam geçmişinden (2013+) hesaplanır, sonra bülten günlerine uygulanır
z = vb.zsig(s.dropna(), 250).reindex(W.index)
pos = np.sign(z).where(z.abs() > 1, 0.0)
print("\nBT |z|>1 (z tam sinyal geçmişinden): bps/işlem, t, n")
for nm, legs in [("f_intra", 1), ("s_intra", 1), ("f_h", 2), ("y_h30", 2)]:
    for pk, a, b in [("2017-18", "2017", "2019"), ("2020-22", "2020", "2023"), ("2023-26", "2023", "2027"), ("tümü", "2017", "2027")]:
        m = (W.index >= a) & (W.index < b) & (pos != 0) & W[nm].notna()
        p = (pos * W[nm])[m]
        if len(p) < 20: continue
        c8 = 8 if legs == 1 else 11; c15 = 15 if legs == 1 else 18
        print(f"  {nm:8s} {pk:8s}: brüt {1e4*p.mean():6.1f} (t {vb.tstat(p):.2f}, n {len(p)}) | net {c8}: {1e4*p.mean()-c8:6.1f} | net {c15}: {1e4*p.mean()-c15:6.1f} | isabet {(p>0).mean():.2f}")
# ortak günlerde vadeli vs spot
m = (pos != 0) & W.f_intra.notna() & W.s_intra.notna()
print(f"\nOrtak işlem günleri n={m.sum()}: vadeli {1e4*(pos*W.f_intra)[m].mean():.1f} bps vs spot {1e4*(pos*W.s_intra)[m].mean():.1f} bps")
