"""README_veri.md uretir. python3 -I veri_readme.py <VERI_DIR> <cikis1> <cikis2>"""
import sys, os, pandas as pd, numpy as np
V, o1, o2 = sys.argv[1:4]; P = f"{V}/panel"
def info(n):
    d = pd.read_parquet(f"{P}/{n}.parquet")
    dc = "date" if "date" in d.columns else "ts_utc"
    if dc in d.columns: a, b = str(d[dc].min())[:16], str(d[dc].max())[:16]
    else: a, b = str(d.index.min().date()), str(d.index.max().date())
    return d, len(d), a, b
F = pd.read_parquet(f"{P}/fut_long.parquet")
sp = pd.read_csv(f"{P}/bolunme_gunleri.csv"); sp = sp[sp.date >= "2017-03-01"]
und = set(pd.read_parquet(f"{P}/fut_ret.parquet").columns)
sp47 = sp[sp.sym.str.replace(".IS", "", regex=False).isin(und)]
spl47 = "; ".join(f"{r.sym.replace('.IS','')} {r.date} ({r.ratio})" for r in sp47.itertuples())
lim = F[F.fut_limit]
rows = []
for n, ad, ac in [("viop_gunluk", "bütün vadeli (F_) satırları, 18 sütun", "date, code, name, seg, und_raw, expiry, settle, prev_settle, open, high, low, close, vwap, value_tl, volume, trades, oi, und"),
                  ("fut_long", "ön vade, tarih×dayanak uzun biçim", "date, und, fut_ret, ret (ham), fut_settle, prev_settle, fut_value_tl, fut_trades, fut_code, expiry, bd, oi, fut_limit, nan_neden, ps_mismatch, n1, split_day"),
                  ("fut_ret", "geniş (indeks=date, sütun=53 dayanak)", "log getiri; temizlenmiş (NaN'lı)"),
                  ("fut_limit", "geniş, 0/1", "limit bayrağı"),
                  ("fut_settle", "geniş", "ön vade uzlaşma"), ("fut_value_tl", "geniş", "ön vade işlem hacmi TL"),
                  ("fut_trades", "geniş", "ön vade işlem sayısı"), ("fut_code", "geniş, metin", "ön vade kontrat kodu"),
                  ("spot_gunluk", "Yahoo günlük, uzun", "sym, date (borsa yerel günü), ts_utc, o, h, l, c, adj, v"),
                  ("dis_gunluk", "Yahoo günlük, uzun", "aynı sütunlar"),
                  ("saatlik", "Yahoo 1h, uzun", "sym, ts_utc (bar başlangıcı), o, h, l, c, v"),
                  ("dk5", "Yahoo 5m, uzun", "sym, ts_utc (bar başlangıcı), o, h, l, c, v")]:
    d, nr, a, b = info(n)
    rows.append(f"| `{n}.parquet` | {ad} | {nr:,} | {a} → {b} | {ac} |")
S = pd.read_parquet(f"{P}/spot_gunluk.parquet"); g = S.groupby("sym").date.min()
kisa_spot = ", ".join(f"{k.replace('.IS','')} {v.date()}" for k, v in g[g > "2017-03-01"].items())
fk = F.groupby("und").date.min(); kisa_fut = ", ".join(f"{k} {v.date()}" for k, v in fk[fk > "2017-04-01"].items())
H = pd.read_parquet(f"{P}/saatlik.parquet"); K = pd.read_parquet(f"{P}/dk5.parquet")
yr = lim.groupby(lim.date.dt.year).size().to_dict(); top = lim.und.value_counts().head(8).to_dict()
txt = f"""# Veri sözlüğü (10.11.2026) — VİOP öncü-gecikmeli çalışması

Konum: `{V}/panel/` (depoya girmez; pickle yok, hepsi parquet — pyarrow 26 kuruldu). Ham: `{V}/raw/viop/` (2.429 bülten, 101 tatil/yok), `{V}/raw/yahoo/` (daily, h1, m5, events, meta.json). Kod: `raporlar/2026-11-10_viop_leadlag_islem/kod/` (veri_indir.py, veri_yahoo.py, veri_viop_oku.py, veri_panel.py, veri_readme_istat.py, veri_readme.py). Sıra: veri_indir → veri_yahoo → veri_viop_oku → veri_panel (hepsi `python3 -I`).

## 1. Paneller
| dosya | biçim | satır | tarih aralığı | sütunlar |
|---|---|---|---|---|
""" + "\n".join(rows) + f"""

- Bülten: 2017-03-06'dan itibaren dosya var (2017-03-01..03 yok); 2429 işlem günü; son gün 2026-11-10 (bugünün bülteni indirilebildi). Bülten dayanak adları: AKBNK.E → `und`=AKBNK; D_XU030D → XU030; D_XLBNKD → XLBNK; D_USDTRY, D_XAUUSD, D_XAGUSD, D_XAUTRY → USDTRY, XAUUSD, XAGUSD, XAUTRY. `fut_*` panelinde 47 pay + 6 = 53 dayanak. Pay kontratı kodu `F_<KOD>MMYY` ya da düzeltilmiş `F_<KOD>MMYYN1` (bedelsiz/temettü sonrası yeniden adlandırılan aynı vade); XAUTRY kodu `F_XAUTRYMMMYY` (M gram altın demektir, mini değil). Kod deseni sıkı regex ile süzüldü (başka önek/sonek taşıyan mini kontrat kodları alınmaz); çarpan farkı ayrıca bültenden doğrulanmadı (açık kalan).
- `fut_ret` kuralı: her gün vadesine ≥2 iş günü (hafta sonu hariç takvim, resmî tatil dikkate alınmadı) kalan en yakın vade; `ln(settle/prev_settle)` AYNI kontrat; aynı vadede N1 ve normal kod birlikte varsa açık pozisyonu büyük olan. KOZAL→TRALT, KOZAA→TRMET (2025-11-24 ad değişimi) birleştirildi (2018-12-17'den beri 1.981 gün). Yahoo'da TRALT/TRMET/TRENJ yeni kodla 2014'ten itibaren tam geçmiş veriyor (3.280 gün; bölünmeye göre düzeltilmiş), eski kodla birleştirmeye gerek olmadı (KOZAL.IS, KOZAA.IS, IPEKE.IS Yahoo'da yok).
- NaN (toplam 24 dayanak-günü): 23 gün bedelsiz/düzeltme (N1 kodunun ilk günü ya da prev_settle önceki gün uzlaşmasından >%0,3 farklı ya da Yahoo bölünme günü) + 1 gün marj dışı (PGSUS 2017-05-03, 5 işlem). NOT (PLAN.md'den sapma): PLAN "|getiri| > ln(1,105)" yazıyor; bu −%10 limit-aşağı günü olan ln(0,9)=−0,1054'ü de siler (ilk denemede 432 gerçek gün silindi). Uygulanan: üst sınır ln(1+m+0,005), alt sınır ln(1−m−0,005); m=0,20 (2020-03-13 öncesi) / 0,10. PLAN.md değiştirilmedi.
- `fut_limit` (|basit getiri| ≥ 0,93·m; yani ≥%9,3 ya da ≥%18,6, NaN olmayan gün): toplam {int(F.fut_limit.sum()):,}; yıl: {yr}; en çok: {top}. Yalnız pay vadelisi için hesaplanır; endeks/kur/metalde 0.
- `fut_trades==0` (uzlaşma teorik) oranı: {(F.fut_trades==0).mean():.2%} — likidite dışlaması backtest ajanında yapılır.
- Dayanak başına başlangıç (2017-04'ten sonra başlayanlar; pay vadelisi o tarihte listelenmiş): {kisa_fut}.
- `spot_gunluk`: 112 sembol (47 dayanak + çift listesi .IS + XU030/XU100/XBANK + ek BIST listesi). Yahoo günlük satırı borsa yerel gününe oturtulur (`date`), yinelenen günler son kayıt tutularak ayıklandı; hacim 0 olan gün silinmedi (SASA 2025-06'dan beri günlerin %42'sinde v=0, fiyat işliyor). Sembol geçmişi 2017-03'ten kısa olanlar: {kisa_spot}. Yahoo'da bulunmayan sembol: yok (406 istekten 406 başarılı; `eksik_semboller.csv` boş). SDTTR 2023-01'den.
- `dis_gunluk`: 71 sembol (çift listesindeki yabancı + ^GSPC, ^STOXX50E, ^AXJO, ^N225, ^KS11). `=X` kur serisi yok. Yabancı günlük `date` kendi borsasının yerel günüdür (Tokyo/Seul/Sidney t günü BIST t kapanışından önce biter).
- Bedelsiz/bölünme günleri (Yahoo `events`): `panel/bolunme_gunleri.csv` (2017-03+ {len(sp)} kayıt, tümü .IS). 47 dayanak için {len(sp47)} kayıt: {spl47}. Saatlik/5 dk verisinde düzeltme YOK; bu günlerin saatlik penceresi (ve N1 geçiş günleri) dışlanmalı. Günlük `c` bölünme düzeltmeli, `adj` temettü+bölünme düzeltmeli.

## 2. fut_limit sayıları
Toplam {int(F.fut_limit.sum()):,} dayanak-günü (pay vadelisi, ≈ {F.fut_limit.sum()/F[F.und.isin(['AKBNK']) | True].shape[0]:.2%} satır). Yıl: {yr}. Dayanak başına en çok: {top}.

## 3. Zaman damgası kuralı (saatlik ve 5 dk)
- Tüm `ts_utc` UTC ve **bar başlangıcıdır** (bar [ts, ts+süre) aralığıdır). TSİ = UTC+3 (yıl boyu). BIST: sürekli işlem 07:00–15:00 UTC (10:00–18:00 TSİ).
- **5 dk (yalnız son 60 gün: {K.ts_utc.min().date()} → {K.ts_utc.max().date()})**, BIST: ilk bar 06:55 (açılış öncesi, hacim 0), 07:00 …, **son bar 14:55 UTC'de başlar** (17:55–18:00 TSİ). Örnek THYAO 2026-11-09: 14:45 bar kapanış 309,25; 14:50 bar kapanış 309,00; 14:55 bar kapanış 309,25 (hacim 1,27 M, günün yoğun barı). Günlük kapanış (kapanış müzayedesi dahil) 310,00. **Kapanış müzayedesi fiyatı geçmiş saatlik/5 dk barlarda YOK**: 5 dk son bar kapanışı günlük kapanıştan 45/60 günde farklı. Yalnız içinde bulunulan gün için 15:00 UTC'de hacmi 0 bir bar görünür (örnek 2026-11-10: 15:00 bar kapanış 313,75 = günlük kapanış); ertesi gün bu bar kaybolur. Backtestte 15:00 UTC başlangıçlı bar kullanma.
- **Saatlik (730 gün: {H.ts_utc.min().date()} → {H.ts_utc.max().date()})** BIST: bar ızgarası :30 (06:30, 07:30, … 14:30). 5 dk ile doğrulandı: 07:30 bar = 07:30–08:30; 14:30 bar yalnız 14:30–15:00 sürer. Örnek 2026-11-09 THYAO: 14:30 bar o=309,00 k=309,25 (5 dk 14:55 kapanışıyla aynı), hacim 3.065.895 = 5 dk toplamı. İlk bar (06:30) yakın tarihte hacmi 0 görünür (5 dk'da 07:00–07:30 hacmi var: Yahoo tuhaflığı). **Eski dönemde son bar 13:30'dur** (13:30–14:30/15:00; THYAO'da 728 günün ~296'sında; örn. 2025-12-01: son bar 13:30, kapanış 276,25; günlük kapanış 276,50). 14:30 barı 2026-03-30'dan itibaren düzenli; öncesinde yalnız bazı dönemlerde (2024-04..2025-09 arası ağırlıkla 14:30'lu). Yarım günler (06:30–09:30, ör. 2026-10-28) ve 08:30 başlayan günler (2026-04-20) var.
- Saatlik son bar kapanışı ile günlük kapanışın |log farkı| medyanı (5 hisse): 14:30-biten günlerde 12 bps, 13:30-biten günlerde 33 bps (müzayede etkisi + eski dönemde kesilmiş son yarım saat).
- Yabancı saatlik: ABD hisse/ETF (SPY) bar ızgarası :30 (2026-11-09 kış: 14:30, 15:30 … 20:30); Avrupa (EXW1.DE) ve emtia/vadeli (BZ=F, GC=F, ES=F) tam saat (00:00…); ^N225 00:00–06:00.

## 4. Önerilen kesin hesap kuralı (ileriye bakma yok)
Genel: bar `ts_utc` = başlangıç; "bilinme anı" = `end = min(ts + süre, 15:00 UTC)` (BIST için); yabancı için `end = ts + süre`. Kesme anı T'de bilinen son fiyat = o günün (UTC takvim günü) `end ≤ T` olan **son barının kapanışı**; `end ≤ T` olan bar yoksa o günün ilk barının **açılışı** (başlangıçta bilinir). Önceki gün aynı kural, getiri = ln(P_T(d) / P_T(önceki BIST günü)) (BIST iş günü takvimi; öncü yabancıysa kendi önceki seansının aynı T'si değil, BIST takvimindeki önceki günün T'si).
- **15:00 UTC'de bilinen son fiyat**: BIST: start ≤ 14:30 olan son barın kapanışı (14:30'lu günlerde 14:30 bar; 13:30'da biten günlerde 13:30 bar) — müzayede fiyatı hariç; 5 dk'da start 14:55 bar kapanışı (açılıp 15:00'de biter). ABD hisse/ETF: 15:00'de `end ≤ T` bar yok (14:30 bar 15:30'da biter) → o günün 14:30 barının AÇILIŞI (yaklaşık açılış fiyatı); 14:30 bar kapanışını kullanma (40 dk ileriye bakma). Avrupa/emtia tam saat: start ≤ 14:00 son bar kapanışı.
- **14:00 UTC'de bilinen son fiyat**: BIST: start ≤ 12:30 olan son barın kapanışı (13:30'a kadar bilinen fiyat; 13:30 barını KULLANMA, 14:30'a kadar ya da 15:00'e kadar uzar). 14:00'e tam oturan fiyat saatlik ızgarada yok; son 60 günde 5 dk start 13:55 kapanışı kullanılabilir. ABD: 14:00'de bar yok (açılış 14:30 UTC) → önceki seans kapanışı (ya da günlük t−1 sürümü). Avrupa/emtia: start ≤ 13:00 kapanışı.
- KATI_1700 için bu yüzden öncü ve hedef 30 dk eski fiyatla kurulur (tutucu); 1750 uyumu yalnız 5 dk (60 gün) ile ölçülür (14:50 UTC bilinen fiyat = start 14:45 bar kapanışı).
- Hacim 0 barları (BIST ilk bar, SASA) silme; fiyat kullanılır.

## 5. Sağlama (fut_ret)
(1) 2026-11-09, 9 dayanak (XU030, XLBNK, USDTRY, XAUUSD, XAGUSD, XAUTRY, AKBNK, THYAO, TUPRS): uzlaşma, önceki uzlaşma ve log getiri bültenle (bağımsız csv ayrıştırma) 9/9 birebir (ör. AKBNK F_AKBNK1126 72,15/69,77 = +3,354%; XU030 F_XU0301226 15251/14878). (2) 2023+ spot düzeltilmiş kapanış getirisiyle korelasyon: AKBNK 0,978 (n=958), THYAO 0,966 (n=963), TUPRS 0,967 (n=961), TRALT 0,975, TRMET 0,970 (hepsi >0,9; 1'den küçük kalma nedeni: uzlaşma fiyatı kapanış müzayedesi fiyatından farklı oluşur ve spot günlük kapanış müzayede fiyatıdır). (3) Vade geçişi 2026-10-30 (29 Ekim tatil): AKBNK 10-28'de F_AKBNK1026 (bd=2) ile ln(63,04/64,35); 10-30'da F_AKBNK1126 ile ln(62,41/64,65)=−3,53%; 64,65 11 numaralı kontratın kendi önceki uzlaşmasıdır (10 numaralı kontratın uzlaşması karıştırılmadı). XU030: 10-30'da F_XU0301226 ln(14108/14649).
"""
open(o1, "w", encoding="utf-8").write(txt); open(o2, "w", encoding="utf-8").write(txt)
print(len(txt.split()))
