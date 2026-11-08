"""Denetim S1: EIA doğalgaz depolama raporu öncesi KOLD long (Kasım-Mart). Bağımsız yeniden üretim + sağlamlık.
Çalıştırma: python3 -I kod/denetim_enerji_tarim/d_s1_eia_kold.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import dsim as D, lib

pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
rng = np.random.default_rng(20261107)
ev = pd.read_csv(os.path.join(lib.ROOT, "data", "events", "eia_ng_storage.csv"), parse_dates=["date"])
rep_dates = pd.DatetimeIndex(ev["date"]).normalize()
WIN = [11, 12, 1, 2, 3]


def eve_signal(df, months=None, dates=rep_dates):
    """t = rapor gününden bir önceki işlem günü (rapor günü df.index'te olmalı)."""
    idx = df.index; pos = idx.get_indexer(dates); pos = pos[pos > 0]
    s = np.zeros(len(idx), bool)
    for p in pos:
        if months is None or idx[p].month in months:
            s[p - 1] = True
    return s



if __name__ == "__main__":
    rows = []
    k = lib.load("KOLD"); cK = D.cost("KOLD")
    sigW = eve_signal(k, WIN); sigA = eve_signal(k)
    print("KOLD maliyet 2500$:", cK, "| rapor tarihi KOLD index'te olmayan:", int((k.index.get_indexer(rep_dates[(rep_dates >= k.index[0]) & (rep_dates <= k.index[-1])]) < 0).sum()))
    for mode in ("C0", "O1", "C1"):
        for h in (1, 2, 3):
            tr = D.sim(k, sigW, h, mode); rows.append({"kural": "S1 Kas-Mar", "sym": "KOLD", "mode": mode, "h": h, **D.st(tr, cK)})
            tr = D.sim(k, sigA, h, mode); rows.append({"kural": "EN01 tam yil", "sym": "KOLD", "mode": mode, "h": h, **D.st(tr, cK)})
    res = pd.DataFrame(rows)
    cols = ["kural", "sym", "mode", "h", "n", "brut_bp", "net_bp", "t", "kazanma", "pf", "is_net_bp", "is_t", "oos_net_bp", "oos_t", "yil_poz", "maxdd", "en_kotu_bp", "en_iyi_bp"]
    print(res[cols].round(2).to_string(index=False))
    res.to_csv(os.path.join(D.OUT, "s1_mod_izgara.csv"), index=False)

    tr = D.sim(k, sigW, 1, "C0")
    base = D.st(tr, cK)
    print("\n== S1 temel (C0 h1, 2500$):", {kk: round(v, 3) if isinstance(v, float) else v for kk, v in base.items()})
    for pos in (1000, 2500, 10000):
        print(f"  pozisyon {pos}$: maliyet {D.cost('KOLD', pos):.1f} bp, net {base['brut_bp'] - D.cost('KOLD', pos):.1f} bp, t {D.st(tr, D.cost('KOLD', pos))['t']:.2f}")
    print("\nYıl yıl (net, 2500$):"); yy = D.yearly(tr, cK); print(yy.round(1).to_string())
    yy.to_csv(os.path.join(D.OUT, "s1_yillik.csv"))

    # en büyük 5 kazanç / kayıp
    tr2 = tr.copy(); tr2["net_bp"] = (tr2["brut"] * 1e4 - cK)
    ung = lib.load("UNG"); ru = ung["c"].pct_change()
    tr2["UNG_cikis_gunu_bp"] = [ru.get(d, np.nan) * 1e4 for d in tr2["cikis"]]
    print("\nEn iyi 5:"); print(tr2.nlargest(5, "net_bp").round(1).to_string(index=False))
    print("En kötü 5:"); print(tr2.nsmallest(5, "net_bp").round(1).to_string(index=False))
    tr2.to_csv(os.path.join(D.OUT, "s1_islemler.csv"), index=False)

    # en iyi 5 çıkarılınca, 2020 / 2022 hariç
    def sub(mask, lab):
        t_ = tr[mask.to_numpy()].reset_index(drop=True); s = D.st(t_, cK)
        print(f"  {lab}: n={s['n']} net={s['net_bp']:.1f} t={s['t']:.2f} IS={s['is_net_bp']:.1f} OOS={s['oos_net_bp']:.1f}")
        return s
    print("\nAlt örneklemler:")
    top5 = tr["brut"].nlargest(5).index
    sub(~tr.index.to_series().isin(top5), "en iyi 5 hariç")
    sub(~tr.index.to_series().isin(tr["brut"].nlargest(10).index), "en iyi 10 hariç")
    sub(tr["sig"].dt.year != 2020, "2020 hariç")
    sub(tr["sig"].dt.year != 2022, "2022 hariç")
    sub(~tr["sig"].dt.year.isin([2020, 2022]), "2020 ve 2022 hariç")
    sub(tr["sig"] >= "2019-01-01", "2018 sonrası (2018-11-15 ani çöküş dahil değil)")
    sub((tr["sig"] < "2018-11-01") | (tr["sig"] > "2018-11-30"), "Kasım 2018 hariç")
    w = tr["brut"].clip(tr["brut"].quantile(0.025), tr["brut"].quantile(0.975))
    print(f"  %2,5 winsorize: brüt {w.mean()*1e4:.1f} net {(w.mean()*1e4 - cK):.1f} t {D.t_of(w - cK/1e4):.2f}")

    # Permütasyon testleri: aynı sayıda rastgele gün, C0 h1 (örtüşme yok sayılır; tek günlük tutuşta fark yok)
    r1 = (k["c"].shift(-1) / k["c"] - 1)  # t kapanışı -> t+1 kapanışı
    valid = r1.notna().to_numpy() & (k.index >= tr["sig"].min()).astype(bool) & (k.index <= tr["sig"].max()).astype(bool)
    obs = tr["brut"].mean(); n = len(tr); R = 5000
    def perm(pool_mask, lab):
        pool = r1.to_numpy()[pool_mask]
        sims = np.array([rng.choice(pool, n, replace=False).mean() for _ in range(R)])
        p = (np.sum(sims >= obs) + 1) / (R + 1)
        print(f"  {lab}: havuz {pool_mask.sum()} gün, null ort {sims.mean()*1e4:.1f} bp, gözlenen {obs*1e4:.1f} bp, p={p:.4f}")
        return p
    nxt_month = np.array(list(k.index[1:].month) + [k.index[-1].month])
    win_mask = np.isin(nxt_month, WIN)
    print("\nPermütasyon (R=5000, brüt ortalama >= gözlenen):")
    p_all = perm(valid, "tüm günler")
    p_win = perm(valid & win_mask, "yalnız Kas-Mar günleri")
    p_win_nonev = perm(valid & win_mask & ~sigA, "Kas-Mar, rapor arifesi olmayan günler")

    # Haftanın günü (Kas-Mar): t -> t+1 getirisi, t+1 haftanın gününe göre; rapor kaymasıyla etki kayıyor mu?
    d = pd.DataFrame({"r": r1, "wd_next": list(k.index[1:].dayofweek) + [np.nan], "eve": sigA, "win": win_mask}).dropna()
    d = d[d.index >= "2017-01-01"]
    print("\nKas-Mar, ertesi günün haftanın gününe göre KOLD t->t+1 brüt bp (eve=rapor arifesi):")
    print(d[d.win].groupby(["wd_next", "eve"])["r"].agg(n="size", ort_bp=lambda v: v.mean() * 1e4, t=lambda v: D.t_of(v)).round(2).to_string())
    print("\nTüm yıl, rapor günü Perşembe değil (tatil kayması) vs rapor olmayan Perşembe:")
    rep_next = d["eve"]; thu_next = d["wd_next"] == 3
    for lab, m in (("rapor günü, Perşembe değil", rep_next & ~thu_next), ("Perşembe, rapor değil", ~rep_next & thu_next), ("rapor günü Perşembe", rep_next & thu_next)):
        x = d.loc[m, "r"]; print(f"  {lab}: n={len(x)} ort={x.mean()*1e4:.1f} bp t={D.t_of(x):.2f}")

    # Mevsim komşuluğu
    print("\nMevsim tanımları (C0 h1, net, 2500$):")
    seas = {"Eki-Mar": [10, 11, 12, 1, 2, 3], "Kas-Mar": WIN, "Kas-Nis": [11, 12, 1, 2, 3, 4], "Ara-Mar": [12, 1, 2, 3], "Kas-Şub": [11, 12, 1, 2], "Ara-Şub": [12, 1, 2],
            "Eki-Nis": [10, 11, 12, 1, 2, 3, 4], "Nis-Eki": [4, 5, 6, 7, 8, 9, 10], "tam yıl": list(range(1, 13))}
    srows = []
    for nm, ms in seas.items():
        t_ = D.sim(k, eve_signal(k, ms), 1, "C0"); s = D.st(t_, cK); srows.append({"mevsim": nm, **s})
        print(f"  {nm}: n={s['n']} net={s['net_bp']:.1f} t={s['t']:.2f} IS={s['is_net_bp']:.1f} ({s['is_t']:.2f}) OOS={s['oos_net_bp']:.1f} ({s['oos_t']:.2f}) yıl+={s['yil_poz']:.2f}")
    pd.DataFrame(srows).to_csv(os.path.join(D.OUT, "s1_mevsim.csv"), index=False)
    print("\nAy ay (tam yıl rapor arifesi, KOLD brüt bp):")
    mm = tr_all = D.sim(k, sigA, 1, "C0"); mm = mm.assign(m=mm["cikis"].dt.month)
    print(mm.groupby("m")["brut"].agg(n="size", ort_bp=lambda v: v.mean() * 1e4, t=lambda v: D.t_of(v)).round(2).T.to_string())

    # Ailede aynı günler: UNG / BOIL / UNL (dayanak ve ayna)
    print("\nAynı günler, diğer ETF'ler (C0 h1):")
    for sym in ("UNG", "BOIL", "UNL"):
        dd = lib.load(sym); t_ = D.sim(dd, eve_signal(dd, WIN), 1, "C0"); s = D.st(t_, D.cost(sym))
        print(f"  {sym}: n={s['n']} brüt={s['brut_bp']:.1f} net={s['net_bp']:.1f} t_brüt={s['t_brut']:.2f} IS={s['is_net_bp']:.1f} OOS={s['oos_net_bp']:.1f}")

    # Kaldıraç kontrolü: KOLD ~ UNG yıllık beta
    rk = k["c"].pct_change(); bet = pd.DataFrame({"k": rk, "u": ru}).dropna()
    print("\nKOLD~UNG yıllık beta:", bet.groupby(bet.index.year).apply(lambda g: np.polyfit(g["u"], g["k"], 1)[0]).round(2).to_dict())

    pd.Series({"p_perm_tum": p_all, "p_perm_kis": p_win, "p_perm_kis_arife_disi": p_win_nonev}).to_csv(os.path.join(D.OUT, "s1_permutasyon.csv"))
