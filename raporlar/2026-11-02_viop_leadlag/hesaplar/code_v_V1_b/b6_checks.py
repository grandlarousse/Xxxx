"""b6: (1) 2000-13 TR olayları yerel taban/trend çıkarılmış; (2) EEM hizalanması plasebosu + EEM olay öncesi stres; (3) ülkeler arası güç: volatilite-ölçekli etki."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vb import *
rng = np.random.default_rng(11)
cal = bist_cal(); N = len(cal)
X = load('XU100.IS'); O = np.log(X.o.reindex(cal).values); C = np.log(X.c.reindex(cal).values)
ev = ev_load(('rating',))
def mk(df):
    df = df.copy(); df['i0'] = [react_idx(cal, a, f) for a, f in zip(df.ann, df.after_close)]
    return df.drop_duplicates('i0').reset_index(drop=True)
post, pre = mk(ev[ev.period == 'post']), mk(ev[ev.period == 'pre'])
wd = lambda i, k: int(cal.searchsorted(cal[i] + pd.Timedelta(days=7 * k)))
print('=== (1) 2000-13 TR olayları: A = c[t0]->c[t+2], yerel taban (±1..6 hafta aynı pencere) ve ±60g trend çıkarılmış ===')
for lab, df in [('PRE 2000-13', pre), ('PRE 2003-13', pre[pre.ann >= '2003-01-01']), ('POST', post)]:
    i0, dr = df.i0.values, df.dir.values
    A = lambda I: C[np.asarray(I) + 2] - C[np.asarray(I)]
    ks = [k for k in range(-6, 7) if k != 0]
    basem = np.array([np.mean([A([wd(i, k)])[0] for k in ks]) for i in i0])
    cc = np.diff(C, prepend=np.nan); mu = np.array([np.nanmean(np.r_[cc[i - 60:i - 5], cc[i + 6:i + 60]]) for i in i0])
    print(fmt(-dr * A(i0), f'{lab} ham')); print(fmt(-dr * (A(i0) - basem), f'{lab} yerel taban')); print(fmt(-dr * (A(i0) - 2 * mu), f'{lab} trend'))
    print(fmt(-dr * (C[i0] - C[i0 - 6]), f'{lab} olay öncesi 5g (kontra işaret; negatif=not yönünde)'))

print('\n=== (2) EEM: TR tarihlerinde hizalanma ne kadar olağandışı? (EEM Pzt açılış->Çar kapanış, TR yönüyle kontra işaret) ===')
e = load('EEM'); eo = np.log(e.o * e.adj / e.c).values; ec = np.log(e.adj).values; ei = e.index
def eemw(dates):
    j = ei.searchsorted(dates); ok = j + 2 < len(ei); out = np.full(len(dates), np.nan); out[ok] = ec[j[ok] + 2] - eo[j[ok]]; return out
d0 = cal[post.i0.values]; dr = post.dir.values
real = np.nanmean(-dr * eemw(d0))
ks = np.r_[-52:-2, 3:53]; pl = []
for b in range(10000):
    dd = d0 + pd.to_timedelta(7 * rng.choice(ks, len(d0)), unit='D'); pl.append(np.nanmean(-dr * eemw(pd.DatetimeIndex(dd))))
pl = np.array(pl); print(f'EEM gerçek {1e4*real:+.1f} bps, plasebo ort {1e4*pl.mean():+.1f}, sd {1e4*pl.std():.1f}, p={(pl>=real).mean():.4f}')
jj = ei.searchsorted(d0)
pre5 = -dr * (ec[jj - 1] - ec[jj - 6]); print(fmt(pre5, 'EEM olay öncesi 5g (kontra işaret; negatif = EM not yönünde hareket)'))
# EEM genel kısa vadeli geri dönüş: her Pzt, önceki 5g'nin tersine, Pzt açılış->Çar kapanış
mon = np.where(ei.dayofweek == 0)[0]; mon = mon[(mon > 6) & (mon + 2 < len(ei))]
gen = -np.sign(ec[mon - 1] - ec[mon - 6]) * (ec[mon + 2] - eo[mon]); print(fmt(gen, 'EEM genel Pzt geri dönüş (tüm Pzt)'))
big = np.abs(ec[mon - 1] - ec[mon - 6]) > 0.03; print(fmt(gen[big], 'EEM genel Pzt geri dönüş |pre5|>%3'))
# XU100 abnormal regression on EEM same window
xu = -dr * (C[post.i0.values + 2] - O[post.i0.values]); em = -dr * eemw(d0)
b = np.polyfit(em, xu, 1); res = xu - b[0] * em; print(f'XU100 ~ EEM olaylar arası regresyon: eğim {b[0]:.2f}, sabit {1e4*b[1]:+.1f} bps'); print(fmt(res, 'XU100 - eğim*EEM (olay-içi regresyon kalıntısı)'))

print('\n=== (3) Güç: volatilite-ölçekli etki (işaretli getiri / önceki 60g 3-günlük sd) ===')
def scaled(c_log, o_log, idx, anns, dirs, open_entry=True):
    out = []
    r = np.diff(c_log, prepend=np.nan)
    for a, d_ in zip(anns, dirs):
        j = idx.searchsorted(a, side='right')
        if j + 2 >= len(idx) or j < 61: out.append(np.nan); continue
        sd3 = np.nanstd(r[j - 60:j]) * np.sqrt(3)
        x = (c_log[j + 2] - (o_log[j] if open_entry else c_log[j])); out.append(-d_ * x / sd3)
    return np.array(out)
tr = scaled(C, O, cal, post.ann.values, post.dir.values); print(fmt(tr / 1e4, 'TR XU100 (birim: SD; "bps" sütunu = SD)'))
E = pd.read_csv(HERE + '/events_xc.csv', parse_dates=['ann'])
MK = {'ZA': '^J203.JO', 'GR': 'GD.AT', 'IT': 'FTSEMIB.MI', 'BR': '^BVSP'}
allx = []
for cty, sym in MK.items():
    d = load(sym); d = d[d.c > 0]; cl = np.log(d.c.values); op = np.log(d.o.where(d.o > 0).values)
    for sc in [1, 0]:
        q = E[(E.country == cty) & (E.sched == sc)]
        if q.empty: continue
        v = scaled(cl, op, d.index, q.ann.values, q.dir.values, open_entry=(cty != 'ZA')); allx += [(cty, sc, x) for x in v]
        print(fmt(v / 1e4, f'{cty} sched={sc} (SD)'))
A_ = pd.DataFrame(allx, columns=['c', 's', 'v'])
v = A_[(A_.s == 1) & (A_.c != 'BR')].v; print(fmt(v / 1e4, 'HAVUZ takvimli ZA+GR+IT (SD)'))
t_, n_ = tstat(v); se = v.std() / np.sqrt(n_)
print(f'TR etkisi {np.nanmean(tr):.2f} SD; havuz {v.mean():.2f} SD (SE {se:.2f}); TR etkisinin havuzda reddi: z = {(np.nanmean(tr) - v.mean())/se:.2f}')
