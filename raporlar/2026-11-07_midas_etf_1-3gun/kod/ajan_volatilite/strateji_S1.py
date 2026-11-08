"""volatilite_S1 — Kısa-vol ETF'sinde 2 günlük RSI dibi (yükselen trendde) — TEKRAR ÜRETİLEBİLİR BETİK.
Kural (t kapanışında, SVXY verisiyle):
    RSI(2) [Wilder, kapanış] < 10  VE  SVXY kapanışı > SMA(200) [kapanış]
  -> SVXY long. Giriş: C0 = t kapanışı (TR kış ~23:50-23:59) ya da O1 = t+1 açılış (TR kış 17:30).
     Çıkış: t+2 kapanışı (h=2). Pozisyondayken yeni sinyal yok sayılır.
  Agresif varyant: aynı SVXY sinyaliyle SVIX (-1x) al (2022-03+ veri).
Çalıştırma: python3 -I kod/ajan_volatilite/strateji_S1.py
Önce (FDR için) şu betikler çalışmış olmalı: hipotez_testleri.py, aday_rsi2.py, ek_testler.py (CSV'leri okur)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, pandas as pd
import vlib, lib, aday_rsi2

def signal_svxy():
    sv = lib.load("SVXY")
    return aday_rsi2.sig_rsi2(sv, 10, 200), sv

def line(tag, s):
    return (f"{tag:<28} n={s['n']:>3}  brüt={s['mean_gross_bp']:7.1f}  net(2.5k)={s['mean_net_bp']:7.1f}  net(1k)={s['net_1000_bp']:7.1f}  "
            f"net(10k)={s['net_10000_bp']:7.1f}  t={s['t']:5.2f}  kazanma={s['win']:.2f}  PF={s['pf']:.2f}  "
            f"IS={s['is_net_bp']:7.1f}(t{s['is_t']:5.2f},n{s['is_n']})  OOS={s['oos_net_bp']:7.1f}(t{s['oos_t']:5.2f},n{s['oos_n']})  "
            f"yıl+={s['years_pos_frac']:.2f}  maxDD={s['maxdd']*100:6.1f}%  en_kötü={s['worst_bp']:7.0f}bp")

def main():
    sig, sv = signal_svxy()
    print("=== volatilite_S1: RSI2(SVXY)<10 & SVXY>SMA200 -> SVXY long ===")
    out = {}
    for mode in ("C0", "O1", "C1"):
        for h in (1, 2, 3):
            s, tr = vlib.ev(sv, sig, h, mode)
            out[(mode, h)] = (s, tr)
            print(line(f"SVXY {mode} h={h}", s))
    s, tr = out[("C0", 2)]
    print("\nAna kural SVXY C0 h=2 — yıllara göre (işlem sayısı, net toplam bp):")
    g = tr.groupby(tr.sig_date.dt.year)["net"]
    print(pd.DataFrame({"n": g.count(), "net_toplam_bp": (g.sum() * 1e4).round(0)}).T.to_string())
    print("Kuyruk dönemleri:", vlib.tail_report(tr))
    print("En kötü 3 işlem (net bp):", [(str(r.sig_date.date()), round(r.net * 1e4)) for r in tr.nsmallest(3, "net").itertuples()])
    so, tro = out[("O1", 2)]
    print("Ana kural SVXY O1 h=2 kuyruk:", vlib.tail_report(tro))
    # aile içi: SVIX (aynı SVXY sinyali), SVXY_EK (2017-07+ sentetik ek), vekil 2009+
    print("\n=== Aile içi / uzun dönem (aynı dayanak; bağımsız kanıt DEĞİL) ===")
    svix = lib.load("SVIX")
    for mode in ("C0", "O1", "C1"):
        s2, _ = vlib.ev(svix, sig.reindex(svix.index).fillna(False), 2, mode)
        print(line(f"SVIX (SVXY sinyali) {mode} h=2", s2))
    ek = vlib.stitched_svxy(); sek = aday_rsi2.sig_rsi2(ek)
    for mode in ("C0", "O1"):
        s3, _ = vlib.ev(ek, sek, 2, mode, cost_df=sv)
        print(line(f"SVXY_EK {mode} h=2", s3))
    px = vlib.synth_proxy(-0.5); spx = aday_rsi2.sig_rsi2(px)
    for mode in ("C0", "C1"):
        s4, tr4 = vlib.ev(px, spx, 2, mode, cost_df=sv)
        print(line(f"VEKIL_S05 {mode} h=2", s4))
        q = tr4[tr4.sig_date < "2019-01-01"]
        print(f"    vekil 2010-2018 alt dönemi: n={len(q)}, net ort={q.net.mean()*1e4:.1f} bp, t={q.net.mean()/q.net.std(ddof=1)*np.sqrt(len(q)):.2f}")
    # ayna: VXX'te RSI2>90 & VXX<SMA200 (uzun vol al) -> beklenen negatif
    vxx = lib.load("VXX"); sm = aday_rsi2.sig_mirror(vxx)
    for mode in ("C0", "O1", "C1"):
        s5, _ = vlib.ev(vxx, sm, 2, mode)
        print(line(f"VXX ayna {mode} h=2", s5))
    # test sayısı ve BH-FDR
    print("\n=== Çoklu test ===")
    P = []
    g = pd.read_csv(os.path.join(lib.ROOT, "sonuclar", "genel_tum.csv"))
    g = g[g.sym.isin(vlib.FAM)]
    P += list(g["p"].values)
    n_gen = len(g)
    files = ["hipotez_testleri.csv", "ek_testler.csv", "aday_rsi2_ozet.csv"]
    n_my = 0
    for f in files:
        d = pd.read_csv(os.path.join(vlib.OUT, f))
        if f == "aday_rsi2_ozet.csv":
            d = d[d.arac != "SVXY"]  # SVXY satırları genel kütüphanenin kopyası
        P += list(d["p"].values); n_my += len(d)
        print(f"  {f}: {len(d)} test")
    nb = pd.read_csv(os.path.join(vlib.OUT, "aday_rsi2_komsu.csv"))
    from scipy import stats as st
    nb_p = [float(2 * st.t.sf(abs(t), n - 1)) if np.isfinite(t) and n > 2 else np.nan for t, n in zip(nb["t"], nb["n"])]
    P += nb_p; n_my += len(nb)
    P = np.array(P, float)
    pass_mask = lib.bh_fdr(P, 0.10)
    thr = np.nanmax(np.where(pass_mask, P, np.nan)) if pass_mask.any() else np.nan
    print(f"  genel kütüphane (aile ETF'leri): {n_gen} test; aile ajanı ek testleri: {n_my} test; TOPLAM {len(P)}")
    print(f"  BH-FDR q=0.10: geçen {int(pass_mask.sum())} test; geçiş eşiği p <= {thr:.5f}")
    for mode, h in [("C0", 2), ("O1", 2), ("C0", 1)]:
        s, _ = out[(mode, h)]
        print(f"  SVXY {mode} h={h}: p={s['p']:.5f} -> FDR {'GEÇER' if s['p'] <= thr else 'geçmez'}")
    # güncel durum
    x = vlib.ctx(sv.index)
    last = sv.index[-1]
    print(f"\nSon gün {last.date()}: SVXY={sv['raw_c'].iloc[-1]:.2f}, RSI2={lib.rsi(sv['c'], 2).iloc[-1]:.1f}, "
          f"SMA200={lib.sma(sv['c'], 200).iloc[-1]:.2f}, VIX/VIX3M={x['R3M'].iloc[-1]:.3f} -> sinyal {'VAR' if sig.iloc[-1] else 'YOK'}")

if __name__ == "__main__":
    main()
