"""sektor_tematik aday stratejileri: tekrar üretilebilir betik. Çalıştırınca tüm sayıları basar ve
sonuclar/aile_sektor_tematik/aday_<id>_*.csv dosyalarını yazar.
Kullanım: python3 -I kod/ajan_sektor_tematik/strateji_adaylari.py

S1  SMH IBS<0.20 -> SMH al (C0: t kapanışı), t+1 kapanışında sat.
S2  Aynı sinyal (SMH verisi) -> SOXL (3x) ile uygula (S1'in kaldıraçlı aracı; bağımsız kanıt DEĞİL).
IBS = (Kapanış - Gün içi en düşük) / (Gün içi en yüksek - Gün içi en düşük), aynı günün verisiyle.
Zamanlama: lib.py ZAMANLAMA SÖZLEŞMESİ (C0 / O1 / C1)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from havuz import *

pd.set_option("display.width", 250); pd.set_option("display.max_rows", 200)


def sig_ibs(sym, th=0.2):
    return lib.ibs(D(sym)) < th


def full(sym, sig, h, mode, pos=2500.0):
    df = D(sym)
    s, tr = lib.evaluate(df, sig, h, mode, cost_for(df, pos))
    s["p"] = lib.t_to_p(s.get("t", np.nan), s.get("n", 0))
    return s, tr


def report(cid, sig_sym, trade_sym, h=1, mode="C0", th=0.2, others=None):
    print("=" * 100)
    print(f"{cid}: sinyal {sig_sym} IBS<{th}  ->  işlem {trade_sym}, giriş {mode}, tutuş h={h}")
    sig = sig_ibs(sig_sym, th)
    s, tr = full(trade_sym, sig, h, mode)
    keys = ["n", "mean_gross_bp", "mean_net_bp", "median_net_bp", "win", "pf", "t", "p", "is_n", "is_net_bp", "is_t",
            "oos_n", "oos_net_bp", "oos_t", "years_pos_frac", "n_years", "maxdd", "worst_bp", "edge_bp", "t_edge", "cost_bp", "days_in_mkt"]
    main = {k: s.get(k) for k in keys}
    print("ANA SONUÇ (2.500 $ pozisyon):"); print(pd.Series(main).round(3).to_string())
    tr.to_csv(os.path.join(OUT, f"aday_{cid}_islemler.csv"), index=False)
    # yıllık
    yr = tr.groupby(tr.sig_date.dt.year).agg(n=("net", "size"), net_bp=("net", lambda x: x.mean() * 1e4), toplam_pct=("net", lambda x: x.sum() * 100))
    print("\nYIL BAZINDA:"); print(yr.round(1).to_string())
    # maliyet duyarlılığı
    rows = []
    for pos in (1000.0, 2500.0, 10000.0):
        ss, _ = full(trade_sym, sig, h, mode, pos)
        rows.append({"pozisyon_usd": pos, "maliyet_bp": ss["cost_bp"], "net_bp": ss["mean_net_bp"], "t": ss["t"],
                     "is_net_bp": ss["is_net_bp"], "oos_net_bp": ss["oos_net_bp"], "pf": ss["pf"]})
    md = pd.DataFrame(rows); print("\nMALİYET DUYARLILIĞI:"); print(md.round(2).to_string())
    # mod sağlamlığı
    rows = []
    for m in ("C0", "O1", "C1"):
        for hh in (1, 2, 3):
            ss, _ = full(trade_sym, sig, hh, m)
            rows.append({"mode": m, "h": hh, "n": ss["n"], "brut_bp": ss["mean_gross_bp"], "kosulsuz_bp": ss.get("uncond_bp"),
                         "kenar_bp": ss.get("edge_bp"), "net_bp": ss["mean_net_bp"], "t": ss["t"], "is_net_bp": ss["is_net_bp"],
                         "oos_net_bp": ss["oos_net_bp"], "yil_poz": ss["years_pos_frac"]})
    mm = pd.DataFrame(rows); print("\nGİRİŞ MODU / TUTUŞ SAĞLAMLIĞI:"); print(mm.round(2).to_string())
    # komşu eşikler (yalnız rapor; seçim yapılmadı)
    rows = []
    for t2 in (0.10, 0.15, 0.20, 0.25, 0.30):
        ss, _ = full(trade_sym, sig_ibs(sig_sym, t2), h, mode)
        rows.append({"esik": t2, "n": ss["n"], "net_bp": ss["mean_net_bp"], "t": ss["t"], "is_net_bp": ss["is_net_bp"], "oos_net_bp": ss["oos_net_bp"]})
    nb = pd.DataFrame(rows); print("\nKOMŞU EŞİKLER (seçim için kullanılmadı):"); print(nb.round(2).to_string())
    oth = None
    if others:
        rows = []
        for o in others:
            if o not in lib.available(): continue
            ss, _ = full(o, sig_ibs(o, th), h, mode)
            rows.append({"etf": o, "kume": CL_OF.get(o, "-"), "n": ss["n"], "net_bp": ss["mean_net_bp"], "t": ss["t"],
                         "is_net_bp": ss["is_net_bp"], "oos_net_bp": ss["oos_net_bp"], "yil_poz": ss["years_pos_frac"]})
        oth = pd.DataFrame(rows).sort_values("t", ascending=False)
        print("\nAYNI KURAL (kendi IBS'i, kendisinde işlem) AİLEDEKİ DİĞER ETF'LERDE:"); print(oth.round(2).to_string())
        print("pozitif net oranı:", round((oth.net_bp > 0).mean(), 2), " t>=2 sayısı:", int((oth.t >= 2).sum()), "/", len(oth))
    md.to_csv(os.path.join(OUT, f"aday_{cid}_maliyet.csv"), index=False)
    mm.to_csv(os.path.join(OUT, f"aday_{cid}_modlar.csv"), index=False)
    return s, tr


if __name__ == "__main__":
    others = REPS + ["SOXX", "QQQ"]
    s1, tr1 = report("sektor_tematik_S1", "SMH", "SMH", 1, "C0", 0.2, others)
    # QQQ ile ayrıştırma: SMH'nin kenarı QQQ'nun kendi IBS etkisinden mi?
    smh = D("SMH"); ibq = lib.ibs(D("QQQ")).reindex(smh.index); ibs_ = lib.ibs(smh)
    print("\nAYRIŞTIRMA (SMH'de işlem, C0 h1):")
    for nm, sg in (("SMH<0.2 & QQQ<0.2", (ibs_ < 0.2) & (ibq < 0.2)), ("SMH<0.2 & QQQ>=0.2", (ibs_ < 0.2) & (ibq >= 0.2)),
                   ("QQQ<0.2 (QQQ sinyali)", ibq < 0.2)):
        ss, _ = full("SMH", sg, 1, "C0"); print(f"  {nm:24s} n={ss['n']:4d} net={ss['mean_net_bp']:7.1f} bp t={ss['t']:.2f} IS={ss['is_net_bp']:.1f} OOS={ss['oos_net_bp']:.1f}")
    trh = add_hedge(tr1.assign(sym="SMH"), "SMH", "C0", "QQQ")
    print(f"  QQQ beta-hedge'li ortalama: {trh.hedged.mean()*1e4:.1f} bp (t={tstat(trh.hedged):.2f})  [teşhis; Midas'ta açığa satış yok]")
    s2, tr2 = report("sektor_tematik_S2", "SMH", "SOXL", 1, "C0", 0.2, None)
    # S2: SOXX sinyaliyle de
    ss, _ = full("SOXL", sig_ibs("SOXX"), 1, "C0")
    print(f"\nS2 varyant: SOXX IBS<0.2 -> SOXL C0 h1: n={ss['n']} net={ss['mean_net_bp']:.1f} t={ss['t']:.2f} IS={ss['is_net_bp']:.1f} OOS={ss['oos_net_bp']:.1f}")
    # risk: en kötü 5 işlem
    for nm, tx in (("S1", tr1), ("S2", tr2)):
        w = tx.nsmallest(5, "net")
        print(f"\n{nm} en kötü 5 işlem:"); print(w[["sig_date", "exit_date"]].assign(net_bp=(w["net"] * 1e4).round(1)).to_string())
    # son sinyaller (izleme için)
    last = ibs_.tail(10)
    print("\nSon 10 gün SMH IBS:"); print(last.round(3).to_string())
