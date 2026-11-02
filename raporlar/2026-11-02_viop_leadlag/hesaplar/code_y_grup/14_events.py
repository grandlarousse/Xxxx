"""Olay çalışması: 2024-2026 ortaklık/grup olayları. AR = r - b*XU100 (b: [-250,-30] gün). Gün 0 = duyurunun ilk işlem günü (akşam duyurusu -> ertesi gün).
UYARI: tek olay, n=1 -> istatistiksel çıkarım yok; t = AR/sd(tahmin penceresi artıkları)."""
from gx import *
EV = [('2024-08-20', 'Koza grubu Hazine payları TVF\'ye devri (RG)', ['TRALT', 'TRMET', 'TRENJ']),
      ('2024-11-21', 'Koza grubu birleşme kararı (KAP 20.11 akşam?)', ['TRALT', 'TRMET', 'TRENJ']),
      ('2025-07-28', 'Koza birleşmesi sonlandırıldı (25.07 akşam)', ['TRALT', 'TRMET', 'TRENJ']),
      ('2026-06-02', 'Can Kültür-OYAK Tekfen satış görüşmesi (2/9 Haz.)', ['TKFEN', 'OYAKC', 'EREGL']),
      ('2026-06-09', 'Can Kültür-OYAK görüşme açıklaması (alternatif tarih)', ['TKFEN', 'OYAKC', 'EREGL']),
      ('2026-06-26', 'ARY Holding %32 -> Libco', ['TKFEN']),
      ('2026-07-24', 'Tekfen %42,8 OYAK/ON Investment devri tamam', ['TKFEN', 'OYAKC', 'EREGL']),
      ('2026-06-29', 'Zorlu/Vestel finansal yeniden yapılandırma başvurusu', ['VESTL', 'VESBE', 'ZOREN']),
      ('2026-08-07', 'Alarko Holding Carrier %42 payını devralıyor (7 Ağu)', ['ALARK', 'ALCAR']),
      ('2026-08-10', 'Alarko-Carrier (ilk iş günü alternatifi)', ['ALARK', 'ALCAR']),
      ('2026-09-16', 'Fon krizi Tera Portföy\'e sıçradı / 17.09 SPK tasfiye', ['TERA', 'TEHOL', 'PEKGY', 'ISMEN', 'GLYHO']),
      ('2026-10-14', 'Hektaş: OYAK\'a bedelli pay, oy %50,95', ['HEKTS', 'EREGL', 'OYAKC'])]
m = R('XU100'); rows = []
for d, desc, syms in EV:
    d0 = pd.Timestamp(d)
    for s in syms:
        r = R(s); df = pd.concat([r.rename('r'), m.rename('m')], axis=1).dropna()
        if d0 not in df.index:
            nxt = df.index[df.index >= d0]
            if not len(nxt): continue
            d0_ = nxt[0]
        else: d0_ = d0
        k = df.index.get_loc(d0_)
        est = df.iloc[max(0, k - 250):k - 30]
        if len(est) < 60: continue
        b = np.polyfit(est.m, est.r, 1); res = est.r - np.polyval(b, est.m); sd = res.std()
        ar = df.r - np.polyval(b, df.m)
        g = lambda a, c: ar.iloc[k + a:k + c + 1].sum()
        rows.append(dict(date=d0_.date(), event=desc, sym=s, AR0=100 * ar.iloc[k], t0=ar.iloc[k] / sd, CAR_m5_m1=100 * g(-5, -1), CAR_0_1=100 * g(0, 1), CAR_2_10=100 * g(2, 10), t_2_10=g(2, 10) / (sd * 3), CAR_0_20=100 * g(0, 20)))
E = pd.DataFrame(rows); E.to_csv(HERE + '/res_events.csv', index=False)
pd.set_option('display.width', 220); pd.set_option('display.max_colwidth', 60)
print(E.round(2).to_string())
