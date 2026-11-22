"""F6 Bilanço olayları: (a) bilanço sonrası sürüklenme, (b) lider bilançosundan emsallere yayılım,
(c) bilanço öncesi prim, (d) önümüzdeki 4 haftanın bilanço takvimi.  Yöntem: ../YONTEM.md (bölüm 3, 5, 6, 7, 8, 10).

Kullanım:  python3 kod/f6_bilanco.py            -> hepsi (indirme önbellekten; yoksa indirir)
           python3 kod/f6_bilanco.py a|b|c|d|son -> tek aşama (ara sonuçlar ek/backtest/f6_bilanco/ara_*.csv)

Tepki günü çıkarımı: takvim tarihi d için {d, d+1} içinde |z(anormal getiri)| x hacim oranı büyük olan gün.
'zaman' alanı dolu kayıtlarda (2026 başı) gerçek etiket kullanılır ve çıkarımın isabeti bunlarla ölçülür.
Giriş her zaman etiketlenen tepki gününün kapanışıdır; sinyal yalnız o güne kadarki veriyi kullanır.
İstatistik (t, maliyet, dönem, sınıf) ortak.py'den gelir: havuz_donemli / havuz_testi / siniflandir.
Kütüphanede havuz için olmayan üç ek ölçüt (en iyi 10 gün hariç, yıl tablosu, dairesel plasebo) burada, kütüphanedeki
tanımın gün bazlı portföy serisine uyarlanmış hâliyle hesaplanır (t yine ortak.hac_t).
"""
import json
import os
import subprocess
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak as o  # noqa: E402

CIKTI = os.path.join(o.KOK, "ek", "backtest", "f6_bilanco")
os.makedirs(CIKTI, exist_ok=True)
TAKVIM = os.path.join(o.VERI, "bilanco_takvimi.csv")
GELECEK = os.path.join(o.VERI, "bilanco_gelecek.csv")
EDGAR = os.path.join(o.VERI, "edgar_8k_202.csv")
Z_ESIK, HACIM_ESIK, LIKIT_MN = 2.0, 1.5, 100.0
UFUK = (1, 2, 3)
T0 = time.time()


def log(*a):
    print(f"[{time.time() - T0:6.1f}s]", *a, flush=True)


# ------------------------------------------------------------------------------------------------------------
# İndirme (önbellekli): gelecek takvim (Nasdaq) ve isteğe bağlı EDGAR 8-K 2.02 kabul saatleri
# ------------------------------------------------------------------------------------------------------------


def curl_json(url):
    cmd = ["curl", "-s", "--compressed", "--max-time", "25", "-A", "Mozilla/5.0", "-H", "Accept: application/json", url]
    try:
        return json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout)
    except Exception:  # noqa: BLE001
        return None


def gelecek_indir():
    """24 Kas - 18 Ara 2026 + 20 ve 23 Kasım (son sinyal için): en çok 20 istek."""
    if os.path.exists(GELECEK):
        return pd.read_csv(GELECEK)
    gunler = [g for g in pd.bdate_range("2026-11-20", "2026-12-18") if str(g.date()) != "2026-11-26"]
    sat, hata = [], 0
    for g in gunler[:20]:
        j = curl_json(f"https://api.nasdaq.com/api/calendar/earnings?date={g.date()}")
        rows = ((j or {}).get("data") or {}).get("rows") or []
        if j is None:
            hata += 1
            if hata >= 5:
                break
        for r in rows:
            sat.append({"tarih": str(g.date()), "sembol": r.get("symbol"), "zaman": r.get("time"), "ad": r.get("name"),
                        "eps_beklenti": r.get("epsForecast"), "tahmin_sayisi": r.get("noOfEsts"), "ceyrek": r.get("fiscalQuarterEnding")})
        time.sleep(0.4)
    d = pd.DataFrame(sat)
    if len(d):
        d.to_csv(GELECEK, index=False)
    log("gelecek takvim:", len(d), "satır,", hata, "hatalı istek")
    return d


EDGAR_CIK = {"AAPL": "0000320193", "NVDA": "0001045810", "KO": "0000021344", "JNJ": "0000200406", "XOM": "0000034088"}


def edgar_indir():
    """İsteğe bağlı ikinci kaynak: 5 şirketin 8-K (madde 2.02) kabul zamanı. En çok 5 istek; olmazsa boş döner."""
    if os.path.exists(EDGAR):
        return pd.read_csv(EDGAR)
    sat = []
    for s, cik in EDGAR_CIK.items():
        j = curl_json(f"https://data.sec.gov/submissions/CIK{cik}.json")
        if not j or s not in (j.get("tickers") or []):
            continue
        f = j["filings"]["recent"]
        for form, items, acc in zip(f["form"], f["items"], f["acceptanceDateTime"]):
            if form == "8-K" and "2.02" in str(items):
                sat.append({"sembol": s, "kabul": acc})
        time.sleep(0.3)
    d = pd.DataFrame(sat)
    if len(d):
        d.to_csv(EDGAR, index=False)
    log("EDGAR:", len(d), "kayıt")
    return d


# ------------------------------------------------------------------------------------------------------------
# Hazırlık: getiri, anormal getiri z'si, hacim oranı, olay tablosu ve tepki günü çıkarımı
# ------------------------------------------------------------------------------------------------------------


class C:
    pass


def para(s):
    s = s.astype(str).str.replace(r"[$,]", "", regex=True).str.replace(r"^\((.*)\)$", r"-\1", regex=True)
    return pd.to_numeric(s, errors="coerce")


def hazirla():
    c = C()
    ev = pd.read_csv(TAKVIM)
    ev = ev[ev.evrende == 1].drop_duplicates(["tarih", "sembol"]).copy()
    c.syms = syms = sorted(set(ev.sembol) & set(o.panel("adjclose").columns))
    c.ix = {s: i for i, s in enumerate(syms)}
    R = o.basit_getiri(syms + ["SPY"])
    spy, R = R["SPY"], R[syms]
    B = pd.DataFrame({s: o.kayan_beta(R[s], spy) for s in syms})
    c.AR = AR = R - B.mul(spy, axis=0)                       # hisse - beta x SPY (beta 250 gün, 1 gün gecikmeli)
    c.Z = Z = o.zskor(AR)                                    # önceki 60 günün std'si
    V, Cl = o.panel("volume", syms), o.panel("close", syms)
    c.VR = VR = V / V.rolling(60, min_periods=20).median().shift(1)
    c.DV = DV = (Cl * V).rolling(60, min_periods=20).median().shift(1) / 1e6   # mn $, maliyet_serisi ile aynı tanım
    c.tk = tk = R.index
    c.T, c.N = T, N = len(tk), len(syms)
    log("paneller hazır", R.shape)

    ev["t"] = pd.to_datetime(ev.tarih)
    ev = ev[ev.sembol.isin(syms)].copy()
    i0 = tk.searchsorted(ev.t.values, "left")                # takvim tarihine eşit ya da sonraki ilk işlem günü
    ev, i0 = ev[i0 < T].copy(), i0[i0 < T]
    ev["i0"], ev["ci"] = i0, pd.Index(syms).get_indexer(ev.sembol)
    ci = ev.ci.values

    def al(M, i):
        out = np.full(len(i), np.nan)
        ok = (i >= 0) & (i < T)
        out[ok] = M[i[ok], ci[ok]]
        return out

    zv, vv = Z.values, VR.values
    for k, ad in ((-1, "m1"), (0, "0"), (1, "1"), (2, "2")):
        ev["z" + ad], ev["v" + ad] = al(zv, i0 + k), al(vv, i0 + k)
    s0, s1 = (ev.z0.abs() * ev.v0).values, (ev.z1.abs() * ev.v1).values
    cik = np.where(s1 > s0, 1.0, 0.0)
    cik[np.isnan(s0) & np.isnan(s1)] = np.nan
    cik[np.isnan(s0) & ~np.isnan(s1)] = 1.0
    son = np.isnan(s1) & ~np.isnan(s0)                       # d+1 henüz yok (verinin son günü): yalnız nedensel kural
    cik[son] = np.where((ev.z0.abs() >= Z_ESIK) & (ev.v0 >= HACIM_ESIK), 0.0, np.nan)[son]
    ev["cikarim"] = cik
    ev["gercek"] = ev.zaman.map({"time-pre-market": 0.0, "time-after-hours": 1.0})
    ev["etiket"] = ev.gercek.where(ev.gercek.notna(), ev.cikarim)
    ev["skor"] = np.fmax(s0, s1)
    # aynı hissede 20 işlem gününden yakın çift kayıt: skoru büyük olanı tut
    ev = ev.sort_values(["sembol", "i0"])
    ev["kume"] = ((ev.sembol != ev.sembol.shift()) | (ev.i0.diff() > 20)).cumsum()
    n_once = len(ev)
    ev = ev.sort_values("skor", ascending=False, na_position="last").drop_duplicates("kume").sort_values(["sembol", "i0"])
    c.cift_kayit = n_once - len(ev)

    # çıkarımın isabeti ('zaman' dolu kayıtlar)
    g = ev[ev.gercek.notna() & ev.z0.notna() & ev.z1.notna() & ev.v0.notna() & ev.v1.notna()]
    c.isabet = {
        "n_etiketli": int(len(g)), "n_acilis_oncesi": int((g.gercek == 0).sum()), "n_kapanis_sonrasi": int((g.gercek == 1).sum()),
        "isabet_z_x_hacim": round(float(((g.z1.abs() * g.v1 > g.z0.abs() * g.v0) == (g.gercek == 1)).mean()), 3),
        "isabet_yalniz_z": round(float(((g.z1.abs() > g.z0.abs()) == (g.gercek == 1)).mean()), 3),
        "isabet_yalniz_hacim": round(float(((g.v1 > g.v0) == (g.gercek == 1)).mean()), 3),
        "isabet_acilis_oncesi": round(float((g[g.gercek == 0].cikarim == 0).mean()), 3),
        "isabet_kapanis_sonrasi": round(float((g[g.gercek == 1].cikarim == 1).mean()), 3),
    }
    gb = g[np.fmax(g.z0.abs(), g.z1.abs()) >= Z_ESIK]
    c.isabet["n_buyuk_tepki"] = int(len(gb))
    c.isabet["isabet_buyuk_tepki"] = round(float((gb.cikarim == gb.gercek).mean()), 3)
    sm, s2 = (ev.zm1.abs() * ev.vm1), (ev.z2.abs() * ev.v2)
    c.isabet["tarih_disi_pay"] = round(float((np.fmax(sm, s2) > ev.skor).mean()), 3)   # d-1 ya da d+2 daha büyük: tarih şüpheli
    c.isabet["etiket_d1_pay"] = round(float((ev.cikarim == 1).mean()), 3)

    eps, bek = para(ev.eps), para(ev.eps_beklenti)
    ss = np.sign(eps - bek)
    ev["surpriz"] = ev.surpriz_yuzde.clip(-200, 200)
    ev["s_isaret"] = ss.where(ss.notna() & (ss != 0), np.sign(ev.surpriz))
    ev["ir"] = ev.i0 + ev.etiket
    ol = ev[ev.ir.notna() & (ev.ir < T)].copy()
    ol["ir"] = ol.ir.astype(int)
    ci, ir = ol.ci.values, ol.ir.values
    ol["z"], ol["ar"], ol["vr"], ol["dv"] = zv[ir, ci], AR.values[ir, ci], vv[ir, ci], DV.values[ir, ci]
    ol["tepki_gunu"] = tk[ir].strftime("%Y-%m-%d")
    ol["yil"] = tk[ir].year
    ol["likit"] = ol.dv >= ol.groupby("yil").dv.transform("median")
    c.ev, c.ol = ev, ol
    ol[["tarih", "sembol", "zaman", "tepki_gunu", "etiket", "cikarim", "gercek", "z", "ar", "vr", "dv", "likit", "surpriz", "s_isaret",
        "z0", "v0", "z1", "v1"]].round(4).to_csv(os.path.join(CIKTI, "olaylar.csv"), index=False)

    # EDGAR ile ikinci isabet ölçümü (varsa)
    if os.path.exists(EDGAR):
        e = pd.read_csv(EDGAR)
        et = pd.to_datetime(e.kabul, utc=True).dt.tz_convert("America/New_York")
        e["gun"], e["saat"] = et.dt.tz_localize(None).dt.normalize(), et.dt.hour + et.dt.minute / 60
        e["ig"] = tk.searchsorted(e.gun.values, "left") + (e.saat >= 16).astype(int).values   # gerçek tepki günü indeksi
        e["i_gun"] = tk.searchsorted(e.gun.values, "left")
        m = e.merge(ol[["sembol", "i0", "ir", "cikarim", "gercek", "z"]], on="sembol")
        m = m[((m.i0 - m.i_gun).abs() <= 2) & m.gercek.isna()]
        m = m.sort_values("kabul").drop_duplicates(["sembol", "i0"])
        c.isabet.update({"edgar_n": int(len(m)), "edgar_isabet": round(float((m.ir == m.ig).mean()), 3),
                         "edgar_tarih_ayni": round(float((m.i0 == m.i_gun).mean()), 3),
                         "edgar_isabet_buyuk": round(float((m[m.z.abs() >= Z_ESIK].ir == m[m.z.abs() >= Z_ESIK].ig).mean()), 3),
                         "edgar_saat_ozet": e.groupby("sembol").saat.median().round(1).to_dict()})
    # gruplar
    hg = sorted({g_ for x in o.meta().gruplar.astype(str) for g_ in x.split(";") if g_.startswith("h_")})
    c.uye = {g_: [s for s in o.grup(g_) if s in c.ix] for g_ in hg}
    # ortak matrisler (ek ölçütler için; kütüphanedeki tanımlarla aynı)
    c.FH = {h: o.ileri_getiri(syms, h) for h in UFUK}
    c.CM = pd.DataFrame({s: o.maliyet_serisi(s) for s in syms}).reindex(tk).fillna(20.0) / 1e4
    vix = o.panel("close", ["^VIX"])["^VIX"].reindex(tk).ffill().shift(1)     # rejim ayrımı: önceki günün VIX kapanışı
    c.vix_y = vix > 20
    c.kriz = ((tk >= "2008-09-01") & (tk <= "2009-06-30")) | ((tk >= "2020-02-01") & (tk <= "2020-04-30"))
    c.yil, c.buyuk = [], []
    log("olaylar:", len(ev), "kayıt,", len(ol), "tepki günü etiketli;", json.dumps(c.isabet, ensure_ascii=False))
    return c


def mat(c, rows, cols, vals):
    M = np.zeros((c.T, c.N))
    rows, cols, vals = np.asarray(rows), np.asarray(cols), np.asarray(vals, dtype=float)
    ok = (rows >= 0) & (rows < c.T) & ~np.isnan(vals)
    M[rows[ok], cols[ok]] = vals[ok]
    return M


def df(c, M):
    return pd.DataFrame(M, index=c.tk, columns=c.syms)


# ------------------------------------------------------------------------------------------------------------
# Test koşucusu
# ------------------------------------------------------------------------------------------------------------


def gunluk(c, S, h, giris_F=None):
    """Gün bazlı eşit ağırlıklı portföy: (net, sürüklenme düzeltilmiş net). havuz_testi ile aynı tanım."""
    F = c.FH[h] if giris_F is None else giris_F
    akt = (S != 0) & F.notna()
    k = akt.sum(axis=1).replace(0, np.nan)
    net = (S * F - c.CM).where(akt).sum(axis=1) / k
    abn = (S * (F - F.mean()) - c.CM).where(akt).sum(axis=1) / k
    return net, abn


def ucuz_ek(c, S, h):
    """E ve F koşulları + yıl tablosu, kriz hariç, VIX rejimi, maliyet iki katı (gün bazlı portföy serisinden)."""
    net, abn = gunluk(c, S, h)
    v = net.dropna()
    out = {}
    if len(v) < 20:
        return out, None
    yt = pd.DataFrame({"n_gun": v.groupby(v.index.year).size(), "net_bps": (v.groupby(v.index.year).mean() * 1e4).round(1)})
    y3 = yt[yt.n_gun >= 3]
    out["yil_pozitif_oran"] = round(float((y3.net_bps > 0).mean()), 2) if len(y3) else np.nan
    out["yil_sayisi"] = int(len(y3))
    if len(v) > 30:
        kalan = v.sort_values(ascending=False).iloc[10:]
        z2 = pd.Series(0.0, index=net.index)
        z2[kalan.index] = kalan
        out["tum_net_bps_ust10_haric"] = round(float(kalan.mean()) * 1e4, 1)
        out["tum_t_ust10_haric"] = round(float(o.hac_t(z2.values, lag=h - 1)), 2)
    if len(y3):
        eniyi = (y3.net_bps * y3.n_gun).idxmax()
        a2 = abn[abn.index.year != eniyi]
        out["eniyi_yil"] = int(eniyi)
        out["eniyi_yil_haric_t"] = round(float(o.hac_t(a2.fillna(0.0).values, lag=h - 1)), 2)
    for ad, m in (("kriz_haric", ~c.kriz), ("vix_yuksek", c.vix_y.values), ("vix_dusuk", ~c.vix_y.values)):
        a = abn[m]
        if a.notna().sum() >= 20:
            out[f"{ad}_bps"] = round(float(a.mean()) * 1e4, 1)
            out[f"{ad}_t"] = round(float(o.hac_t(a.fillna(0.0).values, lag=h - 1)), 2)
    akt = (S != 0) & c.FH[h].notna()
    out["maliyet_ort_bps"] = round(float(c.CM.where(akt).stack().mean()) * 1e4, 1)
    out["maliyet2x_anormal_bps"] = round(float(abn.mean()) * 1e4 - out["maliyet_ort_bps"], 1)
    return out, yt


def plasebo_havuz(c, S, h, n=1000, min_k=60, tohum=0):
    """H koşulu (ortak.plasebo_dairesel'in havuz uyarlaması): sinyal matrisi zamanda dairesel kaydırılır."""
    F = c.FH[h]
    A = (F - F.mean()).values
    sv = S.values
    rows, cols = np.nonzero(sv)
    sg = sv[rows, cols]
    T = c.T

    def stat(r):
        a = A[r, cols]
        ok = ~np.isnan(a)
        num = np.bincount(r[ok], weights=(sg * a)[ok], minlength=T)
        den = np.bincount(r[ok], minlength=T)
        g = den > 0
        return float((num[g] / den[g]).mean()) if g.any() else np.nan

    gercek = stat(rows)
    rng = np.random.default_rng(tohum)
    st = np.array([stat((rows + int(k)) % T) for k in rng.integers(min_k, T - min_k, n)])
    return {"plasebo_p": round(float((np.sum(st >= gercek) + 1) / (n + 1)), 4), "plasebo_ort_bps": round(float(np.nanmean(st)) * 1e4, 2)}


def pahali_ek(c, S, h, n_plasebo=1000):
    """I ve H koşulları + SPY'dan arındırılmış test (ön elemeyi geçenlerde)."""
    ac, er = o.havuz_testi(S, h, giris="acilis"), o.havuz_testi(S, h, giris="ertesi")
    out = {"acilis_anormal_bps": ac.get("anormal_net_bps"), "acilis_net_bps": ac.get("net_bps"), "acilis_t_anormal": ac.get("t_anormal"),
           "ertesi_anormal_bps": er.get("anormal_net_bps"), "ertesi_t_anormal": er.get("t_anormal")}
    out.update(plasebo_havuz(c, S, h, n=n_plasebo))
    kol = S.columns[(S != 0).any()]
    hi = o.havuz_testi(S[kol], h, bit=o.IS_BITIS, hedge="SPY")
    ho = o.havuz_testi(S[kol], h, bas=o.OOS_BAS, hedge="SPY")
    out.update({"hedge_is_bps": hi.get("anormal_net_bps"), "hedge_is_t": hi.get("t_anormal"),
                "hedge_oos_bps": ho.get("anormal_net_bps"), "hedge_oos_t": ho.get("t_anormal")})
    return out


def on_eleme(d):
    return (d.get("is_t_anormal") or 0) >= 2.0 and (d.get("oos_t_anormal") or 0) >= 1.5 and (d.get("is_anormal_net_bps") or 0) > 0


def kos(c, M, sinyal_id, tanim, tur="ana", ufuklar=UFUK, bacaklar=("AL", "SAT"), zorla_ek=False):
    """M: T x N işaret matrisi (+1/-1/0). Her bacak ve ufuk ayrı test satırı."""
    sat = []
    for yon in bacaklar:
        S = df(c, np.where(M > 0, 1.0, 0.0) if yon == "AL" else np.where(M < 0, -1.0, 0.0))
        if not (S != 0).values.any():
            continue
        ss = S.sum(axis=1)
        sonr = S.iloc[-1]
        son3 = S.iloc[-3:]
        acik = [f"{s}@{g.strftime('%m-%d')}" for g, r_ in son3.iterrows() for s in r_[r_ != 0].index]
        for h in ufuklar:
            d = o.havuz_donemli(S, h)
            row = {"aile": "F6", "sinyal_id": f"{sinyal_id}_{yon}_h{h}", "kural": sinyal_id, "oncu": tanim, "hedef": "havuz:evren hisseleri",
                   "bicim": sinyal_id.split("_")[0], "yon": yon, "h": h, "havuz": "portföy", "bayat_isaret": False, "tur": tur}
            row.update(d)
            row["tum_n"], row["oos_n"] = d.get("tum_n_gun", 0), d.get("oos_n_gun", 0)   # G koşulu: sinyal GÜNÜ sayısı (temkinli)
            row.update(o.son_sinyal(ss))
            row["son_adet"] = int((sonr != 0).sum())
            row["son_semboller"] = " ".join(sonr[sonr != 0].index[:60])
            row["acik_3g"] = " ".join(acik[:80])
            if tur in ("ana", "kesif") or zorla_ek:
                u, yt = ucuz_ek(c, S, h)
                row.update(u)
                if on_eleme(d) or zorla_ek:
                    row.update(pahali_ek(c, S, h))
                    if yt is not None:
                        c.yil.append(yt.assign(sinyal_id=row["sinyal_id"]).reset_index(names="yil"))
                    F = c.FH[h]
                    tr = (S * F).where((S != 0) & F.notna()).stack()
                    b = tr.reindex(tr.abs().sort_values(ascending=False).index[:20])
                    c.buyuk.append(pd.DataFrame({"sinyal_id": row["sinyal_id"], "tarih": [i[0].strftime("%Y-%m-%d") for i in b.index],
                                                 "sembol": [i[1] for i in b.index], "islem_getiri_%": (b.values * 100).round(1)}))
                    row["n_asiri_getiri"] = int((tr.abs() > 0.8).sum())
            sat.append(row)
        log(sinyal_id, yon, "bitti")
    return sat


def kaydet(c, sat, ad):
    pd.DataFrame(sat).to_csv(os.path.join(CIKTI, f"ara_{ad}.csv"), index=False)
    if c.yil:
        pd.concat(c.yil).to_csv(os.path.join(CIKTI, f"ara_yil_{ad}.csv"), index=False)
    if c.buyuk:
        pd.concat(c.buyuk).to_csv(os.path.join(CIKTI, f"ara_buyuk_{ad}.csv"), index=False)
    c.yil, c.buyuk = [], []


def ozet_yaz(anahtar, deger):
    yol = os.path.join(CIKTI, "ozet.json")
    d = json.load(open(yol)) if os.path.exists(yol) else {}
    d[anahtar] = deger
    json.dump(d, open(yol, "w"), ensure_ascii=False, indent=1, default=str)


# ------------------------------------------------------------------------------------------------------------
# (a) Bilanço sonrası sürüklenme
# ------------------------------------------------------------------------------------------------------------


def asama_a(c):
    ol = c.ol
    buyuk = ol[ol.z.abs() >= Z_ESIK]
    isr = np.sign(buyuk.z.values)
    sat = []
    sat += kos(c, mat(c, buyuk.ir, buyuk.ci, isr), "a_z", "tepki günü anormal getiri |z|>=2, tepki yönünde")
    ay = buyuk[buyuk.s_isaret.values == isr]
    sat += kos(c, mat(c, ay.ir, ay.ci, np.sign(ay.z)), "a_zs", "|z|>=2 ve EPS sürprizi aynı işaret")
    for ad, m in (("a_z_likit", buyuk.likit), ("a_z_azlikit", ~buyuk.likit)):
        x = buyuk[m.values]
        sat += kos(c, mat(c, x.ir, x.ci, np.sign(x.z)), ad, "|z|>=2; dolar hacmi yılın olay medyanının " + ("üstü" if ad == "a_z_likit" else "altı"))
    # --- sağlamlık (sınıf almaz) ---
    # geç etiketleme: (1) tümüyle nedensel kural: d günü |z|>=2 ve hacim>=1,5x ise d; değilse d+1 günü |z|>=2 ve hacim>=1,5x
    ev = c.ev
    n0 = (ev.z0.abs() >= Z_ESIK) & (ev.v0 >= HACIM_ESIK)
    n1 = ~n0 & (ev.z1.abs() >= Z_ESIK) & (ev.v1 >= HACIM_ESIK)
    M = mat(c, ev.i0[n0], ev.ci[n0], np.sign(ev.z0[n0])) + mat(c, ev.i0[n1] + 1, ev.ci[n1], np.sign(ev.z1[n1]))
    sat += kos(c, np.sign(M), "a_nedensel", "ileri bakışsız etiket: d günü belirginse d, değilse d+1", tur="saglamlik", zorla_ek=True)
    for ad, m in (("a_tarih_gunu", buyuk.etiket == 0), ("a_ertesi_gun", buyuk.etiket == 1)):
        x = buyuk[m.values]
        sat += kos(c, mat(c, x.ir, x.ci, np.sign(x.z)), ad, "|z|>=2; tepki günü = " + ("takvim tarihi" if ad == "a_tarih_gunu" else "tarihten sonraki gün"), tur="saglamlik")
    x = ol[ol.z.abs() >= 3]
    sat += kos(c, mat(c, x.ir, x.ci, np.sign(x.z)), "a_z3", "eşik |z|>=3", tur="saglamlik")
    # kıyas: bilanço dışı günlerde aynı kural (olaydan +-5 gün uzak)
    OL = np.zeros((c.T, c.N))
    OL[ev.i0.values, ev.ci.values] = 1
    OL[ol.ir.values, ol.ci.values] = 1
    yakin = pd.DataFrame(OL).rolling(11, center=True, min_periods=1).max().values > 0
    zv = np.nan_to_num(c.Z.values)
    sat += kos(c, np.where(~yakin & (np.abs(zv) >= Z_ESIK), np.sign(zv), 0.0), "kiyas_bilanco_disi", "bilanço dışı günde |z|>=2, hareket yönünde", tur="kiyas")
    kaydet(c, sat, "a")
    ozet_yaz("isabet", c.isabet)
    ozet_yaz("olay", {"takvim_kaydi": int(len(c.ev)), "tepki_gunu_etiketli": int(len(ol)), "cift_kayit_atilan": int(c.cift_kayit),
                      "z2_ustu_olay": int(len(buyuk)), "z2_al": int((isr > 0).sum()), "z2_sat": int((isr < 0).sum()),
                      "surpriz_ayni_yon": int(len(ay)), "surpriz_kirpilan": int((ol.surpriz_yuzde.abs() > 200).sum())})


# ------------------------------------------------------------------------------------------------------------
# (b) Lider bilançosundan emsallere yayılım
# ------------------------------------------------------------------------------------------------------------


def asama_b(c):
    ol, T, N = c.ol, c.T, c.N
    OWN = np.zeros((T, N), bool)
    OWN[ol.ir.values, ol.ci.values] = True
    son5 = pd.DataFrame(OWN.astype(float)).rolling(6, min_periods=1).max().values > 0       # t-5..t içinde kendi tepki günü
    idx = np.where(OWN, np.arange(T)[:, None].astype(float), np.nan)
    nxt = pd.DataFrame(idx).shift(-1).bfill().values                                         # sonraki kendi tepki günü
    dist = nxt - np.arange(T)[:, None]
    lid = ol[ol.z.abs() >= Z_ESIK]
    G, G3 = np.zeros((T, N)), np.zeros((T, N))
    n_lid3 = 0
    for g, mem in c.uye.items():
        mi = np.array([c.ix[s] for s in mem])
        le = lid[lid.ci.isin(mi)]
        if not len(le):
            continue
        tot = np.zeros(T)
        np.add.at(tot, le.ir.values, np.sign(le.z.values))
        G[:, mi] += tot[:, None]
        rk = c.DV.iloc[:, mi].rank(axis=1, ascending=False).values
        l3 = le[rk[le.ir.values, pd.Index(mi).get_indexer(le.ci.values)] <= 3]
        n_lid3 += len(l3)
        tot3 = np.zeros(T)
        np.add.at(tot3, l3.ir.values, np.sign(l3.z.values))
        G3[:, mi] += tot3[:, None]
    uygun = ~son5
    sig, sig3 = np.sign(G) * uygun, np.sign(G3) * uygun
    zp = np.nan_to_num(c.Z.values) * sig                                                     # emsalin t günü kendi tepkisi (lider yönünde +)
    yak = (dist >= 1) & (dist <= 15)
    sat = []
    sat += kos(c, sig, "b_tum", "grup liderinin tepkisi |z|>=2; son 5 günde açıklamamış emsaller, lider yönünde")
    sat += kos(c, sig3, "b_lider3", "lider = grubun dolar hacmi en yüksek 3 hissesi")
    sat += kos(c, np.where(yak, sig, 0.0), "b_yakinda", "emsal 1-15 gün içinde kendi bilançosunu açıklayacak")
    sat += kos(c, np.where(~yak, sig, 0.0), "b_uzak", "emsalin 15 gün içinde bilançosu yok")
    sat += kos(c, np.where(zp >= 1, sig, 0.0), "b_emsal_ayni", "emsal t günü lider yönünde hareket etmiş (z>=1)")
    sat += kos(c, np.where(np.abs(zp) < 1, sig, 0.0), "b_emsal_notr", "emsal t günü hareketsiz (|z|<1)")
    sat += kos(c, np.where(zp <= -1, sig, 0.0), "b_emsal_ters", "emsal t günü lidere ters hareket etmiş (z<=-1)")
    # KEŞİF (önceden yazılı değil, test sayısına dahil): emsal lider yönünde zaten hareket ettiyse TERSİNE gir
    # (AL = liderin kötü tepkisiyle birlikte düşen emsali al). Hisse düzeyi AL-dönüş: en çok KOŞULLU.
    sat += kos(c, np.where(zp >= 1, -sig, 0.0), "k_emsal_donus", "KEŞİF: emsal lider yönünde z>=1 hareket etmiş; ters yönde gir", tur="kesif")
    kaydet(c, sat, "b")
    # Thomas-Zhang (2008) betimsel sınama: emsalin lidere erken tepkisi ile kendi bilanço tepkisi ters mi?
    r, k = np.nonzero((sig != 0) & yak)
    x = c.AR.values[r, k]
    y = c.AR.values[nxt[r, k].astype(int), k]
    d = pd.DataFrame({"x": x, "y": y, "kume": nxt[r, k].astype(int), "lider_yon": sig[r, k]}).dropna()
    tz = {"n": int(len(d))}
    try:
        import statsmodels.api as sm
        m = sm.OLS(d.y, sm.add_constant(d[["x"]])).fit(cov_type="cluster", cov_kwds={"groups": d.kume})
        tz.update({"egim": round(float(m.params["x"]), 4), "t_kume": round(float(m.tvalues["x"]), 2)})
        m2 = sm.OLS(d.y, sm.add_constant(d[["lider_yon"]])).fit(cov_type="cluster", cov_kwds={"groups": d.kume})
        tz.update({"lider_yonu_bps": round(float(m2.params["lider_yon"]) * 1e4, 1), "lider_yonu_t": round(float(m2.tvalues["lider_yon"]), 2)})
    except Exception as e:  # noqa: BLE001
        tz["hata"] = str(e)[:80]
    ozet_yaz("thomas_zhang", tz)
    ozet_yaz("emsal", {"lider_olay": int(len(lid)), "lider3_olay": int(n_lid3), "emsal_islem": int((sig != 0).sum()),
                       "emsal_ayni_pay": round(float((zp >= 1).sum() / max((sig != 0).sum(), 1)), 3),
                       "emsal_ters_pay": round(float((zp <= -1).sum() / max((sig != 0).sum(), 1)), 3)})


# ------------------------------------------------------------------------------------------------------------
# (c) Bilanço öncesi prim (yalnız yüksek hacimli hisseler: 60 günlük medyan dolar hacmi >= 100 mn $)
# ------------------------------------------------------------------------------------------------------------


def asama_c(c):
    ol, ev, dv = c.ol, c.ev, c.DV.values
    sat, dag = [], {}
    g1 = ol[(ol.ir >= 1)]
    g1 = g1[dv[g1.ir.values - 1, g1.ci.values] >= LIKIT_MN]
    M1 = mat(c, g1.ir.values - 1, g1.ci.values, np.ones(len(g1)))
    sat += kos(c, M1, "c_onceki_kapanis", "tepki gününden önceki kapanışta al, tepki günü kapanışında sat (çıkarılan etiket)", ufuklar=(1,), bacaklar=("AL",), zorla_ek=True)
    g2 = ev[ev.i0 >= 1]
    g2 = g2[dv[g2.i0.values - 1, g2.ci.values] >= LIKIT_MN]
    M2 = mat(c, g2.i0.values - 1, g2.ci.values, np.ones(len(g2)))
    sat += kos(c, M2, "c_etiketsiz_2g", "takvim tarihinden önceki kapanışta al, 2 gün sonra sat (etiket gerektirmez)", ufuklar=(2,), bacaklar=("AL",), zorla_ek=True)
    kaydet(c, sat, "c")
    spyf = {h: o.ileri_getiri(["SPY"], h)["SPY"].values for h in (1, 2)}
    for ad, M, h in (("c_onceki_kapanis", M1, 1), ("c_etiketsiz_2g", M2, 2)):
        r, k = np.nonzero(M)
        f = c.FH[h].values[r, k] - c.CM.values[r, k]
        ok = ~np.isnan(f)
        f, rr, kk = f[ok], r[ok], k[ok]
        dr = c.FH[h].mean().values[kk]
        p5 = np.percentile(f, 5)
        for dn, m in (("tum", np.ones(len(f), bool)), ("is", c.tk[rr] <= o.IS_BITIS), ("oos", c.tk[rr] >= o.OOS_BAS), ("son", c.tk[rr] >= o.SON_BAS)):
            x = f[m]
            if len(x) < 30:
                continue
            q = np.percentile(x, 5)
            dag[f"{ad}_{dn}"] = {"n": int(len(x)), "net_ort_bps": round(float(x.mean()) * 1e4, 1), "std_bps": round(float(x.std()) * 1e4, 0),
                                 "medyan_bps": round(float(np.median(x)) * 1e4, 1), "yuzde5_bps": round(float(q) * 1e4, 0),
                                 "en_kotu_%5_ort_bps": round(float(x[x <= q].mean()) * 1e4, 0), "en_kotu_bps": round(float(x.min()) * 1e4, 0),
                                 "isabet": round(float((x > 0).mean()), 3),
                                 "surukl_duz_ort_bps": round(float((x - dr[m]).mean()) * 1e4, 1),
                                 "spy_ayni_gun_ort_bps": round(float(np.nanmean(spyf[h][rr[m]])) * 1e4, 1)}
    ozet_yaz("on_prim_dagilim", dag)


# ------------------------------------------------------------------------------------------------------------
# (d) Önümüzdeki 4 hafta
# ------------------------------------------------------------------------------------------------------------


def asama_d(c):
    g = gelecek_indir()
    if not len(g):
        ozet_yaz("gelecek", {"hata": "takvim indirilemedi"})
        return
    g = g[g.sembol.isin(c.syms)].copy()
    grp = {s: gr for gr, mem in c.uye.items() for s in mem}
    g["grup"] = g.sembol.map(grp).fillna("")
    gun = pd.to_datetime(g.tarih)
    tatil = pd.tseries.offsets.CustomBusinessDay(holidays=["2026-11-26", "2026-12-25"])
    g["tepki_gunu"] = [(d_ + tatil).date() if z == "time-after-hours" else d_.date() for d_, z in zip(gun, g.zaman)]
    g["on_prim_alim_gunu"] = [(pd.Timestamp(t_) - tatil).date() for t_ in g.tepki_gunu]
    dvs = c.DV.iloc[-1]
    g["dolar_hacim_mn"] = g.sembol.map(dvs).round(0)
    g = g.sort_values(["tarih", "dolar_hacim_mn"], ascending=[True, False])
    g.to_csv(os.path.join(CIKTI, "gelecek_bilanco.csv"), index=False)
    ozet_yaz("gelecek", {"n": int(len(g)), "ilk": g.tarih.min(), "son": g.tarih.max(), "zaman": g.zaman.value_counts().to_dict(),
                         "hafta": g.groupby(pd.to_datetime(g.tarih).dt.strftime("%G-H%V")).sembol.apply(lambda s: " ".join(s)).to_dict()})
    log("gelecek takvim (evren):", len(g))


# ------------------------------------------------------------------------------------------------------------
# Birleştirme ve sınıflandırma
# ------------------------------------------------------------------------------------------------------------


def bitir():
    par = [pd.read_csv(os.path.join(CIKTI, f"ara_{a}.csv")) for a in "abc" if os.path.exists(os.path.join(CIKTI, f"ara_{a}.csv"))]
    d = pd.concat(par, ignore_index=True)
    ana = d[d.tur.isin(["ana", "kesif"])].copy()
    tmp = ana.copy()
    sat_kotu = (tmp.yon == "SAT") & ~(pd.to_numeric(tmp.tum_net_bps, errors="coerce") >= 0)
    tmp.loc[sat_kotu, "tum_anormal_net_bps"] = -1.0          # D koşulu: SAT bacağında ham net >= 0 (siniflandir bunu uygulamıyor)
    tavan = tmp.sinyal_id.str.startswith(("c_", "k_"))               # bilanço öncesi prim: hayatta kalma yanlılığı -> en çok KOŞULLU
    tmp = o.siniflandir(tmp, tavan_kosullu=tavan)
    for k in [x for x in tmp.columns if x.startswith("k_")] + ["p_oos", "bh_oos", "sinif"]:
        ana[k] = tmp[k]
    ana["k_D_sat_ham_net"] = ~sat_kotu
    d = pd.concat([ana, d[~d.tur.isin(["ana", "kesif"])]], ignore_index=True)
    d["sinif"] = d.sinif.fillna("SINIFSIZ")
    d.to_csv(os.path.join(CIKTI, "sonuclar.csv"), index=False)
    sira = {"SAGLAM": 0, "KOSULLU": 1, "IZLE": 2}
    ak = ana[ana.sinif != "ELENDI"].copy()
    ak["_s"] = ak.sinif.map(sira)
    ak = ak.sort_values(["_s", "oos_t_anormal"], ascending=[True, False]).drop(columns="_s")
    ak.to_csv(os.path.join(CIKTI, "ayakta_kalanlar.csv"), index=False)
    for ad in ("yil", "buyuk"):
        pp = [pd.read_csv(os.path.join(CIKTI, f"ara_{ad}_{a}.csv")) for a in "abc" if os.path.exists(os.path.join(CIKTI, f"ara_{ad}_{a}.csv"))]
        if pp:
            pd.concat(pp).to_csv(os.path.join(CIKTI, "yil_tablosu.csv" if ad == "yil" else "en_buyuk_islemler.csv"), index=False)
    n = len(ana)
    ist = pd.to_numeric(ana.is_t_anormal, errors="coerce")
    oost = pd.to_numeric(ana.oos_t_anormal, errors="coerce")
    oz = {"test_ana": int(n), "test_kesif": int((ana.tur == "kesif").sum()), "test_saglamlik_kiyas": int((~d.tur.isin(["ana", "kesif"])).sum()),
          "beklenen_yanlis_pozitif_saglam": round(n * o.P_SIFIR_SAGLAM, 4), "beklenen_yanlis_pozitif_kosullu": round(n * o.P_SIFIR_KOSULLU, 4),
          "sinif": ana.sinif.value_counts().to_dict(),
          "eleme": {"IS t>=2.5 (A)": int(ana.k_A.sum()), "A ve OOS t>=2.0": int((ana.k_A & ana.k_B_zayif).sum()),
                    "A ve OOS t>=2.5 (B)": int((ana.k_A & ana.k_B).sum()), "A ve BH": int((ana.k_A & ana.bh_oos).sum()),
                    "IS t<=-2.0 (ters yön)": int((ist <= -2).sum()), "OOS t<=-2.0 (ters yön)": int((oost <= -2).sum()),
                    "on eleme (IS t>=2, OOS t>=1.5)": int(((ist >= 2) & (oost >= 1.5)).sum())}}
    ozet_yaz("sonuc", oz)
    kol = ["sinyal_id", "tum_n_islem", "tum_n_gun", "tum_net_bps", "tum_anormal_net_bps", "is_anormal_net_bps", "is_t_anormal",
           "oos_anormal_net_bps", "oos_t_anormal", "son_net_bps", "son_anormal_net_bps", "sinif"]
    pd.set_option("display.width", 250)
    print(json.dumps(oz, ensure_ascii=False))
    print(d[d.sinif != "ELENDI"][kol + ["tur"]].to_string(index=False))


if __name__ == "__main__":
    asama = sys.argv[1] if len(sys.argv) > 1 else "hepsi"
    if asama == "indir":
        gelecek_indir()
        e = edgar_indir()
        if len(e):
            et = pd.to_datetime(e.kabul, utc=True)
            print(e.assign(saat_utc=et.dt.hour).groupby("sembol").saat_utc.agg(["size", "median", "min", "max"]), e.kabul.min())
        sys.exit(0)
    if asama == "son":
        bitir()
        sys.exit(0)
    ctx = hazirla()
    if asama in ("a", "hepsi"):
        asama_a(ctx)
    if asama in ("b", "hepsi"):
        asama_b(ctx)
    if asama in ("c", "hepsi"):
        asama_c(ctx)
    if asama in ("d", "hepsi"):
        asama_d(ctx)
    if asama == "hepsi":
        bitir()
    log("bitti:", asama)
