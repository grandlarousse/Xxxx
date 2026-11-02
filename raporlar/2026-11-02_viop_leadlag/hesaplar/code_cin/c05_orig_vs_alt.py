"""cin - Adım 5: Orijinal Çin serisi vs TradingView'da açılabilecek alternatif: senkron, alt->orig(t+1), 2 günlük, haftalık korelasyon.
Ortak işlem günleri (inner join) üzerinde. Başlangıç 2010-01-01 (vadeli: roll-düzeltilmiş dönem ~2018-12+).
Vekil sadakat etiketi (alternatifin orijinali temsil gücü; BIST ilişki etiketi DEĞİL):
  YÜKSEK: haftalık r>=0,80 ve 2g r>=0,70 ve son3y haftalık >=0,75 ; ORTA: haftalık >=0,60 ; DÜŞÜK: haftalık >=0,30 ; ÇOK DÜŞÜK: <0,30
Çıktı: out/code_cin/orig_alt_all.csv, out/cin_alternatifler.csv (orijinal başına tüm adaylar, sıralı)"""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_cin")
import cin_lib as C, numpy as np, pandas as pd
from pairs_def import ORIG, ALT, PAIRS
OUT = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/"
def lab(r):
    w, d2, w3 = r["corr_weekly"], r["corr_2d"], r["corr_weekly_3y"]
    if pd.isna(w): return "ÇOK DÜŞÜK"
    if w >= 0.80 and d2 >= 0.70 and (pd.isna(w3) or w3 >= 0.75) and r["n_w"] >= 100: return "YÜKSEK"
    if w >= 0.60: return "ORTA"
    if w >= 0.30: return "DÜŞÜK"
    return "ÇOK DÜŞÜK"
rows = []
for o, alts in PAIRS.items():
    for a in alts:
        try: res = C.pair_orig_alt(o, a)
        except Exception as e: res = None; print("ERR", o, a, e)
        od = ORIG.get(o, ("", "", "")); ad = ALT.get(a, (ORIG.get(a, ("", ""))[0], "Çin borsası (AÇILMIYOR)" if a.startswith("FUT") else "", "07:00"))
        r = {"orijinal": o, "orijinal_desc": od[0], "orijinal_tv": od[1] + (" (AÇILMIYOR)" if not ("HSI" in od[1] or "HKEX" in od[1] or "FX:" in od[1]) else ""),
             "kapanis_orig_utc": od[2], "alternatif_yahoo": a, "alternatif_desc": ad[0], "alternatif_tv": ad[1], "kapanis_alt_utc": ad[2]}
        if res: r.update(res)
        rows.append(r)
D = pd.DataFrame(rows)
D["guven"] = D.apply(lab, axis=1)
D["kapanis_farki"] = D["kapanis_orig_utc"] + " vs " + D["kapanis_alt_utc"]
D.to_csv(OUT + "code_cin/orig_alt_all.csv", index=False)
def note(r):
    s = []
    if "HKEX" in str(r["alternatif_tv"]) or "HSI:" in str(r["alternatif_tv"]): s.append("HK kaynağı: TV'de açılmayabilir")
    if "OTC" in str(r["alternatif_tv"]): s.append("OTC: likidite/bayat fiyat riski")
    if not pd.isna(r.get("corr_altlead")) and r["corr_altlead"] > 0.15: s.append(f"alt_t->orig_t+1 r={r['corr_altlead']:.2f} (ABD kapanışı sonra: alt bir gün ÖNDE)")
    if not pd.isna(r.get("n")) and r["n"] < 500: s.append("kısa örneklem")
    s.append(f"dönem {r.get('start','')}..{r.get('end','')}; 3y haftalık r={r.get('corr_weekly_3y', np.nan):.2f}")
    return "; ".join(s)
D["not"] = D.apply(note, axis=1)
cols = ["orijinal", "orijinal_desc", "orijinal_tv", "alternatif_yahoo", "alternatif_desc", "alternatif_tv", "corr_sync", "corr_altlead", "corr_2d", "corr_weekly",
        "corr_weekly_3y", "n", "n_w", "kapanis_farki", "beta_w", "not", "guven"]
E = D[cols].sort_values(["orijinal", "corr_weekly"], ascending=[True, False])
E.round(3).to_csv(OUT + "cin_alternatifler.csv", index=False)
best = E.groupby("orijinal").head(3)
best[["orijinal", "alternatif_yahoo", "corr_sync", "corr_altlead", "corr_2d", "corr_weekly", "corr_weekly_3y", "n", "guven"]].round(2).to_csv(OUT + "code_cin/orig_alt_top3.csv", index=False)
print(len(D), "çift test edildi")
