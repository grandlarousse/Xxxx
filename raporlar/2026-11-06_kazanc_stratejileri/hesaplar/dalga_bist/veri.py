"""Veri yükleme, temizlik, küme endeksleri, TL risksiz faiz.
- Fiyatlar: İş Yatırım ChartData düzeltilmiş kapanış (temettü/bedelsiz düzeltmeli). XU100 FİYAT endeksi (temettüsüz):
  hisseler/kümeler XU100'e karşı yılda ~2-4 puan temettü avantajlı görünür (not edildi).
- Takvim: XU100 işlem günleri. Üye fiyatı en çok 5 gün ileri taşınır (askı). Halka arzdan sonraki ilk 20 gün dışlanır.
- Şüpheli günlük getiri |r|>%35 (BIST marj limiti %10, 2015 öncesi %20): o gün 0 yapılır ve listelenir.
- Küme getirisi: mevcut üyelerin günlük getirilerinin eşit ağırlıklı ortalaması (günlük yeniden dengeleme yaklaşımı).
- TL rf: TCMB politika/ortalama fonlama faizine yakın elle kurulmuş adım fonksiyonu (yıllık, basit->günlük bileşik)."""
import os, sys, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kumeler import KUMELER, ENDEKSLER
BASE = "/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/data/dalga_bist/d"
IPO_DISLA = 20
# (yürürlük tarihi, yıllık %) yaklaşık TCMB ortalama fonlama / politika faizi
RF_ADIM = [("2009-06-01", 8.25), ("2009-11-20", 6.5), ("2010-05-18", 7.0), ("2011-01-21", 6.25), ("2011-08-05", 6.0),
           ("2011-10-21", 9.5), ("2012-01-02", 10.5), ("2012-04-01", 9.0), ("2012-07-01", 7.0), ("2012-10-01", 5.6),
           ("2013-05-17", 5.0), ("2013-07-24", 6.8), ("2014-01-29", 10.0), ("2014-05-23", 9.5), ("2014-07-18", 8.5),
           ("2015-01-21", 7.8), ("2015-07-01", 8.7), ("2016-03-25", 8.5), ("2016-07-01", 8.3), ("2017-01-13", 9.5),
           ("2017-02-15", 11.0), ("2017-05-01", 11.9), ("2017-12-01", 12.75), ("2018-05-23", 16.5), ("2018-06-08", 17.75),
           ("2018-08-14", 19.25), ("2018-09-14", 24.0), ("2019-07-26", 19.75), ("2019-09-13", 16.5), ("2019-10-25", 14.0),
           ("2019-12-13", 12.0), ("2020-01-17", 11.25), ("2020-02-20", 10.75), ("2020-03-18", 9.75), ("2020-04-23", 8.75),
           ("2020-05-22", 8.25), ("2020-08-15", 10.5), ("2020-09-25", 11.5), ("2020-11-20", 15.0), ("2020-12-25", 17.0),
           ("2021-03-19", 19.0), ("2021-09-24", 18.0), ("2021-10-22", 16.0), ("2021-11-19", 15.0), ("2021-12-17", 14.0),
           ("2022-08-19", 13.0), ("2022-09-23", 12.0), ("2022-10-21", 10.5), ("2022-11-25", 9.0), ("2023-02-24", 8.5),
           ("2023-06-23", 15.0), ("2023-07-21", 17.5), ("2023-08-25", 25.0), ("2023-09-22", 30.0), ("2023-10-27", 35.0),
           ("2023-11-24", 40.0), ("2023-12-22", 42.5), ("2024-01-26", 45.0), ("2024-03-22", 50.0), ("2024-12-27", 47.5),
           ("2025-01-24", 45.0), ("2025-03-07", 42.5), ("2025-03-24", 46.0), ("2025-07-25", 43.0), ("2025-09-12", 40.5),
           ("2025-10-24", 39.5), ("2025-12-12", 38.0), ("2026-01-23", 37.0), ("2026-06-12", 36.0)]
def yukle(kod):
    p = os.path.join(BASE, kod + ".csv")
    if not os.path.exists(p): return None
    d = pd.read_csv(p, parse_dates=["ldate"]).set_index("ldate")["px"]
    d = d[d > 0]
    return d[~d.index.duplicated(keep="last")]
def panel(son_tarih=None):
    xu = yukle("XU100"); cal = xu.index
    if son_tarih is not None: cal = cal[cal <= pd.Timestamp(son_tarih)]
    kodlar = sorted({k for v in KUMELER.values() for k in v})
    px = {}
    for k in kodlar + ENDEKSLER + ["USDTRY"]:
        s = yukle(k)
        if s is None or len(s) < 30: continue
        s = s.reindex(s.index.union(cal)).ffill(limit=5).reindex(cal)
        # ilk geçerli tarihten önce NaN kalsın
        px[k] = s
    P = pd.DataFrame(px)
    R = P.pct_change(fill_method=None)
    supheli = []
    for k in kodlar:
        if k not in R: continue
        m = R[k].abs() > 0.35
        for d in R.index[m]: supheli.append((k, d.date(), round(R.at[d, k], 3)))
        R.loc[m, k] = 0.0
        fv = P[k].first_valid_index()
        if fv is not None and fv > cal[0] + pd.Timedelta(days=10):  # sonradan listelenen
            i = cal.get_loc(fv); R.loc[cal[:min(i + IPO_DISLA, len(cal))], k] = np.nan
    return P, R, supheli
def kume_getiri(R, uyeler=None, min_uye=1):
    out = {}; nu = {}
    for c, m in (uyeler or KUMELER).items():
        m = [x for x in m if x in R]
        x = R[m]; n = x.notna().sum(axis=1)
        out[c] = x.mean(axis=1).where(n >= min_uye); nu[c] = n
    return pd.DataFrame(out), pd.DataFrame(nu)
def rf_gunluk(cal):
    s = pd.Series({pd.Timestamp(a): b for a, b in RF_ADIM}).sort_index()
    yil = s.reindex(s.index.union(cal)).ffill().reindex(cal) / 100.0
    return (1 + yil) ** (1 / 252.0) - 1, yil
