"""1) Ham zaman damgalarıyla öngörücü fiyatlarının (xau_pHH) gerçekten HH:00 UTC fiyatı olduğunu doğrula.
2) VİOP aktif kontratı ve v_ret / fwd'yi viop_long'dan baştan kur, panel ile karşılaştır."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a2_seans_gunici_rep")
from rep_common import *

v = pd.read_parquet(f"{P}/panel_viop.parquet"); v.index = pd.to_datetime(v.index)
s = pd.read_parquet(f"{P}/panel_spot.parquet"); s.index = pd.to_datetime(s.index)

print("== 1a) panel xau_pHH vs kendi 'bar(HH-1) kapanışı' (tam eşleşme) ==")
for nm, df in [("viop", v), ("spot", s)]:
    for H in (0, 7, 12, 14, 15, 16, 20):
        mine = price_at(day_times(df.index, H)).values
        pan = df[f"xau_p{H:02d}"].values
        d = np.abs(np.log(mine / pan)) * 1e4
        ok = np.isfinite(d)
        # alternatif hipotezler: bar(HH) kapanışı (yani HH+1 fiyatı) ve bar(HH) açılışı
        alt = price_at(day_times(df.index, H + 1)).values
        da = np.abs(np.log(alt / pan)) * 1e4
        print(f"{nm} p{H:02d}: n_panel={np.isfinite(pan).sum()} n_mine={np.isfinite(mine).sum()} both={ok.sum()} "
              f"exact(<0.01bps)={np.mean(d[ok] < 0.01):.4f} maxdiff={np.nanmax(d):.2f}bps | 'HH+1' hipotezi exact={np.nanmean(da[np.isfinite(da)] < 0.01):.4f}")
    # prev
    pidx = df.index
    p15prev = pd.Series(df.xau_p15.values, index=pidx).shift(1)
    p20prev = pd.Series(df.xau_p20.values, index=pidx).shift(1)
    print(f"{nm} xau_p15_prev == p15.shift(1): {np.nanmean(np.isclose(p15prev, df.xau_p15_prev)):.4f}  (NaN-panel {df.xau_p15_prev.isna().sum()})")
    print(f"{nm} xau_p20_prev == p20.shift(1): {np.nanmean(np.isclose(p20prev, df.xau_p20_prev)):.4f}  (NaN-panel {df.xau_p20_prev.isna().sum()})")
    # p20_prev ile gerçek takvim: t-1 endeks günü mü, takvim günü mü?
    gap = (pidx.to_series().diff().dt.days)
    print(f"{nm} endeks günleri arası gün farkı dağılımı:", gap.value_counts().head(6).to_dict())

# eşleşmeyen satırlar
for H in (0, 15, 20):
    mine = price_at(day_times(v.index, H)); pan = v[f"xau_p{H:02d}"]
    bad = v.index[~np.isclose(mine.values, pan.values, rtol=1e-7) & (np.isfinite(mine.values) | np.isfinite(pan.values))]
    print(f"p{H:02d} uyuşmayan/eksik günler (viop): {len(bad)} ->", [str(x.date()) for x in bad[:12]])
    if len(bad):
        print("   panel:", pan.loc[bad[:5]].values, " mine:", mine.loc[bad[:5]].values if False else price_at(day_times(bad[:5], H)).values,
              " asof:", price_asof(day_times(bad[:5], H), 3).values)

print("\n== 1b) dakikalık veride index = bar başlangıcı mı? 14:59 dakika barı kapanışı vs saatlik 14:00 barı kapanışı ==")
m = minute_all()
h = hourly_bars()
cmp = []
for d in pd.DatetimeIndex(sorted(set(m.index.normalize()))):
    t1459 = d + pd.Timedelta(hours=14, minutes=59)
    if t1459 in m.index and (d + pd.Timedelta(hours=14)) in h.index:
        cmp.append((d, m.loc[t1459, "c"], h.loc[d + pd.Timedelta(hours=14), "c"], m.loc[d + pd.Timedelta(hours=14), "o"] if (d + pd.Timedelta(hours=14)) in m.index else np.nan, h.loc[d + pd.Timedelta(hours=14), "o"]))
C = pd.DataFrame(cmp, columns=["d", "m1459c", "h14c", "m1400o", "h14o"])
print("n gün", len(C), " 14:59 kapanış == saatlik 14 kapanış oranı:", np.mean(np.isclose(C.m1459c, C.h14c)), " 14:00 açılış == saatlik açılış:", np.mean(np.isclose(C.m1400o, C.h14o)))

print("\n== 2) VİOP aktif kontrat yeniden kurulumu ==")
A = viop_active()
A = A.reindex(v.index)
print("aktif kod eşleşmesi:", np.mean(A.code.values == v.v_code.values))
print("settle eşleşmesi:", np.nanmean(np.isclose(A.settle, v.v_settle)))
print("ret eşleşmesi (|fark|<1e-10):", np.nanmean(np.abs(A.ret - v.v_ret) < 1e-10), " NaN ret mine/panel:", A.ret.isna().sum(), v.v_ret.isna().sum())
for hh in (1, 3, 5):
    f = fwd(A.ret, hh)
    print(f"fwd{hh}: eşleşme {np.nanmean(np.abs(f - v[f'fwd{hh}']) < 1e-10):.4f}, NaN mine {f.isna().sum()} panel {v[f'fwd{hh}'].isna().sum()}")
# roll günlerinde v_ret aynı kontrat içinde mi? (prev_settle o kontratın önceki uzlaşması mı)
L = pd.read_parquet(f"{P}/viop_long.parquet"); L = L[L.code.astype(str).str.startswith("F_XAUUSD")]; L["date"] = pd.to_datetime(L.date)
Ls = L.set_index(["code", "date"]).sort_index()
chk = []
for code, g in L.sort_values("date").groupby("code"):
    g = g.set_index("date").sort_index()
    ps = g.settle.shift(1)
    chk.append(pd.DataFrame({"code": code, "prev_from_series": ps, "prev_bulletin": g.prev_settle}))
K = pd.concat(chk).dropna()
print("bülten prev_settle == aynı kontratın bir önceki gün settle'ı:", np.mean(np.isclose(K.prev_from_series, K.prev_bulletin)), "n", len(K))
roll = (A.code != A.code.shift(1)).sum() - 1
print("roll sayısı:", roll)
A.to_parquet(f"{OUT}/viop_active_mine.parquet")
