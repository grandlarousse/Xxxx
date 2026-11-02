"""v4: VİOP pay vadelisi (SSF) günlük bülteni ile gap fade — işlenecek enstrümanın KENDİ fiyatlarıyla.
Ham bültenler (data/viop/viop_YYYYMMDD.csv, cp1254, ';', 2. satır İngilizce başlık) bu ajanın kendi ayrıştırıcısıyla okunur.
Ön vade = vadesi bugünden SONRA olan en yakın sözleşme (vade günü bir sonrakine geçilir).
SSF gap = ln(ACILIS / ONCEKI UZLASMA), SSF gün-içi = ln(KAPANIS / ACILIS) ve ln(UZLASMA / ACILIS).
UYARI: bültende ACILIS = günün ilk işlemi (saati bilinmiyor; 09:30'dan itibaren); illikit sözleşmede geç olabilir -> işlem sayısı filtresi.
Ayrıca spot gap ile SSF gap aynı gün karşılaştırılır (SSF açılışı spot müzayede aşırılığını taşıyor mu?).
Çıktı: res/v4_ssf_front.parquet, res/v4_ssf.csv
"""
import os, glob, numpy as np, pandas as pd, vc
TG = vc.VIOP
CACHE = vc.RES + "/v4_ssf_front.parquet"
if not os.path.exists(CACHE):
    fr = []
    files = sorted(glob.glob(vc.DATA + "/viop/viop_*.csv"))
    for f in files:
        try:
            x = pd.read_csv(f, sep=";", encoding="cp1254", header=0, skiprows=[1], dtype=str, usecols=range(21))
        except Exception as e:
            print("okunamadı", f, e); continue
        x.columns = ["date", "code", "name", "market", "segment", "ctype", "cclass", "und", "expiry", "settle", "prev_settle", "chg", "open", "low", "high", "close", "vwap", "value", "prem", "qty", "trades"]
        x = x[x["segment"].str.strip() == "SSF"]
        x["und"] = x["und"].str.replace(".E", "", regex=False).str.strip()
        x = x[x["und"].isin(TG)]
        if x.empty: continue
        for c in ["settle", "prev_settle", "open", "low", "high", "close", "vwap", "value", "qty", "trades"]:
            x[c] = pd.to_numeric(x[c].str.replace(",", ".", regex=False), errors="coerce")
        x["date"] = pd.to_datetime(x["date"]); x["expiry"] = pd.to_datetime(x["expiry"])
        x = x[x["expiry"] > x["date"]].sort_values(["und", "expiry"]).groupby("und").head(1)
        fr.append(x[["date", "code", "und", "expiry", "settle", "prev_settle", "open", "low", "high", "close", "vwap", "value", "qty", "trades"]])
    F = pd.concat(fr, ignore_index=True); F.to_parquet(CACHE)
F = pd.read_parquet(CACHE)
print("SSF ön-vade satırı:", len(F), "gün:", F.date.nunique(), F.date.min().date(), F.date.max().date())
print(F.groupby(F.date.dt.year).und.nunique().to_dict())
F = F[(F.open > 0) & (F.prev_settle > 0) & (F.close > 0) & (F.settle > 0)]
F["sgap"] = np.log(F.open / F.prev_settle); F["s_oc"] = np.log(F.close / F.open); F["s_os"] = np.log(F.settle / F.open)
F = F[F.sgap.abs() < np.log(1.105)]  # pay vadelisinde de fiyat marjı; dışı veri hatası/ bedelsiz düzeltmesi
# spot ile birleştir
SP = []
for s in TG:
    d = vc.decomp(s, start="2017-01-01"); d = d.assign(und=s, date=d.index); SP.append(d[["und", "date", "gap", "intra", "o", "c"]])
SP = pd.concat(SP, ignore_index=True)
M = F.merge(SP, on=["und", "date"], how="left")
M["ssf_open_vs_spotO"] = np.log(M.open / M.o)  # baz + zamanlama farkı
liq = pd.read_csv(vc.RES + "/v1_liq.csv", index_col=0); LIQ = set(liq.index[liq["rank"] <= 23])
rows = []
def ev(spec, df, y, sig, thr):
    pos = (-np.sign(df[sig])).where(df[sig].abs() > thr, 0.0)
    r = (pos * df[y]).where(pos != 0)
    t_ = pd.DataFrame({"date": df.date, "r": r}).dropna()
    for pn, m in [("ALL", t_.date >= "2017-01-01"), ("2017-20", t_.date < vc.SPLIT), ("2021-26", t_.date >= vc.SPLIT), ("2023-26", t_.date >= "2023-01-01"), ("2024+", t_.date >= "2024-01-01"), ("2025", t_.date.dt.year == 2025), ("2026", t_.date.dt.year == 2026)]:
        x = t_[m]
        if len(x) < 30: continue
        dw = x.groupby("date").r.mean(); tw = x.groupby("date").r.sum()
        mm, t, n = vc.nw_mean(dw.values, 5); _, tt, _ = vc.nw_mean(tw.values, 5)
        rows.append(dict(spec=spec, period=pn, n=len(x), days=len(dw), DW_bps=1e4 * mm, DWt=t, TW_bps=1e4 * x.r.mean(), TWt=tt))
for mintr in [0, 50, 200]:
    df = M[M.trades >= mintr]
    for y in ["s_oc", "s_os"]:
        ev(f"SSF kendi gap>1% (işlem>={mintr}) -> {y}", df, y, "sgap", 0.01)
    if mintr == 50:
        ev(f"SSF kendi gap>1% (işlem>=50) UP-short -> s_os", df[df.sgap > 0], "s_os", "sgap", 0.01)
        ev(f"SSF kendi gap>1% (işlem>=50) DOWN-long -> s_os", df[df.sgap < 0], "s_os", "sgap", 0.01)
        ev(f"SSF kendi gap>1% (işlem>=50) likit23 -> s_os", df[df.und.isin(LIQ)], "s_os", "sgap", 0.01)
        ev(f"SSF kendi gap>1% (işlem>=50) illikit24 -> s_os", df[~df.und.isin(LIQ)], "s_os", "sgap", 0.01)
        ev(f"SSF kendi gap>2% (işlem>=50) -> s_os", df, "s_os", "sgap", 0.02)
        # aynı günler/hisseler için SPOT E0 fade (karşılaştırma)
        dd = df.dropna(subset=["gap", "intra"])
        ev(f"[aynı örneklem] SPOT gap>1% -> spot intra (E0)", dd, "intra", "gap", 0.01)
        ev(f"[aynı örneklem] SSF gap>1% -> s_os", dd, "s_os", "sgap", 0.01)
        for s in ["CIMSA", "OYAKC", "ALARK"]:
            ev(f"{s} SSF gap>1% -> s_os", df[df.und == s], "s_os", "sgap", 0.01)
            ev(f"{s} SPOT gap>1% -> intra (aynı günler)", dd[dd.und == s], "intra", "gap", 0.01)
R = pd.DataFrame(rows); R.to_csv(vc.RES + "/v4_ssf.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 300)
print(R.round(2).to_string())
# SSF gap vs spot gap
dd = M.dropna(subset=["gap"]); dd = dd[dd.trades >= 50]
b = np.polyfit(dd.gap, dd.sgap, 1)
print("\nSSF gap ~ spot gap eğim/sabit:", b.round(4), " corr", round(np.corrcoef(dd.gap, dd.sgap)[0, 1], 3), " n", len(dd))
big = dd[dd.gap.abs() > 0.01]
print("|spot gap|>1% günlerinde: ortalama sign(gap)*(sgap) bps", round(1e4 * (np.sign(big.gap) * big.sgap).mean(), 1), " ortalama |spot gap| bps", round(1e4 * big.gap.abs().mean(), 1))
print("SSF açılış − spot açılış (fade yönünde, pozitif = SSF girişi daha iyi), bps:", round(1e4 * (np.sign(big.gap) * big.ssf_open_vs_spotO).mean(), 1), "medyan", round(1e4 * (np.sign(big.gap) * big.ssf_open_vs_spotO).median(), 1))
print("SSF baz (open/O) medyanı tüm günler bps:", round(1e4 * dd.ssf_open_vs_spotO.median(), 1))
print("işlem sayısı medyanı yıl:", M.groupby(M.date.dt.year).trades.median().to_dict())
