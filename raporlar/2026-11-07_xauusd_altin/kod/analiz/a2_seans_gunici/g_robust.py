"""(g) Öne çıkan adaylar için sağlamlık + IS'te seçilen kuralın OOS değerlendirmesi + akşam seansı fiyat kalibrasyonu (2026 bültenleri).
Yeni hipotez kaydı: yalnız 'g_is_selected' (IS seçimi -> tek OOS) ve 'g_early' tekrarları."""
from a2_common import *
reset_families(["g_is_selected", "g_early"])
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40); pd.set_option("display.max_rows", 200)
v = load_viop(); s = load_spot(); sv = segments(v); ss = segments(s)
# ---------- 1) S2 (t-1 20:00 -> t 00:00) mevsimselliği sağlamlık (spot panel 2010-2026)
x = ss.S2_late.dropna()
def mstat(z): m = mean_test(z); return f"{m['mean']*1e4:.2f} bps (t {m['t']:.2f}, n {m['n']})"
print("S2 tümü:", mstat(x))
print("S2 Pazartesi hariç:", mstat(x[x.index.dayofweek != 0]))
print("S2 uç dönem hariç:", mstat(x[extreme_mask(x.index)]))
print("S2 winsor 1-99:", mstat(x.clip(x.quantile(.01), x.quantile(.99))))
print("S2 medyan bps:", round(x.median() * 1e4, 2), " pozitif oranı:", round((x > 0).mean(), 3))
dst = pd.DatetimeIndex([pd.Timestamp(d.date()).tz_localize("America/New_York") for d in x.index]).map(lambda t: t.dst() != pd.Timedelta(0))
print("S2 ABD yaz saati:", mstat(x[np.asarray(dst)]), " | kış:", mstat(x[~np.asarray(dst)]))
# saat parçaları 20-22 ve 22-00
px = price_series()
def snapH(days, H, off=0):
    t = pd.DatetimeIndex([pd.Timestamp(d.date()).tz_localize("UTC") + pd.Timedelta(days=off, hours=H) for d in days])
    i = px.index.searchsorted(t, side="right") - 1; val = px.values[np.clip(i, 0, None)]
    st = (t - px.index[np.clip(i, 0, None)]) / pd.Timedelta(hours=1); return pd.Series(np.where(st <= 1, val, np.nan), index=days)
d = s.index[s.index.dayofweek < 4]
p20 = snapH(d, 20); p22 = snapH(d, 22, 0); p00 = snapH(d, 0, 1); p23 = snapH(d, 23, 0)
a = np.log(p22 / p20); b = np.log(p00 / p22)
print("Sal-Cum gecesi (Pzt-Per t-1): 20->22", mstat(a), " | 22->00", mstat(b), " | 20->00", mstat(a + b))
# ---------- 2) IS'te seçilen (a) ailesi kuralı: IS |t| en büyük segment/h -> OOS tek değerlendirme
A = pd.read_csv(f"{OUT}/a_segments_ic.csv")
best = A.loc[A.t_is.abs().idxmax()]
print("\nIS seçimi (a ailesi):", best.predictor, "h", best.h, "IS t", best.t_is, "-> OOS t", best.t_oos, "OOS ic", best.ic_oos)
p = best.predictor; h = int(best.h)
xs = sv[p] if p in sv else sv[p.replace("_cum5", "")].rolling(5).sum()
pos = np.sign(best.ic_is) * np.sign(xs)
L = legs(pos, v.v_ret, h); df = fmt_legs(L); print(df.to_string())
register(AGENT, "g_is_selected", f"g_is_best_{p}_h{h}", p, h, dict(ic=best.ic_oos, t=best.t_oos, n=None, t_is=best.t_is, t_oos=best.t_oos, ic_oos=best.ic_oos), "IS'te seçilen kural, OOS tek değerlendirme")
df.to_csv(f"{OUT}/g_is_selected_bt.csv", index=False)
# ---------- 3) Kış r_pre (14->15 UTC, fiks öncesi saat) -> fwd1: sağlamlık + erken dönem + backtest
fixwin = pd.Series([pd.Timestamp(t.date()).tz_localize("Europe/London").dst() == pd.Timedelta(0) for t in v.index], index=v.index)
rpre_w = np.log(v.xau_p15 / v.xau_p14).where(fixwin)
print("\nKış r_pre (14->15 UTC) -> fwd1:")
for cond, msk in [("hepsi", pd.Series(True, index=v.index)), ("roll_haric", roll_window_mask(v, 1)), ("uc_haric", extreme_mask(v.index))]:
    st = ic(rpre_w[msk], v.fwd1[msk], 5); print(f"  {cond}: ic {st['ic']:.4f} t {st['t']:.2f} n {st['n']}")
st = ic(rpre_w.clip(rpre_w.quantile(.01), rpre_w.quantile(.99)), v.fwd1, 5, method="pearson"); print(f"  winsor pearson: ic {st['ic']:.4f} t {st['t']:.2f}")
print("  placebo:", placebo_lead(rpre_w, v.v_ret, 1))
fws = pd.Series([pd.Timestamp(t.date()).tz_localize("Europe/London").dst() == pd.Timedelta(0) for t in s.index], index=s.index)
rpre_ws = np.log(s.xau_p15 / s.xau_p14).where(fws)
for h in (1,):
    m = s.index < "2017-01-01"; e = ic(rpre_ws[m], s[f"sfwd{h}"][m], 5)
    dd = pd.concat([rpre_ws[m].rename("x"), s[f"sfwd{h}"][m].rename("y")], axis=1).dropna(); yy = dd.groupby(dd.index.year).apply(lambda g: g.x.corr(g.y, method="spearman"))
    e.update(yrs_same_sign=int((np.sign(yy) == np.sign(e["ic"])).sum()), yrs=int(yy.notna().sum()))
    register(AGENT, "g_early", "g_early_rpre_winter_h1", "kış 14->15 UTC", 1, e, "spot 2010-2016 erken tekrar")
    print(f"  ERKEN 2010-16 (spot, sfwd1): ic {e['ic']:.4f} t {e['t']:.2f} n {e['n']} yıllar {e['yrs_same_sign']}/{e['yrs']}")
    # yaz 14->15 de (aynı saat dilimi; fiks sonrası)
    ysm = np.log(s.xau_p15 / s.xau_p14).where(~fws); e2 = ic(ysm[m], s.sfwd1[m], 5); print(f"  ERKEN yaz 14->15: ic {e2['ic']:.4f} t {e2['t']:.2f}")
pos = np.sign(rpre_w).fillna(0)
L = legs(pos, v.v_ret, 1); df = fmt_legs(L); df.to_csv(f"{OUT}/g_rpre_winter_bt.csv", index=False); print(df.to_string())
for c in (5, 10):
    b = bt_summary(pos, v.v_ret, 1, c); print(f"  maliyet {c}: full {b['full']['sharpe']} IS {b['is']['sharpe']} OOS {b['oos']['sharpe']} OOS_dm {b['oos']['sharpe_demeaned']}")
# ---------- 4) eb_{t-1} -> VİOP fwd (pozitif IC): IS işaretli tercil kuralı (eb yüksek -> uzun)
eb = np.log(v.v_settle / v.xau_p15) - v.ust_nom3m / 100 * v.v_dte / 365
q = eb[eb.index <= IS_END].quantile([1 / 3, 2 / 3]).values
pos = pd.Series(np.where(eb.shift(1) > q[1], 1.0, np.where(eb.shift(1) < q[0], -1.0, 0.0)), index=v.index)
for h in (3, 5):
    b = bt_summary(pos, v.v_ret, h); print(f"\neb_t-1 tercil (yüksek->uzun) h={h}: full {b['full']['sharpe']} (dm {b['full']['sharpe_demeaned']}) IS {b['is']['sharpe']} OOS {b['oos']['sharpe']} (dm {b['oos']['sharpe_demeaned']})")
# ---------- 5) C_pre (00->15 UTC) h=3
pos = np.sign(sv.C_pre).fillna(0); L = legs(pos, v.v_ret, 3); df = fmt_legs(L); print("\nC_pre işaret kuralı h=3:\n", df.to_string()); df.to_csv(f"{OUT}/g_cpre_bt.csv", index=False)
# ---------- 6) Akşam seansı kapanışı (VİOP, 2026 bültenleri) vs spot 20:00 + baz
import glob
ev = []
for f in sorted(glob.glob(f"{S}/dl4/as_*.csv")):
    t = pd.read_csv(f, sep=";", skiprows=[1])
    t = t[t["SOZLESME KODU"].astype(str).str.startswith("F_XAUUSD")]
    if t.empty: continue
    t = t.sort_values("ISLEM MIKTARI", ascending=False).iloc[0]
    day = pd.Timestamp(os.path.basename(f)[3:11])
    ev.append(dict(date=day, code=t["SOZLESME KODU"], ev_open=float(t["ACILIS FIYATI"]), ev_close=float(t["KAPANIS FIYATI"]), ev_qty=float(t["ISLEM MIKTARI"])))
E = pd.DataFrame(ev).set_index("date")
E = E.join(v[["v_code", "v_settle", "xau_p15", "xau_p16", "xau_p20", "v_tot_volume"]], how="inner")
E = E[E.code == E.v_code]
bas = np.log(E.v_settle / E.xau_p15)
d20 = (np.log(E.ev_close / E.xau_p20) - bas) * 1e4; d16 = (np.log(E.ev_open / E.xau_p16) - bas) * 1e4
print(f"\nAkşam seansı (2026, n={len(E)}): kapanış - (spot20:00 + baz) medyan {d20.median():.1f} bps, MAD {(d20 - d20.median()).abs().median():.1f}, std {d20.std():.1f}")
print(f"  açılış - (spot16:00 + baz) medyan {d16.median():.1f} bps, MAD {(d16 - d16.median()).abs().median():.1f}")
print(f"  akşam hacmi / gün toplam hacmi medyan: {(E.ev_qty / E.v_tot_volume).median():.3f}")
E.assign(d20_bps=d20).to_csv(f"{OUT}/g_evening_calibration.csv")
