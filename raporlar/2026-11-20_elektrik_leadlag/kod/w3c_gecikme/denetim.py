"""W3-C öz-denetim: nedensellik (kesik panel = tam panel), deterministiklik, build süresi.
Kullanım: python3 -I denetim.py <panel_dev>"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'ortak'))
sys.path.insert(0, HERE)
import elib  # noqa: E402
import rules  # noqa: E402

P = elib.load(sys.argv[1])
t0 = time.time()
r1 = rules.build(P)
dt = time.time() - t0
r2 = rules.build(P)
print(f'build(): {len(r1)} dondurulmuş kural, {dt:.2f} sn; deterministik: {all(a["sig"].equals(b["sig"]) for a, b in zip(r1, r2))}')
for cut in ('2021-06-30', '2022-06-30', '2024-06-28'):
    print(f'self_check_causal(build, kesim {cut}):', elib.self_check_causal(rules.build, P, cut))
    print(f'self_check_causal(build_tarama, kesim {cut}):', elib.self_check_causal(rules.build_tarama, P, cut))
