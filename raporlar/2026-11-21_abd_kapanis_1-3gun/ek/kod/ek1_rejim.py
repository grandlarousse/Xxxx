#!/usr/bin/env python3
"""ek1_rejim.py - YONTEM.md "Ek 1": rejime kosullu kisa vadeli donus hipotezinin (E1-a, E1-b)
dokunulmamis orneklemde (1993-02-01 -> 2004-12-31) sinanmasi. Gorev KF1.

Bagimsiz betik: projenin motorunu (motor.py) KULLANMAZ; duz pandas/numpy.
Calistirma (ham dosyalar depoda degil):
    python3 -I ek1_rejim.py <ham_klasor> [<cikti_klasor>]
Ham klasorde Yahoo chart API JSON'lari: SPY.json _VIX.json QQQ.json DIA.json MDY.json UPRO.json TQQQ.json

Tanimlar (gorev tanimi + YONTEM Ek 1; hesaptan once yazildi, sonuca gore degistirilmedi):
  getiri            duzeltilmis kapanistan; duzeltilmis acilis = acilis * duz.kapanis / kapanis
  RSI(2)            Wilder (alfa = 1/2), duzeltilmis kapanistan, ilk farkla baslatilir
  IBS               (kapanis - dusuk) / (yuksek - dusuk); yuksek == dusuk ise tanimsiz (sinyal yok)
  rejim(t)          VIX(t-1) > 30  ve  SPY kapanis(t-1) < t-1'de biten 200 gunluk ortalama (temettusuz kapanis)
  islem             sinyal gunu t kapanisinda al, t+h kapanisinda sat (h = 1 birincil)
  bolum             aralarinda 20'den az VIX <= 30 gunu olan VIX > 30 gunleri tek bolum; islem, t-1 gununun bolumune yazilir
  taban             ayni orneklemde rejim(t) dogru olan BUTUN gunlerin 1 gunluk ileri getirisinin ortalamasi
  anormal           islem getirisi - taban  (olcut icin NET getiriden; brutten olani da raporlanir)
  olcekli           net getiri / SPY'nin t-1'de biten 20 gunluk gunluk getiri sigmasi
  maliyet           gidis-donus 12 bps (sinyal gunu < 2001-04-01), 6 bps (sonrasi); duyarlilik x2
  olcutler          (i) net ort > 0; (ii) olcekli t >= 2; (iii) anormal > 0 ve tarihe gore kumelenmis t >= 2;
                    (iv) >= 4 bolum ve bolumlerin >= %70'inde net toplam > 0; (v) en buyuk bolum (islem sayisina gore;
                    esitlikte en kotu durum) cikarilinca net > 0; (vi) maliyet x2 ile net > 0
  sinif             6/6 -> KOSULLU; (i)-(iii) tamam, (iv)-(vi)'dan eksik var -> DUSUK; aksi -> ELENDI
"""
import sys, os, json, math
import numpy as np
import pandas as pd

HAM = sys.argv[1] if len(sys.argv) > 1 else "/tmp/claude-0/-home-user-Xxxx/b23916bf-451a-5d36-8905-d1866417ce1f/scratchpad/ek1_ham"
CIKTI = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "veri")
SON_GUN = pd.Timestamp("2026-11-20")
ORNEK = {"1993-2004": ("1993-02-01", "2004-12-31"), "2005-2026": ("2005-01-03", "2026-11-20"),
         "1993-2026": ("1993-02-01", "2026-11-20")}
ALT = {"2005-2009": ("2005-01-03", "2009-12-31"), "2010-2019": ("2010-01-01", "2019-12-31"),
       "2020-2023": ("2020-01-01", "2023-12-31"), "2024-2026": ("2024-01-01", "2026-11-20")}
ONDALIK = pd.Timestamp("2001-04-01")
BPS = 1e4


# ------------------------------------------------------------------ veri
def yukle(kod):
    with open(os.path.join(HAM, kod + ".json")) as f:
        r = json.load(f)["chart"]["result"][0]
    ts = np.asarray(r["timestamp"], dtype="int64") + int(r["meta"]["gmtoffset"])
    q = r["indicators"]["quote"][0]
    d = pd.DataFrame({"open": q["open"], "high": q["high"], "low": q["low"], "close": q["close"],
                      "adj": r["indicators"]["adjclose"][0]["adjclose"]},
                     index=pd.to_datetime(ts, unit="s").normalize()).astype(float)
    n0 = len(d)
    d = d[d["close"].notna() & d["adj"].notna()]
    d = d[~d.index.duplicated(keep="last")]
    d = d[d.index <= SON_GUN].sort_index()
    d.attrs["bos_satir"] = n0 - len(d)
    return d


def rsi2(adj):
    f = adj.diff()
    ag = f.clip(lower=0).ewm(alpha=0.5, adjust=False).mean()
    al = (-f).clip(lower=0).ewm(alpha=0.5, adjust=False).mean()
    t = ag + al
    return (100 * ag / t.where(t > 0)), ag, al


def ibs(d):
    a = d["high"] - d["low"]
    return (d["close"] - d["low"]) / a.where(a > 0)


def hazirla(spy, vix):
    """SPY takviminde rejim, bolum, sigma20. Hicbiri t gununun VIX'ini ya da t+1 verisini kullanmaz."""
    g = pd.DataFrame(index=spy.index)
    v = vix["close"].reindex(spy.index)            # ileri doldurma yok
    g["vix"] = v
    g["vix_1"] = v.shift(1)
    ma = spy["close"].rolling(200, min_periods=200).mean()
    g["ma200"] = ma
    g["alt_1"] = (spy["close"] < ma).where(ma.notna()).shift(1)      # t-1 kapanisi < t-1'de biten ortalama
    g["rejim"] = (g["vix_1"] > 30) & (g["alt_1"] == True)            # noqa: E712
    g["tanimli"] = g["vix_1"].notna() & g["alt_1"].notna()
    r = spy["adj"].pct_change()
    g["sigma20"] = r.rolling(20, min_periods=20).std().shift(1)
    # bolumler (VIX > 30 gunleri; arada < 20 adet VIX <= 30 gunu varsa ayni bolum)
    bol = np.zeros(len(g), int)
    no, sayac, ilk = 0, 0, True
    vv = v.to_numpy()
    for i in range(len(g)):
        if np.isfinite(vv[i]) and vv[i] > 30:
            if ilk or sayac >= 20:
                no += 1
            bol[i] = no
            sayac, ilk = 0, False
        elif np.isfinite(vv[i]):
            sayac += 1
    g["bolum_gun"] = bol                                             # VIX(t) > 30 gununun bolumu
    g["bolum"] = pd.Series(bol, index=g.index).shift(1).fillna(0).astype(int)   # islem gunu t icin: t-1'in bolumu
    return g


def maliyet(idx, kat=1.0, ek=0.0):
    return pd.Series(np.where(idx < ONDALIK, 12.0, 6.0) + ek, index=idx) / BPS * kat


# ------------------------------------------------------------------ islemler
def islemler(sinyal, px, tak, h=1, giris="K", cikis="kapanis"):
    """sinyal: SPY takviminde bool seri. px: hedefin fiyatlari (SPY takvimine hizalanmis).
    h>1'de acik pozisyon varken (t+1..t+h-1) yeni sinyal alinmaz. Donus: islem tablosu (brut)."""
    adj = px["adj"].to_numpy()
    aop = (px["open"] * px["adj"] / px["close"]).to_numpy()
    s = sinyal.to_numpy(dtype=bool)
    T = len(tak)
    out, mesgul = [], -1
    for t in np.flatnonzero(s):
        if t < mesgul:
            continue
        if cikis == "acilis":                       # gece: t kapanis -> t+1 acilis
            if t + 1 >= T:
                continue
            p0, p1, tc = adj[t], aop[t + 1], t + 1
        else:
            if t + h >= T:
                continue
            p0 = adj[t] if giris == "K" else aop[t + 1]
            p1, tc = adj[t + h], t + h
            mesgul = t + h
        if not (np.isfinite(p0) and np.isfinite(p1)):
            continue
        out.append((tak[t], tak[tc], p1 / p0 - 1.0))
    return pd.DataFrame(out, columns=["t", "cikis_tarihi", "brut"])


def kume_t(a, kume, en_az=2):
    a = np.asarray(a, float)
    n = a.size
    if n < 3:
        return np.nan
    _, tr = np.unique(np.asarray(kume), return_inverse=True)
    gs = np.bincount(tr, weights=a - a.mean())
    G = gs.size
    if G < 2 or G < en_az:
        return np.nan
    se = math.sqrt(G / (G - 1.0) * float((gs * gs).sum())) / n
    return a.mean() / se if se > 0 else np.nan


def ardisik_kayip(net, en_buyuk=False):
    """En uzun ardisik kayip serisi (adet, toplam). en_buyuk=True: toplam kaybi en buyuk seri (adet, toplam)."""
    en, en_cum, k, c = 0, 0.0, 0, 0.0
    for x in net:
        if x < 0:
            k += 1; c += x
            if (c < en_cum) if en_buyuk else (k > en or (k == en and c < en_cum)):
                en, en_cum = k, c
        else:
            k, c = 0, 0.0
    return en, en_cum


def ozet(isl, taban, ek_mal=0.0):
    """isl: t, brut, sigma20, bolum sutunlari. Donus: olcut sozlugu."""
    o = {"n": int(len(isl))}
    if len(isl) == 0:
        return o
    idx = pd.DatetimeIndex(isl["t"])
    m = maliyet(idx, 1.0, ek_mal).to_numpy()
    brut = isl["brut"].to_numpy()
    net, net2 = brut - m, brut - 2 * m
    olc = net / isl["sigma20"].to_numpy()
    olc = olc[np.isfinite(olc)]
    o.update(brut_bps=brut.mean() * BPS, net_bps=net.mean() * BPS, net2x_bps=net2.mean() * BPS,
             t_net=(net.mean() / (net.std(ddof=1) / math.sqrt(len(net))) if len(net) > 2 else np.nan),
             t_olcekli=(olc.mean() / (olc.std(ddof=1) / math.sqrt(len(olc))) if len(olc) > 2 else np.nan),
             net_sigma=olc.mean() if len(olc) else np.nan,
             taban_bps=taban * BPS, anormal_net_bps=(net.mean() - taban) * BPS,
             anormal_brut_bps=(brut.mean() - taban) * BPS,
             t_anormal_tarih=kume_t(net - taban, isl["t"].to_numpy()),
             t_anormal_bolum=kume_t(net - taban, isl["bolum"].to_numpy(), en_az=4),
             se_net_bps=(net.std(ddof=1) / math.sqrt(len(net)) * BPS if len(net) > 2 else np.nan),
             isabet=float((net > 0).mean()), medyan_bps=float(np.median(net)) * BPS,
             en_kotu_bps=net.min() * BPS, en_iyi_bps=net.max() * BPS, toplam_net_bps=net.sum() * BPS)
    k = max(3, int(math.ceil(0.05 * len(net))))
    o["en_iyi5pct_haric_net_bps"] = np.sort(net)[:-k].mean() * BPS if len(net) > k else np.nan
    o["en_uzun_ardisik_kayip"], c = ardisik_kayip(net)
    o["ardisik_kayip_bps"] = c * BPS
    o["en_buyuk_ardisik_kayip_adet"], c = ardisik_kayip(net, en_buyuk=True)
    o["en_buyuk_ardisik_kayip_bps"] = c * BPS
    b = isl["bolum"].to_numpy()
    if (b > 0).any():
        d = pd.DataFrame({"b": b, "net": net})[b > 0]
        g = d.groupby("b")["net"]
        tab = pd.DataFrame({"n": g.size(), "top": g.sum()})
        o["bolum_sayisi"] = int(len(tab))
        o["bolum_pozitif_orani"] = float((tab["top"] > 0).mean())
        buyukler = tab.index[tab["n"] == tab["n"].max()]
        kalanlar = [d.loc[d["b"] != x, "net"] for x in buyukler]
        o["en_buyuk_bolum"] = "/".join(str(int(x)) for x in buyukler)
        o["en_buyuk_bolum_n"] = int(tab["n"].max())
        o["en_buyuk_haric_net_bps"] = min((k_.mean() if len(k_) else np.nan) for k_ in kalanlar) * BPS
        kz = d.loc[d["b"] != tab["top"].idxmax(), "net"]
        o["en_kazancli_bolum"] = int(tab["top"].idxmax())
        o["en_kazancli_haric_net_bps"] = kz.mean() * BPS if len(kz) else np.nan
    else:
        o["bolum_sayisi"] = 0
    return o


def karar(o):
    """Ek 1'in alti olcutu ve sinif."""
    if o.get("n", 0) == 0:
        return dict(o_i=False, o_ii=False, o_iii=False, o_iv=False, o_v=False, o_vi=False, sinif="ELENDI")
    f = lambda x: x is not None and np.isfinite(x)
    k = {"o_i": o["net_bps"] > 0,
         "o_ii": f(o["t_olcekli"]) and o["t_olcekli"] >= 2,
         "o_iii": o["anormal_net_bps"] > 0 and f(o["t_anormal_tarih"]) and o["t_anormal_tarih"] >= 2,
         "o_iv": o.get("bolum_sayisi", 0) >= 4 and o.get("bolum_pozitif_orani", 0) >= 0.70,
         "o_v": f(o.get("en_buyuk_haric_net_bps", np.nan)) and o["en_buyuk_haric_net_bps"] > 0,
         "o_vi": o["net2x_bps"] > 0}
    k = {a: bool(b) for a, b in k.items()}
    if all(k.values()):
        k["sinif"] = "KOSULLU"
    elif k["o_i"] and k["o_ii"] and k["o_iii"]:
        k["sinif"] = "DUSUK"
    else:
        k["sinif"] = "ELENDI"
    return k


def kes(s, a, b):
    return s[(s.index >= pd.Timestamp(a)) & (s.index <= pd.Timestamp(b))]


# ------------------------------------------------------------------ ana akis
def main():
    os.makedirs(CIKTI, exist_ok=True)
    spy, vix = yukle("SPY"), yukle("_VIX")
    tak = spy.index
    g = hazirla(spy, vix)
    hedef = {"SPY": spy}
    notlar = [f"VIX bos satir (atildi): {vix.attrs['bos_satir']}; SPY gunlerinde VIX eksik: {int(g['vix'].isna().sum())}"]
    for k in ("QQQ", "DIA", "MDY", "UPRO", "TQQQ"):
        d = yukle(k)
        eks = int((~d.index.isin(tak)).sum())
        ic = tak[(tak >= d.index[0])]
        notlar.append(f"{k}: {d.index[0].date()}'ten, SPY takviminde olmayan gun {eks}, eksik gun {int((~ic.isin(d.index)).sum())}")
        hedef[k] = d.reindex(tak)
    # veri saglamligi (SPY OHLC)
    bozuk = spy[(spy["low"] > spy[["open", "close"]].min(axis=1) + 1e-9) | (spy["high"] < spy[["open", "close"]].max(axis=1) - 1e-9)
                | (spy["high"] <= spy["low"])]
    notlar.append(f"SPY OHLC tutarsiz gun (dusuk>min(a,k) / yuksek<max(a,k) / yuksek<=dusuk): toplam {len(bozuk)}, "
                  f"1993-2004'te {int((bozuk.index <= pd.Timestamp('2004-12-31')).sum())}")

    def sinyaller(px):
        r, _, _ = rsi2(px["adj"])
        return {"E1-a": (r < 10), "E1-b": (ibs(px) < 0.2)}

    sig = {k: sinyaller(hedef[k]) for k in ("SPY", "QQQ", "DIA", "MDY")}
    fwd = {k: hedef[k]["adj"].shift(-1) / hedef[k]["adj"] - 1 for k in hedef}
    REJ = {"rejim": g["rejim"], "rejim_disi": g["tanimli"] & ~g["rejim"],
           "VIX>30&ust": g["tanimli"] & (g["vix_1"] > 30) & (g["alt_1"] == False),      # noqa: E712
           "VIX<=30&alt": g["tanimli"] & (g["vix_1"] <= 30) & (g["alt_1"] == True),     # noqa: E712
           "VIX<=30&ust": g["tanimli"] & (g["vix_1"] <= 30) & (g["alt_1"] == False)}    # noqa: E712

    def taban(k, rj, a, b):
        x = kes(fwd[k][REJ[rj]], a, b).dropna()
        return (x.mean() if len(x) else np.nan), len(x)

    def kur(k_hedef, kural, rj, h=1, giris="K", cikis="kapanis", sinyal_kaynak=None):
        s = sig[sinyal_kaynak or k_hedef][kural] & REJ[rj]
        isl = islemler(s.fillna(False), hedef[k_hedef], tak, h, giris, cikis)
        isl["sigma20"] = g["sigma20"].reindex(isl["t"]).to_numpy()
        isl["bolum"] = g["bolum"].reindex(isl["t"]).to_numpy() if rj in ("rejim", "VIX>30&ust") else 0
        isl["vix_1"] = g["vix_1"].reindex(isl["t"]).to_numpy()
        return isl

    satirlar, tum_isl = [], []

    def ekle(tur, ornek, a, b, k_hedef, kural, rj, h=1, giris="K", cikis="kapanis", sinyal_kaynak=None, ek_mal=0.0,
             kaydet=True, isl=None):
        if isl is None:
            isl = kur(k_hedef, kural, rj, h, giris, cikis, sinyal_kaynak)
        d = isl[(isl["t"] >= pd.Timestamp(a)) & (isl["t"] <= pd.Timestamp(b))].copy()
        tb, tn = taban(k_hedef, rj, a, b)
        if h != 1 or giris != "K" or cikis != "kapanis":
            tb_h = np.nan                                   # taban yalniz 1 gunluk kapanis-kapanis icin tanimli
        else:
            tb_h = tb
        o = ozet(d, tb_h if np.isfinite(tb_h) else 0.0, ek_mal)
        if not np.isfinite(tb_h):
            for x in ("taban_bps", "anormal_net_bps", "anormal_brut_bps", "t_anormal_tarih", "t_anormal_bolum"):
                o[x] = np.nan
        r = dict(tur=tur, ornek=ornek, kural=kural, hedef=k_hedef, sinyal_kaynagi=sinyal_kaynak or k_hedef, h=h,
                 giris=giris, cikis=cikis, rejim=rj, rejim_gun_sayisi=tn)
        r.update(o)
        if tur in ("birincil", "capraz") or (tur == "ek" and rj == "rejim" and h == 1 and giris == "K"):
            kr = karar(o)
            if tur != "birincil":                      # olcutler yalniz betimsel; sinif verilmez
                kr["sinif"] = "(karar degil; betimsel: " + kr["sinif"] + ")"
            r.update(kr)
        satirlar.append(r)
        if kaydet and len(d):
            idx = pd.DatetimeIndex(d["t"])
            m = maliyet(idx, 1.0, ek_mal).to_numpy()
            e = pd.DataFrame({"tur": tur, "ornek": ornek, "kural": kural, "hedef": k_hedef, "h": h, "giris": giris,
                              "cikis": cikis, "rejim": rj, "tarih": idx.strftime("%Y-%m-%d"),
                              "cikis_tarihi": pd.DatetimeIndex(d["cikis_tarihi"]).strftime("%Y-%m-%d"),
                              "brut_bps": (d["brut"] * BPS).round(2).to_numpy(), "maliyet_bps": (m * BPS).round(1),
                              "net_bps": ((d["brut"].to_numpy() - m) * BPS).round(2),
                              "vix_1": d["vix_1"].round(2).to_numpy(), "sigma20_bps": (d["sigma20"] * BPS).round(1).to_numpy(),
                              "bolum": d["bolum"].to_numpy()})
            tum_isl.append(e)
        return r, d

    KUR = ("E1-a", "E1-b")
    # --- 3. birincil
    a, b = ORNEK["1993-2004"]
    birincil = {k: ekle("birincil", "1993-2004", a, b, "SPY", k, "rejim")[0] for k in KUR}
    # --- 4. capraz kontrol
    a2, b2 = ORNEK["2005-2026"]
    capraz = {k: ekle("capraz", "2005-2026", a2, b2, "SPY", k, "rejim")[0] for k in KUR}
    for ad, (x, y) in ALT.items():
        for k in KUR:
            ekle("capraz_alt", ad, x, y, "SPY", k, "rejim", kaydet=False)
    for k in KUR:
        ekle("ek", "1993-2026", *ORNEK["1993-2026"], "SPY", k, "rejim", kaydet=False)
    # --- 5a. h = 2, 3; ertesi acilis; gece
    for on, (x, y) in (("1993-2004", ORNEK["1993-2004"]), ("2005-2026", ORNEK["2005-2026"])):
        for k in KUR:
            for h in (2, 3):
                ekle("ikincil_a", on, x, y, "SPY", k, "rejim", h=h)
            for h in (1, 2, 3):
                ekle("ikincil_a", on, x, y, "SPY", k, "rejim", h=h, giris="A")
            ekle("ikincil_a", on, x, y, "SPY", k, "rejim", h=0, cikis="acilis")
    # --- 5b. QQQ, DIA, MDY (rejim yine VIX ve SPY'den; sinyal hedefin kendi RSI/IBS'i)
            for hd in ("QQQ", "DIA", "MDY"):
                ekle("ikincil_b", on, x, y, hd, k, "rejim")
    # --- 5c. rejim disi
            for rj in ("rejim_disi", "VIX>30&ust", "VIX<=30&alt", "VIX<=30&ust"):
                ekle("ikincil_c", on, x, y, "SPY", k, rj, kaydet=False)
    # --- 5e. kaldiracli ETF (2010 sonrasi; sinyal SPY'den; TQQQ icin QQQ sinyali de)
    for k in KUR:
        ekle("ikincil_e", "2010-2026", "2010-02-11", "2026-11-20", "SPY", k, "rejim", kaydet=False)
        ekle("ikincil_e", "2010-2026", "2010-02-11", "2026-11-20", "QQQ", k, "rejim", kaydet=False)
        ekle("ikincil_e", "2010-2026", "2010-02-11", "2026-11-20", "UPRO", k, "rejim", sinyal_kaynak="SPY", ek_mal=2.0)
        ekle("ikincil_e", "2010-2026", "2010-02-11", "2026-11-20", "TQQQ", k, "rejim", sinyal_kaynak="SPY", ek_mal=2.0)
        ekle("ikincil_e", "2010-2026", "2010-02-11", "2026-11-20", "TQQQ", k, "rejim", sinyal_kaynak="QQQ", ek_mal=2.0)

    son = pd.DataFrame(satirlar)
    son.to_csv(os.path.join(CIKTI, "ek1_sonuc.csv"), index=False, float_format="%.4f")
    ISL = pd.concat(tum_isl, ignore_index=True)
    ISL.to_csv(os.path.join(CIKTI, "ek1_islemler.csv"), index=False)

    # --- 5d. bolum tablosu (1993-2026)
    bt = []
    bg = g[g["bolum_gun"] > 0].groupby("bolum_gun")
    meta = pd.DataFrame({"vix30_ilk": bg["vix"].apply(lambda s: s.index.min()), "vix30_son": bg["vix"].apply(lambda s: s.index.max()),
                         "vix30_gun": bg.size(), "vix_en_yuksek": bg["vix"].max()})
    rg = pd.DataFrame({"b": g["bolum"], "f": fwd["SPY"], "rj": g["rejim"]})
    rg = rg[rg["rj"] & rg["f"].notna()].groupby("b")["f"]
    meta["rejim_gun"] = rg.size()
    meta["rejim_kosulsuz_toplam_bps"] = rg.sum() * BPS
    for hd in ("SPY", "QQQ", "DIA", "MDY"):
        for k in KUR:
            d = kur(hd, k, "rejim")
            d["net"] = d["brut"] - maliyet(pd.DatetimeIndex(d["t"])).to_numpy()
            for bno, x in d.groupby("bolum"):
                en, c = ardisik_kayip(x["net"].to_numpy())
                _, c2 = ardisik_kayip(x["net"].to_numpy(), en_buyuk=True)
                bt.append(dict(hedef=hd, kural=k, bolum=int(bno), ilk_islem=x["t"].min().date(), son_islem=x["t"].max().date(),
                               n=len(x), toplam_net_bps=x["net"].sum() * BPS, ort_net_bps=x["net"].mean() * BPS,
                               en_kotu_bps=x["net"].min() * BPS, en_iyi_bps=x["net"].max() * BPS,
                               isabet=float((x["net"] > 0).mean()), en_uzun_ardisik_kayip=en, ardisik_kayip_bps=c * BPS,
                               en_buyuk_ardisik_kayip_bps=c2 * BPS))
    BT = pd.DataFrame(bt).merge(meta.reset_index().rename(columns={"bolum_gun": "bolum"}), on="bolum", how="left")
    for c_ in ("vix30_ilk", "vix30_son"):
        BT[c_] = pd.to_datetime(BT[c_]).dt.strftime("%Y-%m-%d")
    sonb = meta.iloc[-1]
    notlar.append(f"son VIX>30 bolumu: no {int(meta.index[-1])}, {sonb['vix30_ilk'].date()} -> {sonb['vix30_son'].date()}, "
                  f"{int(sonb['vix30_gun'])} gun; bu bolumde rejim gunu (ileri getirisi bilinen): {sonb['rejim_gun']}")
    fark = {}
    for k in KUR:
        x, y = birincil[k], capraz[k]
        fark[k] = round((y["net_bps"] - x["net_bps"]) / math.hypot(x["se_net_bps"], y["se_net_bps"]), 2)
    notlar.append(f"2005-2026 ile 1993-2004 net ortalama farkinin t'si (Welch, betimsel): {fark}")
    BT.to_csv(os.path.join(CIKTI, "ek1_bolumler.csv"), index=False, float_format="%.2f")

    # --- ileriye bakma testi: veriyi kesim gununde kesince o gune kadarki sinyaller degismemeli
    bakis = []
    for kesim in ("1998-10-30", "2002-07-31", "2015-08-31"):
        kk = pd.Timestamp(kesim)
        s2, v2 = spy[spy.index <= kk], vix[vix.index <= kk]
        g2 = hazirla(s2, v2)
        r2, _, _ = rsi2(s2["adj"] / s2["adj"].iloc[-1] * spy["adj"].loc[s2.index[-1]])
        for k, sk in (("E1-a", r2 < 10), ("E1-b", ibs(s2) < 0.2)):
            eski = (sig["SPY"][k] & g["rejim"]).reindex(s2.index)
            yeni = sk & g2["rejim"]
            bakis.append((kesim, k, int((eski != yeni).sum()), bool((g2["bolum"] == g["bolum"].reindex(s2.index)).all())))
    notlar.append("ileriye bakma testi (kesim, kural, farkli sinyal gunu, bolum ayni): " + str(bakis))

    # --- 5g. bugun
    c0, h0, l0 = spy["close"].iloc[-1], spy["high"].iloc[-1], spy["low"].iloc[-1]
    r_, ag, al = rsi2(spy["adj"])
    olc = spy["close"].iloc[-1] / spy["adj"].iloc[-1]
    esik_rsi = (spy["adj"].iloc[-1] + max(al.iloc[-1] / 9.0 - ag.iloc[-1], -1e9)) * olc if al.iloc[-1] / 9.0 - ag.iloc[-1] > 0 else None
    seri = 0
    rr = spy["adj"].pct_change().to_numpy()
    for x in rr[::-1]:
        if x < 0:
            seri += 1
        else:
            break
    bugun = {"tarih": str(tak[-1].date()), "spy_kapanis": c0, "spy_yuksek": h0, "spy_dusuk": l0,
             "ma200_t": g["ma200"].iloc[-1], "ma200_fark_pct": (c0 / g["ma200"].iloc[-1] - 1) * 100,
             "vix_t": g["vix"].iloc[-1], "vix_t_1": g["vix_1"].iloc[-1],
             "rsi2_t": r_.iloc[-1], "ibs_t": ibs(spy).iloc[-1], "rejim_t(20 Kasim)": bool(g["rejim"].iloc[-1]),
             "E1-a_sinyal_t": bool(g["rejim"].iloc[-1] and r_.iloc[-1] < 10),
             "E1-b_sinyal_t": bool(g["rejim"].iloc[-1] and ibs(spy).iloc[-1] < 0.2),
             "dusus_serisi_gun": seri, "sigma20_bps(21 Kasim itibariyla)": spy["adj"].pct_change().iloc[-20:].std() * BPS,
             "rejim_23Kasim_VIX(t-1)>30": bool(g["vix"].iloc[-1] > 30),
             "rejim_23Kasim_SPY(t-1)<ma200": bool(c0 < g["ma200"].iloc[-1]),
             "E1-a_tetik_23Kasim: SPY kapanis <": esik_rsi if esik_rsi else "yalniz dusus kapanisinda",
             "E1-a_tetik_getiri_pct": (esik_rsi / c0 - 1) * 100 if esik_rsi else np.nan,
             "E1-b_tetik_23Kasim": "kapanis < dusuk + 0,2*(yuksek - dusuk) (gunun araliginin alt beste biri)",
             "E1-b_ornek_esik(20 Kasim araligi ile)": l0 + 0.2 * (h0 - l0)}
    pd.DataFrame({"alan": list(bugun.keys()), "deger": list(bugun.values())}).to_csv(os.path.join(CIKTI, "ek1_bugun.csv"), index=False)

    # ------------------------------------------------------------------ cikti (stdout)
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", 60); pd.set_option("display.max_rows", 400)
    print("== NOTLAR"); [print("  ", x) for x in notlar]
    print("\n== REJIM GUN SAYISI:", {on: int(kes(g["rejim"], *ORNEK[on]).sum()) for on in ORNEK},
          "| VIX(t-1)>30 gun:", {on: int((kes(g["vix_1"], *ORNEK[on]) > 30).sum()) for on in ORNEK})
    sut = ["tur", "ornek", "kural", "hedef", "sinyal_kaynagi", "h", "giris", "cikis", "rejim", "n", "brut_bps", "net_bps", "net2x_bps",
           "t_net", "t_olcekli", "taban_bps", "anormal_net_bps", "t_anormal_tarih", "t_anormal_bolum", "isabet", "medyan_bps",
           "en_kotu_bps", "en_iyi_bps", "en_iyi5pct_haric_net_bps", "en_uzun_ardisik_kayip", "ardisik_kayip_bps",
           "en_buyuk_ardisik_kayip_adet", "en_buyuk_ardisik_kayip_bps", "se_net_bps", "bolum_sayisi",
           "bolum_pozitif_orani", "en_buyuk_bolum", "en_buyuk_bolum_n", "en_buyuk_haric_net_bps", "en_kazancli_haric_net_bps",
           "o_i", "o_ii", "o_iii", "o_iv", "o_v", "o_vi", "sinif"]
    for tur in ("birincil", "capraz", "capraz_alt", "ek"):
        print(f"\n== {tur.upper()}")
        print(son[son.tur == tur][sut[1:3] + sut[9:]].round(2).T.to_string())
    kisa = ["ornek", "kural", "hedef", "sinyal_kaynagi", "h", "giris", "cikis", "rejim", "n", "brut_bps", "net_bps", "t_net", "t_olcekli",
            "anormal_net_bps", "t_anormal_tarih", "isabet", "en_kotu_bps", "en_uzun_ardisik_kayip", "ardisik_kayip_bps", "en_buyuk_ardisik_kayip_bps",
            "bolum_sayisi", "bolum_pozitif_orani"]
    for tur in ("ikincil_a", "ikincil_b", "ikincil_c", "ikincil_e"):
        print(f"\n== {tur.upper()}")
        print(son[son.tur == tur][kisa].round(2).to_string(index=False))
    print("\n== BOLUM TABLOSU (SPY)")
    print(BT[BT.hedef == "SPY"].drop(columns=["hedef", "en_iyi_bps"]).round(1).to_string(index=False))
    print("\n== BOLUM TABLOSU (QQQ, 2000-2002)")
    q = BT[(BT.hedef == "QQQ") & (BT.ilk_islem.astype(str) >= "2000-01-01") & (BT.ilk_islem.astype(str) <= "2002-12-31")]
    print(q.drop(columns=["hedef", "en_iyi_bps"]).round(1).to_string(index=False))
    print("\n== 1993-2004 ISLEMLER (SPY, h=1)")
    print(ISL[(ISL.tur == "birincil")][["kural", "tarih", "brut_bps", "net_bps", "vix_1", "bolum"]].to_string(index=False))
    print("\n== EKIM-KASIM 2026: rejim ici E1 islemleri")
    print(ISL[(ISL.tur == "capraz") & (ISL.tarih >= "2026-09-15")][["kural", "tarih", "brut_bps", "net_bps", "vix_1", "bolum"]].to_string(index=False))
    print("\n== EKIM-KASIM 2026: rejimden bagimsiz RSI(2)<10 / IBS<0,2 gunleri (betimsel)")
    x = pd.DataFrame({"kapanis": spy["close"], "rsi2": r_, "ibs": ibs(spy), "vix_1": g["vix_1"], "alt_1": g["alt_1"], "rejim": g["rejim"],
                      "ileri1_bps": fwd["SPY"] * BPS})
    x = x[(x.index >= "2026-09-15")]
    print(x[(x.rsi2 < 10) | (x.ibs < 0.2) | (x.vix_1 > 30)].round(2).to_string())
    print("\n== KALDIRACLI: en kotu 5 islem")
    for hd in ("UPRO", "TQQQ"):
        for k in KUR:
            y = ISL[(ISL.tur == "ikincil_e") & (ISL.hedef == hd) & (ISL.kural == k)].drop_duplicates(["tarih"]).nsmallest(5, "net_bps")
            print(hd, k, [(a_, round(b_)) for a_, b_ in zip(y.tarih, y.net_bps)])
    print("\n== BUGUN")
    for k_, v_ in bugun.items():
        print(f"   {k_}: {v_}")
    print("\n== KARAR")
    for k in KUR:
        r = birincil[k]
        print(k, r.get("sinif"), {x: r.get(x) for x in ("o_i", "o_ii", "o_iii", "o_iv", "o_v", "o_vi")})


if __name__ == "__main__":
    main()
