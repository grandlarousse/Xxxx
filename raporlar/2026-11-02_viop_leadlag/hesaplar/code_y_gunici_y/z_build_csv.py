"""Bulgular CSV'si: out/f_y_gunici_y.csv (ana brifing sütunları)."""
import numpy as np, pandas as pd, c_common as c
ll = c.ll; TG = c.VIOP; R = c.RES
COLS = "stock,driver_yahoo,driver_desc,tv_ticker,relation,lag,corr_full,corr_3y,corr_1y,pcorr_xu100,beta,t_stat,gap_corr,intra_corr,is_oos,bt_oos_sharpe,bt_oos_mean_bps,n,confidence,mechanism,notes".split(",")
def tv(s):
    if s.startswith("X"): return f"BIST:{s}"
    return f"BIST:{s} (SSF: BIST:{s}1!)"
def ydrv(s): return s + ".IS" if s[0].isalpha() and s.isupper() else s
DESC = {"XU030": "BIST 30 endeksi", "XBANK": "BIST Banka", "XLBNK": "BIST Likit Banka", "XUSIN": "BIST Sınai", "XHOLD": "BIST Holding"}
LQ = pd.read_csv(R + "/a0_liq.csv").set_index("stock"); SSF = pd.read_csv(R + "/a0_ssf_tick.csv").set_index("stock")
rows = []
def add(**k):
    o = {cn: "" for cn in COLS}; o.update(k); rows.append(o)

# ---- 1) m5 lead-lag (741 ileri çift)
P = pd.read_csv(R + "/a1_m5_pairs.csv"); F = P[P.dir == "fwd"]
for _, r in F.iterrows():
    same = np.sign(r.h1_b1) == np.sign(r.h2_b1) if "h1_b1" in r else False
    if r.std_fdr == 1 and same and abs(r.get("oc_t1", 0)) > 2: conf = "DÜŞÜK"
    elif r.std_fdr == 1: conf = "DÜŞÜK"
    else: conf = "ÇOK DÜŞÜK"
    liq = LQ.loc[r.target]
    add(stock=r.target, driver_yahoo=ydrv(r.leader), driver_desc=DESC.get(r.leader, f"{r.leader} (BIST hissesi)") + " 5 dk getirisi", tv_ticker=f"BIST:{r.leader}",
        relation="lead_5m", lag="1..6 bar (5..30 dk)", corr_full=round(r.corr0, 3), beta=round(r.std_b1, 4), t_stat=round(r.std_t1, 2),
        is_oos=f"1.yarı b1={r.h1_b1:.3f} / 2.yarı b1={r.h2_b1:.3f}", n=int(r.std_n) if not np.isnan(r.std_n) else "",
        confidence=conf, mechanism="Bilgi yayılımı / bayat son fiyat (tik ayrıklığı) — kontroller: hedefin kendi 6 gecikmesi + XU030 6 gecikmesi",
        notes=(f"Σb1..6={r.std_sum:.3f} (t {r.std_tsum:.1f}), Wald FDR={'EVET' if r.std_fdr==1 else 'hayır'} (741 test); bar-içi(ilk işlemden) b1={r.oc_b1:.3f} t {r.oc_t1:.1f}; "
               f"önceki bar fiyat değişmemiş b1={r.pz_b1:.3f} / değişmiş {r.pnz_b1:.3f}; önceki bar hacim≥medyan {r.va_b1:.3f} / < {r.vl_b1:.3f}; gecikmeli pay {r.delay_share:.2f}; "
               f"%90 tepki {r.adj_min90} dk; hedef fiyat-değişmeyen bar %{100*liq.ret0_frac:.0f}, spot tik {liq.tick_bps:.1f} bps. b std birim (slot std). 60 gün (07.08–30.10.2026, fon krizi dahil). İŞLENEMEZ: brüt 1–7 bps/işlem"))
# ---- 2) h1 lead-lag
P = pd.read_csv(R + "/a1b_h1_pairs.csv"); F = P[(P.dir == "fwd") & P.all_b1.notna()]
for _, r in F.iterrows():
    add(stock=r.target, driver_yahoo=ydrv(r.leader), driver_desc=DESC.get(r.leader, f"{r.leader} (BIST hissesi)") + " 60 dk getirisi", tv_ticker=f"BIST:{r.leader}",
        relation="lead_hourly", lag="1..6 saat-bar", corr_full=round(r.corr0, 3), beta=round(r.all_b1, 4), t_stat=round(r.all_t1, 2),
        is_oos=f"IS b1={r.is_b1:.3f} (t {r.is_t1:.1f}) / OOS b1={r.oos_b1:.3f} (t {r.oos_t1:.1f})", n=int(r.all_n),
        confidence="ÇOK DÜŞÜK", mechanism="Saatlik ölçekte gecikmeli yayılım beklenmez (dakikalar içinde fiyatlanıyor)",
        notes=f"Σb1..6={r.all_sum:.3f} (t {r.all_tsum:.1f}); FDR: 741 ileri + 741 ters testin 0'ı geçti. 2023-12..2026-10; parçalar O->07:30, saatlik, 14:30->C")
# ---- 3) Gap fade hisse bazında (günlük 2014+, |gap|>1%), E2 (h1) ile
A = pd.read_csv(R + "/a3_fade_daily.csv"); A = A[A.thr.astype(str) == "0.01"].set_index("stock")
H2 = pd.read_csv(R + "/a7_fade_h1_fdr.csv"); H2 = H2[H2.thr.astype(str) == "0.01"]
E2 = H2[H2.entry == "E2_vwap30"].set_index("stock"); E3 = H2[H2.entry == "E3_0730"].set_index("stock")
# yıllık tutarlılık
yr = {}
for s in TG:
    d = ll.decomp(s); d = d[d.index >= "2014-01-01"]; pos = -np.sign(d["gap"]).where(d["gap"].abs() > 0.01, 0.0)
    g = (pos * d["intra"])[pos != 0]; ym = g.groupby(g.index.year).mean(); yr[s] = (ym > 0).mean()
for s in TG:
    r = A.loc[s]; e2 = E2.loc[s]; e3 = E3.loc[s]
    if r.fdr == 1 and r.is_t > 2 and r.oos_t > 2 and yr[s] >= 0.75 and e2.fdr == 1: conf = "YÜKSEK"
    elif r.all_t > 2 and r.oos_bps > 0 and e2.all_bps > 0: conf = "ORTA"
    elif r.all_bps > 0 and r.oos_bps > 0: conf = "DÜŞÜK"
    else: conf = "ÇOK DÜŞÜK"
    ssf = SSF.loc[s] if s in SSF.index else None
    add(stock=s, driver_yahoo=f"{s}.IS", driver_desc="Kendi açılış gap'i (açılış müzayedesi, |gap|>%1) -> gün-içi dönüş", tv_ticker=tv(s), relation="lead_auction", lag="0 (açılış->kapanış)",
        t_stat=round(r.all_t, 2), is_oos=f"IS2014-20 {r.is_bps:.1f} bps (t {r.is_t:.1f}) / OOS2021-26 {r.oos_bps:.1f} bps (t {r.oos_t:.1f})", bt_oos_sharpe=round(r.oos_sharpe8, 2),
        bt_oos_mean_bps=round(r.oos_bps, 1), n=int(r.all_n), confidence=conf,
        mechanism="Açılış müzayedesinde likidite sağlayıcı eksikliği -> aşırı tepki, gün içinde kısmi dönüş (illikit hisselerde güçlü)",
        notes=(f"Giriş açılış fiyatı (iyimser). h1 2023-12+: E0 {H2[(H2.stock==s)&(H2.entry=='E0_open')].all_bps.values[0]:.1f}, E2 ilk-30dk VWAP vekili {e2.all_bps:.1f} bps (t {e2.all_t:.1f}, FDR {'EVET' if e2.fdr==1 else 'hayır'}), "
               f"E3 07:30 {e3.all_bps:.1f} bps; yılların %{100*yr[s]:.0f}'inde pozitif; 47 test BH-FDR={'EVET' if r.fdr==1 else 'hayır'}; OOS net8 {r.oos_net8:.1f}, net15 {r.oos_net15:.1f}. "
               + (f"SSF tik {ssf.ssf_tick_bps:.1f} bps, SSF hacim ~{ssf.ssf_hacim_mnTL:.0f} mn TL/gün" if ssf is not None else "")))
# ---- 4) Sektör gap yetişmesi
S = pd.read_csv(R + "/a3_sector.csv")
for s in TG:
    a = S[(S.stock == s) & (S.y == "intra_2014+")].iloc[0]; b = S[(S.stock == s) & (S.y == "intra_2021+")].iloc[0]; h = S[(S.stock == s) & (S.y == "O-0730_h1")].iloc[0]
    if a.fdr_sec == 1 and b.t_sec > 1.5: conf = "ORTA"
    elif a.t_sec > 2 or (a.b_sec > 0 and b.b_sec > 0 and h.b_sec > 0): conf = "DÜŞÜK"
    else: conf = "ÇOK DÜŞÜK"
    add(stock=s, driver_yahoo="sektör akranları gap ort. (" + ",".join([p for p in c.SECTOR[c.SEC_OF[s]] if p != s]) + ")" if len(c.SECTOR[c.SEC_OF[s]]) > 1 else "XU030.IS gap",
        driver_desc=f"Sektör ({c.SEC_OF[s]}) akranlarının açılış gap'i, kendi gap + XU030 gap kontrollü", tv_ticker=tv(s), relation="lead_auction", lag="0 (açılış sonrası)",
        beta=round(a.b_sec, 3), t_stat=round(a.t_sec, 2), is_oos=f"2014+ b={a.b_sec:.3f} (t {a.t_sec:.1f}) / 2021+ b={b.b_sec:.3f} (t {b.t_sec:.1f})", n=int(a.n), confidence=conf,
        mechanism="Açılış müzayedesi sektör bilgisini eksik yansıtıyor; hisse ilk 30 dk'da akranlarına yetişiyor",
        notes=f"y=gün-içi (O->C). h1 2023-12+: O->07:30 b_sec={h.b_sec:.3f} (t {h.t_sec:.1f}); 07:30->C b_sec={S[(S.stock==s)&(S.y=='0730-C_h1')].b_sec.values[0]:.3f}. Kendi gap b={a.b_own:.3f} (t {a.t_own:.1f}). 47 test FDR={'EVET' if a.fdr_sec==1 else 'hayır'}")
# ---- 5) Kapanış müzayedesi -> ertesi gün
K = pd.read_csv(R + "/a4_stock.csv"); K = K[K.spec == "summer"]
for s in TG + ["XU030"]:
    g1 = K[(K.stock == s) & (K.y == "gap1")]; r1 = K[(K.stock == s) & (K.y == "r1_1")]
    a = g1[g1.period == "all"].iloc[0]; i_ = g1[g1.period == "is"]; o_ = g1[g1.period == "oos"]
    ib = i_.b_CA.values[0] if len(i_) else np.nan; ob = o_.b_CA.values[0] if len(o_) else np.nan
    rr = r1[r1.period == "all"].iloc[0]
    if a.fdr == 1 and ib < 0 and ob < 0: conf = "ORTA"
    elif a.b_CA < 0 and rr.b_CA < 0: conf = "DÜŞÜK"
    else: conf = "ÇOK DÜŞÜK"
    add(stock=s, driver_yahoo=f"{s}.IS", driver_desc="Kendi kapanış müzayedesi hareketi CA=log(C/P15:00) -> ertesi gün gap ve 07:30'a kadar", tv_ticker=tv(s), relation="lead_auction", lag="1 gün (kapanış->ertesi açılış/07:30)",
        beta=round(a.b_CA, 3), t_stat=round(a.t_CA, 2), is_oos=f"IS b={ib:.3f} / OOS b={ob:.3f}", n=int(a.n), confidence=conf,
        mechanism="Kapanış müzayedesi fiyat baskısı (endeks fonları/MOC emirleri, SSF vade sonu fiziki teslim = spot kapanış fiyatı) ertesi sabah kısmen geri dönüyor",
        notes=f"gap_t+1 b={a.b_CA:.3f}; O->07:30_t+1 b={rr.b_CA:.3f} (t {rr.t_CA:.1f}); yalnız AB yaz saati günleri (h1 14:30 barı var), ~420 gün; 47 test FDR={'EVET' if a.fdr==1 else 'hayır'}. Giriş C_t ancak spot 'kapanış fiyatından işlemler' (18:08–18:10 TSİ) ile; SSF ile birebir işlenemez")
# ---- 6) Gün-içi momentum (Gao vd.)
M = pd.read_csv(R + "/a5_stock.csv"); BT = pd.read_csv(R + "/a5_bt.csv")
for s in ["XU030", "XU100", "XBANK", "XUSIN"] + TG:
    m = M[(M.stock == s) & (M.y == "r_last") & (M.spec == "r_first")]
    a = m[m.period == "all"].iloc[0]; o_ = m[m.period == "oos"].iloc[0]
    i_ = m[m.period == "is"].iloc[0] if (m.period == "is").any() else pd.Series({"b_r_first": np.nan, "t_r_first": np.nan})
    b = BT[(BT.stock == s) & (BT.exit == "close") & (BT.signal == "r1") & (BT.period == "oos")]
    conf = "DÜŞÜK" if s in ["XU030", "XU100"] else ("DÜŞÜK" if (i_.t_r_first > 2 and o_.t_r_first > 2) else "ÇOK DÜŞÜK")
    add(stock=s, driver_yahoo=f"{s}.IS", driver_desc="Kendi ilk yarım saat getirisi (önceki kapanış->10:30 TSİ) -> son 30 dk + kapanış müzayedesi", tv_ticker=("BIST:XU030 (vadeli BIST:XU030D1!)" if s == "XU030" else tv(s)),
        relation="intraday_momentum", lag="aynı gün (07:30 -> 14:30-C)", beta=round(a.b_r_first, 4), t_stat=round(a.t_r_first, 2),
        is_oos=f"IS b={i_.b_r_first:.3f} (t {i_.t_r_first:.1f}) / OOS b={o_.b_r_first:.3f} (t {o_.t_r_first:.1f})", bt_oos_mean_bps=round(b.gross_bps.values[0], 1) if len(b) else "",
        n=int(a.n), confidence=conf, mechanism="Gao vd. 2018: geç bilgi işleyen/rebalans yapan yatırımcılar gün sonunda ilk yarım saatin yönünde işlem yapar",
        notes=(f"BT sign(O->07:30) 14:30->C OOS brüt {b.gross_bps.values[0]:.1f} bps (t {b.t.values[0]:.1f}); " if len(b) else "") + "47 hissede FDR 0/47 (tüm/IS/OOS)")
# ---- 7) Özet/olay satırları
add(stock="XU030", driver_yahoo="takvim", driver_desc="Ayın son iş günü (VİOP vade sonu) ve ayın ilk iş günü", tv_ticker="BIST:XU030 (vadeli BIST:XU030D1!)", relation="event", lag="0",
    beta="", t_stat=-2.04, is_oos="eom cc IS -12 bps (t -0.8) / OOS -39 bps (t -2.1); ilk gün cc IS -14 (t -0.8) / OOS +75 (t 3.3)", n=3201, confidence="DÜŞÜK",
    mechanism="Vade sonu kapanış baskısı/arbitraj çözülmesi + yeni ay fon girişleri (ay başı etkisi); 2021+ yüksek enflasyon rejimine özgü olabilir",
    notes="Günlük 2014-2026, 153 ay. Ay sonu |CA| 37,7 bps vs diğer 20,5 (h1, hisse ort.); m5 müzayede hacim payı %3,9 vs %2,9. SSF vade sonu uzlaşma = spot kapanış fiyatı (47/47 doğrulandı, 30.10.2026 bülteni)")
add(stock="47 havuz", driver_yahoo="XU030.IS", driver_desc="XU030 5 dk getirisi, açılış penceresi (07:05-07:30 UTC hedef) vs gün geri kalanı", tv_ticker="BIST:XU030", relation="lead_5m", lag="1 bar (5 dk)",
    beta=0.158, t_stat=2.78, is_oos="açılış 0,158 (t 2,8) vs 07:30 sonrası 0,059 (t 7,9)", n=16920, confidence="DÜŞÜK", mechanism="Açılış sonrası ilk 30 dk'da fiyat keşfi yavaş; endeks bilgisi hisselere ~5 dk gecikmeyle geçiyor",
    notes="60 gün; std birim; likit/illikit benzer (0,178/0,138)")
add(stock="47 portföy", driver_yahoo="kendi gap", driver_desc="Gap fade portföyü |gap|>%1 (eşit ağırlık)", tv_ticker="-", relation="lead_auction", lag="0",
    t_stat=2.78, is_oos="E0 IS 28,0 bps (t 7,0) / OOS 16,5 (t 2,8); illikit24 OOS 26,9 (t 3,9), likit23 OOS 3,1 (t 0,4); h1 E2 OOS 21,1 (t 1,9), E3 15,3 (t 1,5)",
    bt_oos_mean_bps=16.5, n=28521, confidence="ORTA", mechanism="Açılış müzayedesi aşırı tepkisi (illikit)", notes="Yıllar (E0): 13 yılın 11'inde pozitif; 2025 ≈0 (Mart 2025 şoku -90 bps); 2026 Eyl-Eki fon krizinde m5 örneklemde gap devam etti (fade -45 bps medyan, 60 gün)")
add(stock="47 portföy", driver_yahoo="CA (kapanış müzayedesi)", driver_desc="Kapanış müzayedesi dönüşü portföyü |CA|>25 bps, C_t -> 07:30_t+1", tv_ticker="-", relation="lead_auction", lag="1 gün",
    t_stat=4.14, is_oos="IS 11,7 bps (t 2,5) / OOS 16,4 bps (t 4,1); 2024 12,7 / 2025 17,1 / 2026 13,7", bt_oos_mean_bps=16.4, n=5858, confidence="ORTA",
    mechanism="Kapanış fiyat baskısının ertesi sabah dönüşü", notes="İllikit24 18,7 bps (t 5,2), likit23 7,7 (t 1,7); |CA|>50 bps OOS 25,7 (t 3,5). Vade sonu hariç de aynı (14,4, t 4,5). Spot KFİS ile giriş; maliyet ~8–15 bps -> net 1–10 bps")
add(stock="47 portföy", driver_yahoo="sektör akran gap - kendi gap", driver_desc="Sektör gap yetişme portföyü |s|>%1", tv_ticker="-", relation="lead_auction", lag="0",
    t_stat=4.72, is_oos="E0->C IS 25,3 (t 7,6) / OOS 23,4 (t 4,7); h1: E0->07:30 IS 16,7/OOS 15,9 (t 3,0); E2->C OOS 10,7 (t 1,2); E3->C OOS 6,6 (t 0,8)", bt_oos_mean_bps=23.4, n=20503, confidence="ORTA",
    mechanism="Açılış müzayedesi sektör bilgisini eksik yansıtıyor", notes="Getirinin çoğu ilk 30 dk'da: gerçekçi girişle (E2/E3) maliyet sonrası ~0. Gap fade ile örtüşür (s kendi gap'i içerir)")
out = pd.DataFrame(rows)[COLS]
out.to_csv(c.OUT + "/f_y_gunici_y.csv", index=False)
print(len(out), out.confidence.value_counts().to_dict(), out.relation.value_counts().to_dict())
