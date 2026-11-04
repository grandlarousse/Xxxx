"""(a) Yabancı sektör emsali ayrışması -> hisse VİOP uzlaşma t -> t+h (h=1,2,3,5).
ÖN-KAYIT (sonuçlara bakmadan): sepetler ve hedef eşlemesi aşağıda. Her sepet 47 hisseye uygulanır (plasebo/özgüllük).
Sinyaller (t kapanışında bilinen):
  P_t  = emsal artığı (üye getirisi - beta x bölge endeksi, üyelerin eşit ağırlıklı ortalaması), geçmiş std ile ölçekli
  Ds_t = hisse artığı (VİOP ön vade uzlaşma getirisi - beta x F_XU030), geçmiş std ile ölçekli
  D_t  = b_sync x P_t - Ds_t  (hisse emsalin gerisinde kaldı mı?), geçmiş std ile ölçekli  -> pozitif = hisse geride = AL
Test 1: y_h ~ D_t (NW, lag h+1).  Test 2: y_h ~ P_t + Ds_t (P katsayısı: emsal bilgisinin hisse kendi dönüşünden bağımsız katkısı).
Kural: |D|>1 -> yön(D), h gün tut (örtüşen olay ortalaması, NW t).
Modlar: H = saatlik 15:00 UTC (2023-12+);  DF = günlük vekil, VİOP vadeli 2017+;  DS = günlük vekil, spot 2014+.
  Günlükte Asya (TSE/ASX/KRX) aynı gün t; Avrupa/ABD/emtia t-1 tam gün (shift 1); altın ayrıca VİOP XAUUSD uzlaşması (t, hizalı).
"""
import sys, numpy as np, pandas as pd
import klib as K, ll

REG = {"EU": "^STOXX", "US": "SPY", "JP": "^N225", "AU": "^AXJO", "KR": "^KS11", None: None}
# üye -> bölge (None = ham, ör. emtia)
B = {
 "AIR_EU":   {"LHA.DE": "EU", "AF.PA": "EU", "IAG.L": "EU", "EZJ.L": "EU", "WIZZ.L": "EU", "RYAAY": "US"},
 "AIR_US":   {"DAL": "US", "UAL": "US", "AAL": "US", "LUV": "US"},
 "AIRPORT":  {"ADP.PA": "EU", "FRA.DE": "EU", "AENA.MC": "EU"},
 "REF_US":   {"VLO": "US", "MPC": "US", "PSX": "US", "PBF": "US"},
 "REF_EU":   {"PKN.WA": "EU", "MOL.BD": "EU"},
 "BRENT":    {"BZ=F": None},
 "STEEL_EU": {"MT": "US", "TKA.DE": "EU", "SZG.DE": "EU", "VOE.VI": "EU", "APAM.AS": "EU"},
 "STEEL_US": {"NUE": "US", "STLD": "US", "CLF": "US", "CMC": "US"},
 "STEEL_JP": {"5401.T": "JP", "5411.T": "JP"},
 "MINERS_AU": {"BHP.AX": "AU", "FMG.AX": "AU"},
 "OCTG":     {"TS": "US", "TEN.MI": "EU", "OIH": "US"},
 "GOLD":     {"GC=F": None},
 "GOLDM":    {"GDX": "US", "NEM": "US", "AEM": "US", "B": "US", "KGC": "US"},
 "TKC":      {"TKC": None},   # TL'ye çevrilir (x USDTRY)
 "DEF_EU":   {"RHM.DE": "EU", "BA.L": "EU", "LDO.MI": "EU", "SAAB-B.ST": "EU"},
 "DEF_KR":   {"012450.KS": "KR", "064350.KS": "KR"},
 "BEER":     {"ABI.BR": "EU", "HEIA.AS": "EU", "CARL-B.CO": "EU", "BUD": "US", "TAP": "US"},
}
ASIA = {"STEEL_JP", "MINERS_AU", "DEF_KR"}
TARGET = {"AIR_EU": ["THYAO", "PGSUS", "TAVHL"], "AIR_US": ["THYAO", "PGSUS", "TAVHL"], "AIRPORT": ["TAVHL"],
          "REF_US": ["TUPRS"], "REF_EU": ["TUPRS"], "BRENT": ["TUPRS"],
          "STEEL_EU": ["EREGL", "KRDMD", "BRSAN"], "STEEL_US": ["EREGL", "KRDMD", "BRSAN"], "STEEL_JP": ["EREGL", "KRDMD", "BRSAN"],
          "MINERS_AU": ["EREGL", "KRDMD"], "OCTG": ["BRSAN"], "GOLD": ["TRALT", "TRMET"], "GOLDM": ["TRALT", "TRMET"],
          "GOLD_V": ["TRALT", "TRMET"], "TKC": ["TCELL"], "DEF_EU": ["ASELS"], "DEF_KR": ["ASELS"], "BEER": ["AEFES"]}
HS = [1, 2, 3, 5]

def daily_beta(m, reg):
    """Günlük yerel getirilerle (aynı saat dilimi) üye-bölge betası, BIST takvimine ffill."""
    if reg is None: return None
    a = ll.ret(m, on_bist_cal=False); b = ll.ret(reg, on_bist_cal=False)
    df = pd.concat([a.rename("a"), b.rename("b")], axis=1).dropna()
    bt = K.roll_beta(df["a"], df["b"], 250, 60)
    c = K.cal(); return bt.reindex(bt.index.union(c)).ffill().reindex(c)

def member_ret(m, mode):
    if mode == "H":
        r = K.r_snap(m)
        if m == "TKC": r = r + K.r_snap("TRY=X")
        return r
    r = ll.ret(m)
    if m == "TKC": r = r + ll.ret("TRY=X")
    return r

def peer_signal(bk, mode):
    """Ham emsal artığı (ölçeksiz), BIST takviminde. Günlük modda Asya aynı gün, diğerleri shift(1)."""
    rs = []
    for m, rg in B[bk].items():
        try:
            r = member_ret(m, mode)
            if rg is not None:
                rr = member_ret(REG[rg], mode); bt = daily_beta(m, REG[rg])
                res = r - bt.reindex(r.index) * rr.reindex(r.index)
            else:
                res = r
            rs.append(res.rename(m))
        except Exception as e:
            print("  eksik", bk, m, e)
    P = pd.concat(rs, axis=1).mean(axis=1, skipna=True)
    if mode != "H" and bk not in ASIA: P = P.shift(1)
    return P

def run(mode):
    F = K.fut_panel(); Sp = K.spot_panel()
    if mode in ("H", "DF"):
        R = F; mk = F["XU030"]; start = "2023-12-05" if mode == "H" else "2017-03-06"; split = "2025-05-01" if mode == "H" else "2022-01-01"
    else:
        R = Sp; mk = Sp["XU100"]; start = "2014-01-01"; split = "2021-01-01"
    R = R[R.index >= "2012-01-01"]
    betaS = K.roll_beta(R[K.STOCKS], mk, 250, 60)
    resid = R[K.STOCKS] - betaS.mul(mk, axis=0)
    w = 120 if mode == "H" else 250; mp = 40 if mode == "H" else 60
    Ds = K.sdscale(resid, w, mp)
    sig = {}
    for bk in B:
        P = peer_signal(bk, mode)
        sig[bk] = P
    if mode == "DF":
        sig["GOLD_V"] = F["XAUUSD"]  # VİOP altın uzlaşması (BIST kapanışına hizalı, aynı gün)
    rows = []; idx = R.index[R.index >= start]
    Y = {h: K.fwd(R[K.STOCKS], h) for h in HS}
    mkf = {h: K.fwd(mk, h) for h in HS}
    for bk, P0 in sig.items():
        P0 = P0.reindex(R.index)
        Pz = K.sdscale(P0, w, mp)
        lagged = (mode != "H") and (bk not in ASIA) and bk != "GOLD_V"
        for s in K.STOCKS:
            sr = resid[s]
            sw = (sr + sr.shift(1)) if lagged else sr       # hissenin emsal bilgisine tepki penceresi
            b_sync = K.roll_beta(sw, P0, w, mp)
            D = K.sdscale(b_sync * P0 - sw, w, mp)
            dsz = Ds[s]; dsz1 = Ds[s].shift(1)
            for h in HS:
                for tg in ("raw", "hedged"):
                    y = Y[h][s] if tg == "raw" else (Y[h][s] - betaS[s] * mkf[h])
                    y = y[y.index >= start]
                    r1 = K.reg(y, D, h + 1)
                    X2 = pd.concat([Pz.rename("P"), dsz.rename("Ds")] + ([dsz1.rename("Ds1")] if lagged else []), axis=1)
                    r2 = K.reg(y, X2, h + 1)
                    act = (D.abs() > 1)
                    ev = (np.sign(D) * y).where(act).dropna()
                    m_, t_, n_ = K.mean_nw(ev, h)
                    isy = y[y.index < split]; oos = y[y.index >= split]
                    r1i = K.reg(isy, D, h + 1, 40); r1o = K.reg(oos, D, h + 1, 40)
                    r2i = K.reg(isy, X2, h + 1, 40); r2o = K.reg(oos, X2, h + 1, 40)
                    evi = ev[ev.index < split]; evo = ev[ev.index >= split]
                    rows.append(dict(mode=mode, basket=bk, stock=s, h=h, tgt=tg, target_pair=s in TARGET.get(bk, []),
                                     n=r1["n"], bD=r1["b"] * 1e4, tD=r1["t"], tD_IS=r1i["t"], tD_OOS=r1o["t"],
                                     bP=r2["b"] * 1e4, tP=r2["t"], tP_IS=r2i["t"], tP_OOS=r2o["t"], tDs=r2.get("t2", np.nan),
                                     ev_n=n_, ev_bps=m_ * 1e4, ev_t=t_, ev_IS_bps=evi.mean() * 1e4 if len(evi) > 10 else np.nan,
                                     ev_OOS_bps=evo.mean() * 1e4 if len(evo) > 10 else np.nan))
        print(mode, bk, "bitti", flush=True)
    out = pd.DataFrame(rows)
    out.to_csv(K.RES + f"/a_peers_{mode}.csv", index=False)
    pd.to_pickle({k: v for k, v in sig.items()}, K.RES + f"/a_sig_{mode}.pkl")
    return out

if __name__ == "__main__":
    for m in sys.argv[1:]: run(m)
