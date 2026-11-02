"""A4: backtestler. Look-ahead yok: ABD/Avrupa sürücüsü_{t-1} (BIST kapanışı t-1'den SONRA kapanır, BIST t açılışından ÖNCE bilinir)
-> BIST t açılışında gir, t kapanışında çık (hedef = intra_t). Maliyet 8/10/15 bps gidiş-dönüş. IS 2014-2020 / OOS 2021-2026.
Çıktı: res_bt.csv + res_bt_years.csv"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kc import *
HERE = os.path.dirname(os.path.abspath(__file__))


def basket(syms, start="2005-01-01"):
    X = pd.concat([R(s).rename(s) for s in syms], axis=1)
    X = X[X.index >= start]
    # her sembolü 250g kayan oynaklığa böl (look-ahead yok: shift(1)), sonra ortalama
    vol = X.rolling(250, min_periods=60).std().shift(1)
    return (X / vol).mean(axis=1, skipna=True)


SPECS = []
US_FERT = ["CF", "MOS", "NTR", "IPI", "LXU", "UAN"]
EU_CEM = ["HEI.DE", "HOLN.SW", "BZU.MI"]
US_CEM = ["VMC", "MLM", "CX", "CRH", "EXP"]
GLASS = ["SGO.PA", "OI", "VID.MC"]
fert_b = basket(US_FERT); eucem_b = basket(EU_CEM); uscem_b = basket(US_CEM); glass_b = basket(GLASS)

# (ad, sinyal (t günü bilinir), hedef hisse, mod, eşik, açıklama)
for tgt in ["GUBRF", "HEKTS", "TKFEN"]:
    SPECS.append((f"BT1 ABD gübre sepeti_t-1 -> {tgt} intra_t", fert_b.shift(1), tgt, "intra", "sign", 0.0))
    SPECS.append((f"BT1z ABD gübre sepeti_t-1 |z|>1 -> {tgt} intra_t", fert_b.shift(1), tgt, "intra", "z", 1.0))
    SPECS.append((f"BT1d ABD gübre sepeti_t -> {tgt} t+2..t+5 (t+1 kapanışında gir)", fert_b, tgt, "drift", "z", 1.0))
for tgt in ["SISE", "GUBRF", "CIMSA", "OYAKC", "TKFEN"]:
    # TTF şoku: hipotez = gaz yukarı -> maliyet şoku -> hisse aşağı ⇒ pozisyon = -sign
    SPECS.append((f"BT2 TTF şoku_t-1 |z|>1 (ters) -> {tgt} intra_t", -R("TTF=F").shift(1), tgt, "intra", "z", 1.0))
    SPECS.append((f"BT2d TTF şoku_t |z|>1.5 (ters) -> {tgt} t+2..t+5", -R("TTF=F"), tgt, "drift", "z", 1.5))
SPECS.append(("BT2b NG=F şoku_t-1 |z|>1 (ters) -> SISE intra_t", -R("NG=F").shift(1), "SISE", "intra", "z", 1.0))
SPECS.append(("BT2c cam sepeti_t-1 -> SISE intra_t", glass_b.shift(1), "SISE", "intra", "sign", 0.0))
for tgt in ["CIMSA", "OYAKC"]:
    SPECS.append((f"BT3 AB çimento sepeti_t-1 -> {tgt} intra_t", eucem_b.shift(1), tgt, "intra", "sign", 0.0))
    SPECS.append((f"BT3z AB çimento sepeti_t-1 |z|>1 -> {tgt} intra_t", eucem_b.shift(1), tgt, "intra", "z", 1.0))
    SPECS.append((f"BT3u ABD çimento sepeti_t-1 |z|>1 -> {tgt} intra_t", uscem_b.shift(1), tgt, "intra", "z", 1.0))
# Yurt içi küme: küçük çimento hisseleri_t-1 (BIST kapanışında bilinir) -> CIMSA/OYAKC t (gap+intra = cc, kapanışta gir)
TRC = basket(["AKCNS.IS", "NUHCM.IS", "AFYON.IS", "BUCIM.IS", "KONYA.IS", "BTCIM.IS"], "2009-01-01")
for tgt in ["CIMSA", "OYAKC"]:
    SPECS.append((f"BT4 TR küçük çimento sepeti_t-1 (XU100 artığı) -> {tgt} cc_t", None, tgt, "cc_rel", "z", 1.0))
# Gübre kümesi: BAGFS/EGGUB t-1 -> GUBRF
SPECS.append(("BT5 BAGFS+EGGUB_t-1 -> GUBRF cc_t", None, "GUBRF", "cc_fert", "z", 1.0))


def target(stock, kind):
    dd = DEC(stock)
    if kind == "intra": return dd["intra"]
    if kind == "drift": return sum(R(stock).shift(-k) for k in range(2, 6))
    return R(stock)


rows = []; yrs = []
for name, sig, stock, kind, mode, thr in SPECS:
    if kind == "cc_rel":
        m = R("XU100"); rel = resid(TRC, [m]).reindex(TRC.index)
        sig = rel.shift(1); tg = R(stock)
    elif kind == "cc_fert":
        b = basket(["BAGFS.IS", "EGGUB.IS"], "2009-01-01"); rel = resid(b, [R("XU100")]).reindex(b.index)
        sig = rel.shift(1); tg = R(stock)
    else:
        tg = target(stock, kind)
    for cost in [0, 8, 10, 15]:
        res, pnl, pos = run_bt(sig, tg, cost, thr=thr, mode=mode)
        if kind == "drift":  # örtüşen 4 günlük tutuş: maliyet 4 güne yayılmadı; t NW(5) ile
            pass
        rows.append({"spec": name, "stock": stock, "cost_bps": cost,
                     **{f"{k}_{p}": res[p].get(k, np.nan) for p in ["IS", "OOS", "ALL"] for k in ["n", "mean_bps", "t", "hit", "sharpe", "maxdd_pct"]}})
        if cost == 10:
            yrs.append({"spec": name, **res["by_year_bps"]})
    print(f"{name:60s} | 10bps IS {rows[-2]['mean_bps_IS']:+6.1f}bps t{rows[-2]['t_IS']:+.1f} | OOS {rows[-2]['mean_bps_OOS']:+6.1f}bps t{rows[-2]['t_OOS']:+.1f} SR{rows[-2]['sharpe_OOS']:+.2f} | brüt OOS {rows[-4]['mean_bps_OOS']:+6.1f}", flush=True)
pd.DataFrame(rows).to_csv(os.path.join(HERE, "res_bt.csv"), index=False)
pd.DataFrame(yrs).to_csv(os.path.join(HERE, "res_bt_years.csv"), index=False)
