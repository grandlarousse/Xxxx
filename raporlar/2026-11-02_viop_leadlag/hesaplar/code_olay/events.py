"""Olay tarih listeleri -> out/olay_tarihleri.csv
Kolonlar: date (olay günü, yerel), type, sub, dir (+1 olumlu/şahin.., -1, 0), time_utc (yaklaşık), timing
(in_session / after_close / pre_open / weekend / night), react_date (BIST'in ilk tepki günü; hesapla doldurulur),
source, verified (TCMB/FED/BLS-web, web-haber, hafiza-kural), note
"""
import os, sys, pandas as pd, numpy as np
SC = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad'
sys.path.insert(0, SC + '/code'); import ll
rows = []
def add(d, typ, sub, dr, tutc, timing, src, ver, note=''):
    rows.append(dict(date=pd.Timestamp(d), type=typ, sub=sub, dir=dr, time_utc=tutc, timing=timing, source=src, verified=ver, note=note))

# ---------------- TCMB PPK (politika faizi DEĞİŞİKLİKLERİ; tcmb.gov.tr 1 hafta repo tablosu, yürürlük tarihi-1 iş günü = karar günü)
ppk_chg = [  # karar günü, yeni faiz, önceki faiz
 ('2014-01-28',10.0,4.5,'olağanüstü PPK; gece ~22:00 UTC açıklandı -> 29 Ocak gap'),('2014-05-22',9.5,10.0,''),('2014-06-24',8.75,9.5,''),('2014-07-17',8.25,8.75,''),
 ('2015-01-20',7.75,8.25,''),('2015-02-24',7.5,7.75,''),('2016-11-24',8.0,7.5,''),
 ('2018-05-28',16.5,8.0,'sadeleştirme duyurusu (23 Mayıs olağanüstü GLP artışının ardından); yürürlük 1 Haziran'),('2018-06-07',17.75,16.5,''),('2018-09-13',24.0,17.75,''),
 ('2019-07-25',19.75,24.0,'Çetinkaya görevden alındıktan sonra ilk karar'),('2019-09-12',16.5,19.75,''),('2019-10-24',14.0,16.5,''),('2019-12-12',12.0,14.0,''),
 ('2020-01-16',11.25,12.0,''),('2020-02-19',10.75,11.25,''),('2020-03-17',9.75,10.75,'olağanüstü'),('2020-04-22',8.75,9.75,''),('2020-05-21',8.25,8.75,''),
 ('2020-09-24',10.25,8.25,''),('2020-11-19',15.0,10.25,'Ağbal ilk karar'),('2020-12-24',17.0,15.0,''),('2021-03-18',19.0,17.0,'2 gün sonra Ağbal görevden alındı'),
 ('2021-09-23',18.0,19.0,''),('2021-10-21',16.0,18.0,''),('2021-11-18',15.0,16.0,''),('2021-12-16',14.0,15.0,''),
 ('2022-08-18',13.0,14.0,''),('2022-09-22',12.0,13.0,''),('2022-10-20',10.5,12.0,''),('2022-11-24',9.0,10.5,''),('2023-02-23',8.5,9.0,''),
 ('2023-06-22',15.0,8.5,''),('2023-07-20',17.5,15.0,''),('2023-08-24',25.0,17.5,''),('2023-09-21',30.0,25.0,''),('2023-10-26',35.0,30.0,''),
 ('2023-11-23',40.0,35.0,''),('2023-12-21',42.5,40.0,''),('2024-01-25',45.0,42.5,''),('2024-03-21',50.0,45.0,''),('2024-12-26',47.5,50.0,''),
 ('2025-01-23',45.0,47.5,''),('2025-03-06',42.5,45.0,''),('2025-04-17',46.0,42.5,''),('2025-07-24',43.0,46.0,''),('2025-09-11',40.5,43.0,''),
 ('2025-10-23',39.5,40.5,''),('2025-12-11',38.0,39.5,''),('2026-01-22',37.0,38.0,''),('2026-10-22',36.0,37.0,'beklenti 100bp (CNBC-e anketi)')]
# Sürpriz yönü (sadece 2023-06 sonrası; haber anket medyanlarına göre HAFIZA -> 'hafiza' etiketi; +1 = şahin sürpriz, -1 = güvercin sürpriz, 0 = beklentiye uygun)
surp = {'2023-06-22':-1,'2023-07-20':-1,'2023-08-24':1,'2023-09-21':0,'2023-10-26':0,'2023-11-23':1,'2023-12-21':0,'2024-01-25':0,'2024-03-21':1,
        '2024-12-26':-1,'2025-01-23':0,'2025-03-06':0,'2025-04-17':1,'2025-07-24':-1,'2025-09-11':-1,'2025-10-23':1,'2025-12-11':0,'2026-10-22':0}
for d, new, old, note in ppk_chg:
    tim = 'night' if d == '2014-01-28' else 'in_session'
    add(d, 'PPK', 'hike' if new > old else 'cut', int(np.sign(new - old)), '22:00' if d=='2014-01-28' else '11:00', tim,
        'tcmb.gov.tr 1 hafta repo tablosu', 'web-TCMB', f'{old}->{new}. ' + note)
# Sabit (hold) kararları 2023-06 sonrası (toplantı takvimi: haber/TCMB; hafıza+web)
holds = ['2024-02-22','2024-04-25','2024-05-23','2024-06-27','2024-07-23','2024-08-20','2024-09-19','2024-10-17','2024-11-21',
         '2025-06-19','2026-03-12','2026-04-22','2026-06-11','2026-07-23','2026-09-10']
for d in holds: add(d, 'PPK', 'hold', 0, '11:00', 'in_session', 'haber (cnbce/qnbinvest 2026), hafıza 2024-25', 'web-haber/hafiza')
add('2025-03-20', 'PPK', 'extra_hawk', 1, '?', 'in_session', 'haber', 'hafiza', 'İmamoğlu şoku sonrası olağanüstü PPK: ON borç verme %46')
add('2018-05-23', 'PPK', 'extra_hawk', 1, '13:00', 'in_session', 'haber', 'hafiza', 'olağanüstü: GLP 13.5->16.5')
for r in rows:
    if r['type']=='PPK':
        k = r['date'].strftime('%Y-%m-%d')
        if k in surp: r['sub2'] = surp[k]
        elif r['sub']=='hold' and r['date']>=pd.Timestamp('2024-01-01'): r['sub2'] = 0  # sabit beklentiye uygun (hafıza; 2026 Mar/Tem web: 'beklentilere paralel')

# ---------------- FOMC (federalreserve.gov fomccalendars 2021-26 web; 2014-20 hafıza)
fomc = """2014-01-29 2014-03-19 2014-04-30 2014-06-18 2014-07-30 2014-09-17 2014-10-29 2014-12-17
2015-01-28 2015-03-18 2015-04-29 2015-06-17 2015-07-29 2015-09-17 2015-10-28 2015-12-16
2016-01-27 2016-03-16 2016-04-27 2016-06-15 2016-07-27 2016-09-21 2016-11-02 2016-12-14
2017-02-01 2017-03-15 2017-05-03 2017-06-14 2017-07-26 2017-09-20 2017-11-01 2017-12-13
2018-01-31 2018-03-21 2018-05-02 2018-06-13 2018-08-01 2018-09-26 2018-11-08 2018-12-19
2019-01-30 2019-03-20 2019-05-01 2019-06-19 2019-07-31 2019-09-18 2019-10-30 2019-12-11
2020-01-29 2020-04-29 2020-06-10 2020-07-29 2020-09-16 2020-11-05 2020-12-16
2021-01-27 2021-03-17 2021-04-28 2021-06-16 2021-07-28 2021-09-22 2021-11-03 2021-12-15
2022-01-26 2022-03-16 2022-05-04 2022-06-15 2022-07-27 2022-09-21 2022-11-02 2022-12-14
2023-02-01 2023-03-22 2023-05-03 2023-06-14 2023-07-26 2023-09-20 2023-11-01 2023-12-13
2024-01-31 2024-03-20 2024-05-01 2024-06-12 2024-07-31 2024-09-18 2024-11-07 2024-12-18
2025-01-29 2025-03-19 2025-05-07 2025-06-18 2025-07-30 2025-09-17 2025-10-29 2025-12-10
2026-01-28 2026-03-18 2026-04-29 2026-06-17 2026-07-29 2026-09-16 2026-10-28 2026-12-09""".split()
for d in fomc:
    D = pd.Timestamp(d)
    if D > pd.Timestamp('2026-10-30'): continue
    edt = D.month in (4,5,6,7,8,9,10) or (D.month==3 and D.day>=14) or (D.month==11 and D.day<=6)
    add(d, 'FOMC', 'scheduled', 0, '18:00' if edt else '19:00', 'after_close', 'federalreserve.gov' if D.year>=2021 else 'hafıza', 'web-FED' if D.year>=2021 else 'hafiza')
add('2020-03-03', 'FOMC', 'unscheduled', -1, '15:00', 'in_session', 'hafıza', 'hafiza', 'acil 50bp indirim, 10:00 ET')
add('2020-03-15', 'FOMC', 'unscheduled', -1, '21:00', 'weekend', 'hafıza', 'hafiza', 'Pazar acil 100bp indirim')

# ---------------- Kredi notu (not DEĞİŞİKLİKLERİ + önemli görünüm/izleme; countryeconomy.com + hafıza). Saat: genelde Cuma ~20-21 UTC (BIST kapanışı sonrası)
ratings = [
 ('2014-02-07','SP','outlook',-1,'görünüm negatif'),('2014-04-11','MOODYS','outlook',-1,'görünüm negatif'),
 ('2016-07-18','MOODYS','review',-1,'darbe sonrası izleme (Pzt)'),('2016-07-20','SP','downgrade',-1,'BB+->BB (Çar, darbe sonrası)'),
 ('2016-08-19','FITCH','outlook',-1,'görünüm negatif'),('2016-09-23','MOODYS','downgrade',-1,'Baa3->Ba1 (yatırım yapılabilir seviye kaybı)'),
 ('2017-01-27','FITCH','downgrade',-1,'BBB-->BB+ (son IG not kaybı)'),('2017-03-17','MOODYS','outlook',-1,'görünüm negatif'),
 ('2018-03-07','MOODYS','downgrade',-1,'Ba1->Ba2 (Çar gece)'),('2018-05-01','SP','downgrade',-1,'BB->BB- (Salı gece)'),
 ('2018-06-01','MOODYS','review',-1,'izlemeye alındı'),('2018-07-13','FITCH','downgrade',-1,'BB+->BB'),
 ('2018-08-17','SP','downgrade',-1,'BB-->B+'),('2018-08-17','MOODYS','downgrade',-1,'Ba2->Ba3 (aynı Cuma)'),
 ('2019-06-14','MOODYS','downgrade',-1,'Ba3->B1'),('2019-07-12','FITCH','downgrade',-1,'BB->BB-'),
 ('2020-08-21','FITCH','outlook',-1,'görünüm negatif'),('2020-09-11','MOODYS','downgrade',-1,'B1->B2'),
 ('2022-07-08','FITCH','downgrade',-1,'BB-->B'),('2022-08-12','MOODYS','downgrade',-1,'B2->B3'),('2022-09-30','SP','downgrade',-1,'B+->B'),
 ('2023-03-31','SP','outlook',-1,'görünüm negatif'),('2023-09-08','FITCH','outlook',1,'görünüm durağan'),('2023-09-29','SP','outlook',1,'görünüm durağan'),
 ('2023-11-30','SP','outlook',1,'görünüm pozitif'),('2024-01-12','MOODYS','outlook',1,'görünüm pozitif'),
 ('2024-03-08','FITCH','upgrade',1,'B->B+'),('2024-05-03','SP','upgrade',1,'B->B+'),('2024-07-19','MOODYS','upgrade',1,'B3->B1 (2 kademe)'),
 ('2024-09-06','FITCH','upgrade',1,'B+->BB-'),('2024-11-01','SP','upgrade',1,'B+->BB-'),('2025-07-25','MOODYS','upgrade',1,'B1->Ba3'),
 ('2026-01-23','FITCH','outlook',1,'görünüm pozitif (ntv haberi)'),
]
for d, ag, sub, dr, note in ratings:
    D = pd.Timestamp(d); tim = 'after_close'
    add(d, 'RATING', f'{ag}_{sub}', dr, '~20:30', tim, 'countryeconomy.com + hafıza/haber', 'web-kismi/hafiza', note)

# ---------------- ABD TÜFE ve İstihdam (8:30 ET = 12:30 UTC yaz / 13:30 UTC kış). BLS web yalnız gelecek tarihleri veriyor -> geçmiş: hafıza + kural (doğrulanmalı)
nfp = """2023-12-08 2024-01-05 2024-02-02 2024-03-08 2024-04-05 2024-05-03 2024-06-07 2024-07-05 2024-08-02 2024-09-06 2024-10-04 2024-11-01 2024-12-06
2025-01-10 2025-02-07 2025-03-07 2025-04-04 2025-05-02 2025-06-06 2025-07-03 2025-08-01 2025-09-05 2025-11-20 2025-12-16
2026-01-09 2026-02-11 2026-03-06 2026-04-03 2026-05-08 2026-06-05 2026-07-02 2026-08-07 2026-09-04 2026-10-02""".split()
cpi = """2023-12-12 2024-01-11 2024-02-13 2024-03-12 2024-04-10 2024-05-15 2024-06-12 2024-07-11 2024-08-14 2024-09-11 2024-10-10 2024-11-13 2024-12-11
2025-01-15 2025-02-12 2025-03-12 2025-04-10 2025-05-13 2025-06-11 2025-07-15 2025-08-12 2025-09-11 2025-10-24 2025-12-18
2026-01-13 2026-02-13 2026-03-11 2026-04-10 2026-05-12 2026-06-10 2026-07-14 2026-08-12 2026-09-11 2026-10-14""".split()
def us_t(D):
    # ABD yaz saati: Mart 2. Pazar - Kasım 1. Pazar
    y = D.year; m2 = pd.Timestamp(y,3,1); dst_s = m2 + pd.Timedelta(days=(6-m2.weekday())%7 + 7)
    n1 = pd.Timestamp(y,11,1); dst_e = n1 + pd.Timedelta(days=(6-n1.weekday())%7)
    return '12:30' if dst_s <= D < dst_e else '13:30'
for lst, sub in [(nfp,'NFP'),(cpi,'CPI')]:
    for d in lst:
        D = pd.Timestamp(d)
        add(d, 'USDATA', sub, 0, us_t(D), 'in_session', 'hafıza + BLS kuralı (2025 kapanma gecikmeleri dahil)', 'hafiza', 'doğrulanmalı (BLS arşiv)')

# ---------------- Türkiye TÜFE (TÜİK, ayın 3'ü 10:00 TSİ = 07:00 UTC; hafta sonu/tatil -> sonraki iş günü). Kural tabanlı.
cal = ll.bist_cal()
for y in range(2014, 2027):
    for m in range(1, 13):
        D = pd.Timestamp(y, m, 3)
        if D > pd.Timestamp('2026-10-30'): break
        nxt = cal[cal >= D]
        if len(nxt) == 0: continue
        add(nxt[0].strftime('%Y-%m-%d'), 'TUFE', 'release', 0, '07:00', 'at_open', 'TÜİK kuralı (3ü 10:00 TSİ)', 'kural', 'BIST açılış seansı 09:40-10:00 -> açılış fiyatı veri ÖNCESİ; tepki gün-içi ilk dakikalarda')

# ---------------- Siyasi / jeopolitik şoklar (dir: piyasa için ilk tepki yönü beklentisi; tarih = olayın kendisi)
pol = [
 ('2014-03-30','local_election',1,'weekend','yerel seçim'),('2015-06-07','general_election',-1,'weekend','AKP çoğunluğu kaybetti'),
 ('2015-11-01','general_election',1,'weekend','AKP çoğunluğu geri aldı'),('2016-05-05','political',-1,'in_session','Davutoğlu istifası'),
 ('2016-07-15','coup',-1,'weekend','darbe girişimi (Cuma gece)'),('2017-04-16','referendum',1,'weekend','anayasa referandumu'),
 ('2018-05-23','fx_crisis',-1,'in_session','kur şoku + olağanüstü PPK'),('2018-06-24','general_election',1,'weekend','cumhurbaşkanlığı seçimi'),
 ('2018-08-10','fx_crisis',-1,'in_session','Brunson/tarife, TL çöküşü (Cuma)'),('2019-03-31','local_election',-1,'weekend','yerel seçim'),
 ('2019-05-06','political',-1,'night','YSK İstanbul seçimini iptal (Pzt akşam)'),('2019-06-23','local_election',1,'weekend','İstanbul yenileme'),
 ('2019-07-06','cb_governor',-1,'weekend','Çetinkaya görevden alındı (Cmt)'),('2020-11-07','cb_governor',1,'weekend','Uysal görevden, Ağbal atandı; 8 Kas Albayrak istifası'),
 ('2021-03-20','cb_governor',-1,'weekend','Ağbal görevden alındı (Cmt)'),('2021-11-23','fx_crisis',-1,'in_session','TL çöküşü (ekonomik kurtuluş savaşı söylemi)'),
 ('2021-12-20','policy',1,'night','KKM açıklaması (Pzt ~18:30 UTC)'),('2022-02-24','geopolitics',-1,'pre_open','Rusya Ukrayna işgali'),
 ('2023-02-06','earthquake',-1,'pre_open','Kahramanmaraş depremleri (01:17 UTC)'),('2023-05-14','general_election',-1,'weekend','seçim 1. tur'),
 ('2023-05-28','general_election',-1,'weekend','2. tur'),('2023-06-03','policy',1,'weekend','Şimşek Hazine ve Maliye Bakanı'),
 ('2024-03-31','local_election',-1,'weekend','yerel seçim (muhalefet kazandı)'),('2025-03-19','political',-1,'pre_open','İmamoğlu gözaltısı (sabah, seans öncesi)'),
 ('2026-09-16','fund_crisis',-1,'in_session','fon krizi: BIST100 -%5,5, devre kesici 13:04 UTC'),('2026-09-17','fund_crisis',-1,'pre_open','SPK 131 fon tasfiye kararı, FİK 05:00 UTC'),
]
for d, sub, dr, tim, note in pol:
    add(d, 'POLITICAL', sub, dr, '', tim, 'hafıza + web (fon krizi: kureansiklopedi/hukukcularevi/turkiyetoday)', 'hafiza/web', note)

ev = pd.DataFrame(rows)
# BIST ilk tepki günü: in_session/at_open/pre_open -> aynı gün (BIST açıksa) ; after_close/night/weekend -> sonraki BIST günü
def react(r):
    D = r['date']
    if r['timing'] in ('in_session', 'at_open', 'pre_open'):
        c = cal[cal >= D]
    else:
        c = cal[cal > D]
    return c[0] if len(c) else pd.NaT
ev['react_date'] = ev.apply(react, axis=1)
ev = ev.sort_values(['date', 'type']).reset_index(drop=True)
ev.to_csv(SC + '/out/olay_tarihleri.csv', index=False, date_format='%Y-%m-%d')
print(ev.groupby('type').size().to_dict())
