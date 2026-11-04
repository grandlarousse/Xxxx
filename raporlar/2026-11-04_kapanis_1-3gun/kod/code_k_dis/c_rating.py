"""(c) Kredi notu kararı sonrası ters pozisyon, kapanıştan kapanışa.
Olaylar: out/olay_tarihleri.csv RATING (+ 2026-04-10 Fitch görünüm pozitif->durağan, web: bloomberght/evrensel/qnbinvest).
2026'da başka not/görünüm değişikliği yok: Moody's 23.01 ve 24.07 Ba3 durağan (aksiyon yok), S&P 17.04 ve 16.10 BB- durağan (aksiyon yok), Fitch 17.07 BB- durağan teyit.
Kararlar Cuma gece (~20:30 UTC) -> tepki günü (react_date, genelde Pazartesi) açılışında gap. Kullanıcı tepki günü uzlaşmasında girer
(gap'i KAÇIRIR), yön = -dir (ters), h=1,2,3 gün sonra uzlaşmada çıkar. Önceki: Pzt uzlaşma -> Çar uzlaşma (h=2).
Plasebo: tüm Pazartesi uzlaşmaları (rastgele yönle) -> h gün getirisi dağılımı.
"""
import numpy as np, pandas as pd, klib as K
F = K.fut_panel(); Sp = K.spot_panel()
o = pd.read_csv(K.S + "/out/olay_tarihleri.csv"); r = o[o["type"] == "RATING"].copy()
add = pd.DataFrame([dict(date="2026-04-10", type="RATING", sub="FITCH_outlook", dir=-1, react_date="2026-04-13", note="pozitif->durağan (web)")])
r = pd.concat([r, add], ignore_index=True)
r["react_date"] = pd.to_datetime(r["react_date"]); r["date"] = pd.to_datetime(r["date"])
r["cls"] = np.where(r["sub"].str.contains("upgrade|downgrade"), "notch", np.where(r["sub"].str.contains("outlook"), "outlook", "review"))
# aynı tepki gününde birden çok karar -> tek olay (yön toplamının işareti)
ev = r.groupby("react_date").agg(dir=("dir", "sum"), cls=("cls", lambda x: "notch" if (x == "notch").any() else x.iloc[0]),
                                 subs=("sub", lambda x: "+".join(x))).reset_index()
ev["dir"] = np.sign(ev["dir"])
rows = []; det = []
for inst, R, start in [("F_XU030", F["XU030"], "2017-03-06"), ("XU100_spot", Sp["XU100"], "2014-01-01"), ("XU030_spot", Sp["XU030"], "2014-01-01")]:
    R = R.dropna(); cal = R.index
    for _, e in ev.iterrows():
        if e["react_date"] < pd.Timestamp(start) or e["react_date"] not in cal: continue
        i = cal.get_loc(e["react_date"])
        rec = dict(inst=inst, react=e["react_date"].date(), dir=e["dir"], cls=e["cls"], subs=e["subs"], react_ret=R.iloc[i] * 1e4)
        for h in (1, 2, 3, 5):
            if i + h < len(cal): rec[f"h{h}"] = -e["dir"] * R.iloc[i + 1:i + 1 + h].sum() * 1e4
        det.append(rec)
D = pd.DataFrame(det); D.to_csv(K.RES + "/c_rating_events.csv", index=False)
# plasebo: tüm Pazartesiler (rastgele işaret) — h gün getirisinin mutlak dağılımı (std)
out = []
for inst in D["inst"].unique():
    R = {"F_XU030": F["XU030"], "XU100_spot": Sp["XU100"], "XU030_spot": Sp["XU030"]}[inst].dropna()
    for sel, msk in [("tümü", None), ("notch", "notch"), ("outlook", "outlook"), ("notch+outlook", "no_review")]:
        x = D[D["inst"] == inst]
        if msk == "notch": x = x[x["cls"] == "notch"]
        elif msk == "outlook": x = x[x["cls"] == "outlook"]
        elif msk == "no_review": x = x[x["cls"] != "review"]
        for h in (1, 2, 3, 5):
            v = x[f"h{h}"].dropna()
            if len(v) < 4: continue
            sd_all = (K.fwd(R, h).dropna() * 1e4).std()
            t = v.mean() / (v.std(ddof=1) / np.sqrt(len(v)))
            # bootstrap: rastgele günler, rastgele işaret -> ortalama dağılımı
            rng = np.random.default_rng(7); pool = (K.fwd(R, h).dropna() * 1e4).values
            bs = np.array([np.mean(rng.choice(pool, len(v)) * rng.choice([-1, 1], len(v))) for _ in range(4000)])
            p_bs = (np.abs(bs) >= abs(v.mean())).mean()
            pre = v[pd.to_datetime(x.loc[v.index, "react"]) < pd.Timestamp("2022-01-01")]; post = v[pd.to_datetime(x.loc[v.index, "react"]) >= pd.Timestamp("2022-01-01")]
            out.append(dict(inst=inst, set=sel, h=h, n=len(v), mean_bps=v.mean(), med_bps=v.median(), t=t, p_boot=p_bs, hit=(v > 0).mean(),
                            net8=v.mean() - 8, net15=v.mean() - 15, net_idx3=v.mean() - 3,
                            pre2022_n=len(pre), pre2022=pre.mean(), post2022_n=len(post), post2022=post.mean(),
                            down_n=int((x.loc[v.index, "dir"] < 0).sum()), down_mean=v[x.loc[v.index, "dir"] < 0].mean(),
                            up_n=int((x.loc[v.index, "dir"] > 0).sum()), up_mean=v[x.loc[v.index, "dir"] > 0].mean(), sd_all=sd_all))
O = pd.DataFrame(out); O.to_csv(K.RES + "/c_rating_summary.csv", index=False)
pd.set_option("display.width", 250)
print(O.round(2).to_string())
print(D[D["inst"] == "F_XU030"].round(0).to_string())
# 47 hisse: tepki günü uzlaşması -> h=2, ters yön, hisse başına ortalama (notch+outlook)
x = ev[ev["cls"] != "review"]
rows = []
for s in K.STOCKS:
    R = F[s].dropna(); cal = R.index; vals = {h: [] for h in (1, 2, 3)}
    for _, e in x.iterrows():
        if e["react_date"] not in cal: continue
        i = cal.get_loc(e["react_date"])
        for h in (1, 2, 3):
            if i + h < len(cal): vals[h].append(-e["dir"] * R.iloc[i + 1:i + 1 + h].sum() * 1e4)
    for h in (1, 2, 3):
        v = np.array(vals[h])
        if len(v) >= 6: rows.append(dict(stock=s, h=h, n=len(v), mean=v.mean(), t=v.mean() / (v.std(ddof=1) / np.sqrt(len(v)))))
X = pd.DataFrame(rows); X.to_csv(K.RES + "/c_rating_47.csv", index=False)
print(X.groupby("h")[["n", "mean", "t"]].median().round(2)); print((X.groupby("h")["mean"].apply(lambda s: (s > 0).mean())).round(2))
p = K.t2p(X["t"]); rej, pa = K.bh(p); print("47 hisse FDR geçen:", rej.sum(), "/", len(X))
