"""sektor_tematik: sonuç JSON'unu (izleme, stratejiler, elenen, lead-lag) üretir.
Sayılar önceki betiklerin CSV çıktılarından ve strateji_adaylari.py'nin hesaplarından okunur.
Çıktı: sonuclar/aile_sektor_tematik/sonuc.json"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from havuz import *

R = os.path.join(ROOT, "sonuclar")
scr = pd.read_csv(os.path.join(R, "tarama.csv")).set_index("sym")
tv = pd.read_csv(os.path.join(R, "tv_etf.csv")).set_index("sym").tv
fdr = pd.read_csv(os.path.join(OUT, "fdr_tum_testler.csv"))
N_TEST = len(fdr)
TVX = {"NVDA": "NASDAQ:NVDA", "TSM": "NYSE:TSM", "AVGO": "NASDAQ:AVGO", "MSFT": "NASDAQ:MSFT", "AAPL": "NASDAQ:AAPL",
       "VIX_dlog": "CBOE:VIX", "DGS10_d": "TVC:US10Y"}


def tvc(s):
    return TVX.get(s) or tv.get(s)


# ------------------------- izleme -------------------------
K = {  # karar, gerekçe
 "SMH": ("kabul", "S1 (SMH IBS<0.20) burada doğrulandı; en likit yarı iletken ETF'i (medyan ~4 mlr $/gün), maliyet/1g oynaklık 0.05."),
 "SOXL": ("kabul", "S1 sinyalinin 3x aracı (S2). Çok likit (6.5 mlr $/gün), maliyet/oynaklık 0.015. UYARI: Midas'ta bulunurluğu DOĞRULANAMADI; 3x kaldıraç, 1 günden uzun tutuşta oynaklık kaybı; 1940 Kanunu fonu (PTP değil)."),
 "SOXX": ("yedek", "SMH'nin kopyası (korelasyon 0.98): S1 aynı sonucu veriyor (43 bp, t 3.9) ama bağımsız kanıt değil; SMH daha likit."),
 "XLK": ("yedek", "Aynı IBS kuralı zayıf (net 19 bp, t 2.2, OOS yalnız 5 bp); SMH ile 0.94 korelasyon. S1'in daha az oynak yedeği."),
 "IGV": ("yedek", "Doğrulanmış negatif gecikme: QQQ/SPY güçlü yükseldiği günün ertesi IGV zayıf (FDR, IS/OOS aynı işaret); long-only kurala çevrilince maliyeti karşılamıyor, yalnız 'alma' filtresi. Likit (1.2 mlr $), maliyet/oynaklık 0.06."),
 "XBI": ("yedek", "IBS<0.20 sınırda (net 16 bp, t 1.8, IS ~2 bp): kabul eşiğini geçmiyor. Likit (1.2 mlr $), ayrı küme (biyoteknoloji); sürücü IWM/VIX."),
 "KRE": ("yedek", "Strateji yok; net sürücüler (XLF, IWM, faiz). FOMC karar günü riski ölçüldü (faize duyarlı grup gün içi brüt -26 bp). Likit (1 mlr $), maliyet/oynaklık 0.10 (sınırda)."),
 "XOP": ("yedek", "Strateji yok (enerji_tarim ailesi ayrıca inceliyor); sürücü ham petrol vadelisi. XLE'ye göre daha yüksek oynaklık/maliyet verimi (0.074)."),
 "KWEB": ("yedek", "Doğrulanmış negatif gecikme: EEM güçlü yükseldiği günün ertesi KWEB brüt -14..-34 bp (FDR, IS/OOS negatif) -> long-only için 'alma/çık' kuralı. Gerçek zamanlı izleme: Hang Seng vadelisi. Likit (594 mn $)."),
 "COPX": ("yedek", "Strateji yok; sürücü bakır (CPER/HG1!), maliyet/oynaklık 0.046 (iyi). XME regresyonda öncü görünüyor ama işlem kuralında maliyeti karşılamıyor. metal_madenci ailesi de kapsıyor."),
}
RED_DEFAULT = "Aile testlerinde (ST01-ST06, kalıntı dönüşü, çiftler, genel kütüphane havuzu) doğrulanmış kenar yok"
RED = {
 "XLF": "Düşük 1g oynaklık (maliyet/oynaklık 0.14); doğrulanmış kural yok; bankalar KRE ile izlenir.",
 "XLE": "XOP ile aynı sürücü (korelasyon 0.93); 1g oynaklığı daha düşük (maliyet/oynaklık 0.093); enerji_tarim ailesi kapsıyor.",
 "XLV": "Düşük oynaklık (maliyet/oynaklık 0.12); kenar yok.", "XLI": "Düşük oynaklık (0.12); kenar yok.",
 "XLY": "Düşük oynaklık (0.11); kenar yok.", "XLP": "Düşük oynaklık (0.13); kenar yok.",
 "XLU": "Düşük oynaklık (0.14); FOMC günü zayıflığı; kenar yok.", "XLB": "Düşük oynaklık (0.12); kenar yok.",
 "XLRE": "VNQ/IYR ile kopya (0.98); düşük oynaklık (0.16).", "XLC": "Düşük oynaklık (0.13); kısa geçmiş (2018); kenar yok.",
 "KBE": "KRE'nin kopyası (0.993), daha az likit.", "IBB": "XBI ile 0.90 korelasyon, daha düşük oynaklık; ST04 (IBB->XBI) anlamsız.",
 "OIH": "XOP/XLE ile aynı sürücü; çift (OIH/XLE) testleri negatif.", "XME": "COPX ile 0.81; IBS kuralı ~0; metal_madenci ailesi kapsıyor.",
 "ITB": "Strateji yok (ST06 anlamsız); FOMC günü riski; konut kümesi.", "XHB": "ITB'nin kopyası (0.97).",
 "XRT": "Kenar yok; düşük oynaklık (0.10).", "JETS": "Kenar yok (IBS 7 bp, t 0.8).", "CIBR": "Kenar yok; QQQ'dan negatif gecikme var ama kural maliyeti karşılamıyor.",
 "ITA": "Kenar yok; düşük oynaklık (0.11).", "XAR": "ITA ile 0.92; daha az likit.", "PAVE": "XLI ile 0.94; kenar yok.",
 "IYT": "Düşük likidite (46 mn $) ve oynaklık (0.15); kenar yok.", "VNQ": "Düşük oynaklık (0.15); FOMC günü zayıflığı; kenar yok.",
 "KIE": "Düşük oynaklık (0.15); kenar yok.", "IYR": "VNQ'nun kopyası (0.99).", "FDN": "Yazılım/internet kümesinde IGV tercih; 79 mn $.",
 "SOXS": "Ters 3x: kısa yön için doğrulanmış sinyal yok; sürekli değer kaybı (1 yıl -%90). Midas'ta bulunurluğu doğrulanamadı.",
 "TECL": "XLK IBS kuralı OOS zayıf (TECL C0 h1 OOS 31 bp, t 0.8); kaldıraçlı araç gerekiyorsa SOXL daha güçlü sinyal ve likidite.",
 "TECS": "Ters 3x; kısa yön sinyali yok.", "FAS": "XLF sinyalleri OOS zayıf; 3x kaldıraç.", "FAZ": "Ters 3x; sinyal yok.",
 "LABU": "XBI IBS -> LABU IS zayıf (IS t 0.8-1.2), OOS güçlü: kararsız; 3x.", "LABD": "Ters 3x; sinyal yok.",
 "ERX": "2x enerji; ailede kural yok (enerji_tarim kapsıyor).", "ERY": "Ters 2x; sinyal yok.", "GUSH": "2x XOP; kural yok; 29 mn $.",
 "DRIP": "Ters 2x; sinyal yok.", "NAIL": "3x ITB; IBS kuralı C0'da yok (yalnız C1); kenar yok.", "DFEN": "3x savunma; 16 mn $; kenar yok.",
 "FNGU": "2025-02'de yeniden ihraç (ETN, ihraççı kredi riski); kısa geçmiş.", "FNGD": "Ters 3x ETN; sinyal yok.",
 "CURE": "Düşük likidite (6.6 mn $), makas ~15 bp.", "RETL": "Düşük likidite (3.7 mn $).", "UTSL": "Düşük likidite (5.1 mn $).",
 "ARKK": "ST06 (sert düşüş dönüşü) anlamsız; IBS ~0; QQQ'dan negatif gecikme yalnız IS'te.", "ARKG": "Kenar yok.",
 "ARKW": "ARKK kopyası (0.95), 14 mn $.", "TAN": "Kenar yok (ST06, IBS).", "ICLN": "TAN ile 0.90; kenar yok.",
 "URA": "Kenar yok; SPY/NLR'den negatif gecikme OOS zayıf; metal_madenci ailesi kapsıyor.", "URNM": "URA kopyası (0.95), 34 mn $.",
 "NLR": "URA kopyası (0.95).", "LIT": "18 mn $ ve kenar yok.", "REMX": "Kenar yok (IBS -13 bp).", "BOTZ": "Kenar yok; 29 mn $.",
 "ROBO": "BOTZ kopyası (0.93), 11 mn $.", "QTUM": "Kenar yok; 50 mn $.", "BLOK": "14 mn $; kenar yok (kripto ailesi kapsıyor).",
 "UFO": "20 mn $; kenar yok.", "HACK": "CIBR kopyası (0.97), 13 mn $.", "SKYY": "IGV kümesinde (0.92), 28 mn $.",
 "MOO": "Düşük oynaklık (maliyet/oynaklık 0.21), 18 mn $.", "WCLD": "IGV kümesinde (0.89), 25 mn $.", "DRIV": "1.3 mn $ (likit değil), makas ~35 bp.",
}
izleme = []
for s in FAM:
    r = scr.loc[s]
    karar, ger = K.get(s, ("red", RED.get(s, RED_DEFAULT)))
    izleme.append({"sym": s, "karar": karar, "gerekce": ger, "tv": tv.get(s), "likidite_mn_usd": round(float(r.med_dollar_vol_m), 1),
                   "maliyet_bp": round(float(r.cost_rt_bp), 1), "vol_1d_bp": round(float(r.vol_1d_bp), 1)})
order = {"kabul": 0, "yedek": 1, "red": 2}
izleme.sort(key=lambda x: (order[x["karar"]], -x["likidite_mn_usd"]))

# ------------------------- stratejiler -------------------------
import strateji_adaylari as SA


def pack(sym_sig, sym_tr):
    sig = SA.sig_ibs(sym_sig, 0.2)
    s, tr = SA.full(sym_tr, sig, 1, "C0")
    cs = {p: SA.full(sym_tr, sig, 1, "C0", p)[0]["mean_net_bp"] for p in (1000.0, 2500.0, 10000.0)}
    md = {m: SA.full(sym_tr, sig, 1, m)[0] for m in ("O1", "C1")}
    return s, cs, md


s1, cs1, md1 = pack("SMH", "SMH")
s2, cs2, md2 = pack("SMH", "SOXL")
oth = pd.read_csv(os.path.join(OUT, "aday_sektor_tematik_S1_modlar.csv"))
fdr_note = (f"Bu ajanın {N_TEST} testi üzerinde BH-FDR q=0.10: geçti (p={s1['p']:.5f}); ayrıca genel_tum aile satırlarında "
            f"(21.978 test) BH-FDR q=0.10 geçti.")
strat = [
 {"id": "sektor_tematik_S1", "ad": "Yarı iletken gün sonu zayıflığı dönüşü (SMH IBS<0.20, 1 gün)",
  "kural": ("TradingView'da NASDAQ:SMH günlük grafiği. Gösterge IBS = (close - low) / (high - low), aynı günün mumu "
            "(Pine: ibs = (close-low)/(high-low); high=low ise sinyal yok). Koşul: IBS < 0.20 (kapanış gün içi aralığın alt %20'sinde). "
            "İşlem: NASDAQ:SMH long al, ertesi işlem günü kapanışında sat. Filtre yok (SMA200 filtresi sonucu iyileştirmiyor). "
            "Pozisyondayken ertesi gün yine IBS<0.20 olursa satma, bir gün daha tut (backtest bunu sat+yeniden al sayar; tutmak 3 $ komisyon kazandırır)."),
  "giris": ("C0: ABD kapanışından dakikalar önce SMH'nin anlık fiyatıyla IBS hesapla; <0.20 ise al. Kış saati (1 Kas 2026-14 Mar 2027) TR 23:45-23:58, "
            "yaz saati TR 22:45-22:58. Midas'ta MOC/LOC yok: piyasa emri ya da son fiyatın 1-2 sent üstüne limit emir. "
            "Kaçırılırsa O1: ertesi gün açılışta (kış TR 17:30 / yaz 16:30) al; beklenen net ~15 bp'ye düşer."),
  "tutus": "1 işlem günü (h=1). h=2/h=3 de pozitif (net 52/66 bp, t 3.4/3.3) ama birincil kural h=1.",
  "cikis": "Ertesi işlem günü kapanışından hemen önce sat (kış TR 23:45-23:58 / yaz 22:45-22:58). Stop yok (backtest stopsuz).",
  "islem_etf": ["SMH"], "sinyal_etf": "SMH", "n": int(s1["n"]), "brut_bp": round(s1["mean_gross_bp"], 1), "net_bp": round(s1["mean_net_bp"], 1),
  "kazanma": round(s1["win"], 3), "pf": round(s1["pf"], 2), "t": round(s1["t"], 2), "is_net_bp": round(s1["is_net_bp"], 1),
  "oos_net_bp": round(s1["oos_net_bp"], 1), "yil_pozitif": round(s1["years_pos_frac"], 2), "maxdd": round(s1["maxdd"], 3),
  "en_kotu_bp": round(s1["worst_bp"], 0),
  "maliyet_duyarlilik": f"1.000$: {cs1[1000.0]:.1f} bp | 2.500$: {cs1[2500.0]:.1f} bp | 10.000$: {cs1[10000.0]:.1f} bp (net, işlem başına)",
  "mod_saglamlik": (f"C0 h1 net {s1['mean_net_bp']:.1f}; O1 h1 brüt {md1['O1']['mean_gross_bp']:.1f} (koşulsuza göre kenar {md1['O1']['edge_bp']:.1f}, net {md1['O1']['mean_net_bp']:.1f}, t {md1['O1']['t']:.2f}); "
                    f"C1 h1 brüt {md1['C1']['mean_gross_bp']:.1f} (kenar {md1['C1']['edge_bp']:.1f} ≈ 0). O1'de brüt kenar > 0 olduğu için yalnız kapanışa bağımlı değil, "
                    "ama etki ilk gün içinde sönüyor: en iyi kapanışta (C0) girilir; bir gün geç (C1) girmek kenarı yok eder."),
  "aile_ici": ("Aynı kural her ETF'in kendi IBS'iyle 39 ETF'de (37 küme temsilcisi + SOXX + QQQ): SOXX 43.3 bp (t 3.9, kopya), XLK 19.0 (t 2.2, OOS 5), "
               "QQQ 17.6 (t 2.1), XBI 15.9 (t 1.8); diğer 35'i ~0 ya da negatif (pozitif oran %31). Etki yarı iletken/teknoloji kümesine özgü: 1 bağımsız küme. "
               "SMH sinyallerinin %70'i QQQ IBS<0.20 ile aynı gün; SMH düşük & QQQ değil: 14 bp (t 0.8), ikisi de düşük: 54 bp (t 3.8). "
               "QQQ beta-hedge'li kenar 18 bp (t 4.0): yarı iletkenler Nasdaq dönüşünü ~1.8 beta ile büyütüyor. abd_endeks ailesinin QQQ/TQQQ IBS stratejisiyle aynı bahis sayılmalı."),
  "fdr": fdr_note, "test_sayisi": N_TEST,
  "kazanma_notu": "",
  "guven": "orta",
  "betik": "python3 -I /home/user/Xxxx/raporlar/2026-11-07_midas_etf_1-3gun/kod/ajan_sektor_tematik/strateji_adaylari.py",
  "notlar": ("Kabul eşiklerini geçiyor (n=492 ≥40, t 3.69, IS 43 / OOS 40 bp, 11 yılın 10'u pozitif, O1 brüt kenar > 0). Güven 'orta' çünkü: tek bağımsız küme, "
             "aday çok sayıda test içinden seçildi (FDR'yi yine de geçiyor), C0 girişte IBS kapanıştan ~15 dk önce tahmin ediliyor (eşiğe yakın günlerde yanlış sınıflama). "
             "Komşu eşikler 0.10/0.15/0.25/0.30: net 55/39/40/29 bp, hepsi t>3 (seçim yapılmadı). En kötü işlemler: 2020-03-11 (-10.7%), 2025-01-24 (DeepSeek, -10.0%), "
             "2025-04-03 (gümrük tarifesi, -7.7%): sinyal sert düşüş günlerinde de tetiklenir, pozisyon küçük tutulmalı. Yılda ~49 işlem (zamanın ~%20'si piyasada). "
             "Takvim riskleri: NVDA bilançosu (kapanış sonrası), FOMC/CPI günleri.")},
 {"id": "sektor_tematik_S2", "ad": "S1'in 3x aracı: SMH IBS<0.20 sinyaliyle SOXL (1 gün)",
  "kural": ("Sinyal S1 ile aynı: NASDAQ:SMH günlük IBS = (close-low)/(high-low) < 0.20. İşlem AMEX:SOXL (3x yarı iletken) long al, ertesi işlem günü kapanışında sat. "
            "Sinyal SOXL'ün kendi mumundan DEĞİL, SMH'den hesaplanır (SOXX IBS de olur: 139 bp, t 4.3). Aynı riski almak için SOXL tutarı SMH'ye ayrılacak tutarın ~1/3'ü olmalı."),
  "giris": "C0: kış TR 23:45-23:58 / yaz 22:45-22:58, kapanıştan hemen önce (kaldıraçlı fonun kapanış yeniden dengelemesi son dakikalarda oynaklık yaratır; limit emir). O1 alternatifi: ertesi açılış (kış TR 17:30 / yaz 16:30).",
  "tutus": "1 işlem günü. 1 günden uzun tutuşta oynaklık kaybı ölçüldü: SOXL-3×SOXX sapması h1 -9 bp, h3 -31 bp, σ20≥%3 iken h3 -75 bp (ortalama).",
  "cikis": "Ertesi işlem günü kapanışından hemen önce sat. Stop yok.",
  "islem_etf": ["SOXL"], "sinyal_etf": "SMH", "n": int(s2["n"]), "brut_bp": round(s2["mean_gross_bp"], 1), "net_bp": round(s2["mean_net_bp"], 1),
  "kazanma": round(s2["win"], 3), "pf": round(s2["pf"], 2), "t": round(s2["t"], 2), "is_net_bp": round(s2["is_net_bp"], 1),
  "oos_net_bp": round(s2["oos_net_bp"], 1), "yil_pozitif": round(s2["years_pos_frac"], 2), "maxdd": round(s2["maxdd"], 3),
  "en_kotu_bp": round(s2["worst_bp"], 0),
  "maliyet_duyarlilik": f"1.000$: {cs2[1000.0]:.1f} bp | 2.500$: {cs2[2500.0]:.1f} bp | 10.000$: {cs2[10000.0]:.1f} bp (net, işlem başına; SOXL tutarı)",
  "mod_saglamlik": (f"C0 h1 net {s2['mean_net_bp']:.1f}; O1 h1 brüt {md2['O1']['mean_gross_bp']:.1f} (net {md2['O1']['mean_net_bp']:.1f}, t {md2['O1']['t']:.2f}); "
                    f"C1 h1 brüt {md2['C1']['mean_gross_bp']:.1f} (koşulsuza göre kenar {md2['C1']['edge_bp']:.1f} ≈ 0)."),
  "aile_ici": "S1 ile aynı sinyal: bağımsız kanıt DEĞİL. Diğer 3x araçlar: XLK->TECL C0 h1 74 bp (OOS t 0.8), XBI->LABU C0 h1 66 bp (IS t 0.8), XLF->FAS zayıf; yalnız yarı iletkende tutarlı.",
  "fdr": f"Bu ajanın {N_TEST} testi üzerinde BH-FDR q=0.10: geçti (p={s2['p']:.6f}).", "test_sayisi": N_TEST,
  "guven": "orta",
  "betik": "python3 -I /home/user/Xxxx/raporlar/2026-11-07_midas_etf_1-3gun/kod/ajan_sektor_tematik/strateji_adaylari.py",
  "notlar": ("Risk eşdeğeri karşılaştırma: SOXL'ü SMH tutarının 1/3'üyle (ör. 833 $) almak, 2.500 $'lık SMH ile işlem başına ~aynı dolar kârı verir "
             "(SOXL 833$: ~122 bp x 833 = ~10.1 $; SMH 2.500$: 41.8 bp x 2.500 = ~10.4 $), çünkü sabit 3 $ komisyon küçük tutarda daha ağır. SOXL'ün tek avantajı sermaye verimi; "
             f"karşılığında maxDD {s2['maxdd']*100:.0f}% (işlem başına tam sermaye), en kötü işlem {s2['worst_bp']/100:.1f}% (2020-03-11). "
             "Midas'ta SOXL bulunurluğu DOĞRULANAMADI (notlar/midas_kosullari.md: 'doğrulanamadı'); uygulamada Keşfet > Pay ara ile kontrol edilmeli. PTP değil (1940 Kanunu fonu).")},
]
for x in strat: x.pop("kazanma_notu", None)

# ------------------------- elenen -------------------------
h = pd.read_csv(os.path.join(OUT, "tests_hipotez.csv")).set_index("label")
hv = pd.read_csv(os.path.join(OUT, "havuz_genel.csv"))
bg = pd.read_csv(os.path.join(OUT, "bagimsizlik.csv")).set_index("evren")
fo = pd.read_csv(os.path.join(OUT, "fomc_sektor.csv")).set_index("label")
def hl(lbl, k="mean_net_bp"): return float(h.loc[lbl, k])
mr = hv[(hv.sig == "MR_ibs_lt01_dusus") & (hv["mode"] == "C1") & (hv.h == 3) & (hv.exit == "sabit")].iloc[0]
elenen = [
 {"ad": "MR_ibs_lt01_dusus C1 h=3 'sektörlerin 33/34'ünde pozitif' (genel kütüphane)",
  "neden": (f"Bağımsız kanıt değil: 34 sektör ETF'inin günlük getiri korelasyonundan etkin N = {bg.loc['sektor34','etkin_N_getiri_korelasyonu']:.1f}. "
            f"Havuz t: naif {bg.loc['sektor34','t_naive']:.1f} -> hafta-kümeli {bg.loc['sektor34','t_hafta_kumeli']:.2f}; 37 küme temsilcisinde net {mr.mean_net_bp:.1f} bp, "
            f"t_hafta {mr.t_cl:.2f} / t_ay {mr.t_cl_ay:.2f} (FDR geçmez). SPY beta-hedge'li kenar {bg.loc['sektor34','spy_hedge_bp']:.1f} bp (t {bg.loc['sektor34','t_hedge']:.2f}): "
            "sektöre özgü katkı yok; aynı sinyal SPY'da 55.7 bp, t 2.79. Piyasa geneli etki (abd_endeks ailesinin konusu).")},
 {"ad": "ST01 sektör IBS<0.20 & C>SMA200, C0 h=1 (14 sektör havuzu)",
  "neden": f"Havuz net {hl('ST01 C0 h1'):.1f} bp (t_küme {hl('ST01 C0 h1','t_cl'):.2f}); O1 h1 {hl('ST01 O1 h1'):.1f} bp. Maliyet sonrası negatif; IBS etkisi yalnız yarı iletken/teknolojide (S1)."},
 {"ad": "SPY'a göre kalıntı (beta60) dönüşü: kalıntı z1<-2 -> sektörü al (37 küme / 11 SPDR)",
  "neden": (f"Ters işaret: 37 küme C0 h1 net {hl('kalinti z1<-2 REPS37 C0 h1'):.1f} bp (t {hl('kalinti z1<-2 REPS37 C0 h1','t_cl'):.2f}), SPY-hedge'li "
            f"{hl('kalinti z1<-2 REPS37 C0 h1','mean_hedged_bp'):.1f} bp (t {hl('kalinti z1<-2 REPS37 C0 h1','t_hedged_cl'):.2f}): aşırı satılan sektör ertesi gün de geride kalıyor "
            f"(kalıntı devamı). 11 SPDR: {hl('kalinti z1<-2 SPDR11 C0 h1'):.1f} bp. h2/h3 ve O1/C1'de de negatif ya da sıfır. 'Aşırı satılan sektörü al' kuralı reddedildi.")},
 {"ad": "ST02 kesitsel 1g dönüş: SPY'a göre en kötü 2 SPDR, C0 h=3",
  "neden": f"Net {hl('ST02_en_kotu2_1g C0 h3'):.1f} bp (t {hl('ST02_en_kotu2_1g C0 h3','t_cl'):.2f}); brüt {hl('ST02_en_kotu2_1g C0 h3','mean_gross_bp'):.1f} bp, koşulsuz SPDR ortalaması (12.9 bp) altında; kontrol (en iyi 2) daha iyi."},
 {"ad": "ST03 5 günlük endüstri momentumu: en iyi 3 SPDR, C0 h=3",
  "neden": f"Net {hl('ST03_5g_en_iyi3 C0 h3'):.1f} bp (t {hl('ST03_5g_en_iyi3 C0 h3','t_cl'):.2f}); en kötü 3 kontrolüyle aynı (0.7 bp). 1-3 günde momentum da dönüş de yok."},
 {"ad": "ST04 büyük->küçük endüstri içi (IBB->XBI, XLE->XOP, XLF->KRE, SPY->RSP), C0 h=1",
  "neden": (f"IBB->XBI {hl('ST04 IBB->XBI C0 h1'):.1f} bp (t {hl('ST04 IBB->XBI C0 h1','t_cl'):.2f}, n=117); XLE->XOP {hl('ST04 XLE->XOP C0 h1'):.1f} bp; "
            f"XLF->KRE {hl('ST04 XLF->KRE C0 h1'):.1f} bp; SPY->RSP n=9. Hiçbiri anlamlı değil; XSD verisi yok (SMH->XSD test edilemedi).")},
 {"ad": "ST05 kaldıraçlı sektör ETF'inde 1 günden uzun tutuş",
  "neden": "Ölçüm (strateji değil): log sapma teoriyi izliyor (SOXL h3, σ20≥%3: -168 bp gözlenen / -159 bp teorik). Basit getiri farkı SOXL h1 -9, h3 -31 bp; σ20≥%3 iken h3 -75 bp. Kural: σ20≥%3 iken 3x ürünü en fazla 1 gün tut (st05_kaldirac_kaybi.csv)."},
 {"ad": "ST06 tematik sert düşüş (r≤-2σ20 & C>SMA50), C0 h=2 (ARKK, TAN, URA, LIT, KWEB, JETS, ITB, XHB)",
  "neden": f"Net {hl('ST06 C0 h2'):.1f} bp (t {hl('ST06 C0 h2','t_cl'):.2f}, n=192); IS -48 / OOS +28 bp: tutarsız."},
 {"ad": "Sektör içi çiftler kalıntı z-skoru (KRE/XLF, XBI/IBB, SMH/QQQ, SOXX/SMH, XOP/XLE, OIH/XLE, ITB/XHB, IGV/XLK), z1 ve z5, ±2",
  "neden": (f"8 çift havuzu: geride kalanı al (z1<-2) C0 h1 {hl('8 cift z1<-2 al A C0 h1'):.1f} bp (t {hl('8 cift z1<-2 al A C0 h1','t_cl'):.2f}); öndekinin ortağını al "
            f"{hl('8 cift z1>2 al B C0 h1'):.1f} bp (t {hl('8 cift z1>2 al B C0 h1','t_cl'):.2f}). C0'da tek çift t≥2 yok; 324 testte pozitif FDR geçen yok. Yetişme (SMH, QQQ'ya göre geride) -> SMH al: h1 18 bp, t 0.5.")},
 {"ad": "Kaldıraçlı sektör ETF'lerinde dayanak sinyali (XLK->TECL, XLF->FAS, XBI->LABU, XOP->GUSH, ITB->NAIL)",
  "neden": "Yalnız yarı iletkende (S2) IS ve OOS birlikte güçlü. TECL C0 h1 OOS t 0.8; LABU IS t 0.8-1.2; FAS/GUSH/NAIL C0'da anlamsız. Tek tutarlı küme yarı iletken."},
 {"ad": "Yarı iletkenlerde hisse/Asya öncüleri (NVDA, TSM, AVGO, EWT, EWY -> SMH/SOXX ertesi gün)",
  "neden": "Kendi gecikmesi kontrol edilince katkı yok (SMH için t: NVDA 0.21, TSM 0.51, AVGO -0.28, EWT 0.73, EWY 0.37). Tek başına görülen negatif ilişki (NVDA t -3.0) SMH'nin kendi 1 günlük dönüşü."},
 {"ad": "Lead-lag 'yetişme' bayrakları (SMH 18, SOXX 14, SOXL 5 öncü; GDX, USO, UUP, TIP...)",
  "neden": "Yetişme sinyali -r_T(t) içerdiği için SMH'nin kendi dönüşünü yakalıyor; aynı öncülerin kendi gecikmesi kontrollü lag_t'si |t|<1.7. Öncü katkısı yok."},
 {"ad": "XME -> COPX pozitif gecikme",
  "neden": "Regresyonda t 2.47 (IS 2.0 / OOS 1.5) ama kural: XME z>+1 -> COPX C0 h1 net 4.6 bp (t 0.36), O1 -24 bp. Maliyet sonrası yok."},
 {"ad": "Faize duyarlı sektörlerde FOMC (KRE, XLF, ITB, VNQ, XLU, KIE)",
  "neden": (f"Long kural yok: karar günü gün içi (O1) brüt {fo.iloc[4]['mean_gross_bp']:.1f} bp, net {fo.iloc[4]['mean_net_bp']:.1f} (t {fo.iloc[4]['t_cl']:.2f}, IS -32 / OOS -48), "
            f"karar öncesi kapanış->karar kapanışı brüt {fo.iloc[3]['mean_gross_bp']:.1f}. Takvim riski olarak raporlandı (karar günü bu ETF'lerde yeni long açma).")},
 {"ad": "Genel kütüphane, aile havuzu (31 sinyal × mod × h, 297 test, 37 küme temsilcisi)",
  "neden": "Küme-sağlam t ile hiçbir pozitif sinyal BH-FDR'yi geçmiyor; FDR geçen 35 satırın hepsi maliyet sonrası negatif (ör. momentum ve haftanın günü O1 h1). Tek ETF düzeyinde geçenler yarı iletken/teknoloji kümesinde toplanıyor."},
]

# ------------------------- lead-lag -------------------------
C = pd.read_csv(os.path.join(OUT, "suruculer.csv"))
def drivers(T, k=4, extra=None):
    x = C[C.target == T].head(k)
    out = [{"ad": r.driver, "tv": tvc(r.driver), "corr_1y": round(r.corr_1y, 2), "beta_1y": round(r.beta_1y, 2)} for r in x.itertuples()]
    return out
NQ = {"ad": "Nasdaq-100 vadelisi (neredeyse 24 saat)", "tv": "CME_MINI:NQ1!", "neden": "ETF kapalıyken (TR 00:00-17:30) teknoloji yönünü gösterir; açılış boşluğunu önceden verir."}
ES = {"ad": "S&P 500 vadelisi", "tv": "CME_MINI:ES1!", "neden": "Genel piyasa açılış boşluğu."}
RTY = {"ad": "Russell 2000 vadelisi", "tv": "CME_MINI:RTY1!", "neden": "Küçük ölçekli/bölgesel banka/biyotek açılış boşluğu."}
KOSPI = {"ad": "KOSPI endeksi (Kore)", "tv": "KRX:KOSPI", "neden": "Asya seansında (TR ~03:00-09:30) bellek/yarı iletken (Samsung, SK Hynix) hareketi; SMH açılışını önceden gösterir."}
NK = {"ad": "Nikkei 225 vadelisi (OSE)", "tv": "OSE:NK2251!", "neden": "Asya seansı risk iştahı (Tokyo Electron, Advantest ağırlıklı)."}
NVDA_RT = {"ad": "NVIDIA (uzatılmış seans)", "tv": "NASDAQ:NVDA", "neden": "Bilanço kapanış sonrası açıklanır; after-hours/pre-market fiyatı SMH açılış boşluğunu gösterir (SMH ile 1y korelasyon 0.73)."}
TSM_RT = {"ad": "TSMC ADR (pre-market)", "tv": "NYSE:TSM", "neden": "Tayvan seansı sonrası TSMC ADR'ı pre-market'te (TR 12:00-17:30) fiyatlanır."}
SOXI = {"ad": "PHLX Yarı İletken Endeksi", "tv": "NASDAQ:SOX", "neden": "Yalnız ABD seansında hesaplanır: gerçek zamanlı gün içi sürücü, kapalı saatte öncü değil."}
ZN = {"ad": "10 yıllık ABD tahvil vadelisi", "tv": "CBOT:ZN1!", "neden": "Faiz hareketi gece de işler; banka/konut ETF'lerinin açılışını etkiler."}
US2 = {"ad": "ABD 2 yıllık getiri", "tv": "TVC:US02Y", "neden": "Fed beklentisi; bölgesel bankalar için marj/fonlama baskısı göstergesi."}
CL = {"ad": "WTI ham petrol vadelisi", "tv": "NYMEX:CL1!", "neden": "Neredeyse 24 saat işler; XOP açılışını önceden gösterir (XOP-BNO/USO 1y korelasyon ~0.7)."}
BRN = {"ad": "Brent vadelisi", "tv": "ICEEUR:BRN1!", "neden": "Avrupa/Asya saatlerinde petrol fiyatı."}
HSI = {"ad": "Hang Seng vadelisi", "tv": "HKEX:HSI1!", "neden": "KWEB varlıklarının çoğu Hong Kong'da işlem görür: ABD kapalıyken (TR 04:15-11:10 + gece seansı) KWEB'in açılış boşluğunu doğrudan gösterir."}
HSIX = {"ad": "Hang Seng endeksi", "tv": "TVC:HSI", "neden": "Spot endeks; seans kapanışı."}
CNH = {"ad": "USD/CNH", "tv": "FX:USDCNH", "neden": "Yuan zayıflığı Çin varlıklarında risk iştahını gösterir; 24 saat."}
A50 = {"ad": "FTSE China A50 vadelisi (SGX)", "tv": "SGX:CN1!", "neden": "Çin anakara hisseleri; Asya saatlerinde."}
HG = {"ad": "COMEX bakır vadelisi", "tv": "COMEX:HG1!", "neden": "Neredeyse 24 saat; COPX açılışını önceden gösterir (COPX-CPER 1y korelasyon 0.82)."}
VIXRT = {"ad": "VIX", "tv": "CBOE:VIX", "neden": "Risk iştahı; gün içi (16:15 ET kapanış)."}

YOK = "Doğrulanmış gecikmeli öncü yok."
leadlag = [
 {"sym": "SMH", "suruculer": drivers("SMH") + [{"ad": "NVDA", "tv": "NASDAQ:NVDA", "corr_1y": 0.73}],
  "onculer": [{"ad": "QQQ (zayıf, doğrulanmadı)", "tv": "NASDAQ:QQQ", "tip": "negatif gecikme (kendi gecikmesi kontrollü)",
               "etki": "QQQ +1 sd -> SMH ertesi gün -35 bp (h1); IS t -2.46, OOS t -1.03: OOS zayıf, kabul edilmedi", "t": -2.64, "is_t": -2.46, "oos_t": -1.03, "fdr": False, "ufuk": "1 gün",
               "maliyet_sonrasi": "işlem kuralı olarak test edilmedi (OOS zayıf)"}],
  "gercek_zamanli": [NQ, KOSPI, NK, NVDA_RT, TSM_RT, SOXI],
  "not": YOK + " NVDA/TSM/AVGO/EWT/EWY kendi gecikmesi kontrol edilince katkısız (t 0.2-0.7). Süpürmedeki 18 'yetişme' bayrağı SMH'nin kendi 1 günlük dönüşü (S1 ile aynı olgu). NVDA, TSM ve SOX eşzamanlı sürücüdür, öncü değildir.",
  "takvim_riskleri": "NVDA bilançosu (ABD kapanışı sonrası; tarih şirket takviminden doğrulanmalı), TSMC aylık satış (ayın ~10'u, Asya saati), FOMC (TR 21:00/22:00), CPI (TR 15:30/16:30), ihracat kontrolü haberleri."},
 {"sym": "SOXL", "suruculer": drivers("SOXL"),
  "onculer": [], "gercek_zamanli": [NQ, KOSPI, NVDA_RT, TSM_RT],
  "not": YOK + " Sinyal SMH'den alınır (S2). Kaldıraçlı fon kapanışta yeniden dengeler: son dakikalarda oynaklık artabilir.",
  "takvim_riskleri": "SMH ile aynı; ayrıca σ20≥%3 dönemlerinde 1 günden uzun tutuşta ölçülen kayıp (3 günde ~-75 bp)."},
 {"sym": "SOXX", "suruculer": drivers("SOXX"), "onculer": [], "gercek_zamanli": [NQ, KOSPI, NVDA_RT, SOXI],
  "not": YOK + " SMH ile aynı (kopya).", "takvim_riskleri": "SMH ile aynı."},
 {"sym": "XLK", "suruculer": drivers("XLK"),
  "onculer": [{"ad": "AAPL (3 gün, negatif)", "tv": "NASDAQ:AAPL", "tip": "negatif gecikme (h3)", "etki": "AAPL +1 sd -> XLK sonraki 3 gün -30 bp; ek testte FDR geçti ama h1'de yok ve son 1 yılda AAPL-XLK korelasyonu 0.16: ekonomik yorumu zayıf, kullanılmamalı",
               "t": -3.37, "is_t": -2.01, "oos_t": -2.39, "fdr": True, "ufuk": "3 gün", "maliyet_sonrasi": "işlem kuralına çevrilmedi"}],
  "gercek_zamanli": [NQ, ES, NVDA_RT],
  "not": "Güvenilir gecikmeli öncü yok (AAPL h3 bulgusu tek ufukta, mekanizmasız). Sürücüler eşzamanlı.",
  "takvim_riskleri": "NVDA/AAPL/MSFT bilançoları (kapanış sonrası), FOMC, CPI."},
 {"sym": "IGV", "suruculer": drivers("IGV"),
  "onculer": [{"ad": "QQQ", "tv": "NASDAQ:QQQ", "tip": "negatif gecikme (kendi gecikmesi kontrollü)",
               "etki": "QQQ +1 sd (~1.3%) -> IGV ertesi gün ~-32 bp. Kural: QQQ 1g z>+1 -> ertesi gün IGV brüt -6.7 bp (C0), -11.3 bp (O1); IS ve OOS negatif",
               "t": -3.68, "is_t": -2.29, "oos_t": -2.40, "fdr": True, "ufuk": "1 gün",
               "maliyet_sonrasi": "Long-only: QQQ z<-1 -> IGV al net -2.6 bp (yok). Yalnız filtre: QQQ güçlü yükseldiği akşam yeni IGV alma / mevcut IGV'yi kapat."},
              {"ad": "SPY", "tv": "AMEX:SPY", "tip": "negatif gecikme", "etki": "SPY +1 sd -> IGV ertesi gün ~-35 bp (QQQ ile aynı olgu)", "t": -3.71, "is_t": -2.68, "oos_t": -2.42, "fdr": True, "ufuk": "1 gün",
               "maliyet_sonrasi": "QQQ ile aynı; ayrı kanıt değil"}],
  "gercek_zamanli": [NQ, {"ad": "Microsoft (uzatılmış seans)", "tv": "NASDAQ:MSFT", "neden": "IGV'nin en büyük ağırlıklarından; bilanço kapanış sonrası."}],
  "not": "Gerçek gecikmeli ilişki var (kendi gecikmesi kontrollü, FDR, IS/OOS aynı işaret) ama ekonomik büyüklüğü long-only işlemde maliyetin altında; IGV'nin kendi getirisi pozitif katsayılı (kalıntı devamı).",
  "takvim_riskleri": "MSFT/ORCL/CRM/NOW bilançoları, FOMC."},
 {"sym": "XBI", "suruculer": drivers("XBI"),
  "onculer": [{"ad": "SPY/QQQ (zayıf, doğrulanmadı)", "tv": "AMEX:SPY", "tip": "negatif gecikme", "etki": "SPY +1 sd -> XBI ertesi gün -25 bp; IS t -3.27, OOS t -1.16: OOS zayıf", "t": -3.16, "is_t": -3.27, "oos_t": -1.16, "fdr": False, "ufuk": "1 gün",
               "maliyet_sonrasi": "test edilmedi (OOS zayıf)"}],
  "gercek_zamanli": [RTY, VIXRT],
  "not": YOK + " (SPY/QQQ ilişkisi OOS'ta zayıflıyor).", "takvim_riskleri": "FOMC/CPI (faize duyarlı küçük ölçek), FDA kararları (tek hisse), JPM Sağlık Konferansı (Ocak)."},
 {"sym": "KRE", "suruculer": drivers("KRE"), "onculer": [],
  "gercek_zamanli": [RTY, ZN, US2],
  "not": YOK + " (XLF -> KRE t -1.85; ST04 XLF->KRE anlamsız).",
  "takvim_riskleri": "FOMC karar günü: faize duyarlı 6 ETF'te gün içi brüt -26 bp (IS -32 / OOS -48), karar günü yeni long açma. CPI, banka bilançoları (Ocak/Nisan/Temmuz/Ekim ortası), Fed stres testi (Haziran)."},
 {"sym": "XOP", "suruculer": drivers("XOP"), "onculer": [], "gercek_zamanli": [CL, BRN],
  "not": YOK + " Petrol vadelisi eşzamanlı sürücü ve gece izleme aracıdır (öncü değil).",
  "takvim_riskleri": "EIA haftalık petrol stokları (Çarşamba 10:30 ET: kış TR 18:30 / yaz 17:30), OPEC+ toplantıları, CL vade sonu (data/events/vadeler.csv)."},
 {"sym": "KWEB", "suruculer": drivers("KWEB"),
  "onculer": [{"ad": "EEM", "tv": "AMEX:EEM", "tip": "negatif gecikme (kendi gecikmesi kontrollü)",
               "etki": "EEM +1 sd -> KWEB ertesi gün ~-34..-37 bp. Kural: EEM 1g z>+1 -> ertesi gün KWEB brüt -34 bp (C0), -14 (O1), -25 (C1); IS -37 / OOS -62 bp net",
               "t": -3.84, "is_t": -2.86, "oos_t": -2.71, "fdr": True, "ufuk": "1 gün",
               "maliyet_sonrasi": "Long-only için 'alma/çık' kuralı (brüt etki maliyetin 1-2 katı). Kısa yön ancak ters ETF ile; bu ailede test edilmedi."},
              {"ad": "FXI", "tv": "AMEX:FXI", "tip": "negatif gecikme", "etki": "FXI +1 sd -> KWEB ertesi gün -47 bp (ek test, FDR); OOS t -1.70", "t": -2.66, "is_t": -2.20, "oos_t": -1.70, "fdr": True, "ufuk": "1 gün",
               "maliyet_sonrasi": "EEM ile aynı olgu; işlem kuralı EEM ile test edildi"}],
  "gercek_zamanli": [HSI, HSIX, CNH, A50],
  "not": "Doğrulanmış gecikmeli öncü: EEM (negatif). Hang Seng vadelisi öncü değil, ABD kapalıyken KWEB'in fiyatlandığı piyasadır (açılış boşluğunun kaynağı).",
  "takvim_riskleri": "Hong Kong tatilleri (KWEB işlem görür, dayanak kapalı: bayat NAV), Çin PMI (ayın 1'i), Ekim Altın Haftası, ABD-Çin ticaret/teknoloji kararları."},
 {"sym": "COPX", "suruculer": drivers("COPX"),
  "onculer": [{"ad": "XME (regresyonda; kural başarısız)", "tv": "AMEX:XME", "tip": "pozitif gecikme", "etki": "XME +1 sd -> COPX ertesi gün +23 bp (kendi gecikmesi kontrollü); kural XME z>+1 -> COPX C0 h1 net 4.6 bp (t 0.36), O1 -24 bp",
               "t": 2.47, "is_t": 2.01, "oos_t": 1.50, "fdr": True, "ufuk": "1 gün", "maliyet_sonrasi": "Maliyet sonrası yok; kullanılmamalı"}],
  "gercek_zamanli": [HG, CNH, HSI],
  "not": YOK + " (XME ilişkisi işlem kuralında maliyeti karşılamıyor).", "takvim_riskleri": "Çin PMI/sanayi verileri, HG vade sonu, LME stokları; metal_madenci ailesinin notlarına bakın."},
]

tv_dog = ["TWSE:2330 (TSMC Tayvan hissesi; Asya seansında yarı iletken izleme)", "TWSE:TAIEX 'yonlendirildi' çıktı: geçerli Tayvan endeksi kodu (ör. TVC:TWII) doğrulanmalı",
          "KRX:000660 (SK Hynix; Asya seansında bellek yarı iletkeni)"]

ozet = (f"sektor_tematik (75 ETF, 37 bağımsız küme): {N_TEST} kendi testi + genel kütüphanenin 21.978 aile satırı incelendi. Kabul eşiğini geçen tek bağımsız bulgu "
        "yarı iletkenlerde gün sonu zayıflığının ertesi gün dönüşü: S1 = NASDAQ:SMH IBS<0.20 -> SMH'yi kapanışta al, ertesi kapanışta sat "
        f"(n={s1['n']}, net {s1['mean_net_bp']:.1f} bp @2.500$, t {s1['t']:.2f}, IS {s1['is_net_bp']:.0f} / OOS {s1['oos_net_bp']:.0f} bp, 11 yılın 10'u pozitif, O1'de brüt kenar 27 bp, BH-FDR geçer). "
        f"S2 aynı sinyali SOXL (3x) ile uygular (net {s2['mean_net_bp']:.0f} bp, t {s2['t']:.2f}, maxDD {s2['maxdd']*100:.0f}%; Midas'ta bulunurluğu doğrulanamadı); bağımsız kanıt değildir. "
        "S1, Nasdaq IBS etkisinin yüksek betalı ifadesidir (sinyallerin %70'i QQQ IBS<0.20 ile aynı gün): abd_endeks ailesinin QQQ IBS kuralıyla aynı bahis. "
        "Reddedilenler: 'aşırı satılan sektörü al' (SPY kalıntı z<-2 sonrası sektör geride kalmaya devam ediyor, hedge'li -14 bp, t -2.2), kesitsel 1g dönüş ve 5g momentum (ST02/ST03), "
        "ST01, ST04, ST06, 8 sektör çifti, diğer kaldıraçlı araçlar. Genel kütüphanedeki 'MR_ibs_lt01_dusus C1 h3 sektörlerin 33/34'ünde pozitif' bulgusu tek piyasa etkisi "
        "(etkin N≈2.6, küme-sağlam t 1.8-2.7, SPY'a göre hedge'li kenar ~0). Lead-lag: gerçek gecikmeli öncüler yalnız negatif ve long-only'de 'alma' filtresi düzeyinde "
        "(QQQ->IGV, EEM->KWEB); yarı iletkenlerde NVDA/TSM/AVGO/EWT/EWY öncü değil. Takvim: FOMC karar günü faize duyarlı sektörlerde gün içi brüt -26 bp. Ailede PTP ürünü yok.")

dosyalar = [os.path.join(ROOT, p) for p in [
 "notlar/aile_sektor_tematik.md",
 "kod/ajan_sektor_tematik/strateji_adaylari.py", "kod/ajan_sektor_tematik/ortak.py", "kod/ajan_sektor_tematik/havuz.py",
 "kod/ajan_sektor_tematik/a1_genel_ozet.py", "kod/ajan_sektor_tematik/a2_havuz_genel.py", "kod/ajan_sektor_tematik/a3_hipotezler.py",
 "kod/ajan_sektor_tematik/a4_leadlag.py", "kod/ajan_sektor_tematik/a5_fomc_fdr.py", "kod/ajan_sektor_tematik/a6_bagimsizlik.py",
 "kod/ajan_sektor_tematik/a7_xme_copx.py", "kod/ajan_sektor_tematik/a8_sonuc_json.py",
 "sonuclar/aile_sektor_tematik/sonuc.json", "sonuclar/aile_sektor_tematik/strateji_adaylari_cikti.txt",
 "sonuclar/aile_sektor_tematik/aday_sektor_tematik_S1_islemler.csv", "sonuclar/aile_sektor_tematik/aday_sektor_tematik_S2_islemler.csv",
 "sonuclar/aile_sektor_tematik/genel_aile_ozet.csv", "sonuclar/aile_sektor_tematik/havuz_genel.csv", "sonuclar/aile_sektor_tematik/tests_hipotez.csv",
 "sonuclar/aile_sektor_tematik/st05_kaldirac_kaybi.csv", "sonuclar/aile_sektor_tematik/leadlag_ek.csv", "sonuclar/aile_sektor_tematik/leadlag_kural.csv",
 "sonuclar/aile_sektor_tematik/suruculer.csv", "sonuclar/aile_sektor_tematik/fomc_sektor.csv", "sonuclar/aile_sektor_tematik/bagimsizlik.csv",
 "sonuclar/aile_sektor_tematik/xme_copx_kural.csv", "sonuclar/aile_sektor_tematik/fdr_tum_testler.csv"]]

res = {"family": "sektor_tematik", "ozet": ozet, "izleme": izleme, "stratejiler": strat, "elenen": elenen, "leadlag": leadlag,
       "tv_dogrulanacak": tv_dog, "dosyalar": dosyalar}
def clean(o):
    if isinstance(o, dict): return {k: clean(v) for k, v in o.items()}
    if isinstance(o, list): return [clean(v) for v in o]
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    return o
res = clean(res)
json.dump(res, open(os.path.join(OUT, "sonuc.json"), "w"), ensure_ascii=False, indent=1)
print("yazıldı:", os.path.join(OUT, "sonuc.json"), "izleme", len(izleme), "kabul", sum(x["karar"] == "kabul" for x in izleme),
      "yedek", sum(x["karar"] == "yedek" for x in izleme))
