import csv,sys
out=sys.argv[1]
# ad, aile, S(ses), T(teknik), A(aralık), E(erişim, Türkiye), not
R=[
("Blok flüt","Düdüklü",1,2,1,1,"Okul çalgısı, Türkiye'de her yerde"),
("Tin whistle (İrlanda düdüğü)","Düdüklü",1,1,2,2,"6 delik; Türkiye'de birkaç mağazada"),
("Okarina","Kap",1,2,2,1,"Ses kolay, temiz akort zor"),
("Kızılderili flütü","Düdüklü",1,1,2,4,"Pentatonik hazır; Türkiye'de satıcı bulunamadı"),
("Dilli kaval","Düdüklü",1,3,3,2,"Kavalın düdüklü kardeşi; 7+1 delik"),
("Frula / svirala","Düdüklü",1,2,2,4,"Balkan, 6 delik"),
("Fluier (Romanya)","Düdüklü",1,2,2,4,"6 delik; 'caval' adlı büyük tipi var"),
("Sopilka (Ukrayna)","Düdüklü",1,2,2,4,"6-10 delik"),
("Shvi (Ermenistan)","Düdüklü",1,3,3,4,"7+1 delik"),
("Txistu / galoubet","Düdüklü",1,3,4,5,"3 delik, tek el; nota için aşırı üfleme"),
("Souravli (Yunanistan)","Düdüklü",1,2,2,5,"Yunan düdüklü çoban flütü, 2 oktav"),
("Pinkillo (And)","Düdüklü",2,2,3,5,"6 delik"),
("Suling (Endonezya)","Düdüklü",2,3,3,5,"Halka düdük, 4-6 delik"),
("Salamuri (Gürcistan)","Düdüklü",2,3,3,5,"8+1 delik"),
("Dvoyanka (Bulgaristan)","Düdüklü",2,4,3,5,"Çift gövde, iki ses birden"),
("Koncovka (Slovakya)","Doğuşken",2,2,5,5,"Deliksiz; nota nefes ve uçla seçilir"),
("Seljefløyte (Norveç)","Doğuşken",2,2,5,5,"Deliksiz söğüt flütü"),
("Fujara (Slovakya)","Doğuşken",2,3,5,5,"~1,6-2 m, 3 delik"),
("Tilinkó / tilinca","Doğuşken",5,2,5,5,"Deliksiz ve düdüksüz"),
("İrlanda flütü, anahtarsız","Yan",3,2,3,4,"Parmaklar tin whistle ile aynı"),
("Fife / pífano","Yan",3,2,3,4,"6 delik; 3. oktav zor"),
("Dizi (Çin)","Yan",3,2,3,4,"Titreşen zar (dimo) bakımı ister"),
("Bansuri (Hindistan)","Yan",3,3,3,4,"Yarım delik; bas boylarda el açıklığı"),
("Shinobue (Japonya)","Yan",3,3,3,5,"Şenlik flütü"),
("Sogeum (Kore)","Yan",3,3,3,5,"Daegeum'un küçüğü, zarsız"),
("İrlanda flütü, anahtarlı","Yan",3,3,3,5,"Kromatik notalar anahtarla"),
("Venu (Güney Hindistan)","Yan",3,4,3,5,"8 delik, Karnatik süslemeler"),
("Ryuteki (Japonya)","Yan",3,3,4,5,"Üst oktav kararsız"),
("Daegeum (Kore)","Yan",4,3,4,5,"Büyük, zarlı"),
("Nohkan (Japonya)","Yan",4,4,5,5,"İç daralma (nodo), her flüt farklı"),
("Danso (Kore)","Çentikli",4,1,2,5,"4+1 delik, pentatonik"),
("Quena / quenacho (And)","Çentikli",4,2,3,4,"Eliptik çentik; üst ses zor"),
("Xiao (Çin)","Çentikli",4,2,3,4,"Kısa xiao daha zor"),
("Shakuhachi / hocchiku","Çentikli",5,4,4,4,"Kesik ağız (utaguchi); perde baş açısıyla"),
("Washint (Etiyopya)","Kenar",5,1,2,5,"4 delik, pentatonik"),
("Kurai (Başkurt, Tatar)","Kenar",5,2,4,5,"2-7 delik, 3 oktav"),
("Tsuur / choor / Kazak sybyzgy","Kenar",5,2,4,5,"Diş-dil-dudakla, boğaz sesiyle"),
("Floyera / flogera (Yunanistan)","Kenar",5,3,4,4,"Kavalın kısa, basit kuzeni"),
("Bilûr (Kürt, Güneydoğu Anadolu)","Kenar",5,3,4,3,"~80 cm, 7-8+1 delik, ağızlıksız"),
("Kawala (Mısır, Arap)","Kenar",5,3,4,5,"Ney benzeri, 6 delik, arka delik yok"),
("Blul (Ermenistan)","Kenar",5,3,4,5,"Eğik tutulur"),
("Kargı düdüğü (Türkiye)","Kenar",5,3,4,5,"Uzun kamış flüt; kaynak zayıf"),
("Tzamara (Yunanistan, Epir)","Kenar",5,3,5,5,"Uzun kaval tipi"),
("Dilsiz kaval (Türkiye, Balkanlar)","Kenar",5,4,5,2,"2 oktav + beşli; komalar"),
("Ney (Türk neyi)","Kenar",5,5,4,2,"Makam komaları; başpare yardımcı"),
("Xun (Çin)","Kap",3,2,2,5,"Kil; düdüksüz"),
("Nai (Romanya)","Pan",3,3,3,4,"Kavisli; nota boyun hareketiyle"),
("Siku / zampoña (And)","Pan",3,3,2,4,"İki sıra; geleneksel olarak iki kişi"),
("Miskal / müsikar","Pan",3,3,3,5,"Osmanlı pan flütü, bugün nadir"),
("Kuvytsi (Ukrayna)","Pan",3,2,2,5,"Sınıflaması tartışmalı"),
]
W={'ana':(.5,.2,.2,.1),'esit':(.25,.25,.25,.25),'erisimsiz':(.55,.25,.2,0)}
def sc(r,w): return round(sum(a*b for a,b in zip(r[2:6],w)),2)
rows=[]
for r in R: rows.append(dict(ad=r[0],aile=r[1],S=r[2],T=r[3],A=r[4],E=r[5],**{k:sc(r,w) for k,w in W.items()},notu=r[6]))
for k in W:
    for i,x in enumerate(sorted(rows,key=lambda x:(x[k],x['S'],x['ad']))): x['sira_'+k]=i+1
rows.sort(key=lambda x:x['sira_ana'])
with open(out,'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
n=len(rows)
def spear(a,b): 
    d=sum((x['sira_'+a]-x['sira_'+b])**2 for x in rows); return round(1-6*d/(n*(n*n-1)),3)
print('N',n,'spearman ana-esit',spear('ana','esit'),'ana-erisimsiz',spear('ana','erisimsiz'))
for x in rows:
    flag=' '.join(f"{k}:{x['sira_'+k]}" for k in ('esit','erisimsiz') if abs(x['sira_'+k]-x['sira_ana'])>=6)
    print(f"{x['sira_ana']:2} {x['ana']:.2f} S{x['S']}T{x['T']}A{x['A']}E{x['E']} {x['ad']} [{x['aile']}] {flag}")
