"""(c) Takvim: haftanın günü, ay dönümü, ay mevsimselliği, tatil öncesi/sonrası, FOMC, CPI, NFP, aylık opsiyon vadesi (3. Cuma),
COMEX OG altın opsiyon vadesi, Aralık vergi-zararı ve Ocak etkisi (madenciler).
Kurgu: 'getiri günü' maskesi M (gün D'nin kapanıştan kapanışa getirisi). Giriş = D'den önceki işlem günü kapanışı (takvim önceden bilinir).
FOMC 14:00 ET (2009-2012: 14:15; 2011-12 basın toplantılı 12:30) -> karar anı 15:00 ET'den ÖNCE: FOMC günü getirisi giriş = önceki gün kapanışı.
FOMC sonrası tepki sinyali: FOMC günü spot hareketi (kapanış t-1 -> 15:00 ET t) bilinir.
CPI/NFP 08:30 ET (açılıştan önce) -> giriş = önceki gün kapanışı; yayım günü 15:00 ET hareketi sonrası sinyal olarak.
Olay takvimleri: out/a3_takvim_olay/events_*.csv (2009+). 2008 için FOMC elle (federalreserve.gov tarihleri), CPI/NFP 2008 yok -> olay testleri 2009+.
"""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e1_etf_zaman_takvim")
from e1_common import *
reset("c_")
EV = f"{S}/out/a3_takvim_olay"
TG = ["GLD", "GDX", "GDXJ", "SLV"]
pd.set_option("display.width", 250)
rows = []

def rd_test(fam, name, M, t, h=1, note="", start=None):
    """M: getiri günü maskesi (gün D). Giriş günü sinyali s_t = M_{t+1}. h=1: D günü getirisi; h>1: D..D+h-1."""
    s = M.reindex(IDX).fillna(False).astype(float).shift(-1)
    y = fwd(R[t], h)
    if start is not None: s = s[s.index >= start]; y = y[y.index >= start]
    s = s.where(y.notna())
    st = rstats(s, y, h)
    tid = f"{fam}|{t}|{name}|h{h}"; reg(fam, tid, name, h, st, note)
    on = y[s == 1]; off = y[s == 0]
    rows.append(dict(family=fam, etf=t, test=name, h=h, n_olay=int(s.sum()), ort_olay_bps=round(on.mean() * 1e4, 1), ort_diger_bps=round(off.mean() * 1e4, 1),
                     fark_bps=round((on.mean() - off.mean()) * 1e4, 1), isabet=round((on > 0).mean(), 3), t=round(st["t"], 2), t_is=round(st["t_is"], 2), t_oos=round(st["t_oos"], 2),
                     t_22=round(st["t_22"], 2) if pd.notna(st.get("t_22")) else None, yrs=f"{st['yrs_same_sign']}/{st['yrs']}",
                     ort_olay_oos_bps=round(on[on.index > IS_END].mean() * 1e4, 1), ort_diger_oos_bps=round(off[off.index > IS_END].mean() * 1e4, 1)))
    return st

ix = pd.Series(IDX, index=IDX)
wd = ix.dt.dayofweek
ym = ix.dt.to_period("M")
first_of_m = ym != ym.shift(1); last_of_m = ym != ym.shift(-1)
pos_in_m = ix.groupby(ym).cumcount() + 1; pos_from_end = ix.groupby(ym).cumcount(ascending=False) + 1
# tatiller: hafta içi olup NYSE'nin kapalı olduğu günler (plansız kapanışlar ayrı)
bd = pd.bdate_range(IDX.min(), IDX.max()); closed = bd.difference(IDX)
UNSCHED = pd.DatetimeIndex(["2012-10-29", "2012-10-30", "2018-12-05", "2025-01-09"])
hol = closed.difference(UNSCHED)
nxt = ix.shift(-1); prv = ix.shift(1)
pre_hol = pd.Series([any((h_ > d) and (h_ < n_) for h_ in hol[(hol > d) & (hol < d + pd.Timedelta(days=5))]) if pd.notna(n_) else False for d, n_ in zip(IDX, nxt)], index=IDX)
post_hol = pre_hol.shift(1).fillna(False).astype(bool)
# 3. Cuma (aylık opsiyon vadesi; NYSE tatilse önceki gün)
third_fri = []
for p in ym.unique():
    days = pd.date_range(p.start_time, p.end_time); fr = days[days.dayofweek == 4][2]
    third_fri.append(fr if fr in IDX else IDX[IDX < fr][-1])
third_fri = pd.DatetimeIndex(third_fri)
opex_day = pd.Series(IDX.isin(third_fri), index=IDX)
wk = ix.dt.to_period("W-SUN")
opex_wk = pd.Series(wk.isin(wk[opex_day.values].unique()), index=IDX)
post_opex_wk = pd.Series(wk.isin((wk[opex_day.values] + 1).unique()), index=IDX)
# olaylar
fomc = pd.read_csv(f"{EV}/events_fomc.csv", parse_dates=["date"]); fomc = fomc[fomc.scheduled]
F08 = pd.DatetimeIndex(["2008-01-30", "2008-03-18", "2008-04-30", "2008-06-25", "2008-08-05", "2008-09-16", "2008-10-29", "2008-12-16"])
fomc_d = pd.DatetimeIndex(sorted(set(fomc.date) | set(F08)))
cpi = pd.DatetimeIndex(pd.read_csv(f"{EV}/events_us_cpi.csv", parse_dates=["date"]).date); nfp = pd.DatetimeIndex(pd.read_csv(f"{EV}/events_us_nfp.csv", parse_dates=["date"]).date)
cmx = pd.read_csv(f"{EV}/events_comex.csv", parse_dates=["og_expiry", "gc_fnd"])
og = pd.DatetimeIndex(cmx.og_expiry.dropna()); fnd = pd.DatetimeIndex(cmx.gc_fnd.dropna())
def M(dates): return pd.Series(IDX.isin(dates), index=IDX)
def shiftM(m, k): return m.shift(k).fillna(False).astype(bool)   # k>0: olaydan k gün SONRA
E09 = pd.Timestamp("2009-01-01")

for t in TG:
    # haftanın günü (getiri günü)
    for d_, nm in enumerate(["Pzt", "Sal", "Car", "Per", "Cum"]): rd_test("c_dow", f"getiri_gunu={nm}", wd == d_, t)
    # ay dönümü
    rd_test("c_tom", "TOM(son1+ilk3)", (pos_from_end == 1) | (pos_in_m <= 3), t)
    rd_test("c_tom", "ayin_ilk_gunu", first_of_m, t); rd_test("c_tom", "ayin_son_gunu", last_of_m, t)
    # ay mevsimselliği
    for m_ in range(1, 13): rd_test("c_month", f"ay={m_:02d}", ix.dt.month == m_, t)
    # tatil
    rd_test("c_hol", "tatil_oncesi_gun", pre_hol, t); rd_test("c_hol", "tatil_sonrasi_gun", post_hol, t)
    # opsiyon vadesi (hisse/ETF aylık) ve COMEX OG
    rd_test("c_opex", "opex_haftasi", opex_wk, t); rd_test("c_opex", "opex_cumasi", opex_day, t); rd_test("c_opex", "opex_sonrasi_hafta", post_opex_wk, t)
    ogm = M(og); win_pre = ogm | shiftM(ogm, -1) | shiftM(ogm, -2)
    rd_test("c_og", "COMEX_OG_vade[-2..0]", win_pre, t, start=E09); rd_test("c_og", "COMEX_OG_vade[+1..+2]", shiftM(ogm, 1) | shiftM(ogm, 2), t, start=E09)
    rd_test("c_og", "GC_ilk_bildirim[-1..0]", M(fnd) | shiftM(M(fnd), -1), t, start=E09)
    # FOMC / CPI / NFP: olay günü getirisi (giriş önceki gün kapanışı), h=1,3,5 ; FOMC öncesi 'drift' (olaydan önceki gün)
    for h in [1, 3, 5]:
        rd_test("c_fomc", "FOMC_gunu(giris_onceki_kapanis)", M(fomc_d), t, h)
        rd_test("c_cpi", "CPI_gunu", M(cpi), t, h, start=E09); rd_test("c_nfp", "NFP_gunu", M(nfp), t, h, start=E09)
    rd_test("c_fomc", "FOMC_oncesi_gun", shiftM(M(fomc_d), -1), t)
    rd_test("c_fomc", "FOMC_sonrasi_gun", shiftM(M(fomc_d), 1), t)
    # Aralık vergi zararı / Ocak etkisi
    rd_test("c_taxloss", "Aralik_1-20", (ix.dt.month == 12) & (ix.dt.day <= 20), t)
    rd_test("c_taxloss", "Aralik_son_7_islem_gunu", (ix.dt.month == 12) & (pos_from_end <= 7), t)
    rd_test("c_taxloss", "Ocak_ilk_10_islem_gunu", (ix.dt.month == 1) & (pos_in_m <= 10), t)

C = pd.DataFrame(rows); C.to_csv(f"{O}/c_takvim_testleri.csv", index=False)
print(C.sort_values("t", key=abs, ascending=False).head(45).to_string())
print("takvim testi sayısı:", len(C))

# Olay günü tepkisi sonrası sinyal (FOMC/CPI/NFP günü 15:00 ET'ye kadarki spot hareketi -> sonraki h gün): yalnız altın ETF'leri (GLD) + GDX
ev_rows = []
for t in ["GLD", "GDX", "SLV"]:
    mv = p15("GLD" if t != "SLV" else "SLV") - np.log(D["c_GLD" if t != "SLV" else "c_SLV"]).shift(1)   # gün t 15:00 ET'ye kadar hareket (altın/gümüş)
    for nm, dd in [("FOMC", fomc_d), ("CPI", cpi), ("NFP", nfp)]:
        m = M(dd)
        for h in [1, 3, 5]:
            x = mv.where(m)
            st = rstats(x, fwd(R[t], h), h); reg("c_evreact", f"c_evreact|{t}|{nm}|h{h}", f"{nm} günü 15:00 ET hareketi -> sonrası", h, st, "IC>0 devam, <0 dönüş")
            ev_rows.append(dict(etf=t, olay=nm, h=h, n=st["n"], ic=round(st["ic"], 3), t=round(st["t"], 2), t_is=round(st["t_is"], 2) if pd.notna(st.get("t_is")) else None,
                                t_oos=round(st["t_oos"], 2) if pd.notna(st.get("t_oos")) else None, yrs=f"{st.get('yrs_same_sign')}/{st.get('yrs')}"))
EVR = pd.DataFrame(ev_rows); EVR.to_csv(f"{O}/c_olay_tepki_sonrasi.csv", index=False); print(EVR.to_string())

# Takvim maskeleri kaydet (strateji ve sağlamlık için)
masks = dict(tom=(pos_from_end == 1) | (pos_in_m <= 3), first=first_of_m, pre_hol=pre_hol, opex_wk=opex_wk, fomc=M(fomc_d), cpi=M(cpi), nfp=M(nfp),
             jan10=(ix.dt.month == 1) & (pos_in_m <= 10), dec20=(ix.dt.month == 12) & (ix.dt.day <= 20), og_pre=win_pre, mon=wd == 0, fri=wd == 4)
pd.to_pickle(masks, f"{O}/c_masks.pkl")
