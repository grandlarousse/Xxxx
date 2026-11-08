"""Adım 2: hipotez ızgarası — her test register() ile kaydedilir. Hedef: VİOP fwd{h} (t uzlaşması -> t+h uzlaşması).
Sinyal gün t 15:00 UTC'de bilinir (bkz. a5_01_signals.py). Çıktı: grid_viop.csv
Önce bu ajanın kayıt dosyası sıfırlanır (betik yeniden çalıştırılabilir)."""
from a5_lib import *

REG = f"{REG_DIR}/{AGENT}.csv"
if os.path.exists(REG):
    os.remove(REG)
sig = pd.read_parquet(f"{OUT}/signals_spot.parquet")
vp = load_viop()
Y = {h: vp[f"fwd{h}"] for h in (1, 3, 5)}
rows = []


def run(fam, tid, col, x, h, note="", y=None, viop=True):
    xx = x.reindex(vp.index) if viop else x
    yy = Y[h] if y is None else y
    st = split_stats(xx, yy, h)
    register(AGENT, fam, tid, col, h, st, note)
    r = dict(fam=fam, test_id=tid, col=col, h=h, note=note, **{k: v for k, v in st.items() if k != "by_year"})
    r["by_year"] = st["by_year"]
    rows.append(r)
    return st


# A: yuvarlanan beta artığı (kümülatif k gün, standartlaştırılmış)
models = ["XAG", "DXY", "TBOND", "SPX", "USDJPY", "USDCNH", "BTC", "EURUSD", "MACRO3", "FX3", "ALL7"]
for m in models:
    for W in (60, 120, 250):
        for k in (1, 3, 5):
            c = f"R_{m}_W{W}_k{k}"
            for h in (1, 3, 5):
                run("A_resid", f"A_{m}_W{W}_k{k}_h{h}", c, sig[c], h, "artik z; negatif IC = donus, pozitif = surme")
# A-dec: faktörün ima ettiği hareket (W=120 önceden sabit) ve altının kendi getirisi
for m in models:
    c = f"F_{m}_W120"
    for h in (1, 3, 5):
        run("A_fitted", f"AF_{m}_W120_h{h}", c, sig[c], h, "beta*x / sigma (fitted kısım)")
for k in (1, 3, 5):
    gk = sig.g.rolling(k).sum()
    for h in (1, 3, 5):
        run("A_own", f"AO_g_k{k}_h{h}", f"g_sum{k}", gk, h, "altının kendi 15->15 getirisi (kontrol)")
# B: oranlar
for L in (20, 60, 120):
    for h in (1, 3, 5):
        run("B_ratio", f"B_GSRZ_L{L}_h{h}", f"GSRZ_L{L}", sig[f"GSRZ_L{L}"], h, "log(XAU/XAG) 15:00 z")
        run("B_ratio", f"B_GPTZ_L{L}_h{h}", f"GPTZ_L{L}", sig[f"GPTZ_L{L}"], h, "log(GC/PL) Yahoo t-1 z")
for k in (1, 3, 5):
    for h in (1, 3, 5):
        run("B_ratio", f"B_GSRD_k{k}_h{h}", f"GSRD_k{k}", sig[f"GSRD_k{k}"], h, "dlog(XAU/XAG) k gun, 15:00")
        run("B_ratio", f"B_GPTD_k{k}_h{h}", f"GPTD_k{k}", sig[f"GPTD_k{k}"], h, "dlog(GC/PL) k gun Yahoo t-1")
# B tanı: oran (altın - gümüş) ileri yayılımı döndürüyor mu? (iki bacaklı, spot 15:00 -> 15:00)
for h in (1, 3, 5):
    spread = sig[f"sfwd{h}"] - sig[f"xag_fwd{h}"]
    for c in ("GSRZ_L20", "GSRZ_L60", "GSRZ_L120", "GSRD_k1", "GSRD_k3", "GSRD_k5"):
        run("B_spread_diag", f"BS_{c}_h{h}", c, sig[c], h, "hedef = altın-gümüş spot spread (tanı)", y=spread, viop=False)
# C: gün içi eksik tepki 12->15 ve 07->15 (artık z; negatif IC = yetişme)
for m in ("DXY", "TBOND", "SPX", "MACRO3"):
    for W in (60, 120, 250):
        for h in (1, 3, 5):
            run("C_intraday", f"C_I12_{m}_W{W}_h{h}", f"I12_{m}_W{W}", sig[f"I12_{m}_W{W}"], h, "12-15 UTC artığı (g12 - beta x12)")
for W in (60, 120, 250):
    for h in (1, 3, 5):
        run("C_intraday", f"C_I07_MACRO3_W{W}_h{h}", f"I07_MACRO3_W{W}", sig[f"I07_MACRO3_W{W}"], h, "07-15 UTC artığı")
        # koşullu: yalnız faktör hareketinin büyük olduğu günler (|fit z| IS 80. yüzdelik üstü)
        f = sig[f"I12F_MACRO3_W{W}"].reindex(vp.index); thr = f.abs()[f.index <= IS_END].quantile(0.8)
        xc = sig[f"I12_MACRO3_W{W}"].reindex(vp.index).where(f.abs() > thr)
        run("C_intraday", f"C_I12c_MACRO3_W{W}_h{h}", f"I12_MACRO3_W{W}|fit>q80", xc, h, f"yalnız |fit|>{thr:.2f} (IS q80)")
        run("C_intraday", f"C_I12F_MACRO3_W{W}_h{h}", f"I12F_MACRO3_W{W}", sig[f"I12F_MACRO3_W{W}"], h, "12-15 faktör ima hareketi (fitted)")
# E: VİOP kapanışta hesaplanan altın/gümüş (v_settle / vo_xag_settle; 15:10 UTC, uzlaşmayla eş zamanlı) ve t-1 sürümü
lv = np.log(vp.v_settle / vp.vo_xag_settle)
same = (vp.v_code.str[-4:] == vp.vo_xag_code.astype(str).str[-4:])
lvr = (vp.v_ret - vp.vo_xag_ret)  # kontrat içi getiriler -> roll'dan bağımsız
for L in (20, 60, 120):
    z = (lv - lv.rolling(L, min_periods=int(0.8 * L)).mean()) / lv.rolling(L, min_periods=int(0.8 * L)).std()
    for h in (1, 3, 5):
        run("E_viop_close", f"E_VGSRZ_L{L}_h{h}", f"VGSRZ_L{L}", z, h, "KAPANISTA HESAPLANAN (15:10 UTC)", viop=False)
for k in (1, 3, 5):
    sd = lvr.rolling(120, min_periods=60).std().shift(1)
    z = lvr.rolling(k).sum() / (sd * np.sqrt(k))
    for h in (1, 3, 5):
        run("E_viop_close", f"E_VGSRD_k{k}_h{h}", f"VGSRD_k{k}", z, h, "KAPANISTA HESAPLANAN (15:10 UTC)", viop=False)
        run("E_viop_close", f"E_VGSRD_k{k}_lag1_h{h}", f"VGSRD_k{k}.shift1", z.shift(1), h, "t-1 surumu", viop=False)

G = pd.DataFrame(rows)
G["p"] = 2 * (1 - __import__("scipy").stats.norm.cdf(G.t.abs()))
G.to_csv(f"{OUT}/grid_viop.csv", index=False)
print("toplam test:", len(G))
print(G.groupby("fam").agg(n=("t", "size"), n_abs_t_gt2=("t", lambda s: int((s.abs() > 2).sum())), max_abs_t=("t", lambda s: s.abs().max())).round(2))
print(G.reindex(G.t.abs().sort_values(ascending=False).index).head(25)[["test_id", "ic", "t", "t_is", "t_oos", "ic_oos", "yrs_same_sign", "yrs", "n"]].round(3).to_string())
