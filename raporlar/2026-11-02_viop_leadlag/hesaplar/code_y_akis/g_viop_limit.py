"""Spot tavan/taban kapanışı günlerinde VİOP pay vadelisi (en yakın vade) spot limitini aşıyor mu? Aşıyorsa 'limit yüzünden fiyatlanamayan bilgi' vadelide görünür
ve ertesi gün spot gap'ini öngörür mü? Veri: data/viop/viop_YYYYMMDD.csv (BIST VİOP günlük bülteni; başka ajan indirdi). 2020-03+ (P10 rejimi) günleri.
Ölçü: fut_prem = log(F_kapanış/F_önceki_uzlaşma) - log(S_kapanış/S_önceki_kapanış) (vadeli günlük değişim - spot günlük değişim)."""
import numpy as np, pandas as pd, os, glob, alib
VD = alib.SCR + '/data/viop'
E = pd.read_parquet('res_limit_events.parquet'); E = E[(E.reg == 'P10') & E.viop & (E.TC | E.BC)].copy()
dates = sorted(E.date.unique())
rows = []
for d in dates:
    f = f"{VD}/viop_{pd.Timestamp(d).strftime('%Y%m%d')}.csv"
    if not os.path.exists(f): continue
    try:
        B = pd.read_csv(f, sep=';', encoding='windows-1254', skiprows=[1], dtype=str)
    except Exception: continue
    B.columns = [c.strip() for c in B.columns]
    B = B[B['SOZLESME KODU'].str.startswith('F_') & (B['PAZAR SEGMENTI'].str.strip() == 'SSF')] if 'PAZAR SEGMENTI' in B else B[B['SOZLESME KODU'].str.startswith('F_')]
    for c in ['UZLASMA FIYATI', 'ONCEKI UZLASMA FIYATI', 'KAPANIS FIYATI', 'EN YUKSEK FIYAT', 'EN DUSUK FIYAT', 'ISLEM MIKTARI', 'UZLASMA FIYATI DEGISIMI (%)']:
        B[c] = pd.to_numeric(B[c].str.replace(',', '.'), errors='coerce')
    B['und'] = B['DAYANAK VARLIK'].str.replace('.E', '', regex=False).str.strip()
    B['vade'] = pd.to_datetime(B['VADE TARIHI'], errors='coerce')
    B = B.sort_values('vade').groupby('und').head(1)  # en yakın vade
    for _, e in E[E.date == d].iterrows():
        b = B[B.und == e.stock]
        if not len(b): continue
        b = b.iloc[0]
        rows.append(dict(date=d, stock=e.stock, cls='TC' if e.TC else 'BC', locked=bool(e.TCL or e.BCL), spot_R=e.R, fut_settle_chg=b['UZLASMA FIYATI'] / b['ONCEKI UZLASMA FIYATI'],
                         fut_high_chg=b['EN YUKSEK FIYAT'] / b['ONCEKI UZLASMA FIYATI'], fut_low_chg=b['EN DUSUK FIYAT'] / b['ONCEKI UZLASMA FIYATI'], fut_vol=b['ISLEM MIKTARI'],
                         gap1=e.gap1, intra1=e.intra1, cc1=e.cc1))
V = pd.DataFrame(rows); V.to_csv('res_viop_limit.csv', index=False)
print('olay', len(V), 'tarih aralığı', V.date.min() if len(V) else None, V.date.max() if len(V) else None)
if len(V):
    V['prem'] = np.log(V.fut_settle_chg) - np.log(V.spot_R)
    print('Vadeli uzlaşma değişimi dağılımı (TC):', V[V.cls == 'TC'].fut_settle_chg.describe().round(4).to_dict())
    print('Vadeli en yüksek / önceki uzlaşma (TC) maks:', V[V.cls == 'TC'].fut_high_chg.max(), ' BC en düşük min:', V[V.cls == 'BC'].fut_low_chg.min())
    for cls in ['TC', 'BC']:
        s = V[V.cls == cls].dropna(subset=['prem', 'gap1'])
        print(cls, 'n', len(s), 'corr(prem, gap1)=%.3f corr(prem, cc1)=%.3f  ort prem %.1f bps' % (s.prem.corr(s.gap1), s.prem.corr(s.cc1), 1e4 * s.prem.mean()))
        hi = s[s.prem > s.prem.median()]; lo = s[s.prem <= s.prem.median()]
        print('   prem yüksek yarı gap1 %.0f bps / düşük yarı %.0f bps' % (1e4 * hi.gap1.mean(), 1e4 * lo.gap1.mean()))
