"""0: veri kontrolleri — h1/m5 tutarlılığı, kış 14:30 barı, spot fiyat adımı (ampirik), VİOP pay vadelisi fiyat adımı (bülten), likidite tablosu.
Çıktı: res/a0_liq.csv, res/a0_ssf_tick.csv, ekrana özet."""
import glob, numpy as np, pandas as pd, c_common as c
ll = c.ll

# 1) h1 vs m5 hizalama (yaz, ortak günler)
rows = []
for s in ["GARAN", "THYAO", "XU030", "CIMSA"]:
    P = c.m5_panel(s); H = c.h1_panel(s)
    dd = P["days"]; idx = {"P0730": 6 + 1 - 1 + 6, }  # 07:25 barı c = 07:30 fiyatı -> slot (07:25-06:55)/5 = 6
    for col, slot in [("P0730", 6), ("P0830", 18), ("P1430", 90), ("P1500", 96)]:
        a = H[col].reindex(dd).values; b = P["C"][:, slot]
        ok = ~np.isnan(a) & ~np.isnan(b)
        rows.append((s, col, ok.sum(), np.median(np.abs(a[ok] / b[ok] - 1)) * 1e4 if ok.sum() else np.nan))
print(pd.DataFrame(rows, columns=["sym", "piece", "n", "med_absdiff_bps"]).to_string())
D = c.h1_days(); print("h1 gün:", len(D), "yaz (14:30 barı var):", int(D.summer.sum()), "yarım gün:", int(D.half.sum()))

# 2) spot fiyat adımı: m5 kapanışlarında sıfırdan farklı en küçük |Δfiyat|
rows = []
for s in c.VIOP:
    P = c.m5_panel(s); C = P["C"][:, 1:]; dC = np.abs(np.diff(C, axis=1)); px = C[:, 1:]
    m = (dC > 1e-9) & ~np.isnan(dC)
    tk = pd.Series(np.round(dC[m], 4)); pxs = pd.Series(px[m])
    emp = tk.min() if len(tk) else np.nan
    R = c.m5_ret(s); r = R[:, 1:]
    zero = np.nanmean(r == 0)
    vol = np.nanstd(R)
    # Roll efektif spread (5 dk): 2*sqrt(-cov)
    a = R[:, 1:].ravel(); b = R[:, :-1].ravel(); ok = ~np.isnan(a) & ~np.isnan(b)
    cv = np.cov(a[ok], b[ok])[0, 1]; roll = 2 * np.sqrt(-cv) * 1e4 if cv < 0 else 0.0
    ac1 = np.corrcoef(a[ok], b[ok])[0, 1]
    pm = np.nanmedian(P["C"]); tth = float(c.tick_spot(pm))
    turn = np.nanmedian(np.nansum(P["C"][:, 1:] * P["V"][:, 1:], axis=1)) / 1e6
    rows.append(dict(stock=s, px_med=pm, tick_table=tth, tick_emp_min=emp, tick_bps=1e4 * tth / pm, ret0_frac=zero, sd5m_bps=1e4 * vol,
                     roll_spread_bps=roll, ac1_5m=ac1, turnover_mnTL=turn))
LQ = pd.DataFrame(rows).set_index("stock").sort_values("turnover_mnTL", ascending=False)
LQ["liq_rank"] = np.arange(1, len(LQ) + 1)
LQ.to_csv(c.RES + "/a0_liq.csv"); print(LQ.round(3).to_string())

# 3) VİOP pay vadelisi fiyat adımı (bülten fiyat ondalıkları) + vadeli işlem hacmi
fs = sorted(glob.glob(c.SCR + "/dl/viop/viop_*.csv")) + sorted(glob.glob(c.SCR + "/data/viop/viop_2026*.csv"))
rows = []
for f in fs[-6:]:
    df = pd.read_csv(f, sep=";", encoding="windows-1254", skiprows=[1], dtype=str)
    df.columns = [x.strip() for x in df.columns]
    df = df[df["PAZAR SEGMENTI"].str.strip() == "SSF"]
    for col in ["ACILIS FIYATI", "EN DUSUK FIYAT", "EN YUKSEK FIYAT", "KAPANIS FIYATI", "ISLEM HACMI", "ISLEM SAYISI", "ACIK POZISYON", "UZLASMA FIYATI"]:
        df[col] = pd.to_numeric(df[col].str.replace(",", "."), errors="coerce")
    df["und"] = df["DAYANAK VARLIK"].str.replace(".E", "", regex=False).str.strip()
    df["date"] = df["TARIH"]
    rows.append(df)
if rows:
    V = pd.concat(rows)
    def dec_tick(x):
        x = x.dropna(); x = x[x > 0]
        for tk in [0.01, 0.02, 0.05, 0.1, 0.25, 0.5, 1.0]:
            if not np.allclose(np.round(x / tk) * tk, x, atol=1e-6): return prev
            prev = tk
        return prev
    out = []
    for u, g in V.groupby("und"):
        prices = pd.concat([g[cn] for cn in ["ACILIS FIYATI", "EN DUSUK FIYAT", "EN YUKSEK FIYAT", "KAPANIS FIYATI"]])
        prev = 0.01
        tk = 0.01
        for t_ in [0.01, 0.02, 0.05, 0.1, 0.25, 0.5, 1.0]:
            x = prices.dropna(); x = x[x > 0]
            if np.allclose(np.round(x / t_) * t_, x, atol=1e-6): tk = t_
            else: break
        px = g["KAPANIS FIYATI"].median()
        vol = g.groupby("date")["ISLEM HACMI"].sum().median() / 1e6; ntr = g.groupby("date")["ISLEM SAYISI"].sum().median()
        out.append(dict(stock=u, ssf_px=px, ssf_tick_infer=tk, ssf_tick_bps=1e4 * tk / px, ssf_hacim_mnTL=vol, ssf_islem_sayisi=ntr, n_files=g["date"].nunique()))
    ST = pd.DataFrame(out).set_index("stock").sort_values("ssf_hacim_mnTL", ascending=False)
    ST.to_csv(c.RES + "/a0_ssf_tick.csv"); print(ST.round(2).to_string())
