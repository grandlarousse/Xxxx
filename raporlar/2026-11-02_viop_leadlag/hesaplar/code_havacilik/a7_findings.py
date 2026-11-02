"""A7: f_havacilik.csv üretimi (sayılar res/ altındaki sonuç dosyalarından çekilir)."""
from h import *
A1 = pd.read_csv(RES + "/a1_pairs.csv"); BT = pd.read_csv(RES + "/a5b_attrib.csv"); B5 = pd.read_csv(RES + "/a5_bt.csv")
H4 = pd.read_csv(RES + "/a4_hourly.csv"); BR = pd.read_csv(RES + "/a3_brent_regime.csv")
COLS = "stock,driver_yahoo,driver_desc,tv_ticker,relation,lag,corr_full,corr_3y,corr_1y,pcorr_xu100,beta,t_stat,gap_corr,intra_corr,is_oos,bt_oos_sharpe,bt_oos_mean_bps,n,confidence,mechanism,notes".split(",")
TV = {"BZ=F": "ICEEUR:BRN1! / TVC:UKOIL", "HO=F": "NYMEX:HO1!", "CL=F": "NYMEX:CL1!", "LHA.DE": "XETR:LHA", "AF.PA": "EURONEXT:AF", "IAG.L": "LSE:IAG",
      "EZJ.L": "LSE:EZJ", "RYAAY": "NASDAQ:RYAAY", "WIZZ.L": "LSE:WIZZ", "JET2.L": "LSE:JET2", "DAL": "NYSE:DAL", "UAL": "NASDAQ:UAL", "AAL": "NASDAQ:AAL",
      "JETS": "AMEX:JETS", "ADP.PA": "EURONEXT:ADP", "FRA.DE": "XETR:FRA", "AENA.MC": "BME:AENA", "FHZN.SW": "SIX:FHZN", "TUI1.DE": "XETR:TUI1",
      "MEL.MC": "BME:MEL", "TUR": "NASDAQ:TUR ?", "^VIX": "CBOE:VIX / TVC:VIX", "TRY=X": "FX:USDTRY", "EURUSD=X": "FX:EURUSD", "^TA125.TA": "TASE:TA125 ?",
      "BA": "NYSE:BA", "AIR.PA": "EURONEXT:AIR", "AER": "NYSE:AER", "ELAL.TA": "TASE:ELAL ?", "9202.T": "TSE:9202", "THYAO.IS": "BIST:THYAO", "PGSUS.IS": "BIST:PGSUS",
      "TAVHL.IS": "BIST:TAVHL", "CLEBI.IS": "BIST:CLEBI", "BKNG": "NASDAQ:BKNG", "011170.KS": "KRX:011170 ?", "ES=F": "CME_MINI:ES1!",
      "JETCRACK": "formül: NYMEX:HO1!*42-ICEEUR:BRN1!", "EUAIR+USAIR": "formül sepeti (XETR:LHA,EURONEXT:AF,LSE:IAG,EURONEXT:RYA?,LSE:EZJ,LSE:WIZZ,LSE:JET2 | NYSE:DAL,NASDAQ:UAL,NASDAQ:AAL,NYSE:LUV,NYSE:ALK,NASDAQ:JBLU)"}
rows = []
def pair(st, drv, rel, conf, mech, notes="", desc=None, lead=False):
    x = A1[(A1.stock == st) & (A1.driver == drv)].iloc[0]
    o = dict(stock=st, driver_yahoo=drv, driver_desc=desc or x["desc"], tv_ticker=TV.get(drv, "?"), relation=rel, lag=(1 if lead else 0),
             corr_full=x.corr_full, corr_3y=x.corr_3y, corr_1y=x.corr_1y, pcorr_xu100=x.pcorr_xu100, beta=x.beta,
             t_stat=(x.intra_t if rel == "lead_intra" else x.gap_t if rel == "lead_gap" else x.t_sync), gap_corr=x.gap_corr, intra_corr=x.intra_corr,
             is_oos=(f"intra t IS {x.intra_IS_t:.2f} / OOS {x.intra_OOS_t:.2f}" if lead else f"pc IS {x.pc_IS:.3f} / OOS {x.pc_OOS:.3f}; yıl-işaret {x.yrs_pc_same_sign:.0%}"),
             bt_oos_sharpe=np.nan, bt_oos_mean_bps=np.nan, n=int(x.n), confidence=conf, mechanism=mech, notes=notes)
    rows.append(o)
def manual(**k):
    o = {c: np.nan for c in COLS}; o.update(k); rows.append(o)
# --- senkron sektör emsalleri
for st, drv, conf in [("THYAO", "LHA.DE", "YÜKSEK"), ("THYAO", "EZJ.L", "YÜKSEK"), ("THYAO", "IAG.L", "YÜKSEK"), ("THYAO", "AF.PA", "ORTA"), ("THYAO", "RYAAY", "ORTA"),
                      ("PGSUS", "EZJ.L", "YÜKSEK"), ("PGSUS", "IAG.L", "YÜKSEK"), ("PGSUS", "FRA.DE", "ORTA"), ("PGSUS", "LHA.DE", "ORTA"),
                      ("TAVHL", "ADP.PA", "ORTA"), ("TAVHL", "IAG.L", "ORTA"), ("TAVHL", "FRA.DE", "ORTA"), ("TAVHL", "AENA.MC", "ORTA")]:
    pair(st, drv, "sync", conf, "Küresel havacılık talep/yakıt/jeopolitik ortak faktörü; Avrupa BIST ile neredeyse senkron (kapanış +0,5-1,5 sa)",
         "A2 taramasında (16.365 test, BH-FDR) her üç hissenin XU100-kontrollü en yüksek kısmi korelasyonları havacılık sembolleri" + ("; ADP TAV'ın %46 ortağı" if drv == "ADP.PA" else ""))
for st in STOCKS:
    pair(st, "JETS", "sync", "ORTA", "ABD havayolu faktörü; lag0 BIST kapanışı sonrası 5-6 saati de içerir", "senkron kısmi corr ~0,11-0,13")
pair("THYAO", "PGSUS.IS", "sync", "YÜKSEK", "Aynı sektör/talep/yakıt/kur maruziyeti", "kısmi corr 0,51; 2013+ tüm yıllar pozitif")
pair("TAVHL", "PGSUS.IS", "sync", "YÜKSEK", "Yolcu trafiği ortak faktörü (Sabiha Gökçen değil; TAV yolcu geliri)", "kısmi 0,29")
pair("THYAO", "CLEBI.IS", "sync", "ORTA", "Yer hizmetleri (Çelebi) aynı trafik faktörü", "")
# --- Brent rejimi
for st in STOCKS:
    b = BR[(BR.stock == st)]; y26 = b[b.year == "2026"].pc.values[0]; w = b[b.year == "2026_war_Mar-Oct"]["corr"].values[0]
    pair(st, "BZ=F", "regime", "ORTA" if st != "TAVHL" else "DÜŞÜK",
         "Yakıt maliyeti (THY 2026 hedge ~%48, PGSUS ~%61-68) + 2026 Orta Doğu savaşında petrol = Türkiye/bölge risk faktörü",
         f"Tam dönem zayıf; 2026 kısmi {y26:.2f}, savaş dönemi (Mar-Eki 2026) corr {w:.2f}; 2020-21'de işaret pozitif (talep toparlanması). TAVHL'de yalnız 2022 ve 2026'da negatif")
pair("THYAO", "HO=F", "sync", "DÜŞÜK", "Jet yakıtı proxy (ULSD)", "Brent'e ek bilgi yok; HO korelasyonları Brent ile neredeyse aynı")
pair("PGSUS", "JETCRACK", "lead_intra", "DÜŞÜK", "Rafineri marjı jet yakıtı maliyetini Brent üstüne artırır", "senkron ~0; lag1->intra -0,036 t-1,95; hedge Brent bazlı olduğundan crack hedge'siz kısım", lead=True)
# --- öncülük: gap (işlenemez) ve intra
for st in STOCKS:
    pair(st, "JETS", "lead_gap", "ORTA", "Eşzamansız kapanış: ABD havayolları BIST kapanışından sonra kapanır, bilgi ertesi açılışta fiyatlanır", "İŞLENEBİLİR DEĞİL (açılış gap'i)", lead=True)
pair("PGSUS", "EZJ.L", "lead_intra", "ORTA", "Avrupa havayolu bilgisinin PGSUS'a yavaş yayılması (gün-içi devam, gap'te değil)", "A2'de FDR geçer; tek tek sembol seçimi tarama kaynaklı", lead=True)
pair("THYAO", "RYAAY", "lead_intra", "ORTA", "ABD seansındaki havayolu haberi açılışta eksik fiyatlanıyor", "", lead=True)
pair("THYAO", "TUR", "lead_intra", "ORTA", "Gap aşırı tepkisinin gün-içi dönüşü: TUR (ABD'deki Türkiye ETF'i) t-1 yükselirse THYAO yukarı açılıp gün içinde geri veriyor",
     "A2'de FDR geçer (en güçlü THYAO intra bulgusu); PGSUS/TAVHL'de zayıf; tek başına backtest OOS t 1,15", lead=True)
pair("THYAO", "TRY=X", "lead_intra", "DÜŞÜK", "TL değer kaybı (FX düzeltmeli, gün t-1 UTC) -> döviz gelirli THYAO gün-içi pozitif",
     "IS güçlü (t 4,0) OOS yok (t 0,05); yıllar çok istikrarsız (2022/2024/2025 negatif)", lead=True)
for st in STOCKS:
    pair(st, "TRY=X", "sync", "DÜŞÜK", "Döviz geliri hipotezi (THY USD fonksiyonel, PGSUS %50 EUR/%28 USD gelir)",
         "FX düzeltmesi sonrası XU100-kontrollü kısmi corr ~0 (THYAO 47 hisse içinde 25., PGSUS 33., TAVHL 6.) -> hipotez günlük TL getirisinde DESTEKLENMİYOR")
pair("PGSUS", "EURUSD=X", "sync", "ÇOK DÜŞÜK", "EUR gelir / USD maliyet", "kısmi corr | XU100,USDTRY 0,008 (13./47)")
pair("THYAO", "^VIX", "lead_gap", "DÜŞÜK", "Genel risk iştahı (havacılığa özgü değil)", "senkron kısmi ~0; lag1->gap -0,13 t-6 (eşzamansız)", lead=True)
pair("THYAO", "^TA125.TA", "sync", "ÇOK DÜŞÜK", "İsrail/Orta Doğu riski", "kısmi corr 0,02; olay bazında etki var (aşağı bkz.)")
pair("THYAO", "BA", "sync", "DÜŞÜK", "Uçak üreticisi/teslimat", "kısmi 0,05")
pair("TAVHL", "AIR.PA", "sync", "DÜŞÜK", "Uçak üreticisi (talep döngüsü)", "kısmi 0,09; yalnız sektör betası")
pair("THYAO", "AER", "sync", "ÇOK DÜŞÜK", "Uçak kiralama", "kısmi 0,05")
pair("THYAO", "ELAL.TA", "sync", "ÇOK DÜŞÜK", "Bölgesel havayolu", "kısmi 0,02")
pair("PGSUS", "TUI1.DE", "lead_intra", "DÜŞÜK", "Avrupa paket turizm talebi", "FDR geçer ama IS/OOS t<2,5", lead=True)
pair("THYAO", "PGSUS.IS", "reverse", "ÇOK DÜŞÜK", "PGSUS -> THYAO yönü", "PGSUS_{t-1} -> THYAO intra ~0 (yok)")
pair("PGSUS", "THYAO.IS", "lead_gap", "DÜŞÜK", "Büyük/likit hisseden küçüğe gecikmeli yayılım", "THYAO_{t-1}->PGSUS gap t 3,1, intra t 1,6; çok değişkenli modelde (havayolu sepetleri + PGSUS kendi) emiliyor; h1/m5 gün-içi lead YOK; B4 backtest OOS Sharpe 0,22", lead=True)
# --- backtestler
for st in STOCKS:
    for sig, conf, mech, note in [("AIR_only(eu+us)", "ORTA", "Avrupa+ABD havayolu sepetlerinin (STOXX/SPX'e göre artık, kayan beta) t-1 getirisi -> BIST açılışında pozisyon, kapanışta çık",
                                   "XU100/XU030 gün-içinde etki yok (hisseye özgü); sinyal 1 gün bayatlarsa (t-2) etki kaybolur; 2020-21 katkısı büyük"),
                                  ("COMBO", "ORTA", "AIR_only + (-TUR) birleşimi |z|>1", "TUR bacağı tam dönem bulgusundan sonra eklendi -> IS/OOS gerçek holdout değil; XU030 hedge'li versiyon (maliyet 16-24 bps) KÂRSIZ")]:
        x = BT[(BT.sig == sig) & (BT.target == st)].iloc[0]
        manual(stock=st, driver_yahoo="EUAIR+USAIR" if sig.startswith("AIR") else "EUAIR+USAIR-TUR", driver_desc=f"Backtest {sig} -> gün-içi", tv_ticker=TV["EUAIR+USAIR"],
               relation="lead_intra", lag=1, t_stat=x.OOS_t, is_oos=f"IS {x.IS_mean_bps:.1f}bps t{x.IS_t:.2f} SR{x.IS_sharpe:.2f} / OOS {x.OOS_mean_bps:.1f}bps t{x.OOS_t:.2f}",
               bt_oos_sharpe=x.OOS_sharpe, bt_oos_mean_bps=x.OOS_mean_bps, n=int(x.IS_n + x.OOS_n), confidence=conf if not (sig == "AIR_only(eu+us)" and st == "TAVHL") else "DÜŞÜK",
               mechanism=mech, notes=note + "; maliyet 8 bps (15 bps'de ~7 bps düş)")
for st in STOCKS:
    x = B5[(B5.bt == "B2a_BrentShock->intra") & (B5.stock == st) & (B5.cost == 8)].set_index("period")
    manual(stock=st, driver_yahoo="BZ=F", driver_desc="Backtest: Brent |z|>2 şokuna ters pozisyon, ertesi gün-içi", tv_ticker=TV["BZ=F"], relation="lead_intra", lag=1,
           t_stat=x.loc["OOS", "t"], is_oos=f"IS {x.loc['IS','mean_bps']:.1f}bps t{x.loc['IS','t']:.2f} / OOS {x.loc['OOS','mean_bps']:.1f}bps t{x.loc['OOS','t']:.2f}",
           bt_oos_sharpe=x.loc["OOS", "sharpe"], bt_oos_mean_bps=x.loc["OOS", "mean_bps"], n=int(x.loc["ALL", "n"]), confidence="DÜŞÜK",
           mechanism="Yakıt şoku -> havayolu marjı", notes="Brent-UP olay ortalaması: THYAO intra t+1 2014-20 -%0,83 (t-3,5) ama 2021-26 +%0,92 -> işaret dönüyor; TAVHL IS ters")
    h = H4[(H4.stock == st) & (H4.driver == "BZ=F")].iloc[0]; b5 = B5[(B5.bt == "B5_nightBrent->intra_thr0.01") & (B5.stock == st)].set_index("period")
    manual(stock=st, driver_yahoo="BZ=F", driver_desc="Saatlik: BIST kapanışı(15:00)->açılış(07:00 UTC) Brent hareketi", tv_ticker=TV["BZ=F"], relation="intraday_minutes", lag="15:00->07:00",
           gap_corr=h["N->gap_corr"], intra_corr=h["N->intra_corr"], t_stat=h["N->intra_t"], n=int(h.n),
           is_oos=f"B5 |N|>%1 ters: 2024-25 {b5.loc['2024-25','mean_bps']:.1f}bps / 2026 {b5.loc['2026','mean_bps']:.1f}bps t{b5.loc['2026','t']:.2f}",
           bt_oos_sharpe=b5.loc["2026", "sharpe"], bt_oos_mean_bps=b5.loc["2026", "mean_bps"], confidence="DÜŞÜK" if st != "TAVHL" else "DÜŞÜK",
           mechanism="Gece petrol hareketi açılışta fiyatlanıyor (gap corr ~-0,35/-0,43); 2026 savaş rejiminde gün-içi devam",
           notes="örneklem 2024-06+ (~560 gün), savaş dönemi baskın; gap kısmı nakitte işlenemez (VİOP akşam seansı test EDİLMEDİ)")
# --- olaylar
E = pd.read_csv(RES + "/a6_events.csv")
for ev_key, conf, mech in [("Orta Doğu savaşı", "DÜŞÜK", "Bölgesel savaş -> petrol + yolcu talebi + hava sahası riski"), ("İsrail'in İran'ı vurması", "DÜŞÜK", "Bölgesel savaş"),
                           ("ateşkesi", "DÜŞÜK", "Gerilim azalması"), ("Atatürk Havalimanı", "DÜŞÜK", "Terör/havalimanı güvenliği"), ("Pfizer", "DÜŞÜK", "Salgın/seyahat talebi"),
                           ("Rusya Türk jetini", "DÜŞÜK", "Turizm yaptırımı")]:
    e = E[E.event.str.contains(ev_key)]
    for r in e.itertuples():
        manual(stock=r.stock, driver_yahoo="EVENT", driver_desc=f"{r.t0} {r.event}", tv_ticker="-", relation="event", lag=0, t_stat=r.AR_t0_z,
               is_oos=f"AR t0 {r._8:.1f}% / CAR0-5 {r._11:.1f}%", n=1, confidence=conf, mechanism=mech, notes="tek olay; piyasa modeli artığı (XU100, beta[-260,-11])")
# --- tarama sürprizleri / hipotezler
manual(stock="THYAO", driver_yahoo="011170.KS", driver_desc="Lotte Chemical (Kore) t-1 -> THYAO gün-içi", tv_ticker="KRX:011170 ?", relation="lead_intra", lag=1, intra_corr=0.081,
       confidence="ÇOK DÜŞÜK", mechanism="Mekanizma yok (Kore kapanışı BIST t-1 açılışından önce)", notes="A2 FDR geçer; büyük olasılıkla çoklu test/sahte; Avrupa/EM döngüsel hisselerinin (8TRA.DE, SGO.PA, FSR.JO) PGSUS gün-içine sızması genel 'yavaş yayılım' etkisi olabilir")
manual(stock="THYAO", driver_yahoo="-", driver_desc="VİOP akşam seansında gece Brent/JETS hareketini işlemek", relation="hypothesis", confidence="ÇOK DÜŞÜK",
       mechanism="Gap'in ~%20-45'i gece sürücü hareketleriyle açıklanıyor", notes="yapılmadı: VİOP akşam seansı verisi yok")
manual(stock="PGSUS", driver_yahoo="-", driver_desc="Aylık yolcu/trafik verisi (KAP, DHMİ), mevsimsellik, bayram talebi", relation="hypothesis", confidence="ÇOK DÜŞÜK", mechanism="Talep", notes="yapılmadı")
F = pd.DataFrame(rows)[COLS]
F.to_csv(OUT + "/f_havacilik.csv", index=False, float_format="%.4f")
print(len(F), F.confidence.value_counts().to_dict())
