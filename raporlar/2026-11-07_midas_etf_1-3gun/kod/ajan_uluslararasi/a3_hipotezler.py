"""Görev 3: aileye özel hipotezler (hipotezler.csv UL01-UL06 + yönlendirme). Kurallar ÖNCEDEN sabitlendi
(literatür varsayılanı / yuvarlak eşik); parametre taraması YOK. Her hipotez x mod (C0/O1/C1) x h (1,2,3) bir testtir.
Havuz istatistiği: işlemler sinyal tarihine göre kümelenir (ortak faktör), Newey-West t.
Çalıştır: python3 -I kod/ajan_uluslararasi/a3_hipotezler.py
Çıktı: sonuclar/aile_uluslararasi/hipotez_havuz.csv, hipotez_etf.csv"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import ortak, lib
from strategies import month_nth_from_end

D = {}
def L(s):
    if s not in D: D[s] = lib.load(s)
    return D[s]

def ret(s): return L(s)["c"].pct_change()

def on(s, x):
    """x serisini s'nin tarih ekseninde hizala (t'de bilinen)."""
    return x.reindex(L(s).index)

spy = L("SPY")
r_spy = spy["c"].pct_change()
z_spy = lib.zret(spy["c"], 1, 60)
z_qqq = lib.zret(L("QQQ")["c"], 1, 60)
z_kweb = lib.zret(L("KWEB")["c"], 1, 60)
r_kweb = L("KWEB")["c"].pct_change()
z_uso = lib.zret(L("USO")["c"], 1, 60)

def resid_z(s, lead_r, n=60):
    """Kalıntı r_T - beta60*r_L, z skoru (std t-1'e kadar)."""
    r = ret(s); x = on(s, lead_r)
    b = r.rolling(n).cov(x) / x.rolling(n).var()
    e = r - b * x
    return e / e.rolling(n).std().shift(1), b

fomc = pd.read_csv(os.path.join(ortak.ROOT, "data", "events", "fomc.csv"), parse_dates=["date"])
fomc_d = set(fomc[fomc["event"] == "FOMC_karar"]["date"])

def pre_event(idx, days):
    """t'den sonraki işlem günü olay günüyse True (olay takvimi önceden bilinir)."""
    nxt = pd.Series(list(idx[1:]) + [pd.NaT], index=idx)
    return nxt.isin(days)

IND = ortak.independent(10)
ASYA_UL03 = ["EWJ", "EWY", "EWT", "FXI", "EWA", "EWH"]
H = {}
# UL01 ülke IBS<0.20
H["UL01_ulke_IBS"] = (["EWJ", "EWI", "FXI", "EWT", "EWA", "EZA", "EIS", "INDA", "EWZ", "EWU"],
                      lambda s: lib.ibs(L(s)) < 0.20)
# UL02 kesitsel en düşük IBS 3 ETF
UL02 = ["EWJ","EWG","EWU","EWQ","EWI","EWP","EWC","EWA","EWH","EWS","EWT","EWY","EWZ","EWW","FXI","INDA","EZA"]
_ibs = pd.DataFrame({s: lib.ibs(L(s)) for s in UL02}).reindex(spy.index)
_rank = _ibs.rank(axis=1, method="first")
H["UL02_kesitsel_IBS_min3"] = (UL02, lambda s: on(s, _rank[s] <= 3))
# UL03 ABD aşırı tepki: SPY <= -%1.5 ve ETF <= SPY
H["UL03_SPY_dusus_Asya"] = (ASYA_UL03, lambda s: (on(s, r_spy) <= -0.015) & (ret(s) <= on(s, r_spy)))
# UL04 (vekil) eşzamansız kalıntı dönüşü: (r_T - b60*r_SPY) z <= -2  -> long
H["UL04v_kalinti_SPY_z_le_m2"] = (IND, lambda s: resid_z(s, r_spy)[0] <= -2)
H["UL04v_kalinti_SPY_z_le_m2_asya"] = ([s for s in IND if ortak.REGION.get(s) == "asya"], lambda s: resid_z(s, r_spy)[0] <= -2)
H["UL04v_kalinti_SPY_z_le_m2_avrupa"] = ([s for s in IND if ortak.REGION.get(s) == "avrupa_ortadogu_afrika"], lambda s: resid_z(s, r_spy)[0] <= -2)
# karşılaştırma: yalnız kendi getirisi (öncü yok) z <= -2
H["UL04k_kendi_z_le_m2"] = (IND, lambda s: lib.zret(L(s)["c"], 1, 60) <= -2)
# UL05 ülke ay dönümü: T_son-1 kapanışı -> yeni ayın 2. işlem günü kapanışı (h=3 sabit; modlar bilgi amaçlı)
H["UL05_ay_donumu"] = (["EWJ","EWG","EWU","EWA","EWC","EWZ","FXI","EFA","EEM"], lambda s: pd.Series(month_nth_from_end(L(s).index, 2), index=L(s).index))
# UL06 FOMC öncesi: D-1 kapanışı -> D kapanışı
H["UL06_FOMC_oncesi"] = (["EFA", "EEM", "EWJ", "EWG", "VGK"], lambda s: pre_event(L(s).index, fomc_d))
# Y1 Asya <- SPY gecikmesi: SPY z1 <= -2 -> Asya ETF long
H["Y1_SPY_z_le_m2_Asya"] = (["EWJ", "EWY", "EWT", "FXI", "INDA", "KWEB"], lambda s: on(s, z_spy) <= -2)
H["Y1b_QQQ_z_le_m2_Asya_tekno"] = (["EWT", "EWY", "CQQQ", "KWEB"], lambda s: on(s, z_qqq) <= -2)
H["Y1c_SPY_z_le_m2_DXJ"] = (["DXJ"], lambda s: on(s, z_spy) <= -2)
# Y2 KWEB -> Asya/EM (lead-lag taramasından; KEŞİFSEL): KWEB z1 >= +1 -> hedef long
Y2 = ["EEM", "FXI", "EWH", "EWY", "EWT", "ASHR", "CQQQ", "EWA", "EWS", "INDA"]
H["Y2_KWEB_z_ge_1"] = (Y2, lambda s: on(s, z_kweb) >= 1)
H["Y2b_KWEB_z_ge_1_ve_geride"] = (Y2, lambda s: (on(s, z_kweb) >= 1) & (resid_z(s, r_kweb)[0] < 0))
# Y3 EWZ <- USO: USO z1 >= +1.5 -> EWZ long
H["Y3_USO_z_ge_15_EWZ"] = (["EWZ", "ILF"], lambda s: on(s, z_uso) >= 1.5)

def run():
    rows, erows = [], []
    for hn, (targets, fn) in H.items():
        sigs = {}
        for s in targets:
            sg = fn(s).reindex(L(s).index).fillna(False).astype(bool)
            sg.iloc[:200] = False
            sigs[s] = sg
        for mode in ("C0", "O1", "C1"):
            for h in (1, 2, 3):
                trs = []
                for s in targets:
                    df = L(s)
                    st, tr = ortak.full_stats(df, sigs[s], h, mode, label=hn, sym=s)
                    st.update({"hyp": hn, "mode": mode, "h": h}); erows.append(st)
                    if len(tr): tr["sym"] = s; trs.append(tr)
                trs = pd.concat(trs, ignore_index=True) if trs else pd.DataFrame()
                r = ortak.pooled(trs, h); r.update({"hyp": hn, "mode": mode, "h": h, "targets": ";".join(targets)})
                # maliyet duyarlılığı (havuz, işlem başı brüt - ETF maliyeti)
                if len(trs):
                    cmap = {s: lib.cost_bp(L(s)) for s in targets}
                    sp = {s: lib.spread_bp_tier(L(s)) for s in targets}
                    g = trs.groupby("sig_date").apply(lambda x: pd.Series({"g": x["gross"].mean(), "sp": np.mean([sp[v] for v in x["sym"]])}))
                    r["net_1000_bp"] = (g["g"] * 1e4 - (30 + g["sp"])).mean()
                    r["net_10000_bp"] = (g["g"] * 1e4 - (3 + g["sp"])).mean()
                rows.append(r)
    P = pd.DataFrame(rows); E = pd.DataFrame(erows)
    from scipy import stats as sst
    P["p"] = sst.norm.sf(P["t_nw"])          # tek yönlü (H1: net > 0)
    P["fdr10_bu_dosya"] = lib.bh_fdr(P["p"].values, 0.10) & (P["mean_net_bp"] > 0)
    gm = P.pivot_table(index=["hyp", "h"], columns="mode", values="mean_gross_bp")
    P = P.merge(gm.add_prefix("gross_").reset_index(), on=["hyp", "h"], how="left")
    P.to_csv(os.path.join(ortak.OUT, "hipotez_havuz.csv"), index=False)
    E.to_csv(os.path.join(ortak.OUT, "hipotez_etf.csv"), index=False)
    pd.set_option("display.width", 280); pd.set_option("display.max_rows", 400)
    cols = ["hyp", "mode", "h", "k_etf", "n_dates", "n_trades", "mean_gross_bp", "mean_net_bp", "t_nw", "is_net_bp", "is_t", "oos_net_bp",
            "oos_t", "years_pos_frac", "pf", "maxdd", "net_1000_bp", "net_10000_bp", "fdr10_bu_dosya"]
    print("hipotez testi (havuz) sayısı:", len(P), " FDR geçen:", int(P["fdr10_bu_dosya"].sum()))
    print(P[cols].round(2).to_string(index=False))
    return P, E

if __name__ == "__main__":
    run()
