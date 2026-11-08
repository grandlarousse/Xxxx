"""1) S1/S2/S3 bağımsız yeniden üretim + IBS'in ham fiyattan çapraz kontrolü + en büyük 5 kazanç + veri kalitesi kesişimi."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import dt, lib
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40); pd.set_option("display.max_rows", 200)

SY = ["SPY", "QQQ", "IWM", "DIA", "RSP", "MDY"]
D = {s: lib.load(s) for s in SY + ["SSO", "SPXL", "UPRO", "QLD", "TQQQ"]}

# --- IBS çapraz kontrol: ham OHLC (düzeltmesiz) ile düzeltilmiş OHLC aynı IBS'i vermeli
for s in ("SPY", "QQQ"):
    r = dt.raw(s); r = r[r.c > 0]
    ib_raw = ((r.c - r.l) / (r.h - r.l)).clip(0, 1).reindex(D[s].index)
    ib_adj = pd.Series(dt.my_ibs(D[s]), index=D[s].index)
    diff = (ib_raw - ib_adj).abs()
    sr = (ib_raw < 0.1) & (r.c.reindex(D[s].index) < r.c.shift(1).reindex(D[s].index))
    sa = pd.Series(dt.s1_signal(D[s]), index=D[s].index)
    print(f"{s}: |IBS_ham-IBS_duz| maks={diff.max():.2e}; sinyal (ham) {int(sr.sum())} vs (düz.) {int(sa.sum())}; fark gün {(sr != sa).sum()}",
          "| farklı günler:", list(D[s].index[(sr != sa).values][:5].date))

rows = []
TR = {}
for name, sig_fn, ex_fn in (("S1_IBS", dt.s1_signal, None), ("S3_3dusus", dt.s3_signal, dt.up_close)):
    for s in SY:
        d = D[s]; sg = sig_fn(d); ex = ex_fn(d) if ex_fn else None
        for m in ("C0", "O1", "C1", "C2"):
            tr = dt.sim(d, sg, 3, m, ex)
            for pos in (1000, 2500, 10000):
                st = dt.summarize(d, tr, dt.cost_bp(s, pos)); st.update({"strat": name, "sym": s, "mode": m, "pos": pos})
                rows.append(st)
            TR[(name, s, m)] = tr
R = pd.DataFrame(rows)
R.to_csv(os.path.join(dt.OUT, "yeniden_uretim.csv"), index=False)
cols = ["strat", "sym", "mode", "n", "brut_bp", "net_bp", "win", "pf", "t", "is_n", "is_net_bp", "is_t", "oos_n", "oos_net_bp", "oos_t", "yil_poz", "maxdd", "en_kotu_bp"]
print(R[R.pos == 2500][cols].round(2).to_string(index=False))
print("Maliyet duyarlılığı (net bp):")
print(R.pivot_table(index=["strat", "sym", "mode"], columns="pos", values="net_bp").round(1).to_string())

# --- en büyük 5 kazanç (S1 SPY C1, S2 QQQ C1, S3 SPY C0) ve veri kalitesi kesişimi
vk = pd.read_csv(os.path.join(lib.ROOT, "sonuclar", "veri_kalitesi.csv"), parse_dates=["date"])
vd = pd.read_csv(os.path.join(lib.ROOT, "sonuclar", "veri_duzeltmeleri.csv"))
print("veri_duzeltmeleri satırları (aile çekirdeği):", vd[vd.iloc[:, 0].isin(SY + ["SSO", "SPXL", "QLD", "TQQQ"])].to_string())
for key, cost_sym in ((("S1_IBS", "SPY", "C1"), "SPY"), (("S1_IBS", "QQQ", "C1"), "QQQ"), (("S1_IBS", "QQQ", "C0"), "QQQ"), (("S3_3dusus", "SPY", "C0"), "SPY")):
    d = D[key[1]]; tdf = dt.trades_df(d, TR[key], dt.cost_bp(cost_sym, 2500))
    top = tdf.sort_values("brut_bp", ascending=False).head(5)
    print("\nEn büyük 5 kazanç", key); print(top.round(1).to_string(index=False))
    for _, r in top.iterrows():
        hit = vk[(vk.sym.isin([key[1]])) & (vk.date > r.giris) & (vk.date <= r.cikis)]
        if len(hit): print("   veri_kalitesi kesişimi:", hit[["sym", "date", "ret"]].to_dict("records"))
    tdf.to_csv(os.path.join(dt.OUT, f"islemler_{key[0]}_{key[1]}_{key[2]}.csv"), index=False)
    print("En kötü 3:"); print(tdf.sort_values("brut_bp").head(3).round(1).to_string(index=False))
    print("Son 4 işlem:"); print(tdf.tail(4).round(1).to_string(index=False))

# --- kaldıraçlı araçlar: sinyal dayanaktan
print("\nKaldıraçlı araç (sinyal dayanakta, C1 h3, 2.500$):")
for base, inst in (("SPY", "SSO"), ("SPY", "SPXL"), ("SPY", "UPRO"), ("QQQ", "QLD"), ("QQQ", "TQQQ")):
    sb = pd.Series(dt.s1_signal(D[base]), index=D[base].index).reindex(D[inst].index).fillna(False).values
    tr = dt.sim(D[inst], sb, 3, "C1")
    st = dt.summarize(D[inst], tr, dt.cost_bp(inst, 2500))
    print(inst, {k: round(v, 3) if isinstance(v, float) else v for k, v in st.items()})
