"""(g) Ana bulgu ayrıntısı: altın 15:00 ET (ya da 14:00 ET) hareketi -> GDXJ/GDX ertesi gün dönüşü, yalnız-uzun uygulama.
Kural (IS'te seçildi: eşik 0, h=1): gün t 15:00 ET'de m_t = ln(spot_15:00ET_t / spot_16:00ET_{t-1}) < 0 ise GDXJ'yi t kapanışında al, t+1 kapanışında sat
(ertesi gün yine koşul sağlanıyorsa pozisyon korunur, maliyet ödenmez). Aksi halde nakit.
"""
from common import *
import warnings; warnings.filterwarnings("ignore")
d = load_etf()
m = np.log(d.xau_cut / d.xau_close.shift(1))
x = pd.read_parquet(f"{P}/duka/XAUUSD.parquet")["c"]; x.index = (x.index + pd.Timedelta(hours=1)).tz_convert("America/New_York")
x14 = x[x.index.hour == 14]; x14.index = pd.to_datetime(x14.index.date); x14 = x14[~x14.index.duplicated()].reindex(d.index)
m14 = np.log(x14 / d.xau_close.shift(1))
out = {}
for tgt in ["GDXJ", "GDX"]:
    r = lr(d[f"c_{tgt}"]).dropna()
    for nm, sig in [("m15", m), ("m14", m14)]:
        pos = (sig < 0).astype(float).where(sig.notna(), 0.0)
        res = {}
        for c in (0.0, 10.0, 20.0, 40.0):
            net, wl, _ = bt(pos, r, 1, c)
            res[c] = segs(net)
        bh = segs(np.expm1(r))
        # başabaş maliyet (OOS): brüt yıllık getiri / yıllık devir
        net0, wl, _ = bt(pos, r, 1, 0.0)
        turn = wl.diff().abs()
        oos = net0.index > IS_END
        be = net0[oos].mean() / (turn.reindex(net0.index)[oos].mean()) * 2e4   # gidiş-dönüş bps
        # B&H'ye göre fazla: strateji − maruziyet×B&H ortalaması
        print(f"{tgt} {nm}: brüt/10/20/40 bps OOS Sharpe:", [res[c]["oos"]["sharpe"] for c in (0.0, 10.0, 20.0, 40.0)],
              "IS:", [res[c]["is"]["sharpe"] for c in (0.0, 10.0, 20.0, 40.0)], "22+:", [res[c]["22"]["sharpe"] for c in (0.0, 10.0, 20.0, 40.0)],
              "| B&H IS/OOS/22:", bh["is"]["sharpe"], bh["oos"]["sharpe"], bh["22"]["sharpe"], "| başabaş maliyet OOS (gidiş-dönüş bps):", round(be, 1),
              "| maruziyet:", round(wl.mean(), 2), "| işlem (gidiş-dönüş)/yıl:", round(turn.sum() / len(turn) * 252 / 2, 1))
        if tgt == "GDXJ" and nm == "m15":
            net, wl, _ = bt(pos, r, 1, 10.0)
            yr = pd.DataFrame({"strateji_%": net.groupby(net.index.year).sum() * 100, "BH_%": np.expm1(r).groupby(r.index.year).sum() * 100,
                               "gun_ici_%": wl.shift(1).groupby(wl.index.year).mean() * 100})
            # 'uzun gün' ve 'nakit gün' ortalama getirileri
            R = np.expm1(r); L = wl.shift(1).reindex(R.index)
            yr["uzun_gun_ort_bps"] = R[L == 1].groupby(R[L == 1].index.year).mean() * 1e4
            yr["nakit_gun_ort_bps"] = R[L == 0].groupby(R[L == 0].index.year).mean() * 1e4
            yr = yr.round(1); yr.to_csv(f"{OUT}/g_gdxj_yearly.csv"); print(yr.to_string())
            print("uzun-gün minus nakit-gün farkı, yıl sayısı > 0:", int((yr.uzun_gun_ort_bps > yr.nakit_gun_ort_bps).sum()), "/", len(yr))
            # kayıt
            register(AGENT, "g_main", "g_gdxj_m15_longonly_h1", "m_t<0 iken GDXJ uzun (h=1)", 1,
                     dict(ic=res[10.0]["full"]["ann"], t=res[10.0]["full"]["t"], n=res[10.0]["full"]["n"], t_is=res[10.0]["is"]["t"], t_oos=res[10.0]["oos"]["t"]),
                     note="strateji; ic=yıllık net getiri % (10 bps)")
        out[f"{tgt}_{nm}"] = {c: res[c] for c in res}
json.dump({k: {str(c): v for c, v in vv.items()} for k, vv in out.items()}, open(f"{OUT}/g_main_claim.json", "w"), default=float, indent=1)

# Kaldıraçlı uzun (JNUG / NUGT) yalnız-uzun sürüm — bilgi amaçlı, 20/40 bps
for le, un in [("JNUG", "GDXJ"), ("NUGT", "GDX")]:
    r = lr(d[f"c_{le}"]).dropna()
    pos = (m < 0).astype(float).where(m.notna(), 0.0)
    for c in (20.0, 40.0):
        net, wl, _ = bt(pos, r, 1, c)
        s_ = segs(net); bh = segs(np.expm1(r))
        print(le, c, "bps: Sharpe IS/OOS/22:", s_["is"]["sharpe"], s_["oos"]["sharpe"], s_["22"]["sharpe"], "| B&H:", bh["is"]["sharpe"], bh["oos"]["sharpe"], bh["22"]["sharpe"],
              "| OOS yıllık %:", s_["oos"]["ann"], "vol %:", s_["oos"]["vol"])
