"""4. adım: güncel durum. Son tam kapanış (SON, varsayılan 2026-11-05) + 06.11 gün içi anlık (çekim ~12:45 TSİ).
Küme RS tablosu, durum etiketi, üye tablosu (VİOP), korelasyon/oynaklık (boyutlama)."""
import os, sys, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from veri import panel, kume_getiri, rf_gunluk
from kumeler import KUMELER, VIOP
from dalga import zigzag
import motor as M
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cikti")
pd.set_option("display.width", 260); pd.set_option("display.max_columns", 40); pd.set_option("display.max_rows", 200)
SON = os.environ.get("SON", "2026-11-05")
def kur(son):
    P, R, sup = panel(son); C, NU = kume_getiri(R); rf, _ = rf_gunluk(C.index)
    return P, R, C, NU, M.Veri(P, R, C, NU, rf, KUMELER)
P, R, C, NU, V = kur(SON)
P6, R6, C6, NU6, V6 = kur(None)
t = len(V.cal) - 1; d0 = V.cal[t]
rows = []
for k, c in enumerate(V.kumeler):
    if not V.elig[t, k]: continue
    Rl = V.RelD[c].where(V.elig[:, k])
    s = Rl.dropna(); w = s.iloc[-252:]
    h126 = s.iloc[-126:].max(); h63 = s.iloc[-63:].max()
    dsh = int((s.iloc[-126:][::-1].values >= h126 * 0.9999).argmax())  # son 126g göreli zirvesinden bu yana gün
    ma50 = s.rolling(50).mean().iloc[-1]; ma50_20 = s.rolling(50).mean().iloc[-21]
    r = lambda L: s.iloc[-1] / s.iloc[-1 - L] - 1 if len(s) > L else np.nan
    I = V.ID[c]; a63 = I.iloc[-1] / I.iloc[-64] - 1
    dm6 = (I.iloc[-1] / I.iloc[-127] - 1 > V.rfL[126][t]) and (r(126) > 0)
    br = V.br[t, k]
    dd252 = s.iloc[-1] / w.max() - 1; up252 = s.iloc[-1] / w.min() - 1
    # 06.11 gün içi göreli değişim
    k6 = V6.kumeler.index(c); g6 = V6.Rel[-1, k6] / V6.Rel[-2, k6] - 1 if V6.cal[-1] > d0 else np.nan
    # etiket
    if dsh <= 5 and s.iloc[-1] > ma50: et = "KIRILIM (126g RS zirvesi <=5g)"
    elif s.iloc[-1] >= h63 * 0.9999 - 0 and s.iloc[-1] > ma50: et = "KIRILIM (63g RS zirvesi)"
    elif s.iloc[-1] > ma50 and ma50 > ma50_20 and r(63) > 0: et = "RS YUKSELIS"
    elif r(126) > 0 and (s.iloc[-1] < ma50 or r(21) < -0.05): et = "DONUYOR (zirveden zayif)"
    elif r(126) <= 0 and s.iloc[-1] > ma50 and r(21) > 0: et = "TOPARLANMA DENEMESI"
    else: et = "RS DUSUS"
    uy = [m for m in KUMELER[c] if m in V.allm]
    rows.append(dict(kume=c, uye=int(NU.iloc[t][c]), viop=",".join([m for m in uy if m in VIOP]) or "-",
                     rel21=r(21), rel63=r(63), rel126=r(126), rel252=r(252), tl63=a63, rel_ma50=s.iloc[-1] / ma50 - 1,
                     gun_126g_zirveden=dsh, rel_252g_zirveden=dd252, rel_252g_dipten=up252, genislik50=br, dm6=dm6,
                     rel_0611_gunici=g6, durum=et))
T = pd.DataFrame(rows).set_index("kume")
T["sira_12ay"] = T.rel252.rank(ascending=False).astype("Int64")
T["sira_6ay"] = T.rel126.rank(ascending=False).astype("Int64")
T["komp"] = T[["rel21", "rel63", "rel126"]].mean(1); T["sira_komp"] = T.komp.rank(ascending=False).astype("Int64")
T = T.sort_values("rel252", ascending=False)
print(f"=== KÜME RS TABLOSU (son tam kapanış {d0.date()}; XU100>200GHO={bool(V.mkt200[t])}) ===")
print(T.drop(columns=["komp"]).to_string(float_format=lambda v: f"{v:.3f}"))
T.to_csv(os.path.join(OUT, "guncel_kume_tablosu.csv"), float_format="%.4f")
xu = P["XU100"].dropna()
print("XU100:", xu.iloc[-1], "200GHO:", round(xu.rolling(200).mean().iloc[-1], 1), "50GHO:", round(xu.rolling(50).mean().iloc[-1], 1),
      "zirveden:", round(xu.iloc[-1] / xu.iloc[-252:].max() - 1, 3), "| 06.11 gün içi XU100:", P6["XU100"].dropna().iloc[-1])
# üye tablosu (ilk 8 küme + odak kümeler)
odak = list(T.index[:8]) + [c for c in ["BANKA", "SAVUNMA", "ELK_EKIPMAN", "HAVACILIK", "CELIK"] if c not in T.index[:8]]
mr = []
for c in odak:
    for m in KUMELER[c]:
        if m not in P: continue
        s = P[m].dropna()
        if len(s) < 260:
            g252 = np.nan
        else:
            g252 = s.iloc[-1] / s.iloc[-253] - 1
        x = (1 + R["XU100"].fillna(0)).cumprod()
        rel63 = (s.iloc[-1] / s.iloc[-64]) / (x.iloc[-1] / x.iloc[-64]) - 1 if len(s) > 64 else np.nan
        mr.append(dict(kume=c, hisse=m, viop="V" if m in VIOP else "", g21=s.iloc[-1] / s.iloc[-22] - 1 if len(s) > 22 else np.nan,
                       g63=s.iloc[-1] / s.iloc[-64] - 1 if len(s) > 64 else np.nan, g252=g252, rel63=rel63,
                       ust50=bool(s.iloc[-1] > s.rolling(50).mean().iloc[-1]), ust200=bool(s.iloc[-1] > s.rolling(200).mean().iloc[-1]) if len(s) > 200 else None,
                       zirveden=s.iloc[-1] / s.iloc[-252:].max() - 1))
MR = pd.DataFrame(mr); MR.to_csv(os.path.join(OUT, "guncel_uye_tablosu.csv"), index=False, float_format="%.4f")
print(MR.to_string(index=False, float_format=lambda v: f"{v:.3f}"))
# korelasyon (son 250 gün): günlük küme getirisi ve XU100'e göre fazla getiri
Cd = C.iloc[-250:][T.index]
Ex = Cd.sub(R["XU100"].iloc[-250:], axis=0)
K1 = Cd.corr(); K2 = Ex.corr()
K1.to_csv(os.path.join(OUT, "guncel_korelasyon_getiri.csv"), float_format="%.2f"); K2.to_csv(os.path.join(OUT, "guncel_korelasyon_fazla.csv"), float_format="%.2f")
vol = Cd.std() * np.sqrt(252); volx = Ex.std() * np.sqrt(252)
beta = Cd.apply(lambda s: np.cov(s.fillna(0), R["XU100"].iloc[-250:].fillna(0))[0, 1] / R["XU100"].iloc[-250:].var())
S = pd.DataFrame({"vol_1y": vol, "fazla_vol_1y": volx, "beta_xu100": beta, "ort_kor_getiri": (K1.sum() - 1) / (len(K1) - 1),
                  "ort_kor_fazla": (K2.sum() - 1) / (len(K2) - 1)})
S["ters_vol_agirlik"] = (1 / S.vol_1y) / (1 / S.vol_1y).sum()
print(S.round(3).to_string()); S.to_csv(os.path.join(OUT, "guncel_oynaklik_beta.csv"), float_format="%.4f")
pairs = []
for i, a in enumerate(K2.index):
    for b in K2.index[i + 1:]:
        pairs.append((a, b, K1.at[a, b], K2.at[a, b]))
pp = pd.DataFrame(pairs, columns=["a", "b", "kor_getiri", "kor_fazla"]).sort_values("kor_fazla", ascending=False)
print("En yüksek fazla-getiri korelasyonları:\n", pp.head(15).round(2).to_string(index=False))
print("En negatif:\n", pp.tail(8).round(2).to_string(index=False))
# 12 ay RS rotasyonunun bugünkü seçimi (ilk 3) ve 6 ay / bileşik
for nm, col in [("12ay", "rel252"), ("12-1ay", None), ("6ay", "rel126"), ("komp", "komp")]:
    if col is None:
        sc = pd.Series({c: V.lag21[t, V.kumeler.index(c)] / V.lag[252][t, V.kumeler.index(c)] - 1 for c in T.index})
    else:
        sc = T[col]
    print(f"Rotasyon ilk 3 ({nm}):", list(sc.sort_values(ascending=False).index[:3]), "| son 3:", list(sc.sort_values().index[:3]))
