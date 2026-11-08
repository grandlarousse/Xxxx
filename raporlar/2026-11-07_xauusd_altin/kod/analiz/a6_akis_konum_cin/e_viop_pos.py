"""(e) VİOP yerel konumlanma ve akış -> VİOP fwd{h}.
Bilgi zamanı: VİOP bülteni (OI, hacim) gün t seans sonu (15:15 UTC) sonrasında kesinleşir -> gün t 15:00 UTC kararında yalnız t-1 ve öncesi bilinir.
ANA sürüm: bütün özellikler t-1 (shift(1)). 'Aynı gün' sürümü ayrıca verilir ve 'kapanışta/kapanış sonrası hesaplanan' diye işaretlidir (uygulanamaz üst sınır).
OI değişimi: vadesi o gün dolan kontrat hariç bütün vadelerin oi_chg toplamı (vade sonu mekanik düşüşü ve roll aktarımı netleşir).
"""
from common import *

L = pd.read_parquet(f"{S}/panel/viop_long.parquet"); L["date"] = pd.to_datetime(L["date"]); L["expiry"] = pd.to_datetime(L["expiry"])

def oi_flow(root):
    x = L[L.root == root].copy()
    live = x[x.expiry > x.date]
    g = live.groupby("date").agg(doi=("oi_chg", "sum"), oi=("oi", "sum"), vol=("volume", "sum"), val=("value", "sum"))
    tot = x.groupby("date").agg(oi_all=("oi", "sum"), vol_all=("volume", "sum"))
    g = g.join(tot)
    g["doi_rel"] = g.doi / (g.oi - g.doi).replace(0, np.nan)          # yüzde OI değişimi (vadesi dolmayanlar)
    return g.reindex(D.index)

xu = oi_flow("XAUUSD"); xt = oi_flow("XAUTRYM")

def feats(lag):
    """lag=1: gün t kararında bilinen (t-1 bülteni). lag=0: aynı gün (kapanış sonrası; uygulanamaz)."""
    F = pd.DataFrame(index=D.index)
    r1 = D["v_ret"]; r5 = r1.rolling(5).sum()
    doi1 = xu.doi_rel; doi5 = xu.doi_rel.rolling(5).sum()
    lv = np.log(xu.vol_all); vsh = lv - lv.rolling(20, min_periods=15).median().shift(1)
    F["oi_d1"] = doi1
    F["oi_d5"] = doi5
    F["oi_d1_x_sgnret"] = doi1 * np.sign(r1)
    F["oi_d5_x_sgnret5"] = doi5 * np.sign(r5)
    F["vol_shock"] = vsh
    F["vol_shock_x_sgnret"] = vsh * np.sign(r1)
    F["oi_lvl_z250"] = zroll(np.log(xu.oi_all), 250)
    F["xt_oi_d5"] = xt.doi_rel.rolling(5).sum()
    lvt = np.log(xt.vol_all); F["xt_vol_shock"] = lvt - lvt.rolling(20, min_periods=15).median().shift(1)
    F["xt_oi_d5_x_sgnret5"] = F["xt_oi_d5"] * np.sign(D["vo_xautry_ret"].rolling(5).sum())
    # gram altın / ons altın OI oranı değişimi (yerli perakende TL-altın ilgisi vs USD-altın)
    F["xt_xu_oi_ratio_d5"] = np.log(xt.oi_all / xu.oi_all).diff(5)
    F["xt_oi_lvl_z250"] = zroll(np.log(xt.oi_all), 250)          # gram altın vadeli OI kalabalık seviyesi
    return F.shift(lag)

X1 = feats(1); X0 = feats(0)
X1.to_csv(f"{OUT}/e_viop_features_t1.csv")
DESC = {"oi_d1": "XAUUSD OI günlük % değişim (t-1)", "oi_d5": "XAUUSD OI 5g % değişim (t-1)", "oi_d1_x_sgnret": "OI Δ1 × sign(v_ret) (t-1)",
        "oi_d5_x_sgnret5": "OI Δ5 × sign(5g getiri) (t-1)", "vol_shock": "XAUUSD hacim şoku log/20g medyan (t-1)", "vol_shock_x_sgnret": "hacim şoku × sign(getiri) (t-1)",
        "oi_lvl_z250": "XAUUSD toplam OI seviye 250g z (t-1)", "xt_oi_d5": "XAUTRYM (gram altın) OI 5g % değişim (t-1)", "xt_vol_shock": "XAUTRYM hacim şoku (t-1)",
        "xt_oi_d5_x_sgnret5": "XAUTRYM OI Δ5 × sign(gram 5g getiri) (t-1)", "xt_xu_oi_ratio_d5": "log(XAUTRYM OI / XAUUSD OI) 5g değişim (t-1)",
        "xt_oi_lvl_z250": "XAUTRYM toplam OI seviye 250g z — yerli kalabalık (t-1)"}
rows = []
for k, d in DESC.items():
    rows += T(X1[k], "viop_pos", f"vp_{k}", d, note="t-1 bülteni; gün t 15:00 UTC'de bilinir")
df = save(rows, "e_viop_ic"); show(df)

rows0 = []
for k, d in DESC.items():
    rows0 += T(X0[k], "viop_pos_sameday", f"vp_{k}_sameday", d.replace("(t-1)", "(AYNI GÜN — kapanış sonrası, uygulanamaz)"), hs=(1, 5), note="KAPANIŞTA/SONRASINDA HESAPLANAN")
df0 = save(rows0, "e_viop_ic_sameday"); show(df0)

# sağlamlık: roll günleri (±1 gün) ve uç dönemler hariç
rows2 = []
for k in DESC:
    rows2 += T(X1[k], "viop_pos_robust", f"vp_{k}_exroll_ext", DESC[k] + " roll±1 ve uç dönem hariç", hs=(1, 5), y_mask=(ROLL_NEAR | EXTREME), note="robust")
df2 = save(rows2, "e_viop_robust"); show(df2)
