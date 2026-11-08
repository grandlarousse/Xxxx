"""s1: ABD/küresel çapraz varlıkların gecikmeli (t-1 ABD kapanışı) 1 ve 5 günlük z-ölçekli değişimleri → VİOP fwd1/3/5.
Testler: (a) Spearman IC (split_stats), (b) altının kendi 1/5 günlük getirisi kontrol edilmiş kısmi NW t, (c) büyük hareket
asimetrisi (z>+1.5 ve z<-1.5 kuklaları, w=1), (d) emilim tanısı: x(t-1 ABD kapanışı) → altın [t-1 20:00 → t 15:00] (işlem yapılamaz pencere).
Çalıştır: python3 -W ignore s1_tek_degisken.py"""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a4_abd_capraz")
from a4_common import *
import json

reg_reset("s1_")
d = load_viop()
ch = build_changes(d)
ctrl = gold_controls(d)
absorb = np.log(d["xau_p15"] / d["xau_p20_prev"])  # t-1 20:00 -> t 15:00 UTC (karar anından önce biter)
rows = []
avail_rows = []
for (c, w), r in ch.items():
    fam = PRICE_TICKERS.get(c, RATE_SERIES.get(c))
    if c.startswith("y_"):
        viol, lag = check_avail(d, c)
        if w == 1: avail_rows.append(dict(pred=c, ihlal=viol, medyan_gecikme_saat=round(lag, 1)))
        assert viol == 0, c
    z = zscale(r)
    for h in (1, 3, 5):
        y = d[f"fwd{h}"]
        s = split_stats(z, y, h)
        reg("s1_ic", f"s1_ic_{c}_w{w}_h{h}", f"z(d{w} {c})", h, s, note=fam)
        p = partial_stats(z, y, ctrl, h)
        reg("s1_kismi", f"s1_kismi_{c}_w{w}_h{h}", f"z(d{w} {c}) | g1,g5", h, p, note=fam)
        row = dict(pred=c, aile=fam, w=w, h=h, ic=s["ic"], t=s["t"], ic_is=s["ic_is"], t_is=s["t_is"], ic_oos=s["ic_oos"], t_oos=s["t_oos"],
                   yrs_same=s["yrs_same_sign"], yrs=s["yrs"], n=s["n"], tk_full=p["t"], tk_is=p["t_is"], tk_oos=p["t_oos"])
        if w == 1:
            for nm, dm in [("up", (z > 1.5).astype(float).where(z.notna())), ("dn", (z < -1.5).astype(float).where(z.notna()))]:
                e = event_stats(dm, y, h)
                reg("s1_buyuk", f"s1_buyuk_{nm}_{c}_h{h}", f"1[z(d1 {c}){'>' if nm=='up' else '<'}{'+' if nm=='up' else '-'}1.5]", h, e, note=fam + "; ic=ortalama fark bps")
                row.update({f"{nm}_bps": e["ic"], f"{nm}_t": e["t"], f"{nm}_t_is": e["t_is"], f"{nm}_t_oos": e["t_oos"], f"{nm}_n": e["n"], f"{nm}_yrs": f"{e['yrs_same_sign']}/{e['yrs']}"})
        rows.append(row)
    if w == 1:
        a = split_stats(z, absorb, 1)
        reg("s1_emilim", f"s1_emilim_{c}", f"z(d1 {c}) -> altin[t-1 20:00,t 15:00]", 0, a, note="tani; islem yapilamaz pencere")
        rows.append(dict(pred=c, aile=fam, w=1, h=0, ic=a["ic"], t=a["t"], ic_is=a["ic_is"], t_is=a["t_is"], ic_oos=a["ic_oos"], t_oos=a["t_oos"], yrs_same=a["yrs_same_sign"], yrs=a["yrs"], n=a["n"]))

res = pd.DataFrame(rows)
res.to_csv(f"{OUT}/s1_tek_degisken.csv", index=False)
pd.DataFrame(avail_rows).to_csv(f"{OUT}/s1_bilgi_zamani.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 500)
tr = res[res.h > 0]
print("Test sayısı (bu betik):", len(pd.read_csv(f"{S}/out/registry/{AGENT}.csv").query("test_id.str.startswith('s1_')", engine="python")))
print("\n|t|>=2 tam dönem IC:")
print(tr[tr.t.abs() >= 2][["pred", "w", "h", "ic", "t", "t_is", "t_oos", "yrs_same", "yrs", "tk_full", "tk_oos"]].round(3).to_string())
print("\n|t_is|>=2 (IS seçimi) ve OOS:")
print(tr[tr.t_is.abs() >= 2][["pred", "w", "h", "ic_is", "t_is", "ic_oos", "t_oos", "tk_is", "tk_oos"]].round(3).to_string())
print("\nBüyük hareket |t|>=2:")
for nm in ("up", "dn"):
    q = tr[(tr.w == 1) & (tr[f"{nm}_t"].abs() >= 2)]
    print(nm); print(q[["pred", "h", f"{nm}_bps", f"{nm}_t", f"{nm}_t_is", f"{nm}_t_oos", f"{nm}_n", f"{nm}_yrs"]].round(2).to_string())
print("\nEmilim tanısı (x t-1 ABD kapanışı -> altın t-1 20:00..t 15:00):")
print(res[res.h == 0][["pred", "ic", "t", "t_is", "t_oos"]].round(3).sort_values("t").to_string())
