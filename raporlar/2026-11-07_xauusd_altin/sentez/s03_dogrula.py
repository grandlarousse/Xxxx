"""s03: Ayakta kalan sinyallerin pozisyonlarını kur, analist rakamlarıyla karşılaştır, dönem özetlerini kaydet.
Çıktı: sinyal_pozisyonlari.parquet (VİOP ve ETF ayrı), dogrulama.csv"""
import json, numpy as np, pandas as pd
from sl import *
OUT = f"{S}/out/sentez"

SIG = {}
# VİOP
p, q, rvA = sig_lowmom(); pv = to_viop(p).fillna(0.0); pv[pv.index.isin(HALF_TR)] = 0.0  # veri notu (1): TR yarım günleri dışlandı
SIG["V_LOWMOM_h1"] = dict(front="VIOP", pos=pv, h=1, r=RV, cost=5.0, ref="OOS ham 1,36 / dm 1,31; tam dm 0,99")
SIG["V_LOWMOM_h5"] = dict(front="VIOP", pos=pv, h=5, r=RV, cost=5.0, ref="OOS ham 1,69 / dm 1,63; tam dm 0,95")
SIG["V_QEND_h3"] = dict(front="VIOP", pos=sig_qend(), h=3, r=RV, cost=5.0, ref="OOS 0,99 / dm 0,87")
pg, zg = sig_gdxj_res_viop()
SIG["V_GDXJRES_h3"] = dict(front="VIOP", pos=pg, h=3, r=RV, cost=5.0, ref="tam 0,53 / OOS 0,72 / IS 0,24")
pl, xl = sig_last1h()
SIG["V_LAST1H_h5"] = dict(front="VIOP", pos=pl, h=5, r=RV, cost=5.0, ref="tam 0,515 / OOS 0,63 / dm 0,57")
# ETF (yalnız uzun)
pt, ev = sig_gdx_tatil()
SIG["E_GDXTATIL_h1"] = dict(front="ETF", pos=pt.reindex(E.index).fillna(0), h=1, r=ret_of("GDX"), cost=10.0, ref="OOS 0,75 / dm 0,65 / B&H 0,61")
p2j, x2j, hi2j, lo2j = sig_e2("GDXJ", 1, 0.7)
SIG["E_C2J_h3"] = dict(front="ETF", pos=p2j.clip(lower=0), h=3, r=ret_of("GDXJ"), cost=10.0, ref="OOS yalnız uzun 0,64 / dm 0,40 / B&H 0,31")
p2, x2, hi2, lo2 = sig_e2("GDX", 3, 0.7)
SIG["E_C2_h3"] = dict(front="ETF", pos=p2.clip(lower=0), h=3, r=ret_of("GDX"), cost=10.0, ref="OOS yalnız uzun 0,58 / dm 0,29 / B&H 0,41")
p1, x1, hi1, lo1 = sig_e2("GDX", 10, 0.8)
SIG["E_C1_h5"] = dict(front="ETF", pos=p1.clip(lower=0), h=5, r=ret_of("GLD"), cost=10.0, ref="OOS yalnız uzun 0,73 / B&H 0,72")
SIG["E_C1kap_h5"] = dict(front="ETF", pos=(p1 > -1).astype(float).where(x1.notna(), 1.0), h=5, r=ret_of("GLD"), cost=10.0, ref="kaplama OOS 0,90")
pm, mm = sig_m()
SIG["E_M_GDXJ_h1"] = dict(front="ETF", pos=pm, h=1, r=ret_of("GDXJ"), cost=10.0, ref="OOS 0,72 (10 bps) / 0,51 (20 bps) / B&H 0,54")

rows = []
for k, s in SIG.items():
    for simple in (False, True):
        o = summarize(s["pos"], s["r"], s["h"], s["cost"], s["front"], simple=simple)
        for per, v in o.items():
            rows.append(dict(sinyal=k, getiri="basit" if simple else "log", donem=per, **v))
        print(k, "basit" if simple else "log  ", "| ref:", s["ref"])
        print("   ", {per: (v["sharpe"], v["sharpe_dm"], v["bh_sharpe"]) for per, v in o.items()})
R = pd.DataFrame(rows); R.to_csv(f"{OUT}/dogrulama.csv", index=False)

# işlem başı etki ve yılda işlem (olay tabanlı): pozisyon açılış günleri ve h günlük brüt getiri
ev_rows = []
for k, s in SIG.items():
    pos = s["pos"].reindex(s["r"].index).fillna(0); r = s["r"].astype(float)
    f = sum(r.shift(-j) for j in range(1, s["h"] + 1))
    act = pos != 0
    g = (pos * f)[act].dropna()
    yrs = (r.dropna().index[-1] - r.dropna().index[0]).days / 365.25
    # 'işlem' = aktif gün başına h günlük alt portföy (kademeli); gidiş-dönüş sayısı = netleşmiş ciro/2
    net, turn = bt_eff(eff_of(pos, s["h"]), r.dropna(), s["cost"])
    ev_rows.append(dict(sinyal=k, aktif_gun=int(act.sum()), aktif_gun_yil=round(act.sum() / yrs, 1), brut_bps_aktif_gun=round(g.mean() * 1e4, 1),
                        brut_bps_oos=round(g[g.index > (V_IS_END if s["front"] == "VIOP" else E_IS_END)].mean() * 1e4, 1),
                        gidis_donus_yil=round(turn.sum() / len(net) * 252 / 2, 1), maruziyet=round(float(eff_of(pos, s["h"]).abs().mean()), 3)))
EV = pd.DataFrame(ev_rows); EV.to_csv(f"{OUT}/islem_basi.csv", index=False)
print(EV.to_string())

# pozisyon (etkin, kademeli) serileri
VP = pd.DataFrame({k: eff_of(s["pos"].reindex(V.index).fillna(0), s["h"]) for k, s in SIG.items() if s["front"] == "VIOP"})
EP = pd.DataFrame({k: eff_of(s["pos"].reindex(E.index).fillna(0), s["h"]) for k, s in SIG.items() if s["front"] == "ETF"})
VP.to_parquet(f"{OUT}/poz_viop.parquet"); EP.to_parquet(f"{OUT}/poz_etf.parquet")
VR = pd.DataFrame({k: s["pos"].reindex(V.index).fillna(0) for k, s in SIG.items() if s["front"] == "VIOP"})
ER = pd.DataFrame({k: s["pos"].reindex(E.index).fillna(0) for k, s in SIG.items() if s["front"] == "ETF"})
VR.to_parquet(f"{OUT}/sinyal_viop_ham.parquet"); ER.to_parquet(f"{OUT}/sinyal_etf_ham.parquet")
# net PnL serileri (tam dönem, temel maliyet)
VN = pd.DataFrame({k: bt_eff(eff_of(s["pos"].reindex(s["r"].index).fillna(0), s["h"]), s["r"].dropna(), s["cost"])[0] for k, s in SIG.items() if s["front"] == "VIOP"})
EN = pd.DataFrame({k: bt_eff(eff_of(s["pos"].reindex(s["r"].index).fillna(0), s["h"]), s["r"].dropna(), s["cost"])[0] for k, s in SIG.items() if s["front"] == "ETF"})
VN.to_parquet(f"{OUT}/pnl_viop.parquet"); EN.to_parquet(f"{OUT}/pnl_etf.parquet")
json.dump(dict(e2_esik=dict(C2J=[hi2j, lo2j], C2=[hi2, lo2], C1=[hi1, lo1])), open(f"{OUT}/esikler.json", "w"), indent=1)
