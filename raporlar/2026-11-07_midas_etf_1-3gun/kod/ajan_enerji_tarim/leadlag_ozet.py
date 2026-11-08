"""İzleme listesi (kabul + yedek) için lead-lag özeti.
 (a) eşzamanlı sürücüler: leadlag_sweep.csv corr_1y / beta_1y (aynı gün; ÖNCÜ DEĞİL)
 (b) gecikmeli öncüler: sweep lag_t (kendi gecikmesi kontrollü, NW) + FDR + IS/OOS işaret + bp/sd vs maliyet;
     ek test: yetişme boşluğunun (beta60*r_L - r_T) KENDİ getirisine ek katkısı (fwd ~ own + gap).
 (c) gerçek zamanlı izlenecekler: ETF kapalıyken işleyen vadeli/endeks/döviz (tv_dogrulama.csv'de doğrulanmış kodlar).
Çalıştırma: python3 -I kod/ajan_enerji_tarim/leadlag_ozet.py"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import ortak as O, lib

pd.set_option("display.width", 250)
L = pd.read_csv(os.path.join(O.OUT, "leadlag_aile.csv"))
TVE = pd.read_csv(os.path.join(lib.ROOT, "sonuclar", "tv_etf.csv")).set_index("sym")["tv"].to_dict()
TVV = pd.read_csv(os.path.join(lib.ROOT, "sonuclar", "tv_dogrulama.csv"))
OK = set(TVV[TVV.durum.isin(["dogrulandi", "dogrulandi_kanonik"])].ticker)
LEADER_TV = {"VIX_dlog": "CBOE:VIX", "VIXTS_d": "CBOE:VIX3M", "OVX_dlog": "CBOE:OVX", "GVZ_dlog": "CBOE:GVZ", "VVIX_dlog": "CBOE:VVIX",
             "BTC_16ET": "COINBASE:BTCUSD", "ETH_16ET": "COINBASE:ETHUSD", "DGS10_d": "TVC:US10Y", "DGS2_d": "TVC:US02Y", "DGS30_d": "TVC:US30Y",
             "DFII10_d": "FRED:DFII10", "T10YIE_d": "FRED:T10YIE"}
def tv(x):
    c = TVE.get(x) or LEADER_TV.get(x)
    return c

TARGETS = ["USO", "XLE", "KOLD", "BNO", "UCO", "SCO", "UNG", "BOIL", "XOP", "DRIP", "PDBC"]
RT = {  # gerçek zamanlı izlenecekler (ETF kapalıyken işler); hepsi tv_dogrulama.csv'de doğrulanmış
    "ham_petrol": [("WTI ham petrol vadelisi (ön ay)", "NYMEX:CL1!", "dayanak; Globex ~23 saat, açılış boşluğunu önceden gösterir"),
                   ("WTI 2. ay", "NYMEX:CL2!", "CL2!/CL1!-1 kontango göstergesi"),
                   ("Brent vadelisi (ön ay)", "ICEEUR:BRN1!", "Brent; Londra saatlerinde fiyat keşfi"),
                   ("Dolar endeksi", "TVC:DXY", "dolar şoku emtiaya ters")],
    "dogalgaz": [("Henry Hub doğalgaz vadelisi (ön ay)", "NYMEX:NG1!", "dayanak; Globex'te gece işler"),
                 ("Doğalgaz 2. ay", "NYMEX:NG2!", "NG2!/NG1!-1 kontango göstergesi"),
                 ("Hollanda TTF gaz vadelisi", "ICEENDEX:TFM1!", "Avrupa gazı; ABD açılışından önce işler")],
    "enerji_hisse": [("S&P 500 e-mini", "CME_MINI:ES1!", "genel hisse yönü"),
                     ("WTI vadelisi", "NYMEX:CL1!", "petrol hareketi aynı gün yansır"),
                     ("Doğalgaz vadelisi", "NYMEX:NG1!", "gaz üreticileri")],
    "genis_emtia": [("WTI vadelisi", "NYMEX:CL1!", "en büyük bileşen enerji"), ("Brent", "ICEEUR:BRN1!", "petrol"),
                    ("Altın", "COMEX:GC1!", "metal"), ("Bakır", "COMEX:HG1!", "metal"), ("Mısır", "CBOT:ZC1!", "tarım")],
}
GROUP = {"USO": "ham_petrol", "BNO": "ham_petrol", "UCO": "ham_petrol", "SCO": "ham_petrol", "UNG": "dogalgaz", "BOIL": "dogalgaz",
         "KOLD": "dogalgaz", "XLE": "enerji_hisse", "XOP": "enerji_hisse", "DRIP": "enerji_hisse", "PDBC": "genis_emtia"}
for g, items in RT.items():
    for _, code, _ in items:
        assert code in OK, code

# ---- ek test: yetişme boşluğunun kendi getirisine ek katkısı ----
idx = lib.load("SPY").index
Rr = {}
def lr(s):
    if s not in Rr: Rr[s] = O.logret(s).reindex(idx)
    return Rr[s]
extra = []
CATCH_L = {"USO": ["BNO", "XLE", "USL"], "BNO": ["USO", "XLE"], "UCO": ["USO", "BNO"], "SCO": ["USO", "BNO"], "UNG": ["UNL", "BOIL"],
           "BOIL": ["UNG", "UNL"], "KOLD": ["UNG", "UNL"], "XLE": ["USO", "SPY", "XOP"], "XOP": ["USO", "XLE", "UNG"], "DRIP": ["USO", "XLE"],
           "PDBC": ["USO", "BNO", "DBA"]}
for T, Ls in CATCH_L.items():
    for Ld in Ls:
        y0, x = lr(T), lr(Ld)
        beta = y0.rolling(60).cov(x) / x.rolling(60).var()
        gap = beta * x - y0
        for h in (1, 3):
            d = pd.DataFrame({"y": O.fwd(y0, h), "own": y0, "gap": gap}).dropna()
            rec = {"hedef": T, "oncu": Ld, "h": h, "n": len(d)}
            for nm, m in (("tum", np.ones(len(d), bool)), ("is", d.index <= lib.IS_END), ("oos", d.index > lib.IS_END)):
                dd = d[m]
                b, t = O.nw_t(dd["y"].values, np.column_stack([np.ones(len(dd)), dd["own"].values, dd["gap"].values]), h)
                rec[f"t_gap_{nm}"] = t[2]; rec[f"t_own_{nm}"] = t[1]
                if nm == "tum": rec["bp_per_sd_gap"] = b[2] * dd["gap"].std() * 1e4
            rec["maliyet_bp"] = O.cost(T)
            extra.append(rec)
            O.REG.append({"hyp": "LL_yetisme_ek", "sym": T, "desc": f"fwd{h} ~ own + gap({Ld})", "mode": "-", "h": h, "kind": "regresyon", "sign": 0,
                          "n": rec["n"], "t": rec["t_gap_tum"], "p1": 2 * O.p_one(abs(rec["t_gap_tum"]), rec["n"], +1)})
E = pd.DataFrame(extra)
E.to_csv(os.path.join(O.OUT, "leadlag_yetisme_ek_katki.csv"), index=False)
O.save_registry("leadlag_ozet")

out = {}
rows = []
for T in TARGETS:
    x = L[L.target == T].copy()
    x["abs_corr"] = x["corr_1y"].abs()
    drv = x.sort_values("abs_corr", ascending=False).head(4)
    suruculer = [{"ad": r.leader, "tv": tv(r.leader), "corr_1y": round(float(r.corr_1y), 3), "beta_1y": round(float(r.beta_1y), 3)} for r in drv.itertuples()]
    # gecikmeli öncü ölçütü
    cand = []
    for h in (1, 3):
        y = x.assign(t=x[f"lag_t_h{h}"], ti=x[f"lag_t_h{h}_is"], to=x[f"lag_t_h{h}_oos"], bp=x[f"lag_bp_per_sd_h{h}"], f=x[f"fdr10_lag_t_h{h}"])
        y = y.assign(h=h)
        cand.append(y[["leader", "h", "t", "ti", "to", "bp", "f"]])
    C = pd.concat(cand); C["abs_t"] = C["t"].abs()
    C["ayni_isaret"] = np.sign(C["ti"]) == np.sign(C["to"])
    C["ekonomik"] = C["bp"].abs() > O.cost(T)
    C["gecerli"] = C["f"] & C["ayni_isaret"] & C["ekonomik"]
    best = C.sort_values("abs_t", ascending=False).head(3)
    e = E[E.hedef == T].sort_values("t_gap_tum", key=lambda s: s.abs(), ascending=False).head(1)
    rows.append({"hedef": T, "gecerli_oncu_sayisi": int(C["gecerli"].sum()), "fdr_gecen": int(C["f"].sum()),
                 "en_guclu": "; ".join(f"{r.leader} h{r.h} t={r.t:.2f} (IS {r.ti:.2f}/OOS {r.to:.2f}, {r.bp:.1f} bp/sd, FDR={'E' if r.f else 'H'})" for r in best.itertuples()),
                 "yetisme_ek": "; ".join(f"gap({r.oncu}) h{r.h} t={r.t_gap_tum:.2f} (IS {r.t_gap_is:.2f}/OOS {r.t_gap_oos:.2f}, {r.bp_per_sd_gap:.1f} bp/sd)" for r in e.itertuples()),
                 "maliyet_bp": O.cost(T)})
    out[T] = {"suruculer": suruculer, "gercek_zamanli": [{"ad": a, "tv": c, "neden": n} for a, c, n in RT[GROUP[T]]],
              "en_guclu_gecikmeli": rows[-1]["en_guclu"], "yetisme_ek": rows[-1]["yetisme_ek"], "gecerli": rows[-1]["gecerli_oncu_sayisi"]}
S = pd.DataFrame(rows)
S.to_csv(os.path.join(O.OUT, "leadlag_ozet.csv"), index=False)
json.dump(out, open(os.path.join(O.OUT, "leadlag_ozet.json"), "w"), ensure_ascii=False, indent=1)
print(S.to_string(index=False))
print("\n== yetişme ek katkı (en büyük |t|)"); print(E.sort_values("t_gap_tum", key=lambda s: s.abs(), ascending=False).head(12).round(2).to_string(index=False))
for T in TARGETS:
    print(T, out[T]["suruculer"])
