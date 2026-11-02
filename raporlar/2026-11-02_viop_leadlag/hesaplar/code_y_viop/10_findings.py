"""Bulgular CSV'si: out/f_y_viop.csv (ana brifing sütunları)."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from vcommon import *
COLS = "stock,driver_yahoo,driver_desc,tv_ticker,relation,lag,corr_full,corr_3y,corr_1y,pcorr_xu100,beta,t_stat,gap_corr,intra_corr,is_oos,bt_oos_sharpe,bt_oos_mean_bps,n,confidence,mechanism,notes".split(",")
rows = []
def add(**k): rows.append({c: k.get(c, np.nan) for c in COLS})
L = pd.read_csv(OUT + "/y_viop_likidite.csv")
for _, r in L.iterrows():
    add(stock=r["und"], driver_yahoo="VIOP_bulten", driver_desc=f"Likidite/maliyet ({r['und']} vadelisi)", tv_ticker=r["tv_ticker"], relation="liquidity", lag=0,
        n=r["n_days_12m"], confidence="ORTA" if r["liq_class"] in ("A", "B") else "DÜŞÜK",
        mechanism="Gidiş-dönüş maliyet = max(1 tik, sigma/sqrt(N_işlem)) + 2x2,1 bps komisyon (Wyart vd. 2008 spread yasası)",
        notes=(f"sınıf {r['liq_class']}; ADV medyan {r['adv_tl_median_12m']/1e6:.0f} mn TL ({r['adv_usd_median_12m']/1e6:.1f} mn USD); işlem# medyan {r['trades_median_12m']:.0f}; "
               f"AP {r['oi_tl_median_12m']/1e6:.0f} mn TL; sözleşme {r['contract_size']:g}; tik {r['tick']:g} ({r['tick_bps_last']:.1f} bps son fiyat, {r['tick_bps']:.1f} bps 12a medyan); "
               f"RT küçük emir {r['rt_cost_small_bps']:.1f} bps, muhafazakâr {r['rt_cost_cons_bps']:.1f}, 1 mn TL {r['rt_cost_1m_bps']:.1f}, bireysel tarife {r['rt_cost_retail_bps']:.1f}; "
               f"ön vade hacim payı {r['front_vol_share_12m']:.2f}; vade günü ön vade payı {r['front_share_bd0']:.2f}"))
# ---- baz anomalisi: hisse bazında TS ----
R = pd.read_csv(RES + "/basis_tests_ts.csv")
A = R[(R["per"] == "ALL") & (R["tgt"] != "d_anom")].copy(); A["p"] = ll.t_to_p(A["t"]); A["fdr"], _ = ll.fdr(A["p"].values)
fdr_map = A.set_index(["und", "sig", "tgt", "ver"])["fdr"].to_dict()
def conf(t_all, t_is, t_oos, fdr, mech=True, short=False):
    same = (np.sign(t_is) == np.sign(t_all)) and (np.sign(t_oos) == np.sign(t_all)) if (t_is == t_is and t_oos == t_oos) else False
    if abs(t_all) >= 3 and same and abs(t_is) >= 2 and abs(t_oos) >= 2 and fdr and not short: return "YÜKSEK"
    if (fdr or abs(t_all) >= 2.5) and same: return "ORTA"
    if abs(t_all) >= 1.5: return "DÜŞÜK"
    return "ÇOK DÜŞÜK"
for tgt, rel, desc, mech in [("y_sp_gap", "lead_gap", "Vadeli baz anomalisi_t (uzlaşma/spot kapanış - teorik taşıma, kendi 60g medyanından sapma) -> spot açılış gap'i_{t+1}",
                               "Spot kapanış müzayedesi/vadeli uzlaşma (son 10dk VWAP) arası fiyat ayrışması ertesi açılışta kapanıyor; vadeli önde. Spot gap'i işlenemez."),
                              ("y_L_r_intra", "lead_intra", "Vadeli baz anomalisi_t -> vadeli gün-içi_{t+1} (09:30 açılış -> kapanış)",
                               "Pahalı vadeli ertesi gün-içi ucuzluyor (baz yakınsaması). Açılış fiyatından giriş varsayımı; açılış seansı derinliği çok sığ.")]:
    for u in STOCKS + ["XU030"]:
        x = R[(R["und"] == u) & (R["sig"] == "anom_dev") & (R["tgt"] == tgt) & (R["ver"] == "all")].set_index("per")
        if "ALL" not in x.index: continue
        ta, ti, to = x.loc["ALL", "t"], x["t"].get("IS", np.nan), x["t"].get("OOS", np.nan)
        f = bool(fdr_map.get((u, "anom_dev", tgt, "all"), False))
        add(stock=u, driver_yahoo="VIOP_baz_anomalisi", driver_desc=desc, tv_ticker=f"{TV.get(u)} vs BIST:{u if u!='XU030' else 'XU030'}", relation=rel, lag=1,
            beta=x.loc["ALL", "bps_per_sd"], t_stat=ta, is_oos=f"IS t={ti:.2f} / OOS t={to:.2f}", n=x.loc["ALL", "n"],
            confidence=conf(ta, ti, to, f, short=(u in ("BRSAN", "CIMSA", "DOAS", "ASTOR"))), mechanism=mech,
            notes=f"beta = bps / 1 sd sinyal; kontroller: spot r_t, vadeli r_t; FDR({len(A)} test) {'geçti' if f else 'geçmedi'}")
# havuz FM satırları
FMb = pd.read_csv(RES + "/basis_tests_fm.csv")
def fmrow(df, sig, tgt, ver="all", sub="all", ctrls="sp_cc+L_r_set"):
    x = df[(df["sig"] == sig) & (df["tgt"] == tgt) & (df["ver"] == ver) & (df["sub"] == sub) & (df["ctrls"].fillna("") == ctrls)].set_index("per")
    return x
for tgt, rel, txt in [("y_sp_gap", "lead_gap", "spot gap_{t+1}"), ("y_L_r_intra", "lead_intra", "vadeli gün-içi_{t+1}"), ("y_sp_intra", "lead_intra", "spot gün-içi_{t+1}"),
                      ("y_L_r_set", "lead_multiday", "vadeli uzlaşma getirisi_{t+1}")]:
    for sub in ["all", "AB"]:
        x = fmrow(FMb, "anom_dev", tgt, sub=sub)
        if "ALL" not in x.index: continue
        ta, ti, to = x.loc["ALL", "t"], x["t"].get("IS", np.nan), x["t"].get("OOS", np.nan)
        add(stock=f"PAY47_{sub}", driver_yahoo="VIOP_baz_anomalisi", driver_desc=f"Kesitsel (Fama-MacBeth) baz anomalisi_t -> {txt}", tv_ticker="BIST:<KOD>1!",
            relation=rel, lag=1, beta=x.loc["ALL", "bps_per_sd"], t_stat=ta, is_oos=f"IS {x['bps_per_sd'].get('IS', np.nan):.1f} bps t={ti:.2f} / OOS {x['bps_per_sd'].get('OOS', np.nan):.1f} bps t={to:.2f}",
            n=x.loc["ALL", "n_days"], confidence=("YÜKSEK" if (abs(ta) >= 3 and abs(ti) >= 2 and abs(to) >= 2 and np.sign(ti) == np.sign(to)) else "ORTA" if abs(ta) >= 2 else "DÜŞÜK") if tgt != "y_sp_intra" else ("DÜŞÜK" if abs(ti) < 2 else "ORTA"),
            mechanism="Vadeli-spot göreli fiyat ayrışmasının (likidite baskısı) ertesi gün kapanması; spot tarafı gap'te, vadeli tarafı gün-içinde",
            notes="beta = bps / 1 kesit sd (sıra-normalize); kontroller spot r_t, vadeli r_t; " + ("A/B likit sınıf" if sub == "AB" else "tüm hisseler"))
# ---- temettü ----
dv = pd.read_csv(RES + "/basis_dividend.csv").iloc[0]
add(stock="PAY47", driver_yahoo="VIOP_baz_temettü", driver_desc="Vadeli bazından örtük temettü (r*tau - ln F/S) vs gerçekleşen temettü (vadeye 3-40 gün)", tv_ticker="BIST:<KOD>1!",
    relation="event", lag=0, beta=dv["slope"], t_stat=dv["t"], n=dv["n"], confidence="YÜKSEK",
    mechanism="Temettü düzeltmesi yok (nakit temettüde sözleşme düzeltilmez) -> vadeli fiyatı beklenen temettüyü içerir",
    notes=f"eğim {dv['slope']:.2f}, R2 {dv['r2']:.2f}, sabit {dv['const_bps']:.1f} bps; temettüsüz günlerde medyan sapma ~0 bps (USDTRY örtük faiz taşımayı iyi açıklıyor)")
# ---- AP/hacim FM ----
FMo = pd.read_csv(RES + "/oi_fm_tests.csv")
for sig, tgt, rel, desc, mech in [
    ("vsur", "y_sp_intra", "flow", "Pay vadelisi hacim sürprizi_t (ln hacim - 20g ort.) -> spot gün-içi_{t+1}", "Yüksek vadeli hacmi -> ertesi gün açılışta devam, gün içinde geri dönüş (likidite baskısı)"),
    ("vsur", "y_sp_gap", "flow", "Pay vadelisi hacim sürprizi_t -> spot gap_{t+1}", "Açılışta devam (işlenemez)"),
    ("dOI_z", "y_L_r_set", "flow", "Açık pozisyon değişimi z_t -> vadeli getiri_{t+1}", "AP artışı (yeni pozisyon) ertesi gün hafif negatif; zayıf"),
    ("dOI_z", "y_sp_intra", "flow", "Açık pozisyon değişimi z_t -> spot gün-içi_{t+1}", "zayıf"),
    ("rdOI", "y_sp_cc", "flow", "Fiyat x AP etkileşimi ('yeni long/short') -> spot cc_{t+1}", "Klasik 'AP artışı+fiyat artışı=yeni long -> devam' kuralı DESTEKLENMİYOR"),
    ("fsr", "y_sp_cc", "flow", "Vadeli/spot hacim oranı sürprizi -> spot cc_{t+1}", "bilgili işlem vadeliye kayıyor hipotezi: destek yok")]:
    for sub in ["all", "AB"]:
        x = FMo[(FMo["sig"] == sig) & (FMo["tgt"] == tgt) & (FMo["sub"] == sub)].set_index("per")
        if "ALL" not in x.index: continue
        ta, ti, to = x.loc["ALL", "t"], x["t"].get("IS", np.nan), x["t"].get("OOS", np.nan)
        cf = "ORTA" if (abs(ta) >= 3 and abs(ti) >= 2 and abs(to) >= 2 and np.sign(ti) == np.sign(to)) else "DÜŞÜK" if abs(ta) >= 2 else "ÇOK DÜŞÜK"
        add(stock=f"PAY47_{sub}", driver_yahoo=f"VIOP_{sig}", driver_desc=desc, tv_ticker="BIST:<KOD>1!", relation=rel, lag=1, beta=x.loc["ALL", "bps_per_sd"], t_stat=ta,
            is_oos=f"IS t={ti:.2f} / OOS t={to:.2f}", n=x.loc["ALL", "n_days"], confidence=cf, mechanism=mech,
            notes=f"Fama-MacBeth, sıra-normalize, kontrol r_t; hisse bazında TS: 1444 testte 2 FDR")
TSo = pd.read_csv(RES + "/oi_ts_tests.csv")
for sig, tgt in [("dOI_z", "y_sp_intra"), ("dOI_z", "y_L_r_set"), ("rdOI", "y_L_r_set"), ("vsur", "y_sp_intra")]:
    x = TSo[(TSo["und"] == "XU030") & (TSo["sig"] == sig) & (TSo["tgt"] == tgt)].set_index("per")
    if "ALL" not in x.index: continue
    add(stock="XU030", driver_yahoo=f"VIOP_{sig}", driver_desc=f"XU030 vadelisi {sig}_t -> {tgt}", tv_ticker="BIST:XU030D1!", relation="flow", lag=1,
        beta=x.loc["ALL", "b_bps_sd"], t_stat=x.loc["ALL", "t"], is_oos=f"IS t={x['t'].get('IS', np.nan):.2f} / OOS t={x['t'].get('OOS', np.nan):.2f}", n=x.loc["ALL", "n"],
        confidence="DÜŞÜK" if abs(x.loc["ALL", "t"]) >= 2 else "ÇOK DÜŞÜK", mechanism="Endeks vadelisi AP/hacim; yabancı/yerli kırılımı bültende yok", notes="FDR'den geçmedi")
# ---- açılış: vadeli 09:30 -> spot 10:00 ----
OC = pd.read_csv(RES + "/openclose_tests.csv").set_index("und")
for u, r in OC.iterrows():
    if r.get("open_beta") != r.get("open_beta"): continue
    add(stock=u, driver_yahoo="VIOP_acilis_09:30", driver_desc="Vadeli açılış (09:30, uzlaşmaya göre) -> spot açılış gap'i (09:55/10:00) aynı gün", tv_ticker=TV.get(u),
        relation="lead_auction", lag=0, beta=r["open_beta"], corr_full=np.sqrt(max(r["open_r2"], 0)), t_stat=np.nan, n=r["n_b"], confidence="YÜKSEK" if r["open_r2"] > 0.25 else "ORTA",
        mechanism="Vadeli piyasa spot açılış müzayedesinden 25-30 dk önce açılıyor; gece bilgisini önce fiyatlıyor",
        notes=f"R2 {r['open_r2']:.2f}; spot emirleri 09:40-09:55 müzayedesine vadeli açılışı görerek verilebilir ama tahmin edilen şey spot açılış fiyatının kendisi (gap), gün-içi kalıntı: gF->spot gün-içi b={r.get('gF_intra_b', np.nan):.2f} t={r.get('gF_intra_t', np.nan):.2f}; kalıntı u->gün-içi t={r.get('u_intra_t', np.nan):.2f}")
r = OC.loc["XU030"]
add(stock="XU030", driver_yahoo="VIOP_XU030_18:15_kapanis", driver_desc="XU030 vadeli son fiyatı (18:15) / uzlaşma (18:05-18:15 VWAP) -> spot gap_{t+1}", tv_ticker="BIST:XU030D1!",
    relation="lead_gap", lag=1, beta=r["m_gap_b"], t_stat=r["m_gap_t"], n=r["n_a"], confidence="ORTA",
    mechanism="Vadeli spot kapanışından (18:10) 5 dk sonra kapanıyor; son dakikaların bilgisi ertesi spot açılışında", notes=f"vadeli gece getirisine etkisi yok (b={r['m_fgap_b']:.2f}, t={r['m_fgap_t']:.2f}) -> işlenemez")
# ---- akşam seansı ----
EV = pd.read_csv(RES + "/evening_test.csv").set_index("und")
add(stock="XU030", driver_yahoo="VIOP_bulten_aksam", driver_desc="Bülten fiyat alanları (açılış/yüksek/düşük/kapanış/uzlaşma) akşam seansını (19:00-23:00) İÇERMİYOR", tv_ticker="BIST:XU030D1!",
    relation="hypothesis", lag=0, beta=EV.loc["XU030", "hi_b_ev"], t_stat=EV.loc["XU030", "hi_t_ev"], n=EV.loc["XU030", "n"], confidence="YÜKSEK",
    mechanism="Bülten ~19:45-20:55 TSİ üretiliyor; açılış = 09:30 açılış seansı; yüksek fazlası ES akşam yoluna yüklenmiyor (pay vadelisi kontrolüyle aynı)",
    notes=f"XU030 eğim {EV.loc['XU030','hi_b_ev']:.2f} (t {EV.loc['XU030','hi_t_ev']:.1f}) vs THYAO (akşam seansı yok) {EV.loc['THYAO','hi_b_ev']:.2f} (t {EV.loc['THYAO','hi_t_ev']:.1f}); kapanış-uzlaşma ile ES akşam korelasyonu {EV.loc['XU030','corr_clset_esev']:.3f}. Akşam seansı getirisi bu veriyle ÖLÇÜLEMEZ (TradingView BIST:XU030D1! gün-içi verisi gerekir)")
EE = pd.read_csv(RES + "/evening_es_tests.csv")
for u in ["XU030", "XLBNK"]:
    a = EE[(EE["und"] == u) & (EE["y"] == "gF")].iloc[0]; b = EE[(EE["und"] == u) & (EE["y"] == "R2_decomp_gF")].iloc[0]; c = EE[(EE["und"] == u) & (EE["y"] == "L_r_intra")].iloc[0]
    add(stock=u, driver_yahoo="ES=F", driver_desc="ES akşam penceresi (15:00-20:00 UTC = VİOP akşam seansı) -> endeks vadelisi gece getirisi (uzlaşma->09:30)", tv_ticker="CME_MINI:ES1!",
        relation="lead_gap", lag=1, beta=a["b_ev"], t_stat=a["t_ev"], n=a["n"], confidence="ORTA",
        mechanism="Akşam seansında işlenebilir bilgi payı", notes=f"gece (20:00-06:30 UTC) b={a['b_night']:.2f} t={a['t_night']:.1f}; R2: yalnız akşam {b['b_ev']:.3f}, yalnız gece {b['b_night']:.3f}, ikisi {b['r2']:.3f}; akşam ES -> ertesi vadeli gün-içi b={c['b_ev']:.2f} t={c['t_ev']:.2f} (kalıntı yok). 2024-06+ (ES saatlik)")
# ---- backtestler ----
BT = pd.read_csv(RES + "/backtests.csv")
def btrow(name, stock, rel, desc, conf_, mech, notes=""):
    x = BT[BT["bt"] == name]
    if x.empty: return
    x = x.iloc[0]
    add(stock=stock, driver_yahoo="VIOP_backtest", driver_desc=desc, tv_ticker="BIST:<KOD>1!" if stock.startswith("PAY") else TV.get(stock, ""), relation=rel, lag=1,
        t_stat=x.get("ALL_t"), is_oos=f"IS {x.get('IS_mean_bps', np.nan):.1f} bps (t {x.get('IS_t', np.nan):.1f}) / OOS {x.get('OOS_mean_bps', np.nan):.1f} bps (t {x.get('OOS_t', np.nan):.1f})",
        bt_oos_sharpe=x.get("OOS_sharpe"), bt_oos_mean_bps=x.get("OOS_mean_bps"), n=x.get("ALL_n"), confidence=conf_, mechanism=mech,
        notes=f"{name}; yılların pozitif oranı {x.get('years_pos_frac', np.nan):.2f}; ort. maliyet {x.get('avg_cost_bps', np.nan):.1f} bps. {notes}")
btrow("BT1 baz anomalisi (pahalıyı SAT) q=0.2 -> y_L_r_intra (tümü) NET", "PAY47", "lead_intra", "BT1: baz anomalisi L/S, vadeli 09:30 açılış -> kapanış (NET)", "DÜŞÜK",
      "Baz yakınsaması", "BRÜT +24 bps/gün (t 9). Açılış fiyatından dolum iyimser: açılış seansı medyan hacmi THYAO ~0,56 mn TL; VWAP->VWAP girişte brüt +6,7, net -11 bps. Muhafazakâr maliyette ~0.")
btrow("BT1 baz anomalisi (pahalıyı SAT) q=0.2 -> y_vwap (tümü) NET", "PAY47", "lead_multiday", "BT1b: baz anomalisi L/S, vadeli VWAP(t+1)->VWAP(t+2) (NET; tam uygulanabilir)", "ÇOK DÜŞÜK", "Baz yakınsaması", "Kenar açılış fiyatında; VWAP girişte maliyeti karşılamıyor")
btrow("BT2 vsur (-) L/S -> y_sp_intra NET", "PAY47", "flow", "BT2: vadeli hacim sürprizi L/S (yüksek hacmi sat) -> spot gün-içi (NET)", "DÜŞÜK", "Likidite baskısı geri dönüşü", "BRÜT +10,4 bps (t 4,1), yılların %100'ü pozitif; maliyet ~18 bps > kenar")
btrow("BT2 dOI_z (-) L/S -> y_L_r_intra NET", "PAY47", "flow", "BT2b: AP değişimi L/S (AP artanı sat) -> vadeli gün-içi (NET)", "ÇOK DÜŞÜK", "", "BRÜT +9,2 bps (t 3,6); net negatif")
btrow("BT3b XU030 vadeli: 18:15 kapanışta AL, ertesi 09:30 açılışta kapat NET", "XU030", "regime", "BT3: XU030 vadeli gece long (18:15 -> 09:30) (NET)", "DÜŞÜK", "Gece getiri primi (spot 'gap>0' bulgusunun vadeli karşılığı)", "BRÜT +5,0 bps/gece (t 5,2; yılların %90'ı +), maliyet ~4,8 bps -> net ~0")
btrow("BT3a XU030 vadeli: 09:30 açılışta SAT, 18:15 kapanışta kapat NET", "XU030", "regime", "BT3a: XU030 vadeli gün-içi short (09:30->18:15) (NET)", "ÇOK DÜŞÜK", "Spot 'gün-içi<0' bulgusu", "BRÜT yalnız +2,7 bps (t 0,8): spot gün-içi negatifliği vadelide büyük ölçüde YOK")
btrow("BT5 XU030 baz anomalisi (pahalıysa sat) -> y_L_r_intra NET", "XU030", "lead_intra", "BT5: XU030 baz anomalisi -> XU030 vadeli gün-içi (NET)", "DÜŞÜK", "Baz yakınsaması (yarı ömür ~3,5 gün)", "yılların %50'si +")
btrow("BT4 vadeli açılış gap'i fade (|gF|>0%) -> spot gün-içi NET", "PAY47", "lead_auction", "BT4: vadeli açılış gap'ine karşı spot gün-içi (NET)", "ÇOK DÜŞÜK", "Gap fade", "brüt ~0")
F = pd.DataFrame(rows, columns=COLS)
F.to_csv(OUT + "/f_y_viop.csv", index=False)
print(F.shape); print(F["relation"].value_counts().to_string()); print(F["confidence"].value_counts().to_string())
