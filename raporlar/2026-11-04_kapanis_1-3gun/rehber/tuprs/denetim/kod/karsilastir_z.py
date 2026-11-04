"""DENETİM: bağımsız z (z_bagimsiz.py) <-> günlük betik (sinyal_tuprs.compute, CANLI Yahoo) <-> araştırma (cl.py + c1_ref mantığı, eski veri)
<-> kurucunun cl_t.signal_z. Son 300 BIST günü. Ayrıca takvim ve 'after' eşlemesi denetimi."""
import sys, os, importlib.util, numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
D = S + "/out/rehber/tuprs/denetim"
sys.path.insert(0, D + "/kod")
import z_bagimsiz as zb

def load_mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

Z, R = zb.build()
mine = Z["z"]
cal = Z.index; last300 = cal[-300:]
out = []
def cmp(lab, other):
    o = other.reindex(last300); m = mine.reindex(last300)
    both = o.notna() & m.notna()
    s1 = np.where(m.abs() > 1, np.sign(m), 0); s2 = np.where(o.abs() > 1, np.sign(o), 0)
    ok = both.values
    line = (f"{lab:38s} ortak {int(both.sum()):3d}/300 | yalnız birinde dolu {int((o.notna() != m.notna()).sum()):2d} | maks|Δz| {np.nanmax(np.abs((o - m)[both])):.2e} | "
            f"sinyal eşleşme {np.mean(s1[ok] == s2[ok]) * 100:.1f}% (tüm 300 gün, boş=0: {np.mean(s1 == s2) * 100:.1f}%)")
    print(line); out.append(line)
    diff = last300[(o.notna() != m.notna()).values]
    if len(diff): print("   farklı dolu günler:", [str(d.date()) for d in diff][:10])

# 1) günlük betik, canlı Yahoo
st = load_mod("sinyal_tuprs", S + "/out/rehber/tuprs/sinyal_tuprs.py")
now = pd.Timestamp.now(tz="UTC")
data = {s: st.yahoo_daily(s) for s in st.MEM + [st.MKT]}
Rs = st.compute(data, pd.Timestamp("2026-11-04"), now)
cmp("günlük betik (canlı Yahoo, 6 yıl)", Rs["z"])
# takvim
scal = st.bist_takvim(pd.Timestamp("2021-01-01"), pd.Timestamp("2026-11-04"))
vcal = cal[(cal >= "2021-01-01")]
print("betik takvimi - VİOP takvimi (2021+):", [str(d.date()) for d in scal.difference(vcal)], "| VİOP - betik:", [str(d.date()) for d in vcal.difference(scal)])
# 2) araştırma (orijinal cl.py + orijinal veri, 30.10.2026'ya kadar)
sys.path.insert(0, S + "/out/code_k_dis-suruculer_curut")
import cl
rm = cl.lret("^GSPC", "adj"); RS = []
for m in zb.MEM:
    r = cl.lret(m, "adj"); b = cl.roll_beta(r, rm.reindex(r.index), 250, 100); RS.append((r - b * rm.reindex(r.index)).rename(m))
df = pd.concat(RS, axis=1); P = df.mean(axis=1).where(df.notna().sum(axis=1) >= 3)
Pb_r = cl.to_bist(P, "after"); zr = cl.zscale(Pb_r, 250, 100)
cmp("araştırma cl.py (eski veri, -30.10)", zr)
zold = pd.read_parquet(S + "/out/rehber/tuprs/veri/z_research_old.parquet")["z"]
cmp("araştırma z (kaydedilmiş)", zold)
# 3) kurucunun cl_t
ct = load_mod("cl_t", S + "/out/rehber/tuprs/kod/cl_t.py")
zt, Pbt, _, _ = ct.signal_z()
cmp("kurucu cl_t.signal_z (yeni veri)", zt)
# 4) tam dönem (2017+) bağımsız vs araştırma
a = mine.reindex(zr.index); m = a.notna() & zr.notna()
print(f"\nTam dönem bağımsız vs araştırma: ortak {int(m.sum())}, maks|Δz| {np.abs(a[m] - zr[m]).max():.3e}; yalnız birinde dolu: {int((a.notna() != zr.notna()).sum())}")
dd = zr.index[(a.notna() != zr.notna()).values]
print("   ilk farklı günler:", [str(d.date()) for d in dd[:12]])
# araştırma to_bist'in ilk-gün toplama artefaktı
print("araştırma Pb ilk 3:", Pb_r.dropna().head(3).round(4).to_dict(), "| bağımsız:", Z["P"].reindex(Pb_r.index).head(3).round(4).to_dict())
print("araştırma z ilk geçerli gün:", zr.first_valid_index().date(), "| bağımsız:", mine.reindex(zr.index).first_valid_index().date())
big = (a[m] - zr[m]).abs() > 1e-6
print("tam dönem |Δz|>1e-6 olan gün:", int(big.sum()), "son:", str(zr[m][big].index.max().date()) if big.any() else "-")
s1 = np.sign(a[m]) * (a[m].abs() > 1); s2 = np.sign(zr[m]) * (zr[m].abs() > 1)
print("tam dönem sinyal eşleşme:", round(float((s1 == s2).mean()) * 100, 2), "%; farklı gün:", int((s1 != s2).sum()), [str(d.date()) for d in s1.index[(s1 != s2).values]][:10])
# 5) tatil/eşleme örnekleri
for d in ["2026-09-08", "2026-01-20", "2026-02-17", "2026-10-30", "2026-07-06", "2026-05-26", "2026-06-22", "2025-11-28", "2026-04-06"]:
    d = pd.Timestamp(d)
    if d in Z.index: print(f"   {d.date()} ({d.day_name()[:3]}): ABD günleri [{Z.at[d, 'abd_gunleri']}] P={Z.at[d, 'P']:.4f} z={Z.at[d, 'z']:.3f}")
    else: print(f"   {d.date()}: BIST günü değil")
pd.DataFrame({"bagimsiz": mine, "betik": Rs["z"].reindex(cal), "arastirma": zr.reindex(cal), "cl_t": zt.reindex(cal)}).loc[last300].to_csv(D + "/sonuc/z_karsilastirma_son300.csv")
open(D + "/sonuc/log_karsilastir_z.txt", "w").write("\n".join(out) + "\n")
