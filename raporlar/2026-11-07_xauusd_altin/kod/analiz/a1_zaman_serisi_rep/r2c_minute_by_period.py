#!/usr/bin/env python3
"""Adım 2c: dakikalık ardışık gün testi dönem dönem (uzlaşma penceresi erken yıllarda 15:00'ten önce mi?)."""
import numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"; OUT = f"{S}/out/a1_zaman_serisi_rep"
B = pd.read_parquet(f"{OUT}/base.parquet"); HALF = set(pd.to_datetime(pd.read_csv(f"{OUT}/half_days.csv").iloc[:, 0]))
M = pd.read_parquet(f"{S}/panel/duka_min_XAUUSD.parquet"); M.index = pd.DatetimeIndex(M.index) + pd.Timedelta(minutes=1)
cnt = pd.Series(1, index=M.index).groupby(M.index.normalize()).size()
days = sorted(set(cnt[cnt >= 600].index) & set(B.index))  # tam dakikalık günler (+1dk kaymasının yarattığı sahte günler hariç)
pos = {d: i for i, d in enumerate(B.index)}
wins = {f"{a}-{b}": (a, b) for a, b in [("14:40", "14:50"), ("14:45", "14:55"), ("14:50", "15:00"), ("14:55", "15:05"), ("15:00", "15:10"), ("15:05", "15:15"), ("15:10", "15:20"), ("15:00", "15:15")]}
def tm(d, s): return d + pd.Timedelta(hours=int(s[:2]), minutes=int(s[3:]))
VW = {}
for d in days:
    g = M.c[(M.index > tm(d, "14:00")) & (M.index <= tm(d, "16:00"))]
    VW[d] = {k: np.log(g[(g.index > tm(d, a)) & (g.index <= tm(d, b))].mean()) for k, (a, b) in wins.items()}
VW = pd.DataFrame(VW).T
pairs = [(a, b) for a, b in zip(days[:-1], days[1:]) if pos[b] - pos[a] == 1 and a not in HALF and b not in HALF and B.code[a] == B.code[b]]
E = pd.DataFrame({k: [abs(B.v_ret[b] - (VW.at[b, k] - VW.at[a, k])) * 1e4 for a, b in pairs] for k in wins}, index=[b for a, b in pairs])
per = pd.cut(E.index.year, [2016, 2019, 2021, 2025, 2026], labels=["2017-19", "2020-21", "2022-25", "2026"])
E.to_csv(f"{OUT}/minute_pairs.csv")
print("Medyan |v_ret − Δln VWAP(pencere)| (bps); pencere UTC (fiyat anı):")
print(E.groupby(per).median().round(2).assign(n=E.groupby(per).size()).to_string())
