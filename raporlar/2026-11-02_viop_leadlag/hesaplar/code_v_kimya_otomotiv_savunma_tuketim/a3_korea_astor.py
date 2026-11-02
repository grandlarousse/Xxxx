"""A3 — O3: Kore şebeke hisseleri (267260.KS HD Hyundai Electric, 298040.KS Hyosung Heavy, 010120.KS LS Electric) aynı gün -> ASTOR gap/gün-içi.
Zamanlama: KRX kapanışı 06:30 UTC (15:30 KST), BIST sürekli işlem 07:00 UTC (10:00 TSİ), açılış seansı 06:40-06:55 UTC -> KR_t BIST açılışından ÖNCE bilinir.
KR_t penceresi [06:30 UTC t-1, 06:30 UTC t] -> BIST t-1 seansıyla ÇAKIŞIR; gap_t penceresi [15:10 t-1, 06:55 t]."""
import sys; sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_kimya_otomotiv_savunma_tuketim')
from vk import *
KR = ['267260.KS', '298040.KS', '010120.KS']
A = decomp('ASTOR'); M = decomp('XU100'); rA = ret('ASTOR')
KS = ret('^KS11'); SPX = ret('^GSPC'); ES = ret('ES=F'); NQ = ret('^NDX') if os.path.exists(f'{D}/daily/^NDX.parquet') else ret('^GSPC')
krb = basket(KR, 2)
S0 = '2023-02-01'
def show(lbl, x, y, ctrl=()):
    pc, t, n = pcorr(y, x, list(ctrl), S0, None); return f'{lbl}: {pc:.3f} (t {t:.1f}, n {n})'
print('=== O3 tekil + sepet ===')
for k in KR + ['KR_basket']:
    x = krb if k == 'KR_basket' else ret(k)
    print(k, '|', show('gap', x, A['gap']), '|', show('intra', x, A['intra']), '|', show('cc', x, A['cc']),
          '|', show('gap|KOSPI', x, A['gap'], [KS]), '|', show('gap|KOSPI+SPX_{t-1}+NDX_{t-1}', x, A['gap'], [KS, SPX.shift(1), NQ.shift(1)]),
          '|', show('gap|XU100gap', x, A['gap'], [M['gap']]), '|', show('gap|XU100gap+KOSPI+SPX_{t-1}', x, A['gap'], [M['gap'], KS, SPX.shift(1)]),
          '|', show('intra|XU100intra', x, A['intra'], [M['intra']]), '|', show('ters: ASTOR cc_{t-1} -> KR_t', A['cc'].shift(1), x, [KS]))
print('\n=== yarılar (sepet) ===')
for s, e in [(S0, '2024-12-15'), ('2024-12-16', None), ('2025-01-01', None)]:
    g = pcorr(A['gap'], krb, [], s, e); gc = pcorr(A['gap'], krb, [M['gap'], KS], s, e); i = pcorr(A['intra'], krb, [], s, e); ic = pcorr(A['intra'], krb, [M['intra']], s, e)
    print(f'{s}..{e}: gap {g[0]:.3f} (t {g[1]:.1f}, n {g[2]}) | gap|XU100gap+KOSPI {gc[0]:.3f} (t {gc[1]:.1f}) | intra {i[0]:.3f} (t {i[1]:.1f}) | intra|XU100intra {ic[0]:.3f} (t {ic[1]:.1f})')
print('\n=== yıllık (sepet) gap / intra corr ===')
for y in range(2023, 2027):
    g = pcorr(A['gap'], krb, [], f'{y}-01-01', f'{y}-12-31'); i = pcorr(A['intra'], krb, [], f'{y}-01-01', f'{y}-12-31')
    gc = pcorr(A['gap'], krb, [M['gap'], KS], f'{y}-01-01', f'{y}-12-31')
    print(y, f'gap {g[0]:.3f} (t {g[1]:.1f}) | gap|XU100gap+KOSPI {gc[0]:.3f} | intra {i[0]:.3f} (t {i[1]:.1f}) n {g[2]}')
print('\n=== plasebo: KR sepeti_t -> diğer VİOP hisselerinin gap_t (2023-02+) ===')
V47 = 'AEFES AKBNK AKSEN ALARK ARCLK ASELS ASTOR BIMAS BRSAN CIMSA DOAS DOHOL EKGYO ENJSA ENKAI EREGL FROTO GARAN GUBRF HALKB HEKTS ISCTR KCHOL KRDMD MGROS ODAS OYAKC PETKM PGSUS SAHOL SASA SISE SOKM TAVHL TCELL THYAO TKFEN TOASO TRALT TRMET TSKB TTKOM TUPRS ULKER VAKBN VESTL YKBNK'.split()
rows = []
for s in V47 + ['EUPWR', 'GESAN', 'XU100']:
    try:
        d = decomp(s)
        g = pcorr(d['gap'], krb, [], S0, None); gc = pcorr(d['gap'], krb, [M['gap'], KS], S0, None) if s != 'XU100' else (np.nan, np.nan, 0)
        gk = pcorr(d['gap'], KS, [], S0, None)
        rows.append(dict(sym=s, gap_corr=g[0], gap_t=g[1], gap_pc_ctrl=gc[0], gap_pc_ctrl_t=gc[1], gap_corr_KOSPI=gk[0]))
    except Exception as ex: print(s, ex)
PL = pd.DataFrame(rows).sort_values('gap_corr', ascending=False); PL.to_csv(f'{OUT}/res/a3_placebo.csv', index=False)
print(PL.head(12).round(3).to_string(index=False)); print('...'); print('medyan gap_corr', round(PL.gap_corr.median(), 3), '| ASTOR sırası', list(PL.sym).index('ASTOR') + 1, '/', len(PL))
print('kontrollü (XU100 gap + KOSPI) pc sırası:'); PL2 = PL.sort_values('gap_pc_ctrl', ascending=False); print(PL2.head(8).round(3).to_string(index=False)); print('ASTOR kontrollü sırası', list(PL2.sym).index('ASTOR') + 1)
print('\n=== işlenebilirlik: sign(KR_t) -> ASTOR intra_t (açılışta gir, kapanışta çık) ===')
for c in (0, 8, 15):
    for s, e in [(S0, '2024-12-15'), ('2024-12-16', None)]:
        n, m, t, sh = bt_sign(krb, A['intra'], c, 0, s, e); n2, m2, t2, sh2 = bt_sign(krb, A['intra'], c, krb.std(), s, e)
        print(f'cost {c}: {s}..{e} hepsi n {n} ort {m:.1f} bps t {t:.2f} Sh {sh:.2f} | |KR|>1sd n {n2} ort {m2:.1f} t {t2:.2f}')
# Saatlik: ASTOR açılış saati vs geri kalan (2023-12+)
h = pd.read_parquet(f'{D}/h1/ASTOR.IS.parquet'); h.index = h.index.tz_convert(None)
h['day'] = h.index.normalize()
first = h[(h.index.hour == 6) & (h.index.minute == 30)].set_index('day')
dd = raw('ASTOR')[['o', 'c']].copy(); dd.index = dd.index.normalize()
fh = np.log(first['c'] / dd['o'].reindex(first.index))  # açılış -> 07:30 UTC
rest = np.log(dd['c'].reindex(first.index) / first['c'])
fh = fh.reindex(cal()); rest = rest.reindex(cal())
p1 = pcorr(fh, krb, [], '2023-12-01', None); p2 = pcorr(rest, krb, [], '2023-12-01', None)
print(f'\nh1: KR_t -> ASTOR ilk saat (açılış->10:30 TSİ) {p1[0]:.3f} (t {p1[1]:.1f}, n {p1[2]}) | geri kalan (10:30->kapanış) {p2[0]:.3f} (t {p2[1]:.1f})')
