"""(e) BIST altın BYF'leri (GLDTR, ZGOLD, ISGLK): gram altına göre prim/iskonto ve dönüşü.
Kapsama: Yahoo günlük geçmişi YOK (yalnız 1 gün). Yahoo saatlik (730 gün) indirildi: GLDTR/ZGOLD 2023-12+, ISGLK 2024-07+ (tamamı OOS).
Gram altın (spot) = XAUUSD × USDTRY / 31,1035 (Dukascopy saatlik; fiyat anı = index+1h; 2026-10-30 sonrası USDTRY Yahoo saatlik).
BYF birim başına gram oranı yalnız geçmişten kestirilir: oran_med_{t-1} = son 20 günün (t-1'e kadar) medyanı(BYF_kapanış / gram_15:00 UTC).
  prem_cut_t   = ln(BYF_kesim_t / (oran_med_{t-1} × gram_kesim_t)), kesim = başlangıcı ≤13:30 UTC olan son saatlik barın kapanışı (≤14:30 UTC = 17:30 TSİ)
  prem_close_t = ln(BYF_kapanış_t / (oran_med_{t-1} × gram_15:00UTC_t))  -> gün t kapanışında (15:10 UTC) bilinir; sinyalde t-1.
Hedef: BYF kapanış t -> kapanış t+h (BIST günleri) ve göreli (BYF − gram altın spot 15:00 UTC).
"""
from common import *
import warnings; warnings.filterwarnings("ignore")

def duka_px(sym):
    x = pd.read_parquet(f"{P}/duka/{sym}.parquet")["c"]; x.index = x.index + pd.Timedelta(hours=1); return x[~x.index.duplicated()]
xau = duka_px("XAUUSD"); usd = duka_px("USDTRY")
yu = pd.read_parquet(f"{P}/yahoo_h/USDTRY_X.parquet")["close"]; yu.index = yu.index + pd.Timedelta(hours=1)
usd = usd.combine_first(yu[yu.index > usd.index.max()])
sp = pd.read_parquet(f"{P}/panel_spot.parquet"); sp.index = pd.to_datetime(sp.index)
xp = {}
for H in (12, 13, 14, 15):
    s = sp[f"xau_p{H}"]; s.index = s.index + pd.Timedelta(hours=H); s.index = s.index.tz_localize("UTC"); xp[H] = s
xau = xau.combine_first(pd.concat(xp.values()).sort_index())

def at(series, ts):
    """ts (UTC) anındaki fiyat: tam saatse doğrudan, değilse komşu iki saatin geometrik ortalaması."""
    ts = pd.DatetimeIndex(ts)
    fl = ts.floor("h"); ce = ts.ceil("h")
    a = series.reindex(fl).values; b = series.reindex(ce).values
    return pd.Series(np.where(fl == ce, a, np.sqrt(a * b)), index=ts)

rows = []; mag = []; srows = []; HALF = []
vv = pd.read_parquet(f"{P}/panel_viop.parquet"); vv.index = pd.to_datetime(vv.index); v_tr = vv["tr_prem_matched"]
for t in ["GLDTR", "ZGOLD", "ISGLK"]:
    h1 = pd.read_parquet(f"{OUT}/bist_{t}_1h.parquet")
    h1["day"] = h1.index.normalize().tz_localize(None)
    close = h1.groupby("day")["close"].last()
    cut_bars = h1[(h1.index.hour * 60 + h1.index.minute) <= 13 * 60 + 30]
    cutpx = cut_bars.groupby("day")["close"].last()
    cut_end = cut_bars.groupby("day").apply(lambda g: g.index[-1] + pd.Timedelta(hours=1))
    lastbar = h1.groupby("day").apply(lambda g: g.index[-1].hour * 60 + g.index[-1].minute)
    close = close[lastbar >= 13 * 60 + 30]          # yarım günleri (son bar 09:30) çıkar
    days = close.index
    ts15 = pd.DatetimeIndex([pd.Timestamp(f"{dd.date()} 15:00", tz="UTC") for dd in days])
    gram15 = pd.Series((at(xau, ts15) * at(usd, ts15) / 31.1035).values, index=days)
    ce = pd.DatetimeIndex(cut_end.reindex(days))
    gcut = pd.Series((at(xau, ce) * at(usd, ce) / 31.1035).values, index=days)
    ratio = (close / gram15)
    # yurt içi gram primi (VİOP aynı vadeli XAUTRYM / (XAUUSD×USDTRY/31,1035), 15:10 UTC) — BYF yurt içi altını izler
    trp = v_tr.reindex(days)
    prem_dom = np.log(close / gram15) - trp
    prem_dom = prem_dom - prem_dom.rolling(20, min_periods=10).median().shift(1)
    rmed = ratio.rolling(20, min_periods=10).median().shift(1)
    prem_close = np.log(close / (rmed * gram15)); prem_cut = np.log(cutpx.reindex(days) / (rmed * gcut))
    r = np.log(close).diff(); rg = np.log(gram15).diff(); rel = r - rg
    print(t, "gün:", len(days), days[0].date(), "->", days[-1].date(), "| prim std bps (kapanış/kesim):", round(prem_close.std() * 1e4, 1), round(prem_cut.std() * 1e4, 1),
          "AC1 kapanış:", round(prem_close.autocorr(1), 2), "| ortalama gram/birim:", round(ratio.median(), 4))
    for h in HS:
        rows.append(test("e_bist_byf", f"e_{t}_premcut_rel_h{h}", f"{t} prim kesim (≤14:30 UTC) -> BYF−gram", prem_cut, fwd(rel, h), h, note="2023-12+; tamamı OOS"))
        rows.append(test("e_bist_byf", f"e_{t}_premcut_byf_h{h}", f"{t} prim kesim -> BYF", prem_cut, fwd(r, h), h, note="2023-12+; tamamı OOS"))
        rows.append(test("e_bist_byf", f"e_{t}_premclose_l1_rel_h{h}", f"{t} prim kapanış t-1 -> BYF−gram", prem_close.shift(1), fwd(rel, h), h, note="2023-12+; tamamı OOS"))
    for h in HS:
        rows.append(test("e_bist_byf", f"e_{t}_premdom_l1_rel_h{h}", f"{t} yurt içi prime göre sapma t-1 -> BYF−gram", prem_dom.shift(1), fwd(rel, h), h, note="2023-12+; tamamı OOS"))
    print(t, "yurt içi prime göre sapma std bps:", round(prem_dom.std() * 1e4, 1), "AC1", round(prem_dom.autocorr(1), 2),
          "| prim kapanış (medyandan) robust std (MAD×1.48) bps:", round((prem_close - prem_close.median()).abs().median() * 1.48 * 1e4, 1),
          "| corr(ln oran, VİOP yurt içi prim):", round(np.log(ratio).corr(trp), 2))
    for h in (1, 5):
        for nm_, a_, b_ in [("H1", "2023-12-01", "2025-05-31"), ("H2", "2025-06-01", "2026-12-31")]:
            q_ = ic(prem_cut[a_:b_], fwd(rel, h)[a_:b_], max(h, 5))
            HALF.append(dict(etf=t, h=h, half=nm_, ic=round(q_["ic"], 3), t=round(q_["t"], 2), n=q_["n"]))
    rows.append(test("e_bist_byf_diag", f"e_{t}_premclose_t_rel_h1", f"{t} prim kapanış t (tanı) -> BYF−gram", prem_close, fwd(rel, 1), 1, note="tanı"))
    dd = pd.concat([prem_cut.rename("p"), fwd(rel, 1).rename("y1"), fwd(rel, 5).rename("y5"), fwd(r, 1).rename("r1")], axis=1).dropna()
    q = pd.qcut(dd.p, 5, labels=False)
    mg = dd.groupby(q).agg(p_bps=("p", lambda s: round(s.mean() * 1e4, 1)), rel1_bps=("y1", lambda s: round(s.mean() * 1e4, 1)),
                           rel5_bps=("y5", lambda s: round(s.mean() * 1e4, 1)), byf1_bps=("r1", lambda s: round(s.mean() * 1e4, 1)), n=("p", "size"))
    mg["etf"] = t; mag.append(mg)
    # yalnız uzun: kesimde iskonto < −eşik iken BYF al, h gün tut (BIST'te ters altın BYF yok -> ters sürüm yok)
    for thr_bps in (10, 20):
        pos = (prem_cut < -thr_bps / 1e4).astype(float)
        for h in (1, 5):
            net, wl, _ = bt(pos, r.dropna(), h, 10.0)
            net_rel, _, _ = bt(pos, rel.dropna(), h, 10.0)   # gram altına göre fazla getiri (kuramsal: gram altın bacağı açığa satılamaz)
            srows.append(dict(etf=t, thr_bps=thr_bps, h=h, exposure=round(wl.mean(), 3), sh=perf(net)["sharpe"], ann=perf(net)["ann"],
                              bh_sh=perf(np.expm1(r).dropna())["sharpe"], rel_sh=perf(net_rel)["sharpe"], rel_ann=perf(net_rel)["ann"]))
res = pd.DataFrame(rows)
res.drop(columns=["by_year"], errors="ignore").to_csv(f"{OUT}/e_bist_byf_tests.csv", index=False)
pd.set_option("display.width", 250)
print(res[["test_id", "h", "n", "ic", "t", "t_oos", "t_22", "yrs_same_sign", "yrs"]].round(3).to_string())
mag = pd.concat(mag); mag.to_csv(f"{OUT}/e_bist_byf_quintiles.csv"); print(mag.to_string())
print("yarı-örneklem:", pd.DataFrame(HALF).to_string())
sr = pd.DataFrame(srows); sr.to_csv(f"{OUT}/e_bist_byf_strategies.csv", index=False); print(sr.to_string())
