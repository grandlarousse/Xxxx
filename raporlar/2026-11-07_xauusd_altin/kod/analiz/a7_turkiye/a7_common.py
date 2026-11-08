"""a7_turkiye ortak yardımcılar: veri yükleme, Türkiye'ye özgü öngörücüler, kayıt sarmalayıcıları.
Bilgi zamanları (UTC):
  v_*, vo_*, tr_prem_matched  : gün t ~15:10 UTC (uzlaşma VWAP 15:00-15:10; yarım günlerde ~09:40)  -> sinyalde yalnız t-1 (shift(1)) ya da 'kapanışta' (K) etiketiyle
  dk_USDTRY_p15               : gün t 15:00 UTC (Dukascopy saatlik bar kapanışı)                     -> gün t sinyalinde kullanılabilir
  dk_USDTRY_p07               : gün t 07:00 UTC
  xau_p15                     : gün t 15:00 UTC
  y_XU030_IS                  : BIST kapanışı t-1 (15:10 UTC t-1 ya da önce)
  ust_nom3m                   : t-1 değeri (22:00 UTC t-1)
"""
import sys, os, numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
sys.path.insert(0, f"{S}/code")
from lib_altin import *  # noqa
import lib_altin as L
OUT = f"{S}/out/a7_turkiye"
AG = "a7_turkiye"
REGF = f"{L.REG_DIR}/{AG}.csv"


def reset_family(fam):
    """Betik yeniden çalıştırıldığında aynı aileye ait eski kayıtları sil (çift sayımı önler)."""
    if os.path.exists(REGF):
        r = pd.read_csv(REGF)
        r = r[r.family != fam]
        r.to_csv(REGF, index=False)


def zs(x, w=60, minp=20):
    """Geçmişe dayalı z-skoru (yalnız t ve öncesi)."""
    m = x.rolling(w, min_periods=minp).mean(); s = x.rolling(w, min_periods=minp).std()
    return (x - m) / s


def hourly_px(sym):
    h = L.hourly(sym).copy()
    h.index = (h.index + pd.Timedelta(hours=1)).tz_convert(None)  # fiyat anı = bar sonu
    return h["c"]


def half_days(p):
    """Yarım gün tespiti: uzlaşma 09:40 UTC spotuna 15:00 spotundan çok daha yakınsa.
    Komşu günlerin baz ortalaması (aynı kontrat) taşıma maliyetini temsil eder."""
    c = hourly_px("XAUUSD")
    s10 = pd.Series([c.get(d + pd.Timedelta(hours=10), np.nan) for d in p.index], index=p.index)
    s15 = p["xau_p15"]
    b15 = np.log(p.v_settle / s15); b10 = np.log(p.v_settle / s10)
    same = (p.v_code == p.v_code.shift(1)) & (p.v_code == p.v_code.shift(-1))
    nb = (b15.shift(1) + b15.shift(-1)) / 2
    d15 = (b15 - nb).abs(); d10 = (b10 - nb).abs()
    # Resmi yarım gün takvimi (Ramazan ve Kurban Bayramı arifeleri + 28 Ekim), hafta içi olanlar.
    # Veri kontrolü (a7_01_audit): bu günlerin çoğunda uzlaşma 09:40 UTC spotuna 15:00 spotundan belirgin yakın.
    CAL = ["2018-06-14", "2019-06-03", "2021-05-12", "2023-04-20", "2024-04-09", "2026-03-19",            # Ramazan arifesi
           "2017-08-31", "2018-08-20", "2020-07-30", "2021-07-19", "2022-07-08", "2023-06-27", "2025-06-05", "2026-05-26",  # Kurban arifesi
           "2019-10-28", "2020-10-28", "2021-10-28", "2022-10-28", "2024-10-28", "2025-10-28", "2026-10-28"]  # 28 Ekim
    known = pd.Series(p.index.isin(pd.to_datetime(CAL)), index=p.index)
    return known, d10, d15


def tr_holiday_gaps(p):
    """VİOP kapalı hafta içi günleri (dünya açık). Döndür: her VİOP günü için önceki VİOP gününden bu yana atlanan hafta içi gün sayısı."""
    allwd = pd.bdate_range(p.index.min(), p.index.max())
    missing = allwd.difference(p.index)
    idx = p.index
    gap = pd.Series(0, index=idx)
    for i in range(1, len(idx)):
        gap.iloc[i] = len(pd.bdate_range(idx[i - 1], idx[i])) - 2
    return gap, missing


def build():
    p = L.load_viop()
    f = pd.DataFrame(index=p.index)
    r = p["v_ret"]
    f["v_ret"] = r
    for h in (1, 3, 5):
        f[f"fwd{h}"] = p[f"fwd{h}"]
    # --- USDTRY
    fx15 = p["dk_USDTRY_p15"]; fx07 = p["dk_USDTRY_p07"]
    f["fx15"] = fx15
    f["usd_fut_l1"] = p["vo_usdtry_ret"].shift(1)                    # t-1 15:10
    f["usd_fut_5_l1"] = p["vo_usdtry_ret"].rolling(5).sum().shift(1)  # t-5..t-1
    f["usd_spot_1"] = np.log(fx15).diff()                              # t-1 15:00 -> t 15:00
    f["usd_spot_5"] = np.log(fx15).diff(5)
    f["usd_intra"] = np.log(fx15 / fx07)                               # t 07:00 -> 15:00
    # ima edilen TL faizi (VİOP USDTRY vadeli bazı): ln(F/S)*365/dte + r_usd  ; t-1 sürümü
    rusd = p["ust_nom3m"] / 100 if "ust_nom3m" in p else 0.0
    itl = np.log(p["vo_usdtry_settle"] / fx15) * 365 / p["vo_usdtry_dte"].clip(lower=3) + rusd
    itl = itl.where(p["vo_usdtry_dte"] >= 5)
    f["itl"] = itl                                   # t (K: 15:10)
    f["itl_l1"] = itl.shift(1)
    f["ditl_5_l1"] = itl.diff(5).shift(1)
    f["fxbasis_ann"] = np.log(p["vo_usdtry_settle"] / fx15) * 365 / p["vo_usdtry_dte"].clip(lower=3)
    # --- XU030
    f["xu_l1"] = p["vo_xu030_ret"].shift(1)
    f["xu_5_l1"] = p["vo_xu030_ret"].rolling(5).sum().shift(1)
    f["xuusd_l1"] = (p["vo_xu030_ret"] - p["vo_usdtry_ret"]).shift(1)
    f["yxu_1"] = np.log(p["y_XU030_IS"]).diff()                       # BIST kapanışı t-2 -> t-1
    # --- gram altın primi
    pr = p["tr_prem_matched"]
    f["prem"] = pr                                   # t (K)
    f["prem_l1"] = pr.shift(1)
    f["dprem_l1"] = pr.diff().shift(1)
    f["dprem5_l1"] = pr.diff(5).shift(1)
    f["premz_l1"] = zs(pr, 60).shift(1)
    f["dprem_K"] = pr.diff()                         # t (K)
    f["premz_K"] = zs(pr, 60)
    # --- XAUTRY hacim/OI
    vol = p["vo_xautry_volume"].replace(0, np.nan); oi = p["vo_xautry_oi"].replace(0, np.nan)
    f["gvolz_l1"] = zs(np.log(vol), 20).shift(1)
    f["goi_d5_l1"] = np.log(oi).diff(5).shift(1)
    vx = p["v_volume"].replace(0, np.nan)
    f["gvol_ratio_z_l1"] = zs(np.log(vol / vx), 60).shift(1)
    # TL değeri bazında yurt içi altın akışı: XAUTRY OI değişimi × yön (gram getirisi)
    f["goi_d1_l1"] = np.log(oi).diff().shift(1)
    # --- VİOP XAUUSD bazı (yerel fiyatlama sapması): ln(settle/xau_p15) eksi taşıma (önceki 20 gün baz/dte medyanı × dte)
    b = np.log(p["v_settle"] / p["xau_p15"])
    rate = (b / p["v_dte"].clip(lower=3)).where(p["v_dte"] >= 5)
    exp_b = rate.rolling(20, min_periods=10).median().shift(1) * p["v_dte"]
    f["xbasis_dev_K"] = b - exp_b                    # t (K: 15:10 vs 15:00)
    f["xbasis_dev_l1"] = (b - exp_b).shift(1)
    # --- bayraklar
    f["roll_any"] = sum(((p.v_code.shift(-k) != p.v_code.shift(-k + 1))).astype(int) for k in range(1, 6)) > 0  # t+1..t+5 içinde roll
    f["roll_t"] = p.v_code != p.v_code.shift(1)
    f["zero_vol"] = p["v_volume"].fillna(0) == 0
    hd, _, _ = half_days(p)
    f["half_day"] = hd
    gap, _ = tr_holiday_gaps(p)
    f["gap"] = gap
    f["extreme"] = ((f.index >= "2020-03-01") & (f.index <= "2020-04-30")) | ((f.index >= "2026-01-01") & (f.index <= "2026-02-28"))
    return p, f


def test(fam, tid, x, y, h, note="", reg=True):
    st = L.split_stats(x, y, h)
    if reg:
        L.register(AG, fam, tid, tid, h, st, note)
    return st


def fmt(st):
    return f"IC={st['ic']:+.3f} t={st['t']:+.2f} n={st['n']} | IS {st['ic_is']:+.3f} (t {st['t_is']:+.2f}) | OOS {st['ic_oos']:+.3f} (t {st['t_oos']:+.2f}) | yıl {st['yrs_same_sign']}/{st['yrs']}"


def legs(pos, ret, h, cost=L.COST_BPS):
    """Uzun ve kısa bacak ayrı (tam/IS/OOS) net Sharpe."""
    out = {}
    for nm, pp in [("long", pos.clip(lower=0)), ("short", pos.clip(upper=0))]:
        o = {}
        for seg, m in [("full", slice(None)), ("is", ret.index <= L.IS_END), ("oos", ret.index > L.IS_END)]:
            rr = ret if isinstance(m, slice) else ret[m]
            a = L.backtest(pp.reindex(rr.index), rr, h, cost)
            o[seg] = None if a is None else round(a["sharpe"], 2)
        out[nm] = o
    return out
