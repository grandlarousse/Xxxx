import numpy as np, pandas as pd
import lb

def setup(a='SAHOL', b='AKBNK', fa=None, fb=None, bw=250, zw=60, viop=True):
    df = lb.pair_frame(a, b)
    sig = lb.zsig(df, bw=bw, zw=zw)
    out = dict(sig=sig)
    if viop:
        FA = lb.fut_series(fa or a); FB = lb.fut_series(fb or b)
        cal = FA.index.intersection(FB.index)
        FA = FA.loc[cal]; FB = FB.loc[cal]
        V = pd.DataFrame(index=cal)
        V['z'] = sig.z.reindex(cal); V['beta'] = sig.beta.reindex(cal).ffill()
        for k, F in (('A', FA), ('B', FB)):
            V['F0' + k] = F.F0; V['dF' + k] = F.dF; V['roll' + k] = F.roll.fillna(False).astype(bool)
            V['code' + k] = F.code; V['val' + k] = F.val
        out['V'] = V
    # spot vekili: sabit miktar adj fiyat
    P = pd.DataFrame(index=sig.index)
    P['z'] = sig.z; P['beta'] = sig.beta
    P['F0A'] = sig.pa; P['dFA'] = sig.pa.shift(-1) - sig.pa
    P['F0B'] = sig.pb; P['dFB'] = sig.pb.shift(-1) - sig.pb
    P['rollA'] = False; P['rollB'] = False
    P['cA'] = sig.ca; P['cB'] = sig.cb
    out['P'] = P
    return out


def bist_tick(p):
    # BIST pay fiyat adimi (2014+ tablo, yaklasik)
    p = np.asarray(p, float)
    t = np.where(p < 20, 0.01, np.where(p < 50, 0.02, np.where(p < 100, 0.05, np.where(p < 250, 0.10, np.where(p < 500, 0.25, np.where(p < 1000, 0.5, 1.0))))))
    return t


def run(X, z=None, entry=1.5, exit_=1.5, maxhold=None, fixed=None, cA=8.0, cB=8.0, tick=True, spot=False, ratio='beta', nS=None,
        side='both', zcol='z'):
    zz = (X[zcol] if z is None else z).values
    tr = lb.gen_trades(zz, entry, exit_, maxhold=maxhold, fixed=fixed, side=side)
    idx = X.index
    if spot:
        # spot vekili: tik = BIST fiyat adimi, adj olcegine cevrilmis (tik/fiyat oraninda)
        tA = 0.01; tB = 0.01
        T, d = _eval_spot(tr, X, cA, cB, tick, ratio, nS)
    else:
        T, d = lb.eval_trades(tr, idx, X.F0A.values, X.dFA.values, X.F0B.values, X.dFB.values, X.rollA.values,
                              X.rollB.values, X.beta.values, cA=cA, cB=cB, tick=tick, ratio=ratio, nS=nS)
    return T, d


def _eval_spot(tr, X, cA, cB, tick, ratio, nS):
    # tik orani ham fiyat uzerinden: X'te 'cA','cB' (ham kapanis) olmali
    idx = X.index
    tickA = bist_tick(X.cA.values) / X.cA.values * X.F0A.values  # adj olceginde tik
    tickB = bist_tick(X.cB.values) / X.cB.values * X.F0B.values
    res = []; daily = np.zeros(len(idx))
    FA0, dFA, FB0, dFB, beta = X.F0A.values, X.dFA.values, X.F0B.values, X.dFB.values, X.beta.values
    for (i0, i1, s) in tr:
        if i1 >= len(idx): continue
        b = beta[i0]; a0 = FA0[i0]; b0 = FB0[i0]
        if np.isnan(b) or np.isnan(a0) or np.isnan(b0): continue
        w = b if ratio == 'beta' else 1.0
        sa = np.nansum(dFA[i0:i1]) / a0; sb = np.nansum(dFB[i0:i1]) / b0
        gross = s * (sa - w * sb) * 1e4
        one = cA + w * cB + ((tickA[i0] / a0 + w * tickB[i0] / b0) * 1e4 if tick else 0)
        net = gross - one
        for k in range(i0, i1):
            daily[k + 1] += s * (np.nan_to_num(dFA[k]) / a0 - w * np.nan_to_num(dFB[k]) / b0) * 1e4
        daily[i0] -= one / 2; daily[i1] -= one / 2
        res.append(dict(d0=idx[i0], d1=idx[i1], sgn=s, hold=i1 - i0, beta=b, w=w, gross=gross, cost=one, net=net, nroll=0, bad=False))
    return pd.DataFrame(res), pd.Series(daily, index=idx)


def line(T, d, a, b):
    o = lb.summ(T, d, pd.Timestamp(a), pd.Timestamp(b))
    if o['n'] == 0: return 'n=0'
    return (f"n={o['n']:3d} ({o.get('per_year', np.nan):4.1f}/y) net={o['mean_net']:7.1f} med={o['med_net']:6.1f} "
            f"t={o['t']:5.2f} tNW={o.get('t_nw', np.nan):5.2f} hit={o['hit']:.2f} hold={o['hold_mean']:.1f}/{o['hold_med']:.0f} "
            f"worst={o['worst']:.0f} DD={o.get('maxdd', np.nan):.0f} ann={o.get('ann_bps', np.nan):.0f}")
