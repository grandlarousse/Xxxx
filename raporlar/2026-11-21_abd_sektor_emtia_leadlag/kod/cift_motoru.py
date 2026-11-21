"""Öncü -> hedef çift testi motoru (F1, F2, F3 için ortak; YONTEM.md bölüm 4-7).

Girdi : ek/hipotez/birlesik.csv (önceden yazılı hipotez çiftleri) ya da programdan verilen çift listesi.
Çıktı : ek/backtest/cift/sonuclar.csv (test başına satır) ve ek/backtest/cift/ayakta_kalanlar.csv

Biçimler:
  B1  ham öncü          : z(x_t) >= +1 -> hipotez yönünde AL; <= -1 -> SAT
  B2  yetişme artığı    : e = r - beta*x ; z(e) <= -1 -> AL ; >= +1 -> SAT
  B2x B2, ama hedefin kendi getirisi sakin günlerde (|z(r)| < 1): kendi dönüşünden arındırılmış yetişme
  B3  3 günlük öncü     : z(x_t + x_{t-1} + x_{t-2}) >= +1 -> hipotez yönünde AL; <= -1 -> SAT
  KD  kıyas: hedefin kendi dönüşü (z(r) <= -1 -> AL; >= +1 -> SAT). Hedef başına bir kez; hipotez sayılmaz.

Kullanım: python3 kod/cift_motoru.py            (birlesik.csv'deki bütün F1/F2/F3 çiftleri)
          from cift_motoru import cift_testi     (başka betiklerden tek çift)
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak as o  # noqa: E402

CIKTI = os.path.join(o.KOK, "ek", "backtest", "cift")
_ist = None


def maliyet(hedef):
    """Likidite sınıfına göre gidiş-dönüş maliyet (bps). YONTEM.md bölüm 5."""
    global _ist
    if _ist is None:
        _ist = pd.read_csv(os.path.join(o.KOK, "ek", "ozet_istatistik.csv")).set_index("sembol")
    try:
        h = float(_ist.loc[hedef, "hacim20_mn_usd"])
    except Exception:  # noqa: BLE001
        return 20
    return 5 if h >= 100 else (10 if h >= 20 else 20)


def donem_sinirlari(seri):
    """IS/OOS sınırı: araç 2015'ten sonra başladıysa örneklemin ilk %55'i IS."""
    ilk = seri.first_valid_index()
    if ilk is None:
        return o.IS_BITIS, o.OOS_BAS
    if ilk > pd.Timestamp("2015-01-01"):
        idx = seri.dropna().index
        kes = idx[int(len(idx) * 0.55)]
        return str(kes.date()), str((kes + pd.Timedelta(days=1)).date())
    return o.IS_BITIS, o.OOS_BAS


def donemli(sinyal, hedef, h, mal, giris="kapanis"):
    c = o.panel("adjclose", [hedef])[hedef]
    is_bit, oos_bas = donem_sinirlari(c)
    out = {}
    for ad, b, e in (("tum", None, None), ("is", None, is_bit), ("oos", oos_bas, None), ("son", o.SON_BAS, None)):
        r = o.islem_testi(sinyal, hedef, h, mal, giris, b, e)
        for k, v in r.items():
            out[f"{ad}_{k}"] = v
    return out


def sinyaller(x, r, yon):
    """x: öncünün kapanışta bilinen log getirisi; r: hedefin günlük getirisi. Dönen: {biçim: sinyal serisi}."""
    s = {}
    yz = 1.0 if yon != "-" else -1.0
    z = o.zskor(x, 60)
    s["B1"] = yz * np.sign(z).where(z.abs() >= 1, 0.0)
    beta = o.kayan_beta(r, x)
    e = r - beta * x
    ze = o.zskor(e, 60)
    b2 = -np.sign(ze).where(ze.abs() >= 1, 0.0)
    s["B2"] = b2
    zr = o.zskor(r, 60)
    s["B2x"] = b2.where(zr.abs() < 1, 0.0)
    sd = x.rolling(60, min_periods=40).std().shift(1)
    z3 = x.rolling(3).sum() / (sd * np.sqrt(3))
    s["B3"] = yz * np.sign(z3).where(z3.abs() >= 1, 0.0)
    return {k: v.fillna(0.0) for k, v in s.items()}


def kendi_donusu(r):
    zr = o.zskor(r, 60)
    return (-np.sign(zr).where(zr.abs() >= 1, 0.0)).fillna(0.0)


def ek_olcutler(sinyal, hedef, h, mal):
    """Pahalı sağlamlık ölçütleri (yalnız ön elemeyi geçenler için)."""
    yt = o.yillik_tablo(sinyal, hedef, h, mal)
    yt = yt[yt["n"] >= 3]
    pl = o.plasebo(sinyal, hedef, h)
    ac = o.islem_testi(sinyal, hedef, h, mal, "acilis")
    er = o.islem_testi(sinyal, hedef, h, mal, "ertesi")
    return {
        "yil_pozitif_oran": round(float((yt["net_bps"] > 0).mean()), 2) if len(yt) else np.nan,
        "yil_sayisi": int(len(yt)),
        "plasebo_max_abs_t": round(float(np.nanmax(np.abs([v for v in pl.values() if v is not None and v == v] or [np.nan]))), 2),
        "acilis_anormal_bps": ac.get("anormal_net_bps"),
        "acilis_t_anormal": ac.get("t_anormal"),
        "ertesi_anormal_bps": er.get("anormal_net_bps"),
        "ertesi_t_anormal": er.get("t_anormal"),
    }


def cift_testi(oncu, hedef, yon="+", x=None, etiket=None, ufuklar=(1, 2, 3), bicimler=("B1", "B2", "B2x", "B3")):
    """Tek çift için bütün biçim ve ufuklar. x verilirse (özel öncü serisi) o kullanılır."""
    if x is None:
        x = o.hizali_getiri(oncu)
    r = o.basit_getiri([hedef])[hedef]
    x = x.reindex(r.index)
    mal = maliyet(hedef)
    sat = []
    for b, sig in sinyaller(x, r, yon).items():
        if b not in bicimler:
            continue
        for h in ufuklar:
            d = donemli(sig, hedef, h, mal)
            if d.get("tum_n", 0) < 30:
                continue
            row = {"oncu": etiket or oncu, "hedef": hedef, "bicim": b, "yon": yon, "h": h, "maliyet_bps": mal}
            row.update(d)
            if abs(d.get("tum_t_anormal") or 0) >= 2.5 and (d.get("tum_anormal_net_bps") or 0) > 0:
                row.update(ek_olcutler(sig, hedef, h, mal))
            sat.append(row)
    return sat


def siniflandir(df):
    """YONTEM.md bölüm 6 koşulları. Sütunlar eklenir: k_A..k_I, sinif."""
    g = lambda c: pd.to_numeric(df.get(c), errors="coerce")  # noqa: E731
    df["k_A"] = g("tum_t_anormal") >= 3.0
    df["k_A_zayif"] = g("tum_t_anormal") >= 2.5
    ayni = (np.sign(g("is_anormal_net_bps")) == np.sign(g("oos_anormal_net_bps"))) & (g("oos_anormal_net_bps") > 0)
    df["k_B"] = ayni & (g("oos_t_anormal") >= 2.0)
    df["k_B_zayif"] = ayni & (g("oos_t_anormal") >= 1.5)
    df["k_C"] = g("son_net_bps") > 0
    df["k_D"] = g("tum_anormal_net_bps") >= 10
    df["k_E"] = (g("tum_net_bps_ust10_haric") > 0) & (g("tum_t_ust10_haric") >= 1.5)
    df["k_F"] = g("yil_pozitif_oran") >= 0.6
    df["k_G"] = (g("tum_n") >= 100) & (g("oos_n") >= 40)
    df["k_H"] = g("plasebo_max_abs_t") < 2
    df["k_I"] = g("acilis_anormal_bps") > 0
    tam = df[["k_A", "k_B", "k_C", "k_D", "k_E", "k_F", "k_G", "k_H", "k_I"]].all(axis=1)
    digerleri = df[["k_C", "k_D", "k_E", "k_F", "k_G", "k_H", "k_I"]].sum(axis=1)
    kosullu = df["k_A_zayif"] & df["k_B_zayif"] & (digerleri >= 6) & ~tam
    izle = df["k_A_zayif"] & (g("oos_anormal_net_bps") > 0) & ~tam & ~kosullu
    df["sinif"] = np.where(tam, "SAGLAM", np.where(kosullu, "KOSULLU", np.where(izle, "IZLE", "ELENDI")))
    return df


def main():
    os.makedirs(CIKTI, exist_ok=True)
    hip = pd.read_csv(os.path.join(o.KOK, "ek", "hipotez", "birlesik.csv"))
    m = o.meta()
    abd = set(m[(m["saat_dilimi"] == "America/New_York") & (m["tur"].isin(["EQUITY", "ETF"]))].index)
    hip = hip[(hip.oncu_evrende == 1) & (hip.hedef_evrende == 1) & hip.aile.isin(["F1", "F2", "F3"])]
    hip = hip[hip.hedef.isin(abd) & (hip.oncu != hip.hedef) & hip.oncu.isin(m.index)]
    hip = hip[~hip.oncu.str.endswith("=X")]  # kur çubukları bayat (YONTEM.md bölüm 3)
    hip["yon"] = hip.yon.where(hip.yon.isin(["+", "-"]), "+")
    cift = hip.sort_values("oncelik").drop_duplicates(["oncu", "hedef", "yon"])
    print(len(cift), "tekil çift (yön dahil);", cift.aile.value_counts().to_dict(), flush=True)
    sat = []
    for k, (_, c) in enumerate(cift.iterrows(), 1):
        try:
            for row in cift_testi(c.oncu, c.hedef, c.yon):
                row.update({"aile": c.aile, "ajan": c.ajan, "oncelik": c.oncelik})
                sat.append(row)
        except Exception as e:  # noqa: BLE001
            print("HATA", c.oncu, c.hedef, str(e)[:100], flush=True)
        if k % 100 == 0:
            print(f"{k}/{len(cift)} çift, {len(sat)} test", flush=True)
    # kıyas: hedefin kendi dönüşü
    kd = []
    for hedef in sorted(set(cift.hedef)):
        r = o.basit_getiri([hedef])[hedef]
        sig = kendi_donusu(r)
        mal = maliyet(hedef)
        for h in (1, 2, 3):
            d = donemli(sig, hedef, h, mal)
            if d.get("tum_n", 0) >= 30:
                kd.append({"oncu": "KENDI", "hedef": hedef, "bicim": "KD", "yon": "-", "h": h, "maliyet_bps": mal, "aile": "KIYAS", **d})
    df = pd.DataFrame(sat)
    df["p_tum"] = o.t_to_p(pd.to_numeric(df["tum_t_anormal"], errors="coerce")) / 2  # tek yönlü
    df.loc[pd.to_numeric(df["tum_t_anormal"], errors="coerce") < 0, "p_tum"] = 1.0
    df["bh_q10"] = o.bh_fdr(df["p_tum"].values, 0.10)
    df = siniflandir(df)
    kdf = pd.DataFrame(kd)
    # B2'nin kıyasa göre artı katkısı
    kk = kdf.set_index(["hedef", "h"])["tum_anormal_net_bps"]
    df["kiyas_kd_bps"] = [kk.get((a, b), np.nan) for a, b in zip(df.hedef, df.h)]
    df.to_csv(os.path.join(CIKTI, "sonuclar.csv"), index=False)
    kdf.to_csv(os.path.join(CIKTI, "kiyas_kendi_donusu.csv"), index=False)
    ak = df[df.sinif.isin(["SAGLAM", "KOSULLU", "IZLE"])].sort_values(["sinif", "tum_t_anormal"], ascending=[True, False])
    ak.to_csv(os.path.join(CIKTI, "ayakta_kalanlar.csv"), index=False)
    print("TOPLAM TEST:", len(df), "| sınıflar:", df.sinif.value_counts().to_dict(), "| BH q10 geçen:", int(df.bh_q10.sum()))
    print("biçime göre:", df.groupby("bicim").sinif.value_counts().unstack(fill_value=0).to_string())
    print("t dağılımı (tüm, anormal): ortalama %.2f, >=2: %d, >=3: %d, <=-3: %d" % (
        df.tum_t_anormal.mean(), (df.tum_t_anormal >= 2).sum(), (df.tum_t_anormal >= 3).sum(), (df.tum_t_anormal <= -3).sum()))


if __name__ == "__main__":
    main()
