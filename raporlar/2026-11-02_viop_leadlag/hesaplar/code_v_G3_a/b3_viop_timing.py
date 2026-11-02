"""B3: VİOP bülteni ACILIS / KAPANIS fiyatlarının SAATİNİ ES=F saatlik ile doğrula (2024-06+).
ES fiyatı p(t) = t saatinde başlayan h1 barının açılışı (UTC). Pencereler (T-1 akşamı -> T sabahı):
 w1 15:00->16:00 (BIST kapanışı -> VİOP akşam seansı başlangıcı 19:00 TSİ)
 w2 16:00->20:00 (akşam seansı 19:00-23:00 TSİ)
 w3 20:00->06:00 (akşam seansı sonrası -> VİOP sabah açılışı ~06:20-06:30 UTC)
 w4 06:00->07:00 (VİOP açık, spot açılış ~07:00 UTC)
f_gap = ln(ACILIS_T/UZL_{T-1}) w1..w3'e eşit yüklenirse ACILIS = sabah fiyatı; sadece w1'e yüklenirse = akşam seansının ilk işlemi.
kap_u = ln(KAPANIS_T/UZL_T) T günü 15:10->20:00 ES'e yüklenirse KAPANIS akşam seansını içerir."""
import sys, numpy as np, pandas as pd, numpy.linalg as la
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_G3_a")
from vcommon import *
R = S + "/out/code_v_G3_a/res"
UND = sys.argv[1] if len(sys.argv) > 1 else "XU030"
F = pd.read_parquet(R + f"/b2_{UND}.parquet")
es = pd.read_parquet(D + "/h1/ES=F.parquet")["o"]; es.index = es.index.tz_convert("UTC")
def p(ts):
    i = es.index.searchsorted(ts); return es.iloc[i] if i < len(es) and abs((es.index[i] - ts).total_seconds()) < 3600 else np.nan
dates = F.index[F.index >= "2024-06-12"]
bist = sorted(set(decomp("XU030.IS", start="2024-01-01").index))
prev = {b: a for a, b in zip(bist[:-1], bist[1:])}
rows = []
for T in dates:
    if T not in prev: continue
    P = prev[T]; t = lambda day, hh: pd.Timestamp(day.strftime("%Y-%m-%d") + f" {hh}", tz="UTC")
    v = [p(t(P, "15:00")), p(t(P, "16:00")), p(t(P, "20:00")), p(t(T, "06:00")), p(t(T, "07:00"))]
    k = [p(t(T, "15:00")), p(t(T, "16:00")), p(t(T, "20:00"))]
    rows.append(dict(T=T, w1=np.log(v[1]/v[0]), w2=np.log(v[2]/v[1]), w3=np.log(v[3]/v[2]), w4=np.log(v[4]/v[3]), e1=np.log(k[1]/k[0]), e2=np.log(k[2]/k[1])))
W = pd.DataFrame(rows).set_index("T")
Z = F.join(W, how="inner"); Z["kap_u"] = np.log(np.exp(Z.f_intra) / np.exp(Z.f_intra_s))  # ln(KAP/UZL)
def ols(y, X):
    z = pd.concat([y, X], axis=1).dropna(); A = np.c_[np.ones(len(z)), z.iloc[:, 1:].values]; b = la.lstsq(A, z.iloc[:, 0].values, rcond=None)[0]
    e = z.iloc[:, 0].values - A @ b; se = np.sqrt(np.diag(la.inv(A.T @ A)) * e.var(ddof=A.shape[1])); return pd.DataFrame({"b": b, "t": b / se}, index=["c"] + list(X.columns)).round(3), len(z)
for y in ["f_gap", "gap"]:
    r, n = ols(Z[y], Z[["w1", "w2", "w3", "w4"]]); print(f"\n{y} ~ ES pencereleri (n={n})"); print(r.T.to_string())
r, n = ols(Z["kap_u"], Z[["e1", "e2"]]); print(f"\nln(KAPANIS/UZLASMA)_T ~ ES T günü 15-16, 16-20 UTC (n={n})"); print(r.T.to_string())
print("sd ln(KAP/UZL) bps", round(1e4*Z.kap_u.std(), 1))
