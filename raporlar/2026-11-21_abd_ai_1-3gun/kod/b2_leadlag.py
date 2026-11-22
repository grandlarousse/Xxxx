"""B2 — lead-lag aileleri (PROTOKOL.md madde 9, B2 listesi: 27 birincil test + LL6 ayrı havuz).

Çalıştırma (çalışma dizininden bağımsız):  python kod/b2_leadlag.py
Çıktılar veri/sonuc/: B2_sonuc.csv, B2_islemler.csv, B2_rejim.csv, B2_ekonomi.csv, B2_tasima.csv,
B2_tarama.csv (LL6), B2_zaman.csv (zaman damgası doğrulaması), B2_tani_LL2dusus.csv, B2_tani_acik.csv,
B2_ozet.md (d2_b2.md tabloları).

Zaman kuralı (madde 2.3): sinyal t kapanışında bilinen veriyle. Asya/Avrupa: aynı takvim günü t
yerel barı (ortak.hizala, gecikme 0; yerel tatilde NaN = sinyal yok). =F, =X, DX-Y.NYB: t-1 barı
(ortak.hizala gecikme 1). BTC-USD: takvim günü t-1 barı (00:00 UTC'de kapanan, t-1 akşamı ET),
son kullanılan bardan bu yana birikimli (Pazartesi = Cuma+Cumartesi+Pazar barları; Pazartesi olay
tanımıyla aynı). VIX ailesi (yalnız LL6): t barı; sağ kalan t-1 ile yeniden sınanır.
"""
from __future__ import annotations
import sys
import time
import warnings
from pathlib import Path
import numpy as np
import pandas as pd

KOD = Path(__file__).resolve().parent
sys.path.insert(0, str(KOD))
import ortak as o  # noqa: E402

AJAN = "B2"
T = o.TK()
C = o.evren("Ç")
TEV = o.evren("T")
YENI = o.evren("YENİ")
ARAC = o.evren("ARAÇ")
LIDER = ["NVDA", "TSM", "AVGO", "MU", "MSFT", "GOOGL", "META", "AMZN"]
SEPET = {
    "cip": "NVDA AMD AVGO MRVL TSM INTC ARM QCOM MPWR",
    "ekipman": "ASML AMAT LRCX KLAC TER ONTO CAMT",
    "bellek": "MU SNDK WDC STX P NTAP",
    "ag": "ANET CRDO ALAB COHR LITE CIEN AAOI FN",
    "altyapi": "CLS SMCI DELL HPE VRT ETN GEV BE VST CEG OKLO",
    "yazilim": "ORCL PLTR APP MSFT GOOGL META AMZN AAPL TSLA SNOW NOW CRM ADBE",
    "neocloud": "CRWV NBIS IREN CIFR WULF APLD CORZ",
}
SEPET = {k: v.split() for k, v in SEPET.items()}
UYE = {c: s for s, l in SEPET.items() for c in l}
BTC_HEDEF = ["IREN", "CIFR", "WULF", "APLD", "CORZ", "WGMI"]
VIX_AILE = {"^VIX", "^VIX3M", "^VIX9D", "^VVIX"}
SEVIYE_FARK = {"^TNX", "^IRX"}       # getiri yerine seviye değişimi (faiz)
P23 = pd.Timestamp("2020-01-01")
KESIF = (pd.Timestamp("2010-01-01"), pd.Timestamp("2023-12-29"))
DOGRU = (pd.Timestamp("2024-01-02"), pd.Timestamp("2026-11-20"))
PERM = 500
warnings.filterwarnings("ignore", category=RuntimeWarning)


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


# ---------------------------------------------------------------- yardımcılar
def zskor(X, pencere=60):
    """ortak.zskor ile aynı tanım (t değeri, t-1'e kadarki 60 GEÇERLİ gözlemin ort./std'si), ancak
    boşluklu serilerde (yerel tatil, vadeli/kur boşlukları) çalışır. ortak.zskor rolling(60,
    min_periods=60) ABD satırları üzerinden sayar; pencerede tek NaN varsa sonuç NaN olur (yabancı
    serilerde z'nin ~%92'si kayboluyordu). Boşluksuz seride ikisi özdeştir."""
    if isinstance(X, pd.DataFrame):
        return pd.DataFrame({c: zskor(X[c], pencere) for c in X.columns})
    s = X.dropna()
    mu = s.rolling(pencere, min_periods=pencere).mean().shift(1)
    sd = s.rolling(pencere, min_periods=pencere).std().shift(1)
    return ((s - mu) / sd).reindex(X.index)


def yay(s, kodlar):
    """Tarih serisini (T) kod sütunlarına yay."""
    s = s.reindex(T)
    return pd.DataFrame(np.repeat(s.values[:, None], len(kodlar), 1), index=T, columns=kodlar)


def r_abd(kodlar):
    return o._gunluk_ham(list(kodlar))            # bps, ABD takvimi (salt okuma)


def rol_artik(y, x, pencere=250, en_az=120):
    """y_t - (a + b x_t); a, b t-1'e kadarki 'pencere' günlük OLS (t'de bilinir)."""
    ok = y.notna() & x.notna()
    yy, xx = y.where(ok), x.where(ok)
    cov = xx.rolling(pencere, min_periods=en_az).cov(yy).shift(1)
    var = xx.rolling(pencere, min_periods=en_az).var().shift(1)
    b = cov / var
    a = yy.rolling(pencere, min_periods=en_az).mean().shift(1) - b * xx.rolling(pencere, min_periods=en_az).mean().shift(1)
    return y - (a + b * x)


def btc_t1(kod="BTC-USD"):
    """ABD günü D için: (D-1 takvim günü barının kapanışı) / (önceki ABD günü - 1 takvim günü barının
    kapanışı) - 1. Bar 00:00 UTC'de kapanır -> D-1 akşamı ET; D kapanışında kesin bilinir."""
    s = o.yukle(kod)["AClose"].dropna()
    s.index = pd.to_datetime(s.index).normalize()
    t = T
    son = s.reindex(t - pd.Timedelta(days=1)).values
    once = s.reindex(pd.DatetimeIndex(pd.Series(t).shift(1)) - pd.Timedelta(days=1)).values
    return pd.Series(son / once - 1, index=t)


def btc_pazartesi(kod="BTC-USD"):
    """ABD Pazartesi günleri: Perşembe barı kapanışı -> Pazar barı kapanışı getirisi."""
    s = o.yukle(kod)["AClose"].dropna()
    s.index = pd.to_datetime(s.index).normalize()
    pzt = T[T.dayofweek == 0]
    v = s.reindex(pzt - pd.Timedelta(days=1)).values / s.reindex(pzt - pd.Timedelta(days=4)).values - 1
    return pd.Series(v, index=pzt).reindex(T)


def boot_ar(x, tarih, n=2000, seed=0):
    """Giriş tarihine göre küme yeniden örneklemeli %90 aralık."""
    if len(x) < 2:
        return np.nan, np.nan
    rng = np.random.default_rng(seed)
    d = pd.Series(x).groupby(pd.DatetimeIndex(tarih)).agg(["sum", "count"])
    s, c = d["sum"].values, d["count"].values
    i = rng.integers(0, len(d), (n, len(d)))
    m = s[i].sum(1) / c[i].sum(1)
    return np.percentile(m, 5), np.percentile(m, 95)


# ---------------------------------------------------------------- öncül serileri (t'de bilinen)
def ll1_oncul(oncul_kodlari, hedefler):
    loc = pd.concat([o.hizala(k) for k in oncul_kodlari], axis=1)
    yerel = loc.mean(axis=1, skipna=False) * 1e4          # hepsi işlem görmeli (yerel tatilde sinyal yok)
    grup_t1 = r_abd(hedefler).mean(axis=1, skipna=False).shift(1)   # hedef grubunun t-1 getirisi
    return rol_artik(yerel, grup_t1)


def lider_z():
    ra = o._gunluk_tur(LIDER, "artik")                    # r - beta(t-1) * r_SMH, t'de bilinir
    return zskor(ra)


def sepet_dis(kodlar, gun=1):
    """Her kod için kendi sepetinin kendisi hariç eşit ağırlıklı getirisi (bps); gun=3: t-2..t birikimli."""
    tum = sorted({c for c in UYE})
    R = r_abd(tum) / 1e4
    if gun > 1:
        R = np.exp(np.log1p(R).rolling(gun, min_periods=gun).sum()) - 1
    out = {}
    for c in kodlar:
        uy = [u for u in SEPET[UYE[c]] if u != c]
        sub = R[uy]
        n = sub.notna().sum(1)
        out[c] = (sub.mean(1).where(n >= 2)) * 1e4
    return pd.DataFrame(out)


def ll3c_sinyal(kodlar):
    tum = sorted({c for c in UYE})
    R = r_abd(tum)
    bx = sepet_dis(tum)
    d = R - bx
    S = pd.DataFrame(False, index=T, columns=tum)
    G = pd.DataFrame(np.nan, index=T, columns=tum)
    for s, uy in SEPET.items():
        dd = d[uy]
        q = dd.quantile(1 / 3, axis=1)
        S[uy] = (bx[uy] >= 200) & dd.le(q, axis=0) & dd.notna()
        G[uy] = -dd
    return S.reindex(columns=kodlar), G.reindex(columns=kodlar)


def hyg_artik():
    r = r_abd(["HYG", "SPY"])
    return rol_artik(r["HYG"], r["SPY"])


def tepki_olay(liderler, esik):
    """Liderin bilanço tepki günü getirisi (ham, bps) >= esik (esik>0) ya da <= esik (esik<0)."""
    R = r_abd(liderler)
    out = {}
    for L in liderler:
        tp = pd.DatetimeIndex(o.bilanco(L)["tepki"]).intersection(T)
        v = pd.Series(np.nan, index=T)
        v[tp] = R.loc[tp, L]
        out[L] = v
    return pd.DataFrame(out)


# ---------------------------------------------------------------- test tanımları
def tanimlar():
    """Her test: dict(id, aile, varyant, kaynak, getiri, bilanco, yon, tip, havuz, x(kodlar) / s(kodlar),
    tasinir: YENİ/ARAÇ'a uygulanabilir mi; seri: zaman doğrulaması için öncül serisi."""
    D = []
    ll1 = [("a", ["2330.TW"], ["TSM", "NVDA", "SMH"]), ("b", ["000660.KS", "005930.KS"], ["MU", "WDC", "STX"]),
           ("c", ["8035.T", "ASML.AS"], ["AMAT", "LRCX", "KLAC"]), ("d", ["6857.T"], ["TER", "NVDA"]),
           ("e", ["9984.T"], ["ORCL"])]
    for v, onc, hed in ll1:
        z = zskor(ll1_oncul(onc, hed))
        D.append(dict(id=f"LL1{v}_h1", aile="LL1", varyant=v, kaynak="lit", getiri="ham", bilanco=True, yon=1,
                      tip="egim", havuz=hed, evren="karma", z=z, oncul="+".join(onc),
                      notu=f"{'+'.join(onc)} yerel t artığı (hedef grubu t-1'e göre, 250g OLS t-1'e kadar) -> {' '.join(hed)}"))
    zL = lider_z()
    for L in LIDER:
        D.append(dict(id=f"LL2_{L}_h1", aile="LL2", varyant=L, kaynak="lit", getiri="artik", bilanco=True, yon=1,
                      tip="egim", havuz=[c for c in C if c != L], evren="C", z=zL[L], oncul=L,
                      notu=f"lider {L} artık getiri z'si -> lider dışı Ç"))

    def ll2_olay(kodlar, yon):
        S = pd.DataFrame(False, index=T, columns=kodlar)
        G = pd.DataFrame(np.nan, index=T, columns=kodlar)
        for c in kodlar:
            zz = zL[[L for L in LIDER if L != c]]
            S[c] = (zz >= 2).any(axis=1) if yon > 0 else (zz <= -2).any(axis=1)
            G[c] = zz.max(axis=1) if yon > 0 else zz.min(axis=1)
        return S, G
    D.append(dict(id="LL2olay_al_h1", aile="LL2", varyant="olay_al", kaynak="lit", getiri="artik", bilanco=True,
                  yon=1, tip="olay", havuz=list(C), evren="C", s=lambda k: ll2_olay(k, 1),
                  notu="herhangi bir liderin (kendisi hariç) artık z >= +2 -> al"))
    D.append(dict(id="LL2olay_uzak_h1", aile="LL2", varyant="olay_uzak", kaynak="lit", getiri="artik", bilanco=True,
                  yon=-1, tip="olay", havuz=list(C), evren="C", s=lambda k: ll2_olay(k, -1),
                  notu="herhangi bir liderin (kendisi hariç) artık z <= -2 -> uzak dur"))
    C3 = [c for c in C if c in UYE]
    D.append(dict(id="LL3a_h1", aile="LL3", varyant="a", kaynak="lit", getiri="artik", bilanco=True, yon=1, tip="egim",
                  havuz=C3, evren="C", zf=lambda k: zskor(sepet_dis(k, 1)), oncul="sepet_t",
                  notu="kendisi hariç sepet t getirisi z'si"))
    D.append(dict(id="LL3b_h1", aile="LL3", varyant="b", kaynak="lit", getiri="artik", bilanco=True, yon=1, tip="egim",
                  havuz=C3, evren="C", zf=lambda k: zskor(sepet_dis(k, 3)), oncul="sepet_3g",
                  notu="kendisi hariç sepet 3 günlük (t-2..t) getirisi z'si"))
    D.append(dict(id="LL3c_h1", aile="LL3", varyant="c", kaynak="lit", getiri="artik", bilanco=True, yon=1, tip="olay",
                  havuz=C3, evren="C", s=ll3c_sinyal,
                  notu="sepet (kendisi hariç) >= +%2 iken r - sepet farkı sepet içi alt üçte birde -> al"))
    q = ["QQQ", "SMH"]
    l4 = [("TNX", o.hizala("^TNX", getiri=False).diff(), "^TNX seviye değişimi, t barı"),
          ("DXY", o.hizala("DX-Y.NYB"), "DX-Y.NYB getirisi, t-1 barı"),
          ("JPY", o.hizala("JPY=X"), "JPY=X getirisi, t-1 barı"),
          ("HG", o.hizala("HG=F"), "HG=F getirisi, t-1 barı"),
          ("HYG", hyg_artik(), "HYG'nin SPY'a göre artığı (250g beta t-1'e kadar), t")]
    for v, s, n in l4:
        D.append(dict(id=f"LL4_{v}_h1", aile="LL4", varyant=v, kaynak="turev", getiri="ham", bilanco=True, yon=1,
                      tip="egim", havuz=q, evren="T", z=zskor(s), oncul=v, notu=n + " -> QQQ+SMH"))
    zb = zskor(btc_t1()).where(T >= P23)
    D.append(dict(id="LL4_BTC_h1", aile="LL4", varyant="BTC", kaynak="turev", getiri="ham", bilanco=True, yon=1,
                  tip="egim", havuz=BTC_HEDEF, evren="BTC_istisna", z=zb, oncul="BTC-USD",
                  notu="BTC-USD t-1 takvim barı (birikimli) z'si -> madenci/neocloud, P2-P3"))
    pz = btc_pazartesi().where(T >= P23)
    D.append(dict(id="LL4_BTCpzt_h1", aile="LL4", varyant="BTCpzt", kaynak="turev", getiri="ham", bilanco=True, yon=1,
                  tip="olay", havuz=BTC_HEDEF, evren="BTC_istisna",
                  s=lambda k: ((yay(pz, k) >= 0.05), yay(pz, k)),
                  notu="Pazartesi: BTC Perşembe barı -> Pazar barı >= +%5 -> Pazartesi kapanışında al, P2-P3"))
    L5 = LIDER + ["ASML"]
    for v, esik, yon in (("al", 300, 1), ("uzak", -300, -1)):
        def f(k, esik=esik):
            E = tepki_olay(L5, esik)
            S = pd.DataFrame(False, index=T, columns=k)
            G = pd.DataFrame(np.nan, index=T, columns=k)
            for c in k:
                e = E[[L for L in L5 if L != c]]
                S[c] = (e >= esik).any(axis=1) if esik > 0 else (e <= esik).any(axis=1)
                G[c] = e.max(axis=1) if esik > 0 else e.min(axis=1)
            return S, G
        D.append(dict(id=f"LL5_{v}_h1", aile="LL5", varyant=v, kaynak="lit", getiri="artik", bilanco=False, yon=yon,
                      tip="olay", havuz=list(C), evren="C", s=f,
                      notu=f"lider (LL2 + ASML) bilanço tepki günü getirisi {'>= +%3 -> al' if yon > 0 else '<= -%3 -> uzak dur'}; lider dışı Ç"))
    return D


def X_of(d, kodlar):
    if "zf" in d:
        return d["zf"](kodlar)
    return yay(d["z"], kodlar)


def sinyal_of(d, kodlar):
    if d["tip"] == "egim":
        X = X_of(d, kodlar)
        return X >= 1, X
    return d["s"](kodlar)


# ---------------------------------------------------------------- ana akış
def kos_birincil(D):
    sat, isl_hep, rj_hep, ek_hep, kayit = [], [], [], [], {}
    for d in D:
        t0 = time.time()
        k = d["havuz"]
        S, G = sinyal_of(d, k)
        isl = o.islemler(S, h=1, getiri=d["getiri"], bilanco_at=d["bilanco"], guc=G, test_id=d["id"], yon=d["yon"])
        eg = eg_ac = None
        if d["tip"] == "egim":
            X = X_of(d, k)
            eg = o.egim_testi(X, getiri=d["getiri"], h=1, bilanco_at=d["bilanco"], perm=PERM)
            eg_ac = o.egim_testi(X, getiri=d["getiri"], h=1, cikis="acilis", bilanco_at=d["bilanco"], perm=0)
        r = o.test(isl, egim=eg, test_id=d["id"], ajan=AJAN, aile=d["aile"], varyant=d["varyant"], birincil=1,
                   kaynak=d["kaynak"], evren=d["evren"], h=1, cikis="kapanis", getiri_turu=d["getiri"], yon=d["yon"],
                   notu=d["notu"], perm=PERM)
        if eg_ac is not None:
            r.update(egim_acilis_bps=eg_ac["egim_bps"], t_egim_acilis=eg_ac["t_egim"])
        r["t_birincil"] = r["t_egim"] if eg is not None else r["t_kume"]
        sat.append(r)
        isl_hep.append(isl)
        rj = o.rejim(isl)
        rj_hep.append(rj)
        kayit[d["id"]] = (d, isl, r, rj)
        if d["yon"] > 0 and np.isfinite(r["t_birincil"]) and abs(r["t_birincil"]) >= 2:
            arac = "havuz" if len(k) > 1 else k[0]
            e = o.ekonomi(isl, arac, t_stat=r["t_kume"])
            e.insert(0, "test_id", d["id"]) if "test_id" not in e else None
            ek_hep.append(e)
        log(d["id"], f"n={r['n_islem']} alfa={r['alfa_bps']:.1f} t_kume={r['t_kume']:.2f}",
            f"egim={r.get('egim_bps', np.nan):.2f} t_egim={r.get('t_egim', np.nan):.2f}", f"{time.time()-t0:.0f}s")
    return sat, isl_hep, rj_hep, ek_hep, kayit


def zaman_dogrulama(D):
    """Her eğim öncülü: kullanılan hizalama, 1 gün İLERİ (geleceğe bakış: t+1 değeri) ve 1 gün geri."""
    rows = []
    for d in D:
        if d["tip"] != "egim":
            continue
        X = X_of(d, d["havuz"])
        for ad, Xs in (("kullanilan", X), ("ileri_1g_gelecek", X.shift(-1)), ("geri_1g", X.shift(1))):
            e = o.egim_testi(Xs, getiri=d["getiri"], h=1, bilanco_at=d["bilanco"], perm=0)
            rows.append(dict(test_id=d["id"], oncul=d.get("oncul"), kaydirma=ad, egim_bps=e["egim_bps"],
                             t_egim=e["t_egim"], n_gozlem=e["n_gozlem"]))
    z = pd.DataFrame(rows)
    p = z.pivot(index="test_id", columns="kaydirma", values="t_egim")
    z["patlama_orani"] = z["test_id"].map((p["ileri_1g_gelecek"].abs() / p["kullanilan"].abs()).to_dict())
    return z


def tasima(kayit):
    rows = []
    for tid, (d, isl0, r, _) in kayit.items():
        if not (d["yon"] > 0 and np.isfinite(r["t_birincil"]) and abs(r["t_birincil"]) >= 2):
            continue
        for ev_ad, ev in (("YENİ", YENI), ("ARAÇ", ARAC)):
            k = [c for c in ev if c in UYE] if d["aile"] == "LL3" else list(ev)
            if d["aile"] == "LL3" and ev_ad == "ARAÇ":
                rows.append(dict(test_id=tid, evren=ev_ad, n_islem=0, not_="ARAÇ sepet üyesi değil: uygulanamaz"))
                continue
            if d["id"].startswith("LL4_BTC"):
                k = [c for c in k if c not in BTC_HEDEF]
            if not k:
                continue
            S, G = sinyal_of(d, k)
            if d["id"].startswith("LL4_BTC"):
                S = S.where(np.repeat((S.index >= P23)[:, None], S.shape[1], 1), False)
            isl = o.islemler(S, h=1, getiri=d["getiri"], bilanco_at=d["bilanco"], guc=G, test_id=tid)
            gruplar = [(ev_ad, isl)]
            if ev_ad == "ARAÇ":
                gruplar.append(("ARAÇ_uzun", isl[isl["kod"].map(lambda c: o.KALDIRAC.get(c, 1) > 0)]))
                gruplar += [(f"ARAÇ:{c}", isl[isl["kod"] == c]) for c in sorted(isl["kod"].unique())]
            for g_ad, x in gruplar:
                if len(x) == 0:
                    rows.append(dict(test_id=tid, evren=g_ad, n_islem=0))
                    continue
                lo, hi = boot_ar(x["alfa_bps"].values, x["giris"].values)
                rr = dict(test_id=tid, evren=g_ad, n_islem=len(x), n_gun=x["giris"].nunique(), n_arac=x["kod"].nunique(),
                          ort_bps=x["getiri_bps"].mean(), alfa_bps=x["alfa_bps"].mean(), ar05_bps=lo, ar95_bps=hi,
                          maliyet_bps=x["maliyet_bps"].mean(), alfa_net_bps=(x["alfa_bps"] - x["maliyet_bps"]).mean(),
                          isabet=(x["getiri_bps"] > 0).mean(), alfa_ham_bps=x["alfa_ham_bps"].mean())
                dn = o._donem_no(x["giris"])
                dog = []
                for p_, pa in enumerate(["P1", "P2", "P3"]):
                    m = dn == p_
                    rr[f"alfa_{pa}"], rr[f"n_{pa}"] = (x.loc[m, "alfa_bps"].mean() if m.any() else np.nan), int(m.sum())
                    dog.append(m.sum() >= 50 and rr[f"alfa_{pa}"] > 0)
                s12 = x["giris"] >= o.SON12_BAS
                rr["alfa_son12"], rr["n_son12"] = x.loc[s12, "alfa_bps"].mean() if s12.any() else np.nan, int(s12.sum())
                k1 = rr["n_islem"] >= 100 and rr["n_gun"] >= 60
                k3 = rr["alfa_net_bps"] > 0
                k4 = bool(dog[2] and sum(dog) >= 2)
                rr.update(kural_1=k1, kural_3=k3, kural_4=k4,
                          kural_sonuc=("GÜÇSÜZ" if not k1 else ("uyumlu(1,3,4)" if k3 and k4 else "uyumsuz")))
                rows.append(rr)
    return pd.DataFrame(rows).rename(columns={"not_": "not"})


def tani_ll2_dusus():
    """Tanı (birincil=0): herhangi bir liderin artık z <= -2 SONRASI takipçilerin t+1..t+3 getirisi (AL olarak)."""
    zL = lider_z()
    S = pd.DataFrame(False, index=T, columns=C)
    G = pd.DataFrame(np.nan, index=T, columns=C)
    for c in C:
        zz = zL[[L for L in LIDER if L != c]]
        S[c] = (zz <= -2).any(axis=1)
        G[c] = zz.min(axis=1)
    rows, rj = [], []
    for h in (1, 2, 3):
        for g in ("ham", "artik"):
            tid = f"LL2dusus_tani_{g}_h{h}"
            isl = o.islemler(S, h=h, getiri=g, bilanco_at=True, guc=G, test_id=tid)
            r = o.test(isl, test_id=tid, ajan=AJAN, aile="LL2tani", varyant=f"dusus_{g}", birincil=0, kaynak="lit",
                       evren="C", h=h, cikis="kapanis", getiri_turu=g, yon=1, perm=0, ikincil=(h == 1),
                       notu="tanı: lider düşüş şoku (z<=-2) sonrası takipçiyi AL; betimsel")
            rows.append(r)
            x = o.rejim(isl, n_boot=1000)
            x["h"], x["getiri"] = h, g
            rj.append(x)
    # SMH / SOXL / NVDA tarih düzeyi (lider düşüş şoku günleri, NVDA lider olduğunda kendisi hariç)
    return pd.DataFrame(rows), pd.concat(rj, ignore_index=True)


def acik_sinyaller(D):
    """20.11.2026 kapanışı: her birincil testte sinyal koşulu açık olan kodlar (filtre öncesi koşul;
    uygunluk ayrıca)."""
    gun = T[-1]
    rows = []
    U = None
    for d in D:
        k = d["havuz"]
        S, G = sinyal_of(d, k)
        s = S.loc[gun]
        acik = [c for c in k if bool(s.get(c, False))]
        uy = o.uygun(k).loc[gun]
        bil = o._bilanco_maske(k, 1)[-1] if d["bilanco"] else np.zeros(len(k), bool)
        ok = [c for j, c in enumerate(k) if c in acik and uy[c] and not bil[j]]
        gv = G.loc[gun]
        deger = (f"z={float(X_of(d, k).loc[gun].iloc[0]):.2f}" if d["tip"] == "egim" and "z" in d
                 else (f"guc_max={np.nanmax(gv.values):.2f}" if np.isfinite(gv.values.astype(float)).any() else "değer yok"))
        rows.append(dict(test_id=d["id"], yon=("al" if d["yon"] > 0 else "uzak dur"), tarih=str(gun.date()),
                         n_acik=len(acik), n_acik_uygun=len(ok), kodlar=" ".join(ok[:40]), deger=deger))
    return pd.DataFrame(rows)


def ll6():
    """43 öncül x (Ç, T), 1 gün gecikmeli eğim (öncülün t'de bilinen değerinin z'si -> t..t+1 artık)."""
    sys.path.insert(0, str(KOD))
    from indir import ONCUL
    havuzlar = {"C": list(C), "T": [c for c in TEV if c != "SMH"]}   # SMH artığı özdeş sıfır: atıldı
    rows = []

    def seri(k, gecikme):
        if k in SEVIYE_FARK:
            return o.hizala(k, getiri=False, gecikme=gecikme).diff()
        if k == "BTC-USD" or k == "ETH-USD":
            return btc_t1(k) if gecikme else o.hizala(k, gecikme=0)
        return o.hizala(k, gecikme=gecikme)

    def bir(k, gec, zaman):
        z = zskor(seri(k, gec))
        for ev, kod in havuzlar.items():
            X = yay(z, kod)
            for asama, (b, s) in (("kesif", KESIF), ("dogrulama", DOGRU)):
                m = (T >= b) & (T <= s)
                Xp = X.where(np.repeat(m[:, None], X.shape[1], 1))
                ortak = int((z.reindex(T)[m].notna() & r_abd(kod)[m].notna().any(axis=1)).sum())
                e = o.egim_testi(Xp, getiri="artik", h=1, perm=0)
                eh = o.egim_testi(Xp, getiri="ham", h=1, perm=0)
                rows.append(dict(test_id=f"LL6_{k}_{ev}_{asama}" + ("" if zaman == "std" else "_t1"), ajan=AJAN,
                                 aile="LL6", varyant=f"{k}|{ev}" + ("" if zaman == "std" else "|t1"), birincil=0,
                                 kaynak="turev", evren=ev, h=1, cikis="kapanis", getiri_turu="artik", asama=asama,
                                 oncul=k, zaman=("t-1 barı" if gec else "t barı"), n_ortak_gun=ortak,
                                 n_gozlem=e["n_gozlem"], egim_bps=e["egim_bps"], se_egim_bps=e["se_egim_bps"],
                                 t_egim=e["t_egim"], p_birincil=e["p_egim"], egim_ham_bps=eh["egim_bps"],
                                 t_egim_ham=eh["t_egim"]))
    for k in ONCUL:
        gec = 0 if k in VIX_AILE else (1 if k in o.SONRA_KAPANAN or k.endswith(("=F", "=X")) else 0)
        bir(k, gec, "std")
    L = pd.DataFrame(rows)
    L["ayni_isaret_ham"] = np.sign(L["egim_bps"]) == np.sign(L["egim_ham_bps"])
    kes = L[(L.asama == "kesif")].copy()
    uygun_ = kes["n_ortak_gun"] >= 750
    kes["q_bh"] = np.nan
    kes["kesif_gecti"] = False
    q, red = o.bh_fdr(kes.loc[uygun_, "p_birincil"].values, 0.10)
    kes.loc[uygun_, "q_bh"], kes.loc[uygun_, "kesif_gecti"] = q, red
    dog = L[L.asama == "dogrulama"].set_index("varyant")
    gec = kes[kes.kesif_gecti]
    v = []
    for _, r in gec.iterrows():
        dd = dog.loc[r["varyant"]]
        t_tek = np.sign(r["t_egim"]) * dd["t_egim"]
        v.append(dict(varyant=r["varyant"], dog_t_tek=t_tek, dog_p_tek=o._st.norm.sf(t_tek) if np.isfinite(t_tek) else np.nan))
    V = pd.DataFrame(v, columns=["varyant", "dog_t_tek", "dog_p_tek"])
    V["dog_q"], V["dogrulandi"] = np.nan, False
    if len(V):
        V["dog_q"] = o.bh_fdr(V["dog_p_tek"].fillna(1).values, 0.10)[0]
        V["dogrulandi"] = (V["dog_t_tek"] >= 2) & (V["dog_q"] <= 0.10)
    L = L.merge(kes[["varyant", "q_bh", "kesif_gecti"]], on="varyant", how="left").merge(V, on="varyant", how="left")
    # VIX ailesi sağ kalan: t-1 ile yeniden
    sag = L[(L.asama == "kesif") & (L.dogrulandi == True) & L.oncul.isin(VIX_AILE)]["oncul"].unique()
    ek = []
    if len(sag):
        rows.clear()
        for k in sag:
            bir(k, 1, "t1")
        ek = pd.DataFrame(rows)
        L = pd.concat([L, ek], ignore_index=True)
    oz = dict(n_cift=int(len(kes)), n_cift_750=int(uygun_.sum()), kesif_gecen=int(kes.kesif_gecti.sum()),
              sansla_beklenen=0.10 * int(kes.kesif_gecti.sum()), sansla_beklenen_tum=0.10 * int(uygun_.sum()),
              dogrulanan=int(V["dogrulandi"].sum()) if len(V) else 0,
              dogrulanan_ciftler=list(V.loc[V["dogrulandi"], "varyant"]) if len(V) else [],
              vix_t1_yeniden=list(sag))
    return L, oz


def ozet_md(sat, rj, tas, zam, tani, tani_rj, acik, L, oz):
    S = pd.DataFrame(sat)
    R = pd.concat(rj, ignore_index=True)
    b = R[R.hucre == "BUGUN"].set_index("test_id")
    st = R[R.hucre == "STRES"].set_index("test_id")
    f = lambda v, n=1: "" if pd.isna(v) else f"{v:.{n}f}"
    out = ["| test_id | yön | n_islem | alfa_bps | t_kume | eğim bps/z (t_egim) | alfa_net_bps | alfa_acilis_bps | eğim_açılış (t) | P1 / P2 / P3 alfa | son 12 ay alfa (n) | STRES ort (n, ep) | BUGÜN ort (n_islem, n_epizot) | ön etiket |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for _, r in S.iterrows():
        e, kont, nt = o._etiket(r.fillna({"q_bh": np.nan}), True, None)
        bb = b.loc[r.test_id] if r.test_id in b.index else None
        ss = st.loc[r.test_id] if r.test_id in st.index else None
        bug = "" if bb is None or bb.n_islem == 0 else f"{f(bb.ortalama_bps)} ({int(bb.n_islem)}, {int(bb.n_epizot)})"
        stx = "" if ss is None or ss.n_islem == 0 else f"{f(ss.ortalama_bps)} ({int(ss.n_islem)}, {int(ss.n_epizot)})"
        eg = "" if pd.isna(r.get("egim_bps")) else f"{f(r.egim_bps, 2)} ({f(r.t_egim, 2)})"
        ega = "" if pd.isna(r.get("egim_acilis_bps")) else f"{f(r.egim_acilis_bps, 2)} ({f(r.t_egim_acilis, 2)})"
        out.append(f"| {r.test_id} | {'al' if r.yon > 0 else 'uzak'} | {int(r.n_islem)} | {f(r.alfa_bps)} | {f(r.t_kume, 2)} | {eg} | "
                   f"{f(r.alfa_net_bps)} | {f(r.alfa_acilis_bps)} | {ega} | {f(r.alfa_P1)} / {f(r.alfa_P2)} / {f(r.alfa_P3)} | "
                   f"{f(r.alfa_son12)} ({int(r.n_son12) if pd.notna(r.n_son12) else ''}) | {stx} | {bug} | {e} [{kont}] |")
    out += ["", "**Zaman damgası doğrulaması (t_egim; 'ileri' = öncülün t+1 değeri = geleceğe bakış):**", "",
            "| test_id | kullanılan | 1 gün ileri (gelecek) | 1 gün geri |", "|---|---|---|---|"]
    p = zam.pivot(index="test_id", columns="kaydirma", values="t_egim")
    for tid in p.index:
        out.append(f"| {tid} | {f(p.loc[tid, 'kullanilan'], 2)} | {f(p.loc[tid, 'ileri_1g_gelecek'], 2)} | {f(p.loc[tid, 'geri_1g'], 2)} |")
    out += ["", "**Tanı (a): lider düşüş şoku (z ≤ −2) sonrası takipçiyi AL (birincil=0):**", "",
            "| test_id | n_islem | alfa_bps | t_kume (betimsel) | ham ort_bps | STRES ort (n, ep) | BUGÜN ort (n, ep) |", "|---|---|---|---|---|---|---|"]
    for _, r in tani.iterrows():
        x = tani_rj[(tani_rj.test_id == r.test_id)]
        sx = x[x.hucre == "STRES"].iloc[0]
        bx = x[x.hucre == "BUGUN"].iloc[0]
        g = lambda z: "" if z.n_islem == 0 else f"{f(z.ortalama_bps)} ({int(z.n_islem)}, {int(z.n_epizot)})"
        out.append(f"| {r.test_id} | {int(r.n_islem)} | {f(r.alfa_bps)} | {f(r.t_kume, 2)} | {f(r.ort_bps)} | {g(sx)} | {g(bx)} |")
    out += ["", "**Tanı (b): 20.11.2026 kapanışında açık sinyaller:**", "", "| test_id | yön | değer | n açık (uygun) | kodlar |", "|---|---|---|---|---|"]
    for _, r in acik.iterrows():
        out.append(f"| {r.test_id} | {r.yon} | {r.deger} | {r.n_acik} ({r.n_acik_uygun}) | {r.kodlar} |")
    out += ["", "**Taşıma (YENİ / ARAÇ, havuz satırları):**", "", "| test_id | evren | n_islem | alfa_bps [%90] | alfa_net | P3 alfa | kural |", "|---|---|---|---|---|---|---|"]
    for _, r in tas[~tas.evren.astype(str).str.startswith("ARAÇ:")].iterrows():
        if not r.n_islem:
            out.append(f"| {r.test_id} | {r.evren} | 0 | | | | {r.get('not', '')} |")
            continue
        out.append(f"| {r.test_id} | {r.evren} | {int(r.n_islem)} | {f(r.alfa_bps)} [{f(r.ar05_bps)}, {f(r.ar95_bps)}] | {f(r.alfa_net_bps)} | {f(r.alfa_P3)} | {r.kural_sonuc} |")
    out += ["", f"**LL6:** {oz}", ""]
    kk = L[(L.asama == "kesif") & (L.kesif_gecti == True)]
    if len(kk):
        out += ["| çift | keşif eğim (t) | q | doğrulama eğim (t) | doğrulandı |", "|---|---|---|---|---|"]
        dg = L[L.asama == "dogrulama"].set_index("varyant")
        for _, r in kk.sort_values("t_egim").iterrows():
            d = dg.loc[r.varyant]
            out.append(f"| {r.varyant} | {f(r.egim_bps, 2)} ({f(r.t_egim, 2)}) | {f(r.q_bh, 3)} | {f(d.egim_bps, 2)} ({f(d.t_egim, 2)}) | {r.dogrulandi} |")
    return "\n".join(out)


def main():
    t0 = time.time()
    D = tanimlar()
    assert len(D) == 27, len(D)
    log("birincil testler:", len(D))
    sat, isl, rj, ek, kayit = kos_birincil(D)
    o.kaydet(AJAN, pd.concat(isl, ignore_index=True), "islemler")
    o.kaydet(AJAN, pd.concat(rj, ignore_index=True), "rejim")
    if ek:
        o.kaydet(AJAN, pd.concat(ek, ignore_index=True), "ekonomi")
    log("zaman doğrulaması")
    zam = zaman_dogrulama(D)
    o.kaydet(AJAN, zam, "zaman")
    log("taşıma")
    tas = tasima(kayit)
    o.kaydet(AJAN, tas, "tasima")
    log("tanı")
    tani, tani_rj = tani_ll2_dusus()
    o.kaydet(AJAN, tani, "tani_LL2dusus")
    o.kaydet(AJAN, tani_rj, "tani_LL2dusus_rejim")
    acik = acik_sinyaller(D)
    o.kaydet(AJAN, acik, "tani_acik")
    log("LL6")
    L, oz = ll6()
    o.kaydet(AJAN, L, "tarama")
    # B2_sonuc: 27 birincil + LL6 satırları (aile=LL6, asama; birlestir() ayrı havuzda işler)
    S = pd.DataFrame(sat)
    drop = [c for c in L.columns if c in ("q_bh", "kesif_gecti", "dog_t_tek", "dog_p_tek", "dog_q", "dogrulandi")]
    o.kaydet(AJAN, pd.concat([S, L.drop(columns=drop)], ignore_index=True), "sonuc")
    md = ozet_md(sat, rj, tas, zam, tani, tani_rj, acik, L, oz)
    (o.SONUC / "B2_ozet.md").write_text(md, encoding="utf-8")
    log("bitti", f"{time.time()-t0:.0f}s", oz)


if __name__ == "__main__":
    main()
