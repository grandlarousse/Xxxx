# Günlük veri paneli (2005-01-03 → 2026-11-20)

## Yeniden üretim (sırayla; indirilen dosyaları okuyan her şey `python3 -I`)
```
H=/tmp/claude-0/-home-user-Xxxx/b23916bf-451a-5d36-8905-d1866417ce1f/scratchpad/ham
P=/tmp/claude-0/-home-user-Xxxx/b23916bf-451a-5d36-8905-d1866417ce1f/scratchpad/panel
V=/home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/veri
cd /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/kod
python3 -I veri_indir.py $H            # Yahoo chart API ham JSON (var olanı atlar, atomik yazar)
python3 -I panel_kur.py $H $P $V       # panel/*.pkl + evren.csv + veri_kalite.csv
python3 -I bilanco.py $H $V/bilanco_tarihleri.csv   # SEC EDGAR 8-K Item 2.02
curl -s -A "Mozilla/5.0" -o $V/dix_gex.csv https://squeezemetrics.com/monitor/static/DIX.csv
```
- `evren_tanim.py`: gruplar, kaldıraç/dayanak tablosu, kapanış sınıfı, tür, `YENI_KOD` (BITF→KEEL).
- pyarrow yok → panel pandas pickle (`open/high/low/close/adjclose/volume.pkl`).

## Yükleme
```python
import sys; sys.path.insert(0, "/home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/kod")
from yukle import panel, bilanco, dix_gex, kalite
P = panel()                       # dict: open high low close adjclose adjopen volume evren
r = P["adjclose"].pct_change(fill_method=None)   # ileri doldurma yok; NaN'ı kendin ele al
```
Panel dizini başka yerdeyse `PANEL_DIZIN` ortam değişkeni ya da `panel(dizin)`.

## Tanımlar
- Satır = SPY'ın Yahoo veri günleri (5.507 NYSE günü). Sütun = 470 kod (BITF yerine KEEL).
- Tarih = borsanın yerel takvim tarihi (Tokyo, Londra, UTC kripto vb.); o tarihte veri yoksa NaN. İleri doldurma yok.
- close/open/high/low/volume: Yahoo bölünmeye göre düzeltilmiş, temettüye göre düzeltilmemiş. adjclose: temettü+bölünme. adjopen = open × adjclose/close.
- kapanis_sinifi: ABD16 (16:00 ET), ONCE (ABD kapanışından önce kapananlar + CBOE faiz endeksleri), VIX1615 (16:15 ET), SONRA (kripto, döviz, vadeli, ^BVSP, ^MOVE).
- maliyet_bps: tek yön, adv60 (son 60 gün ort. close×volume; kriptoda volume zaten USD) eşiklerine göre; kaldıraç≠1 ise +1. Endeks ve döviz: NaN (doğrudan işlem görmez).
- kaldirac: TSLQ şu an −2 (2024 ortasına kadar −1), TSLL/CONL/NVDL 2024 başına kadar 1,5×; evren tablosundaki değer güncel kaldıraçtır.

## Bilanço tarihleri
- 8-K ve items içinde 2.02. acceptanceDateTime gerçekten UTC ('Z'); NVDA ile doğrulandı (21:20Z kışın = 16:20 ET).
- seans: <09:30 ET ACILIS_ONCESI; 09:30–kapanış SEANS_ICI; ≥ kapanış KAPANIS_SONRASI. Yarım günlerde kapanış 13:00 (not=yarim_gun_13:00). Hafta sonu/tatil kabulü: not=islem_gunu_degil, ilk_tepki_gunu = sonraki işlem günü.
- 8-K, basın bülteninden dakikalar–saatler sonra kabul edilebilir: SEANS_ICI satırlarının bir kısmı aslında açılış öncesi bültendir (ilk tepki günü yine doğru).
- Aynı çeyrekte birden çok 2.02 (ön duyuru, düzeltme) olabilir; 8-K/A dahil edilmedi.
- www.sec.gov/files/company_tickers.json bu ortamda 403 verdi; kod→CIK eşlemesi efts.sec.gov varlık aramasıyla yapıldı (submissions `tickers` alanıyla kontrol).
