#!/usr/bin/env python3
"""TradingView kodlarinin toplu dogrulamasi (R3).

Yalniz herkese acik https://www.tradingview.com/symbols/BIST-<KOD>/ sayfalari
curl ile cekilir; HTTP kodu ve <title> kaydedilir. Websocket / oturum yok.
Calistirma:  python3 -I tv_check.py <cikti.csv>
"""
import csv, html, re, subprocess, sys, time, urllib.parse

UYELER = ("A1YEN AHGAZ AKENR AKFYE AKSEN AKSUE ALFAS ARFYE AYDEM AYEN BESTE BIOEN BIGEN "
          "CONSE CWENE CANTE CATES ARASE ECOGR ENDAE ENJSA ENERY ESEN GWIND HUNER ENTRA "
          "IZENR KLYPV LYDYE MAGEN MASFN METEN MOGAN NTGAZ NATEN ODAS PAMEL SMRTG TATEN "
          "VEYAS ZEDUR ZOREN").split()
EK = "ASTOR ALARK EUPWR GESAN".split()
ENDEKS = "XELKT XU030 XU100 XUTUM XUHIZ".split()
VADELI = "AKSEN1! ENJSA1! ODAS1! ASTOR1! ALARK1! XU030D1!".split()

def tur(kod):
    if kod in ENDEKS: return "endeks"
    if kod in VADELI: return "vadeli"
    return "xelkt_uyesi" if kod in UYELER else "ek_pay"

def cek(kod):
    url = "https://www.tradingview.com/symbols/BIST-%s/" % urllib.parse.quote(kod, safe="!")
    p = subprocess.run(["curl", "-s", "-L", "--max-time", "40", "-A", "Mozilla/5.0",
                        "-w", "\n__HTTP__%{http_code}", url],
                       capture_output=True, timeout=60)
    govde = p.stdout.decode("utf-8", "replace")
    m = re.search(r"\n__HTTP__(\d{3})$", govde)
    http = m.group(1) if m else "000"
    t = re.search(r"<title[^>]*>(.*?)</title>", govde, re.S)
    baslik = html.unescape(t.group(1)).strip() if t else ""
    baslik = re.sub(r"[\r\n,;]+", " ", baslik)[:160]
    a = re.search(r'"short_description":"([^"]{1,80})"', govde)
    ad = re.sub(r"[\r\n,;]+", " ", a.group(1)) if a else ""
    kanonik = ('<link rel="canonical" href="%s"' % url) in govde
    pro = ('"pro_symbol":"BIST:%s"' % kod) in govde
    return url, http, baslik, ad, kanonik, pro

def main(cikti):
    satirlar = []
    for kod in UYELER + EK + ENDEKS + VADELI:
        tv = "BIST:" + kod
        http, baslik, hata, ad, kanonik, pro = "000", "", "", "", False, False
        for deneme in range(2):          # en cok 1 yeniden deneme
            try:
                url, http, baslik, ad, kanonik, pro = cek(kod)
            except Exception as e:        # noqa
                hata = type(e).__name__
            if http in ("200", "404"):
                break
            time.sleep(5)
        # dogrulama: 200 + sayfa bulundu + (baslikta BIST:KOD  ya da  kanonik URL ve govdede pro_symbol ayni kod)
        ok = http == "200" and "Page not found" not in baslik and (tv in baslik or (kanonik and pro))
        notu = tur(kod)
        if http == "404": notu += "; sayfa yok"
        elif http != "200": notu += "; erisim hatasi " + hata
        elif not ok: notu += "; baslikta/govdede kod yok"
        elif tv not in baslik: notu += "; baslik bicimi farkli - kanonik URL ve pro_symbol ile dogrulandi"
        if ad: notu += "; tv_adi=" + ad
        satirlar.append([kod, tv, http, baslik, "evet" if ok else "hayır", notu])
        print(kod, http, "evet" if ok else "HAYIR", baslik[:70], flush=True)
        time.sleep(1.5)
    with open(cikti, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["kod", "tv_kodu", "http", "sayfa_basligi", "dogrulandi", "not"])
        w.writerows(satirlar)
    print("TOPLAM", len(satirlar), "dogrulanan", sum(r[4] == "evet" for r in satirlar))

if __name__ == "__main__":
    main(sys.argv[1])
