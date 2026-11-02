"""s09b: GERÇEK enstrüman testi — VİOP pay vadelisi (aktif kontrat = önceki gün en yüksek açık pozisyon) açılış->kapanış getirisi.
Sinyaller: 600547.SS D_t (07:00 UTC), 1787.HK D_t (08:10, örtüşmeli), 2899.HK D_t, SHFE HC D_t. + likidite istatistikleri."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_C4C5_b")
from vb import *
V = pd.read_parquet(sys.path[0] + "/viop_ssf_sel.parquet")
V["und"] = V["UNDERLYING"].str.replace(".E", "", regex=False).replace({"KOZAL": "TRALT", "KOZAA": "TRMET"})
def active(und):
    x = V[V.und == und].copy()
    x = x[x["TRADE COUNT"].fillna(0) > 0]
    days = sorted(V[V.und == und]["TRADE DATE"].unique())
    oi = V[V.und == und].pivot_table(index="TRADE DATE", columns="INSTRUMENT SERIES", values="OPEN POSITION", aggfunc="last")
    rows = []
    for i in range(1, len(days)):
        t0, t1 = days[i - 1], days[i]
        if t0 not in oi.index: continue
        o = oi.loc[t0].dropna()
        cand = x[(x["TRADE DATE"] == t1)]
        if len(cand) == 0 or len(o) == 0: continue
        # önceki gün OI en yüksek ve hâlâ işlem gören kontrat; vade günü ise bir sonrakine geç
        ser = [s for s in o.sort_values(ascending=False).index if s in set(cand["INSTRUMENT SERIES"])]
        if not ser: continue
        r = cand[cand["INSTRUMENT SERIES"] == ser[0]].iloc[0]
        if pd.notna(r["EXPIRATION DATE"]) and r["EXPIRATION DATE"] <= t1 and len(ser) > 1:
            r = cand[cand["INSTRUMENT SERIES"] == ser[1]].iloc[0]
        rows.append(dict(d=t1, ser=r["INSTRUMENT SERIES"], o=r["OPENING PRICE"], c=r["CLOSING PRICE"], vwap=r["VWAP"], val=r["TRADED VALUE"], n=r["TRADE COUNT"], oi=r["OPEN POSITION"], os_px=r.get("OPENING SESSION PRICE"), os_val=r.get("TRADED VALUE AT OPENING SESSION")))
    a = pd.DataFrame(rows).set_index("d")
    a["fint"] = np.log(a.c / a.o)
    a.loc[(a.o <= 0) | (a.c <= 0) | (a.fint.abs() > np.log(1.105)), "fint"] = np.nan
    return a
OUT = []
for und in ["TRALT", "KRDMD"]:
    a = active(und)
    sp = bist_dec(und + ".IS")
    j = pd.concat([a.fint, sp.intra.rename("sint")], axis=1).dropna()
    print(f"\n### {und} VİOP: {len(a)} gün {a.index.min().date()}..{a.index.max().date()} | vadeli gün-içi ~ spot gün-içi korelasyonu {j.fint.corr(j.sint):.3f} (n {len(j)}); ort fark {1e4*(j.fint-j.sint).mean():+.1f} bps")
    liq = a.groupby(a.index.year).agg(val_mn=("val", lambda x: x.median() / 1e6), trades=("n", "median"), os_val_k=("os_val", lambda x: x.median() / 1e3), os_share=("os_px", lambda x: x.notna().mean()))
    print("  likidite (yıllık medyan): işlem hacmi mn TL / işlem sayısı / açılış seansı hacmi bin TL / açılış seansı oluşma oranı")
    print("  ", liq.round(2).to_dict("index"))
    sigs = {"600547.SS": to_bist(loc_ret("600547.SS", "adj"), "zero"), "1787.HK": to_bist(loc_ret("1787.HK", "adj"), "zero"), "2899.HK": to_bist(loc_ret("2899.HK", "adj"), "zero"), "SHFE_HC": to_bist(sina_roll("HC")["cc"], "zero")}
    for nm, s in sigs.items():
        s = s.reindex(a.index)
        b, t, n = nw_t(a.fint, s); bs, ts, ns = nw_t(sp.intra.reindex(a.index), s)
        line = f"  {nm:9s} -> VİOP gün-içi r={b:+.3f} t={t:+.2f} n={n} | (aynı günler spot gün-içi r={bs:+.3f} t={ts:+.2f})"
        for cost in [8, 10, 15]:
            r, _, _ = bt(s, a.fint, cost); line += f" | c{cost}: {r['ALL'].get('bps', np.nan):+.1f}bps t{r['ALL'].get('t', np.nan):+.2f} Sh{r['ALL'].get('sh', np.nan):.2f}"
        print(line)
        r, pnl, pos = bt(s, a.fint, 10); by = (1e4 * pnl[pos != 0].groupby(pnl[pos != 0].index.year).mean()).round(1).to_dict()
        print("      yıllık net10:", by)
        OUT.append(dict(und=und, sig=nm, r=b, t=t, n=n))
pd.DataFrame(OUT).to_csv(sys.path[0] + "/s09_viop_results.csv", index=False)
