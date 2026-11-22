"""Eleştirmen itirazlarının bağımsız sağlaması (ana ajan). ortak.py kullanılmaz.

Girdi: veri/sonuc/B1_islemler.csv (F1a_T_h1 işlemleri) ve veri/gunluk/*.csv.
Çıktı: veri/sonuc/ek_kontrol.md (VIX bantları, eşik duyarlılığı, dünkü VIX, tutma süresi,
en kötü günler, evren dışı stres hücresi, yıllık katkı).
"""
from pathlib import Path
import numpy as np
import pandas as pd

KOK = Path(__file__).resolve().parents[1]
G = KOK / "veri" / "gunluk"
T = ["SMH", "SOXX", "QQQ", "XLK", "SPY", "IWM"]
DIS = ["XLF", "XLE", "XLV", "XLI", "XLY", "XLP", "XLB", "DIA", "MDY"]
DONEM = [("2010-01-01", "2019-12-31"), ("2020-01-01", "2022-12-31"), ("2023-01-01", "2026-11-20")]


def oku(kod):
    d = pd.read_csv(G / f"{kod.replace('^', '_')}.csv", parse_dates=["Date"]).set_index("Date").sort_index()
    return d


def gunluk_t(df, sutun="alfa_bps"):
    """Aynı günün bütün işlemleri tek gözlem."""
    g = df.groupby("giris")[sutun].mean()
    if len(g) < 3:
        return np.nan, len(g)
    return g.mean() / (g.std(ddof=1) / np.sqrt(len(g))), len(g)


def donemler(tarihler, takvim, bosluk=10):
    """Sinyal günlerini, arada >= bosluk işlem günü olunca ayrı dönem sayarak etiketle."""
    sira = pd.Series(np.arange(len(takvim)), index=takvim)
    gun = sorted(pd.DatetimeIndex(tarihler).unique())
    et, no, onceki = {}, 0, None
    for g in gun:
        if onceki is not None and sira[g] - sira[onceki] >= bosluk:
            no += 1
        et[g] = no
        onceki = g
    return et


def ozet(df, ad, takvim):
    t, ng = gunluk_t(df)
    et = donemler(df["giris"], takvim)
    ep = df.assign(ep=df["giris"].map(et)).groupby("ep")["alfa_bps"].mean()
    return dict(kesit=ad, n=len(df), gun=ng, alfa=df["alfa_bps"].mean(), ham=df["ham_bps"].mean(),
                isabet=(df["ham_bps"] > 0).mean(), t_gunluk=t, donem=len(ep), arti_donem=int((ep > 0).sum()),
                en_kotu=df["ham_bps"].min())


def main():
    sat = []
    spy = oku("SPY")
    takvim = spy.index
    vix = oku("^VIX")["Close"].reindex(takvim)
    vix_dun = vix.shift(1)

    isl = pd.read_csv(KOK / "veri" / "sonuc" / "B1_islemler.csv", parse_dates=["giris", "cikis"])
    f = isl[isl["test_id"] == "F1a_T_h1"].copy()
    f["vix"] = f["giris"].map(vix)
    f["vix_dun"] = f["giris"].map(vix_dun)

    # 1) VIX bantları
    bant = [(0, 15), (15, 20), (20, 25), (25, 30), (30, 35), (35, 999)]
    r = [ozet(f[(f.vix >= a) & (f.vix < b)], f"VIX {a}-{b if b < 999 else '+'}", takvim) for a, b in bant]
    sat += ["## 1. F1a_T: VIX bantları (bps; t_gunluk = günde tek gözlem)", pd.DataFrame(r).round(2).to_markdown(index=False), ""]

    # 2) Eşik duyarlılığı ve dünkü VIX
    r = [ozet(f[f.vix >= e], f"VIX >= {e}", takvim) for e in (25, 30, 35)]
    r += [ozet(f[f.vix_dun >= e], f"dünkü VIX >= {e}", takvim) for e in (30, 35)]
    r += [ozet(f[(f.vix >= 30) & (f.giris >= "2023-01-01")], "VIX >= 30, 2023+", takvim)]
    r += [ozet(f[(f.vix >= 30) & ~((f.giris >= "2020-01-01") & (f.giris <= "2020-12-31"))], "VIX >= 30, 2020 hariç", takvim)]
    sat += ["## 2. Eşik duyarlılığı", pd.DataFrame(r).round(2).to_markdown(index=False), ""]

    # 3) Tutma süresi: aynı girişler, h1/h2 ham getiri; dönem bazında
    s = f[f.vix >= 30].copy()
    px = {k: oku(k)["AClose"] for k in T}
    def ileri(kod, gun, h):
        p = px[kod]
        i = p.index.get_loc(gun)
        return (p.iloc[i + h] / p.iloc[i] - 1) * 1e4 if i + h < len(p) else np.nan
    s["h1"] = [ileri(k, g, 1) for k, g in zip(s.kod, s.giris)]
    s["h2"] = [ileri(k, g, 2) for k, g in zip(s.kod, s.giris)]
    s["g2"] = s["h2"] - s["h1"]
    et = donemler(s["giris"], takvim)
    s["ep"] = s["giris"].map(et)
    ep = s.groupby("ep")[["h1", "h2", "g2"]].mean()
    gg = s.groupby("giris")["g2"].mean()
    sat += ["## 3. Stres (VIX >= 30): 1 gün ve 2 gün tutma (ham bps)",
            f"- işlem: {len(s)}, dönem: {len(ep)}; h1 ort {s.h1.mean():.1f}, h2 ort {s.h2.mean():.1f}; 2. günün katkısı ort {s.g2.mean():.1f}, medyan {s.g2.median():.1f}",
            f"- 2. gün katkısı günlük t: {gg.mean() / (gg.std(ddof=1) / np.sqrt(len(gg))):.2f} (gün {len(gg)})",
            f"- dönem bazında artı: h1 {int((ep.h1 > 0).sum())}/{len(ep)}, h2 {int((ep.h2 > 0).sum())}/{len(ep)}, 2. gün katkısı artı {int((ep.g2 > 0).sum())}/{len(ep)}",
            f"- işlem isabeti h1 {(s.h1 > 0).mean():.2f}, h2 {(s.h2 > 0).mean():.2f}; en kötü h1 {s.h1.min():.0f}, en kötü h2 {s.h2.min():.0f}",
            f"- sinyal çıkan yıl sayısı: {s.giris.dt.year.nunique()} / {f.giris.dt.year.nunique()}", ""]

    # 4) En kötü günler (2010'dan beri) ve stres işlemlerinin en kötüsü
    r = []
    for k in ["QQQ", "SMH", "TQQQ", "SOXL"]:
        p = oku(k)["AClose"]
        g1, g2 = p.pct_change(), p.pct_change(2)
        r.append(dict(kod=k, en_kotu_1g=g1.min() * 100, tarih_1g=g1.idxmin().date(), en_kotu_2g=g2.min() * 100,
                      tarih_2g=g2.idxmin().date(), sinir_2g_yuzde=3 / abs(g2.min() * 100) * 100))
    sat += ["## 4. En kötü 1 ve 2 günlük hareket (2010'dan beri, kapanıştan kapanışa, %); sınır = 3 / en kötü 2 gün",
            pd.DataFrame(r).round(2).to_markdown(index=False), ""]

    # 5) Kaldıraçlı araçlarda stres işlemleri (aracın kendi IBS'i, VIX >= 30; yalnız fiyat >= 3 ve 250 gün geçmiş)
    r = []
    for k in ["SMH", "QQQ", "SOXL", "TQQQ"]:
        d = oku(k)
        ibs = (d.AClose - d.ALow) / (d.AHigh - d.ALow)
        ok = (d.AHigh > d.ALow) & (np.arange(len(d)) >= 250)
        sin = ok & (ibs < 0.2) & (vix.reindex(d.index) >= 30)
        h1 = (d.AClose.shift(-1) / d.AClose - 1) * 1e4
        x = h1[sin].dropna()
        yil = (d.index[-1] - d.index[250]).days / 365.25
        r.append(dict(kod=k, n=len(x), yilda=len(x) / yil, ham_ort=x.mean(), medyan=x.median(), isabet=(x > 0).mean(),
                      en_kotu=x.min(), q10=x.quantile(0.10)))
    sat += ["## 5. Araç bazında stres işlemleri (kendi IBS < 0,2 ve VIX >= 30; ham bps, 1 gün)",
            pd.DataFrame(r).round(2).to_markdown(index=False), ""]
    yk = pd.DataFrame(r).set_index("kod")
    sat += ["Yıllık katkı (yılda işlem × ham ortalama × pozisyon oranı): " + "; ".join(
        f"{k} %{o}: {yk.loc[k, 'yilda'] * yk.loc[k, 'ham_ort'] / 1e4 * o:.2f} puan" for k, o in
        [("SMH", 19), ("QQQ", 23), ("SOXL", 6), ("TQQQ", 8), ("SOXL", 33)]), ""]

    # 6) Evren dışı 9 ABD ETF'i: stres hücresi (alfa = ham − araç × dönem günlük ortalaması)
    par = []
    for k in DIS:
        d = oku(k)
        ibs = (d.AClose - d.ALow) / (d.AHigh - d.ALow)
        h1 = (d.AClose.shift(-1) / d.AClose - 1) * 1e4
        ok = (d.AHigh > d.ALow) & (np.arange(len(d)) >= 250)
        x = pd.DataFrame(dict(kod=k, giris=d.index, ibs=ibs.values, ham_bps=h1.values, ok=ok.values))
        x["vix"] = x["giris"].map(vix)
        x["alfa_bps"] = np.nan
        for a, b in DONEM:
            m = (x.giris >= a) & (x.giris <= b)
            x.loc[m, "alfa_bps"] = x.loc[m, "ham_bps"] - x.loc[m, "ham_bps"].mean()
        par.append(x[x.ok & (x.ibs < 0.2)].dropna(subset=["ham_bps"]))
    dx = pd.concat(par)
    r = [ozet(dx[(dx.vix >= a) & (dx.vix < b)], f"evren dışı, VIX {a}-{b if b < 999 else '+'}", takvim)
         for a, b in [(0, 30), (30, 35), (35, 999), (30, 999)]]
    sat += ["## 6. Evren dışı 9 ABD ETF'i (XLF XLE XLV XLI XLY XLP XLB DIA MDY), IBS < 0,2", pd.DataFrame(r).round(2).to_markdown(index=False), ""]

    cikti = KOK / "veri" / "sonuc" / "ek_kontrol.md"
    cikti.write_text("\n".join(sat))
    print("\n".join(sat))


if __name__ == "__main__":
    main()
