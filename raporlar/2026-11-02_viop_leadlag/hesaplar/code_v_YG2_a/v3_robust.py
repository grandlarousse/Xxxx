"""v_YG2_a / 3: dayanıklılık ve alternatif tanımlar (spot, giriş C_t, çıkış 07:30_{t+1} = y_c730; eşik 25 bps)
(a) uzun-yalnız (CA<0, C'den al) / kısa ayak (CA>0, C'den açığa sat)
(b) tik ayrıklığı: |C-P1500| kaç tik? tik/fiyat > 20 bps hisseler
(c) aykırı gün: en iyi 5 gün hariç, kırpılmış ortalama, günlük medyan
(d) vade sonu / çeyrek sonu / yüksek-dağılım (toplu müzayede) günleri hariç
(e) hisseye özgü CA (CA - CA_XU030); gün sabit etkili regresyon
(f) plasebo: L30 (sürekli işlemin son 30 dk'sı) işareti ile aynı işlem
(g) kış testi: LH = log(C/P1430) (yıl boyu ölçülebilir); kış günlerinde LH sinyali
(h) hisse yoğunlaşması: hisse bazında ortalama, bir-hisse-hariç min/max
(i) kriz ayları
(j) SSF girişleri: SSF son işlem (close) ve uzlaşma (settle) ile giriş
"""
import numpy as np, pandas as pd, vcommon as v
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
P = v.load()
V47 = [s for s in P.stock.unique() if s not in ("XU030", "XU100")]
X = P[P.stock == "XU030"].set_index("date")
S = P[P.stock.isin(V47)].copy()
S["CA_x"] = S["date"].map(X["CA"]); S["CAid"] = S["CA"] - S["CA_x"]
S["y_c730_x"] = S["date"].map(X["y_c730"]); S["y_c730_id"] = S["y_c730"] - S["y_c730_x"]
days = np.sort(P.date.unique()); half = days[len(days) // 2]
cal = pd.Series(days, index=days); EOM = set(cal.groupby([cal.index.year, cal.index.month]).max().values)
QEND = {d for d in EOM if pd.Timestamp(d).month in (3, 6, 9, 12)}
THR = 0.0025; Y = "y_c730"
res = []
def rec(lab, dd, pnl, ntr, note=""):
    m, t, n = v.nw_t(dd)
    res.append(dict(test=lab, n_days=n, n_tr=ntr, mean_bps=m, t=t, per_trade=np.nanmean(pnl) if len(pnl) else np.nan, note=note))

base = S.CA.notna() & S[Y].notna()
dd, ntr, pnl = v.port(S, "CA", Y, THR, base.values); rec("BAZ |CA|>25 C->07:30", dd, pnl, ntr)
# (a)
dd, ntr, pnl = v.port(S, "CA", Y, THR, (base & (S.CA < 0)).values); rec("(a) uzun-yalnız CA<0", dd, pnl, ntr)
dd, ntr, pnl = v.port(S, "CA", Y, THR, (base & (S.CA > 0)).values); rec("(a) kısa-yalnız CA>0", dd, pnl, ntr)
# (b) tik
S["tick"] = v.tick_spot(S["P1500"]); S["ticks"] = ((S["C"] - S["P1500"]).abs() / S["tick"]).round()
S["tick_bps"] = 1e4 * S["tick"] / S["C"]
for lab, m in [("1 tik", S.ticks == 1), ("2 tik", S.ticks == 2), (">=3 tik", S.ticks >= 3), ("tik/fiyat>20bps", S.tick_bps > 20), ("tik/fiyat<=20bps", S.tick_bps <= 20), ("tik/fiyat<=10bps", S.tick_bps <= 10)]:
    dd, ntr, pnl = v.port(S, "CA", Y, THR, (base & m).values); rec(f"(b) {lab}", dd, pnl, ntr)
print("tik/fiyat>20bps hisse-gün payı (|CA|>25):", round(((S.tick_bps > 20) & (S.CA.abs() > THR)).sum() / (S.CA.abs() > THR).sum(), 3),
      " hisseler:", sorted(S[(S.tick_bps > 20)].stock.unique()))
# (c) aykırı
dd, ntr, pnl = v.port(S, "CA", Y, THR, base.values)
top5 = dd.sort_values().index[-5:]; rec("(c) en iyi 5 gün hariç", dd.drop(top5), pnl, ntr)
bot5 = dd.sort_values().index[:5]; rec("(c) en kötü 5 gün hariç", dd.drop(bot5), pnl, ntr)
q = pnl.quantile([0.01, 0.99]); pw = pnl.clip(q.iloc[0], q.iloc[1]); ddw = pw.groupby(S.loc[pw.index, "date"]).mean(); rec("(c) işlem %1/%99 kırpılmış", ddw, pw, ntr)
res.append(dict(test="(c) günlük portföy medyanı", mean_bps=dd.median(), note=f"işlem medyanı {pnl.median():.2f}"))
# (d)
disp = S[S.CA.notna()].groupby("date")["CA"].apply(lambda x: x.abs().mean())
hi = set(disp[disp > disp.quantile(0.95)].index)
for lab, m in [("vade sonu hariç", ~S.date.isin(EOM)), ("çeyrek sonu hariç", ~S.date.isin(QEND)), ("yüksek dağılım günleri (üst %5 ort|CA|) hariç", ~S.date.isin(hi)),
               ("yalnız yüksek dağılım günleri", S.date.isin(hi))]:
    dd, ntr, pnl = v.port(S, "CA", Y, THR, (base & m).values); rec(f"(d) {lab}", dd, pnl, ntr)
print("yüksek dağılım günleri:", sorted(pd.Timestamp(d).date() for d in hi))
# (e) hisseye özgü
b2 = S.CAid.notna() & S.y_c730_id.notna()
dd, ntr, pnl = v.port(S, "CAid", "y_c730_id", THR, b2.values); rec("(e) hisseye özgü CA_i-CA_X, getiri XU030 hedge'li", dd, pnl, ntr)
d = S[["CA", Y, "date", "L30", "DAY"]].dropna().copy()
for c in ["CA", Y, "L30", "DAY"]: d[c + "_dm"] = d[c] - d.groupby("date")[c].transform("mean")
b, se, n, G = v.ols_cl(d[Y + "_dm"].values, d[["CA_dm", "L30_dm", "DAY_dm"]].values, d["date"].values)
res.append(dict(test="(e) gün-sabit-etkili regresyon C->07:30 ~ CA", mean_bps=np.nan, t=b[1] / se[1], note=f"b_CA {b[1]:.3f}, n {n}"))
# kesitsel ortalama CA (piyasa müzayede hareketi) -> ortalama ertesi getiri
cm = S.groupby("date")[["CA", Y]].mean().dropna()
b, se, n, G = v.ols_cl(cm[Y].values, cm[["CA"]].values, np.arange(len(cm)))
res.append(dict(test="(e) kesit ortalaması CA -> kesit ortalaması C->07:30 (zaman serisi)", t=b[1] / se[1], note=f"b {b[1]:.3f}, n {n}"))
# (f) plasebo L30
dd, ntr, pnl = v.port(S, "L30", Y, THR, (S.L30.notna() & S[Y].notna() & S.CA.notna()).values); rec("(f) plasebo: -sign(L30) |L30|>25, C->07:30", dd, pnl, ntr)
dd, ntr, pnl = v.port(S, "L30", "y_c730", THR, (S.L30.notna() & S[Y].notna() & (S.CA.abs() <= 0.0005)).values); rec("(f) plasebo L30, yalnız |CA|<=5bps günleri", dd, pnl, ntr)
# (g) kış: LH
S["winter"] = ~S["summer"]
for lab, m in [("yaz", S.summer), ("kış", S.winter)]:
    mm = S.LH.notna() & S[Y].notna() & m
    dd, ntr, pnl = v.port(S, "LH", Y, THR, mm.values); rec(f"(g) LH=log(C/P1430) sinyali, {lab}", dd, pnl, ntr)
    d = S[mm][[Y, "LH", "DAY", "date"]].dropna()
    b, se, n, G = v.ols_cl(d[Y].values, d[["LH", "DAY"]].values, d["date"].values)
    res.append(dict(test=f"(g) regresyon C->07:30 ~ LH, {lab}", t=b[1] / se[1], note=f"b_LH {b[1]:.3f}, n {n}, gün {G}"))
# yazın LH vs CA aynı örneklem
mm = S.LH.notna() & S[Y].notna() & S.summer & S.CA.notna()
d = S[mm][[Y, "LH", "CA", "L30", "date"]].dropna()
b, se, n, G = v.ols_cl(d[Y].values, d[["LH"]].values, d["date"].values)
res.append(dict(test="(g) yaz, C->07:30 ~ LH (tek)", t=b[1] / se[1], note=f"b {b[1]:.3f}; var(CA)/var(LH)={d.CA.var() / d.LH.var():.2f}; beklenen ~ -0,35*{d.CA.var() / d.LH.var():.2f}"))
# (h) hisse bazında
rows = []
for s, g in S[base].groupby("stock"):
    gg = g[g.CA.abs() > THR]
    p = -np.sign(gg.CA) * gg[Y] * 1e4
    m, t, n = v.nw_t(p.values) if len(p) > 10 else (np.nan, np.nan, len(p))
    rows.append(dict(stock=s, n=len(p), mean_bps=m, t=t, tick_bps=g.tick_bps.median(), absCA_bps=1e4 * g.CA.abs().mean()))
H = pd.DataFrame(rows).sort_values("mean_bps")
H.to_csv(v.RES + "/v3_stock.csv", index=False)
print(H.round(2).to_string())
loo = []
for s in V47:
    dd, ntr, pnl = v.port(S, "CA", Y, THR, (base & (S.stock != s)).values); loo.append((s, dd.mean()))
loo = pd.DataFrame(loo, columns=["drop", "mean"]); res.append(dict(test="(h) bir-hisse-hariç aralığı", note=f"min {loo['mean'].min():.2f} ({loo.loc[loo['mean'].idxmin(), 'drop']} hariç) / max {loo['mean'].max():.2f}"))
# (i) kriz ayları
for lab, m in [("2025-03 İmamoğlu", (S.date >= "2025-03-01") & (S.date < "2025-04-01")), ("2026-09..10 fon krizi", S.date >= "2026-09-01"),
               ("2024 yaz", S.year == 2024), ("2025", S.year == 2025), ("2026 (Nis-Ağu)", (S.year == 2026) & (S.date < "2026-09-01"))]:
    dd, ntr, pnl = v.port(S, "CA", Y, THR, (base & m).values); rec(f"(i) {lab}", dd, pnl, ntr)
# (j) SSF girişleri
res.append(dict(test="(j) SSF girişleri -> v2_ssf.py çıktısında (settle girişi -10 bps, t -3,3)"))
RR = pd.DataFrame(res); RR.to_csv(v.RES + "/v3_robust.csv", index=False)
print(RR.round(2).to_string())
