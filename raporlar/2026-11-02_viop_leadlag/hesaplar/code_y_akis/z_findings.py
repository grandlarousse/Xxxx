"""Bulgular CSV'si: out/f_y_akis.csv (ana brif sütunları). Sayılar res_*.csv/json ve log_*.txt'den; bazı yıl kırılımları burada hesaplanır."""
import numpy as np, pandas as pd, json, alib
OUT = alib.SCR + '/out/f_y_akis.csv'
E = pd.read_parquet('res_limit_events.parquet'); E = E[E.reg == 'P10'].sort_values(['stock', 'date']).copy()
E['BC_next'] = E.groupby('stock').BC.shift(-1)
def yrs(sub, col, sg=1):
    g = (sg * sub[col]).groupby(sub.date.dt.year).mean(); return f"{int((g > 0).sum())}/{len(g)}"
cols = ['stock', 'driver_yahoo', 'driver_desc', 'tv_ticker', 'relation', 'lag', 'corr_full', 'corr_3y', 'corr_1y', 'pcorr_xu100', 'beta', 't_stat', 'gap_corr', 'intra_corr', 'is_oos',
        'bt_oos_sharpe', 'bt_oos_mean_bps', 'n', 'confidence', 'mechanism', 'notes']
R = []
def add(**k): R.append({c: k.get(c, '') for c in cols})
S = pd.read_csv('res_limit_summary.csv')
def g(cls, grp, v):
    x = S[(S.reg == 'P10') & (S.cls == cls) & (S.grp == grp)]; return x[v].iloc[0] if len(x) else np.nan
bt = json.load(open('res_bt_all.json'))
# --- Limit bulguları
add(stock='ALL_BIST(177)', driver_yahoo='kendi tavan kapanışı (TC)', driver_desc='Tavan kapanış (R>=1,0925 & c=h), ±%10 rejimi 2020-03+', tv_ticker='BIST:<KOD>', relation='event', lag=1,
    t_stat=g('TC', 'all', 'gap1_t'), gap_corr='', intra_corr='', n=int(g('TC', 'all', 'n')),
    is_oos=f"gap1 IS(20-22) {g('TC','IS_2020_22','gap1_bps')} / OOS(23-26) {g('TC','OOS_2023_26','gap1_bps')} bps; yıl {yrs(E[E.TC],'gap1')}",
    bt_oos_sharpe='', bt_oos_mean_bps='', confidence='YÜKSEK (olgu) / işlenemez',
    mechanism='Limit fiyatlamayı keser, bilgi ertesi açılışa taşar (gecikmiş fiyat keşfi)',
    notes=f"Ertesi gün gap +{g('TC','all','gap1_bps')} bps (t {g('TC','all','gap1_t')}), %{100*g('TC','all','p_pos_gap1'):.0f} pozitif; kilitli tavan (TCL) +{g('TCL','all','gap1_bps')} bps; dokunup kapanmayan (TU) yalnız +{g('TU','all','gap1_bps')}. Kapanışta alım kilitli tavanda dolmaz -> gap işlenemez. P(ertesi gün yine TC|TC)=0,26 (taban: 0,29) vs koşulsuz 0,021")
add(stock='VIOP47', driver_yahoo='kendi tavan kapanışı (TC)', driver_desc='Tavan kapanış -> ertesi gün açılıştan kapanışa geri dönüş', tv_ticker='BIST:<KOD>1!', relation='event', lag=1,
    t_stat=bt['BT1a_TC_fade_intra_viop47_c8']['ALL']['t'], n=bt['BT1a_TC_fade_intra_viop47_c8']['n_trades'],
    is_oos=f"BT 8bps: IS(20-22) {bt['BT1a_TC_fade_intra_viop47_c8']['IS_20_22']['mean_bps']} (t {bt['BT1a_TC_fade_intra_viop47_c8']['IS_20_22']['t']}) / OOS(23-26) {bt['BT1a_TC_fade_intra_viop47_c8']['OOS_23_26']['mean_bps']} (t {bt['BT1a_TC_fade_intra_viop47_c8']['OOS_23_26']['t']}); tüm evren yıl {yrs(E[E.TC],'intra1',-1)}",
    bt_oos_sharpe=bt['BT1a_TC_fade_intra_viop47_c8']['OOS_23_26']['sharpe_ann_active'], bt_oos_mean_bps=bt['BT1a_TC_fade_intra_viop47_c8']['OOS_23_26']['mean_bps'],
    confidence='ORTA', mechanism='Açılış seansında aşırı tepki (perakende kuyruğu) -> gün içi kısmi geri dönüş',
    notes=f"Ertesi gün açılışta SAT kapanışta kapat. VİOP47 net +{bt['BT1a_TC_fade_intra_viop47_c15']['ALL']['mean_bps']} bps @15bps (t {bt['BT1a_TC_fade_intra_viop47_c15']['ALL']['t']}); tüm evren +{bt['BT1a_TC_fade_intra_all_c15']['ALL']['mean_bps']} (t {bt['BT1a_TC_fade_intra_all_c15']['ALL']['t']}). Kontrol: +%6..9 kapanış (limite dokunmayan) ertesi gün-içi -8 bps -> etki limite özgü. Açılış fiyatından dolum iyimser varsayım; kriz hariç aynı (+83).")
add(stock='ALL_BIST(177)', driver_yahoo='tavana dokunup geri dönen gün (TU)', driver_desc='Gün içi tavan gördü, altında kapandı', tv_ticker='BIST:<KOD>', relation='event', lag=1,
    t_stat=bt['BT1b_TU_fade_intra_all_c15']['ALL']['t'], n=bt['BT1b_TU_fade_intra_all_c15']['n_trades'],
    is_oos=f"@15bps IS {bt['BT1b_TU_fade_intra_all_c15']['IS_20_22']['mean_bps']} (t {bt['BT1b_TU_fade_intra_all_c15']['IS_20_22']['t']}) / OOS {bt['BT1b_TU_fade_intra_all_c15']['OOS_23_26']['mean_bps']} (t {bt['BT1b_TU_fade_intra_all_c15']['OOS_23_26']['t']}); yıl {yrs(E[E.TU],'intra1',-1)}",
    bt_oos_sharpe=bt['BT1b_TU_fade_intra_all_c15']['OOS_23_26']['sharpe_ann_active'], bt_oos_mean_bps=bt['BT1b_TU_fade_intra_all_c15']['OOS_23_26']['mean_bps'],
    confidence='ORTA', mechanism='Başarısız limit denemesi = alıcı tükenmesi; ertesi gün gün-içi geri dönüş',
    notes=f"Ertesi gün gap ~0 (+{g('TU','all','gap1_bps')}), gün-içi {g('TU','all','intra1_bps')} bps; t+2..5 fazla {g('TU','all','cc2_5x_bps')}. VİOP47 @15: +{bt['BT1b_TU_fade_intra_viop47_c15']['ALL']['mean_bps']} (t {bt['BT1b_TU_fade_intra_viop47_c15']['ALL']['t']}); likit tercil @15 +{bt['BT1b_TU_fade_intra_all_liqH_c15']['ALL']['mean_bps']} (t {bt['BT1b_TU_fade_intra_all_liqH_c15']['ALL']['t']})")
a = E[E.BC & (E.BC_next == False)]
add(stock='ALL_BIST(177)', driver_yahoo='kendi taban kapanışı (BC)', driver_desc='Taban kapanış -> ertesi gün gap ve t+2..t+5 sürüklenme', tv_ticker='BIST:<KOD>', relation='lead_multiday', lag='1..5',
    t_stat=g('BC', 'all', 'cc2_5x_t'), n=int(g('BC', 'all', 'n')),
    is_oos=f"gap1 IS {g('BC','IS_2020_22','gap1_bps')} / OOS {g('BC','OOS_2023_26','gap1_bps')}; t+2..5 fazla IS {g('BC','IS_2020_22','cc2_5x_bps')} / OOS {g('BC','OOS_2023_26','cc2_5x_bps')}; dolum-uygun giriş yıl {yrs(a,'cc2_5x',-1)}",
    bt_oos_sharpe='', bt_oos_mean_bps='+238,5 (dolum-uygun, @15, OOS 2023+)',
    confidence='ORTA', mechanism='Limit satış baskısını erteler; zorunlu satış/teminat tamamlama birkaç güne yayılır (sürüklenme, geri dönüş değil)',
    notes=f"gap1 {g('BC','all','gap1_bps')} bps (t {g('BC','all','gap1_t')}), sonra t+2..5 XU100'e göre {g('BC','all','cc2_5x_bps')} bps. Ham BT (t+1 kapanış short) +628 bps ama t+1 yine tabansa dolum yok: yalnız t+1 taban DEĞİLSE giriş -> +209 bps @15 (t 4,6; IS 2020-22 +153 t1,8; OOS +239 t4,6); VİOP47 +144 (t 2,1). Açığa satış yasağı/yukarı adım kuralı spotta uygulanamazlığı artırır; yasak dönemlerinde etki daha güçlü DEĞİL (+122 vs +292)")
add(stock='ALL_BIST(177)', driver_yahoo='kilitli taban (BCL)', driver_desc='Gün boyu taban (h=l=c): ertesi gün açılışta AL kapanışta sat', tv_ticker='BIST:<KOD>', relation='event', lag=1,
    t_stat=bt['BT1c_BCL_long_intra_all_c15']['ALL']['t'], n=bt['BT1c_BCL_long_intra_all_c15']['n_trades'],
    is_oos=f"IS {bt['BT1c_BCL_long_intra_all_c15']['IS_20_22']['mean_bps']} (t {bt['BT1c_BCL_long_intra_all_c15']['IS_20_22']['t']}) / OOS {bt['BT1c_BCL_long_intra_all_c15']['OOS_23_26']['mean_bps']} (t {bt['BT1c_BCL_long_intra_all_c15']['OOS_23_26']['t']}); yıl 7/7 pozitif",
    bt_oos_sharpe=bt['BT1c_BCL_long_intra_all_c15']['OOS_23_26']['sharpe_ann_active'], bt_oos_mean_bps=bt['BT1c_BCL_long_intra_all_c15']['OOS_23_26']['mean_bps'],
    confidence='DÜŞÜK', mechanism='Kilitli tabanın ertesi günü açılış aşırı satış; gün-içi toparlanma (çarpık: isabet %30, birkaç büyük dönüş)',
    notes="Ertesi gap -763 bps, gün-içi +246; isabet yalnız %28-36 (sağa çarpık). VİOP47'de n=41 (24 gün) - yetersiz. Küçük hisselerde spread 15 bps'i aşar")
add(stock='VIOP47', driver_yahoo='VİOP pay vadelisi uzlaşma - spot (limit günü)', driver_desc='Spot taban/tavan günü vadeli uzlaşma değişimi eksi spot değişimi', tv_ticker='BIST:<KOD>1!', relation='lead_gap', lag=1,
    corr_full='BC 0,56 / TC 0,18', n=763, is_oos='BC IS 0,15 / OOS 0,67; TC IS 0,19 / OOS 0,17; gün-içi Spearman IC BC 0,07 (t 0,8), TC 0,25 (t 2,3)',
    confidence='DÜŞÜK', mechanism='Vadeli de ±%10 limitli (en yüksek/önceki uzlaşma maks 1,100) ama limitte kilitlenmediğinde gerçek fiyata işaret eder',
    notes='Taban günü vadeli spottan az düştüyse (üst %20, prim +211 bps) ertesi gap +109 bps; alt %80 -227..-368. Az sayıda aykırı değere dayalı, IS zayıf. Sinyal 18:15 sonrası; spot girişi kapanış fiyatından işlem seansında (dolum taban için kolay)')
add(stock='BIST_h1(~100)', driver_yahoo='limite yakınlık (gün-içi)', driver_desc='Mıknatıs testi: +%7-8 seviyesinden önce limit mi -%3 mü?', tv_ticker='BIST:<KOD>', relation='intraday_minutes', lag=0,
    n=894, confidence='DÜŞÜK (olumsuz)', mechanism='Limite yaklaşınca hızlanma (magnet) hipotezi',
    notes='Yukarı: P(limit önce)=0,623, martingal 0,564 (+6 puan) ama plasebo (+%3-4 -> +3 puan) 0,600 vs 0,500 (+10 puan) -> ek mıknatıs YOK; genel gün-içi momentum. Aşağı: yakın 0,557 vs 0,564; plasebo 0,463 vs 0,5. Saatlik çözünürlük kaba; büyük hisseler ağırlıklı')
C = pd.read_csv('res_circuit_breaker.csv')
add(stock='XU100', driver_yahoo='EBDKS adayı (XU100 gün-içi dip <= -%5)', driver_desc='Endeks devre kesici günleri 2020-02+ (32 gün; 2025-03-19, 2026-09-16 dahil)', tv_ticker='BIST:XU100', relation='event', lag='1..20',
    t_stat=1.75, n=len(C), is_oos='ertesi gün cc +102 bps (t 1,75, 20/32 pozitif), ertesi gap +8 (t 0,2), ertesi gün-içi +94 (t 1,6), t+1..20 +360 (t 2,2)',
    confidence='DÜŞÜK', mechanism='Panik satışı + devre kesici sonrası kısmi geri dönüş', notes='Ayrım: dipten kapanışa toparlanma çok değişken. 2021-12 ve 2020-03 kümelendi. Eşik değişikliği (5/7 -> tek %6) tarihi doğrulanamadı')
# --- Yabancı akış
FS = pd.read_csv('res_flow_summary.csv'); fa = FS[FS.per == 'ALL'].iloc[0]; fo = FS[FS.per == 'OOS_21_26'].iloc[0]; fi = FS[FS.per == 'IS_05_20'].iloc[0]
yb = pd.read_csv('res_flow_byyear.csv')
add(stock='XU100 (USD)', driver_yahoo='TCMB TP.PYUK3+TP.MKNETHAR.M7', driver_desc='Yabancı hisse net alımı (haftalık, mn $) <- önceki hafta USD getirisi (ters yön)', tv_ticker='(TV yok; EVDS)', relation='reverse', lag='-1 hafta',
    corr_full=round(fa.corr_rev_usd_wm1, 3), t_stat=fa.t_rev, n=int(fa.n), is_oos=f"IS {fi.corr_rev_usd_wm1:.2f} / OOS {fo.corr_rev_usd_wm1:.2f}; yıl {int((yb['rev']>0).sum())}/{len(yb)}",
    confidence='YÜKSEK (olgu; işlem sinyali değil)', mechanism='Yabancılar getiri peşinden gidiyor (pozitif geri besleme)', notes=f"Senkron corr {fa.corr_sync_usd:.2f}; akış öz-korelasyonu {fa.flow_ac1:.2f}. Getiri akışı öncülüyor, tersi değil")
add(stock='XU100 (USD) / XU030', driver_yahoo='TCMB TP.PYUK3+TP.MKNETHAR.M7', driver_desc='Yabancı akış_w -> yayın SONRASI 5 gün getiri (Perşembe 14:30 yayını)', tv_ticker='BIST:XU030D1!', relation='flow', lag='+1 hafta (yayın gecikmeli)',
    corr_full=round(fa.corr_post5_usd, 3), t_stat=fa.t_post5_fz, n=int(fa.n), is_oos=f"IS {fi.corr_post5_usd:.2f} / OOS {fo.corr_post5_usd:.2f}",
    bt_oos_sharpe=-0.06, bt_oos_mean_bps=-3.5, confidence='ÇOK DÜŞÜK (olumsuz)', mechanism='Bilgi içeren akış hipotezi',
    notes='sign(akış z) XU030 Perş kapanış -> Perş kapanış: tüm dönem -5 bps @8 (t -0,4); |z|>1: IS +35 (t 1,4) / OOS -12. Yayın öncesi kısım (işlenemez) corr 0,00; son 3y -0,19')
add(stock='XU030', driver_yahoo='TCMB yayın anı (Perşembe 11:30 UTC)', driver_desc='Akış_z -> yayın günü 11:30->kapanış XU030 getirisi (h1, 2023-11+)', tv_ticker='BIST:XU030', relation='intraday_minutes', lag=0,
    corr_full=0.217, n=153, is_oos='ilk saat (11:30-12:30) corr 0,22; 12:30->kapanış 0,14; plasebo günler -0,18..+0,05',
    bt_oos_sharpe='', bt_oos_mean_bps='+3 @8 / -4 @15 (12:30 sonrası giriş)', confidence='DÜŞÜK',
    mechanism='Yayınlanan akış haberi kısa süreli tepki üretir', notes='Etki ilk saatte; 12:30 sonrası işaret stratejisi maliyeti karşılamıyor. XBANK benzer (0,20)')
X = pd.read_csv('res_flow_xsec.csv')
for _, r in X.iterrows():
    add(stock=r.stock, driver_yahoo='TCMB yabancı akış (haftalık)', driver_desc='Akış_w ~ hisse fazla getirisi_w (XU100 TL\'ye göre) + yayın sonrası 5g', tv_ticker=f'BIST:{r.stock}', relation='flow', lag='0 / +1h',
        corr_full=round(r.corr_sync_x, 3), t_stat=round(r.t_sync, 2), n=int(r.n), is_oos=f"post5 corr IS {r.c_is:.2f} / OOS {r.c_oos:.2f} (t {r.t_post5:.2f}, FDR {'geçti' if r.fdr_post5 else 'geçmedi'})",
        confidence=('DÜŞÜK (senkron)' if r.fdr_sync else 'ÇOK DÜŞÜK'),
        mechanism='Yabancı alımı bankalar/holdinglerde göreli güç; savunmacı/iç talep hisselerinde göreli zayıflık', notes=f"senkron FDR {'geçti' if r.fdr_sync else 'geçmedi'} (47 test); öncülük (post5) 0/47 FDR")
# --- Fon krizi
K = pd.read_csv('res_fundcrisis_xsec.csv'); med = K.groupby('grp').crisis_Sep11_Oct30.median()
add(stock='tasfiye10 (TEHOL, ANELE, TRHOL, OZATD, PEKGY, IEYHO, DSTKF, ISKPL, SELEC, BIGEN)', driver_yahoo='SPK tasfiye kararı 17.09.2026', driver_desc='Fon krizi kesiti 11.09-30.10.2026', tv_ticker='BIST:TEHOL vb.', relation='regime', lag='',
    n=len(K), is_oos=f"medyan getiri tasfiye10 {100*med['tasfiye10']:.0f}% / diğer BIST {100*med['other_bist']:.0f}% / VİOP47 {100*med['viop47']:.0f}%",
    confidence='ORTA (olgu) / ÇOK DÜŞÜK (öncülük)', mechanism='Zorunlu fon satışı + fiili dolaşım kuralı -> küçük, önceden şişmiş hisselerde çöküş',
    notes='Kesit regresyon (n=184): kriz getirisi ~ önceki 12a getiri (-), oynaklık (-), hacim (+), tasfiye kuklası log -1,68 (z -5,4). Sepet_{t-1} -> XU030_t corr 0,00 (kriz), -0,04 (öncesi): öncülük yok. TEFAS günlük akış verisi WAF engeli nedeniyle alınamadı')
# --- Endeks değişiklikleri
IX = pd.read_csv('res_index_summary.csv').set_index('set')
add(stock='BIST30/50/100 giren-çıkan (6 çeyrek, 118 olay)', driver_yahoo='Endeks dönem değişikliği duyurusu', driver_desc='Duyuru -> tepki günü -> yürürlük arifesi kapanışı -> sonrası', tv_ticker='BIST:<KOD>', relation='event', lag='0..20',
    t_stat=IX.loc['excl_2026Q4', 'R0_t'], n=int(IX.loc['excl_2026Q4', 'n']),
    is_oos=f"tepki günü işaretli fazla getiri: tümü {IX.loc['all','R0_bps']} bps (6/6 çeyrek), 2026Q4 hariç {IX.loc['excl_2026Q4','R0_bps']} (5/5); arifeye kadar sürüklenme 2026Q4 hariç {IX.loc['excl_2026Q4','RUN_bps']}; arife günü {IX.loc['excl_2026Q4','EVE_bps']} (0/5)",
    bt_oos_sharpe='', bt_oos_mean_bps=f"{IX.loc['excl_2026Q4','bt_run_c15_bps']} (2026Q4 hariç, tepki kapanışı->arife, @15)", confidence='DÜŞÜK',
    mechanism='Endeks fonu talebi; Türkiye\'de pasif fon payı küçük -> etki duyuru gününde tükeniyor', notes='Olay listesi web haberlerinden (2024Q4, 2025Q3, 2025Q4, 2026Q1, 2026Q2, 2026Q4); 2026Q4 fon krizi çıkarmalarıyla karışık (çıkanlar -%20+ düştü). Arife günü işaretli -100 bps (t -2,5): front-running sonrası kapanışta ters hareket? n küçük')
# --- Takvim
CI = pd.read_csv('res_cal_index.csv')
def ci(flag, col, v):
    x = CI[(CI.flag == flag) & (CI.col == col)]; return x[v].iloc[0]
b5 = bt['BT5_d1_XU030_c8']
add(stock='XU100/XU030', driver_yahoo='ayın ilk işlem günü', driver_desc='Ay dönümü (d1): XU100 cc', tv_ticker='BIST:XU030D1!', relation='event', lag=0,
    t_stat=ci('d1', 'xcc', 't_diff'), n=int(ci('d1', 'xcc', 'n')), is_oos=f"IS {ci('d1','xcc','IS_bps')} / OOS {ci('d1','xcc','OOS_bps')} bps; yıl {ci('d1','xcc','yrs_pos')}",
    bt_oos_sharpe=b5['OOS']['sharpe'], bt_oos_mean_bps=b5['OOS']['mean_bps_per_day_in'], confidence='DÜŞÜK',
    mechanism='Maaş/fon girişleri, ay başı portföy dengelemesi', notes=f"d1 ort +{ci('d1','xcc','mean_bps')} bps vs diğer {ci('d1','xcc','other_bps')}; BT (ay sonu kapanış al -> d1 kapanış sat, @8): tüm {b5['ALL']['mean_bps_per_day_in']} (t {b5['ALL']['t']}), IS {b5['IS']['mean_bps_per_day_in']} / OOS {b5['OOS']['mean_bps_per_day_in']} (t {b5['OOS']['t']}) -> yalnız 2021+ rejimi")
add(stock='XU100', driver_yahoo='çeyrek ilk günü (endeks yürürlük günü)', driver_desc='Mar/Haz/Eyl/Ara son iş günü ertesi', tv_ticker='BIST:XU030D1!', relation='event', lag=1,
    t_stat=ci('qend', 'xcc_next', 't_diff'), n=int(ci('qend', 'xcc_next', 'n')), is_oos=f"IS {ci('qend','xcc_next','IS_bps')} / OOS {ci('qend','xcc_next','OOS_bps')}; yıl {ci('qend','xcc_next','yrs_pos')}",
    confidence='DÜŞÜK', mechanism='Çeyrek başı fon girişleri / endeks dengeleme sonrası', notes='d1 etkisinin çeyrek başı alt kümesi; OOS n=23')
add(stock='XU100', driver_yahoo='bayram/tatil öncesi gün', driver_desc='Ardından >=1 hafta içi kapalı gün', tv_ticker='BIST:XU100', relation='event', lag=0,
    t_stat=ci('pre_hol', 'xintra', 't_diff'), n=int(ci('pre_hol', 'xintra', 'n')), is_oos=f"gün-içi IS {ci('pre_hol','xintra','IS_bps')} / OOS {ci('pre_hol','xintra','OOS_bps')}; yıl {ci('pre_hol','xintra','yrs_pos')}",
    confidence='DÜŞÜK', mechanism='Tatil öncesi risk azaltma (klasik pozitif tatil-öncesi etkisinin TERSİ)', notes=f"tatil öncesi cc {ci('pre_hol','xcc','mean_bps')} vs {ci('pre_hol','xcc','other_bps')}; dini bayram arifesi (yarım gün) cc {ci('pre_rel','xcc','mean_bps')}, ertesi (bayram sonrası ilk gün) +{ci('pre_rel','xcc_next','mean_bps')} (n 44). Bayram gap'i olay ajanınca test edildi")
add(stock='XU100', driver_yahoo='MSCI / FTSE / VİOP vade sonu günleri', driver_desc='Ay sonu (vade sonu), MSCI (Şub/May/Ağu/Kas), FTSE (Mar/Haz/Eyl/Ara 3. Cuma)', tv_ticker='BIST:XU100', relation='event', lag='0/1',
    n=int(ci('me', 'xcc', 'n')), confidence='ÇOK DÜŞÜK (olumsuz)', mechanism='Dengeleme akışları',
    notes=f"ay sonu cc {ci('me','xcc','mean_bps')} vs {ci('me','xcc','other_bps')} (t {ci('me','xcc','t_diff')}); MSCI günü gap {ci('msci','xgap','mean_bps')} (t {ci('msci','xgap','t_diff')}); FTSE gün-içi {ci('ftse','xintra','mean_bps')} (t {ci('ftse','xintra','t_diff')}) -> hiçbiri anlamlı değil")
A = pd.read_csv('res_auction.csv')
am = A[(A.set == 'me') & (A.grp == '47')].iloc[0]; ao = A[(A.set == 'non_me') & (A.grp == '47')].iloc[0]
add(stock='VIOP47', driver_yahoo='kapanış seansı getirisi (vade sonu günü)', driver_desc='log(kapanış/15:00 UTC) ve ertesi gün geri dönüşü (h1 2023-11+)', tv_ticker='BIST:<KOD>1!', relation='lead_auction', lag=1,
    corr_full=f"cc1 {am.corr_cc1}", t_stat=am.rev_cc1_t, n=int(am.n), is_oos='yalnız 36 vade sonu (2023-11..2026-10); IS/OOS ayrımı anlamsız',
    bt_oos_mean_bps=f"{am.rev_cc1_bps} (brüt, -işaret(auc), kapanış->ertesi kapanış)", confidence='DÜŞÜK',
    mechanism='Vade sonu uzlaşması kapanış seansına bağlı -> geçici fiyat baskısı', notes=f"|auc| vade sonu {am.abs_auc_bps} vs normal {ao.abs_auc_bps} bps; geri dönüş katsayısı (cc1) {am.b_cc1} vs normal {ao.b_cc1}. FTSE/çeyrek sonu günlerinde daha güçlü (b -0,9/-0,6) ama n=11-12 gün")
DS = pd.read_csv('res_div_summary.csv').set_index('set')
b6 = bt['BT6b_exday_short_intra_viop47_c15']; b6a = bt['BT6a_pre5_long_all_c15']; b6v = bt['BT6a_pre5_long_viop47_c15']
add(stock='VIOP47 + BIST (130 hisse)', driver_yahoo='temettü ex-günü', driver_desc='Ex-gün açılış -> kapanış (düzeltilmiş açılış h1 ile doğrulandı)', tv_ticker='BIST:<KOD>1!', relation='event', lag=0,
    t_stat=DS.loc['all', 'intra0_t'], n=int(DS.loc['all', 'n']), is_oos=f"gün-içi IS(2010-20) -34 / OOS(21-26) -105 bps; VİOP47 @15 BT IS {b6['IS']['mean_bps']} / OOS {b6['OOS']['mean_bps']} (t {b6['OOS']['t']})",
    bt_oos_mean_bps=b6['OOS']['mean_bps'], confidence='ORTA', mechanism='Ex-gün açılışı temettüden az düşüyor (ilk gap +92 bps), gün içinde düzeliyor (çapa/perakende)',
    notes=f"Fiyat düşüş oranı medyan {DS.loc['all','PDR_med']}; ex-gün düzeltilmiş getiri +{DS.loc['all','r_adj_bps']} (IS +54 / OOS -6) -> kapanış bazlı etki kayboldu, gün-içi kısmı kaldı. Hisse başı yılda 1-4 olay")
add(stock='BIST (130 hisse) / VIOP47', driver_yahoo='temettü ex-günü öncesi 5 gün', driver_desc='ex-5 kapanış al -> ex-1 kapanış sat (XU100\'e göre)', tv_ticker='BIST:<KOD>1!', relation='event', lag='-5..-1',
    t_stat=DS.loc['all', 'pre5_t'], n=int(DS.loc['all', 'n']), is_oos=f"@15 tümü IS {b6a['IS']['mean_bps']} (t {b6a['IS']['t']}) / OOS {b6a['OOS']['mean_bps']} (t {b6a['OOS']['t']}); VİOP47 IS {b6v['IS']['mean_bps']} / OOS {b6v['OOS']['mean_bps']}",
    bt_oos_mean_bps=b6a['OOS']['mean_bps'], confidence='ORTA', mechanism='Temettü yakalama talebi (önceden ilan edilen hak kullanım tarihi)',
    notes=f"sonrası 5 gün {DS.loc['all','post5_bps']} bps (OOS -102, t -4,2) -> ex sonrası geri veriş. VİOP vadeli temettüyü taşımaz ama fiyat değişimini taşır; 5 günlük tutuş, hedge XU030")
BS = pd.read_csv('res_bedelsiz_summary.csv').set_index('set')
add(stock='BIST (bedelsiz yapan, 92 olay)', driver_yahoo='bedelsiz ex-günü (Yahoo split)', driver_desc='Bedelsiz bölünme sonrası 5/20 gün fazla getiri', tv_ticker='BIST:<KOD>', relation='event', lag='+1..+20',
    t_stat=BS.loc['all', 'post5_t'], n=int(BS.loc['all', 'n']), is_oos=f"post20 IS {BS.loc['IS_2010_20','post20_bps']} / OOS {BS.loc['OOS_2021_26','post20_bps']} bps",
    confidence='DÜŞÜK', mechanism='Bedelsiz coşkusu duyuru-ex arasında fiyatlanır, sonra geri verilir',
    notes=f"post5 {BS.loc['all','post5_bps']} bps (medyan {BS.loc['all','post5_med']}), post20 {BS.loc['all','post20_bps']}; ex öncesi 20 gün ortalama ~0 (medyan -101). 47 VİOP hissesinde 2010+ bedelsiz olayı Yahoo'da yok -> VİOP ile işlenemez; spot açığa satış kısıtlı")
# --- veri bulunamayanlar
add(stock='47', driver_yahoo='açığa satış hacmi (günlük, hisse bazlı)', driver_desc='BIST/fintables açığa satış istatistikleri', tv_ticker='?', relation='hypothesis', confidence='ÇOK DÜŞÜK (veri yok)',
    mechanism='Açığa satış baskısı -> ertesi gün', notes='Kamuya açık indirilebilir tarihsel seri bulunamadı (fintables 403; BIST veri sayfasında yok). Yalnız yasak dönemleri rejim olarak test edildi: tavan/taban etkileri yasakta farklı değil')
add(stock='47', driver_yahoo='kredili işlem bakiyesi / teminat tamamlama', driver_desc='SPK/TSPB aylık', tv_ticker='?', relation='hypothesis', confidence='ÇOK DÜŞÜK (veri yok)',
    mechanism='Margin call satışı -> taban serisi', notes='Yalnız Ağustos 2026 stok 129,2 mlr TL ve Eylül teminat tamamlama 1,13 mlr TL (1. tur kaynakları); zaman serisi yok. Taban sürüklenmesi (yukarıda) bu mekanizmayla tutarlı ama test edilmedi')
add(stock='47', driver_yahoo='MKK hisse bazlı yabancı takas oranı', driver_desc='Günlük yabancı payı', tv_ticker='?', relation='hypothesis', confidence='ÇOK DÜŞÜK (veri yok)',
    mechanism='Yabancı payı değişimi -> getiri', notes='Kamuya açık arşiv bulunamadı (yalnız haber özetleri); haftalık toplam akış kullanıldı')
add(stock='47', driver_yahoo='TEFAS hisse fonu akışları (günlük)', driver_desc='Fon büyüklüğü/pay sayısı değişimi', tv_ticker='?', relation='hypothesis', confidence='ÇOK DÜŞÜK (veri yok)',
    mechanism='Fon girişleri -> hisse talebi', notes='tefas.gov.tr API/sayfaları WAF ile reddedildi (HTTP 404 "Method not found" / "Request Rejected"); atlatma denenmedi. Gedik 05.10 raporundan stok rakamlar: tasfiye fonları 1.233 -> 652 mlr TL (31.08->30.09)')
F = pd.DataFrame(R, columns=cols); F.to_csv(OUT, index=False); print('yazıldı', OUT, len(F))
