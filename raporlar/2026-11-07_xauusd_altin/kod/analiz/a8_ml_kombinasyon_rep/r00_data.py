"""Bağımsız yeniden üretim — adım 0: ham kaynaklardan temel seriler (lib_altin KULLANILMADI).
Çıktı: base_viop.parquet, base_spot.parquet, data_check.txt
 - VİOP hedefi: viop_long (root XAUUSD) -> aktif kontrat = önceki günün en büyük AP'li vadesi; v_ret = log(settle/prev_settle) aynı kontrat.
 - Spot: Dukascopy saatlik BID (index = bar başlangıcı; fiyat anı = index+1h) + Ekim-Kasım 2026 dakika yaması (bi5).
 - ABD Hazinesi (CSV), CFTC (zip), SHFE (Sina), Yahoo DXY (ham parquet) -> kendi as-of'umla, cutoff gün t 15:00 UTC.
"""
import os, glob, json, zipfile, lzma, numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
P = f"{S}/panel"; OUT = f"{S}/out/a8_ml_kombinasyon_rep"
log = open(f"{OUT}/data_check.txt", "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s); log.write(s + "\n"); log.flush()

# ---------------- VİOP hedefi
L = pd.read_parquet(f"{P}/viop_long.parquet")
L = L[L.root == "XAUUSD"].copy(); L["date"] = pd.to_datetime(L.date)
say("XAUUSD satır:", len(L), "kodlar:", L.code.nunique(), L.date.min(), L.date.max())
days = np.sort(L.date.unique())
# aktif kontrat: gün t'de, t-1'deki en büyük OI'li kontrat (ileriye bakmasız); ilk gün kendi OI'si
oi = L.pivot_table(index="date", columns="code", values="oi", aggfunc="first")
st = L.pivot_table(index="date", columns="code", values="settle", aggfunc="first")
ps = L.pivot_table(index="date", columns="code", values="prev_settle", aggfunc="first")
vol = L.pivot_table(index="date", columns="code", values="volume", aggfunc="first")
oi1 = oi.shift(1)
prev_big = pd.Series([oi1.loc[t].dropna().idxmax() if oi1.loc[t].notna().any() else oi.loc[t].dropna().idxmax() for t in oi.index], index=oi.index)
act = prev_big.copy()
# aktif kontrat gün t'de listelenmiyorsa (vade sona ermiş), gün t'de listelenenler arasında t-1 OI'si en büyük olan
for t in act.index:
    c = act[t]
    if pd.isna(st.at[t, c]) if c in st.columns else True:
        row = oi1.loc[t].where(st.loc[t].notna())
        act[t] = row.idxmax() if row.notna().any() else st.loc[t].dropna().index[0]
v = pd.DataFrame(index=st.index)
v["code"] = act
v["settle"] = [st.at[t, c] for t, c in act.items()]
v["prev_settle"] = [ps.at[t, c] for t, c in act.items()]
v["volume"] = [vol.at[t, c] for t, c in act.items()]
v["ret"] = np.log(v.settle / v.prev_settle)
# prev_settle ile kendi önceki gün settle'ı tutarlı mı (aynı kontrat)
own_prev = pd.Series([st[c].shift(1).at[t] if c in st else np.nan for t, c in act.items()], index=act.index)
mis = (np.abs(own_prev - v.prev_settle) > 1e-6) & own_prev.notna()
say("prev_settle != kontratın önceki gün settle'ı (gün sayısı):", int(mis.sum()), list(v.index[mis][:8].date))
v["ret_own"] = np.log(v.settle / own_prev)
for h in (1, 3, 5, 10):
    v[f"fwd{h}"] = sum(v.ret.shift(-k) for k in range(1, h + 1))
say("roll günü sayısı:", int((v.code != v.code.shift(1)).sum() - 1), "sıfır hacimli aktif gün:", int((v.volume == 0).sum()))
say("|ret|>5% günleri:", v.ret[v.ret.abs() > 0.05].round(4).to_dict())

# panel ile karşılaştır
pv = pd.read_parquet(f"{P}/panel_viop.parquet"); pv.index = pd.to_datetime(pv.index)
j = v.join(pv[["v_code", "v_ret"]], how="inner")
say("panel VİOP gün sayısı", len(pv), "benim", len(v), "ortak", len(j))
say("kod uyuşmazlığı:", int((j.code != j.v_code).sum()), "| ret max fark:", float((j.ret - j.v_ret).abs().max()),
    "| fwd1/3/5 max fark:", [float((v[f"fwd{h}"].reindex(j.index) - pv[f"fwd{h}"].reindex(j.index)).abs().max()) for h in (1, 3, 5)])
# hedefin t+1..t+h olduğunu doğrula: fwd1_t == ret_{t+1}
say("fwd1_t == ret_{t+1} kontrolü:", bool(np.allclose(v.fwd1.iloc[:-1].values, v.ret.shift(-1).iloc[:-1].values, equal_nan=True)))

# ---------------- spot saatlik (+ dakika yaması)
def hourly_close(sym):
    d = pd.read_parquet(f"{P}/duka/{sym}.parquet")
    if sym in ("XAUUSD", "USDJPY"):
        out = []
        for f in sorted(glob.glob(f"{S}/data/duka_m/{sym}/2026*.bi5")):
            b = open(f, "rb").read()
            if not b: continue
            day = pd.Timestamp(os.path.basename(f)[:8], tz="UTC")
            raw = lzma.decompress(b); a = np.frombuffer(raw, dtype=">i4").reshape(-1, 6); vv = np.frombuffer(raw, dtype=">f4").reshape(-1, 6)[:, 5]
            out.append(pd.DataFrame({"t": day + pd.to_timedelta(a[:, 0], unit="s"), "c": a[:, 2] / 1e3, "v": vv}))
        if out:
            m = pd.concat(out); m = m[m.v > 0].set_index("t").sort_index()
            hc = m.c.resample("1h").last().dropna()
            add = hc[~hc.index.isin(d.index)]
            say(sym, "dakika yamasıyla eklenen saatlik bar:", len(add), add.index.min(), add.index.max())
            c = pd.concat([d.c, add]).sort_index()
        else:
            c = d.c
    else:
        c = d.c
    c.index = c.index + pd.Timedelta(hours=1)  # fiyat anı = bar sonu
    return c[~c.index.duplicated()]

def at_hour(c, dts, H, stale_h=1):
    targ = pd.DatetimeIndex(dts).tz_localize("UTC") + pd.Timedelta(hours=H)
    i = c.index.searchsorted(targ, side="right") - 1
    ok = i >= 0
    val = np.where(ok, c.values[np.clip(i, 0, None)], np.nan)
    ts = c.index.values[np.clip(i, 0, None)]
    age = (targ.values - ts) / np.timedelta64(1, "h")
    return pd.Series(np.where(ok & (age <= stale_h), val, np.nan), index=pd.DatetimeIndex(dts))

xc = hourly_close("XAUUSD")
cand = pd.bdate_range("2010-01-04", "2026-11-06")
p15 = at_hour(xc, cand, 15)
sdays = p15.dropna().index
sp = pd.DataFrame(index=sdays)
for H in (0, 7, 12, 13, 14, 15, 16, 20):
    sp[f"p{H:02d}"] = at_hour(xc, sdays, H)
prevd = pd.DatetimeIndex(pd.Series(sdays).shift(1).fillna(sdays[0]))
sp["p20_prev"] = at_hour(xc, prevd, 20).values; sp["p15_prev"] = at_hour(xc, prevd, 15).values
sp.iloc[0, sp.columns.get_loc("p20_prev")] = np.nan; sp.iloc[0, sp.columns.get_loc("p15_prev")] = np.nan
sp["s_ret"] = np.log(sp.p15 / sp.p15.shift(1))
for h in (1, 3, 5):
    sp[f"sfwd{h}"] = sum(sp.s_ret.shift(-k) for k in range(1, h + 1))
ps_ = pd.read_parquet(f"{P}/panel_spot.parquet"); ps_.index = pd.to_datetime(ps_.index)
say("spot günleri benim", len(sp), "panel", len(ps_), "ortak", len(sp.index.intersection(ps_.index)))
for H in ("p14", "p15", "p07", "p00", "p20_prev"):
    a = sp[H]; b = ps_[f"xau_{H}"].reindex(sp.index)
    say(f"xau_{H} max |fark|:", float((a - b).abs().max()), "NaN uyuşmazlığı:", int((a.isna() != b.isna()).sum()))
say("s_ret max fark:", float((sp.s_ret - ps_.s_ret.reindex(sp.index)).abs().max()))

# dakika verisiyle saat damgası kalibrasyonu: hangi dakikadaki spot VİOP uzlaşmasına en yakın?
mm = pd.read_parquet(f"{P}/duka_min_XAUUSD.parquet"); mm.index = pd.to_datetime(mm.index)
mm["d"] = mm.index.normalize()
res = {}
for hhmm in ["13:00", "14:00", "14:30", "15:00", "15:05", "15:10", "15:15", "15:20", "15:30", "16:00", "17:00"]:
    hh, mi = map(int, hhmm.split(":"))
    q = mm[(mm.index.hour == hh) & (mm.index.minute == mi)].set_index("d").c
    jj = pd.concat([q.rename("spot"), v.settle.rename("st")], axis=1).dropna()
    # VİOP - spot farkı vade carry içerir; günler arası değişimin MAD'ı (seviye farkının medyan sapması)
    dev = np.log(jj.st / jj.spot); res[hhmm] = round(float((dev - dev.median()).abs().median() * 1e4), 2)
say("uzlaşma - spot(dk) log farkı MAD (bps), dakika örnek günleri:", res)
# saatlik bar kapanışı == 14:59 dakika kapanışı mı (bar damgası UTC doğrulaması)
q1459 = mm[(mm.index.hour == 14) & (mm.index.minute == 59)].set_index("d").c
cmp = pd.concat([q1459.rename("m"), sp.p15.rename("h")], axis=1).dropna()
say("saatlik p15 vs dakika 14:59 kapanışı: n", len(cmp), "medyan |fark| USD", float((cmp.m - cmp.h).abs().median()), "max", float((cmp.m - cmp.h).abs().max()))

# ---------------- ABD Hazinesi (ham CSV)
def treas(typ):
    fs = sorted(glob.glob(f"{S}/data/treasury/{typ}_*.csv"))
    t = pd.concat([pd.read_csv(f) for f in fs]); t["Date"] = pd.to_datetime(t["Date"], format="%m/%d/%Y")
    return t.drop_duplicates("Date").set_index("Date").sort_index()
tn = treas("daily_treasury_yield_curve"); tr = treas("daily_treasury_real_yield_curve")
ust = pd.DataFrame({"nom2": tn["2 Yr"], "nom10": tn["10 Yr"]}).join(pd.DataFrame({"real10": tr["10 YR"]}), how="outer")

def asof(vals, avail_utc, dts, H=15):
    vals = pd.Series(np.asarray(vals), index=pd.DatetimeIndex(avail_utc)).sort_index()
    vals = vals[~vals.index.isna()]
    cut = pd.DatetimeIndex(dts).tz_localize("UTC") + pd.Timedelta(hours=H)
    i = vals.index.searchsorted(cut, side="left") - 1   # kesinlikle cutoff'tan ÖNCE
    out = np.where(i >= 0, vals.values[np.clip(i, 0, None)], np.nan)
    when = np.where(i >= 0, vals.index.values[np.clip(i, 0, None)], np.datetime64("NaT"))
    return pd.Series(out, index=pd.DatetimeIndex(dts)), pd.Series(pd.to_datetime(when), index=pd.DatetimeIndex(dts))

ust_av = pd.DatetimeIndex(ust.index).tz_localize("UTC") + pd.Timedelta(hours=22)
for dfx, idx, nm in ((sp, sdays, "spot"),):
    for c in ust.columns:
        x, w = asof(ust[c].values, ust_av, idx); dfx[f"ust_{c}"] = x
        if c == "nom2":
            wi = pd.DatetimeIndex(w); wi = wi.tz_localize("UTC") if wi.tz is None else wi.tz_convert("UTC")
            lead_h = ((pd.DatetimeIndex(idx).tz_localize("UTC") + pd.Timedelta(hours=15)) - wi).total_seconds() / 3600
            say("ust_nom2 bilgi önü (saat) min/medyan:", float(np.nanmin(lead_h)), float(np.nanmedian(lead_h)))
    say("ust (spot) kendi as-of vs panel max fark:", {c: float((sp[f"ust_{c}"] - ps_[f"ust_{c}"].reindex(sdays)).abs().max()) for c in ust.columns})
# t günündeki değer gerçekten t-1 (veya daha eski) tarihli mi?
x, w = asof(ust.nom2.values, ust_av, sdays)
wi = pd.DatetimeIndex(w); wi = wi.tz_localize("UTC") if wi.tz is None else wi.tz_convert("UTC")
src_date = (wi - pd.Timedelta(hours=22)).tz_localize(None).normalize()
say("ust kaynağı gün < t oranı:", float((src_date < sdays).mean()))

# ---------------- CFTC COT (ham zip)
cot = []
for f in sorted(glob.glob(f"{S}/data/cftc/*.zip")):
    z = zipfile.ZipFile(f)
    for nm in z.namelist():
        t = pd.read_csv(z.open(nm), low_memory=False, usecols=lambda c: c.startswith(("CFTC_Contract_Market_Code", "Report_Date_as_YYYY", "M_Money_Positions_Long_All", "M_Money_Positions_Short_All", "Open_Interest_All")))
        cot.append(t)
cot = pd.concat(cot); cot["code"] = cot.CFTC_Contract_Market_Code.astype(str).str.strip().str.zfill(6)
dcol = [c for c in cot.columns if c.startswith("Report_Date_as_YYYY")][0]
cot["rd"] = pd.to_datetime(cot[dcol])
g = cot[cot.code == "088691"].drop_duplicates("rd").set_index("rd").sort_index()
mmoi = (g.M_Money_Positions_Long_All - g.M_Money_Positions_Short_All) / g.Open_Interest_All
say("COT altın ilk/son rapor:", g.index.min().date(), g.index.max().date(), "n", len(g), "haftaiçi Salı oranı", float((g.index.dayofweek == 1).mean()))
cot_av = pd.DatetimeIndex(g.index).tz_localize("UTC") + pd.Timedelta(days=3, hours=21)
x, w = asof(mmoi.values, cot_av, sdays); sp["cot_mm_net_oi"] = x
x2, _ = asof(np.array(g.index.values, dtype="datetime64[ns]").astype("int64"), cot_av, sdays); sp["cot_rd"] = pd.to_datetime(x2)
say("COT mm_net_oi vs panel max fark:", float((sp.cot_mm_net_oi - ps_.cot_gold_mm_net_oi.reindex(sdays)).abs().max()))

# ---------------- SHFE (Sina)
txt = open(f"{S}/data/misc/sina_AU0.txt").read(); js = json.loads(txt[txt.index("(") + 1: txt.rindex(")")])
sh = pd.DataFrame(js); sh["d"] = pd.to_datetime(sh["d"]); sh = sh.set_index("d").sort_index(); sh["c"] = pd.to_numeric(sh.c)
sh_av = pd.DatetimeIndex(sh.index).tz_localize("UTC") + pd.Timedelta(hours=7, minutes=5)
x, w = asof(sh.c.values, sh_av, sdays); sp["shfe_c"] = x
x2, _ = asof(np.array(sh.index.values, dtype="datetime64[ns]").astype("int64"), sh_av, sdays); sp["shfe_date"] = pd.to_datetime(x2)
say("SHFE c vs panel max fark:", float((sp.shfe_c - ps_.shfe_AU0_c.reindex(sdays)).abs().max()))
cnh = hourly_close("USDCNH"); sp["cnh07"] = at_hour(cnh, sdays, 7)
say("USDCNH 07 vs panel max fark:", float((sp.cnh07 - ps_.dk_USDCNH_p07.reindex(sdays)).abs().max()), "NaN (2016 öncesi)", int(sp.cnh07.isna().sum()))

# ---------------- Yahoo DXY (ham)
y = pd.read_parquet(f"{P}/yahoo/DX-Y.NYB.parquet"); y.index = pd.to_datetime(y.index)
yav = (pd.DatetimeIndex(y.index) + pd.Timedelta(hours=17)).tz_localize("America/New_York", nonexistent="shift_forward", ambiguous="NaT").tz_convert("UTC")
ok = ~pd.isna(yav)
x, w = asof(y.close.values[ok], yav[ok], sdays); sp["dxy"] = x
say("DXY vs panel max fark:", float((sp.dxy - ps_.y_DX_Y_NYB.reindex(sdays)).abs().max()))
# DXY tarih etiketi doğru mu? Yahoo kapanışını Dukascopy DOLLARIDXUSD ile saat saat karşılaştır
dk = hourly_close("DOLLARIDXUSD")
yy = y.close.loc["2018":]
best = {}
for lagd in (-1, 0, 1):
    for H in (16, 20, 21, 22):
        dd = pd.DatetimeIndex(yy.index) + pd.Timedelta(days=lagd)
        q = at_hour(dk, dd, H, 2); q.index = yy.index
        r = np.log(yy).diff(); rq = np.log(q).diff()
        best[f"gün{lagd:+d} {H}:00"] = round(float(r.corr(rq)), 4)
say("Yahoo DXY günlük değişimi ile Dukascopy DXY (gün kayması, UTC saat) korelasyonu:", best)
# benzer kontrol: ust nom2 — Treasury D değişimi ile Dukascopy T-bond fiyatının D 20:00 UTC değişimi
tb = hourly_close("USTBONDTRUSD"); n10 = ust.nom10.loc["2019-06":]
cc = {}
for lagd in (-1, 0, 1):
    dd = pd.DatetimeIndex(n10.index) + pd.Timedelta(days=lagd); q = at_hour(tb, dd, 20, 3); q.index = n10.index
    cc[f"gün{lagd:+d}"] = round(float(n10.diff().corr(np.log(q).diff())), 4)
say("Treasury nom10 günlük değişimi vs Dukascopy T-bond (20:00 UTC) korelasyonu (beklenen negatif, gün0 en güçlü):", cc)

sp.to_parquet(f"{OUT}/base_spot.parquet"); v.to_parquet(f"{OUT}/base_viop.parquet")
say("kaydedildi")
