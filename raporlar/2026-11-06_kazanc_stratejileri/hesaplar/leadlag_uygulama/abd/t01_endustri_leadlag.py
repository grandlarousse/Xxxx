"""T01: FF49 sektor lead-lag -> Tier-A hisselerin sektoru (2010-01 .. 2026-09).

Onceden belirlenmis aile (BIRINCIL, sonuca bakmadan yazildi):
  hedef y = hedef sektorun piyasa-artigi (r - beta_t * MKT), t+1..t+h toplami (bps)
  sinyal z = ongorucunun t'de bilinen L gunluk degeri, kayan 252g z-skoru
  kombinasyonlar (L,h): (1,1) (1,3) (5,5)
  ortak ongoruculer (her hedef): MKT, SMB, OWN (kendi artigi), dVIX
  ekonomik bag ongoruculeri: LINKS sozlugu
  istatistik: OLS, Newey-West HAC (lag = h+L); BH-FDR q=0.10 (aile icinde)
  varyant A: t+1..t+h (kapanis-kapanis, ust sinir; kullanici ABD kapanisinda islem yapamaz)
  varyant B: t+2..t+h+1 (1 gun atlamali; t+1 acilis girisinin muhafazakar vekili)
  IS 2010-2020, OOS 2021-2026/09
KESIF ailesi: 48 diger sektor + 7 makro/faktor ongorucu, ayni kombinasyonlar, ayri BH.
Islem kontrolu: yon IS isaretinden; OOS'ta |z|>1 uygun kuyrukta long; artik getiri - maliyet.
"""
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import ortak as o

TARGETS = {"MedEq": "BDX", "Hlth": "EHC", "Fin": "TW, CME", "Insur": "ACGL, MRSH",
           "Meals": "MAR, HLT", "LabEq": "TMO", "Drugs": "RPRX (ekonomik)", "Hshld": "SN"}
COMMON = ["MKT", "SMB", "OWN", "dVIX"]
LINKS = {"MedEq": ["Hlth", "Drugs", "LabEq"],
         "Hlth": ["Insur", "MedEq"],
         "Fin": ["Banks", "absdY10"],
         "Insur": ["dY10", "Fin"],
         "Meals": ["Trans", "Rtail", "dWTI"],
         "LabEq": ["Drugs", "MedEq"],
         "Drugs": ["Hlth", "Insur", "dY10"],
         "Hshld": ["Rtail"]}
COMBOS = [(1, 1), (1, 3), (5, 5)]
MACRO = ["MKT", "SMB", "dVIX", "dY10", "absdY10", "dWTI"]
IS_END, OOS_START = "2020-12-31", "2021-01-01"
T0, T1 = "2010-01-01", "2026-09-30"
COSTS = (10, 20)  # bps gidis-donus (ABD buyuk hisse, IBKR; Turk kurumunda daha yuksek)

d = o.load_panel()
IND = [c for c in d.columns if c not in ("MKT", "SMB", "RF", "VIX", "DGS10", "WTI")]
assert len(IND) == 49
RES, BETA = {}, {}
for c in IND:
    RES[c], BETA[c] = o.resid(d, c)


def signal(name, target, L):
    if name == "OWN":
        x = RES[target].rolling(L).sum()
    elif name in IND:
        x = RES[name].rolling(L).sum()
    elif name == "MKT":
        x = d["MKT"].rolling(L).sum()
    elif name == "SMB":
        x = d["SMB"].rolling(L).sum()
    elif name == "dVIX":
        x = d["VIX"] - d["VIX"].shift(L)
    elif name == "dY10":
        x = (d["DGS10"] - d["DGS10"].shift(L)) * 100
    elif name == "absdY10":
        x = (d["DGS10"].diff().abs() * 100).rolling(L).mean()
    elif name == "dWTI":
        x = np.log(d["WTI"] / d["WTI"].shift(L))
    else:
        raise KeyError(name)
    return o.zroll(x)


def target_y(target, h, skip):
    fr = o.fwd_sum(d[target], h, skip)
    fm = o.fwd_sum(d["MKT"], h, skip)
    return (fr - BETA[target] * fm) * 1e4  # bps


def win(s, a, b):
    return s[(s.index >= a) & (s.index <= b)]


def run(target, pred, L, h):
    z = signal(pred, target, L)
    row = dict(hedef=target, isim=TARGETS[target], ongorucu=pred, L=L, h=h)
    for var, skip in (("A", 0), ("B", 1)):
        y = target_y(target, h, skip)
        lags = h + L + skip
        for per, a, b in (("tam", T0, T1), ("IS", T0, IS_END), ("OOS", OOS_START, T1)):
            bb, tt, pp, n = o.hac_ols(win(y, a, b), win(z, a, b), lags)
            row[f"{var}_{per}_b"] = bb; row[f"{var}_{per}_t"] = tt; row[f"{var}_{per}_p"] = pp
            if var == "A" and per == "tam":
                row["n"] = n
    # islem kontrolu (OOS, yon IS isaretinden): A = ust sinir (t+1 gece dahil), B = 1 gun atlamali
    sgn = np.sign(row["A_IS_b"])
    zz = win(z, OOS_START, T1)
    for var, skip in (("A", 0), ("B", 1)):
        yy = win(target_y(target, h, skip), OOS_START, T1)
        dd = pd.concat([zz, yy], axis=1).dropna(); dd.columns = ["z", "y"]
        fav = dd["z"] * sgn > 1
        unf = dd["z"] * sgn < -1
        row[f"{var}_OOS_uygun_n"] = int(fav.sum())
        row[f"{var}_OOS_uygun_ort_bps"] = dd.loc[fav, "y"].mean()
        row[f"{var}_OOS_ters_ort_bps"] = dd.loc[unf, "y"].mean()
        row[f"{var}_OOS_kosulsuz_bps"] = dd["y"].mean()
        if fav.sum() > 30:
            _, t2, _, _ = o.hac_ols(dd["y"], fav.astype(float), h + L + 1)
            row[f"{var}_OOS_uygun_fark_t"] = t2
        for c in COSTS:
            row[f"{var}_net{c}_bps"] = row[f"{var}_OOS_uygun_ort_bps"] - c
    return row


def family(pairs, label):
    rows = [run(t, p, L, h) for (t, p) in pairs for (L, h) in COMBOS]
    df = pd.DataFrame(rows)
    rej, q = o.bh(df["A_tam_p"].values, 0.10)
    df["A_q"] = q; df["A_FDR10"] = rej
    rejB, qB = o.bh(df["B_tam_p"].values, 0.10)
    df["B_q"] = qB; df["B_FDR10"] = rejB
    df["IS_OOS_ayni_isaret"] = np.sign(df["A_IS_b"]) == np.sign(df["A_OOS_b"])
    df.to_csv(f"{o.CIKTI}/t01_{label}.csv", index=False, float_format="%.4g")
    return df


if __name__ == "__main__":
    prim = [(t, p) for t in TARGETS for p in COMMON + LINKS[t]]
    P = family(prim, "birincil")
    print("BIRINCIL aile: test sayisi", len(P))
    print("  A (kapanis-kapanis) FDR10 gecen:", int(P["A_FDR10"].sum()),
          "| B (1 gun atlamali) FDR10 gecen:", int(P["B_FDR10"].sum()))
    print("  |t|>=1.96 sayisi (A tam):", int((P["A_tam_t"].abs() >= 1.96).sum()), "beklenen sans ~", round(0.05 * len(P), 1))
    cols = ["hedef", "ongorucu", "L", "h", "A_tam_b", "A_tam_t", "A_q", "A_IS_t", "A_OOS_t",
            "B_tam_t", "B_q", "B_OOS_t", "A_OOS_uygun_n", "A_OOS_uygun_ort_bps", "A_net10_bps", "B_OOS_uygun_ort_bps", "B_OOS_ters_ort_bps"]
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
    print(P.sort_values("A_tam_p")[cols].head(25).round(2).to_string(index=False))
    # kesif ailesi
    expl = [(t, p) for t in TARGETS for p in IND + MACRO if p != t] + [(t, "OWN") for t in TARGETS]
    E = family(expl, "kesif")
    print("\nKESIF aile: test sayisi", len(E), "| A FDR10:", int(E["A_FDR10"].sum()), "| B FDR10:", int(E["B_FDR10"].sum()))
    print("  |t|>=1.96 (A tam):", int((E["A_tam_t"].abs() >= 1.96).sum()), "beklenen ~", round(0.05 * len(E)))
    print("  A FDR gecen ve IS/OOS ayni isaret ve OOS |t|>=1.96:",
          int((E["A_FDR10"] & E["IS_OOS_ayni_isaret"] & (E["A_OOS_t"].abs() >= 1.96)).sum()))
    print(E.sort_values("A_tam_p")[cols].head(30).round(2).to_string(index=False))
