"""(3) Pay vadelisi kapanış baz sapması — kesitsel L/S ve tek bacak; bağımsız yeniden hesap.
b = ln(F_son işlem / S_kapanış) (ön vade, vadeye ≥3 gün), sapma a = b − medyan60(b)_{t−1}. Kesitsel: en yüksek %20 SAT, en düşük %20 AL.
Kontroller: E0/E1/E2; E1−E0 ayrıştırması (son işlem − uzlaşma); son işlem 'bayat' mı (illikit); 2022-09-23 sonrası; A sınıfı; maliyet."""
from curlib import *
cal = vcal(); FW = pd.read_parquet(RES + '/_fwd_cache.parquet')
L = pd.read_csv(S + '/out/y_viop_likidite.csv'); L = L[L.und != 'XU030']
U = list(L.und); cls = dict(zip(L.und, L.liq_class)); cost = dict(zip(L.und, L.rt_cost_small_bps))
B = {}; TR = {}; STC = {}
for u in U:
    F = fut(u); fc, jc = F.front_series('close', 3); fs, _ = F.front_series('settle', 3); tr, _ = F.front_series('trades', 3)
    try: sc = spot(u)['c'].reindex(cal)
    except Exception: continue
    b = np.log(fc / sc)
    B[u] = b.where(jc.eq(jc.shift(1)) | True); TR[u] = tr; STC[u] = np.log(fs / fc)
B = pd.DataFrame(B); TR = pd.DataFrame(TR); STC = pd.DataFrame(STC)
A = B - B.rolling(60, min_periods=40).median().shift(1)
A = A.where(A.abs() < 0.08)  # aşırı uçlar (temettü/bedelsiz günleri) dışarı
def fwmat(h, e): return pd.DataFrame({u: FW[f'{u}|{h}|{e}'] for u in A.columns})
out = []
def ls(name, mask, h, e, q=0.2, per_leg_cost=None):
    a = A.where(mask)
    rk = a.rank(axis=1, pct=True); n = a.notna().sum(axis=1)
    ok = n >= 10
    lo = (rk <= q) & ok.values[:, None]; hi = (rk > 1 - q) & ok.values[:, None]
    R = fwmat(h, e)
    long_ = R.where(lo).mean(axis=1); short_ = R.where(hi).mean(axis=1)
    x = (long_ - short_) / 2  # sermaye başına (iki bacak toplam 1)
    d = x.dropna().index; xv = x.dropna().values
    o = summary(d, xv, h); reg('baz', name, h, e, o)
    # iki bacak, her bacak gidiş-dönüş maliyeti: sermaye başına ort. maliyet
    out.append(f'{name:46s} {e} h{h}: {fmt(o)}')
    return x, o
base = TR.fillna(0) >= 0
liqA = pd.DataFrame({u: pd.Series(cls.get(u) == 'A', index=cal) for u in A.columns})
post = pd.DataFrame({u: pd.Series(cal >= '2022-09-23', index=cal) for u in A.columns})
act = TR.fillna(0) >= 1000
for nm, m in [('tümü', base), ('işlem≥1000', act), ('A sınıfı', liqA & act), ('2022-09-23+ ', post & act), ('2022-09-23+ A sınıfı', post & liqA & act)]:
    for h in [1, 3]:
        for e in ['E1', 'E0', 'E2']:
            ls(f'Kesitsel L/S {nm}', m, h, e)
# E1 kazancının ne kadarı t günü içindeki (uzlaşma − son işlem) farkından?
a = A.where(post & liqA & act); rk = a.rank(axis=1, pct=True); n = a.notna().sum(axis=1)
lo = (rk <= 0.2) & (n >= 10).values[:, None]; hi = (rk > 0.8) & (n >= 10).values[:, None]
stc_ls = (STC.where(lo).mean(axis=1) - STC.where(hi).mean(axis=1)) / 2
print('2022-09+ A sınıfı: L/S içinde log(uzlaşma_t/son işlem_t) payı (bps):', round(float(stc_ls.mean() * 1e4), 1))
# son işlem fiyatının uzlaşmadan sapması büyüklüğü (tüm sinyal hücreleri, medyan bps)
print('Medyan |log(uzlaşma/son işlem)| sinyal hücrelerinde (bps):', round(float(np.nanmedian(np.abs(STC.where(lo | hi).values)) * 1e4), 1))
# tek bacak |z|>1,5, A sınıfı 2022-09+, E1/E0/E2, h1
Z = A / A.rolling(120, min_periods=60).std().shift(1)
for nm, m in [('A sınıfı 2022-09+', post & liqA & act), ('tümü işlem≥1000', act)]:
    zz = Z.where(m); on = zz.abs() > 1.5
    st = on.stack(); st = st[st]; dts = st.index.get_level_values(0); uu = st.index.get_level_values(1)
    sd = -np.sign(np.array([zz.at[d_, u_] for d_, u_ in zip(dts, uu)]))
    for e in ['E1', 'E0', 'E2']:
        R = fwmat(1, e); x = sd * np.array([R.at[d_, u_] for d_, u_ in zip(dts, uu)])
        o = summary(dts, x, 1); reg('baz', f'Tek bacak |z|>1,5 {nm}', 1, e, o)
        c_ = np.nanmean([cost[u_] for u_ in uu])
        out.append(f'Tek bacak |z|>1,5 {nm:20s} {e} h1 (ort. maliyet {c_:.1f} bps): {fmt(o)}')
for o_ in out: print(o_)
save('baz')
