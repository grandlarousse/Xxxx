"""Denetim B merceği: S1 istatistiksel sağlamlık.
(a) Rastgele giriş permütasyonu (2.000 tekrar): her hissede aynı sayıda rastgele gün, gerçek tutuş süreleri karıştırılarak;
    evren (i) tüm günler, (ii) yalnız hisse>SMA200 günleri (rejim eşlenik), (iii) ortak dairesel kaydırma (tüm hisselerin sinyal
    vektörü aynı k gün kaydırılır: sinyallerin tarih kümelenmesi ve seri yapısı korunur; çıkış kuralı gerçek fiyatla yeniden uygulanır).
(b) Parametre komşuluğu: RSI eşiği {6,8,10,12,14}, trend SMA {150,200,250}, çıkış SMA {3,5,7}, en uzun tutuş {2,3,4,5}; C0 ve O1.
Çalıştır: python3 -I kod/denetim_tek_hisse_kaldiracli/d3_saglamlik.py"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import io, contextlib, math, itertools
import numpy as np, pandas as pd
import dk

EXTRA = {"NVDA": 2.84, "TSLA": 2.75, "AAPL": 1.28, "AMZN": 2.13, "META": 1.80, "MSFT": 1.10, "GOOGL": 1.55, "MSTR": 12.96, "COIN": 5.13}
RNG = np.random.default_rng(20261107)
NREP = 2000

def main():
    A = pd.read_csv(os.path.join(dk.OUT, "d2_islemler_C0.csv"), parse_dates=["sig_date", "entry_date", "exit_date"])
    AO = pd.read_csv(os.path.join(dk.OUT, "d2_islemler_O1.csv"), parse_dates=["sig_date", "entry_date", "exit_date"])
    data = {}
    for st in dk.STK:
        sd = dk.load_stock(st); px = dk.synth(sd, extra_bp=EXTRA[st])
        c = sd["c"].values; m200 = dk.sma(c, 200)
        data[st] = dict(sd=sd, Pc=px["c"].values, Po=px["o"].values, idx=sd.index, trend=np.nan_to_num(c > m200, nan=0).astype(bool),
                        sig=dk.signal(sd), exc=dk.exit_cond(sd))
    print("=" * 100)
    print(f"(a) Rastgele giriş permütasyonu, {NREP} tekrar, brüt getiri (C0 ve O1), işlem-ağırlıklı ortalama")
    out = []
    for mode, T in (("C0", A), ("O1", AO)):
        act = T.gross.mean() * 1e4
        for uni in ("tum_gunler", "rejim_sma200_ustu"):
            sims = np.zeros(NREP)
            pre = {}
            for st in dk.STK:
                d = data[st]; t = T[T.stock == st]
                H = t.days.values.astype(int)
                n = len(d["Pc"]); lo = 200
                elig = np.arange(lo, n - 5)
                if uni == "rejim_sma200_ustu": elig = elig[d["trend"][elig]]
                pre[st] = (elig, H)
            for r in range(NREP):
                tot = 0.0; cnt = 0
                for st in dk.STK:
                    d = data[st]; elig, H = pre[st]
                    ii = RNG.choice(elig, size=len(H), replace=False); hh = RNG.permutation(H)
                    if mode == "C0":
                        g = d["Pc"][ii + hh] / d["Pc"][ii] - 1
                    else:  # O1: t+1 açılış -> (t+1)+(days-1) kapanış
                        g = d["Pc"][ii + hh] / d["Po"][ii + 1] - 1
                    tot += g.sum(); cnt += len(g)
                sims[r] = tot / cnt * 1e4
            p = (np.sum(sims >= act) + 1) / (NREP + 1)
            print(f"  [{mode}] {uni:20s}: gerçek brüt {act:6.1f} bp | rastgele ort {sims.mean():6.1f} bp, %95 {np.percentile(sims, 95):6.1f} | kenar {act - sims.mean():6.1f} bp | p = {p:.4f}")
            out.append(dict(test=f"perm_{uni}", mode=mode, gercek_bp=act, rastgele_ort=sims.mean(), p95=np.percentile(sims, 95), kenar=act - sims.mean(), p=p))
    # (iii) ortak dairesel kaydırma: sinyal vektörleri birlikte kaydırılır, kural (SMA5 çıkış) gerçek fiyatla uygulanır
    for mode in ("C0", "O1"):
        act_tr = []
        for st in dk.STK:
            d = data[st]; act_tr += [g for (_, _, _, g) in dk.sim(d["sig"], d["exc"], d["Pc"], d["Po"], mode, 3)]
        act = np.mean(act_tr) * 1e4
        n = len(data["AAPL"]["Pc"])
        shifts = RNG.integers(60, n - 260, size=1000)
        sims = []
        for k in shifts:
            tr = []
            for st in dk.STK:
                d = data[st]
                s = np.roll(d["sig"], int(k)); s[:205] = False
                tr += [g for (_, _, _, g) in dk.sim(s, d["exc"], d["Pc"], d["Po"], mode, 3)]
            sims.append(np.mean(tr) * 1e4)
        sims = np.array(sims); p = (np.sum(sims >= act) + 1) / (len(sims) + 1)
        print(f"  [{mode}] ortak dairesel kaydırma (1.000): gerçek {act:6.1f} | kaydırılmış ort {sims.mean():6.1f}, %95 {np.percentile(sims, 95):6.1f} | p = {p:.4f}")
        out.append(dict(test="perm_ortak_kaydirma", mode=mode, gercek_bp=act, rastgele_ort=sims.mean(), p95=np.percentile(sims, 95), kenar=act - sims.mean(), p=p))
    pd.DataFrame(out).to_csv(os.path.join(dk.OUT, "d3_permutasyon.csv"), index=False)

    print("\n(b) Parametre komşuluğu (C0 ve O1; tarih kümelemeli net bp ve t; 2.500$):")
    rows = []
    for mode in ("C0", "O1"):
        for thr, tr_n, ex_n, hm in itertools.product((6, 8, 10, 12, 14), (150, 200, 250), (3, 5, 7), (2, 3, 4, 5)):
            B = dk.run(dk.STK, mode, thr=thr, trend=tr_n, exit_n=ex_n, hmax=hm, extra=EXTRA)
            s = dk.summary(B)
            rows.append(dict(mode=mode, rsi_esik=thr, trend_sma=tr_n, cikis_sma=ex_n, hmax=hm, n=s["n"], net_bp=s["net_bp"], t=s["t"],
                             is_bp=s["is_bp"], is_t=s["is_t"], oos_bp=s["oos_bp"], oos_t=s["oos_t"], yil_poz=s["yil_poz_tarih"]))
    G = pd.DataFrame(rows); G.to_csv(os.path.join(dk.OUT, "d3_komsuluk.csv"), index=False)
    for mode in ("C0", "O1"):
        g = G[G["mode"] == mode]
        print(f"  [{mode}] {len(g)} varyant: net>0 {int((g.net_bp > 0).sum())}, t>=2 {int((g.t >= 2).sum())}, IS>0 ve OOS>0 {int(((g.is_bp > 0) & (g.oos_bp > 0)).sum())}, "
              f"medyan net {g.net_bp.median():.1f} bp, medyan t {g.t.median():.2f}; ana kural sırası (t'ye göre): "
              f"{int((g.t > g[(g.rsi_esik == 10) & (g.trend_sma == 200) & (g.cikis_sma == 5) & (g.hmax == 3)].t.iloc[0]).sum()) + 1}/{len(g)}")
        print("    RSI eşiği dilimi (trend 200, çıkış SMA5, hmax 3):")
        print(g[(g.trend_sma == 200) & (g.cikis_sma == 5) & (g.hmax == 3)][["rsi_esik", "n", "net_bp", "t", "is_bp", "oos_bp"]].round(2).to_string(index=False))
        print("    hmax dilimi (RSI 10, trend 200, SMA5):")
        print(g[(g.rsi_esik == 10) & (g.trend_sma == 200) & (g.cikis_sma == 5)][["hmax", "n", "net_bp", "t", "is_bp", "oos_bp"]].round(2).to_string(index=False))
        print("    çıkış SMA dilimi (RSI 10, trend 200, hmax 3):")
        print(g[(g.rsi_esik == 10) & (g.trend_sma == 200) & (g.hmax == 3)][["cikis_sma", "n", "net_bp", "t", "is_bp", "oos_bp"]].round(2).to_string(index=False))
        print("    trend SMA dilimi (RSI 10, SMA5, hmax 3):")
        print(g[(g.rsi_esik == 10) & (g.cikis_sma == 5) & (g.hmax == 3)][["trend_sma", "n", "net_bp", "t", "is_bp", "oos_bp"]].round(2).to_string(index=False))
        piv = g.groupby("rsi_esik")[["net_bp", "t"]].median()
        print("    RSI eşiğine göre tüm varyantların medyanı:", piv.round(2).to_dict())

if __name__ == "__main__":
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        main()
    txt = buf.getvalue(); print(txt)
    open(os.path.join(dk.OUT, "d3_cikti.txt"), "w").write(txt)
