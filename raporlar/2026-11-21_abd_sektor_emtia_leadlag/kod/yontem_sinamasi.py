"""Yöntem sınaması (hesaplardan ÖNCE): kod/ortak.py ve YONTEM.md yanlış pozitif / yanlış negatif üretir mi?

Kullanım: python3 kod/yontem_sinamasi.py            (yaklaşık 2-4 dakika)
Çıktı   : ekrana özet tablo + ek/dogrulama/yontem_sinamasi.csv

İki bölüm:
  G* = gerçek veriyle denetimler (veri/ dizini)
  S* = sentetik dünyayla denetimler (geçici dizinde üretilir; ortak.VERI oraya çevrilir, sonra geri alınır)
Durum: GECTI / KALDI (kütüphane hatası ya da yöntem açığı) / BILGI (ölçüm).
"""
import os
import shutil
import sys
import tempfile

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak as o  # noqa: E402

GERCEK_VERI = o.VERI
RNG = np.random.default_rng(20261121)
SONUC = []


def kayit(kod, aciklama, deger, beklenen="", durum="BILGI"):
    SONUC.append(dict(kod=kod, aciklama=aciklama, deger=deger, beklenen=beklenen, durum=durum))
    print(f"[{durum:5s}] {kod:5s} {aciklama}: {deger}  (beklenen: {beklenen})", flush=True)


def veri_degistir(yol):
    o.VERI = yol
    for f in (o.meta, o.oku, o.takvim, o._panel):
        f.cache_clear()


def hac_t(Z, L, tur="bartlett"):
    """Sütun bazında HAC t. Z: (T, N), NaN yok."""
    n = Z.shape[0]
    m = Z.mean(0)
    E = Z - m
    v = (E * E).sum(0) / n
    for k in range(1, L + 1):
        w = 1 - k / (L + 1) if tur == "bartlett" else 1.0
        v = v + 2 * w * (E[k:] * E[:-k]).sum(0) / n
    return m / np.sqrt(np.maximum(v, 1e-300) / n)


def oz(t):
    t = np.asarray(t, dtype=float)
    t = t[~np.isnan(t)]
    return f"std={t.std():.2f} |t|>=2:{(np.abs(t) >= 2).mean() * 100:.1f}% t>=3:{(t >= 3).mean() * 100:.2f}%"


# =====================================================================================================================
# G: gerçek veri
# =====================================================================================================================


def gercek():
    tk = o.takvim()
    m = o.meta()
    # G1: takvim başlangıcından önceki getiriler ilk güne yığılıyor mu?
    kotu = []
    for s in ["^N225", "CL=F", "XLE", "^GDAXI", "EWZ"]:
        if s in m.index:
            h = o.hizali_getiri(s)
            kotu.append((s, round(float(h.iloc[0]), 3)))
    en = max(abs(v) for _, v in kotu)
    kayit("G1", "hizali_getiri ilk takvim günü (2005-01-03) değeri", kotu, "|deger| < 0,1", "GECTI" if en < 0.1 else "KALDI")
    z = o.zskor(o.hizali_getiri("^N225"))
    oran = float((z.iloc[41:101].abs() >= 1).mean())  # ilk 40 gün z tanımsız (min_n)
    kayit("G1b", "^N225 |z|>=1 sıklığı, takvimin 41.-100. günleri", round(oran, 3), "~0,3 (0 ise ilk gün aykırı değeri std'yi şişiriyor)", "GECTI" if oran > 0.15 else "KALDI")

    # G2: geç başlayan araçlarda IS dönemi (YONTEM 5: %55/%45 bölünme) kütüphanede var mı?
    sat = []
    for s in ["IBIT", "BITO", "XLC"]:
        if s in m.index:
            d = o.donemli_test(pd.Series(1.0, index=tk), s, 1)
            sat.append((s, d.get("is_n"), d.get("oos_n")))
    kayit("G2", "geç başlayan araçta donemli_test is_n / oos_n", sat, "is_n > 0 (YONTEM %55/%45 diyor)", "KALDI" if any(a[1] in (0, None) for a in sat) else "GECTI")

    # G3: oynaklık kümelenmesi tarama() t'sini ne kadar şişirir?  kappa = E[x^2 f^2] / (E[x^2] E[f^2])
    L = [s for s in ["XLE", "XLF", "XLK", "XLV", "XLI", "XLY", "XLP", "XLU", "XLB", "SPY", "QQQ", "IWM", "GLD", "TLT", "USO",
                     "SMH", "XBI", "KRE", "XOP", "GDX"] if s in m.index]
    X = pd.DataFrame({s: o.hizali_getiri(s) for s in L})
    F = o.ileri_getiri(L, 1)
    R = o.basit_getiri(L)
    sd = R.rolling(60, min_periods=40).std()
    Xz, Fz = X.apply(o.zskor), F / sd  # sd_t yalnız t'ye kadar veri kullanır; f_t ileri getiri
    kap, kapz = [], []
    for a in L:
        for b in L:
            if a == b:
                continue
            for (xx, ff, hedef) in ((X[a], F[b], kap), (Xz[a], Fz[b], kapz)):
                d = pd.concat([xx, ff], axis=1).dropna()
                x, f = d.iloc[:, 0] - d.iloc[:, 0].mean(), d.iloc[:, 1] - d.iloc[:, 1].mean()
                hedef.append(float((x**2 * f**2).mean() / ((x**2).mean() * (f**2).mean())))
    kayit("G3", "tarama() t şişmesi = sqrt(kappa), 20 ETF çifti, ham getiri (medyan; %10-%90)",
          f"{np.sqrt(np.median(kap)):.2f} ({np.sqrt(np.quantile(kap, .1)):.2f}-{np.sqrt(np.quantile(kap, .9)):.2f})", "1,0 olmalı", "KALDI" if np.median(kap) > 1.3 else "GECTI")
    kayit("G3b", "aynı ölçü, z-skorlu öncü ve oynaklığa bölünmüş ileri getiri", f"{np.sqrt(np.median(kapz)):.2f}", "~1,0")
    # G4: körlemesine tarama piyasanın kendi günlük dönüşünü defalarca 'keşfeder' mi?
    tar = o.tarama(X, L, h=1, bit=o.IS_BITIS)
    kayit("G4", "20 ETF x 19 çift, IS, ham tarama: t<=-2 oranı / t>=+2 oranı / medyan t",
          f"{(tar.t <= -2).mean() * 100:.0f}% / {(tar.t >= 2).mean() * 100:.0f}% / {tar.t.median():.2f}", "bağımsız sıfırda %2,3 / %2,3 / 0")
    spy = o.tarama(pd.DataFrame({"SPY_x": X["SPY"]}), ["SPY"], h=1, bit=o.IS_BITIS, min_n=100)
    spy2 = o.tarama(pd.DataFrame({"SPY_x": X["SPY"]}), ["SPY"], h=1, bas=o.OOS_BAS, min_n=100)
    kayit("G4b", "SPY'ın kendi 1 gün gecikmeli korelasyonu IS / OOS (tarama t'si)", f"{spy['corr'].iloc[0]:.3f} (t={spy.t.iloc[0]:.1f}) / {spy2['corr'].iloc[0]:.3f} (t={spy2.t.iloc[0]:.1f})", "bilgi")
    # piyasadan arındırılmış tarama: öncü ve hedef - beta*SPY
    b = {s: float(R[s].cov(R["SPY"]) / R["SPY"].var()) for s in L}
    Xr = pd.DataFrame({s: X[s] - b[s] * X["SPY"] for s in L if s != "SPY"})
    Fr = pd.DataFrame({s: Fz[s] * 0 + (F[s] - b[s] * F["SPY"]) for s in L if s != "SPY"})
    say = []
    for a in Xr.columns:
        for c in Fr.columns:
            if a == c:
                continue
            d = pd.concat([o.zskor(Xr[a]), Fr[c] / sd[c]], axis=1).dropna()
            d = d[d.index <= o.IS_BITIS]
            x, f = d.iloc[:, 0] - d.iloc[:, 0].mean(), d.iloc[:, 1] - d.iloc[:, 1].mean()
            say.append(float((x * f).sum() / np.sqrt((x**2 * f**2).sum())))
    say = np.array(say)
    kayit("G4c", "aynı tarama, SPY'dan arındırılmış + oynaklığa ölçekli + White t: t<=-2 / t>=+2 / medyan", f"{(say <= -2).mean() * 100:.0f}% / {(say >= 2).mean() * 100:.0f}% / {np.median(say):.2f}", "bilgi")

    # G5: HG=F'deki 0,31 bayat ETF mi, vadelide ileri bakış mı? Likit hedefle (FCX, COPX) ayrıştır.
    def bayat(onc, kar):
        f = o.hizali_getiri(onc, bilinen=False)
        c, op = o.panel("adjclose", [kar])[kar], o.panel("ao", [kar])[kar]
        r, gece = np.log(c).diff(), np.log(op / c.shift(1)).shift(-1)
        d = pd.DataFrame({"f": f, "r": r, "g": gece}).dropna()
        d = d[d.index >= "2012-01-01"]
        beta = d.r.cov(d.f) / d.f.var()
        return round(float((beta * d.f - d.r).corr(d.g)), 3)
    cift = [(a, c) for a, c in [("HG=F", "CPER"), ("HG=F", "FCX"), ("HG=F", "COPX"), ("CL=F", "XLE"), ("GC=F", "GDX"), ("^VIX", "SPY"), ("^VIX3M", "SPY"), ("^VVIX", "SPY"), ("VIXY", "SPY"), ("ES=F", "SPY"), ("^TNX", "TLT"), ("DX-Y.NYB", "UUP")]
            if a in m.index and c in m.index]
    kayit("G5", "corr(beta*öncü - hedef, hedefin ertesi gecesi)", [(a, c, bayat(a, c)) for a, c in cift], "likit hedefte ~0 ise vadelide ileri bakış yok")

    # G6: plasebo kaydırmaları takvim sinyallerinde aynı güne mi düşüyor?
    pzt = pd.Series((tk.dayofweek == 0).astype(float), index=tk)
    ay = pd.Series(tk.year * 12 + tk.month, index=tk)
    ilk3 = (ay.groupby(ay).cumcount() < 3).astype(float)
    kayit("G6", "plasebo kaydırması sonrası aynı takvim gününe düşme oranı (5/10/20/40): pazartesi | ayın ilk 3 günü",
          f"{[round(float(pzt.shift(k)[pzt == 1].mean()), 2) for k in (5, 10, 20, 40)]} | {[round(float(ilk3.shift(k)[ilk3 == 1].mean()), 2) for k in (5, 10, 20, 40)]}",
          "~0,2 ve ~0,14 olmalı (bağımsız plasebo)", "KALDI")

    # G7: Yahoo açılış fiyatı kalitesi (I koşulu ve gece/gün içi ayrışması buna dayanıyor)
    c, op, v = o.panel("close"), o.panel("open"), o.panel("volume")
    us = [s for s in o.abd_semboller(["ETF", "EQUITY"]) if s in c.columns]
    esit = ((op[us] == c[us].shift(1)) & c[us].notna())[c.index >= "2015-01-01"].sum() / c[us][c.index >= "2015-01-01"].notna().sum()
    kayit("G7", "açılış == önceki kapanış günlerinin payı > %5 olan ABD sembolü sayısı / toplam (2015+); en kötü 5", f"{int((esit > 0.05).sum())}/{len(us)}; {esit.sort_values(ascending=False).head(5).round(2).to_dict()}", "0")
    # G8: maliyet sınıfı bugünkü hacimden: geçmişte daha pahalı sınıfta olanlar
    dv = (c[us] * v[us]).rolling(20, min_periods=10).mean() / 1e6

    def sinif(x):
        return np.where(x >= 100, 5, np.where(x >= 20, 10, 20))
    bugun = dv.iloc[-1]
    for tarih in ("2012-06-29", "2019-06-28"):
        eski = dv.loc[:tarih].iloc[-1]
        ok = bugun.notna() & eski.notna()
        daha_pahali = (sinif(eski[ok]) > sinif(bugun[ok])).mean()
        kayit("G8", f"{tarih} tarihinde bugünkünden pahalı maliyet sınıfında olan sembol payı (n={int(ok.sum())})", f"{daha_pahali * 100:.0f}%", "0% (aksi halde geçmiş maliyet düşük sayılır)")
    # G5b: VIX ailesi: 16:15 kapanışı ileri bakış mı? SPY'ın ertesi gecesi ~ SPY_t + VIXY_t (16:00) + ^VIX_t (16:15)
    import statsmodels.api as sm
    C_, O_ = o.panel("adjclose"), o.panel("ao")
    r_all = np.log(C_).diff()
    gece_s = np.log(O_ / C_.shift(1)).shift(-1)
    if "^VIX" in m.index and "VIXY" in m.index:
        d = pd.DataFrame({"y": gece_s["SPY"], "spy": r_all["SPY"], "vixy": r_all["VIXY"], "vix": o.hizali_getiri("^VIX", bilinen=False)}).dropna()
        d = d[d.index >= "2012-01-01"]
        f1 = sm.OLS(d.y, sm.add_constant(d[["spy", "vixy", "vix"]])).fit(cov_type="HC0")
        f0 = sm.OLS(d.y, sm.add_constant(d[["spy"]])).fit(cov_type="HC0")
        kayit("G5b", "SPY ertesi gece ~ SPY_t [+ VIXY_t + ^VIX_t]: White t (yalnız SPY | SPY, VIXY, ^VIX)", f"{f0.tvalues['spy']:.1f} | {f1.tvalues['spy']:.1f}, {f1.tvalues['vixy']:.1f}, {f1.tvalues['vix']:.1f}",
              "^VIX, VIXY'ye ek olarak anlamlıysa 16:15 ileri bakışı var")
    # G10: bayat kapanış taraması: hedef ETF'in ertesi gecesi ~ kendi getirisi_t + en yakın likit karşılığın getirisi_t
    etf = [s for s in o.abd_semboller("ETF") if s in C_.columns]
    likit = [s for s in ["SPY", "QQQ", "IWM", "DIA", "XLE", "XLF", "XLK", "XLV", "XLI", "XLY", "XLP", "XLU", "XLB", "GLD", "SLV", "USO", "TLT", "IEF", "HYG",
                         "LQD", "EEM", "EFA", "FXI", "EWJ", "EWZ", "SMH", "XBI", "GDX", "KRE", "XOP", "UNG"] if s in C_.columns]
    vadeli = [s for s in m.index if m.loc[s, "tur"] == "FUTURE"]
    REF = pd.concat([r_all[likit], pd.DataFrame({s: o.hizali_getiri(s, bilinen=False) for s in vadeli})], axis=1)
    REF = REF[REF.index >= "2015-01-01"]
    sat = []
    for s in etf:
        r = r_all[s].reindex(REF.index)
        if r.notna().sum() < 500:
            continue
        cc = REF.drop(columns=[s], errors="ignore").corrwith(r)
        ref = cc.idxmax()
        if cc[ref] < 0.4:
            continue
        d = pd.DataFrame({"y": gece_s[s], "r": r, "x": REF[ref]}).dropna()
        if len(d) < 500:
            continue
        f = sm.OLS(d.y, sm.add_constant(d[["r", "x"]])).fit(cov_type="HC0")
        sat.append((s, ref, round(float(cc[ref]), 2), round(float(f.tvalues["x"]), 1), round(float(f.params["x"] * d.x.std() / d.y.std()), 2), round(float(dv[s].iloc[-1]), 1) if s in dv.columns else np.nan))
    bt = pd.DataFrame(sat, columns=["etf", "karsilik", "corr", "t_x", "etki", "hacim_mn"]).sort_values("t_x", ascending=False)
    supheli = bt[(bt.t_x >= 4) & (bt.etki >= 0.1)]
    bt.to_csv(os.path.join(o.KOK, "ek", "dogrulama", "bayat_kapanis_taramasi.csv"), index=False)
    kayit("G10", f"bayat kapanış şüphesi (t>=4 ve standart etki>=0,1) olan ETF sayısı / taranan; ilk 15 (etf, karşılık, t, etki, hacim mn$)",
          f"{len(supheli)}/{len(bt)}; {[tuple(x) for x in supheli[['etf', 'karsilik', 't_x', 'etki', 'hacim_mn']].head(15).values.tolist()]}", "YONTEM yalnız CPER, CANE, WEAT diyor")
    kayit("G10b", "karşılaştırma: en likit 8 ETF'te aynı ölçü (t_x)", bt[bt.etf.isin(["SPY", "QQQ", "IWM", "XLE", "XLF", "GLD", "TLT", "SMH"])][["etf", "karsilik", "t_x", "etki"]].values.tolist(), "|t| < 3")
    # G12: gecikme() tablosunun ampirik denetimi: ETF/hisse olmayan öncülerin t çubuğu, likit karşılığının ERTESİ GECESİNİ öngörüyor mu?
    aday = likit + [s for s in ["UUP", "FXE", "FXY", "VIXY", "IBIT", "BITO", "EWC", "EWW"] if s in C_.columns and s not in likit]
    RA = r_all[aday][r_all.index >= "2012-01-01"]
    onculer = [s for s in m.index if m.loc[s, "tur"] in ("FUTURE", "INDEX", "ALTSYMBOL", "CRYPTOCURRENCY", "CURRENCY")
               and str(m.loc[s, "saat_dilimi"]).startswith(("America", "UTC", "Europe/London"))]
    sat = []
    for s in onculer:
        x = o.hizali_getiri(s, bilinen=False).reindex(RA.index)
        cc = RA.corrwith(x)
        ref = cc.abs().idxmax()
        if abs(cc[ref]) < 0.3:
            continue
        d = pd.DataFrame({"y": gece_s[ref], "r": r_all[ref], "x": x}).dropna()
        if len(d) < 300:
            continue
        f = sm.OLS(d.y, sm.add_constant(d[["r", "x"]])).fit(cov_type="HC0")
        sat.append((s, ref, round(float(cc[ref]), 2), round(float(f.tvalues["x"] * np.sign(cc[ref])), 1), o.gecikme(s)))
    lt = pd.DataFrame(sat, columns=["oncu", "karsilik", "corr", "t_ileri", "gecikme"]).sort_values("t_ileri", ascending=False)
    lt.to_csv(os.path.join(o.KOK, "ek", "dogrulama", "ileri_bakis_taramasi.csv"), index=False)
    acik = lt[(lt.t_ileri >= 4) & (lt.gecikme == 0)]
    kayit("G12", f"ileri bakış izi (t>=4) olup gecikme()=0 olan öncü sayısı / taranan {len(lt)}; liste (öncü, karşılık, t)", f"{len(acik)}; {acik[['oncu', 'karsilik', 't_ileri']].values.tolist()}",
          "0", "KALDI" if len(acik) else "GECTI")
    kayit("G12b", "gecikme()=1 olan öncülerde aynı ölçü (gecikmesiz kullanılsaydı)", lt[lt.gecikme == 1][["oncu", "karsilik", "t_ileri"]].values.tolist(), "t >> 4 (gecikme gerekli)")
    # G11: aşırı günlük getiriler (YONTEM 2: ETF > %40, hisse > %80)
    Rb = o.basit_getiri(us)
    e_ = [s for s in us if m.loc[s, "tur"] == "ETF"]
    h_ = [s for s in us if m.loc[s, "tur"] == "EQUITY"]
    ae, ah = (Rb[e_].abs() > 0.4).sum(), (Rb[h_].abs() > 0.8).sum()
    kayit("G11", "aşırı getiri günleri: ETF |r|>%40 (gün; sembol) | hisse |r|>%80 (gün; sembol)", f"{int(ae.sum())}; {ae[ae > 0].sort_values(ascending=False).head(8).to_dict()} | {int(ah.sum())}; {ah[ah > 0].sort_values(ascending=False).head(8).to_dict()}", "bilgi")
    # G9: çoklu test: sıfır hipotezinde A ve B koşullarını birlikte geçme olasılığı
    w = 14.0 / (14.0 + 7.9)
    g = np.random.default_rng(1)
    a, bb = g.standard_normal(20_000_000), g.standard_normal(20_000_000)
    tum = np.sqrt(w) * a + np.sqrt(1 - w) * bb
    for ad, sis in (("düzgün t", 1.0), ("t %17 şişik (h=3, kalıcı sinyal)", 1.17)):
        p_sag = ((tum >= 3.0 / sis) & (bb >= 2.0 / sis) & (a > 0)).mean()
        p_kos = ((tum >= 2.5 / sis) & (bb >= 1.5 / sis) & (a > 0)).mean()
        kayit("G9", f"sıfırda A∧B geçme olasılığı ({ad}): SAĞLAM / KOŞULLU -> 100 bin testte beklenen yanlış pozitif", f"{p_sag:.2e} / {p_kos:.2e} -> {p_sag * 1e5:.0f} / {p_kos * 1e5:.0f}", "aile test sayısına göre << 1 olmalı")
    p2 = ((a >= 2.5) & (bb >= 2.5)).mean()
    kayit("G9b", "öneri: IS t>=2,5 ile seç, OOS t>=2,5 ile doğrula -> 100 bin testte beklenen yanlış pozitif", f"{p2 * 1e5:.1f}", "bilgi")


# =====================================================================================================================
# S: sentetik dünya
# =====================================================================================================================


def sentetik_kur(n_nul=600, n_sv=40):
    kok = tempfile.mkdtemp(prefix="yontem_sinamasi_")
    os.makedirs(os.path.join(kok, "ham"))
    gunler = pd.bdate_range("2000-01-03", "2026-11-20")

    def tatil(d):
        return (d.month == 1 and d.day == 1) or (d.month == 7 and d.day == 4) or (d.month == 12 and d.day == 25) or (
            d.month == 11 and d.weekday() == 3 and 22 <= d.day <= 28)
    nyse = pd.DatetimeIndex([d for d in gunler if not tatil(d)])
    T = len(nyse)
    metalar = []

    def yaz(sembol, idx, logp, tur="ETF", tz="America/New_York"):
        c = np.exp(logp)
        r = np.diff(logp, prepend=logp[0])
        op = np.exp(logp - 0.6 * r)  # getirinin %40'ı gece, %60'ı gün içi
        d = pd.DataFrame({"date": idx.strftime("%Y-%m-%d"), "open": op, "high": np.maximum(op, c) * 1.001, "low": np.minimum(op, c) * 0.999,
                          "close": c, "adjclose": c, "volume": 1e6, "dividend": "", "split": ""})
        d.to_csv(os.path.join(kok, "ham", o.dosya_adi(sembol) + ".csv"), index=False)
        metalar.append(dict(sembol=sembol, dosya=sembol + ".csv", tur=tur, borsa="X", borsa_tam="X", saat_dilimi=tz, gmtoffset=0, para="USD",
                            ad=sembol, ilk=str(idx[0].date()), son=str(idx[-1].date()), n=len(idx), gruplar=""))
        return pd.Series(c, index=idx), pd.Series(op, index=idx)

    kap, ac = {}, {}
    mkt = RNG.normal(0.0003, 0.010, T)
    x = RNG.normal(0.0, 0.012, T)
    tgt = 0.5 * x + 0.15 * np.concatenate([[0], x[:-1]]) + RNG.normal(0, 0.010, T)  # öncü 1 gün önde
    u = np.zeros(T)
    e = RNG.normal(0, 0.012, T)
    for t in range(1, T):
        u[t] = -0.2 * u[t - 1] + e[t]  # öncüden bağımsız artık dönüşü
    seriler = {"SPY": mkt, "LEAD": x, "TGT": tgt, "LDA": mkt + RNG.normal(0, 0.006, T), "RSD": mkt + u}
    for s, r in seriler.items():
        kap[s], ac[s] = yaz(s, nyse, np.log(100) + np.cumsum(r))
    # Asya endeksi: kendi tatilleri var, ABD tatilinde açık
    asya_gun = gunler[RNG.random(len(gunler)) > 0.04]
    yaz("ASYA", asya_gun, np.log(100) + np.cumsum(RNG.normal(0, 0.012, len(asya_gun))), tur="INDEX", tz="Asia/Tokyo")
    # Kripto: saatlik süreç. Günlük çubuk d = 00:00 UTC d -> 24:00 UTC d. ABD kapanışı 21:00 UTC.
    t0 = pd.Timestamp("2009-12-31")
    nh = (pd.Timestamp("2026-11-23") - t0).days * 24
    Lh = np.concatenate([[0.0], np.cumsum(RNG.normal(0, 0.03 / np.sqrt(24), nh))])
    kgun = pd.date_range("2010-01-01", "2026-11-20")
    yaz("KRP", kgun, Lh[((kgun - t0).days + 1) * 24], tur="CRYPTOCURRENCY", tz="UTC")
    kn = nyse[nyse >= "2010-01-04"]
    kap["KTGT"], ac["KTGT"] = yaz("KTGT", kn, Lh[(kn - t0).days * 24 + 21])
    # Sıfır hipotezi hedefleri: GARCH(1,1) + t5 kuyruk, 4 bps/gün sürüklenme
    eps = RNG.standard_t(5, size=(T, n_nul)) / np.sqrt(5 / 3)
    hh = np.ones(n_nul)
    rr = np.empty((T, n_nul))
    for t in range(T):
        rr[t] = np.sqrt(hh) * eps[t]
        hh = 0.05 + 0.10 * rr[t] ** 2 + 0.85 * hh
    nul = 0.0004 + 0.012 * rr
    # Ortak stokastik oynaklık dünyası (öncüler ve hedefler bağımsız, oynaklık rejimi ortak)
    lv = np.zeros(T)
    eta = RNG.normal(0, 0.09, T)
    for t in range(1, T):
        lv[t] = 0.98 * lv[t - 1] + eta[t]
    sig = np.exp(lv)[:, None]
    svl, svt = 0.01 * sig * RNG.standard_normal((T, n_sv)), 0.01 * sig * RNG.standard_normal((T, n_sv + 20))
    genis = {}
    for ad, mat in (("NUL", nul), ("SVL", svl), ("SVT", svt)):
        for j in range(mat.shape[1]):
            s = f"{ad}{j:03d}"
            genis[s] = np.exp(np.log(100) + np.cumsum(mat[:, j]))
            metalar.append(dict(sembol=s, dosya=s + ".csv", tur="ETF", borsa="X", borsa_tam="X", saat_dilimi="America/New_York", gmtoffset=0,
                                para="USD", ad=s, ilk="2000-01-03", son="2026-11-20", n=T, gruplar=""))
    G = pd.DataFrame(genis, index=nyse)
    pd.DataFrame(metalar).to_csv(os.path.join(kok, "meta.csv"), index=False)
    tk = nyse[nyse >= o.ALT_SINIR_TARIH]
    C = pd.concat([pd.DataFrame(kap).reindex(nyse), G], axis=1).reindex(tk)
    Gr = np.log(G).diff()
    O = pd.concat([pd.DataFrame(ac).reindex(nyse), np.exp(np.log(G) - 0.6 * Gr)], axis=1).reindex(tk)
    C.to_parquet(os.path.join(kok, "panel_adjclose.parquet"))
    O.to_parquet(os.path.join(kok, "panel_ao.parquet"))
    return kok, nyse, dict(Lh=Lh, t0=t0, n_nul=n_nul, n_sv=n_sv)


def sentetik():
    kok, nyse, ek = sentetik_kur()
    veri_degistir(kok)
    try:
        _sentetik(nyse, ek)
    finally:
        veri_degistir(GERCEK_VERI)
        shutil.rmtree(kok, ignore_errors=True)


def _sentetik(nyse, ek):
    tk = o.takvim()

    # ---- S1: hizali_getiri = her NYSE gününde bilinen son kapanışın farkı mı?
    def beklenen(sembol):
        lp = np.log(o.oku(sembol)["adjclose"])
        son = lp.reindex(lp.index.union(nyse)).ffill().reindex(nyse)
        return son.diff().reindex(tk)
    for s in ("ASYA", "KRP", "LEAD"):
        a, b = o.hizali_getiri(s, bilinen=False), beklenen(s)
        ilk_fark = abs(float(a.iloc[0]) - float(b.iloc[0])) if not np.isnan(b.iloc[0]) else 0.0
        fark = float((a - b).iloc[1:][a.index[1:] >= b.first_valid_index() + pd.Timedelta(days=7)].abs().max())
        bas_ = b.first_valid_index() + pd.Timedelta(days=7)  # serinin ilk haftası: tanım farkı (ilk gözlem tatile denk gelirse)
        nan_ayni = bool((a.isna() == b.isna())[a.index >= bas_].all())
        kayit("S1", f"hizali_getiri({s}) beklenenle en büyük fark: ilk gün / diğer günler / NaN deseni aynı", f"{ilk_fark:.4f} / {fark:.1e} / {nan_ayni}",
              "0 / 0 / True", "GECTI" if ilk_fark < 1e-9 and fark < 1e-9 and nan_ayni else "KALDI")
    # ---- S1b: kripto: ileri bakış ve bayatlık
    Lh, t0 = ek["Lh"], ek["t0"]
    g = tk[(tk >= "2010-03-01") & (tk <= "2026-11-13")]
    i21 = (g - t0).days * 24 + 21
    sonra3 = pd.Series(Lh[i21 + 3] - Lh[i21], index=g)       # kapanıştan sonraki 3 saat (bilinemez)
    son24 = pd.Series(Lh[i21] - Lh[i21 - 24], index=g)       # kapanıştan önceki 24 saat (bilinir)
    a, b = o.hizali_getiri("KRP", True), o.hizali_getiri("KRP", False)
    r = o.log_getiri("KRP")
    pos = nyse.searchsorted(r.index, side="right")
    ok = pos < len(nyse)
    alt = pd.Series(r.values[ok], index=nyse[pos[ok]]).groupby(level=0).sum().reindex(tk)  # öneri: çubuk d -> d'den SONRAKİ ilk NYSE günü
    c1, c2, c3 = float(b.corr(sonra3)), float(a.corr(sonra3)), float(alt.corr(sonra3))
    kayit("S1b", "kripto sinyali ile kapanış sonrası 3 saatin korelasyonu: gecikmesiz / kütüphane (gecikme=1) / öneri (sağdan eşleme)", f"{c1:.3f} / {c2:.3f} / {c3:.3f}",
          ">0,2 (ileri bakış) / ~0 / ~0", "GECTI" if abs(c2) < 0.03 and c1 > 0.2 else "KALDI")
    pzt, sali = g[g.dayofweek == 0], g[g.dayofweek == 1]
    hs = pd.Series(Lh[(pzt - t0).days * 24] - Lh[(pzt - t0).days * 24 - 48], index=pzt)  # cumartesi + pazar çubukları
    hs_sali = pd.Series(hs.values, index=[tk[tk.get_loc(d) + 1] for d in pzt])
    kayit("S1c", "hafta sonu kripto hareketi hangi günün sinyalinde? corr: kütüphane pazartesi / kütüphane salı / öneri pazartesi",
          f"{float(a.reindex(pzt).corr(hs)):.2f} / {float(a.reindex(hs_sali.index).corr(hs_sali)):.2f} / {float(alt.reindex(pzt).corr(hs)):.2f}", "pazartesi yüksek olmalı (bilgi pazartesi 16:00'da biliniyor)",
          "KALDI" if float(a.reindex(pzt).corr(hs)) < 0.3 else "GECTI")
    kayit("S1d", "kripto sinyalinin son 24 saatle korelasyonu: kütüphane / öneri", f"{float(a.corr(son24)):.2f} / {float(alt.corr(son24)):.2f}", "bilgi (ikisi de bayat; birincil öncü IBIT/BITO)")

    # ---- S2: zskor ve kayan_beta geleceği kullanıyor mu? (geleceği boz, geçmiş değişmemeli)
    x, y = o.hizali_getiri("LEAD"), o.hizali_getiri("TGT")
    Tn = 3000
    x2, y2 = x.copy(), y.copy()
    x2.iloc[Tn + 1:] = 9.9
    d1 = float((o.zskor(x2) - o.zskor(x)).iloc[: Tn + 1].abs().max())
    x3, y3 = x.copy(), y.copy()
    x3.iloc[Tn:], y3.iloc[Tn:] = 9.9, -9.9
    d2 = float((o.kayan_beta(y3, x3) - o.kayan_beta(y, x)).iloc[: Tn + 1].abs().max())
    kayit("S2", "gelecek bozulunca zskor(<=T) / kayan_beta(<=T) değişimi", f"{d1:.1e} / {d2:.1e}", "0 / 0", "GECTI" if d1 == 0 and d2 == 0 else "KALDI")

    # ---- S3: ileri_getiri kaydırmaları
    d = o.oku("TGT")
    c, op = d["adjclose"].reindex(tk).values, d["ao"].reindex(tk).values
    hata = 0.0
    for h in (1, 2, 3):
        n = len(c)
        bek = {"kapanis": c[h:] / c[:-h] - 1, "acilis": c[h:][: n - h] / op[1:][: n - h] - 1 if h == 1 else c[h:] / op[1: n - h + 1] - 1,
               "ertesi": c[h + 1:] / c[1: n - h] - 1, "gece": op[1:] / c[:-1] - 1}
        for gir, b_ in bek.items():
            a_ = o.ileri_getiri(["TGT"], h, gir)["TGT"].values
            hata = max(hata, float(np.nanmax(np.abs(a_[: len(b_)] - b_))), float(np.sum(~np.isnan(a_[len(b_):]))))
    kayit("S3", "ileri_getiri dört giriş türü x h=1,2,3: elle hesapla en büyük fark", f"{hata:.1e}", "0", "GECTI" if hata < 1e-12 else "KALDI")

    # ---- S4: bilinen 1 günlük öncülük doğru gecikmede bulunuyor mu?
    z = o.zskor(x)
    sin = np.sign(z).where(z.abs() >= 1, 0.0)
    dogru = o.islem_testi(sin, "TGT", 1, 0)
    ters = o.islem_testi(np.sign(o.zskor(y)).where(o.zskor(y).abs() >= 1, 0.0), "LEAD", 1, 0)
    gec = o.islem_testi(sin.shift(1), "TGT", 1, 0)
    sizinti = o.islem_testi(sin.shift(-1), "TGT", 1, 0)
    ert = o.islem_testi(sin, "TGT", 1, 0, giris="ertesi")
    acl = o.islem_testi(sin, "TGT", 1, 0, giris="acilis")
    kayit("S4", "LEAD->TGT B1 (bps; t): doğru gecikme | ters yön | 1 gün geç | ertesi kapanış girişi | ertesi açılış girişi | KASITLI sızıntı (sinyal 1 gün erken)",
          f"{dogru['anormal_net_bps']};{dogru['t_anormal']} | {ters['anormal_net_bps']};{ters['t_anormal']} | {gec['anormal_net_bps']};{gec['t_anormal']} | "
          f"{ert['anormal_net_bps']};{ert['t_anormal']} | {acl['anormal_net_bps']};{acl['t_anormal']} | {sizinti['anormal_net_bps']};{sizinti['t_anormal']}",
          "~27 bps; t>>3 | ~0 | ~0 | ~0 | ~%60'ı | çok büyük",
          "GECTI" if dogru["t_anormal"] > 8 and abs(ters["t_anormal"]) < 3 and abs(gec["t_anormal"]) < 3 and abs(ert["t_anormal"]) < 3 else "KALDI")
    tar = o.tarama(pd.DataFrame({"LEAD": x, "TGT": y}), ["LEAD", "TGT"], h=1).set_index(["oncu", "hedef"])
    kayit("S4b", "tarama: LEAD->TGT t / TGT->LEAD t", f"{tar.loc[('LEAD', 'TGT'), 't']:.1f} / {tar.loc[('TGT', 'LEAD'), 't']:.1f}", ">>3 / ~0",
          "GECTI" if tar.loc[("LEAD", "TGT"), "t"] > 8 and abs(tar.loc[("TGT", "LEAD"), "t"]) < 3 else "KALDI")
    kayit("S4c", "plasebo (5/10/20/40) LEAD->TGT", o.plasebo(sin, "TGT", 1), "|t| < 2")

    # ---- S5: sıfır hipotezinde islem_testi t'sinin dağılımı (GARCH + kalın kuyruk; hedefler bağımsız)
    nul = [f"NUL{j:03d}" for j in range(ek["n_nul"])]
    R = o.basit_getiri(nul)
    zN = np.log1p(R).apply(o.zskor)
    ay = pd.Series(tk.year * 12 + tk.month, index=tk)
    blok = (ay.groupby(ay).cumcount() < 4).astype(float)               # ay dönümü benzeri: 4 gün üst üste
    z3 = o.zskor(x.rolling(3).sum())
    b3 = np.sign(z3).where(z3.abs() >= 1, 0.0)                         # B3: 3 günlük toplam (kalıcı sinyal)
    dip = (zN <= -1).astype(float)                                     # seyrek, oynaklıkla kümelenen
    for h in (1, 2, 3):
        F = o.ileri_getiri(nul, h)
        gec_ = F.notna().all(axis=1).values
        Fv = F.values[gec_]
        Rv = np.nan_to_num(R.values)
        for ad, S in (("dip z<=-1", dip.values), ("ay dönümü bloğu", np.repeat(blok.values[:, None], len(nul), 1)), ("B3 3 günlük", np.repeat(b3.fillna(0).values[:, None], len(nul), 1))):
            Sv = S[gec_]
            Z = Sv * (Fv - Fv.mean(0))
            t_kut = hac_t(Z, h - 1)
            if h == 3 and ad == "dip z<=-1":  # vektörel hesap kütüphaneyle aynı mı?
                k = [o.islem_testi(dip[s], s, h, 0)["t_anormal"] for s in nul[:40]]
                kayit("S5a", "vektörel HAC ile islem_testi t_anormal farkı (40 hedef)", f"{np.abs(np.array(k) - t_kut[:40]).max():.3f}", "<0,01 (yuvarlama)",
                      "GECTI" if np.abs(np.array(k) - t_kut[:40]).max() < 0.011 else "KALDI")
            poz = sum(np.roll(S, k, axis=0) for k in range(h)) / h
            poz[:h] = 0
            pnl = np.roll(poz, 1, axis=0)[1:] * (Rv[1:] - Rv[1:].mean(0))
            sat = f"kütüphane NW(h-1): {oz(t_kut)}"
            if h > 1:
                sat += f" || Bartlett 2(h-1): std={hac_t(Z, 2 * (h - 1)).std():.2f} || düz ağırlık (Hansen-Hodrick): std={hac_t(Z, h - 1, 'duz').std():.2f} || günlük PnL t: std={hac_t(pnl, 0).std():.2f}"
            kayit("S5", f"sıfırda t dağılımı, h={h}, {ad}", sat, "std=1,00; |t|>=2: %4,6; t>=3: %0,13", "KALDI" if t_kut.std() > 1.08 else "GECTI")
    # ---- S5b: sürüklenme düzeltmesi AL / SAT simetrisi ve maliyet
    al, sat_, hams, hama = [], [], [], []
    for s in nul[:150]:
        rs = pd.Series(RNG.choice([-1.0, 0.0, 1.0], size=len(tk), p=[0.15, 0.7, 0.15]), index=tk)
        r_ = o.islem_testi(rs, s, 3, 5)
        al.append(r_["anormal_bps_al"]); sat_.append(r_["anormal_bps_sat"]); hams.append(r_["net_bps_sat"]); hama.append(r_["net_bps_al"])
    kayit("S5b", "rastgele sinyal, h=3, maliyet 5 bps, hedef sürüklenmesi ~4 bps/gün: anormal AL / anormal SAT / ham net AL / ham net SAT (bps)",
          f"{np.mean(al):.1f} / {np.mean(sat_):.1f} / {np.mean(hama):.1f} / {np.mean(hams):.1f}", "-5 / -5 / ~+9 / ~-19: düzeltme simetrik; SAT'ta anormal, cebe girenden ~14 bps fazla gösterir",
          "GECTI" if abs(np.mean(al) + 5) < 1.5 and abs(np.mean(sat_) + 5) < 1.5 else "KALDI")

    # ---- S6: tarama() yaklaşık t'si
    svl, svt = [f"SVL{j:03d}" for j in range(ek["n_sv"])], [f"SVT{j:03d}" for j in range(ek["n_sv"] + 20)]
    Xs = np.log(o.panel("adjclose", svl)).diff()
    for h in (1, 2, 3):
        t_ = o.tarama(Xs, svt, h=h).t.values
        kayit("S6", f"tarama t, ortak oynaklık rejimi, bağımsız seriler, h={h}", oz(t_), "std=1,00", "KALDI" if abs(t_.std() - 1) > 0.1 else "GECTI")
    Xi = pd.DataFrame(RNG.normal(0, 0.01, (len(tk), 30)), index=tk, columns=[f"I{j}" for j in range(30)])
    for h in (1, 3):
        t_ = o.tarama(Xi, nul[:60], h=h).t.values
        kayit("S6b", f"tarama t, iid öncü x GARCH hedef (oynaklık ortak değil), h={h}", oz(t_), "std=1,00 (h>1'de n/h düzeltmesi fazla tutucu: ~1/sqrt(h))", "KALDI" if abs(t_.std() - 1) > 0.1 else "GECTI")
    Fs = o.ileri_getiri(svt, 1)
    sdv = o.basit_getiri(svt).rolling(60, min_periods=40).std()
    tw = []
    Xz = Xs.apply(o.zskor)
    for a_ in svl[:20]:
        for b_ in svt[:30]:
            d_ = pd.concat([Xz[a_], Fs[b_] / sdv[b_]], axis=1).dropna()
            xx, ff = d_.iloc[:, 0] - d_.iloc[:, 0].mean(), d_.iloc[:, 1] - d_.iloc[:, 1].mean()
            tw.append(float((xx * ff).sum() / np.sqrt((xx**2 * ff**2).sum())))
    kayit("S6c", "öneri: z-skorlu öncü, oynaklığa bölünmüş ileri getiri, White t (h=1)", oz(tw), "std=1,00", "GECTI" if abs(np.std(tw) - 1) < 0.1 else "KALDI")

    # ---- S7: B2 'yetişme artığı' öncüden bağımsız artık dönüşünü öncüye mal eder mi?
    def b2(oncu, hedef):
        xo, rh = o.hizali_getiri(oncu), o.hizali_getiri(hedef)
        e_ = rh - o.kayan_beta(rh, xo) * xo
        ze = o.zskor(e_)
        return (-np.sign(ze)).where(ze.abs() >= 1, 0.0)
    rh = o.hizali_getiri("RSD")
    zr = o.zskor(rh)
    kiyas = (-np.sign(zr)).where(zr.abs() >= 1, 0.0)
    sB2, sSPY, sRast = b2("LDA", "RSD"), b2("SPY", "RSD"), b2("LEAD", "RSD")
    zl = o.zskor(o.hizali_getiri("LDA"))
    b1 = o.islem_testi(np.sign(zl).where(zl.abs() >= 1, 0.0), "RSD", 1, 0)

    def kisa(s_):
        r_ = o.islem_testi(s_, "RSD", 1, 0)
        return f"{r_['anormal_net_bps']};t={r_['t_anormal']}"
    saf = sB2.where(kiyas == 0, 0.0)  # B2 var, kıyas yok
    kayit("S7", "öncüde HİÇ bilgi yokken (hedef artığı kendi kendine dönüyor) RSD: B2(LDA) | kıyas: kendi getirisi | B2 ∧ kıyas yok | B2(SPY artığı) | B2(ilgisiz öncü) | B1(LDA)",
          f"{kisa(sB2)} | {kisa(kiyas)} | {kisa(saf)} | {kisa(sSPY)} | {kisa(sRast)} | {b1['anormal_net_bps']};t={b1['t_anormal']}",
          "B2(LDA), kıyası geçer ve 'artı katkı' gösterir; oysa SPY artığı aynı ya da daha iyi, B1 sıfır -> öncüye özgü bilgi yok", "KALDI")

    # ---- S8: gunluk_pnl zamanlaması ve toplamı islem_testi ile tutarlı mı?
    r1 = o.islem_testi(sin, "TGT", 1, 5)
    p1 = o.gunluk_pnl(sin, "TGT", 1, 5)
    p3 = o.gunluk_pnl(sin, "TGT", 3, 5)
    r3 = o.islem_testi(sin, "TGT", 3, 5)
    kayit("S8", "gunluk_pnl toplamı / islem_testi (n x net ort.): h=1 | h=3 (1/3 ağırlık)", f"{p1.sum() / (r1['n'] * r1['net_bps'] / 1e4):.3f} | {p3.sum() / (r3['n'] * r3['net_bps'] / 1e4 / 3):.3f}",
          "1,00 | ~1,00", "GECTI" if abs(p1.sum() / (r1["n"] * r1["net_bps"] / 1e4) - 1) < 0.01 and abs(p3.sum() / (r3["n"] * r3["net_bps"] / 1e4 / 3) - 1) < 0.05 else "KALDI")
    # ---- S9: bh_fdr ve nw_t bağımsız uygulamalarla aynı mı?
    from statsmodels.stats.multitest import multipletests
    import statsmodels.api as sm
    pp = np.concatenate([RNG.random(900), RNG.random(100) * 0.002])
    ayni = bool((o.bh_fdr(pp, 0.10) == multipletests(pp, alpha=0.10, method="fdr_bh")[0]).all())
    zz = np.convolve(RNG.standard_normal(3000), np.ones(3) / 3, mode="valid") + 0.02
    t_sm = float(sm.OLS(zz, np.ones(len(zz))).fit(cov_type="HAC", cov_kwds={"maxlags": 2, "use_correction": False}).tvalues[0])
    kayit("S9", "bh_fdr == statsmodels fdr_bh | nw_t(lag=2) - statsmodels HAC t", f"{ayni} | {o.nw_t(zz, 2) - t_sm:.1e}", "True | 0", "GECTI" if ayni and abs(o.nw_t(zz, 2) - t_sm) < 1e-6 else "KALDI")
    # ---- S10: havuzlanmış (çok hedefli) testte gün kümelenmesi: aynı günlerde 50 bağlantılı hedef
    Nh, Tg = 50, len(tk)
    carp = []
    for _ in range(300):
        ortak_f = RNG.standard_normal(Tg)
        Rh = 0.01 * (np.sqrt(0.5) * ortak_f[:, None] + np.sqrt(0.5) * RNG.standard_normal((Tg, Nh)))  # ikili korelasyon 0,5
        gun = RNG.random(Tg) < 0.15
        islemler = Rh[gun].ravel()
        saf_t = islemler.mean() / islemler.std() * np.sqrt(len(islemler))
        gunluk = np.where(gun, Rh.mean(1), 0.0)
        carp.append((saf_t, o.nw_t(gunluk, 0)))
    carp = np.array(carp)
    kayit("S10", "50 hedef, korelasyon 0,5, aynı sinyal günleri: işlemleri havuzlayıp düz t | gün bazında portföy serisi + nw_t (sıfırda std)",
          f"{carp[:, 0].std():.2f} | {carp[:, 1].std():.2f}", "1,00 | 1,00 (havuzlanmış düz t ~ sqrt(1+49*0,5) = 5 kat şişer)", "KALDI")


if __name__ == "__main__":
    gercek()
    sentetik()
    df = pd.DataFrame(SONUC)
    os.makedirs(os.path.join(o.KOK, "ek", "dogrulama"), exist_ok=True)
    df.to_csv(os.path.join(o.KOK, "ek", "dogrulama", "yontem_sinamasi.csv"), index=False)
    print("\nÖZET:", df.durum.value_counts().to_dict())
