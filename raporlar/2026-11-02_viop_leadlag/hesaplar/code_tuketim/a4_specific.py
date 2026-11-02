"""A4: Hipoteze özel derin testler.
 (a) ULKER-kakao: aylık/çeyreklik ufuk, 0..6 ay gecikme, TL bazlı kakao, 2023-24 kakao rallisi rejimi
 (b) AEFES-RUB / KZT yıllara göre kısmi korelasyon (Rusya konsolidasyon rejimi: 2018 JV, Eki-2023 geçici yönetim, 1.1.2025 konsolidasyon dışı)
 (c) Olay çalışmaları: Rusya/AB InBev Efes, Mısır devalüasyonları (BIMAS), TÜFE açıklama günleri (perakende)
 (d) Banka/faiz rotasyonu: XBANK kısmi korelasyon; yurt içi gıda-perakende faktörü
Çıktı: a4_*.csv + konsol"""
from common import *
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
out = {}
xu = R("XU100"); fx = R("TRY=X")
# ---------- (a) kakao ----------
cc = zero_mask(R("CC=F")); ul = R("ULKER")
df = pd.concat([ul.rename("ul"), xu.rename("m"), fx.rename("fx"), cc.fillna(0).rename("cc"), zero_mask(R("SB=F")).fillna(0).rename("sb"),
                zero_mask(R("ZW=F")).fillna(0).rename("zw"), zero_mask(R("ZL=F")).fillna(0).rename("zl")], axis=1)
df = df[df.index >= "2008-01-01"].dropna(subset=["ul", "m"])
mo = df.resample("ME").sum(); mo = mo[mo.index < "2026-11-01"]
mo["ul_rel"] = mo["ul"] - mo["m"]; mo["ul_usd"] = mo["ul"] - mo["fx"]; mo["cc_tl"] = mo["cc"] + mo["fx"]
rows = []
for drv in ["cc", "cc_tl", "sb", "zw", "zl"]:
    for k in range(0, 7):
        for tgt in ["ul_rel", "ul_usd"]:
            c, t, n = nwcorr(mo[tgt], mo[drv].shift(k), lags=3)
            cis = nwcorr(win(mo[tgt], None, SPLIT), mo[drv].shift(k), lags=3)[0]; coos = nwcorr(win(mo[tgt], SPLIT), mo[drv].shift(k), lags=3)[0]
            rows.append({"driver": drv, "lag_m": k, "target": tgt, "corr": c, "t": t, "n": n, "c_IS": cis, "c_OOS": coos})
A = pd.DataFrame(rows); A.to_csv(CODE + "/a4_cocoa_monthly.csv", index=False)
print("ULKER aylık (2008+) - kakao/şeker/buğday/soya yağı, gecikmeli; |t|>=2 olanlar:")
print(A[A.t.abs() >= 2].round(3).to_string())
print("kakao lag0..3 özeti:"); print(A[(A.driver.isin(["cc", "cc_tl"]))].pivot_table(index=["driver", "lag_m"], columns="target", values=["corr", "t"]).round(3).to_string())
# çeyreklik 12 aylık kakao değişimi vs ULKER göreli (örtüşmesiz yıllık)
yr = df.resample("YE").sum(); yr["rel"] = yr["ul"] - yr["m"]
print("Yıllık: ULKER-XU100 vs kakao (USD log):"); print(yr[["rel", "cc", "sb", "zw"]].round(3).to_string())
print("yıllık corr rel~cc:", round(yr["rel"].corr(yr["cc"]), 3), " rel~cc(t-1 yıl):", round(yr["rel"].corr(yr["cc"].shift(1)), 3))
# kakao rejimi: 2023-01..2024-12 ralli, 2025-01..2026-10 çöküş
for a_, b_ in [("2023-01-01", "2024-12-31"), ("2024-01-01", "2024-12-31"), ("2025-01-01", "2026-10-30")]:
    x = df[(df.index >= a_) & (df.index <= b_)]
    print(f"Rejim {a_}..{b_}: kakao kum. {100*x.cc.sum():.0f}% (log), ULKER-XU100 kum. {100*(x.ul-x.m).sum():.1f}%, ULKER-MGROS(perakende) {100*(x.ul-R('MGROS').reindex(x.index)).sum():.1f}%, günlük kısmi corr(ul,cc|m)={ll.partial_corr(x.ul, zero_mask(R('CC=F')).reindex(x.index), [x.m])[0]:.3f}")
# büyük kakao hareketleri (|r|>=6%) sonrası ULKER gün-içi
dd = DEC("ULKER"); XD = DEC("XU100")
big = cc.shift(1)
for thr in [0.05, 0.08]:
    up = big >= thr; dn = big <= -thr
    for lab, m_ in [("up", up), ("dn", dn)]:
        x = (dd["intra"] - XD["intra"])[m_.reindex(dd.index).fillna(False)].dropna()
        x2 = sum((ul - xu).shift(-k) for k in range(0, 5))[m_.reindex(ul.index).fillna(False)].dropna()
        print(f"kakao_t-1 {lab} >= {thr:.0%}: n={len(x)} ULKER göreli intra ort {1e4*x.mean():.1f}bps t={x.mean()/(x.std()/np.sqrt(max(len(x),1))):.2f} | t..t+4 göreli cc {1e4*x2.mean():.1f}bps t={x2.mean()/(x2.std()/np.sqrt(max(len(x2),1))):.2f}")
# ---------- (b) AEFES - RUB / KZT / CCOLA yıllara göre ----------
ae = R("AEFES"); rows = []
for drv in ["RUB=X", "KZT=X", "CCOLA", "UAH=X", "CARL-B.CO", "HEIA.AS", "ABI.BR", "^STOXX"]:
    b = R(drv); b = zero_mask(b) if not ll.is_bist(ll.T(drv)) else b
    for y in range(2010, 2027):
        a = ae[ae.index.year == y]
        pc, n = ll.partial_corr(a, b, [xu])
        pcu, _ = ll.partial_corr(a - fx, b, [xu - fx])
        rows.append({"driver": drv, "year": y, "pc": pc, "pc_usd": pcu, "n": n})
Y = pd.DataFrame(rows); Y.to_csv(CODE + "/a4_aefes_by_year.csv", index=False)
print("AEFES yıllara göre kısmi korelasyon (|XU100):"); print(Y.pivot_table(index="year", columns="driver", values="pc").round(3).to_string())
# Avrupa bira emsalleri: Avrupa piyasası kontrolü ekle
for drv in ["CARL-B.CO", "HEIA.AS", "ABI.BR", "CCH.L", "BUD", "KO", "KOF"]:
    b = zero_mask(R(drv)); ctl = zero_mask(R("^STOXX")) if not drv in ("BUD", "KO", "KOF") else zero_mask(R("^GSPC"))
    a = win(ae, START)
    p1 = ll.partial_corr(a, b, [xu])[0]; p2 = ll.partial_corr(a, b, [xu, ctl])[0]; p3 = ll.partial_corr(a, b, [xu, ctl, fx])[0]
    p2i = ll.partial_corr(win(a, None, SPLIT), b, [xu, ctl])[0]; p2o = ll.partial_corr(win(a, SPLIT), b, [xu, ctl])[0]
    print(f"AEFES~{drv}: pc|XU100={p1:.3f}  pc|XU100+yerel endeks={p2:.3f} (IS {p2i:.3f} / OOS {p2o:.3f})  +TRY={p3:.3f}")
for s in ["ULKER", "BIMAS", "MGROS", "SOKM", "CCOLA"]:
    for drv in ["CARL-B.CO", "HEIA.AS", "ABI.BR", "NESN.SW", "MDLZ", "CCH.L"]:
        b = zero_mask(R(drv)); ctl = zero_mask(R("^STOXX")) if drv != "MDLZ" else zero_mask(R("^GSPC"))
        print(f"  {s}~{drv}: pc|XU100+yerel={ll.partial_corr(win(R(s), START), b, [xu, ctl])[0]:.3f}", end="")
    print()
# ---------- (c) olay çalışmaları ----------
def car(stock, date, w=(0, 2), bench="XU100"):
    a = R(stock); m = R(bench); d = pd.Timestamp(date)
    idx = a.index[a.index >= d]
    if len(idx) == 0: return np.nan, np.nan
    i0 = a.index.get_loc(idx[0])
    seg = a.iloc[i0 + w[0]: i0 + w[1] + 1] - m.iloc[i0 + w[0]: i0 + w[1] + 1]
    return 1e4 * (a.iloc[i0] - m.iloc[i0]), 1e4 * seg.sum()
EVT = [
 ("AEFES", "2018-03-22", "AB InBev Efes Rusya/Ukrayna JV kuruluşu (yaklaşık tarih; duyuru 2017-08)"),
 ("AEFES", "2022-02-24", "Rusya'nın Ukrayna işgali"),
 ("AEFES", "2022-03-01", "Rusya yaptırım haftası"),
 ("AEFES", "2022-04-22", "AB InBev JV payını satma kararı (duyuru)"),
 ("AEFES", "2023-10-17", "Putin kararnamesi: AB InBev Efes Rusya varlıklarına geçici yönetim (16.10.2023 akşam)"),
 ("AEFES", "2023-12-26", "AB InBev payının Efes'e devri anlaşması (KAP)"),
 ("AEFES", "2024-08-01", "Rusya onayı reddi haberi (Ağustos 2024; yaklaşık)"),
 ("AEFES", "2024-10-01", "Yeniden yapılandırma: Rusya Efes'e, Ukrayna AB InBev'e (Ekim 2024; yaklaşık)"),
 ("BIMAS", "2016-11-03", "Mısır pound serbest bırakıldı"),
 ("BIMAS", "2022-03-21", "EGP devalüasyonu ~%14"),
 ("BIMAS", "2022-10-27", "EGP devalüasyonu ~%15"),
 ("BIMAS", "2023-01-04", "EGP devalüasyonu"),
 ("BIMAS", "2024-03-06", "EGP devalüasyonu ~%38 + faiz artışı"),
 ("ULKER", "2024-04-19", "Kakao zirvesi (~12.000$/t, 2024-04-19 civarı)"),
 ("ULKER", "2024-12-18", "Kakao ikinci zirve (~12.900$/t, Ara-2024)"),
]
er = []
for s, d, desc in EVT:
    a0, a3 = car(s, d, (0, 2)); a5 = car(s, d, (0, 4))[1]
    er.append({"stock": s, "date": d, "event": desc, "AR_t0_bps": a0, "CAR_t0_t2_bps": a3, "CAR_t0_t4_bps": a5})
ER = pd.DataFrame(er)
# referans: hissenin günlük göreli getiri std'si
for s in ER.stock.unique():
    sd = (R(s) - xu).loc["2014":].std() * 1e4; ER.loc[ER.stock == s, "daily_rel_sd_bps"] = sd
ER.to_csv(CODE + "/a4_events.csv", index=False); print(ER.round(0).to_string())
# TÜFE açıklama günleri: her ayın 3'ü veya sonraki ilk BIST günü (10:00 TSİ). |göreli getiri| ve varyans oranı
cal = R("XU100").dropna().index
cpi = []
for y in range(2014, 2027):
    for m_ in range(1, 13):
        d = pd.Timestamp(y, m_, 3)
        if d > pd.Timestamp("2026-10-30"): break
        nx = cal[cal >= d]
        if len(nx): cpi.append(nx[0])
cpi = pd.DatetimeIndex(cpi)
rr = []
for s in STOCKS + ["CCOLA", "XBANK"]:
    rel = win(R(s) - xu, START).dropna()
    isc = rel.index.isin(cpi)
    a, b = rel[isc], rel[~isc]
    from scipy import stats as st
    lev = st.levene(a, b)
    rr.append({"stock": s, "n_cpi": len(a), "mean_rel_cpi_bps": 1e4 * a.mean(), "t_mean": a.mean() / (a.std() / np.sqrt(len(a))), "sd_cpi_bps": 1e4 * a.std(), "sd_other_bps": 1e4 * b.std(),
               "var_ratio": (a.std() / b.std()) ** 2, "levene_p": lev.pvalue, "mean_abs_cpi": 1e4 * a.abs().mean(), "mean_abs_other": 1e4 * b.abs().mean()})
CP = pd.DataFrame(rr); CP.to_csv(CODE + "/a4_cpi_days.csv", index=False); print("TÜFE günleri:"); print(CP.round(3).to_string())
# ---------- (d) banka rotasyonu + yurt içi tüketim faktörü ----------
xb = R("XBANK"); rows = []
for s in STOCKS + ["CCOLA"]:
    a = win(R(s), START)
    pc = ll.partial_corr(a, xb, [xu])[0]; pci = ll.partial_corr(win(a, None, SPLIT), xb, [xu])[0]; pco = ll.partial_corr(win(a, SPLIT), xb, [xu])[0]
    yrs = [ll.partial_corr(a[a.index.year == y], xb, [xu])[0] for y in range(2014, 2027) if a[a.index.year == y].notna().sum() > 100]
    rows.append({"stock": s, "pc_xbank": pc, "pc_IS": pci, "pc_OOS": pco, "yrs_neg": float(np.mean(np.array(yrs) < 0)), "n_yrs": len(yrs)})
XB = pd.DataFrame(rows); XB.to_csv(CODE + "/a4_xbank.csv", index=False); print("XBANK kısmi (|XU100):"); print(XB.round(3).to_string())
# yurt içi tüketim faktörü: diğer 3 perakende/gıda hissesinin ort. (XU100 artığı) ile kısmi korelasyon
G = ["BIMAS", "MGROS", "SOKM", "ULKER", "AEFES", "CCOLA"]
res = {g: resid(win(R(g), START), xu)[0] for g in G}
RS = pd.DataFrame(res)
print("XU100-artık korelasyon matrisi (2014+; SOKM 2018+):"); print(RS.corr().round(3).to_string())
print("XU100-artık korelasyon matrisi OOS 2021+:"); print(RS[RS.index >= SPLIT].corr().round(3).to_string())
