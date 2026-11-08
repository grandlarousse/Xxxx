"""Adım 2: C1..C6 bağımsız yeniden hesaplama (kendi seri, IC+NW t, IS/OOS, 5/10 bps backtest, B&H, demeaned, bacaklar)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a7_turkiye_rep")
from rep_lib import *
import json
pd.set_option("display.width", 220)
D = pd.read_parquet(f"{OUT}/rep_series.parquet")
V = viop_long()
# XU030 2020-07-27 endeks sadeleştirmesi: bülten prev_settle kullan
xu_fix = np.log(D.xu_settle / pd.Series([V[(V.code == c) & (V.date == d)].prev_settle.iloc[0] for d, c in zip(D.index, D.xu_code)], index=D.index))
print("XU030 ret düzeltmesi: değişen gün", int(((xu_fix - D.xu_ret).abs() > 1e-9).sum()))
D["xu_ret"] = xu_fix
idx = D.index; isx = idx <= IS_END
R = {}
def fmt(s): return f"IC {s['ic']:+.3f} t {s['t']:+.2f} n {s['n']} | IS {s['ic_is']:+.3f} (t {s['t_is']:+.2f}) | OOS {s['ic_oos']:+.3f} (t {s['t_oos']:+.2f}) | yıl {s['yrs']}"
def tpy(pos): pos = pos.fillna(0); return (pos.diff().abs() > 0).sum() / (len(pos) / 252)
def strat(name, pos, ret, h, costs=(5, 10)):
    out = {}
    for c in costs:
        a = bt_seg(pos, ret, h, c); dm = bt_seg(pos, ret, h, c, demean=True)
        lg = {k: bt_seg(pos.clip(lower=0) if k == "long" else pos.clip(upper=0), ret, h, c) for k in ("long", "short")}
        out[c] = dict(full=a["full"]["sharpe"], IS=a["is"]["sharpe"], OOS=a["oos"]["sharpe"], OOS_dm=dm["oos"]["sharpe"], full_dm=dm["full"]["sharpe"],
                      OOS_nonet=a["oos"]["sharpe_nonet"], gross_full=a["full"]["gross_sharpe"],
                      t_full=a["full"]["t"], t_is=a["is"]["t"], t_oos=a["oos"]["t"], expo=a["full"]["expo"],
                      long_oos=lg["long"]["oos"]["sharpe"], short_oos=lg["short"]["oos"]["sharpe"], long_full=lg["long"]["full"]["sharpe"], short_full=lg["short"]["full"]["sharpe"])
    bh = bt_seg(pd.Series(1.0, index=ret.index), ret, 1, 0)
    out["bh"] = dict(full=bh["full"]["sharpe"], IS=bh["is"]["sharpe"], OOS=bh["oos"]["sharpe"])
    out["trades_per_yr"] = tpy(pos)
    pnl = bt(pos, ret, h, 5)["pnl"]; yr = pnl.groupby(pnl.index.year).apply(lambda z: z.mean() / z.std() * np.sqrt(252))
    out["yr_sharpe"] = yr.round(2).to_dict(); out["yrs_pos"] = f"{(yr > 0).sum()}/{len(yr)}"
    R[name] = out
    q = out[5]; q10 = out.get(10, out[5])
    print(f"  [{name}] 5bps: tam {q['full']:+.2f} (dm {q['full_dm']:+.2f}) IS {q['IS']:+.2f} OOS {q['OOS']:+.2f} (dm {q['OOS_dm']:+.2f}; netleştirmesiz {q['OOS_nonet']:+.2f}) | 10bps OOS {q10['OOS']:+.2f}"
          f" | B&H tam {out['bh']['full']:+.2f} IS {out['bh']['IS']:+.2f} OOS {out['bh']['OOS']:+.2f} | uzun bacak OOS {q['long_oos']:+.2f} kısa OOS {q['short_oos']:+.2f} | maruz {q['expo']:.2f} | poz.değ/yıl {out['trades_per_yr']:.1f}"
          f" | pnl t tam {q['t_full']:+.2f} IS {q['t_is']:+.2f} OOS {q['t_oos']:+.2f} | yıllar+ {out['yrs_pos']}")
    return out

# ===================== C1 =====================
print("\n===== C1 USDTRY carry zamanlaması =====")
lfx = np.log(D.fx15); dl = lfx.diff()
bpd = np.log(D.u_settle / D.fx15) / D.u_dte.clip(lower=3)
sig_raw = dl.rolling(20).mean() - 1.4 * bpd
sig = sig_raw.shift(1)
# bilgi zamanı: sig_t = f(fx15 t-1 ve öncesi, u_settle t-1, u_dte t-1). Ham damgalar:
_, ts = duka_at("USDTRY", idx, 15, 1)
lagts = ts.shift(1)
print("  sig_t'deki en geç USDTRY spot damgası - (t 00:00):", (lagts - pd.Series(idx, index=idx)).max(), " (negatif => t-1 içinde)")
uf = {h: fwdsum(D.u_ret, h) for h in (1, 3, 5)}
for h in (1, 3, 5):
    s = ic_split(sig, uf[h], h); R[f"C1_ic_h{h}"] = s; print(f"  h={h}: {fmt(s)}")
pos1 = np.sign(sig).fillna(0.0)
strat("C1", pos1, D.u_ret, 1)
# roll günü: t'de alınan kontratı (a_t) t+1'de tut (OI t bilinmeden)
st = V[V.root == "USDTRY"].pivot_table(index="date", columns="code", values="settle", aggfunc="first").reindex(idx)
hold = pd.Series([np.log(st.iloc[i + 1][c] / st.iloc[i][c]) if i + 1 < len(idx) and pd.notna(st.iloc[i + 1].get(c, np.nan)) else np.nan for i, c in enumerate(D.u_code)], index=idx)
ret_hold = hold.shift(1).fillna(D.u_ret)  # ret_{t+1} = a_t kontratında
print("  a_t tut sürümü ile fark eden gün:", int(((ret_hold - D.u_ret).abs() > 1e-9).sum()))
strat("C1_hold_a_t", pos1, ret_hold, 1, costs=(5,))
print("  KKM: pos(2021-12-20) =", pos1.get(pd.Timestamp("2021-12-20")), " u_ret(2021-12-21) =", round(D.u_ret.get(pd.Timestamp("2021-12-21")) * 100, 2), "%")
for y in (2024, 2025, 2026):
    m = idx.year == y
    a = bt(pos1[m], D.u_ret[m], 1, 5); b = bt(pos1[m], D.u_ret[m], 1, 5, demean=True)
    print(f"  {y}: kısa oranı {(pos1[m] < 0).mean():.2f}, Sharpe {a['sharpe']:+.2f}, yıl içi demeaned {b['sharpe']:+.2f}")
# OOS demeaned: kâr yönü hep kısa ile karşılaştır
strat("C1_always_short", pd.Series(-1.0, index=idx), D.u_ret, 1, costs=(5,))
# OOS'u 2022-01..2023-05 ve 2023-06+ böl
for nm, m in [("2022-01..2023-05", (idx > IS_END) & (idx < "2023-06-01")), ("2023-06+", idx >= "2023-06-01")]:
    a = bt(pos1[m], D.u_ret[m], 1, 5); b = bt(pos1[m], D.u_ret[m], 1, 5, demean=True)
    print(f"  {nm}: Sharpe {a['sharpe']:+.2f}, demeaned {b['sharpe']:+.2f}, kısa oranı {(pos1[m] < 0).mean():.2f}")
# placebo: sinyali kaydır (negatif = gelecek)
print("  placebo IC (h=1):", {k: round(ic(sig.shift(k), uf[1], 1)["ic"], 3) for k in (-2, -1, 0, 1, 2, 3)})
# K sürümü (t 15:10) ile karşılaştırma
print("  K sürümü (shift yok) h=1:", fmt(ic_split(sig_raw, uf[1], 1)))
# bileşenler
print("  yalnız sürüklenme h=1:", fmt(ic_split(dl.rolling(20).mean().shift(1), uf[1], 1)))
print("  yalnız -taşıma   h=1:", fmt(ic_split(-bpd.shift(1), uf[1], 1)))
# XAUUSD'ye etkisi
xf = {h: fwdsum(D.x_ret, h) for h in (1, 3, 5)}
for h in (1, 3, 5): print(f"  carry sinyali -> XAUUSD fwd{h}:", fmt(ic_split(sig, xf[h], h)))

# ===================== C2 =====================
print("\n===== C2 USDTRY spot sürüklenme tahmini =====")
MAN = pd.Timestamp("2023-06-01")
cal = pd.Series(idx, index=idx)
for h in (1, 3, 5):
    y = lfx.shift(-h) - lfx
    fc = {"trail20": dl.rolling(20).mean() * h, "trail60": dl.rolling(60).mean() * h,
          "expanding_mean(rejim içi)": None, "basis_l1": bpd.shift(1) * (cal.shift(-h) - cal).dt.days}
    for reg, m in [("2017-03..2023-05", idx < MAN), ("2023-06+", idx >= MAN), ("2025-04+", idx >= "2025-04-01")]:
        yy = y[m]
        line = []
        for k, v in fc.items():
            if v is None:
                v = (dl[m].expanding(20).mean().shift(0) * h).reindex(idx)  # rejim içi genişleyen ortalama, t'de bilinen
            e = (yy - v[m]).dropna(); r2 = 1 - (e ** 2).mean() / (yy.reindex(e.index) ** 2).mean()
            line.append(f"{k} R2 {r2*100:+.1f}% (ort tahmin {v[m].reindex(e.index).mean()*1e4:.1f} bps)")
        print(f"  h={h} {reg}: gerçekleşen ort {yy.mean()*1e4:.1f} bps | " + " | ".join(line))
    s = ic(dl.rolling(20).mean(), y, h, idx >= MAN)
    yrs = pd.concat([dl.rolling(20).mean(), y], axis=1).dropna()[lambda z: z.index >= MAN]
    yr = yrs.groupby(yrs.index.year).apply(lambda g: g.iloc[:, 0].rank().corr(g.iloc[:, 1].rank()))
    R[f"C2_ic_h{h}"] = dict(s, by_year=yr.round(3).to_dict())
    print(f"  h={h} 2023-06+ IC {s['ic']:+.3f} t {s['t']:+.2f} n {s['n']}; yıllar {yr.round(3).to_dict()}")
    s0 = ic(dl.rolling(20).mean(), y, h, idx < MAN); print(f"      2017-03..2023-05 IC {s0['ic']:+.3f} t {s0['t']:+.2f}")

# ===================== C3 =====================
print("\n===== C3 gram prim ortalamaya dönüş =====")
pr = D.prem_vol
mu60 = pr.rolling(60, min_periods=20).mean(); sd60 = pr.rolling(60, min_periods=20).std()
dev = pr - mu60; z = dev / sd60
print("  eşleşen ay değişimi (prem_vol_ym) sayısı:", int((D.prem_vol_ym != D.prem_vol_ym.shift()).sum() - 1))
for h in (1, 3, 5):
    y = pr.shift(-h) - pr
    s = ic_split(dev.shift(1), y, h); R[f"C3_ic_h{h}"] = s; print(f"  dev(t-1)->Δprem h={h}: {fmt(s)}")
    # ay değişimi içermeyen pencereler
    same = pd.Series([len(set(D.prem_vol_ym.iloc[i:i + h + 1])) == 1 for i in range(len(idx))], index=idx)
    s2 = ic_split(dev.shift(1).where(same), y, h); print(f"       ay değişimi hariç: {fmt(s2)}")
    s3 = ic_split((D.prem_act - D.prem_act.rolling(60, min_periods=20).mean()).shift(1), D.prem_act.shift(-h) - D.prem_act, h); print(f"       prem_act (t-1 OI ayı): {fmt(s3)}")
res = (D.g_ret - D.x_ret - D.u_ret).fillna(0.0)
print("  corr(res, Δprem):", round(res.corr(pr.diff()), 3), " std res bps", round(res.std() * 1e4, 1))
for nm, zz in [("C3_l1", z.shift(1)), ("C3_K", z)]:
    pos = (-(zz > 1).astype(float) + (zz < -1).astype(float))
    g0 = bt_seg(pos, res, 3, 0); a = bt_seg(pos, res, 3, 15); dm = bt_seg(pos, res, 3, 15, demean=True)
    R[nm] = dict(gross_full=g0["full"]["sharpe"], net_full=a["full"]["sharpe"], net_IS=a["is"]["sharpe"], net_OOS=a["oos"]["sharpe"], OOS_dm=dm["oos"]["sharpe"],
                 OOS_nonet=a["oos"]["sharpe_nonet"], expo=a["full"]["expo"], tpy=tpy(pos))
    print(f"  {nm} h=3: brüt tam {g0['full']['sharpe']:+.2f} (OOS {g0['oos']['sharpe']:+.2f}) | net15 tam {a['full']['sharpe']:+.2f} IS {a['is']['sharpe']:+.2f} OOS {a['oos']['sharpe']:+.2f} (dm {dm['oos']['sharpe']:+.2f}; netleştirmesiz {a['oos']['sharpe_nonet']:+.2f}) | maruz {a['full']['expo']:.2f} | poz.değ/yıl {tpy(pos):.0f}")
    # Δprem hedefli (bacaksız, ideal sentetik) brüt
    gp = bt_seg(pos, (-(pr.diff())).fillna(0) * -1 * -1, 3, 0)

# ===================== C4 =====================
print("\n===== C4 dün USDTRY ↑ -> ons kısa =====")
u_l1 = D.u_ret.shift(1)
for h in (1, 3, 5):
    s = ic_split(u_l1, xf[h], h); R[f"C4_ic_h{h}"] = s; print(f"  h={h}: {fmt(s)}")
strat("C4", -np.sign(u_l1).fillna(0.0), D.x_ret, 3)

# ===================== C5 =====================
print("\n===== C5 TR şoku -> ons kısa =====")
usd_spot_1 = lfx.diff()
sh = (usd_spot_1.abs() > 0.025) | (D.xu_ret.shift(1) < -0.05)
print("  şok günü sayısı:", int(sh.sum()), " (fx:", int((usd_spot_1.abs() > 0.025).sum()), ", xu:", int((D.xu_ret.shift(1) < -0.05).sum()), ")")
HALF = pd.to_datetime(["2018-06-14", "2019-06-03", "2021-05-12", "2023-04-20", "2024-04-09", "2026-03-19", "2017-08-31", "2018-08-20", "2020-07-30", "2021-07-19", "2022-07-08",
                       "2023-06-27", "2025-06-05", "2026-05-26", "2019-10-28", "2020-10-28", "2021-10-28", "2022-10-28", "2024-10-28", "2025-10-28", "2026-10-28"])
# yarım günü veriyle doğrula: settle, 10:00 UTC spota mı 15:00'e mi yakın
x10, _ = duka_at("XAUUSD", idx, 10, 1); x15, _ = duka_at("XAUUSD", idx, 15, 1)
hd = pd.Series(idx.isin(HALF), index=idx)
print("  yarım gün doğrulama (medyan |ln(settle/spot)| bps): 10:00", round((np.log(D.x_settle / x10)).abs()[hd].median() * 1e4, 1), " 15:00", round((np.log(D.x_settle / x15)).abs()[hd].median() * 1e4, 1),
      "| normal gün 10:00", round((np.log(D.x_settle / x10)).abs()[~hd].median() * 1e4, 1), " 15:00", round((np.log(D.x_settle / x15)).abs()[~hd].median() * 1e4, 1))
shd = sh & hd
print("  şok günü olup yarım gün olanlar (15:00 bilgisi uzlaşmadan SONRA => ileriye bakar):", list(idx[shd].date), [round(usd_spot_1[d] * 100, 2) for d in idx[shd]])
f3 = xf[3]
for h in (1, 3, 5):
    e = (xf[h][sh] - xf[h].mean()).dropna()
    def tt(z): return z.mean() / z.std() * np.sqrt(len(z)) if len(z) > 2 else np.nan
    ei, eo = e[e.index <= IS_END], e[e.index > IS_END]
    # epizot kümeleme: 10 iş günü içindeki olaylar tek epizot
    ev = e.index; ep = np.cumsum(np.r_[1, (np.diff(np.searchsorted(idx, ev)) > 10).astype(int)])
    epm = e.groupby(ep).mean()
    print(f"  h={h}: n={len(e)} fazla ort {e.mean()*1e4:+.1f} bps naif t {tt(e):+.2f} | IS n={len(ei)} t {tt(ei):+.2f} | OOS n={len(eo)} t {tt(eo):+.2f} | epizot {len(epm)} t {tt(epm):+.2f}")
    R[f"C5_ev_h{h}"] = dict(n=len(e), ex_bps=e.mean() * 1e4, t=tt(e), t_is=tt(ei), t_oos=tt(eo), n_ep=len(epm), t_ep=tt(epm))
strat("C5", -sh.astype(float), D.x_ret, 3)
sh_nohalf = sh & ~hd
strat("C5_no_halfday", -sh_nohalf.astype(float), D.x_ret, 3, costs=(5,))
# OOS olaylarının listesi
oo = idx[sh & (idx > IS_END)]
print("  OOS şok günleri:", len(oo), "->", [str(d.date()) for d in oo])

# ===================== C6 =====================
print("\n===== C6 XAUTRYM OI değişimi -> ons =====")
oi = D.g_oi.replace(0, np.nan)
goi = np.log(oi).diff().shift(1)
for h in (1, 3, 5):
    s = ic_split(goi, xf[h], h); R[f"C6_ic_h{h}"] = s; print(f"  h={h}: {fmt(s)}")
# kontrat içi (roll'da çapraz kontrat farkı yok) ve toplam OI
Vg = V[V.root == "XAUTRYM"]
toi = Vg.groupby("date").oi.sum().reindex(idx).replace(0, np.nan)
oip = Vg.pivot_table(index="date", columns="code", values="oi", aggfunc="first").reindex(idx)
within = pd.Series([np.log(oip.iloc[i][c] / oip.iloc[i - 1][c]) if i > 0 and oip.iloc[i - 1].get(c, 0) > 0 and oip.iloc[i].get(c, 0) > 0 else np.nan for i, c in enumerate(D.g_code)], index=idx)
rollg = D.g_code != D.g_code.shift()
print("  analist tanımında roll günü (çapraz kontrat) |Δln OI| ort:", round(np.log(oi).diff()[rollg].abs().mean(), 3), " normal:", round(np.log(oi).diff()[~rollg].abs().mean(), 3))
for nm, x in [("kontrat içi Δln OI (t-1)", within.shift(1)), ("toplam OI Δln (t-1)", np.log(toi).diff().shift(1)), ("analist, roll günü t-1 hariç", goi.where(~rollg.shift(1).fillna(False).astype(bool)))]:
    s = ic_split(x, xf[3], 3); print(f"  h=3 {nm}: {fmt(s)}")
strat("C6", np.sign(goi).fillna(0.0), D.x_ret, 3)
strat("C6_total_oi", np.sign(np.log(toi).diff().shift(1)).fillna(0.0), D.x_ret, 3, costs=(5,))

json.dump(R, open(f"{OUT}/rep_results.json", "w"), default=lambda o: float(o) if isinstance(o, (np.floating, np.integer)) else str(o), indent=1)
