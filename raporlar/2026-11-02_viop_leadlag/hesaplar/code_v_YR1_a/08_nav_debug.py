"""Kaynak nav_KCHOL.parquet ile kendi NAV'ımı karşılaştır; farkın kaynağını bul."""
import sys; sys.path.insert(0, HERE := '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_YR1_a')
exec(open(HERE + '/07_nav.py').read().split("if __name__ == '__main__':")[0])
src = pd.read_parquet(OUT + '/code_y_grup/nav_KCHOL.parquet')
navr = nav_ret(W0); pos, z = signal(navr)
cmp_ = pd.concat([src['nav'].rename('nav_src'), navr.rename('nav_me'), src['h'].rename('h_src'), K['cc'].rename('h_me'), src['z250'].rename('z_src'), z.rename('z_me')], axis=1)
cmp_ = cmp_[cmp_.index >= '2014-01-01']
print('corr nav', cmp_[['nav_src', 'nav_me']].corr().iloc[0, 1].round(4), ' corr h', cmp_[['h_src', 'h_me']].corr().iloc[0, 1].round(4), ' corr z', cmp_[['z_src', 'z_me']].corr().iloc[0, 1].round(4))
dif = cmp_[(cmp_.nav_src - cmp_.nav_me).abs() > 1e-4]; print('nav farklı gün', len(dif)); print(dif.head(10).round(4).to_string())
difh = cmp_[(cmp_.h_src - cmp_.h_me).abs() > 1e-4]; print('h farklı gün', len(difh)); print(difh.head(10).round(4).to_string())
print('kaynakta eksik tarih (benim takvimde var):', len(cmp_[cmp_.z_src.isna() & cmp_.z_me.notna()]))
ps = positions(src['z250'].reindex(cal), 1.0)
agree = (ps == pos)[cal >= '2014-01-01'].mean(); print('pozisyon uyumu', round(agree, 3))
for lab, pp in [('kaynak z', ps), ('benim z', pos)]:
    sim = simulate(pp, tg, ti, tc, pd.Series(2.0, index=cal), 'open', 8)
    for per, lo, hi in [('IS', '2014-01-01', SPLIT), ('OOS', SPLIT, '2027-01-01')]:
        st = summarize(sim, lo, hi, active='act_p1'); print(lab, per, round(st['mean_bps'], 2), round(st['t_act'], 2), st['n_act'])
# kaynak hedef serilerini de birebir: kaynak 'persistent' satır düşürme mantığı
def persistent_src(zz, gap, intra, cost_bps, legs, thr=1.0):
    df = pd.concat([zz.rename('z'), gap.rename('g'), intra.rename('i')], axis=1).dropna(subset=['g', 'i'])
    p = (-np.sign(df['z'])).where(df['z'].abs() > thr, 0.0).fillna(0.0)
    p1 = p.shift(1).fillna(0); p2 = p.shift(2).fillna(0)
    pnl = p2 * df['g'] + p1 * df['i'] - (cost_bps / 1e4) / 2 * legs * (p1 - p2).abs()
    return pnl, p1
for lab, zz in [('kaynak z', src['z250']), ('benim z', z)]:
    pnl, p1 = persistent_src(zz, tg, ti, 8, 2)
    for per, lo, hi in [('IS', '2014-01-01', SPLIT), ('OOS', SPLIT, '2027-01-01')]:
        pp = pnl[(pnl.index >= lo) & (pnl.index < hi)]; a = p1.reindex(pp.index) != 0
        m, t, n = nwt(pp[a]); print('src-persistent', lab, per, round(1e4 * m, 2), round(t, 2), n)
