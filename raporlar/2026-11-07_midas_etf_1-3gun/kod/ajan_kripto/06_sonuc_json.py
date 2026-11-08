"""6) Sonuç JSON'u (sonuclar/aile_kripto/sonuc.json). Çalıştır: python3 -I kod/ajan_kripto/06_sonuc_json.py
Sayılar 01-05'in ürettiği CSV'lerden okunur; metin alanları bu betikte."""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import kr

R = kr.ROOT; O = kr.OUT
A = pd.read_csv(os.path.join(O, "aday_detay.csv")).set_index("label")
ISL = pd.read_csv(os.path.join(O, "islenebilirlik.csv")).set_index("sym")
SW = pd.read_csv(os.path.join(R, "sonuclar", "leadlag_sweep.csv"))
F = pd.read_csv(os.path.join(O, "fdr_tum.csv"))
TV = pd.read_csv(os.path.join(R, "sonuclar", "tv_etf.csv")).set_index("sym")["tv"].to_dict()
n_tests = len(F) + 765 * 4

def r1(x, k=1):
    return None if x is None or (isinstance(x, float) and not math.isfinite(x)) else round(float(x), k)

S1 = A.loc["S1 SBIT O1"]; S2 = A.loc["S2 BTC_D C0"]
KOD = "/home/user/Xxxx/raporlar/2026-11-07_midas_etf_1-3gun/kod/ajan_kripto"
SON = "/home/user/Xxxx/raporlar/2026-11-07_midas_etf_1-3gun/sonuclar/aile_kripto"
NOT = "/home/user/Xxxx/raporlar/2026-11-07_midas_etf_1-3gun/notlar/aile_kripto.md"

def m(lbl, col="mean_net_bp", k=0):
    v = A.loc[lbl, col]
    if col == "t": k = 2
    return f"{float(v):.{k}f}".replace("-", "−") if k else str(int(round(float(v)))).replace("-", "−")

strat = [
 {
  "id": "kripto_S1",
  "ad": "Perşembe gün içi ters BTC — SBIT (−2x) Perşembe açılış → aynı gün kapanış",
  "kural": ("Takvim kuralı, gösterge yok: her Perşembe (NYSE tam gün açıksa) AMEX:SBIT (ProShares UltraShort Bitcoin, −2x günlük) ABD açılışında "
            "AL, aynı gün kapanıştan önce SAT; pozisyon gece taşınmaz. Sinyal ETF'si yok (gün seçimi); izleme için NASDAQ:IBIT / COINBASE:BTCUSD. "
            "Alternatif −1x araç AMEX:BITI (net kenar küçük: 2.500$'da ~8 bp). Perşembe tatilse (26 Kas 2026 Şükran Günü) işlem yok. "
            "Pine (günlük): sig = dayofweek == dayofweek.thursday; giriş open, çıkış close."),
  "giris": ("Perşembe ABD açılışı: kış saatinde TR 17:30 (yaz saatinde TR 16:30). Açılıştan hemen sonra piyasa emri veya makasın hemen üstünde "
            "limit emir. Pre-market (TR 12:00-17:30) yalnız limit emir; piyasa kapalıyken verilen piyasa emri %3 bloke ile açılışta işler."),
  "tutus": "Gün içi (~6,5 saat), 1 işlem günü",
  "cikis": ("Aynı Perşembe kapanıştan 5-10 dk önce (kış TR ~23:50, yaz ~22:50) piyasa/agresif limit satış (Midas'ta MOC/LOC yok). "
            "24 Ara 2026 Perşembe erken kapanış 13:00 ET = TR 21:00 → çıkış TR ~20:50. Zarar durdur test edilmedi."),
  "islem_etf": ["SBIT", "BITI"],
  "sinyal_etf": "Takvim (Perşembe); dayanak BTC — izleme NASDAQ:IBIT / COINBASE:BTCUSD",
  "n": int(S1.n), "brut_bp": r1(S1.mean_gross_bp), "net_bp": r1(S1.mean_net_bp), "kazanma": r1(S1.win, 3), "pf": r1(S1.pf, 2), "t": r1(S1.t, 2),
  "is_net_bp": 9.2, "oos_net_bp": r1(S1.mean_net_bp),
  "yil_pozitif": r1(S1.years_pos_frac, 2), "maxdd": r1(S1.maxdd, 3), "en_kotu_bp": r1(S1.worst_bp, 0),
  "maliyet_duyarlilik": f"1.000$: {m('S1 SBIT O1','net_1000')} bp | 2.500$: {m('S1 SBIT O1','net_2500')} bp | 10.000$: {m('S1 SBIT O1','net_10000')} bp (net, işlem başı; SBIT makası ~4 bp)",
  "mod_saglamlik": (f"O1 (asıl; Per açılış→Per kapanış): brüt {m('S1 SBIT O1','mean_gross_bp')} / net {m('S1 SBIT O1')} bp, t={m('S1 SBIT O1','t',2)}; "
                    f"C0 (Çar kapanış→Per kapanış, Çarşamba gecesini de taşır): brüt {m('S1 SBIT C0','mean_gross_bp')} / net {m('S1 SBIT C0')}, t={m('S1 SBIT C0','t',2)}; "
                    f"C1 (Per kapanış→Cum kapanış): brüt {m('S1 SBIT C1','mean_gross_bp')} / net {m('S1 SBIT C1')}, t={m('S1 SBIT C1','t',2)} → etki yalnız Perşembe ABD seansında; açılış girişine bağımlı (kapanışa bağımlı değil)."),
  "aile_ici": (f"Long ürünlerde Perşembe gün içi BRÜT getiri (negatif = ters ürün lehine): BTC 16:00 ET serisi {m('S1 aile BTC_ET','mean_gross_bp')} bp (t={m('S1 aile BTC_ET','t',2)}, n={m('S1 aile BTC_ET','n')}), "
               f"IBIT {m('S1 aile IBIT','mean_gross_bp')} (t={m('S1 aile IBIT','t',2)}), BITO 2021-10+ {m('S1 aile BITO','mean_gross_bp')} (t={m('S1 aile BITO','t',2)}), BITX {m('S1 aile BITX','mean_gross_bp')}, "
               f"ETHA {m('S1 aile ETHA','mean_gross_bp')} (t={m('S1 aile ETHA','t',2)}), MSTU {m('S1 aile MSTU','mean_gross_bp')}, CONL {m('S1 aile CONL','mean_gross_bp')}, BLOK 2018+ {m('S1 aile BLOK','mean_gross_bp')} "
               "(2016-2021: −12, 2023-06+: −38); SPY/QQQ'da da 2023-06+ döneminde Perşembe gün içi brüt −12/−21 bp (2016-2023 arası pozitif) → kriptoya özgü değil, dönemsel risk iştahı deseni. "
               f"Ters araçlar: SBIT net +{m('S1 SBIT O1')} (t={m('S1 SBIT O1','t',2)}), BITI net +{m('S1 BITI O1')} (t={m('S1 BITI O1','t',2)}; 2022-06..2024-03 −20, 2024-04+ +27). "
               "SBIT'te diğer hafta günleri gün içi net −17..−40 bp (yalnız Perşembe pozitif)."),
  "test_sayisi": int(n_tests),
  "fdr": ("BH-FDR q=0,10. Tüm aile testleri ({}: genel kütüphane 4.752 aile satırı + dayanak proxy 990 + hipotez 352 + lead-lag 104 + aday 60 + leadlag_sweep 3.060) "
          "üzerinde eşik p≤0,00010; sweep hariç {} testte eşik p≤0,00047. SBIT satırı p=0,018 → GEÇMEDİ. Dayanak satırları GEÇTİ: BTC 16:00 ET Perşembe gün içi (p=0,00009-0,00010), "
          "BITO (p=0,00007), IBIT, ETHA, BITX (p<0,0001).").format(n_tests, len(F)),
  "guven": "dusuk",
  "notlar": ("Biçimsel eşiği geçiyor ama güven düşük: (1) Etki 2024-2025'te yoğun: SBIT yıllık net 2024 +105, 2025 +131, 2026 +12 bp (zayıflıyor). "
             "(2) SBIT öncesi dönem (BITO 2021-10..2024-03, n=125): Perşembe gün içi −12,6 bp (t=−0,5) → SBIT-eşdeğeri net yalnız +9 bp (is_net_bp alanı bu değer; resmî IS ≤2021'de yalnız 10 Perşembe var); "
             "2022'de ters işaret (BITO +32 bp); BITI 2022-06..2024-03 net −20 bp. (3) En iyi 5 işlem çıkarılınca net +42 bp (t=1,36), medyan −5 bp: kazanç birkaç büyük düşüş Perşembesinden. "
             "(4) Mekanizma bilinmiyor; 5 gün × seans seçimi veri madenciliği riski (FDR dayanakta geçiyor, ETF satırında geçmiyor). (5) SPY/QQQ'da da aynı dönemde Perşembe gün içi zayıf → geniş risk iştahı deseni. "
             "(6) CPI'lı Perşembeler (ör. 10 Ara 2026) çok oynak (IBIT gün içi ort. −290 bp, n=7); CPI günleri hariç net 64 bp (t=1,81). "
             "(7) SBIT/BITI'nin Midas'ta bulunurluğu doğrulanmadı; ProShares Trust II PTP bildiriminde (26.02.2026) yer almıyor → PTP/K-1 görünmüyor; uygulamada 'PTP' ibaresini kontrol et. "
             "Öneri: küçük pozisyon, 2026 Q4-2027 Q1 canlı izleme; 12 işlemde ortalama ≤0 ise bırak. Yılda ~50 işlem; ~%48 kazanma, PF 1,76."),
  "betik": f"python3 -I {KOD}/05_adaylar.py  (önce 02, 03, 04; işlemler: {SON}/aday_kripto_S1_islemler.csv)"
 },
 {
  "id": "kripto_S2",
  "ad": "BTC trend filtresi (kapanış > SMA10 > SMA50) → IBIT 3 gün long",
  "kural": ("TradingView günlük grafik NASDAQ:IBIT (ETH için NASDAQ:ETHA kendi grafiği). SİNYAL (t kapanışı): kapanış > SMA(10) VE SMA(10) > SMA(50). "
            "İŞLEM: NASDAQ:IBIT long (Midas'ta IBIT yoksa AMEX:GBTC — sembol sayfası doğrulanmış — veya CBOE:FBTC). 3 işlem günü tut; pozisyondayken yeni sinyal yok sayılır, "
            "çıkış günü koşul sürüyorsa yeniden girilebilir. COINBASE:BTCUSD günlük mumunu sinyal için KULLANMA (00:00 UTC = TR 03:00'te kapanır, ABD kapanışında bilinmez); "
            "BTC ile hesaplanacaksa 16:00 ET (kış TR 00:00) anlık fiyatı kullan. Pine: c=close; sig = c > ta.sma(c,10) and ta.sma(c,10) > ta.sma(c,50)"),
  "giris": ("C0: t günü kapanıştan 5-10 dk önce (kış TR ~23:50, yaz ~22:50) koşul sağlanıyorsa piyasa/agresif limit alış; alternatif: kapanış sonrası after-hours "
            "(kış TR 00:00-04:00, yaz 23:00-03:00) yalnız limit emir. O1 (t+1 açılış TR 17:30) ve C1 (t+1 kapanış) dayanakta pozitif, ETF döneminde zayıf."),
  "tutus": "3 işlem günü",
  "cikis": "Girişten 3 işlem günü sonra kapanıştan 5-10 dk önce (kış TR ~23:50, yaz ~22:50) sat. Erken çıkış/stop yok (test edilmedi).",
  "islem_etf": ["IBIT", "GBTC", "FBTC", "ETHA"],
  "sinyal_etf": "IBIT (kendi günlük kapanışı) veya BTC 16:00 ET fiyatı; ETH için ETHA",
  "n": int(S2.n), "brut_bp": r1(S2.mean_gross_bp), "net_bp": r1(S2.mean_net_bp), "kazanma": r1(S2.win, 3), "pf": r1(S2.pf, 2), "t": r1(S2.t, 2),
  "is_net_bp": r1(S2.is_net_bp), "oos_net_bp": r1(S2.oos_net_bp),
  "yil_pozitif": r1(S2.years_pos_frac, 2), "maxdd": r1(S2.maxdd, 3), "en_kotu_bp": r1(S2.worst_bp, 0),
  "maliyet_duyarlilik": (f"Dayanak BTC_D (IBIT maliyeti): 1.000$ {m('S2 BTC_D C0','net_1000')} | 2.500$ {m('S2 BTC_D C0','net_2500')} | 10.000$ {m('S2 BTC_D C0','net_10000')} bp; "
                         f"IBIT 2024+ (BTC 16:00 ET sinyali): 1.000$ {m('S2 IBIT sinyal=BTC_ET C0','net_1000')} | 2.500$ {m('S2 IBIT sinyal=BTC_ET C0','net_2500')} | 10.000$ {m('S2 IBIT sinyal=BTC_ET C0','net_10000')} bp"),
  "mod_saglamlik": (f"BTC_D 2016-11..2026-11: C0 net {m('S2 BTC_D C0')} (t={m('S2 BTC_D C0','t',2)}), C1 net {m('S2 BTC_D C1')} (t={m('S2 BTC_D C1','t',2)}; IS {m('S2 BTC_D C1','is_net_bp')} / OOS {m('S2 BTC_D C1','oos_net_bp')}); "
                    f"BTC 16:00 ET 2023-08+: C0 {m('S2 BTC_ET C0')} (t={m('S2 BTC_ET C0','t',2)}), O1 {m('S2 BTC_ET O1')}, C1 {m('S2 BTC_ET C1')}; "
                    f"IBIT kendi grafiği: C0 {m('S2 IBIT sinyal=kendi C0')} (t={m('S2 IBIT sinyal=kendi C0','t',2)}), O1 {m('S2 IBIT sinyal=kendi O1')}, C1 {m('S2 IBIT sinyal=kendi C1')}; "
                    f"IBIT←BTC 16:00 ET: C0 {m('S2 IBIT sinyal=BTC_ET C0')}, O1 {m('S2 IBIT sinyal=BTC_ET O1')}, C1 {m('S2 IBIT sinyal=BTC_ET C1')} bp (net)."),
  "aile_ici": (f"ETH_D C0 net {m('S2 ETH_D C0')} (t={m('S2 ETH_D C0','t',2)}; IS {m('S2 ETH_D C0','is_net_bp')} / OOS {m('S2 ETH_D C0','oos_net_bp')}; FDR geçti), ETHA kendi C0 {m('S2 ETHA sinyal=kendi C0')}, "
               f"ETHU {m('S2 ETHU sinyal=ETH_ET C0')}, BITX (BTC sinyali) {m('S2 BITX sinyal=BTC_ET C0')} (t={m('S2 BITX sinyal=BTC_ET C0','t',2)}), BLOK 2018+ {m('S2 BLOK sinyal=kendi C0')} (t={m('S2 BLOK sinyal=kendi C0','t',2)}; IS {m('S2 BLOK sinyal=kendi C0','is_net_bp')} / OOS {m('S2 BLOK sinyal=kendi C0','oos_net_bp')}), "
               f"MSTU {m('S2 MSTU sinyal=kendi C0')}, CONL {m('S2 CONL sinyal=kendi C0')}, BITO {m('S2 BITO sinyal=kendi C0')} (dağıtım verisi eksik). Momentum ailesinin diğer kuralları "
               "(20 gün zirvesi, RSI2>90, 3 gün yükseliş, z1>2) BTC_D ve ETH_D'de IS ve OOS kenarı (koşulsuz aynı tutuşun üstü) pozitif — aile tutarlı, ama OOS kenarı 12-43 bp."),
  "test_sayisi": int(n_tests),
  "fdr": "BTC_D C0 p=0,0007 → GEÇMEDİ (eşik p≤0,00047; sweep dahil p≤0,00010). Aynı kural ETH_D C0'da p=0,00025 → kendi testlerimde GEÇTİ (sweep dahil eşikte geçmiyor).",
  "guven": "dusuk",
  "notlar": ("Biçimsel eşik dayanak uzun testinde geçiyor (t≥2, IS ve OOS>0, yılların %70'i +, n=317, C1'de de pozitif); ETF döneminde zayıf. "
             "Komşu parametreler (SMA 5/50, 10/30, 20/50, 10/100) BTC_D'de benzer (t 3,4-4,2; OOS 41-58 bp) — parametre seçimine duyarlı değil. Ancak: (1) Kazancın çoğu IS boğa piyasası "
             "(IS net 225 / kenar 107 bp; OOS net 58 bp t=1,26, kenar 44 bp). (2) Ayı yıllarında kaybeder (yıllık ort. 2018 −444, 2022 −277 bp/işlem). (3) IBIT'te (2024-01..2026-11) C0 +30-44 bp, t<1; C1 ~0/negatif. "
             "(4) BTC_D'de sinyal 00:00 UTC kapanışından (16:00 ET'den 3-4 saat sonra) — kendi içinde ileri bakışsız ama ETF zamanlamasıyla birebir değil; birebir 16:00 ET serisi yalnız 3,4 yıl. "
             "(5) Kenarın bir kısmı BTC'nin pozitif drift'i: strateji 'trend varken long BTC' — ayı piyasasında da sinyal üretir. (6) Kaldıraçlı araç (BITX) kullanılırsa 2×IBIT'e göre takip kaybı ~−12 bp/gün (3 günde −37 bp). "
             "Yılda ~30 işlem; pozisyonda olma oranı ~%40. Hafta sonu riskini (Cuma→Pazartesi boşluğu) taşır."),
  "betik": f"python3 -I {KOD}/05_adaylar.py  (işlemler: {SON}/aday_kripto_S2_islemler.csv)"
 },
]

def izl(sym, karar, gerekce):
    r = ISL.loc[sym]
    return {"sym": sym, "karar": karar, "gerekce": gerekce, "tv": r.tv, "likidite_mn_usd": r1(r.med_dollar_vol_m, 1),
            "maliyet_bp": r1(r.cost_rt_bp, 1), "vol_1d_bp": r1(r.vol_1d_bp, 0)}

izleme = [
 izl("IBIT", "kabul", "Ana spot BTC aracı: medyan 2,0 mlr$/gün, makas ~2 bp, gidiş-dönüş 14 bp (2.500$), maliyet/1g oynaklık 0,05. S2 burada; S1'in long karşılığı. Sürücü: BTC (corr 1,00). Midas'ta bulunurluğu 'muhtemel' (doğrulanmadı) — yoksa GBTC."),
 izl("FBTC", "yedek", "IBIT kopyası (corr 0,9993, günlük takip farkı 11 bp); 291 mn$/gün, maliyet 14 bp. Bağımsız kanıt değil; IBIT yoksa kullanılabilir."),
 izl("GBTC", "yedek", "IBIT kopyası (corr 0,9992); 136 mn$/gün, makas ~4 bp (16 bp). Midas'ta sembol sayfası DOĞRULANMIŞ tek spot BTC ETF'si → IBIT/FBTC yoksa birinci seçenek. Yüksek yönetim ücreti 1-3 günde önemsiz."),
 izl("BITB", "red", "IBIT kopyası (corr 0,9998), daha az likit (70 mn$), makas ~4 bp. IBIT/FBTC/GBTC varken gereksiz."),
 izl("ARKB", "red", "IBIT kopyası (corr 0,9997), 61 mn$/gün, makas ~4 bp. Gereksiz."),
 izl("BITO", "red", "BTC vadeli ETF: veri kaynağında dağıtım kaydı YOK (ay başı açılışlarda IBIT'e göre ort. −295 bp boşluk = ex-date) → testler aşağı yanlı; yüksek aylık dağıtımlar ABD'de %20 stopaja tabi (ex-date taşımak vergi sızıntısı); vadeli roll maliyeti; fiyat ~10$ → 1 sent makas ~10 bp (22 bp). Spot ETF'ler varken gereksiz."),
 izl("ETHA", "kabul", "Ana spot ETH aracı: 553 mn$/gün, makas ~2 bp (14 bp), maliyet/oynaklık 0,036. BTC'den kısmen ayrışır (corr 0,83-0,93). S2 aile versiyonu (ETH_D'de FDR geçti; ETHA'da zayıf). Midas'ta 'muhtemel'."),
 izl("ETHE", "yedek", "ETHA kopyası (corr 0,9997); 50 mn$/gün, makas ~6 bp (18 bp). Midas'ta sembol sayfası DOĞRULANMIŞ → ETHA yoksa kullan."),
 izl("BITX", "yedek", "2x BTC (172 mn$/gün, 18 bp). Dayanak sinyaliyle kaldıraçlı araç; ama 2×IBIT'e göre takip kaybı −11,5 bp/gün (t=−8,7; 3 günde −37 bp). Kaldıraçlı/ters ürünlerin Midas'ta bulunurluğu doğrulanmadı."),
 izl("BITU", "red", "BITX kopyası (corr 0,987), daha az likit (59 mn$), takip kaybı −11 bp/gün; 24.12.2025'te 2×IBIT'e göre −21 puan açıklanamayan fark (dağıtım/veri). BITX tercih."),
 izl("BITI", "yedek", "−1x BTC (38 mn$/gün, makas ~8 bp, 20 bp). Long-only hesapta kısa BTC aracı; S1'in düşük riskli alternatifi (net kenar küçük ~8 bp). Ay başlarında açıklanamayan −5 puanlık farklar (dağıtım kaydı eksik olabilir)."),
 izl("SBIT", "kabul", "−2x BTC (57 mn$/gün, makas ~4 bp, 16 bp; maliyet/oynaklık 0,028). S1 (Perşembe gün içi, düşük güven) aracı. ProShares Trust II PTP listesinde değil. Uyarı: günlük sıfırlamalı −2x; gece taşımada yol bağımlılığı; Midas'ta bulunurluğu doğrulanmadı."),
 izl("ETHU", "yedek", "2x ETH (144 mn$/gün, 17 bp); 2×ETHA'ya göre takip kaybı −7,9 bp/gün. Kendi stratejisi yok; ETH sinyali için kaldıraçlı araç. Günlük oynaklık 767 bp (en kötü gün −28%)."),
 izl("BLOK", "red", "Blokzincir hisse ETF'si: 14 mn$/gün (sınırda), makas ~8 bp (20 bp), maliyet/oynaklık 0,077 (ailede en kötü). Kendi stratejisi yok; BTC ile eşzamanlı (corr 0,73), gecikmeli öncü yok. BTC/ETH'yi IBIT/ETHA ile işlemek daha ucuz."),
 izl("MSTU", "red", "2x MSTR: 176 mn$/gün ama günlük oynaklık 1.026 bp, en kötü gün −34%, 1 yıl −89%; 2×MSTR'ye göre takip kaybı −15 bp/gün. BTC'den MSTR'ye ertesi gün öncülük yok (t=−1,0; TH06). 1-3 günlük kurallarda kenar yok (S2: −303 bp). Tek hisse kaldıraçlı ailesinde değerlendirilir."),
 izl("CONL", "red", "2x COIN: fiyat 2,79$ → 1 sentlik adım ~36 bp makas (48 bp gidiş-dönüş); 1 yıl −90%; 2022 verisinde dayanakla tutarsız günler. İşlenebilir değil."),
]

def drv(T, leaders):
    out = []
    names = {"BTC_16ET": ("BTC/USD (16:00 ET getirisi; eşzamanlı)", "COINBASE:BTCUSD"), "ETH_16ET": ("ETH/USD (16:00 ET getirisi; eşzamanlı)", "COINBASE:ETHUSD"),
             "QQQ": ("Nasdaq-100 (QQQ)", "NASDAQ:QQQ"), "SPY": ("S&P 500 (SPY)", "AMEX:SPY"), "VIX_dlog": ("VIX (log değişim)", "CBOE:VIX"),
             "ETHA": ("ETHA", "NASDAQ:ETHA"), "IBIT": ("IBIT", "NASDAQ:IBIT")}
    for L in leaders:
        x = SW[(SW.target == T) & (SW.leader == L)]
        if len(x):
            out.append({"ad": names[L][0], "tv": names[L][1], "corr_1y": r1(x.corr_1y.iloc[0], 2), "beta_1y": r1(x.beta_1y.iloc[0], 2)})
    return out

RT_BTC = [
 {"ad": "Bitcoin spot (Coinbase)", "tv": "COINBASE:BTCUSD", "neden": "7/24 işler. ETF kapalıyken (TR 00:00-17:30, kış) BTC'nin 16:00 ET'den sonraki hareketi ertesi açılış boşluğunu belirler: IBIT açılış boşluğu ≈ BTC 16:00→09:30 ET hareketi (R²=0,96, eğim 1,00; Pazartesi R²=0,98 = hafta sonu hareketi). Öncü değil, açılışı önceden gösteren izleme aracı."},
 {"ad": "CME Bitcoin vadeli (ön ay)", "tv": "CME:BTC1!", "neden": "CME Globex Pazar-Cuma (kış: TR 02:00 → ertesi gün 01:00, günlük 1 saat ara); hafta sonu kapalı → Pazartesi 'CME boşluğu'. Kurumsal akış/baz (vadeli primi) göstergesi."},
 {"ad": "Ethereum spot (Coinbase)", "tv": "COINBASE:ETHUSD", "neden": "7/24; kripto risk iştahı (IBIT ile corr 0,92)."},
 {"ad": "Nasdaq-100 E-mini vadeli", "tv": "CME_MINI:NQ1!", "neden": "~23 saat işler; ABD hisse risk iştahı (IBIT-QQQ corr 0,49, beta 1,03). Makro haber (CPI/NFP TR 16:30) tepkisini açılış öncesi gösterir."},
]
RT_ETH = [
 {"ad": "Ethereum spot (Coinbase)", "tv": "COINBASE:ETHUSD", "neden": "7/24; ETHA açılış boşluğunu belirleyen dayanak (ETF kapalıyken TR 00:00-17:30, kış)."},
 {"ad": "CME Ether vadeli (ön ay)", "tv": "CME:ETH1!", "neden": "CME Globex Pazar-Cuma; hafta sonu kapalı; kurumsal akış/baz göstergesi."},
 {"ad": "Bitcoin spot (Coinbase)", "tv": "COINBASE:BTCUSD", "neden": "Kripto piyasa faktörü (ETHA-BTC corr 0,93, beta 1,27)."},
 {"ad": "Bitcoin hakimiyeti", "tv": "CRYPTOCAP:BTC.D", "neden": "ETH/BTC göreli gücü (altcoin risk iştahı); eşzamanlı bağlam, öncü değil."},
]
TAKVIM = ("TR saatiyle (ABD kış saati): CPI 10 Kas 2026 Sal 16:30; aylık opsiyon vadesi 20 Kas Cum; Şükran Günü 26 Kas Per KAPALI (S1 işlemi yok), 27 Kas Cum erken kapanış 21:00; "
          "NFP 4 Ara Cum 16:30; FOMC 9 Ara Çar 22:00 (SEP); CPI 10 Ara Per 16:30 (S1 günü — CPI'lı Perşembeler çok oynak); triple witching 18 Ara Cum; 24 Ara Per erken kapanış 21:00; 25 Ara ve 1 Oca kapalı. "
          "Kripto 7/24 işler: hafta sonu/tatil hareketi Pazartesi (tatil ertesi) açılışında boşluk olarak gelir. CME BTC/ETH vadeli aylık vadesi ayın son Cuması (kural; takvim dosyalarında yok, doğrulanmadı).")
NOT_LL = ("Doğrulanmış gecikmeli öncü YOK. leadlag_sweep'te ailenin 765 hedef×öncü satırında (3.060 test) global ve aile içi BH-FDR geçen 0. Ek testler (BTC/ETH 16:00 ET → hedef t+1/t+3, kendi gecikmesi kontrollü; "
          "'yetişme' u=β60·r_BTC−r_T kendi getirisi kontrollü) hiçbiri |t|≥2 değil. Yetişme kuralları (u≥+2σ → long) maliyetli backtestte anlamsız. BTC gece hareketi → IBIT gün içi devamı: z≥+1'de IBIT O1 net +29 bp (t=1,40), "
          "z≤−1'de SBIT +48 bp (t=1,09) — anlamsız. Gün içi BTC ile korelasyon ~1 olduğundan 'sürücüler' eşzamanlıdır, öncü değildir.")

TAKVIM_KISA = "Bkz. IBIT girdisi: CPI 10 Kas 16:30; 26 Kas kapalı; NFP 4 Ara; FOMC 9 Ara 22:00; CPI 10 Ara (Per) 16:30; 24 Ara erken kapanış 21:00 (TR saati)."
NOT_KISA = "Doğrulanmış gecikmeli öncü YOK (sweep FDR 0; ek testler |t|<2). Sürücüler eşzamanlıdır; ayrıntı IBIT/ETHA girdisinde."
leadlag = []
for T, rt, ld, full in (("IBIT", RT_BTC, ["BTC_16ET", "ETH_16ET", "QQQ", "VIX_dlog"], True), ("FBTC", RT_BTC[:2], ["BTC_16ET", "IBIT"], False),
                        ("GBTC", RT_BTC[:2], ["BTC_16ET", "IBIT"], False), ("BITX", RT_BTC[:2], ["BTC_16ET", "IBIT", "QQQ"], False),
                        ("BITI", RT_BTC[:2], ["BTC_16ET", "IBIT"], False), ("SBIT", RT_BTC, ["BTC_16ET", "IBIT", "QQQ"], True),
                        ("ETHA", RT_ETH, ["ETH_16ET", "BTC_16ET", "QQQ", "VIX_dlog"], True), ("ETHE", RT_ETH[:2], ["ETH_16ET", "ETHA"], False),
                        ("ETHU", RT_ETH[:2], ["ETH_16ET", "ETHA", "BTC_16ET"], False)):
    extra = ""
    if T in ("BITX", "ETHU"): extra = " Kaldıraçlı: 2× dayanak getirisi eksi ~8-12 bp/gün takip kaybı; dayanak (IBIT/ETHA) sinyalleriyle işlem aracı."
    if T in ("BITI", "SBIT"): extra = " Ters ürün: dayanak düşüşünde kazanır; S1 aracı (SBIT) / düşük riskli alternatif (BITI)."
    if T in ("FBTC", "GBTC"): extra = " IBIT kopyası (corr ~0,999)."
    if T == "ETHE": extra = " ETHA kopyası (corr 0,9997)."
    leadlag.append({"sym": T, "suruculer": drv(T, ld), "onculer": [], "gercek_zamanli": rt,
                    "not": (NOT_LL if full else NOT_KISA) + extra, "takvim_riskleri": TAKVIM if full else TAKVIM_KISA})

elenen = [
 {"ad": "KR01 IBIT gece (kapanışta al, açılışta sat)", "neden": "IBIT gece ort. +16,5 bp (t=1,89), gün içi −5 bp; ama her gece işlem → 2.500$'da net +2 bp (t=0,25); 10.000$'da +11 bp (t≈1). Kopyalarda aynı. 'Gece +%165' gözlemi doğru, işlem maliyetinden sonra kenar yok."},
 {"ad": "KR05 kış/yaz gece farkı ve 21-23 UTC penceresi", "neden": "IBIT kış gecesi brüt 28 bp vs yaz 11 bp (ikisi de t<1,7; net ≤14 bp). BTC 21-23 UTC penceresi ort. +6,4 bp (t=3,4, n=1.263) ama 14 bp maliyetin altında; 2026'da −0,5 bp."},
 {"ad": "KR02 hafta sonu (Cuma kapanış → Pazartesi kapanış)", "neden": "BTC_D net 55 bp (t=2,28; IS 87 / OOS 22), IBIT 30 bp (t=0,93). Ama takvim günü başına getiri hafta sonu ile hafta içi arasında farksız (fark t=0,5-0,9): 'etki' 3 takvim günü BTC drift'i, anomali değil."},
 {"ad": "KR03 spot BTC ETF akımı ≥ +500 mn$", "neden": "Akım verisi projede yok → test edilemedi (literatür: ertesi gün korelasyonu ~0,09)."},
 {"ad": "KR04 haftalık momentum (g7 üst %20, 3 gün)", "neden": "BTC_D C0 net 175 bp ama OOS −5 bp (kenar −21); BTC 16:00 ET ve IBIT'te negatif (IBIT C0 −48 bp)."},
 {"ad": "KR06 kaldıraçlı BTC/ETH tutuşu", "neden": "Strateji değil, maliyet: BITX−2×IBIT −11,5 bp/gün (t=−8,7), 3 günde −37 bp; BITU −11,4; ETHU −7,9; SBIT +3, BITI ~0. Kaldıraçlı long ürün, dayanak sinyalinin kenarı >~40 bp/3 gün değilse anlamsız."},
 {"ad": "BTC 1 günlük z > +2 → 3 gün (momentum)", "neden": "Yön tutarlı (BTC_D C0/C1 net ~150 bp, IS ve OOS > 0; BTC 16:00 ET ve IBIT'te üç modda da pozitif) ama t=1,8-1,9 (BTC_D), ETF'de n=16-23 → eşik altı. İzlemeye değer."},
 {"ad": "BTC 1 günlük z < −2 (dönüş) ve 3 gün düşüş", "neden": "z<−2 yalnız C0 h=1'de pozitif (kapanışa bağımlı; O1/C1 ~0 veya negatif). 3 gün düşüş: kenar ≈ 0 (BTC_D, BTC 16:00 ET, IBIT)."},
 {"ad": "20 gün zirve kırılımı / 20 gün dip", "neden": "Zirve: BTC_D C0 h3 net 175 (IS 293 / OOS 28; OOS kenar 13), IBIT C1 −28 bp. Dip: kenar negatif/≈0."},
 {"ad": "Perşembe kapanış → Pazartesi kapanış / Cuma etkisi", "neden": "BTC_D ve ETH_D'de IS/OOS kenarı pozitif ama tutuş 4 takvim günü → drift; IBIT t<1."},
 {"ad": "Ay sonu BTC zayıflığı (sondan 2 gün)", "neden": "BTC 16:00 ET'de O1 h2 −142 bp (FDR geçti) ama uzun BTC_D'de aynı pencere IS'te güçlü pozitif → 2023-2026'ya özgü; aday değil."},
 {"ad": "TH06 BTC → MSTR/MSTU, COIN/CONL ertesi gün; yetişme kuralları", "neden": "Kendi gecikmesi kontrollü t: MSTR −0,98, COIN −1,14, MSTU −0,17; yetişme kuralları (u≥+2σ) n=7-27, t<1,2. Öncülük yok (literatürle uyumlu)."},
 {"ad": "BTC gece hareketi → IBIT gün içi devamı", "neden": "Eğim 0,06 (t=0,9); kural: IBIT +29 bp (t=1,4), SBIT +48 bp (t=1,1) — anlamsız."},
 {"ad": "BLOK ← reel faiz (DFII10 düşüşü) / TIP", "neden": "Sweep'te IS/OOS aynı işaret (h3 t≈3) ama FDR yok; kural: C0 net 55 (t=2,05) yalnız kapanışa bağımlı ve DFII10 kapanışta bilinmiyor; O1 IS −1 bp, C1 −6 bp. Kriptoya özgü değil."},
 {"ad": "Genel kütüphane: ortalamaya dönüş (RSI2, IBS, BB, 3 gün düşüş, 5 gün dip)", "neden": "BTC/ETH'de kenar yok ya da yalnız C0 h=1'de (kapanışa bağımlı); IBIT/ETHA'da net negatif ağırlıklı."},
 {"ad": "Genel kütüphane: VIX rejimi (backwardation, VIX sıçraması)", "neden": "VX_backwardation C1 h1 BTC_D IS/OOS kenarı pozitif (n=112, t=2,1) ama tek koşullu rejim, ETF'de t=1,7 ve n küçük; VIX 16:15 ET kapanır. Eşik altı."},
 {"ad": "BITO / BITX / BITI ay başı-ay sonu takvim satırları", "neden": "FDR geçen 'negatif' satırlar (BITO CA_ay_sonu_3 vb.) veri artefaktı: BITO dağıtımları veri kaynağında yok (ex-date boşlukları)."},
 {"ad": "MSTU, CONL, BLOK ürün düzeyinde", "neden": "MSTU: aşırı oynaklık/kaldıraç kaybı, kenar yok; CONL: 2,79$ fiyat → ~48 bp maliyet; BLOK: 14 mn$/gün, maliyet/oynaklık en kötü."},
]

ozet = ("Kripto ailesi (16 ETF; bağımsız dayanak sayısı fiilen 2-3: BTC, ETH, kripto hisseleri). İstatistiksel güç düşük: spot ETF'ler 2024-01+ (≈700 gün), birebir 16:00 ET BTC serisi 2023-06+; "
        "uzun test BTC/ETH günlük UTC mumuyla (2016-11..2026-11, 3-4 saat zaman kayması) yapıldı. Toplam ~{} test, BH-FDR q=0,10. "
        "KATI EŞİĞİ GÜVENLE GEÇEN STRATEJİ YOK. Biçimsel eşiği geçen iki DÜŞÜK güvenli aday: (S1) Perşembe gün içi ters BTC — SBIT'i Perşembe açılışında (TR 17:30) al, kapanışta sat: "
        "net 84 bp/işlem (t=2,40, n=133), dayanak satırları aile FDR'sini geçiyor, ama etki 2024-2025'e yoğun, öncesinde ≈0 ve 2026'da zayıf; "
        "(S2) BTC trend filtresi (kapanış>SMA10>SMA50) → IBIT 3 gün: BTC 10 yılda net 153 bp (t=3,4; IS 225 / OOS 58), ama FDR geçmiyor, kazanç çoğunlukla IS boğa piyasasından, IBIT döneminde t<1. "
        "Elenenler: IBIT 'gece primi' (maliyet sonrası ≈0), hafta sonu (takvim günü drift'i), haftalık momentum (OOS ≤0), ortalamaya dönüş, BTC→MSTR/COIN öncülüğü, ETF akımı (veri yok). "
        "İzleme: IBIT (kabul; Midas'ta yoksa GBTC — Midas'ta doğrulanmış), ETHA (kabul; yoksa ETHE — doğrulanmış), SBIT (kabul, S1 aracı), BITX/BITI/ETHU/FBTC yedek; BITO, BITB, ARKB, BITU, BLOK, MSTU, CONL red. "
        "Doğrulanmış gecikmeli öncü YOK; gerçek zamanlı izleme: COINBASE:BTCUSD (IBIT açılış boşluğunun %96'sını açıklar), CME:BTC1!, COINBASE:ETHUSD, CME_MINI:NQ1!. "
        "Kaldıraçlı long BTC/ETH ürünlerinde 2×'e göre ~8-12 bp/gün takip kaybı var.").format(n_tests)

dosyalar = [
 f"{NOT}",
 f"{SON}/sonuc.json",
 f"{KOD}/kr.py", f"{KOD}/01_islenebilirlik.py", f"{KOD}/02_genel_aile.py", f"{KOD}/03_hipotezler.py", f"{KOD}/04_leadlag.py", f"{KOD}/05_adaylar.py", f"{KOD}/06_sonuc_json.py",
 f"{SON}/islenebilirlik.csv", f"{SON}/kopya_korelasyon.csv", f"{SON}/genel_aile_satirlar.csv", f"{SON}/genel_aile_tutarlilik.csv", f"{SON}/genel_dayanak_satirlar.csv",
 f"{SON}/hipotez_testleri.csv", f"{SON}/gece_gunici.csv", f"{SON}/seans_getirileri.csv", f"{SON}/ibit_bosluk_btc_gece.csv", f"{SON}/kaldirac_kaybi.csv", f"{SON}/persembe_gunici.csv",
 f"{SON}/leadlag_aile.csv", f"{SON}/leadlag_ek_testler.csv", f"{SON}/leadlag_kural_testleri.csv",
 f"{SON}/aday_detay.csv", f"{SON}/aday_kripto_S1_islemler.csv", f"{SON}/aday_kripto_S2_islemler.csv", f"{SON}/fdr_tum.csv",
 f"{SON}/02_log.txt", f"{SON}/03_log.txt", f"{SON}/04_log.txt", f"{SON}/05_log.txt",
]

out = {"family": "kripto", "ozet": ozet, "izleme": izleme, "stratejiler": strat, "elenen": elenen, "leadlag": leadlag, "dosyalar": dosyalar,
       "tv_dogrulanacak": ["DERIBIT:DVOL (BTC örtük oynaklık endeksi; isteğe bağlı izleme, kod doğrulanmadı)"]}
json.dump(out, open(os.path.join(O, "sonuc.json"), "w"), ensure_ascii=False, indent=1)
print("yazıldı", os.path.join(O, "sonuc.json"), "test sayısı", n_tests)
