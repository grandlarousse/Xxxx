#!/usr/bin/env python3
"""TUPRS <- ABD rafineri sepeti: günlük sinyal betiği (rehber_tuprs).
Gereken: python3 + pandas + numpy + requests. Veri: Yahoo Finance (query1.finance.yahoo.com/v8/finance/chart),
isteğe bağlı VİOP günlük bülteni (borsaistanbul.com/data/vadeli/viop_YYYYMMDD.csv) -> ön vade kontrat ve uzlaşma fiyatı.

KURAL (araştırma c1_ref.py ile birebir):
  r_i  = ln(adj_t/adj_t-1)  (VLO, MPC, PSX, PBF; ABD günü)
  β_i  = 250 ABD günlük cov(r_i, r_SPX)/var(r_SPX), en az 100 gözlem, BİR GÜN ÖNCESİNE KADAR (shift 1)
  artık_i = r_i − β_i·r_SPX ;  P = 4 artığın ortalaması (en az 3 üye)
  BIST günü t'ye ABD günleri 'after' kuralıyla eşlenir: t_önceki <= d < t (BIST tatilinde biriken ABD günleri toplanır;
  t'den önceki ABD günü tatilse P = boş -> sinyal yok)
  z_t = P_t / std(P, önceki 250 BIST günü, en az 100)
  |z_t| > 1 ve pozisyon yok -> yön(z_t) ile TUPRS vadelisini t uzlaşmasında aç; t+2 BIST günü uzlaşmasında kapat.
  Çıkış gününde |z|>1 aynı yön -> 2 gün uzat; ters yön -> çevir; aksi halde kapat.

Kullanım:
  python3 sinyal_tuprs.py                       # hedef seans otomatik (bugün 18:10 TSİ öncesi ise bugün)
  python3 sinyal_tuprs.py --sermaye 1000000 --risk 0.5
  python3 sinyal_tuprs.py --tarih 2026-11-05    # belirli BIST seansı için
  python3 sinyal_tuprs.py --viop 0              # VİOP bültenini indirme
Yatırım tavsiyesi değildir.
"""
import argparse, sys, time, math, io, csv
import numpy as np, pandas as pd, requests

MEM = ["VLO", "MPC", "PSX", "PBF"]
MKT = "^GSPC"
W_BETA, MIN_BETA, W_STD, MIN_STD, THR, H = 250, 100, 250, 100, 1.0, 2
CUTOFF_TSI = (18, 10)   # pay vadelisi seans sonu
# BIST/VİOP tam gün kapalı günler: 2021-01..2026-10 VİOP bülten takviminden (yarım günler işlem günüdür);
# 2027 satırı resmi tatil + dini bayram TAHMİNİDİR (köprü/uzatma kararları dahil değil) — Borsa İstanbul takviminden teyit edip güncelleyin.
BIST_TATIL = """
2021-01-01 2021-04-23 2021-05-13 2021-05-14 2021-05-19 2021-07-15 2021-07-20 2021-07-21 2021-07-22 2021-07-23 2021-08-30 2021-10-29
2022-05-02 2022-05-03 2022-05-04 2022-05-19 2022-07-11 2022-07-12 2022-07-15 2022-08-30
2023-04-21 2023-05-01 2023-05-19 2023-06-28 2023-06-29 2023-06-30 2023-08-30
2024-01-01 2024-04-10 2024-04-11 2024-04-12 2024-04-23 2024-05-01 2024-06-17 2024-06-18 2024-06-19 2024-07-15 2024-08-30 2024-10-29
2025-01-01 2025-03-31 2025-04-01 2025-04-23 2025-05-01 2025-05-19 2025-06-06 2025-06-09 2025-07-15 2025-10-29
2026-01-01 2026-03-20 2026-04-23 2026-05-01 2026-05-19 2026-05-27 2026-05-28 2026-05-29 2026-07-15 2026-10-29
2027-01-01 2027-03-09 2027-03-10 2027-03-11 2027-04-23 2027-05-17 2027-05-18 2027-05-19 2027-07-15 2027-08-30 2027-10-29
"""
TATIL = set(pd.to_datetime(BIST_TATIL.split()))
# NYSE tatilleri (yalnız 'ABD verisi gecikti mi?' uyarısı için; sinyal hesabı Yahoo'daki gerçek ABD günlerini kullanır)
NYSE_TATIL = set(pd.to_datetime("""2025-01-01 2025-01-09 2025-01-20 2025-02-17 2025-04-18 2025-05-26 2025-06-19 2025-07-04 2025-09-01 2025-11-27 2025-12-25
2026-01-01 2026-01-19 2026-02-16 2026-04-03 2026-05-25 2026-06-19 2026-07-03 2026-09-07 2026-11-26 2026-12-25
2027-01-01 2027-01-18 2027-02-15 2027-03-26 2027-05-31 2027-06-18 2027-07-05 2027-09-06 2027-11-25 2027-12-24""".split()))

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}

def yahoo_daily(sym, years=6, retries=4):
    """Yahoo günlük: index = borsa yerel tarihi, sütunlar c (kapanış), adj (temettü düzeltmeli), ts (UTC bar zamanı)."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}"
    params = {"period1": int(time.time()) - int(years * 365.25 * 86400), "period2": int(time.time()) + 86400,
              "interval": "1d", "includePrePost": "false", "events": "div,splits"}
    last = None
    for a in range(retries):
        try:
            r = requests.get(url, params=params, headers=UA, timeout=30)
            if r.status_code == 200:
                res = r.json()["chart"]["result"][0]
                q = res["indicators"]["quote"][0]
                adj = (res["indicators"].get("adjclose") or [{}])[0].get("adjclose") or q["close"]
                idx = pd.to_datetime(res["timestamp"], unit="s", utc=True)
                tz = res["meta"].get("exchangeTimezoneName") or "UTC"
                df = pd.DataFrame({"c": q["close"], "adj": adj, "ts": idx}, index=idx.tz_convert(tz).tz_localize(None).normalize())
                df = df.dropna(subset=["c"]); df = df[~df.index.duplicated(keep="last")].sort_index()
                df.attrs["tz"] = tz
                return df
            last = f"HTTP {r.status_code}"
        except Exception as e:
            last = repr(e)
        time.sleep(2 ** a)
    raise RuntimeError(f"Yahoo verisi alınamadı: {sym} ({last})")

def bist_takvim(bas, son):
    d = pd.bdate_range(bas, son)
    return pd.DatetimeIndex([x for x in d if x not in TATIL])

def is_bist_day(d):
    d = pd.Timestamp(d).normalize(); return d.weekday() < 5 and d not in TATIL

def next_bist(d):
    d = pd.Timestamp(d).normalize() + pd.Timedelta(days=1)
    while not is_bist_day(d): d += pd.Timedelta(days=1)
    return d

def prev_bist(d):
    d = pd.Timestamp(d).normalize() - pd.Timedelta(days=1)
    while not is_bist_day(d): d -= pd.Timedelta(days=1)
    return d

def us_complete(d, now_utc):
    """ABD günü d tamamlandı mı (16:00 New York + 20 dk)?"""
    t = pd.Timestamp(d.year, d.month, d.day, 16, 20).tz_localize("America/New_York")
    return now_utc >= t.tz_convert("UTC")

def roll_beta(y, x, w=W_BETA, minp=MIN_BETA, shift=1):
    m = y.notna() & x.notna(); yy = y.where(m); xx = x.where(m)
    cov = (yy * xx).rolling(w, min_periods=minp).mean() - yy.rolling(w, min_periods=minp).mean() * xx.rolling(w, min_periods=minp).mean()
    var = (xx * xx).rolling(w, min_periods=minp).mean() - xx.rolling(w, min_periods=minp).mean() ** 2
    return (cov / var).shift(shift)

def to_bist_after(s, cal):
    """ABD günü d -> d'den SONRAKİ ilk BIST günü (t_önceki <= d < t). Takvim başlangıcından önceki günler atılır."""
    s = s.dropna(); s = s[s.index >= cal[0]]
    k = np.searchsorted(cal.values, s.index.values, side="right"); ok = k < len(cal)
    out = pd.Series(s.values[ok], index=cal[k[ok]])
    return out.groupby(level=0).sum().reindex(cal)

def compute(data, target, now_utc, include_partial=False):
    """data: {sym: DataFrame(adj, ...)} ; target: BIST seans tarihi. Dönüş: sözlük (z serisi, ayrıntılar)."""
    rm_all = np.log(data[MKT]["adj"]).diff()
    used_us = {}
    RS, B, R, BN = {}, {}, {}, {}
    for m in MEM:
        px = data[m]["adj"].where(data[m]["adj"] > 0)
        r = np.log(px).diff(); rm = rm_all.reindex(r.index)
        b = roll_beta(r, rm); RS[m] = r - b * rm; B[m] = b; R[m] = r
        # DENETİM: bir sonraki ABD gününün betası = yalnız TAMAMLANMIŞ ABD günlerini içeren son 250 günlük pencere (shift yok)
        ok = pd.Series([us_complete(d, now_utc) for d in r.index], index=r.index)
        BN[m] = float(roll_beta(r[ok], rm[ok], shift=0).iloc[-1])
    df = pd.DataFrame(RS)
    P = df.mean(axis=1).where(df.notna().sum(axis=1) >= 3)
    # yalnız tamamlanmış ABD günleri (geçici mod hariç)
    comp = pd.Series([us_complete(d, now_utc) for d in P.index], index=P.index)
    Pc = P[comp] if not include_partial else P
    cal = bist_takvim(target - pd.Timedelta(days=int(365.25 * 4.5)), target)
    Pb = to_bist_after(Pc[Pc.index < target], cal)
    sd = Pb.rolling(W_STD, min_periods=MIN_STD).std().shift(1)
    z = Pb / sd
    sd_next = Pb.rolling(W_STD, min_periods=MIN_STD).std().iloc[-1]   # bir sonraki seansın paydası (bugünkü P dahil)
    tprev = cal[-2]
    days = [d for d in Pc.index if tprev <= d < target]
    return dict(z=z, Pb=Pb, sd=sd, sd_next=sd_next, cal=cal, tprev=tprev, us_days=days, df=df, B=B, R=R, P=P, comp=comp, BN=BN)

def state_machine(z, thr=THR, h=H):
    """Kuralın pozisyon durumu (kural geçmiş boyunca uygulanmış varsayımıyla). Dönüş: son durum ve olay listesi."""
    zz = z.values; idx = z.index; n = len(zz); ev = []; pos = 0; left = 0; ent = None
    for i in range(n):
        zi = zz[i]; sig = np.isfinite(zi) and abs(zi) > thr
        if pos != 0:
            left -= 1
            if left == 0:
                if sig and np.sign(zi) == pos: left = h; ev.append((idx[i], "UZAT", pos))
                elif sig: pos = int(np.sign(zi)); left = h; ent = idx[i]; ev.append((idx[i], "ÇEVİR", pos))
                else: ev.append((idx[i], "KAPAT", pos)); pos = 0
            continue
        if sig: pos = int(np.sign(zi)); left = h; ent = idx[i]; ev.append((idx[i], "AÇ", pos))
    return pos, left, ent, ev

def viop_bulten(d):
    url = f"https://www.borsaistanbul.com/data/vadeli/viop_{d:%Y%m%d}.csv"
    r = requests.get(url, headers=UA, timeout=30)
    if r.status_code != 200 or len(r.content) < 1000: return None
    txt = r.content.decode("windows-1254", errors="replace")
    rows = list(csv.reader(io.StringIO(txt), delimiter=";"))
    hdr = [h.strip() for h in rows[0]]; ix = {h: i for i, h in enumerate(hdr)}
    out = []
    for row in rows[2:]:
        if len(row) < 16: continue
        code = row[ix["SOZLESME KODU"]].strip()
        if code.startswith("F_TUPRS") and not code.endswith(("N1", "N2")) and len(code) == 11:
            f = lambda k: float(row[ix[k]].replace(",", ".")) if row[ix[k]].strip() else float("nan")
            out.append(dict(kod=code, vade=pd.Timestamp(row[ix["VADE TARIHI"]].strip()), uzlasma=f("UZLASMA FIYATI"),
                            kapanis=f("KAPANIS FIYATI"), hacim_tl=f("ISLEM HACMI"), ap=f("ACIK POZISYON")))
    return pd.DataFrame(out).sort_values("vade") if out else None

def fmt(x, n=2):
    return "boş" if x is None or not np.isfinite(x) else f"{x:,.{n}f}".replace(",", "X").replace(".", ",").replace("X", ".")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tarih", help="hedef BIST seansı YYYY-AA-GG (varsayılan: otomatik)")
    ap.add_argument("--sermaye", type=float, default=1_000_000)
    ap.add_argument("--risk", type=float, default=0.5, help="işlem başı risk, sermayenin yüzdesi (0,5–1 önerilir)")
    ap.add_argument("--viop", type=int, default=1)
    a = ap.parse_args()
    now_utc = pd.Timestamp.now(tz="UTC"); now_tsi = now_utc.tz_convert("Europe/Istanbul")
    today = pd.Timestamp(now_tsi.date())
    if a.tarih: target = pd.Timestamp(a.tarih)
    elif is_bist_day(today) and (now_tsi.hour, now_tsi.minute) < CUTOFF_TSI: target = today
    else: target = next_bist(today)
    if not is_bist_day(target): print(f"UYARI: {target.date()} BIST takviminde işlem günü değil (tatil listesi betiğin başında).")
    print("=" * 78); print(f"TUPRS <- ABD rafineri sepeti | çalışma: {now_tsi:%d.%m.%Y %H:%M} TSİ | hedef BIST seansı: {target:%d.%m.%Y}"); print("=" * 78)
    data = {}
    for s in MEM + [MKT, "TUPRS.IS"]:
        data[s] = yahoo_daily(s); time.sleep(0.3)
    print("Kaynak: Yahoo Finance günlük (adj = temettü düzeltmeli kapanış). Son tarihler:")
    for s in MEM + [MKT, "TUPRS.IS"]:
        last = data[s].index[-1]; tag = ""
        if s != "TUPRS.IS" and not us_complete(last, now_utc): tag = "  (bu gün henüz KAPANMADI -> kullanılmaz)"
        if s == "TUPRS.IS" and last == today and (now_tsi.hour, now_tsi.minute) < CUTOFF_TSI: tag = "  (gün içi son fiyat; Yahoo gecikmeli olabilir — yalnız boyut hesabında)"
        print(f"   {s:9s} {last:%d.%m.%Y}  kapanış {fmt(data[s]['c'].iloc[-1])}{tag}")
    R = compute(data, target, now_utc)
    z = R["z"]; zt = z.iloc[-1]; Pt = R["Pb"].iloc[-1]; sdt = R["sd"].iloc[-1]
    # ABD verisi beklenen günü içeriyor mu?
    exp_us = target - pd.Timedelta(days=1)
    while exp_us.weekday() >= 5 or exp_us in NYSE_TATIL: exp_us -= pd.Timedelta(days=1)
    if exp_us >= R["tprev"] and exp_us not in R["us_days"]:
        print(f"\nUYARI: beklenen ABD günü {exp_us:%d.%m.%Y} veride yok ya da henüz kapanmadı. Sinyal KESİN DEĞİL.")
    print(f"\nEşleme: önceki BIST günü {R['tprev']:%d.%m.%Y} <= ABD günü < {target:%d.%m.%Y} -> kullanılan ABD günleri: "
          + (", ".join(f"{d:%d.%m.%Y}" for d in R["us_days"]) if R["us_days"] else "YOK (ABD tatili) -> sinyal yok"))
    for d in R["us_days"]:
        print(f"   {d:%d.%m.%Y}: " + " | ".join(f"{m} r {fmt(R['R'][m].get(d, np.nan) * 100)}% β {fmt(R['B'][m].get(d, np.nan))} artık {fmt(R['df'][m].get(d, np.nan) * 100)}%" for m in MEM)
              + f" | SPX {fmt(np.log(data[MKT]['adj']).diff().get(d, np.nan) * 100)}%")
    print(f"\nSepet artığı P = {fmt(Pt * 100 if np.isfinite(Pt) else np.nan, 3)}%   std250 = {fmt(sdt * 100, 3)}%   z = {fmt(zt)}")
    sig = np.isfinite(zt) and abs(zt) > THR
    print("SİNYAL: " + (("AL (uzun) TUPRS vadeli" if zt > 0 else "SAT (kısa) TUPRS vadeli") + f"  (|z| {fmt(abs(zt))} > {fmt(THR, 1)})" if sig else "YOK (|z| <= 1 ya da boş)"))
    pos, left, ent, ev = state_machine(z.iloc[:-1])
    print("\nKurala göre DÜNKÜ kapanış itibarıyla pozisyon (kural geçmişte aynen uygulandıysa; kendi gerçek pozisyonunuzu esas alın):")
    for d, e, p in ev[-4:]: print(f"   {d:%d.%m.%Y} {e:6s} {'UZUN' if p > 0 else 'KISA'}")
    if pos == 0:
        act = ("AÇ: " + ("UZUN" if zt > 0 else "KISA") + f" — {target:%d.%m.%Y} 18:00–18:10 arası (uzlaşma penceresi)") if sig else "İŞLEM YOK"
        print(f"   Pozisyon yok -> bugün: {act}")
    else:
        if left - 1 > 0: act = f"TUT (çıkış günü {left - 1} BIST günü sonra); yeni sinyale bakılmaz"
        elif sig and np.sign(zt) == pos: act = "UZAT (2 BIST günü daha; kontratın vadesine <3 iş günü kaldıysa sonraki vadeye roll)"
        elif sig: act = "ÇEVİR: mevcut pozisyonu kapat + ters yönde aç (uzlaşma penceresinde)"
        else: act = "KAPAT (18:00–18:10, uzlaşmaya yakın)"
        print(f"   Açık pozisyon: {'UZUN' if pos > 0 else 'KISA'} (giriş {ent:%d.%m.%Y}) -> bugün ({target:%d.%m.%Y}): {act}")
    # kontrat ve boyut
    px = float(data["TUPRS.IS"]["c"].iloc[-1]); src = "Yahoo spot TUPRS.IS son fiyat (vadeli bazı ~%1–3 farklı olabilir)"
    kont = None
    if a.viop:
        d = R["tprev"]
        try:
            vb = viop_bulten(d)
            if vb is not None:
                cal_f = bist_takvim(target, target + pd.Timedelta(days=120))
                vb["is_gunu_kalan"] = [int(((cal_f >= target) & (cal_f <= v)).sum()) - 1 for v in vb["vade"]]
                print(f"\nVİOP bülteni {d:%d.%m.%Y} (borsaistanbul.com) — TUPRS kontratları (iş günü kalan = hedef seanstan vadeye):")
                for _, r in vb.iterrows():
                    print(f"   {r['kod']}  vade {r['vade']:%d.%m.%Y}  kalan {r['is_gunu_kalan']:3d}  uzlaşma {fmt(r['uzlasma'])}  hacim {fmt(r['hacim_tl'] / 1e6, 0)} mn TL  AP {fmt(r['ap'], 0)}")
                ok = vb[vb["is_gunu_kalan"] >= 3]
                if len(ok): kont = ok.iloc[0]; px = float(kont["uzlasma"]); src = f"{kont['kod']} {d:%d.%m.%Y} uzlaşması"
        except Exception as e:
            print(f"\n(VİOP bülteni alınamadı: {e!r})")
    lr = np.log(data["TUPRS.IS"]["c"]).diff().dropna()
    sig_d = float(lr.iloc[-61:-1].std()) if len(lr) > 70 else 0.024
    L = max(1.65 * sig_d * math.sqrt(2), 0.04)
    kv = 100 * px; per = kv * L; nk = int(a.sermaye * a.risk / 100 // per)
    print(f"\nKONTRAT: {'işlem kontratı ' + kont['kod'] if kont is not None else 'vadeye >=3 BIST işlem günü kalan en yakın TUPRS vadelisi'} | fiyat {fmt(px)} TL ({src})")
    print(f"   1 kontrat = 100 pay = {fmt(kv, 0)} TL; teminat (~%15) ≈ {fmt(0.15 * kv, 0)} TL")
    print(f"   Risk ölçüsü: 2 günlük %95 kötü hareket ≈ 1,65·σ·√2 = {fmt(L * 100, 1)}% (σ 60g = {fmt(sig_d * 100, 2)}%, taban %4) -> kontrat başı {fmt(per, 0)} TL")
    print(f"   Sermaye {fmt(a.sermaye, 0)} TL, risk %{fmt(a.risk, 2)} -> {nk} kontrat (nominal {fmt(nk * kv, 0)} TL = sermayenin %{fmt(100 * nk * kv / a.sermaye, 1)}; teminat ≈ {fmt(0.15 * nk * kv, 0)} TL)")
    print("   Oran: tek bacak (yalnız TUPRS). İsteğe bağlı XU030 hedge'i araştırmada ana kural DEĞİL.")
    # bir sonraki seansın tetik seviyesi
    nxt = next_bist(target); sdn = R["sd_next"]
    bbar = np.nanmean([R["BN"][m] for m in MEM])   # DENETİM: sonraki ABD gününün betası (eskiden bir gün eski pencere)
    print(f"\nBİR SONRAKİ SEANS ({nxt:%d.%m.%Y}) için tetik: o güne eşlenecek ABD gün(ler)inin sepet artığı |P| > {fmt(sdn * 100, 2)}%")
    print(f"   (artık = ort(r_i) − ort(β_i·r_SPX); ort β ≈ {fmt(bbar)}). S&P 500 %0 ise: dört hissenin ortalama getirisi >= +{fmt(sdn * 100, 2)}% -> AL, <= −{fmt(sdn * 100, 2)}% -> SAT")
    print(f"   S&P 500 s% oynarsa eşik kayar: AL için ort(r_i) ≥ +{fmt(sdn * 100, 2)}% + ({fmt(bbar)})·s ; SAT için ort(r_i) ≤ −{fmt(sdn * 100, 2)}% + ({fmt(bbar)})·s")
    pos2, left2, ent2, _ = state_machine(z)
    if pos2 == 0: ctx = "pozisyon yok -> eşik aşılırsa o seansın uzlaşmasında AÇ (P>0 uzun, P<0 kısa)"
    elif left2 == 1: ctx = (f"{nxt:%d.%m.%Y} ÇIKIŞ GÜNÜ ({'UZUN' if pos2 > 0 else 'KISA'} pozisyon): eşik pozisyon yönünde aşılırsa UZAT, "
                            f"ters yönde aşılırsa ÇEVİR, aşılmazsa KAPAT")
    else: ctx = f"{nxt:%d.%m.%Y} pozisyon tutulur (giriş {ent2:%d.%m.%Y}); o gün yeni sinyale bakılmaz"
    print(f"   Kurala göre bağlam: {ctx}")
    for m in MEM:
        mk = np.array([us_complete(d, now_utc) for d in data[m].index])
        c0 = float(data[m]["c"][mk].iloc[-1])
        print(f"   {m}: son kapanış {fmt(c0)} -> (eşit hareket, SPX %0) AL ≥ {fmt(c0 * math.exp(sdn))}  SAT ≤ {fmt(c0 * math.exp(-sdn))}")
    # geçici (kapanmamış ABD günü) bilgi
    lastd = data[MKT].index[-1]
    if not us_complete(lastd, now_utc):
        Rp = compute(data, nxt, now_utc, include_partial=True)
        print(f"\nGEÇİCİ (ABD {lastd:%d.%m.%Y} henüz kapanmadı; yalnız bilgi): {nxt:%d.%m.%Y} için şu anki z ≈ {fmt(Rp['z'].iloc[-1])}")
    print("\nNot: sinyal yalnız ÖNCEKİ ABD kapanışlarını kullanır; BIST'in 17:45–17:55 fiyatı sinyale girmez. Emir fiyatını aracı kurum ekranından alın.")
    print("Yatırım tavsiyesi değildir.")

if __name__ == "__main__":
    main()
