"""F1 emtia -> hisse/ETF öncülüğü ve emtia araçlarının kendi düzenleri (YONTEM.md bölüm 4-8).

Çalıştırma: python3 kod/f1_emtia.py            (ara sonuçlar varsa yeniden kullanır)
            python3 kod/f1_emtia.py --yeniden  (her şeyi baştan hesaplar)
Çıktı    : ek/backtest/f1_emtia/{sonuclar.csv, ayakta_kalanlar.csv, curutme.csv, yillik.csv, yeni_rejim.csv}

İstatistik ortak.py ve cift_motoru.py'den gelir; bu betik yalnız öncü serilerini ve sinyalleri kurar.
aile sütunu: 'F1' = önceden yazılı hipotez testi (sayılır), 'F1_kontrol' = gecikmeli öncü / ETF öncü kıyası
(sayılmaz, sınıf yorumlanmaz), 'F1_kesif' = yöntem dışı ek varyant (sayılır, ayrıca işaretli).
"""
import os
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak as o  # noqa: E402
import cift_motoru as cm  # noqa: E402

CIKTI = os.path.join(o.KOK, "ek", "backtest", "f1_emtia")
ARA = os.path.join(CIKTI, "ara")
KRIZ = [("2008-09-01", "2009-06-30"), ("2020-02-01", "2020-04-30")]
VADELI_ETF = {"CL=F": "USO", "BZ=F": "BNO", "NG=F": "UNG", "GC=F": "GLD", "SI=F": "SLV", "HG=F": "CPER",
              "ZS=F": "SOYB", "ZC=F": "CORN", "ZW=F": "WEAT", "SB=F": "CANE", "RB=F": "UGA", "PL=F": "PPLT",
              "PA=F": "PALL"}
RAFINERI = ["VLO", "MPC", "PSX", "PBF", "DK", "DINO", "PARR", "CVI"]
TANKER = ["FRO", "DHT", "STNG", "INSW"]
ZIRVE_HEDEF = ["GLD", "SLV", "USO", "UNG", "DBA", "DBC", "CPER", "DBB", "PPLT", "PALL", "URA"]
T0 = time.time()

XREG = {}   # öncü etiketi -> (x serisi, vadeli mi)
REG = {}    # (oncu, hedef, bicim, yon) -> {"sig": Series ya da DataFrame, "z": Series ya da None, "lag": ..., "giris": ...}


def log(*a):
    print(f"[{time.time() - T0:6.0f}s]", *a, flush=True)


def hizala(r):
    """Kendi takvimindeki seviye farkını NYSE gününe hizalar (hizali_getiri'nin eşleme kuralı: o gün ya da sonraki ilk
    NYSE günü; yerel tatil = 0). Gecikme 0 (vadeliler, tahıllar: YONTEM.md bölüm 3)."""
    r = r.dropna()
    tam, tk = o.oku("SPY").index, o.takvim()
    pos = tam.searchsorted(r.index, side="left")
    ok = pos < len(tam)
    s = pd.Series(r.values[ok], index=tam[pos[ok]]).groupby(level=0).sum().reindex(tk)
    ilk = r.index.min()
    s[s.index < ilk] = np.nan
    return s.where(s.notna() | (s.index < ilk), 0.0)


def seviye(semboller):
    d = pd.concat({s: o.oku(s)["close"] for s in semboller}, axis=1).dropna()
    return d


def sid(r):
    return f"{r.get('grup', '')}:{r['oncu']}>{r['hedef']}:{r['bicim']}:{r['yon']}:h{r['h']}:{r.get('giris', 'kapanis')}"


# ---------------------------------------------------------------- sinyal üretimi (cift_motoru.sinyaller ile aynı) ---
_SCACHE = {}


def cift_sinyal(etiket, x, hedef, yon, bicim, lag=0):
    """cift_motoru.sinyaller çıktısı + sınır denetimi için aynı z. Dönen (sig, z, hedge)."""
    key = (etiket, hedef, yon, lag)
    if key not in _SCACHE:
        rr = o.basit_getiri([hedef, "SPY"])
        r, spy = rr[hedef], rr["SPY"]
        xx = (x.shift(lag) if lag else x).reindex(r.index)
        s = cm.sinyaller(xx, r, yon, spy)
        z = {"B1": o.zskor(xx, 60), "B1r": o.zskor(xx - o.kayan_beta(xx, spy) * spy, 60),
             "B2": o.zskor(r - o.kayan_beta(r, xx) * xx, 60),
             "B3": xx.rolling(3).sum() / (xx.rolling(60, min_periods=40).std().shift(1) * np.sqrt(3))}
        _SCACHE[key] = (s, z)
    s, z = _SCACHE[key]
    sig, hd = s[bicim]
    return sig, z[bicim], hd


# ---------------------------------------------------------------- test sarmalayıcıları -----------------------------
def cift(etiket, hedef, yon, x, grup, vadeli=False, bicimler=("B1", "B1r", "B2", "B3"), aile="F1", gecikmeli=True):
    XREG[etiket] = (x, vadeli)
    rows = []
    for r in cm.cift_testi(etiket, hedef, yon, x=x, etiket=etiket, bicimler=bicimler):
        r.update({"aile": aile, "grup": grup, "vadeli": vadeli, "oncu_gecikme": 0})
        rows.append(r)
    if vadeli and gecikmeli:  # bölüm 3: vadeli öncü 1 gün gecikmeli de raporlanır
        XREG[etiket + "_g1"] = (x.shift(1), vadeli)
        for r in cm.cift_testi(etiket + "_g1", hedef, yon, x=x.shift(1), etiket=etiket + "_g1", bicimler=bicimler):
            r.update({"aile": "F1_kontrol", "grup": grup, "vadeli": vadeli, "oncu_gecikme": 1})
            rows.append(r)
    for r in rows:
        if "son_gun" not in r:
            sig, _, _ = cift_sinyal(r["oncu"], XREG[r["oncu"]][0], r["hedef"], yon, r["bicim"])
            r.update(o.son_sinyal(sig))
    return rows


def tek(sig, hedef, h, oncu, bicim, yon, grup, z=None, lag=None, aile="F1", giris=None):
    """Özel (getiri dışı) sinyal: donemli_test + ön elemeyi geçerse ek_olcutler; öncüye özgülük için SPY hedge'li t."""
    giris = giris or ("acilis" if hedef in o.bayat_hedefler() else "kapanis")
    d = o.donemli_test(sig, hedef, h, giris=giris)
    if d.get("tum_n", 0) < 30:
        return []
    row = {"aile": aile, "grup": grup, "oncu": oncu, "hedef": hedef, "bicim": bicim, "yon": yon, "h": h,
           "havuz": "tek hedef", "bayat_isaret": hedef in o.bayat_hedefler(), "oncu_gecikme": 0, **d}
    dr = o.donemli_test(sig, hedef, h, giris=giris, hedge="SPY")
    row.update({"spyden_ar_is_t": dr.get("is_t_anormal"), "spyden_ar_oos_t": dr.get("oos_t_anormal"),
                "spyden_ar_tum_bps": dr.get("tum_anormal_net_bps")})
    if cm._on_eleme(d):
        row.update(o.ek_olcutler(sig, hedef, h))
    row.update(o.son_sinyal(sig))
    REG[(oncu, hedef, bicim, yon)] = {"sig": sig, "z": z, "lag": lag, "giris": giris}
    return [row]


def havuz(S, ad, h, oncu, bicim, yon, grup, hedge=None, z=None, lag=None, aile="F1"):
    """Çok hedefli test (havuz_testi, gün bazlı portföy t'si). siniflandir için sütunlar eşlenir."""
    d = o.havuz_donemli(S, h, hedge=hedge)
    row = {"aile": aile, "grup": grup, "oncu": oncu, "hedef": ad, "bicim": bicim, "yon": yon, "h": h,
           "havuz": f"portföy ({S.shape[1]} hedef)", "bayat_isaret": any(c in o.bayat_hedefler() for c in S.columns),
           "oncu_gecikme": 0, **d}
    for p in ("tum", "is", "oos", "son"):
        row[f"{p}_n"] = d.get(f"{p}_n_gun", 0)
    if hedge is None:
        dr = o.havuz_donemli(S, h, hedge="SPY")
        row.update({"spyden_ar_is_t": dr.get("is_t_anormal"), "spyden_ar_oos_t": dr.get("oos_t_anormal"),
                    "spyden_ar_tum_bps": dr.get("tum_anormal_net_bps")})
    if cm._on_eleme(d):
        row.update(havuz_ek(S, h))
    s1 = S.abs().max(axis=1) * np.sign(S.sum(axis=1))
    row.update(o.son_sinyal(s1))
    REG[(oncu, ad, bicim, yon)] = {"sig": S, "z": z, "lag": lag, "giris": "kapanis", "hedge": hedge}
    return [row]


def havuz_ek(S, h):
    """Havuz için F, E, H, I yaklaşıkları: gün bazlı anormal portföy serisinden (havuz_gunluk)."""
    p = o.havuz_gunluk(S, h)
    yil = p.dropna().groupby(p.dropna().index.year)
    yt = pd.DataFrame({"n": yil.size(), "m": yil.mean()})
    yt = yt[yt.n >= 3]
    kalan = p.dropna().sort_values(ascending=False).iloc[10:]
    z2 = pd.Series(0.0, index=p.index)
    z2[kalan.index] = kalan
    ac = o.havuz_testi(S, h, giris="acilis")
    # plasebo: portföy serisinde sinyal günleri dairesel kaydırılır (ortak.plasebo_dairesel ile aynı mantık; havuz için)
    cols = [c for c in S.columns if c in o.panel("adjclose").columns]
    F = o.ileri_getiri(cols, h)
    A = (F - F.mean())
    Sx = S[cols].reindex(F.index).fillna(0.0)
    akt = (Sx != 0) & F.notna()
    port = ((Sx * A).where(akt).sum(axis=1) / akt.sum(axis=1)).where(akt.sum(axis=1) > 0)
    yon_gun = np.sign(Sx.sum(axis=1))
    a_gun = (A.where(F.notna()).mean(axis=1)).fillna(0.0).values
    sv = yon_gun.values
    nact = int((sv != 0).sum())
    gercek = float(np.nansum(port.values) / max(nact, 1))
    rng = np.random.default_rng(0)
    ks = rng.integers(60, len(a_gun) - 60, 1000)
    st = np.array([(np.roll(sv, int(k)) * a_gun).sum() / nact for k in ks])
    return {"yil_pozitif_oran": round(float((yt.m > 0).mean()), 2), "yil_sayisi": int(len(yt)),
            "tum_net_bps_ust10_haric": round(float(kalan.mean()) * 1e4, 1),
            "tum_t_ust10_haric": round(float(o.hac_t(z2.values, lag=h - 1)), 2),
            "acilis_anormal_bps": ac.get("anormal_net_bps"), "acilis_net_bps": ac.get("net_bps"),
            "plasebo_p": round(float((np.sum(st >= gercek) + 1) / 1001), 4),
            "not_havuz": "E/F anormal portföy serisinden; plasebo portföy serisinde"}


# ---------------------------------------------------------------- 2a-2i: özel öncüler -------------------------------
def esik_sinyal(z, yz=1.0, esik=1.0):
    return (yz * np.sign(z).where(z.abs() >= esik, 0.0)).fillna(0.0)


def birikim_z(x, k):
    sd = x.rolling(60, min_periods=40).std().shift(1)
    return x.rolling(k).sum() / (sd * np.sqrt(k))


def ozel_testler():
    rows = []
    rr = o.basit_getiri(["SPY"])["SPY"]
    # (a) 3-2-1 crack, dolar/varil, günlük DOLAR değişimi
    lv = seviye(["RB=F", "HO=F", "CL=F"])
    crack = (2 * lv["RB=F"] * 42 + lv["HO=F"] * 42 - 3 * lv["CL=F"]) / 3
    dcr = hizala(crack.diff())
    dcr.to_frame("dcrack").to_csv(os.path.join(ARA, "crack_dolar_degisim.csv"))
    for hd in RAFINERI:
        rows += cift("CRACK321", hd, "+", dcr, "a_crack", vadeli=True)
    log("crack tek hedefler", len(rows))
    base = cm.sinyaller(dcr.reindex(rr.index), rr, "+", rr)
    lagb = cm.sinyaller(dcr.shift(1).reindex(rr.index), rr, "+", rr)
    zc = {"B1": o.zskor(dcr.reindex(rr.index), 60), "B3": birikim_z(dcr.reindex(rr.index), 3)}
    for b in ("B1", "B1r", "B3"):
        sig, hdg = base[b]
        S = pd.DataFrame({c: sig for c in RAFINERI})
        Sl = pd.DataFrame({c: lagb[b][0] for c in RAFINERI})
        for h in (1, 2, 3):
            rows += havuz(S, "SEPET_RAFINERI", h, "CRACK321", b, "+", "a_crack", hedge=hdg, z=zc.get(b), lag=Sl)
            rows += havuz(Sl, "SEPET_RAFINERI", h, "CRACK321_g1", b, "+", "a_crack", hedge=hdg, aile="F1_kontrol")
    # ETF öncü kıyası (kontrol): UGA - USO getiri farkı (benzin marjının ETF vekili) -> rafineri sepeti
    xe = o.hizali_getiri("UGA") - o.hizali_getiri("USO")
    be = cm.sinyaller(xe.reindex(rr.index), rr, "+", rr)
    for b in ("B1", "B1r", "B3"):
        S = pd.DataFrame({c: be[b][0] for c in RAFINERI})
        for h in (1, 2, 3):
            rows += havuz(S, "SEPET_RAFINERI", h, "UGA-USO", b, "+", "a_crack", hedge=be[b][1], aile="F1_kontrol")
    log("crack sepet", len(rows))
    # (b) soya yağı, soya, kırma marjı -> BG, ADM
    lv = seviye(["ZM=F", "ZL=F", "ZS=F"])
    crush = 0.022 * lv["ZM=F"] + 0.11 * lv["ZL=F"] - lv["ZS=F"] / 100
    dcu = hizala(crush.diff())
    for hd in ("BG", "ADM"):
        rows += cift("ZL=F", hd, "+", o.hizali_getiri("ZL=F"), "b_soya", vadeli=True)
        rows += cift("ZS=F", hd, "+", o.hizali_getiri("ZS=F"), "b_soya", vadeli=True)
        rows += cift("KIRMA", hd, "+", dcu, "b_soya", vadeli=True)
        rows += cift("SOYB", hd, "+", o.hizali_getiri("SOYB"), "b_soya", aile="F1_kontrol")  # ETF öncü kıyası
    log("soya", len(rows))
    # (c) vade eğrisi vekilleri
    g = {e: o.hizali_getiri(e) for e in ("USO", "USL", "UNG", "UNL", "BNO")}
    for ad, x, hedefler in (("USO-USL", g["USO"] - g["USL"], ["USO"]), ("UNG-UNL", g["UNG"] - g["UNL"], ["UNG"]),
                            ("BNO-USO", g["BNO"] - g["USO"], ["BNO", "USO"])):
        for hd in hedefler:
            rows += cift(ad, hd, "+", x, "c_egri", bicimler=("B1", "B1r", "B3"))
            # USL/UNL kapanışı bayat (bayat_hedefler): öncü 1 gün gecikmeli kontrol
            XREG[ad + "_g1"] = (x.shift(1), False)
            for r in cm.cift_testi(ad + "_g1", hd, "+", x=x.shift(1), etiket=ad + "_g1", bicimler=("B1", "B1r", "B3")):
                r.update({"aile": "F1_kontrol", "grup": "c_egri", "oncu_gecikme": 1})
                rows.append(r)
    log("egri", len(rows))
    # (d) altın/gümüş oranı uçları: log(GLD/SLV) 60 günlük z (yalnız geçmiş ortalama ve std)
    P = o.panel("adjclose", ["GLD", "SLV"])
    lr = np.log(P["GLD"] / P["SLV"])
    zr = (lr - lr.rolling(60, min_periods=40).mean().shift(1)) / lr.rolling(60, min_periods=40).std().shift(1)
    for hd, yz in (("SLV", 1.0), ("SIL", 1.0), ("GLD", -1.0)):
        s = esik_sinyal(zr, yz)
        for h in (1, 2, 3):
            rows += tek(s, hd, h, "GLD/SLV_z60", "ORAN", "+" if yz > 0 else "-", "d_oran", z=zr, lag=s.shift(1))
    # (e) TIP -> GLD, SLV, GDX, GDXJ ; UUP -> GLD, GDX, REMX (ters)
    for hd in ("GLD", "SLV", "GDX", "GDXJ"):
        rows += cift("TIP", hd, "+", o.hizali_getiri("TIP"), "e_tip_uup")
    for hd in ("GLD", "GDX", "REMX"):
        rows += cift("UUP", hd, "-", o.hizali_getiri("UUP"), "e_tip_uup")
    # (f) GDX -> COPX, PICK, REMX
    for hd in ("COPX", "PICK", "REMX"):
        rows += cift("GDX", hd, "+", o.hizali_getiri("GDX"), "f_gdx")
    log("oran/tip/uup/gdx", len(rows))
    # (g) USO 5 ve 10 günlük birikimli şok
    xu = o.hizali_getiri("USO")
    for k in (5, 10):
        zk = birikim_z(xu, k)
        for esik, aile in ((1.0, "F1"), (2.0, "F1")):  # 1 = yöntem eşiği; 2 = hipotez dosyasındaki eşik (l2 #3-4)
            et = f"USO_{k}g_z{esik:g}"
            for hd, yz in [(t, 1.0) for t in ("XLE", "XOP", "OIH")] + [(t, -1.0) for t in ["JETS"] + TANKER]:
                s = esik_sinyal(zk, yz, esik)
                for h in (1, 2, 3):
                    rows += tek(s, hd, h, et, f"BIRIKIM{k}", "+" if yz > 0 else "-", "g_birikim", z=zk, lag=s.shift(1), aile=aile)
            s = esik_sinyal(zk, -1.0, esik)
            S = pd.DataFrame({c: s for c in TANKER})
            for h in (1, 2, 3):
                rows += havuz(S, "SEPET_TANKER", h, et, f"BIRIKIM{k}", "-", "g_birikim", z=zk, lag=S.shift(1), aile=aile)
    log("birikim", len(rows))
    # (h) rapor günü: sinyal t günü (+1 = t kapanışında al, t+1 kapanışında sat)
    tk = o.takvim()
    gun = pd.Series(tk.weekday, index=tk)
    ertesi = gun.shift(-1)
    for et, hd, t_gun, yon_on in (("UNG_persembe", "UNG", 2, "-"), ("USO_carsamba", "USO", 1, None),
                                  ("USO_persembe_e1_10", "USO", 2, "+")):
        kukla = ((gun == t_gun) & (ertesi == t_gun + 1)).astype(float)
        for yz in (1.0, -1.0):
            y = "+" if yz > 0 else "-"
            aile = "F1" if (yon_on is None or yon_on == y) else "F1_ters"
            rows += tek(kukla * yz, hd, 1, et, "TAKVIM", y, "h_rapor", aile=aile)
            k = REG[(et, hd, "TAKVIM", y)]
            rows[-1].update({f"kaydir{j}_t": o.islem_testi((kukla * yz).shift(j), hd, 1).get("t_anormal") for j in (1, 2, 3, 4)})
    # (i) 52 hafta zirvesine yakınlık: kapanış >= 0,98 x son 252 günün en yüksek kapanışı -> AL
    C = o.panel("adjclose", ZIRVE_HEDEF)
    oran = C / C.rolling(252, min_periods=252).max()
    SZ = (oran >= 0.98).astype(float).where(oran.notna(), 0.0)
    for hd in ZIRVE_HEDEF:
        for h in (1, 2, 3):
            rows += tek(SZ[hd], hd, h, "ZIRVE52_%98", "ZIRVE52", "+", "i_zirve", z=oran[hd], lag=SZ[hd].shift(1))
    for h in (1, 2, 3):
        rows += havuz(SZ, "SEPET_EMTIA11", h, "ZIRVE52_%98", "ZIRVE52", "+", "i_zirve", z=None, lag=SZ.shift(1))
    log("takvim/zirve", len(rows))
    return rows


# ---------------------------------------------------------------- çürütme testleri (bölüm 7) ------------------------
def kisa(sig, hedef, h, hedge=None, giris="kapanis", maliyet=None):
    if isinstance(sig, pd.DataFrame):
        d = o.havuz_donemli(sig, h, hedge=hedge, giris=giris, maliyet_bps=maliyet)
    else:
        d = o.donemli_test(sig, hedef, h, maliyet_bps=maliyet, giris=giris, hedge=hedge)
    return d.get("tum_anormal_net_bps"), d.get("is_t_anormal"), d.get("oos_t_anormal"), d.get("tum_t_anormal")


def maske(sig, m):
    mm = m.reindex(sig.index).fillna(False).astype(bool)
    if isinstance(sig, pd.DataFrame):
        return sig.mul((~mm).astype(float), axis=0)
    return sig.where(~mm, 0.0)


def curut(row, sig, z, hedge, lag_sig, giris="kapanis", etf_row=None):
    hedef, h = row["hedef"], int(row["h"])
    out = {"sinyal_id": row["sinyal_id"]}
    tablo = isinstance(sig, pd.DataFrame)
    # 3. yıl yıl
    if tablo:
        p = o.havuz_gunluk(sig, h).dropna()
        yt = pd.DataFrame({"n": p.groupby(p.index.year).size(), "net_bps": (p.groupby(p.index.year).mean() * 1e4).round(1)})
    else:
        yt = o.yillik_tablo(sig, hedef, h, giris=giris)
    YIL.extend({"sinyal_id": row["sinyal_id"], "yil": int(y), "n": int(r.n), "net_bps": r.net_bps} for y, r in yt.iterrows())
    yt3 = yt[yt.n >= 3]
    out["yil_pozitif"] = f"{int((yt3.net_bps > 0).sum())}/{len(yt3)}"
    if len(yt3):
        eniyi = yt3.net_bps.idxmax()
        out["en_iyi_yil"] = f"{eniyi}:{yt3.net_bps.max():+.0f}"
        out["oos_2019_20_bps"] = round(float(yt.loc[[y for y in yt.index if y in (2019, 2020)], "net_bps"].mean()), 1) if any(y in (2019, 2020) for y in yt.index) else np.nan
        out["oos_2021_sonrasi_bps"] = round(float(yt.loc[[y for y in yt.index if y >= 2021], "net_bps"].mean()), 1) if any(y >= 2021 for y in yt.index) else np.nan
    # 9. sınır sinyalleri hariç
    if z is not None:
        zz = z.reindex(o.takvim())
        sinir = ((zz.abs() >= 1.0) & (zz.abs() < 1.2)) if row["bicim"] != "ZIRVE52" else ((zz >= 0.98) & (zz < 0.985))
        a, ti, to, tt = kisa(maske(sig, sinir), hedef, h, hedge, giris)
        out.update({"sinir_haric_bps": a, "sinir_haric_is_t": ti, "sinir_haric_oos_t": to})
        if row["bicim"] != "ZIRVE52":  # 2. eşik 1,5
            a, ti, to, tt = kisa(maske(sig, zz.abs() < 1.5), hedef, h, hedge, giris)
            out.update({"esik15_bps": a, "esik15_is_t": ti, "esik15_oos_t": to})
    # 11. kriz hariç
    tk = pd.Series(False, index=o.takvim())
    for b, e in KRIZ:
        tk[(tk.index >= b) & (tk.index <= e)] = True
    a, ti, to, tt = kisa(maske(sig, tk), hedef, h, hedge, giris)
    out.update({"kriz_haric_bps": a, "kriz_haric_is_t": ti, "kriz_haric_oos_t": to})
    # 2. maliyet iki katı (tek hedef)
    if not tablo:
        a, ti, to, tt = kisa(sig, hedef, h, hedge, giris, maliyet=o.maliyet_serisi(hedef) * 2)
        out.update({"maliyet2x_bps": a, "maliyet2x_oos_t": to})
    # 8. en büyük 20 işlem
    cols = list(sig.columns) if tablo else [hedef]
    F = o.ileri_getiri(cols, h, giris)
    R = o.basit_getiri(cols)
    S = (sig if tablo else sig.to_frame(hedef)).reindex(F.index).fillna(0.0)
    T = (S * F).where(S != 0).stack().dropna()
    buyuk = T.abs().sort_values(ascending=False).head(20)
    m = o.meta()
    sup = 0
    for (t, c) in buyuk.index:
        i = R.index.get_loc(t)
        w = R[c].iloc[i + 1:i + 1 + h].abs().max()
        esik = 0.8 if m.loc[c, "tur"] == "EQUITY" else 0.4
        sup += int(w > esik)
    out["buyuk20_supheli_gun"] = sup
    out["buyuk20_en_buyuk"] = f"{buyuk.index[0][0].date()} {buyuk.index[0][1]} {T[buyuk.index[0]] * 1e4:+.0f}bps" if len(buyuk) else ""
    gunler = pd.Series(False, index=o.takvim())
    gunler[[t for t, _ in buyuk.index]] = True
    a, ti, to, tt = kisa(maske(sig, gunler), hedef, h, hedge, giris)
    out.update({"buyuk20_haric_bps": a, "buyuk20_haric_t": tt})
    # 6. rejim: VIX > 20 / <= 20 (VIX 16:15 ET; yalnız koşul ayrımı)
    vix = o.panel("adjclose", ["^VIX"])["^VIX"] if "^VIX" in o.panel("adjclose").columns else None
    if vix is not None:
        for ad, mm in (("vix_yuksek", vix > 20), ("vix_dusuk", vix <= 20)):
            a, ti, to, tt = kisa(maske(sig, ~mm), hedef, h, hedge, giris)
            out.update({f"{ad}_bps": a, f"{ad}_t": tt})
    # 7. öncü 1 gün gecikmeli
    if lag_sig is not None:
        a, ti, to, tt = kisa(lag_sig, hedef, h, hedge, giris)
        out.update({"gecikmeli_bps": a, "gecikmeli_is_t": ti, "gecikmeli_oos_t": to})
    if etf_row is not None:
        out.update({"etf_oncu": etf_row.get("oncu"), "etf_oncu_bps": etf_row.get("tum_anormal_net_bps"),
                    "etf_oncu_is_t": etf_row.get("is_t_anormal"), "etf_oncu_oos_t": etf_row.get("oos_t_anormal")})
    return out


YIL = []


def sinyal_bul(row):
    """Satırdan (sig, z, hedge, lag_sig, giris)."""
    k = (row["oncu"], row["hedef"], row["bicim"], row["yon"])
    if k in REG:
        g = REG[k]
        return g["sig"], g["z"], g.get("hedge"), g["lag"], g["giris"]
    x, vad = XREG[row["oncu"]]
    sig, z, hd = cift_sinyal(row["oncu"], x, row["hedef"], row["yon"], row["bicim"])
    lag = cift_sinyal(row["oncu"], x, row["hedef"], row["yon"], row["bicim"], lag=1)[0]
    return sig, z, hd, lag, "kapanis"


def main():
    yeniden = "--yeniden" in sys.argv
    os.makedirs(ARA, exist_ok=True)
    # ---- 1) hazır sonuçlar (cift_motoru): aile F1
    cs = pd.read_csv(os.path.join(o.KOK, "ek", "backtest", "cift", "sonuclar.csv"), low_memory=False)
    f1 = cs[cs.aile == "F1"].copy()
    f1_hip = f1[f1.bicim != "B1r"]
    yeni = f1_hip[(f1_hip.is_t_anormal < 2) & (f1_hip.oos_t_anormal >= 2.5)].copy()
    yeni["kaynak"] = "cift_motoru"
    # ---- 2) özel öncüler
    ara = os.path.join(ARA, "ozel.pkl")
    if os.path.exists(ara) and not yeniden:
        df, XR, RG = pd.read_pickle(ara)
        XREG.update(XR)
        REG.update(RG)
    else:
        df = pd.DataFrame(ozel_testler())
        pd.to_pickle((df, dict(XREG), dict(REG)), ara)
    log("özel testler", len(df))
    df["sinyal_id"] = [sid(r) for r in df.to_dict("records")]
    # sınıflandırma: hipotez satırları (F1, F1_kesif) birlikte; kontrol ayrı
    ana = df[df.aile.isin(["F1", "F1_kesif"])].copy()
    ana["aile_bh"] = "F1"
    kon = df[~df.aile.isin(["F1", "F1_kesif"])].copy()
    ana = cm.etiketle(ana.rename(columns={"aile": "aile_orj", "aile_bh": "aile"})).rename(columns={"aile": "aile_bh", "aile_orj": "aile"})
    kon = o.siniflandir(kon.assign(ozgu=np.nan))
    ozel = ~ana.bicim.isin(["B1", "B1r", "B2", "B3"])
    ozg = (pd.to_numeric(ana.spyden_ar_is_t, errors="coerce") >= 2) & (pd.to_numeric(ana.spyden_ar_oos_t, errors="coerce") >= 2)
    ana.loc[ozel & ana.spyden_ar_is_t.notna(), "ozgu"] = ozg[ozel & ana.spyden_ar_is_t.notna()]
    tum = pd.concat([ana, kon], ignore_index=True)
    yeni2 = ana[(ana.bicim != "B1r") & (ana.is_t_anormal < 2) & (ana.oos_t_anormal >= 2.5)].copy()
    yeni2["kaynak"] = "f1_emtia"
    ys = ["kaynak", "oncu", "hedef", "bicim", "yon", "h", "oos_n", "oos_anormal_net_bps", "is_t_anormal", "oos_t_anormal", "son_net_bps"]
    pd.concat([yeni[ys], yeni2[ys]]).sort_values("oos_t_anormal", ascending=False).to_csv(os.path.join(CIKTI, "yeni_rejim.csv"), index=False)
    # ---- çürütme: ELENDİ dışı (hazır F1 + özel hipotez satırları)
    hazir = f1[f1.sinif != "ELENDI"].copy()
    hazir["grup"] = "hazir_cift"
    hazir["sinyal_id"] = [sid(r) for r in hazir.to_dict("records")]
    for on in hazir.oncu.unique():
        XREG.setdefault(on, (o.hizali_getiri(on), on.endswith("=F")))
    ak = pd.concat([hazir.assign(kaynak="cift_motoru"), ana[ana.sinif != "ELENDI"].assign(kaynak="f1_emtia")], ignore_index=True)
    cur = []
    for r in ak.to_dict("records"):
        sig, z, hd, lag, giris = sinyal_bul(r)
        etf = None
        if str(r["oncu"]).endswith("=F") and VADELI_ETF.get(r["oncu"]):
            e = VADELI_ETF[r["oncu"]]
            rr = cm.cift_testi(e, r["hedef"], r["yon"], ufuklar=(int(r["h"]),), bicimler=(r["bicim"],))
            etf = rr[0] if rr else None
        cur.append(curut(r, sig, z, hd, lag, giris, etf))
        log("çürütme", r["sinyal_id"])
    cur = pd.DataFrame(cur)
    cur.to_csv(os.path.join(CIKTI, "curutme.csv"), index=False)
    pd.DataFrame(YIL).to_csv(os.path.join(CIKTI, "yillik.csv"), index=False)
    # ---- çıktılar
    on = ["aile", "sinyal_id", "grup", "oncu", "hedef", "bicim", "yon", "h", "havuz", "bayat_isaret", "oncu_gecikme"]
    son = ["son_gun", "son_sinyal", "ozgu", "sinif"]
    tum = tum[on + [c for c in tum.columns if c not in on + son] + son]
    tum.to_csv(os.path.join(CIKTI, "sonuclar.csv"), index=False)
    kos = ["k_A", "k_B", "k_B_zayif", "bh_oos", "k_C", "k_D", "k_E", "k_F", "k_G", "k_H", "k_I"]
    temel = ["kaynak", "aile", "sinyal_id", "oncu", "hedef", "bicim", "yon", "h", "havuz", "tum_n", "oos_n", "tum_anormal_net_bps",
             "is_t_anormal", "oos_t_anormal", "son_net_bps", "tum_net_bps_al", "acilis_anormal_bps", "ertesi_anormal_bps",
             "plasebo_p", "yil_pozitif_oran", "b2_kismi_t", "spyden_ar_is_t", "spyden_ar_oos_t", "ozgu"] + kos + ["sinif", "son_gun", "son_sinyal"]
    akk = ak[[c for c in temel if c in ak.columns]].merge(cur, on="sinyal_id", how="left")
    akk.sort_values("oos_t_anormal", ascending=False).to_csv(os.path.join(CIKTI, "ayakta_kalanlar.csv"), index=False)
    hip = ana[ana.bicim != "B1r"]
    print("HAZIR F1 test:", len(f1), "hipotez:", len(f1_hip), "sınıf:", f1.sinif.value_counts().to_dict())
    print("ÖZEL test:", len(df), "hipotez (B1r hariç):", len(hip), "B1r:", (ana.bicim == "B1r").sum(), "kontrol:", len(kon))
    print("özel sınıflar:", ana.sinif.value_counts().to_dict(), "| grup:", ana.groupby("grup").sinif.value_counts().unstack(fill_value=0).to_dict())
    print("k_A:", ana.k_A.sum(), "k_A&k_B_zayif:", (ana.k_A & ana.k_B_zayif).sum(), "IS>=2&OOS>=1.5:", ((ana.is_t_anormal >= 2) & (ana.oos_t_anormal >= 1.5)).sum())
    log("bitti")


if __name__ == "__main__":
    main()
