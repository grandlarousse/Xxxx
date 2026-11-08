"""Denetim: hayatta kalma / seçim yanlılığı testi ve piyasa-geneli ayrıştırması.
(1) Aynı S1 kuralı (değişmeden) ex-ante evrende: Kasım 2016'da piyasa değeri en büyük ~30 ABD hissesi (S1'in 7 hissesi hariç),
    TSM/AVGO ve tek hisse kaldıraçlı ETF'i olan diğer hisseler. Sentetik 2x (gider %1,05 + finansman + 2 bp/gün ek), maliyet 16 bp.
    Zamanlama kenarı: işlemin brüt getirisi - aynı hissede, rejim (hisse>SMA200) günlerinden rastgele girişlerin ortalaması
    (aynı tutuş süresi). Tarih kümelemeli t.
(2) 7 mega-cap S1 işlemlerini piyasa-geneli dip (aynı gün QQQ RSI(2)<10) ve hisseye özgü dip olarak ayır; ayrıca aynı kural
    QQQ üzerinde (sentetik 2x QQQ = QLD benzeri) ve 'yalnız QQQ dibi' sinyaliyle 7 hisse.
Çalıştır: python3 -I kod/denetim_tek_hisse_kaldiracli/d4_hayatta_kalma.py"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import io, contextlib, math
import numpy as np, pandas as pd
import dk, lib, d0_veri

EXTRA = {"NVDA": 2.84, "TSLA": 2.75, "AAPL": 1.28, "AMZN": 2.13, "META": 1.80, "MSFT": 1.10, "GOOGL": 1.55}
RNG = np.random.default_rng(7)

def group_run(stocks, mode="C0", extra_default=2.0):
    rows = []; edges = []
    for st in stocks:
        sd = dk.load_stock(st)
        if len(sd) < 400: continue
        px = dk.synth(sd, extra_bp=EXTRA.get(st, extra_default))
        sig = dk.signal(sd); exc = dk.exit_cond(sd)
        Pc = px["c"].values; Po = px["o"].values
        tr = dk.sim(sig, exc, Pc, Po, mode, 3)
        c = sd["c"].values; trend = np.nan_to_num(c > dk.sma(c, 200), nan=0).astype(bool)
        elig = np.arange(200, len(c) - 5); elig = elig[trend[elig]]
        # rejim eşlenik taban: her tutuş süresi için rejim günlerinden ortalama ileri getiri
        base = {}
        for h in (1, 2, 3):
            if mode == "C0": f = Pc[elig + h] / Pc[elig] - 1
            else: f = Pc[elig + h - 1 + 1] / Po[elig + 1] - 1 if False else Pc[elig + h] / Po[elig + 1] - 1
            base[h] = f.mean()
        cost = 16.0
        for (i, e, x, g) in tr:
            d = x - e + (1 if mode == "O1" else 0)
            hh = x - i
            rows.append((st, sd.index[i], d, g, g - cost / 1e4, g - base.get(hh, base[3])))
    A = pd.DataFrame(rows, columns=["stock", "sig_date", "days", "gross", "net", "excess"])
    return A

def show(A, lab):
    if len(A) < 5:
        print(f"  {lab}: n {len(A)}"); return {}
    s = dk.summary(A); e = dk.pooled(A, "excess")
    per = A.groupby("stock")["net"].mean()
    print(f"  {lab:46s} hisse {A.stock.nunique():2d} n {s['n']:5d} net {s['net_bp']:6.1f} t {s['t']:5.2f} | IS {s['is_bp']:6.1f} ({s['is_t']:.2f}) OOS {s['oos_bp']:6.1f} ({s['oos_t']:.2f}) | "
          f"kenar {e['bp']:6.1f} t {e['t']:.2f} | hisse net>0 oranı {float((per > 0).mean()):.2f}")
    return dict(grup=lab, hisse=A.stock.nunique(), n=s["n"], net_bp=s["net_bp"], t=s["t"], is_bp=s["is_bp"], is_t=s["is_t"],
                oos_bp=s["oos_bp"], oos_t=s["oos_t"], kenar_bp=e["bp"], kenar_t=e["t"], hisse_poz_oran=float((per > 0).mean()))

def main():
    out = []
    print("=" * 110)
    print("(1) Aynı S1 kuralı, farklı evrenler (sentetik 2x, maliyet 16 bp):")
    groups = {"S1_7_megacap (ajan seçimi)": dk.STK,
              "ex-ante 2016 en büyük 30 (S1 7'si hariç)": d0_veri.EXANTE_2016,
              "diğer LETF dayanakları (15)": d0_veri.LETF_OTHER,
              "TSM+AVGO (veride var, S1 dışında)": ["TSM", "AVGO"]}
    keep = {}
    for mode in ("C0", "O1"):
        print(f" [{mode}]")
        for lab, stocks in groups.items():
            A = group_run(stocks, mode); keep[(lab, mode)] = A
            r = show(A, lab); r.update(mode=mode); out.append(r)
        A = pd.concat([keep[(k, mode)] for k in groups if not k.startswith("S1")], ignore_index=True)
        r = show(A, "S1 dışı tüm hisseler (47)"); r.update(mode=mode); out.append(r)
        Ex = keep[("ex-ante 2016 en büyük 30 (S1 7'si hariç)", mode)]
        print("    ex-ante evrende hisse başına net (bp):", Ex.groupby("stock")["net"].mean().mul(1e4).round(0).sort_values().to_dict())
        ex7 = pd.concat([Ex, keep[("S1_7_megacap (ajan seçimi)", mode)][keep[("S1_7_megacap (ajan seçimi)", mode)].stock.isin(["AAPL", "MSFT", "GOOGL", "AMZN", "META"])]])
        r = show(ex7, "ex-ante 2016 en büyük 35 (S1'in 5'i dahil)"); r.update(mode=mode); out.append(r)
    pd.DataFrame(out).to_csv(os.path.join(dk.OUT, "d4_evrenler.csv"), index=False)

    print("\n(2) Piyasa-geneli dip ayrıştırması (7 mega-cap, C0):")
    q = lib.load("QQQ"); qr = pd.Series(dk.rsi_wilder(q["c"].values, 2), index=q.index)
    A = pd.read_csv(os.path.join(dk.OUT, "d2_islemler_C0.csv"), parse_dates=["sig_date", "entry_date", "exit_date"])
    A["qqq_dip"] = (qr.reindex(A.sig_date).values < 10)
    for lab, a in (("QQQ RSI2<10 aynı gün (piyasa dibi)", A[A.qqq_dip]), ("QQQ RSI2>=10 (hisseye özgü dip)", A[~A.qqq_dip])):
        s = dk.summary(a); print(f"  {lab:38s} n {s['n']:4d} net {s['net_bp']:6.1f} t {s['t']:.2f} IS {s['is_bp']:.1f} OOS {s['oos_bp']:.1f} işlem-ort {s['net_islem_bp']:.1f}")
    # QQQ üzerinde aynı kural, sentetik 2x QQQ (QLD benzeri)
    qd = q[["o", "h", "l", "c", "v"]].copy()
    for mode in ("C0", "O1"):
        px = dk.synth(qd, extra_bp=1.0); sig = dk.signal(qd); exc = dk.exit_cond(qd)
        tr = dk.sim(sig, exc, px["c"].values, px["o"].values, mode, 3)
        g = np.array([x[3] for x in tr]); dts = [qd.index[x[0]] for x in tr]
        net = g - 16 / 1e4
        isn = np.array([d <= dk.IS_END for d in dts])
        print(f"  QQQ kendi sinyali -> 2x QQQ [{mode}]: n {len(g)} net {net.mean() * 1e4:.1f} t {dk.tstat(net):.2f} IS {net[isn].mean() * 1e4:.1f} OOS {net[~isn].mean() * 1e4:.1f}")
    # QQQ sinyali -> 7 hisse 2x (hisse sinyali yerine)
    for mode in ("C0",):
        rows = []
        qs = pd.Series(dk.signal(qd), index=qd.index)
        for st in dk.STK:
            sd = dk.load_stock(st); px = dk.synth(sd, extra_bp=EXTRA[st])
            sig = qs.reindex(sd.index).fillna(False).values.astype(bool)
            tr = dk.sim(sig, dk.exit_cond(sd), px["c"].values, px["o"].values, mode, 3)
            for (i, e, x, g) in tr: rows.append((st, sd.index[i], g, g - dk.cost(dk.ETF[st]) / 1e4))
        B = pd.DataFrame(rows, columns=["stock", "sig_date", "gross", "net"])
        s = dk.summary(B.assign(days=0)); print(f"  QQQ sinyali (RSI2<10 & >SMA200) -> 7 hisse 2x [{mode}]: n {s['n']} net {s['net_bp']:.1f} t {s['t']:.2f} IS {s['is_bp']:.1f} OOS {s['oos_bp']:.1f}")

if __name__ == "__main__":
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        main()
    txt = buf.getvalue(); print(txt)
    open(os.path.join(dk.OUT, "d4_cikti.txt"), "w").write(txt)
