"""sade_backtest.py — Görev B: kademeli kuralların ELLE UYGULANABİLİR SADE sürümleri, asıl (hakem) sürümle karşılaştırma.

Çalıştırma:  python3 -W ignore sade_backtest.py      (~1-2 dk, n_jobs=1, ağ gerekmez)
Girdi : panel/panel_viop.parquet, panel_spot.parquet, panel_etf.parquet, panel/duka/XAUUSD.parquet (+ duka_min_XAUUSD.parquet yaması),
        out/sentez/{sinyal_*_ham, poz_*, pnl_*}.parquet (yalnız ASIL'ın birebir tuttuğunu göstermek için), esikler.json
Çıktı : out/rehber/sade_sonuc.csv     (uzun biçim: kural × sürüm × dönem; bütün ölçüler)
        out/rehber/sade_ozet.csv      (geniş biçim: kural × sürüm, ana ölçüler + karar)
        out/rehber/sade_asil_kontrol.csv (ASIL yeniden kurulumu ↔ hakem parquet'leri, maks |Δ|)
        out/rehber/sade_esikler.json  (sade kuralların elle kullanılacak sayıları: LOWMOM HV eşiği, aylık betalar)

Tanımlar (hakem sentezi, sl.py / s03_dogrula.py ve sinyal_altin.py ile aynı):
  VİOP : giriş t uzlaşması, getiri v_ret (aktif kontrat, log) → basit getiri (e^r−1), maliyet 5 bps gidiş-dönüş (stres 10), |Δpoz|·maliyet/2 ertesi gün.
  ETF  : giriş t ABD kapanışı, getiri adjclose log farkı → basit, maliyet 10 bps (stres 20), yalnız uzun.
  Kademeli (ASIL)  : etkin_t = (s_t + s_t-1 + … + s_t-h+1)/h.
  TAM-TUT (b)      : etkin_t = son h gün içindeki EN SON sıfırdan farklı sinyalin işareti (tam kol); yoksa 0. Yeni sinyal süreyi yeniden başlatır,
                     ters sinyal pozisyonu çevirir (VİOP).
  ÇOĞUNLUK (c)     : etkin_t = sign(s_t + … + s_t-h+1) (tam kol). Not: tanım gereği sign(ASIL etkin) ile aynı işarettedir.
  SAYIM            : etkin_t = (son h günün UZUN sayısı − KISA sayısı)/h — ASIL kademeli pozisyonun dilim defteri tutmadan elle yazılışı (birebir aynı).
  GÜÇLÜ (1 kontrat): round(ASIL etkin): son h sinyalin net toplamı |Σ| ≥ h/2 ise tam birim (1 kontratlık yatırımcının yapabileceği yuvarlama).
  SABİT-BETA (d)   : artık, ay başında güncellenen sabit beta ve TradingView'dan okunabilen basit % değişimlerle (log değil).
                     A4: VİOP-satır hizası (hakem tanımı: son ABD kapanışının bir önceki VİOP gününde bilinen kapanışa göre % değişimi;
                         bayram dönüşünde toplam değişim, ABD tatili ertesi sinyal yok); β 60, σ 120 satır; eşik ±0,43σ ayda bir.
                         TANI satırı: her zaman son ABD günlük mumu (ABD takvimi) — bozulmanın kaynağını gösterir.
                     E2: k günlük % değişim C_t-1/C_t-1-k − 1 (GDX/GDXJ, GLD, SPY); β (GLD, SPY) 250 seans OLS, ay başında.
                     (YILLIK) Ocak'ta bir kez; (DONUK-IS) IS döneminde bir kez kestirilip hiç güncellenmez (bakım yapılmazsa ne olur?).
  LOWMOM sade      : HV20-OANDA-*   : OANDA:XAUUSD günlük (kapanış 17:00 NY);  HV20-VIOPUZL-* : BIST aktif vade kodu, 'uzlaşmayı kapanış say'
                     (≈15:10 UTC); CANLI = 18:00 TSİ canlı mumla, KAPANIS = dünkü tamamlanmış mumlarla; YILLIK/SABIT eşik.
                     TANI-15UTC-*   : asıl 15:00 UTC serisinde TV formülü (elle okunamaz; eşik mekaniğinin zararsız olduğunu gösterir).
Karar kuralı (sonuçlardan önce yazıldı, asıl sürüme göre): YAKIN = tam ve OOS Sharpe farkı ≥ −0,15 ve OOS alfa t farkı ≥ −0,5;
  BELİRGİN KÖTÜ = tam ya da OOS Sharpe farkı < −0,25 ya da OOS alfa t farkı < −1; arası KABUL EDİLEBİLİR.
VİOP birleşik: SADE-TAMTUT ve SADE-COGUNLUK önceden tanımlıdır; ONERILEN-* tek tek sonuçlar görüldükten SONRA seçilmiştir (seçim yanlılığı).
  HV(20) (e)       : LOWMOM'da 15:00 UTC rv20 yüzdeliği yerine TradingView 'Historical Volatility' (20) göstergesi:
                     100·stdev_pop(ln(C/C[1]),20)·√365, C = OANDA:XAUUSD günlük kapanışı (17:00 New York) ≈ Dukascopy 17:00 ET.
Dönemler: tam, OOS (VİOP 2022+, ETF 2018+), 2022+, 2026 (Oca–6 Kas). Dönem ölçüleri tam örneklem P&L'inin dilimlenmesiyle (pozisyon dönem başında sıfırlanmaz).
Alfa: net P&L ~ sabit + aynı enstrümanın B&H basit getirisi, NW (HAC) gecikme 5; yıllık % = sabit·252·100.
DENETİM ekleri (2026-11-08, bağımsız denetçi): (1) A8-3 SAYIM-5MUM-RENK satırı: mum RENGİ ile sayım kapanış-kapanış kuralından farklıdır;
  (2) ETF-BIRLESIK-KOMISYON-* satırları: Midas emir başına 1,5 USD sabit komisyon; (3) lowmom_kesin_pasif'e 2010+ spot günleri eklendi.
  Mevcut satırların hiçbiri değişmedi (yedek: denetim_rehber/yedek/).
Karar uyumu: sign(etkin_sade) = sign(etkin_ASIL) olan gün oranı (düz/nakit günler dahil); 'aktif uyum': en az birinin pozisyon taşıdığı günlerde.
"""
import json, math, numpy as np, pandas as pd
import statsmodels.api as sm
import exchange_calendars as xc

S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
P = f"{S}/panel"; SEN = f"{S}/out/sentez"; OUT = f"{S}/out/rehber"
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40); pd.set_option("display.max_rows", 500)

V = pd.read_parquet(f"{P}/panel_viop.parquet"); V.index = pd.to_datetime(V.index)
SP = pd.read_parquet(f"{P}/panel_spot.parquet"); SP.index = pd.to_datetime(SP.index)
E = pd.read_parquet(f"{P}/panel_etf.parquet"); E.index = pd.to_datetime(E.index)
HALF_TR = pd.to_datetime(pd.read_csv(f"{S}/out/a1_zaman_serisi_rep/half_days.csv", header=None)[0].iloc[1:].values)
_CAL = xc.get_calendar("XNYS", start="2008-01-01", end="2026-12-31")
_sch = _CAL.schedule
HALF_US = pd.DatetimeIndex(_sch.index[_sch["close"].dt.tz_convert("America/New_York").dt.hour < 16]).tz_localize(None)
NYSE = pd.DatetimeIndex(_CAL.sessions).tz_localize(None)
ESIK = json.load(open(f"{SEN}/esikler.json"))["e2_esik"]
V_OOS = pd.Timestamp("2022-01-01"); E_OOS = pd.Timestamp("2018-01-01")
COST = dict(VIOP=5.0, ETF=10.0)

RV = V.v_ret.astype(float)                                   # VİOP log getirisi (aktif kontrat)


def ret_of(t):
    c = E[f"c_{t}"].astype(float); r = np.log(c).diff(); r[c.isna() | c.shift(1).isna()] = np.nan
    return r


RE = {t: ret_of(t) for t in ["GDX", "GDXJ", "GLD", "SPY"]}


# ===================================================================================== pozisyon dönüştürücüler
def eff_kademeli(s, h):
    s = s.fillna(0).clip(-1, 1)
    return sum(s.shift(k).fillna(0) for k in range(h)) / h


def eff_tamtut(s, h):
    """Son h gün (bugün dahil) içindeki en son sıfırdan farklı sinyalin işareti; yoksa 0."""
    v = np.sign(s.fillna(0).values); out = np.zeros(len(v))
    for i in range(len(v)):
        for k in range(h):
            if i - k < 0: break
            if v[i - k] != 0: out[i] = v[i - k]; break
    return pd.Series(out, index=s.index)


def eff_cogunluk(s, h):
    return np.sign(s.fillna(0).clip(-1, 1).rolling(h, min_periods=1).sum())


def eff_tamtut_kaplama(nakit, h):
    """Kaplama: varsayılan tam uzun (1); son h gün içinde 'nakit' sinyali (x < alt eşik) varsa 0."""
    v = nakit.fillna(False).astype(float)
    return 1.0 - (v.rolling(h, min_periods=1).max() > 0).astype(float)


# ===================================================================================== backtest ve istatistik
def bt(eff, r, cost_bps):
    """hakem bt_eff ile aynı: kazanç eff_{t-1}·(e^r_t − 1); maliyet |Δeff|·cost/2, ertesi gün."""
    r = np.expm1(r.astype(float).dropna())
    eff = eff.reindex(r.index).fillna(0)
    gross = eff.shift(1) * r
    turn = (eff - eff.shift(1).fillna(0)).abs()
    cost = turn.shift(1).fillna(0) * cost_bps / 2 / 1e4
    net = (gross - cost).dropna()
    return net, turn.reindex(net.index)


def cut(x, a, b):
    if a is not None: x = x[x.index >= a]
    if b is not None: x = x[x.index <= b]
    return x


def periods(front):
    o = V_OOS if front == "VIOP" else E_OOS
    return [("tam", None, None), ("OOS", o, None), ("2022+", pd.Timestamp("2022-01-01"), None), ("2026", pd.Timestamp("2026-01-01"), None)]


def alpha_nw(y, x):
    d = pd.concat([y, x], axis=1).dropna()
    if len(d) < 60 or d.iloc[:, 0].std() == 0: return np.nan, np.nan
    m = sm.OLS(d.iloc[:, 0], sm.add_constant(d.iloc[:, 1:])).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
    return round(float(m.params.iloc[0]) * 252 * 100, 2), round(float(m.tvalues.iloc[0]), 2)


def sharpe(n):
    return round(float(n.mean() / n.std() * np.sqrt(252)), 2) if (len(n) > 30 and n.std() > 0) else np.nan


def sgn_agree(a, b, idx):
    a = np.sign(a.reindex(idx).fillna(0).round(9)); b = np.sign(b.reindex(idx).fillna(0).round(9))
    act = (a != 0) | (b != 0)
    return round(float((a == b).mean() * 100), 1), (round(float((a[act] == b[act]).mean() * 100), 1) if act.any() else np.nan)


def evaluate(rule, ver, tanim, front, effs, rets, bh, asil_effs=None, asil_net=None, sabit_ucret=None):
    """effs/rets: {enstrüman: etkin pozisyon / log getiri}; bh: kıyas basit getirisi (alfa ve B&H Sharpe için).
    sabit_ucret=(USD/emir, sermaye USD): [DENETİM eki] Midas'ın emir başına sabit komisyonu; her enstrüman×gün emri için ücret/sermaye
    getiriden düşülür (bps maliyetine ek; emir ertesi gün yazılır, bt() maliyet zamanlamasıyla aynı)."""
    out = []
    nets, nets_st, turns = [], [], []
    for u in effs:
        n, t = bt(effs[u], rets[u], COST[front]); ns, _ = bt(effs[u], rets[u], 2 * COST[front])
        nets.append(n); nets_st.append(ns); turns.append(t)
    net = pd.concat(nets, axis=1).sum(axis=1, min_count=1).dropna()
    net_st = pd.concat(nets_st, axis=1).sum(axis=1, min_count=1).reindex(net.index)
    if sabit_ucret is not None:
        ucret, sermaye = sabit_ucret
        emir = pd.concat([(t_.shift(1).fillna(0) > 1e-9).astype(float) for t_ in turns], axis=1).sum(axis=1).reindex(net.index).fillna(0)
        net = net - emir * ucret / sermaye; net_st = net_st - emir * ucret / sermaye
    turn = pd.concat(turns, axis=1).sum(axis=1, min_count=1).reindex(net.index).fillna(0)
    tdays = pd.concat([(t_ > 1e-9).astype(float) for t_ in turns], axis=1).sum(axis=1).reindex(net.index).fillna(0)   # emir verilen (enstrüman×gün)
    expo = pd.concat([effs[u].reindex(net.index).fillna(0).abs() for u in effs], axis=1).sum(axis=1)
    for nm, a, b in periods(front):
        n = cut(net, a, b); ix = n.index
        bb = bh.reindex(ix)
        al, at = alpha_nw(n, bb.rename("bh"))
        row = dict(kural=rule, surum=ver, tanim=tanim, cephe=front, donem=nm, n_gun=len(n), sharpe=sharpe(n), sharpe_stres=sharpe(net_st.reindex(ix)),
                   yillik_pct=round(float(n.mean() * 252 * 100), 2), vol_pct=round(float(n.std() * np.sqrt(252) * 100), 2),
                   maxdd_pct=round(float((n.cumsum() - n.cumsum().cummax()).min() * 100), 1),
                   bh_sharpe=sharpe(bb.dropna()), alfa_yillik_pct=al, alfa_t=at,
                   maruziyet=round(float(expo.reindex(ix).mean()), 3), gidis_donus_yil=round(float(turn.reindex(ix).sum() / len(ix) * 252 / 2), 1),
                   emir_gunu_yil=round(float(tdays.reindex(ix).sum() / len(ix) * 252), 1))
        if asil_effs is not None:
            ags, acts = [], []
            for u in effs:
                g, ac = sgn_agree(effs[u], asil_effs.get(u, pd.Series(0.0, index=effs[u].index)), ix); ags.append(g); acts.append(ac)
            # çok enstrümanlıda: bütün enstrümanlarda aynı işaret olan gün oranı
            if len(effs) > 1:
                same = np.ones(len(ix), bool); anyact = np.zeros(len(ix), bool)
                for u in effs:
                    x1 = np.sign(effs[u].reindex(ix).fillna(0).round(9)); x0 = np.sign(asil_effs[u].reindex(ix).fillna(0).round(9))
                    same &= (x1.values == x0.values); anyact |= (x1.values != 0) | (x0.values != 0)
                row["karar_uyumu_pct"] = round(float(same.mean() * 100), 1); row["aktif_uyum_pct"] = round(float(same[anyact].mean() * 100), 1)
            else:
                row["karar_uyumu_pct"] = ags[0]; row["aktif_uyum_pct"] = acts[0]
            row["pnl_korelasyon"] = round(float(n.corr(asil_net.reindex(ix))), 3) if asil_net is not None else np.nan
        out.append(row)
    return out, net


ROWS = []
NETS = {}
EFFS = {}


def run(rule, ver, tanim, front, effs, rets, bh, asil_key=None, sabit_ucret=None):
    ae = EFFS.get(asil_key) if asil_key else None; an = NETS.get(asil_key) if asil_key else None
    ref = asil_key is None                                            # asıl (referans) satırı
    if ref: ae = effs
    rows, net = evaluate(rule, ver, tanim, front, effs, rets, bh, ae, None if ref else an, sabit_ucret=sabit_ucret)
    if ref:
        for r in rows: r["pnl_korelasyon"] = 1.0
    ROWS.extend(rows); NETS[(rule, ver)] = net; EFFS[(rule, ver)] = effs
    return net


# ===================================================================================== ASIL sinyaller (hakem tanımı, bağımsız yeniden kurulum)
def to_viop(x):
    out = x.reindex(V.index); miss = ~V.index.isin(x.index)
    if miss.any():
        pos = x.index.searchsorted(V.index[miss], side="right") - 1
        out[miss] = np.where(pos >= 0, x.values[np.clip(pos, 0, None)], np.nan)
    return out


def asil_lowmom():
    lp = np.log(SP.s_p15); rv = lp.diff().rolling(20).std()
    v = rv.values; q = np.full(len(v), np.nan); hist = []
    for i, xi in enumerate(v):
        if np.isfinite(xi):
            hist.append(xi)
            if len(hist) >= 250: q[i] = (np.asarray(hist) <= xi).mean()
    q = pd.Series(q, index=SP.index); sg = np.sign(lp - lp.shift(5))
    p = pd.Series(np.where(q < 1 / 3, sg, 0.0), index=SP.index).where(q.notna() & sg.notna())
    pv = to_viop(p).fillna(0.0); pv[pv.index.isin(HALF_TR)] = 0.0
    return pv, q, rv


def asil_qend():
    idx = V.index; p = pd.Series(0.0, index=idx)
    for m, g in pd.Series(idx, index=idx).groupby(idx.to_period("M")):
        if m.month in (3, 6, 9, 12) and len(g) >= 2:
            if g.index[-1] == idx[-1] and m == idx[-1].to_period("M"): continue
            p[g.index[-2]] = 1.0
    return p


def asil_a4():
    rm = np.log(V.y_GDXJ).diff(); rg = np.log(V.y_GLD).diff()
    b = rm.rolling(60, min_periods=40).cov(rg).shift(1) / rg.rolling(60, min_periods=40).var().shift(1)
    e = rm - b * rg; z = e / e.rolling(120, min_periods=60).std().shift(1)
    return np.sign(z).where(z.abs() > 0.43, 0.0).where(z.notna(), 0.0), z


def asil_a8():
    x = np.log(V.xau_p15 / V.xau_p14); p = np.sign(x).fillna(0.0); p[p.index.isin(HALF_TR)] = 0.0
    return p


def roll_beta2(y, X, win=250, minp=60):
    Xv = X.values; yv = y.values; n, k = Xv.shape; B = np.full((n, k), np.nan)
    for i in range(n):
        lo = max(0, i - win + 1); xx = Xv[lo:i + 1]; yy = yv[lo:i + 1]
        m = np.isfinite(yy) & np.all(np.isfinite(xx), axis=1)
        if m.sum() < minp: continue
        A = np.column_stack([np.ones(m.sum()), xx[m]]); B[i] = np.linalg.lstsq(A, yy[m], rcond=None)[0][1:]
    return pd.DataFrame(B, index=X.index, columns=X.columns)


_RES = {}


def miner_resid(y):
    if y in _RES: return _RES[y]
    X = pd.concat([RE["GLD"], RE["SPY"]], axis=1); X.columns = ["GLD", "SPY"]
    B = roll_beta2(RE[y], X).shift(1)
    _RES[y] = RE[y] - B["GLD"] * RE["GLD"] - B["SPY"] * RE["SPY"]
    return _RES[y]


def asil_e2(y, k, q):
    x = miner_resid(y).rolling(k, min_periods=k).sum().shift(1)
    xi = x[x.index <= pd.Timestamp("2017-12-31")].dropna(); hi = xi.quantile(q); lo = xi.quantile(1 - q)
    p = pd.Series(0.0, index=x.index); p[x > hi] = 1.0; p[x < lo] = -1.0; p[x.isna()] = 0.0
    return p, x, hi, lo


def asil_e3():
    m = np.log(E.xau_cut) - np.log(E.xau_close.shift(1))
    p = (m < 0).astype(float).where(m.notna(), 0.0); p[p.index.isin(HALF_US)] = 0.0
    return p


def asil_e1():
    ses = NYSE
    hol = pd.DatetimeIndex(_CAL.regular_holidays.holidays(start="2008-01-01", end="2026-12-31"))
    ev = sorted({ses[ses < hd][-1] for hd in hol if hd.weekday() < 5 and len(ses[ses < hd])})
    p = pd.Series(0.0, index=ses)
    for d0 in ev:
        prev = ses[ses < d0]
        if len(prev): p[prev[-1]] = 1.0
    return p.reindex(E.index).fillna(0.0)


print("ASIL sinyaller kuruluyor…", flush=True)
A = {}
A["V_LOWMOM_h1"], LQ, LRV = asil_lowmom()
A["V_QEND_h3"] = asil_qend()
A["V_GDXJRES_h3"], A4Z = asil_a4()
A["V_LAST1H_h5"] = asil_a8()
A["E_GDXTATIL_h1"] = asil_e1()
p2j, x2j, hi2j, lo2j = asil_e2("GDXJ", 1, 0.7); A["E_C2J_h3"] = p2j.clip(lower=0)
p2, x2, hi2, lo2 = asil_e2("GDX", 3, 0.7); A["E_C2_h3"] = p2.clip(lower=0)
p1, x1, hi1, lo1 = asil_e2("GDX", 10, 0.8); A["E_C1_h5"] = p1.clip(lower=0)
A["E_C1kap_h5"] = (p1 > -1).astype(float).where(x1.notna(), 1.0)
A["E_M_GDXJ_h1"] = asil_e3()
HV = dict(V_LOWMOM_h1=1, V_QEND_h3=3, V_GDXJRES_h3=3, V_LAST1H_h5=5, E_GDXTATIL_h1=1, E_C2J_h3=3, E_C2_h3=3, E_C1_h5=5, E_C1kap_h5=5, E_M_GDXJ_h1=1)
UND = dict(E_GDXTATIL_h1="GDX", E_C2J_h3="GDXJ", E_C2_h3="GDX", E_C1_h5="GLD", E_C1kap_h5="GLD", E_M_GDXJ_h1="GDXJ")
for nm, (h_, l_) in dict(C2J=(hi2j, lo2j), C2=(hi2, lo2), C1=(hi1, lo1)).items():
    assert abs(h_ - ESIK[nm][0]) < 1e-12 and abs(l_ - ESIK[nm][1]) < 1e-12, f"E2 eşiği tutmadı: {nm}"

# ---------- ASIL ↔ hakem parquet'leri
VR = pd.read_parquet(f"{SEN}/sinyal_viop_ham.parquet"); ER = pd.read_parquet(f"{SEN}/sinyal_etf_ham.parquet")
VP = pd.read_parquet(f"{SEN}/poz_viop.parquet"); EP = pd.read_parquet(f"{SEN}/poz_etf.parquet")
VN = pd.read_parquet(f"{SEN}/pnl_viop.parquet"); EN = pd.read_parquet(f"{SEN}/pnl_etf.parquet")
KON = []
for k, s in A.items():
    front = "VIOP" if k.startswith("V_") else "ETF"
    raw_h = (VR if front == "VIOP" else ER)[k]; pos_h = (VP if front == "VIOP" else EP)[k]; pnl_h = (VN if front == "VIOP" else EN)[k]
    r = RV if front == "VIOP" else RE[UND[k]]
    eff = eff_kademeli(s.reindex(raw_h.index).fillna(0), HV[k]); net, _ = bt(eff, r, COST[front])
    d_raw = (s.reindex(raw_h.index).fillna(0) - raw_h).abs(); d_eff = (eff - pos_h).abs()
    j = pd.concat([net.rename("a"), pnl_h.rename("b")], axis=1)
    both = j.dropna(); only = int(j.a.isna().ne(j.b.isna()).sum())
    KON.append(dict(sinyal=k, gun=len(raw_h), ham_maks_fark=float(d_raw.max()), ham_farkli_gun=int((d_raw > 1e-12).sum()), etkin_maks_fark=float(d_eff.max()),
                    pnl_maks_fark=float((both.a - both.b).abs().max()), pnl_gun=len(both), pnl_yalniz_birinde=only))
KON = pd.DataFrame(KON); KON.to_csv(f"{OUT}/sade_asil_kontrol.csv", index=False)
print(KON.to_string())
assert (KON.pnl_maks_fark < 1e-12).all() and (KON.ham_farkli_gun == 0).all(), "ASIL hakemle birebir tutmuyor"

# ===================================================================================== SADE yapı taşları
# ---------- LOWMOM (e): TradingView HV(20) ve ROC(5), OANDA:XAUUSD günlük kapanışı (17:00 New York) ≈ Dukascopy
def spot_price_series():
    h = pd.read_parquet(f"{P}/duka/XAUUSD.parquet")["c"]; h.index = h.index.tz_localize(None) + pd.Timedelta(hours=1)
    m = pd.read_parquet(f"{P}/duka_min_XAUUSD.parquet")["c"]; m.index = pd.to_datetime(m.index) + pd.Timedelta(minutes=1)
    m = m[m.index > h.index.max()]
    return pd.concat([h, m]).sort_index()


def daily_close_17et(px):
    days = pd.bdate_range("2009-01-02", "2026-11-06")
    targ = pd.DatetimeIndex([(d + pd.Timedelta(hours=17)).tz_localize("America/New_York").tz_convert("UTC").tz_localize(None) for d in days])
    i = px.index.searchsorted(targ, side="right") - 1
    ok = i >= 0; ts = px.index.values[np.clip(i, 0, None)]
    stale = (targ.values - ts) / np.timedelta64(1, "h")
    vals = np.where(ok & (stale <= 2), px.values[np.clip(i, 0, None)], np.nan)
    return pd.Series(vals, index=days).dropna()


PX = spot_price_series(); C17 = daily_close_17et(PX)
LR = np.log(C17).diff()
HV_K = LR.rolling(20).std(ddof=0) * np.sqrt(365) * 100            # tamamlanmış günlük mumlarla TV HV(20), kapanış günü d'de
ROC5_K = C17 / C17.shift(5) - 1
HVS = HV_K[HV_K.index >= "2010-01-04"].dropna()
THR_Y = {y: float(HVS[HVS.index <= f"{y - 1}-12-31"].quantile(1 / 3)) for y in range(2011, 2028)}   # yıllık eşik: önceki yıl sonuna kadar 1/3 kantil
THR_IS = float(HVS[HVS.index <= "2021-12-31"].quantile(1 / 3)); THR_NOW = float(HVS.quantile(1 / 3))
# asıl eşiğin TV birimine çevrilmiş hali (bilgi): rv20 (√252, ddof=1) 1/3 kantili
asil_thr_now = float(np.quantile(LRV.dropna().values, 1 / 3) * np.sqrt(252) * 100)


# 15:00 UTC spot serisinde TV formülü (yalnız eşik için; VİOP uzlaşması ≈ 15:10 UTC olduğundan BIST:XAUUSD sürümünün eşdeğer eşiği budur)
_lp15 = np.log(SP.s_p15); HV15 = _lp15.diff().rolling(20).std(ddof=0) * np.sqrt(365) * 100; ROC15 = _lp15 - _lp15.shift(5)
_h15 = HV15[HV15.index >= "2010-01-04"].dropna()
THR15_Y = {y: float(_h15[_h15.index <= f"{y - 1}-12-31"].quantile(1 / 3)) for y in range(2011, 2028)}
THR15_IS = float(_h15[_h15.index <= "2021-12-31"].quantile(1 / 3)); THR15_NOW = float(_h15.quantile(1 / 3))


def lowmom_sade(kind, thr_mode):
    """OANDA:XAUUSD günlük grafik (kapanış 17:00 New York).
    kind: 'KAPANIS' (dünkü tamamlanmış mumlar; sabah bilinir) | 'CANLI' (18:00 TSİ'de günlük grafik: son mum = 15:00 UTC fiyatı)."""
    ci = C17.index; out = pd.Series(0.0, index=V.index)
    for t in V.index:
        j = ci.searchsorted(t, side="left") - 1                     # son kapanış günü < t
        if j < 25: continue
        th = THR_Y[t.year] if thr_mode == "yillik" else THR_IS
        if kind == "KAPANIS":
            hv = HV_K.iloc[j]; roc = ROC5_K.iloc[j]
        else:
            p = V.xau_p15.get(t, np.nan)
            if not np.isfinite(p) or t in HALF_TR: continue
            rr = np.append(LR.values[j - 18:j + 1], math.log(p / C17.values[j]))
            hv = rr.std(ddof=0) * math.sqrt(365) * 100; roc = p / C17.values[j - 4] - 1
        if np.isfinite(hv) and np.isfinite(roc) and hv < th: out[t] = float(np.sign(roc))
    return out


def lowmom_viop(kind, thr_mode, adjusted=True):
    """BIST:XAUUSD (aktif vade kodu, 'uzlaşmayı kapanış say' açık) günlük grafik: geçmiş mumlar = uzlaşma (≈15:10 UTC).
    adjusted=True: aynı kontrat içi getiri (aktif vade kodunun kendi geçmişi = roll sıçraması yok); False: sürekli XAUUSD1! (roll sıçramalı).
    CANLI: 18:00 TSİ'de son mum canlı fiyat (≈ spot 15:00 UTC; canlı getiri ≈ ln(spot15_t/spot15_t-1)). KAPANIS: dünkü uzlaşmaya kadar.
    Eşik: 15:00 UTC spot serisinde TV-HV(20) 1/3 kantili (2010→önceki yıl sonu ya da 2010–2021 sabit)."""
    vr = (RV if adjusted else np.log(V.v_settle.astype(float)).diff()).values
    live = np.log(V.xau_p15 / V.xau_p15.shift(1)).values
    out = pd.Series(0.0, index=V.index)
    for i, t in enumerate(V.index):
        if i < 25: continue
        th = THR15_Y.get(t.year, np.nan) if thr_mode == "yillik" else THR15_IS
        if kind == "CANLI":
            if t in HALF_TR: continue
            rr = np.append(vr[i - 19:i], live[i]); roc = np.nansum(vr[i - 4:i]) + live[i]
        else:
            rr = vr[i - 20:i]; roc = vr[i - 5:i].sum()
        if not np.isfinite(rr).all() or not np.isfinite(roc): continue
        hv = rr.std(ddof=0) * math.sqrt(365) * 100
        if hv < th: out.iloc[i] = float(np.sign(roc))
    return out


def lowmom_tani15(thr_mode):
    """TANI (elle okunamaz): asıl 15:00 UTC spot serisi, TV-HV formülü ve yıllık/sabit eşik → eşik mekaniğinin etkisini ayırır."""
    th = pd.Series([THR15_Y.get(d.year, np.nan) if thr_mode == "yillik" else THR15_IS for d in SP.index], index=SP.index)
    p = pd.Series(np.where(HV15 < th, np.sign(ROC15), 0.0), index=SP.index).where(HV15.notna() & ROC15.notna())
    pv = to_viop(p).fillna(0.0); pv[pv.index.isin(HALF_TR)] = 0.0
    return pv


# ---------- A4-C1 (d): aylık sabit β (60 satır) ve aylık eşik 0,43·σ (120 satır), basit % değişim.
#   VİOP-satır hizası (hakem tanımı): GDXJ/GLD'nin son kapanışının, bir önceki VİOP gününde bilinen kapanışa göre % değişimi
#   (normal gün: dünkü günlük mum; bayram dönüşü: bayram boyunca toplam değişim; ABD tatili ertesi: değişim 0 → sinyal yok).
#   abd_takvimi=True (TANI): her zaman yalnız son ABD günlük mumunun % değişimi, β/σ ABD seanslarında.
def a4_sade(abd_takvimi=False, mode="aylik"):
    """mode: 'aylik' (ay başında 60/120 satır), 'yillik' (Ocak başında), 'donuk' (IS 2017-03..2021-12'nin tamamında bir kez; sonra hiç güncellenmez)."""
    if abd_takvimi:
        cj = E.c_GDXJ.astype(float); cg = E.c_GLD.astype(float); idx = E.index
    else:
        cj = V.y_GDXJ.astype(float); cg = V.y_GLD.astype(float); idx = V.index
    rj = cj.pct_change(fill_method=None); rg = cg.pct_change(fill_method=None)
    BM = {}
    if mode == "donuk":
        m_ = (idx >= V.index[0]) & (idx <= pd.Timestamp("2021-12-31"))
        jj = rj[m_].dropna(); gg = rg.reindex(jj.index)
        b = float(np.cov(jj, gg, ddof=1)[0, 1] / np.var(gg, ddof=1)); sd_ = float((jj - b * gg).std(ddof=1))
    for m in pd.period_range(V.index[0].to_period("M"), V.index[-1].to_period("M"), freq="M"):
        if mode == "donuk": BM[m] = (b, sd_); continue
        st = m.start_time if mode == "aylik" else pd.Timestamp(f"{m.year}-01-01")
        jj = rj[idx < st].dropna().iloc[-200:]; gg = rg.reindex(jj.index)
        if len(jj) < 60: BM[m] = (np.nan, np.nan); continue
        j60, g60 = jj.iloc[-60:], gg.iloc[-60:]
        b = float(np.cov(j60, g60, ddof=1)[0, 1] / np.var(g60, ddof=1))
        BM[m] = (b, float((jj - b * gg).iloc[-120:].std(ddof=1)))
    sig = pd.Series(0.0, index=V.index)
    if abd_takvimi:
        last = None
        for t in V.index:
            i = idx.searchsorted(t, side="left") - 1
            if i < 1 or idx[i] == last: continue                     # ABD tatili: yeni mum yok → yeni sinyal yok
            last = idx[i]; b, sd = BM[t.to_period("M")]; e = rj.iloc[i] - b * rg.iloc[i]
            if np.isfinite(e) and np.isfinite(sd): sig[t] = 1.0 if e > 0.43 * sd else (-1.0 if e < -0.43 * sd else 0.0)
    else:
        bm = pd.Series([BM[d.to_period("M")][0] for d in V.index], index=V.index); sd = pd.Series([BM[d.to_period("M")][1] for d in V.index], index=V.index)
        e = rj - bm * rg
        sig = pd.Series(np.where(e > 0.43 * sd, 1.0, np.where(e < -0.43 * sd, -1.0, 0.0)), index=V.index)
    return sig, BM


def guclu(s, h):
    """1 kontratlık yuvarlama: round(kademeli etkin) → son h sinyalin net toplamı |Σ| ≥ h/2 ise tam birim (A4: 3'te ≥2, A8: 5'te ≥3 net = 4-1/5-0)."""
    return np.round(eff_kademeli(s, h) + 1e-12 * np.sign(eff_kademeli(s, h)))


# ---------- E2 (d): ABD takviminde k günlük basit % değişimler (C_t-1/C_t-1-k − 1), aylık sabit β (GLD, SPY; 250 seans OLS, basit getiri)
def e2_sade(y, k, mode="aylik"):
    c = {t: E[f"c_{t}"].astype(float) for t in (y, "GLD", "SPY")}
    r1 = {t: c[t].pct_change(fill_method=None) for t in c}
    Rk = {t: (c[t] / c[t].shift(k) - 1).shift(1) for t in c}       # gün t'de bilinen: t-1'de biten k günlük % değişim
    us = E.index; BM = {}
    D_ = pd.concat([r1[y], r1["GLD"], r1["SPY"]], axis=1)
    if mode == "donuk":                                              # IS (2008–2017) tamamında bir kez; sonra hiç güncellenmez
        d = D_[us <= pd.Timestamp("2017-12-31")].dropna()
        A_ = np.column_stack([np.ones(len(d)), d.iloc[:, 1:].values]); b = np.linalg.lstsq(A_, d.iloc[:, 0].values, rcond=None)[0]
    for m in pd.period_range(us[0].to_period("M"), us[-1].to_period("M"), freq="M"):
        if mode == "donuk": BM[m] = (float(b[1]), float(b[2])); continue
        st = m.start_time
        d = D_[us < st].dropna().iloc[-250:]
        if len(d) < 60: BM[m] = (np.nan, np.nan); continue
        A_ = np.column_stack([np.ones(len(d)), d.iloc[:, 1:].values]); b = np.linalg.lstsq(A_, d.iloc[:, 0].values, rcond=None)[0]
        BM[m] = (float(b[1]), float(b[2]))
    bg = pd.Series([BM[d.to_period("M")][0] for d in us], index=us); bs = pd.Series([BM[d.to_period("M")][1] for d in us], index=us)
    x = Rk[y] - bg * Rk["GLD"] - bs * Rk["SPY"]
    return x, BM


# ===================================================================================== VİOP
print("VİOP sürümleri…", flush=True)
R_V = dict(XAU=RV); BH_V = np.expm1(RV)
ASIL_V = {}
# --- LOWMOM
k = "A1-LOWMOM-h1"; e = eff_kademeli(A["V_LOWMOM_h1"], 1); ASIL_V[k] = e
run(k, "ASIL", "15:00 UTC spot rv20'nin 2010'dan beri yüzdeliği <1/3 iken sign(ln P_t/P_t-5), 1 gün; TR yarım günü yok", "VIOP", dict(XAU=e), R_V, BH_V)
LS = {}
for kind, tm in [("CANLI", "yillik"), ("KAPANIS", "yillik"), ("CANLI", "sabit")]:
    s = lowmom_sade(kind, tm); LS[("OANDA", kind, tm)] = s
    tn = (f"OANDA:XAUUSD günlük (kapanış 17:00 NY) HV(20) < {'yıllık eşik (önceki yıl sonuna kadarki 1/3 kantil)' if tm == 'yillik' else f'sabit %{THR_IS:.2f}'} iken ROC(5) işareti; "
          + ("18:00 TSİ'de canlı mumla, TR yarım günü yok" if kind == "CANLI" else "DÜNKÜ tamamlanmış mumlarla (sabah bilinir)"))
    run(k, f"HV20-OANDA-{kind}-{'YILLIK' if tm == 'yillik' else 'SABIT'}", tn, "VIOP", dict(XAU=eff_kademeli(s, 1)), R_V, BH_V, asil_key=(k, "ASIL"))
for kind, tm, adj in [("CANLI", "yillik", True), ("CANLI", "sabit", True), ("KAPANIS", "yillik", True), ("CANLI", "yillik", False)]:
    s = lowmom_viop(kind, tm, adj); LS[("VIOP", kind, tm, adj)] = s
    tn = (f"{'BIST aktif vade kodu (ör. XAUUSDZ2026)' if adj else 'BIST:XAUUSD1! sürekli (roll sıçramalı)'}, 'uzlaşmayı kapanış say' açık, günlük HV(20) < "
          + (f"yıllık eşik (2026: %{THR15_Y[2026]:.2f})" if tm == "yillik" else f"sabit %{THR15_IS:.2f}") + " iken ROC(5) işareti; "
          + ("18:00 TSİ canlı mumla, TR yarım günü yok" if kind == "CANLI" else "dünkü uzlaşmaya kadar (sabah bilinir)"))
    run(k, f"HV20-VIOPUZL-{kind}-{'YILLIK' if tm == 'yillik' else 'SABIT'}{'' if adj else '-ROLLSICRAMALI'}", tn, "VIOP", dict(XAU=eff_kademeli(s, 1)), R_V, BH_V, asil_key=(k, "ASIL"))
for tm in ("yillik", "sabit"):
    run(k, f"TANI-15UTC-TVFORMUL-{'YILLIK' if tm == 'yillik' else 'SABIT'}", "TANI (elle okunamaz): asıl 15:00 UTC spot serisi + TV HV(20) formülü + " + ("yıllık" if tm == "yillik" else "sabit") + " eşik",
        "VIOP", dict(XAU=eff_kademeli(lowmom_tani15(tm), 1)), R_V, BH_V, asil_key=(k, "ASIL"))
# --- QEND
k = "A3_QEND_h3"; e = eff_kademeli(A["V_QEND_h3"], 3); ASIL_V[k] = e
run(k, "ASIL", "Mar/Haz/Eyl/Ara sondan 2. VİOP günü 1/3 dilim uzun, 3 gün kademeli (etkin 1/3)", "VIOP", dict(XAU=e), R_V, BH_V)
run(k, "TAM-TUT", "Sondan 2. VİOP günü uzlaşmasında 1 tam birim uzun, 3 VİOP günü sonra (yeni çeyreğin 2. günü) kapat", "VIOP",
    dict(XAU=eff_tamtut(A["V_QEND_h3"], 3)), R_V, BH_V, asil_key=(k, "ASIL"))
# --- A4-C1
k = "A4-C1_GDXJ_artik_h3"; s0 = A["V_GDXJRES_h3"]; e = eff_kademeli(s0, 3); ASIL_V[k] = e
run(k, "ASIL", "z=(r_GDXJ−β60·r_GLD)/σ120 (log, VİOP satırı), |z|>0,43 yönünde 1/3 dilim, 3 gün kademeli", "VIOP", dict(XAU=e), R_V, BH_V)
run(k, "TAM-TUT", "Asıl z sinyali; sinyal günü tam birim, son sinyalden 3 gün tut, ters sinyalde çevir", "VIOP", dict(XAU=eff_tamtut(s0, 3)), R_V, BH_V, asil_key=(k, "ASIL"))
run(k, "COGUNLUK", "Asıl z sinyali; son 3 günün sinyal toplamının işaretiyle tam birim", "VIOP", dict(XAU=eff_cogunluk(s0, 3)), R_V, BH_V, asil_key=(k, "ASIL"))
run(k, "GUCLU-COGUNLUK(1 kontrat)", "Asıl z sinyali; son 3 günde net ≥2 aynı yön sinyal varsa tam birim (= 1 kontrata yuvarlanmış asıl)", "VIOP", dict(XAU=guclu(s0, 3)), R_V, BH_V, asil_key=(k, "ASIL"))
a4s, A4BM = a4_sade(False)
d4 = "e=%GDXJ−β·%GLD (basit; son kapanışın önceki VİOP günündeki kapanışa göre değişimi), β ve eşik ±0,43σ ayda bir sabit"
run(k, "SABIT-BETA+SAYIM(kademeli)", d4 + "; pozisyon = (son 3 günün UZUN sayısı − KISA sayısı)/3 birim", "VIOP", dict(XAU=eff_kademeli(a4s, 3)), R_V, BH_V, asil_key=(k, "ASIL"))
run(k, "SABIT-BETA+TAM-TUT", d4 + "; tam birim, son sinyalden 3 gün tut, ters sinyalde çevir", "VIOP", dict(XAU=eff_tamtut(a4s, 3)), R_V, BH_V, asil_key=(k, "ASIL"))
run(k, "SABIT-BETA+COGUNLUK", d4 + "; son 3 günün sinyal toplamının işareti, tam birim", "VIOP", dict(XAU=eff_cogunluk(a4s, 3)), R_V, BH_V, asil_key=(k, "ASIL"))
run(k, "SABIT-BETA+GUCLU(1 kontrat)", d4 + "; son 3 günde net ≥2 aynı yön sinyal varsa tam birim", "VIOP", dict(XAU=guclu(a4s, 3)), R_V, BH_V, asil_key=(k, "ASIL"))
for md, lab in [("yillik", "YILLIK"), ("donuk", "DONUK-IS")]:
    a4m, BMm = a4_sade(False, md)
    run(k, f"SABIT-BETA({lab})+SAYIM", d4.replace("ayda bir sabit", "yılda bir (Ocak) güncellenir" if md == "yillik" else "IS 2017–2021'de bir kez kestirilip hiç güncellenmez")
        + f"{'' if md == 'yillik' else f' (β {BMm[V.index[-1].to_period(chr(77))][0]:.2f}, eşik ±%{0.43 * BMm[V.index[-1].to_period(chr(77))][1] * 100:.2f})'}; 3 gün kademeli sayım",
        "VIOP", dict(XAU=eff_kademeli(a4m, 3)), R_V, BH_V, asil_key=(k, "ASIL"))
a4u, _ = a4_sade(True)
run(k, "TANI-SABIT-BETA-ABD-TAKVIMI+SAYIM", "TANI: bayram dönüşünde de yalnız son ABD günlük mumunun % değişimi (β, σ ABD seanslarında); 3 gün kademeli", "VIOP",
    dict(XAU=eff_kademeli(a4u, 3)), R_V, BH_V, asil_key=(k, "ASIL"))
# --- A8-3
k = "A8-3_seg_last1h_h5"; s8 = A["V_LAST1H_h5"]; e = eff_kademeli(s8, 5); ASIL_V[k] = e
run(k, "ASIL", "sign(spot15/spot14 UTC) yönünde 1/5 dilim, 5 gün kademeli", "VIOP", dict(XAU=e), R_V, BH_V)
run(k, "SAYIM-5MUM(=ASIL)", "OANDA:XAUUSD 1 saatlik, İstanbul saati: bugün dahil son 5 VİOP gününde 17:00 mumunun KAPANIŞI 16:00 mumunun KAPANIŞINDAN yüksekse UZUN, düşükse KISA; pozisyon (UZUN − KISA)/5 birim; asılla birebir aynı (mum RENGİ değil, kapanış-kapanış karşılaştırması)", "VIOP",
    dict(XAU=e.copy()), R_V, BH_V, asil_key=(k, "ASIL"))
# [DENETİM eki] mumun RENGİ (17:00 TSİ = 14:00 UTC saatlik barın açılış→kapanış yönü) ile sayım: kapanış-kapanış kuralından farklı olabilir
#   (bar açılışı önceki barın kapanışına eşit değil). Dukascopy saatlik o/c (2026-10-30'a kadar); sonrası ve bar yoksa asıl dilim.
_HB = pd.read_parquet(f"{P}/duka/XAUUSD.parquet")[["o", "c"]]; _HB.index = _HB.index.tz_localize(None)
s8r = s8.copy()
for t in V.index:
    kb = t + pd.Timedelta(hours=14)
    if t in HALF_TR or kb not in _HB.index: continue
    s8r[t] = float(np.sign(_HB.c.loc[kb] - _HB.o.loc[kb]))
_fark8 = int((s8r != s8).sum())
run(k, "SAYIM-5MUM-RENK", f"DENETİM: son 5 VİOP gününün 17:00 TSİ mumlarının RENGİ (yeşil − kırmızı)/5; Dukascopy'de {_fark8} günde (%{_fark8 / len(s8) * 100:.1f}) kapanış-kapanış kuralından farklı", "VIOP",
    dict(XAU=eff_kademeli(s8r, 5)), R_V, BH_V, asil_key=(k, "ASIL"))
run(k, "TAM-TUT", "Her gün 17:00 TSİ saatlik mumunun rengi yönünde tam birim (her gün yeni sinyal geldiği için fiilen günlük işaret takibi)", "VIOP",
    dict(XAU=eff_tamtut(s8, 5)), R_V, BH_V, asil_key=(k, "ASIL"))
run(k, "COGUNLUK", "Son 5 VİOP gününün 17:00 TSİ mum renklerinin çoğunluğu yönünde tam birim", "VIOP", dict(XAU=eff_cogunluk(s8, 5)), R_V, BH_V, asil_key=(k, "ASIL"))
run(k, "GUCLU-COGUNLUK(1 kontrat)", "Son 5 mumdan en az 4'ü aynı renkse o yönde tam birim, değilse düz (= 1 kontrata yuvarlanmış asıl)", "VIOP",
    dict(XAU=guclu(s8, 5)), R_V, BH_V, asil_key=(k, "ASIL"))

# --- VİOP birleşik
def vcomb(effs, w):
    return sum(effs) * w


asil_comb = vcomb(list(ASIL_V.values()), 0.25)
run("VIOP-BIRLESIK", "ASIL-1/4", "Hakem birleşimi: 4 asıl kademeli etkin pozisyonun ortalaması", "VIOP", dict(XAU=asil_comb), R_V, BH_V)
LO = eff_kademeli(LS[("OANDA", "CANLI", "yillik")], 1); LV = eff_kademeli(LS[("VIOP", "CANLI", "yillik", True)], 1); QT = eff_tamtut(A["V_QEND_h3"], 3)
plans = {  # önceden tanımlı iki plan (sonuçlardan önce yazıldı) + sonradan seçilmiş öneri planı
    "SADE-TAMTUT": ([LO, QT, eff_tamtut(a4s, 3), eff_tamtut(s8, 5)], "ÖNCEDEN: LOWMOM HV20-OANDA-CANLI-YILLIK + QEND TAM-TUT + A4 SABIT-BETA+TAM-TUT + A8 TAM-TUT"),
    "SADE-COGUNLUK": ([LO, QT, eff_cogunluk(a4s, 3), eff_cogunluk(s8, 5)], "ÖNCEDEN: LOWMOM HV20-OANDA-CANLI-YILLIK + QEND TAM-TUT + A4 SABIT-BETA+COGUNLUK + A8 COGUNLUK"),
}
for nm, (effs, ds) in plans.items():
    run("VIOP-BIRLESIK", f"{nm}-4BIRIM", ds + "; her kural tam 1 kontrat birimi, toplam −4..+4", "VIOP", dict(XAU=vcomb(effs, 1.0)), R_V, BH_V, asil_key=("VIOP-BIRLESIK", "ASIL-1/4"))
    run("VIOP-BIRLESIK", f"{nm}-1/4", ds + "; her kural 1/4 birim (toplam −1..+1)", "VIOP", dict(XAU=vcomb(effs, 0.25)), R_V, BH_V, asil_key=("VIOP-BIRLESIK", "ASIL-1/4"))
ds = "SONRADAN SEÇİLDİ: LOWMOM HV20-VIOPUZL-CANLI-YILLIK + QEND TAM-TUT + A4 SABIT-BETA+SAYIM + A8 SAYIM-5MUM"
run("VIOP-BIRLESIK", "ONERILEN-SAYIM-1/4", ds + "; her kural 1/4 birim, kesirli (sayım) pozisyonlar", "VIOP",
    dict(XAU=vcomb([LV, QT, eff_kademeli(a4s, 3), e], 0.25)), R_V, BH_V, asil_key=("VIOP-BIRLESIK", "ASIL-1/4"))
run("VIOP-BIRLESIK", "ONERILEN-4BIRIM-YUVARLA", ds.replace("SAYIM + A8 SAYIM-5MUM", "GUCLU + A8 GUCLU-COGUNLUK") + "; her kural tam 1 kontrat (−4..+4), sayımlar 1 kontrata yuvarlanır", "VIOP",
    dict(XAU=vcomb([LV, QT, guclu(a4s, 3), guclu(s8, 5)], 1.0)), R_V, BH_V, asil_key=("VIOP-BIRLESIK", "ASIL-1/4"))
run("VIOP-BIRLESIK", "ASIL-4BIRIM-YUVARLA", "Kıyas: 4 asıl kural her biri 1 kontrata yuvarlanmış (LOWMOM, QEND tam; A4 ve A8 round(kademeli)); toplam −4..+4", "VIOP",
    dict(XAU=vcomb([ASIL_V["A1-LOWMOM-h1"], QT, guclu(s0, 3), guclu(s8, 5)], 1.0)), R_V, BH_V, asil_key=("VIOP-BIRLESIK", "ASIL-1/4"))

# ===================================================================================== ETF
print("ETF sürümleri…", flush=True)
BH_E = {t: np.expm1(RE[t]) for t in RE}
ASIL_E = {}
k = "E1-C2_GDX_tatil_oncesi"; e = eff_kademeli(A["E_GDXTATIL_h1"], 1); ASIL_E[k] = ("GDX", e)
run(k, "ASIL", "NYSE tatilinden önceki son günden bir önceki kapanışta GDX al, ertesi kapanışta sat (zaten sade)", "ETF", dict(GDX=e), dict(GDX=RE["GDX"]), BH_E["GDX"])
k = "E3-1_altin_gunici_GDXJ_donus"; e = eff_kademeli(A["E_M_GDXJ_h1"], 1); ASIL_E[k] = ("GDXJ", e)
run(k, "ASIL", "spot 15:00 ET < önceki 16:00 ET ise GDXJ 1 gün (zaten sade: iki fiyat karşılaştırması)", "ETF", dict(GDXJ=e), dict(GDXJ=RE["GDXJ"]), BH_E["GDXJ"])
E2D = {"E2-C2j_GDXJ_artik_h3": ("GDXJ", 1, 3, "GDXJ", p2j, hi2j, lo2j, "E_C2J_h3"),
       "E2-C2_GDX_artik_h3": ("GDX", 3, 3, "GDX", p2, hi2, lo2, "E_C2_h3"),
       "E2-C1_madenci_oncu_GLD_h5": ("GDX", 10, 5, "GLD", p1, hi1, lo1, "E_C1_h5")}
E2X = {}
for k, (y, kk, h, u, pp, hi, lo, key) in E2D.items():
    sl_ = pp.clip(lower=0); e = eff_kademeli(sl_, h); ASIL_E[k] = (u, e)
    rr = dict(**{u: RE[u]})
    run(k, "ASIL", f"{y} artığı (GLD+SPY, 250g yuvarlanan OLS, log) {kk} günlük toplam > %{hi * 100:.3f} ise {u} 1/{h} dilim, {h} gün kademeli", "ETF", {u: e}, rr, BH_E[u])
    run(k, "TAM-TUT", f"Asıl sinyal; sinyal günü {u} tam kol, son sinyalden {h} gün tut", "ETF", {u: eff_tamtut(sl_, h)}, rr, BH_E[u], asil_key=(k, "ASIL"))
    xs, BM = e2_sade(y, kk); E2X[k] = (xs, BM)
    ss = (xs > hi).astype(float)
    dd = f"x=%{y}({kk}g)−βG·%GLD({kk}g)−βS·%SPY({kk}g) (TV basit % değişim, t-1'de biter), β ayda bir sabit; x > %{hi * 100:.3f}"
    run(k, "SABIT-BETA+SAYIM(kademeli)", dd + f"; {u} kolunun (son {h} günde x>eşik olan gün sayısı)/{h}'ü tutulur (= kademeli)", "ETF",
        {u: eff_kademeli(ss, h)}, rr, BH_E[u], asil_key=(k, "ASIL"))
    run(k, "SABIT-BETA+TAM-TUT", dd + f"; {u} tam kol, son sinyalden {h} gün tut", "ETF", {u: eff_tamtut(ss, h)}, rr, BH_E[u], asil_key=(k, "ASIL"))
    xd, BMd = e2_sade(y, kk, "donuk"); bd = BMd[us_last := E.index[-1].to_period("M")]
    run(k, "SABIT-BETA(DONUK-IS)+TAM-TUT", dd.replace("β ayda bir sabit", f"β IS 2008–2017'de bir kez (βG {bd[0]:.2f}, βS {bd[1]:.2f}), hiç güncellenmez")
        + f"; {u} tam kol, son sinyalden {h} gün tut", "ETF", {u: eff_tamtut((xd > hi).astype(float), h)}, rr, BH_E[u], asil_key=(k, "ASIL"))
# --- C1 kaplama (GLD tutana)
k = "E2-C1-KAPLAMA"; xs1, _ = E2X["E2-C1_madenci_oncu_GLD_h5"]
e = eff_kademeli(A["E_C1kap_h5"], 5)
run(k, "ASIL", "GLD tut; x (GDX 10g artık) < %-4,022 olan günün 1/5 dilimi nakit, 5 gün kademeli", "ETF", dict(GLD=e), dict(GLD=RE["GLD"]), BH_E["GLD"])
run(k, "TAM-TUT", "GLD tut; asıl x < %-4,022 olursa tamamen nakit, son böyle günden 5 gün sonra GLD'ye dön", "ETF",
    dict(GLD=eff_tamtut_kaplama(x1 < lo1, 5)), dict(GLD=RE["GLD"]), BH_E["GLD"], asil_key=(k, "ASIL"))
run(k, "SABIT-BETA+TAM-TUT", "GLD tut; sabit-beta 10g % artık < %-4,022 olursa tamamen nakit, 5 gün sonra GLD'ye dön", "ETF",
    dict(GLD=eff_tamtut_kaplama(xs1 < lo1, 5)), dict(GLD=RE["GLD"]), BH_E["GLD"], asil_key=(k, "ASIL"))

# --- ETF birleşik (her kural sermayenin 1/5'i, aynı ETF'de netleşir); kıyas GDX/GDXJ/GLD eşit sepet
BASKET = (BH_E["GDX"] + BH_E["GDXJ"] + BH_E["GLD"]) / 3


def ecomb(parts):
    out = {}
    for u, e in parts:
        out[u] = out.get(u, 0) + e / 5
    return out


comb_a = ecomb(ASIL_E.values())
run("ETF-BIRLESIK", "ASIL", "Hakem birleşimi: 5 asıl sinyal × 1/5, aynı ETF'de netleşir", "ETF", comb_a, {u: RE[u] for u in comb_a}, BASKET)
sade_parts = [("GDX", eff_kademeli(A["E_GDXTATIL_h1"], 1)), ("GDXJ", eff_kademeli(A["E_M_GDXJ_h1"], 1))]
for k, (y, kk, h, u, pp, hi, lo, key) in E2D.items():
    sade_parts.append((u, eff_tamtut((E2X[k][0] > hi).astype(float), h)))
comb_s = ecomb(sade_parts)
run("ETF-BIRLESIK", "SADE", "E1-C2 ve E3-1 asıl (zaten sade) + C2j/C2/C1 SABIT-BETA+TAM-TUT; her kural 1/5, aynı ETF'de netleşir", "ETF",
    comb_s, {u: RE[u] for u in comb_s}, BASKET, asil_key=("ETF-BIRLESIK", "ASIL"))
sade_parts2 = [("GDX", eff_kademeli(A["E_GDXTATIL_h1"], 1)), ("GDXJ", eff_kademeli(A["E_M_GDXJ_h1"], 1))]
for k, (y, kk, h, u, pp, hi, lo, key) in E2D.items():
    sade_parts2.append((u, eff_tamtut(pp.clip(lower=0), h)))
comb_s2 = ecomb(sade_parts2)
run("ETF-BIRLESIK", "TAM-TUT(yuvarlanan β)", "E1-C2 ve E3-1 asıl + C2j/C2/C1 TAM-TUT (asıl yuvarlanan β artığıyla); her kural 1/5", "ETF",
    comb_s2, {u: RE[u] for u in comb_s2}, BASKET, asil_key=("ETF-BIRLESIK", "ASIL"))
# [DENETİM eki] Midas sabit komisyonu (KULLANIM §5: emir başına 1,5 USD). bps maliyeti sabit ücreti içermez; kademeli dilimler
#   (1/5 × 1/3 = sermayenin 1/15'i) küçük hesapta ücretle erir. Karar sütunu SADE'yi aynı sermayedeki ASIL ile karşılaştırır.
for C_ in (10000, 25000, 50000):
    kk_ = f"ETF-BIRLESIK-KOMISYON-{C_ // 1000}K"
    run(kk_, "ASIL", f"ASIL birleşim, 10 bps + emir başına 1,5 USD sabit komisyon, sermaye {C_} USD", "ETF", comb_a, {u: RE[u] for u in comb_a}, BASKET,
        sabit_ucret=(1.5, C_))
    run(kk_, "SADE", f"SADE birleşim, 10 bps + emir başına 1,5 USD sabit komisyon, sermaye {C_} USD", "ETF", comb_s, {u: RE[u] for u in comb_s}, BASKET,
        asil_key=(kk_, "ASIL"), sabit_ucret=(1.5, C_))

# ===================================================================================== tablo, karar, eşikler
R = pd.DataFrame(ROWS)
R.to_csv(f"{OUT}/sade_sonuc.csv", index=False)

W = []
for (rule, ver), g in R.groupby(["kural", "surum"], sort=False):
    gi = g.set_index("donem")
    W.append(dict(kural=rule, surum=ver, tanim=gi.loc["tam", "tanim"],
                  tam_sharpe=gi.loc["tam", "sharpe"], oos_sharpe=gi.loc["OOS", "sharpe"], p2022_sharpe=gi.loc["2022+", "sharpe"], p2026_sharpe=gi.loc["2026", "sharpe"],
                  tam_sharpe_stres=gi.loc["tam", "sharpe_stres"], oos_sharpe_stres=gi.loc["OOS", "sharpe_stres"],
                  bh_tam_sharpe=gi.loc["tam", "bh_sharpe"], bh_oos_sharpe=gi.loc["OOS", "bh_sharpe"],
                  tam_alfa_yillik_pct=gi.loc["tam", "alfa_yillik_pct"], tam_alfa_t=gi.loc["tam", "alfa_t"],
                  oos_alfa_yillik_pct=gi.loc["OOS", "alfa_yillik_pct"], oos_alfa_t=gi.loc["OOS", "alfa_t"],
                  tam_yillik_pct=gi.loc["tam", "yillik_pct"], tam_vol_pct=gi.loc["tam", "vol_pct"], tam_maxdd_pct=gi.loc["tam", "maxdd_pct"],
                  maruziyet=gi.loc["tam", "maruziyet"], gidis_donus_yil=gi.loc["tam", "gidis_donus_yil"], emir_gunu_yil=gi.loc["tam", "emir_gunu_yil"],
                  karar_uyumu_pct=gi.loc["tam", "karar_uyumu_pct"], aktif_uyum_pct=gi.loc["tam", "aktif_uyum_pct"], pnl_korelasyon=gi.loc["tam", "pnl_korelasyon"]))
W = pd.DataFrame(W)
# önceden yazılmış karar kuralı: asıl sürüme göre
#   YAKIN      : tam ve OOS Sharpe farkı ≥ −0,15 ve OOS alfa t farkı ≥ −0,5
#   BELİRGİN KÖTÜ: tam ya da OOS Sharpe farkı < −0,25 ya da OOS alfa t farkı < −1,0
#   arada      : KABUL EDİLEBİLİR (biraz kötü)
dec = []
for _, r in W.iterrows():
    a = W[(W.kural == r.kural) & (W.surum.isin(["ASIL", "ASIL-1/4"]))].iloc[0]
    if r.surum in ("ASIL", "ASIL-1/4"): dec.append(("—", np.nan, np.nan, np.nan)); continue
    ds_t, ds_o = r.tam_sharpe - a.tam_sharpe, r.oos_sharpe - a.oos_sharpe
    dt_o = (r.oos_alfa_t - a.oos_alfa_t) if (pd.notna(r.oos_alfa_t) and pd.notna(a.oos_alfa_t)) else 0.0
    if ds_t >= -0.15 and ds_o >= -0.15 and dt_o >= -0.5: d = "YAKIN"
    elif ds_t < -0.25 or ds_o < -0.25 or dt_o < -1.0: d = "BELIRGIN KOTU"
    else: d = "KABUL EDILEBILIR"
    dec.append((d, round(ds_t, 2), round(ds_o, 2), round(dt_o, 2)))
W["karar"] = [d[0] for d in dec]; W["d_tam_sharpe"] = [d[1] for d in dec]; W["d_oos_sharpe"] = [d[2] for d in dec]; W["d_oos_alfa_t"] = [d[3] for d in dec]
W.to_csv(f"{OUT}/sade_ozet.csv", index=False)

# LOWMOM: sade HV okumasının "kesin pasif" bölgesi (asıl kural aktifken sade HV'nin aldığı en yüksek değer)
_ci = C17.index; _vr = RV.values; _lv = np.log(V.xau_p15 / V.xau_p15.shift(1)).values
HO = pd.Series(np.nan, index=V.index); HU = pd.Series(np.nan, index=V.index)
for i, t in enumerate(V.index):
    j = _ci.searchsorted(t, side="left") - 1; p = V.xau_p15.get(t, np.nan)
    if j > 25 and np.isfinite(p): HO[t] = np.append(LR.values[j - 18:j + 1], math.log(p / C17.values[j])).std(ddof=0) * math.sqrt(365) * 100
    if i > 25:
        rr = np.append(_vr[i - 19:i], _lv[i])
        if np.isfinite(rr).all(): HU[t] = rr.std(ddof=0) * math.sqrt(365) * 100
_act = A["V_LOWMOM_h1"] != 0
PASIF = dict(viop_uzlasma_hv_asil_aktifken_maks=round(float(HU[_act].max()), 2), viop_uzlasma_hv_asil_aktifken_q99=round(float(HU[_act].quantile(0.99)), 2),
             oanda_hv_asil_aktifken_maks=round(float(HO[_act].max()), 2), oanda_hv_asil_aktifken_q99=round(float(HO[_act].quantile(0.99)), 2),
             viop_uzlasma_hv_2026_min=round(float(HU[HU.index >= "2026-01-01"].min()), 2), viop_uzlasma_hv_son=round(float(HU.dropna().iloc[-1]), 2),
             oanda_hv_2026_min=round(float(HO[HO.index >= "2026-01-01"].min()), 2), oanda_hv_son=round(float(HO.dropna().iloc[-1]), 2))
# [DENETİM eki] aynı 'canlı' OANDA HV(20) okuması 2010+ spot günlerinde (VİOP öncesi 2010–2016 dahil). Yukarıdaki maksimumlar yalnız
#   2017-03+ VİOP örneklemidir; 2010–2016'da asıl kural HV(20) %21–25 iken de aktif olmuştur → "kesin pasif" eşiği örnekleme duyarlı.
_HO2 = pd.Series(np.nan, index=SP.index)
for t in SP.index:
    j = _ci.searchsorted(t, side="left") - 1; p = SP.s_p15.get(t, np.nan)
    if j > 25 and np.isfinite(p): _HO2[t] = np.append(LR.values[j - 18:j + 1], math.log(p / C17.values[j])).std(ddof=0) * math.sqrt(365) * 100
_act2 = (LQ < 1 / 3) & _HO2.notna()                                        # asıl kural (genişleyen yüzdelik)
_actb = (LRV * np.sqrt(252) * 100 < asil_thr_now) & _HO2.notna()           # bugünkü sabit eşikle (ileriye dönük durum)
for nm_, msk in (("2010_2016", SP.index < pd.Timestamp("2017-01-01")), ("2010_2026", SP.index >= pd.Timestamp("2010-01-01"))):
    a_ = _act2 & msk
    PASIF[f"oanda_hv_asil_aktifken_maks_{nm_}"] = round(float(_HO2[a_].max()), 2)
    PASIF[f"oanda_hv_ge21_iken_aktif_gun_{nm_}"] = int((_HO2[a_] >= 21).sum())
    PASIF[f"oanda_hv_ge17_iken_aktif_orani_{nm_}"] = round(float(_act2[msk & (_HO2 >= 17)].mean()), 4)
PASIF["oanda_hv_bugunku_esikle_aktifken_maks_2010_2026"] = round(float(_HO2[_actb].max()), 2)
PASIF["bist_vekili_15utc_hv_aktifken_maks_2010_2016"] = round(float(HV15[(LQ < 1 / 3) & (SP.index < pd.Timestamp("2017-01-01"))].max()), 2)   # BIST uzlaşma ≈ 15:10 UTC
PASIF["not_"] = ("viop_*/oanda_* maks ve q99 değerleri yalnız 2017-03+ VİOP günleri; *_2010_2016 / *_2010_2026 anahtarları 2010+ spot günleri (denetim eki). "
                 "OANDA HV(20) ≥ 22 → bugünkü eşikle 2010–2026'da hiç aktif olmadı; 17–22 arası ≈%3–4 olasılıkla aktif; < 17 → betik.")
print("LOWMOM kesin-pasif bölgesi:", PASIF)

# elle kullanılacak sayılar
cur_m = pd.Period("2026-11", "M")
ES = dict(
    lowmom=dict(aciklama="TradingView OANDA:XAUUSD günlük grafik, 'Historical Volatility' uzunluk 20 (TV formülü: 100·stdev_pop(ln C/C[1],20)·√365)",
                yillik_esik_hv={str(y): round(v, 2) for y, v in THR_Y.items() if y >= 2017},
                sabit_esik_2010_2021=round(THR_IS, 2), esik_2010_2026_11=round(THR_NOW, 2),
                asil_rv20_esik_bugun_yillik_252=round(asil_thr_now, 2),
                viop_uzlasma_yillik_esik_hv={str(y): round(v, 2) for y, v in THR15_Y.items() if y >= 2017}, viop_uzlasma_sabit_esik_2010_2021=round(THR15_IS, 2),
                viop_uzlasma_esik_2010_2026_11=round(THR15_NOW, 2), son_hv20_15utc=round(float(HV15.iloc[-1]), 2),
                son_hv20_kapanis=round(float(HV_K.iloc[-1]), 2), son_roc5_kapanis_pct=round(float(ROC5_K.iloc[-1] * 100), 2), son_kapanis_gunu=str(C17.index[-1].date())),
    a4_aylik={str(m): dict(beta=round(b, 3), esik_pct=round(0.43 * sd * 100, 3)) for m, (b, sd) in A4BM.items() if m >= pd.Period("2025-11", "M")},  # VİOP-satır hizası
    e2_aylik={k: {str(m): dict(beta_gld=round(b[0], 3), beta_spy=round(b[1], 3)) for m, b in E2X[k][1].items() if m >= pd.Period("2025-11", "M")} for k in E2X},
    e2_esik_pct={k: round(v[5] * 100, 3) for k, v in E2D.items()}, c1_kaplama_alt_esik_pct=round(lo1 * 100, 3), lowmom_kesin_pasif=PASIF,
)
# [DENETİM eki] elle uygulama notları (sayılar bu çalıştırmanın tablosundan)
_w = W.set_index(["kural", "surum"])
_k = {C_: (_w.loc[(f"ETF-BIRLESIK-KOMISYON-{C_ // 1000}K", "ASIL")], _w.loc[(f"ETF-BIRLESIK-KOMISYON-{C_ // 1000}K", "SADE")]) for C_ in (10000, 25000, 50000)}
_a8a, _a8r = _w.loc[("A8-3_seg_last1h_h5", "ASIL")], _w.loc[("A8-3_seg_last1h_h5", "SAYIM-5MUM-RENK")]
ES["denetim_notlari"] = dict(
    A8_3=(f"17:00 TSİ saatlik mumun RENGİ değil, KAPANIŞI 16:00 mumunun KAPANIŞIYLA karşılaştırılmalı (kural ln(p15/p14)). Renkle sayım Dukascopy'de {_fark8} günde "
          f"farklı ve Sharpe tam {_a8a.tam_sharpe:.2f}→{_a8r.tam_sharpe:.2f}, OOS {_a8a.oos_sharpe:.2f}→{_a8r.oos_sharpe:.2f} (SAYIM-5MUM-RENK satırı); kural çok küçük farklara duyarlı."),
    midas_sabit_komisyon={f"{C_ // 1000}K_USD": dict(asil_oos_sharpe=a.oos_sharpe, sade_oos_sharpe=s.oos_sharpe, asil_oos_alfa_pct=a.oos_alfa_yillik_pct, asil_oos_alfa_t=a.oos_alfa_t,
                                                     sade_oos_alfa_pct=s.oos_alfa_yillik_pct, sade_oos_alfa_t=s.oos_alfa_t, asil_emir_yil=a.emir_gunu_yil, sade_emir_yil=s.emir_gunu_yil)
                          for C_, (a, s) in _k.items()},
    midas_not="Emir başına 1,5 USD (KULLANIM §5) bps maliyetine eklendi. Kademeli dilimler sermayenin 1/15'i kadar küçük emirler üretir; küçük hesapta ASIL ETF planının alfası ücretle erir, SADE plan (yılda ≈200 emir) ayakta kalır.",
    parametre_uyumu="A4 ve E2 aylık sayıları (bu dosya, basit %, ay başı penceresi) parametreler.json'daki haftalık log değerlerinden farklıdır; β ile eşik aynı kaynaktan alınmalı (parametreler.json → denetim.sade_esikler_ile_fark).",
    lowmom_kesin_pasif="OANDA canlı HV(20): ≥ 22 kesin pasif (bugünkü eşikle 2010–2026), 17–22 büyük olasılıkla pasif; yalnız 2017+ örneklemine dayanan 'OANDA ≥ 21 kesin' ifadesi 2010–2016'da 9 aktif günle çürüdü. BIST uzlaşma ≥ 17 kuralı 15:00 UTC spot vekiliyle 2010–2016'da da tuttu (aktifken en yüksek HV %" + f"{PASIF['bist_vekili_15utc_hv_aktifken_maks_2010_2016']:.1f}".replace('.', ',') + ").")
json.dump(ES, open(f"{OUT}/sade_esikler.json", "w"), indent=1, ensure_ascii=False)

cols = ["kural", "surum", "tam_sharpe", "oos_sharpe", "p2022_sharpe", "p2026_sharpe", "oos_sharpe_stres", "bh_oos_sharpe", "oos_alfa_yillik_pct", "oos_alfa_t",
        "tam_alfa_t", "maruziyet", "gidis_donus_yil", "emir_gunu_yil", "karar_uyumu_pct", "aktif_uyum_pct", "pnl_korelasyon", "karar"]
print(W[cols].to_string())
print("LOWMOM eşikleri (TV HV20):", ES["lowmom"])
print("A4 bu ay:", ES["a4_aylik"].get(str(cur_m)), " E2 bu ay:", {k: v.get(str(cur_m)) for k, v in ES["e2_aylik"].items()})
