# -*- coding: utf-8 -*-
"""aile_K5.py - Aile E (takvim ve olay) + R7-03 (60/40 ay sonu yeniden dengeleme).
Calistirma:  python3 -I aile_K5.py            (IS -> aday dosyasi -> OOS -> ayrinti; hepsi)
             python3 -I aile_K5.py --asama is (yalniz IS ve aday_K5.csv)
Cikti: ../veri/aday_K5.csv, ../veri/sonuc_K5.csv (motor SEMA), ../veri/ozet_K5.csv (karar tablosu),
       ../veri/takvim_K5.csv (23.11.2026-15.01.2027 tarihli giris/cikis takvimi).
Pencere tanimlari d3_R7/d3_R6/d3_R8 'Sinanacak kurallar' tablolarindan; pencere > 3 gun ise
ayni giristen h = 1, 2, 3 alt pencereleri de ayri varyanttir (test sayisina katilir)."""
import argparse
import os
import sys
import time

import numpy as np
import pandas as pd

KOD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOD)
import motor as M  # noqa: E402
from yukle import fomc, makro, saatlik  # noqa: E402

VERI = M.VERI_DIZIN
ADAY = os.path.join(VERI, "aday_K5.csv")
SONUC = os.path.join(VERI, "sonuc_K5.csv")
OZET = os.path.join(VERI, "ozet_K5.csv")
TAKVIM = os.path.join(VERI, "takvim_K5.csv")

# ---------------------------------------------------------------- takvim (panel + bilinen gelecek)
# Gelecek NYSE gunleri: 2026-11-23 .. 2027-01-29; tatiller 26.11.2026, 25.12.2026, 01.01.2027, 18.01.2027
# yarim gunler 27.11.2026 ve 24.12.2026 (13:00 ET). NYSE resmi takvimi (varsayim olarak yazildi).
GELECEK_TATIL = pd.to_datetime(["2026-11-26", "2026-12-25", "2027-01-01", "2027-01-18"])
GELECEK_YARIM = pd.to_datetime(["2026-11-27", "2026-12-24"])
# 2027 FOMC (Fed takvimi; varsayim): 26-27 Ocak 2027 -> karar 27.01.2027
GELECEK_FOMC = pd.to_datetime(["2027-01-27"])
SANDY = pd.Timestamp("2012-10-26")      # Sandy kapanisi onceden bilinmiyordu: tatil oncesi sayilmaz

YAYIN = {"R7-01": 2008, "R7-02": 2020, "R7-03": 2025, "R7-04": 2011, "R7-05": 2019, "R7-06": 2009,
         "R7-07": 2021, "R7-08": 1972, "R7-09": 2003, "R6-09": 2011, "R8-12": None, "EK": None}


def yayin_yili(kid):
    return YAYIN.get(kid[:5], None)


class Takvim:
    def __init__(self, idx):
        bd = pd.bdate_range(idx[-1] + pd.Timedelta(days=1), "2027-01-29")
        gel = bd[~bd.isin(GELECEK_TATIL)]
        self.T = len(idx)
        self.C = idx.append(gel)                       # panel + gelecek islem gunleri
        C = self.C
        ym = (C.year * 12 + C.month).to_numpy()
        self.yeni_ay = np.r_[True, ym[1:] != ym[:-1]]
        self.ay_son = np.r_[ym[1:] != ym[:-1], False]
        self.ym = ym
        self.pos = {d: i for i, d in enumerate(C)}

    def ay_sonlari(self):
        return np.flatnonzero(self.ay_son)

    def ay_baslari(self):
        return np.flatnonzero(self.yeni_ay)[1:]       # ilk ay eksik olabilir

    def onceki_islem(self, d):
        """d tarihindeki ya da ondan onceki son islem gunu pozisyonu."""
        i = int(self.C.searchsorted(pd.Timestamp(d), side="right")) - 1
        return i

    def tatil_oncesi(self):
        C = self.C
        out = []
        for i in range(len(C) - 1):
            a, b = C[i], C[i + 1]
            ara = pd.bdate_range(a + pd.Timedelta(days=1), b - pd.Timedelta(days=1))
            if len(ara) and a != SANDY:
                out.append(i)
        return np.array(out, int)


def seri(tk, poz, yon, idx):
    """Pozisyon listesinden panel indeksine hizali {-1,0,+1} Series (gelecek pozisyonlar atilir)."""
    s = np.zeros(tk.T)
    poz = np.asarray([p for p in poz if 0 <= p < tk.T], int)
    s[poz] = yon
    return pd.Series(s, index=idx).astype(int)


# ---------------------------------------------------------------- kural tanimlari
def kurallar(m, tk):
    idx = m.idx
    K = []        # (kid, ad, hedefler, sinyal_fn(m) ya da sabit sinyal, h_tuple, cok, guc, gelecek_poz, yon, giris_aciklama)
    e = tk.ay_sonlari()                 # T = ayin son islem gunu
    b = tk.ay_baslari()                 # ayin ilk islem gunu

    def ekle(kid, ad, hedefler, sig, h, gel, yon, tanim, cok=False, guc=None, girdi="takvim"):
        K.append(dict(kid=kid, ad=ad, hedefler=hedefler, sig=sig, h=tuple(h), cok=cok, guc=guc,
                      gel=gel, yon=yon, tanim=tanim, girdi=girdi))

    # R7-01 E1 ay donumu: T-1 kapanisi -> yeni ayin 3. islem gunu (T+3), h=4
    p = e - 1
    ekle("R7-01", "E1 Ay donumu T-1 -> yeni ay 3. gun", ["SPY", "QQQ", "IWM", "SPXL", "TQQQ"],
         seri(tk, p, 1, idx), (1, 2, 3, 4), p, 1, "giris T-1 kapanisi, cikis T+3 kapanisi")
    # R7-02 Dash for Cash
    p = e - 4
    ekle("R7-02A", "E2-A Dash for Cash uzun T-4 -> T+3", ["SPY", "IWM", "QQQ"], seri(tk, p, 1, idx),
         (1, 2, 3, 7), p, 1, "giris T-4, cikis T+3")
    p = e - 9
    ekle("R7-02B", "E2-B satis baskisi kisa T-9 -> T-4", ["SPY", "IWM", "QQQ"], seri(tk, p, -1, idx),
         (1, 2, 3, 5), p, -1, "giris T-9, cikis T-4")
    p = e - 7
    ekle("R7-02B1", "E2-B1 (T+1 kaymasi) kisa T-7 -> T-2", ["SPY", "IWM", "QQQ"], seri(tk, p, -1, idx),
         (1, 2, 3, 5), p, -1, "giris T-7, cikis T-2")
    p = e - 2
    ekle("R7-02A1", "E2-A1 (T+1 kaymasi) uzun T-2 -> T", ["SPY", "IWM", "QQQ"], seri(tk, p, 1, idx),
         (2,), p, 1, "giris T-2, cikis T")

    # R7-03 H1 60/40 sapmasi (SPY, IEF; ABD16, ayni gun guvenli)
    def r703(mm, esik=0.0, kodlar=("SPY", "IEF"), hedef="cift"):
        px = mm.girdi(["SPY", "IEF"], "adjclose")
        ii = mm.idx
        ymm = (ii.year * 12 + ii.month).to_numpy()
        son = np.r_[ymm[1:] != ymm[:-1], False]
        # onceki ay sonu kapanisi (ayin ilk gunundan itibaren sabit)
        ref = px.where(pd.Series(son, index=ii), np.nan).shift(1).ffill()
        a = px["SPY"] / ref["SPY"]
        bb = px["IEF"] / ref["IEF"]
        w = 0.6 * a / (0.6 * a + 0.4 * bb)
        s = w - 0.6
        # ayin son 5 islem gunu (T-4..T); gelecek takvimden bilinir
        pp = np.concatenate([tk.ay_sonlari() - k for k in range(5)])
        mask = np.zeros(len(ii), bool)
        pp = pp[pp < len(ii)]
        mask[pp] = True
        sg = np.where(mask & (s.abs() >= esik) & s.notna(), -np.sign(s), 0.0)   # s>0 -> hisse kisa
        sg = pd.Series(sg, index=ii).fillna(0).astype(int)
        if hedef == "cift":
            return pd.DataFrame({"SPY": sg, "IEF": -sg})
        return sg.rename(hedef)

    for esik, kod in ((0.0, "a"), (0.02, "b")):
        ekle(f"R7-03{kod}", f"H1 60/40 sapma |s|>={esik:.2f} SPY-IEF cifti", ["CIFT"],
             (lambda mm, e_=esik: r703(mm, e_, hedef="cift")), (1,), None, 0,
             "T-4..T her kapanis, 1 gun", cok=True, guc=None, girdi="SPY, IEF adjclose (t)")
        ekle(f"R7-03{kod}S", f"H1 60/40 sapma |s|>={esik:.2f} tek bacak SPY", ["SPY"],
             (lambda mm, e_=esik: r703(mm, e_, hedef="SPY")), (1,), None, 0,
             "T-4..T her kapanis, 1 gun", girdi="SPY, IEF adjclose (t)")
        ekle(f"R7-03{kod}X", f"H1 60/40 sapma |s|>={esik:.2f} tek bacak SPXL", ["SPXL"],
             (lambda mm, e_=esik: r703(mm, e_, hedef="SPXL")), (1,), None, 0,
             "T-4..T her kapanis, 1 gun", girdi="SPY, IEF adjclose (t)")

    # FOMC (planli karar gunleri)
    F = fomc()
    fp = F.loc[F["tur"] == "planli", "karar_gunu"]
    fdates = pd.DatetimeIndex(fp).append(GELECEK_FOMC).sort_values().unique()
    fpos = np.array([tk.pos[d] for d in fdates if d in tk.pos], int)
    p = fpos - 1
    ekle("R7-04", "E3 FOMC oncesi: onceki kapanis -> karar gunu", ["SPY", "QQQ", "IWM", "TLT"],
         seri(tk, p, 1, idx), (1,), p, 1, "giris karar-1 kapanisi, cikis karar gunu kapanisi")
    p = fpos
    ekle("EK-M2", "FOMC sonrasi: karar gunu kapanisi -> +h", ["SPY", "QQQ", "IWM", "TLT"],
         seri(tk, p, 1, idx), (1, 2, 3), p, 1, "giris karar gunu kapanisi")
    # makro
    MK = makro()
    MK = MK[MK["islem_gunu"] & ~MK["ayda_birden_fazla"]]
    for yay, kid in (("CPI", "EK-M3"), ("ISTIHDAM", "EK-M4")):
        dd = MK.loc[MK["yayin"] == yay, "tarih"]
        pp = np.array([tk.pos[d] for d in dd if d in tk.pos], int) - 1
        ekle(kid, f"{yay} oncesi: onceki kapanis -> yayin gunu kapanisi", ["SPY", "QQQ", "IWM", "TLT"],
             seri(tk, pp, 1, idx), (1,), pp, 1, "giris yayin-1 kapanisi, cikis yayin gunu kapanisi")
    # R8-12 ek: FOMC karar gunu SPY <= -%2 -> uzun
    def r812(mm):
        r = mm.girdi_getiri("SPY")
        s = np.zeros(len(mm.idx))
        f = fpos[fpos < len(mm.idx)]
        s[f] = (r.to_numpy()[f] <= -0.02).astype(float)
        return pd.Series(s, index=mm.idx).astype(int)
    ekle("R8-12", "K12 ek: FOMC karar gunu SPY <= -%2 -> uzun", ["SPY", "QQQ"], r812, (1, 2, 3), None, 1,
         "giris karar gunu kapanisi (kosullu)", girdi="SPY kk getiri (t), FOMC")

    # R7-05 E4 FOMC dongusu cift/tek haftalari
    N = len(tk.C)
    son_f = np.full(N, -1)
    sonraki_f = np.full(N, -1)
    j = -1
    fset = set(fpos.tolist())
    for i in range(N):
        if i in fset:
            j = i
        son_f[i] = j
    j = -1
    for i in range(N - 1, -1, -1):
        sonraki_f[i] = j
        if i in fset:
            j = i
    ks = np.where(son_f >= 0, np.arange(N) - son_f, -999)
    ku = np.where(sonraki_f >= 0, sonraki_f - np.arange(N), 999)
    cift = list(np.flatnonzero(ku == 2))                     # gun -2 kapanisi -> -1..+3
    for c0 in (8, 18, 28):
        cift += list(np.flatnonzero((ks == c0) & (ku >= 7)))
    tek = []
    for c0 in (3, 13, 23):
        tek += list(np.flatnonzero((ks == c0) & (ku >= 7)))
    cift, tek = np.array(sorted(cift)), np.array(sorted(tek))
    ekle("R7-05E", "E4 FOMC dongusu cift hafta uzun (5 gun)", ["SPY", "QQQ", "SPXL"], seri(tk, cift, 1, idx),
         (1, 2, 3, 5), cift, 1, "giris pencere oncesi kapanis (gun -2, 8, 18, 28)")
    ekle("R7-05O", "E4 FOMC dongusu tek hafta kisa (5 gun)", ["SPY", "QQQ", "SPXL"], seri(tk, tek, -1, idx),
         (1, 2, 3, 5), tek, -1, "giris gun 3, 13, 23 kapanisi")

    # R7-06 E5 opsiyon vadesi (ayin 3. cumasi; tatilse onceki islem gunu)
    ops = []
    for y in range(2005, 2028):
        for mo in range(1, 13):
            d = pd.Timestamp(y, mo, 1)
            ilk_cuma = d + pd.Timedelta(days=(4 - d.weekday()) % 7)
            uc = ilk_cuma + pd.Timedelta(days=14)
            if tk.C[0] <= uc <= tk.C[-1]:
                ops.append(tk.onceki_islem(uc))
    ops = np.array(sorted(set(ops)), int)
    sepet = ["AAPL", "NVDA", "TSLA", "AMZN", "MSFT"]
    pA = ops - 5
    pB = ops
    for hed in (["SPY"], ["QQQ"], ["SEPET"]):
        if hed == ["SEPET"]:
            sA = pd.DataFrame({k: seri(tk, pA, 1, idx) for k in sepet})
            sB = pd.DataFrame({k: seri(tk, pB, -1, idx) for k in sepet})
            ekle("R7-06A", "E5 vade haftasi uzun (5 buyuk hisse sepeti)", ["SEPET"], sA, (1, 2, 3, 5), pA, 1,
                 "giris vade-5 kapanisi, cikis vade cumasi", cok=True)
            ekle("R7-06B", "E5 vade sonrasi hafta kisa (5 buyuk hisse sepeti)", ["SEPET"], sB, (1, 2, 3, 5), pB, -1,
                 "giris vade cumasi kapanisi, 5 gun", cok=True)
        else:
            ekle("R7-06A", "E5 vade haftasi uzun", hed, seri(tk, pA, 1, idx), (1, 2, 3, 5), pA, 1,
                 "giris vade-5 kapanisi, cikis vade cumasi")
            ekle("R7-06B", "E5 vade sonrasi hafta kisa", hed, seri(tk, pB, -1, idx), (1, 2, 3, 5), pB, -1,
                 "giris vade cumasi kapanisi, 5 gun")

    # R7-07 E6 tatil oncesi gun
    P = tk.tatil_oncesi() - 1
    ekle("R7-07", "E6 tatil oncesi gun (1 gun)", ["IWM", "SPY", "TNA"], seri(tk, P, 1, idx), (1,), P, 1,
         "giris tatil oncesi gunden bir onceki kapanis, cikis tatil oncesi gun kapanisi")

    # EK Sukran Gunu haftasi
    tg = []
    for y in range(2005, 2027):
        d = pd.Timestamp(y, 11, 1)
        ilk_pers = d + pd.Timedelta(days=(3 - d.weekday()) % 7)
        tg.append(ilk_pers + pd.Timedelta(days=21))
    pzt = [tk.onceki_islem(t - pd.Timedelta(days=4)) for t in tg]          # onceki cuma
    sal = [tk.pos[t - pd.Timedelta(days=2)] for t in tg if (t - pd.Timedelta(days=2)) in tk.pos]
    ekle("EK-T1", "Sukran Gunu haftasi: onceki cuma -> Kara Cuma (4 gun)", ["SPY", "IWM", "QQQ"],
         seri(tk, pzt, 1, idx), (1, 2, 3, 4), np.array(pzt), 1, "giris onceki cuma kapanisi")
    ekle("EK-T2", "Sukran Gunu: sali kapanisi -> Kara Cuma (2 gun)", ["SPY", "IWM", "QQQ"],
         seri(tk, sal, 1, idx), (2,), np.array(sal), 1, "giris sali kapanisi")

    # R7-08 E7 Noel rallisi (= yilin son 5 + ilk 2 gunu): Aralik T-5 kapanisi -> Ocak 2. islem gunu (h=7)
    ar = np.array([p_ for p_ in e if tk.C[p_].month == 12], int)
    p = ar - 5
    ekle("R7-08", "E7 Noel rallisi T-5 -> Ocak 2. gun (7 gun)", ["SPY", "IWM", "QQQ"], seri(tk, p, 1, idx),
         (1, 2, 3, 7), p, 1, "giris Aralik T-5 kapanisi")

    # R7-09 E8 vergi zarari: Aralik T-4 kapanisinda YTD en kotu %10 (donem basi evreni) -> Ocak 3. gun (h=7)
    ev = m.evren_maskesi()

    def r709(mm, yon=1, kayma=4, ust=False, tam=False):
        px = mm.df("adjclose")
        ii = mm.idx
        ymm = (ii.year * 12 + ii.month).to_numpy()
        son = np.r_[ymm[1:] != ymm[:-1], False]
        aralik_son = np.flatnonzero(son & (ii.month == 12))
        S = pd.DataFrame(0, index=ii, columns=px.columns)
        G = pd.DataFrame(0.0, index=ii, columns=px.columns)
        evm = ev.reindex(index=ii, columns=px.columns).fillna(False).to_numpy()
        for t_son in aralik_son:
            t = t_son - kayma
            onc = np.flatnonzero(son & (ii.year == ii[t_son].year - 1) & (ii.month == 12))
            if t < 0 or len(onc) == 0:
                continue
            ytd = px.iloc[t] / px.iloc[onc[0]] - 1
            ytd = ytd[evm[t] & ytd.notna()]
            if len(ytd) < 50:
                continue
            q = ytd.quantile(0.9 if ust else 0.1)
            sec = ytd[ytd >= q] if ust else ytd[ytd <= q]
            S.iloc[t, [S.columns.get_loc(k) for k in sec.index]] = yon
            G.iloc[t, [G.columns.get_loc(k) for k in sec.index]] = (-sec if not ust else sec).to_numpy()
        if tam:
            return S, G
        kol = S.columns[(S != 0).any()]
        return S[kol], G[kol]

    ekle("R7-09L", "E8 vergi zarari: YTD en kotu %10 uzun, Aralik T-4 -> Ocak 3. gun", ["COK"],
         (lambda mm: r709(mm, 1, 4)), (1, 2, 3, 7), ar - 4, 1, "giris Aralik T-4 kapanisi", cok=True,
         girdi="hisse YTD getirisi (t), donem basi evreni")
    K[-1]["tam"] = lambda mm: r709(mm, 1, 4, tam=True)
    ekle("R7-09S", "E8 ayni sepet Aralik basi kisa: T-19 -> T-4 (15 gun)", ["COK"],
         (lambda mm: r709(mm, -1, 19)), (15,), ar - 19, -1, "giris Aralik T-19 kapanisi", cok=True,
         girdi="hisse YTD getirisi (t), donem basi evreni")
    p = ar - 4
    ekle("R7-09I", "E8 IWM uzun Aralik T-4 -> Ocak 3. gun", ["IWM"], seri(tk, p, 1, idx), (1, 2, 3, 7), p, 1,
         "giris Aralik T-4 kapanisi")

    # EK tahvil ay sonu / ay basi (TLT)
    for hh in (1, 2, 3):
        p = e - hh
        ekle(f"EK-B1h{hh}", f"TLT ay sonu uzun T-{hh} -> T", ["TLT"], seri(tk, p, 1, idx), (hh,), p, 1,
             f"giris T-{hh} kapanisi, cikis T")
    ekle("EK-B2", "TLT ay basi kisa T -> T+h", ["TLT"], seri(tk, e, -1, idx), (1, 2, 3), e, -1, "giris T kapanisi")

    # R6-09 G9 erken / gec aciklayan (beklenen tarih = gecen yil ayni ceyrekteki gun sirasi)
    B = pd.read_csv(os.path.join(VERI, "bilanco_tarihleri.csv"), parse_dates=["ilk_tepki_gunu"])
    B = B[B["kod"].isin(m.kpos.keys()) & B["ilk_tepki_gunu"].isin(idx)]
    B = B[[m.sinif.get(k, "ABD16") == "ABD16" for k in B["kod"]]]
    C = tk.C
    qid = (C.year * 4 + (C.month - 1) // 3).to_numpy()
    q_bas = {}
    q_len = {}
    for q in np.unique(qid):
        w = np.flatnonzero(qid == q)
        q_bas[q], q_len[q] = w[0], len(w)
    B["pos"] = [tk.pos[d] for d in B["ilk_tepki_gunu"]]
    B["q"] = qid[B["pos"].to_numpy()]
    B["ofs"] = B["pos"].to_numpy() - np.array([q_bas[q] for q in B["q"]])
    B = B.sort_values("pos").groupby(["kod", "q"], as_index=False).first()
    kod_l = sorted(B["kod"].unique())
    SL = np.zeros((len(idx), len(kod_l)))
    kpos_l = {k: i for i, k in enumerate(kod_l)}
    for _, r in B.iterrows():
        q2 = r["q"] + 4
        if q2 not in q_bas:
            continue
        ofs = min(int(r["ofs"]), q_len[q2] - 1)
        E_ = q_bas[q2] + ofs
        s_ = E_ - 3
        if s_ >= len(idx) or s_ < 0:
            continue
        if ofs < 20:
            SL[s_, kpos_l[r["kod"]]] = 1
        elif ofs >= q_len[q2] - 20:
            SL[s_, kpos_l[r["kod"]]] = -1
    SLd = pd.DataFrame(SL, index=idx, columns=kod_l).astype(int)
    # YONTEM 3: hisse evreni donem basi bilgisiyle (sinyal gununde donem basi evreninde olmayan atilir)
    SLd = SLd.where(ev.reindex(index=idx, columns=kod_l).fillna(False).to_numpy(), 0).astype(int)
    SLd = SLd.loc[:, (SLd != 0).any()]
    ekle("R6-09", "G9 erken(+)/gec(-) beklenen bilanco: t-3 -> t+1", ["COK"], SLd, (4,), None, 0,
         "giris beklenen gun-3 kapanisi, cikis beklenen gun+1", cok=True, girdi="8-K 2.02 tarihleri (gecen yil)")
    ekle("R6-09L", "G9 yalniz erken aciklayan uzun", ["COK"], SLd.clip(lower=0), (4,), None, 1,
         "erken bacak", cok=True, girdi="8-K 2.02 tarihleri (gecen yil)")
    ekle("R6-09S", "G9 yalniz gec aciklayan kisa", ["COK"], SLd.clip(upper=0), (4,), None, -1,
         "gec bacak", cok=True, girdi="8-K 2.02 tarihleri (gecen yil)")
    return K


VERI_YOK = [("R7-11", "E9 Endekse ekleme/cikarma", "S&P/Nasdaq duyuru tarihleri ve eklenen/cikarilan kodlar panelde yok"),
            ("R8-12-etiket", "K12 Fed rejim etiketi (son hareket artirim/indirim)", "FRED DFEDTARU/DFEDTARL panelde yok; ayrica K1/K3/K4/K7 baska ailelerin kurallari")]


def sinyal_al(m, k):
    s = k["sig"]
    g = k["guc"]
    if callable(s):
        s = s(m)
    if isinstance(s, tuple):
        s, g = s
    return s, g


def hedef_ve_sinyal(k, s, hed):
    if hed in ("CIFT", "SEPET", "COK"):
        return s, None
    if isinstance(s, pd.DataFrame):
        s = s.iloc[:, 0]
    return s.rename(hed), hed


def tek_yonlu(s):
    a = s.to_numpy() if isinstance(s, (pd.Series, pd.DataFrame)) else s
    return bool((a >= 0).all() or (a <= 0).all())


def secim(df, donem, giris="K", kor="yok", kom="hisse", rejim="hepsi", h=None, cikis="kapanis"):
    q = (df.donem == donem) & (df.giris == giris) & (df.korunma == kor) & (df.komisyon == kom) & \
        (df.rejim == rejim) & (df.cikis == cikis)
    if h is not None:
        q &= df.h == h
    return df[q]


def gecer(row, cok, tekyon):
    t = row["t_kume"] if cok else row["t_olcekli"]
    ok = (row["net_bps"] > 0) and np.isfinite(t) and t >= 2
    if tekyon:
        ok = ok and row["anormal_bps"] > 0 and np.isfinite(row["t_anormal"]) and row["t_anormal"] >= 2
    return bool(ok), t


# ---------------------------------------------------------------- calistir
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--asama", default="hepsi", choices=["is", "hepsi"])
    a = ap.parse_args()
    t0 = time.time()
    m = M.Motor()
    tk = Takvim(m.idx)
    K = kurallar(m, tk)

    # ileriye bakma denetimi: veri kullanan kurallar
    bakis = {}
    for k in K:
        if callable(k["sig"]) and k["kid"] in ("R7-03a", "R8-12", "R7-09L"):
            fn = (lambda mm, k_=k: (lambda r: r[0] if isinstance(r, tuple) else r)(
                k_["sig"](mm) if k_["kid"] != "R7-09L" else k_["tam"](mm)))
            ok, rap = m.bakis_testi(fn)
            bakis[k["kid"]] = ok
            assert ok, (k["kid"], rap)
    print("bakis_testi:", bakis, f"{time.time() - t0:.0f} sn")

    # ---- 1) yalniz IS
    is_sat, aday = [], []
    test_n = 0
    cache = {}
    for ki, k in enumerate(K):
        s, g = sinyal_al(m, k)
        cache[ki] = (s, g)
        for hed in k["hedefler"]:
            ss, hh = hedef_ve_sinyal(k, s, hed)
            cok = k["cok"]
            tekyon = tek_yonlu(ss)
            yy = yayin_yili(k["kid"])
            nt = f"yayin={yy}; {k['tanim']}"
            r = m.degerlendir(ss, hh, kural_id=k["kid"], aile="E" if not k["kid"].startswith("R7-03") else "H",
                              ad=k["ad"], girdi=k["girdi"], h=k["h"], giris=("K",), gece=False,
                              korunma=("yok",), komisyon=("hisse",), donemler=["IS"], rejimler=False,
                              guc=g, notlar=nt)
            is_sat.append(r)
            for _, row in r.iterrows():
                test_n += 1
                ok, t = gecer(row, cok, tekyon)
                aday.append(dict(ki=ki, kural_id=k["kid"], ad=k["ad"], hedef=row["hedef"], hedef_kod=hed, h=int(row["h"]),
                                 yon=row["yon"], cok=cok, tek_yonlu=tekyon, n_islem=row["n_islem"],
                                 yillik_islem=row["yillik_islem"], net_bps=row["net_bps"],
                                 anormal_bps=row["anormal_bps"], t_karar=t, t_anormal=row["t_anormal"],
                                 aday=ok, yayin=yy))
    A = pd.DataFrame(aday)
    A.to_csv(ADAY, index=False)
    print(f"IS: {test_n} test, {int(A.aday.sum())} aday -> {ADAY}  ({time.time() - t0:.0f} sn)")
    print(A[A.aday].round(2).to_string(index=False))
    IS = pd.concat(is_sat, ignore_index=True)
    if a.asama == "is":
        M.yaz_sonuc(IS, SONUC)
        return

    # ---- 2) OOS ve ayrinti: yalniz adaylar
    tum = [IS]
    oz = []
    islem_k = {}
    for _, ad_ in A[A.aday].iterrows():
        k = K[int(ad_.ki)]
        s, g = cache[int(ad_.ki)]
        ss, hh = hedef_ve_sinyal(k, s, ad_.hedef_kod)
        h = int(ad_.h)
        cok = bool(ad_.cok)
        yy = ad_.yayin
        if ad_.hedef_kod in ("SPY", "CIFT"):
            kor = ("yok",)
        else:
            kor = ("yok", "SPY:250", "SPY:60", "SPXU:250")
        nt = f"yayin={yy}; {k['tanim']}"
        r, isl = m.degerlendir(ss, hh, kural_id=k["kid"], aile="E" if not k["kid"].startswith("R7-03") else "H",
                               ad=k["ad"], girdi=k["girdi"], h=(h,), giris=("K", "A", "G"), gece=True,
                               korunma=kor, guc=g, bootstrap=False, notlar=nt, islem_dondur=True)
        rb = m.degerlendir(ss, hh, kural_id=k["kid"], h=(h,), giris=("K", "A", "G"), gece=False,
                           korunma=("yok",), komisyon=("hisse",), donemler=["IS", "OOS", "SON"],
                           rejimler=False, guc=g, bootstrap=True)
        anah = ["donem", "giris", "h", "cikis", "korunma", "komisyon", "rejim"]
        r = r.drop(columns="p_bootstrap").merge(rb[anah + ["p_bootstrap"]], on=anah, how="left")[M.SEMA]
        r = r[~((r.donem == "IS") & (r.giris == "K") & (r.korunma == "yok") & (r.komisyon == "hisse")
                & (r.rejim == "hepsi") & (r.cikis == "kapanis"))]          # IS satiri zaten var
        tum.append(r)
        o = secim(r, "OOS", h=h).iloc[0]
        ok, t = gecer(o, cok, bool(ad_.tek_yonlu))
        islem_k[(k["kid"], ad_.hedef_kod, h)] = isl
        oz.append(dict(ki=int(ad_.ki), kural_id=k["kid"], ad=k["ad"], hedef=ad_.hedef_kod, h=h, yon=o["yon"], cok=cok,
                       tek_yonlu=bool(ad_.tek_yonlu), yayin=yy, is_net_bps=ad_.net_bps, is_t=ad_.t_karar,
                       oos_n=o["n_islem"], oos_net_bps=o["net_bps"], oos_anormal_bps=o["anormal_bps"],
                       oos_t=t, oos_t_olcekli=o["t_olcekli"], oos_t_kume=o["t_kume"], oos_t_anormal=o["t_anormal"],
                       oos_p=o["p_bootstrap"] if np.isfinite(o["p_bootstrap"]) else 1.0,
                       oos_p_wil=o["p_wilcoxon"], oos_gecti=ok))
        print(f"  {k['kid']:8s} {ad_.hedef_kod:5s} h={h} OOS n={o['n_islem']} net={o['net_bps']:.1f} "
              f"t={t:.2f} tan={o['t_anormal']:.2f} p={o['p_bootstrap']:.3f} gecti={ok}  ({time.time() - t0:.0f} sn)")
    Z = pd.DataFrame(oz)
    if len(Z):
        red, qd = M.bh(Z["oos_p"].to_numpy(), 0.10)
        Z["bh_aile_q"] = qd
        Z["bh_aile_red"] = red

    # ---- 3) gecenler: son donem, A/G, gece, korunma, uygulama (kaldiracli), 15:30, bolumler
    KALD = {"SPY": ("SPXL", "SPXU"), "QQQ": ("TQQQ", "SQQQ"), "IWM": ("TNA", "TZA"), "TLT": ("TMF", None)}
    S30 = None
    ek_kol = {}
    for i, z in Z.iterrows() if len(Z) else []:
        res = tum[1 + i]
        kk = z.kural_id
        h = int(z.h)
        cok = bool(z.cok)
        def al(dn, **kw):
            x = secim(res, dn, h=kw.pop("h", h), **kw)
            return x.iloc[0] if len(x) else None
        son = al("SON")
        A_ = al("OOS", giris="A")
        G_ = al("OOS", giris="G")
        gece = al("OOS", h=0, cikis="acilis")
        tumr = al("TUM")
        ek = dict(son_n=son["n_islem"], son_net_bps=son["net_bps"],
                  son_t=son["t_kume"] if cok else son["t_olcekli"], son_t_anormal=son["t_anormal"],
                  girisA_oos_net_bps=A_["net_bps"], girisA_oos_t=A_["t_kume"] if cok else A_["t_olcekli"],
                  girisG_oos_net_bps=G_["net_bps"], gece_oos_net_bps=gece["net_bps"] if gece is not None else np.nan,
                  basabas_bps=al("OOS")["basabas_bps"], net_sigma=al("OOS")["net_sigma"],
                  yillik_islem=al("OOS")["yillik_islem"], yillik_net_pct=al("OOS")["yillik_net_pct"],
                  oos_wil=al("OOS")["p_wilcoxon"], oos_iyi5suz=al("OOS")["en_iyi5suz_bps"],
                  oos_aysiz=al("OOS")["en_iyi_aysiz_bps"], oos_mal2x=al("OOS")["maliyet2x_net_bps"],
                  isoos_pozyil=al("IS+OOS")["pozitif_yil_orani"],
                  oos_2020siz=al("OOS-2020")["net_bps"], oos_2022siz=al("OOS-2022")["net_bps"],
                  oos_subnis=al("OOS-SubNis2020")["net_bps"],
                  oos_sabit=al("OOS", kom="sabit")["net_bps"], oos_oransal=al("OOS", kom="oransal")["net_bps"],
                  stres_net=al("STRES")["net_bps"])
        for kr in ("SPY:250", "SPY:60", "SPXU:250"):
            x = al("OOS", kor=kr)
            ek[f"oos_kor_{kr}"] = x["net_bps"] if x is not None else np.nan
        isl = islem_k[(kk, z.hedef, h)][("K", h, "kapanis", "yok")]
        tab, bo = m.bolum_ozeti(isl, "hisse")
        ek.update(vix30_bolum=bo.get("bolum_sayisi", 0), vix30_ayni_isaret=bo.get("ayni_isaret_orani", np.nan),
                  vix30_net=bo.get("net_bps", np.nan), vix30_destekli=bo.get("destekli", False))
        # ceyrek sonu ayri (R7-03 ve ay sonu kurallari icin bilgi)
        cey = isl[(isl["donem"] == "OOS") & isl["t"].dt.month.isin([3, 6, 9, 12])]
        ek["oos_ceyrek_sonu_net_bps"] = cey["net_hisse"].mean() * 1e4 if len(cey) else np.nan
        # bagimsiz kontrol: adjclose ile brut ortalama (motor disi)
        ac = m.df("adjclose", ham=True)
        bt = []
        for _, tr in isl[isl["donem"] == "OOS"].iterrows():
            p0 = m.idx.get_loc(tr["t"])
            bt.append(tr["yon"] * (ac[tr["hedef"]].iloc[p0 + h] / ac[tr["hedef"]].iloc[p0] - 1))
        ek["bagimsiz_oos_brut_bps"] = np.mean(bt) * 1e4 if bt else np.nan
        ek["motor_oos_brut_bps"] = al("OOS")["brut_bps"]
        # 15:30 kapanis gercekciligi (son ~730 gun)
        if S30 is None:
            S30 = saatlik()
        a15, kp = S30["acilis_1530"], S30["kapanis"]
        r_k, r_15 = [], []
        if not cok:
            hk = z.hedef
            if hk in a15.columns:
                for _, tr in isl.iterrows():
                    d0 = tr["t"]
                    p0 = m.idx.get_loc(d0)
                    if d0 not in a15.index or p0 + h >= len(m.idx):
                        continue
                    d1 = m.idx[p0 + h]
                    if d1 not in kp.index:
                        continue
                    x0, x15, x1 = kp.at[d0, hk], a15.at[d0, hk], kp.at[d1, hk]
                    if np.isfinite([x0, x15, x1]).all():
                        r_k.append(tr["yon"] * (x1 / x0 - 1))
                        r_15.append(tr["yon"] * (x1 / x15 - 1))
        ek["s1530_n"] = len(r_k)
        ek["s1530_koruma"] = (np.mean(r_15) / np.mean(r_k)) if len(r_k) and np.mean(r_k) != 0 else np.nan
        ek["s1530_brutK_bps"] = np.mean(r_k) * 1e4 if r_k else np.nan
        # uygulama satirlari: kaldiracli/ters ETF (gercek ETF fiyati)
        if not cok and z.hedef in KALD:
            uz, ters = KALD[z.hedef]
            s0, _ = cache[int(z.ki)]
            s0 = s0 if not callable(s0) else s0
            sx = s0.iloc[:, 0] if isinstance(s0, pd.DataFrame) else s0
            for etf, carp in ((uz, 1), (ters, -1)):
                if etf is None or etf == z.hedef:
                    continue
                si = (sx * carp).astype(int).rename(etf)
                if not (si != 0).any():
                    continue
                ru = m.degerlendir(si, etf, kural_id=f"{kk}+{etf}", aile="E", ad=f"{z.ad} [uygulama {etf}]",
                                   girdi="ayni sinyal", h=(h,), giris=("K", "A"), gece=False, korunma=("yok",),
                                   rejimler=False, notlar=f"uygulama satiri, test sayilmaz; yayin={z.yayin}")
                tum.append(ru)
                x = secim(ru, "OOS", h=h).iloc[0]
                y = secim(ru, "SON", h=h).iloc[0]
                ek[f"uyg_{etf}_oos_net"] = x["net_bps"]
                ek[f"uyg_{etf}_oos_t"] = x["t_olcekli"]
                ek[f"uyg_{etf}_son_net"] = y["net_bps"]
        ek_kol[i] = ek
    if len(Z):
        Z = pd.concat([Z, pd.DataFrame.from_dict(ek_kol, orient="index")], axis=1)
        Z["sinif"], Z["gerekce"] = zip(*[sinifla(r) for _, r in Z.iterrows()])
        Z.to_csv(OZET, index=False)
        print(Z.round(3).T.to_string())
    S = pd.concat(tum, ignore_index=True)
    M.yaz_sonuc(S, SONUC)
    print(f"sonuc satiri: {len(S)} -> {SONUC}")

    # ---- 4) takvim 23.11.2026 - 15.01.2027
    tak = []
    for k in K:
        if k["gel"] is None:
            continue
        for p in np.asarray(k["gel"], int):
            if p < 0 or p >= len(tk.C):
                continue
            d = tk.C[p]
            if pd.Timestamp("2026-11-20") <= d <= pd.Timestamp("2027-01-15"):
                for h in k["h"]:
                    if p + h < len(tk.C):
                        tak.append(dict(kural_id=k["kid"], ad=k["ad"], yon=k["yon"], h=h,
                                        giris_kapanis=d.date(), cikis_kapanis=tk.C[p + h].date(),
                                        yarim_gun_giris=d in GELECEK_YARIM,
                                        hedefler="/".join(k["hedefler"])))
    TK = pd.DataFrame(tak).sort_values(["giris_kapanis", "kural_id", "h"])
    if len(Z):
        g = Z[Z.oos_gecti]
        TK["oos_gecti"] = [any((g.kural_id == r.kural_id) & (g.h == r.h)) for r in TK.itertuples()]
    TK.to_csv(TAKVIM, index=False)
    print(TK[TK.get("oos_gecti", False) == True].to_string(index=False) if "oos_gecti" in TK else "")  # noqa: E712
    print(f"bitti {time.time() - t0:.0f} sn")


def sinifla(z):
    """YONTEM 9 onerisi (BH aileler arasi ana ajanda; burada aile ici q kullanilir)."""
    if not z["oos_gecti"]:
        ayni = z["oos_net_bps"] > 0
        return ("DUSUK", "IS ile ayni yon ama OOS t<2") if ayni else ("ELENDI", "OOS'ta ters yon")
    eksik = []
    if not (z["oos_t"] >= 2.5):
        eksik.append("zayiflama(OOS t<2,5)")
    if not z.get("bh_aile_red", False):
        eksik.append("BH")
    if z["oos_n"] < 30:
        eksik.append("az olay")
    if not (z["oos_p"] < 0.05 or z["oos_p_wil"] < 0.05):
        eksik.append("anlamlilik")
    kap = (z.get("girisA_oos_net_bps", -1) > 0 and z.get("girisA_oos_t", 0) >= 1.5) or \
          (z.get("s1530_n", 0) >= 30 and z.get("s1530_koruma", 0) >= 0.7)
    if not kap:
        eksik.append("uygulama(kapanis)")
    if not (z.get("son_net_bps", -1) > 0 and z.get("son_t", 0) >= 1.0):
        eksik.append("zayiflama(son donem)")
    if not (z.get("oos_iyi5suz", -1) > 0 and z.get("oos_aysiz", -1) > 0 and z.get("oos_mal2x", -1) > 0):
        eksik.append("saglamlik")
    if not (z.get("oos_net_bps", 0) >= 10 and z.get("net_sigma", 0) >= 0.10 and z.get("yillik_net_pct", 0) >= 3):
        eksik.append("ekonomik taban")
    if not eksik:
        return "UYGUN", "butun olcutler saglandi (bagimsiz kod ve aileler arasi BH ana ajanda)"
    return "KOSULLU", "; ".join(eksik)


if __name__ == "__main__":
    main()
