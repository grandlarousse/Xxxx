"""res_*.csv -> out/f_holding.csv (brif şeması). Güven etiketleri elle (rapordaki gerekçeyle) atanır; sayılar dosyalardan çekilir."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hc, numpy as np, pandas as pd
C = hc.CODE
H = pd.read_csv(f'{C}/res_hyp.csv'); S = pd.read_csv(f'{C}/res_scan.csv'); B = pd.read_csv(f'{C}/res_bt.csv')
N = pd.read_csv(f'{C}/res_subs_nav.csv'); I = pd.read_csv(f'{C}/res_intraday.csv')
TV = {'TRY=X': 'FX:USDTRY', 'EURTRY=X': 'FX:EURTRY', 'RUB=X': 'FX_IDC:USDRUB', 'SBK.JO': 'JSE:SBK', 'FSR.JO': 'JSE:FSR', 'AKBTY': 'OTC:AKBTY',
      '^STOXX50E': 'TVC:SX5E', 'MRL.MC': 'BME:MRL', 'AENA.MC': 'BME:AENA', 'TUR': 'AMEX:TUR', 'F': 'NYSE:F', 'BZ=F': 'ICEEUR:BRN1!', 'TTF=F': 'ICEENDEX:TFM1!',
      'MTF=F': 'ICEEUR:ATW1! ?', '^TNX': 'TVC:US10Y', 'XHB': 'AMEX:XHB', 'ITB': 'AMEX:ITB', 'VNA.DE': 'XETR:VNA', 'VNQ': 'AMEX:VNQ', 'CRAK': 'AMEX:CRAK',
      'HOT.DE': 'XETR:HOT', 'ACS.MC': 'BME:ACS', 'STLAM.MI': 'MIL:STLAM', 'EURUSD=X': 'FX:EURUSD', 'GC=F': 'COMEX:GC1!', 'ES=F': 'CME_MINI:ES1!', 'EUFN': 'NASDAQ:EUFN',
      'CRACK': 'NYMEX:HO1!*42-ICEEUR:BRN1! (spread) ?', 'NAV': 'BIST:TUPRS,BIST:FROTO,BIST:YKBNK,BIST:ARCLK,BIST:TOASO (sepet)'}
def tv(d):
    if d.endswith('.IS'): return 'BIST:' + d[:-3]
    return TV.get(d, '?')
rows = []
def hyp(stock, drv, rel, conf, mech, notes='', usd=False, lag=0):
    st = stock + ('_USD' if usd else '')
    r = H[(H.stock == st) & (H.driver == drv)]
    if r.empty:  # yalnız taramada var -> tarama değerleri
        sc = S[(S.stock == stock) & (S.sym == drv)].iloc[0]
        rows.append(dict(stock=st, driver_yahoo=drv, driver_desc='', tv_ticker=tv(drv), relation=rel, lag=lag, corr_full=sc.c0, corr_3y='', corr_1y='', pcorr_xu100=sc.pc, beta='',
                         t_stat=sc.pc_t, gap_corr=sc.gap1, intra_corr=sc.intra1, is_oos=f"pcIS={sc.pc_IS:.3f}/pcOOS={sc.pc_OOS:.3f}", bt_oos_sharpe='', bt_oos_mean_bps='', n=sc.n,
                         confidence=conf, mechanism=mech, notes=(notes + f" | tarama pc_padj={sc.pc_padj:.3g}").strip(' |')))
        return
    r = r.iloc[0]
    sc = S[(S.stock == stock) & (S.sym == drv)]
    fdr = '' if sc.empty else f"scan pc_padj={sc.iloc[0]['pc_padj']:.3g}, ipc1_padj={sc.iloc[0]['ipc1_padj']:.3g}"
    io = f"pcIS={r.pc_IS:.3f}/pcOOS={r.pc_OOS:.3f}; intraIS_t={r.get('intra_IS_t', np.nan):.2f}/intraOOS_t={r.get('intra_OOS_t', np.nan):.2f}; yrs_same_pc={r.yr_same_sign_pc:.2f}"
    t = r.pc_t if rel == 'sync' else (r.get('intra_t') if rel == 'lead_intra' else r.get('gap_t'))
    rows.append(dict(stock=st, driver_yahoo=drv, driver_desc='', tv_ticker=tv(drv), relation=rel, lag=lag, corr_full=r.corr_full, corr_3y=r.corr_3y, corr_1y=r.corr_1y,
                     pcorr_xu100=r.pc, beta=r.beta, t_stat=t, gap_corr=r.get('gap_c'), intra_corr=r.get('intra_c'), is_oos=io, bt_oos_sharpe='', bt_oos_mean_bps='',
                     n=r.n, confidence=conf, mechanism=mech, notes=(notes + ' | ' + fdr).strip(' |')))
def bt(name, cost=8.0):
    r = B[(B.test == name) & (B.cost_bps == cost)].iloc[0]; return r
def custom(stock, drv, rel, lag, conf, mech, notes, t=np.nan, corr=np.nan, pc=np.nan, n=np.nan, io='', btname=None, gapc=np.nan, intrac=np.nan, beta=np.nan):
    sh = mb = ''
    if btname:
        b = bt(btname); sh = round(b.OOS_sharpe, 2); mb = round(b.OOS_mean_bps, 1)
        b15 = bt(btname, 15.0)
        io += f"; BT(8bps) IS {b.IS_mean_bps:.1f}bps t={b.IS_t:.2f} SR={b.IS_sharpe:.2f} | OOS {b.OOS_mean_bps:.1f}bps t={b.OOS_t:.2f}; 15bps OOS {b15.OOS_mean_bps:.1f}bps"
    rows.append(dict(stock=stock, driver_yahoo=drv, driver_desc='', tv_ticker=tv(drv), relation=rel, lag=lag, corr_full=corr, corr_3y='', corr_1y='', pcorr_xu100=pc, beta=beta,
                     t_stat=t, gap_corr=gapc, intra_corr=intrac, is_oos=io, bt_oos_sharpe=sh, bt_oos_mean_bps=mb, n=n, confidence=conf, mechanism=mech, notes=notes))

# --- ENKAI ---
hyp('ENKAI', 'TRY=X', 'sync', 'ORTA', 'USD fonksiyonel para birimi, ~5 mlr USD net nakit, döviz geliri: TL değer kaybında piyasadan daha az düşer (göreli doğal hedge)', 'ham corr≈0 (piyasa düşüşü dengeliyor); |pc|<0,15 -> YÜKSEK değil')
hyp('ENKAI', 'EURTRY=X', 'sync', 'ORTA', 'aynı (EUR gelir/nakit)', '')
hyp('ENKAI', 'TRY=X', 'sync', 'ORTA', 'USD bazında ENKAI günlük TL şokunu ~1:1 taşır (TL fiyatı kura günlük yansımıyor; beta_USD≈-1)', 'USD bazlı getiri (FX_FIX hizalı)', usd=True)
hyp('ENKAI', 'TRY=X', 'lead_intra', 'DÜŞÜK', 'TL değer kaybının gün-içinde gecikmeli fiyatlanması (nakit zengini)', 'BT5: OOS +28,8bps t=1,46 (188 işlem) – anlamlı değil', lag=1)
hyp('ENKAI', 'TUR', 'lead_intra', 'ORTA', 'ABD seansı Türkiye riski açılışta ENKAI gap’ine yansır, gün-içinde kısmen geri döner (TL hedge göreli toparlanma)', 'açılış aşırı tepki/geri dönüş; 2021-22 rejimine bağımlı', lag=1)
hyp('ENKAI', 'RUB=X', 'lead_gap', 'DÜŞÜK', 'Moskova kira geliri/Rusya inşaat; RUB zayıflığı -> ENKAI', 'FX hizası düzeltilince senkron ≈0; eski hizada pc -0,08 SAHTE idi', lag=1)
hyp('ENKAI', 'BZ=F', 'sync', 'ÇOK DÜŞÜK', 'enerji (doğalgaz santralleri) / Irak-Rusya petrol ekonomisi', 'XU100 kontrollü ≈0')
hyp('ENKAI', 'TTF=F', 'sync', 'ÇOK DÜŞÜK', 'gaz santrali marjı (spark spread)', 'XU100 kontrollü ≈0, işaret tutarsız')
hyp('ENKAI', '^TNX', 'sync', 'ÇOK DÜŞÜK', 'USD nakit faiz geliri (günlük frekansta görünmez)', '')
hyp('ENKAI', 'HOT.DE', 'sync', 'DÜŞÜK', 'uluslararası müteahhit emsali', '')
# --- SAHOL ---
hyp('SAHOL', 'AKBNK.IS', 'sync', 'YÜKSEK', 'Akbank NAV’ın ~%34’ü', 'yurt içi iştirak')
hyp('SAHOL', 'TRY=X', 'sync', 'ORTA', 'banka ağırlıklı holding: TL şoku -> faiz/risk primi -> banka', '')
hyp('SAHOL', 'EURTRY=X', 'sync', 'ORTA', 'aynı', '')
hyp('SAHOL', 'SBK.JO', 'sync', 'ORTA', 'EM banka/yabancı akım faktörü (JSE kapanışı ~BIST ile eşzamanlı)', 'FSR.JO, ABG.JO, NED.JO benzer (FDR geçer)')
hyp('SAHOL', 'AKBTY', 'sync', 'ORTA', 'Akbank ADR (ABD seansı): aynı varlık', '')
hyp('SAHOL', '^STOXX50E', 'sync', 'DÜŞÜK', 'Avrupa risk iştahı/yabancı akım', 'IS 0,04 / OOS 0,10')
hyp('SAHOL', 'KORDS.IS', 'sync', 'ORTA', 'XU100 kontrollü negatif: banka-dışı sanayi iştiraki SAHOL’un banka ağırlığına ters faktör', 'AKSA Sabancı DEĞİL (Akkök); BRISA/AKSA da negatif pc')
hyp('SAHOL', 'TTF=F', 'sync', 'DÜŞÜK', 'Enerjisa Üretim gaz santralleri', '')
hyp('SAHOL', '^TNX', 'sync', 'ÇOK DÜŞÜK', 'ABD faiz -> EM banka', '')
# --- KCHOL ---
for s in ['ARCLK.IS', 'FROTO.IS', 'YKBNK.IS', 'TUPRS.IS', 'TOASO.IS']:
    hyp('KCHOL', s, 'sync', 'YÜKSEK', 'NAV bileşeni (Koç NAV: enerji %38, otomotiv %29, finans %24, d.tüketim %7)', 'yurt içi iştirak; TUPRS 1y corr düşük (0,24)')
hyp('KCHOL', 'BZ=F', 'sync', 'ÇOK DÜŞÜK', 'Tüpraş üzerinden', 'XU100 kontrollü 0,00; dış sürücü holdinge kayda değer yansımıyor')
hyp('KCHOL', 'CRACK', 'sync', 'ÇOK DÜŞÜK', 'dizel crack -> Tüpraş marjı', '')
hyp('KCHOL', 'F', 'lead_gap', 'ORTA', 'Ford Otosan ortağı; ABD kapanışı sonrası bilgi açılışta', 'İŞLENEMEZ (eşzamansız kapanış), intra t≈0', lag=1)
hyp('KCHOL', 'STLAM.MI', 'sync', 'ÇOK DÜŞÜK', 'Tofaş ortağı Stellantis', '')
hyp('KCHOL', 'EURUSD=X', 'lead_gap', 'DÜŞÜK', 'EUR ihracat geliri (FROTO/TOASO/ARCLK)', 'gap t≈2,9; intra yok; senkron pc≈0', lag=1)
hyp('KCHOL', 'TRY=X', 'sync', 'DÜŞÜK', 'ihracatçı iştirakler TL zayıflığından fayda vs. YKBNK zarar: net küçük negatif', '')
hyp('KCHOL', 'MRL.MC', 'sync', 'DÜŞÜK', 'mekanizma şüpheli (Avrupa çevre ülke/faiz risk faktörü?)', 'tarama sürprizi; AENA.MC de pc 0,08')
# --- DOHOL / ALARK / EKGYO ---
hyp('DOHOL', 'KAREL.IS', 'sync', 'ORTA', 'iştirak (Karel)', 'yurt içi')
hyp('DOHOL', 'GC=F', 'sync', 'ÇOK DÜŞÜK', 'Gümüştaş madencilik (altın/gümüş/çinko)', 'pc≈0')
hyp('DOHOL', 'TRY=X', 'sync', 'DÜŞÜK', 'holding düzeyi ~639 mn USD net nakit', 'pc +0,04, OOS 0,06')
hyp('ALARK', 'MTF=F', 'sync', 'ÇOK DÜŞÜK', 'Cenal ithal kömür santrali (enerji gelirin ~%72’si)', 'pc 0,01; BT5 boş; MTF %19 sıfır getiri (bayat)')
hyp('ALARK', 'TTF=F', 'sync', 'ÇOK DÜŞÜK', 'elektrik fiyatı gaz marjinal', '')
hyp('ALARK', 'ACS.MC', 'sync', 'ÇOK DÜŞÜK', 'Avrupa inşaat emsali', 'HOT/FER/SKA/VIE/STR hepsi pc≈0')
hyp('ALARK', 'EURTRY=X', 'sync', 'DÜŞÜK', 'TL şoku', '')
hyp('ALARK', 'ALCAR.IS', 'sync', 'ORTA', 'grup şirketi Alarko Carrier', 'yurt içi')
hyp('EKGYO', 'CRAK', 'sync', 'DÜŞÜK', 'petrol/rafineri yukarı -> TR enflasyon/faiz beklentisi -> konut GYO aşağı (göreli)', 'tarama sürprizi, FDR geçer; BZ ile doğrudan test yapılmadı')
hyp('EKGYO', 'XHB', 'lead_gap', 'DÜŞÜK', 'ABD konut', 'yalnız gap (işlenemez), senkron pc≈0', lag=1)
hyp('EKGYO', '^TNX', 'sync', 'ÇOK DÜŞÜK', 'ABD faiz', 'BT5: IS negatif, OOS pozitif -> tutarsız')
hyp('EKGYO', 'VNA.DE', 'sync', 'ÇOK DÜŞÜK', 'Avrupa konut GYO', '')
hyp('EKGYO', 'RYGYO.IS', 'sync', 'ORTA', 'yurt içi GYO faktörü', 'PSGYO pc 0,165 (kısa örneklem)')
# --- holding-iştirak lead-lag ve backtestler ---
n0 = N[(N.holding == 'KCHOL') & (N.basket == 'fixed') & (N.test == 'open_div->intra_t')].iloc[0]
ik = I[(I.holding == 'KCHOL') & (I.test == 'intra~navgap+hgap') & (I['sample'] == 'ALL')].iloc[0]
custom('KCHOL', 'NAV', 'lead_intra', 0, 'ORTA', 'holding açılışı iştirak sepetinin açılış hareketini eksik/fazla yansıtır; gün içinde NAV’a yakınsar',
       f"sinyal=NAVgap_t-KCHOLgap_t (açılıştan sonra bilinir); kendi gap kontrollü b_nav={ik.b_navgap:.2f} t={ik.t_navgap:.2f}; OOS zayıf", t=n0.t, corr=n0.c, pc=n0.pc_mkt, n=n0.n,
       io=f"t_IS={n0.t_IS:.2f}/t_OOS={n0.t_OOS:.2f}; yrs_same={n0.yr_same:.2f}", btname='BT1 KCHOL open NAV-div -> intra_t')
n1 = N[(N.holding == 'SAHOL') & (N.basket == 'fixed') & (N.test == 'open_div->intra_t')].iloc[0]
custom('SAHOL', 'NAV', 'lead_intra', 0, 'DÜŞÜK', 'aynı (SAHOL)', 'ham t≈0,9; XU100 kontrollü t 5,2 ama BT kaybettiriyor', t=n1.t, corr=n1.c, pc=n1.pc_mkt, n=n1.n,
       io=f"t_IS={n1.t_IS:.2f}/t_OOS={n1.t_OOS:.2f}", btname='BT1 SAHOL open NAV-div -> intra_t')
n2 = N[(N.holding == 'KCHOL') & (N.basket == 'fixed') & (N.test == 'div5->cc_t+1')].iloc[0]
custom('KCHOL', 'NAV', 'lead_multiday', 1, 'DÜŞÜK', 'NAV iskontosu kısa vadeli ortalamaya döner (5g ayrışma)', 'cc_{t+1} hedefi kapanışta giriş gerektirir', t=n2.t, corr=n2.c, pc=n2.pc_mkt, n=n2.n,
       io=f"t_IS={n2.t_IS:.2f}/t_OOS={n2.t_OOS:.2f}", btname='BT2b KCHOL div5_(t-1) -> cc_t (kapanışta giriş)')
custom('SAHOL', 'AKBNK.IS', 'lead_intra', 1, 'DÜŞÜK', 'Akbank’ın dünkü göreli hareketi SAHOL’a gecikmeli yansır', 'günlük kontrollü pc t≈3,4; BT OOS anlamsız', btname='BT4 SAHOL AKBNK_(t-1) -> intra_t')
custom('KCHOL', 'NAV', 'intraday_minutes', 1, 'DÜŞÜK', 'saatlik: iştirak sepeti_(h-1) -> KCHOL_h', 'h1 2023-11..2026-10; kendi gecikme+XU100 kontrollü pc 0,045 t≈3,0; ters yön ≈0; 5dk’da çift yönlü (ortak faktör)', t=2.98, pc=0.045, n=4765)
custom('KCHOL', 'TUPRS.IS', 'lead_multiday', 1, 'ÇOK DÜŞÜK', 'iştirak_t -> holding_{t+1} (günlük)', 'kendi gecikme + XU100 gecikme kontrollü pc≈0 tüm iştiraklerde: günlük yayılım YOK (ham pozitif lag1 = piyasa momentumu)')
custom('ENKAI', 'TUR', 'lead_intra', 1, 'DÜŞÜK', 'bkz. yukarı', 'piyasa-nötr versiyon (BT3b) OOS +10bps t 0,95', btname='BT3 ENKAI -TUR_(t-1) -> intra_t')
custom('ALARK', 'MTF=F', 'lead_intra', 1, 'ÇOK DÜŞÜK', 'kömür', 'negatif kontrol', btname='BT5 ALARK MTF=F_(t-1) -> intra_t')
custom('EKGYO', '^TNX', 'lead_intra', 1, 'ÇOK DÜŞÜK', 'ABD faiz', 'negatif kontrol; IS ve OOS ters işaret', btname='BT5 EKGYO ^TNX_(t-1) -> intra_t')
F = pd.DataFrame(rows)
for c in ['corr_full', 'corr_3y', 'corr_1y', 'pcorr_xu100', 'beta', 't_stat', 'gap_corr', 'intra_corr']:
    F[c] = pd.to_numeric(F[c], errors='coerce').round(3)
F.to_csv(os.path.join(hc.OUT, 'f_holding.csv'), index=False)
pd.set_option('display.width', 250)
print(len(F)); print(F[['stock', 'driver_yahoo', 'relation', 'corr_full', 'corr_3y', 'corr_1y', 'pcorr_xu100', 'beta', 't_stat', 'gap_corr', 'intra_corr', 'confidence', 'bt_oos_mean_bps']].to_string())

