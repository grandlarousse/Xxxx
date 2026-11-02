"""(b) büyük TUR hareketleri (z>2): ENKAI'ye özgü mü, piyasa geneli mi? XU030 (endeks vadelisi, 3 bps), hedge'li ENKAI, 47 hisse ortalaması.
Ayrıca ENKAI gap'inin bu günlerde ne yaptığı (aşırı tepki mi, eksik tepki mi)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vlib as V, numpy as np, pandas as pd
pd.set_option('display.width', 250)
VIOP = ["AEFES","AKBNK","AKSEN","ALARK","ARCLK","ASELS","ASTOR","BIMAS","BRSAN","CIMSA","DOAS","DOHOL","EKGYO","ENJSA","ENKAI","EREGL","FROTO","GARAN","GUBRF","HALKB","HEKTS","ISCTR","KCHOL","KRDMD","MGROS","ODAS","OYAKC","PETKM","PGSUS","SAHOL","SASA","SISE","SOKM","TAVHL","TCELL","THYAO","TKFEN","TOASO","TRALT","TRMET","TSKB","TTKOM","TUPRS","ULKER","VAKBN","VESTL","YKBNK"]
E = V.decomp('ENKAI'); X30 = V.decomp('XU030'); TUR, _ = V.us_prev('TUR'); USD = V.fx_prev('TRY=X')
import importlib.util
spec = importlib.util.spec_from_file_location('bt5', os.path.join(V.CODE, '05_bt.py'))
def hedged(y, win=250):
    df = pd.concat([y.rename('y'), X30['intra'].rename('x')], axis=1).dropna()
    cov = df['y'].rolling(win, min_periods=120).cov(df['x']).shift(1); var = df['x'].rolling(win, min_periods=120).var().shift(1)
    return (df['y'] - (cov / var).clip(0, 2) * df['x']).reindex(y.index)
for thr in [1.0, 2.0]:
    p = V.zpos(-TUR, thr)
    print(f'--- -TUR z>{thr} ---')
    for lab, tgt, c in [('ENKAI intra (8 bps)', E['intra'], 8), ('ENKAI hedge XU030 (11 bps)', hedged(E['intra']), 11), ('XU030 intra (3 bps)', X30['intra'], 3)]:
        o, _ = V.bt(p, tgt, c); print(f'  {lab:28s} ' + V.fmt_bt(o)); print(f'  {"":28s} yıllar {o["by_year"]}')
    # 47 hisse: her hisse için OOS ve IS ortalama getiri (maliyetsiz)
    res = []
    for s in VIOP:
        try: d = V.decomp(s)
        except Exception: continue
        o, _ = V.bt(p, d['intra'], 0)
        res.append({'stock': s, 'IS': o['IS'].get('mean_bps', np.nan), 'OOS': o['OOS'].get('mean_bps', np.nan), 'tIS': o['IS'].get('t', np.nan), 'tOOS': o['OOS'].get('t', np.nan)})
    R = pd.DataFrame(res).set_index('stock')
    print(f'  47 hisse (maliyetsiz) ortalama: IS {R.IS.mean():+.1f} bps (pozitif {int((R.IS > 0).sum())}/{len(R)}), OOS {R.OOS.mean():+.1f} (pozitif {int((R.OOS > 0).sum())}/{len(R)}); ENKAI IS {R.loc["ENKAI","IS"]:+.1f} OOS {R.loc["ENKAI","OOS"]:+.1f}; ENKAI OOS sırası {int((R.OOS > R.loc["ENKAI","OOS"]).sum()) + 1}')
    print('  OOS en yüksek 8:', R.OOS.sort_values(ascending=False).head(8).round(1).to_dict())
# bu günlerde ENKAI gap ve intra (aşırı mı eksik mi tepki?)
z = V.zpos(-TUR, 2.0)
d = pd.concat([TUR.rename('TUR'), USD.rename('USD'), E['gap'].rename('Egap'), E['intra'].rename('Eintra'), X30['gap'].rename('Xgap'), X30['intra'].rename('Xintra'), z.rename('pos')], axis=1).dropna()
d = d[d.pos != 0]
print('\n z>2 günlerinde (pos=+1: TUR çok düştü; -1: TUR çok yükseldi) ortalamalar (bps):')
print((1e4 * d.groupby('pos')[['TUR', 'USD', 'Egap', 'Eintra', 'Xgap', 'Xintra']].mean()).round(0).to_string())
print(d.groupby('pos').size().to_dict())
