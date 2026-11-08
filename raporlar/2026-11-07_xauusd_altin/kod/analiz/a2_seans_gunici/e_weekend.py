"""(e) Hafta sonu boşluğu: Cuma son spot barı kapanışı (~21:00 UTC) -> Pazar ilk bar açılışı (~22:00/23:00 UTC).
Bilgi zamanı: Pazar ~22-23 UTC -> Pazartesi 15:00 UTC'den önce. Pazartesi davranışı ve haftanın günü etkisi (VİOP v_ret)."""
from a2_common import *
reset_families(["e_weekend"])
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
v = load_viop(); s = load_spot(); hb = hourly_bars()
# hafta sonu boşlukları: ardışık barlar arası > 24 saat
bt = hb.index.to_series(); dgap = bt.diff()
starts = bt[dgap > pd.Timedelta(hours=24)]
G = []
for t0 in starts.index:
    i = hb.index.get_loc(t0)
    prev = hb.iloc[i - 1]; cur = hb.iloc[i]
    G.append(dict(close_t=hb.index[i - 1] + pd.Timedelta(hours=1), open_t=t0, fri_close=prev.c, sun_open=cur.o))
G = pd.DataFrame(G)
G["gap"] = np.log(G.sun_open / G.fri_close)
G["mon"] = (G.open_t + pd.Timedelta(hours=3)).dt.tz_convert(None).dt.normalize()  # açılıştan sonraki ilk iş günü (Pazartesi)
G = G[G.close_t.dt.dayofweek == 4]  # yalnız Cuma kapanışı -> Pazar/Pzt açılışı
G = G.drop_duplicates("mon").set_index("mon")
print("hafta sonu sayısı:", len(G), " gap bps std:", round(G.gap.std() * 1e4, 1), " ort:", round(G.gap.mean() * 1e4, 2), " t:", round(mean_test(G.gap)["t"], 2))
print("kapanış saatleri:", G.close_t.dt.hour.value_counts().to_dict(), "açılış saatleri:", G.open_t.dt.hour.value_counts().to_dict())
G.to_csv(f"{OUT}/e_weekend_gaps.csv")
sv = segments(v); ss = segments(s)
def attach(df, seg):
    o = pd.DataFrame(index=df.index)
    o["gap"] = G.gap.reindex(df.index)
    o["mon_rest"] = np.log(df.xau_p15 / G.sun_open.reindex(df.index))   # Pazar açılışı -> Pzt 15:00
    o["mon_day"] = seg.C_day                                             # Pzt 07:00 -> 15:00 (VİOP 06:30 açılışından uzlaşmaya uygulanabilir)
    o["fri_aft"] = seg.S1_eve                                            # Cuma 15:00 -> 20:00
    o["wkend_tot"] = seg.C_post                                          # Cuma 15:00 -> Pzt 00:00
    o.loc[o.index.dayofweek != 0] = np.nan
    return o
W = attach(v, sv); Ws = attach(s, ss)
rows = []
for h in (1, 3, 5):
    rows.append(test("e_weekend", f"e_gap_fwd_h{h}", "gap (Pzt satırı)", W.gap, v[f"fwd{h}"], h, "yalnız Pazartesi"))
    rows.append(test("e_weekend", f"e_wkendtot_fwd_h{h}", "Cuma15->Pzt00", W.wkend_tot, v[f"fwd{h}"], h, "yalnız Pazartesi"))
# gün içi: gap -> Pzt 07->15 (VİOP sabah açılış -> uzlaşma; kapanıştan kapanışa değil)
st = split_stats(Ws.gap, Ws.mon_day, 1); register(AGENT, "e_weekend", "e_gap_to_monday_day", "gap->Pzt 07-15", 0, st, "gün içi; spot 2010-26")
rows.append(dict(family="e_weekend", test_id="e_gap_to_monday_day", predictor="gap -> Pzt 07->15 (gün içi, spot 2010+)", h=0, n=st["n"], ic=round(st["ic"], 4), t=round(st["t"], 2),
                 ic_is=round(st["ic_is"], 4), t_is=round(st["t_is"], 2), ic_oos=round(st["ic_oos"], 4), t_oos=round(st["t_oos"], 2), yrs=f'{st["yrs_same_sign"]}/{st["yrs"]}'))
st = split_stats(Ws.fri_aft, Ws.gap, 1); register(AGENT, "e_weekend", "e_friaft_to_gap", "Cuma öğleden sonra->gap", 0, st, "spot 2010-26")
rows.append(dict(family="e_weekend", test_id="e_friaft_to_gap", predictor="Cuma 15-20 -> gap (spot 2010+)", h=0, n=st["n"], ic=round(st["ic"], 4), t=round(st["t"], 2),
                 ic_is=round(st["ic_is"], 4), t_is=round(st["t_is"], 2), ic_oos=round(st["ic_oos"], 4), t_oos=round(st["t_oos"], 2), yrs=f'{st["yrs_same_sign"]}/{st["yrs"]}'))
R = pd.DataFrame(rows); R.to_csv(f"{OUT}/e_weekend_ic.csv", index=False); print(R.drop(columns=["family", "test_id", "note"], errors="ignore").to_string())
# erken dönem: gap -> sfwd (spot 2010-2016)
for h in (1, 3, 5):
    m = Ws.index < "2017-01-01"; e = ic(Ws.gap[m], s[f"sfwd{h}"][m], max(h, 5))
    register(AGENT, "e_weekend", f"e_early_gap_h{h}", "gap", h, e, "spot 2010-2016")
    print(f"erken 2010-16 gap->sfwd{h}: ic {e['ic']:.4f} t {e['t']:.2f} n {e['n']}")
# haftanın günü: VİOP v_ret ortalaması (gün t getirisi = t-1 uzlaşma -> t uzlaşma)
r = v.v_ret; dw = r.index.dayofweek; names = ["Pzt", "Sal", "Çar", "Per", "Cum"]
D = []
for d in range(5):
    x = r[dw == d] - r.mean()   # gün etkisi = o günün ortalaması - genel ortalama (drift çıkarılmış)
    fm = mean_test(r[dw == d]); dm = mean_test(x); ism = mean_test(x[x.index <= IS_END]); oom = mean_test(x[x.index > IS_END])
    ys = (r[dw == d].groupby(r[dw == d].index.year).mean() - r.groupby(r.index.year).mean())
    xs = s.s_ret[s.index.dayofweek == d]; es = mean_test(xs[xs.index < "2017-01-01"] - s.s_ret[s.index < "2017-01-01"].mean())
    register(AGENT, "e_weekend", f"e_dow_{names[d]}", f"DOW {names[d]} - ort", 0, dict(ic=dm["mean"], t=dm["t"], n=dm["n"], t_is=ism["t"], t_oos=oom["t"], ic_oos=oom["mean"],
             yrs_same_sign=int((np.sign(ys) == np.sign(dm["mean"])).sum()), yrs=len(ys)), "VİOP v_ret gün etkisi (drift çıkarılmış)")
    D.append(dict(gun=names[d], ort_bps=round(fm["mean"] * 1e4, 2), t_ham=round(fm["t"], 2), fark_bps=round(dm["mean"] * 1e4, 2), t_fark=round(dm["t"], 2),
                  t_is=round(ism["t"], 2), t_oos=round(oom["t"], 2), yil_ayni=f'{int((np.sign(ys) == np.sign(dm["mean"])).sum())}/{len(ys)}',
                  spot1016_fark_bps=round(es["mean"] * 1e4, 2), spot1016_t=round(es["t"], 2), n=fm["n"]))
D = pd.DataFrame(D); D.to_csv(f"{OUT}/e_dow.csv", index=False); print("\nHaftanın günü (VİOP v_ret):\n", D.to_string())
# hafta sonu tutma stratejisi: Cuma uzlaşmada al, Pzt uzlaşmada sat (h=1, yalnız Cuma pozisyon)
pos = pd.Series((v.index.dayofweek == 4).astype(float), index=v.index)
L = legs(pos, v.v_ret, 1); df = fmt_legs(L); df.to_csv(f"{OUT}/e_weekend_hold_bt.csv", index=False); print("\nCuma al -> Pzt sat:\n", df[df.leg == "both"].to_string())
# Pazartesi segment ayrıştırması (bps): Cuma 15->20, Cuma 20->Pzt 00 (gap dahil), Pzt Asya, Londra, NY
seg_m = ss[SEGS][ss.index.dayofweek == 0]; seg_o = ss[SEGS][ss.index.dayofweek != 0]
print("\nPzt segment ort (bps):", (seg_m.mean() * 1e4).round(2).to_dict(), "\nDiğer günler:", (seg_o.mean() * 1e4).round(2).to_dict())
gm = G.gap; print("gap yıl yıl ort bps:", (gm.groupby(gm.index.year).mean() * 1e4).round(1).to_dict())
