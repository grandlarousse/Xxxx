"""s3: Plasebolar. (a) bayat sinyal lag 1/2/3 (b) dairesel kaydirma null'u (1000) (c) rastgele isaret (1000)
(d) baska sepetler: ayrik celik sepeti, defansif Japon/Kore, dongusel otomotiv/elektrik (e) ayni sinyal 47 VIOP hissesi + endeksler."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vb, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
rng = np.random.default_rng(7)
cA, _ = vb.comp(vb.JP_AU)
S3 = ["EREGL.IS", "KRDMD.IS", "BRSAN.IS"]
TG = {s: vb.bist(s) for s in S3}
rows = []
for lag in (0, 1, 2, 3, -1):
    c = cA.shift(lag)
    for s, b in TG.items():
        r = vb.isoos(vb.bt(c, b.intra)); cr = vb.corr_t(c, b.intra)
        r.update(test=f"lag{lag}" + (" (gelecek: BIST->Asya ters)" if lag < 0 else ""), stock=s, corr=cr[0], corr_t=cr[1]); rows.append(r)
BASK = {"ayrik_celik(POSCO,HyundaiSteel,RIO,CIA,MIN)": ["005490.KS", "004020.KS", "RIO.AX", "CIA.AX", "MIN.AX"],
        "defansif(Asahi,Kirin,NTT,TEPCO,KEPCO)": ["2502.T", "2503.T", "9432.T", "9501.T", "015760.KS"],
        "banka(MUFG,SMFG,Mizuho,Shinhan,KB)": ["8306.T", "8316.T", "8411.T", "055550.KS", "105560.KS"],
        "dongusel_oto/elektrik(Toyota,Honda,Hyundai,Hitachi,MitsuElec)": ["7203.T", "7267.T", "005380.KS", "6501.T", "6503.T"],
        "agir_sanayi(MHI,Kawasaki,IHI)": ["7011.T", "7012.T", "7013.T"],
        "genis_endeks(N225,KS11,AXJO)": ["^N225", "^KS11", "^AXJO"],
        "yalniz_JP_celik(5411,5401)": ["5411.T", "5401.T"], "yalniz_AU_cevher(FMG,BHP)": ["FMG.AX", "BHP.AX"], "Komatsu": ["6301.T"], "FMG": ["FMG.AX"]}
for nm, syms in BASK.items():
    c, _ = vb.comp(syms)
    for s, b in TG.items():
        r = vb.isoos(vb.bt(c, b.intra)); cr = vb.corr_t(c, b.intra)
        cri = vb.corr_t(c[c.index < vb.SPLIT], b.intra); cro = vb.corr_t(c[c.index >= vb.SPLIT], b.intra)
        r.update(test="sepet:" + nm, stock=s, corr=cr[0], corr_t=cr[1], corr_IS_t=cri[1], corr_OOS_t=cro[1]); rows.append(r)
P = pd.DataFrame(rows); P.to_csv(os.path.join(vb.OUT, "res_s3_placebo.csv"), index=False)
pd.set_option("display.width", 250)
print(P[["test", "stock", "IS_bps", "IS_t", "OOS_n", "OOS_bps", "OOS_t", "corr", "corr_t", "corr_IS_t", "corr_OOS_t"]].round(3).to_string())
# (b) dairesel kaydirma ve (c) rastgele isaret
nul = []
for s, b in TG.items():
    o = vb.bt(cA, b.intra); act = o[o.pos != 0]
    obs = {k: 1e4 * act[m].pnl.mean() for k, m in [("ALL", act.index == act.index), ("OOS", act.index >= vb.SPLIT)]}
    df = pd.concat([cA.rename("s"), b.intra.rename("y")], axis=1).dropna()
    sh = []
    for i in range(1000):
        k = int(rng.integers(30, len(df) - 30))
        s2 = pd.Series(np.roll(df.s.values, k), index=df.index)
        oo = vb.bt(s2, df.y); a = oo[oo.pos != 0]
        sh.append((1e4 * a.pnl.mean(), 1e4 * a[a.index >= vb.SPLIT].pnl.mean()))
    sh = np.array(sh)
    # rastgele isaret: aktif gunlerde pozisyon isaretini karistir (ayni n, ayni long/short orani)
    rs = []
    for i in range(2000):
        p = rng.permutation(act.pos.values); pnl = p * act.y.values - 15e-4
        rs.append((1e4 * pnl.mean(), 1e4 * pnl[act.index >= vb.SPLIT].mean()))
    rs = np.array(rs)
    nul.append(dict(stock=s, obs_ALL=obs["ALL"], obs_OOS=obs["OOS"],
                    shift_p_ALL=(sh[:, 0] >= obs["ALL"]).mean(), shift_p_OOS=(sh[:, 1] >= obs["OOS"]).mean(), shift_med_OOS=np.median(sh[:, 1]), shift_95_OOS=np.percentile(sh[:, 1], 95),
                    perm_p_ALL=(rs[:, 0] >= obs["ALL"]).mean(), perm_p_OOS=(rs[:, 1] >= obs["OOS"]).mean(), perm_med_OOS=np.median(rs[:, 1]), perm_95_OOS=np.percentile(rs[:, 1], 95),
                    n_long=(act.pos > 0).sum(), n_short=(act.pos < 0).sum()))
N = pd.DataFrame(nul); N.to_csv(os.path.join(vb.OUT, "res_s3_null.csv"), index=False); print(N.round(3).to_string())
# (e) genislik: ayni sinyal tum VIOP hisseleri + endeksler
import json
cat = pd.read_csv(os.path.join(vb.DATA, "catalog.csv"))
viop = cat[cat.group == "VIOP"].sym.tolist()
idx = ["XU100.IS", "XU030.IS", "XUSIN.IS", "XBANK.IS", "XMANA.IS", "XHOLD.IS", "XUMAL.IS", "XKMYA.IS", "XMADN.IS", "XTAST.IS", "XUHIZ.IS", "XGIDA.IS", "ISDMR.IS", "KRDMA.IS", "KRDMB.IS"]
br = []
for s in viop + idx:
    if not os.path.exists(os.path.join(vb.DATA, "daily", s + ".parquet")): continue
    try:
        b = vb.bist(s)
    except Exception as e:
        continue
    if b.intra.notna().sum() < 500: continue
    r = vb.isoos(vb.bt(cA, b.intra)); cr = vb.corr_t(cA, b.intra)
    cri = vb.corr_t(cA[cA.index < vb.SPLIT], b.intra); cro = vb.corr_t(cA[cA.index >= vb.SPLIT], b.intra)
    br.append(dict(sym=s, IS_bps=r["IS_bps"], IS_t=r["IS_t"], OOS_bps=r["OOS_bps"], OOS_t=r["OOS_t"], corr=cr[0], corr_t=cr[1], corr_IS_t=cri[1], corr_OOS_t=cro[1], n=cr[2]))
BR = pd.DataFrame(br).sort_values("corr_t", ascending=False); BR.to_csv(os.path.join(vb.OUT, "res_s3_breadth.csv"), index=False)
print(BR.round(2).to_string())
