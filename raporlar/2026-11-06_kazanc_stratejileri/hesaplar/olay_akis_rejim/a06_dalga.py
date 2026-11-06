"""(A-ek) Piyasa capinda geri alim DALGASI: bir haftada GA_YENI (60 gun sessizlik sonrasi ilk geri alim bildirimi) sayisi.
Dalga haftasi = sayi >= 8 (onceden secilmis esik; ayrica >= 12). Ortusmeyi onlemek icin dalgalar arasinda en az 8 hafta.
Giris: dalga haftasinin son islem gunu kapanisi. Cikti: XU100 ve esit agirlikli kucuk hisse (panel, likidite sirasi > 100) ileri 4/8/13 hafta."""
import numpy as np, pandas as pd
import ortak as O
E = pd.read_pickle(O.MY + "/olaylar_A.pkl"); E = E[E.olay == "GA_YENI"].copy(); E["t0"] = pd.to_datetime(E.t0)
TK = O.islem_gunleri(); TK = TK[TK <= "2026-11-05"]
xu = O.endeks("XU100").reindex(TK)
px = pd.read_parquet(O.DATA + "/bist_test/panel_px.parquet"); rk = pd.read_parquet(O.DATA + "/bist_test/panel_liqrank.parquet")
r = px.pct_change().where(rk.shift(1) > 100); ew = (1 + r.mean(axis=1).fillna(0)).cumprod().reindex(TK).ffill()
wk = E.groupby(E.t0.dt.to_period("W-FRI")).size()
wk = wk.reindex(pd.period_range("2018-01-05", "2026-11-06", freq="W-FRI"), fill_value=0)
out = [f"Haftalik GA_YENI sayisi: ortalama {wk.mean():.1f}, medyan {wk.median():.0f}, %90 {wk.quantile(.9):.0f}, en yuksek 10 hafta:\n\n" + O.md(wk.sort_values().tail(10).rename("n").to_frame())]
def ileri(s, t, n):
    i = s.index.get_indexer([t])[0]; return s.iloc[i + n] / s.iloc[i] - 1 if 0 <= i and i + n < len(s) else np.nan
for esik in (8, 12):
    rows = []; last = None
    for p, n in wk.items():
        if n < esik: continue
        if last is not None and (p - last).n < 8: continue
        last = p; t = TK[TK <= p.end_time][-1]
        rows.append({"hafta": str(p), "n": n, "giris": t.date(), "XU100_4h%": 100 * ileri(xu, t, 20), "XU100_8h%": 100 * ileri(xu, t, 40), "XU100_13h%": 100 * ileri(xu, t, 65),
                     "kucuk_EW_8h%": 100 * ileri(ew, t, 40), "kucuk_EW_13h%": 100 * ileri(ew, t, 65), "onceki_4h_XU100%": 100 * (xu.loc[t] / xu.iloc[xu.index.get_loc(t) - 20] - 1)})
    D = pd.DataFrame(rows).set_index("hafta")
    base = {h: 100 * np.nanmean(xu.values[n_:] / xu.values[:-n_] - 1) for h, n_ in [("4h", 20), ("8h", 40), ("13h", 65)]}
    out.append(f"\n#### Dalga esigi >= {esik}/hafta (dalgalar arasi >= 8 hafta). Kosulsuz XU100 ort: 4h {base['4h']:.2f}%, 8h {base['8h']:.2f}%, 13h {base['13h']:.2f}%\n\n" + O.md(D.round(1)))
    x = D["XU100_13h%"].dropna(); out.append(f"esik {esik}: dalga {len(D)}, 13h XU100 ort {x.mean():.1f}%, medyan {x.median():.1f}%, pozitif {int((x>0).sum())}/{len(x)}")
open(O.OUTD + "/A_dalga.md", "w").write("\n".join(out)); print("\n".join(out))
