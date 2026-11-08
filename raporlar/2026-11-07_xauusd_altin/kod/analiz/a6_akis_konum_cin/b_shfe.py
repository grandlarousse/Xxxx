"""(b) Şanghay: SHFE AU0/AG0 primi ve Çin altın ETF'i (518880.SS) primi -> VİOP fwd{h}.
Bilgi zamanı: SHFE gündüz kapanışı 15:00 CST = 07:00 UTC (gün t); spot ve USDCNH 07:00 UTC Dukascopy (gün t). 518880.SS kapanışı 15:00 CST = 07:00 UTC.
Hepsi gün t 15:00 UTC cutoff'undan 8 saat önce bilinir. Çin tatilinde (SHFE tarihi < t) değişim özellikleri NaN.
prem_D = log(AU0_D × 31,1035 / USDCNH_07) − log(XAU_07)  (vadeli carry içerir).
Roll temizliği: Sina AU0 'sürekli ana kontrat' — kontrat değişiminde fiyat carry kadar sıçrar. Ana kontrat değişimi gerçek zamanlı bilinir;
Sina 'p' (açık pozisyon) sütunundaki |Δlog OI| > log(1,25) günleri roll sayılır ve o günün Δprem'i 0 kabul edilir (seviye = temiz Δ'ların birikimi).
"""
from common import *

def sina(nm):
    txt = open(f"{S}/data/misc/sina_{nm}.txt").read()
    js = json.loads(txt[txt.index("(") + 1: txt.rindex(")")])
    d = pd.DataFrame(js); d["d"] = pd.to_datetime(d["d"]); d = d.set_index("d").sort_index()
    for c in "ohlcvps": d[c] = pd.to_numeric(d[c], errors="coerce")
    d = d[(d.p > 1000) & (d.v > 100) & (d.c > 0)]   # bozuk satırlar (ör. 2017-10-09 OI=2)
    return d

def build_prem(nm, spot_sym, start="2010-01-01"):
    s = sina(nm); s = s[s.index >= start]
    days = s.index
    px = snap_h(spot_sym, days, 7)
    if spot_sym == "XAUUSD":   # Ekim-Kasım 2026 yaması panelde
        pv = D["xau_p07"].reindex(days); px = px.fillna(pv)
    cnh = snap_h("USDCNH", days, 7)
    # 2016 öncesi USDCNH Dukascopy yok -> Yahoo CNY=X t-1 kapanışı (24:00 UTC bar sonu, 07:00 UTC'den önce bilinir) — yalnız erken dönem tekrar için
    cny = pd.read_parquet(f"{S}/panel/yahoo/CNY_X.parquet")["close"]; cny.index = pd.to_datetime(cny.index)
    cny_prev = cny.reindex(days - pd.Timedelta(days=1), method="ffill"); cny_prev.index = days
    fx = cnh.fillna(cny_prev)
    fx_src = pd.Series(np.where(cnh.notna(), "dukaCNH", "yahooCNY_t-1"), index=days)
    prem = np.log(s.c * 31.1035 / fx) - np.log(px) if nm == "AU0" else np.log(s.c * 31.1035 / 1000 / fx) - np.log(px)  # AG: CNY/kg
    dprem = prem.diff()
    dloi = np.log(s.p).diff()
    roll_oi = dloi.abs() > np.log(1.25)
    # Sina OI her kontrat değişiminde sıçramıyor (2016-2018 Haziran/Aralık ana kontrat geçişleri). Ek kural: roll aylarında (4,5,10,11,12)
    # pozitif (contango) ve kalıcı fiyat basamağı: Δprem ≥ thr, sonraki 3 gün ort. − önceki gün ≥ 0,7×Δprem ve 10g ort. farkı ≥ 0,6×Δprem.
    # (Basamağın kalıcılığı yalnız kontrat değişim gününü etiketlemek için kullanılır; kontrat değişimi gerçek zamanlı kamuya açıktır.)
    thr = 0.006 if nm == "AU0" else 0.02
    stay = (prem.shift(-1) + prem.shift(-2) + prem.shift(-3)) / 3 - prem.shift(1)
    pers = prem[::-1].rolling(10).mean()[::-1] - prem.rolling(10).mean().shift(1)
    roll_jump = (dprem >= thr) & (stay >= 0.7 * dprem) & (pers >= 0.6 * dprem) & pd.Series(s.index.month.isin([4, 5, 10, 11, 12]), index=s.index)
    roll = roll_oi | roll_jump
    dpc = dprem.where(~roll, 0.0)
    out = pd.DataFrame({"c": s.c, "oi": s.p, "px07": px, "fx07": fx, "fx_src": fx_src, "prem": prem, "dprem": dprem, "roll": roll, "dprem_c": dpc})
    out["prem_c"] = (out.dprem_c.fillna(0).cumsum() + prem.dropna().iloc[0]).where(prem.notna())
    out["roll_oi"] = roll_oi; out["roll_jump"] = roll_jump
    out["shfe_ret"] = np.log(s.c).diff().where(~roll)
    out["spot_ret07"] = np.log(px).diff()
    return out

au = build_prem("AU0", "XAUUSD"); ag = build_prem("AG0", "XAGUSD")
au.to_csv(f"{OUT}/b_shfe_au_prem.csv"); ag.to_csv(f"{OUT}/b_shfe_ag_prem.csv")
print("AU roll günleri (OI/basamak):", int(au.roll_oi.sum()), int(au.roll_jump.sum()), "| 2017+ basamak günleri:", [str(x.date()) for x in au.index[au.roll_jump & (au.index >= "2016")]])
print("AU roll günleri:", int(au.roll.sum()), "| |Δprem| std ham/temiz:", round(au.dprem.std() * 1e4, 1), round(au.dprem_c.std() * 1e4, 1), "bps")
print(au[au.roll][["dprem", "oi"]].assign(dprem_bps=lambda x: (x.dprem * 1e4).round(0)).dprem_bps.describe())
print("AG roll günleri:", int(ag.roll.sum()))

# 518880.SS (Huaan altın ETF; SGE Au99.99 izler) — roll yok; ölçek sabiti + ücret kayması -> değişim ve 60g sapma kullan
e = pd.read_parquet(f"{S}/panel/yahoo/518880.SS.parquet"); e.index = pd.to_datetime(e.index)
e = e[(e.volume > 0) & (e.close > 0)]
ed = e.index
epx = snap_h("XAUUSD", ed, 7).fillna(D["xau_p07"].reindex(ed)); efx = snap_h("USDCNH", ed, 7)
cny = pd.read_parquet(f"{S}/panel/yahoo/CNY_X.parquet")["close"]; cny.index = pd.to_datetime(cny.index)
cp = cny.reindex(ed - pd.Timedelta(days=1), method="ffill"); cp.index = ed
efx = efx.fillna(cp)
E = pd.DataFrame({"close": e.close, "vol": e.volume})
E["eprem"] = np.log(e.close / efx) - np.log(epx)
E["deprem"] = E.eprem.diff()
E["eret"] = np.log(e.close).diff()
E["lvol"] = np.log(e.volume)
E["vshock"] = E.lvol - E.lvol.rolling(20, min_periods=15).median().shift(1)       # anormal hacim (log, önceki 20g medyanına göre)
E["vshock_signed"] = E.vshock * np.sign(E.eret)
E.to_csv(f"{OUT}/b_etf518880.csv")
print("ETF prim Δ ile SHFE prim Δ korelasyonu:", round(E.deprem.corr(au.dprem_c.reindex(E.index)), 3))

def feats(A, pre):
    f = pd.DataFrame(index=A.index)
    f[f"{pre}_dprem1"] = A.dprem_c
    f[f"{pre}_dprem5"] = A.dprem_c.rolling(5).sum()
    f[f"{pre}_premdev20"] = A.prem_c - A.prem_c.rolling(20, min_periods=15).mean()
    f[f"{pre}_premz250"] = zroll(A.prem_c, 250)
    return f

Fa = feats(au, "au"); Fg = feats(ag, "ag")[["ag_dprem1", "ag_premdev20"]]
Fa["au_shfe_ret"] = au.shfe_ret
Fe = pd.DataFrame(index=E.index)
Fe["etf_dprem1"] = E.deprem; Fe["etf_premdev20"] = E.eprem - E.eprem.rolling(20, min_periods=15).mean()
Fe["etf_vshock"] = E.vshock; Fe["etf_vshock_signed"] = E.vshock_signed
F = pd.concat([Fa, Fg, Fe], axis=1)

def to_panel(F, days):
    """SHFE/SSE günü D, panel günü t'ye yalnız D == t ise (aynı gün, 07:00 UTC) eşlenir; Çin tatilinde NaN."""
    return F.reindex(days)

X = to_panel(F, D.index)
X.to_csv(f"{OUT}/b_shfe_features.csv")
DESC = {"au_dprem1": "SHFE AU0 primi 1g değişim (SHFE 07→07 getirisi − spot 07→07 − CNH), roll temiz",
        "au_dprem5": "SHFE AU0 primi 5g değişim", "au_premdev20": "SHFE AU0 primi − 20g ort.", "au_premz250": "SHFE AU0 primi 250g z",
        "au_shfe_ret": "SHFE AU0 getirisi (07→07 UTC, CNY)", "ag_dprem1": "SHFE AG0 gümüş primi 1g değişim", "ag_premdev20": "SHFE AG0 primi − 20g ort.",
        "etf_dprem1": "518880.SS (SGE ETF) primi 1g değişim", "etf_premdev20": "518880.SS primi − 20g ort.",
        "etf_vshock": "518880.SS anormal hacim (log/20g medyan)", "etf_vshock_signed": "518880.SS anormal hacim × sign(getiri)"}
rows = []
for k, desc in DESC.items():
    rows += T(X[k], "shfe", f"shfe_{k}", desc, note="bilgi 07:00 UTC gün t")
df = save(rows, "b_shfe_ic"); show(df)

# erken dönem: spot panel 2010-2016 (2016 öncesi kur = Yahoo CNY t-1)
Xs = to_panel(F, SP.index)
rows3 = []
for k in DESC:
    if Xs[k].loc[:"2016"].notna().sum() > 300:
        rows3 += T_early(Xs[k], "shfe", f"shfe_{k}", DESC[k], note="2016 öncesi kur Yahoo CNY t-1")
df3 = save(rows3, "b_shfe_early"); show(df3, ("test_id", "h", "n", "ic", "t", "yrs_same"))

# sağlamlık: roll temizliği yapılmamış ham Δprem (roll günleri sinyali kirletir mi?)
rows2 = T(au.dprem.reindex(D.index), "shfe_robust", "shfe_au_dprem1_raw", "SHFE AU0 prim Δ (roll temizliği YOK)", hs=(1, 5), note="robust")
rows2 += T(X["au_dprem1"], "shfe_robust", "shfe_au_dprem1_exext", "SHFE AU0 prim Δ (Mart-Nisan 2020, Oca-Şub 2026 hariç)", hs=(1, 5), y_mask=EXTREME, note="robust")
show(pd.DataFrame(rows2))
save(rows2, "b_shfe_robust")
