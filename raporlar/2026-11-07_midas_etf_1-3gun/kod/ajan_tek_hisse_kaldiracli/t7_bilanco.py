"""TH04: bilanço (kazanç duyurusu) etrafı — tek hisse 2x ETF'ler.
Tarihler: sonuclar/aile_tek_hisse_kaldiracli/bilanco_tarihleri.csv (b0_bilanco.py; Nasdaq takvimi, eksikler hacim+boşluktan 'tahmini').
Bu 9 şirket duyuruyu seans sonrası (AMC) yapar: duyuru günü E (t), tepki günü R = E'den sonraki ilk işlem günü (t+1).
Ölçümler (dayanak sentetik kalibre 2x, 2016+; maliyet birincil ETF 2.500$):
  B1 'bilanço kumarı': C_E al -> C_R sat (duyuruyu taşı). Ortalama, std, kuyruklar.
  B2 PEAD (TH04 testi): C_R -> C_R+2 (= C_t+1 -> C_t+3) long; koşulsuz ve tepki yönüne göre (devam/dönüş).
  B3 duyuru öncesi koşu: C_E-3 -> C_E long (duyuruya kadar, duyuru taşınmaz).
  B4 tepki günü O1: R açılışında al, R kapanışında sat (boşluk sonrası gün içi devam/dönüş), tepki yönüne göre.
Çalıştırma: python3 -I kod/ajan_tek_hisse_kaldiracli/t7_bilanco.py   Çıktı: bilanco_testleri.csv, bilanco_olaylar.csv"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import thk, lib

pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40); pd.set_option("display.max_rows", 200)
B = pd.read_csv(os.path.join(thk.OUT, "bilanco_tarihleri.csv"), parse_dates=["date"])
ev = []
for st in thk.STOCKS:
    sdf = thk.load_stock(st); syn = thk.synth_for(st, 2.0); idx = sdf.index
    pos = pd.Series(np.arange(len(idx)), index=idx)
    cost = thk.cost_for(thk.PRIMARY[st]) / 1e4
    sg = sdf["c"].pct_change().rolling(60).std()
    for _, r in B[B.sym == st].iterrows():
        E = r["date"]
        a = idx[idx >= E]
        if not len(a): continue
        iE = pos[a[0]] if a[0] == E else pos[a[0]] - 1   # E işlem günü değilse önceki işlem günü
        iR = iE + 1
        if iE < 3 or iR + 2 >= len(idx): continue
        c = syn["c"].values; o = syn["o"].values; cs = sdf["c"].values; os_ = sdf["o"].values
        react = cs[iR] / cs[iE] - 1
        ev.append({"stock": st, "E": idx[iE], "R": idx[iR], "kaynak": r["kaynak"], "tepki_hisse": react,
                   "tepki_z": react / sg.iloc[iE] if sg.iloc[iE] > 0 else np.nan,
                   "bosluk_hisse": os_[iR] / cs[iE] - 1,
                   "B1_tasima": c[iR] / c[iE] - 1 - cost,
                   "B2_pead": c[iR + 2] / c[iR] - 1 - cost,
                   "B3_oncesi": c[iE] / c[iE - 3] - 1 - cost,
                   "B4_gunici": c[iR] / o[iR] - 1 - cost,
                   "is": idx[iE] <= lib.IS_END})
EV = pd.DataFrame(ev)
EV.to_csv(os.path.join(thk.OUT, "bilanco_olaylar.csv"), index=False)
print("Olay sayısı:", len(EV), EV.groupby("stock").size().to_dict(), "| kaynak:", EV.kaynak.value_counts().to_dict())
# normal günlere göre tepki büyüklüğü
for st in thk.STOCKS:
    sdf = thk.load_stock(st); r = sdf["c"].pct_change().abs()
    e = EV[EV.stock == st]
    print(f"  {st}: ort |tepki| {e.tepki_hisse.abs().mean()*1e4:6.0f} bp (normal gün ort |r| {r.mean()*1e4:4.0f} bp); 2x taşıma en kötü {e.B1_tasima.min()*1e4:7.0f} bp, en iyi {e.B1_tasima.max()*1e4:7.0f} bp")

def tstat(x):
    x = pd.Series(x).dropna()
    if len(x) < 3: return len(x), np.nan, np.nan
    return len(x), x.mean() * 1e4, x.mean() / (x.std(ddof=1) / math.sqrt(len(x)))

rows = []
def add(name, sub, col, note=""):
    n, m, t = tstat(sub[col])
    ni, mi, ti = tstat(sub[sub["is"]][col]); no, mo, to = tstat(sub[~sub["is"]][col])
    yrs = sub.groupby(sub.E.dt.year)[col].mean()
    rows.append({"test": name, "n": n, "net_bp": m, "t": t, "is_n": ni, "is_net_bp": mi, "is_t": ti, "oos_n": no, "oos_net_bp": mo, "oos_t": to,
                 "kazanma": float((sub[col] > 0).mean()) if n else np.nan, "en_kotu_bp": float(sub[col].min() * 1e4) if n else np.nan,
                 "std_bp": float(sub[col].std() * 1e4) if n > 1 else np.nan, "yil_poz": float((yrs > 0).mean()) if len(yrs) else np.nan,
                 "p": lib.t_to_p(t, n), "not": note})
for grp, sub in [("hepsi", EV), ("takvim_dogrulanmis", EV[~EV.kaynak.str.startswith("tahmini")]), ("mega7", EV[EV.stock.isin(["NVDA", "TSLA", "AAPL", "AMZN", "META", "MSFT", "GOOGL"])]),
                 ("kripto2", EV[EV.stock.isin(["MSTR", "COIN"])])]:
    add(f"B1_tasima_{grp}", sub, "B1_tasima", "C_E al, C_R sat (duyuru taşınır)")
    add(f"B2_pead_kosulsuz_{grp}", sub, "B2_pead", "C_R -> C_R+2 long (TH04: ~0 beklenir)")
    add(f"B2_pead_pozitif_tepki_{grp}", sub[sub.tepki_hisse > 0], "B2_pead", "devam: olumlu tepkiden sonra long")
    add(f"B2_pead_negatif_tepki_{grp}", sub[sub.tepki_hisse < 0], "B2_pead", "dönüş: olumsuz tepkiden sonra long")
    add(f"B3_oncesi_{grp}", sub, "B3_oncesi", "C_E-3 -> C_E long (duyuru taşınmaz)")
    add(f"B4_gunici_pozitif_bosluk_{grp}", sub[sub.bosluk_hisse > 0], "B4_gunici", "R açılış->kapanış, olumlu boşluk")
    add(f"B4_gunici_negatif_bosluk_{grp}", sub[sub.bosluk_hisse < 0], "B4_gunici", "R açılış->kapanış, olumsuz boşluk")
T = pd.DataFrame(rows)
T["fdr"] = lib.bh_fdr(T.p.values, 0.10)
T.to_csv(os.path.join(thk.OUT, "bilanco_testleri.csv"), index=False)
print(T.round(2).to_string(index=False))
# PEAD yönü: tepki ile sonraki 2 gün korelasyonu
z = EV.dropna(subset=["tepki_hisse", "B2_pead"])
print("\ncorr(tepki, sonraki 2 gün 2x):", round(z.tepki_hisse.corr(z.B2_pead), 3), " n", len(z))
