"""A5 — S4: Yeniden silahlanma haber günleri (n=6) ASELS AR0. Olay listesi out/code_savunma/events.csv'den (type=='rearm') VERİ olarak okunur.
AR = r - b*XU100 (b: önceki 250 işlem günü, olay penceresi hariç). Temizlenmemiş (ham adj) getiri. Ek: rastgele gün plasebo, bölüm (episode) birleştirme,
gap/gün-içi ayrımı (haber BIST seansında mı, önce mi?), EU savunma sepeti AR0, OTKAR (yurt içi savunma) karşılaştırması."""
import sys; sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_kimya_otomotiv_savunma_tuketim')
from vk import *
ev = pd.read_csv('/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_savunma/events.csv')
C = cal()
def rawret(s):
    d = raw(s); p = d['adj'][d['adj'] > 0]
    if not is_bist_index(s): p = p[d['v'].reindex(p.index).fillna(0) > 0]
    return np.log(p).diff().reindex(C)
A = rawret('ASELS'); M = rawret('XU100'); O = rawret('OTKAR')
dA = raw('ASELS'); intra = np.log(dA['c'] / dA['o']).reindex(C); gap = A - intra
EU_DEF = ['RHM.DE', 'BA.L', 'LDO.MI', 'HO.PA', 'SAAB-B.ST', 'KOG.OL', 'HAG.DE', 'R3NK.DE']; EUD = basket(EU_DEF, 3); STX = ret('^STOXX')
beta = (A.rolling(250, min_periods=150).cov(M) / M.rolling(250, min_periods=150).var()).shift(5)
betaO = (O.rolling(250, min_periods=150).cov(M) / M.rolling(250, min_periods=150).var()).shift(5)
AR = A - beta * M; ARO = O - betaO * M
ARg = gap - beta * (M - (np.log(raw('XU100')['c'] / raw('XU100')['o']).reindex(C)))  # kaba gap AR
bE = (EUD.rolling(250, min_periods=120).cov(STX) / STX.rolling(250, min_periods=120).var()).shift(5); ARE = EUD - bE * STX
rows = []
for _, e in ev.iterrows():
    d = pd.Timestamp(e.bist_day0)
    if d not in C: continue
    p = C.get_loc(d)
    rows.append(dict(date=d.date(), type=e.type, ev=e.event[:45], A_r0=A.iloc[p], XU=M.iloc[p], AR0=AR.iloc[p], AR1=AR.iloc[p + 1] if p + 1 < len(C) else np.nan,
                     CAR05=AR.iloc[p:p + 6].sum(), gap0=gap.iloc[p], intra0=intra.iloc[p], OTKAR_AR0=ARO.iloc[p], EU_AR0=ARE.iloc[p], EU_ARm1=ARE.iloc[p - 1]))
T = pd.DataFrame(rows); pd.set_option('display.width', 250)
print((T.set_index(['date', 'type', 'ev']) * 1e4).round(0).to_string())
for ty in ['rearm', 'war', 'peace']:
    z = T[T.type == ty]
    if len(z) < 2: continue
    m = z.AR0.mean(); t = m / (z.AR0.std() / np.sqrt(len(z)))
    print(f'\n{ty}: n {len(z)} ort AR0 {m*1e4:.0f} bps t {t:.2f} medyan {z.AR0.median()*1e4:.0f} | işaret + oranı {(z.AR0>0).mean():.2f} | CAR0-5 ort {z.CAR05.mean()*1e4:.0f} | gap0 ort {z.gap0.mean()*1e4:.0f}, intra0 ort {z.intra0.mean()*1e4:.0f} | OTKAR AR0 ort {z.OTKAR_AR0.mean()*1e4:.0f} | EU_DEF AR0 ort {z.EU_AR0.mean()*1e4:.0f}')
z = T[T.type == 'rearm'].copy()
# Bölüm birleştirme: 2025-03-03/04/05 tek bölüm (3 günlük CAR), diğerleri tekil
z['ep'] = np.where(pd.to_datetime(z.date).between('2025-03-03', '2025-03-05'), '2025-03-03..05', z.date.astype(str))
epi = z.groupby('ep').AR0.sum(); print('\nbölüm bazında (ardışık günler toplanmış) AR:', (epi * 1e4).round(0).to_dict(), '| n', len(epi), 'ort', round(epi.mean() * 1e4), 'bps t', round(epi.mean() / (epi.std() / np.sqrt(len(epi))), 2))
# Plasebo: 2022+ rastgele 6 gün ortalamasının dağılımı (AR0)
pool = AR[(AR.index >= '2022-01-01')].dropna()
rng = np.random.default_rng(42); sims = np.array([pool.sample(6, random_state=int(s)).mean() for s in rng.integers(0, 1e9, 20000)])
obs = z.AR0.mean(); print(f'plasebo (2022+ rastgele 6 gün, 20k): P(ort >= {obs*1e4:.0f} bps) = {(sims >= obs).mean():.4f}; günlük AR sd {pool.std()*1e4:.0f} bps; |AR|>300 bps gün oranı {(pool.abs()>0.03).mean():.3f}')
# EU_DEF büyük günleri ile ASELS AR0 ilişkisi (veri güdümlü, seçim yanlılığı yok): EU_DEF AR z>2
zE = ARE / ARE.rolling(250, min_periods=120).std().shift(1)
for lab, msk in [('EU_DEF AR z>+2', zE > 2), ('EU_DEF AR z<-2', zE < -2)]:
    for s, e in [('2014-01-01', '2021-12-31'), ('2022-01-01', None)]:
        x = AR[msk & (AR.index >= s) & ((AR.index <= e) if e else True)].dropna()
        print(f'{lab} {s[:4]}-{(e or "2026")[:4]}: n {len(x)} ASELS AR0 ort {x.mean()*1e4:.0f} bps t {x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan:.2f}')
T.to_csv(f'{OUT}/res/a5_events.csv', index=False)
