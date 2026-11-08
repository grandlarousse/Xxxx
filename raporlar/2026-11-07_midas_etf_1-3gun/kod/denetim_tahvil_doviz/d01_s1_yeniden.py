"""DENETİM tahvil_doviz — S1 (10Y Hazine ihalesi A-3 -> A-1, TMV/TBT long) bağımsız yeniden üretim.
lib.trades / lib.evaluate / td.full_eval KULLANILMAZ. Fiyat: lib.load (temizlenmiş, toplam getiri düzeltmeli).
Takvim: SPY işlem günleri (NYSE). İhale tarihleri: data/events/hazine_ihale_10y30y.csv (UST10Y_ihale).
Çalıştır: python3 -I kod/denetim_tahvil_doviz/d01_s1_yeniden.py
"""
import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__))
KOD = os.path.dirname(HERE); ROOT = os.path.dirname(KOD)
sys.path.insert(0, KOD)
import numpy as np, pandas as pd
import lib

OUT = os.path.join(ROOT, "sonuclar", "aile_tahvil_doviz", "denetim")
os.makedirs(OUT, exist_ok=True)
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 300); pd.set_option("display.max_columns", 40)

IDX = lib.load("SPY").index
ev = pd.read_csv(os.path.join(ROOT, "data", "events", "hazine_ihale_10y30y.csv"), parse_dates=["date"])
A10 = pd.DatetimeIndex(sorted(ev[ev.event == "UST10Y_ihale"].date.unique()))
A30 = pd.DatetimeIndex(sorted(ev[ev.event == "UST30Y_ihale"].date.unique()))
tar = pd.read_csv(os.path.join(ROOT, "sonuclar", "tarama.csv")).set_index("sym")

def spread(sym):
    return float(tar.loc[sym, "spread_bp"])

def cost(sym, pos=2500.0):
    return 2 * 1.5 / pos * 1e4 + spread(sym)

def apos(dates, idx=IDX):
    """ihale günü -> işlem günü konumu (ihale işlem günü değilse uyarı)."""
    p = np.searchsorted(idx.values, dates.values)
    ok = (p < len(idx))
    nontrading = [str(d.date()) for d, q in zip(dates, p) if q < len(idx) and idx[q] != d]
    return p[ok], nontrading

def sim(sym, dates, k_entry=3, k_exit=1, mode="C0", df=None):
    """Kendi simülasyonum. A = ihale günü konumu p.
    C0: giriş c[p-k_entry], çıkış c[p-k_exit]
    O1: giriş o[p-k_entry+1], çıkış c[p-k_exit]  (sinyal A-3, ertesi açılış)
    C1: giriş c[p-k_entry+1], çıkış c[p-k_exit+1] (sözleşme: t+1 kapanış -> t+1+h kapanış)
    OA: giriş o[p-k_entry] (A-3 AÇILIŞI), çıkış c[p-k_exit]"""
    if df is None: df = lib.load(sym)
    d = df.reindex(IDX)
    o = d["o"].values; c = d["c"].values
    P, nt = apos(dates)
    rows = []
    for p in P:
        if mode == "C0": e, x, ep = p - k_entry, p - k_exit, None
        elif mode == "O1": e, x = p - k_entry + 1, p - k_exit
        elif mode == "C1": e, x = p - k_entry + 1, p - k_exit + 1
        elif mode == "OA": e, x = p - k_entry, p - k_exit
        sp = p - k_entry - (1 if mode == "OA" else 0)   # sinyal günü konumu
        if sp < 0 or e < 0 or x >= len(IDX) or x <= e - (1 if mode in ("O1", "OA") else 0): continue
        ep = o[e] if mode in ("O1", "OA") else c[e]
        xp = c[x]
        if not (np.isfinite(ep) and np.isfinite(xp)): continue
        sigd = IDX[sp]
        rows.append((sigd, IDX[e], IDX[x], IDX[p], xp / ep - 1))
    t = pd.DataFrame(rows, columns=["sig_date", "entry_date", "exit_date", "auction", "gross"])
    # veri aralığı: SPY takvimi 2016-11-07..; ilk sinyal günü >= df ilk günü
    t = t[t.sig_date >= df.index.min()].reset_index(drop=True)
    return t

def tstat(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if len(x) < 3 or x.std(ddof=1) == 0: return np.nan
    return x.mean() / (x.std(ddof=1) / math.sqrt(len(x)))

def summarize(t, sym, pos=2500.0, label=""):
    cst = cost(sym, pos) / 1e4
    net = t.gross - cst
    is_ = t.sig_date <= pd.Timestamp("2021-12-31")
    yrs = net.groupby(t.sig_date.dt.year).sum()
    eq = np.cumprod(1 + net.values); dd = (eq / np.maximum.accumulate(eq) - 1).min() if len(eq) else np.nan
    w = net[net > 0].sum(); l = -net[net < 0].sum()
    return {"label": label, "sym": sym, "pos": pos, "n": len(t), "gross_bp": t.gross.mean() * 1e4, "t_gross": tstat(t.gross),
            "net_bp": net.mean() * 1e4, "t": tstat(net), "win": (net > 0).mean(), "pf": w / l if l > 0 else np.inf,
            "is_n": int(is_.sum()), "is_net_bp": net[is_].mean() * 1e4, "is_t": tstat(net[is_]),
            "oos_n": int((~is_).sum()), "oos_net_bp": net[~is_].mean() * 1e4, "oos_t": tstat(net[~is_]),
            "years_pos": (yrs > 0).mean(), "n_years": len(yrs), "maxdd": dd, "worst_bp": net.min() * 1e4, "best_bp": net.max() * 1e4,
            "median_net_bp": net.median() * 1e4}

if __name__ == "__main__":
    P, nt = apos(A10)
    print("10Y ihale sayısı (csv):", len(A10), "| işlem günü olmayan ihale günü:", nt)
    res = []
    trs = {}
    for sym in ["TMV", "TBT", "TLT", "TMF"]:
        for m in ["C0", "O1", "C1", "OA"]:
            t = sim(sym, A10, 3, 1, m); trs[(sym, m)] = t
            for pos in (1000.0, 2500.0, 10000.0):
                res.append(summarize(t, sym, pos, f"A10-3->A-1 {m}"))
    R = pd.DataFrame(res)
    print("\n=== S1 kendi simülasyonum (2.500$) ===")
    print(R[R.pos == 2500][["label", "sym", "n", "gross_bp", "t_gross", "net_bp", "t", "win", "pf", "is_n", "is_net_bp", "is_t", "oos_n", "oos_net_bp", "oos_t",
                            "years_pos", "maxdd", "worst_bp"]].round(3).to_string(index=False))
    print("\n=== Maliyet duyarlılığı (net bp) ===")
    print(R[R.label.str.endswith("C0")].pivot(index="sym", columns="pos", values="net_bp").round(1).to_string())
    R.to_csv(os.path.join(OUT, "d01_s1_ozet.csv"), index=False)

    # ajanın işlem listesiyle karşılaştırma
    ag = pd.read_csv(os.path.join(ROOT, "sonuclar", "aile_tahvil_doviz", "S1_islemler_TMV_C0.csv"), parse_dates=["sig_date", "entry_date", "exit_date"])
    me = trs[("TMV", "C0")]
    mg = me.merge(ag, on="sig_date", how="outer", suffixes=("_me", "_ag"), indicator=True)
    print("\nAjan işlemleri ile eşleşme:", mg._merge.value_counts().to_dict(),
          "| max |brüt farkı| bp:", float((mg.gross_me - mg.gross_ag).abs().max() * 1e4))
    # td.load (Yahoo dağıtım) ile lib.load farkı TMV/TBT pencerelerinde
    sys.path.insert(0, os.path.join(KOD, "ajan_tahvil_doviz"))
    try:
        import td
        for sym in ("TMV", "TBT"):
            a = sim(sym, A10, 3, 1, "C0"); b = sim(sym, A10, 3, 1, "C0", df=td.load(sym))
            dd = (a.gross.values - b.gross.values) * 1e4
            print(f"{sym}: lib.load vs td.load pencere getiri farkı max |{np.abs(dd).max():.2f}| bp, ort {dd.mean():.2f} bp")
            dv = td.load(sym)["div"]; dv = dv[dv > 0]
            inwin = [(d, float(v)) for d, v in dv.items() if any((d > e) and (d <= x) for e, x in zip(a.entry_date, a.exit_date))]
            print(f"  {sym} dağıtım ex-date'i pencere içinde: {inwin}")
    except Exception as e:
        print("td karşılaştırma hatası", e)

    # en büyük 5 kazanç ve 5 kayıp, tarih tarih + veri kalitesi
    vk = pd.read_csv(os.path.join(ROOT, "sonuclar", "veri_kalitesi.csv"), parse_dates=["date"])
    vd = pd.read_csv(os.path.join(ROOT, "sonuclar", "veri_duzeltmeleri.csv"))
    tm = trs[("TMV", "C0")].copy(); tl = trs[("TLT", "C0")]
    tm["TLT_bp"] = tl.gross.values * 1e4; tm["net_bp"] = (tm.gross - cost("TMV") / 1e4) * 1e4
    dg = lib.fred("DGS30").reindex(IDX)
    d10 = lib.fred("DGS10").reindex(IDX)
    tm["dDGS30_bp"] = [(dg.get(x) - dg.get(e)) * 100 for e, x in zip(tm.entry_date, tm.exit_date)]
    tm["dDGS10_bp"] = [(d10.get(x) - d10.get(e)) * 100 for e, x in zip(tm.entry_date, tm.exit_date)]
    print("\n=== En iyi 5 TMV işlemi (veri kalitesi kontrolü) ===")
    top = tm.sort_values("net_bp", ascending=False).head(5)
    for _, r in top.iterrows():
        q = vk[(vk.sym.isin(["TMV", "TLT"])) & (vk.date > r.entry_date) & (vk.date <= r.exit_date)]
        print(f"{r.sig_date.date()} -> {r.exit_date.date()} (ihale {r.auction.date()}): TMV net {r.net_bp:7.1f} bp | TLT {r.TLT_bp:6.1f} bp | "
              f"ΔDGS30 {r.dDGS30_bp:5.1f} bp ΔDGS10 {r.dDGS10_bp:5.1f} bp | veri_kalitesi satırı: {len(q)}")
    print("TMV/TLT/TBT veri düzeltmesi satırları:", vd[vd.iloc[:, 0].isin(["TMV", "TLT", "TBT"])].to_dict("records"))
    print("\n=== En kötü 5 TMV işlemi ===")
    print(tm.sort_values("net_bp").head(5)[["sig_date", "exit_date", "auction", "net_bp", "TLT_bp", "dDGS30_bp", "dDGS10_bp"]].round(1).to_string(index=False))
    # TLT getirisi ile Hazine getiri değişimi tutarlılığı (ETF artefaktı mı?)
    print(f"\nPencerede ort ΔDGS10 {np.nanmean(tm.dDGS10_bp):.2f} bp (t {tstat(tm.dDGS10_bp):.2f}); ΔDGS30 {np.nanmean(tm.dDGS30_bp):.2f} bp (t {tstat(tm.dDGS30_bp):.2f})")
    print(f"corr(TLT pencere getirisi, ΔDGS30) = {np.corrcoef(tm.TLT_bp, tm.dDGS30_bp.fillna(0))[0,1]:.3f}")
    tm.to_csv(os.path.join(OUT, "d01_tmv_islemler.csv"), index=False)

    # yıl yıl, hariç tutmalar
    net = tm.net_bp
    print("\n=== Yıl yıl TMV net bp (n) ===")
    print(pd.DataFrame({"net_bp": net.groupby(tm.sig_date.dt.year).mean(), "n": net.groupby(tm.sig_date.dt.year).size(),
                        "TLT_bp": tm.TLT_bp.groupby(tm.sig_date.dt.year).mean()}).round(1).T.to_string())
    for lab, m in [("2020 hariç", tm.sig_date.dt.year != 2020), ("2022 hariç", tm.sig_date.dt.year != 2022),
                   ("2020+2022 hariç", ~tm.sig_date.dt.year.isin([2020, 2022])), ("2023-2026", tm.sig_date.dt.year >= 2023),
                   ("2024-2026", tm.sig_date.dt.year >= 2024)]:
        print(f"{lab:16s}: n={m.sum():3d} net {net[m].mean():6.1f} bp t={tstat(net[m]):.2f}")
    s = net.sort_values()
    for k in (5, 10):
        y = s.iloc[:-k]; print(f"en iyi {k} hariç: n={len(y)} net {y.mean():.1f} bp t={tstat(y):.2f}")
    # winsorize
    w = net.clip(net.quantile(0.05), net.quantile(0.95))
    print(f"%5/%95 winsorize: net {w.mean():.1f} bp t={tstat(w):.2f}; medyan {net.median():.1f} bp")
    json.dump({"ok": True}, open(os.path.join(OUT, "d01_done.json"), "w"))
