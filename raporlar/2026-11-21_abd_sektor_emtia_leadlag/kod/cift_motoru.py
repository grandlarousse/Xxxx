"""Öncü -> hedef çift testi motoru, sürüm 2 (F1, F2a, F3 için ortak; YONTEM.md bölüm 4-7 ve 10).

Girdi : ek/hipotez/birlesik.csv (önceden yazılı hipotez çiftleri) ya da programdan verilen çift / özel öncü serisi.
Çıktı : ek/backtest/cift/sonuclar.csv, ayakta_kalanlar.csv, kiyas_artik_donusu.csv, OZET.txt

Biçimler (x = öncünün t günü kapanışta bilinen log getirisi, r = hedefin t günü getirisi):
  B1   ham öncü        : z(x) >= +1 -> hipotez yönünde AL; <= -1 -> SAT. Hedef: ham ileri getiri.
  B1r  arındırılmış    : z(x - beta*SPY) aynı kural; hedef: ileri getiri - beta*SPY. "Öncüye özgü" etiketi buna bağlı.
  B2   yetişme artığı  : e = r - beta*x ; z(e) <= -1 -> AL ; >= +1 -> SAT. Öncüye özgülük: kısmi regresyon (b2_kismi_t).
  B3   3 günlük öncü   : z(x_t + x_{t-1} + x_{t-2}) >= +1 -> hipotez yönünde AL; <= -1 -> SAT.
Kıyas (hedef başına bir kez, hipotez sayılmaz):
  KDr  hedefin SPY artığının dönüşü: z(r - beta*SPY) <= -1 -> AL ; >= +1 -> SAT.

Kullanım: python3 kod/cift_motoru.py
          from cift_motoru import cift_testi, sinyaller   (özel öncü serisi: cift_testi(..., x=seri, etiket="crack"))
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak as o  # noqa: E402

CIKTI = os.path.join(o.KOK, "ek", "backtest", "cift")
OZET_SUTUN = ["aile", "oncu", "hedef", "bicim", "yon", "h", "tum_n", "tum_anormal_net_bps", "is_t_anormal", "oos_t_anormal",
              "son_net_bps", "tum_net_bps_al", "tum_anormal_bps_al", "ozgu", "sinif", "son_sinyal"]


def sinyaller(x, r, yon, spy=None):
    """Dönen: {biçim: (sinyal serisi, hedge)}. spy: SPY günlük getirisi (B1r için)."""
    s = {}
    yz = 1.0 if yon != "-" else -1.0
    z = o.zskor(x, 60)
    s["B1"] = (yz * np.sign(z).where(z.abs() >= 1, 0.0), None)
    if spy is not None:
        xr = x - o.kayan_beta(x, spy) * spy
        zr = o.zskor(xr, 60)
        s["B1r"] = (yz * np.sign(zr).where(zr.abs() >= 1, 0.0), "SPY")
    e = r - o.kayan_beta(r, x) * x
    ze = o.zskor(e, 60)
    s["B2"] = (-np.sign(ze).where(ze.abs() >= 1, 0.0), None)
    sd = x.rolling(60, min_periods=40).std().shift(1)
    z3 = x.rolling(3).sum() / (sd * np.sqrt(3))
    s["B3"] = (yz * np.sign(z3).where(z3.abs() >= 1, 0.0), None)
    return {k: (v.fillna(0.0), hd) for k, (v, hd) in s.items()}


def kismi_t(x, r, hedef, h, spy):
    """B2'nin öncüye özgülüğü: hedge'li ileri getiri ~ z(e_oncu) + z(e_spy) + z(r). Dönen: -t(z(e_oncu)) (pozitif = yetişme)."""
    import statsmodels.api as sm

    f = o._ileri(hedef, h, "kapanis", "SPY")
    ze = o.zskor(r - o.kayan_beta(r, x) * x, 60)
    zs = o.zskor(r - o.kayan_beta(r, spy) * spy, 60)
    zr = o.zskor(r, 60)
    d = pd.DataFrame({"f": f, "ze": ze, "zs": zs, "zr": zr}).dropna()
    if len(d) < 500:
        return np.nan
    X = sm.add_constant(d[["ze", "zs", "zr"]].clip(-5, 5))
    m = sm.OLS(d["f"], X).fit(cov_type="HAC", cov_kwds={"maxlags": max(h - 1, 0), "kernel": "uniform" if h > 1 else "bartlett"})
    return round(float(-m.tvalues["ze"]), 2)


def _on_eleme(d):
    return (d.get("is_t_anormal") or 0) >= 2.0 and (d.get("oos_t_anormal") or 0) >= 1.5 and (d.get("is_anormal_net_bps") or 0) > 0


def cift_testi(oncu, hedef, yon="+", x=None, etiket=None, ufuklar=(1, 2, 3), bicimler=("B1", "B1r", "B2", "B3")):
    """Tek çift için bütün biçim ve ufuklar. x verilirse (özel öncü serisi, kapanışta bilinen) o kullanılır."""
    if x is None:
        x = o.hizali_getiri(oncu)
    spy = o.basit_getiri(["SPY"])["SPY"]
    r = spy if hedef == "SPY" else o.basit_getiri([hedef])[hedef]
    x = x.reindex(r.index)
    ikiz = abs(x.corr(r)) > 0.95
    sat = []
    for b, (sig, hd) in sinyaller(x, r, yon, spy if (oncu != "SPY" and hedef != "SPY") else None).items():
        if b not in bicimler or (b == "B2" and ikiz):
            continue
        for h in ufuklar:
            d = o.donemli_test(sig, hedef, h, hedge=hd)
            if d.get("tum_n", 0) < 30:
                continue
            row = {"oncu": etiket or oncu, "hedef": hedef, "bicim": b, "yon": yon, "h": h, "havuz": "tek hedef",
                   "bayat_isaret": hedef in o.bayat_hedefler()}
            row.update(d)
            if _on_eleme(d):
                row.update(o.ek_olcutler(sig, hedef, h, hedge=hd))
                row.update(o.son_sinyal(sig))
                if b == "B2":
                    row["b2_kismi_t"] = kismi_t(x, r, hedef, h, spy)
            sat.append(row)
    return sat


def etiketle(df):
    """Öncüye özgülük etiketi ve sınıf. B1/B3: aynı çift ve ufukta B1r IS ve OOS t >= 2,0. B2: kısmi t >= 2,5."""
    anahtar = ["oncu", "hedef", "yon", "h"]
    b1r = df[df.bicim == "B1r"].set_index(anahtar)
    ok = ((pd.to_numeric(b1r["is_t_anormal"], errors="coerce") >= 2.0) & (pd.to_numeric(b1r["oos_t_anormal"], errors="coerce") >= 2.0))
    ozgu_b1 = set(ok[ok].index)
    df["ozgu"] = [((tuple(v) in ozgu_b1) if b in ("B1", "B3", "B1r") else (float(k) >= 2.5 if k == k else False))
                  for b, k, v in zip(df.bicim, df.get("b2_kismi_t", pd.Series(np.nan, index=df.index)), df[anahtar].values)]
    m = o.meta()
    hisse = df.hedef.map(lambda s: m.loc[s, "tur"] == "EQUITY" if s in m.index else False)
    tavan = (df.bicim == "B2") & hisse  # hisse düzeyi AL-dönüş: en çok KOŞULLU
    return o.siniflandir(df, tavan_kosullu=tavan)


def main():
    os.makedirs(CIKTI, exist_ok=True)
    hip = pd.read_csv(os.path.join(o.KOK, "ek", "hipotez", "birlesik.csv"))
    m = o.meta()
    abd = set(m[(m["saat_dilimi"] == "America/New_York") & (m["tur"].isin(["EQUITY", "ETF"]))].index)
    hip = hip[(hip.oncu_evrende == 1) & (hip.hedef_evrende == 1) & hip.aile.isin(["F1", "F2", "F3"])]
    hip = hip[hip.hedef.isin(abd) & (hip.oncu != hip.hedef) & hip.oncu.isin(m.index)]
    hip = hip[~hip.oncu.str.endswith("=X")]                      # kur çubukları bayat (YONTEM.md bölüm 3)
    hip = hip[~hip.hedef.map(o.kaldiracli)]                      # kaldıraçlı ETF keşif hedefi değil
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
            print("HATA", c.oncu, c.hedef, type(e).__name__, str(e)[:100], flush=True)
        if k % 100 == 0:
            print(f"{k}/{len(cift)} çift, {len(sat)} test", flush=True)
    df = etiketle(pd.DataFrame(sat))
    # kıyas: hedefin SPY artığının dönüşü
    kd = []
    spy = o.basit_getiri(["SPY"])["SPY"]
    for hedef in sorted(set(cift.hedef) - {"SPY"}):
        r = o.basit_getiri([hedef])[hedef]
        ze = o.zskor(r - o.kayan_beta(r, spy) * spy, 60)
        sig = (-np.sign(ze).where(ze.abs() >= 1, 0.0)).fillna(0.0)
        for h in (1, 2, 3):
            d = o.donemli_test(sig, hedef, h)
            if d.get("tum_n", 0) < 30:
                continue
            row = {"aile": "KIYAS", "oncu": "SPY-artik", "hedef": hedef, "bicim": "KDr", "yon": "-", "h": h, **d}
            if _on_eleme(d):
                row.update(o.ek_olcutler(sig, hedef, h))
                row.update(o.son_sinyal(sig))
            kd.append(row)
    kdf = pd.DataFrame(kd)
    tur = kdf.hedef.map(lambda s: m.loc[s, "tur"] == "EQUITY")
    kdf = o.siniflandir(kdf, tavan_kosullu=tur)
    kk = kdf.set_index(["hedef", "h"])["tum_anormal_net_bps"]
    df["kiyas_kdr_bps"] = [kk.get((a, b), np.nan) for a, b in zip(df.hedef, df.h)]
    df.to_csv(os.path.join(CIKTI, "sonuclar.csv"), index=False)
    kdf.to_csv(os.path.join(CIKTI, "kiyas_artik_donusu.csv"), index=False)
    ak = df[df.sinif != "ELENDI"].sort_values(["sinif", "oos_t_anormal"], ascending=[True, False])
    ak.to_csv(os.path.join(CIKTI, "ayakta_kalanlar.csv"), index=False)
    satirlar = []
    hip_test = df[df.bicim != "B1r"]
    satirlar.append(f"TOPLAM TEST: {len(df)} (hipotez testi: {len(hip_test)}; B1r arındırma testi: {(df.bicim == 'B1r').sum()})")
    satirlar.append(f"Beklenen yanlış pozitif (sıfır hipotezi): SAĞLAM {len(hip_test) * o.P_SIFIR_SAGLAM:.2f}, KOŞULLU {len(hip_test) * o.P_SIFIR_KOSULLU:.2f}")
    satirlar.append("Sınıflar (aile x biçim):\n" + df.groupby(["aile", "bicim"]).sinif.value_counts().unstack(fill_value=0).to_string())
    satirlar.append("IS t >= 2,5 olan: %d; bunlardan OOS t >= 2,0: %d; OOS t >= 2,5: %d; BH geçen: %d" % (
        df.k_A.sum(), (df.k_A & df.k_B_zayif).sum(), (df.k_A & df.k_B).sum(), (df.k_A & df.bh_oos).sum()))
    for b in ("B1", "B1r", "B2", "B3"):
        x = df[df.bicim == b]
        satirlar.append(f"{b}: n={len(x)} | tüm-örneklem t ort {x.tum_t_anormal.mean():+.2f}, >=2: {(x.tum_t_anormal >= 2).mean():.1%}, <=-2: {(x.tum_t_anormal <= -2).mean():.1%} | OOS t ort {x.oos_t_anormal.mean():+.2f}")
    satirlar.append("Kıyas KDr (hedefin SPY artığı dönüşü) sınıflar: " + str(kdf.sinif.value_counts().to_dict()))
    satirlar.append("\nAYAKTA KALANLAR (ELENDİ dışı):\n" + ak[[c for c in OZET_SUTUN if c in ak.columns]].to_string(index=False))
    kak = kdf[kdf.sinif != "ELENDI"].sort_values("oos_t_anormal", ascending=False)
    satirlar.append("\nKIYAS AYAKTA KALANLAR:\n" + kak[[c for c in OZET_SUTUN if c in kak.columns]].head(60).to_string(index=False))
    open(os.path.join(CIKTI, "OZET.txt"), "w").write("\n".join(satirlar))
    print("\n".join(satirlar[:8]))


if __name__ == "__main__":
    main()
