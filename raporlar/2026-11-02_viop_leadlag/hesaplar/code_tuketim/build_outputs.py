"""Bulgular CSV'sini (f_tuketim.csv) a1..a7 çıktılarından üretir. Yıllık işaret oranı burada NaN yıllar hariç yeniden hesaplanır."""
from common import *
A1 = pd.read_csv(CODE + "/a1_curated.csv").drop_duplicates(["stock", "driver_yahoo"])
SC = pd.read_csv(CODE + "/a3_scan.csv")
xu = R("XU100")
# yıllık işaret tutarlılığı (NaN yıllar hariç)
def yrs_same(stock, drv, sgn):
    a = win(R(stock), START); b = R(drv); b = zero_mask(b) if not ll.is_bist(ll.T(drv)) else b
    v = []
    for y in range(2014, 2027):
        aa = a[a.index.year == y]
        if aa.notna().sum() < 100: continue
        pc, n = ll.partial_corr(aa, b, [xu])
        if n >= 100 and not np.isnan(pc): v.append(np.sign(pc) == sgn)
    return (float(np.mean(v)) if v else np.nan), len(v)
TV = {"XU100": "BIST:XU100", "XU030": "BIST:XU030", "TRY=X": "FX:USDTRY", "EURTRY=X": "FX:EURTRY", "^GSPC": "SP:SPX", "ES=F": "CME_MINI:ES1!", "^VIX": "CBOE:VIX",
 "EEM": "AMEX:EEM", "TUR": "NASDAQ:TUR", "^STOXX50E": "TVC:SX5E", "^STOXX": "TVC:SXXP?", "XLP": "AMEX:XLP", "DBA": "AMEX:DBA", "ZW=F": "CBOT:ZW1!", "BZ=F": "ICEEUR:BRN1!",
 "GC=F": "COMEX:GC1!", "DX-Y.NYB": "TVC:DXY", "CC=F": "ICEUS:CC1!", "KE=F": "CBOT:KE1!", "SB=F": "ICEUS:SB1!", "ZL=F": "CBOT:ZL1!", "KC=F": "ICEUS:KC1!", "ZC=F": "CBOT:ZC1!",
 "MDLZ": "NASDAQ:MDLZ", "HSY": "NYSE:HSY", "NESN.SW": "SIX:NESN", "BARN.SW": "SIX:BARN", "LISN.SW": "SIX:LISN", "LISP.SW": "SIX:LISP", "GIS": "NYSE:GIS", "KHC": "NASDAQ:KHC",
 "ULVR.L": "LSE:ULVR", "BN.PA": "EURONEXT:BN", "EGP=X": "FX_IDC:USDEGP", "KZT=X": "FX_IDC:USDKZT", "SAR=X": "FX_IDC:USDSAR", "KO": "NYSE:KO", "PEP": "NASDAQ:PEP",
 "CCEP": "NASDAQ:CCEP", "CCH.L": "LSE:CCH", "KOF": "NYSE:KOF", "BUD": "NYSE:BUD", "ABI.BR": "EURONEXT:ABI", "HEIA.AS": "EURONEXT:HEIA", "CARL-B.CO": "OMXCOP:CARL_B",
 "TAP": "NYSE:TAP", "ALI=F": "COMEX:ALI1!", "HG=F": "COMEX:HG1!", "RUB=X": "FX_IDC:USDRUB", "PKR=X": "FX_IDC:USDPKR", "UZS=X": "FX_IDC:USDUZS?", "GEL=X": "FX_IDC:USDGEL",
 "UAH=X": "FX_IDC:USDUAH", "JMT.LS": "EURONEXT:JMT", "DNP.WA": "GPW:DNP", "CA.PA": "EURONEXT:CA", "AD.AS": "EURONEXT:AD", "TSCO.L": "LSE:TSCO", "SBRY.L": "LSE:SBRY",
 "WMT": "NASDAQ:WMT?", "COST": "NASDAQ:COST", "TGT": "NYSE:TGT", "KR": "NYSE:KR", "DG": "NYSE:DG", "SHP.JO": "JSE:SHP", "PIK.JO": "JSE:PIK", "WALMEX.MX": "BMV:WALMEX",
 "ASAI3.SA": "BMFBOVESPA:ASAI3", "CPALL.BK": "SET:CPALL", "AXFO.ST": "OMXSTO:AXFO", "COLR.BR": "EURONEXT:COLR", "XRT": "AMEX:XRT", "MAD=X": "FX_IDC:USDMAD", "XBANK": "BIST:XBANK",
 "^VVIX": "CBOE:VVIX?", "^OVX": "CBOE:OVX?", "MC.PA": "EURONEXT:MC"}
def tv(d):
    if d in TV: return TV[d]
    if d.endswith(".IS"): return "BIST:" + d[:-3]
    if d in ("BIMAS", "MGROS", "SOKM", "ULKER", "AEFES", "CCOLA"): return "BIST:" + d
    return "?"
DESC = {"CC=F": "Kakao (ICE US)", "KE=F": "KC HRW buğday (arpa/malt proxy)", "ZW=F": "CBOT buğday", "SB=F": "Şeker #11", "ZL=F": "Soya yağı (palm yağı proxy)", "KC=F": "Kahve",
 "ZC=F": "Mısır (tahıl proxy)", "ALI=F": "Alüminyum (COMEX, kutu)", "RUB=X": "USD/RUB", "KZT=X": "USD/KZT", "EGP=X": "USD/EGP", "MAD=X": "USD/MAD", "TRY=X": "USD/TRY",
 "CCOLA": "Coca-Cola İçecek (AEFES ~%50 iştirak, tam konsolide)", "XBANK": "BIST Banka endeksi", "^VIX": "VIX", "TUR": "iShares MSCI Türkiye ETF"}
MECH_OK = {  # mekanizması makul eşleşmeler (hipotez listesi); diğerleri 'şüpheli'
 "ULKER": {"CC=F", "ZW=F", "KE=F", "SB=F", "ZL=F", "KC=F", "ZC=F", "DBA", "MDLZ", "HSY", "NESN.SW", "BARN.SW", "LISN.SW", "LISP.SW", "GIS", "KHC", "ULVR.L", "BN.PA", "EGP=X", "KZT=X", "SAR=X", "TRY=X", "EURTRY=X", "BIMAS", "MGROS", "SOKM", "XLP", "AEFES", "CCOLA"},
 "AEFES": {"CCOLA", "KO", "PEP", "CCEP", "CCH.L", "KOF", "BUD", "ABI.BR", "HEIA.AS", "CARL-B.CO", "TAP", "ALI=F", "HG=F", "RUB=X", "KZT=X", "PKR=X", "UZS=X", "GEL=X", "UAH=X", "ZC=F", "KE=F", "ZW=F", "SB=F", "DBA", "TRY=X", "EURTRY=X", "EEM", "^STOXX50E", "XLP", "BIMAS", "MGROS", "SOKM", "ULKER"},
}
for s in ("BIMAS", "MGROS", "SOKM"):
    MECH_OK[s] = {"JMT.LS", "DNP.WA", "CA.PA", "AD.AS", "TSCO.L", "SBRY.L", "WMT", "COST", "TGT", "KR", "DG", "SHP.JO", "PIK.JO", "WALMEX.MX", "ASAI3.SA", "CPALL.BK", "AXFO.ST", "COLR.BR", "XRT", "EGP=X", "MAD=X", "ZW=F", "SB=F", "DBA", "TRY=X", "EURTRY=X", "XLP", "BIMAS", "MGROS", "SOKM", "ULKER", "AEFES", "CCOLA", "KZT=X"}
rows = []
for r in A1.itertuples():
    s, d = r.stock, r.driver_yahoo
    if d in ("XU100",): continue
    sg = np.sign(r.pcorr_xu100) if not np.isnan(r.pcorr_xu100) else 1
    ys, ny = yrs_same(s, d, sg)
    sc = SC[(SC.stock == s) & (SC.driver == ll.T(d))]
    t_s = float(sc.t_sync.iloc[0]) if len(sc) else r.pcorr_xu100 * np.sqrt(r.n)
    q_s = float(sc.q_sync.iloc[0]) if len(sc) else np.nan
    mech = d in MECH_OK.get(s, set())
    pc, pi, po = r.pcorr_xu100, r.pc_IS, r.pc_OOS
    same = (np.sign(pi) == np.sign(po)) and (np.sign(pi) == np.sign(pc))
    if mech and abs(pc) >= 0.15 and ys >= 0.75 and same and abs(t_s) >= 3 and min(abs(pi), abs(po)) >= 0.05: conf = "YÜKSEK"
    elif mech and abs(t_s) >= 3 and same and ys >= 0.6: conf = "ORTA"
    elif mech and (abs(t_s) >= 2 or (same and ys >= 0.7 and abs(pc) >= 0.03)): conf = "DÜŞÜK"
    elif (not mech) and abs(t_s) >= 3: conf = "DÜŞÜK"
    else: conf = "ÇOK DÜŞÜK"
    notes = f"pc|XU100+TRY={r.pcorr_xu100_try:.3f}; USD-bazlı pc={getattr(r,'pcorr_usd',np.nan):.3f}; yıl-işaret={ys:.2f} ({ny}y); q_FDR(sync)={q_s:.3g}; lag1 gap t={r.gap_t:.2f}, intra t={r.intra_t:.2f}, intra-artık t={r.intra_resid_t:.2f}, drift(t+1..4) t={r.drift_t:.2f}, ters t={r.rev_t:.2f}"
    rows.append({"stock": s, "driver_yahoo": d, "driver_desc": DESC.get(d, d), "tv_ticker": tv(d), "relation": "sync", "lag": 0, "corr_full": r.corr_full, "corr_3y": r.corr_3y,
                 "corr_1y": r.corr_1y, "pcorr_xu100": pc, "beta": r.beta, "t_stat": t_s, "gap_corr": r.gap_corr, "intra_corr": r.intra_corr,
                 "is_oos": f"pcIS={pi:.3f}/pcOOS={po:.3f}", "bt_oos_sharpe": np.nan, "bt_oos_mean_bps": np.nan, "n": r.n, "confidence": conf,
                 "mechanism": "makul" if mech else "şüpheli/yok", "notes": notes})
F = pd.DataFrame(rows)
# --- elle eklenen özel bulgular (a2, a4, a5, a6, a7) ---
B5 = pd.read_csv(CODE + "/a5_backtests.csv")
def bt(name, cost):
    x = B5[(B5.bt == name) & (B5.cost_bps_rt == cost)]
    return (float(x.OOS_sharpe.iloc[0]), float(x.OOS_mean_bps.iloc[0])) if len(x) else (np.nan, np.nan)
M = []
def add(**k):
    base = {c: np.nan for c in F.columns}; base.update(k); M.append(base)
A = lambda **k: add(**k)
A(stock="AEFES", driver_yahoo="CCOLA.IS", driver_desc="CCOLA saatlik senkron (XU100 artık)", tv_ticker="BIST:CCOLA", relation="intraday_minutes", lag=0, corr_full=0.437, pcorr_xu100=0.218, t_stat=11.25, n=5493,
  confidence="YÜKSEK", mechanism="makul (AEFES ~%50 CCI payı, tam konsolidasyon)", notes="60m bar 2023-11+. Artık lag1 (CCOLA_{h-1}->AEFES_h) corr=0.001 t=0.08: saatlik öncülük YOK.")
s_, m_ = bt("B3a CCOLA_{t-1} -> AEFES intra_t", 8)
A(stock="AEFES", driver_yahoo="CCOLA.IS", driver_desc="CCOLA_{t-1} -> AEFES gün-içi (B3a)", tv_ticker="BIST:CCOLA", relation="lead_intra", lag=1, intra_corr=0.032, t_stat=1.50, bt_oos_sharpe=s_, bt_oos_mean_bps=m_,
  is_oos="8bps: IS +2.2bps t0.46 / OOS -5.2bps t-0.76", confidence="ÇOK DÜŞÜK", mechanism="makul (NAV) ama fiyatlanmış", notes="Spread geri dönüşü (B3b) de başarısız: OOS Sharpe -0.27.")
s_, m_ = bt("B1a kakao_{t-1} -> ULKER intra_t (short if cocoa up)", 8)
A(stock="ULKER", driver_yahoo="CC=F", driver_desc="Kakao_{t-1} -> ULKER gün-içi (B1a)", tv_ticker="ICEUS:CC1!", relation="lead_intra", lag=1, intra_corr=-0.021, t_stat=-1.05, bt_oos_sharpe=s_, bt_oos_mean_bps=m_,
  is_oos="IS -11.0bps t-2.4 (net) / OOS -1.9bps", confidence="ÇOK DÜŞÜK", mechanism="makul (girdi maliyeti) ama hedge+fiyat geçişi",
  notes="Aylık lag0-6 anlamsız; yıllık corr(ULKER-XU100, kakao)=+0.20 (YANLIŞ işaret: 2023-24 kakao +150% log iken ULKER-XU100 +41%). Saatlik kakao~ULKER corr=-0.002. Haftalık B1c OOS Sharpe -0.43.")
A(stock="ULKER", driver_yahoo="CC=F", driver_desc="Kakao sıçraması >=+8% (t-1) -> ULKER göreli t..t+4", tv_ticker="ICEUS:CC1!", relation="event", lag=1, t_stat=-3.29, n=18, bt_oos_mean_bps=-179,
  confidence="DÜŞÜK", mechanism="makul", notes="18 olay, çoğu 2023-25 rallisi; >=5% eşiğinde t=-1.33; eşik seçimi = veri madenciliği riski.")
A(stock="ULKER", driver_yahoo="TRY=X", driver_desc="USDTRY aylık -> ULKER göreli (TL değer kaybı ayı)", tv_ticker="FX:USDTRY", relation="regime", lag=0, pcorr_xu100=-0.156, beta=-0.286, t_stat=-2.20, n=154,
  is_oos="IS pc=-0.08 (t-0.3) / OOS pc=-0.228, β_rel=-0.44 (t-3.5)", confidence="DÜŞÜK", mechanism="makul (YP borç / ithal girdi / fiyat geçiş gecikmesi)", notes="Günlük senkronda yok (pc=-0.002). Yalnız 2021+ rejimi -> ORTA adayı.")
A(stock="AEFES", driver_yahoo="TRY=X", driver_desc="USDTRY aylık -> AEFES göreli (yurt dışı gelir hedge)", tv_ticker="FX:USDTRY", relation="regime", lag=0, pcorr_xu100=0.042, beta=0.09, t_stat=0.89, n=154,
  is_oos="IS β_rel=0.30 (t1.6) / OOS -0.07 (t-0.5)", confidence="DÜŞÜK", mechanism="makul (gelirin çoğu yurt dışı)", notes="FX_FIX sonrası hedge etkisi kayboldu (eski hatalı veride pc=0.18 idi).")
A(stock="AEFES", driver_yahoo="RUB=X", driver_desc="USD/RUB (Rusya bira)", tv_ticker="FX_IDC:USDRUB", relation="regime", lag=0, pcorr_xu100=-0.023, t_stat=-1.3,
  is_oos="yıllık pc: 2014 -0.13, 2015 -0.07, 2016+ ~0 (|pc|<0.12, işaret karışık)", confidence="DÜŞÜK", mechanism="tarihsel makul; 1.1.2025'ten beri Rusya bira konsolidasyon dışı (geçici dış yönetim, finansal yatırım)",
  notes="Rusya etkisi bugün kur değil olay/haber kanalında. RUB=X 2022 sonrası sermaye kontrolleri nedeniyle bilgi değeri düşük.")
A(stock="AEFES", driver_yahoo="EVENT", driver_desc="Rusya şokları: 24.02.2022 işgal (CAR t0..t4 -2133bps), 01.03.2022 (-1178), 17.10.2023 geçici yönetim kararnamesi (t0..t2 -560)", tv_ticker="BIST:AEFES", relation="event",
  confidence="ORTA", mechanism="makul (Rusya bira varlıkları)", notes="Günlük göreli sd ~195bps; tekil olaylar. 26.12.2023 devir anlaşması +178, Eki-2024 yeniden yapılandırma +483 (t0..t4). Bazı tarihler yaklaşık.")
A(stock="AEFES", driver_yahoo="CARL-B.CO|HEIA.AS|ABI.BR|CCH.L|BUD", driver_desc="Küresel bira/şişeleme emsalleri (Avrupa/ABD endeksi kontrollü)", tv_ticker="OMXCOP:CARL_B / EURONEXT:HEIA / EURONEXT:ABI / LSE:CCH / NYSE:BUD",
  relation="sync", lag=0, pcorr_xu100=0.09, is_oos="pc|XU100+STOXX IS/OOS: CARL .090/.091, HEIA .050/.101, ABI .069/.096, CCH .105/.092, BUD .064/.087", confidence="ORTA", mechanism="makul (sektör faktörü)",
  notes="Plasebo: aynı emsallerin ULKER/BIMAS/MGROS/SOKM ile pc ~0 (|pc|<0.04) -> AEFES'e özgü. Büyüklük <0.15 -> YÜKSEK değil.")
A(stock="AEFES", driver_yahoo="GLOBAL", driver_desc="Küresel/EM hisse faktörü: FDR'den geçen 37 yabancı senkron sürücünün 34'ü pozitif", tv_ticker="AMEX:EEM / TVC:SX5E", relation="sync", lag=0, pcorr_xu100=0.044,
  confidence="ORTA", mechanism="makul (yurt dışı gelir payı yüksek)", notes="Diğer hisselerde FDR geçen yabancı sürücü: BIMAS 9, MGROS 3, SOKM 2, ULKER 5 (mekanizmasız, |pc|<0.09).")
for s, pc, pi, po, yn in [("BIMAS", -0.164, -0.300, -0.070, 0.92), ("SOKM", -0.125, -0.187, -0.096, 1.0), ("MGROS", -0.084, -0.025, -0.128, 0.85), ("ULKER", -0.093, -0.147, -0.054, 0.85), ("AEFES", -0.041, -0.174, 0.038, 0.85)]:
    A(stock=s, driver_yahoo="XBANK.IS", driver_desc="BIST Banka endeksi (XU100 kontrollü) - defansif/banka rotasyonu", tv_ticker="BIST:XBANK", relation="sync", lag=0, pcorr_xu100=pc,
      is_oos=f"IS {pi:.3f} / OOS {po:.3f}; yılların {yn:.0%}'inde negatif", confidence="ORTA" if s in ("BIMAS", "SOKM", "ULKER") else "DÜŞÜK",
      mechanism="makul (faiz/risk iştahı rotasyonu) + kısmen endeks bileşimi mekaniği", notes="Dış sürücü değil, BIST-içi faktör.")
A(stock="ALL5", driver_yahoo="XU100.IS", driver_desc="Kuyruk betası: XU100<=-2% günlerinde beta 0.88-1.08 (tam dönem 0.70-0.88); MGROS/SOKM/ULKER/CCOLA aşağı beta > yukarı beta", tv_ticker="BIST:XU100", relation="regime", lag=0,
  is_oos="aşağı-yukarı fark t: MGROS -2.6, SOKM -2.0, ULKER -3.5, CCOLA -2.1; BIMAS +1.4 (yukarı 0.75/aşağı 0.65)", confidence="ORTA", mechanism="defansiflik kuyrukta kayboluyor (likidite satışı)",
  notes="Simetrik temizlik (taban günleri dahil) ile. Eski asimetrik temizlik defansifliği abartıyordu.")
A(stock="ALL5", driver_yahoo="XU100.IS", driver_desc="BIST sert düşüş günü (XU100<=-3%, n=88): ham göreli +21..+145bps, beta-düzeltmeli ~0 veya negatif", tv_ticker="BIST:XU100", relation="event", lag=0, n=88,
  is_oos="β-adj: BIMAS +6.5, SOKM +9.3, MGROS -33, ULKER -55 (t-1.8), AEFES -41, CCOLA -42; sonraki 5g göreli: AEFES -115 (t-1.9), ULKER -113 (t-1.7)", confidence="ORTA",
  mechanism="defansiflik = düşük beta, koşullu alfa yok", notes="B2c (sonraki 5g defansif short) IS -79bps / OOS +92bps: işaret değişiyor -> başarısız.")
A(stock="BIMAS|MGROS|ULKER", driver_yahoo="^STOXX50E", driver_desc="Senkron Avrupa risk-off (SX5E<=-2%, n=118) günü beta-düzeltmeli göreli", tv_ticker="TVC:SX5E", relation="event", lag=0, n=118,
  is_oos="BIMAS +45.5 (IS +69 t2.8 / OOS -0.6); MGROS +36.8 (IS +27.5 / OOS +54.9 t2.0); ULKER +38.5 (IS +20.5 / OOS +73.7 t1.5)", confidence="DÜŞÜK", mechanism="makul (küresel risk-off'ta yerel tüketim)",
  notes="Senkron -> işlenemez. AEFES/CCOLA bu günlerde defansif DEĞİL (β-adj -22/-22bps).")
A(stock="BIMAS|MGROS", driver_yahoo="TRY=X", driver_desc="TL şok günü (USDTRY>=+1.5% aynı gün, n=140) beta-düzeltmeli göreli", tv_ticker="FX:USDTRY", relation="event", lag=0, n=140,
  is_oos="BIMAS +30bps (IS +32 t1.6 / OOS +27 t1.0); MGROS -38bps (IS -52 t-3.1 / OOS -8)", confidence="DÜŞÜK", mechanism="BIMAS fiyatlama gücü/enflasyon hedge; MGROS ithal ürün/kur borcu (tarihsel)",
  notes="MGROS etkisi IS'de (YP borçlu dönem), OOS'ta yok.")
s_, m_ = bt("B2a ABD risk-off_{t-1} -> defansif-XU030 intra_t", 8)
A(stock="BIMAS|MGROS|SOKM|ULKER", driver_yahoo="^GSPC|^VIX", driver_desc="ABD risk-off (SPX_{t-1}<=-1.5% veya VIX_{t-1}>=+15%) -> defansif sepet long / XU030 short (B2a)", tv_ticker="SP:SPX / CBOE:VIX",
  relation="lead_intra", lag=1, bt_oos_sharpe=s_, bt_oos_mean_bps=m_, is_oos="IS -16.9bps (t-1.6) / OOS -3.6bps; t..t+4 versiyonu OOS -34.6bps", n=237, confidence="ÇOK DÜŞÜK", mechanism="makul ama gap'te fiyatlanıyor",
  notes="Çift bacak 16bps. Koşulsuz referans (her gün) brüt ~+2/-2bps.")
A(stock="ALL5", driver_yahoo="^VIX", driver_desc="VIX_{t-1} -> açılış gap'i (eşzamansız kapanış)", tv_ticker="CBOE:VIX", relation="lead_gap", lag=1, gap_corr=-0.11, t_stat=-5.2,
  confidence="ORTA", mechanism="eşzamansız kapanış (piyasa geneli)", notes="İŞLENEMEZ. BIMAS -0.116 (t-5.2), MGROS -0.095, AEFES -0.113; gün-içine taşmıyor (|intra t|<1.8).")
A(stock="MGROS|ULKER|BIMAS", driver_yahoo="TRY=X", driver_desc="USDTRY_{t-1} (UTC günü, BIST kapanışı sonrası saatler dahil) -> açılış gap'i", tv_ticker="FX:USDTRY", relation="lead_gap", lag=1, gap_corr=-0.155, t_stat=-4.3,
  confidence="ORTA", mechanism="akşam saatlerindeki TL hareketi açılışta fiyatlanır (piyasa geneli)", notes="MGROS -0.155 (t-4.3), ULKER -0.088 (t-3.5), BIMAS -0.072 (t-2.9). İŞLENEMEZ; gün-içine taşma yok.")
A(stock="ALL5", driver_yahoo="SCAN", driver_desc="Veri güdümlü tarama: 5 hisse x ~1.120 sürücü x 4 aile = 22.480 test; lag1->gün-içi FDR(aile) 0/5620, gün-içi artık 0/5620", tv_ticker="-", relation="lead_intra", lag=1,
  confidence="ÇOK DÜŞÜK", mechanism="yok", notes="En yüksek |t| (3.6-4.0, q=0.23): Çin A-hisseleri (000921.SZ, 600690.SS -> AEFES; Çin borsası, TV'de açılmaz), 0001.HK->BIMAS, COALINDIA.NS->ULKER: mekanizmasız sahte pozitif. Havuzlanmış FDR'de 13 'geçiş' havuzlama artefaktı.")
A(stock="ALL5", driver_yahoo="TRY=X", driver_desc="Ters yön (BIST_{t-1}->USDTRY_t) - FX_FIX sonrası", tv_ticker="FX:USDTRY", relation="reverse", lag=-1, t_stat=0.48,
  confidence="ÇOK DÜŞÜK", mechanism="yok", notes="Düzeltme öncesi XU100_{t-1}->TRY_t corr=-0.17 (t-6) idi; FX_FIX ile 0.013'e indi -> eski bulgu zaman damgası artefaktıydı.")
A(stock="ALL5", driver_yahoo="CPI_DAY", driver_desc="TÜFE açıklama günü (ayın 3'ü / sonraki iş günü) göreli getiri", tv_ticker="ECONOMICS:TRIRYY?", relation="event", lag=0, n=154,
  is_oos="AEFES +41bps t=2.2 (varyans oranı 1.34, p=0.08); diğerleri |t|<1.3", confidence="ÇOK DÜŞÜK", mechanism="beklenti/sürpriz verisi yok", notes="7 test; çoklu test sonrası anlamsız.")
A(stock="BIMAS", driver_yahoo="EGP=X", driver_desc="Mısır devalüasyon günleri (2016-11, 2022-03, 2022-10, 2023-01, 2024-03)", tv_ticker="FX_IDC:USDEGP", relation="event", lag=0, n=5,
  is_oos="CAR t0..t4: +556,+275,+51,+464,+462 bps", confidence="DÜŞÜK", mechanism="şüpheli (Mısır ~%1 ciro; beklenen işaret negatif)", notes="5/5 pozitif ama n=5, mekanizma ters; günlük EGP=X pc=0.018.")
A(stock="ULKER", driver_yahoo="FCPO (Yahoo'da yok)", driver_desc="Palm yağı (Bursa Malezya)", tv_ticker="MYX:FCPO1!?", relation="hypothesis", confidence="ÇOK DÜŞÜK", mechanism="makul (yağ girdisi)",
  notes="Proxy ZL=F soya yağı pc=0.01 (anlamsız). DCE palm olein Çin borsası -> KULLANMA.")
A(stock="ULKER", driver_yahoo="FINDIK (yok)", driver_desc="Fındık fiyatı", tv_ticker="?", relation="hypothesis", confidence="ÇOK DÜŞÜK", mechanism="makul (çikolata/gofret girdisi)", notes="Piyasa verisi yok; test edilemedi.")
A(stock="AEFES", driver_yahoo="ARPA (yok)", driver_desc="Arpa/malt", tv_ticker="CBOT:KE1! (proxy) / EURONEXT:EBM1!? (Paris buğday)", relation="hypothesis", confidence="DÜŞÜK", mechanism="makul (malt maliyeti)",
  notes="Proxy KE=F pc=-0.063 (IS -0.068 / OOS -0.053), ZC=F -0.042: beklenen negatif işaret, küçük büyüklük.")
A(stock="BIMAS|MGROS|SOKM", driver_yahoo="ASGARI_UCRET/REKABET", driver_desc="Asgari ücret, Rekabet Kurumu, fiyat regülasyonu olayları", tv_ticker="-", relation="hypothesis", confidence="ÇOK DÜŞÜK", mechanism="makul", notes="Olay veri seti kurulmadı.")
CM = pd.read_csv(CODE + "/a4_cocoa_monthly.csv"); x = CM[CM.driver == "cc"]; print("kakao aylık lag0-6 max|t|:", round(x.t.abs().max(), 2))
F = pd.concat([F, pd.DataFrame(M)], ignore_index=True)
F.to_csv(OUT + "/f_tuketim.csv", index=False)
print(F.shape); print(F.confidence.value_counts().to_dict())
print(F[F.relation == "sync"].groupby(["stock", "confidence"]).size().unstack(fill_value=0))
print(F[(F.relation == "sync") & F.confidence.isin(["YÜKSEK", "ORTA"])][["stock", "driver_yahoo", "pcorr_xu100", "t_stat", "is_oos", "confidence"]].round(3).to_string(index=False))
