"""(A) Eslestirilmis kontrol: ham BHAR'in (hisse - XU100) esit agirlikli kucuk hisse primi + carpiklik + kisa vadeli geri donus (olay oncesi dusus)
nedeniyle sistematik pozitif olmasi beklenir (insider SATIS'larinda bile +). Bu yuzden her olay icin AYNI GUN, ayni
'olay oncesi 20g AR' beslisi x '60g medyan TL hacim' uclusu kovasindaki tum diger hisselerin ortalama ileri AR'si cikarilir.
Panel: kardes ajanin temiz getiri paneli (bist_test/panel_px, panel_liq; yalniz bugun islem gorenler).
Cikti: k5/k20/k60 = olay AR - kova ortalamasi; ozet tablolar cikti/A_kontrol.md"""
import numpy as np, pandas as pd
import ortak as O
R = pd.read_pickle(O.MY + "/A_sonuc.pkl")
px = pd.read_parquet(O.DATA + "/bist_test/panel_px.parquet"); liq = pd.read_parquet(O.DATA + "/bist_test/panel_liq.parquet")
px.index = pd.DatetimeIndex(px.index); liq.index = pd.DatetimeIndex(liq.index)
xu = O.endeks("XU100").reindex(px.index).ffill()
F = {h: px.shift(-h).div(px) .sub(1).sub(xu.shift(-h) / xu - 1, axis=0) for h in O.HZ}
PRE = px.shift(1).div(px.shift(21)).sub(1).sub(xu.shift(1) / xu.shift(21) - 1, axis=0)
rows = []
for r in R.itertuples():
    t = r.t0
    if t not in px.index: continue
    pre_cs = PRE.loc[t]; liq_cs = liq.loc[t]
    ok = pre_cs.notna() & liq_cs.notna()
    if ok.sum() < 60: continue
    qp = pre_cs[ok].quantile([.2, .4, .6, .8]).values; ql = liq_cs[ok].quantile([1 / 3, 2 / 3]).values
    bp = np.searchsorted(qp, pre_cs[ok].values); bl = np.searchsorted(ql, liq_cs[ok].values)
    # olay hissesinin kendi kovasi
    e_pre = PRE.at[t, r.kod] if r.kod in PRE.columns and pd.notna(PRE.at[t, r.kod]) else r.on
    e_liq = liq.at[t, r.kod] if r.kod in liq.columns and pd.notna(liq.at[t, r.kod]) else r.vol20
    if not np.isfinite(e_pre) or not np.isfinite(e_liq): continue
    kb = (np.searchsorted(qp, e_pre), np.searchsorted(ql, e_liq))
    names = pre_cs[ok].index[(bp == kb[0]) & (bl == kb[1])]; names = names[names != r.kod]
    o = {"i": r.Index, "kova_n": len(names), "kova_pre": kb[0], "kova_liq": kb[1]}
    for h in O.HZ:
        ev = F[h].at[t, r.kod] if r.kod in F[h].columns and pd.notna(F[h].at[t, r.kod]) else getattr(r, f"ar{h}")
        c = F[h].loc[t, names].mean(); o[f"ar{h}p"] = ev; o[f"kont{h}"] = c; o[f"k{h}"] = ev - c if np.isfinite(ev) and np.isfinite(c) else np.nan
    rows.append(o)
K = pd.DataFrame(rows).set_index("i"); R = R.join(K)
R.to_pickle(O.MY + "/A_sonuc_k.pkl")
out = [f"Kontrol-duzeltilmis AR (k = olay AR - ayni gun ayni [on-20g AR besli x likidite uclu] kovasinin ortalama AR'si). Tavan kilitli girisler ve 60g penceresinde |gunluk getiri|>%40 olan (olasi duzeltme hatasi) olaylar HARIC. Sicrama bayrakli olay: {int(R.sicrama.sum())}/{len(R)}\n"]
ozet = []
for ol in ["GA_YENI", "GA_PROG", "GA_ISLEM", "PAS_ALIS", "PAS_ALIS_KUME", "PAS_SATIS", "PAS_HEPSI"]:
    for vi in ["hepsi", "VIOP", "VIOP-disi"]:
        for dn in ["2018-26", "2024-26"]:
            d = R[(R.olay == ol) & (~R.tavan) & (~R.sicrama)]
            if vi == "VIOP": d = d[d.viop]
            elif vi == "VIOP-disi": d = d[~d.viop]
            if dn == "2024-26": d = d[d.t0 >= "2024-01-01"]
            row = {"olay": ol, "evren": vi, "donem": dn, "n": int(d.k20.notna().sum())}
            for h in O.HZ:
                s = O.ozet(d, f"k{h}"); row[f"k{h}%"] = s.get("ort%"); row[f"t{h}"] = s.get("t_kume"); row[f"med{h}%"] = s.get("medyan%"); row[f"isb{h}%"] = s.get("isabet%")
            s = O.ozet(d, "kont60"); row["kontrol60%"] = s.get("ort%")
            ozet.append(row)
T = pd.DataFrame(ozet).set_index(["olay", "evren", "donem"])
out.append(O.md(T.round(2)))
# yillik kirilim (hepsi)
for ol in ["GA_YENI", "GA_PROG", "PAS_ALIS"]:
    d = R[(R.olay == ol) & (~R.tavan)]
    y = d.groupby("yil").agg(n=("k20", "count"), k20=("k20", "mean"), med20=("k20", "median"), k60=("k60", "mean"), med60=("k60", "median")) * [1, 100, 100, 100, 100]
    out.append(f"\n{ol} yillik (k, %)\n\n" + O.md(y.round(2)))
open(O.OUTD + "/A_kontrol.md", "w").write("\n".join(out)); print("\n".join(out))
