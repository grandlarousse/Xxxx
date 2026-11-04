"""(d) ABD makro günleri / FOMC: kapanışta tutulan pozisyonun 1-3 günlük RİSK/getiri profili (alfa değil).
Pencere tanımı (karar BIST kapanışında):
  FOMC (18:00/19:00 UTC, BIST kapanışından SONRA): FOMC günü t uzlaşması -> t+h (tepki t+1'de).
  NFP/CPI (12:30/13:30 UTC, BIST seansı İÇİNDE): t-1 uzlaşması -> t-1+h (olay günü t pencerenin içinde).
NFP tarihleri 2023-12 öncesi BLS kuralıyla üretildi (12'sini içeren haftadan sonraki 3. Cuma); CPI yalnız 2023-12+ (dosyadan).
Karşılaştırma: olay pencereleri vs diğer tüm pencereler: std oranı (bootstrap p), ortalama farkı, |r|>2σ sıklığı, en kötü %5.
Ayrıca: 'olay penceresinde pozisyonu yarıya indir' kuralının uzun XU030 için yıllık getiri/oynaklık/MaxDD etkisi.
"""
import numpy as np, pandas as pd, klib as K
F = K.fut_panel(); Sp = K.spot_panel()
o = pd.read_csv(K.S + "/out/olay_tarihleri.csv"); o["date"] = pd.to_datetime(o["date"])
fomc = o[(o["type"] == "FOMC") & (o["timing"] == "after_close")]["date"]
cpi = o[(o["type"] == "USDATA") & (o["sub"] == "CPI")]["date"]
nfp_f = o[(o["type"] == "USDATA") & (o["sub"] == "NFP")]["date"]
def nfp_rule(y, m):
    d12 = pd.Timestamp(y, m, 12); sat = d12 + pd.Timedelta(days=(5 - d12.weekday()) % 7)  # haftayı bitiren Cumartesi
    fr = sat + pd.Timedelta(days=6); return fr + pd.Timedelta(days=14)              # 3. Cuma
nfp_r = []
for y in range(2014, 2024):
    for m in range(1, 13):
        d = nfp_rule(y, m) if m < 12 else nfp_rule(y, 12)
        nfp_r.append(d)
nfp = pd.DatetimeIndex(sorted(set([d for d in nfp_r if d < pd.Timestamp("2023-12-01")] + list(nfp_f))))
EV = {"FOMC": (pd.DatetimeIndex(fomc), "after"), "NFP": (nfp, "in"), "CPI": (pd.DatetimeIndex(cpi), "in")}
def windows(R, dates, kind, h):
    cal = R.dropna().index; y = K.fwd(R, h)
    ent = []
    for d in dates:
        if kind == "after":
            i = cal.searchsorted(d, side="right") - 1      # olay günü (ya da öncesi son BIST günü) uzlaşması
        else:
            i = cal.searchsorted(d, side="left") - 1       # olay gününden önceki uzlaşma
        if i >= 0: ent.append(cal[i])
    ent = pd.DatetimeIndex(sorted(set(ent)))
    return y, ent
rows = []
rng = np.random.default_rng(11)
insts = [("F_XU030", F["XU030"], "2017-03-06"), ("XU100_spot", Sp["XU100"], "2014-01-01")] + [(s, F[s], "2017-03-06") for s in K.STOCKS]
for ev, (dates, kind) in EV.items():
    for nm, R, st in insts:
        R = R[R.index >= st]
        for h in (1, 2, 3):
            y, ent = windows(R, dates, kind, h)
            y = y.dropna(); e = y.reindex(ent).dropna(); ne = y.drop(e.index, errors="ignore")
            # diğer olay pencerelerini kontrol grubundan çıkar
            if len(e) < 8: continue
            sd_e, sd_n = e.std(), ne.std(); ratio = sd_e / sd_n
            pool = ne.values
            if nm in ("F_XU030", "XU100_spot", "THYAO", "AKBNK", "GARAN"):
                bs = np.array([np.std(rng.choice(pool, len(e)), ddof=1) for _ in range(3000)]) / sd_n
                p_hi = (bs >= ratio).mean(); p_lo = (bs <= ratio).mean(); p = 2 * min(p_hi, p_lo)
            else:
                # F-testi yaklaşığı (normal varsayımı yok -> log-std farkı, Fisher)
                from scipy import stats
                z = np.log(ratio) / np.sqrt(1 / (2 * (len(e) - 1)) + 1 / (2 * (len(ne) - 1)))
                k_e = stats.kurtosis(e); z = z / np.sqrt(max(1 + k_e / 2, 1)); p = 2 * (1 - stats.norm.cdf(abs(z)))
            mdiff = (e.mean() - ne.mean()) * 1e4; tm = mdiff / 1e4 / np.sqrt(e.var() / len(e) + ne.var() / len(ne))
            rows.append(dict(event=ev, inst=nm, h=h, n=len(e), sd_ev_bps=sd_e * 1e4, sd_other_bps=sd_n * 1e4, ratio=ratio, p_ratio=p,
                             mean_ev_bps=e.mean() * 1e4, mean_other_bps=ne.mean() * 1e4, t_mean=tm,
                             big2s_ev=(e.abs() > 2 * sd_n).mean(), big2s_other=(ne.abs() > 2 * sd_n).mean(),
                             q05_ev_bps=e.quantile(0.05) * 1e4, q05_other_bps=ne.quantile(0.05) * 1e4,
                             IS_ratio=e[e.index < "2022-01-01"].std() / ne[ne.index < "2022-01-01"].std() if (e.index < "2022-01-01").sum() > 5 else np.nan,
                             OOS_ratio=e[e.index >= "2022-01-01"].std() / ne[ne.index >= "2022-01-01"].std() if (e.index >= "2022-01-01").sum() > 5 else np.nan))
D = pd.DataFrame(rows); D.to_csv(K.RES + "/d_macro.csv", index=False)
pd.set_option("display.width", 250)
print(D[D["inst"].isin(["F_XU030", "XU100_spot"])].round(3).to_string())
st = D[~D["inst"].isin(["F_XU030", "XU100_spot"])].groupby(["event", "h"]).agg(n_stock=("inst", "count"), med_ratio=("ratio", "median"),
      share_gt1=("ratio", lambda x: (x > 1).mean()), med_mean_ev=("mean_ev_bps", "median"), med_mean_oth=("mean_other_bps", "median"),
      med_t=("t_mean", "median"))
print(st.round(3))
p = D["p_ratio"].values; rej, pa = K.bh(p); D["q_ratio"] = pa; print("std oranı FDR geçen:", rej.sum(), "/", len(D))
print(D[rej][["event", "inst", "h", "n", "ratio", "p_ratio", "q_ratio"]].round(3).to_string())
p = K.t2p(D["t_mean"]); rej, pa = K.bh(p); print("ortalama farkı FDR geçen:", rej.sum())
# yarıya indirme kuralı: uzun F_XU030 (her gün 1 birim, olay pencerelerinde 0,5) — günlük getiriyle
R = F["XU030"].dropna(); out = []
for ev, (dates, kind) in list(EV.items()) + [("FOMC+NFP+CPI", (None, None))]:
    for h in (1, 2, 3):
        w = pd.Series(1.0, index=R.index)
        evs = [ev] if ev != "FOMC+NFP+CPI" else ["FOMC", "NFP", "CPI"]
        for e_ in evs:
            dd, kk = EV[e_]; _, ent = windows(R, dd, kk, h)
            for d in ent:
                i = R.index.get_loc(d)
                w.iloc[i + 1:i + 1 + h] = 0.5   # pozisyon uzlaşma d'de azaltılır -> d+1..d+h günlerinin getirisine 0,5 ağırlık
        pnl_full = R; pnl_half = R * w - (1 - w).diff().abs().fillna(0) * 2.5e-4 * 0.5  # yarım pozisyon değişimi başına ~2,5 bps (tek yön)
        for lab, pnl in (("tam", pnl_full), ("olayda_yarım", pnl_half)):
            eq = pnl.cumsum(); dd_ = (eq - eq.cummax()).min()
            out.append(dict(event=ev, h=h, rule=lab, ann_ret_pct=pnl.mean() * 252 * 100, ann_vol_pct=pnl.std() * np.sqrt(252) * 100,
                            sharpe=pnl.mean() / pnl.std() * np.sqrt(252), maxdd_pct=dd_ * 100, worst_day_bps=pnl.min() * 1e4,
                            share_days_reduced=(w < 1).mean()))
H = pd.DataFrame(out); H.to_csv(K.RES + "/d_halfrule.csv", index=False); print(H.round(3).to_string())
