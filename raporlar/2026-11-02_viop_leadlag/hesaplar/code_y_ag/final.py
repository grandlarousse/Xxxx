"""Çıktıları derle: out/y_varyans_ayristirma.csv ve out/f_y_ag.csv (ana brifing sütunları)."""
import numpy as np, pandas as pd
from common import *
COLS = ["stock", "driver_yahoo", "driver_desc", "tv_ticker", "relation", "lag", "corr_full", "corr_3y", "corr_1y", "pcorr_xu100", "beta", "t_stat",
        "gap_corr", "intra_corr", "is_oos", "bt_oos_sharpe", "bt_oos_mean_bps", "n", "confidence", "mechanism", "notes"]
GL_TV = "CME_MINI:ES1! | AMEX:EEM | TVC:SX5E | CBOE:VIX | TVC:DXY | ICEEUR:BRN1! | COMEX:GC1! | TVC:US10Y"
rows = []
def add(**k): rows.append({c: k.get(c, np.nan) for c in COLS})

# ---------- 1) varyans ayrıştırması ----------
V = pd.read_csv(os.path.join(CACHE, "vardec_all.csv")); S = pd.read_csv(os.path.join(CACHE, "vardec_sync_compare.csv"))
S2 = S.rename(columns={"align": "spec"}); S2["spec"] = "sync15UTC_" + S2["spec"]; S2["period"] = "2024-06..2026-10"
VV = pd.concat([V, S2], ignore_index=True)
VV["rank_global"] = VV.groupby(["period", "spec"])["sh_global"].rank(ascending=False)
VV["yerli_pay"] = VV[["sh_trmakro", "sh_piyasa", "sh_sektor"]].sum(axis=1, min_count=1)
VV.round(5).to_csv(os.path.join(OUT, "y_varyans_ayristirma.csv"), index=False)
b = V[(V.spec == "base") & (V.stock != "XU100")].pivot_table(index="stock", columns="period",
     values=["sh_global", "sh_trmakro", "sh_piyasa", "sh_sektor", "alone_global", "uniq_global", "alone_trmakro", "uniq_trmakro",
             "alone_piyasa", "uniq_piyasa", "alone_sektor", "uniq_sektor", "n", "idio"])
syn = S[S["align"] == "C"].set_index("stock")
for st in STOCKS:
    per_s = lambda m: "; ".join(f"{p}={100*b.loc[st, (m, p)]:.1f}%" for p in ["2014-17", "2018-20", "2021-23", "2024-26", "son1y"] if pd.notna(b.loc[st, (m, p)]))
    n = int(b.loc[st, ("n", "tam")]); short = st in ("ASTOR", "SOKM", "ENJSA")
    peers = [p for p in CL[SECT[st]] if p != st]
    spec = [("global", "KÜRESEL-8 (ES=F,EEM,^STOXX50E,^VIX,DX-Y.NYB,BZ=F,GC=F,^TNX; t ve t-1)", "Küresel faktör bloğu", GL_TV,
             "Küresel risk iştahı/emtia/dolar; BIST'e çoğunlukla XU100 üzerinden geçer (özgün pay küçük)"),
            ("trmakro", "TRY=X (t,t-1) + TUR (t-1)", "Türkiye makro: USD/TRY + NY'de BIST kapanışı sonrası Türkiye ETF'i", "FX:USDTRY | NASDAQ:TUR",
             "Kur/ülke riski; günlük FX kapanışı (24:00 UTC) BIST'le eşzamansız -> pay düşük ölçülür (15:00 UTC senkron ölçümde ~10 kat)"),
            ("piyasa", "XU100.IS", "BIST 100 (hisseyi içerir: mekanik içerme)", "BIST:XU100", "Ortak yerli piyasa faktörü"),
            ("sektor", "EW akran: " + ",".join(peers), f"Sektör/küme akranları ({SECT[st]}), hisse hariç eşit ağırlık", " | ".join("BIST:" + p for p in peers[:6]),
             "Sektör/şirket grubu ortak şoku")]
    for g, dy_, desc, tv, mech in spec:
        full = b.loc[st, (f"sh_{g}", "tam")]
        if g == "global": conf = "YÜKSEK" if not short else "ORTA"
        elif g == "trmakro": conf = "ORTA"
        else: conf = "YÜKSEK" if not short else "ORTA"
        note = (f"Shapley (düzeltilmiş R²) payı; dönemler: {per_s('sh_'+g)}. Tek başına (üst sınır) tam={100*b.loc[st, ('alone_'+g, 'tam')]:.1f}%, "
                f"özgün (alt sınır) tam={100*b.loc[st, ('uniq_'+g, 'tam')]:.1f}%. Hisseye özgü (idio) tam={100*b.loc[st, ('idio', 'tam')]:.1f}%. "
                f"SÜTUN NOTU: corr_full/corr_3y/corr_1y = Shapley payı (tam / 2024-26 / son 1y); pcorr_xu100 = özgün pay; beta = tek başına pay.")
        if g in ("global", "trmakro") and st in syn.index:
            note += f" 15:00 UTC senkron sürücülerle (2024-06+) Shapley={100*syn.loc[st, 'sh_'+g]:.1f}%."
        add(stock=st, driver_yahoo=dy_, driver_desc=desc, tv_ticker=tv, relation="variance_share", lag="0 (+t-1 Dimson)",
            corr_full=round(full, 4), corr_3y=round(b.loc[st, (f"sh_{g}", "2024-26")], 4), corr_1y=round(b.loc[st, (f"sh_{g}", "son1y")], 4),
            pcorr_xu100=round(b.loc[st, (f"uniq_{g}", "tam")], 4), beta=round(b.loc[st, (f"alone_{g}", "tam")], 4), n=n, confidence=conf,
            mechanism=mech, notes=note, is_oos=f"2014-17={b.loc[st, ('sh_'+g, '2014-17')]:.3f}; 2021-23={b.loc[st, ('sh_'+g, '2021-23')]:.3f}")
x = V[(V.stock == "XU100")].set_index("period")
add(stock="XU100", driver_yahoo="KÜRESEL-8 (t,t-1)", driver_desc="XU100'ün küresel faktör payı", tv_ticker=GL_TV, relation="variance_share", lag="0 (+t-1)",
    corr_full=round(x.loc["tam", "sh_global"], 4), corr_3y=round(x.loc["2024-26", "sh_global"], 4), corr_1y=round(x.loc["son1y", "sh_global"], 4), n=int(x.loc["tam", "n"]),
    confidence="YÜKSEK", mechanism="Küresel risk iştahı", notes="Shapley payı dönemler: " + "; ".join(f"{p}={100*x.loc[p,'sh_global']:.1f}%" for p in ["2014-17", "2018-20", "2021-23", "2024-26", "son1y", "2026oca-agu", "fonkrizi"]) + " (fonkrizi: kompakt spesifikasyon n=43)")
add(stock="XU100", driver_yahoo="TRY=X (t,t-1) + TUR (t-1)", driver_desc="XU100'ün TR makro payı", tv_ticker="FX:USDTRY | NASDAQ:TUR", relation="variance_share", lag="0 (+t-1)",
    corr_full=round(x.loc["tam", "sh_trmakro"], 4), corr_3y=round(x.loc["2024-26", "sh_trmakro"], 4), corr_1y=round(x.loc["son1y", "sh_trmakro"], 4), n=int(x.loc["tam", "n"]),
    confidence="ORTA", mechanism="Kur/ülke riski; 2021 sonrası yönetilen kur ile bilgi içeriği azaldı",
    notes="Dönemler: " + "; ".join(f"{p}={100*x.loc[p,'sh_trmakro']:.1f}%" for p in ["2014-17", "2018-20", "2021-23", "2024-26", "son1y"]) +
          f". 15:00 UTC senkron USDTRY ile (2024-06+): {100*syn.loc['XU100','sh_trmakro']:.1f}% (günlük kapanışla {100*S[(S["align"]=="A")&(S.stock=="XU100")]['sh_trmakro'].iloc[0]:.1f}%)")

# ---------- 2) DY spillover ----------
N = pd.read_csv(os.path.join(CACHE, "dy_static_nodes.csv"))
pa = N[N["align"] == "A"].pivot_table(index="node", columns="period", values=["net", "to", "from"])
pb = N[N["align"] == "B"].pivot_table(index="node", columns="period", values="net")
for st in STOCKS:
    if st not in pa.index: continue
    full = pa.loc[st, ("net", "tam")] if pd.notna(pa.loc[st, ("net", "tam")]) else pa.loc[st, ("net", "2024-26")]
    add(stock=st, driver_yahoo="AG-58 (47 hisse+XU100+10 sürücü)", driver_desc="Diebold–Yilmaz net yönlü spillover (to−from), GFEVD H=10, VAR(1)", tv_ticker="BIST:" + st,
        relation="spillover_net", lag="VAR(1), H=10", corr_full=round(full, 4), corr_3y=round(pa.loc[st, ("net", "2024-26")], 4), corr_1y=round(pa.loc[st, ("net", "son1y")], 4),
        beta=round(pa.loc[st, ("to", "tam")], 4) if pd.notna(pa.loc[st, ("to", "tam")]) else np.nan, t_stat=np.nan,
        is_oos=f"2014-17={pa.loc[st, ('net','2014-17')]:.3f}; 2021-23={pa.loc[st, ('net','2021-23')]:.3f}; B-hizalı tam={pb.loc[st,'tam'] if st in pb.index else np.nan:.3f}",
        confidence="DÜŞÜK", mechanism="Günlük veride GFEVD net değeri ≈ eşzamanlı korelasyon merkeziliği (H=1 ile H=10 sıralaması Spearman 0,99) -> YÖN/NEDENSELLİK DEĞİL",
        notes="SÜTUN NOTU: corr_full/3y/1y = net spillover (pay, 1=%100; tam/2024-26/son1y); beta = 'to' toplamı. Pozitif = net yayıcı (merkezi).")
S1 = pd.read_csv(os.path.join(CACHE, "dy2_static.csv"))
for node, yah in [("ES", "ES=F"), ("EEM", "EEM"), ("VIX", "^VIX"), ("SX5E", "^STOXX50E"), ("USDTRY", "TRY=X"), ("TUR", "TUR"), ("BRENT", "BZ=F"), ("ALTIN", "GC=F"), ("DXY", "DX-Y.NYB"), ("US10Y", "^TNX")]:
    g = S1[(S1.net == "S1") & (S1.node == node)].set_index(["align", "period"])
    c = S1[(S1.net == "S1C") & (S1.node == node)].set_index("align")
    nt = lambda al, p: g.loc[(al, p), "node_to_xu"] if (al, p) in g.index else np.nan
    cC = f"; C(15:00 UTC, 2024-06+)={100*c.loc['C','node_to_xu']:.1f}% (A={100*c.loc['A','node_to_xu']:.1f}%, B={100*c.loc['B','node_to_xu']:.1f}%)" if "C" in c.index else ""
    add(stock="XU100", driver_yahoo=yah, driver_desc=GL_NAME.get(yah, node) + " -> XU100 FEV payı (11 düğümlü ağ)", tv_ticker=TV.get(yah, "?"), relation="spillover_pair",
        lag="VAR(1), H=10", corr_full=round(nt("A", "tam"), 4), corr_3y=round(nt("A", "2024-26"), 4), corr_1y=round(nt("A", "son1y"), 4),
        pcorr_xu100=round(nt("B", "tam"), 4), beta=round(g.loc[("A", "tam"), "netsp"], 4),
        is_oos=f"fonkrizi A={nt('A','fonkrizi'):.3f}; 2026oca-agu A={nt('A','2026oca-agu'):.3f}" + cC,
        confidence="ORTA" if node in ("ES", "EEM", "VIX") else ("DÜŞÜK" if node != "TUR" else "DÜŞÜK (ayna)"),
        mechanism="Küresel/yurt içi sürücünün XU100 tahmin hata varyansına katkısı (H=10)",
        notes="SÜTUN NOTU: corr_* = XU100 FEV payı (A hizalama; tam/2024-26/son1y); pcorr_xu100 = aynı pay B (ABD t+1 hizalı); beta = düğümün net spillover'ı (A, tam). TUR A'da BIST seansını içerdiği için 'ayna'.")

# ---------- 3) Granger ----------
G = pd.read_csv(os.path.join(CACHE, "granger_all.csv.gz")); G = G[(G["shift"] == 0)]
GA = G[(G["align"] == "A") & (G.p == 1)]
piv = GA.pivot_table(index=["src", "tgt"], columns=["period", "kind"], values=["t1", "pc1", "q", "pval"])
sig = GA[(GA.period == "tam") & GA.sig & GA.kind.isin(["cc", "intra"])]
sig2 = G[(G["align"] == "A") & (G.p == 2) & (G.period == "tam") & G.sig & (G.kind == "intra")]
inv = {v: k for k, v in {"ES": "ES=F", "EEM": "EEM", "SX5E": "^STOXX50E", "VIX": "^VIX", "DXY": "DX-Y.NYB", "BRENT": "BZ=F", "ALTIN": "GC=F", "US10Y": "^TNX", "USDTRY": "TRY=X", "TUR": "TUR"}.items()}
def yah(s): return {"ES": "ES=F", "EEM": "EEM", "SX5E": "^STOXX50E", "VIX": "^VIX", "DXY": "DX-Y.NYB", "BRENT": "BZ=F", "ALTIN": "GC=F", "US10Y": "^TNX", "USDTRY": "TRY=X", "TUR": "TUR", "XU100": "XU100.IS"}.get(s, s + ".IS")
for _, r in pd.concat([sig, sig2]).iterrows():
    k = (r.src, r.tgt); g_ = lambda m, p, kd: piv.loc[k, (m, p, kd)] if (m, p, kd) in piv.columns and k in piv.index else np.nan
    us = yah(r.src) in US_CLOSE
    isv, oos = g_("t1", "IS", r.kind), g_("t1", "OOS", r.kind)
    stable = pd.notna(isv) and pd.notna(oos) and np.sign(isv) == np.sign(oos) and abs(oos) >= 2 and abs(isv) >= 2
    if r.kind == "cc" and us: conf = "YÜKSEK (açılış gap'inde fiyatlanır; işlenemez)" if stable else "ORTA (gap kanalı; işlenemez)"
    elif r.kind == "cc": conf = "ORTA" if stable else "DÜŞÜK"
    else: conf = "DÜŞÜK" if stable else "ÇOK DÜŞÜK"
    add(stock=r.tgt, driver_yahoo=yah(r.src), driver_desc=GL_NAME.get(yah(r.src), r.src), tv_ticker=TV.get(yah(r.src), "BIST:" + r.src), relation="granger",
        lag=f"p={int(r.p)} ({r.kind})", corr_full=round(r.pc1, 4), t_stat=round(r.t1, 2), gap_corr=round(g_("pc1", "tam", "gap"), 4), intra_corr=round(g_("pc1", "tam", "intra"), 4),
        is_oos=f"IS t={isv:.2f}; OOS t={oos:.2f}", n=int(r.n), confidence=conf,
        mechanism=("ABD kapanışı BIST kapanışından sonra -> eşzamansız kapanış (gap)" if us else "Yurt içi öncülük adayı (kendi lag + XU100 lag kontrollü)"),
        notes=f"HC1 Wald, BH q={r.q:.3f} (aile: {int(r.p)} lag × tam dönem × {r.kind}, 2.679 test). corr_full = kısmi korelasyon; gap/intra_corr = aynı kaynağın gap ve gün-içi hedefli kısmi korelasyonu.")
gap = GA[(GA.period == "tam") & (GA.kind == "gap") & GA.sig].groupby("src").agg(n=("tgt", "size"), t=("t1", "median"), pc=("pc1", "median"))
for src, r in gap.sort_values("n", ascending=False).head(12).iterrows():
    us = yah(src) in US_CLOSE
    add(stock=f"TÜMÜ ({int(r.n)}/47 hedef)", driver_yahoo=yah(src), driver_desc=GL_NAME.get(yah(src), src), tv_ticker=TV.get(yah(src), "BIST:" + src), relation="granger",
        lag="p=1 (gap)", corr_full=round(r.pc, 4), t_stat=round(r.t, 2), n=np.nan,
        confidence="YÜKSEK (açılış gap'inde fiyatlanır; işlenemez)" if us and r.n >= 20 else ("ORTA" if us else "DÜŞÜK"),
        mechanism="Eşzamansız kapanış: sürücü_{t-1} BIST_t açılışında fiyatlanır" if us else "Yurt içi lag -> gap (bayat fiyat/ertesi gün düzeltme olabilir)",
        notes="BH q<0,05 geçen hedef sayısı (gap ailesi, tam dönem); corr_full/t_stat = medyan kısmi korelasyon / t.")
# THYAO OOS yerli liderlik
th = GA[(GA.src == "THYAO") & (GA.period == "OOS") & (GA.kind == "intra")]
add(stock="TÜMÜ (46 hedef)", driver_yahoo="THYAO.IS", driver_desc="THY dünkü getirisi (XU100 lag kontrollü) -> diğer hisselerin ertesi gün gün-içi getirisi", tv_ticker="BIST:THYAO",
    relation="granger", lag="p=1 (intra)", corr_full=round(th.pc1.median(), 4), t_stat=round(th.t1.median(), 2), is_oos="IS: 0 kenar p<0,01; OOS: 12 kenar p<0,01, 46/46 pozitif; 2021-23 t=3,95, 2024-26 t=0,3 (XU100 intra hedefi)",
    confidence="DÜŞÜK", mechanism="Rejime özgü (2021-23 yüksek enflasyon/perakende yatırımcı dönemi: XU100 lag geri dönüş + THYAO ivmesi); FDR'den geçmiyor (q≈0,2)",
    notes="Tek bir piyasa-zamanlama faktörü gibi davranıyor (hedefler bağımsız değil); 2024-26'da yok. Öngörü gücü testi, strateji değil.")

# ---------- 4) DCC / bulaşma ----------
C = pd.read_csv(os.path.join(CACHE, "contagion_tests.csv"))
src_map = {"XU100": ("XU100.IS", "BIST:XU100", "0"), "ES_l1": ("ES=F", "CME_MINI:ES1!", "1"), "USDTRY": ("TRY=X", "FX:USDTRY", "0")}
for (cn, src), g in C.groupby(["crisis", "src"], sort=False):
    up_raw = (g.z_raw > 1.96).mean(); up_fr = (g.z_FR > 1.96).mean(); dn_fr = (g.z_FR < -1.96).mean()
    yah_, tv_, lg = src_map[src]
    conf = "ORTA" if (up_fr >= 0.3 and g.n_crisis.iloc[0] >= 25) else ("DÜŞÜK" if up_fr >= 0.15 else "DÜŞÜK (bulaşma yok)")
    add(stock="TÜMÜ(47)", driver_yahoo=yah_, driver_desc=f"{cn} ({g.type.iloc[0]}) — korelasyon artışı testi", tv_ticker=tv_, relation="regime", lag=lg,
        corr_full=round(g.rho_calm.mean(), 3), corr_1y=round(g.rho_crisis.mean(), 3), pcorr_xu100=round(g.rho_crisis_FR.mean(), 3), beta=round(g.vol_ratio_src.mean(), 2),
        t_stat=round(g.z_FR.mean(), 2), n=int(g.n_crisis.median()), confidence=conf,
        mechanism="Forbes–Rigobon: kriz korelasyonu kaynak volatilite artışına göre düzeltilir; artış kalırsa 'bulaşma', kalmazsa 'karşılıklı bağımlılık'",
        notes=f"SÜTUN NOTU: corr_full = sakin dönem (önceki 250g) ort. korelasyon; corr_1y = kriz ham; pcorr_xu100 = kriz FR-düzeltilmiş; beta = kaynak vol oranı; t_stat = ort. Fisher-z (FR). "
              f"Anlamlı artış: ham %{100*up_raw:.0f}, FR %{100*up_fr:.0f}; FR anlamlı azalış %{100*dn_fr:.0f}. DCC ort.: {g.dcc_calm.mean():.3f} -> {g.dcc_crisis.mean():.3f}")
D = pd.read_parquet(os.path.join(CACHE, "dcc_paths.parquet")); u = D.xs("USDTRY", axis=1, level=1).mean(axis=1)
add(stock="TÜMÜ(47)", driver_yahoo="TRY=X", driver_desc="USD/TRY–hisse DCC korelasyonu rejim kırılması", tv_ticker="FX:USDTRY", relation="regime", lag="0",
    corr_full=round(u["2014":"2021"].mean(), 3), corr_3y=round(u["2024":].mean(), 3), corr_1y=round(u["2025-10-31":].mean(), 3), n=int(u.notna().sum()),
    confidence="YÜKSEK", mechanism="2014–2021: TL değer kaybı = risk-off (negatif); KKM/yönetilen kur (2022+) sonrası kur–hisse bağı neredeyse kayboldu",
    notes="SÜTUN NOTU: corr_full = 2014–2021 ort. DCC; corr_3y = 2024–2026; corr_1y = son 1y. Yıllık: " + ", ".join(f"{y}:{v:.2f}" for y, v in u.resample('YE').mean().items().__iter__() if True) if False else
          "SÜTUN NOTU: corr_full = 2014–2021 ort. DCC; corr_3y = 2024–2026; corr_1y = son 1y. Yıllık: " + ", ".join(f"{d.year}:{v:.2f}" for d, v in u.resample("YE").mean().items()))

# ---------- 5) iddia kontrolü (varsa) ----------
pth = os.path.join(CACHE, "claims_verdicts.csv")
if os.path.exists(pth):
    T = pd.read_csv(pth)
    def sup(r):
        v = str(r["verdict"]); sh = " [kısa örneklem]" if "kısa" in v else ""
        if v.startswith("AYAKTA = yerli"): return "A2 AYAKTA: yerli küme/sektör" + sh
        if v.startswith("AYAKTA (faktör ikizi") or (v.startswith("AYAKTA") and r["dclass"] == "ORTAK"): return "A3 AYAKTA: ortak faktöre özgün maruziyet (emtia/kur/küresel, XU100 ötesi)" + sh
        if v.startswith("AYAKTA ama küçük"): return "A1b AYAKTA ama küçük (|pc|<0,05)" + sh
        if v.startswith("AYAKTA"): return "A1 AYAKTA: hisseye özgü dış bağ" + sh
        if v.startswith("AYNA"): return "B0 AYNA (ADR/ETF)"
        if v.startswith("ORTAK FAKTÖRÜN") or v.startswith("SADECE ORTAK"): return "B1 SADECE ORTAK FAKTÖR"
        if v.startswith("ZAYIF"): return "B2 ZAYIF / OOS'ta tutmuyor"
        if v.startswith("ZATEN"): return "B3 GÜRÜLTÜ (zaten zayıf)"
        if v.startswith("İŞARET"): return "B4 İŞARET TERS"
        return v
    T["super"] = T.apply(sup, axis=1)
    T.to_csv(pth.replace(".csv", "_final.csv"), index=False)
    T.to_csv(pth.replace(".csv", "_final.csv"), index=False)
    for ag, g in T.groupby("agent"):
        vc = g["super"].value_counts().sort_index()
        add(stock="TÜMÜ", driver_yahoo=f"{ag} ajanı iddiaları", driver_desc="Ortak faktör çerçevesinde yeniden test özeti", tv_ticker="-", relation="claim_check", lag="-",
            n=len(g), confidence="-", mechanism="Küresel 8 (t,t-1) + USDTRY + TUR_{t-1} + XU100 + sektör akranı kontrolü sonrası kalan etki",
            notes="; ".join(f"{k}: {v}" for k, v in vc.items()))
    hi = T[(T["conf_orig"] == "YÜKSEK") | ((T["conf_orig"] == "ORTA") & (T["dclass"] == "DIS"))].drop_duplicates(["agent", "stock", "dcol", "test", "k"])
    def cmap(r):
        v = r["super"]; pcf = abs(r.get("pc_full_tam", 0) or 0)
        if v.startswith("A2"): return "YÜKSEK" if (pcf >= 0.15 and "kısa" not in v) else "ORTA"
        if v.startswith("A1 ") and r["test"] == "gap": return "ORTA (açılışta fiyatlanır; işlenemez)"
        if v.startswith("A1 ") and "kısa" in v: return "DÜŞÜK (kısa örneklem)"
        if v.startswith("A1 ") and r["test"] == "sync": return "YÜKSEK" if pcf >= 0.15 else "ORTA"
        if v.startswith("A1 "): return "DÜŞÜK (öngörü gücü var, işlenebilirlik yok)"
        if v.startswith("A3"): return "ORTA"
        if v.startswith(("A1b", "B2")): return "DÜŞÜK"
        if v.startswith("B0"): return "DÜŞÜK (ayna)"
        if v.startswith("B1"): return "DÜŞÜK (sadece ortak faktör)"
        return "ÇOK DÜŞÜK"
    for _, r in hi.iterrows():
        add(stock=r.stock, driver_yahoo=r.driver_yahoo, driver_desc=f"[{r.agent}] {r.driver_desc}", tv_ticker=r.tv_ticker, relation="claim_check", lag=f"{r.test} k={r.k}",
            corr_full=r.get("raw_corr_tam"), corr_3y=r.get("pc_full_OOS"), pcorr_xu100=r.get("pc_light_tam"), beta=r.get("pc_full_tam"), t_stat=r.get("t_tam"), n=r.get("n_tam"),
            confidence=cmap(r), mechanism=f"KARAR: {r.super} | Orijinal iddia: {r.relation}, güven={r.confidence}; sürücü sınıfı={r.dclass}; ayrıntı={r.verdict}",
            notes=f"SÜTUN NOTU: corr_full = ham korelasyon; pcorr_xu100 = hafif kontrol (XU100 / kendi lag+XU100 lag); beta = tam faktör kontrollü kısmi korelasyon (tam dönem); corr_3y = aynı, OOS 2021-26; q_tam={r.get('q_tam', np.nan):.3g}; OOS t={r.get('t_OOS', np.nan):.2f}")
F = pd.DataFrame(rows, columns=COLS); F.to_csv(os.path.join(OUT, "f_y_ag.csv"), index=False)
print(F.relation.value_counts().to_dict(), F.shape)
