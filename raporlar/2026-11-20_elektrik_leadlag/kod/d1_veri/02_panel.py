"""D1 adim 2: ham veriden panel kur. Kullanim:
  python3 -I 02_panel.py <RAW_DIR> <OUT_DIR> [CUT=YYYY-MM-DD] [START=2010-01-04]
CUT verilirse o tarihten sonraki HICBIR satir kullanilmaz/yazilmaz; duzeltme carpani CUT gunune gore normalize edilir
(c == c_raw son gunde), meta alanlari CUT itibariyla hesaplanir.
Kaynak secimi: kapanis/yuksek/dusuk/hacim/piyasa degeri = Is Yatirim (HG_* ham, PD); duzeltme carpani = Is Yatirim HG/HGDG
oranindan parca parca sabit; acilis = Yahoo acilisi (ham olcege cevrilip Is Yatirim gun araligi ile dogrulanir)."""
import os, sys, json
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d1lib import load_isy_stock, load_yahoo, load_isy_index, tick_size
from universe import STOCKS, XELKT_MEMBERS, IDX_ISY, VIOP

RAW, OUT = sys.argv[1], sys.argv[2]
kw = dict(a.split("=") for a in sys.argv[3:] if "=" in a)
START = pd.Timestamp(kw.get("START", "2010-01-04")); CUT = pd.Timestamp(kw["CUT"]) if "CUT" in kw else None
MARGIN_CHG = pd.Timestamp("2020-03-13")      # bu tarihten itibaren +-%10, oncesi +-%20
os.makedirs(OUT, exist_ok=True)

# ---------- ham yukleme (CUT sonrasi hemen atilir) ----------
def cut(x):
    return x.loc[:CUT] if CUT is not None else x
isy = {s: cut(load_isy_stock(RAW, s)) for s in STOCKS}
yah = {}
for s in STOCKS:
    y, sp, dv, m = load_yahoo(RAW, s); yah[s] = (cut(y), cut(sp), cut(dv), m)
idx_all = cut(pd.DataFrame({c: load_isy_index(RAW, c) for c in IDX_ISY}))

# ---------- takvim: XU100'un (Is Yatirim) islem gordugu gunler ----------
anystock = pd.Index(sorted(set().union(*[set(a.index) for a in isy.values()])))
cal_full = idx_all["XU100"].dropna().index
cal_full = cal_full[(cal_full.dayofweek < 5) & cal_full.isin(anystock)]     # bayat kopya gunler (orn. 2013-01-01) duser
cal = cal_full[cal_full >= START]
pos_full = pd.Series(np.arange(len(cal_full)), index=cal_full)

def margin(dates):
    return pd.Series(np.where(dates >= MARGIN_CHG, 0.10, 0.20), index=dates)

rows, ca_rows, meta_rows = [], [], []
W = {}
for s in STOCKS:
    a = isy[s]; a = a[a.index.isin(cal_full)]
    if len(a) == 0: continue
    y, sp, dv, ym = yah[s]
    isy_first = a.index[0]
    a = a.reindex(cal_full[cal_full >= isy_first])            # hissenin takvimi; eksik satir = NaN
    dupy = (y[["o", "h", "l", "c"]] == y[["o", "h", "l", "c"]].shift(1)).all(axis=1)
    yy = y.reindex(a.index); dup = dupy.reindex(a.index).fillna(True)
    hole = ~(a.vol_tl > 0) | ~(a.h_raw > 0)                  # Is Yatirim'da islem yok gorunen ya da eksik gun
    # --- duzeltme carpani F (ham/duzeltilmis), parca parca sabit ---
    f = a.c_raw / a.c_adj; fz = f.ffill()
    step = (fz / fz.shift(1) - 1).abs()
    cadj = a.c_adj.ffill()
    noise = 2.2 * 0.00005 / np.minimum(cadj, cadj.shift(1))
    cand = set(step[step > np.maximum(0.0005, noise)].index) | (set(sp.index) | set(dv.index)) & set(a.index)
    cand = sorted(d for d in cand if d > a.index[0])
    bounds = [a.index[0]] + cand
    seg_id = pd.Series(np.searchsorted(pd.DatetimeIndex(bounds), a.index, side="right") - 1, index=a.index)
    med = f.groupby(seg_id).median()
    keep = [0]                                               # gercek olmayan adaylari birlestir (medyan farki < %0,03)
    for k in range(1, len(med)):
        if abs(med.iloc[k] / med.iloc[keep[-1]] - 1) > 0.0003: keep.append(k)
    bounds = [bounds[k] for k in keep]
    seg_id = pd.Series(np.searchsorted(pd.DatetimeIndex(bounds), a.index, side="right") - 1, index=a.index)
    F = f.groupby(seg_id).transform("median")
    F = F / F.iloc[-1]                                       # son gunde c == c_raw
    serm = a.sermaye.ffill()
    ca_type = pd.Series("", index=a.index)
    for d in bounds[1:]:
        i = a.index.get_loc(d); st = F.iloc[i] / F.iloc[i - 1] - 1
        w = serm.iloc[max(0, i - 15): i + 16]; serm_chg = w.max() / w.min() - 1 if w.min() > 0 else np.nan
        has_sp = d in sp.index; has_dv = d in dv.index
        typ = "cap" if (has_sp or abs(st) >= 0.12 or (serm_chg > 0.005 and not has_dv)) else "div"
        ca_type[d] = typ
        ca_rows.append(dict(sym=s, date=d, adim=round(st, 5), tur=typ, yahoo_split=sp.get(d, np.nan), yahoo_div=dv.get(d, np.nan),
                            sermaye_degisim=round(serm_chg, 4), ham_once=a.c_raw.iloc[i - 1], ham_gun=a.c_raw.iloc[i]))
    # --- Yahoo -> ham olcek carpani S (bolunme parcalarinda medyan) ---
    q = (a.c_raw / yy.c).where(~hole)
    sb = sorted(set(bounds) | (set(sp.index) & set(a.index)))
    sid = pd.Series(np.searchsorted(pd.DatetimeIndex(sb), a.index, side="right") - 1, index=a.index)
    S = q.groupby(sid).transform("median")
    # --- Is Yatirim delikleri (2010-13 yarim gunler vb.): Yahoo'da gercek islem varsa oradan yama ---
    patch = hole & (yy.v > 0) & ~dup & (yy.c > 0) & S.notna()
    if patch.any():
        stale = a.c_raw.ffill()
        for col in ["c", "h", "l"]: a.loc[patch, col + "_raw"] = (yy[col] * S)[patch].round(4)
        a.loc[patch, "aof_raw"] = ((yy.h + yy.l + yy.c) / 3 * S)[patch]
        a.loc[patch, "vol_tl"] = (yy.v * (yy.h + yy.l + yy.c) / 3)[patch]
        a.loc[patch, "mcap_tl"] = (a.mcap_tl.ffill() * a.c_raw / stale)[patch]
    nov = ~(a.vol_tl > 0) & a.c_raw.notna()                  # gercekten islemsiz gun: fiyat tasinir, h=l=c
    a.loc[nov, ["h_raw", "l_raw"]] = np.c_[a.c_raw[nov], a.c_raw[nov]]
    # --- acilis: Yahoo -> ham olcek -> gun araligi ile dogrula ---
    o_raw = yy.o * S
    tol = 0.003 + 0.6 * tick_size(a.c_raw, a.index) / a.c_raw
    ok = (yy.o > 0) & (yy.v > 0) & ~dup & (o_raw >= a.l_raw * (1 - tol)) & (o_raw <= a.h_raw * (1 + tol)) & (a.vol_tl > 0)
    o_raw = o_raw.where(ok).clip(lower=a.l_raw, upper=a.h_raw)
    # --- seri ---
    d = pd.DataFrame(index=a.index)
    d["o"] = o_raw / F; d["h"] = a.h_raw / F; d["l"] = a.l_raw / F; d["c"] = a.c_raw / F
    d["c_raw"] = a.c_raw; d["o_raw"] = o_raw; d["h_raw"] = a.h_raw; d["l_raw"] = a.l_raw
    d["vol_tl"] = a.vol_tl.fillna(0.0); d["vol_adet"] = (a.vol_tl / a.aof_raw).where(a.aof_raw > 0, 0.0).fillna(0.0).round()
    d["mcap_tl"] = a.mcap_tl.where(a.mcap_tl > 0)
    d["adjf"] = F; d["ca"] = ca_type
    d["kaynak"] = np.where(patch, "yahoo_yama", np.where(ok, "isy+yahoo_acilis", "isy"))
    d["c_isyadj"] = a.c_adj
    # getiri (askidan donuste son kapanisa gore)
    pc = d.c.ffill().shift(1)
    d["ret_cc"] = d.c / pc - 1
    d["ret_co"] = d.o / pc - 1
    d["ret_oc"] = d.c / d.o - 1
    ref = a.c_raw.ffill().shift(1) * F / F.shift(1)          # bugunun ham olceginde baz fiyat
    m = margin(a.index); tk = tick_size(ref * (1 + m), a.index) / ref
    tolu = np.maximum(0.006, tk + 1e-9)
    eps = 1e-9
    d["lim_up_touch"] = (a.h_raw / ref - 1 >= m - tolu)
    d["lim_dn_touch"] = (a.l_raw / ref - 1 <= -(m - tolu))
    d["lim_up"] = d.lim_up_touch & (a.c_raw / ref - 1 >= m - tolu) & (a.c_raw >= a.h_raw - eps)
    d["lim_dn"] = d.lim_dn_touch & (a.c_raw / ref - 1 <= -(m - tolu)) & (a.c_raw <= a.l_raw + eps)
    tku = tick_size(ref * (1 + m), a.index); upl = np.floor(ref * (1 + m) / tku + 1e-6) * tku      # ust sinir asagi yuvarlanir
    tkd = tick_size(ref * (1 - m), a.index); dnl = np.ceil(ref * (1 - m) / tkd - 1e-6) * tkd       # alt sinir yukari yuvarlanir
    d["lim_up_exact"] = (a.c_raw >= upl - 1e-6) & (a.vol_tl > 0)
    d["lim_dn_exact"] = (a.c_raw <= dnl + 1e-6) & (a.vol_tl > 0)
    d = d[a.c_raw.notna()]                                   # tamamen eksik gunler px'e yazilmaz
    d["ipo_n"] = (pos_full.reindex(d.index) - pos_full[isy_first] + 1).astype(int)
    d["sym"] = s
    W[s] = d
    d2 = d[d.index >= START]
    if len(d2) == 0: continue
    last = d2.iloc[-1]; t1 = d2.vol_tl.iloc[-252:]
    tk1 = float(tick_size([last.c_raw], [d2.index[-1]])[0])
    meta_rows.append(dict(sym=s, ad=ym.get("longName") or ym.get("shortName") or s, grup="XELKT" if s in XELKT_MEMBERS else "komsu",
                          ilk_islem_tarihi=str(isy_first.date()), viop=int(s in VIOP), son_tarih=str(d2.index[-1].date()), son_fiyat=last.c_raw,
                          tick=tk1, tick_bps=round(tk1 / last.c_raw * 1e4, 2), adv_tl_medyan_12ay=round(float(t1.median()), 0),
                          mcap_tl_son=d2.mcap_tl.dropna().iloc[-1] if d2.mcap_tl.notna().any() else np.nan, n_gun=len(d2),
                          lim_up_sayisi=int(d2.lim_up.sum()), lim_dn_sayisi=int(d2.lim_dn.sum()),
                          lim_up_touch_sayisi=int(d2.lim_up_touch.sum()), lim_dn_touch_sayisi=int(d2.lim_dn_touch.sum()),
                          sifir_hacim_gun=int((d2.vol_tl <= 0).sum()), yahoo_yama_gun=int((d2.kaynak == "yahoo_yama").sum()), acilis_eksik_gun=int(d2.o.isna().sum())))

syms = [s for s in STOCKS if s in W and (W[s].index >= START).any()]
def wide(col, fill=None, dtype=None):
    x = pd.DataFrame({s: W[s][col] for s in syms}).reindex(cal)
    if fill is not None: x = x.fillna(fill)
    if dtype is not None: x = x.astype(dtype)
    x.index.name = "date"; return x

px = pd.concat([W[s][W[s].index >= START] for s in syms]); px.index.name = "date"
px = px.reset_index()[["date", "sym", "o", "h", "l", "c", "c_raw", "vol_tl", "vol_adet", "mcap_tl", "kaynak", "o_raw", "h_raw", "l_raw", "adjf", "ca", "c_isyadj"]]
px.to_parquet(os.path.join(OUT, "px.parquet"), index=False)
ret_cc = wide("ret_cc"); close_raw = wide("c_raw"); vol = wide("vol_tl")
listed = pd.DataFrame({s: (cal >= W[s].index[0]) for s in syms}, index=cal)
ipo_n = pd.DataFrame({s: (pos_full.reindex(cal) - pos_full[W[s].index[0]] + 1).clip(lower=0) for s in syms}).astype(int); ipo_n.index.name = "date"
has = close_raw.notna()
vol = vol.where(has | ~listed, 0.0)                       # listelenmis ama satir yok (islem sirasi kapali) -> hacim 0
zero_vol = listed & ~(vol > 0)
out = {"ret_cc": ret_cc, "ret_co": wide("ret_co"), "ret_oc": wide("ret_oc"), "vol_tl": vol, "close_raw": close_raw,
       "lim_up": wide("lim_up", False, bool), "lim_dn": wide("lim_dn", False, bool),
       "lim_up_touch": wide("lim_up_touch", False, bool), "lim_dn_touch": wide("lim_dn_touch", False, bool),
       "lim_up_exact": wide("lim_up_exact", False, bool), "lim_dn_exact": wide("lim_dn_exact", False, bool),
       "zero_vol": zero_vol, "ipo_n": ipo_n,
       "ca_day": wide("ca").eq("cap"), "div_day": wide("ca").eq("div"),
       "tradable": (ipo_n > 20) & (vol > 0) & has}
for k, v in out.items():
    v.index.name = "date"; v.to_parquet(os.path.join(OUT, k + ".parquet"))
# ---------- endeksler ----------
idx = idx_all.reindex(cal); idx.index.name = "date"
idx.to_parquet(os.path.join(OUT, "idx.parquet"))
idx.pct_change(fill_method=None).to_parquet(os.path.join(OUT, "idx_ret.parquet"))
io = {}
for c in ["XU030", "XU100"]:
    y = cut(load_yahoo(RAW, c)[0]).reindex(cal)
    k = y.c / idx[c]; kmed = k.rolling(21, center=True, min_periods=5).median()
    good = (y.o > 0) & ((k / kmed - 1).abs() < 0.002) & ((y.o / y.c - 1).abs() < 0.12)
    io[c] = (idx[c] * y.o / y.c).where(good)
io = pd.DataFrame(io); io.index.name = "date"; io.to_parquet(os.path.join(OUT, "idx_open.parquet"))
# ---------- meta, kurumsal islem listesi ----------
pd.DataFrame(meta_rows).to_csv(os.path.join(OUT, "meta.csv"), index=False)
ca = pd.DataFrame(ca_rows)
if len(ca): ca = ca[ca.date >= START]
ca.to_csv(os.path.join(OUT, "ca_events.csv"), index=False)
print("panel:", OUT, "| gun:", len(cal), cal[0].date(), "->", cal[-1].date(), "| hisse:", len(syms), "| px satir:", len(px),
      "| acilis dolu orani:", round(px.o.notna().mean(), 4), "| kurumsal islem:", len(ca), "| idx_open dolu:", io.notna().mean().round(3).to_dict())
