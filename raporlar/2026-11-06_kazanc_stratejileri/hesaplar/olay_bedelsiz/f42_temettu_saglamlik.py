"""Yuksek verimli temettu 'duyuru -> hak-1' etkisi icin hizli saglamlik: yil, verim esigi, giris gecikmesi (t0, t0+1, t0+5),
cikis (hak-1, hak-3), kilit bilgisi olan hisseler, alternatif kiyas (XUTUM/XYUZO), buyukluk (HisseTekil piyasa degeri olanlar)."""
import numpy as np, pandas as pd
import f20_es as E
from f31_calistir import md, P2, T, I, H as HP
M = E.matrisler(); cal = M["cal"]
tm = pd.read_pickle(f"{E.CACHE}/olaylar_temettu.pkl"); tm = tm[(tm.hak >= "2015-01-01") & (tm.verim > 0) & (tm.verim < 0.5) & tm.p1.notna()]
alt = {ix: pd.read_parquet(f"{E.CACHE}/px_chart/{ix}.parquet").px.reindex(cal).pct_change() for ix in ["XUTUM", "XYUZO"]}
xu = (1 + M["rm"].fillna(0)).cumprod()
rec = []
for _, e in tm.iterrows():
    k = e.kod
    if k not in M["R"].columns: continue
    jh = E.day_idx(cal, e.hak); jp = E.t0_idx(cal, e.p1)
    if jh is None or jp is None or jp >= jh - 1: continue
    r = M["R"][k]; g = r.iloc[jp:jh]
    if g.isna().any(): continue
    vd = e.verim * float(np.prod(1 + g))
    pdv = M["PD"][k].iloc[jp - 1] if k in M["PD"].columns else np.nan
    for gec in [0, 1, 5]:
        for cik in [1, 3]:
            ji, jo = jp + gec, jh - cik
            if jo <= ji: continue
            jg, _ = E.dolabilir_giris(M, k, ji, 5)
            if jg is None or jg >= jo: continue
            ham, x = E.bhar(M, k, jg, jo)
            if pd.isna(ham): continue
            row = dict(kod=k, yil=e.hak.year, vd=vd, gec=gec, cik=cik, giris=cal[jg], bhar=ham - x, ham=ham, kilit=k in M["VWR"].columns,
                       pdrel=np.log(pdv / xu.iloc[jp - 1]) if pd.notna(pdv) and pdv > 0 else np.nan)
            for ix, s in alt.items(): row["bhar_" + ix] = ham - (float(np.prod(1 + s.iloc[jg + 1:jo + 1])) - 1)
            rec.append(row)
D = pd.DataFrame(rec); D["donem"] = np.where(D.yil >= 2024, "2024-26", "2015-23")
def oz(g, col="bhar"):
    z = E.ozet(g[col], g.giris); return dict(N=z["N"], ort=z["ort"], med=z["med"], t=z["t"], isabet=z["isabet"])
s = "# Temettu saglamlik (otomatik)\n"
rows = []
for thr in [0.03, 0.05, 0.08]:
    for gec in [0, 1, 5]:
        for cik in [1, 3]:
            g = D[(D.vd >= thr) & (D.gec == gec) & (D.cik == cik)]
            for per in ["tum", "2024-26"]:
                gg = g if per == "tum" else g[g.donem == "2024-26"]
                rows.append(dict(esik=f">={thr:.0%}", giris=f"t0+{gec}", cikis=f"hak-{cik}", donem=per) | oz(gg))
S = pd.DataFrame(rows); F = dict(N=I, ort=P2, med=P2, t=T, isabet=HP)
s += "\n## Esik x giris gecikmesi x cikis\n\n" + md(S, ["esik", "giris", "cikis", "donem", "N", "ort", "med", "t", "isabet"], F)
b = D[(D.vd >= 0.05) & (D.gec == 0) & (D.cik == 1)]
Y = pd.DataFrame([dict(yil=y) | oz(g) for y, g in b.groupby("yil")])
s += "\n## Yil (verim>=%5, t0 -> hak-1)\n\n" + md(Y, ["yil", "N", "ort", "med", "t", "isabet"], F)
rows = [dict(alt="kilit bilgisi olan (HisseTekil)") | oz(b[b.kilit]), dict(alt="ChartData-only") | oz(b[~b.kilit])]
for ix in ["XUTUM", "XYUZO"]: rows.append(dict(alt=f"kiyas {ix}") | oz(b, "bhar_" + ix))
q = b.pdrel.quantile([1/3, 2/3]).values
for nm, m in [("kucuk", b.pdrel <= q[0]), ("orta", (b.pdrel > q[0]) & (b.pdrel <= q[1])), ("buyuk", b.pdrel > q[1])]: rows.append(dict(alt=f"boyut {nm}") | oz(b[m]))
s += "\n## Alt kume / kiyas (verim>=%5, t0 -> hak-1)\n\n" + md(pd.DataFrame(rows), ["alt", "N", "ort", "med", "t", "isabet"], F)
open(f"{E.CACHE}/sonuc/temettu_saglamlik.md", "w").write(s); print(s)
