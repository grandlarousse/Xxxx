"""Hisse bölünmeleri (Yahoo) -> veri/bolunme.csv (kod, tarih, oran). Amaç: madde 2.2'deki
'fiyat >= 3 $' koşulunu o günkü GERÇEK (bölünmeden arındırılmamış) fiyatla sınamak; Yahoo 'Close'
bölünmeye göre geriye dönük düzeltilmiştir. Kullanım: python kod/bolunme_indir.py"""
import sys, time
from pathlib import Path
import pandas as pd
import yfinance as yf
sys.path.insert(0, str(Path(__file__).parent))
from indir import HEDEF, ETF
rows = []
for k in HEDEF + ETF:
    for i in range(5):
        try:
            s = yf.Ticker(k).splits
            break
        except Exception as e:
            s = None; time.sleep(2 * (i + 1))
    if s is None:
        print(k, "indirilemedi"); continue
    for t, v in s.items():
        rows.append((k, pd.Timestamp(t).tz_localize(None).normalize().date(), float(v)))
pd.DataFrame(rows, columns=["kod", "tarih", "oran"]).to_csv(Path(__file__).resolve().parents[1] / "veri" / "bolunme.csv", index=False)
print(len(rows), "bölünme")
