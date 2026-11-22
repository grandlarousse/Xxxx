"""F3 çapraz varlık: faiz, kredi, dolar, volatilite, risk iştahı, genişlik, kripto, yurt dışı -> ABD ETF'leri.

YONTEM.md bölüm 3-8'e bağlı. İstatistik ortak.py ve cift_motoru.py'den gelir (bu dosyada yeniden yazılmaz).
Bölümler (her biri ara sonucu ek/backtest/f3_capraz/ara/ altına yazar; dosya varsa yeniden hesaplamaz):
  b1 : cift_motoru sonuçlarındaki F3 satırları (ELENDİ dışı) -> çürütme testleri ve öncüye özgülük
  b2 : özel öncüler (a-i) -> donemli_test / cift_testi
  b3 : rejim tablosu (koşullu 1-3 gün getiri, isabet, oynaklık; IS / OOS / SON)
  b4 : 20.11.2026 kapanışında göstergeler ve açık koşullar
  son: sınıflandırma, çürütme, çıktı dosyaları
Kullanım: python3 kod/f3_capraz.py [b1|b2|b3|b4|son|hepsi] [--yeniden]
"""
import os
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak as o  # noqa: E402
import cift_motoru as cm  # noqa: E402

CIKTI = os.path.join(o.KOK, "ek", "backtest", "f3_capraz")
ARA = os.path.join(CIKTI, "ara")
os.makedirs(ARA, exist_ok=True)
YENIDEN = "--yeniden" in sys.argv
END3 = ["SPY", "QQQ", "IWM"]
SEK = ["XLK", "XLF", "XLI", "XLY", "XLV", "XLP", "XLU", "XLB", "XLE", "XLC", "XLRE"]
H14 = END3 + SEK
UFUK = (1, 2, 3)
KRIZ = [("2008-09-01", "2009-06-30"), ("2020-02-01", "2020-04-30")]
TK = o.takvim()


def onbellek(ad, fn):
    yol = os.path.join(ARA, ad + ".csv")
    if os.path.exists(yol) and not YENIDEN:
        return pd.read_csv(yol)
    t0 = time.time()
    df = fn()
    df.to_csv(yol, index=False)
    print(f"{ad}: {len(df)} satır, {time.time() - t0:.0f} sn", flush=True)
    return df


def seviye(s):
    return o.panel("adjclose", [s])[s]


def sv(maske):
    """Bool -> +1/0 sinyal (NYSE takvimi)."""
    return maske.reindex(TK).fillna(False).astype(float)


# ------------------------------------------------------------------------------------------------------------
# Göstergeler (hepsi t günü 16:00 ET'de bilinen; VIX ailesi 16:15 ET -> gecikmeli varyant ayrıca)
# ------------------------------------------------------------------------------------------------------------
_G = {}


def gostergeler():
    if _G:
        return _G
    vix, v3, v9 = seviye("^VIX"), seviye("^VIX3M"), seviye("^VIX9D")
    lv = np.log(vix)
    sd = lv.diff().rolling(60, min_periods=40).std().shift(1)
    _G["vix"] = vix
    _G["vix_vix3m"] = vix / v3
    _G["vix9d_vix"] = v9 / vix
    _G["vix_z5"] = (lv - lv.shift(5)) / (sd * np.sqrt(5))
    hyg = np.log(seviye("HYG"))
    h5 = hyg - hyg.shift(5)
    _G["hyg5"] = h5
    _G["hyg5_esik05"] = h5.rolling(250, min_periods=200).quantile(0.05).shift(1)
    yol = os.path.join(ARA, "genislik.csv")
    if os.path.exists(yol) and not YENIDEN:
        g = pd.read_csv(yol, parse_dates=["date"]).set_index("date")
    else:
        P = o.panel("adjclose", o.abd_semboller("EQUITY"))
        ma = P.rolling(20, min_periods=20).mean()
        mn = P.rolling(20, min_periods=20).min()
        ok = ma.notna() & P.notna()
        k = ok.sum(axis=1)
        g = pd.DataFrame({"ust20_oran": ((P > ma) & ok).sum(axis=1) / k,
                          "yenidip20_oran": ((P <= mn) & ok).sum(axis=1) / k, "n_hisse": k})
        g.loc[g.n_hisse < 100, ["ust20_oran", "yenidip20_oran"]] = np.nan
        g.index.name = "date"
        g.to_csv(yol)
    _G["ust20"] = g["ust20_oran"].reindex(TK)
    _G["yenidip"] = g["yenidip20_oran"].reindex(TK)
    _G["yenidip_esik95"] = _G["yenidip"].rolling(250, min_periods=200).quantile(0.95).shift(1)
    _G["n_hisse"] = g["n_hisse"].reindex(TK)
    tnx = seviye("^TNX").ffill(limit=3)
    _G["tnx"] = tnx
    _G["tnx_fark"] = tnx.diff()  # yüzde puan (0,10 = 10 bp)
    return _G


def kosullar():
    """Seviye / olay sinyalleri (AL = +1). kaynak: hipotez dosyası, görev tanımı ya da keşif (ajan seçimi)."""
    g = gostergeler()
    k = {
        "VIX>20": (g["vix"] > 20, "gorev"),
        "VIX>25": (g["vix"] > 25, "gorev"),
        "VIX>30": (g["vix"] > 30, "gorev"),
        "VIX>35": (g["vix"] > 35, "gorev"),
        "VIX_z5>=2": (g["vix_z5"] >= 2, "gorev"),
        "VIX/VIX3M>1": (g["vix_vix3m"] > 1, "hipotez"),
        "VIX9D/VIX>1.1": (g["vix9d_vix"] > 1.1, "hipotez"),
        "HYG5_alt%5": (g["hyg5"] <= g["hyg5_esik05"], "gorev"),
        "GENISLIK<%20": (g["ust20"] < 0.20, "gorev"),
        "GENISLIK<%10": (g["ust20"] < 0.10, "gorev"),
        "YENIDIP_ust%5": (g["yenidip"] >= g["yenidip_esik95"], "kesif"),
    }
    return {a: (sv(m), kay) for a, (m, kay) in k.items()}


HEDEF_KOSUL = {
    "VIX>20": H14, "VIX>25": H14, "VIX>30": H14, "VIX>35": H14, "VIX_z5>=2": H14,
    "VIX/VIX3M>1": H14 + ["SOXX", "SMH"], "VIX9D/VIX>1.1": ["SPY", "QQQ"],
    "HYG5_alt%5": H14 + ["KRE"], "GENISLIK<%20": END3, "GENISLIK<%10": END3, "YENIDIP_ust%5": END3,
}


def bolum_say(sig, bosluk=5, bas=None, bit=None):
    """Bağımsız olay (dönem) sayısı: aralarında > bosluk işlem günü olan sinyal kümeleri."""
    s = sig.fillna(0.0)
    if bas:
        s = s[s.index >= bas]
    if bit:
        s = s[s.index <= bit]
    p = np.where(s.values != 0)[0]
    return int(0 if len(p) == 0 else 1 + (np.diff(p) > bosluk).sum())


def tek_test(sig, hedef, h, bilgi, hedge=None, gecikmeli=False):
    sig = sig.reindex(TK).fillna(0.0)
    d = o.donemli_test(sig, hedef, h, hedge=hedge)
    if d.get("tum_n", 0) < 30:
        return None
    row = {**bilgi, "havuz": "tek hedef", "bayat_isaret": hedef in o.bayat_hedefler()}
    row.update(d)
    row.update(o.son_sinyal(sig))
    if cm._on_eleme(d):
        row.update(o.ek_olcutler(sig, hedef, h, hedge=hedge))
    if gecikmeli:
        e = o.donemli_test(sig.shift(1).fillna(0.0), hedef, h, hedge=hedge)
        row.update({"gec1_" + c: e.get(c) for c in ("tum_anormal_net_bps", "is_t_anormal", "oos_t_anormal", "son_net_bps")})
    if hedef != "SPY":
        e = o.donemli_test(sig, hedef, h, hedge="SPY")
        row.update({"spyarin_" + c: e.get(c) for c in ("tum_anormal_net_bps", "is_t_anormal", "oos_t_anormal")})
    return row


# ------------------------------------------------------------------------------------------------------------
# Öncü serileri (cift_testi'ye x olarak)
# ------------------------------------------------------------------------------------------------------------
def ozel_x():
    hz = o.hizali_getiri
    hyg, ief = hz("HYG"), hz("IEF")
    x = {
        "HYG-IEF_artik": hyg - o.kayan_beta(hyg, ief) * ief,
        "^TNX_fark": gostergeler()["tnx_fark"],
        "SPHB-SPLV": hz("SPHB") - hz("SPLV"),
        "IWM-SPY": hz("IWM") - hz("SPY"),
        "XLY-XLP": hz("XLY") - hz("XLP"),
        "RSP-SPY": hz("RSP") - hz("SPY"),
        "CPER-GLD": hz("CPER") - hz("GLD"),
    }
    return {k: v.reindex(TK) for k, v in x.items()}


# (oncu_etiket, gerçek_öncü, hedefler, yön, kaynak)
CIFT_GRUP = [
    ("HYG-IEF_artik", "HYG", ["BX", "KKR", "APO", "ARES"], "+", "hipotez"),
    ("HYG-IEF_artik", "HYG", ["SPY", "IWM", "XLF", "KRE"], "+", "gorev"),
    ("TLT", "TLT", ["XLU", "XLRE", "ITB", "XHB", "KRE", "XLF", "IGV", "XBI"], "+", "gorev"),
    ("^TNX_fark", "^TNX", ["XLU", "XLRE", "ITB", "XHB", "KRE", "XLF", "IGV", "XBI"], "-", "gorev"),
    ("UUP", "UUP", ["GLD", "GDX", "EEM", "XLP", "XLB"], "-", "gorev"),
] + [(sp, sp.split("-")[0], END3 + ["XLY", "XLI", "XLF", "XLB", "XLE"], "+", "gorev")
     for sp in ("SPHB-SPLV", "IWM-SPY", "XLY-XLP", "RSP-SPY", "CPER-GLD")] + [
    (c, c, ["COIN", "MSTR", "MARA", "RIOT", "CLSK", "IREN"], "-", "hipotez") for c in ("IBIT", "BITO", "GBTC")]


def uup_z5():
    x = o.hizali_getiri("UUP")
    sd = x.rolling(60, min_periods=40).std().shift(1)
    return x.rolling(5).sum() / (sd * np.sqrt(5))


def b2_ozel():
    sat = []
    # a, b, c(kuyruk), g: seviye / olay sinyalleri
    for ad, (sig, kay) in kosullar().items():
        vixmi = ad.startswith("VIX")
        nb = {"n_bolum": bolum_say(sig), "n_bolum_is": bolum_say(sig, bit=o.IS_BITIS), "n_bolum_oos": bolum_say(sig, bas=o.OOS_BAS)}
        for hd in HEDEF_KOSUL[ad]:
            for h in UFUK:
                bilgi = {"aile": "F3", "sinyal_id": f"{ad}|{hd}|SEVIYE|+|h{h}", "oncu": ad, "hedef": hd, "bicim": "SEVIYE",
                         "yon": "+", "h": h, "kaynak": kay, **nb}
                r = tek_test(sig, hd, h, bilgi, gecikmeli=vixmi)
                if r:
                    sat.append(r)
    # UUP 5 günlük z > 2 -> SAT (hipotez)
    z = uup_z5()
    sig = -sv(z >= 2)
    for hd in ["EEM", "GDX", "XLB"]:
        for h in UFUK:
            bilgi = {"aile": "F3", "sinyal_id": f"UUP_z5>=2|{hd}|OLAY|-|h{h}", "oncu": "UUP_z5>=2", "hedef": hd, "bicim": "OLAY",
                     "yon": "-", "h": h, "kaynak": "hipotez", "n_bolum": bolum_say(sig)}
            r = tek_test(sig, hd, h, bilgi)
            if r:
                sat.append(r)
    # c, d, e, f, h: öncü -> hedef çiftleri (B1, B1r, B3; B2 'artık dönüşü' cift_motoru'nda ölçüldü, burada yok)
    X = ozel_x()
    for et, gercek, hedefler, yon, kay in CIFT_GRUP:
        x = X.get(et)
        for hd in hedefler:
            if hd not in o.meta().index:
                continue
            try:
                rows = cm.cift_testi(gercek, hd, yon, x=x, etiket=et, bicimler=("B1", "B1r", "B3"))
            except Exception as e:  # noqa: BLE001
                print("HATA", et, hd, type(e).__name__, str(e)[:80], flush=True)
                continue
            for r in rows:
                r.update({"aile": "F3", "kaynak": kay, "sinyal_id": f"{et}|{hd}|{r['bicim']}|{yon}|h{r['h']}"})
                sat.append(r)
    return pd.DataFrame(sat)


# ------------------------------------------------------------------------------------------------------------
# Sinyalin yeniden kurulması (çürütme testleri için)
# ------------------------------------------------------------------------------------------------------------
def sinyal_kur(row, X=None):
    """Dönen (sinyal, hedge, z). z: sınır sinyali / eşik testi için (yoksa None)."""
    b, hd, yon, on = row["bicim"], row["hedef"], row["yon"], row["oncu"]
    if b == "SEVIYE":
        return kosullar()[on][0], None, None
    if b == "OLAY":
        z = uup_z5()
        return -sv(z >= 2), None, None
    X = X or {}
    x = X.get(on)
    if x is None:
        x = o.hizali_getiri(on)
    rr = o.basit_getiri([hd, "SPY"])
    r, spy = rr[hd], rr["SPY"]
    x = x.reindex(r.index)
    gercek = on.split("-")[0].replace("_fark", "").replace("_artik", "")
    s = cm.sinyaller(x, r, yon, spy if (gercek != "SPY" and hd != "SPY") else None)
    sig, hedge = s[b]
    if b == "B1":
        z = o.zskor(x, 60)
    elif b == "B1r":
        z = o.zskor(x - o.kayan_beta(x, spy) * spy, 60)
    elif b == "B3":
        z = x.rolling(3).sum() / (x.rolling(60, min_periods=40).std().shift(1) * np.sqrt(3))
    else:
        z = o.zskor(r - o.kayan_beta(r, x) * x, 60)
    return sig, hedge, z


def kontrol_t(sig, hedef, h):
    """Öncüye özgülük (hedefin kendi gecikmesi ve SPY kontrolü): ileri getiri ~ sinyal + z(r_hedef) + z(5g r_hedef)
    + z(r_SPY). HAC (düz, gecikme h-1) t'si, tüm / IS / OOS. Uyarı: 1. dalgada HYG->SPY ve VIX->SPY etkisi SPY'ın
    kendi dönüşünden geliyordu; bu regresyon onu ayırır."""
    import statsmodels.api as sm

    f = o._ileri(hedef, h, "kapanis")
    rr = o.basit_getiri([hedef, "SPY"])
    r = rr[hedef]
    sd = r.rolling(60, min_periods=40).std().shift(1)
    d = pd.DataFrame({"f": f, "s": sig.reindex(f.index).fillna(0.0), "zr": o.zskor(r, 60),
                      "z5": r.rolling(5).sum() / (sd * np.sqrt(5))})
    if hedef != "SPY":
        d["zs"] = o.zskor(rr["SPY"], 60)
    d = d.dropna()
    is_bit, oos_bas = o.donem_sinirlari(hedef)
    out = {}
    for ad, m in (("tum", slice(None)), ("is", d.index <= is_bit), ("oos", d.index >= oos_bas)):
        e = d.loc[m]
        if len(e) < 250 or (e.s != 0).sum() < 20:
            out[f"kontrol_t_{ad}"] = np.nan
            continue
        X = sm.add_constant(e.drop(columns="f").clip(-5, 5))
        kw = {"maxlags": max(h - 1, 0), "kernel": "uniform" if h > 1 else "bartlett"}
        mm = sm.OLS(e["f"], X).fit(cov_type="HAC", cov_kwds=kw)
        out[f"kontrol_t_{ad}"] = round(float(mm.tvalues["s"]), 2)
        out[f"kontrol_b_{ad}_bps"] = round(float(mm.params["s"]) * 1e4, 1)
    return out


def curut(sig, hedef, h, hedge=None, z=None):
    """YONTEM.md bölüm 7 testleri (10: 5 dakikalık veri yok; 12: B2 yok)."""
    sig = sig.reindex(TK).fillna(0.0)
    out = {}

    def t(s, onek, **kw):
        d = o.islem_testi(s.reindex(TK).fillna(0.0), hedef, h, hedge=kw.pop("hedge", hedge), **kw)
        out[onek + "_n"] = d.get("n")
        out[onek + "_bps"] = d.get("anormal_net_bps")
        out[onek + "_t"] = d.get("t_anormal")
        return d

    t(sig, "c1_acilis", giris="acilis")                          # 1 giriş gecikmesi
    t(sig, "c1_ertesi", giris="ertesi")
    if z is not None:                                            # 2 eşik 1,5
        t(sig.where(z.reindex(TK).abs() >= 1.5, 0.0), "c2_z15")
    t(sig, "c2_maliyet2x", maliyet_bps=2 * o.maliyet_serisi(hedef))
    yt = o.yillik_tablo(sig, hedef, h)                           # 3 en iyi yıl hariç
    if len(yt):
        eny = int(yt["toplam_yuzde"].idxmax())
        out["c3_en_iyi_yil"] = eny
        t(sig.where(sig.index.year != eny, 0.0), "c3_eniyiyil_haric")
        out["c3_yil_pozitif"] = f"{int((yt.net_bps > 0).sum())}/{len(yt)}"
    if hedge is None and hedef != "SPY":                         # 4 piyasadan arındırma
        t(sig, "c4_spyarin", hedge="SPY")
    vix = gostergeler()["vix"].reindex(TK)                       # 6 rejim
    t(sig.where(vix > 20, 0.0), "c6_vix_ust20")
    t(sig.where(vix <= 20, 0.0), "c6_vix_alt20")
    c = seviye(hedef).reindex(TK)
    ust = c > c.rolling(200, min_periods=200).mean()
    t(sig.where(ust, 0.0), "c6_sma200_ust")
    t(sig.where(~ust, 0.0), "c6_sma200_alt")
    t(sig.shift(1), "c7_oncu_gec1")                              # 7 öncü 1 gün gecikmeli
    f = o._ileri(hedef, h, "kapanis", hedge)                     # 8 en büyük 20 işlem
    r = o.basit_getiri([hedef])[hedef]
    mx = pd.concat([r.shift(-k).abs() for k in range(1, h + 1)], axis=1).max(axis=1)
    akt = (sig != 0) & f.notna()
    tr = (sig * f)[akt]
    top = tr.abs().sort_values(ascending=False).index[:20]
    out["c8_buyuk20_ort_bps"] = round(float(tr.loc[top].mean()) * 1e4, 1)
    out["c8_buyuk20_bozuk"] = int((mx.loc[top] > (0.4 if o.meta().loc[hedef, "tur"] == "ETF" else 0.8)).sum())
    out["c8_buyuk20_tarih"] = ";".join(str(d.date()) for d in sorted(top)[:20])
    if z is not None:                                            # 9 sınır sinyalleri hariç
        zz = z.reindex(TK).abs()
        t(sig.where(~((zz >= 1.0) & (zz < 1.2)), 0.0), "c9_sinir_haric")
    s11 = sig.copy()                                             # 11 kriz hariç
    for a, b in KRIZ:
        s11[(s11.index >= a) & (s11.index <= b)] = 0.0
    t(s11, "c11_kriz_haric")
    out.update(kontrol_t(sig, hedef, h))
    return out


# ------------------------------------------------------------------------------------------------------------
# Bölüm 1: cift_motoru F3 sonuçları
# ------------------------------------------------------------------------------------------------------------
def b1_cift():
    yol = os.path.join(o.KOK, "ek", "backtest", "cift", "sonuclar.csv")
    d = pd.read_csv(yol, low_memory=False)
    f = d[d.aile == "F3"].copy()
    ozet = {"f3_test": len(f), "f3_hipotez_testi": int((f.bicim != "B1r").sum()), "sinif": f.sinif.value_counts().to_dict()}
    print("cift F3:", ozet, flush=True)
    ak = f[f.sinif != "ELENDI"].copy()
    sat = []
    for _, row in ak.iterrows():
        sig, hedge, z = sinyal_kur(row)
        rr = row.to_dict()
        rr["kaynak"] = "cift_motoru"
        rr["sinyal_id"] = f"{row.oncu}|{row.hedef}|{row.bicim}|{row.yon}|h{row.h}"
        rr.update(curut(sig, row.hedef, int(row.h), hedge, z))
        sat.append(rr)
    out = pd.DataFrame(sat)
    out.attrs["ozet"] = ozet
    pd.Series({k: str(v) for k, v in ozet.items()}).to_csv(os.path.join(ARA, "b1_cift_ozet.csv"))
    return out


# ------------------------------------------------------------------------------------------------------------
# Bölüm 3: rejim tablosu (betimsel; brüt ileri getiri, maliyetsiz)
# ------------------------------------------------------------------------------------------------------------
def b3_rejim():
    K = {a: s for a, (s, _) in kosullar().items() if a not in ("YENIDIP_ust%5",)}
    hed = H14
    sat = []
    for h in UFUK:
        F = o.ileri_getiri(hed, h)
        for ad, s in K.items():
            m = s.reindex(F.index).fillna(0.0) != 0
            for dn, b, e in (("IS", None, o.IS_BITIS), ("OOS", o.OOS_BAS, None), ("SON", o.SON_BAS, None)):
                idx = F.index
                pm = pd.Series(True, index=idx)
                if b:
                    pm &= idx >= b
                if e:
                    pm &= idx <= e
                nb = bolum_say(s, bas=b, bit=e)
                for hd in hed:
                    f = F[hd][pm & F[hd].notna()]
                    fk = f[m.reindex(f.index)]
                    if len(f) < 100:
                        continue
                    sat.append({"kosul": ad, "hedef": hd, "h": h, "donem": dn, "n_gun": len(fk), "n_bolum": nb,
                                "ort_kosul_bps": round(fk.mean() * 1e4, 1) if len(fk) else np.nan,
                                "ort_kosulsuz_bps": round(f.mean() * 1e4, 1),
                                "isabet_kosul": round((fk > 0).mean(), 3) if len(fk) else np.nan,
                                "isabet_kosulsuz": round((f > 0).mean(), 3),
                                "std_kosul_bps": round(fk.std() * 1e4, 1) if len(fk) > 2 else np.nan,
                                "std_kosulsuz_bps": round(f.std() * 1e4, 1),
                                "medyan_kosul_bps": round(fk.median() * 1e4, 1) if len(fk) else np.nan})
    df = pd.DataFrame(sat)
    df["fark_bps"] = (df.ort_kosul_bps - df.ort_kosulsuz_bps).round(1)
    df["oynaklik_kat"] = (df.std_kosul_bps / df.std_kosulsuz_bps).round(2)
    return df


# ------------------------------------------------------------------------------------------------------------
# Bölüm 4: 20.11.2026 kapanışı
# ------------------------------------------------------------------------------------------------------------
def b4_son():
    g = gostergeler()
    son = TK[-1]
    sat = [{"gosterge": k, "deger": round(float(v.reindex(TK).loc[son]), 4) if pd.notna(v.reindex(TK).loc[son]) else np.nan}
           for k, v in g.items()]
    for ad, (s, _) in kosullar().items():
        sat.append({"gosterge": "KOSUL " + ad, "deger": float(s.loc[son]),
                    "son_10_gun": "g" + "".join(str(int(v)) for v in s.iloc[-10:].values),
                    "acik_gun_ardisik": int((s.iloc[::-1].cumprod()).sum())})
    for ad, x in ozel_x().items():
        sat.append({"gosterge": "z60 " + ad, "deger": round(float(o.zskor(x, 60).loc[son]), 2)})
    for s_ in ("TLT", "UUP", "IBIT", "BITO", "GBTC", "HYG", "IEF"):
        sat.append({"gosterge": "z60 " + s_, "deger": round(float(o.zskor(o.hizali_getiri(s_), 60).loc[son]), 2)})
    sat.append({"gosterge": "z5 UUP", "deger": round(float(uup_z5().loc[son]), 2)})
    df = pd.DataFrame(sat)
    df.insert(0, "tarih", str(son.date()))
    return df


# ------------------------------------------------------------------------------------------------------------
# Son: sınıflandırma ve çıktılar
# ------------------------------------------------------------------------------------------------------------
SUTUN_ON = ["aile", "sinyal_id", "kaynak", "oncu", "hedef", "bicim", "yon", "h", "havuz", "bayat_isaret"]


def son_adim():
    b2 = onbellek("b2_ozel", b2_ozel)
    b2 = b2[b2.bicim.notna()].copy()
    # öncüye özgülük: cift satırları cift_motoru.etiketle mantığı (B1r IS ve OOS t >= 2,0); seviye satırları SPY'dan
    # arındırılmış aynı test (IS ve OOS t >= 2,0); SPY hedefinde arındırma yok -> kontrol regresyonu (aşağıda)
    b2 = cm.etiketle(b2)
    sev = b2.bicim.isin(["SEVIYE", "OLAY"])
    b2.loc[sev, "ozgu"] = (pd.to_numeric(b2.loc[sev, "spyarin_is_t_anormal"], errors="coerce") >= 2.0) & \
                          (pd.to_numeric(b2.loc[sev, "spyarin_oos_t_anormal"], errors="coerce") >= 2.0)
    b2 = o.siniflandir(b2, aile_sutunu="aile")
    ak = b2[b2.sinif != "ELENDI"].copy()
    X = ozel_x()
    cur = []
    for _, row in ak.iterrows():
        sig, hedge, z = sinyal_kur(row, X)
        cur.append(curut(sig, row.hedef, int(row.h), hedge, z))
    ak = pd.concat([ak.reset_index(drop=True), pd.DataFrame(cur)], axis=1)
    print("ELENDİ dışı (özel öncüler):", len(ak), flush=True)
    for c in ("kontrol_t_is", "kontrol_t_oos"):
        if c not in ak.columns:
            ak[c] = np.nan
    spy_sev = ak.bicim.isin(["SEVIYE", "OLAY"]) & (ak.hedef == "SPY")
    ak.loc[spy_sev, "ozgu"] = (ak.loc[spy_sev, "kontrol_t_is"] >= 2.0) & (ak.loc[spy_sev, "kontrol_t_oos"] >= 2.0)
    b1 = onbellek("b1_cift", b1_cift)
    b1["kaynak"] = "cift_motoru"
    ak = pd.concat([ak, b1], ignore_index=True, sort=False)
    sira = {"SAGLAM": 0, "KOSULLU": 1, "IZLE": 2}
    ak["_s"] = ak.sinif.map(sira)
    ak = ak.sort_values(["_s", "oos_t_anormal"], ascending=[True, False]).drop(columns="_s")
    on = [c for c in SUTUN_ON if c in b2.columns]
    b2 = b2[on + [c for c in b2.columns if c not in on]]
    b2.to_csv(os.path.join(CIKTI, "sonuclar.csv"), index=False)
    kos = ["k_A", "k_B", "k_B_zayif", "bh_oos", "k_C", "k_D", "k_E", "k_F", "k_G", "k_H", "k_I"]
    ana = on + ["tum_n", "oos_n", "tum_anormal_net_bps", "is_t_anormal", "oos_t_anormal", "son_net_bps", "son_n",
                "tum_net_bps_ust10_haric", "tum_t_ust10_haric", "yil_pozitif_oran", "plasebo_p", "acilis_anormal_bps",
                "acilis_net_bps", "ozgu", "n_bolum", "n_bolum_oos", "gec1_tum_anormal_net_bps", "gec1_is_t_anormal",
                "gec1_oos_t_anormal", "spyarin_is_t_anormal", "spyarin_oos_t_anormal"] + kos + ["sinif", "son_gun", "son_sinyal"]
    ana = [c for c in dict.fromkeys(ana) if c in ak.columns]
    ak = ak[ana + [c for c in ak.columns if c.startswith(("c1_", "c2_", "c3_", "c4_", "c6_", "c7_", "c8_", "c9_", "c11_", "kontrol_"))]]
    ak.to_csv(os.path.join(CIKTI, "ayakta_kalanlar.csv"), index=False)
    # Bilgi amaçlı (sınıf almaz): eşiğe yakın adaylar (IS t >= 1,5 ve OOS t >= 1,0) çürütme testleriyle;
    # ters yönde tutarlı olanlar (IS t <= -2,5 ve OOS t <= -2,0; YONTEM.md bölüm 6: raporlanır, sınıflandırılmaz)
    yak = b2[(b2.is_t_anormal >= 1.5) & (b2.oos_t_anormal >= 1.0) & (b2.bicim != "B1r")].copy()
    cur = []
    for _, row in yak.iterrows():
        sig, hedge, z = sinyal_kur(row, X)
        cur.append(curut(sig, row.hedef, int(row.h), hedge, z))
    yak = pd.concat([yak.reset_index(drop=True), pd.DataFrame(cur)], axis=1)
    yak[[c for c in ana if c in yak.columns] + [c for c in pd.DataFrame(cur).columns]].to_csv(
        os.path.join(CIKTI, "yakin_adaylar.csv"), index=False)
    ters = b2[(b2.is_t_anormal <= -2.5) & (b2.oos_t_anormal <= -2.0)]
    ters[[c for c in ana if c in ters.columns]].to_csv(os.path.join(CIKTI, "ters_yon.csv"), index=False)
    print("yakın aday:", len(yak), "ters yönde tutarlı:", len(ters))
    hip = b2[b2.bicim != "B1r"]
    print("TEST:", len(b2), "hipotez testi:", len(hip), "B1r:", (b2.bicim == "B1r").sum(), "keşif:", (hip.kaynak == "kesif").sum())
    print("Beklenen yanlış pozitif: SAĞLAM %.3f KOŞULLU %.3f" % (len(hip) * o.P_SIFIR_SAGLAM, len(hip) * o.P_SIFIR_KOSULLU))
    print(b2.groupby("bicim").sinif.value_counts().unstack(fill_value=0).to_string())
    print("k_A:", int(b2.k_A.sum()), "k_A&k_B_zayif:", int((b2.k_A & b2.k_B_zayif).sum()), "k_A&k_B:", int((b2.k_A & b2.k_B).sum()),
          "BH:", int((b2.k_A & b2.bh_oos).sum()))
    return b2, ak


if __name__ == "__main__":
    ne = [a for a in sys.argv[1:] if not a.startswith("--")] or ["hepsi"]
    if ne[0] in ("b2", "hepsi"):
        onbellek("b2_ozel", b2_ozel)
    if ne[0] in ("b1", "hepsi"):
        onbellek("b1_cift", b1_cift)
    if ne[0] in ("b3", "hepsi"):
        r = onbellek("b3_rejim", b3_rejim)
        r.to_csv(os.path.join(CIKTI, "rejim_tablosu.csv"), index=False)
    if ne[0] in ("b4", "hepsi"):
        s = onbellek("b4_son", b4_son)
        s.to_csv(os.path.join(CIKTI, "son_degerler.csv"), index=False)
    if ne[0] in ("son", "hepsi"):
        son_adim()
