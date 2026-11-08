"""Aile ajanlarının izleme kararlarını denetçi itirazlarıyla uzlaştırır (ana ajan kararı).
İlke: denetçi daha temkinli bir karar önerdiyse o uygulanır; kopya/likiditesiz/düşük oynaklıklı ürünler elenir.
Kademe: A = denetimden geçmiş (doğrulandı) kuralın sinyal/işlem aracı; B = yalnız 'zayıf' kuralı olan; C = kural yok, sürücüyle takip.
Çıktı: sonuclar/izleme_son.csv (aile, sym, karar, kademe, not)"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)

OVR = {  # (aile, sym): (yeni karar, not)
    ("abd_endeks", "RSP"): ("red", "Denetçi: SPY ile aynı sivri tepe; bağımsız değer yok."),
    ("abd_endeks", "DIA"): ("red", "Denetçi: SPY ile 0,84 korelasyon, daha az likit; bağımsız değer yok."),
    ("abd_endeks", "IWM"): ("yedek", "Kendi sinyali gürültü; yalnız küçük şirket izlemesi (CME_MINI:RTY1!)."),
    ("abd_endeks", "SPXL"): ("yedek", "3x: pozisyon dayanak eşdeğerinin en çok 1/3'ü."),
    ("abd_endeks", "TQQQ"): ("yedek", "3x: QQQ sinyalinin aracı; tek işlemde -%31 görüldü; küçük pay."),
    ("sektor_tematik", "SOXL"): ("yedek", "Koşullu: Midas bulunurluğu doğrulanmadı; risk eşdeğerinde SMH'ye üstünlüğü yok; 1 günden uzun tutma."),
    ("sektor_tematik", "XLK"): ("red", "Denetçi: IBS kuralı OOS ~5 bp, SMH ile 0,94 korelasyon."),
    ("sektor_tematik", "IGV"): ("red", "Denetçi: negatif gecikme SPY kontrolüyle kayboluyor; kural maliyet altında."),
    ("sektor_tematik", "XOP"): ("red", "Enerji ailesinde kartı var (kopya kayıt)."),
    ("sektor_tematik", "COPX"): ("red", "Metal ailesinde kartı var (kopya kayıt)."),
    ("tek_hisse_kaldiracli", "AAPU"): ("yedek", "Denetçi: S1'in en zayıf dayanağı."),
    ("tek_hisse_kaldiracli", "METU"): ("yedek", "Denetçi: gerçek ETF'te S1 negatif; geçmiş kısa."),
    ("enerji_tarim", "USO"): ("yedek", "PTP %10 kesinti riski teyit edilene kadar referans/izleme; S2 zayıf."),
    ("enerji_tarim", "KOLD"): ("yedek", "Koşullu: S1 zayıf; PTP; Midas'ta doğrulanmadı."),
    ("enerji_tarim", "BOIL"): ("red", "Long stratejisi yok, koşulsuz bozulma -36 bp/gün, EIA günü -66 bp; yalnız 'kaçın' kuralı."),
    ("enerji_tarim", "XOP"): ("kabul", "Denetçi: PTP'siz, XLE kadar uygun 1-3 günlük enerji aracı."),
    ("metal_madenci", "SLV"): ("yedek", "Strateji/öncü yok; COMEX:SI1! ile izlenir; 30.01.2026'da tek gün -%28,5."),
    ("metal_madenci", "COPX"): ("yedek", "Strateji yok; COMEX:HG1! ile izlenir."),
    ("tahvil_doviz", "TMV"): ("yedek", "S1 örneklem öncesinde çalışmıyor; -3x; Midas doğrulanmadı."),
    ("tahvil_doviz", "TLT"): ("kabul", "Uzun vade faiz izleme aracı ve TMV/TBT/TMF dayanağı (kural yok)."),
    ("volatilite", "SVIX"): ("red", "Denetçi: kanıt yalnız 2022+, -1x yapı Şubat 2018 tipi olayda ~%90+ kayıp."),
    ("volatilite", "SVXY"): ("kabul", "Koşullu: Midas'ta sembol ve PTP %10 kesintisi yoksa; aksi halde yalnız sinyal kaynağı."),
    ("volatilite", "VXX"): ("yedek", "İşlem adayı değil; yalnız koruma (1-3 günlük hiçbir long kural pozitif değil)."),
    ("kripto", "SBIT"): ("yedek", "S1 çürütüldü; yalnız kısa BTC görüşü için araç."),
    ("kripto", "GBTC"): ("kabul", "Midas'ta sembol sayfası doğrulanmış spot BTC ETF'i; IBIT ile eş birincil."),
    ("kripto", "ETHE"): ("kabul", "Midas'ta sembol sayfası doğrulanmış spot ETH ETF'i; ETHA ile eş birincil."),
    ("uluslararasi", "EWJ"): ("yedek", "Tek başına S1 t 1,21, OOS +5 bp."),
    ("uluslararasi", "EFA"): ("red", "Günlük oynaklık 104 bp, maliyet/oynaklık 0,125; strateji/öncü yok."),
    ("uluslararasi", "VGK"): ("red", "Günlük oynaklık 105 bp, maliyet/oynaklık 0,13; strateji/öncü yok."),
}

KAD_OVR = {"SOXX": "A",   # SMH IBS sinyalinin kopya aracı (son kontrol: C0 44 bp, t 3,7)
           "KORU": "B",   # EWY IBS sinyalinin 3x aracı
           "IBIT": "C", "GBTC": "C", "FBTC": "C", "ETHA": "C"}   # kripto_S2 strateji değil, zayıf rejim filtresi (IBIT'te t 0,6)

def main():
    rows = []
    for f in ["abd_endeks", "sektor_tematik", "tek_hisse_kaldiracli", "enerji_tarim", "metal_madenci", "tahvil_doviz", "volatilite", "kripto", "uluslararasi"]:
        r = json.load(open(os.path.join(ROOT, "sonuclar", f"aile_{f}", "sonuc.json")))
        d = json.load(open(os.path.join(ROOT, "sonuclar", f"aile_{f}", "denetim.json")))
        ver = {s["id"]: s["karar"] for s in d["stratejiler"]}
        tools = {}
        for s in r["stratejiler"]:
            k = ver.get(s["id"])
            if k == "curutuldu": continue
            for x in (s.get("islem_etf") or []) + [s.get("sinyal_etf") or ""]:
                sym = x.split(" ")[0].split("/")[0].replace("AMEX:", "").replace("NASDAQ:", "").upper()
                if sym: tools.setdefault(sym, set()).add(k)
        for x in r["izleme"]:
            sym = x["sym"].upper(); karar, note = x["karar"], ""
            if (f, sym) in OVR: karar, note = OVR[(f, sym)]
            ks = tools.get(sym, set())
            kad = "A" if "dogrulandi" in ks else ("B" if "zayif" in ks else "C")
            kad = KAD_OVR.get(sym, kad)
            rows.append({"aile": f, "sym": sym, "ajan_karar": x["karar"], "karar": karar, "kademe": kad, "not": note})
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(ROOT, "sonuclar", "izleme_son.csv"), index=False)
    v = df[df.karar.isin(["kabul", "yedek"])]
    print(v.groupby(["karar", "kademe"]).size())
    for k in ["A", "B", "C"]:
        print(k, sorted(v[v.kademe == k].sym.unique()))

if __name__ == "__main__":
    main()
