"""Bağımsız takvimler: spot günlük seri, NFP (BLS arşiv HTML'inden kendi ayrıştırmam), OG vadesi (kendi kuralım + kendi NYSE takvimim),
Ramazan/Kurban bayramı (Diyanet tarihleri, bellekten; VİOP boşluklarıyla doğrulanır), TR yarım günleri (ampirik tespit)."""
import re, numpy as np, pandas as pd
from dateutil.easter import easter
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
O = f"{S}/out/a3_takvim_olay_rep"
B = pd.read_parquet(f"{O}/base.parquet"); V = B.index

# ---------- spot günlük (Dukascopy saatlik; fiyat anı = bar başı + 1 saat) ----------
H = pd.read_parquet(f"{S}/panel/duka/XAUUSD.parquet"); H.index = H.index.tz_convert(None)
cl = H["c"].copy(); cl.index = cl.index + pd.Timedelta(hours=1)
wd = pd.bdate_range("2010-01-04", "2026-11-06")
SP = pd.DataFrame(index=wd)
for hh in (7, 10, 12, 13, 14, 15, 20):
    SP[f"p{hh:02d}"] = cl.reindex(wd + pd.Timedelta(hours=hh)).values
SP = SP[SP.p15.notna()]
SP["s_ret"] = np.log(SP.p15 / SP.p15.shift(1))
for h in (1, 3, 5):
    SP[f"sfwd{h}"] = sum(SP.s_ret.shift(-k) for k in range(1, h + 1))
print("spot günleri:", len(SP), SP.index[0].date(), SP.index[-1].date(), " yıl başına:", SP.groupby(SP.index.year).size().to_dict())
PS = pd.read_parquet(f"{S}/panel/panel_spot.parquet"); PS.index = pd.to_datetime(PS.index)
j = SP.index.intersection(PS.index)
print("panel_spot ile: ben", len(SP), "panel", len(PS), "ortak", len(j), " s_ret max|fark|", float((SP.s_ret.reindex(j) - PS.s_ret.reindex(j)).abs().max()),
      " sfwd3 max|fark|", float((SP.sfwd3.reindex(j) - PS.sfwd3.reindex(j)).abs().max()))
SP.to_parquet(f"{O}/spot_daily.parquet")

# ---------- NFP: BLS arşiv sayfasındaki empsit_MMDDYYYY bağlantıları ----------
html = open(f"{S}/out/a3_takvim_olay/dl/bls_empsit.htm", encoding="utf-8", errors="ignore").read()
nfp = sorted(set(pd.to_datetime(m, format="%m%d%Y") for m in re.findall(r"empsit_(\d{8})\.(?:htm|pdf)", html)))
nfp = pd.DatetimeIndex([d for d in nfp if d <= pd.Timestamp("2026-11-06")])
print("NFP yayım sayısı (≤2026-11-06):", len(nfp), " hafta günü dağılımı:", pd.Series(nfp.dayofweek).value_counts().to_dict())
an = pd.read_csv(f"{S}/out/a3_takvim_olay/events_us_nfp.csv", parse_dates=["date"])
an = pd.DatetimeIndex(an.date[an.date <= "2026-11-06"])
print("  analist listesiyle fark: bende olup onda olmayan", sorted(set(nfp) - set(an))[:10], " onda olup bende olmayan", sorted(set(an) - set(nfp))[:10])
# bağımsız ikinci kontrol: yayım saatinde (12:30/13:30 UTC) spot hareketi büyük mü
us_dst = lambda d: (d >= pd.Timestamp(d.year, 3, 8) + pd.offsets.Week(weekday=6) * 0) and False
def is_us_dst(d):
    # 2007+: Mart'ın 2. Pazarı → Kasım'ın 1. Pazarı
    m = pd.Timestamp(d.year, 3, 1); s = m + pd.Timedelta(days=(6 - m.dayofweek) % 7 + 7)
    n = pd.Timestamp(d.year, 11, 1); e = n + pd.Timedelta(days=(6 - n.dayofweek) % 7)
    return s <= d < e
absr = np.log(cl / cl.shift(1)).abs()
def rel_move(d):
    hh = 13 if is_us_dst(d) else 14   # 12:30 yayımı -> 12:00-13:00 barı (anı 13:00) ; 13:30 -> 13:00-14:00 (anı 14:00)
    v = absr.get(d + pd.Timedelta(hours=hh), np.nan)
    ref = absr.reindex([d - pd.Timedelta(days=k) + pd.Timedelta(hours=hh) for k in range(7, 50, 7)]).median()
    return v / ref
rm = pd.Series([rel_move(d) for d in nfp if d >= pd.Timestamp("2010-01-01")], index=[d for d in nfp if d >= pd.Timestamp("2010-01-01")])
print("  NFP yayım barında |getiri| / aynı saat önceki haftalar medyanı: medyan oran", round(rm.median(), 2), " oran<1 olan yayım:", int((rm < 1).sum()), "/", rm.notna().sum())
pd.Series(nfp, name="date").to_csv(f"{O}/cal_nfp.csv", index=False)

# ---------- NYSE tatilleri (kendi kuralım) ----------
def nyse_holidays(y0=2008, y1=2027, special=True):
    out = set()
    for y in range(y0, y1 + 1):
        def obs(d, sat_to_fri=True):
            if d.dayofweek == 5: return d - pd.Timedelta(days=1) if sat_to_fri else None
            if d.dayofweek == 6: return d + pd.Timedelta(days=1)
            return d
        def nth(month, wd_, n):
            f = pd.Timestamp(y, month, 1); f = f + pd.Timedelta(days=(wd_ - f.dayofweek) % 7); return f + pd.Timedelta(weeks=n - 1)
        def last(month, wd_):
            l = pd.Timestamp(y, month, 1) + pd.offsets.MonthEnd(0); return l - pd.Timedelta(days=(l.dayofweek - wd_) % 7)
        ny = obs(pd.Timestamp(y, 1, 1), sat_to_fri=False)
        if ny is not None: out.add(ny)
        out |= {nth(1, 0, 3), nth(2, 0, 3), pd.Timestamp(easter(y)) - pd.Timedelta(days=2), last(5, 0), obs(pd.Timestamp(y, 7, 4)),
                nth(9, 0, 1), nth(11, 3, 4), obs(pd.Timestamp(y, 12, 25))}
        if y >= 2022: out.add(obs(pd.Timestamp(y, 6, 19)))
    if special: out |= {pd.Timestamp("2012-10-29"), pd.Timestamp("2012-10-30"), pd.Timestamp("2018-12-05"), pd.Timestamp("2025-01-09")}
    return out
try:
    import holidays as hol
    ref = set(pd.Timestamp(x) for x in hol.financial_holidays("NYSE", years=range(2008, 2028)).keys())
    mine = nyse_holidays()
    print("NYSE tatil kontrolü (holidays paketi ile): bende fazla", sorted(mine - ref), " eksik", sorted(ref - mine)[:10])
except Exception as e:
    print("holidays paketi yok:", e)

def og_expiry(special=True):
    hs = nyse_holidays(special=special)
    bd = pd.bdate_range("2008-01-01", "2027-12-31"); bd = bd[~bd.isin(list(hs))]
    rows = []
    for per in pd.period_range("2009-01", "2026-12", freq="M"):
        m = bd[(bd.year == per.year) & (bd.month == per.month)]
        d4 = m[-4]
        nxt = bd[bd > d4][0]
        prior_holiday = (nxt - d4).days > 1 and not (d4.dayofweek == 4)   # ertesi takvim günü iş günü değil (hafta içi tatil)
        # "tatil arifesi": bir sonraki takvim günü hafta içi ve tatil
        nd = d4 + pd.Timedelta(days=1)
        eve = (nd.dayofweek < 5) and (nd in hs)
        if d4.dayofweek == 4 or eve:
            d = bd[bd < d4][-1]
        else:
            d = d4
        rows.append(dict(month=str(per), og=d, d4=d4, alt=m[-5]))
    return pd.DataFrame(rows)
OG = og_expiry(); OGns = og_expiry(special=False)
print("OG: özel kapanışlarla/kapanışsız farklı ay:", OG[OG.og != OGns.og][["month", "og"]].assign(og_ns=OGns.og[OG.og != OGns.og]).to_string())
for k, v in {"2025-11": "2025-11-24", "2026-01": "2026-01-27", "2025-03": "2025-03-26", "2025-05": "2025-05-27", "2025-09": "2025-09-25"}.items():
    print("  bilinen vade", k, v, "kural:", OG.set_index("month").og[k].date(), "OK" if str(OG.set_index("month").og[k].date()) == v else "UYUMSUZ")
cx = pd.read_csv(f"{S}/out/a3_takvim_olay/events_comex.csv", parse_dates=["og_expiry"])
mm = OG.merge(cx[["month", "og_expiry"]], on="month", how="left")
print("  analist OG tarihleriyle uyumsuz ay sayısı:", int((mm.og != mm.og_expiry).sum()), mm[mm.og != mm.og_expiry][["month", "og", "og_expiry"]].to_string())
OG.to_csv(f"{O}/cal_og.csv", index=False)

# ---------- Bayramlar (Diyanet; ilk gün) ----------
RAM = ["2010-09-09", "2011-08-30", "2012-08-19", "2013-08-08", "2014-07-28", "2015-07-17", "2016-07-05", "2017-06-25", "2018-06-15", "2019-06-04",
       "2020-05-24", "2021-05-13", "2022-05-02", "2023-04-21", "2024-04-10", "2025-03-30", "2026-03-20"]
KUR = ["2010-11-16", "2011-11-06", "2012-10-25", "2013-10-15", "2014-10-04", "2015-09-24", "2016-09-12", "2017-09-01", "2018-08-21", "2019-08-11",
       "2020-07-31", "2021-07-20", "2022-07-09", "2023-06-28", "2024-06-16", "2025-06-06", "2026-05-27"]
BY = pd.DataFrame([dict(b="Ramazan", start=pd.Timestamp(d), ndays=3) for d in RAM] + [dict(b="Kurban", start=pd.Timestamp(d), ndays=4) for d in KUR]).sort_values("start")
BY["arife"] = BY.start - pd.Timedelta(days=1)
# VİOP boşluklarıyla doğrulama: bayram günleri VİOP'ta kapalı mı, ilk VİOP günü bayram sonu mu
vset = set(V)
chk = []
for _, r in BY[BY.start >= V[0]].iterrows():
    days_ = [r.start + pd.Timedelta(days=k) for k in range(r.ndays)]
    open_in = [d for d in days_ if d in vset]
    post = V[V > r.start][0]; pre = V[V < r.start][-1]
    chk.append(dict(b=r.b, start=r.start.date(), pre=pre.date(), post=post.date(), viop_open_during=len(open_in), gap_bdays=len(pd.bdate_range(pre, post)) - 2))
chk = pd.DataFrame(chk); print("Bayram VİOP kontrolü:\n", chk.to_string())
an_b = pd.read_csv(f"{S}/out/a3_takvim_olay/events_tr_bayram.csv", parse_dates=["start"])
print("  analist bayram başlangıçlarıyla fark:", sorted(set(BY.start) ^ set(an_b.start[an_b.start >= "2010-01-01"])))
BY.to_csv(f"{O}/cal_bayram.csv", index=False)

# ---------- TR yarım günleri: ampirik (uzlaşma 10:00 UTC spota mı 15:00'e mi uyuyor) ----------
r_v = B.ret
a15 = np.log(B.p15 / B.p15.shift(1)); a10 = np.log(B.p10 / B.p15.shift(1))
e15 = (r_v - a15).abs(); e10 = (r_v - a10).abs()
cand = B.index[(e15 > 25e-4) & (e10 < 0.5 * e15)]
known = set(BY.arife) | {pd.Timestamp(y, 10, 28) for y in range(2017, 2027)}
print("ampirik yarım gün adayı:", len(cand), " bilinenlerle (arife/28 Ekim) kesişim:", len(set(cand) & known))
kn_in_v = sorted(d for d in known if d in vset)
print("  bilinen yarım günler VİOP'ta açık:", len(kn_in_v), " bunların e15/e10 medyanı (bps):", round(e15.reindex(kn_in_v).median() * 1e4, 1), round(e10.reindex(kn_in_v).median() * 1e4, 1))
print("  normal günlerde e15/e10 medyanı (bps):", round(e15.drop(kn_in_v, errors="ignore").median() * 1e4, 1), round(e10.drop(kn_in_v, errors="ignore").median() * 1e4, 1))
extra = sorted(set(cand) - known)
print("  bilinen dışı adaylar (ilk 40):", [d.date().isoformat() for d in extra[:40]])
pd.Series(kn_in_v, name="date").to_csv(f"{O}/cal_halfdays.csv", index=False)
pd.Series(extra, name="date").to_csv(f"{O}/cal_halfday_candidates_extra.csv", index=False)
