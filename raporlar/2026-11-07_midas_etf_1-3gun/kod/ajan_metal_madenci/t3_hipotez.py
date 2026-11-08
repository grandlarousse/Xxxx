"""Görev 3: aileye özel hipotezler (önceden belirlenmiş kurallar; parametre taraması YOK).
H01 ay sonu (turn-of-month, McConnell-Xu penceresi -1..+3)   H02 tatil öncesi
H03 IBS<0.1 & düşüş (madenciler)                             H04 VIX backwardation dönüşü
H05 (MM01) gece vs gün içi -> ayrı betik t3b_gece.py         H06 (MM02) madenci-metal artık yetişme (GDX/GDXJ/RING<-GLD, SIL/SILJ<-SLV, COPX<-CPER)
H07 altın/gümüş oranı z20 +-2                                H08 GVZ sıçrama / gerilme
H09 (MM03) reel faiz + dolar; DFII10 günlük düşüş; UUP düşüşü H10 (MM04) FOMC sonrası / öncesi
H11 (MM05) GLD RSI2 (genel kütüphaneden okunur)              H13 bakır/baz metal <- Çin (KWEB/FXI)  H14 URA <- SPY büyük düşüş
Çalıştır: python3 -I kod/ajan_metal_madenci/t3_hipotez.py
Çıktı: sonuclar/aile_metal_madenci/hipotez_etf.csv, hipotez_havuz.csv, hipotez_yillik.csv, testler_t3.csv"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import mm, lib, strategies as S

REG = mm.Registry("t3")
ETF_ROWS, POOL_ROWS, YEAR_ROWS = [], [], []
DF = {}
def D(s):
    if s not in DF: DF[s] = mm.load(s)
    return DF[s]

def run(hid, label, sigfun, syms, hs=(1, 2, 3), md=("C0", "O1", "C1"), pools=None, warm=200, exitfun=None, yearly_for=None):
    """Her ETF x mod x h için tam istatistik + kayıt; pools: {ad: [syms]} havuz testleri."""
    for s in syms:
        df = D(s); sig = sigfun(df, s)
        for m in md:
            for h in hs:
                ex = exitfun(df) if exitfun else None
                st, tr = mm.full(s, sig, h, m, df=df, exit_sig=ex, warm=warm)
                if st.get("n", 0) == 0: continue
                st.update({"hid": hid, "kural": label, "mode": m, "h": h})
                ETF_ROWS.append(st)
                REG.add(f"{hid}_{label}", s, m, h, st["n"], st["t"], st["mean_net_bp"])
                if yearly_for and (s, m, h) in yearly_for:
                    y = mm.yearly(tr); y["hid"] = hid; y["kural"] = label; y["sym"] = s; y["mode"] = m; y["h"] = h
                    YEAR_ROWS.append(y.reset_index().rename(columns={"sig_date": "yil"}))
    for pn, ps in (pools or {}).items():
        for m in md:
            for h in hs:
                r, E = mm.pooled(ps, sigfun, h, m, warm=warm, dfs={s: D(s) for s in ps})
                if r.get("n_ev", 0) == 0: continue
                r.update({"hid": hid, "kural": label, "havuz": pn, "mode": m, "h": h})
                POOL_ROWS.append(r)
                REG.add(f"{hid}_{label}_havuz", pn, m, h, r["n_ev"], r["t_nw"], r["net_bp"])
                if yearly_for and (pn, m, h) in yearly_for:
                    y = E.groupby(E.index.year).agg(n=("net", "size"), net_bp=("net", "mean"), toplam_net_pct=("net", "sum"))
                    y["net_bp"] *= 1e4; y["toplam_net_pct"] *= 100
                    y["hid"] = hid; y["kural"] = label; y["sym"] = pn; y["mode"] = m; y["h"] = h
                    YEAR_ROWS.append(y.reset_index().rename(columns={"sig_date": "yil"}))

METALS = ["GLD", "SLV", "PPLT", "PALL", "CPER"]
POOLS_ALL = {"REP12": mm.REP12, "MADENCI5": mm.MINERS, "METAL5": METALS}

def main():
    ctx = {"VIX": lib.vol_index("VIX"), "VIX3M": lib.vol_index("VIX3M")}
    # ---------------- H01 ay sonu (son işlem günü kapanışı -> yeni ayın h. günü)
    f = lambda df, s: S.month_last_day(df.index)
    run("H01", "ay_sonu", f, mm.REP17 + ["NUGT", "JNUG", "AGQ", "UGL", "SPY"], pools=POOLS_ALL,
        yearly_for={("GDX", "C0", 3), ("REP12", "C0", 3), ("MADENCI5", "C0", 3), ("GLD", "C0", 3), ("METAL5", "C0", 3)})
    # ---------------- H02 tatil öncesi (klasik: 1 gün)
    f = lambda df, s: S.pre_holiday(df.index)
    run("H02", "tatil_oncesi", f, mm.REP17 + ["SPY"], pools=POOLS_ALL, yearly_for={("REP12", "C0", 1), ("MADENCI5", "C0", 1)})
    # ---------------- H03 IBS<0.1 & düşüş
    f = lambda df, s: (lib.ibs(df) < 0.1) & (df["c"] < df["c"].shift(1))
    run("H03", "ibs01_dusus", f, mm.REP17 + ["NUGT", "JNUG"], pools=POOLS_ALL,
        yearly_for={("GDX", "C0", 3), ("GDXJ", "C0", 3), ("MADENCI5", "C0", 3), ("MADENCI5", "C0", 1)})
    # ---------------- H04 VIX backwardation dönüşü (VIX/VIX3M 1'in altına iner)
    f = lambda df, s: S.LIB["VX_backw_donus"](df, ctx)
    run("H04", "vix_backw_donus", f, mm.REP17, pools=POOLS_ALL, yearly_for={("MADENCI5", "C1", 2), ("REP12", "C0", 2)})
    # ---------------- H06 (MM02) artık yetişme: res=r_T - beta60*r_L <= -1.5*sd60(res) [sd t-1'e kadar]
    def resid_sig(lead, k=1.5):
        def f(df, s):
            L = D(lead)["c"].reindex(df.index)
            rt = np.log(df["c"]).diff(); rl = np.log(L).diff()
            b = rt.rolling(60).cov(rl) / rl.rolling(60).var()
            res = rt - b * rl
            return res <= -k * res.rolling(60).std().shift(1)
        return f
    for tgt, lead in [("GDX", "GLD"), ("GDXJ", "GLD"), ("RING", "GLD"), ("SIL", "SLV"), ("SILJ", "SLV"), ("COPX", "CPER")]:
        run("H06", f"artik_{tgt}_{lead}", resid_sig(lead), [tgt], hs=(1, 2, 3))
    # kontrol: kendi düşüşü (z1<-1.5) aynı ETF'lerde (yetişme mi, kendi dönüşü mü?)
    f = lambda df, s: lib.zret(df["c"], 1) < -1.5
    run("H06k", "kendi_z1_lt_m1.5", f, ["GDX", "GDXJ", "RING", "SIL", "SILJ", "COPX"], hs=(1, 2, 3))
    # havuz: madenciler artık sinyali
    def pool_resid(df, s):
        lead = {"GDX": "GLD", "GDXJ": "GLD", "RING": "GLD", "SIL": "SLV", "SILJ": "SLV"}[s]
        return resid_sig(lead)(df, s)
    run("H06", "artik_havuz", pool_resid, [], pools={"MADENCI5": mm.MINERS})
    # ---------------- H07 altın/gümüş oranı z20
    def ratio_z(df_unused=None):
        x = np.log(D("GLD")["c"] / D("SLV")["c"].reindex(D("GLD").index))
        return (x - x.rolling(20).mean()) / x.rolling(20).std()
    z = ratio_z()
    run("H07", "oran_z20_gt2_SLVal", lambda df, s: (z > 2).reindex(df.index), ["SLV", "SIL"])
    run("H07", "oran_z20_lt_m2_GLDal", lambda df, s: (z < -2).reindex(df.index), ["GLD", "GDX"])
    # ---------------- H08 GVZ
    gvz = lib.vol_index("GVZ")
    run("H08", "gvz_sicrama15", lambda df, s: (gvz.pct_change() > 0.15).reindex(df.index), ["GLD", "SLV", "GDX"], pools={"G3": ["GLD", "SLV", "GDX"]})
    run("H08", "gvz_gerilme", lambda df, s: (gvz > 1.10 * gvz.rolling(10).mean()).reindex(df.index), ["GLD", "SLV", "GDX"], pools={"G3": ["GLD", "SLV", "GDX"]})
    # ---------------- H09 (MM03) reel faiz + dolar
    ry = lib.fred("DFII10")
    uup = D("UUP")["c"]
    def mm03(df, s):
        r = ry.reindex(df.index).ffill()
        u = uup.reindex(df.index)
        return ((r.shift(1) - r.shift(4)) <= -0.10) & ((u / u.shift(3) - 1) <= -0.005)
    run("H09", "MM03_reelfaiz_dolar", mm03, ["GLD", "SLV", "GDX"], pools={"G3": ["GLD", "SLV", "GDX"]})
    # DFII10 t günü değişimi <= -5 bp (Hazine verisi kapanıştan sonra yayımlanır -> yalnız O1/C1)
    def dfii_drop(df, s):
        r = ry.reindex(df.index).ffill(); return (r - r.shift(1)) <= -0.05
    run("H09", "DFII10_d_le_m5bp", dfii_drop, ["GLD", "SLV", "GDX"], md=("O1", "C1"), pools={"G3": ["GLD", "SLV", "GDX"]})
    def dfii_up(df, s):
        r = ry.reindex(df.index).ffill(); return (r - r.shift(1)) >= 0.05
    run("H09", "DFII10_d_ge_5bp", dfii_up, ["GLD", "SLV", "GDX"], md=("O1", "C1"), pools={"G3": ["GLD", "SLV", "GDX"]})
    # UUP günlük düşüşü z1<-1.5 (t kapanışında bilinir)
    zu = lib.zret(uup, 1)
    run("H09", "UUP_z1_lt_m1.5", lambda df, s: (zu < -1.5).reindex(df.index), ["GLD", "SLV", "GDX"], pools={"G3": ["GLD", "SLV", "GDX"]})
    # ---------------- H10 (MM04) FOMC
    fomc = mm.events("fomc", "FOMC_karar")
    def fomc_post(df, s): return mm.date_sig(df, fomc)
    def fomc_pre3(df, s):
        idx = df.index; pos = idx.get_indexer(fomc[fomc.isin(idx)]) - 3
        return mm.date_sig(df, idx[pos[pos >= 0]])
    def fomc_pre1(df, s):
        idx = df.index; pos = idx.get_indexer(fomc[fomc.isin(idx)]) - 1
        return mm.date_sig(df, idx[pos[pos >= 0]])
    run("H10", "FOMC_sonrasi", fomc_post, ["GLD", "SLV", "GDX"], pools={"G3": ["GLD", "SLV", "GDX"]}, warm=0)
    run("H10", "FOMC_oncesi_D-3_D", fomc_pre3, ["GLD", "SLV", "GDX"], hs=(3,), md=("C0",), pools={"G3": ["GLD", "SLV", "GDX"]}, warm=0)
    run("H10", "FOMC_oncesi_D-1_D", fomc_pre1, ["GLD", "SLV", "GDX"], hs=(1,), md=("C0",), pools={"G3": ["GLD", "SLV", "GDX"]}, warm=0)
    # ---------------- H13 bakır / baz metal <- Çin (KWEB 1g z>1: DBB-KWEB FDR bulgusu; CPER<-FXI)
    zk = lib.zret(D("KWEB")["c"], 1); zf = lib.zret(D("FXI")["c"], 1)
    run("H13", "KWEB_z1_gt1", lambda df, s: (zk > 1).reindex(df.index), ["DBB", "CPER", "COPX"])
    run("H13", "FXI_z1_gt1", lambda df, s: (zf > 1).reindex(df.index), ["CPER", "DBB", "COPX"])
    # ---------------- H14 URA <- SPY büyük düşüş (leadlag'de negatif katsayı)
    zs = lib.zret(D("SPY")["c"], 1)
    run("H14", "SPY_z1_lt_m1.5", lambda df, s: (zs < -1.5).reindex(df.index), ["URA", "URNM"])

    E = pd.DataFrame(ETF_ROWS); P = pd.DataFrame(POOL_ROWS)
    E.to_csv(os.path.join(mm.OUTD, "hipotez_etf.csv"), index=False)
    P.to_csv(os.path.join(mm.OUTD, "hipotez_havuz.csv"), index=False)
    if YEAR_ROWS: pd.concat(YEAR_ROWS).to_csv(os.path.join(mm.OUTD, "hipotez_yillik.csv"), index=False)
    R = REG.save()
    print("t3 test sayısı:", len(R))

if __name__ == "__main__":
    main()
