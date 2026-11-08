"""(d) Caldara–Iacoviello günlük GPR -> VİOP fwd{h}.
Bilgi zamanı: panelde gün D değeri D+1 23:00 UTC'de mevcut varsayıldı -> gün t'de en son D = t-2. Gerçek zamanlı yayın haftalık güncelleniyor
olabilir ve geçmiş değerler revize edilebilir (indirme 2026) -> sonuçlar en iyi ihtimalle DÜŞÜK güven.
NOT: panel_viop/panel_spot içindeki gpr_* sütunları SABİT (97,67) — panel kurucudaki tarih dönüşümü bozuk. Burada ham dosyadan
(data/misc/gpr_daily.xls, DAY=YYYYMMDD) yeniden kuruldu: gün t için D ≤ t−2 takvim günü olan son değer (D+1 23:00 UTC < t 15:00 UTC).
"""
from common import *

GR = pd.read_excel(f"{S}/data/misc/gpr_daily.xls")
GR["d"] = pd.to_datetime(GR["DAY"].astype(str), format="%Y%m%d"); GR = GR.set_index("d").sort_index()[["GPRD", "GPRD_ACT", "GPRD_THREAT", "GPRD_MA30", "GPRD_MA7"]].astype(float)

def gpr_asof(days):
    days = pd.DatetimeIndex(days)
    out = GR.reindex(GR.index.union(days - pd.Timedelta(days=2))).ffill().reindex(days - pd.Timedelta(days=2))
    out.index = days
    return out

def build(P):
    F = pd.DataFrame(index=P.index)
    G = gpr_asof(P.index)
    g = np.log(G["GPRD"].clip(lower=1)); th = np.log(G["GPRD_THREAT"].clip(lower=1)); ac = np.log(G["GPRD_ACT"].clip(lower=1))
    P = G.rename(columns=lambda c: "gpr_" + c)
    # panel gün endeksinde as-of değerler; değer değişmediyse (hafta sonu yok) yine de seviye; değişim için yalnız yeni değer günleri
    F["gpr_shock30"] = g - np.log(P["gpr_GPRD_MA30"].clip(lower=1))
    F["gpr_z250"] = zroll(g, 250)
    F["gpr_d1"] = g.diff()
    F["gpr_threat_shock"] = th - th.rolling(22, min_periods=15).mean()
    F["gpr_act_shock"] = ac - ac.rolling(22, min_periods=15).mean()
    F["gpr_ma7_vs_ma30"] = np.log(P["gpr_GPRD_MA7"].clip(lower=1)) - np.log(P["gpr_GPRD_MA30"].clip(lower=1))
    return F

X = build(D)
X.to_csv(f"{OUT}/d_gpr_features.csv")
DESC = {"gpr_shock30": "GPR log(GPRD/MA30)", "gpr_z250": "GPR log seviye 250g z", "gpr_d1": "GPR günlük log değişim",
        "gpr_threat_shock": "GPR tehdit alt endeksi şoku (22g)", "gpr_act_shock": "GPR eylem alt endeksi şoku (22g)", "gpr_ma7_vs_ma30": "GPR MA7/MA30"}
rows = []
for k, d in DESC.items():
    rows += T(X[k], "gpr", k, d, note="bilgi t-2 (varsayım); yayın zamanlaması belirsiz -> DUSUK")
df = save(rows, "d_gpr_ic"); show(df)

# uç olay kuralı: IS'te GPR şokunun %95 eşiği aşılınca uzun (güvenli liman hipotezi), h=1,3,5
thr = X["gpr_shock30"][X.index <= IS_END].quantile(0.95)
pos = (X["gpr_shock30"] > thr).astype(float)
print("IS %95 eşik:", round(thr, 3), "aktif gün:", int(pos.sum()))
rr = []
for h in (1, 3, 5):
    s = rule_stats(pos, h); register(AG, "gpr_rule", "gpr_extreme95_long", "GPR şoku > IS %95 -> uzun", h, s, "kural; aktif günlerde fwd ort. (bps)")
    s2 = rule_stats(pos, h, demean=True); register(AG, "gpr_rule", "gpr_extreme95_long_dm", "GPR şoku > IS %95 -> uzun (drift çıkarılmış)", h, s2, "kural demeaned")
    rr.append(dict(h=h, mean_bps=s["ic"], t=s["t"], n=s["n"], t_is=s["t_is"], t_oos=s["t_oos"], mean_dm_bps=s2["ic"], t_dm=s2["t"]))
print(pd.DataFrame(rr).round(2).to_string(index=False)); pd.DataFrame(rr).to_csv(f"{OUT}/d_gpr_rule.csv", index=False)

Xs = build(SP)
rows3 = []
for k, d in DESC.items():
    rows3 += T_early(Xs[k], "gpr", k, d)
df3 = save(rows3, "d_gpr_early"); show(df3, ("test_id", "h", "n", "ic", "t", "yrs_same"))
