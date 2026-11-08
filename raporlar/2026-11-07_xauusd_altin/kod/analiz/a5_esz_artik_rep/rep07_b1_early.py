"""B1 erken dönem (Yahoo GC=F/SI=F t-1 vekili) ve Pearson duyarlılığı. Yahoo tarih d kapanışı ≈ d 17:00 ET (21-22 UTC) → spot günü t'de yalnız d < t kullanılır."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a5_esz_artik_rep")
from rep_lib import *
D = pd.read_parquet(f"{OUT}/spot_snaps.parquet"); D = D[D.index >= "2010-01-01"]
va = pd.read_parquet(f"{OUT}/viop_rep.parquet")
gc = pd.read_parquet(f"{P}/yahoo/GC_F.parquet"); si = pd.read_parquet(f"{P}/yahoo/SI_F.parquet")
print("Yahoo ts_utc saatleri:", gc.ts_utc.dt.hour.value_counts().head(3).to_dict())
y = pd.concat([gc.close.rename("gc"), si.close.rename("si")], axis=1).dropna()
y.index = pd.to_datetime(y.index)
r = np.log(y.gc / y.si); dr = r.diff(); sdr = dr.rolling(120, min_periods=96).std().shift(1)
cal = D.index
def asof_prev(s):  # spot günü t için Yahoo tarihi < t olan son değer
    s = s.dropna(); idx = s.index.searchsorted(cal, side="left") - 1
    out = pd.Series(np.where(idx >= 0, s.values[np.clip(idx, 0, None)], np.nan), index=cal)
    return out
lp = np.log(D.XAU_p15)
sf = {h: sum(lp.diff().shift(-k) for k in range(1, h + 1)) for h in (1, 3, 5)}
pre = cal < "2017-03-06"
for k in (1, 3, 5):
    z = asof_prev(dr.rolling(k).sum() / (sdr * np.sqrt(k)))
    out = []
    for h in (1, 3, 5):
        st = ic_t(z[pre], sf[h][pre], max(h, 5)); out.append(f"h{h} ic {st['ic']:.3f} t {st['t']:.2f} n {st['n']}")
    print(f"GSY k{k} 2010-01..2017-03 spot:", " | ".join(out))
# B1 Pearson duyarlılığı (Dukascopy 15:00)
lr = np.log(D.XAU_p15 / D.XAG_p15); dlr = lr.diff(); sd = dlr.rolling(120, min_periods=96).std().shift(1)
z5 = (dlr.rolling(5).sum() / (sd * np.sqrt(5))).reindex(va.index)
for nm, x, yy in [("Pearson", z5, va.fwd1), ("Pearson z±3", z5.clip(-3, 3), va.fwd1), ("Pearson 2026 hariç", z5[z5.index.year < 2026], va.fwd1),
                  ("Pearson hedef ±3σ kırpılmış", z5, va.fwd1.clip(-3 * va.fwd1.std(), 3 * va.fwd1.std()))]:
    st = stats(x, yy, 1, method="pearson"); print(f"B1 {nm}: ic {st['ic']:.3f} t {st['t']:.2f} IS {st['t_is']:.2f} OOS {st['t_oos']:.2f}")
st = stats(z5[z5.index.year < 2026], va.fwd1, 1); print(f"B1 Spearman 2026 hariç: t {st['t']:.2f} OOS {st['t_oos']:.2f}")
pre2 = (D.index >= "2016-01-01") & (D.index < "2017-03-06")
z5s = dlr.rolling(5).sum() / (sd * np.sqrt(5)); sk = np.log(D.XAU_p15.shift(-1) / D.XAU_p16)
st = ic_t(z5s[pre2], sk[pre2], 5); print("B1 2016-01..2017-03 Dukascopy skip hedef:", {a: round(b, 3) for a, b in st.items()})
# B1 kararlılık: OOS'u yıllara böl, backtest yıllık
pos = -np.sign(z5).fillna(0); pnl = bt(pos, va.ret, 1, 5.0)["pnl"]
print("B1 yıllık net %:", (pnl.groupby(pnl.index.year).sum() * 100).round(1).to_dict())
print("B&H yıllık %:", (va.ret.groupby(va.index.year).sum() * 100).round(1).to_dict())

# Uzlaştırma: analistin spot-takvim sürümü (ffill'li panel y_* ile, tekrar günleri dy=0) vs Yahoo-takvim sürümü; aynı örneklem
sp = pd.read_parquet(f"{P}/panel_spot.parquet"); sp.index = pd.to_datetime(sp.index)
yl = np.log(sp.y_GC_F / sp.y_SI_F); yl = yl.where(sp.y_GC_F.diff().ne(0) | sp.y_SI_F.diff().ne(0)).ffill()
dy = yl.diff(); sdy = dy.rolling(120, min_periods=96).std().shift(1)
pre_s = sp.index < "2017-03-06"
for k in (5,):
    zs = (dy.rolling(k).sum() / (sdy * np.sqrt(k)))
    zy = asof_prev(dr.rolling(k).sum() / (sdr * np.sqrt(k))).reindex(sp.index)
    common = zs.notna() & zy.notna() & pre_s
    for h in (1, 3, 5):
        a = ic_t(zs[common], sp[f"sfwd{h}"][common], max(h, 5)); b = ic_t(zy[common], sp[f"sfwd{h}"][common], max(h, 5))
        c = ic_t(zy[pre_s & zy.notna()], sp[f"sfwd{h}"][pre_s], max(h, 5))
        print(f"GSY k{k} h{h}: spot-takvim t {a['t']:.2f} | Yahoo-takvim aynı örneklem t {b['t']:.2f} (n {b['n']}) | Yahoo-takvim tüm 2010-17 t {c['t']:.2f} (n {c['n']})")
    print("  iki sürüm korelasyonu:", round(zs[common].corr(zy[common]), 3))
