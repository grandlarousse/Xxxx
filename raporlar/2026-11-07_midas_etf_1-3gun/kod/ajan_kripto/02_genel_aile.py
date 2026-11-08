"""2) Genel kütüphane (strategies.LIB) aile içi tutarlılık + uzun geçmişli dayanak (BTC/ETH) üzerinde aynı sinyaller.
Çalıştır: python3 -I kod/ajan_kripto/02_genel_aile.py
 (a) sonuclar/genel_tum.csv aile satırları (16 ETF x 297 satır)
 (b) aynı 31 sinyal: BTC_D ve ETH_D (2016-11..2026-11, günlük UTC mum, NYSE günlerine örneklenmiş; C0 ve C1),
     BTC_ET ve ETH_ET (2023-06..2026-11, 16:00 ET saatlik; C0/O1/C1). Maliyet: IBIT (BTC) / ETHA (ETH) 2.500$.
 (c) aile içi BH-FDR (q=0.10) tüm satırlarda; tutarlılık bağımsız dayanak temsilcilerinde sayılır.
Çıktı: sonuclar/aile_kripto/genel_aile_satirlar.csv, genel_aile_tutarlilik.csv, genel_dayanak_satirlar.csv"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import kr, lib
import strategies as S

g = pd.read_csv(os.path.join(kr.ROOT, "sonuclar", "genel_tum.csv"))
fam = g[g.sym.isin(kr.FAM)].copy()
fam["kaynak"] = "genel_tum"

CTX = {"VIX": lib.vol_index("VIX"), "VIX3M": lib.vol_index("VIX3M")}

def edges(df, tr, h, mode):
    u = lib.uncond(df, h, mode).dropna(); out = {}
    for nm, mt, mu in (("is", tr.sig_date <= lib.IS_END, u.index <= lib.IS_END), ("oos", tr.sig_date > lib.IS_END, u.index > lib.IS_END)):
        if mt.sum() > 1:
            uu = u[mu]; uu = uu[uu.index >= tr.sig_date[mt].min()]
            out[nm + "_edge_bp"] = (tr.gross[mt].mean() - uu.mean()) * 1e4
    return out

def run_lib(df, name, spread, modes):
    rows = []
    for sn, fn in S.LIB.items():
        try:
            sig = fn(df, CTX).reindex(df.index).fillna(False).astype(bool)
        except Exception as e:
            print("hata", sn, e); continue
        sig.iloc[:60] = False
        for mode in modes:
            for h in (1, 2, 3):
                s, tr = kr.full_eval(df, sig, h, mode, spread, label=sn)
                if s.get("n", 0) > 1: s.update(edges(df, tr, h, mode))
                s.update({"sym": name, "sig": sn, "exit": "sabit", "n_sig_days": int(sig.sum())})
                rows.append(s)
            if sn in S.EXITS:
                s, tr = kr.full_eval(df, sig, 3, mode, spread, exit_sig=S.EXITS[sn](df), label=sn)
                s.update({"sym": name, "sig": sn, "exit": "kural_max3", "n_sig_days": int(sig.sum())})
                rows.append(s)
    return rows

sp_btc = kr.spread_bp("IBIT"); sp_eth = kr.spread_bp("ETHA")
rows = []
rows += run_lib(kr.crypto_daily_proxy("BTC-USD"), "BTC_D", sp_btc, ("C0", "C1"))
rows += run_lib(kr.crypto_daily_proxy("ETH-USD"), "ETH_D", sp_eth, ("C0", "C1"))
rows += run_lib(kr.crypto_et_proxy("BTC-USD"), "BTC_ET", sp_btc, ("C0", "O1", "C1"))
rows += run_lib(kr.crypto_et_proxy("ETH-USD"), "ETH_ET", sp_eth, ("C0", "O1", "C1"))
dy = pd.DataFrame(rows)
dy["kaynak"] = "dayanak_proxy"
dy.to_csv(os.path.join(kr.OUT, "genel_dayanak_satirlar.csv"), index=False)

allr = pd.concat([fam, dy], ignore_index=True)
allr["fdr_aile"] = lib.bh_fdr(allr["p"].values, 0.10)
n_tests = int(allr["p"].notna().sum())
allr.to_csv(os.path.join(kr.OUT, "genel_aile_satirlar.csv"), index=False)
print("Aile genel test sayısı (p'li satır):", n_tests, " FDR geçen:", int(allr.fdr_aile.sum()),
      " FDR geçen & net>0:", int((allr.fdr_aile & (allr.mean_net_bp > 0)).sum()))
print(allr[allr.fdr_aile][["sym", "sig", "mode", "h", "exit", "n", "mean_gross_bp", "mean_net_bp", "t", "is_net_bp", "oos_net_bp", "years_pos_frac"]].round(2).to_string())

# tutarlılık: bağımsız dayanak temsilcileri
REP = ["IBIT", "ETHA", "BLOK", "MSTU", "CONL"]       # ETF'ler (kaldıraçsız temsilci; MSTU/CONL kendi araçları)
key = ["sig", "mode", "h", "exit"]
def piv(name, col="mean_net_bp"):
    return allr[allr.sym == name].set_index(key)[col]
agg = []
base = allr[allr.sym == "BTC_D"].set_index(key)
for k, r in base.iterrows():
    rec = dict(zip(key, k))
    rec.update({"BTC_D_n": r.n, "BTC_D_net": r.mean_net_bp, "BTC_D_t": r.t, "BTC_D_is": r.is_net_bp, "BTC_D_oos": r.oos_net_bp,
                "BTC_D_edge": r.edge_bp, "BTC_D_is_edge": r.get("is_edge_bp", np.nan), "BTC_D_oos_edge": r.get("oos_edge_bp", np.nan),
                "BTC_D_yil": r.years_pos_frac, "BTC_D_fdr": r.fdr_aile})
    for nm in ["ETH_D", "BTC_ET", "ETH_ET"]:
        try:
            rr = allr[(allr.sym == nm) & (allr.sig == k[0]) & (allr["mode"] == k[1]) & (allr.h == k[2]) & (allr.exit == k[3])].iloc[0]
            rec[nm + "_net"] = rr.mean_net_bp; rec[nm + "_t"] = rr.t
            if nm == "ETH_D":
                rec["ETH_D_is"] = rr.is_net_bp; rec["ETH_D_oos"] = rr.oos_net_bp
                rec["ETH_D_is_edge"] = rr.get("is_edge_bp", np.nan); rec["ETH_D_oos_edge"] = rr.get("oos_edge_bp", np.nan)
        except IndexError:
            pass
    sub = allr[(allr.sym.isin(REP)) & (allr.sig == k[0]) & (allr["mode"] == k[1]) & (allr.h == k[2]) & (allr.exit == k[3])]
    rec["etf_pos"] = int((sub.mean_net_bp > 0).sum()); rec["etf_n"] = len(sub)
    for s in REP:
        v = sub[sub.sym == s]
        rec[s + "_net"] = float(v.mean_net_bp.iloc[0]) if len(v) else np.nan
        rec[s + "_t"] = float(v.t.iloc[0]) if len(v) else np.nan
    agg.append(rec)
A = pd.DataFrame(agg)
A["uzun_tutarli"] = (A.BTC_D_is > 0) & (A.BTC_D_oos > 0) & (A.ETH_D_is > 0) & (A.ETH_D_oos > 0) & (A.BTC_D_yil >= 0.6)
A["etf_tutarli"] = A["uzun_tutarli"] & (A.BTC_ET_net > 0) & (A.IBIT_net > 0) & (A.etf_pos >= 4)
# drift'ten arındırılmış: kenar (brüt - koşulsuz aynı tutuş) IS ve OOS'ta BTC_D ve ETH_D'de > 0
A["kenar_tutarli"] = A["uzun_tutarli"] & (A.BTC_D_is_edge > 0) & (A.BTC_D_oos_edge > 0) & (A.ETH_D_is_edge > 0) & (A.ETH_D_oos_edge > 0)
A = A.sort_values("BTC_D_t", ascending=False)
A.to_csv(os.path.join(kr.OUT, "genel_aile_tutarlilik.csv"), index=False)
pd.set_option("display.width", 300); pd.set_option("display.max_columns", 50)
print("\nUzun geçmiş BTC_D+ETH_D'de IS ve OOS>0 (yılların>=%60'ı +):", int(A.uzun_tutarli.sum()), "/", len(A))
print(A[A.uzun_tutarli].round(1).to_string(index=False))
print("\nETF'lerde de tutarlı:", int(A.etf_tutarli.sum()))
print("Kenar (drift arındırılmış) IS ve OOS > 0, BTC_D ve ETH_D:", int(A.kenar_tutarli.sum()))
print(A[A.kenar_tutarli][["sig", "mode", "h", "exit", "BTC_D_n", "BTC_D_net", "BTC_D_t", "BTC_D_is_edge", "BTC_D_oos_edge", "ETH_D_is_edge", "ETH_D_oos_edge", "BTC_ET_net", "IBIT_net", "IBIT_t", "etf_pos"]].round(1).to_string(index=False))
print("\nBTC_D en yüksek t ilk 25:")
print(A.head(25).round(1).to_string(index=False))
