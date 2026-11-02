"""S4: Sağlamlık. Bileşenler tek tek / birini-dışarıda-bırak; alternatif kompozitler (geniş endeksler, Japon çelik-dışı, Kore çelik);
eşik / z penceresi / temizlik; geçmiş-beta hedge; regresyon kontrolleri; yoğunlaşma; mevsim (ASX kapanış marjı); plasebo (t-1 sinyal).
Çıktı: res_s4_*.csv"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v, numpy as np, pandas as pd
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 300); pd.set_option("display.max_columns", 40)
JP_AU = ["5411.T", "5401.T", "6301.T", "FMG.AX", "BHP.AX"]
ST = ["EREGL.IS", "KRDMD.IS"]
D = {s: v.decomp(s) for s in ST + ["XU100.IS", "XU030.IS", "BRSAN.IS"]}

def line(sig, st, label, cost=15, thr=1.0, w=250, rez=True, tgt=None, mode="z"):
    y = D[st]["intra"] if tgt is None else tgt
    res, pnl, pos = v.bt(sig, y, cost=cost, mode=mode, thr=thr, w=w, rez=rez)
    r = {"label": label, "stock": st, "cost": cost, "thr": thr, "w": w}
    r.update(v.flat(res)); return r

rows = []
# 1) bileşenler ve LOO
comp = v.composite(JP_AU)
for st in ST:
    rows.append(line(comp, st, "BASE JP_AU"))
    for s in JP_AU:
        rows.append(line(v.composite([s]), st, f"tek {s}"))
        rows.append(line(v.composite([x for x in JP_AU if x != s]), st, f"LOO -{s}"))
    rows.append(line(v.composite(["5411.T", "5401.T", "6301.T"]), st, "yalnız JP (5411,5401,6301)"))
    rows.append(line(v.composite(["FMG.AX", "BHP.AX"]), st, "yalnız AU (FMG,BHP)"))
    rows.append(line(v.composite(["5411.T", "5401.T"]), st, "yalnız JP çelik (5411,5401)"))
    # alternatif / plasebo kompozitler
    rows.append(line(v.composite(["^N225"]), st, "^N225"))
    rows.append(line(v.composite(["^AXJO"]), st, "^AXJO"))
    rows.append(line(v.composite(["^KS11"]), st, "^KS11"))
    rows.append(line(v.composite(["^N225", "^AXJO", "^KS11"]), st, "geniş Asya endeksleri"))
    rows.append(line(v.composite(["8306.T", "9432.T", "7203.T", "6758.T", "9434.T"]), st, "JP çelik-dışı (MUFG,NTT,Toyota,Sony,SoftBank)"))
    rows.append(line(v.composite(["7011.T", "7012.T", "7013.T"]), st, "JP ağır sanayi/savunma (7011,7012,7013)"))
    rows.append(line(v.composite(["005490.KS", "004020.KS"]), st, "Kore çelik (POSCO,Hyundai Steel)"))
    rows.append(line(v.composite(["RIO.AX", "MIN.AX", "CIA.AX", "S32.AX"]), st, "diğer AU madenci (RIO,MIN,CIA,S32)"))
    rows.append(line(v.composite(JP_AU + ["RIO.AX", "005490.KS", "004020.KS", "MIN.AX"]), st, "genişletilmiş çelik/madenci (9)"))
    # eşik, pencere, temizlik, maliyet
    for thr in (0.5, 1.5, 2.0): rows.append(line(comp, st, f"BASE eşik {thr}", thr=thr))
    for w in (120, 500): rows.append(line(comp, st, f"BASE z-pencere {w}", w=w))
    rows.append(line(v.composite(JP_AU, w=500), st, "bileşen z 500 + kompozit z 500", w=500))
    rows.append(line(v.composite(JP_AU, sigma_clip=None), st, "temizliksiz bileşen getirisi"))
    rows.append(line(comp, st, "BASE işaret (eşiksiz)", mode="sign", thr=0.0))
    for c in (0, 8, 25): rows.append(line(comp, st, f"BASE maliyet {c}", cost=c))
    # hedge: geçmiş 250g beta (look-ahead yok)
    a = D[st]["intra"]; m = D["XU100.IS"]["intra"]; m30 = D["XU030.IS"]["intra"]
    for mn, mm in [("XU100", m), ("XU030", m30)]:
        df = pd.concat([a.rename("a"), mm.rename("m")], axis=1).dropna()
        cov = df["a"].rolling(250, min_periods=120).cov(df["m"]).shift(1); var = df["m"].rolling(250, min_periods=120).var().shift(1)
        b = (cov / var); hed = df["a"] - b * df["m"]
        rows.append(line(comp, st, f"hedge geçmiş-beta {mn}", tgt=hed))
        rows.append(line(comp, st, f"hedge beta=1 {mn}", tgt=df["a"] - df["m"]))
    # plasebo: dünkü sinyal (t-1) -> intra_t
    rows.append(line(comp.shift(1), st, "PLASEBO kompozit t-1"))
R = pd.DataFrame(rows); R.to_csv(os.path.join(v.OUT, "res_s4_variants.csv"), index=False)
cols = ["label", "stock", "cost", "IS_n", "IS_bps", "IS_t", "OOS_n", "OOS_bps", "OOS_t", "OOS_sh", "yrs_pos"]
for st in ST:
    print(st); print(R[R.stock == st][cols].round(2).to_string(index=False))
