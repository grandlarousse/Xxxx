"""SAHOL'ün kendi göreli MR'ı mı? SAHOL vs XU030/XU100/XBANK/XHOLD ve AKBNK vs XBANK; aynı kural."""
import sys; sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_YR1_a')
from vlib import *
import importlib; r3 = importlib.import_module('03_ratio_alt') if False else None
exec(open(HERE + '/03_ratio_alt.py').read().split("if __name__ == '__main__':")[0])
rows = []
for A, B in [('SAHOL', 'AKBNK'), ('SAHOL', 'XU030'), ('SAHOL', 'XU100'), ('SAHOL', 'XBANK'), ('SAHOL', 'XLBNK'), ('SAHOL', 'XHOLD'), ('AKBNK', 'XBANK'), ('AKBNK', 'XU030'), ('KCHOL', 'TUPRS'), ('KCHOL', 'YKBNK'), ('AGHOL', 'AEFES'), ('SAHOL', 'ENJSA')]:
    try:
        P = pair(A, B)
        if P['S'].dropna().shape[0] < 500: raise ValueError('kısa')
        for w, thr in [(60, 1.5), (40, 1.5), (120, 1.5)]:
            o, _, _ = run(P, w, thr); rows.append(dict(pair=f'{A}/{B}', w=w, thr=thr, **o))
    except Exception as e: rows.append(dict(pair=f'{A}/{B}', err=str(e)[:60]))
pd.set_option('display.width', 250)
print(pd.DataFrame(rows).round(2).to_string())
