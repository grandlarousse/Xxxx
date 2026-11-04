"""Betiği kendi veri akışıyla çalıştırıp S'yi yazar (karşılaştırma için; bağımsız koddan ayrı süreç)."""
import sys, time, pandas as pd
sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/rehber/koza')
import sinyal_koza as K
D = {}
for s in K.SYMS:
    D[s], _ = K.fetch(s); time.sleep(0.3)
R = pd.DataFrame({s: K.spot_ret(D[s], s) for s in K.SYMS})
S = K.signal(R, 'TRMET')
S.to_parquet('/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/denetim_koza/betik_sig.parquet')
print(S.tail(3))
