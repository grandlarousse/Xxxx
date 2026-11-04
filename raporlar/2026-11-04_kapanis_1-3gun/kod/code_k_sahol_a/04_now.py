"""4) Güncel durum: veri 03.11.2026 kapanışına kadar (Yahoo 02.11 günlük bar + 03.11 regularMarketPrice; VİOP bülteni 03.11 dahil).
z, β, kuralların model pozisyonu, son işlemler, yarın için tetik seviyeleri, kontrat oranı ve 1 mn TL boyutlama örneği."""
import sys; sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_k_sahol_a')
import kl, numpy as np, pandas as pd
kl.use_new_data(); K = kl.signal()
pA, pB = kl.spot_px('SAHOL'), kl.spot_px('AKBNK')
FA, FB = kl.cont('SAHOL', 1), kl.cont('AKBNK', 1)
t = K.index[-1]; print('Son spot günü:', t.date(), ' son VİOP bülteni:', FA.index[-1].date())
print(pd.DataFrame({'SAHOL': pA.c, 'AKBNK': pB.c}).reindex(K.index).join(K[['beta', 'z']]).tail(12).round(4).to_string())
# kuralların model durumu (spot girdiyle; sinyal güncel güne kadar)
cA = pd.Series(16e-4, index=K.index); cB = cA
for nm, kw in {'A bant içi (çıkış |z|<=1,5)': dict(exit_z=1.5), 'C z<1': dict(exit_z=1.0), 'B z<0,5': dict(exit_z=0.5)}.items():
    D, T = kl.run_rule(K.z, K.rA, K.rB, K.beta, cA, cB, **kw)
    last = T.tail(3)[['entry_date', 'exit_date', 'side', 'z_in', 'days', 'open', 'net']].copy(); last['net'] = (1e4 * last['net']).round(0)
    print(f'\n{nm}: model pozisyonu bugün = {D.pos.iloc[-1]:+.0f}; son 3 işlem (spot, bps):'); print(last.to_string())
# yarın için tetik: z_{t+1}(x) = ±1,5 olacak spread hareketi x (= rA - β rB)
S = K.S.values; b1 = float((K.rA.rolling(250, min_periods=125).cov(K.rB) / K.rB.rolling(250, min_periods=125).var()).iloc[-1])  # yarın kullanılacak β (bugüne kadarki veriyle)
def zx(x):
    w = np.r_[S[-59:], S[-1] + x]; return (w[-1] - w.mean()) / w.std(ddof=1)
def solve(target):
    lo, hi = (-0.5, 0.0) if target < 0 else (0.0, 0.5)
    for _ in range(80):
        m = (lo + hi) / 2
        if (zx(m) - target) * (zx(lo) - target) <= 0: hi = m
        else: lo = m
    return (lo + hi) / 2
print(f'\nYarın kullanılacak β = {b1:.4f}')
for tg in [1.5, -1.5, 0.5, -0.5]:
    x = solve(tg)
    print(f'  z_yarın = {tg:+.1f} için spread hareketi x = {100 * x:+.2f}% -> AKBNK sabitken SAHOL {pA.c.iloc[-1] * np.exp(x):.2f} TL ; SAHOL sabitken AKBNK {pB.c.iloc[-1] * np.exp(-x / b1):.2f} TL')
# kontrat oranı ve boyutlama
fa, fb = FA.F.iloc[-1], FB.F.iloc[-1]; print(f'\nÖn vade (devir R=1 kuralıyla tutulacak): {FA.hold.iloc[-1]} {fa:.2f}  {FB.hold.iloc[-1]} {fb:.2f}  vade {FA.expiry.iloc[-1].date()}')
ratio = b1 * fa / fb; print(f'β-ağırlıklı kontrat oranı N_B/N_A = β·F_A/F_B = {ratio:.3f} ; eşit TL oranı = {fa / fb:.3f}')
for cap, risk_unit, lab in [(1e6, 0.09, 'muhafazakâr: tarihsel en kötü işlem ≈ −%9 SAHOL nominali'), (1e6, 0.03, 'orta: OOS 5. yüzdelik işlem kaybı ≈ −%3')]:
    na = int(np.floor(cap * 0.01 / (risk_unit * fa * 100))); nb = int(round(na * ratio))
    nomA, nomB = na * fa * 100, nb * fb * 100; mar = 0.14 * nomA + 0.15 * nomB
    print(f'  {lab}: {na} SAHOL + {nb} AKBNK kontratı; nominal {nomA:,.0f} + {nomB:,.0f} TL; başlangıç teminatı ≈ {mar:,.0f} TL (%{100 * mar / cap:.1f});'
          f' beklenen yıllık (A, 1.189 bps) ≈ {nomA * 0.1189:,.0f} TL; OOS MDD (A, −2.365 bps) ≈ {nomA * -0.2365:,.0f} TL')
