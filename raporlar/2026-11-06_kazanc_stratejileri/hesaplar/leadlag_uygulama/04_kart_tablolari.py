#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
04_kart_tablolari.py - hisse_kartlari/<KOD>.json'daki ORTA ve YUKSEK guvenli TUM suruculeri bu profilin etiketlerine
cevirir (KENAR / FILTRE / RISK / YOK / TEST EDILMEDI) ve Markdown ek tablosu uretir.
Esleme kurali (kapanistan kapanisa, karar 18:00-18:15 TSI, gun ici ekran yok):
  gap_oncu, olay           -> RISK  (bilgi acilis gap'inde / olay aninda fiyatlaniyor)
  senkron, rejim           -> FILTRE (hedge, kume, boyut, konum; oncu degil). 'ayni varlik' (ADR) -> YOK
  gunici_oncu (t-1 -> gun ici t) -> RISK (t gununde, kullanicinin kapanis girisinden ONCE fiyatlaniyor); istisnalar asagida
  mikroyapi: 09:30 vadeli acilisi -> YOK (yalniz acilis icrasi); baz anomalisi -> RISK (ertesi gap);
             kapanis muzayedesi donusu -> FILTRE (yalniz spot KFI yurutmesi); kendi gap fade -> YOK (acilis emri ister);
             tavan/limit -> RISK (kilit)
  cok_gunluk SAHOL/AKBNK orani -> KENAR (K1, 20 gun)
Kartlardaki sayi metni kisaltilarak alinir; tam metin kartta.
"""
import json, os, sys

KART = "/home/user/Xxxx/raporlar/2026-11-02_viop_leadlag/hisse_kartlari"
HISSELER = ["TUPRS", "SAHOL", "AKBNK", "ENJSA", "KCHOL", "BRSAN", "TRMET", "TRALT"]
OZEL = {
    ("TUPRS", 5): ("KENAR", "kapanis->kapanis surumu (US t-1 -> F_TUPRS t uzlasma -> t+2) rehberde test edildi: net +42 bps (8 bps), 2024-26 t 1,0; gun ici surumu bu profil icin degil"),
    ("TUPRS", 11): ("YOK", "brut 8,5 bps < 2 bacak maliyeti"),
    ("TUPRS", 15): ("YOK", "saatlik, seans ici; maliyet sonrasi negatif"),
    ("SAHOL", 14): ("FILTRE", "yeni cc testi: +22 bps/1sd, t 2,96 (q 0,03) ama tek bacak net -4,6 bps -> yalniz K1 bilgisi"),
    ("ENJSA", 6): ("FILTRE", "yalniz spot KFI 18:10-18:15 yurutmesi (sert CA yukselisinden sonra kapanistan alma); VIOP'ta yok"),
    ("ENJSA", 7): ("YOK", "acilis emri ister (profil disi)"),
    ("ENJSA", 8): ("YOK", "bilgi ilk 30 dk'da; profil disi"),
    ("TRMET", 8): ("FILTRE", "Koza z3 kuralinin icinde (u = TRMET - b*grup); yeni cc testi tek basina t -1,6, q 0,39"),
    ("TRMET", 9): ("FILTRE", "yalniz spot KFI yurutmesi; VIOP uzlasmasi CA'nin %41'ini izliyor"),
    ("TRALT", 1): ("RISK", "t gununde fiyatlaniyor; yeni cc testi (FF49 Gold artigi -> TRALT t->t+1) +4,7 bps, t 0,78"),
    ("BRSAN", 4): ("RISK", "kenar ilk 30 dk'da; 07:30 sonrasi negatif"),
    ("BRSAN", 6): ("YOK", "acilis gap'ine gun ici yetisme; profil disi"),
    ("BRSAN", 7): ("YOK", "acilis emri ister (profil disi)"),
    ("BRSAN", 8): ("RISK", "kilitli tavanda dolum yok; boyut/kuyruk bilgisi"),
    ("AKBNK", 16): ("YOK", "bilgi ilk 30 dk'da; profil disi"),
    ("SAHOL", 3): ("KENAR", "K1: z60 +-2, ertesi gun giris, 20 gun; 1 gun gecikmeyle +160/+310 bps/islem"),
    ("AKBNK", 9): ("KENAR", "K1 bacagi"),
    ("TUPRS", 2): ("FILTRE", "piyasa baglami; XU030 hedge'i TUPRS'ta ise yaramiyor, gece riskini artiriyor [PL s3]"),
}


def etiket(h, i, d):
    if (h, i) in OZEL:
        return OZEL[(h, i)]
    rel = (d.get("relation") or "").lower(); tr = (d.get("tradable") or "").lower(); drv = (d.get("driver") or "").lower()
    if rel in ("gap_oncu", "olay"):
        return ("RISK", "acilis gap'i / olay aninda fiyatlaniyor")
    if rel in ("senkron", "rejim"):
        if "aynı varlık" in tr:
            return ("YOK", "ayni varlik (bayat ADR)")
        met = (d.get("metric") or "")
        if "ortak faktör" in met and ("yalnız ortak" in met or "sadece ortak" in met or "'yalnız ortak" in met):
            return ("FILTRE", "zayif: ortak faktor kontrolunde ~0 (dolayli bag); oncu degil")
        return ("FILTRE", "hedge / kume / boyut; oncu degil")
    if rel == "gunici_oncu":
        return ("RISK", "t gununde fiyatlaniyor (kapanis girisinden once biter)")
    if rel == "mikroyapi":
        if "09:30" in drv or "açılış" in drv and "vadeli" in drv:
            return ("YOK", "yalniz acilis icrasi")
        if "baz" in drv:
            return ("RISK", "ertesi spot gap; vadelide kalinti yok")
        if "müzayede" in drv:
            return ("FILTRE", "yalniz spot KFI yurutmesi")
        if "gap" in drv:
            return ("YOK", "acilis emri ister")
        if "tavan" in drv or "limit" in drv:
            return ("RISK", "kilit")
        return ("YOK", "")
    if rel == "cok_gunluk":
        return ("TEST EDILMEDI", "")
    return ("TEST EDILMEDI", "")


def kisa(s, n):
    s = (s or "").replace("|", "/").replace("\n", " ").strip()
    return s if len(s) <= n else s[:n - 1].rstrip() + "…"


def main():
    out = ["## Ek A. Kart sürücüleri (yalnız ORTA ve YÜKSEK güven) → bu profilin etiketi", "",
           "Kaynak `2026-11-02_viop_leadlag/hisse_kartlari/<KOD>.json`. Sayılar kısaltıldı; tam metin kartta. "
           "Eşleme kuralı `hesaplar/leadlag_uygulama/04_kart_tablolari.py` başlığında. Kartı olmayanlar: ENERY, AHGAZ, RYSAS (§3).", ""]
    say = {}
    for h in HISSELER:
        d = json.load(open(os.path.join(KART, h + ".json")))
        out += [f"### {h} (`{d['tv_spot']}`, `{d['tv_viop']}`)", "",
                "| # | Sürücü | TradingView | İlişki | Sayılar (kart) | Kartın hükmü | Güven | Etiket | Not |", "|---|---|---|---|---|---|---|---|---|"]
        for i, x in enumerate(d["drivers"]):
            c = (x.get("confidence") or "").upper()
            if c not in ("ORTA", "YUKSEK", "YÜKSEK"):
                continue
            e, n = etiket(h, i, x)
            say[e] = say.get(e, 0) + 1
            tv = x.get("tv") or ""
            out.append(f"| {i} | {kisa(x['driver'], 70)} | `{kisa(tv, 60)}` | {x.get('relation')} | {kisa(x.get('metric'), 170)} | "
                       f"{kisa(x.get('tradable'), 90)} | {c} | **{e}** | {kisa(n, 110)} |")
        out.append("")
    out.insert(4, "Etiket sayımı (8 kart, ORTA+YÜKSEK): " + ", ".join(f"{k} {v}" for k, v in sorted(say.items())) + ".")
    out.insert(5, "")
    txt = "\n".join(out)
    dst = sys.argv[1] if len(sys.argv) > 1 else "ek_kartlar.md"
    open(dst, "w").write(txt + "\n")
    print(dst, len(txt), say)


if __name__ == "__main__":
    main()
