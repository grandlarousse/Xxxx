"""STRATEJİ uluslararasi_S2 (KEŞİFSEL, düşük güven) — EWY gün sonu dip dönüşü.
Kural (strategies.LIB 'MR_ibs_lt01_dusus', değiştirilmeden): EWY'de IBS_t=(C-L)/(H-L) < 0.10 VE C_t < C_t-1 -> EWY'yi t kapanışında al (C0),
t+1 kapanışında sat (h=1). Kaldıraçlı uygulama: aynı EWY sinyaliyle KORU.
Uyarı: genel kütüphanenin 31 sinyal x 9 kombinasyon x 68 ETF taramasından seçildi; aile içi tek yönlü BH-FDR'yi GEÇMİYOR.
Çalıştır: python3 -I kod/ajan_uluslararasi/strateji_S2_ewy_ibs.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import ortak, lib
import strategies as S

def main():
    pd.set_option("display.width", 250)
    ewy = lib.load("EWY")
    sig = S.LIB["MR_ibs_lt01_dusus"](ewy, None).reindex(ewy.index).fillna(False).astype(bool); sig.iloc[:200] = False
    keys = ["n", "mean_gross_bp", "mean_net_bp", "net_1000_bp", "net_10000_bp", "win", "pf", "t", "is_n", "is_net_bp", "is_t", "oos_n", "oos_net_bp",
            "oos_t", "years_pos_frac", "maxdd", "worst_bp", "cost_bp", "edge_bp"]
    R = []
    for sym, df in (("EWY", ewy), ("KORU", lib.load("KORU"))):
        for mode in ("C0", "O1", "C1"):
            for h in (1, 2, 3):
                st, tr = ortak.full_stats(df, sig.reindex(df.index).fillna(False), h, mode, label="S2", sym=sym)
                R.append({"arac": sym, "mode": mode, "h": h, **{k: st.get(k) for k in keys}})
    R = pd.DataFrame(R)
    print("=== uluslararasi_S2: EWY sinyali (IBS<0.10 ve düşüş günü) ===")
    print(R.round(2).to_string(index=False))
    st, tr = lib.evaluate(ewy, sig, 1, "C0")
    y = tr.groupby(tr["sig_date"].dt.year)["net"].agg(["count", "mean", "sum"]); y[["mean", "sum"]] *= 1e4
    print("\n=== EWY C0 h=1 yıllık (net bp) ===\n" + y.round(1).to_string())
    # aynı kural ailenin diğer likit bağımsız ETF'lerinde (C0 h=1)
    O = []
    for s in ortak.independent(10):
        df = lib.load(s)
        sg = S.LIB["MR_ibs_lt01_dusus"](df, None).reindex(df.index).fillna(False).astype(bool); sg.iloc[:200] = False
        st, _ = ortak.full_stats(df, sg, 1, "C0", label="S2", sym=s)
        O.append({"sym": s, "bolge": ortak.REGION.get(s), **{k: st.get(k) for k in ["n", "mean_gross_bp", "mean_net_bp", "t", "is_net_bp", "oos_net_bp", "cost_bp"]}})
    O = pd.DataFrame(O).sort_values("t", ascending=False)
    print("\n=== Aynı kural, ailenin likit bağımsız ETF'leri (C0 h=1) ===")
    print(O.round(2).to_string(index=False))
    print("pozitif net oranı:", round((O["mean_net_bp"] > 0).mean(), 2), " t>=2 sayısı:", int((O["t"] >= 2).sum()), "/", len(O))
    r = np.log(ewy["c"]).diff()
    print("\nEWY 1 günlük otokorelasyon  IS:", round(r[r.index <= lib.IS_END].autocorr(1), 3), " OOS:", round(r[r.index > lib.IS_END].autocorr(1), 3))
    R.to_csv(os.path.join(ortak.OUT, "S2_ewy.csv"), index=False); O.to_csv(os.path.join(ortak.OUT, "S2_aile.csv"), index=False)

if __name__ == "__main__":
    main()
