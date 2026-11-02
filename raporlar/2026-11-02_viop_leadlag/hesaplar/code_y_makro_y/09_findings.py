"""Bulgular CSV'si (out/f_y_makro_y.csv) — ana brifing sütunları + BH-FDR. Tüm scan_*.csv, night.csv, hourly_ll.csv, regime_beta.csv, usd_real.csv, bt.csv birleşir."""
import numpy as np, pandas as pd, glob, json
from scipy import stats
import mlib as M, ll
OUT = M.S + "/out/f_y_makro_y.csv"
DRV = {  # var -> (driver_yahoo, açıklama, TV, mekanizma notu, ilk tarih)
 "y_usd": ("TRY=X", "USDTRY spot (Yahoo, UTC gün sonu ~24:00)", "FX:USDTRY / FX_IDC:USDTRY"),
 "y_eur": ("EURTRY=X", "EURTRY spot (Yahoo, ~24:00 UTC)", "FX:EURTRY"),
 "y_bsk": ("0.5*TRY=X+0.5*EURTRY=X", "Sepet kur (0,5 USD + 0,5 EUR)", "(FX:USDTRY+FX:EURTRY)/2"),
 "y_xau": ("GC=F*TRY=X", "Gram altın TL (ons ~18 UTC x kur ~24 UTC; zaman uyumsuz)", "FX_IDC:XAUTRYG"),
 "v_usd": ("VIOP F_USDTRY (ön ay)", "USDTRY vadeli uzlaşma (~15:00 UTC, BIST kapanışıyla hizalı)", "BIST:USDTRY1!"),
 "v_eur": ("VIOP F_EURTRY (ön ay)", "EURTRY vadeli uzlaşma (~15:00 UTC)", "BIST:EURTRY1!"),
 "v_bsk": ("VIOP sepet", "Sepet kur VİOP (0,5 USD + 0,5 EUR vadeli)", "(BIST:USDTRY1!+BIST:EURTRY1!)/2"),
 "v_xau": ("VIOP F_XAUTRYM (ön ay)", "Gram altın TL vadeli uzlaşma (~15:00 UTC)", "BIST:XAUTRY1!"),
 "d_ir12": ("VIOP USDTRY 1-2 ay yayılımı + ^IRX", "Zımni TL faizi değişimi (yp; VİOP ileri kur)", "BIST:USDTRY2!/BIST:USDTRY1! (yayılım; faiz değil)"),
 "d_ir13": ("VIOP USDTRY 1-3 ay yayılımı + ^IRX", "Zımni TL faizi (1-3 ay) değişimi", "BIST:USDTRY3!/BIST:USDTRY1! (?)"),
 "d_dibs2": ("BAP gösterge-benzeri 2y DİBS", "2 yıllık DİBS bileşik getiri değişimi (BAP kapanış ~14:30 UTC)", "TVC:TR02Y"),
 "d_dibs5": ("BAP 5y DİBS", "5 yıllık DİBS getiri değişimi", "TVC:TR05Y"),
 "d_dibs10": ("BAP 10y DİBS", "10 yıllık DİBS getiri değişimi", "TVC:TR10Y"),
 "d_dibs1": ("BAP 1y DİBS", "~1 yıllık DİBS getiri değişimi", "TVC:TR01Y (?)"),
 "d_tlref": ("BIST TLREF", "TLREF gecelik faiz değişimi", "? (TradingView'da TLREF bulunamadı)"),
 "tur": ("TUR", "iShares MSCI Turkey (USD, ~20/21 UTC)", "NASDAQ:TUR"),
 "emb": ("EMB", "JPM USD EM tahvil ETF (CDS vekili)", "NASDAQ:EMB"),
 "tur_eem": ("TUR-EEM", "Türkiye'ye özgü risk primi vekili (TUR − EEM)", "NASDAQ:TUR/AMEX:EEM"),
 "h15_usd": ("TRY=X h1 @15:00", "USDTRY 15:00 UTC hizalı (2024+)", "FX:USDTRY (1s grafik 18:00 TSİ)"),
 "h15_xau": ("GC=F*TRY=X h1 @15:00", "Gram altın 15:00 UTC hizalı (2024-06+)", "FX_IDC:XAUTRYG"),
 "h15_bsk": ("sepet h1 @15:00", "Sepet kur 15:00 UTC hizalı", "(FX:USDTRY+FX:EURTRY)/2"),
 "n_usd": ("TRY=X h1 gece", "USDTRY gece hareketi 15:00 UTC(t-1)->06:00 UTC(t)", "FX:USDTRY"),
 "n_eur": ("EURTRY=X h1 gece", "EURTRY gece hareketi", "FX:EURTRY"), "n_bsk": ("sepet gece", "Sepet gece hareketi", "(FX:USDTRY+FX:EURTRY)/2"),
 "n_xau": ("GC=F*TRY=X h1 gece", "Gram altın gece hareketi 15:00->06:00 UTC", "FX_IDC:XAUTRYG"), "n_gc": ("GC=F h1 gece", "Ons altın gece hareketi", "COMEX:GC1!"),
}
def tv_stock(s): return "BIST:" + s
def p_from_t(t): return 2 * (1 - stats.norm.cdf(np.abs(t)))
def p_from_r(r, n): return p_from_t(np.arctanh(np.clip(r, -0.999, 0.999)) * np.sqrt(np.maximum(n - 4, 1)))
scans = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(M.RES + "/scan_*.csv"))], ignore_index=True)
scans = scans.drop_duplicates(["var", "stock"], keep="last")
scans = scans[scans["stock"] != "XHOLD"]
# FDR aileleri (tüm değişkenler x hedefler birlikte)
fam = {}
scans["p_pc"] = p_from_r(scans["pc"], scans["n"]); scans["p_c"] = p_from_r(scans["corr_full"], scans["n"])
scans["p_sync"] = scans["p_pc"].where(scans["pc"].notna(), scans["p_c"])
for col, tcol in [("p_gap", "L_gap_t"), ("p_intra", "L_intra_t"), ("p_intraX", "L_intraX_t"), ("p_md", "L_md_t"), ("p_rev", "R_t")]:
    scans[col] = p_from_t(scans[tcol])
for col in ["p_sync", "p_gap", "p_intra", "p_intraX", "p_md", "p_rev"]:
    rej, padj = ll.fdr(scans[col].values); scans[col.replace("p_", "fdr_")] = rej; fam[col] = (int(np.isfinite(scans[col]).sum()), int(rej.sum()))
json.dump(fam, open(M.RES + "/fdr_families.json", "w"), indent=1)
print("FDR aileleri (test sayısı, geçen):", fam)
scans.to_csv(M.RES + "/scan_all_fdr.csv", index=False)
rows = []
def conf_sync(r):
    big = (abs(r.get("pc", np.nan)) >= 0.15) or (abs(r["corr_full"]) >= 0.30 and pd.isna(r.get("pc")))
    same = (np.sign(r.get("pc_is", np.nan)) == np.sign(r.get("pc_oos", np.nan))) and abs(r.get("pc_oos", 0)) >= 0.05 and abs(r.get("pc_is", 0)) >= 0.05
    yr = r.get("yr_same_pc", 0) >= 0.75
    if big and same and yr and r["fdr_sync"]: return "YÜKSEK"
    if r["fdr_sync"] and abs(r.get("pc", 0)) >= 0.07 and np.sign(r.get("pc_oos", 0)) == np.sign(r.get("pc", 0)): return "ORTA"
    if r["fdr_sync"] or abs(r.get("pc", 0)) >= 0.05: return "DÜŞÜK"
    return "ÇOK DÜŞÜK"
def conf_lead(t, tis, toos, fdr, n):
    if abs(t) >= 3 and np.sign(tis) == np.sign(toos) == np.sign(t) and abs(tis) >= 2 and abs(toos) >= 2 and fdr: return "YÜKSEK"
    if fdr and np.sign(toos) == np.sign(t) and abs(t) >= 2.5: return "ORTA"
    if abs(t) >= 2: return "DÜŞÜK"
    return "ÇOK DÜŞÜK"
MECH = {"B": "TL zayıflığı = TR risk primi ↑ / fonlama maliyeti ↑ → bankalar piyasanın altında", "E": "döviz geliri / ihracat: TL değer kaybı TL bazlı değeri korur (doğal hedge)",
        "D": "TL gelirli yurt içi iş: kur şoku talep/maliyet üzerinden olumsuz", "I": "ithal girdi / döviz borcu", "H": "holding (banka iştiraki + sanayi karışık)"}
GROUP = __import__("importlib").import_module("07_usd_real".replace(".py", "")) if False else None
from importlib import util as _u
spec = _u.spec_from_file_location("ur", M.D + "/07_usd_real.py")
G = {}
src = open(M.D + "/07_usd_real.py").read(); i = src.find("GROUP = {"); j = src.find("}", i); exec(src[i:j + 1], G); GROUP = G["GROUP"]
def mech(var, s):
    g = GROUP.get(s, "IDX")
    if var.startswith(("y_usd", "v_usd", "h15_usd", "y_bsk", "v_bsk", "y_eur", "v_eur", "n_usd", "n_bsk", "n_eur")): return MECH.get(g, "endeks: kur ↔ risk primi")
    if "xau" in var or var == "n_gc": return "altın üreticisi (TRALT/TRMET) doğrudan; diğerleri TL bileşeni / risk-off" if s in ("TRALT", "TRMET") else "gram altın = ons x kur; TL bileşeni ve risk-off ikamesi"
    if var.startswith(("d_ir", "d_dibs", "d_tlref")): return "TL faizi ↑ → banka fonlama/menkul değer kaybı, GYO/holding iskonto oranı ↑"
    if var in ("tur", "tur_eem", "emb"): return "yabancı risk iştahı / Türkiye risk primi vekili (TUR hisseleri içerir: mekanik)"
    return ""
for _, r in scans.iterrows():
    v, s = r["var"], r["stock"]
    if v not in DRV: continue
    dy, dd, tv = DRV[v]
    base = dict(stock=s, driver_yahoo=dy, driver_desc=dd, tv_ticker=tv, corr_full=r["corr_full"], corr_3y=r["corr_3y"], corr_1y=r["corr_1y"], pcorr_xu100=r.get("pc"), n=r["n"])
    # senkron
    o = dict(base, relation="sync", lag=0, beta=r.get("beta_x") if pd.notna(r.get("beta_x")) else r.get("beta"), t_stat=r.get("t_beta_x") if pd.notna(r.get("t_beta_x")) else r.get("t_beta"),
             gap_corr=np.nan, intra_corr=np.nan, is_oos=f"pc IS {r.get('pc_is', np.nan):.2f} / OOS {r.get('pc_oos', np.nan):.2f}; yıl-işaret {r.get('yr_same_pc', np.nan):.2f}",
             confidence=conf_sync(r), mechanism=mech(v, s), notes=f"FDR(senkron)={'evet' if r['fdr_sync'] else 'hayır'}; pc 3y {r.get('pc_3y', np.nan):.2f} 1y {r.get('pc_1y', np.nan):.2f}; beta=XU100 kontrollü")
    rows.append(o)
    # öncülük gap (işlenemez) / intra (işlenebilir) / intraX
    tim = "değişken ~24:00 UTC biter: t-1 değeri BIST kapanışından sonraki saatleri içerir (gap = eşzamansız kapanış)" if v.startswith(("y_", "tur", "emb")) else "değişken BIST kapanışıyla hizalı (~15:00 UTC): t-1 -> t gerçek öncülük"
    for rel, tcol, ccol, fcol in [("lead_gap", "L_gap_t", "L_gap_corr", "fdr_gap"), ("lead_intra", "L_intra_t", "L_intra_corr", "fdr_intra")]:
        t = r.get(tcol)
        if pd.isna(t): continue
        if abs(t) < 2 and not (s in ("XU100", "XBANK", "TRALT") and v in ("y_usd", "v_usd", "y_xau", "v_xau", "d_ir12", "d_dibs2")): continue
        o = dict(base, relation=rel, lag=1, beta=r.get(tcol.replace("_t", "_b")), t_stat=t, gap_corr=r.get("L_gap_corr"), intra_corr=r.get("L_intra_corr"),
                 is_oos=f"t IS {r.get(tcol + '_is', np.nan):.2f} / OOS {r.get(tcol + '_oos', np.nan):.2f}",
                 confidence=conf_lead(t, r.get(tcol + "_is", 0), r.get(tcol + "_oos", 0), r[fcol], r["n"]) if rel == "lead_intra" else ("ORTA (işlenemez)" if (abs(t) >= 3 and r[fcol]) else "DÜŞÜK (işlenemez)"),
                 mechanism=mech(v, s), notes=f"{tim}; kontroller hisse_(t-1), XU100_(t-1); FDR={'evet' if r[fcol] else 'hayır'}; hisseye özgü intraX t={r.get('L_intraX_t', np.nan):.2f}")
        rows.append(o)
    if pd.notna(r.get("L_md_t")) and abs(r["L_md_t"]) >= 2.5:
        rows.append(dict(base, relation="lead_multiday", lag="1->t+1..t+4", beta=r.get("L_md_b"), t_stat=r["L_md_t"], gap_corr=np.nan, intra_corr=np.nan, is_oos="", confidence="DÜŞÜK" if r["fdr_md"] else "ÇOK DÜŞÜK",
                         mechanism=mech(v, s), notes="t+1..t+4 kümülatif cc (t günü hariç), NW 8 gecikme"))
    if pd.notna(r.get("R_t")) and (abs(r["R_t"]) >= 2 or s in ("XU100", "XBANK")):
        rows.append(dict(base, relation="reverse", lag=-1, beta=r.get("R_b"), t_stat=r["R_t"], gap_corr=np.nan, intra_corr=np.nan,
                         is_oos=f"t IS {r.get('R_t_is', np.nan):.2f} / OOS {r.get('R_t_oos', np.nan):.2f}",
                         confidence=("ORTA" if (r["fdr_rev"] and np.sign(r.get("R_t_is", 0)) == np.sign(r.get("R_t_oos", 0))) else ("DÜŞÜK" if abs(r["R_t"]) >= 2 else "ÇOK DÜŞÜK")),
                         mechanism="BIST hissesi/endeksi -> ertesi gün değişken (BIST kur/faizi öngörüyor mu?)", notes=f"değişken_t ~ hisse_(t-1) + değişken_(t-1) + XU100_(t-1); FDR={'evet' if r['fdr_rev'] else 'hayır'}"))
F = pd.DataFrame(rows)
# gece hareketleri
try:
    N = pd.read_csv(M.RES + "/night.csv")
    N["p"] = p_from_t(N["intra_t"]); rej, _ = ll.fdr(N["p"].values); N["fdr"] = rej
    N["pg"] = p_from_t(N["gap_t"]); rejg, _ = ll.fdr(N["pg"].values); N["fdrg"] = rejg
    for _, r in N.iterrows():
        if r["stock"] == "XHOLD" or pd.isna(r.get("intra_t")): continue
        dy, dd, tv = DRV[r["var"]]
        if abs(r["gap_t"]) >= 2.5 or r["stock"] in ("TRALT", "TRMET", "XU100", "XBANK"):
            F.loc[len(F)] = dict(stock=r["stock"], driver_yahoo=dy, driver_desc=dd, tv_ticker=tv, relation="lead_gap", lag="gece(0)", corr_full=r["gap_corr"], t_stat=r["gap_t"], gap_corr=r["gap_corr"], intra_corr=r["intra_corr"], n=r["n"],
                                 is_oos=f"t 1.yarı {r['gap_t_h1']:.2f} / 2.yarı {r['gap_t_h2']:.2f} (bölünme 2025-06)", confidence="ORTA (işlenemez)" if r["fdrg"] else "DÜŞÜK (işlenemez)",
                                 mechanism=mech(r["var"], r["stock"]), notes=f"gece hareketi açılışta fiyatlanır; gapX (XU100 gap kontrollü) t={r.get('gapX_t', np.nan):.2f}; 2024+ saatlik")
        if abs(r["intra_t"]) >= 2 or r["stock"] in ("TRALT", "TRMET", "XU100", "XBANK"):
            F.loc[len(F)] = dict(stock=r["stock"], driver_yahoo=dy, driver_desc=dd, tv_ticker=tv, relation="lead_intra", lag="gece(0)", corr_full=r["intra_corr"], t_stat=r["intra_t"], gap_corr=r["gap_corr"], intra_corr=r["intra_corr"], n=r["n"],
                                 is_oos=f"t 1.yarı {r['intra_t_h1']:.2f} / 2.yarı {r['intra_t_h2']:.2f}", confidence=("DÜŞÜK" if (abs(r["intra_t"]) >= 2 and np.sign(r["intra_t_h1"]) == np.sign(r["intra_t_h2"])) else "ÇOK DÜŞÜK"),
                                 mechanism=mech(r["var"], r["stock"]), notes=f"sinyal 06:00 UTC'de bilinir, açılıştan (07:00) önce -> işlenebilir; FDR={'evet' if r['fdr'] else 'hayır'} ({len(N)} test); intraX t={r.get('intraX_t', np.nan):.2f}")
except Exception as e: print("night", e)
# saatlik
try:
    H = pd.read_csv(M.RES + "/hourly_ll.csv"); H["p"] = p_from_t(H["t"]); rej, _ = ll.fdr(H["p"].values); H["fdr"] = rej
    hv = {"TRY=X": "h15_usd", "EURTRY=X": "n_eur", "BSK": "h15_bsk", "XAUTRY": "h15_xau", "GC=F": "n_gc"}
    for _, r in H.iterrows():
        if r["j"] < 2 and not (r["j"] == -1): continue
        if abs(r["t"]) < 2.5: continue
        dy, dd, tv = DRV[hv[r["driver"]]]
        F.loc[len(F)] = dict(stock=r["stock"], driver_yahoo=r["driver"] + " (h1)", driver_desc=f"{r['driver']} saatlik; j={r['j']} (j>=2: sürücü >=30 dk önde; j=-1: BIST önde)", tv_ticker=tv, relation="lead_hourly" if r["j"] >= 2 else "reverse",
                             lag=f"{r['j']}h", corr_full=r["corr"], t_stat=r["t"], n=r["n"], is_oos="", confidence="DÜŞÜK" if r["fdr"] else "ÇOK DÜŞÜK",
                             mechanism="saatlik bilgi yayılımı", notes=f"FDR={'evet' if r['fdr'] else 'hayır'} ({len(H)} test); XU100 kontrollü t={r['tX']:.2f}; 2024+ (altın 2024-06+, TRALT 2025-11+)")
except Exception as e: print("hourly", e)
# USD geçişkenliği
U = pd.read_csv(M.RES + "/usd_real.csv")
for _, r in U.iterrows():
    s = r["stock"]
    F.loc[len(F)] = dict(stock=s, driver_yahoo="TRY=X (haftalık)", driver_desc="Kur geçişkenliği: haftalık r_TL ~ r_USDTRY (b=1 'dolar hissesi', b<0 TL riski)", tv_ticker="FX:USDTRY", relation="usd_passthrough", lag="0 (haftalık)",
                         beta=r.get("pt_w_full"), t_stat=r.get("pt_w_full_t"), corr_full=np.nan, n=r["n"],
                         is_oos=f"b IS {r.get('pt_w_is', np.nan):.2f} / OOS {r.get('pt_w_oos', np.nan):.2f}; aylık {r.get('pt_m_full', np.nan):.2f}; XU100'e göreli {r.get('rel_w_full', np.nan):.2f} (t {r.get('rel_w_full_t', np.nan):.1f})",
                         confidence=("ORTA" if abs(r.get("rel_w_full_t", 0)) >= 3 else ("DÜŞÜK" if abs(r.get("rel_w_full_t", 0)) >= 2 else "ÇOK DÜŞÜK")),
                         mechanism=MECH.get(r["group"], "endeks"), notes=f"grup={r['group']}; yıllık ort. log getiri 2014-26: TL {r['ann_tl_full']:.1f}% / USD {r['ann_usd_full']:.1f}% / reel {r['ann_real_full']:.1f}%; USD bazlı beta (XU100-USD kontrollü, haftalık) {r.get('usdb_w_full', np.nan):.2f} (t {r.get('usdb_w_full_t', np.nan):.1f})")
# rejim
Rg = pd.read_csv(M.RES + "/regime_beta.csv")
for s in Rg["stock"].unique():
    x = Rg[Rg.stock == s].set_index("regime")
    if not {"vol_H", "vol_L"} <= set(x.index): continue
    F.loc[len(F)] = dict(stock=s, driver_yahoo="TRY=X", driver_desc="USDTRY senkron kısmi korelasyon, kur-vol rejimine göre (20g vol, genişleyen terciller)", tv_ticker="FX:USDTRY", relation="regime", lag=0,
                         pcorr_xu100=x.loc["vol_H", "pc"], beta=x.loc["vol_H", "beta_x"], t_stat=x.loc["vol_H", "t"], n=x.loc["vol_H", "n"],
                         is_oos=f"pc yüksek-vol {x.loc['vol_H','pc']:.2f} / orta {x.loc['vol_M','pc'] if 'vol_M' in x.index else np.nan:.2f} / düşük {x.loc['vol_L','pc']:.2f}; carry23-25 {x.loc['carry 2023H2-2025Q1','pc'] if 'carry 2023H2-2025Q1' in x.index else np.nan:.2f}; 2025-03 sonrası {x.loc['2025-03 sonrası','pc'] if '2025-03 sonrası' in x.index else np.nan:.2f}",
                         confidence="ORTA" if (abs(x.loc["vol_H", "pc"]) >= 0.15 and abs(x.loc["vol_H", "pc"]) > 2 * abs(x.loc["vol_L", "pc"])) else "DÜŞÜK",
                         mechanism=MECH.get(GROUP.get(s, "IDX"), "endeks"), notes="beta/t yüksek-vol rejimi; rejim eşikleri t-1'e kadar veriyle")
# backtestler
B = pd.read_csv(M.RES + "/bt.csv")
for _, r in B[B["cost_bps"].isin([8, 16])].iterrows():
    F.loc[len(F)] = dict(stock=r["bt"].split("->")[-1].split(" ")[0], driver_yahoo=r["bt"].split("->")[0], driver_desc=r["bt"], tv_ticker="", relation="backtest", lag=1,
                         bt_oos_sharpe=r["OOS_sharpe"], bt_oos_mean_bps=r["OOS_mean_bps"], t_stat=r["OOS_t"], n=r["OOS_n"],
                         is_oos=f"IS {r['IS_mean_bps']:.1f} bps (t {r['IS_t']:.2f}, n {r['IS_n']}) / OOS {r['OOS_mean_bps']:.1f} bps (t {r['OOS_t']:.2f}, n {r['OOS_n']}); brüt OOS {r['OOS_gross_bps']:.1f}",
                         confidence=("ORTA" if (r["OOS_t"] >= 2 and r["IS_t"] >= 1.5) else ("DÜŞÜK" if (r["OOS_mean_bps"] > 0 and r["IS_mean_bps"] > 0) else "ÇOK DÜŞÜK")),
                         mechanism="", notes=f"maliyet {r['cost_bps']} bps; eşik {r['thr']}; yıllar {r['by_year']}")
# elle düzeltme: otomatik YÜKSEK çıkan gün-içi öncülükler backtestte doğrulanmadı / yurt dışı sürücü (TUR) -> ORTA
m = (F["relation"] == "lead_intra") & (F["confidence"] == "YÜKSEK")
F.loc[m, "notes"] = F.loc[m, "notes"].astype(str) + " | ELLE ORTA'ya indirildi: regresyon t>=3 ve IS/OOS aynı işaret, ama işaret-tabanlı backtest maliyet sonrası anlamsız (BT5 / gap-fade özel hali; TUR yurt dışı ETF)"
F.loc[m, "confidence"] = "ORTA"
cols = ["stock", "driver_yahoo", "driver_desc", "tv_ticker", "relation", "lag", "corr_full", "corr_3y", "corr_1y", "pcorr_xu100", "beta", "t_stat", "gap_corr", "intra_corr", "is_oos", "bt_oos_sharpe", "bt_oos_mean_bps", "n", "confidence", "mechanism", "notes"]
for c in cols:
    if c not in F: F[c] = np.nan
F = F[cols]
for c in ["corr_full", "corr_3y", "corr_1y", "pcorr_xu100", "beta", "t_stat", "gap_corr", "intra_corr", "bt_oos_sharpe", "bt_oos_mean_bps"]: F[c] = pd.to_numeric(F[c], errors="coerce").round(4)
F.to_csv(OUT, index=False); print(F.shape); print(F["relation"].value_counts()); print(F["confidence"].value_counts())
