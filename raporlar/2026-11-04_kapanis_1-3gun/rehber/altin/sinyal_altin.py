#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sinyal_altin.py — Strateji (C): TRALT <- ALTIN (2 gün tutulan, XU030 ile hedge'li VİOP pozisyonu)

KURAL (araştırma kuralının pratik hâli; ayrıntı REHBER_altin.md):
  g_t  = ln( ons altın fiyatı t günü 17:55 TSİ / ons altın fiyatı önceki BIST günü 17:55 TSİ )
  σ    = son 250 BIST gününün aynı türden günlük altın değişimlerinin standart sapması (bugün hariç)
  z_t  = g_t / σ
  |z|>1 ve açık pozisyon yoksa:  z>+1 -> TRALT vadeli AL + XU030 vadeli SAT ;  z<-1 -> TRALT SAT + XU030 AL
  Giriş: t günü 18:00–18:10 (uzlaşma penceresi). Çıkış: 2 BIST günü sonra 18:00–18:10.
  Oran : 1 XU030 kontratı başına N = round( 10*XU030 / (β * 100*TRALT) ) TRALT kontratı (β = 250g spot beta).

Veri: yalnız Yahoo Finance (query1.finance.yahoo.com/v8/finance/chart).
  - Altın: COMEX altın vadelisi. Yahoo'nun sürekli "GC=F" serisi vade geçişinde %0,5–2 sıçrar; bu yüzden
    bugünkü ve dünkü fiyat AYNI kontrattan (ör. GCZ26.CMX) alınır. σ için GC=F 60 dk barlarının 15:00 UTC (18:00 TSİ)
    anlık değişimleri kullanılır (backtest'teki "betik sigması" ile aynı).
  - BIST takvimi + beta: XU030.IS, TRALT.IS günlük.
  - ABD/BIST tatil hizalaması araştırma koduyla aynı: değişim her zaman "BIST günü t / önceki BIST günü" arasıdır;
    ABD tatilinde (COMEX kapalı) o günün fiyatı son bilinen fiyattır (değişim ~0 -> sinyal çıkmaz); BIST tatilinde
    değişim tatil boyunca birikir (VİOP uzlaşma/önceki uzlaşma mantığı).

Kullanım:
  python3 sinyal_altin.py                      # 1.000.000 TL sermaye, %0,75 risk
  python3 sinyal_altin.py --sermaye 2000000 --risk 0.5
  python3 sinyal_altin.py --f-tralt 34.94 --f-xu030 14412   # vadeli fiyatlarını elle ver (kontrat oranı için)
Gereksinim: python3, pandas, numpy, requests.  Yatırım tavsiyesi değildir.
"""
import argparse, sys, time, datetime as dt
import numpy as np, pandas as pd, requests

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}
URL = "https://query1.finance.yahoo.com/v8/finance/chart/{}"
MON = {"Jan": "F", "Feb": "G", "Mar": "H", "Apr": "J", "May": "K", "Jun": "M", "Jul": "N", "Aug": "Q", "Sep": "U", "Oct": "V", "Nov": "X", "Dec": "Z"}
SNAP_UTC = (14, 55)          # 17:55 TSİ (Türkiye UTC+3, yaz saati yok)
SIGMA_UTC = (15, 0)          # σ için 60 dk barlarla 18:00 TSİ
THR, H, WIN, MINP = 1.0, 2, 250, 100

def yahoo(sym, interval, rng=None, p1=None):
    params = {"interval": interval, "includePrePost": "false"}
    if rng: params["range"] = rng
    else: params.update(period1=p1 or 946684800, period2=int(time.time()) + 86400)
    for a in range(5):
        try:
            r = requests.get(URL.format(sym), params=params, headers=UA, timeout=30)
            if r.status_code == 200:
                j = r.json()["chart"]
                if j.get("result"):
                    res = j["result"][0]; ts = res.get("timestamp")
                    if not ts: return None, res.get("meta", {})
                    q = res["indicators"]["quote"][0]
                    adj = (res["indicators"].get("adjclose") or [{}])[0].get("adjclose")
                    df = pd.DataFrame({"o": q["open"], "h": q["high"], "l": q["low"], "c": q["close"], "v": q["volume"],
                                       "adj": adj if adj else q["close"]}, index=pd.to_datetime(ts, unit="s", utc=True))
                    return df.dropna(subset=["c"]), res["meta"]
            if r.status_code in (404,): return None, {}
        except Exception:
            pass
        time.sleep(1.5 * 2 ** a)
    return None, {}

def daily_bist(sym, years=3):
    df, meta = yahoo(sym, "1d", p1=int(time.time()) - years * 366 * 86400)
    if df is None: sys.exit(f"HATA: {sym} günlük verisi alınamadı")
    tz = meta.get("exchangeTimezoneName", "Europe/Istanbul")
    df.index = df.index.tz_convert(tz).tz_localize(None).normalize()
    df = df[~df.index.duplicated(keep="last")]
    stale = (df["v"].fillna(0) <= 0) & (df["h"] == df["l"])       # tatil/bayat satırlar (araştırma koduyla aynı süzgeç)
    return df[~stale], meta

def snap_series(bars, step_min, cal, hh, mm, max_age_h=96):
    """Her BIST günü için hh:mm UTC'de BİLİNEN son fiyat = bitişi (başlangıç+adım) <= hh:mm olan son barın kapanışı.
    Bayat (ABD tatili vb.) ise son bilinen fiyat kullanılır (max_age_h saate kadar) ve bayrağı döner."""
    s = pd.Series(bars["c"].values, index=(bars.index + pd.Timedelta(minutes=step_min)).tz_convert(None))
    s = s[s > 0].sort_index(); s = s[~s.index.duplicated(keep="last")]
    tg = pd.DatetimeIndex(cal) + pd.Timedelta(hours=hh, minutes=mm)
    pos = np.searchsorted(s.index.values, tg.values, side="right") - 1
    ok = pos >= 0; pc = np.clip(pos, 0, None)
    age = (tg.values - s.index.values[pc]) / np.timedelta64(1, "h")
    v = np.where(ok & (age <= max_age_h), s.values[pc], np.nan)
    out = pd.DataFrame({"px": v, "age_h": np.where(ok, age, np.nan)}, index=pd.DatetimeIndex(cal))
    out.loc[out.index < s.index[0].normalize() + pd.Timedelta(days=1), "px"] = np.nan
    return out

FIXED_HOL = {(1, 1), (4, 23), (5, 1), (5, 19), (7, 15), (8, 30), (10, 29)}   # sabit resmî tatiller (dini bayramlar DEĞİL)

def half_days(today):
    """Yarım gün (arife) tespiti: Yahoo XU030.IS 60 dk barlarında son barın başlangıcı <= 13:00 TSİ olan günler (bugün hariç).
    [DENETİM EKİ] Arife günü VİOP uzlaşması ~12:20–12:35 TSİ'de oluşur; ertesi günün g'si bu saatteki altına göre ölçülmeli."""
    h, _ = yahoo("XU030.IS", "60m", rng="730d")
    if h is None or not len(h): return set()
    loc = h.index.tz_convert("Europe/Istanbul")
    s = pd.Series(loc.hour + loc.minute / 60.0, index=loc.tz_localize(None).normalize())
    last = s.groupby(level=0).max()
    return set(d for d in last.index[last <= 13.0] if d < today)

def active_contract():
    _, meta = yahoo("GC=F", "1d", rng="5d")
    nm = (meta.get("shortName") or "")            # ör. "Gold Dec 26"
    p = nm.split()
    if len(p) >= 3 and p[-2] in MON:
        return f"GC{MON[p[-2]]}{p[-1]}.CMX", nm
    return None, nm

def fmt(x, n=2):
    if x is None or (isinstance(x, float) and not np.isfinite(x)): return "—"
    return f"{x:,.{n}f}".replace(",", "X").replace(".", ",").replace("X", ".")

def main():
    ap = argparse.ArgumentParser(description="TRALT <- altın günlük sinyal")
    ap.add_argument("--sermaye", type=float, default=1_000_000, help="TL (vars. 1.000.000)")
    ap.add_argument("--risk", type=float, default=0.75, help="işlem başı risk, sermayenin %%'si (1σ 2 günlük hedge'li hareket; vars. 0,75)")
    ap.add_argument("--f-tralt", type=float, default=None, help="TRALT ön vade vadeli fiyatı (yoksa Yahoo spot)")
    ap.add_argument("--f-xu030", type=float, default=None, help="XU030 ön vade vadeli fiyatı (yoksa Yahoo spot endeks)")
    ap.add_argument("--yarim-gun", default="", help="yarım gün (arife) tarihleri, virgülle (ör. 2027-03-08); geçmiştekiler Yahoo'dan otomatik bulunur")
    ap.add_argument("--tatil", action="store_true", help="bugün BIST tatili (dini bayram vb.); betik aksi hâlde hafta içi günü açık varsayar")
    a = ap.parse_args()
    now = pd.Timestamp.now(tz="UTC").tz_localize(None)
    print("=" * 78); print(f"TRALT <- ALTIN sinyali | çalışma zamanı {now:%Y-%m-%d %H:%M} UTC ({(now + pd.Timedelta(hours=3)):%H:%M} TSİ)"); print("=" * 78)
    # --- BIST takvimi ve beta
    x30, mx = daily_bist("XU030.IS"); tra, mt = daily_bist("TRALT.IS")
    # [DENETİM DÜZELTMESİ] Yahoo XU030.IS bazı BIST günlerini atlıyor (ör. her yıl 25 Aralık; 2020-12-25 ... 2025-12-25).
    # Takvim = XU030.IS ∪ TRALT.IS (2018-12+ VİOP takvimiyle birebir; yalnız Şubat 2023 deprem kapanışı farklı).
    cal = x30.index.union(tra.index)
    today = (now + pd.Timedelta(hours=3)).normalize()
    assumed_today = False
    if today not in cal and today.weekday() < 5 and (today.month, today.day) not in FIXED_HOL and not a.tatil:
        # [DENETİM DÜZELTMESİ] Seans öncesi (≈10:00 TSİ'den önce) Yahoo'da bugünün barı yoktur; eskiden betik "bugün işlem günü değil" diyordu.
        cal = cal.append(pd.DatetimeIndex([today])); assumed_today = True
    half = half_days(today) | set(pd.to_datetime([s for s in a.yarim_gun.split(",") if s.strip()]).normalize())
    rT = np.log(tra["adj"]).diff().reindex(cal); rX = np.log(x30["adj"]).diff().reindex(cal)
    m = rT.notna() & rX.notna()
    def rbeta(y, x):
        yy, xx = y.where(m), x.where(m)
        cov = (yy * xx).rolling(WIN, min_periods=MINP).mean() - yy.rolling(WIN, min_periods=MINP).mean() * xx.rolling(WIN, min_periods=MINP).mean()
        var = (xx * xx).rolling(WIN, min_periods=MINP).mean() - xx.rolling(WIN, min_periods=MINP).mean() ** 2
        return (cov / var).shift(1)
    beta = rbeta(rT, rX)
    # --- altın
    ac, acname = active_contract()
    g60, _ = yahoo("GC=F", "60m", rng="730d")
    if g60 is None: sys.exit("HATA: GC=F 60 dk verisi alınamadı")
    g60 = g60[(g60.index.second == 0) & (g60.index.minute == 0)]          # Yahoo'nun eklediği canlı satırı at
    src5 = ac
    b5, meta5 = (yahoo(ac, "5m", rng="60d") if ac else (None, {}))
    if b5 is None or len(b5) < 100:
        src5 = "GC=F"; b5, meta5 = yahoo("GC=F", "5m", rng="60d")
        print("UYARI: aktif kontrat 5 dk verisi yok -> GC=F kullanılıyor (vade geçiş günü sıçraması riski!)")
    live_px, live_t = meta5.get("regularMarketPrice"), meta5.get("regularMarketTime")
    live_t = pd.to_datetime(live_t, unit="s") if live_t else b5.index[-1].tz_convert(None)
    b5 = b5[(b5.index.second == 0) & (b5.index.minute % 5 == 0)]
    # σ: 60 dk 15:00 UTC anlık değişimleri (bugün hariç; son 250 BIST günü)
    s60 = snap_series(g60, 60, cal, *SIGMA_UTC, max_age_h=30)["px"]
    hl = [d for d in cal if d in half]
    if hl:   # [DENETİM DÜZELTMESİ] arife günü referansı 12:30 TSİ (09:30 UTC) — VİOP yarım gün uzlaşmasıyla aynı an
        s60.loc[hl] = snap_series(g60, 60, pd.DatetimeIndex(hl), 9, 30, max_age_h=30)["px"].values
    r60 = np.log(s60 / s60.shift(1))
    sig_ser = r60.rolling(WIN, min_periods=MINP).std().shift(1)
    # 17:55 anlık fiyatlar (aynı kontrat)
    sn = snap_series(b5, 5, cal, *SNAP_UTC)
    if hl:
        sh = snap_series(b5, 5, pd.DatetimeIndex(hl), 9, 30)
        sn.loc[hl, "px"] = sh["px"].values; sn.loc[hl, "age_h"] = sh["age_h"].values
    # bugün 17:55 öncesiyse: canlı fiyat
    is_bist_today = today in cal
    before = is_bist_today and (now < today + pd.Timedelta(hours=SNAP_UTC[0], minutes=SNAP_UTC[1]))
    if is_bist_today and before and live_px:
        sn.loc[today, "px"] = float(live_px); sn.loc[today, "age_h"] = (now - live_t) / pd.Timedelta(hours=1)
    g = np.log(sn["px"] / sn["px"].shift(1))
    sig = sig_ser.reindex(sn.index)
    z = g / sig
    # [DENETİM EKİ] 5 dk verisi yalnız ~60 gün: daha eski günler için 18:00 TSİ (60 dk) z'si -> pozisyon simülasyonu için uzun geçmiş
    z60 = (r60 / sig_ser).reindex(sn.index)
    z_hist = z.where(z.notna(), z60)
    # --- kaynak ve son tarih
    lag = (now - live_t) / pd.Timedelta(minutes=1)
    print(f"Kaynak: Yahoo Finance. Altın kontratı: {src5} ({acname}); 5 dk son bar {b5.index[-1].tz_convert(None):%Y-%m-%d %H:%M} UTC; "
          f"canlı fiyat {fmt(live_px,1)} @ {live_t:%Y-%m-%d %H:%M} UTC ({fmt(lag,0)} dk önce; Yahoo COMEX verisi ~10 dk gecikmeli olabilir)")
    print(f"        σ için GC=F 60 dk: {g60.index[0]:%Y-%m-%d} → {g60.index[-1]:%Y-%m-%d %H:%M} UTC; "
          f"XU030.IS son gün {x30.index[-1]:%Y-%m-%d}, TRALT.IS son gün {tra.index[-1]:%Y-%m-%d}")
    # --- son tamamlanmış BIST günü ve bugün
    done = [d for d in sn.index if d < today or (d == today and not before)]
    last_done = done[-1]
    def line(d, tag):
        px, ag = sn.loc[d, "px"], sn.loc[d, "age_h"]
        zz = z.loc[d]; sgn = "AL (TRALT long / XU030 short)" if zz > THR else ("SAT (TRALT short / XU030 long)" if zz < -THR else "sinyal yok")
        if d in half: sgn += " [ARİFE: yeni pozisyon AÇILMAZ]"
        prev = sn.index[sn.index.get_loc(d) - 1]
        st = " [BAYAT FİYAT: ABD tatili/ veri boşluğu]" if np.isfinite(ag) and ag > 1.5 else ""
        hh = "12:30" if d in half else "17:55"; hp = " 12:30" if prev in half else ""
        print(f"{tag} {d:%Y-%m-%d}: altın {hh} = {fmt(px,1)} (önceki BIST günü {prev:%Y-%m-%d}{hp}: {fmt(sn.loc[prev,'px'],1)}) | "
              f"g = {fmt(g.loc[d]*100,2)}% | σ = {fmt(sig.loc[d]*100,2)}% | z = {fmt(zz,2)} -> {sgn}{st}")
    print("-" * 78)
    if assumed_today:
        print(f"NOT: Yahoo'da bugünün ({today:%Y-%m-%d}) BIST barı henüz yok (seans öncesi?). Bugün BIST AÇIK varsayıldı; "
              "dini bayram/tatilse --tatil ile çalıştırın.")
    if half:
        print("Yarım günler (arife; referans 12:30 TSİ): " + ", ".join(f"{d:%Y-%m-%d}" for d in sorted(half) if d >= cal[-300]))
    for d in done[-4:-1]: line(d, "  geçmiş   ")
    line(last_done, "SON KAPANIŞ")
    if is_bist_today and before:
        line(today, "BUGÜN(GEÇİCİ, canlı fiyat)")
        print("            -> Kesin karar 17:55 TSİ fiyatıyla verilir; betiği 17:50–17:55 arasında yeniden çalıştırın.")
    elif is_bist_today and not before:
        ag = sn.loc[today, "age_h"]
        if np.isfinite(ag) and ag > 0.09:
            print(f"UYARI: bugünkü 17:55 barı Yahoo'da henüz yok; kullanılan fiyat {fmt(ag*60,0)} dk eski. TVC:GOLD ile elle teyit edin.")
    elif not is_bist_today:
        print(f"Bugün ({today:%Y-%m-%d}) BIST işlem günü değil.")
    if today in half:
        print("BUGÜN YARIM GÜN (arife): yeni pozisyon AÇILMAZ. Bugün çıkış günüyse yarım gün kapanışındaki uzlaşma penceresinde "
              "(≈12:20–12:35 TSİ; saati aracı kurumdan teyit edin) kapatın.")
    # --- kural gereği açık pozisyon (son 120 BIST günü, örtüşmesiz simülasyon; 5 dk z yoksa 18:00 z'si)
    zz = z_hist.dropna(); zz = zz[zz.index <= last_done]
    idx = list(zz.index[-120:]); i = 0; pos = None; hist = []
    while i < len(idx):
        d = idx[i]
        if abs(zz.loc[d]) > THR and d not in half:
            j = i + H; ex = idx[j] if j < len(idx) else None
            hist.append((d, np.sign(zz.loc[d]), ex)); i = j if ex is not None else len(idx)
        else: i += 1
    print("-" * 78)
    calf = list(cal) + [d for d in pd.bdate_range(cal[-1] + pd.Timedelta(days=1), periods=5)]
    if hist:
        d, s, ex = hist[-1]
        if ex is None:
            k = calf.index(d) + H; exd = calf[k] if k < len(calf) else None
            print(f"AÇIK POZİSYON (kurala göre): {'LONG TRALT/SHORT XU030' if s>0 else 'SHORT TRALT/LONG XU030'} giriş {d:%Y-%m-%d} uzlaşma, "
                  f"çıkış {exd:%Y-%m-%d} 18:00–18:10 (takvim tahmini; BIST tatilini kontrol edin)")
        else:
            print(f"Açık pozisyon yok. Son işlem: {'LONG' if s>0 else 'SHORT'} TRALT, giriş {d:%Y-%m-%d}, çıkış {ex:%Y-%m-%d}.")
        print("Son işlemler: " + "; ".join(f"{a:%m-%d}{'+' if b>0 else '-'}→{(c.strftime('%m-%d') if c is not None else 'açık')}" for a, b, c in hist[-6:]))
    else:
        print("Son 40 günde kural sinyali yok; açık pozisyon yok.")
    # --- tetik seviyeleri
    print("-" * 78)
    sig_now = r60.rolling(WIN, min_periods=MINP).std().dropna().iloc[-1]
    if is_bist_today:
        prv = sn.index[sn.index.get_loc(today) - 1]; p0 = sn.loc[prv, "px"]; s0 = sig.loc[today]
        print(f"BUGÜN ({today:%Y-%m-%d}) 17:55 TETİĞİ: referans {prv:%Y-%m-%d} 17:55 = {fmt(p0,1)}, σ = {fmt(s0*100,2)}% -> "
              f"altın >= {fmt(p0*np.exp(THR*s0),1)} AL ; <= {fmt(p0*np.exp(-THR*s0),1)} SAT")
        ref_px, lab = sn.loc[today, "px"], ("bugünkü canlı fiyat (17:55'te güncelleyin)" if before else "bugünün 17:55 fiyatı")
    else:
        ref_px, lab = sn.loc[last_done, "px"], f"{last_done:%Y-%m-%d} 17:55 fiyatı"
    print(f"BİR SONRAKİ BIST GÜNÜ İÇİN YAKLAŞIK TETİK (referans = {lab} {fmt(ref_px,1)}, σ ≈ {fmt(sig_now*100,2)}%): "
          f"17:55'te altın >= {fmt(ref_px*np.exp(THR*sig_now),1)} -> AL ; <= {fmt(ref_px*np.exp(-THR*sig_now),1)} -> SAT")
    print("   Not: TVC:GOLD / OANDA:XAUUSD spot fiyatı COMEX vadelisinden ~%0,3–1 düşüktür; SEVİYE değil YÜZDE değişimi karşılaştırın:"
          f" eşik ±{fmt(THR*sig_now*100,2)}%.")
    # --- kontrat oranı ve büyüklük
    b = float(beta.dropna().iloc[-1])
    pT = a.f_tralt or float(tra["c"].iloc[-1]); pX = a.f_xu030 or float(x30["c"].iloc[-1])
    nT_c, nX_c = 100 * pT, 10 * pX
    N = max(1, int(round(nX_c / (b * nT_c))))
    hr = (rT - beta * rX); hr = hr[hr.index <= last_done]; sd2 = hr.rolling(2).sum().iloc[-WIN:].std()   # [DENETİM] bugünün yarım barı hariç
    unit_not = N * nT_c; unit_risk = sd2 * unit_not
    units = int(np.floor(a.sermaye * a.risk / 100 / unit_risk)) if unit_risk > 0 else 0
    marj = 0.15 * unit_not + 0.11 * nX_c
    # ön vade: vadeye >= 3 BIST iş günü kalan en yakın ay (VİOP vadesi = ayın son iş günü)
    ref = today if is_bist_today else last_done + pd.offsets.BDay(1)
    y_, m_ = ref.year, ref.month
    def last_bday(y, mth): return pd.bdate_range(pd.Timestamp(y, mth, 1), pd.Timestamp(y, mth, 1) + pd.offsets.MonthEnd(0))[-1]
    left = len(pd.bdate_range(ref, last_bday(y_, m_))) - 1
    if left < 3: y_, m_ = (y_ + (m_ == 12), m_ % 12 + 1)
    mc = "FGHJKMNQUVXZ"[m_ - 1]
    yx, mx_ = (y_, m_) if m_ % 2 == 0 else (y_ + (m_ == 12), m_ % 12 + 1)     # XU030 vadelisi yalnız çift aylarda (Şub/Nis/.../Ara)
    mcx = "FGHJKMNQUVXZ"[mx_ - 1]
    print("-" * 78)
    print(f"KULLANILACAK KONTRATLAR (vadeye >= 3 iş günü): VİOP F_TRALT{m_:02d}{y_%100:02d} ve F_XU030{mx_:02d}{yx%100:02d} "
          f"(TradingView: BIST:TRALT{mc}{y_}, BIST:XU030D{mcx}{yx}); bu ay kalan iş günü (tatiller hariç değil) = {left}")
    print(f"KONTRAT ORANI: β(TRALT,XU030; 250g spot) = {fmt(b,3)} | fiyatlar TRALT {fmt(pT,2)}, XU030 {fmt(pX,0)} "
          f"({'elle' if a.f_tralt or a.f_xu030 else 'Yahoo spot; vadeli fiyatı ~%1–5 farklı'})")
    print(f"   1 BİRİM = 1 XU030D kontratı ({fmt(nX_c,0)} TL) + {N} TRALT kontratı ({fmt(unit_not,0)} TL); β_etkin = {fmt(nX_c/unit_not,3)}")
    print(f"   1 birimin 1σ 2 günlük hedge'li riski ≈ {fmt(sd2*100,2)}% × {fmt(unit_not,0)} = {fmt(unit_risk,0)} TL; teminat ≈ {fmt(marj,0)} TL (%15/%11 varsayımı)")
    print(f"   Sermaye {fmt(a.sermaye,0)} TL, risk %{fmt(a.risk,2)} -> {units} birim = {units} XU030 + {units*N} TRALT kontratı"
          + ("  (UYARI: 1 birim bile risk bütçesini aşıyor; işlem yapmayın ya da riski yükseltin)" if units == 0 else ""))
    if is_bist_today and today not in half and np.isfinite(z.loc[today]) and abs(z.loc[today]) > THR:
        d_ = "TRALT AL / XU030 SAT" if z.loc[today] > 0 else "TRALT SAT / XU030 AL"
        print(f"BUGÜNKÜ EMİR{' (GEÇİCİ — 17:50–17:55 fiyatıyla teyit edin)' if before else ''}: {d_}: {max(units,0)*N} TRALT + {max(units,0)} XU030D, 18:00–18:10 arasında"
              " (açık pozisyon yoksa; aynı yönde açık pozisyon bugün kapanacaksa KAPATMAYIN, 2 gün daha taşıyın).")
    print("=" * 78)

if __name__ == "__main__":
    main()
