"""Fiyata bağlı maliyet: bacak gidiş-dönüş = taban (komisyon+yarım spread) + 1 tik/fiyat. VİOP tik 0,01 TL varsayımı (spot tik daha geniş olabilir).
Ayrıca yıllık ortalama tik/fiyat (bps)."""
import vb, numpy as np, pandas as pd, warnings, importlib.util
warnings.filterwarnings('ignore')
spec = importlib.util.spec_from_file_location('f7', '07_fut.py'); f7 = importlib.util.module_from_spec(spec); spec.loader.exec_module(f7)
P = vb.pair_inputs('SAHOL', 'AKBNK'); A, B, beta = P['A'], P['B'], P['beta']; z = vb.zscore(P['S'], 60); pos = vb.positions(z, 1.5)
tA = 1e4 * 0.01 / A['c']; tB = 1e4 * 0.01 / B['c']
print('yıllık ort. tik/fiyat bps: SAHOL', tA.groupby(tA.index.year).mean().round(1).loc[2014:].to_dict()); print('                      AKBNK', tB.groupby(tB.index.year).mean().round(1).loc[2014:].to_dict())
def pnl_var(base):
    Pg = pos.shift(2).fillna(0); Pi = pos.shift(1).fillna(0); bi = beta.shift(1)
    sg = A['gap'] - bi * B['gap']; si = A['intra'] - bi * B['intra']
    gross = Pg * sg.fillna(0) + Pi * si.fillna(0)
    cA = (base + tA.shift(1)) / 1e4; cB = (base + tB.shift(1)) / 1e4
    cost = (cA / 2 + bi.abs() * cB / 2) * (Pi - Pg).abs()
    return pd.DataFrame({'net': gross - cost, 'exp': (Pg != 0) | (Pi != 0), 'valid': sg.notna() | si.notna(), 'Pi': Pi, 'Pg': Pg})
for base in [6, 15]:
    print(f'spot, taban {base} + 1 tik:'); print(vb.table(pnl_var(base))[['bps', 't']].round(2).T.to_string())
# vadeli (açılış dolumu, devirli) taban 6 + tik
FA, FB = f7.cont('SAHOL'), f7.cont('AKBNK')
for base in [6, 15]:
    rows = {}
    for lab, lo, hi in f7.PER:
        # maliyeti günlük değişken yapmak için bt'yi iki kez çağırmak yerine: sabit maliyet = dönem ort. (taban + tik)
        m = (A.index >= lo) & (A.index < hi); c_eff = base + 0.5 * (tA[m].mean() + tB[m].mean())
        d = f7.bt(pos, beta, FA, FB, 'X_open', c_eff, True); s = vb.summ(d, lo, hi); rows[lab] = (round(c_eff, 1), round(s['bps'], 1), round(s['t'], 2))
    print(f'vadeli açılış dolumu, taban {base}+tik (efektif maliyet, bps/gün, t):', rows)
