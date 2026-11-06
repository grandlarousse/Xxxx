"""4) Greenwood-Shleifer-You (2019) tarzi: +100% kosu sonrasi cokus mu devam mi?
Olay: sektor VW 24-ay ham getiri >= 100%, 24-ay piyasa-net (R_i - R_m) >= 100%, 60-ay ham >= 50%, firma sayisi >= 10.
Ilk gecis ayi; ayni sektorde 24 ay icinde yeni olay sayilmaz.
Cokus: olay ayindan sonraki 24 ayda herhangi bir noktada %40 dusus (tepe-dip, mutlak).
Ozellikler (karar aninda bilinen, French verisinden vekiller):
  acc   = R(t-24..t) - R(t-24..t-12)   (GSY ivme tanimi)
  volr  = 12 aylik gunluk volatilitenin sektorler arasi yuzdelik sirasi; dvolr = volr(t) - volr(t-12)
  iss   = log(ME_t/ME_{t-12}) - log(1+R_{t-12..t})   (ihrac + yeni giris vekili; ME = firma sayisi x ort. buyukluk)
  dnf   = log(nfirms_t / nfirms_{t-24})  (yeni sirket girisi vekili)
  tilt  = EW 24ay getiri - VW 24ay getiri  (kucuk/yeni firmalar onde mi; GSY 'age tilt' vekili)
  bmr   = BE/ME sektorler arasi yuzdelik (son bilinen yil)
  mkt24 = piyasa 24 ay getiri (CAPE vekili)
"""
import os
import numpy as np
import pandas as pd
from dalga_tanim import base_data, OUT
from ff_load import load_daily49

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 40)
pd.set_option("display.max_rows", 300)

R, RM, RF, m = base_data(start="1926-07")
EW = (m["ew"] / 100).loc[R.index[0]:]
nf = m["nfirms"].loc[R.index[0]:]
sz = m["size"].loc[R.index[0]:]
ME = nf * sz
bm = m["bm_y"]
d = load_daily49()["vw"] / 100
dvol = d.groupby(d.index.to_period("M")).std() * np.sqrt(252)
vol12 = (dvol ** 2).rolling(12, min_periods=10).mean() ** 0.5
vol12 = vol12.reindex(R.index)
volr = vol12.rank(axis=1, pct=True)

lr = np.log1p(R)
lm = np.log1p(RM)
P = lr.cumsum()
PM = lm.cumsum()
def cum(n):
    return np.expm1(P - P.shift(n))
R24, R12, R60 = cum(24), cum(12), cum(60)
R24_first = np.expm1(P.shift(12) - P.shift(24))
M24 = np.expm1(PM - PM.shift(24))
net24 = R24.sub(M24, axis=0)
EW24 = np.expm1(np.log1p(EW).rolling(24).sum())

cond = (R24 >= 1.0) & (net24 >= 1.0) & (R60 >= 0.5) & (nf >= 10)

idx = list(R.index)
events = []
for ind in R.columns:
    last = -999
    c = cond[ind].values
    for t in range(len(idx)):
        if c[t] and (t == 0 or not c[t - 1]) and (t - last) > 24:
            last = t
            p0 = P[ind].values[t]
            fut = P[ind].values[t:t + 25]
            futm = PM.values[t:t + 25]
            full = len(fut) == 25 and not np.isnan(fut).any()
            if len(fut) > 1:
                runmax = np.maximum.accumulate(fut)
                dd = np.min(fut - runmax)
                crash = dd <= np.log(0.6)
                pk = int(np.argmax(fut[:np.argmin(fut - runmax) + 1])) if crash else int(np.argmax(fut))
            else:
                dd, crash, pk = np.nan, np.nan, 0
            ev = dict(ind=ind, date=idx[t], t=t, r24=R24[ind].iloc[t], net24=net24[ind].iloc[t],
                      acc=R24[ind].iloc[t] - R24_first[ind].iloc[t],
                      volr=volr[ind].iloc[t], dvolr=volr[ind].iloc[t] - volr[ind].iloc[t - 12] if t >= 12 else np.nan,
                      iss=np.log(ME[ind].iloc[t] / ME[ind].iloc[t - 12]) - np.log1p(R12[ind].iloc[t]),
                      dnf=np.log(nf[ind].iloc[t] / nf[ind].iloc[t - 24]),
                      tilt=EW24[ind].iloc[t] - R24[ind].iloc[t],
                      mkt24=M24.iloc[t], nfirms=nf[ind].iloc[t],
                      full=full, crash=bool(crash) if full else (bool(crash) if crash else np.nan),
                      maxdd=np.expm1(dd) if len(fut) > 1 else np.nan,
                      to_peak_mo=pk, ret_to_peak=np.expm1(fut[pk] - p0) if len(fut) > 1 else np.nan)
            for h in (6, 12, 24):
                if t + h < len(idx):
                    ev[f"f{h}"] = np.expm1(P[ind].values[t + h] - p0)
                    ev[f"fn{h}"] = ev[f"f{h}"] - np.expm1(PM.values[t + h] - PM.values[t])
                else:
                    ev[f"f{h}"] = ev[f"fn{h}"] = np.nan
            # BE/ME: son bilinen yil (Temmuz'dan itibaren o yil)
            y = idx[t].year if idx[t].month >= 7 else idx[t].year - 1
            if y in bm.index:
                row = bm.loc[y]
                ev["bmr"] = row.rank(pct=True)[ind]
            else:
                ev["bmr"] = np.nan
            events.append(ev)
E = pd.DataFrame(events)
E.to_pickle(os.path.join(OUT, "gsy_events.pkl"))
print("Toplam olay:", len(E), " 1928-2012 arasi:", ((E.date >= pd.Period("1928-01", "M")) & (E.date <= pd.Period("2012-03", "M"))).sum())
print(E[["ind", "date", "r24", "net24", "acc", "volr", "dvolr", "iss", "dnf", "tilt", "bmr", "mkt24", "crash", "maxdd", "to_peak_mo", "ret_to_peak", "f12", "fn12", "f24", "fn24"]].round(2).to_string())

F = E[E.full == True].copy()
F["crash"] = F.crash.astype(bool)
print("\nTam 24 ay gozlemli olay:", len(F), "cokus orani:", round(F.crash.mean(), 3))
print("ileri 12 ay ham ort/medyan:", round(F.f12.mean(), 3), round(F.f12.median(), 3), " net:", round(F.fn12.mean(), 3))
print("ileri 24 ay ham ort/medyan:", round(F.f24.mean(), 3), round(F.f24.median(), 3), " net:", round(F.fn24.mean(), 3))
print("cokenlerde tepeye kadar ort ay:", round(F[F.crash].to_peak_mo.mean(), 1), " tepeye kadar ort getiri:", round(F[F.crash].ret_to_peak.mean(), 3))
print("cokmeyenler ileri 12/24:", round(F[~F.crash].f12.mean(), 3), round(F[~F.crash].f24.mean(), 3), " cokenler:", round(F[F.crash].f12.mean(), 3), round(F[F.crash].f24.mean(), 3))
print("Donem bazli:", F.groupby(F.date.apply(lambda p: "<=2014" if p.year <= 2014 else ">=2015")).agg(n=("ind", "size"), crash=("crash", "mean"), f12=("f12", "mean"), f24=("f24", "mean")).round(3).to_string())

# kontrol: kosulsuz %40 cokus orani (rastgele sektor-ay)
uc = []
Pv = P.values
for j in range(Pv.shape[1]):
    for t in range(60, Pv.shape[0] - 24, 3):
        fut = Pv[t:t + 25, j]
        if np.isnan(fut).any() or nf.values[t, j] < 10:
            continue
        uc.append(np.min(fut - np.maximum.accumulate(fut)) <= np.log(0.6))
print("Kosulsuz 24 ay %40 cokus olasiligi (sektor-ay):", round(np.mean(uc), 3))

# ozellik bazinda: medyan ustu/alti cokus orani ve ileri getiriler; zaman kumelenmesi icin yil-kume t
feats = ["acc", "volr", "dvolr", "iss", "dnf", "tilt", "bmr", "mkt24", "r24", "net24"]
rows = []
for f in feats:
    g = F.dropna(subset=[f])
    med = g[f].median()
    hi, lo = g[g[f] > med], g[g[f] <= med]
    # yil kumeli fark t-istatistigi (basit: yil ortalamalari uzerinden)
    def yr_t(col):
        a = g.assign(h=(g[f] > med).astype(int), y=g.date.apply(lambda p: p.year))
        a["x"] = a[col].astype(float)
        # regress x on h with year-clustered se
        X = np.column_stack([np.ones(len(a)), a.h.values])
        b = np.linalg.lstsq(X, a.x.values, rcond=None)[0]
        e = a.x.values - X @ b
        XtX_inv = np.linalg.inv(X.T @ X)
        meat = np.zeros((2, 2))
        for _, gg in a.assign(e=e).groupby("y"):
            Xi = np.column_stack([np.ones(len(gg)), gg.h.values])
            s = Xi.T @ gg.e.values
            meat += np.outer(s, s)
        V = XtX_inv @ meat @ XtX_inv
        return b[1] / np.sqrt(V[1, 1]) if V[1, 1] > 0 else np.nan
    rows.append(dict(feat=f, n=len(g), med=med, crash_hi=hi.crash.mean(), crash_lo=lo.crash.mean(), t_crash=yr_t("crash"),
                     f12_hi=hi.f12.mean(), f12_lo=lo.f12.mean(), f24_hi=hi.f24.mean(), f24_lo=lo.f24.mean(),
                     t_f24=yr_t("f24"), fn24_hi=hi.fn24.mean(), fn24_lo=lo.fn24.mean()))
T = pd.DataFrame(rows)
print("\n== Ozellik medyan bolmesi: cokus orani ve ileri getiri (yuksek vs dusuk) ==")
print(T.round(3).to_string())

# skor: risk bayraklari (acc, dvolr, iss, tilt medyan ustu) sayisi -- medyanlar ornek-ici (GSY gibi), ayrica genisleyen
flags = ["acc", "dvolr", "iss", "tilt"]
G = F.dropna(subset=flags).copy()
for f in flags:
    G[f + "_hi"] = G[f] > G[f].median()
G["score"] = G[[f + "_hi" for f in flags]].sum(axis=1)
print("\nRisk skoru (ornek-ici medyan, 0-4) -> cokus orani, ileri 12/24 ay:")
print(G.groupby("score").agg(n=("ind", "size"), crash=("crash", "mean"), f12=("f12", "mean"), f24=("f24", "mean"), fn24=("fn24", "mean")).round(3).to_string())
# genisleyen (look-ahead yok): her olay icin onceki olaylarin medyani (en az 8 onceki olay)
G = G.sort_values("date").reset_index(drop=True)
sc = []
for i in range(len(G)):
    prev = G.iloc[:i]
    prev = prev[prev.date < G.date.iloc[i]]
    if len(prev) < 8:
        sc.append(np.nan); continue
    sc.append(sum(G[f].iloc[i] > prev[f].median() for f in flags))
G["score_oos"] = sc
print("\nRisk skoru (genisleyen medyan, look-ahead yok):")
print(G.dropna(subset=["score_oos"]).groupby("score_oos").agg(n=("ind", "size"), crash=("crash", "mean"), f12=("f12", "mean"), f24=("f24", "mean")).round(3).to_string())

# ---- Islem stratejileri olaydan sonra (24 ay ufuk): tut / hemen cik (T-bill) / trailing stop / skor>=3 ise cik
rfv = np.log1p(RF).values
def path_ret(ind, t, rule, X=0.2, maxh=24):
    j = R.columns.get_loc(ind)
    p = P.values[:, j]
    end = min(t + maxh, len(p) - 1)
    if rule == "hold":
        return np.expm1(p[end] - p[t])
    if rule == "tbill":
        return np.expm1(rfv[t + 1:end + 1].sum())
    if rule == "trail":
        pk = p[t]
        for s in range(t + 1, end + 1):
            pk = max(pk, p[s])
            if p[s] <= pk + np.log(1 - X):
                return np.expm1(p[s] - p[t] + rfv[s + 1:end + 1].sum())
        return np.expm1(p[end] - p[t])
out = []
for _, e in F.iterrows():
    o = dict(ind=e.ind, date=e.date, crash=e.crash, hold=path_ret(e.ind, e.t, "hold"), tbill=path_ret(e.ind, e.t, "tbill"))
    for X in (0.10, 0.15, 0.20, 0.25):
        o[f"trail{int(X*100)}"] = path_ret(e.ind, e.t, "trail", X)
    out.append(o)
S = pd.DataFrame(out)
S = S.merge(G[["ind", "date", "score", "score_oos"]], on=["ind", "date"], how="left")
S["score_exit"] = np.where(S.score_oos >= 3, S.tbill, S.hold)
S["score_trail"] = np.where(S.score_oos >= 3, S.tbill, S.trail15)
print("\n== Olay sonrasi 24 ay strateji getirileri (ortalama / medyan / kayip orani / en kotu) ==")
for c in ["hold", "tbill", "trail10", "trail15", "trail20", "trail25", "score_exit", "score_trail"]:
    v = S[c].dropna()
    print(f"{c:12s} n={len(v):3d} ort={v.mean():+.3f} med={v.median():+.3f} kayip%={(v<0).mean():.2f} en_kotu={v.min():+.3f}  cokenlerde ort={S.loc[S.crash, c].mean():+.3f} cokmeyenlerde ort={S.loc[~S.crash, c].mean():+.3f}")
vv = S.dropna(subset=["score_oos"])
print(" (skor-oos tanimli alt ornek n=%d) hold ort=%.3f trail15 ort=%.3f score_exit ort=%.3f score_trail ort=%.3f" % (len(vv), vv.hold.mean(), vv.trail15.mean(), vv.score_exit.mean(), vv.score_trail.mean()))

# ---- 2026-09 itibariyla canli kosular (son 24 ay) ve ozellikleri
t = len(idx) - 1
live = []
for ind in R.columns:
    live.append(dict(ind=ind, r24=R24[ind].iloc[t], net24=net24[ind].iloc[t], r12=R12[ind].iloc[t],
                     acc=R24[ind].iloc[t] - R24_first[ind].iloc[t], volr=volr[ind].iloc[t],
                     dvolr=volr[ind].iloc[t] - volr[ind].iloc[t - 12],
                     iss=np.log(ME[ind].iloc[t] / ME[ind].iloc[t - 12]) - np.log1p(R12[ind].iloc[t]),
                     dnf=np.log(nf[ind].iloc[t] / nf[ind].iloc[t - 24]), tilt=EW24[ind].iloc[t] - R24[ind].iloc[t],
                     dd_from_high=np.expm1(P[ind].iloc[t] - P[ind].iloc[t - 12:t + 1].max()), event=bool(cond[ind].iloc[t])))
L = pd.DataFrame(live).sort_values("r24", ascending=False)
print("\n== 2026-09 sonu: en guclu 24 ay kosulari ve GSY ozellikleri ==")
print(L.head(15).round(3).to_string())
print("Olay medyanlari (karsilastirma):", F[["acc", "volr", "dvolr", "iss", "dnf", "tilt"]].median().round(3).to_dict())
L.to_pickle(os.path.join(OUT, "gsy_live.pkl"))
