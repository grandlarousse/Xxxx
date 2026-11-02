"""A4: Saatlik veriyle kesin hizalama. BIST kapanışı t-1 (15:00 UTC) -> BIST açılışı t (07:00 UTC) arasındaki sürücü hareketi (N)
ile ertesi gün gap_t (=log(o_t/c_{t-1})) ve gün-içi devam/dönüş (intra_t = log(c_t/o_t)) ilişkisi.
N = log(P_drv(t,07:00)/P_drv(t-1,15:00)); ABD-seans kısmı U = P(t-1,21:00)/P(t-1,15:00); Asya/gece kısmı = N-U (24s enstrümanlarda).
Ayrıca BIST seansı içindeki sürücü hareketi (07:00->15:00) ile intra senkron ilişkisi ve ilk saat / gün geri kalanı ayrımı.
Çıktı: res/a4_hourly.csv, res/a4_summary.txt, res/a4_panel.parquet"""
from h import *
from h import _nwcorr

DRV = ["ES=F", "NQ=F", "BZ=F", "CL=F", "HO=F", "JETS", "DAL", "UAL", "AAL", "LHA.DE", "AF.PA", "IAG.L", "RYAAY", "ADP.PA", "FRA.DE", "AENA.MC", "TRY=X", "EURUSD=X", "TUR", "^GDAXI", "TKC"]

def snap(sym, hhmm):
    try:
        return ll.snap_daily(sym, hhmm)
    except Exception as e:
        print("snap err", sym, e); return None

def stock_frame(st):
    d = ll.raw(ll.T(st)).copy(); d.index = pd.DatetimeIndex(d["ldate"].values); d = d[~d.index.duplicated(keep="last")]
    d = d[d["v"].fillna(0) > 0]
    dd = D(st)
    h = ll.raw(ll.T(st), "h1")
    # ilk saat: 06:30 barının kapanışı (07:30 UTC) / günün açılışı
    fb = h[(h.index.hour == 6) & (h.index.minute == 30)]["c"]; fb.index = pd.DatetimeIndex(fb.index.tz_convert(None).normalize())
    out = pd.DataFrame({"gap": dd["gap"], "intra": dd["intra"], "cc": dd["cc"], "o": d["o"], "c": d["c"]})
    out["fh"] = np.log(fb.reindex(out.index) / out["o"])  # ilk ~30dk sürekli işlem (açılış->07:30)
    out["rest"] = out["intra"] - out["fh"]
    return out

if __name__ == "__main__":
    cal = None
    snaps = {}
    for s in DRV:
        a = snap(s, "15:00"); b = snap(s, "07:00"); c = snap(s, "21:00")
        if a is None: continue
        snaps[s] = (a, b, c)
    rows = []; txt = []
    panel = {}
    for st in STOCKS:
        F = stock_frame(st)
        F = F[F.index >= "2023-12-01"]
        bist_days = F.index
        for s, (p15, p07, p21) in snaps.items():
            # önceki BIST günü
            prev = pd.Series(bist_days[:-1], index=bist_days[1:])
            P15 = p15.reindex(prev.values).values; P21 = p21.reindex(prev.values).values
            P07 = p07.reindex(prev.index).values; P15t = p15.reindex(prev.index).values
            N = pd.Series(np.log(P07 / P15), index=prev.index)
            U = pd.Series(np.log(P21 / P15), index=prev.index)
            if s in ["JETS", "DAL", "UAL", "AAL", "RYAAY", "TUR", "TKC"]:
                N = U.copy()  # ABD hisseleri: yalnız ABD seansı (gece işlemi yok)
            if s in ["LHA.DE", "AF.PA", "IAG.L", "ADP.PA", "FRA.DE", "AENA.MC", "^GDAXI"]:
                p17 = snap(s, "17:00"); N = pd.Series(np.log(p17.reindex(prev.values).values / P15), index=prev.index)  # Avrupa kapanışına kadar
            A_ = N - U
            SES = pd.Series(np.log(P15t / P07), index=prev.index)  # BIST seansı içinde sürücü
            G = F.reindex(prev.index)
            panel[(st, s, "N")] = N; panel[(st, s, "SES")] = SES
            o = {"stock": st, "driver": s, "n": int(pd.concat([N, G["gap"]], axis=1).dropna().shape[0])}
            for lab, y in [("gap", G["gap"]), ("intra", G["intra"]), ("fh", G["fh"]), ("rest", G["rest"])]:
                c, t, n = _nwcorr(y, N); o[f"N->{lab}_corr"] = c; o[f"N->{lab}_t"] = t
            c, t, n = _nwcorr(G["gap"], U); o["U->gap_corr"] = c
            c, t, n = _nwcorr(G["gap"], A_); o["Asia->gap_corr"] = c
            c, t, n = _nwcorr(G["intra"], A_); o["Asia->intra_corr"] = c; o["Asia->intra_t"] = t
            c, t, n = _nwcorr(G["intra"], SES); o["SES~intra_corr"] = c
            # gap'in sürücüyle açıklanamayan kısmı -> intra
            df = pd.concat([G["gap"].rename("g"), N.rename("n"), G["intra"].rename("i")], axis=1).dropna()
            if len(df) > 100:
                b = np.polyfit(df["n"], df["g"], 1); res_ = df["g"] - np.polyval(b, df["n"])
                o["gap_beta_on_N"] = b[0]
                o["resgap->intra_corr"] = df["i"].corr(res_); o["fitgap->intra_corr"] = df["i"].corr(pd.Series(np.polyval(b, df["n"]), index=df.index))
            rows.append(o)
        panel[(st, "_", "gap")] = F["gap"]; panel[(st, "_", "intra")] = F["intra"]; panel[(st, "_", "fh")] = F["fh"]; panel[(st, "_", "rest")] = F["rest"]
        c, t, n = _nwcorr(F["intra"], F["gap"]); txt.append(f"{st}: corr(gap_t, intra_t) 2023-12+ = {c:.3f} (t={t:.2f}, n={n}); fh vs gap {F['fh'].corr(F['gap']):.3f}; rest vs gap {F['rest'].corr(F['gap']):.3f}")
        Fl = D(st); Fl = Fl[Fl.index >= "2014-01-01"]
        for per, a0, b0 in [("2014-2020", "2014", "2021-01-01"), ("2021-2026", "2021-01-01", "2027")]:
            c, t, n = _nwcorr(Fl["intra"], Fl["gap"], start=a0, end=b0); txt.append(f"   uzun dönem corr(gap,intra) {per}: {c:.3f} (t={t:.2f}, n={n})")
    H = pd.DataFrame(rows); H.to_csv(RES + "/a4_hourly.csv", index=False)
    pd.DataFrame(panel).to_parquet(RES + "/a4_panel.parquet")
    cols = ["stock", "driver", "n", "N->gap_corr", "N->gap_t", "U->gap_corr", "Asia->gap_corr", "N->intra_corr", "N->intra_t", "N->fh_corr", "N->rest_corr", "N->rest_t", "Asia->intra_corr", "SES~intra_corr", "resgap->intra_corr", "fitgap->intra_corr"]
    txt.append(H[cols].round(3).to_string(index=False))
    open(RES + "/a4_summary.txt", "w").write("\n".join(txt))
    print("ok")
