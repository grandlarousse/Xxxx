"""Denetim A merceği: S1'in bağımsız yeniden üretimi (lib.trades/evaluate/thk kullanılmadan).
Çalıştır: python3 -I kod/denetim_tek_hisse_kaldiracli/d2_S1_yeniden.py"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import io, contextlib, math
import numpy as np, pandas as pd
import dk, lib

EXTRA = {"NVDA": 2.84, "TSLA": 2.75, "AAPL": 1.28, "AMZN": 2.13, "META": 1.80, "MSFT": 1.10, "GOOGL": 1.55, "MSTR": 12.96, "COIN": 5.13}
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)

def fmt(s):
    return (f"n {s['n']:4d} (tarih {s.get('n_tarih',0)}) brüt {s['brut_bp']:7.1f} net {s['net_bp']:7.1f} t {s['t']:5.2f} | "
            f"işlem-ağırlıklı {s['net_islem_bp']:6.1f} (t {s['t_islem']:.2f}) | IS {s['is_bp']:6.1f} ({s['is_t']:.2f}) OOS {s['oos_bp']:6.1f} ({s['oos_t']:.2f}) | "
            f"kaz {s['win']:.3f} PF {s['pf']:.2f} yıl+ tarih {s['yil_poz_tarih']:.2f} işlem {s['yil_poz_islem']:.2f} | en kötü {s['en_kotu_bp']:.0f}")

def earn_react_days():
    B = pd.read_csv(os.path.join(dk.ROOT, "sonuclar", "aile_tek_hisse_kaldiracli", "bilanco_tarihleri.csv"), parse_dates=["date"])
    out = {}
    for st, g in B.groupby("sym"):
        idx = dk.load_stock(st).index
        s = set()
        for _, r in g.iterrows():
            a = idx[idx >= r["date"]]
            if not len(a): continue
            pre = "pre-market" in str(r.get("time", ""))
            k = idx.get_loc(a[0])
            if a[0] == r["date"] and not pre: k += 1
            if k < len(idx): s.add(idx[k])
        out[st] = s
    return out

def flag_earn(A, R):
    f = []
    for _, t in A.iterrows():
        idx = dk.load_stock(t.stock).index
        ie = idx.get_loc(t.entry_date); ix = idx.get_loc(t.exit_date)
        f.append(any(idx[j] in R.get(t.stock, set()) for j in range(ie + 1, ix + 1)))
    return np.array(f, bool)

def main():
    res = []
    print("=" * 110)
    print("1) DAYANAK sentetik 2x (bağımsız kalibrasyon: d1_kalibrasyon.csv), 7 mega-cap, 2.500$")
    base = {}
    for m in ("C0", "O1", "C1"):
        A = dk.run(dk.STK, m, extra=EXTRA)
        base[m] = A
        s = dk.summary(A, f"sentetik_{m}"); res.append(s)
        print(f"[{m}] " + fmt(s))
    A = base["C0"]
    A.to_csv(os.path.join(dk.OUT, "d2_islemler_C0.csv"), index=False)
    # Ajanın işlem listesiyle eşleşme
    ag = pd.read_csv(os.path.join(dk.ROOT, "sonuclar", "aile_tek_hisse_kaldiracli", "aday_S1_islemler_dayanak_C0.csv"), parse_dates=["sig_date", "exit_date"])
    k1 = set(zip(A.stock, A.sig_date, A.exit_date)); k2 = set(zip(ag.stock, ag.sig_date, ag.exit_date))
    print(f"Ajan işlem listesiyle eşleşme: denetim {len(k1)}, ajan {len(k2)}, ortak {len(k1 & k2)}, yalnız denetim {len(k1 - k2)}, yalnız ajan {len(k2 - k1)}")
    for x in sorted(k1 ^ k2)[:12]: print("   fark:", x[0], x[1].date(), x[2].date(), "denetimde" if x in k1 else "ajanda")
    # hisse başına
    print("\nHisse başına (C0):")
    for st in dk.STK:
        s = dk.summary(A[A.stock == st], st); print(f"  {st:5s} n {s['n']:3d} net(işlem) {s['net_islem_bp']:7.1f} t {s['t_islem']:.2f} IS {s['is_bp']:.0f} OOS {s['oos_bp']:.0f}")
    # maliyet duyarlılığı
    print("\n2) Maliyet duyarlılığı (pozisyon 1.000 / 2.500 / 10.000 $):")
    for m in ("C0", "O1", "C1"):
        for pos in (1000.0, 2500.0, 10000.0):
            B = dk.run(dk.STK, m, extra=EXTRA, pos=pos); s = dk.summary(B, f"maliyet_{m}_{int(pos)}"); res.append(s)
            print(f"  {m} {int(pos):5d}$: net {s['net_bp']:6.1f} t {s['t']:.2f}  IS {s['is_bp']:.1f} OOS {s['oos_bp']:.1f}")
    # muhafazakâr çıkış (koşul j kapanışında, çıkış j+1 açılışı)
    print("\n3) Muhafazakâr çıkış: koşul kapanışta görülür, ertesi açılışta satılır:")
    for m in ("C0", "O1"):
        B = dk.run(dk.STK, m, extra=EXTRA, exit_next_open=True); s = dk.summary(B, f"cikis_ertesi_acilis_{m}"); res.append(s)
        print(f"  [{m}] " + fmt(s))
    # yıllar
    print("\n4) Yıl yıl (C0; tarih-ortalama net toplamı bp | işlem sayısı | işlem ort. bp):")
    g = A.groupby("sig_date")["net"].mean()
    for y in sorted(set(A.sig_date.dt.year)):
        a = A[A.sig_date.dt.year == y]
        print(f"  {y}: toplam {g[g.index.year == y].sum() * 1e4:8.0f}  n {len(a):3d}  ort {a.net.mean() * 1e4:7.1f}  t {dk.tstat(a.net.values):.2f}")
    for lab, yy in (("2020 hariç", [2020]), ("2022 hariç", [2022]), ("2020 ve 2022 hariç", [2020, 2022]),
                    ("2020 ve 2024 hariç (en iyi iki yıl)", [2020, 2024])):
        for m in ("C0", "O1"):
            Bm = base[m]; mk = ~Bm.sig_date.dt.year.isin(yy)
            s = dk.summary(Bm[mk], f"{lab}_{m}"); res.append(s)
            print(f"  {lab:34s} [{m}] " + fmt(s))
    # en büyük 5 kazanç
    print("\n5) En büyük 5 kazanç (C0) ve veri kalitesi kontrolü:")
    VK = pd.read_csv(os.path.join(dk.ROOT, "sonuclar", "veri_kalitesi.csv"), parse_dates=["date"])
    VD = pd.read_csv(os.path.join(dk.ROOT, "sonuclar", "veri_duzeltmeleri.csv"), parse_dates=["date"])
    R = earn_react_days()
    A["bilanco"] = flag_earn(A, R)
    top = A.sort_values("net", ascending=False).head(5)
    for _, t in top.iterrows():
        sd = dk.load_stock(t.stock)
        r = sd["c"].loc[t.entry_date:t.exit_date].pct_change().dropna()
        e = dk.ETF[t.stock]
        vk = VK[(VK.sym == e) & (VK.date >= t.entry_date) & (VK.date <= t.exit_date)]
        vd = VD[(VD.sym == e) & (VD.date >= t.entry_date) & (VD.date <= t.exit_date)]
        print(f"  {t.stock} sinyal {t.sig_date.date()} çıkış {t.exit_date.date()} brüt {t.gross * 1e4:.0f} bp; hisse günlük: {[(str(i.date()), round(v * 100, 1)) for i, v in r.items()]}; "
              f"bilanço tepki günü tutuşta: {bool(t.bilanco)}; veri_kalitesi satırı: {len(vk)}; veri_duzeltmesi: {len(vd)}")
    for k in (5, 10):
        for m in ("C0", "O1"):
            Bm = base[m].sort_values("net", ascending=False).iloc[k:]
            s = dk.summary(Bm, f"en_iyi_{k}_cikarildi_{m}"); res.append(s)
            print(f"  En iyi {k} işlem çıkarıldı [{m}]: " + fmt(s))
    # bilanço
    print("\n6) Bilanço tepki günü taşıyan işlemler (ajanın bilanco_tarihleri.csv'si, bağımsız işaretleme):")
    for m in ("C0", "O1"):
        Bm = base[m].copy(); Bm["bilanco"] = flag_earn(Bm, R)
        s1 = dk.summary(Bm[Bm.bilanco], f"bilanco_yalniz_{m}"); s2 = dk.summary(Bm[~Bm.bilanco], f"bilanco_haric_{m}")
        res += [s1, s2]
        print(f"  [{m}] yalnız bilanço: n {s1['n']} işlem ort {s1['net_islem_bp']:.0f} bp; hariç: " + fmt(s2))
        Bm.to_csv(os.path.join(dk.OUT, f"d2_islemler_{m}.csv"), index=False)
    # gerçek ETF
    print("\n7) GERÇEK ETF fiyatı (lib.load), sinyal hisseden:")
    for m in ("C0", "O1", "C1"):
        for since, lab in ((None, "tum"), (dk.SWITCH, "2x_donemi")):
            B = dk.run(dk.STK, m, data="etf", since=since); s = dk.summary(B, f"gercek_{lab}_{m}"); res.append(s)
            print(f"  [{m}] {lab:9s} " + fmt(s))
            if m == "C0" and lab == "tum":
                B.to_csv(os.path.join(dk.OUT, "d2_islemler_gercek_C0.csv"), index=False)
                for st in dk.STK:
                    b = B[B.stock == st]; print(f"      {dk.ETF[st]} n {len(b)} net {b.net.mean() * 1e4:.0f} t {dk.tstat(b.net.values):.2f}")
                Bb = B.copy(); Bb["bilanco"] = flag_earn(Bb, R)
                s = dk.summary(Bb[~Bb.bilanco], "gercek_tum_C0_bilanco_haric"); res.append(s)
                print("      bilanço hariç: " + fmt(s))
    # 1.000$ gerçek ETF
    for m in ("C0", "O1"):
        B = dk.run(dk.STK, m, data="etf", pos=1000.0); s = dk.summary(B, f"gercek_tum_{m}_1000"); res.append(s)
        print(f"  [{m}] gerçek ETF 1.000$: net {s['net_bp']:.1f} t {s['t']:.2f}")
    # günlük portföy (1/7 sermaye her hisse kolu), NW t
    print("\n8) Günlük portföy getirisi (her hisseye 1/7 sermaye; pozisyondayken 2x sentetik, maliyet giriş günü düşülür), Newey-West t (5 gecikme):")
    for m in ("C0", "O1"):
        Bm = base[m]
        allidx = dk.load_stock("AAPL").index
        port = pd.Series(0.0, index=allidx); expo = pd.Series(0.0, index=allidx)
        for st in dk.STK:
            sd = dk.load_stock(st); px = dk.synth(sd, extra_bp=EXTRA[st])
            rc = px["c"].pct_change()
            for _, t in Bm[Bm.stock == st].iterrows():
                ie = px.index.get_loc(t.entry_date); ix = px.index.get_loc(t.exit_date)
                if m == "O1":
                    port.iloc[ie] += (px["c"].iloc[ie] / px["o"].iloc[ie] - 1) / 7; expo.iloc[ie] += 1 / 7
                    rng = range(ie + 1, ix + 1)
                else:
                    rng = range(ie + 1, ix + 1)
                for j in rng:
                    port.iloc[j] += rc.iloc[j] / 7; expo.iloc[j] += 1 / 7
                port.loc[t.entry_date] -= t.cost_bp / 1e4 / 7
        port = port.loc[Bm.sig_date.min():]
        ann = port.mean() * 252; vol = port.std() * math.sqrt(252)
        print(f"  [{m}] yıllık ort {ann * 100:.1f}%  oynaklık {vol * 100:.1f}%  Sharpe {ann / vol:.2f}  NW t {dk.nw_t(port.values):.2f}  ort. maruziyet {expo.loc[port.index].mean():.3f}  "
              f"IS NW t {dk.nw_t(port[port.index <= dk.IS_END].values):.2f}  OOS NW t {dk.nw_t(port[port.index > dk.IS_END].values):.2f}")
        eq = (1 + port).cumprod(); print(f"       maxDD {((eq / eq.cummax()) - 1).min() * 100:.1f}%")
    pd.DataFrame(res).to_csv(os.path.join(dk.OUT, "d2_ozet.csv"), index=False)

if __name__ == "__main__":
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        main()
    txt = buf.getvalue(); print(txt)
    open(os.path.join(dk.OUT, "d2_cikti.txt"), "w").write(txt)
