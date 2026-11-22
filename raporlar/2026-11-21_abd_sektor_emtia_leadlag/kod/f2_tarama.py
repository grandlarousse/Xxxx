"""F2b: körlemesine öncülük taraması, yürüyen seçim, grup içinde geride kalan, ETF negatif öncülük, yabancı seans farkı.

YONTEM.md bölüm 4 (F2b), 5, 6, 7. İstatistik (t, maliyet, dönem, sınıf) ortak.py ve cift_motoru.py'den gelir.

Aşamalar (her biri tek başına < 5 dk; ara sonuçlar ek/backtest/f2_tarama/ara/ altında):
  1   körlemesine tarama: IS t matrisi, BH q=%10, OOS replikasyon oranı, en güçlü 30 (+) ve 30 (-) çiftin işlem testi
  2a  yürüyen seçim: her yıl başında önceki 5 yılın taraması, hedef başına en güçlü 5 öncü (|t| >= 3) -> sinyal matrisleri
  2b  yürüyen seçimin havuz testi (dönem dönem, maliyetli)
  3a  grup içinde geride kalan (G1) ve sektör ETF artığı (G1e): ana satırlar
  3b  G1/G1e: maliyet duyarlılığı, alt dönemler, SPY hedge'li sürüm
  4   ETF düzeyinde negatif öncülük: kısmi regresyon + hedge'li test
  5   yabancı seans farkı (ABD kâğıdı - yerel kâğıt)
  6   çürütme testleri (tek hedefli SAĞLAM/KOŞULLU satırlar)
  ozet  sonuclar.csv, ayakta_kalanlar.csv, ozet.json

Kullanım: python3 kod/f2_tarama.py <aşama>     (hepsi: sırayla bütün aşamalar)
"""
import json
import os
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak as o  # noqa: E402
import cift_motoru as cm  # noqa: E402

CIKTI = os.path.join(o.KOK, "ek", "backtest", "f2_tarama")
ARA = os.path.join(CIKTI, "ara")
os.makedirs(ARA, exist_ok=True)
T0 = time.time()

DONEM = [("2005-09", "2005-01-01", "2009-12-31"), ("2010-14", "2010-01-01", "2014-12-31"),
         ("2015-18", "2015-01-01", "2018-12-31"), ("2019-21", "2019-01-01", "2021-12-31"),
         ("2022-23", "2022-01-01", "2023-12-31"), ("2024-26", "2024-01-01", None)]
ON = ["aile", "sinyal_id", "oncu", "hedef", "bicim", "yon", "h", "havuz", "bayat_isaret"]


def log(*a):
    print(f"[{time.time() - T0:6.1f}s]", *a, flush=True)


def jyaz(ad, d):
    json.dump(d, open(os.path.join(ARA, ad), "w"), ensure_ascii=False, indent=1, default=lambda x: float(x) if isinstance(x, (np.floating, np.integer)) else str(x))


def hisse_mi(s):
    m = o.meta()
    return bool(s in m.index and m.loc[s, "tur"] == "EQUITY")


# ----------------------------------------------------------------------------------------------------------------
# Ortak yardımcılar
# ----------------------------------------------------------------------------------------------------------------


def evrenler():
    m = o.meta()
    abd = [s for s in o.abd_semboller(["EQUITY", "ETF"]) if not o.kaldiracli(s)]
    dis = sorted((set(o.grup("dis_hisse")) | set(o.grup("endeks_dis")) | set(o.grup("ek_dis"))) - set(abd))
    hedef = [s for s in abd if str(m.loc[s, "ilk"]) < "2010-01-01"]
    return abd + dis, hedef, dis


def oncu_matrisi():
    """SPY'dan arındırılmış öncü getirileri (ortak.artik_getiri); önbellekli."""
    yol = os.path.join(ARA, "oncu_artik.parquet")
    if os.path.exists(yol):
        return pd.read_parquet(yol)
    oncu, _, _ = evrenler()
    X = pd.DataFrame({s: o.artik_getiri(s) for s in oncu})
    X.to_parquet(yol)
    return X


def ham_oncu_matrisi():
    yol = os.path.join(ARA, "oncu_ham.parquet")
    if os.path.exists(yol):
        return pd.read_parquet(yol)
    oncu, _, _ = evrenler()
    X = pd.DataFrame({s: o.hizali_getiri(s) for s in oncu})
    X.to_parquet(yol)
    return X


def tek_satir(sig, hedef, h, ids, hedge=None):
    """Tek hedefli test satırı (cift_motoru.cift_testi ile aynı kalıp)."""
    d = o.donemli_test(sig, hedef, h, hedge=hedge)
    row = dict(ids)
    row.update(hedef=hedef, h=h, havuz="tek hedef", bayat_isaret=hedef in o.bayat_hedefler(), hedge=hedge or "")
    row.update(d)
    if cm._on_eleme(d):
        row.update(o.ek_olcutler(sig, hedef, h, hedge=hedge))
    row.update(o.son_sinyal(sig))
    return row


def _gunluk(S, h, maliyet=None, giris="kapanis", hedge=None):
    """Gün bazlı eşit ağırlıklı portföy serileri (net ve sürüklenme düzeltilmiş net). ortak.havuz_testi ile aynı
    hesap; E/F/H koşulları için günlük seriye ihtiyaç var (ortak.havuz_gunluk yalnız anormal seriyi verir)."""
    cols = [c for c in S.columns if c in o.panel("adjclose").columns]
    F = o.ileri_getiri(cols, h, giris)
    if hedge:
        fh = o.ileri_getiri([hedge], h, giris)[hedge]
        r = o.basit_getiri(cols + ([hedge] if hedge not in cols else []))
        B = pd.DataFrame({c: o.kayan_beta(r[c], r[hedge]) for c in cols})
        F = F - B.mul(fh, axis=0)
    Sx = S[cols].reindex(F.index).fillna(0.0)
    if maliyet is None:
        C = pd.DataFrame({c: o.maliyet_serisi(c) for c in cols}).reindex(F.index).fillna(20.0) / 1e4
    else:
        C = pd.DataFrame(float(maliyet) / 1e4, index=F.index, columns=cols)
    akt = (Sx != 0) & F.notna()
    k = akt.sum(axis=1)
    net = (Sx * F - C).where(akt)
    abn = (Sx * (F - F.mean()) - C).where(akt)
    return (net.sum(axis=1) / k).where(k > 0), (abn.sum(axis=1) / k).where(k > 0), F, Sx


def havuz_ek(S, h, maliyet=None, hedge=None, n_plasebo=300):
    """Havuz testleri için E, F, H, I koşullarının ölçütleri (gün bazlı portföy serisinden)."""
    p_net, p_abn, F, Sx = _gunluk(S, h, maliyet, "kapanis", hedge)
    out = {}
    v = p_net.dropna()
    if len(v) > 30:
        kalan = v.sort_values(ascending=False).iloc[10:]
        z2 = pd.Series(0.0, index=p_net.index)
        z2[kalan.index] = kalan
        out["tum_net_bps_ust10_haric"] = round(float(kalan.mean()) * 1e4, 1)
        out["tum_t_ust10_haric"] = round(float(o.hac_t(z2.values, lag=h - 1)), 2)
    g = v.groupby(v.index.year)
    yt = pd.DataFrame({"n": g.size(), "m": g.mean()})
    yt = yt[yt["n"] >= 3]
    out["yil_pozitif_oran"] = round(float((yt["m"] > 0).mean()), 2) if len(yt) else np.nan
    out["yil_sayisi"] = int(len(yt))
    ac = o.havuz_testi(S, h, maliyet, "acilis", hedge=hedge)
    er = o.havuz_testi(S, h, maliyet, "ertesi", hedge=hedge)
    out.update(acilis_anormal_bps=ac.get("anormal_net_bps"), acilis_net_bps=ac.get("net_bps"), acilis_t_anormal=ac.get("t_anormal"),
               ertesi_anormal_bps=er.get("anormal_net_bps"), ertesi_t_anormal=er.get("t_anormal"))
    # dairesel plasebo (sinyal matrisinin satırları aynı miktarda kaydırılır; kesit yapısı korunur)
    ilk = int(np.argmax((Sx.values != 0).any(axis=1)))
    A = np.nan_to_num((F - F.mean()).values[ilk:]).astype(np.float32)
    V = F.notna().values[ilk:].astype(np.float32)
    Sv = Sx.values[ilk:].astype(np.float32)

    def stat(Sk):
        num = (Sk * A).sum(axis=1)
        cnt = (np.abs(Sk) * V).sum(axis=1)
        ok = cnt > 0
        return float((num[ok] / cnt[ok]).mean()) if ok.any() else np.nan

    if len(A) > 200:
        gercek = stat(Sv)
        rng = np.random.default_rng(0)
        st = np.array([stat(np.roll(Sv, int(k), axis=0)) for k in rng.integers(60, len(A) - 60, n_plasebo)])
        out["plasebo_p"] = round(float((np.sum(st >= gercek) + 1) / (n_plasebo + 1)), 4)
        out["plasebo_ort_bps"] = round(float(np.nanmean(st)) * 1e4, 2)
    return out


def havuz_satir(S, h, ids, maliyet=None, hedge=None, ek=True):
    d = o.havuz_donemli(S, h, maliyet, hedge=hedge)
    for p in ("tum", "is", "oos", "son"):
        d[f"{p}_n"] = d.get(f"{p}_n_gun", 0)
    row = dict(ids)
    row.update(h=h, havuz="portföy", bayat_isaret=False, hedge=hedge or "")
    row.update(d)
    if ek and cm._on_eleme(d):
        row.update(havuz_ek(S, h, maliyet, hedge))
    son = S.iloc[-1]
    row["son_gun"] = str(S.index[-1].date())
    row["son_sinyal"] = float(son.sum())  # son gün açık pozisyon sayısı (işaretli)
    return row


def bacaklar(S):
    return (("AL", S.clip(lower=0)), ("SAT", S.clip(upper=0)))


def donem_tablosu(S, h, ids, donemler, maliyet=None, hedge=None):
    sat = []
    for ad, b, e in donemler:
        r = o.havuz_testi(S, h, maliyet, "kapanis", b, e, hedge)
        row = dict(ids)
        row.update(h=h, donem=ad, maliyet=("likidite" if maliyet is None else maliyet), hedge=hedge or "")
        row.update(r)
        sat.append(row)
    return sat


def kismi_reg(f, Xd, bas=None, bit=None):
    """f ~ sabit + Xd (z-skorlar, +-5 kırpılmış), White (HC0) t. Dönen: {sütun: (bps/z, t)}."""
    import statsmodels.api as sm

    d = pd.concat([f.rename("f"), Xd], axis=1).dropna()
    if bas is not None:
        d = d[d.index >= bas]
    if bit is not None:
        d = d[d.index <= bit]
    if len(d) < 250:
        return {}
    m = sm.OLS(d["f"], sm.add_constant(d[list(Xd.columns)].clip(-5, 5))).fit(cov_type="HC0")
    out = {c: (round(float(m.params[c]) * 1e4, 2), round(float(m.tvalues[c]), 2)) for c in Xd.columns}
    out["n"] = int(len(d))
    return out


def sinifla(df, tavan=None):
    """cift_motoru.etiketle (öncüye özgü etiketi + sınıf); tavan: en çok KOŞULLU olacak satırlar."""
    df = df.reset_index(drop=True)
    if "yon" not in df.columns:
        df["yon"] = "+"
    df = cm.etiketle(df)
    if tavan is not None:
        t = tavan(df)
        df.loc[t & (df["sinif"] == "SAGLAM"), "sinif"] = "KOSULLU"
    return df


def kaydet(df, ad):
    df = df.copy()
    df["sinyal_id"] = [f"{a}|{x}->{y}|{b}|{yn}|h{h}" for a, x, y, b, yn, h in zip(df.aile, df.oncu, df.hedef, df.bicim, df.yon, df.h)]
    kol = ON + [c for c in df.columns if c not in ON]
    df[kol].to_csv(os.path.join(ARA, ad), index=False)
    return df


# ----------------------------------------------------------------------------------------------------------------
# 1) Körlemesine tarama
# ----------------------------------------------------------------------------------------------------------------


def asama1():
    oncu, hedef, dis = evrenler()
    X = oncu_matrisi()
    log("öncü", X.shape[1], "hedef", len(hedef), "yabancı öncü", len(dis))
    yol = os.path.join(ARA, "tarama_tum.parquet")
    if os.path.exists(yol):
        T = pd.read_parquet(yol)
    else:
        Tis = o.tarama(X, hedef, 1, bit=o.IS_BITIS)
        log("IS tarama", len(Tis))
        Toos = o.tarama(X, hedef, 1, bas=o.OOS_BAS)
        log("OOS tarama", len(Toos))
        T = Tis.merge(Toos, on=["oncu", "hedef"], how="left", suffixes=("_is", "_oos"))
        T.to_parquet(yol)
    T["p_is"] = o.t_to_p(T["t_is"].values)
    T["sec"] = o.bh_fdr(T["p_is"].values, 0.10)
    T["isaret"] = np.sign(T["t_is"])
    T["t_oos_h"] = T["t_oos"] * T["isaret"]  # IS işaretine hizalı OOS t
    bayat = o.bayat_hedefler()
    T["bayat"] = T["hedef"].isin(bayat)
    m = o.meta()
    T["hedef_hisse"] = T["hedef"].map(lambda s: m.loc[s, "tur"] == "EQUITY")
    T["oncu_dis"] = T["oncu"].isin(dis)
    N = len(T)
    oz = {"n_cift": N, "n_oncu": int(T.oncu.nunique()), "n_hedef": int(T.hedef.nunique()),
          "is_|t|>=2": float((T.t_is.abs() >= 2).mean()), "is_|t|>=2.5": float((T.t_is.abs() >= 2.5).mean()),
          "is_t<=-2.5": float((T.t_is <= -2.5).mean()), "is_t>=2.5": float((T.t_is >= 2.5).mean()),
          "oos_|t|>=2.5": float((T.t_oos.abs() >= 2.5).mean()), "oos_t<=-2.5": float((T.t_oos <= -2.5).mean()),
          "oos_t>=2.5": float((T.t_oos >= 2.5).mean()),
          "teorik_|t|>=2.5": float(o.t_to_p(2.5)), "teorik_tek_yon_2.5": float(o.t_to_p(2.5, tek_yon=True)),
          "is_oos_t_korelasyon": float(T[["t_is", "t_oos"]].corr().iloc[0, 1])}
    S = T[T.sec & T.t_oos.notna()].copy()
    oz["bh_secilen"] = int(T.sec.sum())
    oz["bh_secilen_oos_var"] = int(len(S))
    oz["bh_esik_|t|"] = float(T.loc[T.sec, "t_is"].abs().min()) if T.sec.any() else None
    # ikiz, aynı grup ve tezgah üstü (OTC; kapanışı bayat olabilir) bayrakları
    H = ham_oncu_matrisi()
    rh = o.basit_getiri(hedef)
    ana_borsa = {"NYQ", "NMS", "NGM", "NCM", "PCX", "ASE", "BTS", "NAS", "NYS", "TEX"}
    otc_h = sorted(s for s in hedef if str(m.loc[s, "borsa"]) not in ana_borsa)
    oz["otc_hedefler"] = otc_h

    def bayrakla(D):
        D = D.copy()
        D["corr"] = [H[a].corr(rh[b]) for a, b in zip(D.oncu, D.hedef)]
        D["ayni_grup"] = [len(set(str(m.loc[a, "gruplar"]).split(";")) & set(str(m.loc[b, "gruplar"]).split(";"))) > 0 for a, b in zip(D.oncu, D.hedef)]
        D["ikiz"] = D["corr"].abs() > 0.95
        D["otc"] = D["hedef"].isin(otc_h)
        return D

    S = bayrakla(S)
    S["tutan"] = S["t_oos_h"] >= 2.5
    S["p_oos"] = o.t_to_p(S["t_oos_h"].values, tek_yon=True)
    S["bh_oos"] = o.bh_fdr(S["p_oos"].values, 0.10)

    def oran(d):
        return {"n": int(len(d)), "tutan": int(d.tutan.sum()), "oran": round(float(d.tutan.mean()), 4) if len(d) else None,
                "ayni_isaret": round(float((d.t_oos_h > 0).mean()), 3) if len(d) else None,
                "medyan_t_oos_hizali": round(float(d.t_oos_h.median()), 2) if len(d) else None,
                "bh_oos": int(d.bh_oos.sum())}

    oz["replikasyon"] = {
        "hepsi": oran(S), "pozitif": oran(S[S.isaret > 0]), "negatif": oran(S[S.isaret < 0]),
        "bayat_ve_ikiz_haric": oran(S[~S.bayat & ~S.ikiz]),
        "pozitif_bayat_ikiz_haric": oran(S[(S.isaret > 0) & ~S.bayat & ~S.ikiz]),
        "negatif_bayat_ikiz_haric": oran(S[(S.isaret < 0) & ~S.bayat & ~S.ikiz]),
        "hedef_etf": oran(S[~S.hedef_hisse]), "hedef_hisse": oran(S[S.hedef_hisse]),
        "oncu_yabanci": oran(S[S.oncu_dis]), "ayni_grup": oran(S[S.ayni_grup]), "farkli_grup": oran(S[~S.ayni_grup]),
        "ikiz": oran(S[S.ikiz]), "bayat_hedef": oran(S[S.bayat]), "otc_hedef": oran(S[S.otc]),
        "otc_bayat_ikiz_haric": oran(S[~S.otc & ~S.bayat & ~S.ikiz]),
        "pozitif_otc_bayat_ikiz_haric": oran(S[(S.isaret > 0) & ~S.otc & ~S.bayat & ~S.ikiz]),
    }
    oz["secilen_en_sik_hedef"] = S.hedef.value_counts().head(8).to_dict()
    oz["secilen_en_sik_oncu"] = S.oncu.value_counts().head(8).to_dict()
    oz["t_ortalama"] = {"is": round(float(T.t_is.mean()), 3), "oos": round(float(T.t_oos.mean()), 3), "is_std": round(float(T.t_is.std()), 3), "oos_std": round(float(T.t_oos.std()), 3)}
    # şansla beklenen: teorik %0,62; ampirik taban = seçilmeyen çiftlerde IS işaretine hizalı OOS t >= 2,5 oranı
    U = T[~T.sec & T.t_oos.notna()]
    oz["taban_oran"] = {"teorik": float(o.t_to_p(2.5, tek_yon=True)),
                        "secilmeyen_hepsi": float((U.t_oos_h >= 2.5).mean()),
                        "secilmeyen_pozitif": float((U[U.isaret > 0].t_oos_h >= 2.5).mean()),
                        "secilmeyen_negatif": float((U[U.isaret < 0].t_oos_h >= 2.5).mean()),
                        "secilmeyen_|t_is|<1": float((U[U.t_is.abs() < 1].t_oos_h >= 2.5).mean())}
    # |t_IS| dilimine göre replikasyon (seçim eşiğinden bağımsız doz-yanıt)
    T2 = T[T.t_oos.notna()]
    dil = pd.cut(T2.t_is.abs(), [0, 1, 2, 2.5, 3, 3.5, 4, 5, 99])
    oz["dilim"] = {str(k): {"n": int(len(v)), "oos_hizali_t>=2.5": round(float((v.t_oos_h >= 2.5).mean()), 4),
                            "ort_t_oos_hizali": round(float(v.t_oos_h.mean()), 3)} for k, v in T2.groupby(dil, observed=True)}
    # YONTEM bölüm 6 yolu: A (IS |t| >= 2,5) ile seçim, OOS'ta B (hizalı t >= 2,5) ve OOS p değerlerine BH q=%10
    A = T[(T.t_is.abs() >= 2.5) & T.t_oos.notna()].copy()
    A["p_oos"] = o.t_to_p(A["t_oos_h"].values, tek_yon=True)
    A["bh_oos"] = o.bh_fdr(A["p_oos"].values, 0.10)
    A["tutan"] = A["t_oos_h"] >= 2.5
    AB = bayrakla(A[A.tutan])
    pp, pn = float((T.t_is >= 2.5).mean()) * float((T.t_oos >= 2.5).mean()), float((T.t_is <= -2.5).mean()) * float((T.t_oos <= -2.5).mean())
    oz["A_ve_B"] = {"k_A": int(len(A)), "gozlenen": int(len(AB)), "gozlenen_poz": int((AB.isaret > 0).sum()), "gozlenen_neg": int((AB.isaret < 0).sum()),
                    "beklenen_teorik": round(N * 2 * float(o.t_to_p(2.5, tek_yon=True)) ** 2, 1),
                    "beklenen_ampirik_marjinal": round(N * (pp + pn), 1), "beklenen_ampirik_poz": round(N * pp, 1), "beklenen_ampirik_neg": round(N * pn, 1),
                    "bh_oos_gecen": int(A.bh_oos.sum()), "bh_gecenler": [f"{a}->{b}" for a, b in zip(A[A.bh_oos].oncu, A[A.bh_oos].hedef)],
                    "otc_bayat_ikiz_haric": int((~AB.otc & ~AB.bayat & ~AB.ikiz).sum()),
                    "en_sik_hedef": AB.hedef.value_counts().head(10).to_dict(), "en_sik_oncu": AB.oncu.value_counts().head(10).to_dict(),
                    "ayni_grup": int(AB.ayni_grup.sum()), "hedef_hisse": int(AB.hedef_hisse.sum()), "oncu_yabanci": int(AB.oncu_dis.sum())}
    oz["yanlis_pozitif_beklenen_A_ve_B"] = oz["A_ve_B"]["beklenen_teorik"]
    S.sort_values("t_oos_h", ascending=False).to_csv(os.path.join(ARA, "tarama_secilen.csv"), index=False)
    AB.sort_values("t_oos_h", ascending=False).to_csv(os.path.join(CIKTI, "tarama_A_ve_B.csv"), index=False)
    jyaz("ozet1.json", oz)
    log(json.dumps({k: v for k, v in oz.items() if k not in ("dilim",)}, ensure_ascii=False, default=float)[:6000])

    # İşlem testi: (i) ön kayıtlı yol = IS'te BH q=%10 ile seçilip OOS'ta tutanlar (en çok 30 + 30);
    # (ii) keşif = A ve B'yi geçen diğer çiftlerin en güçlü 30 (+) ve 30 (-)'u. İkizler ve ikiz tekrarları hariç.
    C = H.corr(min_periods=250)
    sat, test_edilen = [], set()
    for isr, aile, kaynak in ((1, "F2b+", S[S.tutan]), (-1, "F2b-", S[S.tutan]), (1, "F2b+AB(keşif)", AB), (-1, "F2b-AB(keşif)", AB)):
        c = kaynak[(kaynak.isaret == isr) & ~kaynak.ikiz].sort_values("t_oos_h", ascending=False)
        sec = []
        for r in c.itertuples():
            if (r.oncu, r.hedef) in test_edilen:
                continue
            tekrar = False
            for q in sec:
                if q.hedef == r.hedef and abs(C.loc[q.oncu, r.oncu]) > 0.95:
                    tekrar = True
                if q.oncu == r.oncu and q.hedef in C.index and r.hedef in C.index and abs(C.loc[q.hedef, r.hedef]) > 0.95:
                    tekrar = True
            if not tekrar:
                sec.append(r)
            if len(sec) == 30:
                break
        log(aile, "aday", len(c), "seçilen", len(sec))
        for r in sec:
            test_edilen.add((r.oncu, r.hedef))
            yon = "+" if isr > 0 else "-"
            try:
                rows = cm.cift_testi(r.oncu, r.hedef, yon, bicimler=("B1", "B1r"))
                if r.oncu == "SPY":  # cift_motoru SPY öncüde B1r üretmez: aynı sinyal, SPY ile hedge'li ileri getiri
                    z = o.zskor(o.hizali_getiri("SPY"), 60)
                    sg = (isr * np.sign(z).where(z.abs() >= 1, 0.0)).fillna(0.0)
                    rows += [tek_satir(sg, r.hedef, h, {"oncu": "SPY", "bicim": "B1r", "yon": yon}, hedge="SPY") for h in (1, 2, 3)]
            except Exception as e:  # noqa: BLE001
                log("HATA", r.oncu, r.hedef, type(e).__name__, str(e)[:80])
                continue
            # öncüye özgü mü: hedge'li ileri getiri ~ z(öncü artığı) + z(hedef SPY artığı) + z(hedef getirisi)
            rr = o.basit_getiri([r.hedef, "SPY"])
            rt, spy = rr[r.hedef], rr["SPY"]
            Xd = pd.DataFrame({"zx": o.zskor(X[r.oncu], 60), "zs": o.zskor(rt - o.kayan_beta(rt, spy) * spy, 60), "zr": o.zskor(rt, 60)})
            if r.oncu == "SPY":
                Xd = Xd.drop(columns=["zr"])
            f = o._ileri(r.hedef, 1, "kapanis", "SPY")
            ki = kismi_reg(f, Xd, bit=o.IS_BITIS).get("zx", (np.nan, np.nan))[1]
            ko = kismi_reg(f, Xd, bas=o.OOS_BAS).get("zx", (np.nan, np.nan))[1]
            for row in rows:
                row.update(aile=aile, tarama_t_is=round(r.t_is, 2), tarama_t_oos=round(r.t_oos, 2), tarama_bh_oos=bool(r.bh_oos),
                           corr=round(r.corr, 3), ayni_grup=bool(r.ayni_grup), otc=bool(r.otc), kismi_t_is=ki, kismi_t_oos=ko)
                sat.append(row)
    df = pd.DataFrame(sat)
    df = sinifla(df, tavan=lambda d: d.aile.str.startswith("F2b-") & d.hedef.map(hisse_mi))
    # B koşulunun BH kısmı: taramada IS'ten seçilen BÜTÜN çiftlerin OOS p değerleri üzerinden (30'luk liste OOS'a bakılarak seçildi)
    df.loc[(df.sinif == "SAGLAM") & ~df.tarama_bh_oos, "sinif"] = "KOSULLU"
    # Tezgah üstü (OTC) hedefin kapanışı bayattır: esas alınan giriş ertesi açılıştır (YONTEM bölüm 3). Açılış girişinde
    # sürüklenme düzeltilmiş net <= 0 ise sinyal işlenemez -> ELENDİ.
    df["bayat_isaret"] = df["bayat_isaret"] | df["otc"]
    bayat_duser = df["otc"] & ~(pd.to_numeric(df.get("acilis_anormal_bps"), errors="coerce") > 0) & (df["sinif"] != "ELENDI")
    df["not"] = np.where(bayat_duser, "bayat OTC kapanışı: ertesi açılış girişinde etki yok (kural sınıfı: " + df["sinif"] + ")", "")
    df.loc[bayat_duser, "sinif"] = "ELENDI"
    df = kaydet(df, "satir_1.csv")
    g = ["aile", "oncu", "hedef", "bicim", "h", "tum_n", "tum_anormal_net_bps", "tum_net_bps", "is_t_anormal", "oos_t_anormal", "son_net_bps",
         "tum_net_bps_al", "acilis_anormal_bps", "tarama_t_is", "tarama_t_oos", "kismi_t_oos", "otc", "ozgu", "sinif", "son_sinyal"]
    log(df[df.sinif != "ELENDI"][g].to_string())
    log("aşama 1 sınıflar:", df.groupby(["aile", "bicim"]).sinif.value_counts().unstack(fill_value=0).to_string())


# ----------------------------------------------------------------------------------------------------------------
# 2) Yürüyen seçim
# ----------------------------------------------------------------------------------------------------------------


def asama2a():
    oncu, hedef, dis = evrenler()
    X = oncu_matrisi()
    Z = X.apply(lambda c: o.zskor(c, 60)).clip(-5, 5)
    Zf = Z.fillna(0.0)
    tk = o.takvim()
    parca = {"tum": [], "poz": [], "neg": []}
    ist, onceki, son_liste = [], None, None
    for Y in range(2012, 2027):
        gun = tk[tk.year == Y - 1]
        bit = str(gun[-2].date())  # son günün ileri getirisi yıl Y'ye taşar; bir gün erken kes
        T = o.tarama(X, hedef, 1, bas=f"{Y - 5}-01-01", bit=bit)
        T["a"] = T["t"].abs()
        T = T[T.a >= 3].sort_values("a", ascending=False).groupby("hedef").head(5)
        cift = set(zip(T.oncu, T.hedef))
        ist.append({"yil": Y, "hedef_sayisi": int(T.hedef.nunique()), "cift": len(T), "negatif_pay": round(float((T.t < 0).mean()), 3),
                    "onceki_yilla_ortak_pay": round(len(cift & onceki) / max(len(cift), 1), 3) if onceki is not None else np.nan,
                    "ort_|t|": round(float(T.a.mean()), 2)})
        onceki = cift
        W = T.assign(s=np.sign(T.t)).pivot(index="oncu", columns="hedef", values="s").fillna(0.0)
        pencere = slice(f"{Y - 1}-09-01", f"{Y}-12-31")
        Zs = Zf.loc[pencere, W.index]
        for ad, Wv in (("tum", W), ("poz", W.clip(lower=0)), ("neg", W.clip(upper=0))):
            k = (Wv != 0).sum()
            comp = pd.DataFrame(Zs.values @ Wv.values, index=Zs.index, columns=W.columns) / k.where(k > 0)
            zc = comp.apply(lambda c: o.zskor(c, 60))
            sig = np.sign(zc).where(zc.abs() >= 1, 0.0).fillna(0.0).loc[str(Y)]
            parca[ad].append(sig)
            if ad == "tum" and Y == 2026:
                son = pd.DataFrame({"sinyal": sig.iloc[-1], "z": zc.iloc[-1].round(2)})
                son["oncüler"] = [";".join(f"{a}({'+' if s > 0 else '-'})" for a, s in W[c][W[c] != 0].items()) for c in son.index]
                son_liste = son[son.sinyal != 0].sort_values("z")
        log("yıl", Y, ist[-1])
    for ad, pl in parca.items():
        S = pd.concat(pl).reindex(tk).fillna(0.0)
        S.to_parquet(os.path.join(ARA, f"yuruyen_S_{ad}.parquet"))
    pd.DataFrame(ist).to_csv(os.path.join(CIKTI, "yuruyen_secim_istatistik.csv"), index=False)
    son_liste.to_csv(os.path.join(CIKTI, "yuruyen_son_gun.csv"))


def asama2b():
    S = {ad: pd.read_parquet(os.path.join(ARA, f"yuruyen_S_{ad}.parquet")) for ad in ("tum", "poz", "neg")}
    etf = [c for c in S["tum"].columns if not hisse_mi(c)]
    his = [c for c in S["tum"].columns if hisse_mi(c)]
    var = {"YS-tum": S["tum"], "YS-poz(keşif)": S["poz"], "YS-neg(keşif)": S["neg"], "YS-tum-ETF(keşif)": S["tum"][etf], "YS-tum-hisse(keşif)": S["tum"][his]}
    don = [("2012-14", "2012-01-01", "2014-12-31")] + DONEM[2:]
    sat, dt = [], []
    for ad, Sv in var.items():
        for h in (1, 2, 3):
            for yon, Sb in bacaklar(Sv):
                sat.append(havuz_satir(Sb, h, {"aile": "F2b-yuruyen", "oncu": "yürüyen seçim (5 yıl, en iyi 5, |t|>=3)", "hedef": f"{Sv.shape[1]} hedef", "bicim": ad, "yon": yon}))
            dt += donem_tablosu(Sv, h, {"bicim": ad}, don)
        log(ad, "bitti")
    for h in (1, 2, 3):  # piyasadan arındırılmış sürüm (sağlamlık)
        for yon, Sb in bacaklar(S["tum"]):
            sat.append(havuz_satir(Sb, h, {"aile": "F2b-yuruyen", "oncu": "yürüyen seçim (5 yıl, en iyi 5, |t|>=3)", "hedef": f"{S['tum'].shape[1]} hedef", "bicim": "YS-tum-SPYhedge", "yon": yon}, hedge="SPY"))
    log("hedge bitti")
    tumu = [("2012-26", "2012-01-01", None), ("IS 2012-18", "2012-01-01", o.IS_BITIS), ("OOS 2019-26", o.OOS_BAS, None)]
    for ad in ("tum", "poz", "neg"):  # maliyetsiz (brüt) tablo: sinyalin maliyet öncesi içeriği var mı?
        dt += donem_tablosu(S[ad], 1, {"bicim": f"YS-{ad}"}, tumu + don, maliyet=0)
        dt += donem_tablosu(S[ad], 1, {"bicim": f"YS-{ad}"}, tumu, maliyet=0, hedge="SPY")
    df = pd.DataFrame(sat)
    hisse_iceren = ~df.bicim.str.contains("ETF")
    df = o.siniflandir(df, tavan_kosullu=(df.yon == "AL") & hisse_iceren)
    kaydet(df, "satir_2.csv")
    pd.DataFrame(dt).to_csv(os.path.join(CIKTI, "yuruyen_donem.csv"), index=False)
    log(df[["bicim", "yon", "h", "tum_n", "tum_anormal_net_bps", "tum_net_bps", "is_t_anormal", "oos_t_anormal", "son_net_bps", "sinif"]].to_string())


# ----------------------------------------------------------------------------------------------------------------
# 3) Grup içinde geride kalan
# ----------------------------------------------------------------------------------------------------------------

GRUP_ETF = {"h_altin_gumus": "GDX", "h_bakir_celik_aluminyum": "XME", "h_banka_bolgesel": "KRE", "h_banka_buyuk": "XLF",
            "h_boru_lng": "XLE", "h_cin_adr": "FXI", "h_denizcilik": "IYT", "h_diger_adr": "EEM", "h_dogalgaz": "XOP",
            "h_donanim_ag": "XLK", "h_fintech_kripto": "XLF", "h_gyo": "IYR", "h_ilac_biyotek": "XLV", "h_internet_medya": "FDN",
            "h_kamu_hizmet": "XLU", "h_kimya_gubre": "XLB", "h_komur": "XME", "h_konut": "ITB", "h_lityum_nadir": "XME",
            "h_makine_sanayi": "XLI", "h_medikal_hizmet": "XLV", "h_nukleer_guc": "XLU", "h_oto_ev": "XLY",
            "h_perakende_tuketim": "XRT", "h_petrol_entegre_ep": "XLE", "h_petrol_hizmet": "OIH", "h_rafineri": "XLE",
            "h_savunma_havacilik": "ITA", "h_seyahat": "XLY", "h_sigorta_borsa": "KIE", "h_tasimacilik": "IYT",
            "h_tematik_yuksek_beta": "QQQ", "h_temel_tuketim": "XLP", "h_temiz_enerji": "PBW", "h_yapi_orman": "XHB",
            "h_yariiletken": "SMH", "h_yazilim": "IGV"}


def geride_kalan_sinyalleri():
    yol = os.path.join(ARA, "g1_sinyal.pkl")
    if os.path.exists(yol):
        return pd.read_pickle(yol)
    m = o.meta()
    gr = {}
    for s in o.abd_semboller("EQUITY"):
        g = [x for x in str(m.loc[s, "gruplar"]).split(";") if x.startswith("h_")]
        if g and s in o.panel("adjclose").columns:
            gr[s] = g[0]
    hs = sorted(gr)
    R = o.basit_getiri(hs)
    R = R.where(R.abs() < 0.8)  # YONTEM 2.2: hissede |günlük getiri| > %80 bozuk veri sayılır
    G = pd.DataFrame(np.nan, index=R.index, columns=hs)
    gs = pd.Series(gr)
    for g, ss in gs.groupby(gs):
        ss = list(ss.index)
        sub = R[ss]
        n = sub.notna().sum(axis=1)
        G[ss] = (-sub).add(sub.sum(axis=1), axis=0).div((n - 1).where(n > 2), axis=0)
    gap = G - R

    def kantil(gp):
        q = gp.rank(axis=1, pct=True).where(gp.notna().sum(axis=1) >= 100, axis=0)
        return ((q > 0.8).astype(float) - (q <= 0.2).astype(float)).where(gp.notna(), 0.0)

    S = kantil(gap)
    dv = (o.panel("close", hs) * o.panel("volume", hs)).rolling(60, min_periods=20).median().shift(1)
    likit = dv.ge(dv.median(axis=1), axis=0)
    az = dv.lt(dv.median(axis=1), axis=0)
    zg = G.apply(lambda c: o.zskor(c, 60))
    buyuk = zg.abs() > 2
    etf = {s: GRUP_ETF[gr[s]] for s in hs}
    re = o.basit_getiri(sorted(set(etf.values())))
    gapE = pd.DataFrame({s: o.kayan_beta(R[s], re[etf[s]]) * re[etf[s]] - R[s] for s in hs})
    out = {"G1": S, "G1-likit": S.where(likit, 0.0), "G1-azlikit": S.where(az, 0.0), "G1-buyukhareket": S.where(buyuk, 0.0),
           "G1e": kantil(gapE), "_grup": gs, "_gap": gap.iloc[-1], "_gapE": gapE.iloc[-1]}
    pd.to_pickle(out, yol)
    return out


def asama3a():
    sv = geride_kalan_sinyalleri()
    log("sinyaller hazır", {k: int((v != 0).values.sum()) for k, v in sv.items() if not k.startswith("_")})
    sat = []
    for ad in ("G1", "G1-likit", "G1-azlikit", "G1-buyukhareket", "G1e"):
        for h in (1, 2, 3):
            for yon, Sb in bacaklar(sv[ad]):
                sat.append(havuz_satir(Sb, h, {"aile": "F2-geride", "oncu": "grup (kendisi hariç)" if ad != "G1e" else "sektör ETF'i", "hedef": f"{Sb.shape[1]} hisse", "bicim": ad, "yon": yon}))
        log(ad, "bitti")
    df = pd.DataFrame(sat)
    df = o.siniflandir(df, tavan_kosullu=(df.yon == "AL"))
    kaydet(df, "satir_3a.csv")
    log(df[["bicim", "yon", "h", "tum_n", "tum_anormal_net_bps", "tum_net_bps", "is_t_anormal", "oos_t_anormal", "oos_anormal_net_bps", "son_net_bps", "sinif"]].to_string())
    # son gün listesi
    S, gs = sv["G1"], sv["_grup"]
    son = pd.DataFrame({"grup": gs, "G1": S.iloc[-1], "gap_bps": (sv["_gap"] * 1e4).round(0), "G1e": sv["G1e"].iloc[-1], "gapE_bps": (sv["_gapE"] * 1e4).round(0)})
    son[(son.G1 != 0) | (son.G1e != 0)].sort_values("gap_bps", ascending=False).to_csv(os.path.join(CIKTI, "geride_kalan_son_gun.csv"))


def asama3b():
    sv = geride_kalan_sinyalleri()
    md, dt, sat = [], [], []
    for ad in ("G1", "G1e"):
        for h in (1, 2, 3):
            for c in (5, 10, 20):
                d = o.havuz_donemli(sv[ad], h, c)
                md.append({"bicim": ad, "h": h, "maliyet_bps": c, **{k: v for k, v in d.items() if k.split("_", 1)[0] in ("tum", "is", "oos", "son")}})
            dt += donem_tablosu(sv[ad], h, {"bicim": ad}, DONEM)
            dt += donem_tablosu(sv[ad], h, {"bicim": ad}, DONEM, maliyet=0)
        log(ad, "maliyet ve dönem bitti")
    pd.DataFrame(md).to_csv(os.path.join(CIKTI, "geride_kalan_maliyet.csv"), index=False)
    pd.DataFrame(dt).to_csv(os.path.join(CIKTI, "geride_kalan_donem.csv"), index=False)
    for h in (1, 3):
        for yon, Sb in bacaklar(sv["G1"]):
            sat.append(havuz_satir(Sb, h, {"aile": "F2-geride", "oncu": "grup (kendisi hariç)", "hedef": f"{Sb.shape[1]} hisse", "bicim": "G1-SPYhedge", "yon": yon}, hedge="SPY"))
        log("hedge h", h)
    df = pd.DataFrame(sat)
    df = o.siniflandir(df, tavan_kosullu=(df.yon == "AL"))
    kaydet(df, "satir_3b.csv")
    log(df[["bicim", "yon", "h", "tum_n", "tum_anormal_net_bps", "is_t_anormal", "oos_t_anormal", "son_net_bps", "sinif"]].to_string())


# ----------------------------------------------------------------------------------------------------------------
# 4) ETF düzeyinde negatif öncülük
# ----------------------------------------------------------------------------------------------------------------

CIFT4 = [("SPY", "IWM"), ("QQQ", "IWM"), ("XLF", "KRE"), ("SPY", "IJR"), ("SPY", "XBI")]


def asama4():
    sat, kiyas, km = [], [], []
    for L, F in CIFT4:
        for row in cm.cift_testi(L, F, "-", bicimler=("B1", "B1r")):
            row.update(aile="F2e-neg", hedge="SPY" if row["bicim"] == "B1r" else "")
            sat.append(row)
        rr = o.basit_getiri([L, F])
        rl, rt = rr[L], rr[F]
        zl = o.zskor(o.hizali_getiri(L), 60)
        sig = (-np.sign(zl).where(zl.abs() >= 1, 0.0)).fillna(0.0)
        e = rt - o.kayan_beta(rt, rl) * rl
        ze, zt = o.zskor(e, 60), o.zskor(rt, 60)
        sig_e = (-np.sign(ze).where(ze.abs() >= 1, 0.0)).fillna(0.0)
        sig_t = (-np.sign(zt).where(zt.abs() >= 1, 0.0)).fillna(0.0)
        for h in (1, 2, 3):
            sat.append(tek_satir(sig, F, h, {"aile": "F2e-neg", "oncu": L, "bicim": "B1-oncuHedge", "yon": "-"}, hedge=L))
            kiyas.append(tek_satir(sig, L, h, {"aile": "KIYAS", "oncu": L, "bicim": "oncu-kendi-donus", "yon": "-"}))
            kiyas.append(tek_satir(sig_t, F, h, {"aile": "KIYAS", "oncu": F, "bicim": "hedef-kendi-donus", "yon": "-"}))
            kiyas.append(tek_satir(sig_e, F, h, {"aile": "KIYAS", "oncu": f"{F}-b*{L}", "bicim": "hedef-artik-donus-oncuHedge", "yon": "-"}, hedge=L))
        # kısmi regresyon (h=1): toplam etki, ayrıştırma, öncüyle hedge'li hedef
        f_ham, f_hed = o._ileri(F, 1, "kapanis"), o._ileri(F, 1, "kapanis", L)
        for dn, b, en in (("IS", None, o.IS_BITIS), ("OOS", o.OOS_BAS, None), ("SON", o.SON_BAS, None)):
            m1 = kismi_reg(f_ham, pd.DataFrame({"z_oncu": zl}), b, en)
            m2 = kismi_reg(f_ham, pd.DataFrame({"z_oncu": zl, "z_hedef_artik": ze}), b, en)
            m3 = kismi_reg(f_hed, pd.DataFrame({"z_oncu": zl, "z_hedef_artik": ze}), b, en)
            km.append({"oncu": L, "hedef": F, "donem": dn, "n": m1.get("n"),
                       "M1_oncu_bps": m1["z_oncu"][0], "M1_oncu_t": m1["z_oncu"][1],
                       "M2_oncu_bps": m2["z_oncu"][0], "M2_oncu_t": m2["z_oncu"][1], "M2_hedefartik_bps": m2["z_hedef_artik"][0], "M2_hedefartik_t": m2["z_hedef_artik"][1],
                       "M3_oncu_bps": m3["z_oncu"][0], "M3_oncu_t": m3["z_oncu"][1], "M3_hedefartik_bps": m3["z_hedef_artik"][0], "M3_hedefartik_t": m3["z_hedef_artik"][1]})
        log(L, F, "bitti")
    df = sinifla(pd.DataFrame(sat))
    kd = o.siniflandir(pd.DataFrame(kiyas))
    kd["ozgu"] = False
    kaydet(pd.concat([df, kd], ignore_index=True), "satir_4.csv")
    K = pd.DataFrame(km)
    K.to_csv(os.path.join(CIKTI, "etf_negatif_kismi.csv"), index=False)
    log(K.to_string())
    al = pd.concat([df, kd])
    log(al[["aile", "oncu", "hedef", "bicim", "h", "tum_n", "tum_anormal_net_bps", "tum_net_bps", "is_t_anormal", "oos_t_anormal", "son_net_bps", "sinif"]].to_string())


# ----------------------------------------------------------------------------------------------------------------
# 5) Yabancı seans farkı
# ----------------------------------------------------------------------------------------------------------------

CIFT5 = [("BABA", "9988.HK", None), ("TSM", "2330.TW", None), ("BHP", "BHP.AX", "FXA"), ("RIO", "RIO.AX", "FXA"),
         ("ASML", "ASML.AS", "FXE"), ("SHEL", "SHEL.L", "FXB"), ("FXI", "^HSI", None), ("EWJ", "^N225", "FXY"),
         ("EWG", "^GDAXI", "FXE"), ("EWT", "^TWII", None), ("EWY", "^KS11", None)]


def asama5():
    sat, tn = [], []
    spy = o.basit_getiri(["SPY"])["SPY"]
    for adr, yerel, fx in CIFT5:
        xl = o.hizali_getiri(yerel)
        x = xl + (o.hizali_getiri(fx) if fx else 0.0)
        et = f"{yerel}+{fx}" if fx else yerel
        for row in cm.cift_testi(yerel, adr, "+", x=x, etiket=et, bicimler=("B2",)):
            row.update(aile="F2y-B2", hedge="")
            sat.append(row)
        r = o.hizali_getiri(adr)
        rs = o.basit_getiri([adr])[adr]
        e = r - x                                  # ABD kâğıdı - yerel kâğıt (dolar cinsinden yaklaşık), aynı NYSE günü
        ze = o.zskor(e, 60)
        prim = e.cumsum()                          # ABD kapanışındaki prim düzeyi (ABD seansında yerel kapanıştan sonraki hareket)
        sap = prim - prim.rolling(60, min_periods=40).mean().shift(1)
        zp = o.zskor(sap, 60)
        f = o._ileri(adr, 1, "kapanis", "SPY")
        kont = {"zs": o.zskor(rs - o.kayan_beta(rs, spy) * spy, 60), "zr": o.zskor(rs, 60)}
        for bic, z, aile in (("D1-fark", ze, "F2y-fark"), ("D2-prim", zp, "F2y-prim(keşif)")):
            sig = (-np.sign(z).where(z.abs() >= 1, 0.0)).fillna(0.0)
            kt = {dn: kismi_reg(f, pd.DataFrame({"zx": z, **kont}), b, en).get("zx", (np.nan, np.nan))[1]
                  for dn, b, en in (("tum", None, None), ("is", None, o.IS_BITIS), ("oos", o.OOS_BAS, None))}
            for h in (1, 2, 3):
                row = tek_satir(sig, adr, h, {"aile": aile, "oncu": et, "bicim": bic, "yon": "-"})
                row.update(b2_kismi_t=-kt["tum"], kismi_t_is=-kt["is"], kismi_t_oos=-kt["oos"])
                sat.append(row)
        d = pd.DataFrame({"r": r, "xl": xl, "x": x, "e": e, "f1": r.shift(-1)}).dropna()
        tn.append({"abd": adr, "yerel": yerel, "kur_etf": fx or "", "ilk_gun": str(d.index[0].date()), "n": len(d),
                   "corr_abd_yerel_ayni_gun": round(d.r.corr(d.xl), 3), "std_fark_kursuz_bps": round((d.r - d.xl).std() * 1e4, 0),
                   "std_fark_kurlu_bps": round(d.e.std() * 1e4, 0), "corr_fark_ertesi_abd": round(d.e.corr(d.f1), 3),
                   "corr_abd_ertesi_abd": round(d.r.corr(d.f1), 3), "son_gun_fark_z": round(float(ze.dropna().iloc[-1]), 2),
                   "son_gun_prim_z": round(float(zp.dropna().iloc[-1]), 2)})
        log(adr, yerel, "bitti")
    df = sinifla(pd.DataFrame(sat), tavan=lambda d: d.hedef.map(hisse_mi))
    kaydet(df, "satir_5.csv")
    T = pd.DataFrame(tn)
    T.to_csv(os.path.join(CIKTI, "yabanci_seans_tanim.csv"), index=False)
    log(T.to_string())
    log(df[["aile", "oncu", "hedef", "bicim", "h", "tum_n", "tum_anormal_net_bps", "tum_net_bps", "is_t_anormal", "oos_t_anormal", "son_net_bps", "b2_kismi_t", "ozgu", "sinif"]].to_string())


# ----------------------------------------------------------------------------------------------------------------
# 6) Çürütme testleri (YONTEM bölüm 7): tek hedefli SAĞLAM/KOŞULLU satırlar için sağlamlık varyantları (yeni hipotez değil)
# ----------------------------------------------------------------------------------------------------------------


def asama6():
    d = pd.read_csv(os.path.join(ARA, "satir_1.csv"))
    k = d[d.sinif.isin(["SAGLAM", "KOSULLU"])]
    vix = o.panel("adjclose", ["^VIX"])["^VIX"].shift(1)  # bir önceki günün VIX kapanışı (16:15 ileri bakışı olmasın)
    tk = o.takvim()
    kriz = pd.Series(((tk >= "2008-09-01") & (tk <= "2009-06-30")) | ((tk >= "2020-02-01") & (tk <= "2020-04-30")), index=tk)
    al = ["tum_n", "tum_net_bps", "tum_anormal_net_bps", "tum_t_anormal", "is_t_anormal", "oos_t_anormal", "oos_anormal_net_bps", "son_n", "son_net_bps",
          "tum_net_bps_al", "tum_anormal_bps_al", "tum_net_bps_sat"]
    sat = []
    for (oncu, hedef, yon, bicim), g in k.groupby(["oncu", "hedef", "yon", "bicim"]):
        rr = o.basit_getiri([hedef, "SPY"])
        r, spy = rr[hedef], rr["SPY"]
        x = o.hizali_getiri(oncu).reindex(r.index)
        sig, hd = cm.sinyaller(x, r, yon, spy if oncu != "SPY" else None)[bicim]
        yz = 1.0 if yon == "+" else -1.0
        z = o.zskor(x, 60) if bicim == "B1" else o.zskor(x - o.kayan_beta(x, spy) * spy, 60)
        zs, zt = o.zskor(o.hizali_getiri("SPY"), 60), o.zskor(r, 60)
        s_spy = (yz * np.sign(zs).where(zs.abs() >= 1, 0.0)).fillna(0.0)
        var = {"ana": sig,
               "esik |z|>=1,5": (yz * np.sign(z).where(z.abs() >= 1.5, 0.0)).fillna(0.0),
               "sinir haric |z|>=1,2": (yz * np.sign(z).where(z.abs() >= 1.2, 0.0)).fillna(0.0),
               "oncu 1 gun gecikmeli": sig.shift(1).fillna(0.0),
               "kriz haric": sig.where(~kriz.reindex(sig.index).fillna(False), 0.0),
               "VIX>20": sig.where(vix.reindex(sig.index) > 20, 0.0), "VIX<=20": sig.where(vix.reindex(sig.index) <= 20, 0.0),
               "oncu yerine SPY": s_spy,
               "oncu sinyali var, SPY sinyali yok": sig.where(s_spy.reindex(sig.index) == 0, 0.0),
               "hedefin kendi donusu": (-np.sign(zt).where(zt.abs() >= 1, 0.0)).fillna(0.0)}
        for h in sorted(g.h.unique()):
            ids = {"oncu": oncu, "hedef": hedef, "bicim": bicim, "yon": yon, "h": int(h), "hedge": hd or ""}
            for ad, sg in var.items():
                dt = o.donemli_test(sg, hedef, int(h), hedge=hd)
                sat.append({**ids, "varyant": ad, **{c: dt.get(c) for c in al}})
            dt = o.donemli_test(sig, hedef, int(h), maliyet_bps=o.maliyet_serisi(hedef) * 2, hedge=hd)
            sat.append({**ids, "varyant": "maliyet 2 kat", **{c: dt.get(c) for c in al}})
            for gr in ("acilis", "ertesi"):
                dt = o.donemli_test(sig, hedef, int(h), giris=gr, hedge=hd)
                sat.append({**ids, "varyant": f"giris={gr}", **{c: dt.get(c) for c in al}})
            yt = o.yillik_tablo(sig, hedef, int(h))
            sat.append({**ids, "varyant": "en iyi yil haric (toplam %)", "tum_n": int(yt["n"].sum()),
                        "tum_net_bps": round(float((yt["toplam_yuzde"].sum() - yt["toplam_yuzde"].max()) * 100 / max(yt["n"].sum() - yt.loc[yt["toplam_yuzde"].idxmax(), "n"], 1)), 1),
                        "not": f"en iyi yil {int(yt['toplam_yuzde'].idxmax())}: {yt['toplam_yuzde'].max()}%; pozitif yil {int((yt.net_bps > 0).sum())}/{len(yt)}"})
    C = pd.DataFrame(sat)
    C.to_csv(os.path.join(CIKTI, "curutme.csv"), index=False)
    log(C.to_string())


# ----------------------------------------------------------------------------------------------------------------
# Özet
# ----------------------------------------------------------------------------------------------------------------


def ozet():
    par = [pd.read_csv(os.path.join(ARA, f)) for f in ("satir_1.csv", "satir_2.csv", "satir_3a.csv", "satir_3b.csv", "satir_4.csv", "satir_5.csv") if os.path.exists(os.path.join(ARA, f))]
    df = pd.concat(par, ignore_index=True)
    if "not" not in df.columns:
        df["not"] = ""
    df["not"] = df["not"].fillna("")
    # YONTEM bölüm 6: piyasadan arındırılmış testte tutmayan öncü-hedef sinyali "piyasa dönüşü"dür, lead-lag sayılmaz
    ay = df.aile.astype(str).str.startswith("F2b") & (df.sinif != "ELENDI") & ~(df.ozgu.astype(str) == "True")
    m1, m2 = ay & (df.bicim == "B1"), ay & (df.bicim == "B1r")
    df.loc[m1, "not"] = (df.loc[m1, "not"] + " öncüye özgü değil (arındırılmış B1r testinde IS ve OOS t >= 2 yok): piyasa dönüşü sayılır, lead-lag değil.").str.strip()
    df.loc[m2, "not"] = (df.loc[m2, "not"] + " arındırılmış testte IS ve OOS t >= 2 birlikte sağlanmıyor: öncüye özgü etiketi yok.").str.strip()
    tv = df.aile.astype(str).str.startswith("F2b-AB") & (df.sinif == "KOSULLU") & (df.get("k_B", False).astype(str) == "True")
    df.loc[tv, "not"] = (df.loc[tv, "not"] + " Tavan: taramadaki OOS BH'yi geçmiyor ve hisse düzeyi ters (dönüş türü) sinyal; en çok KOŞULLU.").str.strip()
    kesif = df.aile.astype(str).str.contains("keşif") | df.bicim.astype(str).str.contains("keşif")
    df.loc[kesif & (df.sinif != "ELENDI"), "not"] = (df.loc[kesif & (df.sinif != "ELENDI"), "not"] + " Keşif: çift hem IS hem OOS'a bakılarak seçildi (kazananın laneti); kullanılamaz.").str.strip()
    kol = ON + [c for c in df.columns if c not in ON]
    df[kol].to_csv(os.path.join(CIKTI, "sonuclar.csv"), index=False)
    hip = df[(df.aile != "KIYAS")]
    ak = hip[hip.sinif != "ELENDI"].copy()
    ak["sira"] = ak.sinif.map({"SAGLAM": 0, "KOSULLU": 1, "IZLE": 2})
    ak = ak.sort_values(["sira", "oos_t_anormal"], ascending=[True, False]).drop(columns="sira")
    ilk = ON + ["sinif", "k_A", "k_B", "k_B_zayif", "bh_oos", "k_C", "k_D", "k_E", "k_F", "k_G", "k_H", "k_I", "son_gun", "son_sinyal",
                "tum_n", "tum_anormal_net_bps", "tum_net_bps", "is_t_anormal", "oos_t_anormal", "oos_anormal_net_bps", "son_net_bps", "ozgu", "not"]
    ilk = [c for c in ilk if c in ak.columns]
    ak[ilk + [c for c in ak.columns if c not in ilk]].to_csv(os.path.join(CIKTI, "ayakta_kalanlar.csv"), index=False)
    o1 = json.load(open(os.path.join(ARA, "ozet1.json"))) if os.path.exists(os.path.join(ARA, "ozet1.json")) else {}
    n_tar = o1.get("n_cift", 0)
    n_islem = int(len(hip))
    oz = {"tarama_cift": n_tar, "islem_testi": n_islem, "kiyas_satiri": int((df.aile == "KIYAS").sum()), "toplam_test": n_tar + n_islem,
          "beklenen_yp_tarama_A_ve_B": o1.get("yanlis_pozitif_beklenen_A_ve_B"),
          "beklenen_yp_islem_saglam": round(n_islem * o.P_SIFIR_SAGLAM, 3), "beklenen_yp_islem_kosullu": round(n_islem * o.P_SIFIR_KOSULLU, 3),
          "sinif_aile": hip.groupby("aile").sinif.value_counts().unstack(fill_value=0).to_dict("index"),
          "sinif_toplam": hip.sinif.value_counts().to_dict()}
    json.dump(oz, open(os.path.join(CIKTI, "ozet.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(oz, ensure_ascii=False, indent=1))
    g = ["aile", "oncu", "hedef", "bicim", "yon", "h", "tum_n", "tum_anormal_net_bps", "tum_net_bps", "is_t_anormal", "oos_t_anormal", "son_net_bps", "ozgu", "sinif", "son_sinyal"]
    pd.set_option("display.width", 250)
    print(ak[[c for c in g if c in ak.columns]].to_string(index=False))


ASAMA = {"1": asama1, "2a": asama2a, "2b": asama2b, "3a": asama3a, "3b": asama3b, "4": asama4, "5": asama5, "6": asama6, "ozet": ozet}

if __name__ == "__main__":
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", 40)
    pd.set_option("display.max_rows", 400)
    sec = sys.argv[1:] or ["hepsi"]
    for a in (list(ASAMA) if sec == ["hepsi"] else sec):
        log("=== aşama", a)
        ASAMA[a]()
    log("bitti")
