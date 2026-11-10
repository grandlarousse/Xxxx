"""(6) 2026 işlemleri tek tek + kötü senaryo + roll + ana ajan rakamlarıyla mutabakat + spot 2010–2016 + güncel durum."""
import numpy as np, pandas as pd
from adv_lib import *
pd.set_option("display.width", 250)
R = us_returns(); e, B = rolling_resid(R); pv = viop(); r = pv.v_ret
E10 = e.rolling(10).sum(); thrA = E10[:"2017-12-31"].dropna().quantile(.8); thrB = E10["2008":"2017-12-31"].dropna().quantile(.8)
x, used = map_us_to_viop(E10, pv.index); bh = (np.exp(r) - 1).iloc[1:]
print("=== MUTABAKAT: iki eşikle ana ajanın rakamları ===")
for nm, th in [("eşik %2,307 (2006-08..2017)", thrA), ("eşik %2,541 (2008..2017)", thrB)]:
    s = (x > th).astype(float)
    for H in (3, 5):
        pos = position(s, H)
        for c in (5, 22):
            p = pnl(pos, r, c); t = trades(pos, r, c); tc = t[~t.open_]; al = alpha(p, bh)
            print(f"  {nm} H={H} {c}bps: sinyal günü {int(s.sum())} | {len(tc)} işlem ort %{tc.ret.mean()*100:.2f} kazanan %{(tc.ret>0).mean()*100:.0f} en kötü %{tc.ret.min()*100:.1f} | Sharpe {sharpe(p):.2f} alfa %{al[0]:.1f} t {al[1]:.2f} | h3 t {nw_diff(fwd(r,3), s, 5)['t']:.2f} h5 t {nw_diff(fwd(r,5), s, 5)['t']:.2f}")
sig = (x > thrA).astype(float); pos = position(sig, 3)
# ---- işlemler, gün içi en düşük ile
def trade_table(pos, cost=5):
    t = trades(pos, r, cost); rows = []
    for _, q in t.iterrows():
        i = pv.index.get_loc(q.entry); j = pv.index.get_loc(q.exit) if not q.open_ else len(pv) - 1
        ent = pv.v_settle.iloc[i]; seg = pv.iloc[i + 1:j + 1]
        # gün içi en düşük: aynı kontratın düşük fiyatı / o günün önceki uzlaşması üzerinden zincirlenmiş
        cum = r.iloc[i + 1:j + 1].cumsum(); prevcum = cum.shift(1).fillna(0)
        lowrel = prevcum.values + np.log(seg.v_low.replace(0, np.nan) / seg.v_prev_settle).values
        rolls = int((pv.v_code.iloc[i + 1:j + 1].values != pv.v_code.iloc[i:j].values).sum())
        rows.append(dict(giris=q.entry.date(), cikis=(q.exit.date() if not q.open_ else "AÇIK"), gun=int(q.days), takvim_gun=(pv.index[j] - q.entry).days, giris_fyt=ent, cikis_fyt=pv.v_settle.iloc[j],
                         x_giris=round(x.iloc[i] * 100, 1), getiri=round(q.ret * 100, 2), en_kotu_uzlasma=round((np.exp(min(cum.min(), 0)) - 1) * 100, 2) if len(cum) else 0,
                         en_kotu_gunici=round((np.exp(np.nanmin(np.append(lowrel, 0))) - 1) * 100, 2), en_iyi_uzlasma=round((np.exp(max(cum.max(), 0)) - 1) * 100, 2) if len(cum) else 0, roll=rolls, acik=q.open_))
    return pd.DataFrame(rows)
T = trade_table(pos)
print("\n=== 2026 İŞLEMLERİ (H=3, 5 bps; getiri % USD fiyat üzerinden, kaldıraçsız) ===")
print(T[pd.to_datetime(T.giris) >= "2026-01-01"].drop(columns=["acik"]).to_string(index=False))
print("\n=== 2025 İŞLEMLERİ ==="); print(T[(pd.to_datetime(T.giris) >= "2025-01-01") & (pd.to_datetime(T.giris) < "2026-01-01")].drop(columns=["acik"]).to_string(index=False))
Tc = T[~T.acik]
print("\nTüm kapalı işlemler özeti:", len(Tc), "| getiri ort %", round(Tc.getiri.mean(), 2), "std %", round(Tc.getiri.std(), 2), "| en kötü gün içi düşüş: medyan %", round(Tc.en_kotu_gunici.median(), 2), " %10'luk %", round(Tc.en_kotu_gunici.quantile(.1), 2), " en kötü %", round(Tc.en_kotu_gunici.min(), 2))
print("  işlemlerin yüzde kaçı bir noktada (uzlaşmada) −%2'den kötü gördü:", round((Tc.en_kotu_uzlasma < -2).mean() * 100), "| gün içinde −%2:", round((Tc.en_kotu_gunici < -2).mean() * 100), "| gün içinde −%3:", round((Tc.en_kotu_gunici < -3).mean() * 100), "| −%5:", round((Tc.en_kotu_gunici < -5).mean() * 100))
print("  getiri dağılımı % (5/25/50/75/95):", Tc.getiri.quantile([.05, .25, .5, .75, .95]).round(2).tolist())
print("  roll içeren işlem:", int((Tc.roll > 0).sum()), "/", len(Tc), "| takvim günü süresi medyan", Tc.takvim_gun.median(), "maks", Tc.takvim_gun.max())
ls = (Tc.getiri < 0).astype(int); streak = ls.groupby((ls == 0).cumsum()).cumsum().max()
print("  en uzun ardışık zarar serisi:", int(streak), "işlem")
p = pnl(pos, r, 5); eq = (1 + p).cumprod(); dd = eq / eq.cummax() - 1
uw = (dd < 0).astype(int); L = uw.groupby((uw == 0).cumsum()).cumsum()
print("  maks düşüş %", round(dd.min() * 100, 1), "tarih", dd.idxmin().date(), "| en uzun su altı süresi (VİOP günü):", int(L.max()), "bitiş", L.idxmax().date())
print("  2022-01..2024-12: işlem", int(((pd.to_datetime(Tc.giris) >= '2022-01-01') & (pd.to_datetime(Tc.giris) < '2025-01-01')).sum()), "toplam %", round(Tc[(pd.to_datetime(Tc.giris) >= '2022-01-01') & (pd.to_datetime(Tc.giris) < '2025-01-01')].getiri.sum(), 1))
print("  2018-01..2024-12 strateji bileşik % :", round(((1 + p['2018':'2024']).prod() - 1) * 100, 1), "| B&H vadeli % :", round(((1 + bh['2018':'2024']).prod() - 1) * 100, 1))
# ---- roll günü: eski kontratta kalan kullanıcı ile v_ret farkı
vl = pd.read_parquet(S + "/panel/viop_long.parquet"); vl = vl[vl.root == "XAUUSD"].copy(); vl["date"] = pd.to_datetime(vl.date)
rd = pv.index[(pv.v_code != pv.v_code.shift()).values][1:]
dif = []
for d in rd:
    old = pv.v_code.shift(1).loc[d]; o = vl[(vl.date == d) & (vl.code == old)]
    if len(o) and o.settle.iloc[0] > 0 and o.prev_settle.iloc[0] > 0: dif.append(np.log(o.settle.iloc[0] / o.prev_settle.iloc[0]) - r.loc[d])
dif = np.array(dif)
print(f"\nROLL: {len(rd)} roll günü; eski kontrat getirisi − v_ret (bps): ort {dif.mean()*1e4:.1f}, |ort| {np.abs(dif).mean()*1e4:.1f}, maks |.| {np.abs(dif).max()*1e4:.0f}")
print("  aktif kontratın roll günündeki vadeye kalan gün (eski kontrat):", pv.v_dte.shift(1).loc[rd].describe().round(0).to_dict())
# ---- spot 2010–2016 (ana ajanın iddiası) — bağımsız
ps = pd.read_parquet(S + "/panel/panel_spot.parquet"); ps.index = pd.to_datetime(ps.index)
xs, _ = map_us_to_viop(E10, ps.index); ss = (xs > thrA).astype(float); sr = ps.s_ret
print("\nSPOT 15:00 UTC hedefi (seçim döneminin içinde — bağımsız kanıt DEĞİL):")
for nm, a, b in [("2010–2016", "2010", "2016"), ("2010–2012", "2010", "2012"), ("2013–2016", "2013", "2016"), ("2017–2026", "2017", None), ("2018–2024", "2018", "2024")]:
    for h in (3, 5):
        q = nw_diff(fwd(sr, h)[a:b], ss[a:b], 10); print(f"  {nm} h{h}: fark {q['diff']:+.3f}% t {q['t']:.2f} n {q['n1']}/{q['N']}", end=" |")
    print()
yy = pd.DataFrame({"f5": fwd(sr, 5) * 100, "s": ss}).dropna(); g = yy.groupby([yy.index.year, "s"]).f5.mean().unstack(); g["fark"] = g[1.0] - g[0.0]
print("  spot h5 fark yıl yıl:", g.fark.round(2).to_dict(), "| pozitif yıl", int((g.fark > 0).sum()), "/", len(g))
# ---- güncel durum
print("\nGÜNCEL: son 15 VİOP günü"); print(pd.DataFrame({"abd_kapanis": used.dt.date, "x%": (x * 100).round(2), "sinyal": sig.astype(int), "poz(H=3)": pos.astype(int), "v_settle": pv.v_settle, "v_ret%": (r * 100).round(2)}).tail(15).to_string())
lastE = E10.dropna().iloc[-3:]; print("son ABD kapanışlarında x%:", (lastE * 100).round(2).to_dict(), "| eşik %", round(thrA * 100, 2), "| son betalar:", B.iloc[-1].round(2).to_dict())
rat = (R.GDX - R.GLD).rolling(10).sum(); print("basit oran biçimi (ln GDX/GLD 10g) son 3:", (rat.iloc[-3:] * 100).round(2).to_dict(), "| eşik %", round(rat[:'2017-12-31'].dropna().quantile(.8) * 100, 2))
