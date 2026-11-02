"""A6: (i) Olay çalışması (jeopolitik/terör/salgın/kur şokları) — piyasa modeli artık getirisi (XU100, beta [-260,-11]).
(ii) Gün-içi THYAO<->PGSUS<->TAVHL lead-lag (h1 2023-12+, m5 son ~60 gün).
(iii) Brent şok günleri (z>2,5) sonrası olay ortalaması. Çıktı: res/a6_events.csv, res/a6_summary.txt"""
from h import *
from h import _nwcorr

EV = [  # (BIST t0, olay, not: t0 = haberin ilk fiyatlanabildiği BIST seansı)
    ("2015-11-24", "Rusya Türk jetini düşürdü -> Rus turizm yaptırımı", "seans içi haber"),
    ("2016-06-29", "Atatürk Havalimanı saldırısı (28.06 akşamı)", "kapanış sonrası"),
    ("2016-07-18", "15 Temmuz darbe girişimi (Cuma gecesi)", "hafta sonu"),
    ("2020-03-12", "ABD'nin Avrupa seyahat yasağı / WHO pandemi", "kapanış sonrası"),
    ("2020-11-09", "Pfizer aşı açıklaması", "seans içi ~11:45 UTC"),
    ("2021-12-21", "20 Aralık KKM / TL dönüşü (akşam)", "kapanış sonrası"),
    ("2023-10-09", "7 Ekim Hamas saldırısı", "hafta sonu"),
    ("2024-04-15", "İran'ın İsrail'e drone saldırısı (13.04)", "hafta sonu"),
    ("2024-10-02", "İran füze saldırısı (01.10 akşamı)", "kapanış sonrası"),
    ("2025-03-19", "İmamoğlu gözaltısı", "seans öncesi"),
    ("2025-06-13", "İsrail'in İran'ı vurması", "gece"),
    ("2025-06-23", "ABD'nin İran nükleer tesislerini vurması (21-22.06)", "hafta sonu"),
    ("2025-06-24", "İsrail-İran ateşkesi", "gece"),
    ("2026-03-02", "Orta Doğu savaşı / Hormuz kapanması (28.02-01.03)", "hafta sonu"),
]

def car_table():
    m = R("XU100"); rows = []
    bz = R("BZ=F")
    for d0, ev, note in EV:
        d0 = pd.Timestamp(d0)
        for st in STOCKS:
            r = R(st)
            df = pd.concat([r.rename("r"), m.rename("m")], axis=1).dropna()
            if d0 not in df.index:
                nxt = df.index[df.index >= d0]
                if len(nxt) == 0: continue
                d0 = nxt[0]
            i0 = df.index.get_loc(d0)
            est = df.iloc[max(0, i0 - 260): i0 - 10]
            b = np.polyfit(est["m"], est["r"], 1); sd = (est["r"] - np.polyval(b, est["m"])).std()
            ar = df["r"] - np.polyval(b, df["m"])
            o = {"t0": d0.date(), "event": ev, "note": note, "stock": st, "beta": b[0], "raw_t0_%": 100 * df["r"].iloc[i0], "xu100_t0_%": 100 * df["m"].iloc[i0],
                 "AR_t0_%": 100 * ar.iloc[i0], "AR_t0_z": ar.iloc[i0] / sd, "CAR_0_1_%": 100 * ar.iloc[i0:i0 + 2].sum(), "CAR_0_5_%": 100 * ar.iloc[i0:i0 + 6].sum(),
                 "CAR_0_20_%": 100 * ar.iloc[i0:i0 + 21].sum(), "brent_t-1..t0_%": 100 * (bz.reindex(df.index).iloc[i0 - 1:i0 + 1].sum())}
            dd = D(st)
            if d0 in dd.index: o["gap_t0_%"] = 100 * dd.loc[d0, "gap"]; o["intra_t0_%"] = 100 * dd.loc[d0, "intra"]
            rows.append(o)
    return pd.DataFrame(rows)

def brent_shock_events(z=2.5):
    bz = R("BZ=F").where(R("BZ=F") != 0)
    mu = bz.rolling(250, min_periods=60).std().shift(1); zz = bz / mu
    up = zz[zz > z].index; dn = zz[zz < -z].index
    m = R("XU100"); out = []
    for lab, days in [("Brent_UP", up), ("Brent_DOWN", dn)]:
        for st in STOCKS:
            dd = D(st); r = R(st)
            # Brent kapanışı ~19 UTC (BIST kapanışından sonra) -> BIST etkisi t+1 açılışında (gap) ve t+1 gün-içi
            nxt = [dd.index[dd.index > d][0] for d in days if (dd.index > d).any() and d >= pd.Timestamp("2014-01-01")]
            g = dd["gap"].reindex(nxt); i = dd["intra"].reindex(nxt)
            ex = (r - m).reindex(nxt)
            xm = (r - m).dropna(); fw = pd.Series([xm.loc[xm.index > d].iloc[1:5].sum() for d in nxt], index=nxt)
            for per, msk in [("2014-2020", g.index < SPLIT), ("2021-2026", g.index >= SPLIT)]:
                out.append({"shock": lab, "stock": st, "per": per, "n": int(msk.sum()), "sync_ret_t_%": 100 * r.reindex([d for d in days if d >= pd.Timestamp("2014")]).mean() if per == "2014-2020" else np.nan,
                            "gap_t+1_%": 100 * g[msk].mean(), "intra_t+1_%": 100 * i[msk].mean(), "intra_t": i[msk].mean() / i[msk].std() * np.sqrt(msk.sum()) if msk.sum() > 2 else np.nan,
                            "excess_vs_xu100_t+1_%": 100 * ex[msk].mean(), "excess_t+2..t+5_%": 100 * fw[msk].mean()})
    return pd.DataFrame(out)

def intraday_leadlag():
    out = []
    def bars(sym, kind):
        h = ll.raw(sym, kind); h = h[(h["v"].fillna(0) > 0)]
        r = np.log(h["c"]).diff(); day = h.index.tz_convert(None).normalize()
        dv = np.asarray(day); first = np.r_[True, dv[1:] != dv[:-1]]; r[first] = np.nan  # gün başı (gece) barını at
        return r
    for kind in ["h1", "m5"]:
        try:
            R_ = {s: bars(s + ".IS", kind) for s in STOCKS}
        except Exception as e:
            out.append({"kind": kind, "err": str(e)}); continue
        for a in STOCKS:
            for b in STOCKS:
                if a == b: continue
                df = pd.concat([R_[b].rename("b"), R_[a].shift(1).rename("a"), R_[b].shift(1).rename("bown")], axis=1).dropna()
                c, t, n = _nwcorr(df["b"], df["a"])
                pc, _ = ll.partial_corr(df["b"], df["a"], [df["bown"]])
                c0 = pd.concat([R_[b], R_[a]], axis=1).dropna().corr().iloc[0, 1]
                out.append({"kind": kind, "leader": a, "follower": b, "sync_corr": c0, "lag1bar_corr": c, "t": t, "pc_ctrl_own_lag": pc, "n": n})
    return pd.DataFrame(out)

if __name__ == "__main__":
    E = car_table(); E.to_csv(RES + "/a6_events.csv", index=False)
    B = brent_shock_events(); B.to_csv(RES + "/a6_brent_shocks.csv", index=False)
    I = intraday_leadlag(); I.to_csv(RES + "/a6_intraday_ll.csv", index=False)
    txt = "OLAYLAR (AR = piyasa modeli artığı)\n" + E[["t0", "event", "stock", "raw_t0_%", "xu100_t0_%", "AR_t0_%", "AR_t0_z", "CAR_0_5_%", "CAR_0_20_%", "brent_t-1..t0_%"]].round(2).to_string(index=False)
    txt += "\n\nBRENT ŞOK GÜNLERİ (|r/sd|>2,5) SONRASI\n" + B.round(3).to_string(index=False)
    txt += "\n\nGÜN-İÇİ LEAD-LAG\n" + I.round(3).to_string(index=False)
    open(RES + "/a6_summary.txt", "w").write(txt); print("ok")
