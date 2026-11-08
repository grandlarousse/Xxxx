"""Sonuç JSON'unu (sonuc.json) hesaplanmış tablolardan üretir (sayılar dosyalardan okunur, elle yazılmaz).
Önce: b0, b0b, b1, t1, t2, t3, t4, t5, t5b, t7, aday_S1, t6 çalışmış olmalı.
Çalıştırma: python3 -I kod/ajan_tek_hisse_kaldiracli/t8_sonuc.py"""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import thk

O = thk.OUT; R = thk.ROOT
def rd(fn, **k): return pd.read_csv(os.path.join(O, fn), **k)
def f1(x, d=1):
    if x is None or (isinstance(x, float) and not np.isfinite(x)): return "yok"
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
def num(x, d=2):
    return None if x is None or (isinstance(x, float) and not np.isfinite(x)) else round(float(x), d)

ISL = rd("islenebilirlik.csv").set_index("sym")
S1 = rd("aday_S1_ozet.csv")
HE = rd("aday_S1_hisse_etf.csv")
FDR = rd("fdr_tum_testler.csv")
HYP = rd("hipotez_testleri.csv")
BT = rd("bilanco_testleri.csv") if os.path.exists(os.path.join(O, "bilanco_testleri.csv")) else None
GB = rd("gelecek_bilanco.csv") if os.path.exists(os.path.join(O, "gelecek_bilanco.csv")) else None
DRV = rd("leadlag_suruculer.csv")
LLX = rd("leadlag_ek_regresyon.csv")
NIGHT = rd("btc_gece_acilis.csv").set_index("hisse")
LLK = rd("oncu_kural_testleri.csv")
TH01 = rd("th01_oynaklik_kaybi.csv")

def s1(test, mode):
    r = S1[(S1.test == test) & (S1["mode"] == mode)]
    return r.iloc[0] if len(r) else None

ntest = len(FDR); thr = FDR[FDR.fdr].p.max() if FDR.fdr.any() else float("nan")
ngec = int(FDR.fdr.sum()); ngec_pos = int((FDR.fdr & (FDR.t > 0)).sum())
hp = HYP[HYP.duzey == "havuz"]
th03 = hp[(hp.hipotez == "TH03_rsi2_trend_sma5cikis")].set_index("mode")
c0 = s1("dayanak_7", "C0"); o1 = s1("dayanak_7", "O1"); c1 = s1("dayanak_7", "C1")
gC0 = s1("gercek_etf_tum", "C0"); gO1 = s1("gercek_etf_tum", "O1"); gC1 = s1("gercek_etf_tum", "C1")
g2C0 = s1("gercek_etf_2x_donemi", "C0"); g2O1 = s1("gercek_etf_2x_donemi", "O1")
m1k = s1("maliyet_1000", "C0"); m10k = s1("maliyet_10000", "C0"); m1kO = s1("maliyet_1000", "O1"); m10kO = s1("maliyet_10000", "O1")
kr = s1("dayanak_kripto", "C0")
b_d = s1("bilanco_dahil", "C0"); b_h = s1("bilanco_haric", "C0"); b_y = s1("bilanco_yalniz", "C0")
b_hO = s1("bilanco_haric", "O1"); b_hg = s1("bilanco_haric_gercek_etf", "C0")
kom = S1[S1.test.str.startswith("komsu_")]
kom_pos = int((kom.net_bp > 0).sum()); kom_t2 = int((kom.t >= 2).sum())

hs = HE[(HE.veri == "dayanak_sentetik") & (HE["mode"] == "C0")].set_index("stock")
ge = HE[(HE.veri == "gercek_etf_tum") & (HE["mode"] == "C0")].set_index("etf")
hisse_txt = "; ".join(f"{st}->{hs.loc[st,'etf']} n={int(hs.loc[st,'n'])} net {f1(hs.loc[st,'mean_net_bp'],0)} bp t={f1(hs.loc[st,'t'],2)}" for st in hs.index)
etf_txt = "; ".join(f"{e} n={int(ge.loc[e,'n'])} net {f1(ge.loc[e,'mean_net_bp'],0)} t={f1(ge.loc[e,'t'],2)}" for e in ge.index)

fdr_txt = (f"Birleşik BH-FDR q=0,10, toplam {ntest} test (genel_tum aile satırları + dayanak genel kütüphane hisse ve havuz satırları + "
           f"hipotez, öncü-kural, lead-lag regresyon, bilanço ve S1 kontrol testleri): eşik p<={thr:.1e}, geçen {ngec} (pozitif {ngec_pos}; hepsi tek hisse satırı, seçim). "
           f"S1 ana satırı (C0 havuz) p={th03.loc['C0','p']:.4f}: birleşik FDR'yi GEÇMEZ. Ön-kayıtlı hipotez ailesi içinde ({len(hp)} havuz testi) GEÇER "
           f"(C0 ve O1 havuz satırları fdr_havuz=True).")

S1J = {
    "id": "tek_hisse_kaldiracli_S1",
    "ad": "Mega-cap hisse RSI(2) dibi (hisse 200 günlük ortalamanın üstünde) -> 2x tek hisse ETF, SMA5'e dönüşte çıkış (en çok 3 gün)",
    "kural": ("TradingView günlük grafik, sinyal DAYANAK HİSSENİN verisinden (ETF'nin kendi fiyatından değil): NASDAQ:NVDA, NASDAQ:TSLA, NASDAQ:AAPL, "
              "NASDAQ:AMZN, NASDAQ:META, NASDAQ:MSFT, NASDAQ:GOOGL. Göstergeler (kaynak: kapanış): RSI uzunluk 2 (standart Wilder RSI), SMA 200, SMA 5. "
              "Giriş sinyali t günü: hisse RSI(2) < 10 VE hisse kapanışı > hisse SMA(200). İşlem aracı (aynı hissenin 2x ETF'i): NVDA->NASDAQ:NVDL, "
              "TSLA->NASDAQ:TSLL, AAPL->NASDAQ:AAPU, AMZN->NASDAQ:AMZU, META->NASDAQ:METU, MSFT->NASDAQ:MSFU, GOOGL->NASDAQ:GGLL. "
              "Çıkış: girişten sonraki işlem günlerinde hisse kapanışı > hisse SMA(5) olan ilk gün kapanışta sat; olmazsa girişten sonraki 3. işlem günü "
              "kapanışında sat. Aynı hissede pozisyondayken gelen yeni sinyal yok sayılır; hisseler birbirinden bağımsız işlenir (aynı anda birden çok pozisyon "
              "olabilir: medyan 2, en çok 7). Stop yok (backtest stopsuz). Bilanço: tutuş içinde bilanço tepki günü olan işlemler ayrıca raporlandı (bkz. notlar)."),
    "giris": ("C0 (ana): sinyal günü kapanıştan hemen önce (TR kış 23:45-23:58, yaz 22:45-22:58) hissenin canlı fiyatıyla RSI(2) ve SMA200'ü kontrol edip ETF'i "
              "normal seansta piyasa ya da agresif limit emirle al (Midas'ta MOC/LOC yok). RSI(2) son fiyata çok duyarlı: eşiğe yakınsa O1'i kullan. "
              "O1 (yedek, kapanış izlemeye gerek yok): ertesi gün açılışta al, TR kış 17:30 (yaz 16:30); pre-market (TR kış 12:00-17:30) yalnız limit emir."),
    "tutus": "En çok 3 işlem günü (ortalama 2,5 gün: işlemlerin %62'si 3 gün, %22'si 2 gün, %15'i 1 gün).",
    "cikis": ("Her işlem günü kapanıştan hemen önce (TR kış 23:45-23:58, yaz 22:45-22:58) hisse fiyatı kendi SMA(5)'inin üstündeyse ETF'i sat; değilse "
              "sinyal gününden sonraki 3. işlem günü (t+3) aynı saatte sat. C0'da kontrol t+1, t+2, t+3 kapanışlarında; O1'de giriş günü (t+1) kapanışından "
              "itibaren, en geç t+3. Kapanış sonrası (TR kış 00:00-04:00) yalnız limit emirle satılabilir; backtest kapanış fiyatını kullanır."),
    "islem_etf": ["NVDL", "TSLL", "AAPU", "AMZU", "METU", "MSFU", "GGLL"],
    "sinyal_etf": "Dayanak hisseler: NASDAQ:NVDA, NASDAQ:TSLA, NASDAQ:AAPL, NASDAQ:AMZN, NASDAQ:META, NASDAQ:MSFT, NASDAQ:GOOGL",
    "n": int(c0.n), "brut_bp": num(c0.brut_bp, 1), "net_bp": num(c0.net_bp, 1), "t": num(c0.t, 2),
    "is_net_bp": num(c0.is_net_bp, 1), "oos_net_bp": num(c0.oos_net_bp, 1), "kazanma": num(c0.kazanma, 3), "pf": num(c0.pf, 2),
    "maxdd": num(c0.maxdd_portfoy_1_7, 3), "en_kotu_bp": num(c0.en_kotu_bp, 0), "yil_pozitif": num(c0.yil_poz, 2),
    "test_sayisi": ntest, "fdr": fdr_txt,
    "maliyet_duyarlilik": (f"Dayanak havuzu C0: 1.000$ {f1(m1k.net_bp)} bp (t={f1(m1k.t,2)}), 2.500$ {f1(c0.net_bp)} bp (t={f1(c0.t,2)}), 10.000$ {f1(m10k.net_bp)} bp (t={f1(m10k.t,2)}). "
                           f"O1: {f1(m1kO.net_bp)} / {f1(o1.net_bp)} / {f1(m10kO.net_bp)} bp. Gidiş-dönüş maliyet 16-23 bp (TSLL 23 bp: 8,8$ fiyatta 1 sentlik adım ~11 bp makas). "
                           f"Ortalama brüt kenar ({f1(c0.brut_bp,0)} bp) maliyetin ~6-8 katı."),
    "mod_saglamlik": (f"Dayanak havuzu (2016-11..2026-11, sentetik kalibre 2x): C0 net {f1(c0.net_bp)} bp t={f1(c0.t,2)} (IS {f1(c0.is_net_bp)} t={f1(c0.is_t,2)}, OOS {f1(c0.oos_net_bp)} t={f1(c0.oos_t,2)}); "
                      f"O1 {f1(o1.net_bp)} t={f1(o1.t,2)} (IS {f1(o1.is_net_bp)}, OOS {f1(o1.oos_net_bp)}); C1 {f1(c1.net_bp)} t={f1(c1.t,2)} (IS {f1(c1.is_net_bp)}, OOS {f1(c1.oos_net_bp)}). "
                      f"Zamanlama kenarı (aynı tutuş süreli koşulsuz getiri düşülmüş): C0 {f1(c0.edge_eslenik_bp)} bp t={f1(c0.t_edge_eslenik,2)}, O1 {f1(o1.edge_eslenik_bp)} bp t={f1(o1.t_edge_eslenik,2)}, "
                      f"C1 {f1(c1.edge_eslenik_bp)} bp t={f1(c1.t_edge_eslenik,2)}: kenar ilk günlerde, gecikmeli girişte (C1) yarıya iner. "
                      f"Gerçek ETF verisi (2022+, sinyal hisseden): C0 {f1(gC0.net_bp)} bp t={f1(gC0.t,2)} (n={int(gC0.n)}), O1 {f1(gO1.net_bp)} t={f1(gO1.t,2)}, C1 {f1(gC1.net_bp)} t={f1(gC1.t,2)}; "
                      f"yalnız 2x dönemi (2024+): C0 {f1(g2C0.net_bp)} t={f1(g2C0.t,2)}, O1 {f1(g2O1.net_bp)} t={f1(g2O1.t,2)}. Kapanışa bağımlı değil (O1'de de çalışıyor)."),
    "aile_ici": (f"Dayanak (C0, hisse başına): {hisse_txt}. 7/7 pozitif, tek başına t>=2 yalnız MSFT: kanıt havuzdan geliyor. "
                 f"Gerçek ETF (C0, 2022+, 2022-24'te Direxion/GraniteShares ürünleri 1,5x idi): {etf_txt}. "
                 f"Kopya NVDU: NVDL ile aynı sonuç (bağımsız kanıt değil). Kripto vekilleri (MSTR/COIN, TH03 kapsamı dışı): n={int(kr.n)} net {f1(kr.net_bp)} bp t={f1(kr.t,2)} (COIN negatif) -> MSTU/CONL'e uygulanmaz. "
                 f"Ayna: aynı sinyalle ters ETF almak NVDS -324 bp (t=-3,33), TSLQ -194 bp (t=-0,98): beklenen yönde. "
                 f"Komşu parametreler (RSI<5/10/15, trend filtresi var/yok, SMA5 çıkış ya da sabit 1-3 gün; C0 ve O1, {len(kom)} varyant): {kom_pos} pozitif, {kom_t2} tanesi t>=2; "
                 f"RSI<5 ve trend filtresiz varyantlar benzer ya da biraz daha iyi, RSI<15 ve sabit 1 gün zayıf. Parametre seçilmedi (TH03 ön-kayıtlı). "
                 f"Genel kütüphanedeki aynı kural ETF'nin KENDİ fiyatıyla hesaplanınca zayıf (genel_tum: MR_rsi2_lt10_ust200 C0 h3 erken çıkışlı, 9 ETF ort. +12 bp): "
                 f"sinyali hisseden hesapla."),
    "guven": "dusuk",
    "betik": "python3 -I /home/user/Xxxx/raporlar/2026-11-07_midas_etf_1-3gun/kod/ajan_tek_hisse_kaldiracli/aday_S1.py",
    "notlar": None,
}
yr = None
try:
    A = pd.read_csv(os.path.join(O, "aday_S1_islemler_dayanak_C0.csv"), parse_dates=["sig_date"])
    g = A.groupby("sig_date")["net"].mean(); yr = (g.groupby(g.index.year).sum() * 1e4).round(0).astype(int).to_dict()
except Exception:
    pass
bil_txt = ""
if b_d is not None and b_h is not None:
    bil_txt = (f" BİLANÇO (önemli): işlemlerin {int(b_y.n)}'ü (~%4) tutuşta bir bilanço tepki gününü taşıyor ve ortalama {f1(b_y.net_bp,0)} bp (t={f1(b_y.t,2)}, en kötü {f1(b_y.en_kotu_bp,0)} bp) getiriyor. "
               f"Bunlar çıkarılınca C0 n={int(b_h.n)} net {f1(b_h.net_bp)} bp t={f1(b_h.t,2)} (IS {f1(b_h.is_net_bp)} t={f1(b_h.is_t,2)}, OOS {f1(b_h.oos_net_bp)} t={f1(b_h.oos_t,2)}), "
               f"O1 {f1(b_hO.net_bp)} t={f1(b_hO.t,2)}, gerçek ETF C0 {f1(b_hg.net_bp)} t={f1(b_hg.t,2)}; zamanlama kenarı ~47 bp t~1,35-1,49 (anlamsız). "
               f"Yani sürüklenme dışı kenarın önemli kısmı az sayıda bilanço öncesi dip işleminden geliyor. Muhafazakâr kullanım: tutuş içinde bilanço (seans sonrası duyuru) varsa girme "
               f"ya da duyuru günü kapanıştan önce çık (TH04).")
S1J["notlar"] = (f"Yıllık (sinyal tarihi başına ort. net, bp toplamı): {yr}. Negatif yıllar 2022 ve 2025 (ayı/sert düşüş dönemlerinde dip alımı tekrar tekrar zarar). "
                 f"En kötü işlem {f1(c0.en_kotu_bp,0)} bp (TSLA 2x, ~-%45); hisse başına maxDD %18-%72 (TSLA); 1/7 sermaye kaba portföy maxDD {f1(100*c0.maxdd_portfoy_1_7,1)}%. "
                 f"Sinyaller piyasa geneli düşüşlerde kümelenir (eşzamanlı 7 pozisyona kadar): pozisyon başına sermayeyi buna göre böl. "
                 f"Kanıt sınırlılıkları: (1) dayanak evreni sonradan kazananlardan oluşuyor (hayatta kalma/seçim yanlılığı): net getirinin bir kısmı 2016-2026 mega-cap yükselişi; "
                 f"zamanlama kenarı ~74-76 bp ve t~2,1 (C0/O1), bilanço işlemleri hariç ~47 bp t~1,4. (2) Birleşik FDR'yi geçmiyor. (3) 2x ETF 1-3 günde 2x hisseden 9-14 bp geride (finansman/ücret; TH01). "
                 f"(4) Midas'ta bu ETF'lerin bulunurluğu resmî olarak doğrulanamadı. Son veri (06.11.2026): 7 hissenin hiçbirinde sinyal yok; NVDA, TSLA SMA200 altında (filtre kapalı).{bil_txt}")

# ---------------- izleme ----------------
TV = pd.read_csv(os.path.join(R, "sonuclar", "tv_etf.csv")).drop_duplicates("sym").set_index("sym")["tv"].to_dict()
def ratio(e): return f1(ISL.loc[e, "maliyet_vol_orani"], 3)
def r1y(e): return f1(100 * ISL.loc[e, "ret_1y"], 0)
def w1(e): return f1(100 * ISL.loc[e, "worst_1d_1y"], 1)
IZ = []
basket = {"NVDL": "NVDA", "TSLL": "TSLA", "AAPU": "AAPL", "AMZU": "AMZN", "METU": "META", "MSFU": "MSFT", "GGLL": "GOOGL"}
for e, st in basket.items():
    extra = {"NVDL": "NVDA 2x'lerin en likidi (NVDU'dan 13 kat hacim, daha dar makas).",
             "TSLL": "Fiyat 8,8$: 1 sentlik adım ~11 bp makas, maliyet 23 bp (ailede CONL'den sonra en yüksek).",
             "AAPU": "AAPL en düşük oynaklıklı dayanak: S1 kenarı en zayıf (C0 +54 bp, t=0,93).",
             "AMZU": "", "METU": "Gerçek ETF geçmişi kısa (2024-06+); S1 gerçek veride n=21, -45 bp (dayanakta +45 bp).",
             "MSFU": "S1'de en güçlü dayanak (MSFT C0 +141 bp, t=2,28) ama tek başına seçme: havuzla uygula.",
             "GGLL": ""}[e]
    IZ.append({"sym": e, "tv": TV.get(e), "karar": "kabul",
               "gerekce": (f"S1 sepetinin {st} aracı (sinyal NASDAQ:{st}). Medyan günlük hacim {f1(ISL.loc[e,'med_dolar_hacim_mn'],0)} mn$, maliyet {f1(ISL.loc[e,'maliyet_rt_bp_2500'],1)} bp, "
                           f"maliyet/1g oynaklık {ratio(e)}. Gerçekleşen kaldıraç son 1y {f1(ISL.loc[e,'beta_1y'],2)} (2024 başına kadar 1,5x idi). 1y getiri %{r1y(e)}, son 1y en kötü gün %{w1(e)}. {extra} "
                           f"Midas'ta bulunurluğu resmî doğrulanmadı."),
               "likidite_mn_usd": num(ISL.loc[e, "med_dolar_hacim_mn"], 1), "maliyet_bp": num(ISL.loc[e, "maliyet_rt_bp_2500"], 1), "vol_1d_bp": num(ISL.loc[e, "vol_1d_bp"], 1)})
mstu_d = TH01[(TH01.etf == "MSTU") & (TH01.h == 3) & (TH01.kova == "tum")].iloc[0]
IZ += [
    {"sym": "NVDU", "tv": TV.get("NVDU"), "karar": "yedek",
     "gerekce": f"NVDL'nin kopyası (aynı dayanak, 2x; günlük getiri korelasyonu 1,00). Hacim {f1(ISL.loc['NVDU','med_dolar_hacim_mn'],0)} mn$, maliyet {f1(ISL.loc['NVDU','maliyet_rt_bp_2500'],0)} bp (NVDL 16 bp). Yalnız Midas'ta NVDL yoksa S1 için.",
     "likidite_mn_usd": num(ISL.loc["NVDU", "med_dolar_hacim_mn"], 1), "maliyet_bp": num(ISL.loc["NVDU", "maliyet_rt_bp_2500"], 1), "vol_1d_bp": num(ISL.loc["NVDU", "vol_1d_bp"], 1)},
    {"sym": "MSTU", "tv": TV.get("MSTU"), "karar": "yedek",
     "gerekce": (f"Doğrulanmış strateji YOK (S1 MSTR'de n=68, t=0,78; TH06 BTC öncülüğü yok). Yalnız net sürücüyle takip edilebilir: BTC (corr_1y 0,86); BTC'nin gece hareketi "
                 f"(16:00->09:00 ET) MSTR açılış boşluğu varyansının %{f1(100*NIGHT.loc['MSTR','r2'],0)}'ini açıklıyor. Maliyet/oynaklık oranı ailede en iyi ({ratio('MSTU')}) "
                 f"ama 3 günlük tutuşta 2xMSTR'den ort. {f1(mstu_d.basit_sapma_ort_bp,0)} bp geride (swap finansmanı), 1y getiri %{r1y('MSTU')}, son 1y en kötü gün %{w1('MSTU')}. "
                 f"Çok küçük pozisyon dışında önerilmez."),
     "likidite_mn_usd": num(ISL.loc["MSTU", "med_dolar_hacim_mn"], 1), "maliyet_bp": num(ISL.loc["MSTU", "maliyet_rt_bp_2500"], 1), "vol_1d_bp": num(ISL.loc["MSTU", "vol_1d_bp"], 1)},
    {"sym": "CONL", "tv": TV.get("CONL"), "karar": "red",
     "gerekce": (f"Fiyat {f1(ISL.loc['CONL','fiyat'],2)}$: 1 sentlik adım ~36 bp makas, maliyet {f1(ISL.loc['CONL','maliyet_rt_bp_2500'],0)} bp (ailede en yüksek). 1y getiri %{r1y('CONL')}. "
                 f"COIN'de S1 negatif (n=31, -71 bp); BTC öncülüğü yok. Kripto maruziyeti için MSTU daha ucuz."),
     "likidite_mn_usd": num(ISL.loc["CONL", "med_dolar_hacim_mn"], 1), "maliyet_bp": num(ISL.loc["CONL", "maliyet_rt_bp_2500"], 1), "vol_1d_bp": num(ISL.loc["CONL", "vol_1d_bp"], 1)},
    {"sym": "TSLQ", "tv": TV.get("TSLQ"), "karar": "red",
     "gerekce": ("Ters TSLA (2024-07'den beri -2x; öncesi -1x; tarama.csv 'lev=-1' eski). Ailede doğrulanmış kısa yön sinyali yok: büyük yükseliş sonrası ters "
                 "(TH02c) C0 h2 -253 bp, RSI2>90 ve SMA200 altı (TH07) -44 bp, S1 aynası -194 bp. Uzun dönem pozitif sürüklenmeye karşı pozisyon."),
     "likidite_mn_usd": num(ISL.loc["TSLQ", "med_dolar_hacim_mn"], 1), "maliyet_bp": num(ISL.loc["TSLQ", "maliyet_rt_bp_2500"], 1), "vol_1d_bp": num(ISL.loc["TSLQ", "vol_1d_bp"], 1)},
    {"sym": "NVDS", "tv": TV.get("NVDS"), "karar": "red",
     "gerekce": (f"Ters NVDA (-1,5x; 2024-07 öncesi -1,25x). Hacim yalnız {f1(ISL.loc['NVDS','med_dolar_hacim_mn'],1)} mn$, maliyet {f1(ISL.loc['NVDS','maliyet_rt_bp_2500'],0)} bp, maliyet/oynaklık 0,075 (ailede en kötü). "
                 "Büyük NVDA yükselişinden sonra NVDS almak (TH02c) C0 h2 -254 bp t=-3,05 (FDR'de anlamlı ZARAR); S1 aynası -324 bp t=-3,33."),
     "likidite_mn_usd": num(ISL.loc["NVDS", "med_dolar_hacim_mn"], 1), "maliyet_bp": num(ISL.loc["NVDS", "maliyet_rt_bp_2500"], 1), "vol_1d_bp": num(ISL.loc["NVDS", "vol_1d_bp"], 1)},
]

# ---------------- lead-lag ----------------
LLtv = {"SPY": "AMEX:SPY", "QQQ": "NASDAQ:QQQ", "XLK": "AMEX:XLK", "SMH": "NASDAQ:SMH"}
ll2 = LLK[(LLK.duzey == "havuz") & (LLK.hipotez == "LL2_SPY_z_lt_m2")].set_index(["mode", "h"])
ll1 = LLK[(LLK.duzey == "havuz") & (LLK.hipotez == "LL1_QQQ_z_lt_m2")].set_index(["mode", "h"])
kural_txt = (f"Kurala çevrildiğinde (piyasa sert düşüş günü z<-2 -> 2x hisse ETF long, 9 dayanak havuzu): SPY C0 h1 {f1(ll2.loc[('C0',1),'mean_net_bp'],0)} bp t={f1(ll2.loc[('C0',1),'t'],2)}, "
             f"O1 h1 {f1(ll2.loc[('O1',1),'mean_net_bp'],0)} bp t={f1(ll2.loc[('O1',1),'t'],2)}; QQQ O1 h1 {f1(ll1.loc[('O1',1),'mean_net_bp'],0)} bp t={f1(ll1.loc[('O1',1),'t'],2)} (yalnız bu varyant), "
             f"C0/C1 ve h2-3 anlamsız; gerçek ETF'de (2022+) C0 negatif. İşlem için doğrulanmadı.")
BIL = pd.read_csv(os.path.join(O, "bilanco_tarihleri.csv"), parse_dates=["date"])
def gb_txt(st):
    r = GB[GB.sym == st] if GB is not None else pd.DataFrame()
    if not len(r) or pd.isna(r.iloc[0].tarih):
        b = BIL[(BIL.sym == st) & (BIL.date.dt.month.isin([1, 2])) & (BIL.date.dt.year >= 2023) & (~BIL.kaynak.str.startswith("tahmini"))]
        if len(b):
            lo = b.date.dt.strftime("%d.%m").min(); hi = b.date.dt.strftime("%d.%m").max()
            return (f"{st} sonraki bilanço tarihi henüz açıklanmadı (Nasdaq boş); 2023-2026 düzenine göre yaklaşık {lo}-{hi}.2027 arası, seans sonrası "
                    f"(tepki ertesi gün açılış boşluğunda). Son duyuru {BIL[BIL.sym == st].date.max().date()}.")
        return f"{st} sonraki bilanço tarihi alınamadı."
    r = r.iloc[0]
    z = {"seans_sonrasi": "seans sonrası (16:00 ET sonrası; TR kış 00:00 sonrası)", "seans_oncesi": "seans öncesi"}.get(r.zaman, "saat belirtilmemiş")
    return f"{st} sonraki bilanço {r.tarih} {z}{' (Nasdaq/Zacks tahmini)' if r.tahmini_mi else ''}."
TAKVIM = ("Yaklaşan ortak olaylar: CPI 10.11.2026 08:30 ET (TR 16:30, açılıştan önce); opsiyon aylık vadesi 20.11.2026; ABD kapalı 26.11.2026, "
          "27.11.2026 erken kapanış 13:00 ET (TR 21:00); NFP 04.12.2026 08:30 ET (TR 16:30); CPI 10.12.2026; FOMC 09.12.2026 14:00 ET (TR 22:00); "
          "triple witching 18.12.2026; 24.12 erken kapanış, 25.12 kapalı.")
LL = []
for e in ["NVDL", "TSLL", "AAPU", "AMZU", "METU", "MSFU", "GGLL", "NVDU", "MSTU"]:
    st = thk.UNDER[e]
    d = DRV[DRV.etf == e]
    sur = [{"ad": (f"{r.surucu} (dayanak hisse, aynı gün)" if r.kaynak == "dayanak" else f"{r.surucu} günlük getiri (aynı gün)"),
            "tv": (r.tv if isinstance(r.tv, str) and r.tv else ""), "corr_1y": num(r.corr_1y, 3), "beta_1y": num(r.beta_1y, 3)} for _, r in d.iterrows() if isinstance(r.tv, str) and r.tv]
    onc = []
    x = LLX[(LLX.hisse == st) & (LLX.gecerli_oncu)]
    for _, r in x.sort_values("t").iterrows():
        nm = {"lag": f"{r.oncu} günlük getirisi (t) -> {st} t+1 getirisi, kendi getirisi kontrollü",
              "yetisme": f"{r.oncu}'ya göre geride kalma (beta60 x r_{r.oncu} - r_{st}) (t) -> {st} t+1"}[r.tip]
        onc.append({"ad": nm, "tv": LLtv.get(r.oncu, ""), "tip": f"gecikmeli ({r.tip}), NEGATİF katsayı",
                    "etki": f"1 sd {r.oncu} hareketi -> 2x ETF'te ertesi gün {f1(r.etki_2x_bp_per_sd,0)} bp (ters yönde); maliyet {f1(r.maliyet_rt_bp,0)} bp",
                    "t": num(r.t, 2), "is_t": num(r.t_IS, 2), "oos_t": num(r.t_OOS, 2), "fdr": True, "ufuk": "1 gün",
                    "maliyet_sonrasi": ("FDR yalnız 152 testlik ek lead-lag ailesinde geçiyor, birleşik FDR'de geçmiyor; OOS t zayıf. " + kural_txt)})
    gz = [{"ad": f"{st} uzatılmış seans (pre-market 04:00-09:30 ET = TR kış 12:00-17:30; after-hours 16:00-20:00 ET = TR kış 00:00-04:00)", "tv": thk.TV_STOCK[st],
           "neden": "ETF'nin açılış boşluğunun ana kaynağı hissenin kendi gece fiyatı (2x). TradingView'da 'uzatılmış saatler' açılmalı; bilanço tepkisi after-hours'ta görülür."},
          {"ad": "Nasdaq 100 E-mini vadelisi", "tv": "CME_MINI:NQ1!", "neden": "Neredeyse 24 saat işler; ETF kapalıyken piyasa yönünü ve açılış boşluğunu önceden gösterir (öncü değil, izleme)."},
          {"ad": "S&P 500 E-mini vadelisi", "tv": "CME_MINI:ES1!", "neden": "Genel piyasa gece riski (makro veri 08:30 ET = TR 16:30, açılıştan önce)."}]
    if st == "NVDA":
        gz.append({"ad": "Nikkei 225 vadelisi (OSE)", "tv": "OSE:NK2251!", "neden": "Asya seansındaki teknoloji/yarı iletken risk iştahı (zayıf, yalnız bağlam)."})
    if st == "MSTR":
        gz = [{"ad": "Bitcoin spot (Coinbase)", "tv": "COINBASE:BTCUSD",
               "neden": f"7/24 işler. BTC'nin 16:00 ET -> ertesi 09:00 ET hareketi MSTR açılış boşluğuyla corr {f1(NIGHT.loc['MSTR','corr_btc_gece_vs_acilis_boslugu'],2)}, beta {f1(NIGHT.loc['MSTR','beta'],2)} (MSTU ≈ 2x): gece BTC %5 düşerse MSTU açılışı ~%12 aşağı beklenir."},
              {"ad": "CME Bitcoin vadelisi", "tv": "CME:BTC1!", "neden": "Kurumsal BTC fiyatı; hafta sonu kapalı (Pazar akşamı açılış boşluğu)."},
              {"ad": "MSTR uzatılmış seans", "tv": "NASDAQ:MSTR", "neden": "Pre-market TR kış 12:00-17:30."},
              {"ad": "Ethereum spot", "tv": "COINBASE:ETHUSD", "neden": "Kripto risk iştahının ikinci göstergesi."},
              {"ad": "Nasdaq 100 E-mini vadelisi", "tv": "CME_MINI:NQ1!", "neden": "Genel risk iştahı."}]
    note = ("İşlem için doğrulanmış gecikmeli öncü yok. Genel taramada (leadlag_sweep.csv, aile hedefleri 576 satır) FDR bayrağı 0. "
            "Ek dayanak testinde (2016+, kendi gecikmesi kontrollü, Newey-West) bulunan ilişkiler NEGATİF işaretli piyasa-geri dönüşü (piyasa bugün yükselirse "
            "hisse ertesi gün piyasa kısmını kısmen geri veriyor); OOS'ta zayıf ve kurala çevrilince maliyet sonrası doğrulanmıyor. "
            "Eşzamanlı sürücüler (dayanak hisse, QQQ, XLK, SPY) aynı gün hareket eder, öncü değildir.")
    if st == "MSTR":
        note = ("Doğrulanmış gecikmeli öncü yok. TH06: BTC 16:00 ET artığı -> MSTR ertesi gün t=-0,98 (h1), BTC getirisi t=-1,26, yetişme boşluğu t=-0,89 (2023-06+, IS yok). "
                "Kural testi (u>=2sd -> 2x long, C0 h1) n=45 +213 bp t=0,85. BTC yalnız eşzamanlı sürücü ve gerçek zamanlı izleme aracıdır.")
    if st == "NVDA":
        note += " NVDL <- SMH: SMH getirisi -> NVDA t+1 t=-1,72 (IS -2,69, OOS +0,30), yetişme t=-2,08 (OOS -0,13); kural (yetişme>=2sd, C0 h1) +68 bp t=0,55: öncü değil."
    LL.append({"sym": e, "suruculer": sur, "onculer": onc, "gercek_zamanli": gz, "not": note,
               "takvim_riskleri": (gb_txt(st) + " " + TAKVIM)})

# ---------------- elenenler ----------------
def hrow(h, m, hh):
    r = hp[(hp.hipotez == h) & (hp["mode"] == m) & (hp.h == hh)]
    return r.iloc[0] if len(r) else None
EL = []
r = hrow("TH02a_buyuk_dusus_long_4", "C0", 2); r5 = hrow("TH02a_buyuk_dusus_long_diger5", "C0", 2)
EL.append({"ad": "TH02a büyük düşüş günü (r<=-2,5σ20) sonrası 2x long, C_t -> C_t+2 (NVDA/TSLA/MSTR/COIN)",
           "neden": f"Ön-kayıtlı C0 h2: n={int(r.n)} net {f1(r.mean_net_bp,0)} bp t={f1(r.t,2)} (eşik altı); C0 h1 t=2,31 ama C1 negatif; diğer 5 dayanakta C0 h2 {f1(r5.mean_net_bp,0)} bp, OOS {f1(r5.oos_net_bp,0)} bp: ailede tutarsız."})
r = hrow("TH02b_buyuk_yukselis_long_4", "C0", 2); rn = hrow("TH02c_buyuk_yukselis_ters_nvda", "C0", 2); rt = hrow("TH02c_buyuk_yukselis_ters", "C0", 2)
EL.append({"ad": "TH02b/c büyük yükseliş günü sonrası dönüş (long kapat / ters ETF al)",
           "neden": f"Dönüş yok, tersine devam: 2x long C0 h2 {f1(r.mean_net_bp,0)} bp (t={f1(r.t,2)}). Ters ETF almak zarar: NVDS sentetik {f1(rn.mean_net_bp,0)} bp t={f1(rn.t,2)} (FDR'de anlamlı zarar), TSLQ sentetik {f1(rt.mean_net_bp,0)} bp."})
r = hrow("TH05_opex_haftasi", "C0", 5)
EL.append({"ad": "TH05 opsiyon vadesi haftası (vade öncesi Cuma -> OE haftası Çarşamba), NVDA/TSLA/AAPL 2x",
           "neden": f"Net {f1(r.mean_net_bp,0)} bp t={f1(r.t,2)} ama koşulsuz sürüklenmeye göre kenar {f1(r.edge_bp,0)} bp t={f1(r.t_edge,2)}: zamanlama değeri yok; diğer 6 dayanakta t=0,72. abd_endeks ailesinde de elendi."})
r = hrow("TH06_btc_artik_u_ge2sd", "C0", 1)
EL.append({"ad": "TH06 BTC@16:00 ET artığı -> MSTU/CONL ertesi gün",
           "neden": f"Regresyonda öncülük yok (t -0,9 ile -1,3, 2023-06+). Kural C0 h1 n={int(r.n)} {f1(r.mean_net_bp,0)} bp t={f1(r.t,2)}; IS yok, n küçük."})
r = hrow("TH01_kurali_TH03_uzerinde", "C0", 3)
EL.append({"ad": "TH01 kuralı (tahmini 3 günlük oynaklık kaybı >%0,5 ise 1 gün tut) S1 üzerinde",
           "neden": f"S1'i kötüleştiriyor: 9 dayanakta {f1(r.mean_net_bp,0)} bp (t={f1(r.t,2)}) vs kuralsız ~109 bp. 1-3 günde basit getiride beklenen sapma oynaklıktan değil finansman/ücretten geliyor (mega-cap 2x: 3 günde 9-14 bp; MSTU 57 bp)."})
r = hrow("SMH_NVDA_yetisme_ge2sd", "C0", 1)
EL.append({"ad": "NVDL <- SMH yetişme (NVDA, SMH'nin beta-ima ettiği hareketin gerisinde kaldıysa al)", "neden": f"C0 h1 n={int(r.n)} {f1(r.mean_net_bp,0)} bp t={f1(r.t,2)}; regresyonda işaret negatif ve OOS sıfır."})
for h in ("TH07_ters_rsi2_gt90_ayi_tsla", "TH07_ters_rsi2_gt90_ayi_nvda"):
    r = hrow(h, "C0", 2)
    EL.append({"ad": f"{h.replace('_', ' ')} (aşırı alım + SMA200 altı -> ters ETF, ek hipotez)", "neden": f"C0 h2 {f1(r.mean_net_bp,0)} bp t={f1(r.t,2)}; tüm varyantlar zayıf/negatif."})
EL.append({"ad": "Genel kütüphane CA_cum O1 h3 (Cuma sinyali -> Pazartesi açılış al, Çarşamba kapanış sat)",
           "neden": "Dayanak havuzu 9/9 pozitif, t=3,34 (IS 2,65, OOS 2,27) ama birleşik FDR'yi geçmiyor ve aynı etki QQQ/TQQQ/XLK'de var (piyasa geneli Nasdaq takvim etkisi; abd_endeks ailesi de 'teknoloji trendinin yan ürünü' diye eledi). Mekanizma yok."})
EL.append({"ad": "Genel kütüphane MR_ibs_lt01_dusus (IBS<0,10 ve düşüş günü), 2x hisse ETF",
           "neden": "Dayanak havuzu C0 h1 +44 bp t=2,04 (9/9 pozitif) ama O1 h1 +3 bp, C1 negatif: kapanışa bağımlı ve havuz eşiği (2,5) altında."})
EL.append({"ad": "Genel kütüphane MR_z1_lt_m2 / MO_z1_gt_2 / MO_20g_zirve (büyük gün sonrası devam-dönüş, 20 gün zirvesi)",
           "neden": "z<-2 dönüşü O1 h1 9/9 pozitif ama t=1,60; 20 gün zirvesi ve z>2 devamı zamanlama kenarı negatif/sıfır."})
EL.append({"ad": "Piyasa sert düşüş günü (QQQ/SPY z<-2) -> 2x hisse ETF (lead-lag bulgusunun kuralı)", "neden": kural_txt})
if BT is not None:
    def bt(name):
        r = BT[BT.test == name]
        return r.iloc[0] if len(r) else None
    a = bt("B1_tasima_hepsi"); b = bt("B2_pead_kosulsuz_hepsi"); bp_ = bt("B2_pead_pozitif_tepki_hepsi"); bn = bt("B2_pead_negatif_tepki_hepsi")
    if a is not None:
        EL.append({"ad": "TH04 bilanço: duyuruyu 2x ETF ile taşımak ve bilanço sonrası sürüklenme (PEAD)",
                   "neden": (f"Taşıma (C_E -> C_R, 2x): n={int(a.n)} ort {f1(a.net_bp,0)} bp t={f1(a.t,2)}, std {f1(a.std_bp,0)} bp, en kötü {f1(a.en_kotu_bp,0)} bp: kumar. "
                             f"Sonrası C_R -> C_R+2: koşulsuz {f1(b.net_bp,0)} bp t={f1(b.t,2)}; olumlu tepki sonrası {f1(bp_.net_bp,0)} bp t={f1(bp_.t,2)}; olumsuz tepki sonrası {f1(bn.net_bp,0)} bp t={f1(bn.t,2)}. "
                             f"Mega-cap 7'de olumlu tepki sonrası devam {f1(bt('B2_pead_pozitif_tepki_mega7').net_bp,0)} bp t={f1(bt('B2_pead_pozitif_tepki_mega7').t,2)} ama OOS {f1(bt('B2_pead_pozitif_tepki_mega7').oos_net_bp,0)} bp t={f1(bt('B2_pead_pozitif_tepki_mega7').oos_t,2)} (zayıflıyor); "
                             f"duyuru öncesi 3 gün {f1(bt('B3_oncesi_mega7').net_bp,0)} bp t={f1(bt('B3_oncesi_mega7').t,2)} (IS t={f1(bt('B3_oncesi_mega7').is_t,2)}, OOS t={f1(bt('B3_oncesi_mega7').oos_t,2)}). "
                             f"KAÇINILACAK: tepki günü açılışında 2x ETF almak (boşluğu kovalamak) olumlu boşlukta {f1(bt('B4_gunici_pozitif_bosluk_hepsi').net_bp,0)} bp (t={f1(bt('B4_gunici_pozitif_bosluk_hepsi').t,2)}), "
                             f"olumsuz boşlukta {f1(bt('B4_gunici_negatif_bosluk_hepsi').net_bp,0)} bp (t={f1(bt('B4_gunici_negatif_bosluk_hepsi').t,2)}); bilanço test ailesinde FDR'den geçiyor, IS ve OOS negatif. "
                             f"Strateji yok; TH04 kuralı (duyurudan önce kapat) risk yönetimi olarak önerilir.")})

dosyalar = sorted([os.path.join(O, f) for f in os.listdir(O) if f.endswith((".csv", ".txt", ".json")) and not f.startswith("_")]) + \
    sorted([os.path.join(thk.HERE, f) for f in os.listdir(thk.HERE) if f.endswith(".py")]) + \
    [os.path.join(R, "notlar", "aile_tek_hisse_kaldiracli.md")]
OZ = (f"Tek hisse kaldıraçlı aile (12 ETF, 9 bağımsız dayanak). ETF geçmişleri kısa (2022+) ve Direxion/GraniteShares ürünleri 2024 başına kadar 1,5x idi; "
      f"bu yüzden kurallar dayanak hisselerde 2016-11..2026-11 sentetik kalibre 2x ile test edilip gerçek ETF verisiyle kontrol edildi. Toplam {ntest} test, birleşik BH-FDR'yi geçen pozitif "
      f"{ngec_pos} (hepsi tek hisse satırı: seçim yanlılığı). Eşiği geçen tek aday S1: ön-kayıtlı TH03 (hisse RSI(2)<10 ve hisse>SMA200 -> 2x ETF, SMA5'e dönüşte ya da en çok 3 günde çık), "
      f"7 mega-cap havuzunda C0 n={int(c0.n)}, net {f1(c0.net_bp)} bp, t={f1(c0.t,2)}, IS {f1(c0.is_net_bp)} / OOS {f1(c0.oos_net_bp)} bp, O1'de de {f1(o1.net_bp)} bp (t={f1(o1.t,2)}); "
      f"gerçek ETF'de (2022+) C0 {f1(gC0.net_bp)} bp t={f1(gC0.t,2)}. Ancak birleşik FDR'yi geçmiyor, koşulsuz sürüklenme düşülmüş zamanlama kenarı t~2,1 ve bunun önemli kısmı ~24 bilanço öncesi dip işleminden geliyor "
      f"(bilanço işlemleri hariç kenar t~1,4), dayanaklar sonradan kazananlar: güven düşük. "
      f"Kripto (MSTU/CONL) ve ters ürünler (TSLQ/NVDS) için doğrulanmış strateji yok; ters ETF almak tüm testlerde zarar. Doğrulanmış gecikmeli öncü yok "
      f"(BTC, SMH, QQQ dahil); ETF'ler kapalıyken izlenecekler: hissenin kendi uzatılmış seansı, CME_MINI:NQ1!, MSTU için COINBASE:BTCUSD. "
      f"2x ETF'ler 1-3 günde 2x hisseden 9-14 bp (MSTU 57 bp) geride. Midas'ta bu ürünlerin bulunurluğu resmî doğrulanmadı.")
J = {"family": "tek_hisse_kaldiracli", "ozet": OZ, "izleme": IZ, "stratejiler": [S1J], "elenen": EL, "leadlag": LL,
     "dosyalar": dosyalar, "tv_dogrulanacak": []}
json.dump(J, open(os.path.join(O, "sonuc.json"), "w"), ensure_ascii=False, indent=1, default=lambda x: x.item() if hasattr(x, "item") else str(x))
print(json.dumps(J, ensure_ascii=False, indent=1, default=lambda x: x.item() if hasattr(x, "item") else str(x))[:6000])
