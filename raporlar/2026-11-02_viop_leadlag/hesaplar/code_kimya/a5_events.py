"""A5: olay/rejim testleri.
(a) 6 Şubat 2023 depremi: çimento hisseleri anormal getirisi (XU100'e göre), ve öncesi/sonrası rejim (beta, XU100 korelasyonu, yurt içi küme kısmi korelasyonu).
(b) İran/İsrail olayları ve Razi haberleri -> GUBRF anormal getirisi (piyasa modeli, [-250,-20] tahmin penceresi).
(c) Gaz krizi rejimi (2021-07..2022-12): TTF ile senkron/kısmi korelasyon rejime göre.
(d) HEKTS bireysel yatırımcı yapısı: otokorelasyon, |r| kümelenmesi, 'tarım teması' kümesi; OYAK kardeş etkisi (HEKTS-OYAKC).
(e) İhracatçı kur faktörü (FX düzeltmeli): aylık kısmi korelasyon USDTRY, EURTRY.
Çıktı: res_events.csv, res_regime.csv"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kc import *
from kc import _corr
HERE = os.path.dirname(os.path.abspath(__file__))
m = R("XU100")


def car(stock, date, win=(0, 5), est=(-250, -20), market=None):
    a = R(stock); mk = m if market is None else market
    df = pd.concat([a.rename("a"), mk.rename("m")], axis=1).dropna()
    pos = df.index.searchsorted(pd.Timestamp(date))
    if pos >= len(df): return np.nan, np.nan
    e = df.iloc[max(0, pos + est[0]):pos + est[1]]
    b, a0 = np.polyfit(e.m, e.a, 1)
    ar = df.a - (a0 + b * df.m); sd = ar.iloc[max(0, pos + est[0]):pos + est[1]].std()
    w = ar.iloc[pos + win[0]:pos + win[1] + 1]
    return float(w.sum()), float(w.sum() / (sd * np.sqrt(len(w))))


rows = []
# (a) deprem
EQ = "2023-02-06"
for s in ["CIMSA", "OYAKC", "AKCNS.IS", "NUHCM.IS", "AFYON.IS", "BUCIM.IS", "KONYA.IS", "BTCIM.IS", "EKGYO", "SISE", "GUBRF", "HEKTS", "TKFEN", "ENKAI", "KRDMD", "EREGL"]:
    for win in [(0, 0), (0, 5), (0, 20), (0, 60)]:
        c, z = car(s, EQ, win)
        rows.append({"event": "deprem_2023-02-06", "stock": s, "win": f"{win}", "CAR_pct": 100 * c, "z": z})
# (b) İran/İsrail + Razi olayları (hafta sonu olayında ilk işlem günü kullanılır)
EV = {"Razi dava/bedelsiz SPK engeli (2022-12-16)": "2022-12-16",
      "Iran->Israel insansız hava saldırısı (2024-04-13 Cmt)": "2024-04-15",
      "Iran füze saldırısı (2024-10-01 akşam)": "2024-10-02",
      "Israil'in Iran'ı vurması (2024-10-26 Cmt)": "2024-10-28",
      "Razi satış ihalesi YK kararı (2025-02-28)": "2025-03-03",
      "Israil-Iran savaşı başlangıcı (2025-06-13)": "2025-06-13",
      "ABD'nin Iran nükleer tesislerini vurması (2025-06-22 Paz)": "2025-06-23",
      "Iran-Israil ateşkes (2025-06-24)": "2025-06-24",
      "Razi ihalesinin sonlandırılması (2025-11-28)": "2025-11-28"}
for name, d in EV.items():
    for s in ["GUBRF", "HEKTS", "TKFEN", "BAGFS.IS", "TUPRS", "XU100"]:
        for win in [(0, 0), (0, 2), (0, 10)]:
            if s == "XU100":
                r = R("XU100"); pos = r.index.searchsorted(pd.Timestamp(d)); c = r.iloc[pos + win[0]:pos + win[1] + 1].sum(); z = np.nan
            else:
                c, z = car(s, d, win)
            rows.append({"event": name, "stock": s, "win": f"{win}", "CAR_pct": 100 * c, "z": z})
E = pd.DataFrame(rows); E.to_csv(os.path.join(HERE, "res_events.csv"), index=False)
pd.set_option("display.width", 250)
print(E[(E.win.isin(["(0, 0)", "(0, 5)", "(0, 20)", "(0, 60)"])) & (E.event.str.startswith("deprem"))].pivot(index="stock", columns="win", values="CAR_pct").round(1).to_string())
g = E[(E.stock == "GUBRF")].pivot(index="event", columns="win", values="CAR_pct").round(1)
gz = E[(E.stock == "GUBRF")].pivot(index="event", columns="win", values="z").round(1)
print(pd.concat([g, gz.add_suffix("_z")], axis=1).to_string())

# rejim tablosu
reg = []
PER = {"pre_EQ_2021-2022": ("2021-01-01", "2023-02-01"), "post_EQ_2023-02..2024-02": ("2023-02-15", "2024-02-15"), "2024-03..2026-10": ("2024-03-01", "2026-11-01"),
       "IS_2014-2020": ("2014-01-01", "2021-01-01"), "gas_crisis_2021-07..2022-12": ("2021-07-01", "2023-01-01"), "2018_kur_krizi": ("2018-05-01", "2018-12-31"),
       "2025-03_imamoglu..": ("2025-03-19", "2025-06-30"), "fon_krizi_2026-09..10": ("2026-09-01", "2026-11-01")}
TRC = ["AKCNS.IS", "NUHCM.IS", "AFYON.IS", "BUCIM.IS", "KONYA.IS"]
trc = pd.concat([R(x) for x in TRC], axis=1).mean(axis=1)
for lab, (a0, a1) in PER.items():
    for s in ["CIMSA", "OYAKC"]:
        a = R(s); df = pd.concat([a.rename("a"), m.rename("m")], axis=1).dropna(); df = df[(df.index >= a0) & (df.index < a1)]
        beta = np.polyfit(df.m, df.a, 1)[0] if len(df) > 30 else np.nan
        reg.append({"period": lab, "stock": s, "corr_xu100": df.a.corr(df.m), "beta_xu100": beta, "pc_trcement": pc(a, trc, [m], a0, a1, min_n=30)[0],
                    "pc_EKGYO": pc(a, R("EKGYO"), [m], a0, a1, min_n=30)[0], "pc_HEI": pc(a, R("HEI.DE"), [m], a0, a1, min_n=30)[0],
                    "vol_ann": a[(a.index >= a0) & (a.index < a1)].std() * np.sqrt(252)})
    for s in ["SISE", "GUBRF", "CIMSA", "OYAKC", "TKFEN", "HEKTS", "XU100"]:
        reg.append({"period": lab, "stock": s, "c_TTF": _corr(R(s), R("TTF=F"), a0, a1, min_n=30)[0],
                    "pc_TTF": pc(R(s), R("TTF=F"), [m], a0, a1, min_n=30)[0] if s != "XU100" else np.nan,
                    "c_TTF_l1gap": _corr(DEC(s)["gap"], R("TTF=F").shift(1), a0, a1, min_n=30)[0]})
RG = pd.DataFrame(reg); RG.to_csv(os.path.join(HERE, "res_regime.csv"), index=False)
print(RG[RG.stock.isin(["CIMSA", "OYAKC"]) & RG.corr_xu100.notna()][["period", "stock", "corr_xu100", "beta_xu100", "pc_trcement", "pc_EKGYO", "pc_HEI", "vol_ann"]].round(2).to_string(index=False))
print(RG[RG.c_TTF.notna()].pivot(index="stock", columns="period", values="c_TTF").round(2).to_string())
print(RG[RG.pc_TTF.notna()].pivot(index="stock", columns="period", values="pc_TTF").round(2).to_string())

# (d) HEKTS bireysel yapı
hx = []
for s in STOCKS + ["XU100"]:
    a = R(s); a = a[a.index >= "2014-01-01"]
    hx.append({"stock": s, "ac1": a.autocorr(1), "ac1_IS": a[a.index < SPLIT].autocorr(1), "ac1_OOS": a[a.index >= SPLIT].autocorr(1),
               "absac1": a.abs().autocorr(1), "vol_ann": a.std() * np.sqrt(252), "gap_intra_corr": DEC(s)[["gap", "intra"]].dropna().corr().iloc[0, 1],
               "gap_intra_OOS": DEC(s)[DEC(s).index >= SPLIT][["gap", "intra"]].dropna().corr().iloc[0, 1],
               "beta_xu100_OOS": np.polyfit(*pd.concat([m.rename("m"), R(s).rename("a")], axis=1).dropna().loc["2021":].T.values, 1)[0] if s != "XU100" else 1.0})
HX = pd.DataFrame(hx); HX.to_csv(os.path.join(HERE, "res_stockchar.csv"), index=False)
print(HX.round(3).to_string(index=False))
