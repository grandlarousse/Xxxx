"""Adım 1: ham veriden VİOP hedefi ve 15:00/12:00/07:00 UTC görüntüleri; panel ile karşılaştırma. Çıktı: data_rep.parquet"""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a5_esz_artik_rep")
from rep_lib import *

va = viop_active("XAUUSD")
print("VİOP günleri:", len(va), va.index[0].date(), va.index[-1].date())
mis = (va.prev_settle - va.prev_own).abs() > 1e-9
print("prev_settle != kontratın önceki uzlaşması:", int(mis.sum()), list(va.index[mis].date)[:10])
print("ret NaN:", int(va.ret.isna().sum()), " |ret|>5%:", list(va.index[va.ret.abs() > 0.05].date))
for h in (1, 3, 5):
    va[f"fwd{h}"] = fwd_sum(va.ret, h)
va["roll"] = va.code != va.code.shift(1)
print("roll günleri:", int(va.roll.sum()))

# panel ile karşılaştır (yalnız doğrulama için)
vp = pd.read_parquet(f"{P}/panel_viop.parquet"); vp.index = pd.to_datetime(vp.index)
cmp = pd.concat([va[["code", "ret", "fwd1", "fwd3", "fwd5"]], vp[["v_code", "v_ret", "fwd1", "fwd3", "fwd5"]].add_prefix("p_")], axis=1)
print("kod eşleşmesi:", (cmp.code == cmp.p_v_code).mean().round(4), " ret max fark:", (cmp.ret - cmp.p_v_ret).abs().max(),
      " fwd3 max fark:", (cmp.fwd3 - cmp.p_fwd3).abs().max())
print(cmp[cmp.code != cmp.p_v_code][["code", "p_v_code"]].head())

# spot görüntüleri: takvim = Pzt-Cum ve XAU 14:00 barı mevcut
syms = dict(XAU="XAUUSD", XAG="XAGUSD", DXY="DOLLARIDXUSD", TBOND="USTBONDTRUSD", SPX="USA500IDXUSD", EURUSD="EURUSD")
p15 = snap("XAUUSD", 15)
cal = p15.index[p15.index.dayofweek < 5]
D = pd.DataFrame(index=cal)
for k, s in syms.items():
    for HH in (7, 12, 15, 16):
        D[f"{k}_p{HH:02d}"] = snap(s, HH).reindex(cal)
sp = pd.read_parquet(f"{P}/panel_spot.parquet"); sp.index = pd.to_datetime(sp.index)
print("spot takvimi: benim", len(cal), cal[0].date(), cal[-1].date(), " panel", len(sp), " ortak", len(cal.intersection(sp.index)),
      " yalnız panelde:", len(sp.index.difference(cal)), list(sp.index.difference(cal).date)[:12])
print("yalnız bende:", list(cal.difference(sp.index).date)[:12])
for k, s in syms.items():
    for HH in (7, 15):
        col = "xau_p%02d" % HH if k == "XAU" else f"dk_{s}_p{HH:02d}"
        if col not in sp: continue
        a = D[f"{k}_p{HH:02d}"]; b = sp[col].reindex(cal)
        both = a.notna() & b.notna()
        print(f"{k} p{HH}: benim notna {a.notna().sum()}, panel notna {b.notna().sum()}, ortak {both.sum()}, fark>1e-6: {int(((a-b).abs()>1e-6)[both].sum())}, "
              f"panelde var bende yok: {int((b.notna() & a.isna()).sum())}")
a = D.XAU_p12; b = sp.xau_p12.reindex(cal); print("XAU p12 fark:", int(((a - b).abs() > 1e-6).sum()), " panel var bende yok:", int((b.notna() & a.isna()).sum()))
D.to_parquet(f"{OUT}/spot_snaps.parquet")
va.to_parquet(f"{OUT}/viop_rep.parquet")
