"""v4: (i) saatlik bar bazında katkı profili (sinyal yönünde her saatlik dilimin brüt getirisi), (ii) beta120 varyantı (min 90),
(iii) TUR_{t-1} -> THYAO gün-içi yıllık corr, (iv) COMBO / AIR IS-OOS ve son 3 yıl, maliyet 8/15, (v) temizlikte atılan gün sayısı,
(vi) kaynakta denenen varyant sayısı için kaba çoklu test düzeltmesi."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_A4_a")
from vcore import *
from scipy import stats
pd.set_option("display.width", 250)
ST = ["THYAO.IS", "PGSUS.IS", "TAVHL.IS"]
SA = pd.read_parquet(OUTD + "/v1_signals_A.parquet")
sig = SA.AIR.shift(1)
D = {s: bist_day(s) for s in ST}

if __name__ == "__main__":
    # (i) saatlik profil
    print("=== Sinyal yönündeki brüt getiri, saatlik dilimlere göre (bps/işlem, 2023-11..2026-10; dilim sonu UTC) ===")
    for s in ST + ["XU030.IS"]:
        d = bist_day(s); h = raw(s, "h1").copy(); h["hm"] = h.index.strftime("%H:%M"); h.index = pd.DatetimeIndex(h.ldate)
        P = h.pivot_table(index=h.index, columns="hm", values="c", aggfunc="last")
        P.insert(0, "open", d.o.reindex(P.index)); P["close"] = d.c.reindex(P.index)
        cols = ["open", "06:30", "07:30", "08:30", "09:30", "10:30", "11:30", "12:30", "13:30"]
        # 14:30 barı kışın eksik: 13:30 kapanışından günlük kapanışa tek dilim
        endlab = lambda c: (pd.Timestamp("2000-01-01 " + c) + pd.Timedelta(hours=1)).strftime("%H:%M")
        R = pd.DataFrame({f"->{endlab(c2)}": np.log(P[c2] / P[c1]) for c1, c2 in zip(cols[:-1], cols[1:])})
        R["13:30bar->kapanış"] = np.log(P["close"] / P["13:30"])
        R = R[d.intra.reindex(R.index).notna()]
        df = R.join(sig.rename("s"), how="inner"); pos = np.sign(df.s).where(df.s.abs() > 1, 0)
        a = pos != 0
        prof = {c: 1e4 * (pos[a] * df[c][a]).mean() for c in R.columns}
        tt = {c: (pos[a] * df[c][a]).mean() / (pos[a] * df[c][a]).std() * np.sqrt(a.sum()) for c in R.columns}
        tot = (pos[a] * R.sum(axis=1, min_count=len(R.columns))[a.index][a]).mean() * 1e4
        print(s.replace(".IS", ""), "n", int(a.sum()), " ".join(f"{k}:{v:+.1f}(t{tt[k]:+.1f})" for k, v in prof.items()), f"| toplam(tam günler) {tot:+.1f}")
    # (ii) beta120
    x = build_signals(drv_ret_cal, w_beta=120)
    import vcore
    def rres120(y, xx): return vcore.rresid(y, xx, 120, 90)
    EU, _ = basket(EU_AIR); US, _ = basket(US_AIR)
    a120 = zs(rres120(EU, drv_ret_cal("^STOXX"))).clip(-3, 3) + zs(rres120(US, drv_ret_cal("^GSPC"))).clip(-3, 3)
    print("\n=== beta penceresi 120 (min 90) ===")
    for s in ST:
        o, _, _ = bt(a120.shift(1), D[s].intra, 8, 1.0)
        print(s, {p: {k: round(o[p].get(k, np.nan), 2) for k in ["n", "bps", "t_nw"]} for p in ["IS", "OOS"]})
    # (iii) TUR yıllık
    print("\n=== corr(TUR_{t-1}, gün-içi_t) yıllara göre ===")
    for s in ST:
        j = pd.concat([D[s].intra.rename("y"), SA.TUR.shift(1).rename("x")], axis=1).dropna()
        yc = j.groupby(j.index.year).apply(lambda g: g.y.corr(g.x)).round(3)
        print(s, yc.to_dict(), " negatif yıl:", int((yc < 0).sum()), "/", len(yc))
    # (iv) son 3 yıl ve maliyet
    print("\n=== Son 3 yıl (2023-11-01..) ve 2024+ , AIR ve COMBO, 8/15 bps ===")
    for nm in ["AIR", "COMBO"]:
        for s in ST:
            for cost in [8, 15]:
                for a_ in ["2023-11-01", "2024-01-01"]:
                    o, _, _ = bt(SA[nm].shift(1), D[s].intra, cost, 1.0, start=a_, split=pd.Timestamp("2100-01-01")); d = o["ALL"]
                    print(f"{nm:5s} {s:9s} cost{cost:2d} {a_}+ n={d['n']} net={d['bps']:.1f} t={d['t_nw']:.2f} brüt={d['gross_bps']:.1f}")
    # (v) temizlik
    print("\n=== Temizlikte NaN olan günler (2014+) ===")
    for s in ST:
        d = raw(s).copy(); d.index = pd.DatetimeIndex(d.ldate); d = d[d.index >= "2014-01-01"]
        cc = np.log(d.adj).diff(); bad = (cc > UP) | (cc < DN); v0 = (d.v.fillna(0) <= 0).sum()
        print(s, "fiyat ±%10,5 dışı:", int(bad.sum()), list(d.index[bad].strftime("%Y-%m-%d"))[:8], " hacimsiz gün:", int(v0))
    # (vi) çoklu test: kaynakta ~14 sinyal varyantı x 3 hisse denendi (a5: B1a-B1f, a5b: 8 sinyal). Bonferroni (14) / (42)
    print("\n=== Kaba çoklu test (iki yönlü normal p) ===")
    for lab, t in [("THYAO OOS", 2.77), ("PGSUS OOS", 2.78), ("TAVHL OOS", 2.31), ("THYAO ALL sürekli reg", 4.42), ("PGSUS ALL sürekli reg", 4.51), ("TAVHL ALL sürekli reg", 3.23)]:
        p = 2 * (1 - stats.norm.cdf(abs(t))); print(f"{lab}: t={t} p={p:.4f} Bonf14={min(1,p*14):.3f} Bonf42={min(1,p*42):.3f}")
    print("ok")
