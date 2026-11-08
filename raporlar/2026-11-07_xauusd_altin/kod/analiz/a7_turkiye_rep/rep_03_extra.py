"""Adım 3: ek kontroller — C1 pozisyon dağılımı/yıl içi demeaned, dışlamalar; C2 sabit-drift kıyası ve yıl ayrıştırması; erken dönem (spot panel)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a7_turkiye_rep")
from rep_lib import *
D = pd.read_parquet(f"{OUT}/rep_series.parquet"); idx = D.index
lfx = np.log(D.fx15); dl = lfx.diff()
bpd = np.log(D.u_settle / D.fx15) / D.u_dte.clip(lower=3)
sig = (dl.rolling(20).mean() - 1.4 * bpd).shift(1); pos = np.sign(sig).fillna(0.0)
print("C1 pozisyon dağılımı (yıl: uzun/kısa/sıfır oranı; sıfır = sinyal NaN, çoğu Dukascopy boşluğunun 20 günlük pencereyi bozması)")
for y in range(2017, 2027):
    m = idx.year == y; pp = pos[m]
    a = bt(pp, D.u_ret[m], 1, 5); b = bt(pp, D.u_ret[m], 1, 5, demean=True)
    nz = pp[pp != 0]
    print(f"  {y}: uzun {(pp>0).mean():.2f} kısa {(pp<0).mean():.2f} sıfır {(pp==0).mean():.2f} | sıfır-dışı içinde kısa {(nz<0).mean():.2f} | Sharpe {a['sharpe']:+.2f} yıl içi dm {b['sharpe']:+.2f}")
print("  Dukascopy USDTRY NaN günleri:", [str(d.date()) for d in idx[D.fx15.isna()]][:40])
# min_periods=15 ile (boşluk etkisini azalt)
sig15 = (dl.rolling(20, min_periods=15).mean() - 1.4 * bpd).shift(1); pos15 = np.sign(sig15).fillna(0.0)
for nm, pp in [("rolling min15", pos15)]:
    o = bt_seg(pp, D.u_ret, 1, 5); od = bt_seg(pp, D.u_ret, 1, 5, demean=True)
    print(f"  C1 {nm}: tam {o['full']['sharpe']:+.2f} IS {o['is']['sharpe']:+.2f} OOS {o['oos']['sharpe']:+.2f} (dm {od['oos']['sharpe']:+.2f}) maruz {o['full']['expo']:.2f}")
uf1 = fwdsum(D.u_ret, 1)
crisis = ((idx >= "2018-08-01") & (idx <= "2018-09-30")) | ((idx >= "2021-11-01") & (idx <= "2022-01-31"))
rollw = pd.Series(False, index=idx)
chg = D.u_code != D.u_code.shift()
for k in range(0, 6): rollw |= chg.shift(-k).fillna(False).astype(bool)
for nm, m in [("TL krizleri hariç", ~crisis), ("roll t+1..t+5 hariç", ~rollw.values), ("2017-2021", idx <= IS_END), ("2023-06+", idx >= "2023-06-01"), ("2024+", idx >= "2024-01-01"), ("KKM haftası hariç", ~((idx >= "2021-12-15") & (idx <= "2021-12-24")))]:
    s = ic(sig, uf1, 1, m); print(f"  C1 IC {nm}: {s['ic']:+.3f} t {s['t']:+.2f} n {s['n']}")
# yıl içi IC
d = pd.concat([sig, uf1], axis=1).dropna(); d.columns = ["x", "y"]
print("  C1 yıl içi IC:", d.groupby(d.index.year).apply(lambda g: round(g.x.rank().corr(g.y.rank()), 3)).to_dict())
# OOS'ta demeaned'in kaynağı: 2023-06..2023-12 vs 2024+
for nm, m in [("2022", idx.year == 2022), ("2023-01..05", (idx >= "2023-01-01") & (idx < "2023-06-01")), ("2023-06..12", (idx >= "2023-06-01") & (idx <= "2023-12-31")), ("2024-01..2026-11", idx >= "2024-01-01")]:
    a = bt(pos[m], D.u_ret[m], 1, 5); b = bt(pos[m], D.u_ret[m], 1, 5, demean=True)
    print(f"  C1 {nm}: Sharpe {a['sharpe']:+.2f} dm {b['sharpe']:+.2f} kısa oranı {(pos[m]<0).mean():.2f} ortalama USDTRY fut getirisi {D.u_ret[m].mean()*252*100:+.1f}%/yıl")

print("\nC2: sabit (kâhin) rejim-ortalaması drift kıyası, R2 vs RW = ort^2/E[y^2]; trail20 IC yıl ayrıştırması")
MAN = pd.Timestamp("2023-06-01")
for h in (1, 3, 5):
    y = lfx.shift(-h) - lfx
    for reg, m in [("2023-06+", idx >= MAN), ("2023-06..2025-12", (idx >= MAN) & (idx < "2026-01-01")), ("2025-04+", idx >= "2025-04-01")]:
        yy = y[m].dropna(); r2c = yy.mean() ** 2 / (yy ** 2).mean()
        # gerçekçi sabit: önceki 250 günün ortalaması
        f250 = (dl.rolling(250, min_periods=120).mean() * h)[m]
        e = (y[m] - f250).dropna(); r2_250 = 1 - (e ** 2).mean() / (y[m].reindex(e.index) ** 2).mean()
        fc = dl.rolling(20).mean() * h
        e2 = (y[m] - fc[m]).dropna(); r2t = 1 - (e2 ** 2).mean() / (y[m].reindex(e2.index) ** 2).mean()
        s = ic(dl.rolling(20).mean(), y, h, m)
        print(f"  h={h} {reg:17s}: trail20 R2 {r2t*100:+.1f}% | kâhin sabit drift R2 {r2c*100:+.1f}% | önceki-250g ort R2 {r2_250*100:+.1f}% | trail20 IC {s['ic']:+.3f} t {s['t']:+.2f} n {s['n']}")
    s = ic(dl.rolling(20).mean(), y, h, idx < MAN); print(f"  h={h} 2017-03..2023-05 trail20 IC {s['ic']:+.3f} t {s['t']:+.2f} (R2 negatif ama sıra korelasyonu pozitif)")
    # ölçek: trail20'ye OLS katsayısı (2017-03..2023-05)
    dd = pd.concat([dl.rolling(20).mean() * h, y], axis=1)[idx < MAN].dropna()
    b, t = nw_slope_t(dd.iloc[:, 1].values, dd.iloc[:, 0].values, max(h, 5)); print(f"        2017-03..2023-05 y ~ trail20*h: b {b:+.2f} (NW t {t:+.2f}) -> 1'in altında: büyüklük aşırı tahmin")

print("\nErken dönem (spot panel 2010-2016): Yahoo USDTRY_X t-1 değişimi -> sfwd3 (C4) ve TL şoku (C5)")
ps = pd.read_parquet(f"{P}/panel_spot.parquet"); ps.index = pd.to_datetime(ps.index)
cols = [c for c in ps.columns if "USDTRY" in c]; print("  sütunlar:", cols)
if "y_USDTRY_X" in ps:
    av = pd.to_datetime(ps["y_USDTRY_X_avail"]) if "y_USDTRY_X_avail" in ps else None
    if av is not None:
        lag_h = (av.dt.tz_localize(None) if av.dt.tz is not None else av) - ps.index.to_series()
        print("  y_USDTRY_X_avail - gün başı (saat) max:", lag_h.max(), " -> 15:00'ten önce mi:", bool((lag_h <= pd.Timedelta(hours=15)).all()))
    yu = np.log(ps["y_USDTRY_X"]).diff()
    sr = np.log(ps["s_p15"]).diff() if "s_p15" in ps else ps["s_ret"]
    s3 = fwdsum(sr, 3); mE = (ps.index >= "2010-01-01") & (ps.index <= "2016-12-31")
    s = ic(yu, s3, 3, mE); print(f"  C4 erken: IC {s['ic']:+.3f} t {s['t']:+.2f} n {s['n']}")
    shk = (yu.abs() > 0.025) & mE
    e = (s3[shk] - s3[mE].mean()).dropna()
    print(f"  C5 erken TL şoku: n {len(e)}, fazla {e.mean()*1e4:+.1f} bps, t {e.mean()/e.std()*np.sqrt(len(e)):+.2f}")
