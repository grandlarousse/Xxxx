"""rules.build öz-denetimi: nedensellik (kesik panel), determinizm, süre; dondurulmuş kuralların IS satırları (elib.eval_rule)."""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
from common import elib
import rules
P = elib.load(sys.argv[1])
t0 = time.time(); A = rules.build(P); dt = time.time() - t0
B = rules.build(P)
print(f'build süresi: {dt:.1f} sn; kural sayısı {len(A)}; birincil {sum(r["birincil"] for r in A)}')
print('deterministik:', all(a['sig'].equals(b['sig']) for a, b in zip(A, B)))
for cut in ['2021-06-30', '2022-06-30']:
    print(f'self_check_causal (kesim {cut}):', elib.self_check_causal(rules.build, P, cut=cut))
for r in A:
    for row in elib.eval_rule(r, P, family='A6'):
        print(f"{r['ad']:45s} {row['arac']:11s} h{row['h']} n_bag={row['n_bagimsiz_IS']:4d} fazla={row['ort_fazla_IS_bps']:7.1f} t={row['t_IS']:5.2f} "
              f"net_temel={row.get('net_temel_bps_IS', min(row.get('settle_net_temel_IS_bps', 0), row.get('last_net_temel_IS_bps', 0))):7.1f}")
