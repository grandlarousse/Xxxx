"""1-2. adım: veri kontrolü, küme endeksleri, dalga listesi (küme + sektör endeksleri). Çıktı: cikti/*.csv"""
import os, sys, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from veri import panel, kume_getiri, rf_gunluk
from kumeler import KUMELER, ENDEKSLER
from dalga import dalgalar
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cikti"); os.makedirs(OUT, exist_ok=True)
SON = sys.argv[1] if len(sys.argv) > 1 else None
P, R, sup = panel(SON)
print("şüpheli günlük getiriler (|r|>%35 -> 0):", len(sup)); [print(" ", x) for x in sup]
C, NU = kume_getiri(R)
C = C.where(NU >= 2)
cal = C.index; rf, rfy = rf_gunluk(cal)
xu = (1 + R["XU100"].fillna(0)).cumprod(); usd = P["USDTRY"].ffill()
I = (1 + C.fillna(0)).cumprod().where(C.notna().cummax())
Rel = I.div(xu, axis=0)
# sektör endeksleri
SE = [e for e in ENDEKSLER if e not in ("XU100", "XUTUM", "XU050", "XU030") and e in P]
IE = P[SE].ffill(limit=5); RelE = IE.div(P["XU100"], axis=0)
bas = pd.Timestamp("2011-06-01")
def tablo(Rel, I, kaynak, D, esik):
    W = dalgalar(Rel.loc[bas:], D=D, esik=esik)
    rows = []
    for _, w in W.iterrows():
        a, b = w.dip, w.tepe
        tl = I.at[b, w.kume] / I.at[a, w.kume] - 1
        x = xu.at[b] / xu.at[a] - 1
        u = (1 + tl) / (usd.at[b] / usd.at[a]) - 1
        ib = cal.get_loc(b); b3 = cal[min(ib + 63, len(cal) - 1)]
        sonra = Rel.at[b3, w.kume] / Rel.at[b, w.kume] - 1
        lid = ""
        if kaynak == "kume":
            best = -9
            for m in KUMELER[w.kume]:
                if m in P and pd.notna(P.at[a, m]) and pd.notna(P.at[b, m]):
                    g = P.at[b, m] / P.at[a, m] - 1
                    if g > best: best, lid = g, f"{m} {g:+.0%}"
        rows.append(dict(kaynak=kaynak, kume=w.kume, dip=a.date(), tepe=b.date(), teyitli=w.teyitli, gun=w.gun,
                         rel=w.rel, max6ay_rel=w.max6ay, tl=tl, usd=u, xu100=x, sonraki3ay_rel=sonra, lider=lid,
                         uye_n=int(NU.at[b, w.kume]) if kaynak == "kume" else np.nan))
    return pd.DataFrame(rows)
for D, esik, ad in [(0.15, 0.30, "taban"), (0.20, 0.50, "sert")]:
    T1 = tablo(Rel, I, "kume", D, esik); T2 = tablo(RelE, IE, "endeks", D, esik)
    T = pd.concat([T1, T2]).sort_values(["dip"])
    T.to_csv(os.path.join(OUT, f"dalgalar_{ad}.csv"), index=False, float_format="%.4f")
    print(f"\n=== DALGALAR ({ad}: D={D:.0%}, eşik={esik:.0%}/6ay) küme={len(T1)} endeks={len(T2)}")
    if ad == "taban":
        pd.set_option("display.width", 250); pd.set_option("display.max_rows", 500)
        print(T1.sort_values("dip").to_string(index=False, float_format=lambda v: f"{v:.2f}"))
        print(T2.sort_values("dip").to_string(index=False, float_format=lambda v: f"{v:.2f}"))
# küme özet: yıllık getiri, üye sayıları
yil = C.groupby(C.index.year).apply(lambda z: (1 + z.fillna(0)).prod() - 1)
yil["XU100"] = R["XU100"].groupby(R.index.year).apply(lambda z: (1 + z.fillna(0)).prod() - 1)
yil["USDTRY"] = usd.groupby(usd.index.year).last() / usd.groupby(usd.index.year).last().shift(1) - 1
yil.to_csv(os.path.join(OUT, "kume_yillik_tl.csv"), float_format="%.4f")
NU.resample("YE").last().to_csv(os.path.join(OUT, "kume_uye_sayisi.csv"))
TMP = "/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/data/dalga_bist"
Rel.to_csv(os.path.join(TMP, "kume_goreli_endeks.csv"), float_format="%.5f")
I.to_csv(os.path.join(TMP, "kume_tl_endeks.csv"), float_format="%.5f")
print(yil.loc[2012:].round(2).T.to_string())
