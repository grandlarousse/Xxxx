"""02: VİOP pay vadelisi (KCHOL, ENKAI) ve XU030 vadelisi: likidite ve 'açılış' fiyatının zamanlaması denetimi.
Soru 1: bültendeki ACILIS FIYATI hangi ana ait? (akşam seansı (önceki gün 16:00 UTC) mı, 06:30 UTC mi?)
Soru 2: KCHOL/ENKAI vadelisinin hacmi, işlem sayısı (likidite) yıllara göre."""
import sys; sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_H45_b')
from blib import *


def front(und):
    df = viop_panel()
    d = df[(df.und == und) & (df['ISLEM SAYISI'] > 0)].copy()
    d = d.sort_values(['date', 'ISLEM HACMI']).groupby('date').tail(1).set_index('date').sort_index()
    out = pd.DataFrame({'Fo': d['ACILIS FIYATI'], 'Fc': d['KAPANIS FIYATI'], 'Fs': d['UZLASMA FIYATI'], 'Fps': d['ONCEKI UZLASMA FIYATI'],
                        'Fvw': d['AGIRLIKLI ORTALAMA FIYAT'], 'Fh': d['EN YUKSEK FIYAT'], 'Fl': d['EN DUSUK FIYAT'],
                        'val': d['ISLEM HACMI'], 'ntr': d['ISLEM SAYISI'], 'oi': d['ACIK POZISYON'], 'code': d['SOZLESME KODU'],
                        'exp': d['exp']})
    out = out[(out.Fo > 0) & (out.Fc > 0) & (out.Fps > 0)]
    return out


if __name__ == '__main__':
    tur, tui, tun = us_lag('TUR')
    for und in ('KCHOL', 'ENKAI', 'XU030'):
        F = front(und)
        spot = bist(und) if und != 'XU030' else bist('XU030')
        j = F.join(spot, how='inner')
        j['Fgap'] = np.log(j.Fo / j.Fps)
        j['Fintra'] = np.log(j.Fc / j.Fo)
        j['Fvwret'] = np.log(j.Fs / j.Fvw)
        j['spot_o_vs_Fo'] = np.log(j.o / j.Fo)
        print(f'\n=== {und} front vadeli: {F.index.min().date()} .. {F.index.max().date()}  gün {len(F)}')
        g = j.groupby(j.index.year)
        tab = pd.DataFrame({
            'gün': g.size(),
            'medyan_hacim_mnTL': g['val'].median() / 1e6,
            'medyan_işlem#': g['ntr'].median(),
            'medyan_AP': g['oi'].median(),
            'corr(Fgap,spotgap)': g.apply(lambda x: x['Fgap'].corr(x['gap'])),
            'corr(Fgap,TUR-1)': g.apply(lambda x: x['Fgap'].corr(tur.reindex(x.index))),
            'corr(spotgap,TUR-1)': g.apply(lambda x: x['gap'].corr(tur.reindex(x.index))),
            'corr(Fintra,spotintra)': g.apply(lambda x: x['Fintra'].corr(x['intra'])),
            'med|ln(o/Fo)|bps': g['spot_o_vs_Fo'].apply(lambda x: 1e4 * x.abs().median()),
            'HL/2 bps(Corwin~)': g.apply(lambda x: 1e4 * np.log(x.Fh / x.Fl).median() / 2),
        })
        print(tab.round(3).to_string())
        if und == 'XU030':
            # 2024-11-19 sonrası vs öncesi
            for a, b in [('2017', '2024-11-18'), ('2024-11-19', '2027')]:
                jj = j[(j.index >= a) & (j.index <= b)]
                print(f'  {a}..{b}: corr(Fgap,spotgap) {jj.Fgap.corr(jj.gap):.3f}  corr(Fgap,TUR-1) {jj.Fgap.corr(tur.reindex(jj.index)):.3f}')
