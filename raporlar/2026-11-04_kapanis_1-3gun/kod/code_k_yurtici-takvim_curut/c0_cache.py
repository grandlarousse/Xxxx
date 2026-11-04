"""Önbellek: VİOP47 + XU030 için tüm günlerde ileri getiri (E0/E1/E2, h=1,2,3,5) ve spot getiriler; limit kilidi bayrakları."""
from curlib import *
L = pd.read_csv(S + '/out/y_viop_likidite.csv')
UNDS = list(L.und)
cal = vcal()
rows = {}
for u in UNDS:
    try:
        F = fut(u)
    except Exception as e:
        print('yok', u, e); continue
    for h in [1, 2, 3, 5]:
        for e in ['E0', 'E1', 'E2']:
            rows[(u, h, e)] = F.fwd(cal, h, e)
    # sinyal günü ön vade uzlaşmasının limitte olup olmadığı (dolum kısıtı)
    fs, jj = F.front_series('settle', min_dte=0)
    r = pd.Series(np.nan, index=cal)
    ok = jj.values >= 0
    rr = F.R.values[np.arange(len(cal))[ok], jj.values[ok]]
    r[ok] = rr
    rows[(u, 0, 'r_front')] = r.values
    print(u, end=' ', flush=True)
FW = pd.DataFrame({f'{u}|{h}|{e}': v for (u, h, e), v in rows.items()}, index=cal)
FW.to_parquet(RES + '/_fwd_cache.parquet')
# spot getiriler
SR = {}
for u in UNDS + ['XU100']:
    try: SR[u] = spot_ret(u)
    except Exception as e: print('spot yok', u, e)
SR = pd.DataFrame(SR)
SR.to_parquet(RES + '/_spot_ret.parquet')
print('\nbitti', FW.shape, SR.shape)
