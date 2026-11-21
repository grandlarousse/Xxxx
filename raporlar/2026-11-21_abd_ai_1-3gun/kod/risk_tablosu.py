"""Betimleyici risk tablosu (hipotez testi YOK).

Çıktılar: ek/risk_tablosu.csv, ek/korelasyon.csv, ek/kumeler.csv
Kullanım: python kod/risk_tablosu.py
Tanımlar (hepsi düzeltilmiş fiyatla; yüzdeler % cinsinden):
  vol_*: günlük basit getirinin standart sapması (%, yıllıklaştırılmamış).
  beta/R²: son 252 ABD işlem günü günlük getiri, OLS.
  sd_hg / q01_hg / q05_hg: 2023-01-01'den beri örtüşen h günlük kapanış->kapanış getirileri.
  gece: D-1 kapanış -> D açılış; gun_ici: D açılış -> D kapanış. Ortalama bps/gün (basit getiri),
        oynaklık payı = log getiri varyansları oranı var(gece)/(var(gece)+var(gun_ici)).
  atr14: son 14 günün ortalama gerçek aralığı / son kapanış (%).
  zirveden: son kapanış / son 252 gün en yüksek kapanış - 1.
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform

sys.path.insert(0, str(Path(__file__).parent))
import ortak as o
from indir import HEDEF, ETF

EK = o.KOK / "ek"
B23 = "2023-01-01"
TAKVIM = o.abd_takvimi()
SON = TAKVIM[-1]
BIR_YIL = TAKVIM[-252]


def satir(kod, rq, rs):
    d = o.yukle(kod)
    d = d[d.index.isin(TAKVIM)]
    c, op, hi, lo = d["AClose"], d["AOpen"], d["AHigh"], d["ALow"]
    r = c.pct_change()
    s = {"grup": "ETF" if kod in ETF else "hisse", "ilk_tarih": d.index[0].date(),
         "son_tarih": d.index[-1].date(), "son_kapanis": round(d["Close"].iloc[-1], 2),
         "son_gun_%": 100 * r.iloc[-1]}
    s["dolar_hacmi_60g_mn"] = (d["Close"] * d["Volume"]).iloc[-60:].median() / 1e6
    s["vol_60g"] = 100 * r.iloc[-60:].std()
    s["vol_1y"] = 100 * r.loc[BIR_YIL:].std()
    s["vol_2023"] = 100 * r.loc[B23:].std()
    s["yillik_vol_1y"] = s["vol_1y"] * np.sqrt(252)
    y = r.loc[BIR_YIL:]
    for ad, x in [("QQQ", rq), ("SMH", rs)]:
        j = pd.concat([y, x], axis=1).dropna()
        if len(j) > 60:
            cv = np.cov(j.iloc[:, 0], j.iloc[:, 1])
            s[f"beta_{ad}"] = cv[0, 1] / cv[1, 1]
            if ad == "SMH":
                s["R2_SMH"] = np.corrcoef(j.iloc[:, 0], j.iloc[:, 1])[0, 1] ** 2
    c23 = c.loc[B23:]
    s["n_2023"] = len(c23)
    for h in (1, 2, 3):
        rh = (c23.shift(-h) / c23 - 1).dropna()
        s[f"sd_{h}g"] = 100 * rh.std()
        s[f"q01_{h}g"] = 100 * rh.quantile(0.01)
        s[f"q05_{h}g"] = 100 * rh.quantile(0.05)
        if h == 1:
            s["q99_1g"] = 100 * rh.quantile(0.99)
    r23 = r.loc[B23:]
    s["en_kotu_gun_%"] = 100 * r23.min()
    s["en_kotu_tarih"] = r23.idxmin().date() if r23.notna().any() else None
    s["en_iyi_gun_%"] = 100 * r23.max()
    s["zirveden_%"] = 100 * (c.iloc[-1] / c.loc[BIR_YIL:].max() - 1)
    s["zirve_tarihi"] = c.loc[BIR_YIL:].idxmax().date()
    if c.index[0] <= pd.Timestamp("2025-12-31"):
        s["ytd_2026_%"] = 100 * (c.iloc[-1] / c.loc[:"2025-12-31"].iloc[-1] - 1)
    g = (op / c.shift(1) - 1).loc[B23:]
    gi = (c / op - 1).loc[B23:]
    s["gece_bps"] = 1e4 * g.mean()
    s["gun_ici_bps"] = 1e4 * gi.mean()
    lg, lgi = np.log1p(g).var(), np.log1p(gi).var()
    s["gece_vol_payi"] = lg / (lg + lgi)
    tr = pd.concat([hi - lo, (hi - c.shift(1)).abs(), (lo - c.shift(1)).abs()], axis=1).max(axis=1)
    s["atr14_%"] = 100 * tr.iloc[-14:].mean() / c.iloc[-1]
    if "yama" in d and d["yama"].fillna("").ne("").any():
        s["not"] = "son kapanış saatlik son bardan (bölünme günü Yahoo boşluğu)"
    return s


def main():
    kodlar = [k for k in HEDEF + ETF if (o.VERI / "gunluk" / f"{o.dosya_adi(k)}.csv").exists()]
    rq = o.yukle("QQQ")["AClose"].pct_change().loc[BIR_YIL:]
    rs = o.yukle("SMH")["AClose"].pct_change().loc[BIR_YIL:]
    tab = pd.DataFrame({k: satir(k, rq, rs) for k in kodlar}).T
    tab.index.name = "kod"

    # korelasyon + kümeleme (son 252 gün, en az 200 gözlem)
    R = o.panel("AClose", kodlar).pct_change().loc[BIR_YIL:]
    R = R.loc[:, R.notna().sum() >= 200]
    C = R.corr()
    C.round(3).to_csv(EK / "korelasyon.csv")
    D = np.sqrt(np.clip(0.5 * (1 - C.values), 0, None))
    np.fill_diagonal(D, 0)
    # Ward bağlantısı (ortalama bağlantı tek dev küme zinciri üretiyordu), 15 küme
    Z = linkage(squareform(D, checks=False), "ward")
    etiket = pd.Series(fcluster(Z, t=15, criterion="maxclust"), index=C.index, name="kume")
    # küme adı: kümenin en yüksek dolar hacimli üyesi
    hacim = tab["dolar_hacmi_60g_mn"].astype(float)
    ad = {kno: hacim.reindex(g.index).idxmax() for kno, g in etiket.groupby(etiket)}
    tab["kume"] = etiket.map(lambda x: f"{x}:{ad[x]}")
    kum = pd.DataFrame({"kume": etiket, "kume_adi": etiket.map(ad)}).sort_values(["kume", "kume_adi"])
    # küme içi ortalama korelasyon
    ic = {kno: C.loc[g.index, g.index].values[np.triu_indices(len(g), 1)].mean() if len(g) > 1 else np.nan
          for kno, g in etiket.groupby(etiket)}
    kum["kume_ici_ort_korelasyon"] = kum["kume"].map(ic).round(3)
    kum.to_csv(EK / "kumeler.csv")

    num = tab.columns.difference(["grup", "ilk_tarih", "son_tarih", "en_kotu_tarih", "zirve_tarihi", "kume", "not"])
    tab[num] = tab[num].apply(pd.to_numeric).round(3)
    tab.to_csv(EK / "risk_tablosu.csv")
    print(tab.shape, "son gün", SON.date())
    print(kum.groupby("kume").agg(ad=("kume_adi", "first"), n=("kume_adi", "size"),
                                  ic=("kume_ici_ort_korelasyon", "first"),
                                  uyeler=("kume_adi", lambda x: " ".join(x.index))).to_string())


if __name__ == "__main__":
    main()
