"""f_kimya.csv üretici: res_hyp/res_lowfreq (senkron), backtest/olay/saatlik sonuçları + elle eklenen satırlar."""
import sys, os, numpy as np, pandas as pd
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/code"); import ll
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
TV = {"CF": "NYSE:CF", "NTR": "NYSE:NTR", "MOS": "NYSE:MOS", "YAR.OL": "OSL:YAR", "ICL": "NYSE:ICL", "IPI": "NYSE:IPI", "LXU": "NYSE:LXU", "OCI.AS": "EURONEXT:OCI",
      "SQM": "NYSE:SQM", "UAN": "NYSE:UAN", "CVR": "AMEX:CVR?", "2020.SR": "TADAWUL:2020", "ABUK.CA": "EGX:ABUK", "MFPC.CA": "EGX:MFPC", "ATT.WA": "GPW:ATT", "SDF.DE": "XETR:SDF",
      "TTF=F": "ICEENDEX:TFM1!?", "NG=F": "NYMEX:NG1!", "ZW=F": "CBOT:ZW1!", "ZC=F": "CBOT:ZC1!", "ZS=F": "CBOT:ZS1!", "KE=F": "CBOT:KE1!", "DBA": "AMEX:DBA", "MOO": "AMEX:MOO",
      "CTVA": "NYSE:CTVA", "FMC": "NYSE:FMC", "BAYN.DE": "XETR:BAYN", "UPL.NS": "NSE:UPL", "NUF.AX": "ASX:NUF", "SUMICHEM.NS": "NSE:SUMICHEM", "KWS.DE": "XETR:KWS",
      "FLR": "NYSE:FLR", "KBR": "NYSE:KBR", "J": "NYSE:J", "ACS.MC": "BME:ACS", "FER.MC": "BME:FER?", "HOT.DE": "XETR:HOT", "SKA-B.ST": "OMXSTO:SKA_B",
      "SGO.PA": "EURONEXT:SGO", "OI": "NYSE:OI", "VID.MC": "BME:VID", "VRLA.PA": "EURONEXT:VRLA", "5201.T": "TSE:5201", "GLW": "NYSE:GLW", "AMBP": "NYSE:AMBP",
      "SOLB.BR": "EURONEXT:SOLB", "SYENS.BR": "EURONEXT:SYENS", "GEL": "NYSE:GEL", "NRP": "NYSE:NRP", "TATACHEM.NS": "NSE:TATACHEM",
      "HEI.DE": "XETR:HEI", "HOLN.SW": "SIX:HOLN", "CX": "NYSE:CX", "BZU.MI": "MIL:BZU", "TITC.BR": "EURONEXT:TITC", "TITC.AT": "ATHEX:TITC", "CRH": "NYSE:CRH", "VMC": "NYSE:VMC",
      "MLM": "NYSE:MLM", "EXP": "NYSE:EXP", "1101.TW": "TWSE:1101", "MTF=F": "ICEEUR:ATW1!?", "BTU": "NYSE:BTU", "BZ=F": "ICEEUR:BRN1!", "CL=F": "NYMEX:CL1!",
      "XLB": "AMEX:XLB", "XHB": "AMEX:XHB", "ITB": "AMEX:ITB", "TRY=X": "FX:USDTRY", "EURTRY=X": "FX:EURTRY", "EURUSD=X": "FX:EURUSD", "^STOXX": "TVC:SXXP?", "^GDAXI": "XETR:DAX",
      "^GSPC": "SP:SPX", "ACWI": "NASDAQ:ACWI", "GC=F": "COMEX:GC1!", "^VIX": "CBOE:VIX", "^OVX": "CBOE:OVX?", "BTC-USD": "BITSTAMP:BTCUSD", "KZT=X": "FX_IDC:USDKZT?", "AZN=X": "FX_IDC:USDAZN?",
      "ES=F": "CME_MINI:ES1!", "TKGBY": "OTC:TKGBY", "AKBTY": "OTC:AKBTY", "TAN": "AMEX:TAN", "ICLN": "NASDAQ:ICLN", "ENPH": "NASDAQ:ENPH", "STR.VI": "VIE:STR", "KRBN": "AMEX:KRBN",
      "011170.KS": "KRX:011170", "^KS11": "KRX:KOSPI?", "005380.KS": "KRX:005380", "XBANK.IS": "BIST:XBANK", "XU100.IS": "BIST:XU100"}


def tv(s): return TV.get(s, "BIST:" + s[:-3] if s.endswith(".IS") else "?")


DESC = {"BAGFS.IS": "Bagfaş (BIST gübre)", "EGGUB.IS": "Ege Gübre (BIST gübre)", "HEKTS.IS": "Hektaş", "GUBRF.IS": "Gübretaş", "TKFEN.IS": "Tekfen", "OYAKC.IS": "Oyak Çimento",
        "CIMSA.IS": "Çimsa", "AKCNS.IS": "Akçansa (BIST çimento)", "NUHCM.IS": "Nuh Çimento", "AFYON.IS": "Afyon Çimento", "BUCIM.IS": "Bursa Çimento", "KONYA.IS": "Konya Çimento",
        "BTCIM.IS": "Batıçim", "EKGYO.IS": "Emlak Konut (inşaat/konut vekili)", "ENKAI.IS": "Enka İnşaat (BIST taahhüt)", "XBANK.IS": "BIST Banka endeksi", "ISCTR.IS": "İş Bankası (SISE ana ortağı)",
        "TTF=F": "Hollanda TTF doğalgaz", "NG=F": "Henry Hub doğalgaz", "TRY=X": "USDTRY", "EURTRY=X": "EURTRY", "EURUSD=X": "EURUSD", "MTF=F": "Rotterdam kömür (bayat seri)"}


def conf_sync(r, mech=True):
    pcf, pis, poos, yrs = r.pc_full, r.pc_IS, r.pc_OOS, r.yrs_same_sign
    same = np.sign(pis) == np.sign(poos) if pd.notna(pis) and pd.notna(poos) else False
    if mech and abs(pcf) >= 0.15 and yrs >= 0.75 and same and abs(poos) >= 0.10 and r.fdr: return "YÜKSEK"
    if mech and abs(pcf) >= 0.08 and same and r.fdr: return "ORTA"
    if abs(pcf) >= 0.04 or abs(r.corr_full) >= 0.10: return "DÜŞÜK"
    return "ÇOK DÜŞÜK"


H = pd.read_csv(os.path.join(HERE, "res_hyp.csv")); L = pd.read_csv(os.path.join(HERE, "res_lowfreq.csv"))
M = H.merge(L, on=["stock", "driver"], how="left")
rej, padj = ll.fdr(ll.t_to_p(M.t_sync.values), 0.05); M["fdr"] = rej
NTEST = int(M.t_sync.notna().sum())
rows = []
for _, r in M.iterrows():
    dom = r.driver.endswith(".IS")
    mech = True
    c = conf_sync(r, mech)
    if r.driver in ("TRY=X", "EURTRY=X", "EURUSD=X") and c in ("YÜKSEK", "ORTA"): c = "ORTA"
    note = (f"pc_ext(XU100+USDTRY+ACWI l0/l1)={r.pc_ext:+.2f}; haftalık pc={r.pc_w:+.2f} (t{r.t_w:+.1f}); aylık pc={r.pc_m:+.2f}; USD-bazlı aylık pc={r.pc_m_usd:+.2f}; "
            f"lag1 cc t={r.cc_l1_t:+.1f}; drift t+2..5 t={r.drift_2_5_t:+.1f}; ters(hisse_t-1->sürücü_t) c={r.rev_l1:+.3f} t={r.rev_l1_t:+.1f}; yıl-işaret={r.yrs_same_sign:.2f}; FDR({NTEST} test)={'geçti' if r.fdr else 'geçmedi'}")
    rows.append(dict(stock=r.stock, driver_yahoo=r.driver, driver_desc=DESC.get(r.driver, r.driver), tv_ticker=tv(r.driver), relation="sync", lag=0,
                     corr_full=r.corr_full, corr_3y=r.corr_3y, corr_1y=r.corr_1y, pcorr_xu100=r.pc_full, beta=r.beta, t_stat=r.t_sync, gap_corr=r.gap_l1,
                     intra_corr=r.intra_l1, is_oos=f"pc IS {r.pc_IS:+.2f} / OOS {r.pc_OOS:+.2f}; lag1->intra IS {r.intra_l1_IS:+.3f} / OOS {r.intra_l1_OOS:+.3f} (t{r.intra_l1_t:+.1f})",
                     bt_oos_sharpe=np.nan, bt_oos_mean_bps=np.nan, n=r.n, confidence=c,
                     mechanism=("yurt içi sektör/tema kümesi (aynı BIST yatırımcı akımı)" if dom else "küresel emsal/emtia maruziyeti (hipotez)"), notes=note))
F = pd.DataFrame(rows)

# backtest / olay / saatlik / tarama satırları
B = pd.read_csv(os.path.join(HERE, "res_bt.csv")); S = pd.read_csv(os.path.join(HERE, "res_selfbt.csv")); I = pd.read_csv(os.path.join(HERE, "res_intraday.csv"))


def btrow(df, spec, costcol="cost_bps"):
    x = df[(df.spec == spec) & (df[costcol] == 10)].iloc[0]; g = df[(df.spec == spec) & (df[costcol] == 0)].iloc[0]; h = df[(df.spec == spec) & (df[costcol] == 15)].iloc[0]
    return x, f"10bps: IS {x.mean_bps_IS:+.1f}bps (t{x.t_IS:+.1f}, n{int(x.n_IS)}) / OOS {x.mean_bps_OOS:+.1f}bps (t{x.t_OOS:+.1f}, n{int(x.n_OOS)}); brüt OOS {g.mean_bps_OOS:+.1f}; 15bps OOS {h.mean_bps_OOS:+.1f}"


EX = [  # (stock, driver, desc, relation, lag, df, spec, conf, mech, note)
    ("GUBRF", "CF+MOS+NTR+IPI+LXU+UAN", "ABD gübre hisse sepeti (vol-ölçekli)", "lead_intra", 1, B, "BT1 ABD gübre sepeti_t-1 -> GUBRF intra_t", "ÇOK DÜŞÜK", "ABD seansı -> ertesi gün BIST gün-içi", "BT1 başarısız: maliyet sonrası ~0/negatif"),
    ("GUBRF", "CF+MOS+NTR+IPI+LXU+UAN", "ABD gübre sepeti |z|>1", "lead_intra", 1, B, "BT1z ABD gübre sepeti_t-1 |z|>1 -> GUBRF intra_t", "ÇOK DÜŞÜK", "büyük ABD gübre şoku -> GUBRF gün-içi", "t<1; istatistik yok"),
    ("TKFEN", "CF+MOS+NTR+IPI+LXU+UAN", "ABD gübre sepeti", "lead_intra", 1, B, "BT1 ABD gübre sepeti_t-1 -> TKFEN intra_t", "ÇOK DÜŞÜK", "Toros Tarım gübre bacağı", "OOS negatif (t-2.3): gap'te fiyatlanıp gün-içi geri dönüş"),
    ("SISE", "TTF=F", "TTF şoku (ters pozisyon)", "lead_intra", 1, B, "BT2 TTF şoku_t-1 |z|>1 (ters) -> SISE intra_t", "ÇOK DÜŞÜK", "enerji maliyeti şoku (cam fırınları)", "BT2 başarısız; TTF yükselişi SISE'ye özgü değil, TR makro faktörü"),
    ("SISE", "TTF=F", "TTF şoku t -> t+2..t+5", "lead_multiday", 1, B, "BT2d TTF şoku_t |z|>1.5 (ters) -> SISE t+2..t+5", "ÇOK DÜŞÜK", "yavaş fiyatlama", "örtüşen 4g tutuş; anlamsız"),
    ("SISE", "SGO.PA+OI+VID.MC", "cam emsal sepeti", "lead_intra", 1, B, "BT2c cam sepeti_t-1 -> SISE intra_t", "ÇOK DÜŞÜK", "cam emsalleri", "brüt ~0"),
    ("CIMSA", "HEI.DE+HOLN.SW+BZU.MI", "AB çimento sepeti", "lead_intra", 1, B, "BT3 AB çimento sepeti_t-1 -> CIMSA intra_t", "DÜŞÜK", "AB emsal bilgisi gap'te AŞIRI fiyatlanıp gün-içi tersine dönüyor", "İŞARET NEGATİF: brüt OOS -10bps (t-2.7); takip değil ters; IS zayıf (t-1.5)"),
    ("OYAKC", "HEI.DE+HOLN.SW+BZU.MI", "AB çimento sepeti", "lead_intra", 1, B, "BT3 AB çimento sepeti_t-1 -> OYAKC intra_t", "ÇOK DÜŞÜK", "AB emsal", "anlamsız"),
    ("CIMSA", "AKCNS+NUHCM+AFYON+BUCIM+KONYA+BTCIM", "TR küçük çimento sepeti (XU100 artığı)", "lead_multiday", 1, B, "BT4 TR küçük çimento sepeti_t-1 (XU100 artığı) -> CIMSA cc_t", "ÇOK DÜŞÜK", "yurt içi küme içi yayılım", "senkron güçlü ama öncülük yok"),
    ("GUBRF", "BAGFS.IS+EGGUB.IS", "BIST gübre kümesi (XU100 artığı)", "lead_multiday", 1, B, "BT5 BAGFS+EGGUB_t-1 -> GUBRF cc_t", "ÇOK DÜŞÜK", "küme içi yayılım", "öncülük yok (hafif ters)"),
    ("CIMSA", "(kendi açılış gap'i |gap|>%1)", "gap-fade: -sign(gap_t) -> intra_t", "lead_intra", 0, S, "gap-fade |gap|>1% CIMSA", "ORTA", "büyük açılış boşluğu (çoğu küresel/AB kaynaklı) gün-içinde kısmen geri dönüyor", "sürücü değil mikro-yapı; açılış fiyatıyla dolum iyimser; 13 yılın 11'i +"),
    ("OYAKC", "(kendi açılış gap'i |gap|>%1)", "gap-fade: -sign(gap_t) -> intra_t", "lead_intra", 0, S, "gap-fade |gap|>1% OYAKC", "ORTA", "aynı", "13 yılın 12'si +; açılış dolumu iyimser"),
    ("GUBRF", "(kendi açılış gap'i |gap|>%1)", "gap-fade", "lead_intra", 0, S, "gap-fade |gap|>1% GUBRF", "DÜŞÜK", "aynı", "IS negatif, OOS pozitif -> istikrarsız"),
    ("HEKTS", "(kendi cc_t-1)", "momentum cc_t-1 -> cc_t", "lead_multiday", 1, S, "momentum cc_t-1 -> cc_t HEKTS", "DÜŞÜK", "bireysel yatırımcı ağırlığı -> pozitif otokorelasyon (ac1 OOS ~0.10)", "kapanış seansında gir varsayımı; t1.4"),
]
for st, dr, de, rel, lag, df, spec, cf, mech, note in EX:
    x, txt = btrow(df, spec, "cost_bps" if "cost_bps" in df else "cost")
    F.loc[len(F)] = dict(stock=st, driver_yahoo=dr, driver_desc=de, tv_ticker=("; ".join(tv(s) for s in dr.split("+")) if "+" in dr and "(" not in dr else (tv(dr) if "(" not in dr else "BIST:" + st)),
                         relation=rel, lag=lag, corr_full=np.nan, corr_3y=np.nan, corr_1y=np.nan, pcorr_xu100=np.nan, beta=np.nan, t_stat=x.t_OOS, gap_corr=np.nan, intra_corr=np.nan,
                         is_oos=txt, bt_oos_sharpe=x.sharpe_OOS, bt_oos_mean_bps=x.mean_bps_OOS, n=x.n_OOS, confidence=cf, mechanism=mech, notes=note + " | IS 2014-2020, OOS 2021-2026")
# saatlik kesin hizalama satırları
for _, r in I[I.c_sync_snap.notna()].iterrows():
    if r.stock == "XU100": continue
    cf = "DÜŞÜK" if abs(r.pc_sync_snap) >= 0.05 or abs(r.t_after_intra1) >= 3 else "ÇOK DÜŞÜK"
    F.loc[len(F)] = dict(stock=r.stock, driver_yahoo=r.driver, driver_desc=DESC.get(r.driver, r.driver) + " (15:00 UTC snap)", tv_ticker=tv(r.driver), relation="intraday_minutes", lag=0,
                         corr_full=r.c_sync_snap, corr_3y=r.c_sync_snap, corr_1y=np.nan, pcorr_xu100=r.pc_sync_snap, beta=np.nan, t_stat=r.t_sync_snap, gap_corr=r.c_after_gap1, intra_corr=r.c_after_intra1,
                         is_oos="yalnız 2023-11/2024-06 sonrası (OOS içi)", bt_oos_sharpe=np.nan, bt_oos_mean_bps=np.nan, n=r.n, confidence=cf,
                         mechanism="BIST kapanışına hizalı gerçek senkron; gap/intra = sürücünün 15:00 UTC sonrası parçası -> t+1",
                         notes=f"standart günlük lag0 c={r.c_sync_daily:+.3f}; kapanış-sonrası->intra t={r.t_after_intra1:+.1f}")
F.loc[len(F)] = dict(stock="CIMSA", driver_yahoo="(olay) 6 Şubat 2023 depremi", driver_desc="deprem sonrası yeniden yapım rejimi", tv_ticker="BIST:CIMSA", relation="event", lag=0,
                     corr_full=np.nan, corr_3y=np.nan, corr_1y=np.nan, pcorr_xu100=np.nan, beta=np.nan, t_stat=7.9, gap_corr=np.nan, intra_corr=np.nan,
                     is_oos="tek olay", bt_oos_sharpe=np.nan, bt_oos_mean_bps=np.nan, n=1, confidence="YÜKSEK",
                     mechanism="talep şoku: çimento sektörü tavan serisi", notes="CAR(0,0)=+10.3% z4.2; CAR(0,5)=+46.6% z7.9; CAR(0,20)=+15.6%; CAR(0,60)=-9.7% (geri verdi). Küme pc (TR çimento) 0.45->0.70 deprem sonrası, 2024+ 0.39. Tekrarlanamaz")
F.loc[len(F)] = dict(stock="OYAKC", driver_yahoo="(olay) 6 Şubat 2023 depremi", driver_desc="deprem sonrası yeniden yapım rejimi", tv_ticker="BIST:OYAKC", relation="event", lag=0,
                     corr_full=np.nan, corr_3y=np.nan, corr_1y=np.nan, pcorr_xu100=np.nan, beta=np.nan, t_stat=8.3, gap_corr=np.nan, intra_corr=np.nan,
                     is_oos="tek olay", bt_oos_sharpe=np.nan, bt_oos_mean_bps=np.nan, n=1, confidence="YÜKSEK",
                     mechanism="talep şoku (bölgeye yakın fabrikalar)", notes="CAR(0,0)=+10.6% z4.0; CAR(0,5)=+54.4% z8.3; CAR(0,20)=+68.6% z5.6; CAR(0,60)=+40.6% z2.0; XU100 betası 0.84->1.09")
F.loc[len(F)] = dict(stock="GUBRF", driver_yahoo="(olay) İran/İsrail savaş ve Razi haberleri (9 olay)", driver_desc="Razi (%48,88) jeopolitik riski", tv_ticker="BIST:GUBRF", relation="event", lag=0,
                     corr_full=np.nan, corr_3y=np.nan, corr_1y=np.nan, pcorr_xu100=np.nan, beta=np.nan, t_stat=np.nan, gap_corr=np.nan, intra_corr=np.nan, is_oos="olay",
                     bt_oos_sharpe=np.nan, bt_oos_mean_bps=np.nan, n=9, confidence="ÇOK DÜŞÜK", mechanism="Razi faaliyet kârının büyük kısmı (bir kaynağa göre ~%85) İran'da",
                     notes="Hiçbir olayda |z|>2 yok: Haz-2025 savaşı CAR(0,10)=-8.9% z-1.1; Razi ihalesi iptali (28.11.2025) CAR(0,2)=-6.5% z-1.8; Ara-2022 dava CAR(0,10)=+11.3%. İran borsası Yahoo'da yok -> doğrudan test yapılamadı")
F.loc[len(F)] = dict(stock="GUBRF", driver_yahoo="(Yahoo'da yok) Üre / DAP vadelileri", driver_desc="CME Üre (Granular) FOB US Gulf / Orta Doğu, DAP NOLA", tv_ticker="?", relation="hypothesis", lag=0,
                     corr_full=np.nan, corr_3y=np.nan, corr_1y=np.nan, pcorr_xu100=np.nan, beta=np.nan, t_stat=np.nan, gap_corr=np.nan, intra_corr=np.nan, is_oos="yapılmadı",
                     bt_oos_sharpe=np.nan, bt_oos_mean_bps=np.nan, n=0, confidence="ÇOK DÜŞÜK", mechanism="Razi geliri = üre/amonyak fiyatı (İran gazı yerel/ucuz)",
                     notes="Vekil UAN (CVR Partners), CF, NTR, 2020.SR (SABIC Agri), ABUK.CA test edildi: hiçbiri XU100 kontrollü anlamlı değil. Üre vadelisi TV kodu doğrulanmadı")
F.loc[len(F)] = dict(stock="SISE", driver_yahoo="(Çin) ZCE soda külü vadelisi", driver_desc="Çin soda külü - kullanıcıda AÇILMIYOR", tv_ticker="(Çin borsası verilmez) alternatif: NSE:TATACHEM, EURONEXT:SOLB, NYSE:GEL", relation="hypothesis", lag=0,
                     corr_full=np.nan, corr_3y=np.nan, corr_1y=np.nan, pcorr_xu100=np.nan, beta=np.nan, t_stat=np.nan, gap_corr=np.nan, intra_corr=np.nan, is_oos="yapılmadı",
                     bt_oos_sharpe=np.nan, bt_oos_mean_bps=np.nan, n=0, confidence="ÇOK DÜŞÜK", mechanism="soda külü fiyatı -> Şişecam kimyasallar (Wyoming %51, Pacific Soda %100)",
                     notes="Alternatifler test edildi: TATACHEM pc=+0.06 (yıl 0.77, FDR geçti) DÜŞÜK; SOLB pc~0; GEL/NRP ~0")
# tarama sürprizleri
SC = pd.read_csv(os.path.join(HERE, "res_scan_fdr.csv"))
picks = [("GUBRF", "TAN", "sync_pc"), ("GUBRF", "ICLN", "sync_pc"), ("SISE", "TKGBY", "sync_pc"), ("SISE", "011170.KS", "intra_l1"), ("SISE", "^KS11", "intra_l1"), ("CIMSA", "^STOXX", "gap_l1_pc"),
         ("CIMSA", "SGO.PA", "gap_l1_pc"), ("CIMSA", "STR.VI", "sync_pc"), ("HEKTS", "CVR", "sync_pc"), ("OYAKC", "KTOS", "sync_pc")]
for st, dr, te in picks:
    x = SC[(SC.stock == st) & (SC.driver == dr) & (SC.test == te)]
    if not len(x): continue
    x = x.iloc[0]
    rel = {"sync_pc": "sync", "intra_l1": "lead_intra", "gap_l1_pc": "lead_gap"}[te]
    cf = "DÜŞÜK" if x.robust else "ÇOK DÜŞÜK"
    mech = {"TAN": "şüpheli: 2020-21 'yeşil/tema' bireysel yatırımcı akımı?", "ICLN": "şüpheli (aynı)", "TKGBY": "banka-sanayi stil faktörü (SISE banka değil)",
            "011170.KS": "Asya_t-1 bilgisinin yavaş yayılımı? (Asya kümesi tek faktör)", "^KS11": "aynı", "^STOXX": "CIMSA gap'i Avrupa'ya XU100'den duyarlı (AB satışları) ama gün-içi geri dönüyor",
            "SGO.PA": "aynı (işlenemez)", "STR.VI": "Avrupa inşaat", "CVR": "ABD azot gübresi (HEKTS'te gübre yok) -> şüpheli", "KTOS": "mekanizma yok -> sahte"}[dr]
    F.loc[len(F)] = dict(stock=st, driver_yahoo=dr, driver_desc="tarama sürprizi (" + te + ")", tv_ticker=tv(dr), relation=rel, lag=0 if te == "sync_pc" else 1,
                         corr_full=x.r, corr_3y=x.c_3y, corr_1y=np.nan, pcorr_xu100=x.r if "pc" in te else np.nan, beta=np.nan, t_stat=x.t_nw, gap_corr=x.r if "gap" in te else np.nan,
                         intra_corr=x.r if "intra" in te else np.nan, is_oos=f"IS {x.c_IS:+.3f} / OOS {x.c_OOS:+.3f}; yıl-işaret {x.yrs_same:.2f}", bt_oos_sharpe=np.nan, bt_oos_mean_bps=np.nan,
                         n=x.n, confidence=cf, mechanism=mech, notes="tarama 2014-2026, 39.132 test, BH-FDR q=0.05 geçti; 1.087 sürücü")
# ---- A8 tamamlayıcı sonuçlar ----
RO = pd.read_csv(os.path.join(HERE, "res_extra_rolling.csv")).set_index(["stock", "driver"])
def _rn(st, dr):
    k = (st, dr.replace(".IS", "") if dr.replace(".IS", "") in [x[1] for x in RO.index] else dr)
    if k not in RO.index: return ""
    x = RO.loc[k]; return f" | 250g kayan pc: min {x.pc250_min:+.2f} medyan {x.pc250_med:+.2f} maks {x.pc250_max:+.2f}, pozitif oran {x.pc250_frac_pos:.2f}, SON {x.pc250_last:+.2f}"
for i, r in F.iterrows():
    if r.relation == "sync": F.at[i, "notes"] = r.notes + _rn(r.stock, r.driver_yahoo)
msk = (F.stock == "SISE") & (F.driver_yahoo == "XBANK.IS") & (F.relation == "sync")
F.loc[msk, "confidence"] = "ORTA"; F.loc[msk, "notes"] = F.loc[msk, "notes"] + " | SON 250g'de işaret döndü (+0,15) -> YÜKSEK'ten ORTA'ya indirildi"
VM = pd.read_csv(os.path.join(HERE, "res_extra_volmom_bt.csv"))
for st, cf in [("HEKTS", "ORTA"), ("GUBRF", "DÜŞÜK")]:
    x = VM[(VM.stock == st) & (VM.target == "cc") & (VM.cost == 10)].iloc[0]; g = VM[(VM.stock == st) & (VM.target == "cc") & (VM.cost == 0)].iloc[0]
    it = VM[(VM.stock == st) & (VM.target == "intra") & (VM.cost == 10)].iloc[0]
    F.loc[len(F)] = dict(stock=st, driver_yahoo="(kendi r_t-1 x anormal TL hacmi_t-1 üst tercil)", driver_desc="hacim koşullu momentum (bireysel ilgi vekili)", tv_ticker="BIST:" + st,
                         relation="lead_multiday", lag=1, corr_full=np.nan, corr_3y=np.nan, corr_1y=np.nan, pcorr_xu100=np.nan, beta=np.nan, t_stat=x.t_OOS, gap_corr=np.nan, intra_corr=np.nan,
                         is_oos=f"10bps: IS {x.mean_bps_IS:+.1f}bps (t{x.t_IS:+.1f}) / OOS {x.mean_bps_OOS:+.1f}bps (t{x.t_OOS:+.1f}); brüt IS {g.mean_bps_IS:+.1f} (t{g.t_IS:+.1f}) / OOS {g.mean_bps_OOS:+.1f} (t{g.t_OOS:+.1f}); brüt pozitif yıl {int(g.pos_years)}/{int(g.years)}",
                         bt_oos_sharpe=x.sharpe_OOS, bt_oos_mean_bps=x.mean_bps_OOS, n=x.n_OOS, confidence=cf,
                         mechanism="bireysel yatırımcı ilgisi: yüksek hacimli gün getirisi ertesi güne (özellikle gece/gap) taşıyor",
                         notes=f"getiri büyük ölçüde t gap'inde: aynı sinyal -> intra_t 10bps OOS {it.mean_bps_OOS:+.1f}bps (t{it.t_OOS:+.1f}). Uygulama: spot kapanış 18:10, VİOP pay vadelisi 18:15'e kadar açık -> kapanışta giriş mümkün (baz/likidite riski). Diğer 4 hissede yok")
F.loc[len(F)] = dict(stock="GUBRF", driver_yahoo="(kendi tavan/taban günü |r_t-1|>%9,5)", driver_desc="limit günü sonrası", tv_ticker="BIST:GUBRF", relation="lead_gap", lag=1,
                     corr_full=np.nan, corr_3y=np.nan, corr_1y=np.nan, pcorr_xu100=np.nan, beta=np.nan, t_stat=2.6, gap_corr=np.nan, intra_corr=np.nan, is_oos="tam dönem 2014-2026",
                     bt_oos_sharpe=np.nan, bt_oos_mean_bps=np.nan, n=np.nan, confidence="DÜŞÜK", mechanism="fiyat marjı birikmiş talebi ertesi açılışa taşıyor",
                     notes="sign(r_t-1)*cc_t = +230bps brüt (t2,6) ama sign*intra_t = -155bps (t-2,6): devam GAP'te, gün içinde geri dönüş. Örneklem küçük")
EVO = pd.read_csv(os.path.join(HERE, "res_extra_oyak_tekfen.csv"))
def _ev(lab, st, w): x = EVO[(EVO.event.str.startswith(lab)) & (EVO.stock == st) & (EVO.win == w)].iloc[0]; return x.CAR_pct, x.z
c1, z1 = _ev("OYAK", "TKFEN", "(0, 10)"); c0, z0 = _ev("OYAK", "TKFEN", "(0, 0)"); c2, z2 = _ev("Pay", "TKFEN", "(0, 10)")
F.loc[len(F)] = dict(stock="TKFEN", driver_yahoo="(olay) OYAK'ın Tekfen %42,8 payını devralması", driver_desc="KAP 09.06.2026 görüşme / 24.07.2026 devir (ON Investment B.V.)", tv_ticker="BIST:TKFEN",
                     relation="event", lag=0, corr_full=np.nan, corr_3y=np.nan, corr_1y=np.nan, pcorr_xu100=np.nan, beta=np.nan, t_stat=z2, gap_corr=np.nan, intra_corr=np.nan, is_oos="tek olay (2026)",
                     bt_oos_sharpe=np.nan, bt_oos_mean_bps=np.nan, n=1, confidence="ORTA", mechanism="hakim ortak değişimi: Toros-Hektaş-gübre sinerjisi beklentisi",
                     notes=f"görüşme haberi: CAR(0,0)={c0:+.1f}% (z{z0:+.1f}), CAR(0,10)={c1:+.1f}% (z{z1:+.1f}); devir tamamlanınca CAR(0,10)={c2:+.1f}% (z{z2:+.1f}). "
                           "OYAK grubu ortak hareketi henüz yok: TKFEN-HEKTS pc 0,21 -> 0,01, TKFEN-OYAKC 0,01 -> 0,06 (n=101 gün) -> TKFEN-HEKTS-OYAKC 'OYAK kümesi' hipotezi ÇOK DÜŞÜK, izlenmeli")
HL = pd.read_csv(os.path.join(HERE, "res_extra_hourly_leadlag.csv"))
for _, x in HL[HL.fdr].iterrows():
    F.loc[len(F)] = dict(stock=x.stock.replace(".IS", ""), driver_yahoo=x.leader, driver_desc=f"saatlik küme-içi öncülük ({x.cluster})", tv_ticker=tv(x.leader if x.leader.endswith(".IS") else x.leader + ".IS"),
                         relation="intraday_minutes", lag=1, corr_full=x.c, corr_3y=np.nan, corr_1y=np.nan, pcorr_xu100=x.pc_xu, beta=np.nan, t_stat=x.t, gap_corr=np.nan, intra_corr=np.nan,
                         is_oos="2023-11..2026-10 (yalnız OOS)", bt_oos_sharpe=np.nan, bt_oos_mean_bps=x.bt_gross_bps, n=x.n, confidence="DÜŞÜK",
                         mechanism="küme içinde bilgi 1 saat gecikmeyle yayılıyor (büyük/likit -> küçük)",
                         notes=f"40 testte BH-FDR geçti; |x|>%0,5 sinyalinde BRÜT {x.bt_gross_bps:.1f}bps/işlem (n{int(x.bt_n)}) < 8-15bps maliyet -> işlenemez")
GF = pd.read_csv(os.path.join(HERE, "res_extra_gapfade_h1.csv"))
for st in ["CIMSA", "OYAKC"]:
    g = GF[(GF.stock == st) & (GF.thr == 0.01) & (GF.cost == 10)].set_index("entry")
    msk = (F.stock == st) & (F.driver_yahoo.str.contains("açılış gap"));
    F.loc[msk, "notes"] = F.loc[msk, "notes"] + f" | GERÇEKÇİ DOLUM (2023-12+, 10bps): açılış {g.loc['open','mean_bps']:+.0f}bps (t{g.loc['open','t']:+.1f}), 10:30 TSİ giriş {g.loc['0730UTC','mean_bps']:+.0f} (t{g.loc['0730UTC','t']:+.1f}), 11:30 TSİ {g.loc['0830UTC','mean_bps']:+.0f} (t{g.loc['0830UTC','t']:+.1f}) -> gecikmeli girişte de sürüyor"
# saatlik FDR notu
I2 = pd.read_csv(os.path.join(HERE, "res_intraday_fdr.csv"))
for i, r in F[F.relation == "intraday_minutes"].iterrows():
    x = I2[(I2.stock == r.stock) & (I2.driver == r.driver_yahoo) & I2.c_sync_snap.notna()]
    if len(x): F.at[i, "notes"] = r.notes + f" | FDR(63 saatlik test): senkron {'geçti' if x.iloc[0].t_sync_snap_fdr else 'geçmedi'}, kapanış-sonrası->intra {'geçti' if x.iloc[0].t_after_intra1_fdr else 'geçmedi'}"
F.loc[(F.stock == "SISE") & (F.driver_yahoo == "NG=F") & (F.relation == "intraday_minutes"), "confidence"] = "DÜŞÜK"
F.loc[F.driver_yahoo.str.contains("Üre / DAP"), "tv_ticker"] = "CBOT:UFV1! (Üre FOB US Gulf); CBOT:UME1! (Üre FOB Orta Doğu)"
num = ["corr_full", "corr_3y", "corr_1y", "pcorr_xu100", "beta", "t_stat", "gap_corr", "intra_corr", "bt_oos_sharpe", "bt_oos_mean_bps"]
F[num] = F[num].astype(float).round(3)
order = {"YÜKSEK": 0, "ORTA": 1, "DÜŞÜK": 2, "ÇOK DÜŞÜK": 3}
F = F.sort_values(["stock", "confidence", "pcorr_xu100"], key=lambda s: s.map(order) if s.name == "confidence" else (s.abs() * -1 if s.name == "pcorr_xu100" else s))
F.to_csv(os.path.join(OUT, "f_kimya.csv"), index=False)
print(F.shape, F.confidence.value_counts().to_dict(), "hyp FDR geçen:", int(M.fdr.sum()), "/", NTEST)
print(F[F.confidence.isin(["YÜKSEK", "ORTA"])][["stock", "driver_yahoo", "relation", "corr_full", "pcorr_xu100", "t_stat", "confidence"]].to_string(index=False))
