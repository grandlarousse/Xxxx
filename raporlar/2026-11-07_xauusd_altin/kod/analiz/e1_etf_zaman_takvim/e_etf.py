"""(e) Hangi ETF? Gider oranı (yayımlanmış, yaklaşık), likidite (dolar hacim), spread tahmini (Abdi-Ranaldo 2017, günlük H/L/C),
spot altına (Dukascopy 16:00 ET = xau_close) iz sürme: günlük korelasyon, iz sürme hatası, yıllık iz sürme farkı; 1/3/5 günlük sapma.
Not: xau_close Dukascopy BID saatlik barından; ETF kapanışı 16:00 ET resmî kapanış (kapanış müzayedesi)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e1_etf_zaman_takvim")
from e1_common import *
reset("e_")
pd.set_option("display.width", 250)
# yayımlanmış gider oranları (%, yaklaşık; ihraççı sayfalarından bellek — DOĞRULANMADI, kullanıcı kontrol etmeli)
ER = {"GLD": 0.40, "IAU": 0.25, "GLDM": 0.10, "SGOL": 0.17, "BAR": 0.1749, "AAAU": 0.18, "GDX": 0.51, "GDXJ": 0.51, "SLV": 0.50,
      "UGL": 0.95, "GLL": 0.95, "AGQ": 0.95, "ZSL": 0.95, "NUGT": 1.0, "DUST": 1.0, "JNUG": 1.0, "JDST": 1.0}
rows = []
xs = np.log(D.xau_close).diff()
for t in ["GLD", "IAU", "GLDM", "SGOL", "BAR", "AAAU", "GDX", "GDXJ", "SLV", "UGL", "GLL", "NUGT", "DUST", "JNUG", "JDST", "AGQ", "ZSL"]:
    y = yahoo(t).reindex(IDX)
    last = y[y.index >= IDX[-1] - pd.Timedelta(days=365)].dropna()
    dv = (last.close * last.volume)
    # Not: Abdi-Ranaldo (günlük H/L/C) bu likiditede oynaklığı ölçüyor (tüm altın ETF'lerinde ~61 bps) -> kullanılmadı. Roll (5 dk) aşağıda.
    o = dict(etf=t, gider_orani_pct=ER.get(t), fiyat_usd=round(last.close.iloc[-1], 2), medyan_gunluk_dolar_hacim_mn=round(dv.median() / 1e6, 1),
             tick_spread_1cent_bps=round(0.01 / last.close.median() * 1e4, 2),
             gunluk_tutma_maliyeti_bps=round(ER.get(t, np.nan) / 252 * 100, 3))
    if t in ("GLD", "IAU", "GLDM", "SGOL", "BAR", "AAAU"):
        d = pd.concat([R[t], xs], axis=1, keys=["e", "x"]).dropna()
        d = d[d.index >= "2018-09-01"]  # ortak dönem (AAAU/GLDM sonrası)
        o.update(kor_spot_gunluk=round(d.e.corr(d.x), 5), iz_hatasi_yillik_pct=round((d.e - d.x).std() * np.sqrt(252) * 100, 2),
                 iz_farki_yillik_pct=round((d.e - d.x).mean() * 252 * 100, 2))
        for h in [1, 3, 5]:
            g = np.arange(len(d)) // h; eh = d.e.groupby(g).sum(); xh = d.x.groupby(g).sum()
            o[f"sapma_std_h{h}_bps"] = round((eh - xh).std() * 1e4, 1)
    rows.append(o)
# Roll (1984) tahmini, 5 dk normal seans kapanışları (son 60 gün): kotasyon farkı + kısa vadeli fiyat etkisi -> ÜST SINIR
for o in rows:
    f5 = f"{S}/panel/yahoo_5m/{o['etf']}.parquet"
    if not os.path.exists(f5): continue
    m = pd.read_parquet(f5); m.index = pd.to_datetime(m.index); e = m.index.tz_convert("America/New_York"); hm = e.strftime("%H:%M")
    k = (hm >= "09:35") & (hm < "15:55"); m = m[k]; dd = e[k].normalize()
    r = np.log(m.close).groupby(dd).diff(); q = pd.concat([r, r.groupby(dd).shift(1)], axis=1).dropna(); c_ = np.cov(q.iloc[:, 0], q.iloc[:, 1])[0, 1]
    o["roll_5dk_ust_sinir_bps"] = round(2 * np.sqrt(-c_) * 1e4, 1) if c_ < 0 else None
E = pd.DataFrame(rows); E.to_csv(f"{O}/e_etf_secim.csv", index=False); print(E.to_string())
# yıllık iz sürme farkı GLD/IAU/GLDM vs spot (16:00 ET)
yr = []
for t in ["GLD", "IAU", "GLDM", "SGOL"]:
    d = pd.concat([R[t], xs], axis=1, keys=["e", "x"]).dropna()
    g = d.groupby(d.index.year).apply(lambda q: pd.Series(dict(etf_pct=np.expm1(q.e.sum()) * 100, spot_pct=np.expm1(q.x.sum()) * 100, fark_log_pct=(q.e - q.x).sum() * 100, n=len(q))))
    g["etf"] = t; yr.append(g.reset_index())
YR = pd.concat(yr); YR.to_csv(f"{O}/e_yillik_iz_farki.csv", index=False)
print(YR.pivot_table(index="date", columns="etf", values="fark_log_pct").round(2).to_string())
# GLD - IAU - GLDM günlük getiri farkı (aynı kapanış anı)
d = pd.DataFrame({t: R[t] for t in ["GLD", "IAU", "GLDM"]}).dropna()
print("günlük fark std (bps): GLD-IAU", round((d.GLD - d.IAU).std() * 1e4, 2), " GLD-GLDM", round((d.GLD - d.GLDM).std() * 1e4, 2), " IAU-GLDM", round((d.IAU - d.GLDM).std() * 1e4, 2))
# GLD kapanış primi (t-1, NAV LBMA PM'e göre) -> sonraki getiri (iz sürme farkı dönüşü mü?)
prem = (np.log(D.c_GLD) - np.log(D.flow_gld_nav_t)).shift(1)   # t-1 kapanış/NAV_{t-1}; NAV t-1 akşam yayımlanır -> gün t'de bilinir
for h in [1, 3]:
    st = split_stats(prem, fwd(R.GLD, h), h); reg("e_prem", f"e_prem|GLD|h{h}", "GLD kapanış/NAV primi t-1", h, st, "prim = LBMA PM -> 16:00 ET altın hareketi + gürültü")
    print("GLD prim t-1 -> fwd", h, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in st.items() if k != "by_year"})
