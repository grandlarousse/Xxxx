"""Bilanço duyuru tarihleri ve saatleri (Yahoo, yfinance Ticker.get_earnings_dates).

Kullanım: python kod/bilanco_indir.py [KOD ...]   (varsayılan: indir.HEDEF, yani Ç + YENİ hisseler)
Çıktı: veri/bilanco/<KOD>.csv  sütunlar: tarih (ET yerel gün), saat (HH:MM ET), zaman
       (sonra = 16:00 ve sonrası, once = 09:30 öncesi, seans = 09:30-16:00, bilinmiyor = 00:00 ya da yok),
       eps_tahmin, eps_gercek, surpriz_yuzde
       veri/bilanco/kapsam.csv : kod başına ilk/son tarih, adet, saat bilgisi oranı.
Tepki günü bu dosyada HESAPLANMAZ; ortak.bilanco() hesaplar (madde 2.4).
"""
import sys, time
from pathlib import Path
import pandas as pd
import yfinance as yf

sys.path.insert(0, str(Path(__file__).parent))
from indir import HEDEF

OUT = Path(__file__).resolve().parents[1] / "veri" / "bilanco"


def zaman_sinifi(ts):
    if ts.hour == 0 and ts.minute == 0:
        return "bilinmiyor"
    m = ts.hour * 60 + ts.minute
    return "sonra" if m >= 16 * 60 else ("once" if m < 9 * 60 + 30 else "seans")


def indir(kod, deneme=5):
    for i in range(deneme):
        try:
            d = yf.Ticker(kod).get_earnings_dates(limit=100)
            return d
        except Exception as e:
            son = e
            time.sleep(2 * (i + 1))
    print(f"  {kod}: indirilemedi: {son}")
    return None


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    kodlar = sys.argv[1:] or HEDEF
    kapsam = {}
    for k in kodlar:
        d = indir(k)
        if d is None or d.empty:
            kapsam[k] = dict(ilk=None, son=None, adet=0, adet_gecmis=0, saat_orani=None, not_="BOŞ")
            continue
        idx = d.index.tz_convert("America/New_York") if d.index.tz is not None else d.index
        df = pd.DataFrame({"tarih": idx.tz_localize(None).normalize(), "saat": idx.strftime("%H:%M"),
                           "zaman": [zaman_sinifi(t) for t in idx],
                           "eps_tahmin": d["EPS Estimate"].values, "eps_gercek": d["Reported EPS"].values,
                           "surpriz_yuzde": d["Surprise(%)"].values})
        df = df.sort_values(["tarih", "eps_gercek"]).drop_duplicates("tarih", keep="last").reset_index(drop=True)
        df.to_csv(OUT / f"{k}.csv", index=False)
        g = df[df.tarih <= "2026-11-20"]
        kapsam[k] = dict(ilk=str(g.tarih.min())[:10] if len(g) else None, son=str(g.tarih.max())[:10] if len(g) else None,
                         adet=len(df), adet_gecmis=len(g),
                         saat_orani=round((g.zaman != "bilinmiyor").mean(), 3) if len(g) else None,
                         n_once=int((g.zaman == "once").sum()), n_sonra=int((g.zaman == "sonra").sum()),
                         n_seans=int((g.zaman == "seans").sum()), not_="")
        print(k, kapsam[k], flush=True)
        time.sleep(0.5)
    pd.DataFrame(kapsam).T.to_csv(OUT / "kapsam.csv")


if __name__ == "__main__":
    main()
