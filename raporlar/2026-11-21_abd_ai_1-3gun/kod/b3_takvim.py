"""B3: takvim, akış ve bilanço aileleri (PROTOKOL madde 9, B3 listesi; 13 birincil test).

Çalıştırma (tek komut, bütün tablolar):  python3 kod/b3_takvim.py
Çıktılar (veri/sonuc/): B3_sonuc.csv, B3_islemler.csv, B3_rejim.csv, B3_ekonomi.csv, B3_tasima.csv,
B3_olaylar.csv (SMH <= -%8), B3_olaylar_5.csv (SMH <= -%5), B3_olaylar_ozet.csv, B3_bilanco_ornek.csv,
B3_bilanco_kapsam.csv, B3_tani_son30.csv, B3_tani_son30_olay.csv, B3_takvim_ileri.csv, B3_acik.csv,
B3_tani.csv (birincil=0 tanılar), B3_ozet.md (tablo taslağı).

Birincil testler (hepsi 'al', yon=+1, getiri 'ham', bilanço maskesi yok: madde 2.4 B3'ü kapsamıyor):
  F7a VIX > VIX3M (t barı) -> al, h=1, Ç ve T.     F7b VIX günlük >= +%20 -> al, h=1, Ç ve T.
  F11a ^SOX <= -%3 -> SMH al, h=1.                  F11b ^SOX >= +%3 -> SMH al, h=1.
  F8a S-4 kapanışı al, S-1 sat (h=3), T.            F8b S al, S+3 sat (h=3), T.
  F8c planlı FOMC karar gününden önceki kapanış al, karar günü sat (h=1), T.
  F9a A-3 al, A sat (h=3), Ç.  F9b A al, tepki günü sat (h=1), Ç.
  F9c tepki günü getirisi >= +%5 -> tepki kapanışı al, h=3, Ç.  F9d <= -%5 -> al, h=1, Ç.
F7'de |t| >= 2 çıkarsa madde 2.3 gereği t-1 barıyla yeniden sınanır (birincil=0, yan yana).
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "kod"))
import ortak as o  # noqa: E402

AJAN = "B3"
TKV = o.TK()
C_ = o.evren("Ç")
T_ = o.evren("T")
Y_ = o.evren("YENİ")
A_ = o.evren("ARAÇ")
SON = o.SON_GUN
# Gelecek takvim (tanı b/c için; NYSE tatilleri elle): 26.11 Şükran, 25.12 Noel, 01.01 Yılbaşı
TATIL = pd.DatetimeIndex(["2026-11-26", "2026-12-25", "2027-01-01", "2027-01-18"])
ILERI_TK = pd.bdate_range("2026-11-23", "2027-02-26").difference(TATIL)
TAM_TK = TKV.append(ILERI_TK)


def log(*a):
    print("[B3]", *a, flush=True)


def bcast(ser, kodlar):
    s = ser.reindex(TKV).fillna(False).astype(bool)
    return pd.DataFrame({k: s for k in kodlar})


def ser_ad(ser, ad):
    return ser.reindex(TKV).fillna(False).astype(bool).rename(ad)


# ---------------------------------------------------------------- sinyal girdileri
VIX = o.yukle("^VIX")["Close"]
VIX3M = o.yukle("^VIX3M")["Close"]
SOX = o.yukle("^SOX")["Close"]
vix_t = VIX.reindex(TKV)
v3_t = VIX3M.reindex(TKV)
ORAN = vix_t / v3_t
F7A = (vix_t > v3_t)                                       # NaN -> False
F7B = (VIX.pct_change(fill_method=None).reindex(TKV) >= 0.20)
SOXR = SOX.pct_change(fill_method=None).reindex(TKV)
F11A = SOXR <= -0.03
F11B = SOXR >= 0.03

# ay sonu: S = ayın son işlem günü; yalnız tamamlanmış aylar (Kasım 2026 dışarıda: S = 30.11 > SON_GUN)
_ay = pd.Series(TKV, index=TKV).groupby(TKV.to_period("M")).max()
_ay = _ay[_ay.index < pd.Period("2026-11", "M")]
iS = TKV.get_indexer(pd.DatetimeIndex(_ay.values))
F8A = pd.Series(False, index=TKV)
F8A.iloc[iS[iS >= 4] - 4] = True
F8B = pd.Series(False, index=TKV)
F8B.iloc[iS] = True
_fo = o.fomc()
_fo = _fo[(_fo >= TKV[0]) & (_fo <= SON)]
iF = TKV.get_indexer(_fo)
FOMC_KAYIP = int((iF < 0).sum())
iF = iF[iF > 0]
F8C = pd.Series(False, index=TKV)
F8C.iloc[iF - 1] = True

GH = o._gunluk_ham(sorted(set(C_ + Y_ + T_)))              # günlük getiri bps (ABD takvimi)


def bilanco_sinyal(kodlar):
    """F9a-d sinyal matrisleri ve güç (|tepki getirisi|)."""
    S = {v: pd.DataFrame(False, index=TKV, columns=kodlar) for v in "abcd"}
    G = pd.DataFrame(np.nan, index=TKV, columns=kodlar)
    hacimli = pd.DataFrame(False, index=TKV, columns=kodlar)
    gh = o._gunluk_ham(kodlar)
    for k in kodlar:
        b = o.bilanco(k)
        if not len(b):
            continue
        iA = TKV.get_indexer(pd.DatetimeIndex(b["A"]))
        iT = TKV.get_indexer(pd.DatetimeIndex(b["tepki"]))
        ok = (iA >= 0) & (iT >= 0)
        iA, iT, yon = iA[ok], iT[ok], b["yontem"].values[ok]
        j = kodlar.index(k)
        S["a"].iloc[iA[iA >= 3] - 3, j] = True
        S["b"].iloc[iA, j] = True
        rt = gh[k].values[iT]
        S["c"].iloc[iT[rt >= 500], j] = True
        S["d"].iloc[iT[rt <= -500], j] = True
        G.iloc[iT, j] = np.abs(rt)
        for d_ in (0, 3):           # hacim kuralıyla atanmış olayların A ve A-3 günleri (tanı)
            q = iA[yon == "hacim"] - d_
            hacimli.iloc[q[q >= 0], j] = True
    return S, G, hacimli


F9S_C, F9G_C, F9HAC_C = bilanco_sinyal(C_)


# ---------------------------------------------------------------- test tanımları
def tanimlar():
    """(test_id, aile, varyant, evren, kodlar, sinyal, h, guc, tm1_sinyal)."""
    L = []
    for ev, K in (("C", C_), ("T", T_)):
        g = pd.DataFrame({k: ORAN for k in K})
        L.append((f"F7a_{ev}_h1", "F7", "a", ev, K, bcast(F7A, K), 1, g, bcast(F7A.shift(1, fill_value=False), K)))
        gb = pd.DataFrame({k: VIX.pct_change(fill_method=None).reindex(TKV) for k in K})
        L.append((f"F7b_{ev}_h1", "F7", "b", ev, K, bcast(F7B, K), 1, gb, bcast(F7B.shift(1, fill_value=False), K)))
    L.append(("F11a_SMH_h1", "F11", "a", "SMH", ["SMH"], ser_ad(F11A, "SMH"), 1, None, None))
    L.append(("F11b_SMH_h1", "F11", "b", "SMH", ["SMH"], ser_ad(F11B, "SMH"), 1, None, None))
    L.append(("F8a_T_h3", "F8", "a", "T", T_, bcast(F8A, T_), 3, None, None))
    L.append(("F8b_T_h3", "F8", "b", "T", T_, bcast(F8B, T_), 3, None, None))
    L.append(("F8c_T_h1", "F8", "c", "T", T_, bcast(F8C, T_), 1, None, None))
    for v, h in (("a", 3), ("b", 1), ("c", 3), ("d", 1)):
        L.append((f"F9{v}_C_h{h}", "F9", v, "C", C_, F9S_C[v], h, F9G_C, None))
    return L


def boot_ort(x, n=2000, seed=0):
    if len(x) < 2:
        return np.nan, np.nan
    rng = np.random.default_rng(seed)
    g = x.groupby("giris")["alfa_bps"].agg(["sum", "count"])
    s, c = g["sum"].values, g["count"].values
    i = rng.integers(0, len(g), (n, len(g)))
    m = s[i].sum(1) / c[i].sum(1)
    return np.percentile(m, 5), np.percentile(m, 95)


def tasima_satirlari(t_id, kaynak_t, ev_ad, isl, kodlar):
    rows = []
    for k, x in [("havuz", isl)] + [(k, isl[isl["kod"] == k]) for k in kodlar]:
        lo, hi = boot_ort(x)
        n = len(x)
        rows.append(dict(test_id=t_id, kaynak_t=kaynak_t, evren=ev_ad, kod=k, getiri_turu="ham", n_islem=n,
                         n_gun=x["giris"].nunique() if n else 0,
                         ort_bps=x["getiri_bps"].mean() if n else np.nan,
                         alfa_bps=x["alfa_bps"].mean() if n else np.nan, ar05_bps=lo, ar95_bps=hi,
                         medyan_bps=x["getiri_bps"].median() if n else np.nan,
                         isabet=(x["getiri_bps"] > 0).mean() if n else np.nan,
                         maliyet_bps=x["maliyet_bps"].mean() if n else np.nan,
                         alfa_net_bps=(x["alfa_bps"] - x["maliyet_bps"]).mean() if n else np.nan,
                         en_kotu_bps=x["getiri_bps"].min() if n else np.nan,
                         alfa_P3_bps=x.loc[x["giris"] >= "2023-01-01", "alfa_bps"].mean() if n else np.nan,
                         n_P3=int((x["giris"] >= "2023-01-01").sum()) if n else 0,
                         alfa_son12_bps=x.loc[x["giris"] >= o.SON12_BAS, "alfa_bps"].mean() if n else np.nan,
                         filtre="tam (madde 2.2)",
                         not_=("n<30: yalnız betimsel" if n < 30 else "")))
    return rows


def tasima_sinyal(aile, varyant, K):
    if aile == "F7":
        base = F7A if varyant == "a" else F7B
        return bcast(base, K)
    if aile == "F8":
        return bcast({"a": F8A, "b": F8B, "c": F8C}[varyant], K)
    if aile == "F11":
        return bcast(F11A if varyant == "a" else F11B, K)
    if aile == "F9":
        S, _, _ = bilanco_sinyal(K)
        return S[varyant]
    raise ValueError(aile)


def tasima(sonuc):
    rows = []
    for r in sonuc:
        if r["birincil"] != 1:
            continue
        aile, v, ev, h = r["aile"], r["varyant"], r["evren"], int(r["h"])
        hedefler = []
        if aile == "F9" or (aile == "F7" and ev == "C"):
            hedefler.append(("YENİ", [k for k in Y_ if len(o.bilanco(k)) or aile != "F9"]))
        if aile == "F8" or (aile == "F7" and ev == "T"):
            hedefler.append(("ARAÇ", A_))
        if aile == "F11":
            hedefler.append(("ARAÇ", ["SOXL", "USD"]))   # "SMH al" taşıyıcıları (ters ETF yok)
        for ev_ad, K in hedefler:
            S = tasima_sinyal(aile, v, K)
            isl = o.islemler(S, h=h, getiri="ham", test_id=f"{r['test_id']}>{ev_ad}")
            rows += tasima_satirlari(r["test_id"], r["t_kume"], ev_ad, isl, K)
        log("taşıma", r["test_id"])
    return pd.DataFrame(rows).rename(columns={"not_": "not"})


# ---------------------------------------------------------------- ana testler
def ana_testler():
    sonuc, isl_hep, rj_hep, ek_hep, tani = [], [], [], [], []
    isl_sakla = {}
    for t_id, aile, v, ev, K, S, h, G, S1 in tanimlar():
        isl = o.islemler(S, h=h, getiri="ham", guc=G, test_id=t_id)
        r = o.test(isl, test_id=t_id, ajan=AJAN, aile=aile, varyant=v, birincil=1, kaynak="lit", evren=ev,
                   h=h, cikis="kapanis", getiri_turu="ham", yon=+1)
        if aile == "F11":
            # ortak._etiket aile[:2] == "F1" eşleşmesiyle F11'e F1 ailesinin 7. (T işareti) ve 8. (15:30)
            # ölçütlerini uyguluyor (ortak.py hatası). SMH zaten T evreninde: 7. ölçüt için kendi alfası.
            r["alfa_temiz"] = r["alfa_bps"]
            r["not"] = (str(r.get("not") or "") + "; ortak._etiket F11'i F1 sanıyor: 8. ölçüt (15:30) F11 için geçersiz").strip("; ")
        sonuc.append(r)
        isl_sakla[t_id] = isl
        isl_hep.append(isl)
        rj_hep.append(o.rejim(isl))
        if np.isfinite(r["t_kume"]) and abs(r["t_kume"]) >= 2 and r["n_islem"] > 0:
            arac = "havuz" if len(K) > 1 else K[0]
            ek = o.ekonomi(isl, arac, t_stat=r["t_kume"])
            ek.insert(0, "test_id", t_id) if "test_id" not in ek else None
            ek_hep.append(ek)
        log(t_id, f"n={r['n_islem']} alfa={r['alfa_bps']:.1f} t={r['t_kume']:.2f} p_perm={r['p_perm']:.3f}")
        # madde 2.3: VIX ailesi |t| >= 2 -> t-1 barıyla yeniden sınama (yan yana, birincil=0)
        if S1 is not None and np.isfinite(r["t_kume"]) and abs(r["t_kume"]) >= 2:
            i1 = o.islemler(S1, h=h, getiri="ham", guc=G.shift(1), test_id=t_id + "_tm1")
            r1 = o.test(i1, test_id=t_id + "_tm1", ajan=AJAN, aile=aile, varyant=v + "_tm1", birincil=0,
                        kaynak="lit", evren=ev, h=h, cikis="kapanis", getiri_turu="ham", yon=+1,
                        notu="madde 2.3: VIX t-1 barıyla yeniden sınama")
            sonuc.append(r1)
            isl_hep.append(i1)
            log(t_id + "_tm1", f"n={r1['n_islem']} alfa={r1['alfa_bps']:.1f} t={r1['t_kume']:.2f}")
    # tanı (birincil=0): F9a/F9b'de saat bilgisi olmayan (hacim kuralı) olaylar çıkınca; A seçimi
    # tepki günü hacmine dayandığı için bu olaylarda geleceğe bakış riski var.
    for v, h in (("a", 3), ("b", 1)):
        S = F9S_C[v] & ~F9HAC_C
        isl = o.islemler(S, h=h, getiri="ham", test_id=f"F9{v}_C_h{h}_saatli")
        r = o.test(isl, perm=0, ikincil=False, test_id=f"F9{v}_C_h{h}_saatli", ajan=AJAN, aile="F9",
                   varyant=v + "_saatli", birincil=0, kaynak="lit", evren="C", h=h, yon=+1,
                   notu="tanı: yalnız saat bilgili olaylar")
        tani.append(r)
    return sonuc, isl_hep, rj_hep, ek_hep, tani, isl_sakla


# ---------------------------------------------------------------- olay listesi
def olaylar():
    smh = o.fiyat("SMH")["AClose"]
    r = (smh.pct_change(fill_method=None) * 1e4).reindex(TKV)
    kod = ["SMH", "SOXL", "NVDA", "QQQ"]
    F = {(k, h): o.ileri(k, h) for k in kod for h in (1, 2, 3)}
    Fo = {k: o.ileri(k, 1, "acilis") for k in kod}
    rg = o._rejim_gunleri()
    smh_dd = (smh / smh.rolling(250, min_periods=250).max() - 1).reindex(TKV) * 100
    out = {}
    for esik in (-800, -500):
        g = TKV[(r <= esik).values]
        rows = []
        ep = o._epizot(g)
        for d in g:
            x = dict(tarih=d.date(), smh_gun_bps=r[d], vix=vix_t[d], vix_vix3m=ORAN[d],
                     smh_zirveden_yuzde=smh_dd[d], BUGUN=bool(rg.at[d, "BUGUN"]), epizot=ep[d])
            for k in kod:
                x[f"{k}_acilis_bps"] = Fo[k][d]
                for h in (1, 2, 3):
                    x[f"{k}_h{h}_bps"] = F[(k, h)][d]
            rows.append(x)
        out[esik] = pd.DataFrame(rows)
    # özet: koşulsuz (aynı tarihlerin tamamı 2010+) ile kıyas
    oz = []
    for esik, df in out.items():
        for alt, m in (("tum", np.ones(len(df), bool)), ("BUGUN", df["BUGUN"].values),
                       ("P3", pd.to_datetime(df["tarih"]).values >= np.datetime64("2023-01-01"))):
            for k in kod:
                for h in ("acilis", "h1", "h2", "h3"):
                    c = df.loc[m, f"{k}_{h}_bps"].dropna()
                    hh = 1 if h in ("acilis", "h1") else int(h[1])
                    ks = (F[(k, hh)] if h != "acilis" else Fo[k]).dropna()
                    oz.append(dict(esik_bps=esik, alt=alt, kod=k, ufuk=h, n=len(c),
                                   n_epizot=df.loc[m].loc[c.index, "epizot"].nunique() if len(c) else 0,
                                   ort_bps=c.mean(), medyan_bps=c.median(), isabet=(c > 0).mean() if len(c) else np.nan,
                                   en_kotu_bps=c.min() if len(c) else np.nan, en_iyi_bps=c.max() if len(c) else np.nan,
                                   kosulsuz_ort_bps=ks.mean()))
    return out[-800], out[-500], pd.DataFrame(oz)


# ---------------------------------------------------------------- bilanço kapsamı / örnek
def bilanco_kontrol():
    ornek = []
    for k in ("NVDA", "MU", "AVGO"):
        b = o.bilanco(k).tail(8)
        gh = GH[k]
        for _, x in b.iterrows():
            ornek.append(dict(kod=k, duyuru=x.duyuru.date(), saat=x.saat, zaman=x.zaman, A=x.A.date(),
                              tepki=x.tepki.date(), yontem=x.yontem, tepki_hacim=x.tepki_hacim.date(),
                              hacim_ayni=x.tepki == x.tepki_hacim, tepki_getiri_bps=gh.get(x.tepki, np.nan),
                              A_getiri_bps=gh.get(x.A, np.nan)))
    kap = []
    for k in C_:
        b = o.bilanco(k)
        kap.append(dict(kod=k, n_olay=len(b), ilk=b["duyuru"].min().date() if len(b) else None,
                        son=b["duyuru"].max().date() if len(b) else None,
                        saat_orani=(b["yontem"] == "saat").mean() if len(b) else np.nan,
                        hacim_ayni_orani=(b["tepki"] == b["tepki_hacim"]).mean() if len(b) else np.nan))
    return pd.DataFrame(ornek), pd.DataFrame(kap)


# ---------------------------------------------------------------- tanı a: son 30 dakika
def tani_son30():
    rows = []
    sm = o.yukle("SMH", saatlik=True)
    gun = sm.index.normalize().tz_localize(None)
    bar = sm.index.strftime("%H:%M")
    b1530 = sm[bar == "15:30"].copy()
    b1530.index = gun[bar == "15:30"]
    son30 = (b1530["Close"] / b1530["Open"] - 1) * 1e4
    # tutarlılık: saatlik 15:30 bar kapanışı ~ günlük ham kapanış
    gk = o.fiyat("SMH")["Close"].reindex(son30.index)
    uyum = (b1530["Close"] / gk - 1).abs().median() * 1e4
    smr = (o.fiyat("SMH")["AClose"].pct_change(fill_method=None) * 1e4).reindex(son30.index)
    F = {(k, c): o.ileri(k, 1, c).reindex(son30.index) for k in ("SMH", "SOXL") for c in ("kapanis", "acilis")}
    det = []
    for yon, ad in ((-1, "dusus<=-3%"), (+1, "yukselis>=+3%")):
        m = (yon * smr >= 300)
        for grp, mm in (("son30_gun_yonunde", m & (yon * son30 > 0)), ("son30_ters_ya_da_0", m & (yon * son30 <= 0))):
            d = son30.index[mm.values]
            for x in d:
                det.append(dict(tarih=x.date(), kosul=ad, grup=grp, smh_gun_bps=smr[x], son30_bps=son30[x],
                                **{f"{k}_{c}_bps": F[(k, c)][x] for k in ("SMH", "SOXL") for c in ("acilis", "kapanis")}))
            for k in ("SMH", "SOXL"):
                for c in ("acilis", "kapanis"):
                    v = F[(k, c)][mm.values].dropna()
                    rows.append(dict(kosul=ad, grup=grp, kod=k, cikis=c, n=len(v), ort_bps=v.mean(),
                                     medyan_bps=v.median(), isabet=(v > 0).mean() if len(v) else np.nan,
                                     en_kotu_bps=v.min() if len(v) else np.nan,
                                     not_="yalnız betimsel (n<30)" if len(v) < 30 else "yalnız betimsel"))
    return pd.DataFrame(rows).rename(columns={"not_": "not"}), pd.DataFrame(det), uyum, \
        (son30.index.min().date(), son30.index.max().date(), len(son30))


# ---------------------------------------------------------------- tanı b: önümüzdeki 6 hafta
def takvim_ileri():
    rows = []
    for ay in ("2026-11", "2026-12"):
        g = TAM_TK[TAM_TK.to_period("M") == pd.Period(ay, "M")]
        iS = TAM_TK.get_loc(g.max())
        rows.append(dict(sinyal="F8a", olay=f"{ay} ay sonu", giris=TAM_TK[iS - 4].date(), cikis=TAM_TK[iS - 1].date(), not_="S-4 al, S-1 sat"))
        rows.append(dict(sinyal="F8b", olay=f"{ay} ay sonu", giris=TAM_TK[iS].date(), cikis=TAM_TK[iS + 3].date(), not_="S al, S+3 sat"))
    for f in o.fomc():
        if pd.Timestamp("2026-11-21") <= f <= pd.Timestamp("2027-01-08"):
            i = TAM_TK.get_loc(f)
            rows.append(dict(sinyal="F8c", olay=f"FOMC {f.date()}", giris=TAM_TK[i - 1].date(), cikis=f.date(), not_="t-1 kapanış al, karar günü sat"))
    # bilanço: Ç (ve YENİ) içinde 23.11.2026 - 08.01.2027 duyuruları, ham dosyadan
    beklenen = {"MRVL": "2026-12-01", "AVGO": "2026-12-09", "MU": "2026-12-17"}
    for k in C_ + Y_:
        yol = o.VERI / "bilanco" / f"{o.dosya_adi(k)}.csv"
        if not yol.exists():
            continue
        b = pd.read_csv(yol, parse_dates=["tarih"])
        b = b[(b.tarih > SON) & (b.tarih <= "2027-01-08")]
        for _, x in b.iterrows():
            if x.tarih not in TAM_TK:
                tepki = TAM_TK[TAM_TK.searchsorted(x.tarih)]
            elif x.zaman == "sonra":
                tepki = TAM_TK[TAM_TK.get_loc(x.tarih) + 1]
            elif x.zaman in ("once", "seans"):
                tepki = x.tarih
            else:
                tepki = None
            if tepki is None:
                rows.append(dict(sinyal="F9", olay=f"{k} bilanço {x.tarih.date()} (saat yok)", giris=None, cikis=None,
                                 not_="saat yok: tepki günü hacim kuralıyla sonradan belli olur"))
                continue
            iT = TAM_TK.get_loc(tepki)
            A = TAM_TK[iT - 1]
            ev = "Ç" if k in C_ else "YENİ"
            uy = ""
            if k in beklenen:
                uy = "veri/bilanco ile uyumlu" if str(x.tarih.date()) == beklenen[k] else f"UYUŞMAZ: görev {beklenen[k]}"
            rows.append(dict(sinyal="F9a", olay=f"{k} ({ev}) bilanço {x.tarih.date()} {x.saat} {x.zaman}",
                             giris=TAM_TK[iT - 4].date(), cikis=A.date(), not_=f"A-3 al, A sat; {uy}".strip("; ")))
            rows.append(dict(sinyal="F9b", olay=f"{k} ({ev}) bilanço {x.tarih.date()}", giris=A.date(), cikis=tepki.date(),
                             not_="A al, tepki kapanışı sat"))
            rows.append(dict(sinyal="F9c/d", olay=f"{k} ({ev}) tepki günü {tepki.date()}", giris=tepki.date(),
                             cikis=f"{TAM_TK[iT + 3].date()} (c) / {TAM_TK[iT + 1].date()} (d)",
                             not_="tepki getirisi >= +%5 -> h=3; <= -%5 -> h=1"))
    for k, d in beklenen.items():
        if not any(str(r_["olay"]).startswith(k + " ") and "bilanço" in str(r_["olay"]) for r_ in rows):
            rows.append(dict(sinyal="F9", olay=f"{k} {d}", giris=None, cikis=None, not_="UYUŞMAZ: veri/bilanco'da yok"))
    return pd.DataFrame(rows).rename(columns={"not_": "not"}).sort_values("giris", key=lambda s: s.astype(str))


# ---------------------------------------------------------------- tanı c: 20.11.2026 kapanışında açık sinyaller
def acik():
    rows = []
    son = TKV[-3:]                              # h<=3: son 3 günün girişleri SON_GUN'de hâlâ açık olabilir
    for t_id, aile, v, ev, K, S, h, G, _ in tanimlar():
        U = o.uygun(K)
        S = S.to_frame() if isinstance(S, pd.Series) else S
        for i, d in enumerate(son):
            kalan = len(TKV) - 1 - TKV.get_loc(d)            # SON_GUN'e kadar geçen gün
            if kalan >= h:
                continue
            for k in K:
                if bool(S.at[d, k]):
                    rows.append(dict(test_id=t_id, kod=k, giris=d.date(), h=h, cikis_gun_sonra=h - kalan,
                                     filtre_gecer=bool(U.at[d, k]),
                                     guc=(G.at[d, k] if G is not None else np.nan)))
    durum = dict(tarih=str(SON.date()), vix=vix_t[SON], vix3m=v3_t[SON], vix_vix3m=ORAN[SON],
                 vix_degisim=VIX.pct_change(fill_method=None)[SON], sox_getiri=SOXR[SON],
                 BUGUN=bool(o._rejim_gunleri().at[SON, "BUGUN"]), STRES=bool(o._rejim_gunleri().at[SON, "STRES"]))
    return pd.DataFrame(rows), durum


# ---------------------------------------------------------------- özet tablosu
def md_tab(df, nd=1):
    """tabulate olmadan markdown tablo."""
    if df is None or not len(df):
        return "(boş)"
    def h(v):
        if isinstance(v, (float, np.floating)):
            return "" if not np.isfinite(v) else f"{v:.{nd}f}"
        return str(v)
    L = ["| " + " | ".join(map(str, df.columns)) + " |", "|" + "---|" * len(df.columns)]
    L += ["| " + " | ".join(h(v) for v in row) + " |" for row in df.itertuples(index=False)]
    return "\n".join(L)


def f(x, n=1):
    return "" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{x:.{n}f}"


def ozet_md(sonuc, rj, etiket):
    rjb = rj[rj["hucre"] == "BUGUN"].set_index("test_id")
    satir = ["| test_id | n_islem | alfa_bps | t_kume | alfa_net_bps | P1 / P2 / P3 alfa | son 12 ay alfa | BUGÜN ort (n_islem, n_epizot) | t_takvim | p_perm | ön etiket |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in sonuc:
        tid = r["test_id"]
        if tid in rjb.index:
            b = rjb.loc[tid]
            bc = f"{f(b.get('ortalama_bps'))} ({int(b['n_islem'])}, {int(b['n_epizot'])})"
        else:
            bc = ""
        satir.append(f"| {tid} | {r['n_islem']} | {f(r['alfa_bps'])} | {f(r['t_kume'], 2)} | {f(r['alfa_net_bps'])} | "
                     f"{f(r['alfa_P1'])} / {f(r['alfa_P2'])} / {f(r['alfa_P3'])} | {f(r['alfa_son12'])} (n={r['n_son12']}) | {bc} | "
                     f"{f(r['t_takvim'], 2)} | {f(r['p_perm'], 3)} | {etiket.get(tid, '')} |")
    return "\n".join(satir)


def main():
    sonuc, isl_hep, rj_hep, ek_hep, tani, isl_sakla = ana_testler()
    o.kaydet(AJAN, sonuc)
    o.kaydet(AJAN, pd.concat(isl_hep, ignore_index=True), "islemler")
    rj = pd.concat(rj_hep, ignore_index=True)
    o.kaydet(AJAN, rj, "rejim")
    o.kaydet(AJAN, pd.concat(ek_hep, ignore_index=True) if ek_hep else pd.DataFrame(), "ekonomi")
    o.kaydet(AJAN, pd.DataFrame(tani), "tani")
    o.kaydet(AJAN, tasima(sonuc), "tasima")
    e8, e5, eoz = olaylar()
    o.kaydet(AJAN, e8, "olaylar")
    o.kaydet(AJAN, e5, "olaylar_5")
    o.kaydet(AJAN, eoz, "olaylar_ozet")
    orn, kap = bilanco_kontrol()
    o.kaydet(AJAN, orn, "bilanco_ornek")
    o.kaydet(AJAN, kap, "bilanco_kapsam")
    s30, s30d, uyum, s30k = tani_son30()
    o.kaydet(AJAN, s30, "tani_son30")
    o.kaydet(AJAN, s30d, "tani_son30_olay")
    ti = takvim_ileri()
    o.kaydet(AJAN, ti, "takvim_ileri")
    ac, durum = acik()
    # bilanço olayı SON_GUN'den sonra olan ama girişi SON_GUN'de ya da önce olan F9a/F9b pozisyonları
    # (bilanco() SON_GUN sonrasını atar; ham dosyadan takvim_ileri ile bulunur)
    gi = pd.to_datetime(ti["giris"].astype(str), errors="coerce")
    ek_ac = ti[(gi <= SON) & ti["sinyal"].isin(["F9a", "F9b"])]
    if len(ek_ac):
        ek_ac = pd.DataFrame(dict(test_id=ek_ac["sinyal"] + "_" + np.where(ek_ac["olay"].str.contains("(Ç)", regex=False), "C", "YENI"),
                                  kod=ek_ac["olay"].str.split(" ").str[0], giris=ek_ac["giris"], cikis=ek_ac["cikis"],
                                  h=np.where(ek_ac["sinyal"] == "F9a", 3, 1), filtre_gecer=np.nan, guc=np.nan))
        ac = pd.concat([ac, ek_ac], ignore_index=True)
    o.kaydet(AJAN, ac, "acik")
    # ön etiket: mevcut *_sonuc.csv dosyalarıyla (BH havuzu eksik olabilir), dosya yazmadan
    try:
        b, _, oz = o.birlestir(yaz=False)
        b = b[b["ajan"] == AJAN]
        etiket = dict(zip(b["test_id"], b["etiket"].astype(str) + " [q=" + b["q_bh"].round(3).astype(str) + "]"))
    except Exception as ex:  # noqa: BLE001
        oz, etiket = {"hata": str(ex)}, {}
    md = ["# B3 tablo taslağı", "", f"birlestir özeti (ön): {oz}", "", ozet_md(sonuc, rj, etiket), "",
          f"F8c: FOMC günlerinden takvimde bulunamayan: {FOMC_KAYIP}", "",
          f"Son30 tanı kapsamı: {s30k}; saatlik 15:30 bar kapanışı ile günlük kapanış medyan farkı {uyum:.1f} bps", "",
          "## Son 30 dakika tanısı", md_tab(s30), "",
          "## Olay özeti (SMH <= -%8 / -%5)",
          md_tab(eoz[eoz["ufuk"].isin(["acilis", "h1", "h3"])]), "",
          "## Bilanço örneği", md_tab(orn, 0), "",
          "## Önümüzdeki takvim", md_tab(ti), "",
          f"## 20.11.2026 durumu: {durum}", md_tab(ac, 3) if len(ac) else "(açık sinyal yok)", "",
          "## Tanı (birincil=0)", md_tab(pd.DataFrame(tani)[["test_id", "n_islem", "alfa_bps", "t_kume", "alfa_net_bps", "alfa_P3", "n_P3"]], 2)]
    (o.SONUC / "B3_ozet.md").write_text("\n".join(md), encoding="utf-8")
    log("bitti; B3_ozet.md yazıldı")


if __name__ == "__main__":
    main()
