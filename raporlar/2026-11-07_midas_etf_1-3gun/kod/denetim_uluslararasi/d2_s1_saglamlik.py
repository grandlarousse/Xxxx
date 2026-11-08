"""Denetim D2: uluslararasi_S1 istatistiksel sağlamlık.
- NW t neden basit t'den büyük (gün serisinin 1. gecikme otokorelasyonu)
- yıl yıl, 2020 / 2022 / 2026 hariç, en iyi 5 işlem / 5 gün hariç
- parametre komşuluğu (eşik x göreli koşul), plato mu sivri mi
- permütasyon: (a) rastgele tarih (ETF yapısı korunur), (b) koşullu: SPY<=-%1,5 günlerinde rastgele ETF seçimi,
  (c) koşullu: yüksek oynaklık (SPY<=-%1,5) günlerinde tüm sepet
- FDR yeniden hesap (6 birincil hipotez; basit t ile)
Çalıştır: python3 -I kod/denetim_uluslararasi/d2_s1_saglamlik.py"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from scipy import stats as st
import sim
from sim import L
from d1_s1_yeniden import SEPET, EK, s1, r_spy

rng = np.random.default_rng(20261107)

def date_series(tr):
    return tr.groupby("sig_date")["net"].mean().sort_index()

def main():
    pd.set_option("display.width", 250); pd.set_option("display.max_rows", 300)
    tr = sim.basket(SEPET, s1(), 1, "C0")
    d = date_series(tr)
    x = d.to_numpy()
    ac1 = pd.Series(x).autocorr(1)
    print(f"Gün serisi n={len(x)} ort={x.mean()*1e4:.1f} bp; basit t={sim.simple_t(x):.2f}; NW(1) t={sim.nw_t(x,1):.2f}; NW(3) t={sim.nw_t(x,3):.2f}; 1. gecikme otokor.={ac1:.3f}")
    gaps = pd.Series(d.index).diff().dt.days.dropna()
    print(f"Ardışık sinyal günleri arası takvim günü: medyan {gaps.median():.0f}, <=3 gün olan oran {(gaps<=3).mean():.2f}")
    # h=1 C0 işlemleri zaman olarak çakışmaz -> NW gerekmez; basit t uygun
    p_simple = st.t.sf(sim.simple_t(x), len(x) - 1); p_nw = st.norm.sf(sim.nw_t(x, 1))
    print(f"tek yönlü p: basit {p_simple:.4f}, NW {p_nw:.4f}; 6 birincil hipotezde BH eşiği (rank1) 0.1/6={0.1/6:.4f}")
    print(f"Bonferroni(6) eşiği 0.05/6={0.05/6:.4f}")

    # yıl yıl
    y = d.groupby(d.index.year).agg(["count", "mean", "sum"]); y[["mean", "sum"]] *= 1e4
    print("\nYıl yıl (sinyal günü ort. net bp):"); print(y.round(1).to_string())

    rows = []
    def add(nm, tt, h=1):
        r = sim.summarize(tt, h); r["set"] = nm; rows.append(r)
    add("tam", tr)
    for ex in ([2020], [2022], [2026], [2020, 2022], [2020, 2026]):
        add(f"{ex} hariç", tr[~tr["sig_date"].dt.year.isin(ex)])
    top5 = tr["net"].nlargest(5).index; add("en iyi 5 işlem hariç", tr.drop(top5))
    top5d = d.nlargest(5).index; add("en iyi 5 gün hariç", tr[~tr["sig_date"].isin(top5d)])
    top10 = tr["net"].nlargest(10).index; add("en iyi 10 işlem hariç", tr.drop(top10))
    add("Mart 2020 hariç", tr[~((tr["sig_date"].dt.year == 2020) & (tr["sig_date"].dt.month == 3))])
    # VIX rejimi
    vix = sim.lib.vol_index("VIX")
    vv = vix.reindex(tr["sig_date"]).to_numpy()
    add("VIX<25 günleri", tr[vv < 25]); add("VIX>=25 günleri", tr[vv >= 25])
    R = pd.DataFrame(rows)
    cols = ["set", "n_dates", "n_trades", "gross_bp", "net_bp", "t_simple", "t_nw", "is_net_bp", "oos_net_bp", "years_pos", "win", "pf"]
    print("\n=== Alt örnekler (C0 h=1, 2.500$) ==="); print(R[cols].round(2).to_string(index=False))
    R.to_csv(os.path.join(sim.OUT, "d2_s1_altornek.csv"), index=False)

    # parametre komşuluğu
    G = []
    for thr in (-0.010, -0.0125, -0.015, -0.0175, -0.020, -0.025):
        for k in (0.75, 1.0, 1.25, 1.5):
            tt = sim.basket(SEPET, s1(thr=thr, k=k), 1, "C0")
            r = sim.summarize(tt, 1); r.update(thr=thr, k=k); G.append(r)
        tt = sim.basket(SEPET, s1(thr=thr, rel=None), 1, "C0")
        r = sim.summarize(tt, 1); r.update(thr=thr, k=np.nan); G.append(r)   # yalnız SPY koşulu (tüm sepet)
        tt = sim.basket(SEPET, s1(thr=thr, rel="gt"), 1, "C0")
        r = sim.summarize(tt, 1); r.update(thr=thr, k=-1); G.append(r)       # tümleyen ETF>SPY
    G = pd.DataFrame(G)
    print("\n=== Parametre komşuluğu (k: ETF<=k*SPY; NaN: yalnız SPY koşulu; -1: tümleyen ETF>SPY) ===")
    print(G[["thr", "k", "n_dates", "n_trades", "gross_bp", "net_bp", "t_simple", "is_net_bp", "oos_net_bp", "years_pos"]].round(2).to_string(index=False))
    G.to_csv(os.path.join(sim.OUT, "d2_s1_komsuluk.csv"), index=False)

    # Permütasyonlar
    # ortak takvim: tüm sepet ETF'lerinin ve SPY'ın ortak günleri
    cal = L("SPY").index
    for s in SEPET: cal = cal.intersection(L(s).index)
    cal = cal[200:-1]
    nxt = {s: (L(s)["c"].shift(-1) / L(s)["c"] - 1) for s in SEPET}
    R1 = pd.DataFrame({s: nxt[s].reindex(cal) for s in SEPET})
    C = pd.Series({s: sim.cost(s) for s in SEPET})
    NET = R1 - C / 1e4
    sets = tr.groupby("sig_date")["sym"].apply(list)
    obs = x.mean()
    # (a) rastgele tarih, ETF yapısı korunur
    NP = 5000; sims = np.empty(NP)
    netv = NET.to_numpy(); col = {s: i for i, s in enumerate(SEPET)}
    setlist = [[col[s] for s in v] for v in sets.values]
    for b in range(NP):
        dd = rng.choice(len(cal), size=len(setlist), replace=False)
        vals = [np.nanmean(netv[i, cs]) for i, cs in zip(dd, setlist)]
        sims[b] = np.nanmean(vals)
    pa = (np.sum(sims >= obs) + 1) / (NP + 1)
    print(f"\n(a) Rastgele tarih permütasyonu ({NP}): gözlenen {obs*1e4:.1f} bp, sim ort {np.nanmean(sims)*1e4:.1f}, %95 {np.nanpercentile(sims,95)*1e4:.1f}, p={pa:.4f}")
    # (b) koşullu: SPY<=-1.5 günlerinde aynı sayıda ETF'i rastgele seç
    spyd = cal[(r_spy.reindex(cal) <= -0.015).to_numpy()]
    kmap = sets.apply(len)
    days_b = [dte for dte in kmap.index if dte in NET.index]
    simsb = np.empty(NP)
    for b in range(NP):
        vals = []
        for dte in days_b:
            row = NET.loc[dte].to_numpy(); ok = np.where(np.isfinite(row))[0]
            pick = rng.choice(ok, size=min(kmap[dte], len(ok)), replace=False)
            vals.append(row[pick].mean())
        simsb[b] = np.mean(vals)
    obs_b = np.mean([NET.loc[dte, sets[dte]].mean() for dte in days_b])
    pb = (np.sum(simsb >= obs_b) + 1) / (NP + 1)
    print(f"(b) Koşullu (aynı SPY düşüş günü, rastgele ETF seçimi): gözlenen {obs_b*1e4:.1f}, sim ort {simsb.mean()*1e4:.1f}, %95 {np.percentile(simsb,95)*1e4:.1f}, p={pb:.4f}")
    # (c) SPY<=-1.5 günlerinden rastgele aynı sayıda gün; tüm sepet (seçim yok) -> 'yalnız SPY düşüşü' boş hipotezi
    simsc = np.empty(NP); ks = kmap.values
    for b in range(NP):
        dd = rng.choice(len(spyd), size=len(days_b), replace=len(spyd) < len(days_b))
        vals = []
        for i, k in zip(dd, ks):
            row = NET.loc[spyd[i]].to_numpy(); ok = np.where(np.isfinite(row))[0]
            pick = rng.choice(ok, size=min(k, len(ok)), replace=False); vals.append(row[pick].mean())
        simsc[b] = np.mean(vals)
    pc = (np.sum(simsc >= obs_b) + 1) / (NP + 1)
    print(f"(c) SPY<=-%1,5 günlerinden rastgele gün + rastgele ETF: sim ort {simsc.mean()*1e4:.1f}, %95 {np.percentile(simsc,95)*1e4:.1f}, p={pc:.4f}; SPY düşüş günü sayısı {len(spyd)}")
    # eşleştirilmiş fark: aynı gün ETF<=SPY eksi ETF>SPY (gross)
    diffs = []
    for dte in spyd:
        row = R1.loc[dte]; rr = pd.Series({s: L(s)["c"].pct_change().get(dte) for s in SEPET})
        a = row[rr <= r_spy[dte]].dropna(); bset = row[rr > r_spy[dte]].dropna()
        if len(a) and len(bset): diffs.append((dte, a.mean() - bset.mean()))
    df_ = pd.Series(dict(diffs))
    print(f"Eşleştirilmiş fark (ETF<=SPY eksi ETF>SPY, brüt): n={len(df_)} ort {df_.mean()*1e4:.1f} bp, t {sim.simple_t(df_.values):.2f}, IS {df_[df_.index<=sim.IS_END].mean()*1e4:.1f} / OOS {df_[df_.index>sim.IS_END].mean()*1e4:.1f}; 2020 hariç {df_[df_.index.year!=2020].mean()*1e4:.1f} (t {sim.simple_t(df_[df_.index.year!=2020].values):.2f})")
    pd.DataFrame({"perm": ["a_rastgele_tarih", "b_kosullu_etf_secimi", "c_spy_dusus_gunu_rastgele"], "obs_bp": [obs*1e4, obs_b*1e4, obs_b*1e4],
                  "sim_mean_bp": [np.nanmean(sims)*1e4, simsb.mean()*1e4, simsc.mean()*1e4], "p": [pa, pb, pc], "n_perm": NP}).to_csv(
        os.path.join(sim.OUT, "d2_s1_permutasyon.csv"), index=False)

    # IBS ile örtüşme: S1 işlemleri sinyal günü IBS'e göre
    ib = []
    for _, r in tr.iterrows():
        df = L(r["sym"]); rng_ = df.loc[r["sig_date"], "h"] - df.loc[r["sig_date"], "l"]
        ib.append((df.loc[r["sig_date"], "c"] - df.loc[r["sig_date"], "l"]) / rng_ if rng_ > 0 else np.nan)
    tr["ibs"] = ib
    for lo, hi in ((0, 0.1), (0.1, 0.3), (0.3, 1.01)):
        part = tr[(tr["ibs"] >= lo) & (tr["ibs"] < hi)]
        print(f"S1 işlemleri IBS [{lo},{hi}): n={len(part)} brüt {part['gross'].mean()*1e4:.1f} net {part['net'].mean()*1e4:.1f} t {sim.simple_t(part['net'].values):.2f}")

    # kaldıraçlı uygulama (dayanak sinyali)
    print("\nKaldıraçlı (dayanak sinyali, C0):")
    for lev, und in (("KORU", "EWY"), ("YINN", "FXI")):
        for h in (1, 2):
            tt = sim.sim(lev, s1(under={lev: und})(lev), h, "C0")
            r = sim.summarize(tt, h, by_date=False)
            print(f"  {lev}<-{und} h={h}: n={r['n_trades']} brüt {r['gross_bp']:.0f} net {r['net_bp']:.0f} t {r['t_simple']:.2f} IS {r['is_net_bp']:.0f} OOS {r['oos_net_bp']:.0f} en kötü {r['worst_bp']:.0f} yıl+ {r['years_pos']:.2f}")
    # Başka ailedeki KWEB (aynı mekanizma, Çin interneti) — bilgi
    for s in ("KWEB", "MCHI", "EWY"):
        tt = sim.sim(s, s1()(s), 1, "C0"); r = sim.summarize(tt, 1, by_date=False)
        print(f"  {s} S1 C0 h1: n={r['n_trades']} net {r['net_bp']:.0f} t {r['t_simple']:.2f} IS {r['is_net_bp']:.0f} OOS {r['oos_net_bp']:.0f}")

if __name__ == "__main__":
    main()
