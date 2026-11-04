"""DENETİM — pratik kuralın BAĞIMSIZ backtest'i (bt_pratik.py / cl_t.py import EDİLMEZ).
Kural: pozisyon yokken |z_t|>thr -> yön(z_t), t günü vadeye >=3 BIST işlem günü kalan en yakın standart F_TUPRS kontratı, t uzlaşmasında aç.
Çıkış günü e=s+h: |z_e|>thr aynı yön -> UZAT (kontratın e'de <3 iş günü kaldıysa e uzlaşmasında roll), ters yön -> ÇEVİR
(kapat + o günün ön vadesinde ters aç), aksi halde KAPAT. Pozisyon içinde sinyale bakılmaz.
Getiri: tutulan kontratın kendi uzlaşma zinciri ln(settle/prev_settle) (prev_settle yoksa önceki BIST gününün uzlaşması).
Maliyet: pozisyon başına 1 tur (8 ya da 15 bps) + 2 tik/fiyat; her roll +1 tur. Tik 0,01 TL (2025 öncesi), 0,05 TL (2025+).
TL: 1 kontrat = 100 pay; segment başına d*100*S_giriş*(exp(lr)-1) (DOĞRUSAL vadeli kâr/zarar; kısa için 1-exp(lr)).
z kaynağı: --z bagimsiz (z_bagimsiz.py) ya da --z arastirma (cl.py c1_ref mantığı, eski veri + yeni günler bağımsızdan)."""
import os, sys, json, argparse, numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
D = S + "/out/rehber/tuprs/denetim"
sys.path.insert(0, D + "/kod")
import z_bagimsiz as zb

def tstat(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    return x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 4 and x.std(ddof=1) > 0 else np.nan

def load_contracts(cal):
    cols = ["date", "code", "expiry", "settle", "prev_settle", "close", "value_tl"]
    p = pd.read_parquet(S + "/data/viop_panel.parquet", columns=cols)
    q = pd.read_parquet(S + "/dl_k_sahol_a/viop_new.parquet", columns=cols)
    q = q[q["date"] > p["date"].max()]
    for c in ("code",): p[c] = p[c].astype(str); q[c] = q[c].astype(str)
    x = pd.concat([p, q], ignore_index=True)
    x = x[x["code"].str.fullmatch(r"F_TUPRS\d{4}")].copy()
    x["date"] = pd.DatetimeIndex(x["date"]).normalize(); x["expiry"] = pd.DatetimeIndex(x["expiry"]).normalize()
    x = x[x["settle"] > 0]
    # takvimin ötesindeki vadeler için iş günü uzantısı (Kasım–Aralık 2026'da tam gün tatil yok; 2027-01-01 hariç)
    ext = pd.bdate_range(cal[-1] + pd.Timedelta(days=1), "2027-03-31")
    ext = ext[~ext.isin(pd.to_datetime(["2027-01-01"]))]
    fullcal = cal.append(ext)
    pos = {d: i for i, d in enumerate(fullcal)}
    ecount = np.searchsorted(fullcal.values, x["expiry"].values, side="right") - 1   # vadeye eşit/önceki son iş günü
    x["tdl"] = ecount - np.array([pos[d] for d in x["date"]])
    C = {}
    for code, g in x.groupby("code"):
        g = g.set_index("date").sort_index()
        C[code] = g
    return x, C

def build_lr(C, cal):
    """kontrat -> pd.Series(gün -> log getiri), takvimde ardışık."""
    prev = pd.Series(cal[:-1], index=cal[1:])
    L = {}
    for code, g in C.items():
        ps = g["prev_settle"].where(g["prev_settle"] > 0)
        pd_ = prev.reindex(g.index)
        fb = g["settle"].reindex(pd_.values).values  # önceki BIST günü uzlaşması (varsa)
        ps = ps.fillna(pd.Series(fb, index=g.index))
        L[code] = np.log(g["settle"] / ps)
    return L

def front_map(x):
    f = x[x["tdl"] >= 3].sort_values(["date", "expiry"]).groupby("date").head(1).set_index("date")
    return f["code"]

def simulate(z, cal, C, L, FR, thr=1.0, h=2):
    zz = z.reindex(cal).values; n = len(cal)
    def seg(code, i0, i1):
        if code not in L: return np.nan
        s = 0.0
        for j in range(i0 + 1, i1 + 1):
            v = L[code].get(cal[j], np.nan)
            if not np.isfinite(v): return np.nan
            s += v
        return s
    def tdl(code, i):
        g = C[code]; return int(g.at[cal[i], "tdl"]) if cal[i] in g.index else -9
    pos_rows = []; openpos = None
    i = 0
    while i < n:
        zi = zz[i]
        if not (np.isfinite(zi) and abs(zi) > thr) or cal[i] not in FR.index:
            i += 1; continue
        d = np.sign(zi); code = FR.at[cal[i]]
        if i + h < n and not np.isfinite(seg(code, i, i + h)):
            i += 1; continue
        segs = []; s = i; still_open = False
        while True:
            e = s + h
            if e >= n:
                openpos = dict(giris=cal[s if not segs else segs[0][1]], yon=int(d), kontrat=code, blok_bas=cal[s], gun_gecen=n - 1 - s,
                               tamam_blok=len(segs)); still_open = True; i = n; break
            g = seg(code, s, e)
            segs.append((code, s, e, g, float(C[code].at[cal[s], "settle"]), float(C[code].at[cal[e], "settle"])))
            ze = zz[e]
            if np.isfinite(ze) and abs(ze) > thr and cal[e] in FR.index:
                if np.sign(ze) == d:
                    nc = code if tdl(code, e) >= 3 else FR.at[cal[e]]
                    if e + h < n and not np.isfinite(seg(nc, e, e + h)):
                        i = e + 1; break
                    code = nc; s = e; continue
                i = e; break  # çevir
            i = e + 1; break
        if segs and not still_open:
            pos_rows.append(segs_to_row(segs, d, cal))
    return pd.DataFrame(pos_rows).set_index("giris") if pos_rows else pd.DataFrame(), openpos

def tick(d): return 0.05 if d >= pd.Timestamp("2025-01-01") else 0.01

def segs_to_row(segs, d, cal):
    lr = sum(sg[3] for sg in segs)
    nroll = sum(1 for k in range(1, len(segs)) if segs[k][0] != segs[k - 1][0])
    e0 = segs[0][4]
    tl = 0.0
    # doğrusal kâr/zarar: aynı kontrat ardışık segmentleri birleştir
    k = 0
    while k < len(segs):
        code = segs[k][0]; lrc = 0.0; ent = segs[k][4]
        while k < len(segs) and segs[k][0] == code:
            lrc += segs[k][3]; k += 1
        tl += d * 100 * ent * (np.exp(lrc) - 1)
    tick_bps = [2 * tick(cal[segs[0][1]]) / e0 * 1e4] + [2 * tick(cal[segs[k][1]]) / segs[k][4] * 1e4 for k in range(1, len(segs)) if segs[k][0] != segs[k - 1][0]]
    return dict(giris=cal[segs[0][1]], cikis=cal[segs[-1][2]], yon=int(d), kontrat=segs[0][0], son_kontrat=segs[-1][0], blok=len(segs),
                gun=segs[-1][2] - segs[0][1], roll=nroll, giris_fiyat=e0, brut_log_bps=d * lr * 1e4, brut_tl=tl, brut_dog_bps=tl / (100 * e0) * 1e4,
                tik_bps=sum(tick_bps), n_tur=1 + nroll)

def stats(Pz, base, col="brut_log_bps", split="2022-01-01"):
    net = Pz[col] - base * Pz["n_tur"] - Pz["tik_bps"]
    net_tl = Pz["brut_tl"] - (base * Pz["n_tur"] + Pz["tik_bps"]) / 1e4 * 100 * Pz["giris_fiyat"]
    idx = Pz.index; yrs = (idx[-1] - idx[0]).days / 365.25
    isd = idx < pd.Timestamp(split)
    per = {}
    for lab, a, b in [("2017-19", "2017", "2020"), ("2020-21", "2020", "2022"), ("2022-23", "2022", "2024"), ("2024-26", "2024", "2027")]:
        m = (idx >= a) & (idx < b); per[lab] = (round(net[m].mean(), 1), round(tstat(net[m]), 2), int(m.sum()))
    srt = net.sort_values()
    cum = net.cumsum(); dd = (cum - cum.cummax()); ctl = net_tl.cumsum(); ddtl = ctl - ctl.cummax()
    m24 = idx >= "2024-01-01"; c24 = net_tl[m24].cumsum(); dd24 = (c24 - c24.cummax()).min()
    streak = 0; best = 0
    for v in net.values:
        streak = streak + 1 if v < 0 else 0; best = max(best, streak)
    return dict(n=len(net), yil=round(len(net) / yrs, 1), ort_gun=round(Pz["gun"].mean(), 2), gun_dag=Pz["gun"].value_counts().sort_index().to_dict(),
                brut=round(Pz[col].mean(), 1), net=round(net.mean(), 1), t=round(tstat(net), 2), isabet=round((net > 0).mean(), 3),
                IS=(round(net[isd].mean(), 1), round(tstat(net[isd]), 2), int(isd.sum())), OOS=(round(net[~isd].mean(), 1), round(tstat(net[~isd]), 2), int((~isd).sum())),
                donem=per, yillar={int(k): int(round(v)) for k, v in net.groupby(idx.year).mean().items()},
                top10_haric=(round(srt.iloc[:-10].mean(), 1), round(tstat(srt.iloc[:-10]), 2)),
                en_kotu=(str(srt.index[0].date()), round(srt.iloc[0], 0)), maxdd_bps=round(dd.min(), 0),
                maxdd_bps_tarih=(str(cum[:dd.idxmin()].idxmax().date()), str(dd.idxmin().date())),
                tl_ort=round(net_tl.mean(), 0), tl_2024_26=round(net_tl[m24].mean(), 0), maxdd_tl=round(ddtl.min(), 0), maxdd_tl_2024_26=round(dd24, 0),
                en_kotu_tl=(str(net_tl.idxmin().date()), round(net_tl.min(), 0)), kayip_serisi=best,
                uzun=(round(net[Pz["yon"] > 0].mean(), 1), int((Pz["yon"] > 0).sum())), kisa=(round(net[Pz["yon"] < 0].mean(), 1), int((Pz["yon"] < 0).sum())))

def research_z():
    sys.path.insert(0, S + "/out/code_k_dis-suruculer_curut"); import cl
    rm = cl.lret("^GSPC", "adj"); RS = []
    for m in zb.MEM:
        r = cl.lret(m, "adj"); b = cl.roll_beta(r, rm.reindex(r.index), 250, 100); RS.append((r - b * rm.reindex(r.index)).rename(m))
    df = pd.concat(RS, axis=1); P = df.mean(axis=1).where(df.notna().sum(axis=1) >= 3)
    return cl.zscale(cl.to_bist(P, "after"), 250, 100)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--z", default="bagimsiz"); a = ap.parse_args()
    Z, _ = zb.build()
    cal = Z.index[Z.index <= "2026-11-03"]          # backtest: son tamamlanmış BIST günü 03.11.2026
    z = Z["z"]
    if a.z == "arastirma":
        zr = research_z(); z = zr.combine_first(z)   # 30.10 sonrası günler bağımsızdan
    x, C = load_contracts(cal); L = build_lr(C, cal); FR = front_map(x)
    out = {}
    Pz, op = simulate(z, cal, C, L, FR, 1.0, 2)
    Pz = Pz[Pz.index >= "2017-03-06"]
    for base in (8, 15):
        out[f"log_{base}+tik"] = stats(Pz, base)
        out[f"dogrusal_{base}+tik"] = stats(Pz, base, col="brut_dog_bps")
    out["acik"] = {k: str(v) for k, v in (op or {}).items()}
    Pz.round(3).to_csv(D + f"/sonuc/bt_bagimsiz_pozisyonlar_{a.z}.csv")
    # duyarlılık: eşik ±0,25, tutma 1/2/3
    G = []
    for thr in (0.75, 1.0, 1.25):
        for h in (1, 2, 3):
            P2, _ = simulate(z, cal, C, L, FR, thr, h); P2 = P2[P2.index >= "2017-03-06"]
            s8 = stats(P2, 8); s15 = stats(P2, 15)
            G.append(dict(esik=thr, h=h, n=s8["n"], yil=s8["yil"], ort_gun=s8["ort_gun"], brut=s8["brut"], net8=s8["net"], t8=s8["t"], net15=s15["net"], t15=s15["t"],
                          IS=s8["IS"][0], IS_t=s8["IS"][1], OOS=s8["OOS"][0], OOS_t=s8["OOS"][1], n24=s8["donem"]["2024-26"][2], net8_24=s8["donem"]["2024-26"][0], t8_24=s8["donem"]["2024-26"][1],
                          top10=s8["top10_haric"][0], top10_t=s8["top10_haric"][1]))
    G = pd.DataFrame(G); G.to_csv(D + f"/sonuc/duyarlilik_{a.z}.csv", index=False)
    out["duyarlilik"] = G.to_dict("records")
    json.dump(out, open(D + f"/sonuc/bt_bagimsiz_{a.z}.json", "w"), ensure_ascii=False, indent=1, default=str)
    print(json.dumps({k: v for k, v in out.items() if k != "duyarlilik"}, ensure_ascii=False, indent=1, default=str))
    print(G.to_string())
