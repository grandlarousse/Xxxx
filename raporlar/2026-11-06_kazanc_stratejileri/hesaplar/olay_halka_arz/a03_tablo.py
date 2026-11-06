"""Adım 3: halkarz.com detay satırlarını (WebFetch ile sayfadan birebir alınan alanlar, raw_web/detay_satirlar.txt)
halka arz tablosuna çevirir -> out/ipo_tablo.csv
Alan sırası: kod | arz tarihi | fiyat | dağıtım | pay lot | ek pay lot | pazar | ilk işlem | büyüklük | fiili dolaşım |
             bireysel kişi | bireysel lot | toplam kişi | dağıtılan pay satırı | satmama taahhüdü | fiyat istikrarı | iskonto
Not: halkarz.com python-requests isteğine 403 verdi; tarama durduruldu, sayfalar WebFetch aracıyla tek tek okundu.
Fiyat aralığı verilen 9 arzın nihai fiyatı haber/aracı kurum kaynaklarından veya ilk gün fiyat limitinden çıkarıldı (FIYAT_DUZELT)."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
from common import RAW_WEB, OUT

AY = {"ocak": 1, "şubat": 2, "mart": 3, "nisan": 4, "mayıs": 5, "haziran": 6, "temmuz": 7, "ağustos": 8,
      "eylül": 9, "ekim": 10, "kasım": 11, "aralık": 12}
# nihai fiyat: (fiyat, kaynak)
FIYAT_DUZELT = {
    "ARZUM": (17.00, "BIST duyurusu/haber: aralık üstü 17,00"),
    "KRVGD": (9.00, "Midas/haber: 9,00"),
    "AYDEM": (9.90, "şirket sonuç bülteni: 9,90"),
    "BIOEN": (18.00, "haber: nihai 18,00"),
    "PENTA": (32.00, "haber: aralık altı 32,00"),
    "KLKIM": (14.75, "çıkarım: ilk gün max 16,22 = 14,75x1,10"),
    "MERCN": (8.81, "çıkarım: ilk gün max 9,69 = 8,81x1,10"),
    "ANGEN": (22.50, "çıkarım: ilk gün max 24,74 = 22,50x1,10"),
    "HTTBT": (12.25, "çıkarım: ilk gün max 13,47 = 12,25x1,10"),
}
HARIC = {"BEWEN": "ertelendi", "ENPRA": "kısmi bölünme (PÖİP), arz değil", "MARMR": "kısmi bölünme, arz değil",
         "ERCB": "arz bilgisi yok (doğrudan kotasyon)", "GMTAS": "talep toplama yok (aynı gün işlem), arz verisi yok",
         "DMLKT": "gayrimenkul sertifikası, pay değil"}


def num(s):
    """'45.830.000' -> 45830000 ; '16,93' -> 16.93 ; '16.93' -> 16.93"""
    if s is None:
        return None
    s = str(s).strip().replace("Lot", "").replace("TL", "").replace("%", "").replace("～", "").replace("~", "").strip().rstrip(".")
    if s in ("", "NA"):
        return None
    m = re.search(r"[\d.,]+", s)
    if not m:
        return None
    t = m.group(0).rstrip(".,")
    if "," in t:
        t = t.replace(".", "").replace(",", ".")
    elif t.count(".") >= 2 or re.fullmatch(r"\d{1,3}(\.\d{3})+", t):
        t = t.replace(".", "")
    try:
        return float(t)
    except ValueError:
        return None


def size_tl(s):
    if not s or s == "NA":
        return None
    v = num(s)
    if v is None:
        return None
    s2 = s.lower()
    if "milyar" in s2:
        return v * 1e9
    if "milyon" in s2:
        return v * 1e6
    return None


def trdate(s):
    if not s or s == "NA":
        return pd.NaT
    m = re.search(r"(\d{1,2})\s+([A-Za-zÇĞİÖŞÜçğıöşü]+)\s+(\d{4})", s)
    if not m:
        return pd.NaT
    ay = AY.get(m.group(2).lower().replace("i̇", "i"))
    return pd.Timestamp(int(m.group(3)), ay, int(m.group(1))) if ay else pd.NaT


def lockup_days(s):
    """Ortaklar için satmama süresi (gün). Yoksa None."""
    if not s or s == "NA":
        return None
    parts = [p for p in s.split(";") if "rtak" in p]
    p = parts[0] if parts else s
    m = re.search(r"(\d+)\s*(Yıl|Ay|Gün)", p, flags=re.I)
    if not m:
        return None
    n = int(m.group(1)); u = m.group(2).lower()
    return n * 365 if u.startswith("y") else (n * 30 if u.startswith("a") else n)


def main():
    yil = {l.split("|")[1]: int(l.split("|")[0]) for l in open(os.path.join(RAW_WEB, "liste_yillar.txt"), encoding="utf-8") if l.strip()}
    rows = []
    for l in open(os.path.join(RAW_WEB, "detay_satirlar.txt"), encoding="utf-8"):
        f = [x.strip() for x in l.rstrip("\n").split(" | ")]
        if len(f) < 17:
            print("kısa satır", f[:2]); continue
        kod = f[0]
        fiyat_txt = f[2]
        fiyat = num(fiyat_txt) if "-" not in fiyat_txt.replace(" - ", "-") or fiyat_txt == "NA" else None
        kaynak = "halkarz.com"
        if kod in FIYAT_DUZELT:
            fiyat, kaynak = FIYAT_DUZELT[kod]
        yontem = "Eşit" if "Eşit" in f[3] else ("Oransal" if "Oransal" in f[3] else "NA")
        r = dict(kod=kod, arz_yili=yil.get(kod), arz_tarihi_txt=f[1], fiyat=fiyat, fiyat_kaynak=kaynak, dagitim=yontem,
                 pay_lot=num(f[4]), ek_pay_lot=num(f[5]) or 0.0, pazar=f[6], ilk_islem_hz=trdate(f[7]),
                 buyukluk_txt=f[8], buyukluk_tl_hz=size_tl(f[8]), fiili_dolasim=num(f[9]),
                 bireysel_kisi=num(f[10]), bireysel_lot=num(f[11]), toplam_kisi=num(f[12]), dagitilan_txt=f[13],
                 satmama_txt=f[14], lockup_gun=lockup_days(f[14]), fiyat_istikrari=f[15], iskonto=num(f[16]),
                 haric=HARIC.get(kod, ""))
        rows.append(r)
    df = pd.DataFrame(rows)
    df["buyukluk_tl"] = df["fiyat"] * (df["pay_lot"] + df["ek_pay_lot"])  # tutarlı tanım: ek satış dahil üst sınır
    df["buyukluk_tl"] = df["buyukluk_tl_hz"].fillna(df["buyukluk_tl"])
    df["lot_kisi"] = df["bireysel_lot"] / df["bireysel_kisi"]
    df["tl_kisi"] = df["lot_kisi"] * df["fiyat"]
    fi = df["fiyat_istikrari"].fillna("NA").str.lower()
    df["istikrar"] = ~(fi.str.startswith("planlanm") | (fi == "na"))
    df["lockup_varsayim"] = df["lockup_gun"].isna()
    df["lockup_gun"] = df["lockup_gun"].fillna(365)
    df.to_csv(os.path.join(OUT, "ipo_tablo.csv"), index=False)
    print(df.shape, "hariç:", (df.haric != "").sum())
    print(df.groupby("arz_yili").agg(n=("kod", "size"), esit=("dagitim", lambda x: (x == "Eşit").mean()),
                                    kisi_med=("bireysel_kisi", "median"), tl_kisi_med=("tl_kisi", "median"),
                                    buyuk_med=("buyukluk_tl", "median")))
    print(df[df.fiyat.isna() | df.ilk_islem_hz.isna()][["kod", "fiyat", "ilk_islem_hz", "haric"]])


if __name__ == "__main__":
    main()
