"""(3) TRALT ile TRMET arasında klasik lead-lag var mı? Günlük veri.
A) Çapraz lag-k (k=1..3) regresyonu: y_t = a + Σ b_k x_{t−k} + Σ c_k y_{t−k} + Σ d_k XU030_{t−k} (+ isteğe bağlı eşzamanlı XU030), NW(5) t.
B) XU030'dan arındırılmış (β250 shift1) getirilerle aynı regresyon (idiyosenkratik öncülük).
C) Göreli yayılım s = r_TRMET − β·r_TRALT öz-korelasyonu (momentum mu?) — spot kapanış ve VİOP uzlaşma ayrı ayrı.
D) Zamanlama: VİOP uzlaşma yayılımı(t+1) ~ spot yayılım(t) (uzlaşma kapanışı geç mi izliyor?).
Dönemler: 2011–16, 2017–21, 2022–26, 2024–26."""
import numpy as np, pandas as pd, statsmodels.api as sm
import kl
from kl import C
cal = kl.use_ext_panel()
R = pd.DataFrame({s: kl.spot_ret_fresh(s) for s in ['TRMET', 'TRALT', 'TRENJ', 'XU030']}).dropna(how='all')
R = R[R.index >= '2010-03-01']
PER = [('2011–16', '2011-01-01', '2016-12-31'), ('2017–21', '2017-01-01', '2021-12-31'), ('2022–26', '2022-01-01', '2026-12-31'),
       ('2024–26', '2024-01-01', '2026-12-31'), ('tümü 2011+', '2011-01-01', '2026-12-31')]


def ols_nw(y, X, lags=5):
    d = pd.concat([y, X], axis=1).dropna()
    if len(d) < 100: return None
    m = sm.OLS(d.iloc[:, 0], sm.add_constant(d.iloc[:, 1:])).fit(cov_type='HAC', cov_kwds={'maxlags': lags})
    return m, len(d)


def resid_xu(y):
    b = kl.beta(y, R.XU030).clip(0, 3)
    return y - b * R.XU030


out = []
for lab_mode, mode in [('ham (gecikmeli XU030 kontrollü)', 'raw'), ('XU030-arındırılmış', 'res')]:
    for ydep, xlead in [('TRMET', 'TRALT'), ('TRALT', 'TRMET')]:
        y0 = R[ydep] if mode == 'raw' else resid_xu(R[ydep]); x0 = R[xlead] if mode == 'raw' else resid_xu(R[xlead])
        for plab, a, b in PER:
            m_ = (R.index >= a) & (R.index <= b)
            X = pd.DataFrame({f'{xlead}_l{k}': x0.shift(k) for k in [1, 2, 3]})
            for k in [1, 2, 3]: X[f'{ydep}_l{k}'] = y0.shift(k)
            if mode == 'raw':
                for k in [1, 2, 3]: X[f'XU_l{k}'] = R.XU030.shift(k)
            r = ols_nw(y0[m_], X[m_])
            if r is None: continue
            m, N = r
            row = dict(mod=lab_mode, y=ydep, x=xlead, donem=plab, N=N)
            for k in [1, 2, 3]:
                row[f'b{k}'] = m.params[f'{xlead}_l{k}']; row[f't{k}'] = m.tvalues[f'{xlead}_l{k}']
                row[f'own{k}'] = m.params[f'{ydep}_l{k}']; row[f'town{k}'] = m.tvalues[f'{ydep}_l{k}']
            # basit çapraz korelasyon lag1
            row['corr_l1'] = y0[m_].corr(x0.shift(1)[m_]); row['corr_0'] = y0[m_].corr(x0[m_])
            out.append(row)
L = pd.DataFrame(out)
pd.set_option('display.width', 250)
print('A/B) Çapraz lag regresyonu: y_t ~ x_{t-1..3} + y_{t-1..3} (+ XU030_{t-1..3}); NW(5) t')
print(L[['mod', 'y', 'x', 'donem', 'N', 'corr_0', 'corr_l1', 'b1', 't1', 'b2', 't2', 'b3', 't3', 'own1', 'town1']].round(3).to_string(index=False))
L.to_csv(kl.OUT + '/kod/res_leadlag.csv', index=False)

# C) yayılım öz-korelasyonu — spot ve VİOP uzlaşma
bTA = kl.beta(R.TRMET, R.TRALT).clip(0.3, 2.0)
s_spot = (R.TRMET - bTA * R.TRALT) / (1 + bTA)
FM, FA = C.fut('TRMET'), C.fut('TRALT')
rM = pd.Series(FM.fwd(cal, 1, 'E0'), index=cal).shift(1)  # t-1 uzlaşma -> t uzlaşma, vade sabit (vade > t)
rA = pd.Series(FA.fwd(cal, 1, 'E0'), index=cal).shift(1)
b_c = bTA.reindex(cal)
s_fut = (rM - b_c * rA) / (1 + b_c)
s_sp_c = s_spot.reindex(cal)
print('\nC) Göreli yayılım s = (r_TRMET − β·r_TRALT)/(1+β) öz-korelasyonu (lag 1, 2, 3) ve D) uzlaşma(t+1) ~ spot(t)')
rows = []
for plab, a, b in PER:
    m_s = (s_spot.index >= a) & (s_spot.index <= b); ss = s_spot[m_s]
    m_f = (cal >= max(pd.Timestamp(a), pd.Timestamp('2019-01-01'))) & (cal <= b)
    sf = s_fut[m_f]; sp = s_sp_c[m_f]
    rows.append(dict(donem=plab, spot_ac1=ss.autocorr(1), spot_ac2=ss.autocorr(2), spot_ac3=ss.autocorr(3), N_spot=int(ss.notna().sum()),
                     fut_ac1=sf.autocorr(1) if sf.notna().sum() > 50 else np.nan, fut_ac2=sf.autocorr(2) if sf.notna().sum() > 50 else np.nan,
                     fut_t1_spot_t=sf.corr(sp.shift(1)) if sf.notna().sum() > 50 else np.nan,
                     spot_t1_fut_t=sp.corr(sf.shift(1)) if sf.notna().sum() > 50 else np.nan,
                     fut_spot_0=sf.corr(sp) if sf.notna().sum() > 50 else np.nan, N_fut=int(sf.notna().sum())))
A = pd.DataFrame(rows); print(A.round(3).to_string(index=False)); A.to_csv(kl.OUT + '/kod/res_spread_ac.csv', index=False)

# E) 3 günlük artık (z3) ile ileri getirinin ayrıştırılması: TRMET mi gidiyor, TRALT mı geri geliyor?
SIG = kl.koza_signal(R, 'TRMET')
z = SIG.z3.reindex(cal); on = (z.abs() > 1.5).fillna(False).values; d = cal[on]; sd = np.sign(z[on].values)
xM = sd * FM.fwd(d, 2, 'E0'); xA = sd * FA.fwd(d, 2, 'E0')
XU = C.fut('XU030'); xX = sd * XU.fwd(d, 2, 'E0')
bM = kl.beta(R.TRMET, R.XU030).clip(0.3, 2).reindex(d).values; bA = kl.beta(R.TRALT, R.XU030).clip(0.3, 2).reindex(d).values
ok = np.isfinite(xM) & np.isfinite(xA) & np.isfinite(xX)
print(f'\nE) Sinyal günleri (örtüşen, n={ok.sum()}), yön uygulanmış 2 günlük VİOP getirileri (bps):')
print(f'   TRMET1! {np.mean(xM[ok]) * 1e4:+.1f} | TRALT1! {np.mean(xA[ok]) * 1e4:+.1f} | XU030D {np.mean(xX[ok]) * 1e4:+.1f} | '
      f'TRMET−β·XU {np.mean((xM - bM * xX)[ok]) * 1e4:+.1f} | TRALT−β·XU {np.mean((xA - bA * xX)[ok]) * 1e4:+.1f}')
print('   (yön: z3>0 iken TRMET AL. TRALT "−β·XU" pozitifse TRALT da aynı yöne gidiyor = TRMET\'i takip etmiyor, çift kazancı TRMET\'in fazlasından)')
# F) TRMET'in kendi 3 günlük XU030-artığı (grup değil) — momentum grup-göreli mi, mutlak mı?
uX = resid_xu(R.TRMET); zX = kl.zk(uX, 3).reindex(cal); onX = (zX.abs() > 1.5).fillna(False).values; dX = cal[onX]; sX = np.sign(zX[onX].values)
xx = sX * (FM.fwd(dX, 2, 'E0') - kl.beta(R.TRMET, R.XU030).clip(0.3, 2).reindex(dX).values * XU.fwd(dX, 2, 'E0'))
print(f'F) TRMET XU030-artığı z3>1,5 (grup yok), TRMET1!−β·XU030D h2: n={np.isfinite(xx).sum()}, ort {np.nanmean(xx) * 1e4:+.1f} bps')
m_, t_, n_ = C.clnw(dX, xx, 2); print(f'   NW t {t_:.2f}')
