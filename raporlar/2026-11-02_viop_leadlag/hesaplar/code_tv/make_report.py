"""tv_map.csv + candidates.json -> out/r1_tv.md (kurallar tablosu ve öncelikli liste otomatik doldurulur)."""
import csv, json, os, collections
D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(D, '..')
m = list(csv.DictReader(open(os.path.join(OUT, 'tv_map.csv'), encoding='utf8')))
cand = json.load(open(os.path.join(D, 'candidates.json'), encoding='utf8'))
by = {r['yahoo']: r for r in m if r['yahoo']}
extra = {r['name']: r for r in m if not r['yahoo']}
ex_of = {c['yahoo']: c['exch'] for c in cand}
st = collections.Counter(r['status'] for r in m)

def row(y):
    r = by.get(y)
    if not r: return f'| {y} | (katalogda yok) | | | |'
    return f"| {y} | `{r['tv_best']}` | {(' / '.join('`'+a.strip()+'`' for a in r['tv_alt'].split('|') if a.strip())) or '—'} | {r['status']} | {r['notes'].split(';')[0][:90]} |"
def xrow(name):
    r = extra.get(name)
    if not r: return ''
    return f"| — | `{r['tv_best']}` | {(' / '.join('`'+a.strip()+'`' for a in r['tv_alt'].split('|') if a.strip())) or '—'} | {r['status']} | {name} |"

# Kural tablosu
EX = collections.OrderedDict()
for r in m:
    y = r['yahoo']
    if not y: continue
    e = ex_of.get(y, '')
    pre = r['tv_best'].split(':')[0] if r['tv_best'] else '(kod yok)'
    k = (e, pre)
    d = EX.setdefault(k, {'n': 0, 'v': 0, 'u': 0, 'c': 0, 'ex': y + ' → ' + r['tv_best']})
    d['n'] += 1
    d['v'] += r['status'] == 'VERIFIED_PAGE'; d['u'] += r['status'] == 'UNCERTAIN'; d['c'] += r['status'] == 'CONVENTION'
rules = sorted(EX.items(), key=lambda kv: -kv[1]['n'])

L = []
A = L.append
A('# r1_tv — Yahoo → TradingView ticker eşlemesi (ajan: tv)')
A('Tarih: 01.11.2026. Çıktı: `out/tv_map.csv` (yahoo,name,tv_best,tv_alt,status,evidence_url,notes). Kod: `out/code_tv/`.')
A('')
A('## 1. Net bulgular')
A(f"- **{len(m)} satır** ({len(by)} katalog sembolü + {len(extra)} ek satır: VİOP vadelileri, TR tahvil faizleri, CFD'ler vb.). Durum dağılımı: " + ', '.join(f'{k}={v}' for k, v in st.most_common()) + '.')
A('- VERIFIED_PAGE = halka açık `tradingview.com/symbols/EXCH-SYM/` sayfası **bu oturumda okundu** ve sayfadaki `symbolInfo` (resolved_symbol, açıklama, ISIN) kaydedildi; hisse/ETF\'lerde Yahoo adı ile TV açıklaması karşılaştırıldı (uyuşmazlık → UNCERTAIN).')
A('- **VİOP TradingView\'da VAR** (BIST öneki, 15 dk gecikmeli ücretsiz): endeks vadelisi `BIST:XU030D1!` (kök `XU030D`, D = vadeli), pay vadelisi `BIST:THYAO1!` (kök = hisse kodu), döviz `BIST:USDTRY1!`, altın `BIST:XAUTRY1!`. `BIST:XU0301!`, `BIST:F_XU0301!`, `BIST:F_THYAO1!`, `BIST:THYAOD1!` **YOK** (404).')
A('- Önek tuzakları (sayfa ile doğrulandı): NYSE Arca ETF\'leri **AMEX:** (AMEX:EEM, AMEX:FXI, AMEX:GDX); Nasdaq\'ta işlem gören iShares\'ler **NASDAQ:** (NASDAQ:TUR, NASDAQ:EMB, NASDAQ:EUFN, NASDAQ:MCHI); Cboe BZX\'e taşınan iShares\'ler **CBOE:** (CBOE:ITA; AMEX:ITA/BATS:ITA yazılınca CBOE:ITA\'ya çözülüyor). LSE\'de 2 harfli kodlar nokta ile biter (LSE:BA., LSE:QQ., LSE:BP., LSE:NG.). İskandinav B/A hisseleri alt çizgi (OMXSTO:SAAB_B, OMXCOP:CARL_B, OMXHEX:NDA_FI).')
A('- **Ticker çakışmaları**: LSE:IAG (IAG havayolu) ≠ NYSE:IAG (IAMGOLD); NYSE:B = Barrick (yeni kod), NYSE:GOLD = Gold.com (Barrick DEĞİL); NYSE:HEI = HEICO ≠ XETR:HEI (Heidelberg Materials); NYSE:TS = Tenaris; NYSE:SMA = SmartStop; NYSE:STC = Stewart Information (Yahoo grubu "tel" yanlış etiketli olabilir).')
A('- **Türkiye CDS TradingView\'da bulunamadı** (denenen adaylar 404; arama sonucu yok) → alternatif vekil: `TVC:TR10Y`, `TVC:TR02Y`, `OTC:AKBTY`/`NYSE:TKC` spread, `NASDAQ:TUR`, `NASDAQ:EMB`.')
A('- Çin borsaları için kod verilmedi (CHINA_BLOCKED); ABD ETF alternatifleri sayfa ile doğrulandı (AMEX:ASHR, CBOE:CNYA, AMEX:FXI, NASDAQ:MCHI, AMEX:KWEB). HKEX: semboller TV\'de mevcut ama kullanıcıda açılmayabilir → her HK satırına ADR/OTC alternatifi eklendi.')
A('')
A('## 2. Yöntem')
A('- Yalnızca **halka açık sembol sayfaları** düz GET ile okundu (curl varsayılan UA; Origin/Referer taklidi YOK, iç API/websocket YOK), ~1 istek/sn, en fazla 2 sıralı işçi. Kod: `code_tv/tvpage.py`, `run_verify.py`, `finalize.py`; ham sonuçlar `code_tv/cache*.jsonl`.')
A('- Kanıt mantığı: HTTP 200 + `symbolInfo` → sembol var; 404 → yok. Bazı sayfalar (FX, SP:SPX, XAUTRY) 301 ile kanonik `/symbols/SYM/` sayfasına yönleniyor; bu **yalnızca sembol mevcutsa** oluyor (kontrol: `FX-NOTREAL`, `OANDA-XAUTRY`, `FX-XAUTRY` → 404; `FX_IDC-XAUTRY`, `SAXO-XAUTRY` → 301). Bu durumda talep edilen kod geçerli kabul edildi, notta kanonik sayfanın gösterdiği kod yazıldı.')
A('- Talep edilen kod başka bir koda çözülüyorsa (ör. AMEX:ITA → CBOE:ITA) **tv_best = çözülen kod**.')
A('- WebSearch: VİOP kodu (`BIST-XU030D1!` arama sonucu), TradingView veri kapsamı sayfası (https://www.tradingview.com/data-coverage/).')
A('')
A('## 3. Kurallar tablosu (Yahoo borsası → TradingView öneki)')
A('| Yahoo exch | TV öneki | n | sayfa ile doğrulanan | UNCERTAIN | yalnız kural | örnek |')
A('|---|---|---|---|---|---|---|')
for (e, pre), d in rules:
    A(f"| {e} | {pre} | {d['n']} | {d['v']} | {d['u']} | {d['c']} | {d['ex']} |")
A('')
A('Ek kurallar: ABD sınıf hisseleri `-` → `.` (BRK-B → NYSE:BRK.B); Stockholm/Helsinki/Kopenhag `-` → `_`; LSE 2 harf → sonuna `.`; HKEX baştaki sıfırlar atılır (0700.HK → HKEX:700); BMV seri harfi `/` ile (GFNORTEO.MX → BMV:GFNORTE/O, BIMBOA.MX → BMV:BIMBO/A, ALPEKA.MX → BMV:ALPEK/A; `BMV:ALPEKA` 404); Toronto `-` → `.` (HPS-A.TO → TSX:HPS.A, kural); Kore/Tayvan/Japonya/Suudi sayısal kod aynen (KRX:005930, TSE:7203, TADAWUL:2222); vadeli = `KÖK1!` (ön ay sürekli), `KÖK2!` ikinci ay; vade kodu = KÖK+ay harfi+yıl (BIST:XU030DZ2026 = Aralık 2026).')
A('')
A('## 4. VİOP — TradingView durumu')
A('| VİOP sözleşmesi | TradingView kodu | durum |')
A('|---|---|---|')
for name in ['VİOP BIST30 endeks vadeli (sürekli)', 'VİOP Likit Banka endeks vadeli', 'VİOP Banka Dışı Likit 10 vadeli', 'VİOP BIST Sürdürülebilirlik 25 vadeli',
             'VİOP USDTRY vadeli (sürekli)', 'VİOP EURTRY vadeli', 'VİOP Altın (TL/gram) vadeli', 'VİOP Gram gümüş vadeli', 'VİOP BIST30 Aralık 2026 kontratı (örnek vade kodu)']:
    r = extra.get(name)
    if r: A(f"| {name} | `{r['tv_best']}` | {r['status']} |")
viop = [c for c in cand if c['group'] == 'VIOP']
ok_f, no_f = [], []
cache = {}
for cf in ('cache.jsonl', 'cache_b.jsonl', 'cache_manual.jsonl'):
    p = os.path.join(D, cf)
    if os.path.exists(p):
        for l in open(p, encoding='utf8'):
            try:
                x = json.loads(l); cache[x['tv']] = x
            except Exception: pass
for c in viop:
    f = f"BIST:{c['yahoo'].split('.')[0]}1!"
    x = cache.get(f)
    (ok_f if x and x.get('http') == '200' else no_f).append(f)
A('')
A(f"**Pay vadelileri:** 47 VİOP dayanağından {len(ok_f)} tanesinin `BIST:<KOD>1!` sürekli kontrat sayfası okundu (VERIFIED_PAGE)" + (f"; bulunamayan/okunamayan: {', '.join(no_f)}" if no_f else '; hepsi mevcut') + '. Kodlar tv_map.csv\'de ilgili hissenin `tv_alt` sütununda.')
A('- Not: VİOP verisi ücretsiz kullanıcıya **15 dk gecikmeli**; gerçek zamanlı "Borsa Istanbul futures/options" paketi ücretli. Pay vadelilerinde hacim düşük olduğundan sürekli kontrat grafiği boşluklu/bayat olabilir; roll günlerinde (vade sonu) baz farkı kadar sıçrama olur.')
A('- Akşam seansı: VİOP akşam seansı barlarının TradingView\'da görünüp görünmediği bu çalışmada doğrulanmadı (sayfa seans bilgisi vermiyor) — UNCERTAIN.')
A('')
A('## 5. Öncelikli liste (görev 2–3) — seçilen kodlar')
A('| Yahoo | tv_best | tv_alt | durum | not |')
A('|---|---|---|---|---|')
P = '''XU100.IS XU030.IS XBANK.IS XUSIN.IS XHOLD.IS XLBNK.IS ^GSPC ^NDX ^DJI ^RUT ^SOX ^GDAXI ^STOXX50E ^STOXX ^FTSE ^FCHI ^IBEX FTSEMIB.MI ^N225 ^KS11 ^HSI ^BVSP DX-Y.NYB ^VIX ^MOVE ^TNX
ES=F NQ=F YM=F BZ=F CL=F HO=F RB=F NG=F TTF=F MTF=F GC=F SI=F PL=F PA=F HG=F ALI=F TIO=F HRC=F ZW=F ZC=F ZS=F KC=F CC=F SB=F CT=F ZN=F
TRY=X EURTRY=X EURUSD=X CNH=X CNY=X ZAR=X MXN=X BRL=X HUF=X PLN=X JPY=X BTC-USD
TUR EEM EMB JETS ITA GDX GDXJ SLX XME FXI ASHR MCHI KWEB EUFN KBE CRAK KRBN GRID URA TKC AKBTY TKGBY BBVA'''.split()
for y in P: A(row(y))
for name in ['Türkiye 10Y tahvil faizi', 'Türkiye 2Y tahvil faizi', 'Türkiye 5Y tahvil faizi', 'ABD 2Y tahvil faizi', 'Türkiye 5Y CDS (TradingView aday)', 'Ons altın TL (XAUTRY)',
             'Brent CFD', 'WTI CFD', 'Altın CFD', 'Gümüş CFD', 'SGX demir cevheri 62% (FEF)', 'CME Bitcoin vadeli', 'ICE Rotterdam kömür (API2)', 'Avrupa karbon (EUA) vadeli', 'CBOE VIX vadeli']:
    A(xrow(name))
A('')
A('Sektör emsalleri (görev 3):')
A('')
A('| Yahoo | tv_best | tv_alt | durum | not |')
A('|---|---|---|---|---|')
P3 = '''RHM.DE LDO.MI BA.L SAAB-B.ST KOG.OL HO.PA HAG.DE R3NK.DE BBVA.MC LHA.DE AF.PA IAG.L RYAAY RYA.IR WIZZ.L ADP.PA FRA.DE AENA.MC VLO PKN.WA MOL.BD MOH.AT ELPE.AT MT MT.AS
TKA.DE SZG.DE VOE.VI VALE TS NEM SSRM EGO CF NTR YAR.OL F STLA STLAM.MI RNO.PA VOW3.DE WHR ELUX-B.ST 066570.KS 034220.KS 267260.KS 298040.KS 010120.KS 012450.KS
064350.KS 079550.KS ENR.DE GEV SGO.PA OI HEI.DE HOLN.SW CX LYB BAS.DE 051910.KS IVL.BK ALPEKA.MX RELIANCE.NS 2010.SR 3402.T KO CCH.L HEIA.AS ABI.BR'''.split()
for y in P3: A(row(y))
A('')

A('## 6. Çin ve Hong Kong')
A('- SSE:/SZSE:/SHFE:/DCE:/ZCE:/CFFEX:/INE:/GFEX: için **kod verilmedi** (status=CHINA_BLOCKED). TradingView\'da doğrulanmış alternatifler: `AMEX:ASHR` (CSI 300), `CBOE:CNYA` (MSCI China A), `AMEX:FXI`, `NASDAQ:MCHI`, `AMEX:KWEB`, `SGX:CN1!` (FTSE China A50 vadeli, SGX — Çin borsası değil), `FX:USDCNH` (offshore yuan), `FX_IDC:USDCNY`. Çin emtiaları yerine: demir cevheri `SGX:FEF1!` / `COMEX:TIO1!`, çelik `COMEX:HRC1!`, bakır `COMEX:HG1!` / `LME:CA1!` (LME gün sonu). Hangi alternatifin veride en iyi temsil ettiğini cin ajanı test ediyor.')
A('- HKEX: hisse sayfaları TV\'de mevcut (ör. `HKEX:700`, `HKEX:9988`) ama **kullanıcıda açılmayabilir** → her HK satırına ADR/OTC alternatifi (`OTC:TCEHY`, `NYSE:BABA`, `OTC:BYDDY`, `OTC:XIACY` …) konuldu. Hang Seng endeksi için HKEX\'e bağlı olmayan `TVC:HSI` (TradingView kendi akışı) önerilir; `HSI:HSCEI` (H-share endeksi) Hang Seng Indexes kaynaklı, açılması belirsiz; alternatif `AMEX:FXI`. `HKEX:HSI1!` vadelisi HKEX verisi (muhtemelen açılmaz).')
A('')
A('## 7. Ücretli / gecikmeli veri akışları (kaynak: https://www.tradingview.com/data-coverage/ , 01.11.2026 okundu; fiyatlar değişebilir)')
A('| Akış | Ücretsiz | Gerçek zamanlı |')
A('|---|---|---|')
for a_, b_, c_ in [('BIST hisse/endeks', '15 dk gecikmeli', 'ücretli (~8 $/ay non-pro)'), ('BIST vadeli/opsiyon (VİOP)', '15 dk gecikmeli', 'ücretli (~7 $/ay)'),
                   ('CME/CBOT/COMEX/NYMEX (ES1!, CL1!, GC1!, ZW1! …)', '10 dk gecikmeli', 'CME paketi ücretli (~7 $/ay non-pro)'),
                   ('ICE US (KC1!, CC1!, SB1!, CT1!, DX1!)', '10 dk gecikmeli', 'pahalı (~139 $/ay)'), ('ICE Europe (BRN1!, ATW1!) / ICE Endex (TFM1!, ECF1!)', '10 dk gecikmeli', 'pahalı (~130–152 $/ay)'),
                   ('SGX vadeli (FEF1!, CN1!)', '10 dk gecikmeli', 'pahalı (~132 $/ay)'), ('LME (CA1!)', 'gün sonu', 'ücretli'),
                   ('NYSE/NASDAQ/AMEX hisse-ETF', 'Cboe One ile sınırlı gerçek zamanlı', 'tam akış ücretli (düşük)'), ('Cboe endeksleri (VIX, OVX, GVZ)', '15 dk gecikmeli', 'ücretli'),
                   ('S&P (SP:SPX) / Dow Jones (DJ:DJI)', '10 dk gecikmeli', 'ücretli'), ('Avrupa borsaları (XETR, EURONEXT, LSE, SIX, MIL, BME, Nordic, OSL, VIE, GPW, BET, ATHEX)', '15 dk gecikmeli', 'ücretli'),
                   ('TSE, KRX, ASX, BMV', '20 dk gecikmeli', 'ücretli'), ('TVC: (UKOIL, USOIL, GOLD, DXY, US10Y, TR10Y, UKX, SX5E, NI225, HSI)', 'ücretsiz (TradingView türetilmiş/CFD)', '—'),
                   ('FX:, FX_IDC:, OANDA:, SAXO:, BITSTAMP:', 'ücretsiz', '—')]:
    A(f'| {a_} | {b_} | {c_} |')
A('')
A('Pratik: gün-içi/canlı izleme için ücretsiz ve gecikmesiz olanlar TVC:/FX: CFD\'leridir (TVC:UKOIL, TVC:GOLD, TVC:DXY, FX:USDTRY). Vadeli kontrat (1!) ile CFD arasında baz/vade farkı olur; backtest\'te kullanılan Yahoo serisi vadeli ise grafikte de 1! kullanmak daha tutarlıdır.')
A('')
A('## 8. FX günlük bar kapanışı (koordinatör notu)')
A('- Doğrulanan: `FX:USDTRY` sayfasındaki `symbolInfo.timezone = America/New_York` (FXCM akışı). BIST sembolleri `Europe/Istanbul`.')
A('- Doğrulanamayan (yalnız topluluk/forum kaynakları): TV FX günlük barı 17:00 New York\'ta kapanır (= 21:00 UTC yaz / 22:00 UTC kış). Yani TV\'deki FX:USDTRY günlük kapanışı BIST kapanışından (15:00 UTC) ~6–7 saat sonra; Yahoo `TRY=X` günlük barı ile birebir aynı olmayabilir. Kullanıcı BIST kapanışı anındaki kuru görmek isterse 1 saatlik grafikte 15:00 UTC (18:00 TSİ) barına bakmalı. Durum: UNCERTAIN (seans dosyası halka açık sayfada yok).')
A('')
A('## 9. Tuzaklar ve sınırlamalar')
A('- Katalogda isim/grup uyuşmazlıkları (TV açıklamasıyla teyitli): `NYSE:SMA` = SmartStop Self Storage (SMA Solar değil → `XETR:S92`), `NYSE:STC` = Stewart Information (Saudi Telecom değil → `TADAWUL:7010`), `NYSE:EDF` = Virtus Stone Harbor EM fonu (Électricité de France değil), `NYSE:GOLD` = Gold.com (Barrick = `NYSE:B`), `NYSE:IAG` = IAMGOLD (IAG havayolu = `LSE:IAG` / `BME:IAG`), `NYSE:HEI` = HEICO (Heidelberg = `XETR:HEI`). `ICEEUR:G1!` = UK Short Gilt (gasoil değil).')
A('- `MOEX:ROSN` sayfası `RUS:ROSN`\'a yönleniyor; Rusya verisi yaptırımlar nedeniyle bayat/sınırlı olabilir. `OTC:TYIDY` (Toyota Industries ADR) ve `TSE:5202` (Nippon Sheet Glass) 404 — muhtemelen delist/özelleştirme; UNCERTAIN.')
A('- `COMEX:BUS1!` (busheling hurda) ve `BIST:XAGTRY1!` 404 → UNCERTAIN. Türkiye CDS: TradingView\'da bulunamadı.')
A('- Doğrulama tarihi 01–02.11.2026; semboller zamanla değişebilir (ör. kod değişikliği KOZAL→TRALT, KOZAA→TRMET; ikisi de BIST\'te doğrulandı). Sayfa varlığı, kullanıcının hesabında verinin açılacağını garanti etmez (bölgesel/lisans kısıtları). Mekanik kuralla eşlenip sayfası okunamayan satırlar CONVENTION olarak işaretli.')
A('- Yöntem dışı bırakılanlar: TradingView iç API\'leri/websocket ve başlık sahteciliği kullanılmadı; seans saatleri ve akşam seansı kapsamı bu nedenle doğrulanamadı.')
open(os.path.join(OUT, 'r1_tv.md'), 'w', encoding='utf8').write('\n'.join(L) + '\n')

print('ok', len(L))
