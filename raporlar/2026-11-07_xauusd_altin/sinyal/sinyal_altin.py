#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sinyal_altin.py — altın için günlük sinyal betiği (VİOP F_XAUUSD ve Midas ABD ETF'leri).

Hakem sentezinde (out/sentez/HAKEM.md, sinyal_tablosu.csv) ayakta kalan 11 kuralı tek dosyada hesaplar:
  VİOP : A1-LOWMOM-h1 (+ h5 tutuş varyantı), A3_QEND_h3, A4-C1_GDXJ_artik_h3, A8-3_seg_last1h_h5
  ETF  : E1-C2_GDX_tatil_oncesi, E2-C2j, E2-C2, E2-C1 (+ kaplama sürümü), E3-1, E3-3 (PHYS/GLD), E3-4 (CEF)

Modlar
  --canli [--tarih G]            ağdan indirir: Dukascopy bi5 (LZMA), Yahoo v8 chart JSON, Borsa İstanbul VİOP bülteni,
                                 ABD Hazinesi CSV. --tarih verilmezse bugün (İstanbul); işlem günü değilse bir sonraki işlem günü.
  --panel --tarih G              araştırma panellerinden (panel_viop/spot/etf.parquet) geçmiş bir günü yeniden üretir.

İleriye bakma denetimi
  Her gözlem kendi yayın/kapanış zamanıyla (UTC) taşınır. Bir cephe için önce karar anı belirlenir
  (VİOP: gün t 15:00 UTC, TR yarım gününde 09:30 UTC; ETF: gün t 15:00 ET, ABD yarım gününde 12:00 ET).
  Hesapta yalnız zaman damgası karar anından önce (≤) olan veriler kullanılır; her kullanım 'denetim' tablosuna yazılır.
  İhlal görülürse o sinyal üretilmez (IleriyeBakma hatası). Gerçek saat karar anından önceyse sinyal 'ÖN-İZLEME' ya da
  'BEKLİYOR' diye işaretlenir; eksik veride 'HESAPLANAMADI'.

Bağımlılıklar: pandas, numpy, requests + standart kütüphane (lzma, struct, zoneinfo, json, argparse).
Çalıştırma: python3 -W ignore sinyal_altin.py --canli            |  python3 -W ignore sinyal_altin.py --panel --tarih 2026-11-06
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import datetime as dt
import shutil
import threading
import json
import lzma
import math
import os
import random
import struct
import sys
import time
import urllib.parse
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
import requests

SURUM = "1.0 (2026-11-08)"
TZ_TR = ZoneInfo("Europe/Istanbul")
TZ_NY = ZoneInfo("America/New_York")
UTC = dt.timezone.utc
BURASI = os.path.dirname(os.path.abspath(__file__))

# =====================================================================================================================
# 1. PARAMETRELER (hakem tablosu; eşikler IS döneminde donduruldu — out/sentez/esikler.json)
# =====================================================================================================================
P = dict(
    LOWMOM_K=5, LOWMOM_RV=20, LOWMOM_Q=1 / 3, LOWMOM_MINP=250, SPOT_BASLANGIC="2010-01-04",
    A4_BETA=60, A4_BETA_MINP=40, A4_STD=120, A4_STD_MINP=60, A4_ESIK=0.43, A4_GECMIS=600,
    E2_BETA=250, E2_BETA_MINP=60, E2_BASLANGIC="2008-01-01",
    PHYS_K=60, PHYS_STD=250, PHYS_ESIK=-1.5, CEF_BETA=250, CEF_K=60, CEF_STD=250, CEF_ESIK=-2.0,
    PSR=0.10, ARACI_PSR=0.20, NOMINAL_TAVAN=2.0,
)
E2 = {  # x = madenci artığı k günlük toplam (t-1'de biter); IS (2008–2017) kantil eşikleri
    "E2-C2j_GDXJ_artik_h3": dict(y="GDXJ", k=1, h=3, q=0.70, hi=0.006671748163646159, lo=-0.009247357938417262, arac="GDXJ"),
    "E2-C2_GDX_artik_h3": dict(y="GDX", k=3, h=3, q=0.70, hi=0.00806428927236583, lo=-0.013474905841117723, arac="GDX"),
    "E2-C1_madenci_oncu_GLD_h5": dict(y="GDX", k=10, h=5, q=0.80, hi=0.02514805305931152, lo=-0.040224303799222996, arac="GLD"),
}
ETF_TICKER = ["GLD", "GDX", "GDXJ", "SPY", "PHYS", "CEF", "SLV"]

# Ayakta kalan sinyaller: güven etiketi (hakem son güveni = min(REP, ADV)), kural özeti, hakem notu
BILGI = {
    "A1-LOWMOM-h1": dict(cephe="VIOP", guven="DÜŞÜK", h=1, arac="F_XAUUSD", ad="Sakin piyasa momentumu",
                         kural="x=ln(P_t/P_t-5), P=spot 15:00 UTC; rv20 yüzdeliği (2010'dan beri, bugün dahil) <1/3 ise sign(x) yönünde 1 birim, t+1 uzlaşmasında kapat; TR yarım günü hariç",
                         bilgi="gün t 15:00 UTC spot (Dukascopy)",
                         not_="Hakem OOS net Sharpe 1,35 (B&H 0,62). Izgara tepesi; kazanç birkaç sakin döneme yığılı; birincil q 0,33. 2026 oynaklığında yapısal olarak pasif."),
    "A3_QEND_h3": dict(cephe="VIOP", guven="DÜŞÜK", h=3, arac="F_XAUUSD", ad="Çeyrek sonu",
                       kural="Mar/Haz/Eyl/Ara'nın sondan 2. VİOP günü uzlaşmasında UZUN, 3 VİOP günü sonra kapat",
                       bilgi="takvim (önceden bilinir)",
                       not_="Olay başına +76,7 bps, yılda 4 işlem; sağlam kısmı yıl dönümü; tatil öncesi GDX ile aynı takvim ailesi; q 0,33."),
    "A4-C1_GDXJ_artik_h3": dict(cephe="VIOP", guven="DÜŞÜK", h=3, arac="F_XAUUSD", ad="GDXJ artığı (VİOP)",
                                kural="e=r_GDXJ−β60·r_GLD (t-2→t-1 ABD kapanışı, VİOP satırlarında fark), z=e/std(e, önceki 120 gün); z>0,43 UZUN, z<−0,43 KISA; 3 gün kademeli",
                                bilgi="t-1 16:00 ET ABD kapanışı",
                                not_="E2-C2j ile aynı öngörücü (sıra korelasyonu 0,87): iki cephede tek fenomen say, birini seç ya da yarım ağırlık ver. Kural P&L t'si zayıf; q 0,29."),
    "A8-3_seg_last1h_h5": dict(cephe="VIOP", guven="DÜŞÜK", h=5, arac="F_XAUUSD", ad="Son saat momentumu",
                               kural="pos=sign(ln(spot 15:00/spot 14:00 UTC)); t uzlaşmasında gir, 5 gün kademeli; TR yarım günü hariç",
                               bilgi="gün t 14:00 ve 15:00 UTC spot",
                               not_="2026 Sharpe 1,93 ama 2024'te −2,31; 2010–16'da yok; 309 testten seçildi; q 0,50."),
    "E1-C2_GDX_tatil_oncesi": dict(cephe="ETF", guven="ORTA", h=1, arac="GDX", ad="Tatil öncesi GDX",
                                   kural="NYSE tatilinden önceki son işlem gününden bir önceki kapanışta GDX al, tatil öncesi günün kapanışında sat; yalnız uzun",
                                   bilgi="takvim (NYSE)",
                                   not_="Olay başına +47 bps, yılda ~9 işlem; OOS 0,75 (B&H 0,60); aynı gün altın kontrolüyle etki yarıya iniyor; q 0,126."),
    "E2-C2j_GDXJ_artik_h3": dict(cephe="ETF", guven="ORTA", h=3, arac="GDXJ", ad="GDXJ artık momentumu",
                                 kural="e=r_GDXJ−b_GLD·r_GLD−b_SPY·r_SPY (250g OLS, β_t-1); x=e_t-1 > IS %70 kantili (+%0,667) ise GDXJ al, 3 gün kademeli; aksi nakit",
                                 bilgi="t-1 16:00 ET kapanışı",
                                 not_="OOS 0,81 (B&H 0,54, basit getiri); 2026 Sharpe 0,21; dürüst geniş ızgara IS seçimiyle OOS≈0; q 0,056. A4-C1 ile aynı fenomen."),
    "E2-C2_GDX_artik_h3": dict(cephe="ETF", guven="ORTA", h=3, arac="GDX", ad="GDX artık momentumu",
                               kural="GDX'in GLD+SPY'ye göre 3 günlük artık toplamı (t-1'de biter) > IS %70 kantili (+%0,806) ise GDX al, 3 gün kademeli; aksi nakit",
                               bilgi="t-1 16:00 ET kapanışı",
                               not_="C2j ile aynı aile; 2022+ döneminde B&H'nin altında (0,69'a karşı 0,77); q 0,069."),
    "E2-C1_madenci_oncu_GLD_h5": dict(cephe="ETF", guven="ORTA", h=5, arac="GLD", ad="Madenci öncülüğü → GLD",
                                      kural="GDX'in GLD+SPY'ye göre 10 günlük artık toplamı > IS %80 kantili (+%2,515) ise GLD al, 5 gün kademeli; aksi nakit. Kaplama: GLD tut, yalnız < %20 kantilde (−%4,02) nakit",
                                      bilgi="t-1 16:00 ET kapanışı",
                                      not_="OOS t 1,94; yalnız uzun sürüm B&H'yi geçmiyor (0,78'e karşı 0,81); q 0,019."),
    "E3-1_altin_gunici_GDXJ_donus": dict(cephe="ETF", guven="ORTA", h=1, arac="GDXJ", ad="Altın gün içi → GDXJ dönüşü",
                                         kural="m_t=ln(spot 15:00 ET_t / spot 16:00 ET_t-1) < 0 ise GDXJ'yi t kapanışında al, t+1 kapanışında sat (koşul sürerse koru); aksi nakit; ABD yarım günü hariç",
                                         bilgi="gün t 15:00 ET spot",
                                         not_="Bonferroni'yi geçen tek fenomen (q 0,0001); ama B&H'ye göre OOS net alfa 10 bps maliyette t 1,4; yılda ~66 gidiş-dönüş."),
    "E3-3_PHYS_GLD_iskonto": dict(cephe="ETF", guven="ORTA", h=5, arac="PHYS/GLD", ad="PHYS/GLD iskontosu (araç seçimi)",
                                  kural="z=[ln(PHYS/GLD)_t-1 − 60g medyan]/250g std; altın alınacaksa ve z<−1,5 ise GLD yerine PHYS",
                                  bilgi="t-1 16:00 ET kapanışı",
                                  not_="Yönlü sinyal değil; fark küçük (z<−2 iken 5 günde +19–21 bps); Midas'ta PHYS listelendiği teyit edilmedi."),
    "E3-4_CEF_artik": dict(cephe="ETF", guven="ORTA", h=5, arac="CEF", ad="CEF artığı (araç seçimi)",
                           kural="CEF'in GLD+SLV'ye göre artık seviyesinin z'si (60g medyan, 250g std; t-1) < −2 ise CEF'i tercih et",
                           bilgi="t-1 16:00 ET kapanışı",
                           not_="Yönlü sinyal değil; geçiş kuralı OOS'ta başarısız; Midas'ta CEF listelendiği teyit edilmedi."),
}

# =====================================================================================================================
# 2. TAKVİMLER (yerleşik; panel 2017–2026 ile birebir doğrulandı — bkz. KULLANIM.md)
# =====================================================================================================================
# Türkiye resmi tatilleri (yalnız hafta içine düşenler; 'holidays' paketi ile üretildi, VİOP 2017-03..2026-11 takvimiyle birebir)
_TR_TATIL_STR = (
    "20100101 20100423 20100519 20100830 20100909 20100910 20101029 20101116 20101117 20101118 20101119 20110519 20110830 20110831 "
    "20110901 20111107 20111108 20111109 20120423 20120501 20120820 20120821 20120830 20121025 20121026 20121029 20130101 20130423 "
    "20130501 20130808 20130809 20130830 20131015 20131016 20131017 20131018 20131029 20140101 20140423 20140501 20140519 20140728 "
    "20140729 20140730 20141006 20141007 20141029 20150101 20150423 20150501 20150519 20150717 20150924 20150925 20151029 20160101 "
    "20160519 20160705 20160706 20160707 20160830 20160912 20160913 20160914 20160915 20170501 20170519 20170626 20170627 20170830 "
    "20170901 20170904 20180101 20180423 20180501 20180615 20180821 20180822 20180823 20180824 20180830 20181029 20190101 20190423 "
    "20190501 20190604 20190605 20190606 20190715 20190812 20190813 20190814 20190830 20191029 20200101 20200423 20200501 20200519 "
    "20200525 20200526 20200715 20200731 20200803 20201029 20210101 20210423 20210513 20210514 20210519 20210715 20210720 20210721 "
    "20210722 20210723 20210830 20211029 20220502 20220503 20220504 20220519 20220711 20220712 20220715 20220830 20230421 20230501 "
    "20230519 20230628 20230629 20230630 20230830 20240101 20240410 20240411 20240412 20240423 20240501 20240617 20240618 20240619 "
    "20240715 20240830 20241029 20250101 20250331 20250401 20250423 20250501 20250519 20250606 20250609 20250715 20251029 20260101 "
    "20260320 20260423 20260501 20260519 20260527 20260528 20260529 20260715 20261029 20270101 20270309 20270310 20270311 20270423 "
    "20270517 20270518 20270519 20270715 20270830 20271029")
# Türkiye yarım günleri (arife + 28 Ekim, hafta içi): uzlaşma 12:30–12:40 TSİ (09:30–09:40 UTC); akşam seansı yok
_TR_YARIM_STR = ("20100908 20101028 20101115 20111028 20121024 20130807 20131014 20131028 20141003 20141028 20150716 20150923 "
                 "20151028 20160704 20161028 20170831 20180614 20180820 20190603 20191028 20200730 20201028 20210512 20210719 "
                 "20211028 20220708 20221028 20230420 20230627 20240409 20241028 20250605 20251028 20260319 20260526 20261028 "
                 "20270308 20271028")
TR_TATIL = {dt.datetime.strptime(s, "%Y%m%d").date() for s in _TR_TATIL_STR.split()}
TR_YARIM = {dt.datetime.strptime(s, "%Y%m%d").date() for s in _TR_YARIM_STR.split()}
TR_KAPSAM = (dt.date(2010, 1, 1), dt.date(2027, 12, 31))
NYSE_ADHOC = {dt.date(2012, 10, 29), dt.date(2012, 10, 30), dt.date(2018, 12, 5), dt.date(2025, 1, 9)}  # plansız kapanışlar

# ABD olay takvimi (out/a3_takvim_olay/events_*.csv'den; UTC saatleri). --olay-dizini ile CSV'ler okunursa genişletilir.
FOMC = {"2025-01-29": "19:00", "2025-03-19": "18:00", "2025-05-07": "18:00", "2025-06-18": "18:00", "2025-07-30": "18:00",
        "2025-09-17": "18:00", "2025-10-29": "18:00", "2025-12-10": "19:00", "2026-01-28": "19:00", "2026-03-18": "18:00",
        "2026-04-29": "18:00", "2026-06-17": "18:00", "2026-07-29": "18:00", "2026-09-16": "18:00", "2026-10-28": "18:00",
        "2026-12-09": "19:00", "2027-01-27": "19:00", "2027-03-17": "18:00", "2027-04-28": "18:00", "2027-06-09": "18:00",
        "2027-07-28": "18:00", "2027-09-15": "18:00", "2027-10-27": "18:00", "2027-12-08": "19:00"}
NFP = {"2025-01-10": "13:30", "2025-02-07": "13:30", "2025-03-07": "13:30", "2025-04-04": "12:30", "2025-05-02": "12:30",
       "2025-06-06": "12:30", "2025-07-03": "12:30", "2025-08-01": "12:30", "2025-09-05": "12:30", "2025-11-20": "13:30",
       "2025-12-16": "13:30", "2026-01-09": "13:30", "2026-02-11": "13:30", "2026-03-06": "13:30", "2026-04-03": "12:30",
       "2026-05-08": "12:30", "2026-06-05": "12:30", "2026-07-02": "12:30", "2026-08-07": "12:30", "2026-09-04": "12:30",
       "2026-10-02": "12:30", "2026-11-06": "13:30", "2026-12-04": "13:30"}
CPI = {"2025-01-15": "13:30", "2025-02-12": "13:30", "2025-03-12": "12:30", "2025-04-10": "12:30", "2025-05-13": "12:30",
       "2025-06-11": "12:30", "2025-07-15": "12:30", "2025-08-12": "12:30", "2025-09-11": "12:30", "2025-10-24": "12:30",
       "2025-12-18": "13:30", "2026-01-13": "13:30", "2026-02-13": "13:30", "2026-03-11": "12:30", "2026-04-10": "12:30",
       "2026-05-12": "12:30", "2026-06-10": "12:30", "2026-07-14": "12:30", "2026-08-12": "12:30", "2026-09-11": "12:30",
       "2026-10-14": "12:30"}
CPI_TAHMINI = {"2026-11-10": "13:30", "2026-12-10": "13:30"}  # BLS 2026 takviminden hatırlanan; KONTROL EDİN
TAKVIM_SONU = dict(NFP="2026-12-04", CPI="2026-10-14", FOMC="2027-12-08")


def tr_is_gunu(d: dt.date) -> bool:
    return d.weekday() < 5 and d not in TR_TATIL


def tr_yarim(d: dt.date) -> bool:
    return d in TR_YARIM


def viop_gunleri(a: dt.date, b: dt.date) -> list:
    out, d = [], a
    while d <= b:
        if tr_is_gunu(d): out.append(d)
        d += dt.timedelta(days=1)
    return out


def _nth(y, m, wd, n):
    if n > 0:
        d = dt.date(y, m, 1)
        d += dt.timedelta(days=(wd - d.weekday()) % 7)
        return d + dt.timedelta(weeks=n - 1)
    d = dt.date(y, m + 1, 1) - dt.timedelta(days=1) if m < 12 else dt.date(y, 12, 31)
    return d - dt.timedelta(days=(d.weekday() - wd) % 7)


def _paskalya(y):
    a, b, c = y % 19, y // 100, y % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l_ = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l_) // 451
    return dt.date(y, (h + l_ - 7 * m + 114) // 31, ((h + l_ - 7 * m + 114) % 31) + 1)


def _gozlenen(d):
    return d - dt.timedelta(days=1) if d.weekday() == 5 else (d + dt.timedelta(days=1) if d.weekday() == 6 else d)


_NYSE_CACHE: dict = {}


def nyse_tatilleri(y: int) -> dict:
    """NYSE düzenli tatilleri (gözlenen tarih → ad). Yılbaşı Cumartesiye düşerse kapanış yok (NYSE kuralı)."""
    if y in _NYSE_CACHE: return _NYSE_CACHE[y]
    T = {}
    ny = dt.date(y, 1, 1)
    if ny.weekday() == 6: T[dt.date(y, 1, 2)] = "Yılbaşı (gözlenen)"
    elif ny.weekday() < 5: T[ny] = "Yılbaşı"
    T[_nth(y, 1, 0, 3)] = "Martin Luther King Jr. Günü"
    T[_nth(y, 2, 0, 3)] = "Başkanlar Günü"
    T[_paskalya(y) - dt.timedelta(days=2)] = "Kutsal Cuma"
    T[_nth(y, 5, 0, -1)] = "Anma Günü (Memorial Day)"
    if y >= 2022: T[_gozlenen(dt.date(y, 6, 19))] = "Juneteenth"
    T[_gozlenen(dt.date(y, 7, 4))] = "Bağımsızlık Günü"
    T[_nth(y, 9, 0, 1)] = "İşçi Günü (Labor Day)"
    T[_nth(y, 11, 3, 4)] = "Şükran Günü"
    T[_gozlenen(dt.date(y, 12, 25))] = "Noel"
    _NYSE_CACHE[y] = T
    return T


def spot_kapali(d: dt.date) -> bool:
    """Dukascopy XAUUSD'nin 15:00 UTC fiyatının olmadığı günler (panel 2010–2026): 1 Ocak, 25 Aralık, Kutsal Cuma (2013+)
    ve NYSE'nin bunlar için gözlenen tatilleri (ör. 26 Aralık, 2 Ocak, 24 Aralık 2021)."""
    if (d.month, d.day) in ((1, 1), (12, 25)): return True
    ad = nyse_tatilleri(d.year).get(d, "")
    return ad.startswith(("Yılbaşı", "Noel")) or (ad == "Kutsal Cuma" and d.year >= 2013)


def nyse_yarim(d: dt.date) -> bool:
    """13:00 ET erken kapanış: 3 Temmuz (Pzt–Prş), Şükran Günü ertesi Cuma, 24 Aralık (Pzt–Prş)."""
    y = d.year
    if d == dt.date(y, 7, 3) and d.weekday() <= 3: return True
    if d == _nth(y, 11, 3, 4) + dt.timedelta(days=1): return True
    if d == dt.date(y, 12, 24) and d.weekday() <= 3: return True
    return False


def nyse_is_gunu(d: dt.date) -> bool:
    return d.weekday() < 5 and d not in nyse_tatilleri(d.year) and d not in NYSE_ADHOC


def nyse_gunleri(a: dt.date, b: dt.date) -> list:
    out, d = [], a
    while d <= b:
        if nyse_is_gunu(d): out.append(d)
        d += dt.timedelta(days=1)
    return out


def sonraki(d, fn, n=1):
    k = 0
    while True:
        d += dt.timedelta(days=1)
        if fn(d):
            k += 1
            if k == n: return d


def onceki(d, fn, n=1):
    k = 0
    while True:
        d -= dt.timedelta(days=1)
        if fn(d):
            k += 1
            if k == n: return d


def og_vade(y: int, m: int) -> dt.date:
    """COMEX altın opsiyonu (OG) son işlem günü: ayın sondan 4. iş günü; Cuma ya da tatil arifesiyse bir önceki iş günü."""
    hol = set(nyse_tatilleri(y)) | NYSE_ADHOC
    son = (dt.date(y, m + 1, 1) if m < 12 else dt.date(y + 1, 1, 1)) - dt.timedelta(days=1)
    bd = [dt.date(y, m, i) for i in range(1, son.day + 1)]
    bd = [d for d in bd if d.weekday() < 5 and d not in hol]
    og = bd[-4]
    if og.weekday() == 4 or (og + dt.timedelta(days=1)) in hol:
        og = [d for d in bd if d < og][-1]
    return og


def viop_vade_son_gunu(code: str) -> dt.date | None:
    """F_XAUUSD1226 → Aralık 2026'nın son VİOP iş günü (vade sonu)."""
    try:
        mm, yy = int(code[-4:-2]), 2000 + int(code[-2:])
    except Exception:
        return None
    d = (dt.date(yy, mm + 1, 1) if mm < 12 else dt.date(yy + 1, 1, 1)) - dt.timedelta(days=1)
    while not tr_is_gunu(d): d -= dt.timedelta(days=1)
    return d


def utc(d: dt.date, hh: int, mm: int = 0) -> pd.Timestamp:
    return pd.Timestamp(dt.datetime(d.year, d.month, d.day, hh, mm, tzinfo=UTC))


def et(d: dt.date, hh: int, mm: int = 0) -> pd.Timestamp:
    return pd.Timestamp(dt.datetime(d.year, d.month, d.day, hh, mm, tzinfo=TZ_NY)).tz_convert("UTC")


def et16(gunler) -> pd.DatetimeIndex:
    """Gün listesi → o günün 16:00 ET anı (UTC), vektörel."""
    g = pd.DatetimeIndex(pd.to_datetime(list(gunler))) + pd.Timedelta(hours=16)
    return g.tz_localize(TZ_NY, nonexistent="shift_forward", ambiguous="NaT").tz_convert("UTC").as_unit("ns")


def asof_once(k: pd.DataFrame, kesimler: list):
    """Her kesim anı için avail < kesim olan son kapanış (kesinlikle önce). Döndür: (değer, gün, avail) listeleri."""
    k = k[k["close"].notna()]
    if not len(k): return [np.nan] * len(kesimler), [None] * len(kesimler), [None] * len(kesimler)
    av = pd.DatetimeIndex(k["avail"]).as_unit("ns").asi8
    ct = pd.DatetimeIndex(kesimler).as_unit("ns").asi8
    idx = np.searchsorted(av, ct, side="left") - 1
    cl = k["close"].values; gi = list(k.index); avl = list(k["avail"])
    return ([float(cl[i]) if i >= 0 else np.nan for i in idx], [gi[i] if i >= 0 else None for i in idx], [avl[i] if i >= 0 else None for i in idx])


def viop_karar(d: dt.date) -> pd.Timestamp:
    return utc(d, 9, 30) if tr_yarim(d) else utc(d, 15, 0)


def etf_karar(d: dt.date) -> pd.Timestamp:
    return et(d, 12, 0) if nyse_yarim(d) else et(d, 15, 0)


# =====================================================================================================================
# 3. YARDIMCILAR: biçim, denetim
# =====================================================================================================================
class IleriyeBakma(Exception):
    pass


DENETIM: list = []


def kontrol(veri: str, gozlem_ts, karar: pd.Timestamp, sinyal: str):
    """Kullanılan en son gözlemin zamanı karar anından sonra olamaz. Her çağrı denetim tablosuna yazılır."""
    if gozlem_ts is None or (isinstance(gozlem_ts, float) and not np.isfinite(gozlem_ts)):
        DENETIM.append(dict(sinyal=sinyal, veri=veri, son_gozlem_utc=None, karar_utc=str(karar), sonuc="VERİ YOK"))
        return False
    g = pd.Timestamp(gozlem_ts)
    if g.tzinfo is None: g = g.tz_localize("UTC")
    ok = g <= karar
    DENETIM.append(dict(sinyal=sinyal, veri=veri, son_gozlem_utc=str(g.tz_convert("UTC")), karar_utc=str(karar), sonuc="OK" if ok else "İHLAL"))
    if not ok: raise IleriyeBakma(f"{sinyal}: {veri} gözlemi {g} > karar anı {karar}")
    return True


def fs(x, nd=2, isaret=False, yuzde=False):
    """Türkçe sayı biçimi (binlik nokta, ondalık virgül)."""
    if x is None: return "—"
    try:
        xf = float(x)
    except Exception:
        return str(x)
    if not np.isfinite(xf): return "—"
    if yuzde: xf *= 100
    s = f"{xf:+,.{nd}f}" if isaret else f"{xf:,.{nd}f}"
    s = s.replace(",", "§").replace(".", ",").replace("§", ".")
    return ("%" + s) if yuzde and not isaret else (s[0] + "%" + s[1:] if yuzde else s)


def tsi(ts: pd.Timestamp) -> str:
    return pd.Timestamp(ts).tz_convert(TZ_TR).strftime("%H:%M TSİ")


def gun_adi(d: dt.date) -> str:
    return ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"][d.weekday()]


def kademe(pos: dict, gunler: list, t: dt.date, h: int):
    """pos: gün → yeni dilim (−1..1). Etkin pozisyon (t uzlaşması/kapanışı sonrası) = son h dilimin ortalaması.
    Döndür: (yeni, açık dilimler {gün: dilim}, etkin_t, etkin_onceki, bugünkü işlem)."""
    i = gunler.index(t)
    son = [gunler[i - k] for k in range(h) if i - k >= 0]
    onc = [gunler[i - k] for k in range(1, h + 1) if i - k >= 0]
    v = lambda d: float(pos.get(d, 0.0) or 0.0)
    eff = sum(v(d) for d in son) / h
    effp = sum(v(d) for d in onc) / h
    acik = {str(d): v(d) for d in son[1:]}
    return v(t), acik, eff, effp, eff - effp


# =====================================================================================================================
# 4. AĞ KATMANI (yeniden deneme, geri çekilme, önbellek)
# =====================================================================================================================
class AgHatasi(Exception):
    pass


class Ag:
    def __init__(self, onbellek: str, deneme: int = int(os.environ.get("SINYAL_AG_DENEME", "7")), log=print):
        self.onbellek = onbellek
        os.makedirs(onbellek, exist_ok=True)
        self.deneme = deneme
        self.log = log
        self._yerel = threading.local()
        self.istek = 0
        self._ardisik_hata = {}   # ana bilgisayar → art arda kalıcı başarısızlık sayısı (devre kesici)
        self._basarili = set()    # bu çalıştırmada en az bir kez yanıt veren ana bilgisayarlar
        self._agsiz_host = set()  # hiç yanıt vermeden devre kesiciye düşen ana bilgisayarlar
        self._kilit = threading.Lock()

    @staticmethod
    def _baglanti_yok(e: Exception) -> bool:
        """Ağın/vekil sunucunun hiç olmadığını gösteren hata (sıfırlanan bağlantı, zaman aşımı ve 5xx değil)."""
        if isinstance(e, requests.exceptions.ProxyError): return True
        m = repr(e)
        return any(k in m for k in ("NewConnectionError", "NameResolutionError", "Failed to resolve", "Name or service not known",
                                     "getaddrinfo failed", "Network is unreachable", "Connection refused"))

    @property
    def s(self):
        if not hasattr(self._yerel, "s"): self._yerel.s = self._oturum()
        return self._yerel.s

    @s.setter
    def s(self, v):
        self._yerel.s = v

    @staticmethod
    def _oturum():
        s = requests.Session()
        s.headers["User-Agent"] = "Mozilla/5.0 (sinyal_altin.py)"
        return s

    def al(self, url: str, yol: str | None = None, kalici: bool = False, zaman_asimi: int = 45, bekle: float = 0.15, deneme: int | None = None,
           bos_kabul: bool = True):
        """200 → içerik; 404 → b'' ; kalıcı başarısızlık → None. kalici=True ise önbellekteki dosya kullanılır; önbellekteki BOŞ dosyaya
        (eski 404) yalnız bos_kabul=True ise güvenilir (henüz yayımlanmamış dosyanın 404'ü kalıcı eksik sayılmasın diye)."""
        if yol and kalici and os.path.exists(yol):
            b = open(yol, "rb").read()
            if b or bos_kabul: return b
        host = urllib.parse.urlparse(url).netloc
        if self._ardisik_hata.get(host, 0) >= 3:
            return None  # devre kesici: bu kaynak art arda 3 kez yanıt vermedi; bu çalıştırmada atlanır
        if len(self._agsiz_host) >= 2 and host not in self._basarili:
            return None  # iki kaynak hiç bağlanamadı: ağ yok sayılır, beklemeden geç
        son_hata = None
        yok_say = 0
        for a in range(deneme or self.deneme):
            try:
                self.istek += 1
                r = self.s.get(url, timeout=zaman_asimi)
                if r.status_code in (200, 404):
                    with self._kilit: self._ardisik_hata[host] = 0; self._basarili.add(host)
                if r.status_code == 200:
                    if yol:
                        os.makedirs(os.path.dirname(yol), exist_ok=True)
                        with open(yol + ".part", "wb") as f: f.write(r.content)
                        os.replace(yol + ".part", yol)
                    time.sleep(bekle)
                    return r.content
                if r.status_code == 404:
                    if yol and kalici:
                        os.makedirs(os.path.dirname(yol), exist_ok=True)
                        open(yol, "wb").close()
                    return b""
                son_hata = f"HTTP {r.status_code}"
            except requests.RequestException as e:
                son_hata = type(e).__name__
                self.s = self._oturum()
                if self._baglanti_yok(e) and host not in self._basarili:
                    yok_say += 1
                    if yok_say >= 3: break  # bağlantı hiç kurulamıyor: uzun geri çekilmeyle bekleme
                    time.sleep(0.5); continue
            time.sleep(min(25.0, 0.8 * 1.8 ** a) + random.uniform(0, 0.6))
        with self._kilit:
            self._ardisik_hata[host] = self._ardisik_hata.get(host, 0) + 1
            if self._ardisik_hata[host] == 3:
                self.log(f"  [ağ] {host} art arda 3 kez yanıt vermedi; bu çalıştırmada atlanıyor (ilgili sinyaller HESAPLANAMADI)")
                if host not in self._basarili:
                    self._agsiz_host.add(host)
                    if len(self._agsiz_host) == 2:
                        self.log("  [ağ] iki kaynağa hiç bağlanılamadı: ağ bağlantısı yok sayılıyor; kalan kaynaklar önbellekten (varsa) okunacak")
        self.log(f"  [ağ] başarısız: {url} ({son_hata})")
        return None


# =====================================================================================================================
# 5. VERİ KAYNAKLARI
# =====================================================================================================================
def _bi5_mum(b: bytes, taban: pd.Timestamp, nokta=1e3) -> pd.DataFrame:
    """Dukascopy mum dosyası (LZMA): kayıt >iiiiif = (saniye, açılış, kapanış, düşük, yüksek, hacim). Hacmi 0 olanlar atılır."""
    if not b: return pd.DataFrame(columns=["t", "c"])
    raw = lzma.decompress(b)
    a = np.frombuffer(raw, dtype=">i4").reshape(-1, 6).astype(np.int64)  # büyük-endian → yerel
    vol = np.frombuffer(raw, dtype=">f4").reshape(-1, 6)[:, 5].astype(np.float64)
    d = pd.DataFrame({"t": taban + pd.to_timedelta(a[:, 0], unit="s"), "c": a[:, 2] / nokta, "v": vol})
    return d[d.v > 0][["t", "c"]]


def _bi5_tick(b: bytes, taban: pd.Timestamp, nokta=1e3) -> pd.DataFrame:
    """Dukascopy saatlik tick dosyası: kayıt >IIIff = (ms, ask, bid, ask hacmi, bid hacmi). BID kullanılır (mumlar BID)."""
    if not b: return pd.DataFrame(columns=["t", "c"])
    raw = lzma.decompress(b)
    rs = struct.calcsize(">IIIff")  # 20 bayt
    n = len(raw) // rs
    if n == 0: return pd.DataFrame(columns=["t", "c"])
    a = np.frombuffer(raw[: n * rs], dtype=">u4").reshape(-1, 5)
    return pd.DataFrame({"t": taban + pd.to_timedelta(a[:, 0].astype(np.int64), unit="ms"), "c": a[:, 2].astype(np.int64) / nokta})


def _saatlik_nokta(d: pd.DataFrame, bar_dk: int) -> pd.Series:
    """Mum/tick tablosundan saatlik kapanış noktaları: anı = saat sonu (bar başlangıcı + 1 saat), değer = saatteki son fiyat."""
    if d is None or len(d) == 0: return pd.Series(dtype=float)
    t = pd.DatetimeIndex(d["t"])
    s = pd.Series(d["c"].values, index=t).sort_index()
    g = s.groupby(s.index.floor("1h")).last()
    g.index = g.index + pd.Timedelta(hours=1)
    return g


def snap(seri: pd.Series, T: pd.Timestamp, bayat=pd.Timedelta(hours=1)):
    """T anındaki (T dahil) son değer; T'den en çok 'bayat' önce olmalı (panel kurucusundaki snap ile aynı kural)."""
    if seri is None or len(seri) == 0: return np.nan, None
    i = seri.index.searchsorted(T, side="right") - 1
    if i < 0: return np.nan, None
    ts = seri.index[i]
    if T - ts > bayat: return np.nan, ts
    return float(seri.iloc[i]), ts


class PanelKaynak:
    """Araştırma panellerinden okur. Her değer kendi zaman damgasıyla verilir:
       spot s_p15 → gün 15:00 UTC; xau_p14/p15 → gün 14:00/15:00 UTC; xau_cut → gün 15:00 ET; xau_close → gün 16:00 ET;
       c_<ETF> (temettü düzeltmeli kapanış) → gün 16:00 ET. gpr_* ve *_prev sütunları (bilinen hatalar) kullanılmaz."""
    mod = "panel"

    def __init__(self, pdir: str, log=print):
        self.log = log
        V = pd.read_parquet(os.path.join(pdir, "panel_viop.parquet"),
                            columns=["xau_p14", "xau_p15", "v_settle", "v_code", "v_expiry", "vo_usdtry_settle", "ust_nom10", "ust_real10"])
        SP = pd.read_parquet(os.path.join(pdir, "panel_spot.parquet"), columns=["s_p15"])
        E = pd.read_parquet(os.path.join(pdir, "panel_etf.parquet"), columns=[f"c_{t}" for t in ETF_TICKER] + ["xau_cut", "xau_close"])
        for X in (V, SP, E): X.index = pd.DatetimeIndex(pd.to_datetime(X.index)).normalize().as_unit("ns")
        self.V, self.SP, self.E = V, SP, E
        self.son_gun = dict(viop=V.index.max().date(), spot=SP.index.max().date(), etf=E.index.max().date())
        an = {}
        for d, v in SP.s_p15.dropna().items(): an[utc(d.date(), 15)] = float(v)
        for col, H in (("xau_p14", 14), ("xau_p15", 15)):
            for d, v in V[col].dropna().items(): an[utc(d.date(), H)] = float(v)
        for d, v in E.xau_cut.dropna().items(): an[et(d.date(), 15)] = float(v)
        for d, v in E.xau_close.dropna().items(): an[et(d.date(), 16)] = float(v)
        self._an = an
        self.etf_gunleri = [d.date() for d in E.index]
        self._kap = {}
        av = et16([d.date() for d in E.index])
        for t in ETF_TICKER:
            self._kap[t] = pd.DataFrame({"close": E[f"c_{t}"].astype(float).values, "avail": av}, index=[d.date() for d in E.index])
        # takvim tutarlılığı: panel VİOP günleri = yerleşik TR takvimi
        bd = viop_gunleri(V.index.min().date(), V.index.max().date())
        fark = set(bd) ^ set(d.date() for d in V.index)
        if fark: self.log(f"  [uyarı] panel VİOP günleri ile yerleşik TR takvimi {len(fark)} günde farklı: {sorted(fark)[:5]}")

    def hazirla(self, gereken: dict):
        return

    def xau_an(self, T: pd.Timestamp):
        v = self._an.get(pd.Timestamp(T))
        if v is None or not np.isfinite(v): return np.nan, None, "panelde yok"
        return v, pd.Timestamp(T), "panel"

    def p15_seri(self, bitis: dt.date, karar: pd.Timestamp) -> pd.Series:
        s = self.SP.s_p15.dropna()
        s = s[s.index <= pd.Timestamp(bitis)]
        av = pd.DatetimeIndex(s.index).tz_localize("UTC") + pd.Timedelta(hours=15)
        s = s[np.asarray(av <= karar)]
        s.index = [d.date() for d in s.index]
        return s

    def kapanis(self, t: str, karar: pd.Timestamp) -> pd.DataFrame:
        k = self._kap[t]
        return k[np.asarray(k["avail"] <= karar)]

    def veri_gunleri_etf(self, bitis: dt.date) -> list:
        """ETF veri takvimi (GLD işlem günleri); panel sonundan sonrası yerleşik NYSE takvimi."""
        g = [d for d in self.etf_gunleri if d <= bitis]
        if bitis > self.son_gun["etf"]: g += nyse_gunleri(self.son_gun["etf"] + dt.timedelta(days=1), bitis)
        return g

    def viop_bilgi(self, t: dt.date, karar: pd.Timestamp) -> dict:
        V = self.V[self.V.index < pd.Timestamp(t)]  # gün t uzlaşması 15:10 UTC'de → karar anından sonra; yalnız t-1
        if V.empty: return {}
        r = V.iloc[-1]; d = V.index[-1].date()
        kontrol("VİOP bülteni (panel v_settle)", utc(d, 20, 15), karar, "risk")  # bülten: t-1 akşam gün sonu (23:15 TSİ), muhafazakâr
        return dict(tarih=str(d), kod=r.v_code, uzlasma=float(r.v_settle), vade=str(pd.Timestamp(r.v_expiry).date()) if pd.notna(r.v_expiry) else None,
                    usdtry=float(r.vo_usdtry_settle) if pd.notna(r.vo_usdtry_settle) else np.nan, usdtry_kaynak="VİOP F_USDTRY uzlaşması (panel)")

    def ust_bilgi(self, t: dt.date, karar: pd.Timestamp) -> dict:
        V = self.V[self.V.index <= pd.Timestamp(t)]
        if V.empty or pd.Timestamp(t) not in self.V.index: return {}
        r = self.V.loc[pd.Timestamp(t)]
        return dict(nom10=float(r.ust_nom10), real10=float(r.ust_real10), not_="panel ust_* (t-1 değeri, D 22:00 UTC yayın varsayımı)")


class CanliKaynak:
    """Ağdan indirir. Dukascopy: tamamlanmış aylar için saatlik ay dosyası, içinde bulunulan ay için günlük dakika dosyası,
    bugün için saatlik tick dosyası; henüz yayımlanmamış son dilim için Yahoo GC=F dakikalık (baz düzeltmeli) yedek."""
    mod = "canli"
    DUKA = "https://datafeed.dukascopy.com/datafeed"
    YAHOO = "https://query1.finance.yahoo.com/v8/finance/chart/"

    def __init__(self, onbellek: str, saat: pd.Timestamp | None = None, simule: bool = False, log=print):
        self.ag = Ag(onbellek, log=log)
        self.ob = onbellek
        self.log = log
        self.saat = saat if saat is not None else pd.Timestamp.now(tz="UTC")
        self.simule = simule
        self.xau = pd.Series(dtype=float, index=pd.DatetimeIndex([], tz="UTC"))
        self.xau_kaynak = pd.Series(dtype=object, index=pd.DatetimeIndex([], tz="UTC"))
        self._kap = {}
        self.uyarilar = []
        self.etf_gunleri = []
        self.eksik_gunler = set()

    # ---------------- Dukascopy ----------------
    def _duka_ay(self, y, m):
        url = f"{self.DUKA}/XAUUSD/{y}/{m - 1:02d}/BID_candles_hour_1.bi5"
        yol = os.path.join(self.ob, "duka", "XAUUSD", f"h_{y}_{m:02d}.bi5")
        bitis = pd.Timestamp(dt.datetime(y + (m == 12), m % 12 + 1, 1, tzinfo=UTC))
        tam = bitis <= self.saat - pd.Timedelta(hours=6)
        b = self.ag.al(url, yol, kalici=tam, deneme=max(self.ag.deneme, 10) if self.ag.deneme >= 7 else self.ag.deneme, bos_kabul=bitis <= self.saat - pd.Timedelta(days=10))
        if b is None: return None
        if b and tam:  # tam ay dosyası ay × 24 saatlik kayıt içerir; eksikse kalıcı önbellekte tutma (dakika dosyalarına geç)
            try:
                kayit = len(lzma.decompress(b)) // 24
            except Exception:
                kayit = -1
            if kayit != int((bitis - pd.Timestamp(dt.datetime(y, m, 1, tzinfo=UTC))).total_seconds() // 3600):
                try: os.remove(yol)
                except OSError: pass
                return None
        d = _bi5_mum(b, pd.Timestamp(dt.datetime(y, m, 1, tzinfo=UTC)))
        if len(d) == 0: return pd.Series(dtype=float)
        s = pd.Series(d["c"].values, index=pd.DatetimeIndex(d["t"]) + pd.Timedelta(hours=1))
        return s

    def _duka_gun(self, d: dt.date):
        url = f"{self.DUKA}/XAUUSD/{d.year}/{d.month - 1:02d}/{d.day:02d}/BID_candles_min_1.bi5"
        yol = os.path.join(self.ob, "duka", "XAUUSD", f"m_{d:%Y%m%d}.bi5")
        tam = utc(d, 0) + pd.Timedelta(days=1, hours=3) <= self.saat
        if not tam: return None
        b = self.ag.al(url, yol, kalici=True, deneme=max(self.ag.deneme, 10) if self.ag.deneme >= 7 else self.ag.deneme, bos_kabul=utc(d, 0) + pd.Timedelta(days=8) <= self.saat)
        if b is None: return None
        try:
            m = _bi5_mum(b, utc(d, 0))
        except Exception:  # bozuk dosya: önbellekten sil, tick yedeğine geç
            try: os.remove(yol)
            except OSError: pass
            return None
        if len(m) == 0 and not spot_kapali(d): return None  # boş/404: yayımlanmamış olabilir → tick yedeği
        return _saatlik_nokta(m, 1)

    def _duka_tick(self, d: dt.date, H: int):
        bitis = utc(d, H) + pd.Timedelta(hours=1)
        if bitis > self.saat: return None  # saat tamamlanmadı (gerçekte dosya henüz yayımlanmaz)
        url = f"{self.DUKA}/XAUUSD/{d.year}/{d.month - 1:02d}/{d.day:02d}/{H:02d}h_ticks.bi5"
        yol = os.path.join(self.ob, "duka", "XAUUSD", f"t_{d:%Y%m%d}_{H:02d}.bi5")
        b = self.ag.al(url, yol, kalici=bitis + pd.Timedelta(hours=2) <= self.saat, deneme=max(self.ag.deneme, 10) if self.ag.deneme >= 7 else self.ag.deneme, bos_kabul=bitis + pd.Timedelta(days=2) <= self.saat)
        if b is None or len(b) == 0: return None
        try:
            tk = _bi5_tick(b, utc(d, H))
        except Exception:  # bozuk dosya
            try: os.remove(yol)
            except OSError: pass
            return None
        tk = tk[tk.t < bitis]
        if len(tk) == 0: return None
        return pd.Series([float(tk.c.iloc[-1])], index=pd.DatetimeIndex([bitis]))

    def _yahoo_gc_dakika(self, a: pd.Timestamp, b: pd.Timestamp):
        u = (f"{self.YAHOO}GC%3DF?period1={int(a.timestamp())}&period2={int(b.timestamp()) + 60}&interval=1m&includePrePost=true")
        raw = self.ag.al(u, None)
        if not raw: return None
        try:
            j = json.loads(raw)["chart"]["result"][0]
            ts = j.get("timestamp") or []
            cl = j["indicators"]["quote"][0]["close"]
        except Exception:
            return None
        s = pd.Series(cl, index=pd.to_datetime(ts, unit="s", utc=True) + pd.Timedelta(minutes=1), dtype=float).dropna()
        return s[s.index <= self.saat]

    def _ay_on_indir(self, son_gun: dt.date):
        """Önbellekte olmayan tamamlanmış ayları 3 paralel bağlantıyla indir (ilk kurulum)."""
        isler = []
        y, m = 2010, 1
        while (y, m) <= (son_gun.year, son_gun.month):
            ay_bitis = pd.Timestamp(dt.datetime(y + (m == 12), m % 12 + 1, 1, tzinfo=UTC))
            yol = os.path.join(self.ob, "duka", "XAUUSD", f"h_{y}_{m:02d}.bi5")
            if ay_bitis <= self.saat - pd.Timedelta(hours=6) and not os.path.exists(yol): isler.append((y, m))
            m += 1
            if m == 13: y, m = y + 1, 1
        if len(isler) < 3: return
        self.log(f"  [Dukascopy] önbellekte olmayan {len(isler)} aylık dosya indiriliyor (ilk kurulum; 503'ler nedeniyle uzun sürebilir)...")
        t0 = time.time()
        with cf.ThreadPoolExecutor(3) as ex:
            for i, _ in enumerate(ex.map(lambda a: self._duka_ay(*a), isler)):
                if (i + 1) % 20 == 0: self.log(f"    {i + 1}/{len(isler)} ({time.time() - t0:.0f} sn)")

    def tohumla(self, dizin: str):
        """Araştırma düzenindeki ham Dukascopy aylık dosyalarını (YYYY_AA0.bi5, ay 0 tabanlı) önbelleğe kopyala."""
        hedef = os.path.join(self.ob, "duka", "XAUUSD"); os.makedirs(hedef, exist_ok=True)
        n = 0; eksik = []
        for fn in sorted(os.listdir(dizin)):
            if not fn.endswith(".bi5") or "_" not in fn: continue
            try:
                y, m0 = fn[:-4].split("_"); y, m = int(y), int(m0) + 1
            except ValueError:
                continue
            ay_bitis = pd.Timestamp(dt.datetime(y + (m == 12), m % 12 + 1, 1, tzinfo=UTC))
            yol = os.path.join(hedef, f"h_{y}_{m:02d}.bi5")
            if y >= 2010 and ay_bitis <= self.saat - pd.Timedelta(days=3) and not os.path.exists(yol):
                kaynak = os.path.join(dizin, fn)
                # ay içinde indirilmiş (eksik) dosyayı tam ay diye kopyalama: tam saatlik ay dosyası ay × 24 kayıt içerir
                try:
                    b = open(kaynak, "rb").read()
                    kayit = len(lzma.decompress(b)) // 24 if b else 0
                except Exception:
                    kayit = -1
                beklenen = int((ay_bitis - pd.Timestamp(dt.datetime(y, m, 1, tzinfo=UTC))).total_seconds() // 3600)
                if kayit != beklenen:
                    eksik.append(f"{y}-{m:02d}"); continue
                shutil.copyfile(kaynak, yol); n += 1
        self.log(f"  [önbellek] {n} aylık Dukascopy dosyası {dizin} dizininden kopyalandı"
                 + (f"; {len(eksik)} dosya eksik/bozuk olduğu için atlandı ({', '.join(eksik[:5])}) — ağdan indirilecek" if eksik else ""))

    def _xau_hazirla(self, son_gun: dt.date, bugun_saatler: dict):
        """2010-01'den son_gun'e kadar saatlik kapanış noktaları; son gün(ler) için tick ve GC=F yedeği."""
        self._ay_on_indir(son_gun)
        self._eksik_ay = []
        parcalar, kaynak = [], []
        y, m = 2010, 1
        ay_say = 0
        while (y, m) <= (son_gun.year, son_gun.month):
            ay_bitis = pd.Timestamp(dt.datetime(y + (m == 12), m % 12 + 1, 1, tzinfo=UTC))
            s = None
            if ay_bitis <= self.saat - pd.Timedelta(hours=6):
                s = self._duka_ay(y, m)
                ay_say += 1
                if ay_say % 40 == 0: self.log(f"  [Dukascopy] {y}-{m:02d} saatlik ay dosyası ...")
            if s is not None and len(s) > 0:
                parcalar.append(s); kaynak.append(pd.Series("Dukascopy saatlik", index=s.index))
            else:
                # ay dosyası yok/yayımlanmadı → günlük dakika dosyaları (yalnız son 70 gün; daha eskisi eksik sayılır)
                d = dt.date(y, m, 1)
                while d.month == m and d <= son_gun:
                    if d.weekday() < 5 and (son_gun - d).days <= 70:
                        g = self._duka_gun(d)
                        src = "Dukascopy dakika"
                        gecmis = utc(d, 0) + pd.Timedelta(days=1, hours=3) <= self.saat  # gün tamamlandı ve yayımlanmış olmalı
                        if g is None:
                            # dakika dosyası yok/alınamadı → yalnız gereken saatlerin tick dosyaları (VİOP 14/15 UTC, ETF 15/16 ET)
                            hs = set(bugun_saatler.get(d, set())) | {12, 13, 14, int(et(d, 15).hour) - 2, int(et(d, 15).hour) - 1,
                                                                     int(et(d, 16).hour) - 2, int(et(d, 16).hour) - 1}
                            parts = [self._duka_tick(d, H) for H in sorted(hs)]
                            parts = [p for p in parts if p is not None]
                            g = pd.concat(parts) if parts else None
                            src = "Dukascopy tick"
                            if gecmis and not spot_kapali(d):
                                if g is not None and len(g): self.uyarilar.append(f"Dukascopy {d} dakika dosyası alınamadı; saatlik tick yedeği kullanıldı")
                                else: self.eksik_gunler.add(d)
                        if g is not None and len(g):
                            parcalar.append(g); kaynak.append(pd.Series(src, index=g.index))
                    d += dt.timedelta(days=1)
                if ay_bitis <= self.saat - pd.Timedelta(days=70):
                    self._eksik_ay.append(f"{y}-{m:02d}")
            m += 1
            if m == 13: y, m = y + 1, 1
        if self.eksik_gunler:
            eg = sorted(self.eksik_gunler)
            self.uyarilar.append(f"Dukascopy: {len(eg)} gün alınamadı (dakika ve tick; {eg[0]}" + (f" … {eg[-1]}" if len(eg) > 1 else "") +
                                 ") — spot serisinde EKSİK gün; ilgili sinyaller YAKLAŞIK/HESAPLANAMADI")
        if self._eksik_ay:
            ea = self._eksik_ay
            self.uyarilar.append(f"Dukascopy: {len(ea)} aylık saatlik dosya alınamadı ({ea[0]}" + (f" … {ea[-1]}" if len(ea) > 1 else "") +
                                 "); LOWMOM yüzdeliği eksik geçmişle hesaplanır ya da hesaplanamaz")
        if not parcalar:
            return
        s = pd.concat(parcalar); k = pd.concat(kaynak)
        o = ~s.index.duplicated(keep="last")
        s, k = s[o], k[o]
        srt = np.argsort(s.index.values, kind="stable")
        s, k = s.iloc[srt], k.iloc[srt]
        s = s[s.index <= self.saat]; k = k[k.index <= self.saat]
        # GC=F yedeği: son Dukascopy noktasından şimdiye kadar (en çok 3 saat), baz oranı son ortak anda
        son = s.index.max()
        if self.saat - son > pd.Timedelta(minutes=3) and self.saat - son < pd.Timedelta(hours=3) and son.date() == self.saat.date():
            gc = self._yahoo_gc_dakika(son - pd.Timedelta(minutes=30), self.saat)
            if gc is not None and len(gc):
                ortak = gc[(gc.index <= son) & (gc.index >= son - pd.Timedelta(minutes=3))]
                if len(ortak):
                    oran = float(s.iloc[-1]) / float(ortak.iloc[-1])
                    ek = gc[gc.index > son] * oran
                    if len(ek):
                        s = pd.concat([s, ek]); k = pd.concat([k, pd.Series(f"Yahoo GC=F (baz oranı {oran:.5f})", index=ek.index)])
                        self.uyarilar.append(f"Son dilim ({son:%H:%M}–{ek.index.max():%H:%M} UTC) Yahoo GC=F vadelisinden baz düzeltmeli; yaklaşık")
        self.xau, self.xau_kaynak = s, k

    # ---------------- Yahoo günlük ----------------
    def _yahoo_gunluk(self, t: str):
        p1 = int(pd.Timestamp(P["E2_BASLANGIC"], tz="UTC").timestamp())
        p2 = int((self.saat + pd.Timedelta(days=1)).timestamp())
        u = f"{self.YAHOO}{urllib.parse.quote(t)}?period1={p1}&period2={p2}&interval=1d&includeAdjustedClose=true&events=div%2Csplit"
        yol = os.path.join(self.ob, "yahoo", f"{t}.json")
        raw = self.ag.al(u, yol, kalici=False)
        eski = False
        if not raw and os.path.exists(yol):
            raw = open(yol, "rb").read(); eski = True
            self.uyarilar.append(f"Yahoo {t}: ağdan alınamadı, önbellekteki eski dosya kullanıldı")
        if not raw: return None
        j = json.loads(raw)["chart"]["result"][0]
        tz = j["meta"].get("exchangeTimezoneName", "America/New_York")
        ts = j.get("timestamp") or []
        q = j["indicators"]["quote"][0]
        adj = (j["indicators"].get("adjclose") or [{}])[0].get("adjclose")
        c = adj if adj else q["close"]
        d = pd.DataFrame({"ts": pd.to_datetime(ts, unit="s", utc=True), "close": pd.to_numeric(pd.Series(c), errors="coerce")})
        d["date"] = d.ts.dt.tz_convert(tz).dt.date
        d = d.dropna(subset=["close"]).drop_duplicates("date", keep="last").set_index("date")
        d["avail"] = et16(d.index)  # ABD kapanışı 16:00 ET (yarım günde 13:00; 16:00 muhafazakâr)
        return d[["close", "avail"]]

    # ---------------- BIST bülteni, Hazine ----------------
    def _viop_bulten(self, d: dt.date):
        u = f"https://www.borsaistanbul.com/data/vadeli/viop_{d:%Y%m%d}.csv"
        yol = os.path.join(self.ob, "viop", f"viop_{d:%Y%m%d}.csv")
        b = self.ag.al(u, yol, kalici=utc(d, 18) <= self.saat, bos_kabul=utc(d, 0) + pd.Timedelta(days=4) <= self.saat)  # erken 404 kalıcı sayılmasın
        if b is None: return None
        if len(b) < 1000: return pd.DataFrame()
        txt = b.decode("windows-1254", errors="replace").splitlines()
        rows = []
        for l in txt[2:]:
            p = l.split(";")
            if len(p) < 22 or not (p[1].startswith("F_XAUUSD") or p[1].startswith("F_USDTRY")): continue
            rows.append(dict(tarih=p[0], kod=p[1], vade=p[8], uzlasma=float(p[9] or "nan"), onceki=float(p[10] or "nan"),
                             hacim=float(p[19] or 0), oi=float(p[21] or 0)))
        return pd.DataFrame(rows)

    def _ust(self, y: int, tip: str):
        u = (f"https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/{y}/all?"
             f"type={tip}&field_tdr_date_value={y}&page&_format=csv")
        yol = os.path.join(self.ob, "ust", f"{tip}_{y}.csv")
        b = self.ag.al(u, yol, kalici=False)
        if not b and os.path.exists(yol): b = open(yol, "rb").read()
        if not b: return None
        import io
        x = pd.read_csv(io.BytesIO(b))
        x["Date"] = pd.to_datetime(x["Date"], format="%m/%d/%Y")
        return x.set_index("Date").sort_index()

    # ---------------- arayüz ----------------
    def hazirla(self, gereken: dict):
        son_gun = gereken["son_gun"]
        self.log(f"  [canlı] veri indiriliyor (önbellek: {self.ob}; saat {self.saat:%Y-%m-%d %H:%M} UTC{' SİMÜLE' if self.simule else ''})")
        self._xau_hazirla(son_gun, gereken.get("tick_saatleri", {}))
        if len(self.xau): self.log(f"  [canlı] XAUUSD noktaları: {len(self.xau)} (son {self.xau.index.max():%Y-%m-%d %H:%M} UTC, {self.xau_kaynak.iloc[-1]})")
        for t in ETF_TICKER:
            d = self._yahoo_gunluk(t)
            if d is not None: self._kap[t] = d
        if "GLD" in self._kap:
            self.etf_gunleri = [x for x in self._kap["GLD"].index if x >= pd.Timestamp(P["E2_BASLANGIC"]).date()]
        self._viop_t1 = gereken.get("viop_t1")
        self._bulten = self._viop_bulten(self._viop_t1) if self._viop_t1 else None
        self._ust_n = self._ust(son_gun.year, "daily_treasury_yield_curve")
        self._ust_r = self._ust(son_gun.year, "daily_treasury_real_yield_curve")
        if self._ust_n is not None and son_gun.month == 1:
            a = self._ust(son_gun.year - 1, "daily_treasury_yield_curve"); b = self._ust(son_gun.year - 1, "daily_treasury_real_yield_curve")
            if a is not None: self._ust_n = pd.concat([a, self._ust_n]).sort_index()
            if b is not None and self._ust_r is not None: self._ust_r = pd.concat([b, self._ust_r]).sort_index()
        self.log(f"  [canlı] {self.ag.istek} HTTP isteği")

    def xau_an(self, T: pd.Timestamp):
        v, ts = snap(self.xau[self.xau.index <= T], T)
        if ts is None or not np.isfinite(v): return np.nan, ts, "Dukascopy'de yok"
        return v, ts, str(self.xau_kaynak.loc[ts]) if ts in self.xau_kaynak.index else "?"

    def p15_seri(self, bitis: dt.date, karar: pd.Timestamp) -> pd.Series:
        s = self.xau[self.xau.index <= karar]
        days = pd.bdate_range(P["SPOT_BASLANGIC"], pd.Timestamp(bitis))
        T = pd.DatetimeIndex(days).tz_localize("UTC") + pd.Timedelta(hours=15)
        if len(s) == 0: return pd.Series(dtype=float)
        idx = s.index.searchsorted(T, side="right") - 1
        ok = idx >= 0
        ii = np.clip(idx, 0, None)
        ts = s.index[ii]
        vals = np.where(ok & ((T - ts) <= pd.Timedelta(hours=1)), s.values[ii], np.nan)
        out = pd.Series(vals, index=[d.date() for d in days]).dropna()
        return out

    def kapanis(self, t: str, karar: pd.Timestamp) -> pd.DataFrame:
        if t not in self._kap: return pd.DataFrame(columns=["close", "avail"])
        k = self._kap[t]
        g = [d for d in self.etf_gunleri]
        if g: k = k.reindex(g)
        k = k.assign(avail=et16(k.index))
        return k[np.asarray(k["avail"] <= karar)]

    def veri_gunleri_etf(self, bitis: dt.date) -> list:
        g = [d for d in self.etf_gunleri if d <= bitis]
        son = g[-1] if g else dt.date(2008, 1, 1)
        if bitis > son: g += nyse_gunleri(son + dt.timedelta(days=1), bitis)
        return g

    def viop_bilgi(self, t: dt.date, karar: pd.Timestamp) -> dict:
        B = self._bulten
        if B is None: return dict(hata="VİOP bülteni alınamadı")
        if len(B) == 0: return dict(hata=f"{self._viop_t1} bülteni yok (404: tatil?)")
        x = B[B.kod.str.startswith("F_XAUUSD")]
        u = B[B.kod.str.startswith("F_USDTRY")].sort_values("vade")
        if x.empty: return dict(hata="bültende F_XAUUSD yok")
        if str(x.tarih.iloc[0]) != str(self._viop_t1): return dict(hata=f"bülten tarihi {x.tarih.iloc[0]} ≠ {self._viop_t1}")
        kontrol("VİOP bülteni", utc(self._viop_t1, 20, 15), karar, "risk")  # t-1 akşam gün sonu (23:15 TSİ), muhafazakâr
        a = x.sort_values("oi", ascending=False).iloc[0]
        return dict(tarih=str(self._viop_t1), kod=a.kod, uzlasma=float(a.uzlasma), vade=a.vade, oi=float(a.oi),
                    usdtry=float(u.uzlasma.iloc[0]) if len(u) else np.nan, usdtry_kaynak=f"VİOP {u.kod.iloc[0]} uzlaşması (vadeli, taşıma içerir)" if len(u) else "")

    def ust_bilgi(self, t: dt.date, karar: pd.Timestamp) -> dict:
        if self._ust_n is None: return {}
        n = self._ust_n["10 Yr"]
        av = pd.DatetimeIndex([utc(d.date(), 22) for d in n.index])
        n = n[np.asarray(av <= karar)]
        r = None
        if self._ust_r is not None:
            rr = self._ust_r["10 YR"]; avr = pd.DatetimeIndex([utc(d.date(), 22) for d in rr.index]); rr = rr[np.asarray(avr <= karar)]
            r = float(rr.iloc[-1]) if len(rr) else None
        if not len(n): return {}
        return dict(nom10=float(n.iloc[-1]), real10=r, tarih=str(n.index[-1].date()), not_="ABD Hazinesi CSV (D 22:00 UTC yayın varsayımı)")


# =====================================================================================================================
# 6. SİNYALLER
# =====================================================================================================================
def _sonuc(sid, **kw):
    b = BILGI[sid]
    r = dict(id=sid, ad=b["ad"], cephe=b["cephe"], guven=b["guven"], h=b["h"], arac=b["arac"], kural=b["kural"], bilgi_zamani=b["bilgi"],
             hakem_notu=b["not_"], durum=None, deger=None, deger_metin="", esik_metin="", aktif=None, yon="—", yeni_dilim=0.0,
             acik_dilimler={}, etkin=0.0, etkin_onceki=0.0, islem=0.0, gerekce="", veri_zamani=None, ek={})
    r.update(kw)
    return r


def _durum_zaman(karar, simdi, mod):
    """Gerçek saat karar anından önceyse ön-izleme."""
    return "ÖN-İZLEME" if (mod == "canli" and simdi < karar) else None


# ---------------- VİOP ----------------
def lowmom_tablo(K, t: dt.date, karar: pd.Timestamp):
    """Spot takviminde q (genişleyen yüzdelik, bugün dahil), rv20 (yıllık), x (5g log getiri) ve pozisyon."""
    p15 = K.p15_seri(t, karar)
    if len(p15) < P["LOWMOM_MINP"] + 30: return None
    lp = np.log(p15.astype(float))
    r = lp.diff()
    rv = r.rolling(P["LOWMOM_RV"]).std()
    x = lp - lp.shift(P["LOWMOM_K"])
    return p15, rv, x


def lowmom_gun(tab, d: dt.date):
    """VİOP günü d için (spot takviminde yoksa en çok 4 gün önceki spot günü; analistin to_viop kuralı)."""
    p15, rv, x = tab
    idx = p15.index
    if d in idx: j = idx.get_loc(d)
    else:
        prev = [k for k in range(len(idx)) if idx[k] <= d]
        if not prev or (d - idx[prev[-1]]).days > 4: return None
        j = prev[-1]
    rvv = rv.values[: j + 1]
    fin = rvv[np.isfinite(rvv)]
    rvj = rv.values[j]
    if len(fin) < P["LOWMOM_MINP"] or not np.isfinite(rvj): q = np.nan
    else: q = float((fin <= rvj).mean())
    xj = float(x.values[j]) if np.isfinite(x.values[j]) else np.nan
    pos = (float(np.sign(xj)) if q < P["LOWMOM_Q"] else 0.0) if (np.isfinite(q) and np.isfinite(xj)) else np.nan
    esik = float(np.quantile(fin, P["LOWMOM_Q"]) * math.sqrt(252)) if len(fin) >= P["LOWMOM_MINP"] else np.nan
    return dict(spot_gun=idx[j], q=q, rv=float(rvj * math.sqrt(252)), x=xj, pos=pos, rv_esik=esik, p=float(p15.values[j]))


def viop_sinyalleri(K, t: dt.date, simdi: pd.Timestamp):
    out = dict(cephe="VIOP", tarih=str(t), gun=gun_adi(t))
    if not tr_is_gunu(t):
        out["kapali"] = True
        return out
    yarim = tr_yarim(t)
    karar = viop_karar(t)
    out.update(karar_utc=str(karar), karar_tsi=tsi(karar), yarim=yarim,
               emir="uzlaşma penceresi 12:30–12:40 TSİ (yarım gün)" if yarim else "uzlaşma penceresi 18:00–18:10 TSİ (15:00–15:10 UTC)")
    on = _durum_zaman(karar, simdi, K.mod)
    gun = viop_gunleri(t - dt.timedelta(days=1100), t)
    S = []

    # ---- A1-LOWMOM-h1 (+h5)
    sid = "A1-LOWMOM-h1"
    try:
        tab = lowmom_tablo(K, t, karar)
        pos = {}
        if tab is not None:
            for d in gun[-7:]:
                g_ = None if tr_yarim(d) else lowmom_gun(tab, d)
                pos[d] = 0.0 if (g_ is None or not np.isfinite(g_["pos"])) else g_["pos"]
        g = lowmom_gun(tab, t) if tab is not None else None
        if yarim:
            ye, acik, eff, effp, isl = kademe(pos, gun, t, 1)
            ye5, acik5, eff5, effp5, isl5 = kademe(pos, gun, t, 5)
            S.append(_sonuc(sid, durum="DEVRE DIŞI", yeni_dilim=0.0, etkin=eff, etkin_onceki=effp, islem=isl,
                            gerekce="TR yarım günü: uzlaşma 09:30–09:40 UTC'de; 15:00 UTC bilgisi ileriye bakar (veri notu 1).",
                            ek=dict(h5=dict(yeni=ye5, acik=acik5, etkin=eff5, islem=isl5))))
        elif g is None:
            S.append(_sonuc(sid, durum="HESAPLANAMADI", gerekce="spot 15:00 UTC geçmişi yetersiz/eksik (son 4 günde spot gözlemi yok)"))
        else:
            _, gozlem, src_l = K.xau_an(utc(g["spot_gun"], 15)) if K.mod == "canli" else (None, utc(g["spot_gun"], 15), "panel")
            kontrol("spot XAUUSD 15:00 UTC serisi", gozlem, karar, sid)
            bugun_var = g["spot_gun"] == t
            akt = bool(np.isfinite(g["q"]) and g["q"] < P["LOWMOM_Q"])
            ye, acik, eff, effp, isl = kademe(pos, gun, t, 1)
            ye5, acik5, eff5, effp5, isl5 = kademe(pos, gun, t, 5)
            durum0 = "AKTİF" if akt else "PASİF"
            if not bugun_var and simdi < karar: durum = f"BEKLİYOR (ön-izleme: {durum0})"
            elif on: durum = f"ÖN-İZLEME ({durum0})"
            elif bugun_var and str(src_l).startswith("Yahoo"): durum = f"YAKLAŞIK ({durum0}; 15:00 UTC spotu GC=F'ten baz düzeltmeli)"
            elif bugun_var and K.mod == "canli" and gozlem is not None and (utc(t, 15) - pd.Timestamp(gozlem)) > pd.Timedelta(minutes=2):
                durum = f"YAKLAŞIK ({durum0}; 15:00 UTC değeri {pd.Timestamp(gozlem):%H:%M} UTC gözlemi — veri gecikmeli, yeniden çalıştırın)"
            else: durum = durum0
            eks = sorted(x for x in getattr(K, "eksik_gunler", set()) if (t - x).days <= 35)
            if eks:
                durum += " — YAKLAŞIK (spot serisinde eksik gün)"
                if abs(g["q"] - P["LOWMOM_Q"]) < 0.05: durum = "HESAPLANAMADI (eksik spot günü ve eşiğe yakın)"
            ger = ((f"Eksik spot günleri: {', '.join(map(str, eks))}. " if eks else "") + f"rv20 %{fs(g['rv'] * 100, 1)}, 2010'dan beri yüzdeliği {fs(g['q'], 3)}; eşik yüzdelik 1/3 ≈ rv20 %{fs(g['rv_esik'] * 100, 1)}. "
                   + (f"Sakin rejim: 5 günlük spot getirisi %{fs(g['x'] * 100, 2, True)} → {'UZUN' if g['x'] > 0 else 'KISA'}." if akt else
                      f"Oynaklık eşiğin üstünde → nakit (5g getiri %{fs(g['x'] * 100, 2, True)} yalnız bilgi)."))
            if not bugun_var:
                ger += (f" Gün t 15:00 UTC fiyatı henüz yok; değerler {g['spot_gun']} 15:00 UTC verisiyle." if simdi < karar else
                        f" Gün t spot takviminde yok; {g['spot_gun']} değeri kullanıldı (analistin to_viop kuralı, ≤4 gün).")
            S.append(_sonuc(sid, durum=durum, deger=g["q"], deger_metin=f"yüzdelik {fs(g['q'], 3)} (rv20 %{fs(g['rv'] * 100, 1)}); x %{fs(g['x'] * 100, 2, True)}",
                            esik_metin=f"yüzdelik < 0,333 (rv20 < %{fs(g['rv_esik'] * 100, 1)})", aktif=akt,
                            yon=("UZUN" if g["x"] > 0 else "KISA") if akt else "NAKİT", yeni_dilim=ye, acik_dilimler=acik,
                            etkin=eff, etkin_onceki=effp, islem=isl, gerekce=ger, veri_zamani=str(gozlem),
                            ek=dict(q=g["q"], rv20=g["rv"], x5=g["x"], p15=g["p"], spot_gun=str(g["spot_gun"]), rv_esik=g["rv_esik"],
                                    h5=dict(yeni=ye5, acik=acik5, etkin=eff5, islem=isl5))))
    except IleriyeBakma as e:
        S.append(_sonuc(sid, durum="HATA", gerekce=str(e)))
    except Exception as e:  # beklenmeyen veri sorunu: sinyal düşer, betik sürer
        S.append(_sonuc(sid, durum="HESAPLANAMADI", gerekce=f"beklenmeyen hata: {type(e).__name__}: {e}"))

    # ---- A3_QEND_h3
    sid = "A3_QEND_h3"
    def qend_gun(d):
        if d.month not in (3, 6, 9, 12): return 0.0
        ay = viop_gunleri(dt.date(d.year, d.month, 1), (dt.date(d.year, d.month + 1, 1) if d.month < 12 else dt.date(d.year + 1, 1, 1)) - dt.timedelta(days=1))
        return 1.0 if len(ay) >= 2 and d == ay[-2] else 0.0
    pos = {d: qend_gun(d) for d in gun[-6:]}
    ye, acik, eff, effp, isl = kademe(pos, gun, t, 3)
    # sonraki giriş
    d = t; nx = None
    for _ in range(400):
        d = d + dt.timedelta(days=1)
        if tr_is_gunu(d) and qend_gun(d) == 1.0: nx = d; break
    cik = sonraki(nx, tr_is_gunu, 3) if nx else None
    akt = eff > 0
    S.append(_sonuc(sid, durum=("AKTİF (GİRİŞ GÜNÜ)" if ye > 0 else ("AKTİF (açık dilim)" if akt else "PASİF")), deger=ye,
                    deger_metin="bugün giriş günü" if ye > 0 else "bugün giriş günü değil", esik_metin="Mar/Haz/Eyl/Ara sondan 2. VİOP günü",
                    aktif=bool(akt), yon="UZUN" if akt else "NAKİT", yeni_dilim=ye, acik_dilimler=acik, etkin=eff, etkin_onceki=effp, islem=isl,
                    gerekce=f"Takvim kuralı. Sonraki giriş {nx} ({gun_adi(nx)}) uzlaşması, çıkış {cik} uzlaşması." if nx else "Takvim kuralı.",
                    veri_zamani="takvim", ek=dict(sonraki_giris=str(nx), sonraki_cikis=str(cik))))
    if t > TR_KAPSAM[1] - dt.timedelta(days=100): S[-1]["gerekce"] += " UYARI: yerleşik TR takvimi 2027 sonunda bitiyor."

    # ---- A4-C1_GDXJ_artik_h3
    sid = "A4-C1_GDXJ_artik_h3"
    try:
        gg = gun[-P["A4_GECMIS"]:]
        kg = K.kapanis("GDXJ", karar); kl = K.kapanis("GLD", karar)
        if len(kg) and len(kl):
            kes = [utc(d, 15) for d in gg]
            kes[-1] = min(kes[-1], karar)  # gün t: 15:00 UTC (yarım günde 09:30 UTC)
            vj, gj, aj = asof_once(kg, kes); vl, gl, al_ = asof_once(kl, kes)
            y_j = pd.Series(vj, index=gg); y_l = pd.Series(vl, index=gg)
            beklenen = onceki(t, nyse_is_gunu)  # t'den önceki son ABD seansı
            kontrol("Yahoo GDXJ kapanışı", aj[-1], karar, sid); kontrol("Yahoo GLD kapanışı", al_[-1], karar, sid)
            rm = np.log(y_j).diff(); rg = np.log(y_l).diff()
            W, MP = P["A4_BETA"], P["A4_BETA_MINP"]
            b = rm.rolling(W, min_periods=MP).cov(rg).shift(1) / rg.rolling(W, min_periods=MP).var().shift(1)
            e = rm - b * rg
            z = e / e.rolling(P["A4_STD"], min_periods=P["A4_STD_MINP"]).std().shift(1)
            pz = np.sign(z).where(z.abs() > P["A4_ESIK"], 0.0).where(z.notna(), 0.0)
            pos = {d: float(pz.loc[d]) for d in gg[-6:]}
            zt = float(z.loc[t]) if np.isfinite(z.loc[t]) else np.nan
            if gj[-1] != beklenen or gl[-1] != beklenen:
                S.append(_sonuc(sid, durum="HESAPLANAMADI", gerekce=f"ABD kapanışı eksik: beklenen {beklenen}, GDXJ son {gj[-1]}, GLD son {gl[-1]}"))
            elif not np.isfinite(zt):
                S.append(_sonuc(sid, durum="HESAPLANAMADI", gerekce="z hesaplanamadı (geçmiş yetersiz)"))
            else:
                ye, acik, eff, effp, isl = kademe(pos, gg, t, 3)
                akt = abs(zt) > P["A4_ESIK"]
                S.append(_sonuc(sid, durum="AKTİF" if akt else "NÖTR", deger=zt,
                                deger_metin=f"z {fs(zt, 2, True)} (r_GDXJ %{fs(rm.loc[t] * 100, 2, True)}, r_GLD %{fs(rg.loc[t] * 100, 2, True)}, β60 {fs(b.loc[t], 2)})",
                                esik_metin="|z| > 0,43", aktif=bool(akt), yon=("UZUN" if zt > 0 else "KISA") if akt else "NAKİT", yeni_dilim=ye,
                                acik_dilimler=acik, etkin=eff, etkin_onceki=effp, islem=isl,
                                gerekce=f"Madenci artığı {beklenen} ABD kapanışından (t-1). Yeni 1/3 dilim {'UZUN' if ye > 0 else ('KISA' if ye < 0 else 'yok')}; açık dilimlerle etkin {fs(eff, 3, True)} birim.",
                                veri_zamani=str(aj[-1]), ek=dict(z=zt, r_gdxj=float(rm.loc[t]), r_gld=float(rg.loc[t]), beta60=float(b.loc[t]), abd_kapanis=str(beklenen))))
        else:
            S.append(_sonuc(sid, durum="HESAPLANAMADI", gerekce="Yahoo GDXJ/GLD verisi yok"))
    except IleriyeBakma as e:
        S.append(_sonuc(sid, durum="HATA", gerekce=str(e)))
    except Exception as e:  # beklenmeyen veri sorunu: sinyal düşer, betik sürer
        S.append(_sonuc(sid, durum="HESAPLANAMADI", gerekce=f"beklenmeyen hata: {type(e).__name__}: {e}"))

    # ---- A8-3_seg_last1h_h5
    sid = "A8-3_seg_last1h_h5"
    try:
        pos = {}
        for d in gun[-6:]:
            if tr_yarim(d): pos[d] = 0.0; continue
            T15, T14 = utc(d, 15), utc(d, 14)
            if T15 > karar: pos[d] = np.nan; continue
            p15, ts15, _ = K.xau_an(T15); p14, ts14, _ = K.xau_an(T14)
            pos[d] = float(np.sign(math.log(p15 / p14))) if (np.isfinite(p15) and np.isfinite(p14)) else 0.0
        eks8 = [d for d in gun[-5:-1] if not tr_yarim(d) and not spot_kapali(d) and
                (not np.isfinite(K.xau_an(utc(d, 15))[0]) or not np.isfinite(K.xau_an(utc(d, 14))[0]))]
        if yarim:
            ye, acik, eff, effp, isl = kademe({k: (0.0 if not np.isfinite(v) else v) for k, v in pos.items()}, gun, t, 5)
            S.append(_sonuc(sid, durum="DEVRE DIŞI", yeni_dilim=0.0, acik_dilimler=acik, etkin=eff, etkin_onceki=effp, islem=isl,
                            gerekce=f"TR yarım günü: 15:00 UTC bilgisi uzlaşmadan sonra (veri notu 1); yeni dilim yok, açık dilimler sürüyor (etkin {fs(eff, 2, True)})."))
        else:
            p15, ts15, src15 = K.xau_an(utc(t, 15)); p14, ts14, src14 = K.xau_an(utc(t, 14))
            if K.mod == "canli" and ts15 is not None and ts14 is not None and ts15 == ts14:
                p15 = np.nan  # 15:00 değeri yok, 14:00 gözlemi tekrar ediyor (ör. 14 UTC saat dosyası alınamadı): x=0 sayma
            pz = {k: (0.0 if not np.isfinite(v) else v) for k, v in pos.items()}
            yok = ("BEKLİYOR" if simdi < utc(t, 14) else
                   "KOŞULLU (panelde gün t verisi yok)" if (K.mod == "panel" and t > K.son_gun["viop"]) else "HESAPLANAMADI (gün t spot verisi yok)")
            if spot_kapali(t) and not np.isfinite(p15):
                # spot piyasası kapalı (25 Aralık, 1 Ocak, Kutsal Cuma…): hakem kuralı bu günde dilimi 0 sayar (fillna(0))
                pz[t] = 0.0
                ye, acik, eff, effp, isl = kademe(pz, gun, t, 5)
                S.append(_sonuc(sid, durum="NÖTR (spot piyasası kapalı)", yeni_dilim=0.0, acik_dilimler=acik, etkin=eff, etkin_onceki=effp, islem=isl,
                                yon="NAKİT", gerekce=f"Spot altın bugün işlem görmüyor; 14→15 UTC hareketi yok, yeni dilim 0 (hakem kuralı). Açık dilimlerle etkin {fs(eff, 2, True)} birim."))
            elif not np.isfinite(p14):
                ye, acik, eff, effp, isl = kademe(pz, gun, t, 5)
                ac = sum(acik.values()) / 5
                S.append(_sonuc(sid, durum=yok, yeni_dilim=np.nan, etkin=ac, islem=ac - effp,
                                gerekce=(f"UYARI: {', '.join(map(str, eks8))} dilimleri bilinmiyor (spot yok), 0 sayıldı. " if eks8 else "") + f"Gün t 14:00 UTC spot yok. Kural: 15:00 UTC'de ln(spot15/spot14)>0 ise yeni 1/5 dilim UZUN, <0 ise KISA. Açık dilimlerin toplamı {fs(ac, 2, True)} birim → etkin {fs(ac + 0.2, 2, True)} (UZUN) ya da {fs(ac - 0.2, 2, True)} (KISA).",
                                acik_dilimler=acik, etkin_onceki=effp, ek=dict(acik_toplam_5te=ac, senaryo=dict(UZUN=ac + 0.2, KISA=ac - 0.2))))
            else:
                kontrol("spot XAUUSD 14:00 UTC", ts14, karar, sid)
                if np.isfinite(p15): kontrol("spot XAUUSD 15:00 UTC", ts15, karar, sid)
                if not np.isfinite(p15):
                    pz[t] = 0.0
                    ye, acik, eff, effp, isl = kademe(pz, gun, t, 5)
                    ac = sum(acik.values()) / 5
                    S.append(_sonuc(sid, durum="BEKLİYOR" if simdi < karar else yok, yeni_dilim=np.nan, etkin=ac, islem=ac - effp,
                                    gerekce=f"14:00 UTC spot {fs(p14, 2)} USD; 15:00 UTC fiyatı bunun üstündeyse UZUN, altındaysa KISA dilim (etkin {fs(ac + 0.2, 2, True)} / {fs(ac - 0.2, 2, True)}).",
                                    deger_metin=f"spot14 {fs(p14, 2)} USD", esik_metin="spot15 > spot14 → UZUN", acik_dilimler=acik, etkin_onceki=effp,
                                    ek=dict(p14=p14, senaryo=dict(UZUN=ac + 0.2, KISA=ac - 0.2))))
                else:
                    x = math.log(p15 / p14)
                    pz[t] = float(np.sign(x))
                    ye, acik, eff, effp, isl = kademe(pz, gun, t, 5)
                    taze = (utc(t, 15) - ts15) <= pd.Timedelta(minutes=2)
                    yaklasik = str(src15).startswith("Yahoo") or str(src14).startswith("Yahoo")
                    durum = ("UZUN" if x > 0 else "KISA") if x != 0 else "NÖTR"
                    if on: durum = f"ÖN-İZLEME ({durum})"
                    elif not taze: durum = f"YAKLAŞIK ({durum}; 15:00 UTC değeri {ts15:%H:%M} UTC gözlemi — veri gecikmeli, yeniden çalıştırın)"
                    elif yaklasik: durum = f"YAKLAŞIK ({durum}; spot GC=F'ten baz düzeltmeli, Dukascopy saat dosyası henüz yok — birkaç dakika sonra yeniden çalıştırın)"
                    # kırılganlık: kalan süre içinde işaretin dönme olasılığı kaba ölçü (dakikalık σ ≈ günlük σ/√1440)
                    S.append(_sonuc(sid, durum=durum, deger=x, deger_metin=f"ln(p15/p14) {fs(x * 1e4, 1, True)} bps (p14 {fs(p14, 2)}, p15 {fs(p15, 2)})",
                                    esik_metin="0 (işaret)", aktif=x != 0, yon="UZUN" if x > 0 else ("KISA" if x < 0 else "NAKİT"), yeni_dilim=float(np.sign(x)),
                                    acik_dilimler=acik, etkin=eff, etkin_onceki=effp, islem=isl,
                                    gerekce=(f"UYARI: {', '.join(map(str, eks8))} dilimleri bilinmiyor (spot yok), 0 sayıldı. " if eks8 else "") + f"Son saat (14→15 UTC) hareketi yönünde 1/5 dilim; açık dilimlerle etkin {fs(eff, 2, True)} birim. "
                                            + (f"15:00 değeri {ts15:%H:%M} UTC gözlemi ({src15})." if (not taze or yaklasik) else ""),
                                    veri_zamani=str(ts15), ek=dict(p14=p14, p15=p15, p15_kaynak=src15, p15_zaman=str(ts15))))
    except IleriyeBakma as e:
        S.append(_sonuc(sid, durum="HATA", gerekce=str(e)))
    except Exception as e:  # beklenmeyen veri sorunu: sinyal düşer, betik sürer
        S.append(_sonuc(sid, durum="HESAPLANAMADI", gerekce=f"beklenmeyen hata: {type(e).__name__}: {e}"))

    out["sinyaller"] = S
    # eşit ağırlıklı birleşim (LOWMOM-h1, QEND, A4-C1, A8-3; her biri 1/4)
    ana = [s for s in S if s["id"] in ("A1-LOWMOM-h1", "A3_QEND_h3", "A4-C1_GDXJ_artik_h3", "A8-3_seg_last1h_h5")]
    out["birlesik"] = dict(etkin=sum(float(s["etkin"] or 0) for s in ana) / 4, onceki=sum(float(s["etkin_onceki"] or 0) for s in ana) / 4,
                           eksik=[s["id"] for s in ana if str(s["durum"]).startswith(("HESAPLANAMADI", "BEKLİYOR", "HATA", "KOŞULLU"))])
    out["birlesik"]["islem"] = out["birlesik"]["etkin"] - out["birlesik"]["onceki"]
    sen = {}
    for s in ana:
        for k, v in (s["ek"].get("senaryo") or {}).items():
            sen[f"{s['id']}={k}"] = out["birlesik"]["etkin"] + (v - float(s["etkin"] or 0)) / 4
    out["birlesik"]["senaryo"] = sen
    return out


# ---------------- ETF ----------------
def _getiri(k: pd.DataFrame, gunler: list) -> pd.Series:
    c = k["close"].reindex(gunler).astype(float)
    r = np.log(c).diff()
    r[c.isna() | c.shift(1).isna()] = np.nan
    return r


def _beta2(Y: np.ndarray, X: np.ndarray, i: int, win: int, minp: int):
    """β_{i-1}: [i-win, i-1] satırlarında sabitli OLS (analist roll_beta2 + shift(1) ile aynı)."""
    lo = max(0, i - win)
    yy, xx = Y[lo:i], X[lo:i]
    m = np.isfinite(yy) & np.all(np.isfinite(xx), axis=1)
    if m.sum() < minp: return None
    A = np.column_stack([np.ones(m.sum()), xx[m]])
    return np.linalg.lstsq(A, yy[m], rcond=None)[0][1:]


def madenci_artik(R: pd.DataFrame, y: str, satirlar) -> pd.Series:
    Y = R[y].values; X = R[["GLD", "SPY"]].values
    e = pd.Series(np.nan, index=R.index)
    for i in satirlar:
        if i < 1: continue
        b = _beta2(Y, X, i, P["E2_BETA"], P["E2_BETA_MINP"])
        if b is None or not np.isfinite(Y[i]) or not np.all(np.isfinite(X[i])): continue
        e.iloc[i] = Y[i] - b[0] * X[i, 0] - b[1] * X[i, 1]
    return e


def etf_sinyalleri(K, t: dt.date, simdi: pd.Timestamp, esik_yeniden=False):
    out = dict(cephe="ETF", tarih=str(t), gun=gun_adi(t))
    if not nyse_is_gunu(t):
        out["kapali"] = True
        return out
    yarim = nyse_yarim(t)
    karar = etf_karar(t)
    kap = et(t, 13) if yarim else et(t, 16)
    out.update(karar_utc=str(karar), karar_et=pd.Timestamp(karar).tz_convert(TZ_NY).strftime("%H:%M ET"), karar_tsi=tsi(karar), yarim=yarim,
               emir=(f"yarım gün: kapanış 13:00 ET ({tsi(kap)}); emir 12:50–12:58 ET" if yarim else
                     f"kapanış 16:00 ET ({tsi(kap)}); Midas'ta MOC yok → emir 15:50–15:58 ET ({tsi(kap - pd.Timedelta(minutes=10))}–{tsi(kap - pd.Timedelta(minutes=2))})"))
    on = _durum_zaman(karar, simdi, K.mod)
    gunler = K.veri_gunleri_etf(t)
    if t not in gunler: gunler = gunler + [t]
    i_t = gunler.index(t)
    S = []
    onceki_seans = gunler[i_t - 1] if i_t >= 1 else onceki(t, nyse_is_gunu)  # dizinin başında takvimden

    # ---- E1-C2 tatil öncesi GDX
    sid = "E1-C2_GDX_tatil_oncesi"
    def tatil_giris(d):
        n1 = sonraki(d, nyse_is_gunu); n2 = sonraki(n1, nyse_is_gunu)
        hol = [h for y in {n1.year, n2.year} for h in nyse_tatilleri(y) if n1 < h < n2 and h.weekday() < 5]
        return (1.0 if hol else 0.0), n1, hol
    p_t, n1, hol = tatil_giris(t)
    p_p, _, _ = tatil_giris(onceki_seans)
    d = t; nx = None
    for _ in range(400):
        d = sonraki(d, nyse_is_gunu)
        if tatil_giris(d)[0] == 1.0: nx = d; break
    nxh = tatil_giris(nx)[2] if nx else []
    S.append(_sonuc(sid, durum="AKTİF (GİRİŞ GÜNÜ)" if p_t else "PASİF", deger=p_t, deger_metin="bugün giriş günü" if p_t else "bugün giriş günü değil",
                    esik_metin="sonraki seans tatil öncesi son gün", aktif=bool(p_t), yon="UZUN" if p_t else "NAKİT", yeni_dilim=p_t,
                    etkin=p_t, etkin_onceki=p_p, islem=p_t - p_p,
                    gerekce=(f"Bugün kapanışta GDX al, {n1} ({gun_adi(n1)}) kapanışında sat; ardından {nyse_tatilleri(hol[0].year)[hol[0]]} ({hol[0]})." if p_t else
                             f"Sonraki giriş {nx} kapanışı, çıkış {sonraki(nx, nyse_is_gunu)} kapanışı ({nyse_tatilleri(nxh[0].year)[nxh[0]]} öncesi)." if nx else ""),
                    veri_zamani="takvim", ek=dict(sonraki_giris=str(nx))))
    if p_t and nyse_yarim(n1): S[-1]["gerekce"] += f" Not: çıkış günü {n1} yarım gün (13:00 ET kapanış)."

    # ---- E2 madenci artıkları
    R = None
    try:
        kk = {x: K.kapanis(x, karar) for x in ("GLD", "GDX", "GDXJ", "SPY")}
        for x, k in kk.items():
            if len(k): kontrol(f"Yahoo {x} kapanışı", k["avail"].iloc[-1], karar, "E2")
        gg = gunler[: i_t]  # t-1'e kadar (t kapanışı giriş fiyatı, kullanılmaz)
        R = pd.DataFrame({x: _getiri(kk[x], gg) for x in kk}, index=gg)
        eksik_t = [x for x in kk if not len(kk[x].dropna()) or kk[x].dropna().index.max() != onceki_seans]
    except IleriyeBakma as e:
        eksik_t = ["HATA"]; R = None
        for sid in E2: S.append(_sonuc(sid, durum="HATA", gerekce=str(e)))
    except Exception as e:
        eksik_t = ["HATA"]; R = None
        for sid in E2: S.append(_sonuc(sid, durum="HESAPLANAMADI", gerekce=f"beklenmeyen hata: {type(e).__name__}: {e}"))
    esik_yeni = {}
    if R is not None:
        n = len(R)
        art = {}
        for sid, c in E2.items():
            if c["y"] not in art:
                bas = max(1, n - 40) if not esik_yeniden else 1
                art[c["y"]] = madenci_artik(R, c["y"], range(bas, n))
            e = art[c["y"]]
            E = e.rolling(c["k"], min_periods=c["k"]).sum()  # E_d: e_{d-k+1..d}
            # x_d = E_{d-1}: gün d'de bilinen (t-1'de biter)
            xs = pd.Series(E.values, index=R.index).shift(1)
            xs.loc[t] = float(E.iloc[-1]) if len(E) else np.nan
            if esik_yeniden:
                xi = xs[[d <= dt.date(2017, 12, 31) for d in xs.index]].dropna()
                esik_yeni[sid] = (float(xi.quantile(c["q"])), float(xi.quantile(1 - c["q"])))
            dd = list(xs.index)
            pos = {d: (1.0 if (np.isfinite(xs.loc[d]) and xs.loc[d] > c["hi"]) else 0.0) for d in dd[-(c["h"] + 2):]}
            xt = float(xs.loc[t])
            eksik = [x for x in eksik_t if x in (c["y"], "GLD", "SPY")]
            if eksik:
                S.append(_sonuc(sid, durum="HESAPLANAMADI", gerekce=f"t-1 ({onceki_seans}) kapanışı eksik: {', '.join(eksik)}"))
                continue
            if not np.isfinite(xt):
                S.append(_sonuc(sid, durum="HESAPLANAMADI", gerekce="artık hesaplanamadı (geçmiş yetersiz)"))
                continue
            ye, acik, eff, effp, isl = kademe(pos, dd, t, c["h"])
            akt = xt > c["hi"]
            bolge = "üst kantil üstü" if akt else ("alt kantil altı: kısa bölge, yalnız uzun → nakit" if xt < c["lo"] else "arada")
            S.append(_sonuc(sid, durum="AKTİF (UZUN)" if akt else "NAKİT", deger=xt, deger_metin=f"x %{fs(xt * 100, 3, True)} ({bolge})",
                            esik_metin=f"x > %{fs(c['hi'] * 100, 3, True)}", aktif=bool(akt), yon="UZUN" if akt else "NAKİT", yeni_dilim=ye,
                            acik_dilimler=acik, etkin=eff, etkin_onceki=effp, islem=isl,
                            gerekce=f"{c['y']}'in GLD+SPY'ye göre {c['k']} günlük artık toplamı ({onceki_seans} kapanışında biter). {c['arac']} kolu etkin {fs(eff, 2)} (1/{c['h']} dilimler).",
                            veri_zamani=str(kk["GLD"]["avail"].iloc[-1]), ek=dict(x=xt, hi=c["hi"], lo=c["lo"])))
            if sid == "E2-C1_madenci_oncu_GLD_h5":
                # Kaplama (hakem E_C1kap_h5): dilim = 0 yalnız x < alt %20 kantil iken (x yoksa 1); o da 5 gün kademeli
                kp = {d: (0.0 if (np.isfinite(xs.loc[d]) and xs.loc[d] < c["lo"]) else 1.0) for d in dd[-(c["h"] + 2):]}
                kap_poz, _, keff, keffp, kisl = kademe(kp, dd, t, c["h"])
                S[-1]["ek"].update(kaplama_poz=kap_poz, kaplama_etkin=keff, kaplama_etkin_onceki=keffp, kaplama_islem=kisl)
                S[-1]["gerekce"] += (f" Kaplama sürümü (GLD tutana): bugünkü 1/5 dilim {'GLD TUT' if kap_poz else 'NAKİT (x alt %20 kantilin altında)'}"
                                     f" (eşik x < %{fs(c['lo'] * 100, 2, True)}); kademeli etkin GLD {fs(keff, 2)} (önce {fs(keffp, 2)}) → işlem {fs(kisl, 2, True)}.")
    out["esik_yeniden"] = esik_yeni

    # ---- E3-1 altın gün içi → GDXJ
    sid = "E3-1_altin_gunici_GDXJ_donus"
    try:
        xc, tsc, srcc = K.xau_an(et(onceki_seans, 16))
        # önceki gün pozisyonu (bugünkü işlem için). Yarım günde de gerekir: t-1'de açılan GDXJ bugün kapanışta satılır.
        pp = 0.0
        if not nyse_yarim(onceki_seans):
            o2 = gunler[i_t - 2] if i_t >= 2 else None
            if o2 is not None:
                a1, _, _ = K.xau_an(et(onceki_seans, 15)); a0, _, _ = K.xau_an(et(o2, 16))
                if np.isfinite(a1) and np.isfinite(a0): pp = 1.0 if math.log(a1 / a0) < 0 else 0.0
        if yarim:
            S.append(_sonuc(sid, durum="DEVRE DIŞI", yeni_dilim=0.0, etkin=0.0, etkin_onceki=pp, islem=(-pp if pp else 0.0),
                            gerekce="ABD yarım günü (13:00 ET kapanış): 15:00 ET karar anı kapanıştan sonra (veri notu 3); yeni pozisyon yok."
                                    + (" Dünkü GDXJ pozisyonu bugün kapanışta (13:00 ET) satılır." if pp else "")))
        elif not np.isfinite(xc):
            S.append(_sonuc(sid, durum="HESAPLANAMADI", etkin_onceki=pp, islem=(-pp if pp else 0.0), gerekce=f"{onceki_seans} 16:00 ET spot yok"))
        else:
            kontrol("spot XAUUSD 16:00 ET (t-1)", tsc, karar, sid)
            xn, tsn, srcn = K.xau_an(et(t, 15))
            if not np.isfinite(xn) or (et(t, 15) - tsn) > pd.Timedelta(hours=1):
                S.append(_sonuc(sid, durum="KOŞULLU" if simdi < karar else ("KOŞULLU (panelde gün t verisi yok)" if (K.mod == "panel" and t > K.son_gun["etf"])
                                                                              else "HESAPLANAMADI (gün t 15:00 ET spotu yok)"),
                                deger_metin=f"eşik fiyat {fs(xc, 2)} USD", yeni_dilim=np.nan, etkin=0.0, islem=(-pp if pp else 0.0),
                                esik_metin=f"15:00 ET spot < {fs(xc, 2)} USD → GDXJ al", etkin_onceki=pp,
                                gerekce=f"{gun_adi(t)} 15:00 ET'de spot altın {onceki_seans} 16:00 ET fiyatının ({fs(xc, 2)} USD) altındaysa GDXJ'yi kapanışta al, ertesi kapanışta sat; değilse nakit.",
                                ek=dict(esik_fiyat=xc, senaryo=dict(AL=1.0, NAKIT=0.0))))
            else:
                kontrol("spot XAUUSD 15:00 ET (t)", tsn, karar, sid)
                m = math.log(xn / xc)
                p = 1.0 if m < 0 else 0.0
                taze = (et(t, 15) - tsn) <= pd.Timedelta(minutes=2)
                yaklasik = str(srcn).startswith("Yahoo")
                durum = "AKTİF (UZUN)" if p else "NAKİT"
                if on: durum = f"ÖN-İZLEME ({durum})"
                elif not taze: durum = f"YAKLAŞIK ({durum}; 15:00 ET değeri {tsn.tz_convert(TZ_NY):%H:%M} ET gözlemi — veri gecikmeli, yeniden çalıştırın)"
                elif yaklasik: durum = f"YAKLAŞIK ({durum}; spot GC=F'ten baz düzeltmeli — birkaç dakika sonra yeniden çalıştırın)"
                S.append(_sonuc(sid, durum=durum, deger=m, deger_metin=f"m {fs(m * 1e4, 1, True)} bps (spot {fs(xn, 2)} / {fs(xc, 2)})",
                                esik_metin=f"m < 0 (spot < {fs(xc, 2)} USD)", aktif=bool(p), yon="UZUN" if p else "NAKİT", yeni_dilim=p, etkin=p,
                                etkin_onceki=pp, islem=p - pp,
                                gerekce=f"Altın {onceki_seans} 16:00 ET'den bu yana %{fs(m * 100, 2, True)}; {'düşüş → GDXJ ertesi gün dönüş beklentisi' if p else 'yükseliş → nakit'}."
                                        + (f" 15:00 ET değeri {tsn.tz_convert(TZ_NY):%H:%M} ET gözlemi ({srcn})." if (not taze or yaklasik) else ""),
                                veri_zamani=str(tsn), ek=dict(m=m, spot_cut=xn, spot_close_prev=xc, kaynak=srcn)))
    except IleriyeBakma as e:
        S.append(_sonuc(sid, durum="HATA", gerekce=str(e)))
    except Exception as e:  # beklenmeyen veri sorunu: sinyal düşer, betik sürer
        S.append(_sonuc(sid, durum="HESAPLANAMADI", gerekce=f"beklenmeyen hata: {type(e).__name__}: {e}"))

    # ---- E3-3 PHYS/GLD ve E3-4 CEF (araç seçimi)
    for sid in ("E3-3_PHYS_GLD_iskonto", "E3-4_CEF_artik"):
        try:
            gg = gunler[: i_t]
            kg = K.kapanis("GLD", karar)
            if sid.startswith("E3-3"):
                kp = K.kapanis("PHYS", karar)
                if not len(kp) or kp.dropna().index.max() != onceki_seans:
                    S.append(_sonuc(sid, durum="HESAPLANAMADI", gerekce="PHYS t-1 kapanışı yok")); continue
                kontrol("Yahoo PHYS kapanışı", kp["avail"].iloc[-1], karar, sid)
                c1 = kp["close"].reindex(gg).astype(float); c0 = kg["close"].reindex(gg).astype(float)
                lvl = np.log(c1 / c0).iloc[-700:]
                esik = P["PHYS_ESIK"]; k_ = P["PHYS_K"]
            else:
                kc = K.kapanis("CEF", karar); ks = K.kapanis("SLV", karar)
                if not len(kc) or kc.dropna().index.max() != onceki_seans:
                    S.append(_sonuc(sid, durum="HESAPLANAMADI", gerekce="CEF t-1 kapanışı yok")); continue
                kontrol("Yahoo CEF kapanışı", kc["avail"].iloc[-1], karar, sid)
                rC, rG, rS = _getiri(kc, gg), _getiri(kg, gg), _getiri(ks, gg)
                dd = pd.concat([rC.rename("y"), rG.rename("g"), rS.rename("s")], axis=1).dropna()
                Yv = dd.y.values; XX = np.column_stack([np.ones(len(dd)), dd[["g", "s"]].values])
                eC = pd.Series(np.nan, index=dd.index)
                W = P["CEF_BETA"]
                for i in range(max(W, len(dd) - 700), len(dd)):
                    b = np.linalg.lstsq(XX[i - W:i], Yv[i - W:i], rcond=None)[0]
                    eC.iloc[i] = Yv[i] - XX[i, 1:] @ b[1:]
                er = eC.reindex(gg)
                lvl = er.fillna(0).cumsum().where(er.notna()).iloc[-700:]
                esik = P["CEF_ESIK"]; k_ = P["CEF_K"]
            dev = lvl - lvl.rolling(k_, min_periods=k_ // 2).median()
            z = dev / dev.rolling(P["PHYS_STD"], min_periods=120).std()
            zt = float(z.iloc[-1]) if len(z) else np.nan
            if not np.isfinite(zt):
                S.append(_sonuc(sid, durum="HESAPLANAMADI", gerekce="z hesaplanamadı")); continue
            akt = zt < esik
            arac = ("PHYS" if akt else "GLD") if sid.startswith("E3-3") else ("CEF" if akt else "GLD/SLV")
            S.append(_sonuc(sid, durum=f"ARAÇ: {arac}", deger=zt, deger_metin=f"z {fs(zt, 2, True)}", esik_metin=f"z < {fs(esik, 1, True)}", aktif=bool(akt),
                            yon="—", gerekce=(f"Altın alınacaksa {arac} tercih edilir (z {fs(zt, 2, True)})." if akt else f"İskonto eşiğin üstünde; olağan araç ({arac})."),
                            veri_zamani=str(kg["avail"].iloc[-1]), ek=dict(z=zt)))
        except IleriyeBakma as e:
            S.append(_sonuc(sid, durum="HATA", gerekce=str(e)))
        except Exception as e:  # beklenmeyen veri sorunu: sinyal düşer, betik sürer
            S.append(_sonuc(sid, durum="HESAPLANAMADI", gerekce=f"beklenmeyen hata: {type(e).__name__}: {e}"))

    # sıra: hakem listesi
    sira = list(k for k in BILGI if BILGI[k]["cephe"] == "ETF")
    S = sorted(S, key=lambda s: sira.index(s["id"]))
    out["sinyaller"] = S
    # birleşim: 5 yönlü sinyal, her biri sermayenin 1/5'i; aynı ETF'de netleşir
    yon = [s for s in S if s["id"] in ("E1-C2_GDX_tatil_oncesi", "E2-C2j_GDXJ_artik_h3", "E2-C2_GDX_artik_h3", "E2-C1_madenci_oncu_GLD_h5", "E3-1_altin_gunici_GDXJ_donus")]
    ag = {}
    for s in yon:
        a = BILGI[s["id"]]["arac"]
        ag.setdefault(a, [0.0, 0.0])
        ag[a][0] += float(s["etkin"] or 0) / 5; ag[a][1] += float(s["etkin_onceki"] or 0) / 5
    sen = {}
    for s in yon:
        for k, v in (s["ek"].get("senaryo") or {}).items():
            a = BILGI[s["id"]]["arac"]
            sen[f"{s['id']}={k}"] = {a: ag[a][0] + (v - float(s["etkin"] or 0)) / 5}
    out["birlesik"] = dict(agirlik={a: v[0] for a, v in ag.items()}, onceki={a: v[1] for a, v in ag.items()},
                           islem={a: v[0] - v[1] for a, v in ag.items()}, senaryo=sen,
                           eksik=[s["id"] for s in yon if str(s["durum"]).startswith(("HESAPLANAMADI", "HATA", "KOŞULLU", "BEKLİYOR"))])
    return out


# =====================================================================================================================
# 7. TAKVİM UYARILARI, RİSK, BAĞLAM
# =====================================================================================================================
def _olaylari_oku(dizin: str | None):
    if not dizin or not os.path.isdir(dizin): return
    try:
        for fn, D in (("events_fomc.csv", FOMC), ("events_us_nfp.csv", NFP), ("events_us_cpi.csv", CPI)):
            p = os.path.join(dizin, fn)
            if not os.path.exists(p): continue
            x = pd.read_csv(p)
            col = "announce_utc" if "announce_utc" in x else "release_utc"
            for _, r in x.iterrows():
                D.setdefault(str(r["date"])[:10], str(r[col]))
    except Exception:
        pass


def takvim_uyarilari(tv: dt.date, te: dt.date):
    U = []
    bas = min(tv, te); bit = bas + dt.timedelta(days=9)
    # Türkiye
    d = bas
    while d <= bit:
        if d.weekday() < 5 and d in TR_TATIL: U.append(("VİOP", str(d), f"Türkiye resmi tatili — VİOP kapalı ({gun_adi(d)})"))
        if d in TR_YARIM: U.append(("VİOP", str(d), "Türkiye yarım günü — uzlaşma 12:30–12:40 TSİ, akşam seansı yok; 15:00 UTC sinyalleri (LOWMOM, son saat) devre dışı"))
        if d.weekday() < 5 and not nyse_is_gunu(d):
            ad = nyse_tatilleri(d.year).get(d, "plansız kapanış")
            U.append(("NYSE", str(d), f"NYSE tatili ({ad}) — ETF işlem yok"))
        if nyse_is_gunu(d) and nyse_yarim(d): U.append(("NYSE", str(d), "NYSE yarım günü — kapanış 13:00 ET; E3-1 devre dışı, emir 12:50–12:58 ET"))
        d += dt.timedelta(days=1)
    # çeyrek sonu / ay başı (her iki takvim)
    for ad, fn, g0 in (("VİOP", tr_is_gunu, tv), ("NYSE", nyse_is_gunu, te)):
        g = [g0] + [sonraki(g0, fn, k) for k in range(1, 6)]
        for i, x in enumerate(g):
            nxt = sonraki(x, fn)
            if x.month in (3, 6, 9, 12) and nxt.month != x.month: U.append((ad, str(x), f"çeyrek sonu son işlem günü ({x.month}. ay)"))
            prv = onceki(x, fn)
            if prv.month != x.month: U.append((ad, str(x), "ay başı (ayın ilk işlem günü)"))
    # ABD makro olayları
    for nm, D in (("FOMC karar", FOMC), ("ABD istihdam (NFP)", NFP), ("ABD TÜFE (CPI)", CPI), ("ABD TÜFE (CPI, tahmini — kontrol edin)", CPI_TAHMINI)):
        for k, v in D.items():
            kd = dt.date.fromisoformat(k)
            if bas <= kd <= bit:
                hh, mm = map(int, v.split(":"))
                U.append(("ABD", k, f"{nm} {v} UTC ({tsi(utc(kd, hh, mm))})" + (" — VİOP uzlaşmasından SONRA" if (hh, mm) > (15, 10) else " — VİOP kararından ÖNCE")))
    for nm, son in TAKVIM_SONU.items():
        if bit > dt.date.fromisoformat(son):
            U.append(("ABD", "—", f"{nm} yerleşik listesi {son} tarihinde bitiyor; sonrası için resmi takvimi kontrol edin"))
    # COMEX OG vadesi
    for y, m in {(bas.year, bas.month), (bit.year, bit.month)}:
        og = og_vade(y, m)
        if bas <= og <= bit + dt.timedelta(days=5): U.append(("COMEX", str(og), f"COMEX altın opsiyonu (OG) son işlem günü ({m % 12 + 1}. ay kontratı)"))
    # LBMA Aralık
    if bas.month == 12 and bas.day >= 15:
        U.append(("VİOP", "—", "LBMA 24 ve 31 Aralık'ta yalnız AM ihalesi yapabilir; F_XAUUSD1226 vade sonu fiyatı AM'e göre belirlenebilir; 31 Aralık akşam seansı yok"))
    U = sorted(set(U), key=lambda x: (x[1], x[0]))
    return [dict(alan=a, tarih=b, mesaj=c) for a, b, c in U]


def risk_bolumu(K, tv: dt.date, te: dt.date, simdi, sermaye=None):
    R = dict()
    # VİOP: spot 15:00 UTC serisi
    kv = viop_karar(tv)
    p15 = K.p15_seri(tv, kv)
    if len(p15) > 300:
        lp = np.log(p15.astype(float))
        r = lp.diff().dropna()
        sig = float(r.iloc[-20:].std())
        P0 = float(p15.iloc[-1])
        band = {}
        for h in (1, 3, 5):
            hh = lp.diff(h).dropna().iloc[-250:]
            band[h] = dict(normal_pct=1.96 * sig * math.sqrt(h), alt_tarihsel_pct=float(-np.quantile(hh, 0.025)), ust_tarihsel_pct=float(np.quantile(hh, 0.975)),
                           usd=P0 * (math.exp(1.96 * sig * math.sqrt(h)) - 1), var99_tarihsel_pct=float(-np.quantile(hh, 0.01)))
        R["viop"] = dict(rv20_yillik=sig * math.sqrt(252), fiyat=P0, fiyat_gunu=str(p15.index[-1]), bant=band)
    vb = K.viop_bilgi(tv, kv)
    R["viop_bulten"] = vb
    if vb and "uzlasma" in vb:
        u = vb["uzlasma"]; kur = vb.get("usdtry", np.nan)
        R["teminat"] = dict(psr=P["PSR"], usd=P["PSR"] * u, tl=P["PSR"] * u * kur if np.isfinite(kur) else np.nan,
                            araci_usd=P["ARACI_PSR"] * u, araci_tl=P["ARACI_PSR"] * u * kur if np.isfinite(kur) else np.nan,
                            nominal_usd=u, nominal_tl=u * kur if np.isfinite(kur) else np.nan, kur=kur, kur_kaynak=vb.get("usdtry_kaynak"))
        if sermaye and np.isfinite(kur):
            R["teminat"]["azami_sozlesme_2x"] = int(P["NOMINAL_TAVAN"] * sermaye / (u * kur))
        vs = viop_vade_son_gunu(vb.get("kod", ""))
        if vs:
            kalan = len(viop_gunleri(tv, vs)) - 1
            R["vade"] = dict(kod=vb.get("kod"), son_islem=str(vs), kalan_viop_gunu=kalan)
    # ETF
    ke = etf_karar(te)
    E = {}
    gun = K.veri_gunleri_etf(te)
    gg = [d for d in gun if d < te]
    for x in ("GLD", "GDX", "GDXJ"):
        k = K.kapanis(x, ke)
        if len(k) < 300: continue
        r = _getiri(k, gg).dropna()
        sig = float(r.iloc[-20:].std())
        c0 = float(k["close"].dropna().iloc[-1])
        E[x] = dict(rv20_yillik=sig * math.sqrt(252), son_kapanis=c0, gun=str(k["close"].dropna().index[-1]),
                    bant={h: dict(normal_pct=1.96 * sig * math.sqrt(h), usd=c0 * (math.exp(1.96 * sig * math.sqrt(h)) - 1),
                                  var99_tarihsel_pct=float(-np.quantile(np.log(k["close"].reindex(gg).astype(float)).diff(h).dropna().iloc[-250:], 0.01))) for h in (1, 3, 5)})
    R["etf"] = E
    R["ust"] = K.ust_bilgi(tv, kv)
    return R


# =====================================================================================================================
# 8. RAPOR
# =====================================================================================================================
def rapor_metin(S: dict) -> str:
    L = []
    w = L.append
    w("=" * 100)
    w(f"ALTIN SİNYALLERİ — sinyal_altin.py {SURUM}")
    w(f"Mod: {S['mod'].upper()} | çalışma anı {S['calisma_utc']} UTC ({S['calisma_tsi']}) | istenen tarih {S['istenen']}")
    w("Uyarı: VİOP sinyallerinin hepsi DÜŞÜK, ETF sinyalleri ORTA güvenli. Hakem birleşim rakamları üst sınırdır; gerçekçi beklenti yarısı.")
    w("Bu çıktı yatırım tavsiyesi değildir; kuralların mekanik hesabıdır.")
    for blok, baslik in (("viop", "VİOP F_XAUUSD"), ("etf", "MIDAS / ABD ETF")):
        B = S[blok]
        w("")
        w("=" * 100)
        if B.get("kapali"):
            w(f"[{baslik}] {B['tarih']} {B['gun']}: piyasa kapalı."); continue
        if blok == "viop":
            w(f"[1] {baslik} — gün t = {B['tarih']} {B['gun']}; karar anı {B['karar_utc'][11:16]} UTC ({B['karar_tsi']}); giriş: {B['emir']}")
        else:
            w(f"[2] {baslik} — gün t = {B['tarih']} {B['gun']}; karar anı {B['karar_et']} ({B['karar_tsi']}); giriş: {B['emir']}")
        if B.get("not"): w(f"    Not: {B['not']}")
        w("-" * 100)
        for s in B["sinyaller"]:
            w(f"• {s['id']} — {s['ad']} [güven: {s['guven']}] → {s['durum']}")
            if s["deger_metin"] or s["esik_metin"]:
                w(f"    değer: {s['deger_metin'] or '—'} | eşik: {s['esik_metin'] or '—'}")
            if not s["id"].startswith(("E3-3", "E3-4")):
                ac = ", ".join(f"{k[5:]}:{fs(v, 0, True)}" for k, v in s["acik_dilimler"].items()) or "—"
                yd = s["yeni_dilim"]
                w(f"    yön: {s['yon']} | tutuş: {s['h']} gün{' (kademeli, her gün 1/' + str(s['h']) + ')' if s['h'] > 1 else ''} | yeni dilim: {fs(yd, 0, True) if yd is not None and np.isfinite(yd) else '—'} | açık dilimler: {ac}")
                w(f"    etkin poz.: {fs(s['etkin'], 3, True)} (önce {fs(s['etkin_onceki'], 3, True)}) → bugünkü işlem: {fs(s['islem'], 3, True)} birim ({s['arac']})")
            w(f"    gerekçe: {s['gerekce']}")
            if s["id"] == "A1-LOWMOM-h1" and s["ek"].get("h5"):
                h5 = s["ek"]["h5"]
                w(f"    h=5 varyantı (bağımsız değil): etkin {fs(h5['etkin'], 3, True)}, bugünkü işlem {fs(h5['islem'], 3, True)}")
            w(f"    kural: {s['kural']}")
            w(f"    bilgi zamanı: {s['bilgi_zamani']}; son gözlem: {s['veri_zamani'] or '—'}")
            w(f"    hakem: {s['hakem_notu']}")
        b = B["birlesik"]
        w("-" * 100)
        if blok == "viop":
            w(f"Birleşik VİOP (LOWMOM-h1, QEND, A4-C1, son saat; her biri 1/4): etkin {fs(b['etkin'], 3, True)} birim; "
              f"önceki {fs(b['onceki'], 3, True)} → bugünkü işlem {fs(b['islem'], 3, True)} birim.")
            for k, v in b.get("senaryo", {}).items(): w(f"    senaryo {k}: birleşik etkin {fs(v, 3, True)} birim (işlem {fs(v - b['onceki'], 3, True)})")
            w("    1 birim = seçtiğiniz tam nominal (öneri: nominal ≤ 2 × özsermaye). A4-C1 ile ETF E2-C2j aynı fenomen: ikisini birden tam ağırlıkla kullanmayın.")
        else:
            ag = ", ".join(f"{a} %{fs(v * 100, 1)}" for a, v in b["agirlik"].items())
            isl = ", ".join(f"{a} {fs(v * 100, 1, True)} puan" for a, v in b["islem"].items() if abs(v) > 1e-9) or "değişiklik yok"
            w(f"Birleşik ETF (5 yönlü sinyal, her biri sermayenin 1/5'i, aynı ETF'de netleşir): {ag}; bugünkü işlem: {isl}.")
            for k, v in b.get("senaryo", {}).items():
                w(f"    senaryo {k}: " + ", ".join(f"{a} %{fs(x * 100, 1)} (işlem {fs((x - b['onceki'].get(a, 0)) * 100, 1, True)} puan)" for a, x in v.items()))
            ph = [s for s in B["sinyaller"] if s["id"].startswith(("E3-3", "E3-4"))]
            w("    Araç seçimi: " + "; ".join(f"{s['id']}: {s['durum']} ({s['deger_metin']})" for s in ph))
        if b.get("eksik"): w(f"    Eksik/bekleyen: {', '.join(b['eksik'])} — bu sinyallerin bugünkü yeni dilimi birleşimde 0 sayıldı (senaryolara bakın).")
    # takvim
    w("")
    w("=" * 100)
    w("[3] TAKVİM UYARILARI (önümüzdeki ~10 gün)")
    for u in S["takvim"]: w(f"  {u['tarih']:<10} {u['alan']:<6} {u['mesaj']}")
    if not S["takvim"]: w("  —")
    # risk
    R = S["risk"]
    w("")
    w("=" * 100)
    w("[4] RİSK")
    if "viop" in R:
        v = R["viop"]
        w(f"  VİOP/spot: rv20 %{fs(v['rv20_yillik'] * 100, 1)} yıllık (spot 15:00 UTC, {v['fiyat_gunu']} fiyat {fs(v['fiyat'], 2)} USD)")
        for h, b in v["bant"].items():
            w(f"    {h} gün %95 hareket: ±%{fs(b['normal_pct'] * 100, 2)} (≈ ±{fs(b['usd'], 0)} USD/ons; normal varsayım) | son 250 gün tarihsel %2,5–%97,5: "
              f"−%{fs(b['alt_tarihsel_pct'] * 100, 2)} / +%{fs(b['ust_tarihsel_pct'] * 100, 2)} | tarihsel VaR99 %{fs(b['var99_tarihsel_pct'] * 100, 2)}")
    if R.get("teminat"):
        tm = R["teminat"]
        w(f"  VİOP teminat yaklaşımı (1 sözleşme = 1 ons; {R['viop_bulten'].get('kod')} {R['viop_bulten'].get('tarih')} uzlaşması {fs(tm['nominal_usd'], 1)} USD):")
        w(f"    Takasbank PSR %{fs(tm['psr'] * 100, 0)} → ≈ {fs(tm['usd'], 0)} USD ≈ {fs(tm['tl'], 0)} TL / sözleşme; aracı kurum %20 isterse ≈ {fs(tm['araci_usd'], 0)} USD ≈ {fs(tm['araci_tl'], 0)} TL")
        w(f"    nominal ≈ {fs(tm['nominal_tl'], 0)} TL / sözleşme (kur {fs(tm['kur'], 3)}: {tm['kur_kaynak']}). PSR güncel değeri için Takasbank risk parametrelerini kontrol edin.")
        if tm.get("azami_sozlesme_2x") is not None: w(f"    Özsermayeye göre azami sözleşme (nominal ≤ 2× özsermaye): {tm['azami_sozlesme_2x']}")
    elif R.get("viop_bulten", {}).get("hata"):
        w(f"  VİOP bülteni: {R['viop_bulten']['hata']} — teminat hesaplanamadı")
    if R.get("vade"):
        vd = R["vade"]
        w(f"  Aktif kontrat {vd['kod']}: son işlem günü {vd['son_islem']} ({vd['kalan_viop_gunu']} VİOP günü kaldı)"
          + (" — UYARI: tutuş süresi vade sonunu aşabilir; açık pozisyon genelde 3–4 gün kala yeni vadeye geçer" if vd["kalan_viop_gunu"] <= 7 else ""))
    for x, e in R.get("etf", {}).items():
        w(f"  {x}: rv20 %{fs(e['rv20_yillik'] * 100, 1)} yıllık; son kapanış {fs(e['son_kapanis'], 2)} USD ({e['gun']}); %95 hareket "
          + " | ".join(f"{h}g ±%{fs(b['normal_pct'] * 100, 2)}" for h, b in e["bant"].items())
          + "; tarihsel VaR99 " + " / ".join(f"{h}g %{fs(b['var99_tarihsel_pct'] * 100, 1)}" for h, b in e["bant"].items()))
    w("  Hakem notu: ±%10 VİOP fiyat limitine hiç ulaşılmadı (en büyük günlük düşüş −%7,8); 2σ dip alma kuralları zarar ediyor.")
    if R.get("ust"):
        u = R["ust"]
        w(f"  Bağlam (sinyal değil): ABD 10y nominal %{fs(u.get('nom10'), 2)}, 10y reel %{fs(u.get('real10'), 2)} ({u.get('not_')})")
    # veri
    w("")
    w("=" * 100)
    w("[5] VERİ VE ZAMAN DAMGASI DENETİMİ")
    ihlal = [d for d in S["denetim"] if d["sonuc"] == "İHLAL"]
    w(f"  {len(S['denetim'])} kontrol; ihlal {len(ihlal)}; veri yok {sum(1 for d in S['denetim'] if d['sonuc'] == 'VERİ YOK')}")
    gor = {}
    for d in S["denetim"]:
        gor[(d["veri"], d["karar_utc"])] = d
    for (v, k), d in list(gor.items())[:30]:
        w(f"  {d['sonuc']:<8} {v:<34} son gözlem {str(d['son_gozlem_utc'])[:19]:<19}  ≤  karar {k[:16]}")
    for u in S.get("uyarilar", []): w(f"  uyarı: {u}")
    w("=" * 100)
    return "\n".join(L)


# =====================================================================================================================
# 9. ANA AKIŞ
# =====================================================================================================================
def calistir(args, log=print) -> dict:
    DENETIM.clear()
    simdi_gercek = pd.Timestamp.now(tz="UTC")
    simule = bool(args.simule_an)
    simdi = pd.Timestamp(args.simule_an).tz_convert("UTC") if simule else simdi_gercek
    if args.tarih:
        t0 = dt.date.fromisoformat(args.tarih)
    else:
        t0 = simdi.tz_convert(TZ_TR).date()
    _olaylari_oku(args.olay_dizini)
    notlar = {}
    tv = t0 if tr_is_gunu(t0) else sonraki(t0, tr_is_gunu)
    te = t0 if nyse_is_gunu(t0) else sonraki(t0, nyse_is_gunu)
    if tv != t0: notlar["viop"] = f"{t0} VİOP işlem günü değil; bir sonraki işlem günü {tv} için hesaplandı."
    if te != t0: notlar["etf"] = f"{t0} NYSE işlem günü değil; bir sonraki işlem günü {te} için hesaplandı."
    if args.panel:
        K = PanelKaynak(args.panel_dizini, log=log)
        simdi = pd.Timestamp("2262-01-01", tz="UTC")  # panel: 'şimdi' yok; her veri kendi damgasıyla
    else:
        K = CanliKaynak(args.onbellek, saat=simdi, simule=simule, log=log)
        if args.tohum_dizini: K.tohumla(args.tohum_dizini)
        kv, ke = viop_karar(tv), etf_karar(te)
        tick = {}
        for d, Hs in ((tv, [12, 13, 14]), (te, [int(et(te, 15).hour) - 2, int(et(te, 15).hour) - 1])):
            tick.setdefault(d, set()).update(Hs)
        tick.setdefault(onceki(te, nyse_is_gunu), set()).update([int(et(te, 16).hour) - 2, int(et(te, 16).hour) - 1])
        gereken = dict(son_gun=max(tv, te), tick_saatleri=tick, viop_t1=onceki(tv, tr_is_gunu))
        K.hazirla(gereken)
    V = viop_sinyalleri(K, tv, simdi)
    if notlar.get("viop"): V["not"] = notlar["viop"]
    Et = etf_sinyalleri(K, te, simdi, esik_yeniden=args.esik_yeniden)
    if notlar.get("etf"): Et["not"] = notlar["etf"]
    S = dict(surum=SURUM, mod="panel" if args.panel else ("canli-simule" if simule else "canli"), istenen=str(t0),
             calisma_utc=(simdi_gercek if not simule else simdi).strftime("%Y-%m-%d %H:%M"),
             calisma_tsi=(simdi_gercek if not simule else simdi).tz_convert(TZ_TR).strftime("%Y-%m-%d %H:%M TSİ"),
             viop=V, etf=Et, takvim=takvim_uyarilari(tv, te), risk=_guvenli(lambda: risk_bolumu(K, tv, te, simdi, args.ozsermaye_tl)),
             denetim=list(DENETIM), uyarilar=getattr(K, "uyarilar", []))
    if not args.panel:
        if simdi > viop_karar(tv) + pd.Timedelta(minutes=10) and tv == simdi.date():
            S["uyarilar"].append("VİOP uzlaşma penceresi geçti; yarın için --tarih ile ön-izleme alın.")
        if simdi > (et(te, 13) if nyse_yarim(te) else et(te, 16)) and te == simdi.tz_convert(TZ_NY).date():
            S["uyarilar"].append("ABD kapanışı geçti; yarın için --tarih ile ön-izleme alın.")
    return S


def _guvenli(fn):
    try:
        return fn()
    except Exception as e:  # risk bölümü hesaplanamazsa rapor yine üretilir
        return dict(hata=f"{type(e).__name__}: {e}")


def _json_temiz(o):
    if isinstance(o, dict): return {str(k): _json_temiz(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [_json_temiz(v) for v in o]
    if isinstance(o, (np.floating, float)): return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    if isinstance(o, (pd.Timestamp, dt.date, dt.datetime)): return str(o)
    return o


def main(argv=None):
    ap = argparse.ArgumentParser(description="Altın günlük sinyal betiği (VİOP F_XAUUSD + Midas ABD ETF'leri)")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--canli", action="store_true", help="ağdan güncel veriyi indir")
    g.add_argument("--panel", action="store_true", help="araştırma panellerinden geçmiş günü yeniden üret (--tarih gerekli)")
    ap.add_argument("--tarih", help="gün t (YYYY-MM-DD); canlıda varsayılan bugün (İstanbul)")
    ap.add_argument("--panel-dizini", default=os.path.normpath(os.path.join(BURASI, "..", "..", "panel")))
    ap.add_argument("--olay-dizini", default=os.path.normpath(os.path.join(BURASI, "..", "a3_takvim_olay")),
                    help="events_fomc/us_nfp/us_cpi.csv dizini (varsa yerleşik listeyi genişletir)")
    ap.add_argument("--onbellek", default=os.path.join(os.path.expanduser("~"), ".cache", "sinyal_altin"))
    ap.add_argument("--tohum-dizini", help="canlı: önbelleği bu dizindeki ham Dukascopy aylık XAUUSD dosyalarıyla (YYYY_AA0.bi5) doldur")
    ap.add_argument("--ozsermaye-tl", type=float, default=None, help="VİOP azami sözleşme hesabı için özsermaye (TL)")
    ap.add_argument("--json", help="sonuçları JSON dosyasına yaz")
    ap.add_argument("--esik-yeniden", action="store_true", help="E2 eşiklerini IS (2008–2017) verisinden yeniden hesapla ve göster")
    ap.add_argument("--simule-an", help="TEST: canlı modu bu UTC anında çalışıyormuş gibi (ör. 2026-11-06T14:50:00Z)")
    ap.add_argument("--sessiz", action="store_true")
    a = ap.parse_args(argv)
    if a.panel and not a.tarih: ap.error("--panel için --tarih gerekli")
    log = (lambda *x, **k: None) if a.sessiz else (lambda *x, **k: print(*x, file=sys.stderr, **k))
    S = calistir(a, log=log)
    print(rapor_metin(S))
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f: json.dump(_json_temiz(S), f, ensure_ascii=False, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
