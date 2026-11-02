"""Bulgular CSV'si (f_y_grup.csv) ve ortaklık tablosu (y_ortaklik.csv) üretimi."""
from gx import *
V = set(ll.VIOP)
cols = ['stock','driver_yahoo','driver_desc','tv_ticker','relation','lag','corr_full','corr_3y','corr_1y','pcorr_xu100','beta','t_stat','gap_corr','intra_corr','is_oos','bt_oos_sharpe','bt_oos_mean_bps','n','confidence','mechanism','notes']
F = []
def add(**k):
    r = {c: k.get(c, '') for c in cols}; F.append(r)
D = pd.read_csv(HERE + '/res_pairs.csv')
MECH = {'ps': 'ana ortaklık-iştirak (NAV payı)', 'sib': 'aynı grup kardeş şirket', 'cls': 'aynı şirketin pay grupları', 'jv': 'ortak girişim', 'none': 'grup bağı yok (kontrol)', '?': 'bağ doğrulanamadı', 'sib26': 'OYAK-Tekfen (Tem.2026 sonrası)'}
# ---- senkron satırları
for r in D.itertuples():
    if r.ana in V: st, dr, beta, tb = r.ana, r.yavru, r.beta_a_on_b, r.t_beta_ab
    elif r.yavru in V: st, dr, beta, tb = r.yavru, r.ana, r.beta_b_on_a, r.t_beta_ab
    else: st, dr, beta, tb = r.ana, r.yavru, r.beta_a_on_b, r.t_beta_ab
    pc, same = r.pc_full, np.sign(r.pc_IS) == np.sign(r.pc_OOS) if not np.isnan(r.pc_IS) else True
    if r.tur == 'none' or r.grup == 'KONTROL': conf = 'KONTROL'
    elif abs(pc) >= 0.15 and r.pc_yr_pos >= 0.75 and same and r.sync_fdr: conf = 'YÜKSEK'
    elif abs(pc) >= 0.05 and r.sync_fdr and same: conf = 'ORTA'
    elif r.sync_fdr: conf = 'DÜŞÜK'
    else: conf = 'ÇOK DÜŞÜK'
    if conf == 'YÜKSEK' and (r.n < 1500 or r.grup in ('?',) or (r.ana, r.yavru) == ('ISCTR', 'TSKB')): conf = 'ORTA'  # kısa örneklem / grup bağı yok / sektör faktörü
    note = f'grup={r.grup}; pc yıllar aynı işaret %{100*r.pc_yr_pos:.0f}; t_beta={tb:.1f}'
    if r.ana == 'ISCTR' and r.yavru == 'SISE': note += '; XU100+XBANK+XUSIN kontrollü pc=+0,083 (banka-sanayi rotasyonu XU100 kontrolünde işareti çeviriyor)'
    if r.ana == 'ISCTR' and r.yavru == 'TSKB': note += '; XBANK eklenince pc 0,05 -> çoğu banka faktörü'
    if r.ana == 'SAHOL' and r.yavru == 'AKBNK': note += '; XBANK kontrollü pc 0,147'
    if r.ana == 'KCHOL' and r.yavru == 'YKBNK': note += '; XBANK kontrollü pc 0,156'
    if r.grup == 'ZORLU': note += '; 29.06.2026 yapılandırma sonrası pc VESTL-VESBE 0,85, ZOREN-VESTL 0,67 (n=88): kredi riski ortak faktörü'
    if r.grup == 'KARDEMIR': note += '; pay grubu: aynı şirket'
    add(stock=st, driver_yahoo=S(dr), driver_desc=f'{dr} ({MECH.get(r.tur, r.tur)})', tv_ticker=f'BIST:{dr}', relation='sync', lag=0, corr_full=r.corr_full, corr_3y=r.corr_3y, corr_1y=r.corr_1y,
        pcorr_xu100=pc, beta=beta, t_stat=tb, is_oos=f'pc IS {r.pc_IS:.3f} / OOS {r.pc_OOS:.3f}', n=r.n, confidence=conf, mechanism=MECH.get(r.tur, r.tur), notes=note)
# ---- günlük öncülük (anlamlı olanlar)
for r in D.itertuples():
    for pre, x, y in [('Y2A_', r.yavru, r.ana), ('A2Y_', r.ana, r.yavru)]:
        for fam, rel in [('l1_intra', 'lead_intra'), ('l1_gap', 'lead_gap'), ('l1_cc', 'lead_multiday'), ('g2i', 'lead_auction')]:
            t = getattr(r, f'{pre}{fam}_t'); tIS = getattr(r, f'{pre}{fam}_t_IS'); tOOS = getattr(r, f'{pre}{fam}_t_OOS'); fdr = getattr(r, f'{pre}{fam}_fdr')
            if not (abs(t) >= 2.5 or fdr): continue
            same = (np.sign(tIS) == np.sign(tOOS)) if not np.isnan(tIS) else False
            if fam == 'g2i':
                conf = 'ORTA (istatistik) / ÇOK DÜŞÜK (işlem)' if (fdr and same) else 'DÜŞÜK'
                note = 'aynı gün: lider açılış gap ayrışması -> takipçi gün-içi (kendi gap + XU100 gap kontrollü). 10:30 TSİ girişte kazanç ~0 (res_bt2_check): ilk 30 dk içinde fiyatlanıyor; grup primi +0,42 t (pc ve likidite kontrollü, z=4,2)'
                lag = 0
            else:
                conf = 'ORTA' if (fdr and same and abs(tOOS) >= 2) else ('DÜŞÜK' if same else 'ÇOK DÜŞÜK')
                note = 'x_{t-1} -> y_t; y_{t-1} ve XU100_{t-1} kontrollü. 712 testte BH-FDR; plasebo 500 rastgele çiftte %|t|>2 = %4,4 (intra)'
                lag = 1
            st, dr = (y, x)
            add(stock=st, driver_yahoo=S(dr), driver_desc=f'{dr} -> {st} ({r.grup}, {MECH.get(r.tur, r.tur)})', tv_ticker=f'BIST:{dr}', relation=rel, lag=lag, pcorr_xu100=r.pc_full, t_stat=t,
                gap_corr=getattr(r, f'{pre}l1_gap_t') if fam != 'g2i' else '', intra_corr=getattr(r, f'{pre}l1_intra_t') if fam != 'g2i' else '', is_oos=f't IS {tIS:.2f} / OOS {tOOS:.2f}', n=getattr(r, f'{pre}{fam}_n') if fam != 'l1_cc' else getattr(r, f'{pre}l1_cc_n'),
                confidence=conf, mechanism=MECH.get(r.tur, r.tur), notes=note + f'; FDR={bool(fdr)}')
# ---- saatlik
Hh = pd.read_csv(HERE + '/res_hourly.csv'); Hh = Hh[(Hh.grup != 'PEER')]
for r in Hh.itertuples():
    if not (abs(r.h_t) >= 2.3 or r.fdr): continue
    same = np.sign(r.t_h1) == np.sign(r.t_h2)
    conf = 'ORTA (istatistik) / ÇOK DÜŞÜK (işlem)' if (r.fdr and same) else 'DÜŞÜK'
    add(stock=r.y, driver_yahoo=S(r.x), driver_desc=f'{r.x}_(h-1) -> {r.y}_h saatlik ({r.grup})', tv_ticker=f'BIST:{r.x}', relation='lead_hourly', lag='1 bar (60dk)', pcorr_xu100=r.h_pc0, beta=r.h_bstd, t_stat=r.h_t,
        is_oos=f'yarı1 t {r.t_h1:.2f} / yarı2 t {r.t_h2:.2f}', n=r.n_h, confidence=conf, mechanism='holding/küçük pay grubu bilgiyi gecikmeli fiyatlıyor',
        notes=f'2023-12..2026-10; kendi lag + XU100 lag kontrollü; likit barlarda t={r.h_t_liq:.2f}; 218 saatlik testte FDR={bool(r.fdr)}; grup %t>2=9,5 vs emsal 9,8 (fark yok). Saatlik backtest brüt 0-12 bps, 8 bps maliyetle negatif (res_hourly_bt)')
# ---- backtestler
B = pd.read_csv(HERE + '/res_bt.csv')
def btrow(bt, name, target, conf, mech, note, stock=None, driver=None, desc=None, rel='lead_multiday', lag='1+'):
    x = B[(B.bt == bt) & (B.name == name) & (B.target == target)]
    a, b = x[x.cost == 8].iloc[0], x[x.cost == 15].iloc[0]
    add(stock=stock or name.split('/')[0].split('->')[-1], driver_yahoo=driver or '', driver_desc=desc or f'{bt}: {name} {target}', tv_ticker='', relation=rel, lag=lag,
        t_stat=a.t_OOS, is_oos=f'IS {a.mean_IS:.1f} bps (t {a.t_IS:.2f}) / OOS {a.mean_OOS:.1f} bps (t {a.t_OOS:.2f}); 15bps OOS {b.mean_OOS:.1f}', bt_oos_sharpe=a.sh_OOS, bt_oos_mean_bps=a.mean_OOS, n=a.n_OOS,
        confidence=conf, mechanism=mech, notes=note + f'; yılların %{100*a.yrs_pos:.0f}ı pozitif')
btrow('BT1', 'KCHOL', 'H-bXU030 (kalici, z250>1)', 'ORTA', 'NAV iskontosu ortalamaya dönüş (iskonto açılınca KCHOL XU030a göre kazanıyor)', 'z250 kapanışta, t+1 açılış girişi, VİOP KCHOL + XU030 hedge; 12 pencere x eşik kombinasyonunda OOS t 1,7-3,7 hepsi pozitif (spread hedefinde 0,5-2,8); holdingin kendi göreli fiyat z-skoru (plasebo) OOS t≈0; ortak regresyonda NAV OOS t -3,1', stock='KCHOL', driver='NAV(TUPRS,FROTO,YKBNK,ARCLK,TOASO,...)', desc='KCHOL NAV iskontosu z250 -> KCHOL-b*XU030 kalıcı pozisyon')
btrow('BT1', 'SAHOL', 'spread H-bNAV (kalici, z250>1)', 'DÜŞÜK', 'NAV iskontosu ortalamaya dönüş', 'IS çok güçlü (t 5,0), OOS zayıf (t 0,9); 2021 sonrası etki azalmış', stock='SAHOL', driver='NAV(AKBNK,ENJSA,...)', desc='SAHOL NAV iskontosu z250 -> SAHOL-b*NAV')
btrow('BT1', 'AGHOL', 'spread H-bNAV (kalici, z250>1)', 'DÜŞÜK', 'NAV iskontosu ortalamaya dönüş', 'IS negatif, OOS +18 bps (t 1,8); AGHOL VİOPta yok; NAV ağırlıkları yaklaşık', stock='AGHOL', driver='NAV(AEFES,MGROS,ASUZU,ADEL)', desc='AGHOL NAV iskontosu z250 -> AGHOL-b*NAV')
btrow('BT1', 'TRENJ', 'spread H-bNAV (kalici, z250>1)', 'DÜŞÜK', 'zincir iştirak (TRENJ->TRMET) iskontosu', 'IS t 1,3 / OOS t 2,2; TRENJ VİOPta yok', stock='TRENJ', driver='TRMET.IS', desc='TRENJ/TRMET iskontosu z250')
btrow('BT2', 'AGHOL', 'NAVgap ayrisma -> H intra', 'ÇOK DÜŞÜK (işlem)', 'açılış ayrışması', 'açılış girişli IS +40 / OOS +48 bps; ama kazancın tamamı AGHOLün KENDİ gap fade bileşeninden (lider-yalnız OOS +4 bps) ve 10:30 girişte -3 bps', stock='AGHOL', driver='NAV gap', desc='AEFES/MGROS sepet gap ayrışması -> AGHOL gün-içi', rel='lead_auction', lag=0)
btrow('BT2', 'KCHOL', 'NAVgap ayrisma -> H intra', 'ÇOK DÜŞÜK (işlem)', 'açılış ayrışması (R1 bulgusu)', 'IS +25 / OOS +15 bps (t 1,0); 10:30 girişte -6,5 bps: R1 OOS zayıflaması teyit', stock='KCHOL', driver='NAV gap', desc='Koç iştirak sepeti gap ayrışması -> KCHOL gün-içi', rel='lead_auction', lag=0)
btrow('BT2', 'ISCTR', 'NAVgap ayrisma -> H intra', 'ÇOK DÜŞÜK', 'İş grubu iştirak sepeti', 'ham IS +1 / OOS -2 bps: ISCTR banka faktörüyle fiyatlanıyor, iştirak sepetini izlemiyor', stock='ISCTR', driver='SISE,ISMEN,ANHYT,ANSGR,TSKB...', desc='İş iştirak sepeti gap ayrışması -> ISCTR gün-içi', rel='lead_auction', lag=0)
btrow('BT2', 'DOHOL', 'NAVgap ayrisma -> H intra', 'ÇOK DÜŞÜK', 'DOHOL NAVının çoğu nakit/halka açık değil', 'yalnız GWIND; OOS +5 bps (t 0,3)', stock='DOHOL', driver='GWIND.IS', desc='GWIND gap ayrışması -> DOHOL gün-içi', rel='lead_auction', lag=0)
btrow('BT2b', 'KRDMD->KRDMB', 'takipci gun-ici', 'DÜŞÜK (işlem)', 'pay grubu: likit D -> illikit B', 'açılış girişli OOS +136 bps (t 6,2) ama 10:30 girişte lider-yalnız -6 bps; kalan kazanç KRDMB kendi gap fadei (illikit açılış seansı); spot, açığa satış zor, spread >15 bps olabilir', stock='KRDMB', driver='KRDMD.IS', desc='KRDMD açılış ayrışması -> KRDMB gün-içi', rel='lead_auction', lag=0)
btrow('BT2b', 'TUPRS->AYGAZ', 'takipci gun-ici', 'ÇOK DÜŞÜK (işlem)', 'Aygazın Tüpraş payı (EYAŞ üzerinden)', 'açılış girişli OOS +101 bps (t 4,3); 10:30 girişte lider-yalnız -20, birleşik -2 bps', stock='AYGAZ', driver='TUPRS.IS', desc='TUPRS gap -> AYGAZ gün-içi', rel='lead_auction', lag=0)
btrow('BT2b', 'SAHOL->ENJSA', 'takipci gun-ici', 'DÜŞÜK', 'ENJSA açılış gap fadei', '10:30 girişte birleşik +50 bps (t 2,2, n=88) — ama lider bileşen IS negatif; kendi gap fadei', stock='ENJSA', driver='SAHOL.IS', desc='SAHOL gap ayrışması -> ENJSA gün-içi', rel='lead_auction', lag=0)
btrow('BT3', 'SAHOL/AKBNK', 'oran z60 (kalici)', 'YÜKSEK', 'ana-iştirak oranı ortalamaya dönüş (AKBNK SAHOL NAVının ~%45i)', 'iki bacak da VİOPta; parametre seti (20-120 gün, eşik 1-2) IS t 2,5-4,3, OOS t 2,5-3,9; 13 yılın 12sinde pozitif; grup dışı 19 benzer çiftte ortalama OOS t 0,24; SAHOL/YKBNK OOS t 1,7, SAHOL/XBANK 1,96 -> kısmen SAHOL-banka faktörü', stock='SAHOL', driver='AKBNK.IS', desc='SAHOL/AKBNK log-oran z60 -> t+1 açılışta spread pozisyonu')
btrow('BT3', 'ANSGR/ANHYT', 'oran z250 (kalici)', 'DÜŞÜK', 'kardeş sigorta şirketleri: oran MOMENTUMU (MR kaybettiriyor)', 'MR işaretiyle IS t -3,2, OOS t -1,8 -> ters (trend takibi) sinyal; mekanizma belirsiz', stock='ANSGR', driver='ANHYT.IS', desc='ANSGR/ANHYT oran z250')
btrow('BT3', 'KRDMB/KRDMD', 'oran z60 (kalici)', 'ÇOK DÜŞÜK', 'pay grubu oranı', '2026da B/D 0,9->3,5->1,3 balon; kısa vadeli MR kaybettiriyor (OOS -24 bps)', stock='KRDMD', driver='KRDMB.IS', desc='KRDMB/KRDMD oran z60', rel='regime')
btrow('BT3', 'KRDMA/KRDMD', 'oran z60 (kalici)', 'ÇOK DÜŞÜK', 'pay grubu oranı', 'OOS +14 bps t 1,0, IS negatif', stock='KRDMD', driver='KRDMA.IS', desc='KRDMA/KRDMD oran z60', rel='regime')
btrow('BT3', 'ISCTR/SISE', 'oran z60 (kalici)', 'ÇOK DÜŞÜK', 'ana-iştirak oranı', 'IS ~0, OOS -7 bps', stock='ISCTR', driver='SISE.IS', desc='ISCTR/SISE oran z60')
btrow('BT3', 'AEFES/CCOLA', 'oran z250 (kalici)', 'DÜŞÜK', 'AEFES CCOLAnın %50,3ü', 'IS +15 (t 2,7), OOS +4 (t 0,5)', stock='AEFES', driver='CCOLA.IS', desc='AEFES/CCOLA oran z250')
btrow('BT4', 'TVF-sektor | XU100<-0.03', 't+1 cc (kapanis girisi, iyimser)', 'DÜŞÜK', 'devlet desteği (stres sonrası TVF hisselerine alım) hipotezi', 'n küçük (IS 24 / OOS 49 gün); 15 bps maliyette OOS +42 bps t~1,1; gün-içi versiyon t 0,96', stock='THYAO', driver='TVF sepeti', desc='XU100<-%3 günü -> ertesi gün TVF sepeti (THYAO,HALKB,TCELL,TTKOM,VAKBN) - sektör kontrol', rel='event')
# ---- TVF ortak faktör (senkron, olumsuz)
add(stock='THYAO', driver_yahoo='TVF sepeti', driver_desc='TVF ortak faktörü (THYAO,HALKB,TCELL,TTKOM,VAKBN): farklı sektör TVF-TVF çiftleri', tv_ticker='', relation='sync', lag=0, pcorr_xu100=-0.024,
    t_stat=0.90, is_oos='2017-20 b=-0,015; 2020-22 -0,015; 2022-24 +0,014; 2024-26 +0,033 (t 1,6)', n=1081, confidence='ÇOK DÜŞÜK', mechanism='ortak devlet sahipliği', notes='çift-düzeyi regresyon pc~aynı sektör+iki banka+ikisi TVF: ikisi-TVF katsayısı ≈0; DiD (TVFye katılım ±2 yıl) -0,10..+0,06; TVF ayrı bir faktör DEĞİL')
add(stock='TTKOM', driver_yahoo='TVF sepeti', driver_desc='TVF sepeti artığı_{t-1} -> TTKOM gün-içi', tv_ticker='', relation='lead_intra', lag=1, t_stat=2.33, n=1156, confidence='ÇOK DÜŞÜK', mechanism='ortak devlet sahipliği', notes='5 üyede test: THYAO -0,07, HALKB 1,74, TCELL 1,41, TTKOM 2,33, VAKBN 0,07 -> çoklu test sonrası anlamsız')
# ---- olaylar
Ev = pd.read_csv(HERE + '/res_events.csv')
for r in Ev.itertuples():
    if abs(r.t0) < 2 and abs(r.t_2_10) < 2: continue
    add(stock=r.sym, driver_yahoo='olay', driver_desc=f'{r.date}: {r.event}', tv_ticker=f'BIST:{r.sym}', relation='event', lag=0, t_stat=r.t0, is_oos=f'AR0 {r.AR0:.1f}%, CAR[0,1] {r.CAR_0_1:.1f}%, CAR[2,10] {r.CAR_2_10:.1f}% (t {r.t_2_10:.1f}), CAR[0,20] {r.CAR_0_20:.1f}%',
        n=1, confidence='DÜŞÜK (tek olay)', mechanism='ortaklık/kontrol değişikliği', notes='XU100 piyasa modeli artığı (log %); tek olay -> genelleme yok')
# ---- pay grubu primi (rejim)
add(stock='KRDMD', driver_yahoo='KRDMB.IS', driver_desc='KRDMB/KRDMD fiyat oranı (B grubu primi)', tv_ticker='BIST:KRDMB', relation='regime', lag='', corr_full=0.719, pcorr_xu100=0.576, n=4221, confidence='DÜŞÜK',
    mechanism='imtiyazlı pay grubu (YK seçimi) + illikidite spekülasyonu', notes='oran 2010-25 medyan ~1,0-1,1; 2026 Mart-Haz. 1,9->3,5 (B primi balonu), fon krizi sonrası Eki. 1,0-1,3. ADF p(2021+)=0,67: kısa vadede durağan değil. A/D 2025 Haz. 1,87 -> 0,89. Büyük sapmalar aylar içinde kapanıyor ama arada çok büyük ters hareket')
# ---- hipotezler / test edilemeyenler
for st, dr, desc, note in [('TKFEN', 'EREGL.IS/OYAKC.IS', 'OYAK-Tekfen yeni grup bağı (Tem.2026)', 'n=107 gün: TKFEN-EREGL pc -0,15, TKFEN-OYAKC 0,06; henüz ortak fiyatlama yok; devir sonrası TKFEN CAR[2,10] +34%'),
                           ('ISCTR', 'TİBAŞ Holding', 'İş Bankası iştiraklerini TİBAŞ Holdinge kısmi bölünme (2024 kararı)', 'tescil/uygulama tarihi doğrulanamadı; test edilmedi'),
                           ('BRSAN', 'BORLS.IS', 'Borusan-Borlease bağı', 'BORLS-BRSAN pc ≈0; Borlease Borusan Otomotiv bağlantısı doğrulanmadı'),
                           ('GLYHO', 'PASEU.IS', 'Global Yatırım-Pasifik Eurasia bağı', 'PASEUnun GLYHO iştiraki olduğu DOĞRULANAMADI (pc 0,05)'),
                           ('DOAS', 'Doğuş Holding', 'Doğuş grubu: BISTte başka likit iştirak yok (DOCO Doğuş değil, THY ile ortak girişim)', 'test edilemedi'),
                           ('GUBRF', 'BAGFS.IS', 'Gübretaş-Bagfaş: grup bağı yok (sektör emsali)', 'pc 0,24 senkron; öncülük yok'),
                           ('-', 'Kibar Holding', 'Kibar grubu: BISTte halka açık şirketi bulunamadı', 'test edilemedi')]:
    add(stock=st, driver_yahoo=dr, driver_desc=desc, relation='hypothesis', confidence='ÇOK DÜŞÜK / SPEKÜLATİF', notes=note)
f = pd.DataFrame(F)[cols]
for c in ['corr_full','corr_3y','corr_1y','pcorr_xu100','beta','t_stat','gap_corr','intra_corr','bt_oos_sharpe','bt_oos_mean_bps']:
    f[c] = pd.to_numeric(f[c], errors='coerce').round(4).astype(object).where(pd.to_numeric(f[c], errors='coerce').notna(), '')
f.to_csv(OUT + '/f_y_grup.csv', index=False)
print(len(f), f.relation.value_counts().to_dict(), f.confidence.value_counts().to_dict())
