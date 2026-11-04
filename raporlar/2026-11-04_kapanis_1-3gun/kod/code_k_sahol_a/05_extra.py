"""5) Ek: Kural A için zaman sınırı (max 3/5/10), MDD tarihleri, long/short ayrımı, maliyet başabaş, son 12 ay."""
import sys; sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_k_sahol_a')
import kl, numpy as np, pandas as pd, importlib.util
spec = importlib.util.spec_from_file_location('c2', kl.HERE + '/02_c2c.py'); c2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)
IS = ('2014-01-01', '2021-01-01'); OOS = ('2021-01-01', '2027-01-01')
z, ra, rb, beta, cA, cB, rl = c2.fut_inputs(8, 1)
for nm, kw in [('A', dict(exit_z=1.5)), ('A|max3', dict(exit_z=1.5, maxN=3)), ('A|max5', dict(exit_z=1.5, maxN=5)), ('A|max10', dict(exit_z=1.5, maxN=10)), ('C', dict(exit_z=1.0)), ('C|max10', dict(exit_z=1.0, maxN=10)), ('B', dict(exit_z=0.5))]:
    Ds, Ts = kl.run_rule(*c2.spot_inputs(8)[:6], **kw); Df, Tf = kl.run_rule(z, ra, rb, beta, cA, cB, roll=rl, **kw)
    si, so = kl.summ(Ds, Ts, *IS), kl.summ(Df, Tf, *OOS)
    cum = Df[Df.index >= OOS[0]].net.cumsum(); trough = (cum - cum.cummax()).idxmin(); peak = cum[:trough].idxmax()
    T = Tf[(Tf.entry_date >= OOS[0]) & ~Tf.open]
    ls = T.groupby('side').net.agg(['size', lambda x: 1e4 * x.mean()]).round(1).to_dict('index')
    l12 = kl.summ(Df, Tf, '2025-11-01', '2027-01-01')
    # başabaş maliyet: brüt ort / (1+β) her bacak gidiş-dönüş (yaklaşık; devirler hariç)
    be = 1e4 * T.gross.mean() / (1 + T.beta.abs().mean()) / (1 + T.nroll.mean())
    print(f"{nm:8s} IS {si['net_bps']:6.1f} (t {si['t_trade']:.2f}) | OOS {so['net_bps']:6.1f} (t {so['t_trade']:.2f}, günlük t {so['t_daily']:.2f}) ort.tutma {so['hold_mean']:.1f} | "
          f"MDD {so['mdd_bps']:.0f} bps {peak.date()}→{trough.date()} | long/short {ls} | son 12 ay n={l12.get('n')} net {l12.get('net_bps', np.nan):.0f} | başabaş maliyet ≈ {be:.0f} bps/bacak")
