"""Çürütücü B: S3-S8 (+ IYR, EWJ ek adayları) için çürütme testleri (YONTEM.md bölüm 6-7).

Çıktı: ek/dogrulama/curutme_b/{testler.csv, plasebo.csv, yillik.csv, donem_blok.csv, coklu_test.csv, son_gun.csv, OZET.txt}
Değerlendirme çekirdeği (deg, gdeg) bu betikte yeniden yazıldı; ortak.py'den yalnız veri okuma, hizalama, z/beta, maliyet
ve hac_t kullanılır. Taban satırlar ortak.donemli_test / havuz_donemli ile çapraz kontrol edilir.
Kullanım: python3 kod/curutme_b.py   (~1-2 dk)
"""
import os
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak as o  # noqa: E402

T0 = time.time()
CIKTI = os.path.join(o.KOK, "ek", "dogrulama", "curutme_b")
os.makedirs(CIKTI, exist_ok=True)
TK = o.takvim()
SPY = o.basit_getiri(["SPY"])["SPY"]
VIX = o.panel("close", ["^VIX"])["^VIX"]
KRIZ = pd.Series(((TK >= "2008-09-01") & (TK <= "2009-06-30")) | ((TK >= "2020-02-01") & (TK <= "2020-04-30")), index=TK)
PER = (("tum", None, None), ("is", None, o.IS_BITIS), ("oos", o.OOS_BAS, None), ("son", o.SON_BAS, None))
ROWS, PLAS, YIL, BLOK, SON, NOTLAR = [], [], [], [], [], []
VAR = set(o.meta().index)


def log(*a):
    print(f"[{time.time() - T0:5.0f}s]", *a, flush=True)


def _dl(x, b, e):
    if b is not None:
        x = x[x.index >= b]
    if e is not None:
        x = x[x.index <= e]
    return x


def bmin(w):
    return {250: 120}.get(w, w // 2)


def zmin(w):
    return {60: 40}.get(w, int(w * 2 / 3))


# ------------------------------------------------------------------------------------------------ çekirdek
def ileri(hedef, h, giris="kapanis", hedge=None, bwin=250):
    f = o.ileri_getiri([hedef], h, giris)[hedef]
    if hedge and hedge != hedef:
        fh = o.ileri_getiri([hedge], h, giris)[hedge]
        r = o.basit_getiri([hedef, hedge])
        f = f - o.kayan_beta(r[hedef], r[hedge], bwin, bmin(bwin)) * fh
    return f


def deg(sig, f, c, h, mask=None, haric_ust=0, haric_yil=False):
    """Tek hedef. sig: +1/-1/0; f: ileri getiri; c: maliyet (oran). Sürüklenme düzeltmesi dönem içi ortalama."""
    s = sig.reindex(f.index).fillna(0.0).copy()
    if mask is not None:
        s = s.where(mask.reindex(f.index).fillna(False).astype(bool), 0.0)
    cc = c.reindex(f.index).fillna(20 / 1e4) if isinstance(c, pd.Series) else pd.Series(float(c), index=f.index)
    if haric_ust or haric_yil:
        ok = f.notna() & (s != 0)
        abn = (s * (f - f[f.notna()].mean()) - cc)[ok]
        if haric_ust and len(abn) > haric_ust:
            s.loc[abn.sort_values(ascending=False).index[:haric_ust]] = 0.0
        if haric_yil and len(abn):
            y = abn.groupby(abn.index.year).sum().idxmax()
            s[s.index.year == y] = 0.0
    out = {}
    for ad, b, e in PER:
        ff, ss, c2 = _dl(f, b, e), _dl(s, b, e), _dl(cc, b, e)
        ok = ff.notna()
        ff, ss, c2 = ff[ok], ss[ok], c2[ok]
        akt = ss != 0
        n = int(akt.sum())
        out[ad + "_n"] = n
        if n < 10 or len(ff) < 60:
            continue
        dr = ff.mean()
        net = (ss * ff - c2)[akt]
        abn = (ss * (ff - dr) - c2)[akt]
        z = np.zeros(len(ff))
        z[akt.values] = abn.values
        zn = np.zeros(len(ff))
        zn[akt.values] = net.values
        out[ad + "_net"] = round(float(net.mean()) * 1e4, 1)
        out[ad + "_abn"] = round(float(abn.mean()) * 1e4, 1)
        out[ad + "_t"] = round(float(o.hac_t(z, h - 1)), 2)
        out[ad + "_tnet"] = round(float(o.hac_t(zn, h - 1)), 2)
        out[ad + "_isabet"] = round(float((ss * ff)[akt].gt(0).mean()), 3)
    return out


def gpanel(cols, h, giris="kapanis", hedge=None):
    F = o.ileri_getiri(cols, h, giris)
    if hedge:
        fh = o.ileri_getiri([hedge], h, giris)[hedge]
        r = o.basit_getiri(cols + [hedge])
        F = F - pd.DataFrame({c: o.kayan_beta(r[c], r[hedge]) for c in cols}).mul(fh, axis=0)
    return F


def gdeg(S, F, C, h, mask=None, haric_ust=0, haric_yil=False):
    """Grup (portföy) testi: gün başına eşit ağırlıklı ortalama; t gün serisinden."""
    S = S.reindex(F.index).fillna(0.0).copy()
    if mask is not None:
        S = S.where(mask.reindex(F.index).fillna(False).astype(bool), 0.0) if isinstance(mask, pd.DataFrame) else S.mul(
            mask.reindex(F.index).fillna(False).astype(float), axis=0)
    if haric_ust or haric_yil:
        akt = (S != 0) & F.notna()
        k = akt.sum(axis=1)
        pa = ((S * (F - F.mean()) - C).where(akt).sum(axis=1) / k).where(k > 0).dropna()
        if haric_ust:
            S.loc[pa.sort_values(ascending=False).index[:haric_ust]] = 0.0
        if haric_yil:
            y = pa.groupby(pa.index.year).sum().idxmax()
            S.loc[S.index.year == y] = 0.0
    out = {}
    for ad, b, e in PER:
        FF, SS, CC = _dl(F, b, e), _dl(S, b, e), _dl(C, b, e)
        akt = (SS != 0) & FF.notna()
        k = akt.sum(axis=1)
        var = k > 0
        out[ad + "_n"] = int(var.sum())
        if var.sum() < 10:
            continue
        dr = FF.mean()
        pa = ((SS * (FF - dr) - CC).where(akt).sum(axis=1) / k).where(var)
        pn = ((SS * FF - CC).where(akt).sum(axis=1) / k).where(var)
        out[ad + "_net"] = round(float(pn.mean()) * 1e4, 1)
        out[ad + "_abn"] = round(float(pa.mean()) * 1e4, 1)
        out[ad + "_t"] = round(float(o.hac_t(pa.fillna(0.0).values, h - 1)), 2)
        out[ad + "_tnet"] = round(float(o.hac_t(pn.fillna(0.0).values, h - 1)), 2)
        out[ad + "_isabet"] = round(float((pn[var] > 0).mean()), 3)
    return out


def ekle(sinyal, test, varyant, d, hedef=None, kume=ROWS):
    r = {"sinyal": sinyal, "test": test, "varyant": varyant}
    for k in ("tum_n", "tum_abn", "tum_net", "tum_t", "tum_tnet", "is_n", "is_abn", "is_t", "oos_n", "oos_abn", "oos_t",
              "oos_net", "is_net", "son_n", "son_net", "son_abn", "son_t", "tum_isabet"):
        r[k] = d.get(k)
    kume.append(r)
    return r


def hac_ols(y, X, L):
    X = np.column_stack([np.ones(len(y)), X])
    XtXi = np.linalg.inv(X.T @ X)
    b = XtXi @ X.T @ y
    Xu = X * (y - X @ b)[:, None]
    S = Xu.T @ Xu
    for k in range(1, L + 1):
        G = Xu[k:].T @ Xu[:-k]
        S += G + G.T
    V = XtXi @ S @ XtXi
    d = np.diag(V)
    if (d <= 0).any():
        d = np.diag(XtXi @ (Xu.T @ Xu) @ XtXi)
    return b, b / np.sqrt(d)


def hizala(r):
    """f1_emtia.hizala ile aynı: kendi takvimindeki fark, o gün ya da sonraki ilk NYSE gününe toplanır."""
    r = r.dropna()
    tam = o.oku("SPY").index
    pos = tam.searchsorted(r.index, side="left")
    ok = pos < len(tam)
    s = pd.Series(r.values[ok], index=tam[pos[ok]]).groupby(level=0).sum().reindex(TK)
    ilk = r.index.min()
    s[s.index < ilk] = np.nan
    return s.where(s.notna() | (s.index < ilk), 0.0)


def crack_serisi():
    lv = pd.concat({s: o.oku(s)["close"] for s in ("RB=F", "HO=F", "CL=F")}, axis=1, sort=True).dropna()
    crack = (2 * lv["RB=F"] * 42 + lv["HO=F"] * 42 - 3 * lv["CL=F"]) / 3
    return hizala(crack.diff()), crack, lv


def ll_sig(x, arindir=True, zwin=60, bwin=250, esik=1.0, lag=0, faktor=None):
    x = x.reindex(TK)
    if lag:
        x = x.shift(lag)
    if arindir:
        fk = SPY if faktor is None else o.basit_getiri([faktor])[faktor]
        x = x - o.kayan_beta(x, fk, bwin, bmin(bwin)) * fk
    z = o.zskor(x, zwin, zmin(zwin))
    return np.sign(z).where(z.abs() >= esik, 0.0).fillna(0.0), z


def yillik(ad, sig, f, c):
    s = sig.reindex(f.index).fillna(0.0)
    ok = f.notna() & (s != 0)
    abn = (s * (f - f[f.notna()].mean()) - c.reindex(f.index).fillna(20 / 1e4))[ok]
    g = abn.groupby(abn.index.year)
    t = pd.DataFrame({"n": g.size(), "abn_bps": (g.mean() * 1e4).round(1)})
    for y, r in t.iterrows():
        YIL.append({"sinyal": ad, "yil": y, "n": int(r.n), "abn_bps": r.abn_bps})
    t = t[t.n >= 3]
    i, oo = t[t.index <= 2018], t[t.index >= 2019]
    return (f"yıl+ IS {(i.abn_bps > 0).sum()}/{len(i)}, OOS {(oo.abn_bps > 0).sum()}/{len(oo)} | " +
            " ".join(f"{str(y)[2:]}:{v:+.0f}" for y, v in t.abn_bps.items()))


# ------------------------------------------------------------------------------------------------ öncü-hedef (S5-S8)
def ll_testler(ad, x, hedef, h, arindir, plasebo_oncu, roll=None, diger_hedge=()):
    hd = "SPY" if arindir else None
    c = o.maliyet_serisi(hedef) / 1e4
    f = ileri(hedef, h, hedge=hd)
    fham = ileri(hedef, h)
    sig, z = ll_sig(x, arindir)
    d0 = deg(sig, f, c, h)
    ekle(ad, "0 taban", "tanım", d0)
    chk = o.donemli_test(sig, hedef, h, hedge=hd)
    NOTLAR.append(f"{ad} taban: n {d0['tum_n']} abn {d0['tum_abn']} tIS {d0.get('is_t')} tOOS {d0.get('oos_t')} | ortak: n {chk['tum_n']} "
                  f"abn {chk['tum_anormal_net_bps']} tIS {chk.get('is_t_anormal')} tOOS {chk.get('oos_t_anormal')}")
    # 1 gecikme
    for L in (1, 2):
        ekle(ad, "1 öncü gecikme", f"{L} gün", deg(ll_sig(x, arindir, lag=L)[0], f, c, h))
    # 3 aynı gün tepki kontrolü (regresyon)
    r = o.basit_getiri([hedef])[hedef]
    zres = o.zskor(r - o.kayan_beta(r, SPY) * SPY, 60).clip(-5, 5)
    zret = o.zskor(r, 60).clip(-5, 5)
    D = pd.DataFrame({"f": f, "sig": sig, "zc": z.clip(-5, 5), "zres": zres, "zret": zret}).dropna()
    for pad, b, e in PER[:3]:
        dd = _dl(D, b, e)
        if len(dd) < 300:
            continue
        b1, t1 = hac_ols(dd.f.values, dd[["sig"]].values, h - 1)
        b2, t2 = hac_ols(dd.f.values, dd[["sig", "zres", "zret"]].values, h - 1)
        b3, t3 = hac_ols(dd.f.values, dd[["zc", "zres", "zret"]].values, h - 1)
        ROWS.append({"sinyal": ad, "test": "3 regresyon", "varyant": f"{pad}: sig tek başına b={b1[1] * 1e4:.1f}bps t={t1[1]:.2f} | kontrollü "
                     f"b={b2[1] * 1e4:.1f} t={t2[1]:.2f} (zres t={t2[2]:.2f}, zret t={t2[3]:.2f}) | sürekli z kontrollü t={t3[1]:.2f}"})
    ayni = (sig * zres) >= 0.5
    ekle(ad, "3 aynı gün", "hedef aynı gün aynı yönde tepki verdi (z>=0,5)", deg(sig, f, c, h, mask=ayni))
    ekle(ad, "3 aynı gün", "hedef tepki vermedi (z<0,5)", deg(sig, f, c, h, mask=~ayni))
    rr = (r - o.kayan_beta(r, SPY) * SPY) if arindir else r
    NOTLAR.append(f"{ad} hedefin sinyal günü aynı gün {'artık ' if arindir else ''}getirisi: AL günleri {rr[sig > 0].mean() * 1e4:+.0f} bps, "
                  f"SAT günleri {rr[sig < 0].mean() * 1e4:+.0f} bps; corr(z, aynı gün) {z.corr(rr):.2f}")
    # 4 tanım kırılganlığı
    for zw in (40, 120):
        ekle(ad, "4 kırılganlık", f"z penceresi {zw}", deg(ll_sig(x, arindir, zwin=zw)[0], f, c, h))
    for es in (0.75, 1.5, 2.0):
        ekle(ad, "4 kırılganlık", f"eşik {es}", deg(ll_sig(x, arindir, esik=es)[0], f, c, h))
    if arindir:
        for bw in (120, 500):
            ekle(ad, "4 kırılganlık", f"beta penceresi {bw}", deg(ll_sig(x, True, bwin=bw)[0], ileri(hedef, h, hedge="SPY", bwin=bw), c, h))
    for hh in (1, 2, 3):
        if hh != h:
            ekle(ad, "4 kırılganlık", f"h={hh}", deg(sig, ileri(hedef, hh, hedge=hd), c, hh))
    ekle(ad, "4 kırılganlık", "arındırma " + ("yok (ham öncü, ham hedef)" if arindir else "var (SPY)"),
         deg(ll_sig(x, not arindir)[0], ileri(hedef, h, hedge=None if arindir else "SPY"), c, h))
    for hg in diger_hedge:
        if hg in VAR:
            ekle(ad, "4 kırılganlık", f"öncü ve hedef {hg}'den arındırılmış", deg(ll_sig(x, True, faktor=hg)[0], ileri(hedef, h, hedge=hg), c, h))
    ekle(ad, "4 kırılganlık", "sınır sinyalleri hariç (|z| 1,0-1,2)", deg(sig, f, c, h, mask=z.abs() >= 1.2))
    ekle(ad, "4 kırılganlık", "maliyet 2 kat", deg(sig, f, c * 2, h))
    # 5 alt dönem / rejim
    ekle(ad, "5 rejim", "VIX > 20", deg(sig, f, c, h, mask=VIX > 20))
    ekle(ad, "5 rejim", "VIX <= 20", deg(sig, f, c, h, mask=VIX <= 20))
    ekle(ad, "5 rejim", "VIX > 30", deg(sig, f, c, h, mask=VIX > 30))
    ekle(ad, "5 rejim", "kriz hariç", deg(sig, f, c, h, mask=~KRIZ))
    ekle(ad, "5 rejim", "en iyi 10 işlem hariç", deg(sig, f, c, h, haric_ust=10))
    ekle(ad, "5 rejim", "en iyi yıl hariç", deg(sig, f, c, h, haric_yil=True))
    if roll is not None:
        ekle(ad, "5 rejim", "vade geçişi günleri hariç", deg(sig, f, c, h, mask=~roll))
        ekle(ad, "5 rejim", "yalnız vade geçişi günleri", deg(sig, f, c, h, mask=roll))
    NOTLAR.append(f"{ad} {yillik(ad, sig, f, c)}")
    for bl, b, e in (("2005-12", None, "2012-12-31"), ("2013-18", "2013-01-01", "2018-12-31"), ("2019-21", "2019-01-01", "2021-12-31"),
                     ("2022-23", "2022-01-01", "2023-12-31"), ("2024-26", "2024-01-01", None)):
        ss, ff = _dl(sig, b, e), _dl(f, b, e)
        ok = ff.notna() & (ss != 0)
        ab = (ss * (ff - f[f.notna()].mean()))[ok] - c.reindex(ff.index)[ok]
        zz = pd.Series(0.0, index=ff.index[ff.notna()])
        zz[ab.index] = ab
        BLOK.append({"sinyal": ad, "blok": bl, "n": int(ok.sum()), "abn_bps": round(ab.mean() * 1e4, 1) if len(ab) else np.nan,
                     "t": round(float(o.hac_t(zz.values, h - 1)), 2) if len(ab) >= 10 else np.nan,
                     "es_zamanli_corr": round(float(_dl(z, b, e).clip(-5, 5).corr(_dl(rr, b, e))), 3)})
    # 6 uygulanabilirlik
    al, sat = sig.where(sig > 0, 0.0), sig.where(sig < 0, 0.0)
    ekle(ad, "6 bacak", "AL bacağı (tanımdaki hedge ile)", deg(al, f, c, h))
    ekle(ad, "6 bacak", "SAT bacağı (tanımdaki hedge ile)", deg(sat, f, c, h))
    ekle(ad, "6 bacak", "AL bacağı HEDGE'SİZ (ham hedef getirisi)", deg(al, fham, c, h))
    ekle(ad, "6 bacak", "AL hedge'siz, VIX <= 20", deg(al, fham, c, h, mask=VIX <= 20))
    ekle(ad, "6 bacak", "AL hedge'siz, VIX > 20", deg(al, fham, c, h, mask=VIX > 20))
    ekle(ad, "6 bacak", "AL hedge'siz, en iyi 10 hariç", deg(al, fham, c, h, haric_ust=10))
    ekle(ad, "6 bacak", "AL hedge'siz, kriz hariç", deg(al, fham, c, h, mask=~KRIZ))
    ekle(ad, "6 bacak", "AL hedge'siz, öncü 1 gün gecikmeli", deg(ll_sig(x, arindir, lag=1)[0].clip(lower=0), fham, c, h))
    ekle(ad, "6 bacak", "SAT bacağı HEDGE'SİZ (açığa, ham)", deg(sat, fham, c, h))
    ekle(ad, "6 giriş", "ertesi açılış girişi", deg(sig, ileri(hedef, h, "acilis", hd), c, h))
    ekle(ad, "6 giriş", "ertesi kapanış girişi (1 gün geç)", deg(sig, ileri(hedef, h, "ertesi", hd), c, h))
    ekle(ad, "6 parça", "gece (kapanış t -> açılış t+1), maliyetsiz", deg(sig, ileri(hedef, 1, "gece", hd), 0.0, 1))
    ekle(ad, "6 parça", "gün içi t+1 (açılış -> kapanış), maliyetsiz", deg(sig, ileri(hedef, 1, "acilis", hd), 0.0, 1))
    if h > 1:
        ekle(ad, "6 parça", f"t+1 kapanış -> t+{h} kapanış, maliyetsiz", deg(sig, ileri(hedef, h - 1, "ertesi", hd), 0.0, h - 1))
    # 2 plasebo öncüler
    for pn, px in plasebo_oncu.items():
        d = deg(ll_sig(px, arindir)[0], f, c, h)
        ekle(ad, "2 plasebo öncü", pn, d, kume=PLAS)
    son = {"sinyal": ad, "son_gun": str(z.dropna().index[-1].date())}
    for k in (1, 2, 3):
        son[f"z_t-{k - 1}"] = round(float(z.iloc[-k]), 2) if z.iloc[-k] == z.iloc[-k] else np.nan
        son[f"sig_t-{k - 1}"] = float(sig.iloc[-k])
    SON.append(son)
    return sig, z, f, c


def hg(sym):
    return o.hizali_getiri(sym)


def oncu_sozluk(liste):
    return {s: hg(s) for s in liste if s in VAR}


def genis_plasebo(ad, hedef, h, oncular, gercek, arindir=True):
    """Çok sayıda öncüyle aynı test: gerçek öncünün sırası."""
    hd = "SPY" if arindir else None
    f, c = ileri(hedef, h, hedge=hd), o.maliyet_serisi(hedef) / 1e4
    sat = []
    for s in oncular:
        if s == hedef or s not in VAR:
            continue
        try:
            d = deg(ll_sig(hg(s), arindir)[0], f, c, h)
        except Exception:  # noqa: BLE001
            continue
        if d.get("tum_n", 0) >= 300 and d.get("is_t") is not None and d.get("oos_t") is not None:
            sat.append({"oncu": s, **d})
    df = pd.DataFrame(sat)
    g = df[df.oncu == gercek].iloc[0]
    NOTLAR.append(f"{ad} geniş plasebo ({len(df)} öncü -> {hedef}): tüm t>=2 olan %{(df.tum_t >= 2).mean() * 100:.0f}, tüm t ort {df.tum_t.mean():+.2f}, "
                  f"medyan abn {df.tum_abn.median():+.1f} bps; IS t>=2,5 ve OOS t>=2,0: {int(((df.is_t >= 2.5) & (df.oos_t >= 2.0)).sum())}; "
                  f"{gercek} sırası (tüm t): {int((df.tum_t > g.tum_t).sum()) + 1}/{len(df)}; IS t>=2 ve OOS t>=2 olanlar: "
                  f"{', '.join(df[(df.is_t >= 2) & (df.oos_t >= 2)].oncu)}")
    df.insert(0, "sinyal", ad)
    return df


def genis_hedef(ad, x, hedefler, h, gercek, arindir=True):
    sat = []
    sig = ll_sig(x, arindir)[0]
    for s in hedefler:
        if s not in VAR:
            continue
        try:
            d = deg(sig, ileri(s, h, hedge="SPY" if arindir else None), o.maliyet_serisi(s) / 1e4, h)
        except Exception:  # noqa: BLE001
            continue
        if d.get("tum_n", 0) >= 300 and d.get("is_t") is not None and d.get("oos_t") is not None:
            sat.append({"hedef": s, **d})
    df = pd.DataFrame(sat)
    g = df[df.hedef == gercek]
    NOTLAR.append(f"{ad} aynı öncü -> {len(df)} hedef: tüm t>=2 %{(df.tum_t >= 2).mean() * 100:.0f}, tüm t ort {df.tum_t.mean():+.2f}; IS>=2,5&OOS>=2,0: "
                  f"{int(((df.is_t >= 2.5) & (df.oos_t >= 2.0)).sum())}; {gercek} sırası {int((df.tum_t > g.tum_t.iloc[0]).sum()) + 1 if len(g) else '-'}/{len(df)}; "
                  + "; ".join(f"{r.hedef} {r.tum_abn:+.0f}bps t{r.is_t:+.1f}/{r.oos_t:+.1f}" for r in df.sort_values('tum_t', ascending=False).head(12).itertuples()))
    df.insert(0, "sinyal", ad)
    return df


# ------------------------------------------------------------------------------------------------ grup kuralları (S3, S4)
def kural(sem, tur, esik, zwin=60, ma=200, vix_esik=20.0):
    c = o.panel("adjclose", sem)
    r = c.pct_change(fill_method=None)
    sd = r.rolling(zwin, min_periods=zmin(zwin)).std().shift(1)
    if tur == "Z5_SAT_VIX":
        z = r.rolling(5).sum() / (sd * np.sqrt(5))
        S = -((z >= esik) & c.notna()).astype(float)
        S = S.mul((VIX.reindex(c.index) > vix_esik).astype(float), axis=0)
    elif tur == "Z1_AL_ALT200":
        z = r / sd
        m = c.rolling(ma, min_periods=ma).mean()
        S = ((z <= -esik) & (c < m)).astype(float)
    elif tur == "Z5_SAT_ALT200":
        z = r.rolling(5).sum() / (sd * np.sqrt(5))
        m = c.rolling(ma, min_periods=ma).mean()
        S = -((z >= esik) & (c < m)).astype(float)
    elif tur == "IBS_AL_UST200":
        hi, lo, cl = o.panel("high", sem), o.panel("low", sem), o.panel("close", sem)
        ibs = ((cl - lo) / (hi - lo)).where(hi > lo)
        m = c.rolling(ma, min_periods=ma).mean()
        S = ((ibs < esik) & (c > m)).astype(float)
        z = ibs
    return S, z


def grup_testler(ad, grup_adi, tur, esik, h, sektor_etf):
    abd = set(o.abd_semboller("EQUITY"))
    sem = [s for s in o.grup(grup_adi) if s in abd]
    C = pd.DataFrame({s: o.maliyet_serisi(s) for s in sem}).fillna(20.0) / 1e4
    F = gpanel(sem, h)
    S, Z = kural(sem, tur, esik)
    d0 = gdeg(S, F, C, h)
    ekle(ad, "0 taban", "tanım", d0)
    chk = o.havuz_donemli(S, h)
    NOTLAR.append(f"{ad} taban ({len(sem)} hisse): gün {d0['tum_n']} abn {d0['tum_abn']} ham net {d0['tum_net']} tIS {d0.get('is_t')} tOOS {d0.get('oos_t')} | "
                  f"ortak: gün {chk['tum_n_gun']} abn {chk['tum_anormal_net_bps']} tIS {chk.get('is_t_anormal')} tOOS {chk.get('oos_t_anormal')}")
    ekle(ad, "1 gecikme", "sinyal 1 gün geç (ertesi kapanış girişi)", gdeg(S, gpanel(sem, h, "ertesi"), C, h))
    ekle(ad, "1 gecikme", "ertesi açılış girişi", gdeg(S, gpanel(sem, h, "acilis"), C, h))
    ekle(ad, "1 gecikme", "sinyal 2 gün geç", gdeg(S.shift(2), F, C, h))
    ekle(ad, "3 piyasa", "SPY hedge'li", gdeg(S, gpanel(sem, h, hedge="SPY"), C, h))
    if sektor_etf in VAR:
        ekle(ad, "3 piyasa", f"{sektor_etf} hedge'li", gdeg(S, gpanel(sem, h, hedge=sektor_etf), C, h))
    # aynı kural SPY ve sektör ETF'inde
    for e in ("SPY", sektor_etf):
        if e in VAR:
            Se, _ = kural([e], tur, esik)
            ekle(ad, "3 piyasa", f"aynı kural {e}'in kendisinde", deg(Se[e], ileri(e, h), o.maliyet_serisi(e) / 1e4, h))
    # piyasa koşulu: grup sinyali varken SPY'ın aynı günü
    spy_s, _ = kural(["SPY"], tur, esik)
    ekle(ad, "3 piyasa", "SPY'da aynı sinyal YOKKEN", gdeg(S, F, C, h, mask=spy_s["SPY"] == 0))
    ekle(ad, "3 piyasa", "SPY'da aynı sinyal VARKEN", gdeg(S, F, C, h, mask=spy_s["SPY"] != 0))
    # 4 kırılganlık
    for es in sorted({esik - 0.5, esik - 0.25, esik + 0.25, esik + 0.5}):
        ekle(ad, "4 kırılganlık", f"eşik {es}", gdeg(kural(sem, tur, es)[0], F, C, h))
    for zw in (40, 120):
        ekle(ad, "4 kırılganlık", f"z penceresi {zw}", gdeg(kural(sem, tur, esik, zwin=zw)[0], F, C, h))
    if tur == "Z5_SAT_VIX":
        for ve in (15, 18, 22, 25, 30):
            ekle(ad, "4 kırılganlık", f"VIX eşiği {ve}", gdeg(kural(sem, tur, esik, vix_esik=ve)[0], F, C, h))
        ekle(ad, "4 kırılganlık", "VIX koşulu yok", gdeg(kural(sem, tur, esik, vix_esik=0)[0], F, C, h))
        ekle(ad, "4 kırılganlık", "VIX <= 20 iken", gdeg(kural(sem, tur, esik, vix_esik=0)[0], F, C, h, mask=VIX <= 20))
    else:
        for m in (100, 150, 250):
            ekle(ad, "4 kırılganlık", f"ortalama {m} gün", gdeg(kural(sem, tur, esik, ma=m)[0], F, C, h))
        ekle(ad, "5 rejim", "VIX > 20", gdeg(S, F, C, h, mask=VIX > 20))
        ekle(ad, "5 rejim", "VIX <= 20", gdeg(S, F, C, h, mask=VIX <= 20))
        ekle(ad, "5 rejim", "VIX > 30", gdeg(S, F, C, h, mask=VIX > 30))
    for hh in (1, 2, 3):
        if hh != h:
            ekle(ad, "4 kırılganlık", f"h={hh}", gdeg(S, gpanel(sem, hh), C, hh))
    ekle(ad, "4 kırılganlık", "maliyet 2 kat", gdeg(S, F, C * 2, h))
    ekle(ad, "5 rejim", "kriz hariç", gdeg(S, F, C, h, mask=~KRIZ))
    ekle(ad, "5 rejim", "en iyi 10 gün hariç", gdeg(S, F, C, h, haric_ust=10))
    ekle(ad, "5 rejim", "en iyi yıl hariç", gdeg(S, F, C, h, haric_yil=True))
    # yıl yıl (gün bazlı portföy)
    akt = (S != 0) & F.notna()
    k = akt.sum(axis=1)
    pa = ((S * (F - F.mean()) - C).where(akt).sum(axis=1) / k).where(k > 0).dropna()
    pn = ((S * F - C).where(akt).sum(axis=1) / k).where(k > 0).dropna()
    g = pa.groupby(pa.index.year)
    t = pd.DataFrame({"n": g.size(), "abn_bps": (g.mean() * 1e4).round(1), "ham_net_bps": (pn.groupby(pn.index.year).mean() * 1e4).round(1)})
    for y, r in t.iterrows():
        YIL.append({"sinyal": ad, "yil": y, "n": int(r.n), "abn_bps": r.abn_bps, "ham_net_bps": r.ham_net_bps})
    t3 = t[t.n >= 3]
    NOTLAR.append(f"{ad} yıl+ (abn) IS {(t3[t3.index <= 2018].abn_bps > 0).sum()}/{(t3.index <= 2018).sum()}, OOS {(t3[t3.index >= 2019].abn_bps > 0).sum()}/"
                  f"{(t3.index >= 2019).sum()}; ham net yıl+ {(t3.ham_net_bps > 0).sum()}/{len(t3)} | " + " ".join(f"{str(y)[2:]}:{v:+.0f}({int(n)})" for y, v, n in zip(t3.index, t3.abn_bps, t3.n)))
    NOTLAR.append(f"{ad} sinyal günlerinin dağılımı: VIX>30 %{(VIX.reindex(pa.index) > 30).mean() * 100:.0f}, kriz dönemleri %{KRIZ.reindex(pa.index).mean() * 100:.0f}; "
                  f"en yoğun 3 yıl günlerin %{t.n.sort_values().tail(3).sum() / t.n.sum() * 100:.0f}'i ({', '.join(str(y) for y in t.n.sort_values().tail(3).index)})")
    # hisse hisse ve biri hariç
    his = []
    for s in sem:
        d = deg(S[s], F[s], C[s], h)
        his.append({"sinyal": ad, "hisse": s, **d})
        ekle(ad, "2 hisse hisse", s, d, kume=PLAS)
    hd = pd.DataFrame(his)
    lo = []
    for s in sem:
        d = gdeg(S.drop(columns=s), F.drop(columns=s), C.drop(columns=s), h)
        lo.append((s, d.get("is_t"), d.get("oos_t"), d.get("tum_abn")))
    lo = pd.DataFrame(lo, columns=["h", "is_t", "oos_t", "abn"])
    NOTLAR.append(f"{ad} hisse hisse: abn > 0 olan {(hd.tum_abn > 0).sum()}/{hd.tum_abn.notna().sum()}; OOS abn > 0 {(hd.oos_abn > 0).sum()}/{hd.oos_abn.notna().sum()}; "
                  f"biri hariç en düşük tIS {lo.is_t.min()} ({lo.h[lo.is_t.idxmin()]}), en düşük tOOS {lo.oos_t.min()} ({lo.h[lo.oos_t.idxmin()]})")
    # 2 plasebo: aynı kural bütün hisse gruplarında
    m = o.meta()
    gs = sorted(set(x for y in m.gruplar.astype(str) for x in y.split(";") if x.startswith("h_")))
    sat = []
    for gname in gs:
        ss = [s for s in o.grup(gname) if s in abd]
        if len(ss) < 5:
            continue
        Sg, _ = kural(ss, tur, esik)
        Cg = pd.DataFrame({s: o.maliyet_serisi(s) for s in ss}).fillna(20.0) / 1e4
        d = gdeg(Sg, gpanel(ss, h), Cg, h)
        d2 = gdeg(Sg, gpanel(ss, h, hedge="SPY"), Cg, h)
        sat.append({"grup": gname, **d, "spyh_is_t": d2.get("is_t"), "spyh_oos_t": d2.get("oos_t"), "spyh_abn": d2.get("tum_abn")})
        ekle(ad, "2 aynı kural başka grupta", gname, d, kume=PLAS)
    gd = pd.DataFrame(sat)
    me = gd[gd.grup == grup_adi].iloc[0]
    NOTLAR.append(f"{ad} aynı kural {len(gd)} hisse grubunda: abn medyan {gd.tum_abn.median():+.1f} bps, abn > 0 olan {(gd.tum_abn > 0).sum()}; IS t>=2,5&OOS t>=2,0: "
                  f"{', '.join(gd[(gd.is_t >= 2.5) & (gd.oos_t >= 2.0)].grup)}; IS t>=2&OOS t>=1,5: {int(((gd.is_t >= 2) & (gd.oos_t >= 1.5)).sum())}; "
                  f"{grup_adi} sırası (abn) {int((gd.tum_abn > me.tum_abn).sum()) + 1}/{len(gd)}; IS t ort {gd.is_t.mean():+.2f}, OOS t ort {gd.oos_t.mean():+.2f}; "
                  f"SPY hedge'li {grup_adi}: abn {me.spyh_abn} t {me.spyh_is_t}/{me.spyh_oos_t}")
    gd.insert(0, "sinyal", ad)
    son = S.iloc[-1]
    SON.append({"sinyal": ad, "son_gun": str(S.index[-1].date()), "acik_hisseler": ",".join(son[son != 0].index), "n_acik": int((son != 0).sum()),
                "vix": float(VIX.iloc[-1]), "son3gun_sinyal_sayisi": int((S.iloc[-3:] != 0).values.sum())})
    return gd, S


def tek_testler(ad, hedef, tur, esik, h):
    S, Z = kural([hedef], tur, esik)
    s, c, f = S[hedef], o.maliyet_serisi(hedef) / 1e4, ileri(hedef, h)
    d0 = deg(s, f, c, h)
    ekle(ad, "0 taban", "tanım", d0)
    chk = o.donemli_test(s, hedef, h)
    NOTLAR.append(f"{ad} taban: n {d0['tum_n']} abn {d0['tum_abn']} ham net {d0['tum_net']} tIS {d0.get('is_t')} tOOS {d0.get('oos_t')} | ortak: n {chk['tum_n']} abn "
                  f"{chk['tum_anormal_net_bps']} tIS {chk.get('is_t_anormal')} tOOS {chk.get('oos_t_anormal')}")
    ekle(ad, "1 gecikme", "ertesi açılış girişi", deg(s, ileri(hedef, h, "acilis"), c, h))
    ekle(ad, "1 gecikme", "ertesi kapanış girişi", deg(s, ileri(hedef, h, "ertesi"), c, h))
    ekle(ad, "3 piyasa", "SPY hedge'li", deg(s, ileri(hedef, h, hedge="SPY"), c, h))
    ekle(ad, "3 piyasa", "aynı kural SPY'da", deg(kural(["SPY"], tur, esik)[0]["SPY"], ileri("SPY", h), o.maliyet_serisi("SPY") / 1e4, h))
    for es in ((esik - 0.5, esik - 0.25, esik + 0.25, esik + 0.5) if esik > 1 else (0.1, 0.15, 0.25, 0.3)):
        ekle(ad, "4 kırılganlık", f"eşik {es}", deg(kural([hedef], tur, es)[0][hedef], f, c, h))
    for m in (100, 150, 250):
        ekle(ad, "4 kırılganlık", f"ortalama {m} gün", deg(kural([hedef], tur, esik, ma=m)[0][hedef], f, c, h))
    for hh in (1, 2, 3):
        if hh != h:
            ekle(ad, "4 kırılganlık", f"h={hh}", deg(s, ileri(hedef, hh), c, hh))
    ekle(ad, "4 kırılganlık", "maliyet 2 kat", deg(s, f, c * 2, h))
    ekle(ad, "5 rejim", "VIX > 20", deg(s, f, c, h, mask=VIX > 20))
    ekle(ad, "5 rejim", "VIX <= 20", deg(s, f, c, h, mask=VIX <= 20))
    ekle(ad, "5 rejim", "kriz hariç", deg(s, f, c, h, mask=~KRIZ))
    ekle(ad, "5 rejim", "en iyi 10 işlem hariç", deg(s, f, c, h, haric_ust=10))
    ekle(ad, "5 rejim", "en iyi yıl hariç", deg(s, f, c, h, haric_yil=True))
    ekle(ad, "6 parça", "gece, maliyetsiz", deg(s, ileri(hedef, 1, "gece"), 0.0, 1))
    ekle(ad, "6 parça", "gün içi t+1, maliyetsiz", deg(s, ileri(hedef, 1, "acilis"), 0.0, 1))
    NOTLAR.append(f"{ad} {yillik(ad, s, f, c)}")
    SON.append({"sinyal": ad, "son_gun": str(s.index[-1].date()), "sig_t-0": float(s.iloc[-1]), "z_t-0": round(float(Z[hedef].iloc[-1]), 2)})


# ------------------------------------------------------------------------------------------------ çoklu test bağlamı
def coklu_test():
    sat = []
    for dosya, aile in (("f1_emtia", "F1"), ("cift", "F2"), ("cift", "F3"), ("cift", "F1"), ("f4_kendi", None)):
        d = pd.read_csv(os.path.join(o.KOK, "ek", "backtest", dosya, "sonuclar.csv"), low_memory=False)
        if aile and "aile" in d.columns:
            d = d[d.aile == aile]
        if dosya == "f4_kendi":
            d = d[d.havuz == "portföy"]
        i, oo = pd.to_numeric(d["is_t_anormal"], errors="coerce"), pd.to_numeric(d["oos_t_anormal"], errors="coerce")
        n = int((i.notna() & oo.notna()).sum())
        sat.append({"dosya": dosya, "aile": aile or "F4 portföy", "n_test": n, "sifir_beklenen_t>=2.5": round(n * 0.0062, 1),
                    "IS_t>=2.5": int((i >= 2.5).sum()), "IS_t<=-2.5": int((i <= -2.5).sum()),
                    "OOS_t>=2.5": int((oo >= 2.5).sum()), "OOS_t<=-2.5": int((oo <= -2.5).sum()),
                    "OOS_t>=3.4": int((oo >= 3.4).sum()), "OOS_t<=-3.4": int((oo <= -3.4).sum()),
                    "yeni_rejim(IS<2,OOS>=2.5)": int(((i < 2) & (oo >= 2.5)).sum()), "ters(IS>-2,OOS<=-2.5)": int(((i > -2) & (oo <= -2.5)).sum()),
                    "IS>=2.5&OOS>=2.0": int(((i >= 2.5) & (oo >= 2.0)).sum()), "IS<=-2.5&OOS<=-2.0": int(((i <= -2.5) & (oo <= -2.0)).sum()),
                    "IS>=2.5&OOS>=2.0 beklenen": round(n * 1.4e-4, 2)})
    return pd.DataFrame(sat)


# ------------------------------------------------------------------------------------------------ ana
def main():
    dcr, crack, lv = crack_serisi()
    # vade geçişi günleri: RB/HO ayın son iş günü ve sonraki ilk gün; CL ayın 19-23'ü
    ay_son = pd.Series(TK, index=TK).groupby([TK.year, TK.month]).transform("max") == pd.Series(TK, index=TK)
    ay_ilk = pd.Series(TK, index=TK).groupby([TK.year, TK.month]).transform("min") == pd.Series(TK, index=TK)
    roll = ay_son | ay_ilk | pd.Series((TK.day >= 19) & (TK.day <= 23), index=TK)
    emtia = ["CL=F", "BZ=F", "RB=F", "HO=F", "NG=F", "GC=F", "HG=F", "ZC=F", "ZW=F", "ZS=F", "ZM=F", "ZL=F", "SB=F", "KC=F"]
    rb_cr = hizala((lv["RB=F"] * 42 - lv["CL=F"]).diff())
    ho_cr = hizala((lv["HO=F"] * 42 - lv["CL=F"]).diff())
    cl_d = hizala(lv["CL=F"].diff())
    cr_pl = {"crack 1 gün ileri (ileri bakış kıyası)": dcr.shift(-1), "benzin marjı (RB-CL) $": rb_cr, "dizel marjı (HO-CL) $": ho_cr, "CL=F $ farkı": cl_d,
             **oncu_sozluk(emtia + ["XLE", "XOM", "USO", "UGA", "TLT", "GLD", "XLU"])}

    # ---- S5
    log("S5")
    p5 = dict(cr_pl)
    p5["VLO kendi getirisi (momentum)"] = hg("VLO")
    sig5, z5, f5, c5 = ll_testler("S5 crack->VLO", dcr, "VLO", 2, True, p5, roll=roll, diger_hedge=("XLE",))
    raf = [s for s in ("VLO", "MPC", "PSX", "PBF", "DINO", "HFC", "DK", "PARR", "CVI", "XOM", "CVX", "COP", "XLE", "OXY", "PG", "JPM", "WMT", "UNH") if s in VAR]
    gh5 = genis_hedef("S5 crack->VLO", dcr, raf, 2, "VLO")
    # ---- S8
    log("S8")
    p8 = dict(cr_pl)
    p8["PBF kendi getirisi (momentum)"] = hg("PBF")
    p8["SPY getirisi"] = hg("SPY")
    sig8, z8, f8, c8 = ll_testler("S8 crack->PBF ham", dcr, "PBF", 3, False, p8, roll=roll, diger_hedge=("XLE",))
    gh8 = genis_hedef("S8 crack->PBF ham", dcr, raf, 3, "PBF", arindir=False)
    # ---- S6
    log("S6")
    yar = [s for s in o.grup("h_yariiletken")]
    don = [s for s in o.grup("h_donanim_ag")]
    ilgisiz = ["XOM", "JPM", "PG", "WMT", "KO", "UNH", "CAT", "BA", "GLD", "TLT", "XLU", "VLO", "HD", "DIS"]
    p6 = oncu_sozluk(["NVDA", "AMD", "INTC", "TXN", "AVGO", "AMAT", "LRCX", "KLAC", "QCOM", "STX", "SMH", "SOXX", "QQQ"] + ilgisiz)
    p6["WDC kendi getirisi (momentum)"] = hg("WDC")
    sig6, z6, f6, c6 = ll_testler("S6 MU->WDC", hg("MU"), "WDC", 3, True, p6, diger_hedge=("SMH", "QQQ"))
    abd = o.abd_semboller("EQUITY")
    rng = np.random.default_rng(0)
    rast = list(rng.choice(sorted(set(abd) - set(yar) - set(don)), 120, replace=False))
    gp6a = genis_plasebo("S6 MU->WDC (yarıiletken+donanım öncüler)", "WDC", 3, sorted(set(yar + don)), "MU")
    gp6b = genis_plasebo("S6 MU->WDC (120 rastgele ilgisiz hisse + MU)", "WDC", 3, rast + ["MU"], "MU")
    gh6 = genis_hedef("S6 MU->WDC", hg("MU"), sorted(set(yar + don)), 3, "WDC")
    # ters yön
    ekle("S6 MU->WDC", "2 ters yön", "WDC -> MU (h=3, arındırılmış)", deg(ll_sig(hg("WDC"))[0], ileri("MU", 3, hedge="SPY"), o.maliyet_serisi("MU") / 1e4, 3))
    # S2 ile çakışma
    hi, lo_, cl = o.panel("high", yar), o.panel("low", yar), o.panel("close", yar)
    ibs = ((cl - lo_) / (hi - lo_)).where(hi > lo_)
    S2 = ((ibs < 0.2) & cl.notna()).astype(float).mul((VIX.reindex(cl.index) > 20).astype(float), axis=0)
    s2gun = S2.sum(axis=1) > 0
    s2pnl = o.havuz_gunluk(S2, 1)
    ekle("S6 MU->WDC", "8 S2 çakışma", "S2 sinyali olan günler", deg(sig6, f6, c6, 3, mask=s2gun))
    ekle("S6 MU->WDC", "8 S2 çakışma", "S2 sinyali OLMAYAN günler", deg(sig6, f6, c6, 3, mask=~s2gun))
    ekle("S6 MU->WDC", "8 S2 çakışma", "AL bacağı, S2 sinyali olmayan günler", deg(sig6.clip(lower=0), f6, c6, 3, mask=~s2gun))
    okk = f6.notna() & (sig6 != 0)
    s6abn = (sig6 * (f6 - f6[f6.notna()].mean()))[okk]
    ort = pd.concat([s6abn, s2pnl], axis=1, keys=["s6", "s2"]).dropna()
    NOTLAR.append(f"S6-S2 çakışma: S6 işlem günlerinin %{s2gun.reindex(s6abn.index).mean() * 100:.0f}'inde S2 de açık (S6 AL günlerinde %"
                  f"{s2gun.reindex(sig6[sig6 > 0].index).mean() * 100:.0f}, SAT günlerinde %{s2gun.reindex(sig6[sig6 < 0].index).mean() * 100:.0f}); "
                  f"ortak günlerde işlem getirisi korelasyonu {ort.s6.corr(ort.s2):.2f} (n {len(ort)}); S6 işlemlerinin %{(VIX.reindex(s6abn.index) > 20).mean() * 100:.0f}'i VIX>20'de")
    # ---- S7
    log("S7")
    p7 = oncu_sozluk(["ZC=F", "ZW=F", "ZS=F", "ZM=F", "CL=F", "HO=F", "GC=F", "HG=F", "SB=F", "KC=F", "NG=F", "DBA", "SOYB", "CORN", "XLE", "XLP", "TLT"])
    for hed, es in (("BG", "ADM"), ("ADM", "BG")):
        pp = dict(p7)
        pp[f"{hed} kendi getirisi (momentum)"] = hg(hed)
        pp[f"{es} getirisi"] = hg(es)
        ll_testler(f"S7 ZL->{hed}", hg("ZL=F"), hed, 1, True, pp, diger_hedge=("XLP",))
    tar = [s for s in o.grup("h_temel_tuketim")] + [s for s in ("DAR", "INGR", "CTVA", "DE", "AGCO", "MOS", "NTR", "CF", "VLO", "MPC", "PSX", "XOM", "REX", "GPRE", "AGRO") if s in VAR]
    gh7 = genis_hedef("S7 ZL->BG", hg("ZL=F"), sorted(set(tar)), 1, "BG")
    # OOS'ta ZL -> tüm hedefler (yeni rejim iddiası yalnız BG/ADM'ye mi özgü?)
    # ---- S3, S4
    log("S3")
    g3, S3 = grup_testler("S3 sigorta-borsa SAT", "h_sigorta_borsa", "Z5_SAT_VIX", 1.5, 2, "KIE")
    for adg, liste in (("sigorta (PGR ALL AIG MET PRU CB TRV)", ["PGR", "ALL", "AIG", "MET", "PRU", "CB", "TRV"]),
                       ("borsa/veri (ICE CME NDAQ CBOE SPGI MCO MSCI)", ["ICE", "CME", "NDAQ", "CBOE", "SPGI", "MCO", "MSCI"])):
        ll = [s for s in liste if s in S3.columns]
        ekle("S3 sigorta-borsa SAT", "2 alt grup", adg, gdeg(S3[ll], gpanel(ll, 2), pd.DataFrame({s: o.maliyet_serisi(s) for s in ll}).fillna(20.0) / 1e4, 2))
    log("S4")
    g4, S4 = grup_testler("S4 temel tüketim AL", "h_temel_tuketim", "Z1_AL_ALT200", 1.5, 1, "XLP")
    # ---- ek adaylar
    log("ek adaylar")
    tek_testler("EK IYR z5 SAT alt200", "IYR", "Z5_SAT_ALT200", 1.5, 2)
    tek_testler("EK EWJ IBS AL üst200", "EWJ", "IBS_AL_UST200", 0.2, 1)
    # ---- veri denetimi: hedeflerin en büyük günlük hareketleri
    for s in ("VLO", "PBF", "WDC", "BG", "ADM", "MU"):
        r = o.basit_getiri([s])[s].dropna()
        e = r.abs().sort_values(ascending=False).head(4)
        NOTLAR.append(f"veri {s}: en büyük |günlük getiri| " + ", ".join(f"{d.date()} {r[d] * 100:+.0f}%" for d in e.index))
    for ad, sg, ff in (("S5", sig5, f5), ("S6", sig6, f6), ("S8", sig8, f8)):
        ok = ff.notna() & (sg != 0)
        e = (sg * ff)[ok].sort_values(ascending=False).head(6)
        NOTLAR.append(f"{ad} en iyi 6 işlem: " + ", ".join(f"{d.date()} {v * 100:+.0f}%" for d, v in e.items()))
    NOTLAR.append(f"crack son 5 gün $/varil: " + ", ".join(f"{d.date()} {v:.1f}" for d, v in crack.tail(5).items()) + f" | VIX son {VIX.iloc[-1]:.1f}")
    ct = coklu_test()

    T = pd.DataFrame(ROWS)
    P = pd.DataFrame(PLAS)
    T.to_csv(os.path.join(CIKTI, "testler.csv"), index=False)
    P.to_csv(os.path.join(CIKTI, "plasebo.csv"), index=False)
    pd.DataFrame(YIL).to_csv(os.path.join(CIKTI, "yillik.csv"), index=False)
    B = pd.DataFrame(BLOK)
    B.to_csv(os.path.join(CIKTI, "donem_blok.csv"), index=False)
    pd.DataFrame(SON).to_csv(os.path.join(CIKTI, "son_gun.csv"), index=False)
    ct.to_csv(os.path.join(CIKTI, "coklu_test.csv"), index=False)
    pd.concat([gp6a, gp6b]).to_csv(os.path.join(CIKTI, "genis_plasebo_s6.csv"), index=False)
    pd.concat([gh5, gh8, gh6, gh7]).to_csv(os.path.join(CIKTI, "ayni_oncu_baska_hedef.csv"), index=False)
    pd.concat([g3, g4]).to_csv(os.path.join(CIKTI, "ayni_kural_baska_grup.csv"), index=False)

    pd.set_option("display.width", 260, "display.max_columns", 30, "display.max_rows", 2000, "display.max_colwidth", 200)
    kol = ["test", "varyant", "tum_n", "tum_abn", "tum_net", "is_t", "oos_t", "oos_abn", "son_net"]
    cikti = []
    for s in T.sinyal.unique():
        cikti.append(f"\n===== {s} =====")
        x = T[T.sinyal == s]
        reg = x[x.test == "3 regresyon"]
        cikti.append(x[x.test != "3 regresyon"][kol].to_string(index=False))
        cikti += ["   REG " + v for v in reg.varyant]
        pp = P[P.sinyal == s]
        if len(pp):
            cikti.append("-- plasebo / kıyas --")
            cikti.append(pp[kol].to_string(index=False))
    cikti.append("\n===== DÖNEM BLOKLARI =====\n" + B.to_string(index=False))
    cikti.append("\n===== ÇOKLU TEST =====\n" + ct.T.to_string())
    cikti.append("\n===== SON GÜN =====\n" + pd.DataFrame(SON).to_string(index=False))
    cikti.append("\n===== NOTLAR =====\n" + "\n".join(NOTLAR))
    open(os.path.join(CIKTI, "OZET.txt"), "w").write("\n".join(cikti))
    log("bitti; satır:", len(T), len(P))


if __name__ == "__main__":
    main()
