"""Aday stratejilerin tekrar üretilebilir raporu (çalıştırınca bütün sayıları basar).
S1 metal_madenci_S1: Ay sonu (son işlem günü kapanışı) -> yeni ayın 3. işlem günü kapanışı, GDX
S2 metal_madenci_S2: aynı takvim kuralı, GLD (S1 ile aynı etki; bağımsız kanıt değildir)
S3 metal_madenci_S3: GDXJ IBS<0.10 ve kapanış < önceki kapanış -> C0 al, 3 gün tut
S4 metal_madenci_S4: S3 kuralı GLD'de (GLD IBS<0.10 ve düşüş -> C0 al, 3 gün tut)
S5 metal_madenci_S5: SILJ kapanışı 20g Bollinger alt bandının (SMA20 - 2*std20) altında -> ertesi gün kapanışında (C1) al, 3 gün tut
Her biri için: n, brüt/net (2.500$), kazanma, PF, t, IS/OOS, yıl pozitif oranı, maxDD, en kötü işlem, maliyet duyarlılığı
(1.000/2.500/10.000$), mod sağlamlığı (C0/O1/C1), komşu h, ailedeki diğer ETF'ler, yıl içi (yıl ortalamasından arındırılmış) kenar,
2026 gümüş şoku hariç, en iyi yıl hariç, kaldıraçlı uygulama.
Çalıştır: python3 -I kod/ajan_metal_madenci/t5_adaylar.py
Çıktı: sonuclar/aile_metal_madenci/aday_ozet.csv, aday_yillik.csv, aday_islemler_<id>.csv"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import mm, lib, strategies as S

def sig_month_end(df): return S.month_last_day(df.index)
def sig_ibs(df): return (lib.ibs(df) < 0.10) & (df["c"] < df["c"].shift(1))
def sig_bb(df): return df["c"] < lib.sma(df["c"], 20) - 2 * df["c"].rolling(20).std()

CANDS = [
    {"id": "metal_madenci_S1", "ad": "Ay sonu - altın madencileri", "sym": "GDX", "sig": sig_month_end, "h": 3, "mode": "C0",
     "aile": ["GDXJ", "RING", "SIL", "SILJ", "XME", "COPX", "URA", "LIT", "REMX", "GLD", "SLV", "PPLT", "PALL", "CPER", "DBB"],
     "kaldiracli": ["NUGT", "JNUG"]},
    {"id": "metal_madenci_S2", "ad": "Ay sonu - altın (fiziki)", "sym": "GLD", "sig": sig_month_end, "h": 3, "mode": "C0",
     "aile": ["IAU", "GLDM", "SLV", "SIVR", "PPLT", "PALL", "CPER", "DBB"], "kaldiracli": ["UGL"]},
    {"id": "metal_madenci_S3", "ad": "Genç altın madencileri IBS dip alımı", "sym": "GDXJ", "sig": sig_ibs, "h": 3, "mode": "C0",
     "aile": ["GDX", "RING", "SIL", "SILJ", "XME", "COPX", "URA", "GLD", "SLV", "PPLT", "PALL", "CPER", "LIT", "REMX"], "kaldiracli": ["JNUG"]},
    {"id": "metal_madenci_S4", "ad": "Altın (GLD) IBS dip alımı", "sym": "GLD", "sig": sig_ibs, "h": 3, "mode": "C0",
     "aile": ["IAU", "GLDM", "GDX", "GDXJ", "SIL", "SLV", "PPLT", "PALL", "CPER"], "kaldiracli": ["UGL"]},
    {"id": "metal_madenci_S5", "ad": "Genç gümüş madencileri Bollinger alt bant (1 gün bekle)", "sym": "SILJ", "sig": sig_bb, "h": 3, "mode": "C1",
     "aile": ["SIL", "GDX", "GDXJ", "RING", "XME", "COPX", "URA", "GLD", "SLV", "LIT", "REMX"], "kaldiracli": []},
]

def next_month_ends(after, k=3):
    hol = pd.read_csv(os.path.join(mm.ROOT, "data", "events", "nyse_tatil.csv"))
    hol = pd.to_datetime(hol.loc[hol.event == "NYSE_tatil", "date"])
    days = pd.bdate_range(after + pd.Timedelta(days=1), after + pd.Timedelta(days=130))
    days = days[~days.isin(hol)]
    s = pd.Series(days, index=days)
    me = s.groupby([days.year, days.month]).max()
    return [pd.Timestamp(d) for d in me.values if pd.Timestamp(d) > after][:k]

def yil_ici(df, tr, h, mode):
    u = lib.uncond(df, h, mode).dropna()
    uy = u.groupby(u.index.year).mean()
    ex = tr["gross"].values - uy.reindex(tr["sig_date"].dt.year).values
    t = ex.mean() / (ex.std(ddof=1) / math.sqrt(len(ex)))
    yr = pd.Series(ex, index=tr["sig_date"].dt.year).groupby(level=0).mean()
    return ex.mean() * 1e4, t, float((yr > 0).mean())

def main():
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40); pd.set_option("display.max_rows", 300)
    summ, yrows = [], []
    for c in CANDS:
        s0 = c["sym"]; df = mm.load(s0); sig = c["sig"](df)
        st, tr = mm.full(s0, sig, c["h"], c["mode"], df=df)
        print("=" * 110); print(c["id"], c["ad"], "| işlem:", s0, "| mod:", c["mode"], "| h:", c["h"])
        print("ANA:", mm.fmt(st))
        tr.to_csv(os.path.join(mm.OUTD, f"aday_islemler_{c['id']}.csv"), index=False)
        e, te, yp = yil_ici(df, tr, c["h"], c["mode"])
        yr = tr.groupby(tr["sig_date"].dt.year)["net"].sum()
        best_y = yr.idxmax(); m = tr["sig_date"].dt.year != best_y
        x = tr.loc[m, "net"]; t_exb = x.mean() / (x.std(ddof=1) / math.sqrt(len(x)))
        print(f"  yıl içi kenar (yıl ortalaması çıkarılmış brüt): {e:.1f} bp, t={te:.2f}, yılların pozitif oranı={yp:.2f}")
        print(f"  en iyi yıl ({best_y}) hariç: net={x.mean()*1e4:.1f} bp, t={t_exb:.2f}, n={len(x)}")
        print(f"  maliyet duyarlılığı: 1.000$ net={st['net_1000_bp']:.1f} bp | 2.500$ net={st['mean_net_bp']:.1f} | 10.000$ net={st['net_10000_bp']:.1f}"
              f"  (maliyet 2.500$={st['cost_bp']:.1f} bp)")
        ms = mm.modes(s0, sig, c["h"], df=df)
        print("  mod sağlamlığı (n, brüt, net, t):", {k: tuple(round(v, 2) if isinstance(v, float) else v for v in vv) for k, vv in ms.items()})
        for h in (1, 2, 3):
            sh, _ = mm.full(s0, sig, h, c["mode"], df=df)
            print(f"  komşu h={h}: n={sh['n']} brüt={sh['mean_gross_bp']:.1f} net={sh['mean_net_bp']:.1f} t={sh['t']:.2f} IS={sh['is_net_bp']:.1f} OOS={sh['oos_net_bp']:.1f}")
        y = mm.yearly(tr); y["id"] = c["id"]; yrows.append(y.reset_index().rename(columns={"sig_date": "yil"}))
        print("  yıllık:", " ".join(f"{int(i)}:{r.net_bp:.0f}bp(n={int(r.n)})" for i, r in y.iterrows()))
        fam = []
        for s in c["aile"] + c["kaldiracli"]:
            d = mm.load(s); sa, _ = mm.full(s, c["sig"](d), c["h"], c["mode"], df=d)
            fam.append(f"{s}:{sa['mean_net_bp']:.0f}bp/t{sa['t']:.2f}")
        print("  aile (aynı kural, kendi verisiyle):", "; ".join(fam))
        for s in c["kaldiracli"]:
            # kaldıraçlı uygulama: sinyal dayanaktan (s0), işlem kaldıraçlıda
            d = mm.load(s); sk = sig.reindex(d.index).fillna(False)
            sl, _ = mm.full(s, sk, c["h"], c["mode"], df=d)
            print(f"  kaldıraçlı uygulama ({s0} sinyali -> {s} işlemi): {mm.fmt(sl, ('n','mean_gross_bp','mean_net_bp','t','is_net_bp','oos_net_bp','maxdd','worst_bp'))}")
        last_sig = sig.iloc[:-1][sig.iloc[:-1]].index.max()   # son bar ay sonu sayılmasın (veri kesiti)
        print(f"  son (tamamlanmış) sinyal günü: {last_sig.date() if pd.notna(last_sig) else '-'}; veri son günü: {df.index[-1].date()}")
        if c["sig"] is sig_month_end:
            print("  sonraki ay sonu sinyalleri (NYSE takvimi):", ", ".join(str(d.date()) for d in next_month_ends(df.index[-1], 3)))
        st.update({"id": c["id"], "ad": c["ad"], "yil_ici_kenar_bp": e, "t_yil_ici": te, "best_year_excl_net_bp": x.mean() * 1e4,
                   "t_best_year_excl": t_exb, "C0": ms["C0"], "O1": ms["O1"], "C1": ms["C1"], "aile": "; ".join(fam)})
        summ.append(st)
    pd.DataFrame(summ).to_csv(os.path.join(mm.OUTD, "aday_ozet.csv"), index=False)
    pd.concat(yrows).to_csv(os.path.join(mm.OUTD, "aday_yillik.csv"), index=False)

if __name__ == "__main__":
    main()
