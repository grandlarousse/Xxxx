"""Adım 5: rapor tabloları (markdown) -> out/tablolar.md. Girdi: out/ipo_olay.csv, out/seri_ici_gunler.csv, px/.
ARDYZ (06.02.2020) hariç: o tarihte BIST günlük marjı ±%20 idi (sonra ±%10); seri tanımı karşılaştırılamaz."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from common import OUT, PX
from a04_olay import summ, load_xu, load_stock, SON, MALIYET

L = []


def P(s=""):
    L.append(s)


def md(df, idx=True):
    P(df.to_markdown(index=idx, floatfmt=".1f") if hasattr(df, "to_markdown") else df.to_string())
    P()


def pct_tab(rows, keys):
    out = []
    for nm, x, cl in rows:
        s = summ(x, cl)
        if s.get("n", 0) == 0:
            continue
        out.append(dict(seri=nm, n=s["n"], ort=100 * s["ort"], med=100 * s["med"], t=s["t"], t_kume=s["t_kume"],
                        isabet=100 * s["isabet"], p5=100 * s["p5"], p95=100 * s["p95"]))
    d = pd.DataFrame(out).set_index("seri")
    return d.round({"ort": 1, "med": 1, "t": 2, "t_kume": 2, "isabet": 0, "p5": 1, "p95": 1})


def wins(x, q=0.025):
    x = pd.Series(x, dtype=float)
    lo, hi = x.quantile(q), x.quantile(1 - q)
    return x.clip(lo, hi)


def cal_port(ev, entry_col, h, cost=MALIYET):
    """Takvim-zamanı portföyü: her arz için E kapanışında al, h gün tut; aktif pozisyonlara eşit ağırlık.
    Pozisyon yokken getiri 0 (nakit; TL faizi eklenmedi). Maliyet giriş gününe yazılır."""
    xu = load_xu()
    rets = {}
    for r in ev.itertuples():
        if pd.isna(getattr(r, entry_col)):
            continue
        df = load_stock(r.kod, pd.Timestamp(r.d1) - pd.Timedelta(days=1))
        if df is None:
            continue
        a = df["adj"]
        i0 = a.index.searchsorted(pd.Timestamp(getattr(r, entry_col)))
        i1 = min(i0 + h, len(a) - 1)
        if i1 <= i0:
            continue
        rr = a.pct_change().iloc[i0 + 1:i1 + 1].copy()
        rr.iloc[0] -= cost
        rets[r.kod] = rr
    M = pd.DataFrame(rets)
    port = M.mean(axis=1, skipna=True)
    nact = M.notna().sum(axis=1)
    idx = xu.index[(xu.index >= port.index.min()) & (xu.index <= SON)]
    port = port.reindex(idx)
    act = port.notna()
    mr = xu.pct_change().reindex(idx)
    p0 = port.fillna(0.0)
    ex = (port - mr)[act]
    ann = lambda s: (1 + s).prod() ** (252 / max(len(s), 1)) - 1
    eq = (1 + p0).cumprod()
    dd = (eq / eq.cummax() - 1).min()
    return dict(gun=len(idx), aktif_gun=int(act.sum()), ort_poz=float(nact[nact > 0].mean()),
                yillik_port_aktif=ann(port[act]), yillik_xu_aktif=ann(mr[act]),
                fark_gunluk_bp=1e4 * ex.mean(), t_fark=ex.mean() / (ex.std(ddof=1) / math.sqrt(len(ex))),
                sharpe_aktif=port[act].mean() / port[act].std() * math.sqrt(252), maxdd=dd), port, mr


def main():
    ev = pd.read_csv(os.path.join(OUT, "ipo_olay.csv"), parse_dates=["d1", "E", "L", "ilk_islem_hz"])
    ev = ev[ev.kod != "ARDYZ"].copy()
    ev["ay"] = ev["E"].dt.to_period("M").astype(str)
    ev["ay1"] = ev["d1"].dt.to_period("M").astype(str)
    ev["donem"] = np.where(ev.yil >= 2024, "2024-26", "2020-23")
    ev["seri_k"] = pd.cut(ev.seri, [-1, 0, 2, 5, 10, 99], labels=["0", "1-2", "3-5", "6-10", "11+"])
    ev["buyuk_t"] = ev.groupby("yil")["buyukluk_tl"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=["küçük", "orta", "büyük"]))
    ev["kisi_t"] = ev.groupby("yil")["bireysel_kisi"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=["az", "orta", "çok"]))
    sd = pd.read_csv(os.path.join(OUT, "seri_ici_gunler.csv"), parse_dates=["tarih"])
    sd = sd[sd.kod != "ARDYZ"]

    # ---------- T1 örneklem
    P("## T1. Örneklem ve ilk gün / tavan serisi (yıl = ilk işlem yılı)")
    g = ev.groupby("yil")
    t1 = pd.DataFrame({
        "n": g.size(), "eşit%": 100 * g.apply(lambda d: (d.dagitim == "Eşit").mean()),
        "bireysel_kişi_med(bin)": g.bireysel_kisi.median() / 1e3, "kişi_başı_TL_med": g.tl_kisi.median(),
        "büyüklük_med(mn TL)": g.buyukluk_tl.median() / 1e6, "gün1_ort%": 100 * g.gun1.mean(),
        "gün1_tavan%": 100 * g.gun1_tavan.mean(), "gün1_kilit%": 100 * g.gun1_kilit.mean(),
        "seri_ort": g.seri.mean(), "seri_med": g.seri.median(), "seri>=5 %": 100 * g.apply(lambda d: (d.seri >= 5).mean()),
        "seri>=10 %": 100 * g.apply(lambda d: (d.seri >= 10).mean()),
        "arz→tepe_med%": 100 * g.arz_tepe.median(), "arz→tepe_ort%": 100 * g.arz_tepe.mean()})
    tot = pd.DataFrame({"n": [len(ev)], "eşit%": [100 * (ev.dagitim == "Eşit").mean()], "bireysel_kişi_med(bin)": [ev.bireysel_kisi.median() / 1e3],
                        "kişi_başı_TL_med": [ev.tl_kisi.median()], "büyüklük_med(mn TL)": [ev.buyukluk_tl.median() / 1e6],
                        "gün1_ort%": [100 * ev.gun1.mean()], "gün1_tavan%": [100 * ev.gun1_tavan.mean()], "gün1_kilit%": [100 * ev.gun1_kilit.mean()],
                        "seri_ort": [ev.seri.mean()], "seri_med": [ev.seri.median()], "seri>=5 %": [100 * (ev.seri >= 5).mean()],
                        "seri>=10 %": [100 * (ev.seri >= 10).mean()], "arz→tepe_med%": [100 * ev.arz_tepe.median()], "arz→tepe_ort%": [100 * ev.arz_tepe.mean()]}, index=["Tümü"])
    md(pd.concat([t1, tot]).round(1))
    P("Seri uzunluğu dağılımı (adet): " + ", ".join(f"{k}:{v}" for k, v in ev.seri.value_counts().sort_index().items()))
    P()
    P("Gün1 getirisi dağılımı (adet): " + ", ".join(f"{k}:{v}" for k, v in pd.cut(ev.gun1, [-0.11, -0.05, -0.001, 0.001, 0.05, 0.0949, 0.11]).value_counts().sort_index().items()))
    P()

    # ---------- T2 katılımcı getirisi (arz fiyatından)
    P("## T2. Katılımcı getirisi (arz fiyatından, bedelsiz düzeltmeli), arz başına")
    rows = [("gün1 kapanış", ev.kat_gun1, ev.ay1), ("seri sonu E günü AOF", ev.kat_E_aof, ev.ay1), ("E kapanış", ev.kat_E_kap, ev.ay1),
            ("E+21 kapanış", ev.kat_E21, ev.ay1), ("E+63 kapanış", ev.kat_E63, ev.ay1), ("E+126 kapanış", ev.kat_E126, ev.ay1), ("E+250 kapanış", ev.kat_E250, ev.ay1)]
    md(pct_tab(rows, None))
    P("Yıllara göre medyan katılımcı getirisi (%):")
    md((100 * ev.groupby("yil")[["kat_gun1", "kat_E_aof", "kat_E21", "kat_E63", "kat_E126", "kat_E250"]].median()).round(1))
    P("Arz fiyatının altına düşme oranı (%), ufuk bazında:")
    md(pd.DataFrame({h: [100 * (ev[c] < 0).mean(), ev[c].notna().sum()] for h, c in [("E+21", "kat_E21"), ("E+63", "kat_E63"), ("E+126", "kat_E126"), ("E+250", "kat_E250")]}, index=["arz altı %", "n"]).round(1))

    # ---------- T3 hesap başına TL
    P("## T3. Tek hesapla her arza katılan bireysel yatırımcı: yıllık TL kâr (nominal)")
    e = ev.copy()
    e["tl_al"] = np.minimum(e.lot_kisi * e.fiyat, 20000.0)  # talep tavanı 20 bin TL/arz (yalnız düşük talepli arzlarda bağlar)
    for nm, c in [("gün1", "kat_gun1"), ("E_AOF", "kat_E_aof"), ("E+21", "kat_E21"), ("E+63", "kat_E63")]:
        e[f"kar_{nm}"] = e.tl_al * (e[c] - 0.002)  # satışta ~%0,2 komisyon+BSMV
    rows = []
    for y, d in e.groupby("yil"):
        de = d[d.dagitim == "Eşit"]
        rows.append(dict(yil=y, arz_eşit=len(de), arz_tümü=len(d), alınan_TL_top=de.tl_al.sum(), alınan_TL_med=de.tl_al.median(),
                         kar_gün1=de.kar_gün1.sum(), kar_E_AOF=de["kar_E_AOF"].sum(), kar_E21=de["kar_E+21"].sum(min_count=1), kar_E63=de["kar_E+63"].sum(min_count=1),
                         arz_başı_kar_E_AOF_med=de["kar_E_AOF"].median(), oransal_ort_kar_E_AOF=d[d.dagitim != "Eşit"]["kar_E_AOF"].mean()))
    md(pd.DataFrame(rows).set_index("yil").round(0))
    P("Varsayım: her eşit dağıtımlı arza tek hesapla katılım, kişi başı alınan = bireysel lot/bireysel kişi (en çok 20 bin TL), satışta %0,2 maliyet.")
    P("Not: Oransal dağıtımda lot/kişi ortalamadır (talep tutarına bağlı). E+21/E+63 son arzlarda eksik (pencere dolmadı).")
    P()

    # ---------- T4 seri sonrası
    P("## T4. Seri sonrası (E = ilk tavan olmayan gün). Giriş E kapanışı. BH = XU100'e göre al-tut fazla getiri; CAR = günlük AR toplamı; CARb = beta-düzeltilmiş")
    for h in (5, 21, 63, 126):
        rows = [(f"R{h} ham", ev[f"Ekap_R{h}"], ev.ay), (f"BH{h}", ev[f"Ekap_BH{h}"], ev.ay), (f"CAR{h}", ev[f"Ekap_CAR{h}"], ev.ay),
                (f"CARb{h}", ev[f"Ekap_CARb{h}"], ev.ay), (f"BH{h} winsor%2.5", wins(ev[f"Ekap_BH{h}"]), ev.ay),
                (f"BH{h} net(-25bp)", ev[f"Ekap_BH{h}"] - MALIYET, ev.ay)]
        md(pct_tab(rows, None))
    P("### T4b. Alternatif girişler (BH, %)")
    rows = []
    for nm, lab in [("Ekap", "E kapanış"), ("Eaof", "E AOF"), ("E1kap", "E+1 kapanış")]:
        for h in (5, 21, 63):
            rows.append((f"{lab} BH{h}", ev[f"{nm}_BH{h}"], ev.ay))
    md(pct_tab(rows, None))
    ok1 = ev.E1_kilit_tavan != True
    P(f"E+1 kilitli tavan (alış dolmaz) olan arz: {int((ev.E1_kilit_tavan == True).sum())}; hariç tutulunca E+1 BH21: "
      f"ort {100*ev.loc[ok1,'E1kap_BH21'].mean():.1f}%, med {100*ev.loc[ok1,'E1kap_BH21'].median():.1f}%")
    P(f"E günü taban kapanış: {int(ev.E_taban.sum())} arz; kilitli taban: {int((ev.E_taban_kilit == True).sum())} (açığa satış/satış dolmaz).")
    P()

    P("### T4c. Kırılımlar: E kapanış girişli BH21 ve BH63 (%)")
    for col, lab in [("yil", "yıl"), ("donem", "dönem"), ("seri_k", "seri uzunluğu"), ("buyuk_t", "büyüklük (yıl içi tercil)"),
                     ("kisi_t", "başvuran kişi (yıl içi tercil)"), ("dagitim", "dağıtım"), ("istikrar", "fiyat istikrarı")]:
        rows = []
        for k, d in ev.groupby(col, observed=True):
            for h in (21, 63):
                s = summ(d[f"Ekap_BH{h}"], d.ay)
                if s.get("n", 0) == 0:
                    continue
                rows.append({lab: k, "h": h, "n": s["n"], "ort": 100 * s["ort"], "med": 100 * s["med"], "t_kume": s["t_kume"], "isabet": 100 * s["isabet"]})
        md(pd.DataFrame(rows).set_index([lab, "h"]).round({"ort": 1, "med": 1, "t_kume": 2, "isabet": 0}))

    # ---------- T5 takvim zamanı portföy
    P("## T5. Takvim-zamanı portföyü (E kapanışında al, h gün tut, eşit ağırlık, 25 bp maliyet; boşta nakit=0)")
    rows = []
    ev["E1"] = ev.groupby("kod")["E"].transform(lambda x: x)  # E+1 girişi için yardımcı
    for h in (5, 21, 63):
        for sub, d in [("tümü", ev), ("2024-26", ev[ev.yil >= 2024])]:
            s, port, mr = cal_port(d, "E", h)
            s.update(h=h, örnek=sub, giris="E kap"); rows.append(s)
    for h in (63, 126):
        d = ev.copy()
        nxt = {}
        for r in d.itertuples():
            df = load_stock(r.kod, pd.Timestamp(r.d1) - pd.Timedelta(days=1))
            i0 = df.index.searchsorted(pd.Timestamp(r.E))
            nxt[r.kod] = df.index[i0 + 1] if i0 + 1 < len(df) else pd.NaT
        d["E1"] = d.kod.map(nxt)
        s, port, mr = cal_port(d, "E1", h)
        s.update(h=h, örnek="tümü", giris="E+1 kap"); rows.append(s)
    t5 = pd.DataFrame(rows).set_index(["giris", "h", "örnek"])
    for c in ["yillik_port_aktif", "yillik_xu_aktif", "maxdd"]:
        t5[c] = (100 * t5[c]).round(1)
    md(t5.round(2))

    # ---------- T6 ikincil piyasa: gün1 kapanışından alış
    P("## T6. Gün1 kapanışından alış (ikincil piyasa). Gün1 kilitli tavansa alış dolmaz")
    lk = ev.gun1_kilit == True
    rows = []
    for h in (5, 21, 63):
        rows += [(f"tümü BH{h}", ev[f"G1_BH{h}"], ev.ay1), (f"dolabilir (kilitsiz) BH{h}", ev.loc[~lk, f"G1_BH{h}"], ev.loc[~lk, "ay1"]),
                 (f"kilitli (dolmaz) BH{h}", ev.loc[lk, f"G1_BH{h}"], ev.loc[lk, "ay1"])]
    md(pct_tab(rows, None))

    # ---------- T7 seri içi
    P("## T7. Seri içindeki tavan kapanışlar: kilitli mi, ertesi gün ne oldu?")
    sd["kilit"] = sd.kilit.astype(bool)
    rows = []
    for k, d in sd.groupby("kilit"):
        s = summ(d.ertesi, d.tarih.dt.to_period("M").astype(str))
        rows.append(dict(kilitli=k, gün=len(d), ertesi_ort=100 * s["ort"], ertesi_med=100 * s["med"], t_kume=s["t_kume"], ertesi_tavan=100 * d.ertesi_tavan.mean()))
    md(pd.DataFrame(rows).set_index("kilitli").round(2))
    rows = []
    for k, d in sd.groupby(pd.cut(sd.gun, [0, 1, 3, 6, 10, 99], labels=["1", "2-3", "4-6", "7-10", "11+"]), observed=True):
        rows.append({"seri_günü": k, "gün": len(d), "kilitli%": 100 * d.kilit.mean(), "ertesi_tavan%": 100 * d.ertesi_tavan.mean(),
                     "kilitsiz_ertesi_ort%": 100 * d[~d.kilit].ertesi.mean(), "kilitsiz_n": int((~d.kilit).sum())})
    md(pd.DataFrame(rows).set_index("seri_günü").round(1))

    # ---------- T7b uygulanabilir sürüm: seri içinde kuyruk gün içinde bozulduğunda (min<max) AOF'tan al
    P("## T7b. Uygulanabilir sürüm (ileriye bakış yok): önceki kapanış tavan iken gün içinde kuyruk bozulursa (min<max) o günün AOF'undan al")
    P("Bu küme hem tekrar tavan kapatan günleri hem seriyi bitiren E günlerini içerir; kapanışın tavan olup olmayacağı alış anında bilinmez.")
    rows = []
    for r in ev.itertuples():
        df = load_stock(r.kod, pd.Timestamp(r.d1) - pd.Timedelta(days=1))
        if df is None or df["HG_MAX"].isna().all():
            continue
        a = df["adj"]; raw = df["HG_KAPANIS"]
        for i in range(1, int(r.seri) + 1):
            if i >= len(df) or pd.isna(df["HG_MAX"].iloc[i]) or pd.isna(df["HG_AOF"].iloc[i]):
                continue
            if abs(df["HG_MAX"].iloc[i] - df["HG_MIN"].iloc[i]) < 1e-6:
                continue
            p0 = df["HG_AOF"].iloc[i] * a.iloc[i] / raw.iloc[i]
            row = dict(kod=r.kod, gun=i + 1, tarih=df.index[i], seri_bitti=(i == int(r.seri)))
            for h, nm in ((0, "kap0"), (1, "kap1"), (5, "kap5"), (21, "kap21")):
                if i + h < len(df):
                    row[nm] = a.iloc[i + h] / p0 - 1
            rows.append(row)
    qb = pd.DataFrame(rows)
    qb["ay"] = qb.tarih.dt.to_period("M").astype(str)
    md(pct_tab([("AOF→aynı gün kapanış", qb.kap0, qb.ay), ("AOF→ertesi kapanış", qb.kap1, qb.ay), ("AOF→+5 gün", qb.kap5, qb.ay),
                ("AOF→+21 gün", qb.kap21, qb.ay)], None))
    P(f"Olay günü: {len(qb)}; bunların %{100*qb.seri_bitti.mean():.0f}'i seriyi bitiren gün (E).")
    P()

    # ---------- T8 lock-up
    P("## T8. Satmama taahhüdü (lock-up) bitişi: CAR (XU100'e göre, %). L = ilk işlem + süre (yoksa 365 gün varsayımı)")
    lu = ev[ev.LU_m10m1.notna()].copy()
    lu["ayL"] = lu.L.dt.to_period("M").astype(str)
    rows = []
    for nm in ["m10m1", "0p5", "0p20", "m20p20"]:
        rows += [(f"CAR[{nm}]", lu[f"LU_{nm}"], lu.ayL), (f"CARb[{nm}]", lu[f"LUb_{nm}"], lu.ayL)]
    md(pct_tab(rows, None))
    rows = []
    for k, d in [("süre sayfada yazılı", lu[~lu.lockup_varsayim]), ("365 gün varsayım", lu[lu.lockup_varsayim]),
                 ("L öncesi fiyat > arz×2", lu[lu.LU_fiyat_vs_arz > 1]), ("L öncesi fiyat ≤ arz×2", lu[lu.LU_fiyat_vs_arz <= 1]),
                 ("2024-26", lu[lu.L.dt.year >= 2024])]:
        for nm in ["0p5", "0p20"]:
            s = summ(d[f"LU_{nm}"], d.ayL)
            if s.get("n", 0):
                rows.append({"alt örnek": k, "pencere": nm, "n": s["n"], "ort": 100 * s["ort"], "med": 100 * s["med"], "t_kume": s["t_kume"], "isabet": 100 * s["isabet"]})
    md(pd.DataFrame(rows).set_index(["alt örnek", "pencere"]).round({"ort": 1, "med": 1, "t_kume": 2, "isabet": 0}))

    # ---------- T9 kısa/kaçın
    P("## T9. 'Seri bitince açığa sat / uzak dur' = T4'ün tersi. Kısa pozisyon getirisi (−BH, %, maliyet hariç)")
    rows = [(f"−BH{h}", -ev[f"Ekap_BH{h}"], ev.ay) for h in (5, 21, 63, 126)]
    rows += [(f"−BH{h} (seri≥5)", -ev.loc[ev.seri >= 5, f"Ekap_BH{h}"], ev.loc[ev.seri >= 5, "ay"]) for h in (5, 21, 63)]
    okE = ev.E_taban_kilit != True
    rows = [(f"−BH5 kilitli taban hariç", -ev.loc[okE, "Ekap_BH5"], ev.loc[okE, "ay"]),
            (f"−BH5 net(-25bp) kilitli taban hariç", -ev.loc[okE, "Ekap_BH5"] - MALIYET, ev.loc[okE, "ay"])]
    rows += [(f"−BH5 {y}", -d["Ekap_BH5"], d["ay"]) for y, d in ev[okE].groupby("yil")]
    rows += [("−BH5 2024-26", -ev.loc[okE & (ev.yil >= 2024), "Ekap_BH5"], ev.loc[okE & (ev.yil >= 2024), "ay"])]
    md(pct_tab(rows, None))

    # ---------- uç değerler
    P("## T10. Uç değerler: E kapanışından 63 gün BH en iyi/en kötü 8")
    cols = ["kod", "yil", "seri", "kat_E_aof", "Ekap_BH63", "Ekap_R63"]
    b = ev.sort_values("Ekap_BH63", ascending=False)[cols]
    md(pd.concat([b.head(8), b.dropna().tail(8)]).assign(**{c: lambda d, c=c: (100 * d[c]).round(1) for c in ["kat_E_aof", "Ekap_BH63", "Ekap_R63"]}).set_index("kod"))
    P("Pozitif BH63 payının ortalamaya katkısı: en iyi 10 arz çıkarılınca BH63 ort = "
      f"{100*ev.Ekap_BH63.drop(ev.Ekap_BH63.nlargest(10).index).mean():.1f}% (tümü {100*ev.Ekap_BH63.mean():.1f}%)")
    open(os.path.join(OUT, "tablolar.md"), "w", encoding="utf-8").write("\n".join(L))
    print("\n".join(L))


if __name__ == "__main__":
    main()
