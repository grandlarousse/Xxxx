"""D4: Kaçırılan fırsat/risk kısa testleri.
 (a) Başabaş enflasyonun KAPANIŞTA GÖZLENEBİLİR vekili: r_TIP(t) - beta60*r_IEF(t) (ikisi de 16:00 ET'de bilinir).
     T10YIE_d (15:30 ET kotasyonu, kapanıştan sonra yayımlanır) yerine bu vekil SLV/GLD'yi öngörüyor mu?
 (b) Aday sinyallerin çakışması (S1/S2/S3/S4 aynı gün): yoğunlaşma riski.
 (c) S3 sinyallerinin geniş piyasa IBS'si ile ilişkisi (GDXJ kenarı genel hisse IBS etkisi mi?).
 (d) S3 C0 kenarının ne kadarı ilk gecede; Mart 2020 NAV iskontosu.
Çalıştır: python3 -I kod/denetim_metal_madenci/d4_kacirilan.py"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import motor as M, lib
from d1_yeniden import ibs_sig, month_end

def warm(s, w=200):
    s = s.copy(); s.iloc[:w] = False; return s

def main():
    rows = []
    tip = M.px("TIP")["c"]; ief = M.px("IEF")["c"]
    rt, ri = np.log(tip).diff(), np.log(ief).diff()
    beta = (rt.rolling(60).cov(ri) / ri.rolling(60).var()).shift(1)
    bei = rt - beta * ri
    t10 = lib.fred("T10YIE"); t10.index = pd.to_datetime(t10.index); t10d = t10.diff().reindex(bei.index)
    print(f"(a) vekil ile T10YIE_d eşzamanlı korelasyonu: {bei.corr(t10d):.2f}")
    for T in ("SLV", "GLD", "GDX"):
        d = M.px(T); r = np.log(d["c"]).diff()
        for h in (1, 3):
            y = sum(r.shift(-k) for k in range(1, h + 1))
            df = pd.DataFrame({"y": y, "x": bei, "own": r, "own1": r.shift(1)}).dropna()
            out = []
            for nm, m in (("tüm", slice(None)), ("IS", df.index <= M.IS_END), ("OOS", df.index > M.IS_END)):
                dd = df[m] if nm != "tüm" else df
                b, tt, n = M.nw_t_reg(dd["y"].values, np.column_stack([np.ones(len(dd)), dd["x"], dd["own"], dd["own1"]]), max(h, 5))
                out.append((nm, tt[1], b[1] * dd["x"].std() * 1e4))
            print(f"    {T} h{h}: " + " | ".join(f"{a} t={b:.2f} ({c:.1f} bp/sd)" for a, b, c in out))
            rows.append(dict(test="TIP-IEF vekil", sym=T, h=h, t=out[0][1], is_t=out[1][1], oos_t=out[2][1], bp_sd=out[0][2]))
        # kural: vekil z60 >= +1.5 -> T long, C0/O1, h1/h3
        z = bei / bei.rolling(60).std().shift(1)
        for mode in ("C0", "O1"):
            for h in (1, 3):
                s = warm((z >= 1.5).reindex(d.index).fillna(False))
                r_ = M.summ(M.sim(d, s, h, mode, M.cost_static(d)), f"vekil z>=1.5 -> {T} {mode} h{h}")
                print(f"    kural {r_['label']}: n={r_['n']} net={r_['net_bp']:.1f} t={r_['t']:.2f} IS t{r_['is_t']:.2f} OOS t{r_['oos_t']:.2f}")
                rows.append(dict(test="vekil kural", sym=T, h=h, mode=mode, n=r_["n"], net_bp=r_["net_bp"], t=r_["t"], is_t=r_["is_t"], oos_t=r_["oos_t"]))
    # (b) çakışma
    gdxj, gld, gdx = M.px("GDXJ"), M.px("GLD"), M.px("GDX")
    s3 = warm(ibs_sig(gdxj)); s4 = warm(ibs_sig(gld)).reindex(gdxj.index).fillna(False)
    s1 = warm(month_end(gdx)).reindex(gdxj.index).fillna(False)
    print(f"\n(b) S3 sinyal günü {int(s3.sum())}; S4 {int(s4.sum())}; ikisi aynı gün {int((s3 & s4).sum())} "
          f"(S4 günlerinin %{100*(s3&s4).sum()/s4.sum():.0f}'i S3 ile aynı); S3 & ay sonu {int((s3 & s1).sum())}")
    tr3 = M.sim(gdxj, s3, 3, "C0", 14.0); tr4 = M.sim(gld, warm(ibs_sig(gld)), 3, "C0", 13.0)
    m = tr3.merge(tr4, on="sig", suffixes=("_3", "_4"))
    print(f"    S3-S4 aynı gün işlemlerinin net getiri korelasyonu: {m['net_3'].corr(m['net_4']):.2f} (n={len(m)})")
    # S4'ün S3 ile çakışmayan günleri
    only4 = tr4[~tr4["sig"].isin(tr3["sig"])]; both4 = tr4[tr4["sig"].isin(tr3["sig"])]
    print(f"    S4 yalnız (S3 yok): n={len(only4)} net={only4['net'].mean()*1e4:.1f} t={M.tstat(only4['net']):.2f} | S3 ile birlikte: n={len(both4)} net={both4['net'].mean()*1e4:.1f} t={M.tstat(both4['net']):.2f}")
    # (c) geniş piyasa IBS ile
    spy = M.px("SPY"); ibs_spy = ((spy["c"] - spy["l"]) / (spy["h"] - spy["l"]).where(spy["h"] > spy["l"])).reindex(gdxj.index)
    tr3["spy_ibs_low"] = (ibs_spy.reindex(tr3["sig"]).values < 0.2)
    for nm, g in tr3.groupby("spy_ibs_low"):
        print(f"(c) S3, SPY IBS<0.2 = {nm}: n={len(g)} net={g['net'].mean()*1e4:.1f} t={M.tstat(g['net']):.2f}")
        rows.append(dict(test="S3 x SPY IBS<0.2", sym="GDXJ", grp=str(nm), n=len(g), net_bp=g["net"].mean() * 1e4, t=M.tstat(g["net"])))
    gld_ibs = ((gld["c"] - gld["l"]) / (gld["h"] - gld["l"]).where(gld["h"] > gld["l"])).reindex(tr3["sig"]).values
    tr3["gld_dn"] = gld_ibs < 0.2
    for nm, g in tr3.groupby("gld_dn"):
        print(f"(c) S3, GLD IBS<0.2 = {nm}: n={len(g)} net={g['net'].mean()*1e4:.1f} t={M.tstat(g['net']):.2f}")
    # (d) ilk gece payı
    o = gdxj["o"]; c = gdxj["c"]
    on1 = (o.shift(-1) / c - 1).reindex(tr3["sig"]).values
    print(f"\n(d) S3 sinyal gecesi (C_t -> O_t+1) ort {np.nanmean(on1)*1e4:.1f} bp (t {M.tstat(on1[np.isfinite(on1)]):.2f}); "
          f"koşulsuz gece ort {np.nanmean((o.shift(-1)/c-1).values)*1e4:.1f} bp")
    x = np.sort(on1)[::-1][:5]; print("    en büyük 5 sinyal gecesi (bp):", np.round(x * 1e4).tolist())
    pd.DataFrame(rows).to_csv(os.path.join(M.OUTD, "d4_kacirilan.csv"), index=False)

if __name__ == "__main__":
    main()
