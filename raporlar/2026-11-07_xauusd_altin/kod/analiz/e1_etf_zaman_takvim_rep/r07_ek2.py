"""7) Örnek öncesi sepet SPY kontrollü tek dummy; GLD gece payı vs zaman payı (gece 17,5 sa / 24 sa)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e1_etf_zaman_takvim_rep")
from rep_lib import *
CAL2 = xc.get_calendar("XNYS", start="1993-01-01", end="2027-12-31")
SS = CAL2.sessions_in_range("1994-01-03", END); SS = pd.DatetimeIndex(SS.tz_localize(None) if SS.tz is not None else SS)
rows = []
for rule in CAL2.regular_holidays.rules:
    for d in rule.dates(pd.Timestamp("1993-12-01"), pd.Timestamp("2027-01-31")):
        if d.dayofweek < 5: rows.append((pd.Timestamp(d), rule.name))
HH = pd.DataFrame(rows, columns=["date", "name"]).drop_duplicates("date").set_index("date").sort_index(); HH = HH[~HH.index.isin(SS)]
ix = pd.Series(SS, index=SS); ym = ix.dt.to_period("M"); FIRST = ym != ym.shift(1); FIRST.iloc[0] = False; nxt = ix.shift(-1)
PRE = pd.Series([((HH.index > d) & (HH.index < n)).any() if pd.notna(n) else False for d, n in zip(SS, nxt)], index=SS)
BAS = (FIRST | PRE).astype(float)
def lr(t):
    y = pd.read_parquet(f"{S}/panel/yahoo/{t}.parquet"); y.index = pd.to_datetime(y.index); r = np.log(y.adjclose.reindex(SS)).diff(); r[r.abs() > 0.5] = np.nan; return r
M = ["NEM", "AEM", "KGC", "GFI", "HMY", "B", "AU", "RGLD", "AGI", "EGO", "IAG"]
RR = pd.DataFrame({t: lr(t) for t in M}); EW = RR.mean(axis=1).where(RR.notna().sum(axis=1) >= 4); SPY = lr("SPY"); GC = lr("GC_F")
for lab, a, b in [("1995-2007", "1995-01-01", "2007-12-31"), ("2008-2026", "2008-01-01", END)]:
    for ctrl in [[], ["SPY"], ["SPY", "GC"]]:
        d = pd.concat([EW.rename("y"), SPY.rename("SPY"), GC.rename("GC"), BAS.rename("b")], axis=1).dropna(); d = d[(d.index >= a) & (d.index <= b)]
        bb, tt = nw_ols(d.y.values, d[ctrl + ["b"]].values, 5)
        print(f"EW madenci sepet {lab} ctrl={ctrl}: {bb[-1]*1e4:.1f} bps t={tt[-1]:.2f} n_ev={int(d.b.sum())}")
    d = pd.concat([GC.rename("y"), BAS.rename("b")], axis=1).dropna(); d = d[(d.index >= a) & (d.index <= b)]
    bb, tt = nw_ols(d.y.values, d.b.values, 5); print(f"GC=F sepet {lab}: {bb[-1]*1e4:.1f} bps t={tt[-1]:.2f}")

# GLD: gün içi getiri, zaman payıyla beklenen (6,5/24 × toplam) kısma göre
y = yahoo("GLD").reindex(SESS); tot = np.log(y.adjclose).diff(); intra = np.log(y.close / y.open); night = tot - intra
for share in [6.5 / 24, 6.5 / 23]:
    x = (intra - share * tot).dropna()
    for k in PERIODS:
        q = per(x, k); b, t = nw_ols(q.values, np.ones((len(q), 0)), 5)
        print(f"GLD gün içi - {share:.3f}×toplam [{k}]: {q.mean()*252*100:.2f}%/yıl t={t[0]:.2f}")
