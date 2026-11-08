"""A ızgarası, çapraz varlık 15:00 fiyatları panel_spot dk_* sütunlarından (as-of; USDJPY Eki-Kas 2026 dakikadan yamalı).
Doğrulama: rep01'de panel dk_*_p15 = Dukascopy 14:00 barı kapanışı (ortak günlerde 0 fark), eksik barda daha erken barın kapanışı (ileriye bakma yok)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a5_esz_artik_rep")
from rep_lib import *
sp = pd.read_parquet(f"{P}/panel_spot.parquet"); sp.index = pd.to_datetime(sp.index)
va = pd.read_parquet(f"{OUT}/viop_rep.parquet"); V = lambda s: s.reindex(va.index); Y = {h: va[f"fwd{h}"] for h in (1, 3, 5)}
syms = dict(XAG="XAGUSD", DXY="DOLLARIDXUSD", TBOND="USTBONDTRUSD", SPX="USA500IDXUSD", USDJPY="USDJPY", USDCNH="USDCNH", BTC="BTCUSD", EURUSD="EURUSD", COPPER="COPPERCMDUSD")
models = {"XAG": ["XAG"], "DXY": ["DXY"], "TBOND": ["TBOND"], "SPX": ["SPX"], "USDJPY": ["USDJPY"], "USDCNH": ["USDCNH"], "BTC": ["BTC"],
          "EURUSD": ["EURUSD"], "MACRO3": ["DXY", "TBOND", "SPX"], "FX3": ["EURUSD", "USDJPY", "USDCNH"], "ALL7": ["XAG", "DXY", "TBOND", "SPX", "USDJPY", "USDCNH", "COPPER"]}
g = np.log(sp.xau_p15).diff()
for clean in (False, True):
    px = pd.DataFrame({k: sp[f"dk_{v}_p15"] for k, v in syms.items()})
    if clean:  # yalnız TBOND 2018-02-06 ve 2018-02-27 açık hatalı baskılar
        px.loc[["2018-02-06", "2018-02-27"], "TBOND"] = np.nan
    X = np.log(px).diff()
    rows = []
    for m, cols in models.items():
        for W in (60, 120, 250):
            rr = rolling_ols(g, X[cols], W)
            for k in (1, 3, 5):
                z = rr.e.rolling(k, min_periods=k).sum() / (rr.sig * np.sqrt(k))
                for h in (1, 3, 5):
                    st = stats(V(z), Y[h], h)
                    rows.append(dict(test=f"A_{m}_W{W}_k{k}_h{h}", m=m, W=W, k=k, h=h, **{a: b for a, b in st.items() if a != "by_year"}))
    A = pd.DataFrame(rows); A.to_csv(f"{OUT}/rep_agrid_panel_clean{int(clean)}.csv", index=False)
    print(f"\n[clean={clean}] A testleri {len(A)}: |t|>2 {int((A.t.abs() > 2).sum())} ({(A.t.abs() > 2).mean():.1%}), maks|t| {A.t.abs().max():.2f}, "
          f"IS->OOS aynı işaret {(np.sign(A.t_is) == np.sign(A.t_oos)).mean():.2f}, IC>0 {(A.ic > 0).mean():.2f}")
    for h in (1, 3, 5):
        s = A[A.h == h].loc[lambda d: d.t_is.abs().idxmax()]; print(f"  IS seçimi h{h}: {s.test} t_is {s.t_is:.2f} -> OOS {s.t_oos:.2f}, full {s.t:.2f}")
    print(A.reindex(A.t.abs().sort_values(ascending=False).index).head(5)[["test", "t", "t_is", "t_oos", "yrs"]].round(2).to_string())
    can = A[(A.W == 120) & (A.k == 1)]; print("  kanonik W120 k1 maks |t|:", round(can.t.abs().max(), 2), can.loc[can.t.abs().idxmax(), "test"])
# analistin grid'i ile karşılaştır
G = pd.read_csv(f"{S}/out/a5_esz_artik/grid_viop.csv"); G = G[G.fam == "A_resid"].set_index("test_id")
A = A.set_index("test")
j = A.join(G[["t", "t_is", "t_oos"]], rsuffix="_an")
print("\nbenim(clean) vs analist A t: korelasyon", round(j.t.corr(j.t_an), 4), " maks |fark|", round((j.t - j.t_an).abs().max(), 3), j.assign(d=(j.t - j.t_an).abs()).d.idxmax())
