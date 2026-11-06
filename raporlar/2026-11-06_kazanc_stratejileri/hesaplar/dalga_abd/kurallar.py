"""2) Karar-aninda bilinen yakalama kurallari (aylik, Ken French 49 sektor VW).
Tum sinyaller ay sonu t kapanisi ile hesaplanir, pozisyon t+1 ayinin getirisini alir.
Aile A: RS kirilimi (yeni N-ay RS zirvesi) + cikis (RS trailing / RS<MA / sure).
Aile B: top-k momentum rotasyonu (L ay, atlamali/atlamasiz), aylik.
Aile C: cift momentum (mutlak filtre: L-ay getirisi > T-bill; ya da piyasa 10-ay SMA filtresi).
Aile D: tampon (top-k gir, sira > B olunca cik) + fiyat trailing stop.
Maliyet: tek yon c (baz 0.10%, stres 0.25%).
"""
import os, itertools
import numpy as np
import pandas as pd
from dalga_tanim import base_data, find_waves, OUT

C_BASE = 0.0010
C_STRESS = 0.0025


def perf(r, rf, freq=12):
    r = r.dropna()
    if len(r) == 0:
        return {}
    rf = rf.reindex(r.index).fillna(0)
    w = (1 + r).cumprod()
    yrs = len(r) / freq
    cagr = w.iloc[-1] ** (1 / yrs) - 1
    ex = r - rf
    sh = ex.mean() / ex.std() * np.sqrt(freq) if ex.std() > 0 else np.nan
    dd = (w / w.cummax() - 1).min()
    return dict(cagr=cagr, vol=r.std() * np.sqrt(freq), sharpe=sh, maxdd=dd)


# ---------------------------------------------------------------- Aile A
def rs_breakout(R, RM, RF, N=12, exit_kind="trail", X=0.15, M=10, H=6, absfilt=False, c=C_BASE, minlen=24):
    """Sektor bazli olay kurali. Doner: trades DataFrame, aylik portfoy getirisi (EW acik pozisyonlar, bos ise T-bill)."""
    trades = []
    lrel = np.log1p(R).sub(np.log1p(RM), axis=0)
    labs = np.log1p(R)
    T = len(R.index)
    pos_ret = {}  # (t_index) -> list of returns of open slices
    for ind in R.columns:
        r = R[ind].values
        valid = ~np.isnan(r)
        x = np.where(valid, lrel[ind].values, 0.0).cumsum()
        p = np.where(valid, labs[ind].values, 0.0).cumsum()
        first = np.argmax(valid)
        inpos = False
        for t in range(first + minlen, T - 1):
            if not valid[t]:
                continue
            if not inpos:
                win = x[t - N:t]
                sig = x[t] > win.max()
                if sig and absfilt:
                    rf12 = np.log1p(RF.values[t - 11:t + 1]).sum()
                    sig = (p[t] - p[t - 12]) > rf12
                if sig:
                    inpos = True
                    e = t
                    xmax = x[t]
                    continue
            else:
                xmax = max(xmax, x[t])
                ex = False
                if exit_kind == "trail":
                    ex = x[t] <= xmax + np.log(1 - X)
                elif exit_kind == "ma":
                    ex = x[t] < x[t - M + 1:t + 1].mean()
                elif exit_kind == "time":
                    ex = (t - e) >= H
                if ex or t == T - 2:
                    trades.append(dict(ind=ind, e_i=e, x_i=t, entry=R.index[e], exit=R.index[t], months=t - e,
                                       rel=np.exp(x[t] - x[e]) - 1, abs=np.exp(p[t] - p[e]) - 1,
                                       open_end=(not ex)))
                    inpos = False
    tr = pd.DataFrame(trades)
    if len(tr) == 0:
        return tr, pd.Series(dtype=float), pd.Series(dtype=float)
    tr["abs_net"] = (1 + tr["abs"]) * (1 - c) ** 2 - 1
    tr["rel_net"] = (1 + tr["rel"]) * (1 - c) ** 2 - 1
    # portfoy: her ay acik pozisyonlarin EW ortalamasi
    slices = np.zeros(T)
    counts = np.zeros(T)
    Rv = R.values
    for _, row in tr.iterrows():
        j = R.columns.get_loc(row.ind)
        for t in range(row.e_i + 1, row.x_i + 1):
            rr = Rv[t, j]
            if np.isnan(rr):
                rr = 0.0
            if t == row.e_i + 1:
                rr = (1 + rr) * (1 - c) - 1
            if t == row.x_i:
                rr = (1 + rr) * (1 - c) - 1
            slices[t] += rr
            counts[t] += 1
    port = pd.Series(np.where(counts > 0, slices / np.maximum(counts, 1), RF.values), index=R.index)
    port.iloc[:minlen] = np.nan
    return tr, port, pd.Series(counts, index=R.index)


def wave_capture(trades, waves, R, RM):
    """Her dalga icin: tespit (tepe oncesi giris / dalga basinda acik), giris gecikmesi, yakalama orani."""
    lrel = np.log1p(R).sub(np.log1p(RM), axis=0)
    xs = {ind: np.nan_to_num(lrel[ind].values).cumsum() for ind in R.columns}
    out = []
    pos = {p: i for i, p in enumerate(R.index)}
    for _, w in waves.iterrows():
        if w.start not in pos or w.peak not in pos:
            continue
        a, b = pos[w.start], pos[w.peak]
        x = xs[w.ind]
        tot = x[b] - x[a]
        tw = trades[(trades.ind == w.ind) & (trades.x_i > a) & (trades.e_i < b)]
        if len(tw) == 0:
            out.append(dict(ind=w.ind, start=w.start, detected=False, capture=0.0, lag=np.nan, giveback=np.nan, ntr=0))
            continue
        cap = 0.0
        for _, t in tw.iterrows():
            cap += x[t.x_i] - x[max(t.e_i, a)]
        e0 = max(tw.e_i.min(), a)
        lag = (x[e0] - x[a]) / tot
        last = tw.iloc[-1]
        gb = (x[b] - x[last.x_i]) / tot if last.x_i >= b else np.nan
        out.append(dict(ind=w.ind, start=w.start, detected=True, capture=cap / tot, lag=lag, giveback=gb, ntr=len(tw)))
    return pd.DataFrame(out)


def false_starts(trades, waves, R):
    """Giris sinyali bir dalga araliginda (bas<=giris<tepe) degilse 'yanlis baslangic'."""
    pos = {p: i for i, p in enumerate(R.index)}
    wv = {}
    for _, w in waves.iterrows():
        if w.start in pos and w.peak in pos:
            wv.setdefault(w.ind, []).append((pos[w.start], pos[w.peak]))
    fs = []
    for _, t in trades.iterrows():
        ok = any(a <= t.e_i < b for a, b in wv.get(t.ind, []))
        fs.append(not ok)
    return np.array(fs)


# ---------------------------------------------------------------- Aile B/C/D
def rotation(R, RM, RF, L=6, skip=0, k=3, absfilt=False, mktfilt=False, buffer=None, trail=None, c=C_BASE, start_i=13):
    """Aylik rotasyon. Doner: net getiri serisi, agirlik matrisi, devir."""
    lr = np.log1p(R)
    mom = lr.rolling(L, min_periods=L).sum().shift(skip)
    rfc = np.log1p(RF).rolling(L).sum().shift(skip)
    mk = (1 + RM).cumprod()
    mk_sma = mk.rolling(10).mean()
    T, Nn = R.shape
    W = np.zeros((T, Nn))
    held = set()
    peakp = {}
    cum = (1 + R.fillna(0)).cumprod().values
    Mv = mom.values
    for t in range(start_i, T - 1):
        m = Mv[t]
        ok = ~np.isnan(m) & ~np.isnan(R.values[t])
        if ok.sum() < k:
            continue
        order = np.argsort(-np.where(ok, m, -np.inf))
        rank = np.empty(Nn, int)
        rank[order] = np.arange(Nn)
        if buffer is None:
            sel = set(order[:k])
        else:
            keep = {j for j in held if ok[j] and rank[j] < buffer}
            sel = set(keep)
            for j in order:
                if len(sel) >= k:
                    break
                sel.add(j)
        # trailing fiyat stopu: tutulan ve tepe-dusus >= trail ise cikar, bu ay yerine nakit
        if trail is not None:
            for j in list(sel):
                if j in held:
                    peakp[j] = max(peakp.get(j, cum[t, j]), cum[t, j])
                else:
                    peakp[j] = cum[t, j]
            stopped = {j for j in sel if cum[t, j] <= peakp[j] * (1 - trail)}
        else:
            stopped = set()
        w = np.zeros(Nn)
        slots = 1.0 / k
        for j in sel:
            if j in stopped:
                continue
            if absfilt and not (m[j] > rfc.values[t]):
                continue
            w[j] = slots
        if mktfilt and mk.values[t] < mk_sma.values[t]:
            w[:] = 0
        W[t] = w
        held = {j for j in sel if j not in stopped} if trail is not None else sel
        for j in list(peakp):
            if j not in held:
                peakp.pop(j, None)
    Wdf = pd.DataFrame(W, index=R.index, columns=R.columns)
    Rn = R.fillna(0).values
    gross = np.zeros(T)
    turn = np.zeros(T)
    for t in range(start_i, T - 1):
        w = W[t]
        # onceki agirliklarin kayma sonrasi degeri
        if t > start_i:
            wp = W[t - 1] * (1 + Rn[t])
            tot = wp.sum() + (1 - W[t - 1].sum()) * (1 + RF.values[t])
            wp = wp / tot if tot > 0 else wp
        else:
            wp = np.zeros(Nn)
        turn[t + 1] = np.abs(w - wp).sum()
        gross[t + 1] = (w * Rn[t + 1]).sum() + (1 - w.sum()) * RF.values[t + 1]
    net = gross - turn * c
    s = pd.Series(net, index=R.index)
    s.iloc[:start_i + 1] = np.nan
    return s, Wdf, pd.Series(turn, index=R.index)


def rotation_capture(Wdf, waves, R, RM, post=24):
    lrel = np.log1p(R).sub(np.log1p(RM), axis=0)
    pos = {p: i for i, p in enumerate(R.index)}
    H = (Wdf.values > 0)
    out = []
    for _, w in waves.iterrows():
        if w.start not in pos or w.peak not in pos:
            continue
        a, b = pos[w.start], pos[w.peak]
        j = R.columns.get_loc(w.ind)
        dx = np.nan_to_num(lrel[w.ind].values)
        x = dx.cumsum()
        tot = x[b] - x[a]
        cap = sum(dx[t] for t in range(a + 1, b + 1) if H[t - 1, j])
        # tepe sonrasi: kesintisiz tutulmaya devam edilen aylardaki kayip
        gb = 0.0
        t = b + 1
        while t < len(dx) and H[t - 1, j] and t <= b + post:
            gb += dx[t]
            t += 1
        held_months = [t for t in range(a + 1, b + 1) if H[t - 1, j]]
        det = len(held_months) > 0
        lag = (x[held_months[0] - 1] - x[a]) / tot if det else np.nan
        out.append(dict(ind=w.ind, start=w.start, detected=det, capture=(cap + gb) / tot, cap_in=cap / tot,
                        lag=lag, post_loss=gb / tot))
    return pd.DataFrame(out)


def decade_table(s, bench, rf):
    d = pd.DataFrame({"s": s, "b": bench, "rf": rf}).dropna()
    d["dec"] = (d.index.year // 10) * 10
    rows = {}
    for dec, g in d.groupby("dec"):
        rows[dec] = dict(s=(1 + g.s).prod() ** (12 / len(g)) - 1, b=(1 + g.b).prod() ** (12 / len(g)) - 1)
    return pd.DataFrame(rows).T


if __name__ == "__main__":
    R, RM, RF, m = base_data()
    waves = pd.read_pickle(os.path.join(OUT, "waves_40_20.pkl"))
    res = []
    # --------- Aile A grid
    allA = {}
    for N, ek, absf in itertools.product((6, 12), ("trail10", "trail15", "trail20", "ma6", "ma10", "time3", "time6", "time12"), (False, True)):
        kw = dict(N=N, absfilt=absf)
        if ek.startswith("trail"):
            kw.update(exit_kind="trail", X=int(ek[5:]) / 100)
        elif ek.startswith("ma"):
            kw.update(exit_kind="ma", M=int(ek[2:]))
        else:
            kw.update(exit_kind="time", H=int(ek[4:]))
        tr, port, cnt = rs_breakout(R, RM, RF, **kw)
        wc = wave_capture(tr, waves, R, RM)
        fs = false_starts(tr, waves, R)
        p_all = perf(port.loc["1930":], RF)
        p_00 = perf(port.loc["2000":], RF)
        p_15 = perf(port.loc["2015":], RF)
        name = f"A_N{N}_{ek}_{'abs' if absf else 'none'}"
        allA[name] = (tr, port, wc)
        res.append(dict(rule=name, fam="A", ntr=len(tr), tr_per_yr=len(tr) / (len(R) / 12), avg_mo=tr.months.mean(),
                        win_rel=(tr.rel_net > 0).mean(), avg_rel=tr.rel_net.mean(), med_rel=tr.rel_net.median(),
                        avg_abs=tr.abs_net.mean(), false_start=fs.mean(), hit=wc.detected.mean(),
                        capture_med=wc.capture.median(), capture_mean=wc.capture.mean(), lag_med=wc.lag.median(),
                        cagr=p_all["cagr"], sharpe=p_all["sharpe"], maxdd=p_all["maxdd"], cagr00=p_00["cagr"],
                        sharpe00=p_00["sharpe"], cagr15=p_15["cagr"], maxdd15=p_15["maxdd"],
                        avg_open=cnt.loc["1930":].mean()))
    # --------- Aile B/C/D grid
    allB = {}
    for L, skip, k in itertools.product((1, 3, 6, 12), (0, 1), (1, 3, 5, 10)):
        if L == 1 and skip == 1:
            continue
        for var in ("plain", "abs", "mkt", "buf", "trail15"):
            kw = dict(L=L, skip=skip, k=k)
            if var == "abs":
                kw["absfilt"] = True
            elif var == "mkt":
                kw["mktfilt"] = True
            elif var == "buf":
                kw["buffer"] = 3 * k
            elif var == "trail15":
                kw["trail"] = 0.15
            s, W, turn = rotation(R, RM, RF, **kw)
            s_st, _, _ = rotation(R, RM, RF, **{**kw, "c": C_STRESS})
            wc = rotation_capture(W, waves, R, RM)
            name = f"{'B' if var=='plain' else ('C' if var in ('abs','mkt') else 'D')}_L{L}s{skip}_k{k}_{var}"
            allB[name] = (s, W)
            p_all = perf(s.loc["1930":], RF)
            p_00 = perf(s.loc["2000":], RF)
            p_15 = perf(s.loc["2015":], RF)
            ps_all = perf(s_st.loc["1930":], RF)
            res.append(dict(rule=name, fam=name[0], turn_yr=turn.loc["1930":].mean() * 12, hit=wc.detected.mean(),
                            capture_med=wc.capture.median(), capture_mean=wc.capture.mean(), lag_med=wc.lag.median(),
                            postloss_med=wc.post_loss.median(),
                            cagr=p_all["cagr"], sharpe=p_all["sharpe"], maxdd=p_all["maxdd"], cagr_stress=ps_all["cagr"],
                            cagr00=p_00["cagr"], sharpe00=p_00["sharpe"], maxdd00=p_00["maxdd"],
                            cagr15=p_15["cagr"], sharpe15=p_15["sharpe"], maxdd15=p_15["maxdd"]))
    res = pd.DataFrame(res)
    res.to_pickle(os.path.join(OUT, "kurallar_grid.pkl"))
    bm = perf(RM.loc["1930":], RF); bm00 = perf(RM.loc["2000":], RF); bm15 = perf(RM.loc["2015":], RF)
    ew = R.mean(axis=1)
    ewp = perf(ew.loc["1930":], RF); ew00 = perf(ew.loc["2000":], RF); ew15 = perf(ew.loc["2015":], RF)
    print("PIYASA 1930+:", bm, "\n 2000+:", bm00, "\n 2015+:", bm15)
    print("EW49 1930+:", ewp, "\n 2000+:", ew00, "\n 2015+:", ew15)
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", 40)
    pd.set_option("display.max_rows", 500)
    A = res[res.fam == "A"].drop(columns=["turn_yr", "postloss_med", "cagr_stress", "maxdd00", "sharpe15"], errors="ignore")
    print(A.round(3).to_string())
    BC = res[res.fam != "A"][["rule", "turn_yr", "hit", "capture_med", "lag_med", "postloss_med", "cagr", "cagr_stress", "sharpe", "maxdd", "cagr00", "sharpe00", "maxdd00", "cagr15", "sharpe15", "maxdd15"]]
    print(BC.round(3).to_string())
    pd.to_pickle(allB, os.path.join(OUT, "rot_series.pkl"))
    pd.to_pickle({k: (v[0], v[1]) for k, v in allA.items()}, os.path.join(OUT, "rsb_series.pkl"))
