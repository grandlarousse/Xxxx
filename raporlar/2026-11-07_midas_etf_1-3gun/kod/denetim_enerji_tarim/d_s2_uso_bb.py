"""Denetim S2: USO alt Bollinger(20, 2) kapanışı -> t+1 kapanışında gir -> t+3 kapanışında çık (C1 h2).
Bağımsız yeniden üretim + parametre komşuluğu + permütasyon + gecikme profili + tüm evrende aynı kural.
Çalıştırma: python3 -I kod/denetim_enerji_tarim/d_s2_uso_bb.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import dsim as D, lib

pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
rng = np.random.default_rng(7)


def bb_sig(df, n=20, k=2.0, warm=200, ddof=1):
    c = df["c"]; m = c.rolling(n).mean(); sd = c.rolling(n).std(ddof=ddof)
    s = (c < m - k * sd).to_numpy().copy(); s[:warm] = False
    return s


def main():
    uso = lib.load("USO"); cU = D.cost("USO")
    sig = bb_sig(uso)
    print("USO sinyal günü sayısı:", int(sig.sum()), "| maliyet", cU)
    rows = []
    for mode in ("C0", "O1", "C1"):
        for h in (1, 2, 3):
            tr = D.sim(uso, sig, h, mode); rows.append({"mode": mode, "h": h, **D.st(tr, cU)})
    g = pd.DataFrame(rows)
    cols = ["mode", "h", "n", "brut_bp", "net_bp", "t", "kazanma", "pf", "is_n", "is_net_bp", "is_t", "oos_n", "oos_net_bp", "oos_t", "yil_poz", "maxdd", "en_kotu_bp", "en_iyi_bp"]
    print(g[cols].round(2).to_string(index=False)); g.to_csv(os.path.join(D.OUT, "s2_mod_izgara.csv"), index=False)

    tr = D.sim(uso, sig, 2, "C1"); base = D.st(tr, cU)
    for pos in (1000, 2500, 10000):
        print(f"  pozisyon {pos}$: net {base['brut_bp'] - D.cost('USO', pos):.1f} bp t {D.st(tr, D.cost('USO', pos))['t']:.2f}")
    print("\nYıl yıl:"); yy = D.yearly(tr, cU); print(yy.round(1).to_string()); yy.to_csv(os.path.join(D.OUT, "s2_yillik.csv"))
    tr2 = tr.assign(net_bp=tr["brut"] * 1e4 - cU)
    print("\nEn iyi 5:"); print(tr2.nlargest(5, "net_bp").to_string(index=False))
    print("En kötü 5:"); print(tr2.nsmallest(5, "net_bp").to_string(index=False))
    tr2.to_csv(os.path.join(D.OUT, "s2_islemler.csv"), index=False)

    def sub(mask, lab):
        t_ = tr[np.asarray(mask)].reset_index(drop=True); s = D.st(t_, cU)
        print(f"  {lab}: n={s['n']} net={s['net_bp']:.1f} t={s['t']:.2f} IS={s.get('is_net_bp', np.nan):.1f} OOS={s.get('oos_net_bp', np.nan):.1f}")
    print("\nAlt örneklemler:")
    sub(~tr.index.isin(tr["brut"].nlargest(5).index), "en iyi 5 hariç")
    sub(tr["sig"].dt.year != 2020, "2020 hariç")
    sub(tr["sig"].dt.year != 2022, "2022 hariç")
    sub(~tr["sig"].dt.year.isin([2020, 2022]), "2020 ve 2022 hariç")
    sub(tr["sig"] >= "2020-06-01", "Haziran 2020 sonrası (çok vadeli USO)")
    w = tr["brut"].clip(tr["brut"].quantile(0.025), tr["brut"].quantile(0.975))
    print(f"  %2,5 winsorize: net {(w.mean()*1e4 - cU):.1f} t {D.t_of(w - cU/1e4):.2f}")
    # sinyal kümelenmesi: aynı kırılım dalgasından kaç işlem
    gaps = tr["sig"].diff().dt.days
    print("  ardışık işlemler arası takvim günü medyanı:", gaps.median(), "| <=10 gün arayla gelen işlem sayısı:", int((gaps <= 10).sum()))

    # Gecikme profili: sinyalden sonra j. günün ortalama getirisi (tüm sinyal günleri, örtüşmeli, tanımlayıcı)
    r = uso["c"].pct_change()
    pos = np.where(sig)[0]
    prof = []
    for j in range(0, 8):
        x = np.array([r.iloc[p + j] for p in pos if p + j < len(r)]) if j > 0 else np.array([r.iloc[p] for p in pos])
        prof.append({"gun": f"t+{j}", "n": len(x), "ort_bp": x.mean() * 1e4, "t": D.t_of(x)})
    print("\nGecikme profili (tüm sinyal günleri, örtüşmeli; t+0 = sinyal günü):"); print(pd.DataFrame(prof).round(2).to_string(index=False))
    # yalnız işlem açılan sinyaller için t+1..t+4
    prof2 = []
    ix = uso.index
    for j in range(1, 6):
        x = np.array([r.iloc[ix.get_loc(d) + j] for d in tr["sig"] if ix.get_loc(d) + j < len(r)])
        prof2.append({"gun": f"t+{j}", "n": len(x), "ort_bp": x.mean() * 1e4, "t": D.t_of(x)})
    print("Gecikme profili (yalnız işlem açılan 54 sinyal):"); print(pd.DataFrame(prof2).round(2).to_string(index=False))

    # Giriş gecikmesi taraması: C0 kapanışından d gün sonra gir, 2 gün tut (d=0..5)
    lag_rows = []
    for d in range(0, 6):
        s_sh = np.zeros_like(sig); s_sh[d:] = sig[:len(sig) - d] if d else sig
        t_ = D.sim(uso, s_sh, 2, "C0"); s = D.st(t_, cU)
        lag_rows.append({"giris_gecikmesi": d, "h": 2, **{kk: s[kk] for kk in ["n", "brut_bp", "net_bp", "t", "is_net_bp", "is_t", "oos_net_bp", "oos_t"]}})
    print("\nGiriş gecikmesi d (t+d kapanışında gir, 2 gün tut):"); print(pd.DataFrame(lag_rows).round(2).to_string(index=False))

    # Parametre komşuluğu (C1 h2), IS ve OOS ayrı
    pr = []
    for n in (10, 14, 16, 20, 24, 30, 40):
        for k in (1.5, 1.75, 2.0, 2.25, 2.5):
            t_ = D.sim(uso, bb_sig(uso, n, k), 2, "C1"); s = D.st(t_, cU)
            pr.append({"n_bb": n, "k": k, **{kk: s.get(kk, np.nan) for kk in ["n", "net_bp", "t", "is_net_bp", "is_t", "oos_net_bp", "oos_t"]}})
    pr = pd.DataFrame(pr); pr.to_csv(os.path.join(D.OUT, "s2_parametre_komsuluk.csv"), index=False)
    print("\nParametre komşuluğu C1 h2 — net bp:"); print(pr.pivot(index="n_bb", columns="k", values="net_bp").round(0).to_string())
    print("t:"); print(pr.pivot(index="n_bb", columns="k", values="t").round(2).to_string())
    print("IS net bp:"); print(pr.pivot(index="n_bb", columns="k", values="is_net_bp").round(0).to_string())
    print("OOS net bp:"); print(pr.pivot(index="n_bb", columns="k", values="oos_net_bp").round(0).to_string())
    print("n:"); print(pr.pivot(index="n_bb", columns="k", values="n").to_string())

    # Permütasyon: aynı sayıda (54) rastgele gün, aynı C1 h2 yapısı (t+1 kapanış -> t+3 kapanış)
    c = uso["c"]; fr = (c.shift(-3) / c.shift(-1) - 1)
    first = uso.index.get_loc(tr["sig"].iloc[0]); last = len(uso) - 4
    pool = fr.to_numpy()[first:last]; pool = pool[np.isfinite(pool)]
    obs = tr["brut"].mean(); R = 5000; n_ = len(tr)
    sims = np.array([rng.choice(pool, n_, replace=False).mean() for _ in range(R)])
    p_all = (np.sum(sims >= obs) + 1) / (R + 1)
    # rejim eşli: 20 günlük z-getirisi en düşük %15'teki günler (düşüş rejimi), sinyal günleri hariç
    z = (np.log(c).diff(5) / (np.log(c).diff().rolling(60).std() * np.sqrt(5))).to_numpy()
    m = np.isfinite(z) & np.isfinite(fr.to_numpy()) & ~sig
    m[:first] = False; m[last:] = False
    thr = np.nanquantile(z[m], 0.15); pool2 = fr.to_numpy()[m & (z <= thr)]
    sims2 = np.array([rng.choice(pool2, n_, replace=False).mean() for _ in range(R)])
    p_reg = (np.sum(sims2 >= obs) + 1) / (R + 1)
    print(f"\nPermütasyon (R={R}): gözlenen brüt {obs*1e4:.1f} bp | tüm günler null {sims.mean()*1e4:.1f} bp p={p_all:.4f} | düşüş rejimi (5g z alt %15) null {sims2.mean()*1e4:.1f} bp p={p_reg:.4f}")

    # Diğer ETF'ler: USO sinyaliyle ve kendi bandıyla, C1 h2
    orow = []
    for sym in ("BNO", "DBO", "UCO", "USL", "XOP", "XLE", "OIH", "PDBC", "SCO", "GUSH", "ERX"):
        dd = lib.load(sym)
        s_uso = pd.Series(sig, index=uso.index).reindex(dd.index).fillna(False).to_numpy()
        a = D.st(D.sim(dd, s_uso, 2, "C1"), D.cost(sym)); b = D.st(D.sim(dd, bb_sig(dd), 2, "C1"), D.cost(sym))
        orow.append({"sym": sym, "uso_sinyal_net": a["net_bp"], "uso_sinyal_t": a["t"], "uso_IS": a["is_net_bp"], "uso_OOS": a["oos_net_bp"],
                     "kendi_n": b["n"], "kendi_net": b["net_bp"], "kendi_t": b["t"], "kendi_IS": b.get("is_net_bp"), "kendi_OOS": b.get("oos_net_bp")})
    orow = pd.DataFrame(orow); print("\nDiğer ETF'ler C1 h2:"); print(orow.round(2).to_string(index=False))
    orow.to_csv(os.path.join(D.OUT, "s2_aile.csv"), index=False)
    pd.Series({"p_perm_tum": p_all, "p_perm_rejim": p_reg}).to_csv(os.path.join(D.OUT, "s2_permutasyon.csv"))


if __name__ == "__main__":
    main()
