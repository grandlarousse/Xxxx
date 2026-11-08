#!/usr/bin/env python3
"""Adım 2b: zaman kalibrasyonunun standart hatalı (dönem havuzlu) sürümü + dakikalık ardışık gün testi + yarım gün (arife) listesi kontrolü."""
import numpy as np, pandas as pd, statsmodels.api as sm, warnings
warnings.filterwarnings("ignore")
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"; OUT = f"{S}/out/a1_zaman_serisi_rep"
B = pd.read_parquet(f"{OUT}/base.parquet"); HR = pd.read_parquet(f"{OUT}/spot_hours.parquet"); lh = np.log(HR)
# Türkiye yarım günleri (arife + 28 Ekim) — takvim bilgisi; hafta sonuna düşenler veride zaten yok
HALF = pd.to_datetime(["2018-06-14", "2019-06-03", "2021-05-12", "2023-04-20", "2024-04-09", "2026-03-19",  # Ramazan arifesi
                       "2017-08-31", "2018-08-20", "2020-07-30", "2021-07-19", "2022-07-08", "2023-06-27", "2025-06-05", "2026-05-26",  # Kurban arifesi
                       "2019-10-28", "2020-10-28", "2021-10-28", "2022-10-28", "2024-10-28", "2025-10-28", "2026-10-28"])  # 28 Ekim
HALF = HALF[HALF.isin(B.index)]
seg = pd.DataFrame({f"r{a}-{a+1}": lh[a + 1] - lh[a] for a in range(8, 19)})
D = B[["v_ret"]].join(seg, how="inner"); D["v_next"] = B.v_ret.shift(-1).reindex(D.index)
D = D[~D.index.isin(HALF)]
for nm, m in [("2017-2019", D.index.year <= 2019), ("2020-2021", (D.index.year >= 2020) & (D.index.year <= 2021)), ("2022-2026", D.index.year >= 2022)]:
    g = D[m].dropna()
    for tgt in ["v_ret", "v_next"]:
        r = sm.OLS(g[tgt], sm.add_constant(g[seg.columns])).fit(cov_type="HC1")
        print(nm, tgt, "n", len(g), " ".join(f"{c}:{r.params[c]:.2f}({r.bse[c]:.2f})" for c in ["r12-13", "r13-14", "r14-15", "r15-16", "r16-17"]))
# yarım günler: settle_t gün t'nin hangi saatine yakın? (komşu günlerin 15:00 bazı referans)
lb = pd.DataFrame({hh: np.log(B.settle) - lh[hh].reindex(B.index) for hh in range(9, 17)})
ref = lb[15].where(~B.index.isin(HALF)).rolling(11, center=True, min_periods=4).median()
dev = (lb.sub(ref, axis=0) * 1e4).round(1)
print("\nYarım gün adayları: |ln(settle/spot_HH) − komşu günlerin 15:00 bazı| (bps)")
print(dev.loc[HALF].to_string())
print("normal günlerde aynı ölçüt medyanı:", dev[~dev.index.isin(HALF)].abs().median().round(1).to_dict())
pd.Series(HALF).to_csv(f"{OUT}/half_days.csv", index=False)

# dakikalık ardışık günler: v_ret_t ile Δln VWAP(spot, [τ-10dk, τ]) farkının dağılımı
M = pd.read_parquet(f"{S}/panel/duka_min_XAUUSD.parquet"); M.index = pd.DatetimeIndex(M.index) + pd.Timedelta(minutes=1)
cnt = pd.Series(1, index=M.index).groupby(M.index.normalize()).size()
days = sorted(set(cnt[cnt >= 600].index) & set(B.index))  # +1dk kaymasının yarattığı sahte günler hariç
taus = [f"{h:02d}:{m:02d}" for h in [14, 15] for m in range(0, 60, 5)] + ["16:00"]
vw = {}
for d in days:
    g = M.c[(M.index >= d + pd.Timedelta(hours=13)) & (M.index < d + pd.Timedelta(hours=17))]
    vw[d] = {t: np.log(g[(g.index > d + pd.Timedelta(hours=int(t[:2]), minutes=int(t[3:])) - pd.Timedelta(minutes=10)) &
                         (g.index <= d + pd.Timedelta(hours=int(t[:2]), minutes=int(t[3:])))].mean()) for t in taus}
V = pd.DataFrame(vw).T
pos = {d: i for i, d in enumerate(B.index)}
pairs = [(a, b) for a, b in zip(days[:-1], days[1:]) if pos[b] - pos[a] == 1 and b not in HALF and a not in HALF]
E = pd.DataFrame({t: [(B.v_ret[b] - (V.at[b, t] - V.at[a, t])) * 1e4 for a, b in pairs] for t in taus}, index=[b for a, b in pairs])
print(f"\nArdışık dakikalık gün çifti: {len(pairs)} (yıllar: {pd.Series([b.year for b in E.index]).value_counts().sort_index().to_dict()})")
print("MAD |v_ret − Δln VWAP10(τ)| (bps), τ = pencere sonu UTC:")
print(E.abs().median().round(2).to_string())
