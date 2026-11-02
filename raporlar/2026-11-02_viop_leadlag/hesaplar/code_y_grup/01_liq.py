from gx import *
syms = sorted(set([a for p in PAIRS for a in p[:2]] + TVF + ['XU100','XU030','XHOLD']))
rows = []
for s in syms:
    try:
        d = px(s); r = R(s)
        tl, z = liq(s); tl3, z3 = liq(s, '2021-01-01')
        rows.append(dict(sym=s, first=d.index[0].date(), last=d.index[-1].date(), n=int(r.notna().sum()), tl_med_1y_mn=round(tl, 1), zero_1y=round(z, 3), tl_med_21_mn=round(tl3, 1), zero_21=round(z3, 3), name=ll.meta(S(s)).get('longName')))
    except Exception as e:
        rows.append(dict(sym=s, name='ERR ' + str(e)[:60]))
df = pd.DataFrame(rows); df.to_csv(HERE + '/res_liq.csv', index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 200)
print(df.to_string())
