"""02: Bağımsız veri inşası (günlük). Çıktı: res/02_daily.parquet
Index = TCELL işlem günü t (sinyal günü). Sütunlar t+1 hedefleri için '1' soneki.
FX: Yahoo TRY=X ldate D 'c' ≈ D günü 00-05 UTC (01'de doğrulandı, 2024+); 2011-2023 parite varyansı k1'i seçiyor; 2005-2010 k0.
 fx_k1(t) = ldate > t olan ilk bar (≈ t+1 sabahı 00-05 UTC; BIST açılışı 07:00 UTC'den önce)  [2011+]
 fx_k0(t) = ldate <= t son bar (≈ t sabahı; BIST seansı t'den ÖNCE -> kesinlikle ileriye bakmaz ama TKC kapanışıyla ~16-20 saat uyumsuz)
"""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_S2_a")
from vs import *
tc = bist_decomp("TCELL.IS")
xu = bist_decomp("XU100.IS") if True else None
x30 = bist_decomp("XU030.IS")
tt = bist_decomp("TTKOM.IS")
tkA = dser("TKC", "adj", drop_zero_vol=True); tkC = dser("TKC", "c", drop_zero_vol=True)
fx = dser("TRY=X", "c")
dates = tc.index
def fx_at(dates, k):
    fi = fx.index
    if k == 0: pos = fi.searchsorted(dates, side="right") - 1
    else: pos = fi.searchsorted(dates, side="right") + (k - 1)
    ok = (pos >= 0) & (pos < len(fi))
    p = np.clip(pos, 0, len(fi) - 1)
    v = pd.Series(np.where(ok, fx.values[p], np.nan), index=dates)
    lagd = pd.Series(np.where(ok, (fi[p] - dates).days, 999), index=dates)
    v[lagd.abs() > 5] = np.nan
    return v, lagd
fx1, lag1 = fx_at(dates, 1); fx0, lag0 = fx_at(dates, 0)
# 2011 öncesi Yahoo FX barı gün sonu (k0) -> 'gün sonu' kur
fx_eod = fx1.where(dates >= "2011-01-01", fx0)
df = pd.DataFrame(index=dates)
df["tkA"] = tkA.reindex(dates); df["tkC"] = tkC.reindex(dates)
df["tcA"] = tc.adj; df["tcC"] = tc.c
df["fx_eod"] = fx_eod; df["fx_k0"] = fx0; df["fx_lagdays"] = lag1
df["P"] = np.log(df.tkA * df.fx_eod / (2.5 * df.tcA))
df["Pc"] = np.log(df.tkC * df.fx_eod / (2.5 * df.tcC))
df["P_k0"] = np.log(df.tkA * df.fx_k0 / (2.5 * df.tcA))
def dev(P, w=20, minp=10):
    return P - P.shift(1).rolling(w, min_periods=minp).mean()
df["D"] = dev(df.P); df["Dc"] = dev(df.Pc); df["D_k0"] = dev(df.P_k0)
df["D10"] = dev(df.P, 10, 5); df["D60"] = dev(df.P, 60, 30)
df["D_med"] = df.P - df.P.shift(1).rolling(20, min_periods=10).median()
# ADR oranı kontrolü: Pc seviyesi (yıllık medyan)
# t+1 hedefleri (bir sonraki TCELL işlem günü)
for c in ["cc", "gap", "intra", "o", "c"]:
    df[c + "1"] = tc[c].shift(-1)
df["date1"] = pd.Series(tc.index, index=tc.index).shift(-1)
df["cc0"] = tc.cc; df["intra0"] = tc.intra; df["gap0"] = tc.gap
for nm, X in [("xu", xu), ("x30", x30), ("tt", tt)]:
    X = X.reindex(dates)
    df[nm + "_gap1"] = X.gap.shift(-1); df[nm + "_intra1"] = X.intra.shift(-1); df[nm + "_cc0"] = X.cc; df[nm + "_intra0"] = X.intra
# FX değişimi (k0 -> k1): t günü boyunca kur hareketi
df["dfx_day"] = np.log(df.fx_eod / df.fx_k0)
# TKC'nin günlük getirisi ve ES
es = dser("ES=F", "c")
df["es_cc"] = np.log(es).diff().reindex(dates)  # ES ldate t kapanışı (~21 UTC t)
df["tk_ret"] = np.log(tkA).diff().reindex(dates)
df.to_parquet(OUT + "/02_daily.parquet")
print("n gün", len(df), "D mevcut", df.D.notna().sum(), "2014+ D&intra1", df[(df.index >= "2014")][["D", "intra1", "gap1"]].dropna().shape[0])
print("Pc yıllık medyan (%):", (100 * df.Pc.groupby(df.index.year).median()).round(2).to_dict())
print("fx k1 bar - t gün farkı dağılımı (2014+):", df.loc["2014":, "fx_lagdays"].value_counts().sort_index().to_dict())
print("std D (bps) yıllık:", (1e4 * df.D.groupby(df.index.year).std()).round(0).to_dict())
print("|D|>15% gün sayısı:", int((df.D.abs() > 0.15).sum()))
