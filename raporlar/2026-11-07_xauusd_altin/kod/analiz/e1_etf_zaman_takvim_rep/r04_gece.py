"""4) C6: gece (kapanış t-1 -> açılış t) / gün içi (açılış t -> kapanış t) ayrışımı, CO stratejisi, başabaş, açılış dolumu.
Gece log = log(adj_t/adj_{t-1}) - log(close_t/open_t) (temettü gece bacağında). Yahoo open = resmî açılış baskısı."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e1_etf_zaman_takvim_rep")
from rep_lib import *
pd.set_option("display.width", 250)

def nd(t):
    y = yahoo(t).reindex(SESS)
    tot = np.log(y.adjclose).diff()
    intra = np.log(y.close / y.open)
    night = tot - intra
    # alternatif: ham fiyatla (temettüsüz) gece
    night_raw = np.log(y.open / y.close.shift(1))
    return night, intra, tot, night_raw, y

def mean_t(s, L=5):
    s = s.dropna()
    if len(s) < 100: return np.nan, np.nan
    b, t = nw_ols(s.values, np.ones((len(s), 0)), L, add_const=True)
    return s.mean() * 252 * 100, t[0]

rows, yr, be, strat = [], [], [], []
for t in ["GLD", "IAU", "GLDM", "GDX", "GDXJ", "SLV", "NUGT", "JNUG"]:
    n, d, tot, nr, y = nd(t)
    # veri kalitesi: açılış = önceki kapanış, açılış = kapanış, aralıksız bar
    q = y.dropna(subset=["open"])
    dq = dict(etf=t, n=len(q), open_eq_prevclose=int((q.open == q.close.shift(1)).sum()), open_eq_close=int((q.open == q.close).sum()),
              hl_zero=int((q.high == q.low).sum()), open_outside_hl=int(((q.open > q.high * 1.0001) | (q.open < q.low * 0.9999)).sum()))
    print("veri kalitesi", dq)
    for nm, s in [("gece", n), ("gun_ici", d), ("gece_hamfiyat", nr)]:
        o = dict(etf=t, seg=nm)
        for k in PERIODS:
            a, tt = mean_t(per(s, k)); o[f"ann_{k}"] = round(a, 2) if pd.notna(a) else None; o[f"t_{k}"] = round(tt, 2) if pd.notna(tt) else None
        ym_ = s.dropna().groupby(s.dropna().index.year).mean()
        o["yrs_pos"] = f"{int((ym_ > 0).sum())}/{len(ym_)}"
        rows.append(o)
    yy = pd.DataFrame({"gece": n.groupby(n.index.year).sum() * 100, "gun_ici": d.groupby(d.index.year).sum() * 100, "toplam": tot.groupby(tot.index.year).sum() * 100})
    yy["etf"] = t; yr.append(yy)
    # CO: kapanışta al, açılışta sat (her gün bir gidiş-dönüş), OC: açılışta al kapanışta sat
    co = np.expm1(n); oc = np.expm1(d); bh = np.expm1(tot)
    for c in [0, 5, 10, 20]:
        for k in PERIODS:
            for nm_, s_ in [("CO", co), ("OC", oc)]:
                p = per(s_.dropna(), k) - c / 1e4
                strat.append(dict(etf=t, strateji=nm_, cost_bps=c, period=k, **perf(p)))
            if c == 0:
                strat.append(dict(etf=t, strateji="al_tut", cost_bps=0, period=k, **perf(per(bh.dropna(), k))))
    # drift çıkarılmış CO: gece getirisinden tam örneklem toplam günlük ortalama çıkarılır (gece bacağının "ekstra" kısmı)
    for k in PERIODS:
        tt_ = per(bh.dropna(), k); co_k = per(co.dropna(), k)
        strat.append(dict(etf=t, strateji="CO_demeaned(gece - gunluk_ort)", cost_bps=10, period=k, **perf(co_k - tt_.mean() - 10 / 1e4)))
        strat.append(dict(etf=t, strateji="CO_demeaned(gece - gece_ort)", cost_bps=10, period=k, **perf(co_k - co_k.mean() - 10 / 1e4)))
    be.append(dict(etf=t, **{f"basabas_bps_{k}": round(per(co.dropna(), k).mean() * 1e4, 2) for k in PERIODS}))

M = pd.DataFrame(rows); M.to_csv(f"{OUT}/r04_gece_ortalama.csv", index=False); print(M.to_string())
Y = pd.concat(yr); Y.to_csv(f"{OUT}/r04_yillik_gece.csv")
for t in ["GLD", "GDX"]:
    print(t); print(Y[Y.etf == t][["gece", "gun_ici", "toplam"]].round(1).T.to_string())
g = Y[Y.etf == "GLD"]; print("GLD gece>0 yıl:", int((g.gece > 0).sum()), "/", len(g), " gece>gün içi:", int((g.gece > g.gun_ici).sum()))
B = pd.DataFrame(be); B.to_csv(f"{OUT}/r04_basabas.csv", index=False); print(B.to_string())
ST = pd.DataFrame(strat); ST.to_csv(f"{OUT}/r04_CO_OC.csv", index=False)
print(ST[ST.period.isin(["full", "oos", "p22"])].pivot_table(index=["etf", "strateji", "cost_bps"], columns="period", values=["ann", "sh"], aggfunc="first").round(2).to_string())

# ---- açılış dolumu gerçekçiliği: 5 dk veri (son 60 gün), saatlik (730 gün)
print("\nAçılış dolumu")
fl = []
for t in ["GLD", "GDX", "GDXJ", "NUGT", "SLV", "IAU"]:
    m = pd.read_parquet(f"{S}/panel/yahoo_5m/{t}.parquet"); m.index = pd.to_datetime(m.index)
    e = m.index.tz_convert("America/New_York"); m["d"] = e.normalize().tz_localize(None); m["hm"] = e.strftime("%H:%M")
    b930 = m[m.hm == "09:30"].set_index("d"); b935 = m[m.hm == "09:35"].set_index("d")
    yy = yahoo(t)
    q = pd.DataFrame({"o_daily": yy.open, "pc": yy.close.shift(1)}).reindex(b930.index)
    q["o5"] = b930.open; q["c5"] = b930.close; q["o935"] = b935.open.reindex(q.index); q = q.dropna()
    fl.append(dict(etf=t, n=len(q), bas=str(q.index.min().date()), bit=str(q.index.max().date()),
                   abs_c0935_vs_dailyopen_bps=round(np.log(q.c5 / q.o_daily).abs().mean() * 1e4, 1),
                   abs_first5open_vs_dailyopen_bps=round(np.log(q.o5 / q.o_daily).abs().mean() * 1e4, 1),
                   signed_c0935_vs_dailyopen_bps=round(np.log(q.c5 / q.o_daily).mean() * 1e4, 1),
                   abs_gece_bps=round(np.log(q.o_daily / q.pc).abs().mean() * 1e4, 1),
                   median_abs_c0935_bps=round(np.log(q.c5 / q.o_daily).abs().median() * 1e4, 1)))
FL = pd.DataFrame(fl); FL.to_csv(f"{OUT}/r04_dolum.csv", index=False); print(FL.to_string())

# saatlik: gece getirisi resmi açılışa kadar vs 10:30 ET'ye kadar (son 730 gün)
hr = []
for t in ["GLD", "GDX", "GDXJ", "NUGT"]:
    hh = pd.read_parquet(f"{S}/panel/yahoo_h/{t}.parquet"); hh.index = pd.to_datetime(hh.index)
    e = hh.index.tz_convert("America/New_York"); hh["d"] = e.normalize().tz_localize(None); hh["hm"] = e.strftime("%H:%M")
    f = hh[hh.hm == "09:30"].set_index("d")
    yy = yahoo(t); q = pd.DataFrame({"pc": yy.close.shift(1), "o": yy.open}).reindex(f.index); q["c1030"] = f.close; q = q.dropna()
    hr.append(dict(etf=t, n=len(q), gece_resmi_acilis_bps=round(np.log(q.o / q.pc).mean() * 1e4, 2), gece_1030_bps=round(np.log(q.c1030 / q.pc).mean() * 1e4, 2)))
print(pd.DataFrame(hr).to_string())
