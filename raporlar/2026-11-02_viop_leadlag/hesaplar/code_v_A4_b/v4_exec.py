"""v4: açılış fiyatı gerçekçiliği ve VİOP pay vadelisi ile işlenebilirlik.
 (a) h1 (2023-11-30+): giriş/çıkış alternatifleri.
 (b) VİOP bülteni (2017-2026, eldeki tüm günler): en yüksek hacimli vadeli, açılış->kapanış; likidite filtreleri;
     Yahoo spot gün-içi ile vadeli gün-içi korelasyonu yıllara göre (Yahoo açılışının 2017-2022 gerçekçiliği için dolaylı kontrol).
"""
import sys, glob; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_A4_b")
from core import *
pd.set_option("display.width", 250)
SG = pd.read_parquet(RES + "/signals.parquet"); AIR = SG.AIR_C
TGT = ["THYAO", "PGSUS", "TAVHL"]

# ---------- (a) saatlik
print("== (a) Saatlik giriş/çıkış alternatifleri (2023-11-30..2026-10-30), brüt bps (iid t) ve 8 bps net ==")
rows = []
for st in TGT:
    h = raw(st + ".IS", "h1").copy(); h["hm"] = h.index.strftime("%H:%M"); h["d"] = pd.DatetimeIndex(h.ldate).normalize()
    dd = bist_day(st + ".IS")
    g = h.groupby("d")
    first = h[h.hm == "06:30"].set_index("d"); second = h[h.hm == "07:30"].set_index("d"); third = h[h.hm == "08:30"].set_index("d")
    lastc = h[h.hm.isin(["13:30", "14:30"])].groupby("d").c.last()
    E = pd.DataFrame({"o_d": dd.o, "c_d": dd.c})
    E["e_1030"] = first.c; E["e_1130"] = second.c; E["e_1230"] = third.c
    E["e_vw1"] = (first.h + first.l + first.c) / 3          # ilk saat tipik fiyat (VWAP vekili)
    E["e_vw2"] = (second.h + second.l + second.c) / 3       # ikinci saat tipik fiyat
    E["x_last_cont"] = lastc
    E = E.dropna(subset=["e_1030"]); E = E[E.index >= "2023-11-30"]
    # temizlik: kurumsal işlem günleri
    E = E[dd.intra.reindex(E.index).notna()]
    variants = {
        "açılış->kapanış(müzayede)": np.log(E.c_d / E.o_d),
        "10:30->kapanış": np.log(E.c_d / E.e_1030),
        "ilk saat tipik->kapanış": np.log(E.c_d / E.e_vw1),
        "11:30->kapanış": np.log(E.c_d / E.e_1130),
        "ikinci saat tipik->kapanış": np.log(E.c_d / E.e_vw2),
        "12:30->kapanış": np.log(E.c_d / E.e_1230),
        "10:30->son sürekli bar": np.log(E.x_last_cont / E.e_1030),
        "açılış->10:30 (kaçan kısım)": np.log(E.e_1030 / E.o_d),
    }
    for nm, y in variants.items():
        r = bt(AIR, y, 8, 1.0); r15 = bt(AIR, y, 15, 1.0)
        rows.append({"tgt": st, "giriş": nm, "n": r["n"], "brüt": r["gross"], "t_brüt": r["t_g"], "net8": r["bps"], "t8": r["t"], "net15": r15["bps"]})
    # 2024-11+ (son 2 yıl) ayrıca
H = pd.DataFrame(rows); H.to_csv(RES + "/v4a_hourly.csv", index=False)
print(H.round(2).to_string(index=False))

# ---------- (b) VİOP bülteni
files = sorted(glob.glob(S + "/data/viop/viop_*.csv"))
recs = []
pref = tuple(f";F_{s}" for s in TGT + ["XU030"])
for f in files:
    with open(f, "rb") as fh:
        for line in fh:
            if b";F_THYAO" in line or b";F_PGSUS" in line or b";F_TAVHL" in line or b";F_XU030" in line:
                p = line.decode("windows-1254", "replace").strip().split(";")
                if len(p) < 23: continue
                code = p[1]
                und = p[7].split(".")[0]
                if und not in TGT + ["XU030"]: continue
                if not code.startswith("F_" + und) or "M" in code[len("F_" + und):len("F_" + und) + 1]: continue
                def fl(x):
                    try: return float(x)
                    except: return np.nan
                recs.append({"date": p[0], "code": code, "und": und, "exp": p[8], "settle": fl(p[9]), "open": fl(p[12]), "low": fl(p[13]), "high": fl(p[14]), "close": fl(p[15]),
                             "vwap": fl(p[16]), "tl": fl(p[17]), "qty": fl(p[19]), "ntr": fl(p[20]), "oi": fl(p[21]),
                             "os_px": fl(p[23]) if len(p) > 23 else np.nan, "os_ntr": fl(p[27]) if len(p) > 27 else np.nan})
V = pd.DataFrame(recs); V["date"] = pd.to_datetime(V.date)
V = V[(V.tl > 0) & (V.open > 0) & (V.close > 0)]
F = V.sort_values("tl").groupby(["und", "date"]).tail(1).set_index(["und", "date"]).sort_index()
F.to_parquet(RES + "/v4b_viop_front.parquet")
print("\n== (b) VİOP en yüksek hacimli vadeli: gün sayısı ==", F.groupby(level=0).size().to_dict())
rows = []; yrs = {}
for st in TGT:
    f = F.loc[st].copy()
    y_f = np.log(f.close / f.open)
    y_fv = np.log(f.close / f.vwap)   # VWAP -> kapanış (çok muhafazakâr: günün ortalama fiyatından giriş)
    sp = bist_day(st + ".IS")
    yi = sp.intra.reindex(f.index)
    j = pd.concat([y_f.rename("f"), yi.rename("s")], axis=1).dropna()
    cy = j.groupby(j.index.year).apply(lambda g: g.f.corr(g.s)).round(3).to_dict()
    print(f"{st}: corr(vadeli gün-içi, Yahoo spot gün-içi) yıllara göre: {cy}")
    # Yahoo spot açılışı ile vadeli açılışı arası fark (baz düzeltmeli): log(o_s/c_s) - log(o_f/c_f) dağılımı
    df_ = pd.concat([np.log(sp.o / sp.c).reindex(f.index).rename("s"), np.log(f.open / f.close).rename("f")], axis=1).dropna()
    dif = (df_.s - df_.f)
    print(f"   |açılış farkı (spot-vadeli, kapanışa göre)| medyan bps yıllara göre:", (1e4 * dif.abs().groupby(dif.index.year).median()).round(1).to_dict())
    liq = f.tl.groupby(f.index.year).median() / 1e6; ntr = f.ntr.groupby(f.index.year).median()
    print(f"   medyan günlük işlem hacmi (mn TL): {liq.round(1).to_dict()}; medyan işlem sayısı: {ntr.to_dict()}")
    if f.os_ntr.notna().any():
        o2 = f[f.os_ntr.notna()]
        print(f"   açılış seansı: işlem olan gün oranı {(o2.os_ntr > 0).mean():.2f}, medyan açılış seansı işlem sayısı {o2.os_ntr.median():.0f} (n gün {len(o2)})")
    for lab, yy, flt in [("vadeli açılış->kapanış", y_f, None), ("vadeli açılış->kapanış (işlem sayısı>=50)", y_f, f.ntr >= 50),
                         ("vadeli VWAP->kapanış", y_fv, None), ("spot (aynı günler)", yi, None)]:
        yv = yy if flt is None else yy[flt]
        for per in ["ALL", "IS", "OOS", "24-26"]:
            r = bt(AIR, yv, 8, 1.0, *PER[per]); r15 = bt(AIR, yv, 15, 1.0, *PER[per])
            rows.append({"tgt": st, "seri": lab, "per": per, "n": r["n"], "brüt": r["gross"], "t_brüt": r.get("t_g"), "net8": r["bps"], "t8": r["t"], "net15": r15["bps"], "t15": r15["t"]})
    g, _ = pnl_series(AIR, y_f); yrs[st] = (1e4 * g.groupby(g.index.year).mean()).round(1); yrs[st + "_n"] = g.groupby(g.index.year).size()
VB = pd.DataFrame(rows); VB.to_csv(RES + "/v4b_viop_bt.csv", index=False)
print(VB.round(2).to_string(index=False))
print("\nVİOP vadeli brüt bps/işlem yıllara göre:\n", pd.DataFrame(yrs).T.to_string())
