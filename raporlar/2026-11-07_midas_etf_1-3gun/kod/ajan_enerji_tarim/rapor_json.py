"""enerji_tarim ailesi sonuç JSON'u (sonuclar/aile_enerji_tarim/sonuc.json).
Önce: h_dogalgaz.py, h_petrol.py, h_tarim_leadlag.py, leadlag_ozet.py, ek_kontroller.py, fdr_toplam.py.
Çalıştırma: python3 -I kod/ajan_enerji_tarim/rapor_json.py"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import ortak as O, lib
import strategies as S

ROOT = lib.ROOT
K = os.path.join(ROOT, "kod", "ajan_enerji_tarim")
T = O.tarama()
TV = pd.read_csv(os.path.join(ROOT, "sonuclar", "tv_etf.csv")).set_index("sym")["tv"].to_dict()
LL = json.load(open(os.path.join(O.OUT, "leadlag_ozet.json")))
own = pd.read_csv(os.path.join(O.OUT, "fdr_aileye_ozel.csv"))
N_OWN, N_GEN = len(own), len(pd.read_csv(os.path.join(O.OUT, "genel_aile.csv"), usecols=["sym"]))
N_ALL = N_OWN + N_GEN
r1 = lambda x: None if x is None or (isinstance(x, float) and not np.isfinite(x)) else round(float(x), 1)
r3 = lambda x: None if x is None or (isinstance(x, float) and not np.isfinite(x)) else round(float(x), 3)

# ---------------- stratejiler ----------------
eia = O.events("eia_ng_storage")["date"]
def s1_sig(sym):
    idx = lib.load(sym).index
    nm = pd.Series(list(idx[1:].month) + [idx[-1].month], index=idx)
    return O.day_before(idx, eia) & nm.isin([11, 12, 1, 2, 3])
uso = lib.load("USO")
s2sig = S.LIB["MR_bb20_alt"](uso, None).reindex(uso.index).fillna(False).astype(bool); s2sig.iloc[:200] = False

def pack(sym, sig, h, mode):
    s, tr = O.full(sym, sig, h, mode); return s, tr
def modes(sym, sig):
    out = []
    for m in ("C0", "O1", "C1"):
        for h in (1, 2, 3):
            s, _ = O.full(sym, sig, h, m)
            out.append(f"{m} h{h}: brüt {s['mean_gross_bp']:.0f} / net {s['mean_net_bp']:.0f} bp (t {s['t']:.2f})")
    return "; ".join(out)
def fam(syms, sigf, h, mode):
    out = []
    for d in syms:
        s, _ = O.full(d, sigf(d), h, mode)
        out.append(f"{d}: net {s['mean_net_bp']:.0f} bp t {s['t']:.2f} (IS {s['is_net_bp']:.0f}/OOS {s['oos_net_bp']:.0f})")
    return "; ".join(out)

s1, tr1 = pack("KOLD", s1_sig("KOLD"), 1, "C0")
s1full, _ = O.full("KOLD", O.day_before(lib.load("KOLD").index, eia), 1, "C0")
s2, tr2 = pack("USO", s2sig, 2, "C1")
p_s1 = float(own[(own.hyp == "EN01k_EIA_kis_KOLD") & (own["mode"] == "C0") & (own.h == 1)].p1.iloc[0])
p_s2 = O.p_one(s2["t"], s2["n"], +1)

strat = [
 {"id": "enerji_tarim_S1", "ad": "EIA doğalgaz depolama raporu öncesi KOLD (yalnız Kasım-Mart)",
  "kural": "Takvim kuralı, fiyat göstergesi yok. EIA haftalık doğalgaz depolama raporunun (ir.eia.gov/ngs/schedule.html; normalde Perşembe 10:30 ET = TR 18:30 kış / 17:30 yaz; tatil haftalarında kayar) tarihi Kasım, Aralık, Ocak, Şubat veya Mart ayındaysa: rapordan bir önceki ABD işlem günü AMEX:KOLD (-2x doğalgaz) kapanışta alınır, rapor günü kapanışta satılır. Nisan-Ekim raporlarında işlem yok. Sinyal verisi: yalnız takvim; izleme: NYMEX:NG1! ve AMEX:KOLD.",
  "giris": "Rapordan önceki işlem günü ABD kapanışına yakın: kış saatinde TR 23:45-23:59 (yaz 22:45-22:59) piyasa emri (MOC/LOC yok) ya da kapanış sonrası after-hours limit (TR 00:00-04:00; backtest kapanış fiyatını varsayar). Alternatif O1: rapor günü açılışta (TR 17:30 kış), rapordan önce al -> net daha düşük (aşağıda). Yakın tarihler: 12 Kas 2026 Per (rapor 13 Kas Cum), 18 Kas Çar, 24 Kas Sal (rapor 25 Kas Çar 12:00 ET = TR 20:00), 2 Ara, 9 Ara, 16 Ara, 23 Ara, 30 Ara.",
  "tutus": "1 işlem günü (rapor günü kapanışına kadar)",
  "cikis": "Rapor günü ABD kapanışından dakikalar önce (TR ~23:45-23:59 kış) sat. Backtest stop kullanmaz; tek işlemde -%16'ya varan kayıp görüldü.",
  "islem_etf": ["KOLD"], "sinyal_etf": "takvim: data/events/eia_ng_storage.csv (EIA)",
  "n": int(s1["n"]), "brut_bp": r1(s1["mean_gross_bp"]), "net_bp": r1(s1["mean_net_bp"]), "kazanma": r3(s1["win"]), "pf": r3(s1["pf"]), "t": r3(s1["t"]),
  "is_net_bp": r1(s1["is_net_bp"]), "oos_net_bp": r1(s1["oos_net_bp"]), "yil_pozitif": r3(s1["years_pos_frac"]), "maxdd": r3(s1["maxdd"]), "en_kotu_bp": r1(s1["worst_bp"]),
  "maliyet_duyarlilik": f"net bp: 1.000$ {s1['net_bp_1000']:.1f} / 2.500$ {s1['net_bp_2500']:.1f} / 10.000$ {s1['net_bp_10000']:.1f} (KOLD makas 4 bp)",
  "mod_saglamlik": modes("KOLD", s1_sig("KOLD")) + ". C1 negatif beklenen bir sonuç: etki rapor gününün kendisinde; O1 (rapor günü açılışta giriş) net 64,5 bp t 2,13 ile ayakta.",
  "aile_ici": "Aynı günlerde dayanak/ayna: " + fam(("UNG", "BOIL", "UNL"), s1_sig, 1, "C0") + f". Önceden belirlenmiş TAM YIL hipotezi (EN01) KOLD: net {s1full['mean_net_bp']:.1f} bp, t {s1full['t']:.2f} (eşik altı; en iyi %5 işlem çıkarılınca brüt -13 bp). Nisan-Ekim: net 3 bp t 0,10. Komşu mevsim tanımları: Eki-Mar t 2,35, Kas-Nis 2,26, Kas-Şub 2,23, Ara-Şub 1,60.",
  "fdr": f"Geçmiyor. Tek yönlü p={p_s1:.4f}; aileye özel {N_OWN} test içinde BH(q=0,10) ilk sıra eşiği {0.10/N_OWN:.5f}; birleşik {N_ALL} testte de geçmiyor.",
  "test_sayisi": N_ALL, "oos_net_bp_t": None,
  "guven": "dusuk",
  "notlar": f"IS t {s1['is_t']:.2f}, OOS t {s1['oos_t']:.2f} (ikisi de pozitif ama tek başına anlamsız). Kasım-Mart ayrımı tam yıl sonucu görüldükten SONRA eklendi (post-hoc); literatür (Prokopczuk ve diğ. 2021: rapor günü NG -%0,37) yönü destekliyor ama 2014-2018 alt döneminde etki yok demişti. Getiri kalın kuyruklu (en iyi işlem +%42, en kötü -%16, maxDD -%42). KOLD Midas'ta doğrulanamadı; ProShares Trust II PTP: %10 brüt satış stopajı uygulanırsa işlem başına ~-1000 bp => beklenti ~-900 bp. Her işlemden önce uygulamada PTP ibaresi/kesinti kontrol edilmeli; kesinti varsa İŞLEM YAPMA. Risk notu (aynı bulgu): UNG/BOIL long pozisyonu Çarşamba kapanışından Perşembe (rapor) kapanışına taşımayın (UNG rapor günü brüt ort. -28 bp; brüt yıl ortalaması 2018-2026'nın 9 yılının hepsinde negatif).",
  "betik": os.path.join(K, "aday_S1_eia_kold.py")},
 {"id": "enerji_tarim_S2", "ad": "USO alt Bollinger kırılımı, 1 gün bekle, 2 gün long (ham petrol)",
  "kural": "AMEX:USO günlük grafiği, Bollinger Bantları (uzunluk 20, kaynak kapanış, StdDev 2.05 — TradingView popülasyon std kullandığı için 2.05, backtestteki örneklem std'li 2.0'a denk). Sinyal: t günü USO kapanışı alt bandın altında. t günü işlem YAPMA; t+1 günü kapanışa yakın AMEX:USO al (2x araç: AMEX:UCO), t+3 günü kapanışında sat. Pozisyondayken gelen yeni sinyaller yok sayılır. PTP'siz uygulama AMEX:XOP ile denendi: daha zayıf ve ufka duyarlı (notlar).",
  "giris": "Sinyal gününden SONRAKİ işlem günü (t+1) ABD kapanışına yakın: kış TR 23:45-23:59, yaz 22:45-22:59 piyasa emri ya da after-hours limit. t kapanışında girmek (C0) zararlı çıktı.",
  "tutus": "2 işlem günü (t+1 kapanışı -> t+3 kapanışı)",
  "cikis": "t+3 günü ABD kapanışından dakikalar önce sat (TR ~23:45-23:59 kış). Erken çıkış kuralı yok.",
  "islem_etf": ["USO", "UCO"], "sinyal_etf": "USO",
  "n": int(s2["n"]), "brut_bp": r1(s2["mean_gross_bp"]), "net_bp": r1(s2["mean_net_bp"]), "kazanma": r3(s2["win"]), "pf": r3(s2["pf"]), "t": r3(s2["t"]),
  "is_net_bp": r1(s2["is_net_bp"]), "oos_net_bp": r1(s2["oos_net_bp"]), "yil_pozitif": r3(s2["years_pos_frac"]), "maxdd": r3(s2["maxdd"]), "en_kotu_bp": r1(s2["worst_bp"]),
  "maliyet_duyarlilik": f"net bp: 1.000$ {s2['net_bp_1000']:.1f} / 2.500$ {s2['net_bp_2500']:.1f} / 10.000$ {s2['net_bp_10000']:.1f}",
  "mod_saglamlik": modes("USO", s2sig) + ". Kapanışa değil GECİKMEYE bağımlı: t+1 günü ortalama düşüş sürüyor, dönüş t+2..t+3'te. Sinyal 1 gün kaydırılıp t+2 açılışında girilse (h=2) net 90 bp t 3,14.",
  "aile_ici": "USO sinyaliyle C1 h2: " + fam(("BNO", "DBO", "UCO", "XOP", "XLE", "PDBC", "SCO"), lambda d: s2sig, 2, "C1") + ". Her ETF KENDİ bandıyla: BNO net 40 t 0,90; DBO 85 t 2,37; XLE -20; XOP -42; OIH -36 => sonuç sinyal günlerine duyarlı. XOP'ta h=1 ve h=3 ~0 (ufka kırılgan).",
  "fdr": f"Geçmiyor. Genel kütüphane taramasından (31 sinyal x 3 mod x 3 ufuk x 28 ETF) seçildi; tek yönlü p={p_s2:.4f}, birleşik {N_ALL} testte BH ilk sıra eşiği {0.10/N_ALL:.6f}.",
  "test_sayisi": N_ALL,
  "guven": "dusuk",
  "notlar": f"IS t {s2['is_t']:.2f} (anlamsız), OOS t {s2['oos_t']:.2f}; yıl yıl 7/9 pozitif, 2026'da tek işlem (-149 bp); 2026 hariç t 3,04. IS dönemi USO'nun 2020 Nisan negatif fiyat ve çok vadeli yapıya geçiş dönemini içerir (2020: 9 işlem, ort. +28 bp). Önceden hipotez değildi (veri madenciliği riski). USO ve UCO PTP: USCF'nin 31.07.2026 qualified notice'ının 92 günü ~31.10.2026'da doldu, yenisi bulunamadı; %10 brüt stopaj uygulanırsa işlem başına ~-1000 bp => beklenti negatif. Midas'ta USO/UCO bulunurluğu doğrulanamadı. Son durum: 06.11.2026 USO kapanışı 148,41, alt bant ~144,5 (sinyal yok).",
  "betik": os.path.join(K, "aday_S3_uso_bb_gecikmeli.py")},
]
for s_ in strat:
    s_.pop("oos_net_bp_t", None)

# ---------------- izleme listesi ----------------
def row(sym, karar, gerekce):
    t = T.loc[sym]
    return {"sym": sym, "tv": TV[sym], "karar": karar, "likidite_mn_usd": r1(t.med_dollar_vol_m), "maliyet_bp": r1(t.cost_rt_bp),
            "vol_1d_bp": r1(t.vol_1d_bp), "gerekce": f"[{O.PTP[sym]}] maliyet/oynaklık {t.cost_rt_bp / t.vol_1d_bp:.3f}. " + gerekce}
izleme = [
 row("USO", "kabul", "Ham petrolün en likit ETF'i (745 mn$, 14 bp); S2 adayının aracı; NYMEX:CL1! ile gece/gündüz izlenebilir. PTP: %10 brüt satış stopajı riski (USCF bildirimi 31.10.2026'da süresi doldu) -> her işlemden önce uygulamada kontrol; Midas'ta bulunurluk doğrulanamadı. 2020 sonrası çok vadeli/5 günlük roll yapısı."),
 row("XLE", "kabul", "Ailenin en likit ve PTP'siz aracı (2 mlr$, 13,6 bp). Doğrulanmış strateji yok (EN06 yetişme, EN08 IBS elendi; S2 sinyaliyle t 1,80); sürücüleri net (petrol, S&P 500). Enerjide PTP riski almadan yön görüşü için ana araç."),
 row("KOLD", "kabul", "S1 adayının aracı (-2x doğalgaz, 97 mn$, 16 bp). Koşullu: Midas'ta bulunurluk doğrulanamadı; ProShares Trust II PTP (26.02.2026 bildirimi 92 gün geçerliydi, sonrası kontrol edilmedi). Kaldıraç bozulması: koşulsuz günlük ort. -10 bp; yalnız 1 günlük tutuş için."),
 row("BNO", "yedek", "Brent; USO ile 0,97-0,98 korelasyon (bağımsız kanıt değil). USO yerine kullanılabilir (91 mn$, 16 bp); aynı PTP (USCF) riski."),
 row("UCO", "yedek", "2x ham petrol (115 mn$, 16 bp); S2 sinyalinin kaldıraçlı aracı (net 225 bp, aynı sinyal). PTP (ProShares Trust II); Midas'ta doğrulanamadı; oynaklık bozulması."),
 row("SCO", "yedek", "-2x ham petrol (102 mn$, 17 bp); açığa satış olmadığından petrol düşüş görüşü için tek pratik araç. Doğrulanmış strateji yok. PTP."),
 row("UNG", "yedek", "Doğalgaz dayanak referansı (137 mn$, 22,7 bp). Uzun vadeli negatif sürüklenme (koşulsuz -10 bp/gün); EIA günü long tutmayın. PTP ve Midas'ta 2024'te %10 kesinti şikâyeti belgelenmiş. Long araç olarak önerilmez."),
 row("BOIL", "yedek", "2x doğalgaz (146 mn$, 18 bp); yalnız güçlü kısa vadeli long görüş için. Koşulsuz -36 bp/gün bozulma; EIA günü (Perşembe) ortalama -85 bp. PTP; Midas'ta doğrulanamadı."),
 row("XOP", "yedek", "PTP'siz petrol/gaz üreticileri (532 mn$, 14 bp, oynaklık XLE'den yüksek). XLE ile 0,92-0,94 korelasyon. S2 sinyaliyle net 131 bp t 2,49 ama h=1/h=3'te ~0 (kırılgan)."),
 row("DRIP", "yedek", "-2x XOP (55 mn$, 16 bp); PTP'siz enerji düşüş aracı (ERY'den likit/ucuz). Doğrulanmış strateji yok."),
 row("PDBC", "yedek", "K-1'siz geniş emtia (92 mn$, 17 bp), USO ile 0,89 korelasyon: petrol görüşü için PTP'siz ama düşük oynaklıklı vekil (maliyet/oynaklık 0,13). Doğrulanmış strateji yok."),
 row("USL", "red", "Likidite 0,57 mn$, maliyet 47 bp; USO kopyası (12 aylık şerit)."),
 row("UNL", "red", "Likidite 0,45 mn$, maliyet 47 bp; UNG kopyası. Kontango vekili (UNG/UNL) testi de elendi."),
 row("UGA", "red", "Likidite 3,5 mn$, maliyet 27 bp; USO ile 0,86 korelasyon; strateji yok."),
 row("DBO", "red", "11 mn$, 20 bp, K-1 (muhtemel PTP); USO kopyası (0,95). USO tercih edilir."),
 row("DBC", "red", "PDBC kopyası (0,98) ve K-1 (muhtemel PTP); daha az likit (22 mn$, 20 bp)."),
 row("GSG", "red", "K-1 (muhtemel PTP), 25 mn$, 20 bp; PDBC/USO ile 0,94-0,97 korelasyon."),
 row("COMT", "red", "7,7 mn$, 27 bp; GSG/PDBC kopyası."),
 row("BCI", "red", "Maliyet/oynaklık 0,17 (günlük oynaklık 115 bp), strateji yok."),
 row("DBA", "red", "Maliyet/oynaklık 0,28 (günlük oynaklık 72 bp); K-1; strateji yok."),
 row("CORN", "red", "4,7 mn$, 27 bp, maliyet/oynaklık 0,25; K-1; strateji yok."),
 row("WEAT", "red", "10 mn$, maliyet/oynaklık 0,13; K-1; genel kütüphanede tutarlı sinyal yok."),
 row("SOYB", "red", "1,8 mn$, 47 bp, maliyet/oynaklık 0,55."),
 row("CANE", "red", "2,5 mn$, 27 bp. Petrolün gecikmeli etkisi istatistiksel olarak gerçek (FDR) ama 10 bp/sd < 27 bp maliyet ve yalnız düşüş yönünde."),
 row("OIH", "red", "Likit (134 mn$, 16 bp) ama XLE ile 0,86 korelasyon ve ayrı strateji yok; XLE/XOP yeterli."),
 row("ERX", "red", "2x XLE, 29 mn$, 20 bp; strateji yok, kaldıraç bozulması; XLE tercih edilir."),
 row("ERY", "red", "-2x XLE, 17,7 mn$, 22,8 bp; DRIP daha likit ve ucuz."),
 row("GUSH", "red", "2x XOP, 29 mn$, 20 bp; strateji yok."),
]

# ---------------- lead-lag ----------------
CAL = {
 "ham_petrol": "EIA WPSR Çar 10:30 ET (TR 18:30; 12 Kas Per 12:00 ET); API Salı 16:30 ET; CL vadesi 20 Kas, 21 Ara 2026; USO roll 1-7 Ara 2026; OVX >= 1,25xSMA20 iken boyutu küçült.",
 "dogalgaz": "EIA depolama: 13 Kas Cum, 19 Kas, 25 Kas Çar 12:00 ET, 3/10/17/24/31 Ara (TR 18:30); NG vadesi 25 Kas, 29 Ara; UNG roll 11-16 Kas, 15-18 Ara; BOIL/KOLD roll 8-14 Ara 2026.",
 "enerji_hisse": "EIA WPSR (Çar); CPI 10 Kas, NFP 4 Ara, FOMC 9 Ara 2026; yarım gün 27 Kas (TR 21:00).",
 "genis_emtia": "EIA WPSR (Çar); CPI 10 Kas, FOMC 9 Ara 2026; dolar şokları.",
}
GROUP = {"USO": "ham_petrol", "BNO": "ham_petrol", "UCO": "ham_petrol", "SCO": "ham_petrol", "UNG": "dogalgaz", "BOIL": "dogalgaz",
         "KOLD": "dogalgaz", "XLE": "enerji_hisse", "XOP": "enerji_hisse", "DRIP": "enerji_hisse", "PDBC": "genis_emtia"}
EIA_ONC = {"KOLD": ("+", 2.243, 1.968, 1.217, "Kas-Mar rapor günü KOLD +95 bp (diğer günler -20 bp); S1 net +100 bp (2.500$)"),
           "UNG": ("-", -2.32, -2.20, -1.17, "Kas-Mar rapor günü UNG -65 bp (diğer günler -5 bp); long araç için kaçın sinyali"),
           "BOIL": ("-", -3.08, None, None, "Kas-Mar rapor öncesi gün BOIL long net -137 bp; kaçın sinyali")}
leadlag = []
for sym in ["USO", "XLE", "KOLD", "BNO", "UCO", "SCO", "UNG", "BOIL", "XOP", "DRIP", "PDBC"]:
    d = LL[sym]
    onc = []
    if sym in EIA_ONC:
        yon, t_, ti, to, etki = EIA_ONC[sym]
        onc.append({"ad": "EIA doğalgaz depolama raporu takvimi (Kasım-Mart) — takvim olayı, gecikmeli fiyat öncüsü değil", "tv": "yok (takvim: ir.eia.gov/ngs/schedule.html)",
                    "tip": "takvim_olayi (doğrulanmamış: FDR geçmiyor, post-hoc mevsim ayrımı)", "etki": etki, "fdr": False, "t": t_, "is_t": ti, "oos_t": to,
                    "maliyet_sonrasi": "KOLD +100 bp net; UNG/BOIL long negatif", "ufuk": "1 gün (rapor günü)"})
        onc[-1] = {k: v for k, v in onc[-1].items() if v is not None}
    best1 = d["en_guclu_gecikmeli"].split("; ")[0]
    not_ = (f"Doğrulanmış gecikmeli öncü YOK (ölçüt: FDR + IS/OOS aynı işaret + bp/sd > {O.cost(sym):.0f} bp maliyet; geçen 0). "
            f"En güçlü geçmeyen: {best1}. Yetişme boşluğunun kendi getirisine ek katkısı: {d['yetisme_ek']}. Sürücüler eşzamanlıdır, öncü değildir.")
    if sym in ("USO", "UCO"):
        not_ += " Kendi fiyat sinyali: S2 (düşük güven)."
    leadlag.append({"sym": sym,
                    "suruculer": [{"ad": x["ad"] + "", "tv": x["tv"], "corr_1y": x["corr_1y"], "beta_1y": x["beta_1y"]} for x in d["suruculer"][:3]],
                    "onculer": onc, "gercek_zamanli": d["gercek_zamanli"], "not": not_, "takvim_riskleri": CAL[GROUP[sym]]})

elenen = [
 {"ad": "Genel kütüphane (31 sinyal x C0/O1/C1 x h1-3) aile genelinde", "neden": "8 bağımsıza yakın küme temsilcisinde (USO, UNG, XLE, OIH, DBA, CORN, WEAT, CANE) tutarlı sinyal yok: en yüksek Stouffer t 2,10 (VX_backw_donus C0 h2, IS&OOS pozitif yalnız 2/8). Tek yönlü (net>0) BH-FDR: 8316 satırda 0 geçen."},
 {"ad": "EN01 tam yıl: EIA öncesi gün KOLD long (önceden belirlenmiş hipotez)", "neden": f"C0 h1 net {s1full['mean_net_bp']:.0f} bp, t {s1full['t']:.2f} < 2; en iyi %5 işlem çıkarılınca brüt -13 bp. Nisan-Ekim'de etki yok (t 0,10). Yalnız Kas-Mar alt kümesi S1 olarak düşük güvenle tutuldu."},
 {"ad": "EN02 kontango vekili k20 = Δ20 ln(UNL) - Δ20 ln(UNG) > 0 -> KOLD long", "neden": "C0 h3 net 103 bp t 2,29 ama komşu pencereler kırılgan (k10 t 0,54; k40 t 0,96; k60 t 0,51); UNG ileri getirisi ~ k20 regresyonu t -0,99. Parametre şansı."},
 {"ad": "EN03 UNG roll penceresi (R1 öncesi KOLD long; roll günü UNG-UNL farkı) ve BOIL/KOLD roll günleri", "neden": "KOLD C0 h1-3 t <= 1,13, IS/OOS işaret değiştiriyor; UNG-UNL roll günü farkı -15 vs -6 bp (t -0,89). BOIL-2xUNG roll günü farkı t 1,89 (tanımlayıcı, ters yönde)."},
 {"ad": "NG son işlem günü ve ertesi (vadeler.csv)", "neden": "UNG vade günü +31 bp (t 1,61), ertesi -56 bp (t -1,38); IS ve OOS işaret değiştiriyor."},
 {"ad": "Doğalgaz mevsimselliği (Kas-Mar) ve haftanın günü", "neden": "UNG Kas-Mar günlük -22 vs -2 bp (t -1,37); Aralık -60 bp (t -2,13; 12 aydan biri, çoklu test). Haftanın günü: yalnız Çarşamba->Perşembe (EIA) anlamlı; o da S1/EN01'in kopyası."},
 {"ad": "Doğalgaz büyük gün sonrası devam/dönüş (MO_z1_gt_2, MR_z1_lt_m2; UNG/BOIL/KOLD)", "neden": "Hiçbir mod/ufukta pozitif t > 1 yok; IS ve OOS çoğunlukla ters işaretli (ör. UNG MO_z1_gt_2 C0 h1 IS +33, OOS -341 bp)."},
 {"ad": "EN04 EIA WPSR günü (petrol)", "neden": "USO |getiri| oranı 1,04 (t 0,78); yön yok; WPSR öncesi USO long O1 h1 net -25 bp. Risk/boyut kuralı olarak bile zayıf."},
 {"ad": "EN05 USO roll günleri", "neden": "USO-USL roll günü farkı -3 vs -2 bp (t -0,24); 2020 öncesi -20 bp (t -1,04), sonrası 0. Önden koşma izi yok (literatürle uyumlu)."},
 {"ad": "EN06 petrol -> XLE/XOP/OIH yetişme (z(res)>=2) ve tersi (XLE -> USO)", "neden": "XLE C0 h1 net 50 bp t 1,37 yalnız IS (OOS 1,5 bp), O1/C1 negatif; kendi getirisi kontrollü yetişme katsayısı t 0,56 (h1), 0,91 (h3). Tersi USO long: tüm modlarda negatif."},
 {"ad": "EN07 OVX sıçraması (OVX >= 1,25 x SMA20) yön sinyali olarak", "neden": "USO long C0 h3 net -186 bp, XLE ~0. Yalnız oynaklık bilgisi geçerli: 3 günlük |hareket| 2,4 kat (t 5,8) -> kaldıraçlı petrol pozisyonunu küçültme kuralı olarak kullanılabilir."},
 {"ad": "EN08 enerji IBS < 0,15 ve C > SMA200 (XLE, XOP, USO, BNO)", "neden": "Net ortalamalar -32..+5 bp; hiçbir ETF/modda t > 0,4 yok."},
 {"ad": "USO/USL eğri vekili (c20 > 0 -> USO long)", "neden": "C0 h3 net 25 bp t 1,47; O1 h1 negatif; regresyon t 0,44."},
 {"ad": "BNO-USO (Brent-WTI) yayılımı ortalamaya dönüş (z20 <= -2 / >= 2)", "neden": "İleri yayılım ~ z regresyonu t -0,15 (h1), 0,46 (h3); kurallar t < 0,4 ya da negatif."},
 {"ad": "VX_backw_donus (VIX/VIX3M 1'in altına dönüş) -> USO/BNO/UCO C1 h2", "neden": "Eşiği biçimsel geçiyor (USO net 162 bp t 2,43, n 51) ama 2026'nın 6 işlemi toplam net getirinin ~%58'i; 2026 hariç ~77 bp, t ~1,2. PTP'siz XLE'de t 1,37 (OOS t 0,45); C0/O1 h1 negatif; SPY'de etki yok; taramadan seçildi."},
 {"ad": "MR_bb20_alt her ETF'in KENDİ bandıyla (BNO, XLE, XOP, OIH, PDBC)", "neden": "C1 h2'de BNO net 40 bp t 0,90; XLE -20; XOP -42; OIH -36; PDBC -1. Yalnız USO'nun sinyal günleri işe yarıyor (S2 düşük güven)."},
 {"ad": "CANE <- petrol (leadlag_sweep'te FDR geçen tek gecikmeli öncü; sweep catch DBO<-BNO h3 FDR geçen diğer satır)", "neden": "CANE: etki 10-12 bp/sd < 27 bp maliyet; z1(BNO) >= 1 sonrası CANE C0 h1 brüt +2 bp (net -25); etki yalnız petrol düşüş günlerinde (kaçın sinyali); likidite 2,5 mn$. DBO<-BNO yetişme h3: OOS t 1,03, DBO bir USO kopyası (11 mn$, K-1)."},
 {"ad": "XOP <- UNG (z1(UNG) >= 2 -> XOP long)", "neden": "C0 h1 net 36 bp t 0,89 yalnız IS; OOS -25 bp; O1/C1 ~0 ya da negatif. Sweep'te lag t 2,0-2,5 ama FDR yok ve 12-22 bp/sd ~ maliyet."},
 {"ad": "Genel kütüphanede eşiği biçimsel geçen diğer tek-ETF satırları", "neden": "DBO MR_3gun_dusus C0 h3 (t 2,39): kopyaları USO -3 bp, BNO +10 bp. BNO MR_rsi2_lt10_ust200 C0 h3 (t 2,05): USO t 1,1, XLE ~0. UCO/BNO VX_kontango_09 C0 h3 (t 2,0-2,1): O1/C1'de t <= 1,3 (VIX 16:15 kapanışına bağımlı), XLE/XOP ~0. CANE MO_z1_gt_2 C1 h3 (t 2,69): DBA -33, CORN -21 bp. ERY MO_z1_gt_2 O1 h2 (t 2,13): OOS t 1,35, IS 2020 aykırılarıyla şişkin. GUSH MO_3gun_yukselis C1 h3: OOS 0,3 bp. KOLD CA_sal O1 h2 (t 2,03): Çarşamba açılış -> Perşembe kapanış = EIA etkisi (S1 kapsamında)."},
 {"ad": "Tarım ve geniş emtia ETF'leri (DBA, CORN, WEAT, SOYB, CANE, DBC, GSG, COMT, BCI)", "neden": "Maliyet/oynaklık 0,12-0,55 ve likidite düşük; genel kütüphanede aile içinde tutarlı sinyal yok (tek ETF sonuçları, ör. CANE MO_z1_gt_2 C1 h3 t 2,69, tarım kümesinde tekrar etmiyor). Petrol/SPY'nin kendi gecikmesine ek katkısı DBA/CORN/WEAT/SOYB'de anlamsız."},
]

ozet = (f"enerji_tarim ailesinde (28 ETF; bağımsıza yakın 5 küme: ham petrol+geniş emtia, doğalgaz, enerji hisseleri, tarım, şeker) toplam {N_ALL} test yapıldı "
        f"({N_OWN} aileye özel + {N_GEN} genel kütüphane satırı). BH-FDR (q=0,10) birleşik testte HİÇBİR long strateji geçmiyor; güvenilir, işlenebilir strateji bulunamadı. "
        "Eşiği biçimsel geçen iki zayıf aday düşük güvenle raporlandı: S1 EIA doğalgaz raporu öncesi KOLD (yalnız Kasım-Mart; net +100 bp/işlem, t 2,24, post-hoc mevsim ayrımı) ve "
        "S2 USO alt Bollinger kırılımından 1 gün sonra 2 günlük USO long (net +121 bp, t 2,95, genel taramadan seçildi, t kapanışında girişte zararlı). "
        "İkisi de PTP ürünlerinde (KOLD, USO/UCO): Midas'ta %10 brüt satış stopajı uygulanırsa işlem başına ~-1000 bp ile beklenti negatife döner; uygulamada PTP ibaresi/kesinti yoksa ve ürün bulunuyorsa düşünülmeli. "
        "En sağlam bulgu bir KAÇIN kuralı: UNG/BOIL long'unu EIA günü (genelde Çarşamba kapanışı -> Perşembe kapanışı) taşımayın (UNG rapor günü brüt -28 bp; 2018-2026 her yıl brüt negatif). "
        "Aile hedefleri için doğrulanmış gecikmeli öncü yok; öncü izlenimi veren CANE<-petrol etkisi maliyetin altında. Gerçek zamanlı izleme: NYMEX:CL1!, ICEEUR:BRN1!, NYMEX:NG1!/NG2!, ICEENDEX:TFM1!, CME_MINI:ES1!. "
        "İzleme listesi: kabul USO, XLE, KOLD; yedek BNO, UCO, SCO, UNG, BOIL, XOP, DRIP, PDBC; PTP'siz enerji aracı XLE/XOP/DRIP/PDBC.")

dosyalar = [os.path.join(ROOT, "notlar", "aile_enerji_tarim.md"), os.path.join(O.OUT, "sonuc.json"), O.OUT + "/ (tüm tablolar)",
            os.path.join(K, "aday_S1_eia_kold.py"), os.path.join(K, "aday_S3_uso_bb_gecikmeli.py"), os.path.join(K, "aday_S2_vix_backw_petrol.py"),
            os.path.join(K, "fdr_toplam.py"), os.path.join(K, "h_dogalgaz.py"), os.path.join(K, "h_petrol.py"), os.path.join(K, "h_tarim_leadlag.py"),
            os.path.join(K, "leadlag_ozet.py"), os.path.join(K, "alt_kume.py"), os.path.join(K, "rapor_json.py")]
res = {"family": "enerji_tarim", "ozet": ozet, "izleme": izleme, "stratejiler": strat, "elenen": elenen, "leadlag": leadlag, "dosyalar": dosyalar,
       "tv_dogrulanacak": []}
json.dump(res, open(os.path.join(O.OUT, "sonuc.json"), "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: (v if k in ("family", "ozet") else len(v)) for k, v in res.items()}, ensure_ascii=False, indent=1))
for s_ in strat:
    print(s_["id"], {k: s_[k] for k in ["n", "brut_bp", "net_bp", "t", "is_net_bp", "oos_net_bp", "yil_pozitif", "kazanma", "pf", "maxdd", "en_kotu_bp"]})
    print("  ", s_["maliyet_duyarlilik"]); print("  ", s_["aile_ici"][:400])
