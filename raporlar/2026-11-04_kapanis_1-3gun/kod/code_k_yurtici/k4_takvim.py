"""(d) Takvim: ay sonu/ay başı (= pay vadelisi vade sonu), XU030 vade ayları, tatil/bayram öncesi-sonrası, BIST30 dönem değişikliği — kapanıştan kapanışa.
Enstrümanlar: XU030 vadelisi (uzlaşma), 47 pay vadelisi eşit ağırlıklı sepet (günlük ortalama), spot XU100 (2005+, kıyas; koşulsuz h-günlük ortalama çıkarılır).
Giriş: olay günü göreli kapanış/uzlaşma (k), tutma h. Vadeli getirisi taşıma (faiz) içermez -> doğrudan fazla getiri.
Takvim bayrakları: out/code_y_akis/_cal_flags.parquet (me: ayın son işlem günü; pre_hol: ardından ≥1 hafta içi kapalı gün; pre_rel: ≥2 gün (dini bayram arifesi))."""
from klib import *
C = ctx(); vcal = C['vcal']; scal = C['scal']
CF = pd.read_parquet(S + '/out/code_y_akis/_cal_flags.parquet')
CF.index = pd.to_datetime(CF.index)
def ev_dates(flag): return CF.index[CF[flag].astype(bool)]
# sepet: 47 pay vadelisi günlük eşit ağırlık (yalnız f0_h)
Fd = {h: C['F'][f'f0_{h}'][[u for u in VIOP47 if u in C['F'][f'f0_{h}'].columns]].mean(axis=1) for h in H}
Xf = {h: C['F'][f'f0_{h}']['XU030'] for h in H}
SF = {h: C['SF'][h]['XU100'] for h in H}
out = []
def run(name, dates, h, inst):
    if inst == 'XU030F': s = Xf[h]; cal = vcal; ise = V_IS_END; costs = [3, 8]
    elif inst == 'SSF47': s = Fd[h]; cal = vcal; ise = V_IS_END; costs = [8, 15]
    else:
        s = SF[h] - SF[h].rolling(500, min_periods=200).mean().shift(h + 1); cal = scal; ise = S_IS_END; costs = [3, 8]
    dd = pd.DatetimeIndex(dates); dd = dd[dd.isin(cal)]
    tr = pd.DataFrame({'date': dd, 'ret': s.reindex(dd).values})
    st = trade_stats(tr, 'ret', h=h, is_end=ise, costs=costs)
    if inst != 'SSF47' and st.get('n', 0): st['net8'] = st['gross'] - costs[0]; st['net15'] = st['gross'] - costs[1]
    reg('d_takvim', name, inst, 'E0', h, st)
    out.append(f'{name:28s} {inst:7s} h{h} {fmt(st)}')
ME = ev_dates('me'); PH = ev_dates('pre_hol'); PR = ev_dates('pre_rel')
PHo = PH.difference(PR)  # dini bayram dışı tatil öncesi
for inst in ['XU030F', 'SSF47', 'XU100x']:
    cal = vcal if inst != 'XU100x' else scal
    for k in [-3, -2, -1, 0]:
        for h in H:
            if k + h < 0: continue
            run(f'ay sonu ME{k:+d} giriş', shift_date(ME, k, cal), h, inst)
    for k, hs in [(-2, [1, 2]), (-1, [1, 2, 3]), (0, [1, 2, 3])]:
        for h in hs:
            run(f'dini bayram arife{k:+d}', shift_date(PR, k, cal), h, inst)
            run(f'diğer tatil öncesi{k:+d}', shift_date(PHo, k, cal), h, inst)
# XU030 vade ayları (çift aylar) vs diğer aylar: ME-1 -> h2
MEe = ME[ME.month % 2 == 0]; MEo = ME[ME.month % 2 == 1]
for h in [1, 2, 3]:
    run('XU030 vade ayı ME-1', shift_date(MEe, -1, vcal), h, 'XU030F')
    run('XU030 vadesiz ay ME-1', shift_date(MEo, -1, vcal), h, 'XU030F')
for o in out: print(o)
# ---- BIST30 dönem değişikliği (6 çeyrek; VİOP47'deki giren/çıkanlar) ----
sys.path.insert(0, S + '/out/code_y_akis'); from index_events import EV
rows = []
for e in EV:
    for key, sg in [('BIST30_in', 1), ('BIST30_out', -1), ('BIST50_in', 1), ('BIST50_out', -1)]:
        for u in e.get(key, []):
            if u in VIOP47: rows.append(dict(und=u, q=e['q'], react=pd.Timestamp(e['react']), eve=pd.Timestamp(e['eff_eve']), side=sg, idx=key))
IE = pd.DataFrame(rows); print('\nendeks olayları (VİOP47):', len(IE)); print(IE.to_string())
out2 = []
for lab, base, sh in [('tepki günü kapanışından', 'react', 0), ('tepki+1', 'react', 1), ('arife-3', 'eve', -3), ('arife kapanışından (sonrası)', 'eve', 0)]:
    for h in [1, 2, 3, 5]:
        ev = IE.copy(); ev['date'] = shift_date(ev[base], sh, vcal)
        for hedge in [False, True]:
            ev['ret'] = vectorized_fut(ev, h, 'E0', hedge=hedge)
            st = trade_stats(ev, 'ret', h=h, is_end=V_IS_END)
            reg('d_takvim', f'BIST30/50 değişikliği {lab}', 'VIOP' + ('_hedge' if hedge else ''), 'E0', h, st)
            out2.append(f'BIST30/50 {lab:30s} {"hedge" if hedge else "ham  "} h{h} {fmt(st)}')
for o in out2: print(o)
D = save_registry('d_takvim'); print('test sayısı', len(D))
