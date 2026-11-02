"""f_enerji.csv üretimi: senkron satırlar sync_pairs.csv'den otomatik, diğerleri sonuç dosyalarındaki değerlerle."""
import pandas as pd, numpy as np, elib
from elib import R, DEC, ll
SP = pd.read_csv(elib.RES + "/sync_pairs.csv"); SP = SP[SP.base == "TL"]
COLS = "stock,driver_yahoo,driver_desc,tv_ticker,relation,lag,corr_full,corr_3y,corr_1y,pcorr_xu100,beta,t_stat,gap_corr,intra_corr,is_oos,bt_oos_sharpe,bt_oos_mean_bps,n,confidence,mechanism,notes".split(",")
rows = []
def sync(stock, drv, conf, mech, notes="", tv=None, desc=None):
    r = SP[(SP.stock == stock) & (SP.driver_yahoo == drv)].iloc[0]
    rows.append({"stock": stock, "driver_yahoo": drv, "driver_desc": desc or r.driver_desc, "tv_ticker": tv or r.tv_ticker, "relation": "sync", "lag": 0,
                 "corr_full": r.corr_full, "corr_3y": r.corr_3y, "corr_1y": r.corr_1y, "pcorr_xu100": r.pcorr_xu100, "beta": r.beta, "t_stat": r.t_sync,
                 "gap_corr": r.gap_lag1_corr, "intra_corr": r.intra_lag1_corr, "is_oos": f"pc IS {r.pc_is:.2f} / OOS {r.pc_oos:.2f}; haftalık c={r.corr_w:.2f} pc={r.pcorr_w_xu100:.2f}; yıl işaret %{100*r.yr_same_sign:.0f}",
                 "n": int(r.n), "confidence": conf, "mechanism": mech, "notes": notes})
def man(**k): rows.append(k)
# --- backtest değerleri ---
xud = DEC("XU100"); tu = DEC("TUPRS")
US = pd.concat([R(s) for s in ["VLO", "MPC", "PSX", "PBF"]], axis=1).mean(axis=1).shift(1); US = US[US.index >= "2014-01-01"]
bt = {}
for lab, kw, c in [("s8", dict(mode="sign"), 8), ("s15", dict(mode="sign"), 15), ("z8", dict(mode="z", thr=1.0), 8), ("z15", dict(mode="z", thr=1.0), 15)]:
    res, _ = ll.backtest(US, tu.intra, cost_bps=c, **kw); bt[lab] = res
print({k: (round(v["IS"]["sharpe"], 2), round(v["OOS"]["sharpe"], 2), round(v["OOS"]["mean_bps"], 1)) for k, v in bt.items()})
# ===== TUPRS =====
sync("TUPRS", "CRAK", "YÜKSEK", "Küresel rafineri hisseleri ortak faktörü (marj beklentisi + enerji sektörü betası)", "ABD kapanışlı -> günlük lag0 kısmen BIST sonrası bilgi; haftalık daha temiz. 250g kayan corr hep >0 (0,12-0,54)")
sync("TUPRS", "BZ=F", "YÜKSEK", "Stok kazancı/kaybı + USD bazlı ürün fiyatlaması + enerji betası", "Aylık USD pc=0,35 (OOS 0,51); 2026 haftalık pc=0,64 (rejim). Seviye değil getiri.")
sync("TUPRS", "PKN.WA", "ORTA", "Avrupa entegre rafineri emsali (Orlen)", "AB rafineri sepeti (PKN,MOL,MOH,ELPE,NESTE,GALP,REP,OMV) aylık USD pc=0,43 (IS 0,32/OOS 0,58)")
sync("TUPRS", "REP.MC", "ORTA", "Avrupa rafineri/entegre emsal")
sync("TUPRS", "HO=F", "ORTA", "Dizel ürün fiyatı (Tüpraş üretiminin ~%33-39'u dizel); Brent ile aynı bilgi", "Brent'ten bağımsız katkı yok")
sync("TUPRS", "HO_CRACK", "DÜŞÜK", "Dizel crack (HO*42-BZ) marjı: teoride EBITDA sürücüsü", "OLUMSUZ: günlük/haftalık ~0; sadece çeyreklik ortalama crack değişimi aynı çeyrek pc=0,47 (n=68) ve 2025-26 haftalık pc 0,38/0,54. NY ULSD, Akdeniz dizelinin zayıf vekili; roll gürültüsü",
     tv="NYMEX:HO1!*42-ICEEUR:BRN1!")
sync("TUPRS", "C321", "DÜŞÜK", "3-2-1 crack", "OLUMSUZ: günlük/haftalık/aylık ~0")
sync("TUPRS", "AYGAZ.IS", "YÜKSEK", "Koç grubu: Aygaz, Tüpraş'ın dolaylı ortağı (Enerji Yatırımları) + LPG", "BIST içi")
sync("TUPRS", "TRY=X", "DÜŞÜK", "USD bazlı ürün fiyatlaması -> TL değer kaybında koruma hipotezi", "XU100 kontrollü USDTRY betası haftalık 0,10 (t=1,3), aylık 0,10 (t=0,9): piyasanın ötesinde 'dolar hissesi' etkisi zayıf. FX_FIX sonrası")
man(stock="TUPRS", driver_yahoo="VLO+MPC+PSX+PBF", driver_desc="ABD rafineri sepeti (eşit ağırlık) t-1 getirisi", tv_ticker="NYSE:VLO, NYSE:MPC, NYSE:PSX, NYSE:PBF (veya AMEX:CRAK)", relation="lead_intra", lag=1,
    t_stat=4.53, intra_corr=0.07, gap_corr=0.03, is_oos="hedge'li gün-içi t: IS 1.8 / OOS 3.95; tek VLO tarama H1 (FDR padj<0.001) IS t=3.76 OOS t=4.48",
    bt_oos_sharpe=round(bt["z8"]["OOS"]["sharpe"], 2), bt_oos_mean_bps=round(bt["z8"]["OOS"]["mean_bps"], 1), n=2788, confidence="ORTA",
    mechanism="Sektöre özgü bilgiye açılışta eksik tepki: ABD rafineri hareketinin ~%38'i gap'te, ~%62'si gün-içinde fiyatlanıyor (ES=F lag1 kontrolünde anlamlı, ES kendisi değil)",
    notes=f"BT1zo |z|>1 tek bacak: brüt IS 17,7 bps (t=2,4) OOS 25,6 (t=2,3); net Sharpe 8bps IS {bt['z8']['IS']['sharpe']:.2f}/OOS {bt['z8']['OOS']['sharpe']:.2f}, 15bps IS {bt['z15']['IS']['sharpe']:.2f}/OOS {bt['z15']['OOS']['sharpe']:.2f}. İşaret (filtresiz) 8bps: IS {bt['s8']['IS']['sharpe']:.2f}/OOS {bt['s8']['OOS']['sharpe']:.2f}. 2017 ve 2021 negatif. Hedge'li (2 bacak) net negatif/0.")
man(stock="TUPRS", driver_yahoo="PKN.WA+MOL.BD+MOH.AT+ELPE.AT+NESTE.HE+GALP.LS+REP.MC+OMV.VI", driver_desc="AB rafineri sepeti t-1", tv_ticker="GPW:PKN, BET:MOL, ATHEX:MOH, ATHEX:ELPE, OMXHEX:NESTE, EURONEXT:GALP, BME:REP, VIE:OMV", relation="lead_intra", lag=1,
    t_stat=3.93, is_oos="hedge'li gün-içi t IS 3.0 / OOS 2.5", bt_oos_sharpe=-0.68, bt_oos_mean_bps=8.5, n=2788, confidence="DÜŞÜK",
    mechanism="AB kapanışı BIST'ten 0,5-1,5 saat sonra; kalan bilgi ertesi gün-içi", notes="İstatistik var ama brüt 8 bps/işlem: 2 bacak maliyet sonrası negatif (BT1e)")
man(stock="TUPRS", driver_yahoo="BZ=F (saatlik)", driver_desc="Brent: BIST kapanış(15:00 UTC t-1) -> BIST açılış(07:00 UTC t) hareketi", tv_ticker="ICEEUR:BRN1!", relation="lead_gap", lag=1,
    t_stat=5.49, gap_corr=0.57, intra_corr=-0.10, is_oos="sadece 2024-06..2026-10 (saatlik); hedge'li gap corr 0,66; günlük BZ lag1->gap t=3,5 (2014+)", n=559, confidence="ORTA",
    mechanism="Eşzamansız kapanış: gece Brent hareketi açılış gap'inde fiyatlanır", notes="İŞLENEBİLİR DEĞİL (açılışta fiyatlanmış; sonrasında gün-içi devam yok, -0,10). VİOP akşam seansı hariç. HO=F 0,50, CL=F 0,61 benzer")
man(stock="TUPRS", driver_yahoo="BZ=F (saatlik)", driver_desc="Brent seans içi eşzamanlı (07-15 UTC)", tv_ticker="ICEEUR:BRN1!", relation="intraday_minutes", lag=0, intra_corr=0.22, t_stat=4.97,
    is_oos="2024-06+; hedge'li 0,31", n=567, confidence="ORTA", mechanism="Eşzamanlı fiyatlama", notes="Saatlik lead Brent(h-1)->TUPRS(h): brüt 3,3 bps/işlem (t=3,5), |Δ|>%0,5 filtresiyle 6,6 bps -> 8-15 bps maliyetin ALTINDA, işlenemez")
man(stock="TUPRS", driver_yahoo="HO_CRACK (çeyreklik)", driver_desc="Çeyrek ortalaması dizel crack değişimi / Brent", tv_ticker="NYMEX:HO1!*42-ICEEUR:BRN1!", relation="regime", lag=0, corr_full=0.38, pcorr_xu100=0.47,
    is_oos="sonraki çeyreğe öncülük yok (pc 0,02)", n=68, confidence="ORTA", mechanism="Rafineri marjı -> kâr; düşük frekansta görünür", notes="Günlük/haftalık görünmez; 2022 dizel patlamasında haftalık pc -0,12 (Brent 0,43). Q4-2026 ort. HO crack ~93 $/bbl (aşırı rejim)")
man(stock="TUPRS", driver_yahoo="BZ=F şok", driver_desc="|z(Brent t-1)|>2 günlerinde TUPRS gap'ini ters işlem (fade)", tv_ticker="ICEEUR:BRN1!", relation="event", lag=1,
    is_oos="brüt IS -4,3 bps / OOS +55,9 bps (n=85, t=2,5)", bt_oos_sharpe=0.74, bt_oos_mean_bps=47.9, n=210, confidence="DÜŞÜK", mechanism="Açılışta aşırı tepki hipotezi", notes="IS başarısız; filtresiz fade negatif; seçim yanlılığı riski")
man(stock="TUPRS", driver_yahoo="HOxBZ / C321 t-1", driver_desc="Crack değişimi t-1 -> TUPRS gün-içi", tv_ticker="NYMEX:HO1!/ICEEUR:BRN1!", relation="lead_intra", lag=1, t_stat=0.17,
    is_oos="BT2: brüt IS -0,8 / OOS 1,5 bps", bt_oos_sharpe=-0.55, n=3097, confidence="DÜŞÜK", mechanism="Marj haberi", notes="OLUMSUZ bulgu")
# ===== PETKM =====
sync("PETKM", "TUPRS.IS", "ORTA", "Ortak nafta/Brent maruziyeti ve 'enerji/kimya' BIST faktörü", "BIST içi; pc 0,14 (haftalık 0,09)")
sync("PETKM", "BZ=F", "DÜŞÜK", "Nafta maliyeti (STAR'dan boru hattıyla) ~ Brent; ürün fiyatları da petrole bağlı -> net etki belirsiz", "Aylık USD pc 0,06 (IS -0,04/OOS 0,21)")
sync("PETKM", "LYB", "DÜŞÜK", "Küresel petrokimya döngüsü", "OLUMSUZ: XU100 kontrollü ~0; aylık USD petrokimya sepeti pc 0,08")
sync("PETKM", "011170.KS", "DÜŞÜK", "Asya petrokimya (Lotte); BIST açılışından önce kapanır", "lag0 -> PETKM gap t=4,0 ama gün-içi yok; BT4 (Asya sepeti lag0 -> gün-içi) IS -0,59/OOS -0,26 Sharpe brüt", tv="KRX:011170")
sync("PETKM", "1301.TW", "DÜŞÜK", "Formosa Plastics (PVC/PE)", "lag0 -> gap t=5,5; gün-içi yok", tv="TWSE:1301")
man(stock="PETKM", driver_yahoo="BZ=F (saatlik)", driver_desc="Brent gece hareketi -> PETKM gap", tv_ticker="ICEEUR:BRN1!", relation="lead_gap", lag=1, gap_corr=0.42, intra_corr=-0.08, t_stat=3.80,
    is_oos="2024-06+; hedge'li gap 0,61", n=559, confidence="DÜŞÜK", mechanism="Eşzamansız kapanış / enerji faktörü", notes="İşlenemez (açılışta fiyatlanmış)")
# ===== SASA =====
man(stock="SASA", driver_yahoo="HEKTS+KONTR+ASTOR+SMRTG+EUPWR+GESAN+CWENE+YEOTK+ALFAS", driver_desc="BIST bireysel-favori sepeti", tv_ticker="BIST:HEKTS, BIST:KONTR, BIST:ASTOR ...", relation="sync", lag=0,
    pcorr_xu100=0.19, is_oos="pc IS 0,11 / OOS 0,17", n=2500, confidence="ORTA", mechanism="Bireysel yatırımcı akışı/duyarlılık faktörü (SASA yüksek bireysel ağırlıklı)", notes="HEKTS tek başına pc 0,26 (tarama). Sepet kompozisyonu önceden seçildi, n yaklaşık")
sync("SASA", "IVL.BK", "ÇOK DÜŞÜK", "Polyester/PET emsali (Indorama)", "OLUMSUZ: pc ~0; aylık USD polyester sepeti (IVL,ALPEKA,1326.TW,3402.T) pc -0,04", tv="SET:IVL")
sync("SASA", "1326.TW", "ÇOK DÜŞÜK", "Formosa Chemicals & Fibre (PTA/polyester)", "lag0 -> gap t=4,4 (genel Asya açılış etkisi), gün-içi yok", tv="TWSE:1326")
sync("SASA", "BZ=F", "ÇOK DÜŞÜK", "Paraksilen/PTA maliyet vekili", "OLUMSUZ; Çin ZCE PTA kullanılamıyor, test edilmiş alternatif yok")
sync("SASA", "CT=F", "ÇOK DÜŞÜK", "Pamuk: polyester elyaf ikamesi", "OLUMSUZ", tv="ICEUS:CT1!")
# ===== AKSEN =====
man(stock="AKSEN", driver_yahoo="PTF (EPİAŞ)", driver_desc="Türkiye gün öncesi elektrik fiyatı, aylık ortalama değişim (USD)", tv_ticker="TV'de yok (EPİAŞ Şeffaflık Platformu)", relation="sync", lag=0,
    corr_full=0.24, pcorr_xu100=0.26, is_oos="pc IS 0,28 / OOS 0,24; TL bazlı XU100+USDTRY kontrollü 0,24; çeyreklik pc 0,16", n=153, confidence="ORTA",
    mechanism="Gaz/kömür santrali gelirleri spot fiyata bağlı (Türkiye portföyü)", notes="Günlük PTF haberi (t-1'de ilan) ilişkisi YOK (t<1,1); öncülük yok (sonraki ay pc -0,08). Veri: GitHub'daki EPİAŞ dışa aktarımları, 2018 ort. 231,64 TL/MWh ile birebir doğrulandı")
sync("AKSEN", "ZOREN.IS", "YÜKSEK", "BIST elektrik üreticileri sektör faktörü", "BIST içi")
sync("AKSEN", "TTF=F", "DÜŞÜK", "Avrupa gaz fiyatı", "OLUMSUZ: pc ~0, 2021-22 gaz krizinde bile haftalık pc -0,01. PTF~TTF aylık corr 0,13 (çeyreklik 0,43): BOTAŞ düzenlemeli gaz fiyatı bağlantıyı kesiyor")
sync("AKSEN", "RWE.DE", "DÜŞÜK", "Avrupa elektrik şirketleri", "OLUMSUZ: pc 0,03; aylık USD AB utility sepeti pc -0,03")
# ===== ENJSA =====
man(stock="ENJSA", driver_yahoo="PTF (EPİAŞ)", driver_desc="PTF 7g ort. değişimi (t-1 haberi) -> ENJSA gün-içi", tv_ticker="TV'de yok (EPİAŞ)", relation="lead_intra", lag=1, intra_corr=0.04, t_stat=2.44,
    is_oos="BT5 brüt IS ~0 / OOS -3,3 bps", bt_oos_sharpe=-0.58, n=2149, confidence="DÜŞÜK", mechanism="Perakende marj/son kaynak tarifesi", notes="Aylık pc -0,09 (IS -0,46 n=34/OOS -0,01): tutarsız")
sync("ENJSA", "EOAN.DE", "DÜŞÜK", "Avrupa regüle dağıtım emsali", "OLUMSUZ: pc 0,03 (IS 0,09/OOS 0,02). Regüle RAB TÜFE endeksli -> sürücüler yurt içi (enflasyon, WACC kararı) — test edilmedi")
sync("ENJSA", "TTF=F", "ÇOK DÜŞÜK", "Gaz", "OLUMSUZ")
# ===== ODAS =====
sync("ODAS", "ZOREN.IS", "YÜKSEK", "BIST elektrik/küçük-orta ölçekli enerji faktörü", "BIST içi; pc 0,24 (haftalık 0,33)")
sync("ODAS", "AKSEN.IS", "YÜKSEK", "BIST elektrik sektör faktörü", "BIST içi")
sync("ODAS", "GC=F", "DÜŞÜK", "Altın madeni projesi (Anadolu Export/Yıldız-Karaağaç; ~348 bin oz kaynak)", "OLUMSUZ: günlük pc -0,02; aylık USD pc IS +0,17 / OOS -0,22 (işaret döndü); BT6 net negatif. Maden üretim aşamasında değil")
sync("ODAS", "MTF=F", "ÇOK DÜŞÜK", "Kömür (Çan Kömür, yerli linyit)", "OLUMSUZ; MTF=F 2025-12'den beri bayat", tv="ICEEUR:ATW1! ?")
man(stock="ODAS", driver_yahoo="PTF (EPİAŞ)", driver_desc="Aylık ortalama PTF değişimi", tv_ticker="TV'de yok (EPİAŞ)", relation="sync", lag=0, corr_full=0.08, pcorr_xu100=0.07, is_oos="IS 0,11 / OOS 0,07", n=153,
    confidence="DÜŞÜK", mechanism="Kömür santrali gelirleri", notes="Zayıf")
man(stock="ODAS", driver_yahoo="TRY=X", driver_desc="USDTRY (haftalık, XU100 kontrollü beta)", tv_ticker="FX:USDTRY", relation="sync", lag=0, beta=-0.28, t_stat=-3.2, is_oos="aylık -0,19 (t=-0,9)", n=660,
    confidence="DÜŞÜK", mechanism="Döviz borcu hipotezi", notes="FX_FIX sonrası; aylık anlamsız. AKSEN -0,12 (t=-2,0)")
man(stock="ODAS", driver_yahoo="KONTR.IS, GESAN.IS, JANTS.IS t-1", driver_desc="BIST küçük/bireysel enerji hisseleri t-1 -> ODAS hedge'li gün-içi", tv_ticker="BIST:KONTR, BIST:GESAN", relation="lead_intra", lag=1,
    t_stat=4.17, is_oos="KONTR IS t 1,1 / OOS 2,95", n=2000, confidence="DÜŞÜK", mechanism="Bireysel momentum yayılımı", notes="Tarama FDR geçti (H1), IS zayıf")
man(stock="ENJSA", driver_yahoo="SI=F t-1", driver_desc="Gümüş", tv_ticker="COMEX:SI1!", relation="lead_intra", lag=1, t_stat=3.98, is_oos="IS t 0,75 / OOS 3,82", n=2100, confidence="ÇOK DÜŞÜK",
    mechanism="Yok (muhtemel sahte)", notes="Tarama FDR geçti (6.510 test/aile) ama mekanizma yok")
man(stock="ALL6", driver_yahoo="panel taraması", driver_desc="6 hisse x 1.085 sembol x 6 test aileleri = 39.060 test", tv_ticker="-", relation="hypothesis", lag=0, n=39060, confidence="-",
    mechanism="Veri güdümlü", notes="BIST dışı kısmi senkron korelasyonda PETKM/SASA/AKSEN/ENJSA/ODAS için |pc|>0,10 olan tek küresel sembol yok; TUPRS'ta tüm üst sıralar petrol/rafineri (EQNR, CRAK, BZ, BNO...)")
df = pd.DataFrame(rows)[COLS]
for c in ["corr_full", "corr_3y", "corr_1y", "pcorr_xu100", "beta", "t_stat", "gap_corr", "intra_corr"]: df[c] = pd.to_numeric(df[c], errors="coerce").round(3)
df.to_csv(elib.SCR + "/out/f_enerji.csv", index=False)
print(len(df), "satır yazıldı")
