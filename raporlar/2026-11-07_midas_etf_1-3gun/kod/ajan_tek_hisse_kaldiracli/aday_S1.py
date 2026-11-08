"""Aday strateji tek_hisse_kaldiracli_S1 — hisse RSI(2) dibi (hisse 200 günlük ortalamanın üstünde), 2x tek hisse ETF ile,
çıkış: hisse kapanışı 5 günlük ortalamanın üstüne çıktığı ilk gün (en fazla 3 gün). Ön-kayıtlı hipotez TH03 (notlar/hipotezler.csv).
Sinyal: dayanak hisse (NVDA, TSLA, AAPL, AMZN, META, MSFT, GOOGL). İşlem: NVDL, TSLL, AAPU, AMZU, METU, MSFU, GGLL.
Çalıştırma (sayıları basar): python3 -I kod/ajan_tek_hisse_kaldiracli/aday_S1.py
Çıktılar: sonuclar/aile_tek_hisse_kaldiracli/aday_S1_*.csv, aday_S1_cikti.txt"""
import os, sys, math, io, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import thk, lib

pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40); pd.set_option("display.max_rows", 300)
STK = ["NVDA", "TSLA", "AAPL", "AMZN", "META", "MSFT", "GOOGL"]
ETF = {s: thk.PRIMARY[s] for s in STK}
SWITCH = {"NVDL": "2024-02-01", "TSLL": "2024-04-10", "AAPU": "2024-04-10", "AMZU": "2024-04-15", "METU": "2024-06-06",
          "MSFU": "2024-04-10", "GGLL": "2024-04-10", "NVDU": "2024-04-15", "MSTU": "2024-09-19", "CONL": "2024-02-01"}

def SIG(sdf, thr=10, trend=True):
    c = sdf["c"]; s = lib.rsi(c, 2) < thr
    if trend: s = s & (c > lib.sma(c, 200))
    s.iloc[:200] = False
    return s
def EXIT(sdf): return sdf["c"] > lib.sma(sdf["c"], 5)

_S = {s: thk.load_stock(s) for s in STK + ["MSTR", "COIN"]}
_Y = {s: thk.synth_for(s, 2.0) for s in _S}

# bilanço tarihleri (varsa): duyuru E (genelde seans sonrası). Tutuş [giriş kapanışı, çıkış kapanışı] arasında
# E kapanışından sonraki tepki günü (E+1) varsa işlem 'bilanco_iceren' sayılır.
BIL = None
bp = os.path.join(thk.OUT, "bilanco_tarihleri.csv")
if os.path.exists(bp):
    BIL = pd.read_csv(bp, parse_dates=["date"])

def earn_flag(tr, st, idx):
    if BIL is None or len(tr) == 0: return pd.Series(False, index=tr.index)
    E = BIL[BIL.sym == st]
    pos = pd.Series(np.arange(len(idx)), index=idx)
    react = set()
    for _, r in E.iterrows():
        d = r["date"]
        a = idx[idx >= d]
        if not len(a): continue
        bmo = str(r.get("time", "")).find("pre-market") >= 0
        i = pos[a[0]] if bmo else (pos[a[0]] + 1 if a[0] == d else pos[a[0]])
        if i < len(idx): react.add(idx[i])
    out = []
    for _, t in tr.iterrows():
        ie, ix = pos[t.entry_date], pos[t.exit_date]
        # tepki günü girişten sonraki bir gün olmalı (O1'de giriş günü açılış boşluğu zaten yaşanmış olur)
        lo = ie + 1
        out.append(any(idx[j] in react for j in range(lo, ix + 1)))
    return pd.Series(out, index=tr.index)

def edge_matched(A, mode, data="synth"):
    """Zamanlama kenarı: her işlemin brüt getirisi - aynı tutuş süresi ve giriş yapısındaki koşulsuz ortalama
    (a) tüm günler, (b) yalnız hisse>SMA200 günleri (rejim tabanı). Tarih kümelemeli t."""
    ex = []
    for st in A.stock.unique():
        df = _Y[st] if data == "synth" else lib.load(ETF[st])
        c = df["c"]; o = df["o"]; sdf = _S[st].reindex(df.index)
        trd = sdf["c"] > lib.sma(sdf["c"], 200)
        a = A[A.stock == st]
        for d in sorted(a.days.unique()):
            if mode == "O1": f = c.shift(-(d - 1)) / o - 1                      # giriş günü açılış -> d. günün kapanışı
            elif mode == "C1": f = (c.shift(-d) / c - 1).shift(-1)             # bir gün sonra kapanış girişi
            else: f = c.shift(-d) / c - 1
            f = f.loc[a.sig_date.min():]
            b_all = f.mean(); b_tr = f[trd.reindex(f.index).fillna(False)].mean()
            for _, r in a[a.days == d].iterrows():
                ex.append((r.sig_date, r.gross - b_all, r.gross - b_tr))
    E = pd.DataFrame(ex, columns=["d", "ex_all", "ex_tr"])
    out = {}
    for col in ("ex_all", "ex_tr"):
        g = E.groupby("d")[col].mean()
        out[col] = (g.mean() * 1e4, g.mean() / (g.std() / math.sqrt(len(g))),
                    g[g.index <= lib.IS_END].mean() * 1e4, g[g.index > lib.IS_END].mean() * 1e4)
    return out

def run_set(stocks, mode, thr=10, trend=True, exit_rule=True, h=3, pos=2500.0, data="synth", etf_map=None, since=None, earn="dahil"):
    trs = []; rows = []
    for st in stocks:
        sdf = _S[st]
        if data == "synth":
            df = _Y[st]; e = (etf_map or ETF).get(st, thk.PRIMARY.get(st))
        else:
            e = (etf_map or ETF)[st]; df = lib.load(e)
        sig = SIG(sdf, thr, trend).reindex(df.index).fillna(False)
        if since is not None:
            sig = sig & (df.index >= pd.Timestamp(since.get(e, "1900-01-01")))
        ex = EXIT(sdf).reindex(df.index).fillna(False) if exit_rule else None
        cost = 2 * lib.COMM_USD / pos * 1e4 + thk.spread_bp(e)
        s, tr = lib.evaluate(df, sig, h=h, mode=mode, cost=cost, exit_sig=ex)
        if len(tr):
            tr = tr.assign(stock=st, etf=e, mode_=mode, excess=tr.gross - s.get("uncond_bp", 0) / 1e4)
            tr["bilanco"] = earn_flag(tr, st, df.index).values
            if earn == "haric":
                tr = tr[~tr.bilanco]
            elif earn == "yalniz":
                tr = tr[tr.bilanco]
            s2 = lib.stats(tr, df, h, mode) if len(tr) else {"n": 0}
            s2["cost_bp"] = cost
            s = s2 if earn != "dahil" else s
        rows.append(dict(stock=st, etf=e, mode=mode, **{k: s.get(k, np.nan) for k in
                    ["n", "mean_gross_bp", "mean_net_bp", "t", "win", "pf", "maxdd", "worst_bp", "edge_bp", "t_edge",
                     "is_net_bp", "is_t", "oos_net_bp", "oos_t", "years_pos_frac", "cost_bp"]}))
        trs.append(tr)
    n, nd, mb, t = thk.pooled_date_t(trs)
    _, _, gb, _ = thk.pooled_date_t(trs, "gross")
    _, _, eb, te = thk.pooled_date_t(trs, "excess")
    _, ni, mi, ti = thk.pooled_date_t([x[x.sig_date <= lib.IS_END] for x in trs if len(x)])
    _, no, mo, to = thk.pooled_date_t([x[x.sig_date > lib.IS_END] for x in trs if len(x)])
    A = pd.concat([x for x in trs if len(x)], ignore_index=True) if any(len(x) for x in trs) else pd.DataFrame(columns=["sig_date", "net", "gross"])
    g = A.groupby("sig_date")["net"].mean().sort_index() if len(A) else pd.Series(dtype=float)
    yrs = g.groupby(g.index.year).sum() if len(g) else pd.Series(dtype=float)
    wins = A.net[A.net > 0].sum(); loss = -A.net[A.net < 0].sum()
    eq = (1 + g / len(stocks)).cumprod() if len(g) else pd.Series([1.0])   # her sinyal tarihine 1/7 sermaye (kaba portföy)
    dd = float((eq / eq.cummax() - 1).min()) if len(eq) else np.nan
    pool = {"n": n, "n_tarih": nd, "brut_bp": gb, "net_bp": mb, "t": t, "edge_bp": eb, "t_edge": te, "is_n": ni, "is_net_bp": mi, "is_t": ti,
            "oos_n": no, "oos_net_bp": mo, "oos_t": to, "kazanma": float((A.net > 0).mean()) if len(A) else np.nan,
            "pf": float(wins / loss) if loss > 0 else np.nan, "yil_poz": float((yrs > 0).mean()) if len(yrs) else np.nan,
            "en_kotu_bp": float(A.net.min() * 1e4) if len(A) else np.nan, "maxdd_portfoy_1_7": dd,
            "p": lib.t_to_p(t, nd) if nd else np.nan}
    return pool, pd.DataFrame(rows), A, yrs

def main():
    P = []; HROWS = []
    print("=" * 100); print("S1 — DAYANAK (sentetik kalibre 2x, 2016-11..2026-11), 7 mega-cap; maliyet 2.500$ (birincil ETF makası dahil)")
    for m in ("C0", "O1", "C1"):
        pool, rows, A, yrs = run_set(STK, m)
        P.append(dict(test="dayanak_7", mode=m, **pool)); HROWS.append(rows.assign(veri="dayanak_sentetik"))
        print(f"\n[{m}] havuz:", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in pool.items()})
        print(rows.round(2).to_string(index=False))
        em = edge_matched(A, m)
        print(f"Zamanlama kenarı (tutuş süresi eşlenmiş taban): tüm günler {em['ex_all'][0]:.1f} bp t {em['ex_all'][1]:.2f} (IS {em['ex_all'][2]:.1f}, OOS {em['ex_all'][3]:.1f}); "
              f"hisse>SMA200 günleri tabanı {em['ex_tr'][0]:.1f} bp t {em['ex_tr'][1]:.2f} (IS {em['ex_tr'][2]:.1f}, OOS {em['ex_tr'][3]:.1f})")
        P[-1].update({"edge_eslenik_bp": em["ex_all"][0], "t_edge_eslenik": em["ex_all"][1], "edge_rejim_bp": em["ex_tr"][0], "t_edge_rejim": em["ex_tr"][1]})
        if m == "C0":
            print("Yıllık (tarih başına ortalama net toplamı, bp):", (yrs * 1e4).round(0).to_dict())
            A.to_csv(os.path.join(thk.OUT, "aday_S1_islemler_dayanak_C0.csv"), index=False)
            # eşzamanlı pozisyon sayısı
            conc = []
            for d in sorted(set(A.entry_date)):
                conc.append(((A.entry_date <= d) & (A.exit_date > d)).sum())
            print("Eşzamanlı açık pozisyon: medyan", int(np.median(conc)), "maks", int(max(conc)))
    print("\nMaliyet duyarlılığı (dayanak, havuz):")
    for m in ("C0", "O1"):
        for pos in (1000.0, 2500.0, 10000.0):
            pool, _, _, _ = run_set(STK, m, pos=pos)
            P.append(dict(test=f"maliyet_{int(pos)}", mode=m, **pool))
            print(f"  {m} {int(pos)}$: net {pool['net_bp']:.1f} bp, t {pool['t']:.2f}")
    print("\nKomşu parametreler (dayanak havuzu; ana kural: RSI<10, trend filtresi, SMA5 çıkış<=3g). Parametre SEÇİLMEDİ, yalnız rapor:")
    for m in ("C0", "O1"):
        for thr in (5, 10, 15):
            for trend in (True, False):
                for ex, h in ((True, 3), (False, 1), (False, 2), (False, 3)):
                    pool, _, _, _ = run_set(STK, m, thr=thr, trend=trend, exit_rule=ex, h=h)
                    P.append(dict(test=f"komsu_rsi{thr}_{'trend' if trend else 'trendsiz'}_{'sma5' if ex else 'sabit'}_h{h}", mode=m, **pool))
                    print(f"  {m} RSI<{thr:>2} {'trend ' if trend else 'trdsiz'} {'SMA5<=3' if ex else f'sabit h{h}':>8}: n {pool['n']:4d} net {pool['net_bp']:7.1f} t {pool['t']:5.2f} | IS {pool['is_net_bp']:7.1f} ({pool['is_t']:.2f}) OOS {pool['oos_net_bp']:7.1f} ({pool['oos_t']:.2f}) | edge t {pool['t_edge']:.2f}")
    print("\nAile içi kontrol: MSTR, COIN (kripto vekilleri; TH03 kapsamı dışı)")
    for m in ("C0", "O1"):
        pool, rows, _, _ = run_set(["MSTR", "COIN"], m)
        P.append(dict(test="dayanak_kripto", mode=m, **pool))
        print(f"  {m}: n {pool['n']} net {pool['net_bp']:.1f} t {pool['t']:.2f}; hisse:", rows[["stock", "n", "mean_net_bp", "t"]].round(2).values.tolist())
    print("\n" + "=" * 100); print("S1 — GERÇEK ETF VERİSİ (sinyal hisseden, işlem ETF fiyatında); 2022-2024'te Direxion/GraniteShares ürünleri 1,5x idi")
    for m in ("C0", "O1", "C1"):
        for since, lab in ((None, "tum"), (SWITCH, "2x_donemi")):
            pool, rows, A, yrs = run_set(STK, m, data="etf", since=since)
            P.append(dict(test=f"gercek_etf_{lab}", mode=m, **pool)); HROWS.append(rows.assign(veri=f"gercek_etf_{lab}"))
            print(f"\n[{m}] gerçek ETF ({lab}) havuz: n {pool['n']} tarih {pool['n_tarih']} brüt {pool['brut_bp']:.1f} net {pool['net_bp']:.1f} t {pool['t']:.2f} kazanma {pool['kazanma']:.2f} PF {pool['pf']:.2f} yıl+ {pool['yil_poz']:.2f} en kötü {pool['en_kotu_bp']:.0f}")
            if lab == "tum":
                em = edge_matched(A, m, data="etf")
                print(f"  gerçek ETF zamanlama kenarı: tüm günler {em['ex_all'][0]:.1f} bp t {em['ex_all'][1]:.2f}; SMA200 rejim tabanı {em['ex_tr'][0]:.1f} bp t {em['ex_tr'][1]:.2f}")
                print(rows[["etf", "n", "mean_gross_bp", "mean_net_bp", "t", "win", "worst_bp", "maxdd", "years_pos_frac", "cost_bp"]].round(2).to_string(index=False))
                if m == "C0":
                    A.to_csv(os.path.join(thk.OUT, "aday_S1_islemler_gercek_C0.csv"), index=False)
                    # ETF işlem getirisi - 2 x hisse getirisi (aynı giriş/çıkış)
                    dev = []
                    for st in STK:
                        x = A[A.stock == st]
                        if not len(x): continue
                        sc = _S[st]["c"]
                        r = sc.reindex(x.exit_date).values / sc.reindex(x.entry_date).values - 1
                        dev.append((ETF[st], len(x), float(((x.gross.values - 2 * r)).mean() * 1e4)))
                    print("ETF işlem brüt getirisi − 2×hisse (bp; 2022-24 1,5x dönemi dahil olduğundan negatif/pozitif sapabilir):", dev)
    # NVDU kopyası
    pool, rows, _, _ = run_set(["NVDA"], "C0", data="etf", etf_map={"NVDA": "NVDU"})
    print("\nKopya NVDU (C0):", rows[["etf", "n", "mean_net_bp", "t"]].round(2).values.tolist())
    pool, rows, _, _ = run_set(["NVDA"], "C0", data="etf")
    print("NVDL aynı dönem karşılaştırma (C0, tüm):", rows[["etf", "n", "mean_net_bp", "t"]].round(2).values.tolist())
    # Ters ayna (beklenen negatif)
    for st, e in (("TSLA", "TSLQ"), ("NVDA", "NVDS")):
        pool, rows, _, _ = run_set([st], "C0", data="etf", etf_map={st: e})
        print(f"Ayna: aynı sinyalle {e} almak (beklenen negatif):", rows[["etf", "n", "mean_net_bp", "t"]].round(2).values.tolist())
    print("\n" + "=" * 100); print("Bilanço etkisi (tutuş içinde bilanço tepki günü olan işlemler)")
    if BIL is None:
        print("  bilanco_tarihleri.csv yok")
    else:
        for m in ("C0", "O1"):
            for earn in ("dahil", "haric", "yalniz"):
                pool, rows, _, yrs = run_set(STK, m, earn=earn)
                P.append(dict(test=f"bilanco_{earn}", mode=m, **pool))
                print(f"  {m} bilanço {earn:>6}: n {pool['n']:4d} net {pool['net_bp']:7.1f} t {pool['t']:5.2f} IS {pool['is_net_bp']:7.1f} ({pool['is_t']:.2f}) OOS {pool['oos_net_bp']:7.1f} ({pool['oos_t']:.2f}) yıl+ {pool['yil_poz']:.2f} en kötü {pool['en_kotu_bp']:.0f}")
                if earn == "haric":
                    print("     yıllık:", (yrs * 1e4).round(0).to_dict())
            for earn in ("haric",):
                pool, rows, _, _ = run_set(STK, m, earn=earn, data="etf")
                P.append(dict(test=f"bilanco_{earn}_gercek_etf", mode=m, **pool))
                print(f"  {m} gerçek ETF bilanço {earn}: n {pool['n']} net {pool['net_bp']:.1f} t {pool['t']:.2f}")
            for pos in (1000.0, 10000.0):
                pool, _, _, _ = run_set(STK, m, earn="haric", pos=pos)
                P.append(dict(test=f"bilanco_haric_maliyet_{int(pos)}", mode=m, **pool))
                print(f"  {m} bilanço hariç {int(pos)}$: net {pool['net_bp']:.1f} t {pool['t']:.2f}")
    print("\n" + "=" * 100); print("Güncel durum (son veri 2026-11-06 kapanışı):")
    for st in STK:
        sdf = _S[st]; c = sdf["c"]
        r2 = lib.rsi(c, 2).iloc[-1]; s200 = lib.sma(c, 200).iloc[-1]; s5 = lib.sma(c, 5).iloc[-1]
        print(f"  {st:5s} kapanış {c.iloc[-1]:9.2f}  RSI2 {r2:6.1f}  SMA200 {s200:9.2f} ({'üstünde' if c.iloc[-1] > s200 else 'ALTINDA'})  SMA5 {s5:9.2f}  sinyal: {'EVET' if (r2 < 10 and c.iloc[-1] > s200) else 'hayır'}")
    pd.DataFrame(P).to_csv(os.path.join(thk.OUT, "aday_S1_ozet.csv"), index=False)
    pd.concat(HROWS, ignore_index=True).to_csv(os.path.join(thk.OUT, "aday_S1_hisse_etf.csv"), index=False)

if __name__ == "__main__":
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        main()
    txt = buf.getvalue(); print(txt)
    open(os.path.join(thk.OUT, "aday_S1_cikti.txt"), "w").write(txt)
