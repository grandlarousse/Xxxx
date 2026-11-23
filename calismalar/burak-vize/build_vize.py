"""Burak'ın vize ödevine eklemeleri ve MLA dipnotlarını uygular (sürüm 2: doğrulama ve eleştiri sonrası).

Kullanım: python3 -I build_vize.py <cikti_isaretli.docx> <cikti_temiz.docx>
Markup: {+eklenen+} sarı, {~düzeltilen~} turkuaz, [[fn:dipnot metni]], *italik*, **kalın**.
Arşiv belgesi dipnotları (BCA ile başlayanlar) işaretli sürümde yeşil vurgulanır.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docxedit import Doc

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'odev', 'Burak_vize.docx')
KS = 'Kurnaz Şahin, “Cumhuriyetin Kuruluşuna”'
KM = 'Kurnaz Şahin, “Erken Cumhuriyet”'
KT = 'Kurnaz Şahin, *Osmanlı’dan Cumhuriyet’e*'
ZC29 = '*TBMM Zabıt Ceridesi*, D. 3, c. 12'
IBK = 'İnhisar Beyiyeleri Kanunu'

# ---------------------------------------------------------------- ÖZET / ABSTRACT
OZET = (
    'Bu araştırmada Osmanlı Devleti’nin son dönemlerinde, Kurtuluş Savaşı sırasında ve sonrasında kurulan '
    'Türkiye Cumhuriyeti’nde gaziler ve engelliler için hangi kuruluşların kurulduğu ve ne gibi sosyal hizmetler '
    'sunulduğu sorusunun cevabı aranmıştır. Savaş {~yıllarında ve~} sonrasında dernekler ve cemiyetler kurularak '
    'gazilerle engelliler için gelir toplanmaya çalışılmıştır; bunu yaparken gerek yardım adı altında gerek sinema veya '
    'satış yoluyla elde edilen gelirlerle yardımcı olunmaya çalışılmıştır. Bunun dışında devlet, Osmanlı Devleti’nden '
    'kalan Darülaceze, Kızılay gibi kurumları yeniden düzenleyip bu amaç uğruna faal hâle getirerek eğitim, bakım ve '
    'hizmet sunmayı sağlamıştır. Kurtuluş Savaşı’nda yaralanıp gazi ve malul duruma düşenler için neler yapılmaya '
    'çalışıldığı ve işgalden kurtuluş sürecinde ve 1923’te Lozan Antlaşması imzalandıktan sonra hangi sağlık '
    'kuruluşlarının ve yardım cemiyetlerinin faal olduğu incelenmiştir. Gazilere ve engellilere yardımcı olabilmek '
    'adına sağlık kuruluşları bir politika belirleyerek ilerlemiş, kurulan cemiyetler ise gazilere ve malul insanlara '
    'yardım edebilmek için {~birtakım~} girişimlerle gelir elde etmeye çalışmıştır. {+1929’daki Meclis encümeni '
    'mazbatasına göre yardımın muhatabı yaklaşık 120.000 şehit yetimi ve dulu ile 14.000 kadar harp malulüydü. '
    '1938-1963 tarihli arşiv kararları ise sağır, dilsiz ve körlere yönelik devlet desteğinin yanında bu alandaki '
    'sivil derneklerin de güçlendiğine işaret etmektedir. +}Bu araştırmada {~Cumhuriyet Arşivi’ndeki 1938-1963 tarihli '
    'altı İcra Vekilleri Heyeti ve Bakanlar Kurulu kararı, *Resmî Gazete* ve TBMM zabıtları ile konuyla ilgili '
    'akademik çalışmalar~} kullanılmıştır.'
)

ABSTRACT = (
    '{~This study examines the institutions and services established for veterans and persons with disabilities in '
    'the late Ottoman period, during the Turkish War of Independence and in the Republic of Türkiye. During and after '
    'the wars, associations and charitable societies tried to raise funds for veterans and persons with disabilities '
    'through donations, cinema screenings and sales. The state, in turn, reorganized institutions inherited from the '
    'Ottoman period, such as the Red Crescent (Hilal-i Ahmer, later Kızılay) and Darülaceze, and provided care, '
    'education and services. The study examines what was done for those wounded and disabled in the War of '
    'Independence and which health institutions and charitable societies remained active during the liberation from '
    'occupation and after the Treaty of Lausanne (1923). According to the 1929 report of the parliamentary National '
    'Defence Committee, the aid concerned some 120,000 orphans and widows of fallen soldiers and about 14,000 disabled '
    'veterans. Council of Ministers decrees dated 1938-1963 indicate that, alongside state support for deaf, mute and '
    'blind people, civil associations in this field also grew stronger. The study draws on six decrees held in the '
    'Republic Archives, the Official Gazette, the minutes of the Grand National Assembly of Türkiye and the relevant '
    'scholarly literature.~}'
)

# ---------------------------------------------------------------- GİRİŞ
GIRIS = (
    'Osmanlı İmparatorluğu yükseliş döneminde çok geniş topraklara hâkim olmuş ve bu toprakları başarılı bir şekilde '
    'uzun yıllar boyunca idare etmeyi {~başarmış~}, içerisinde pek çok kurumun ve karmaşık sistemlerin bulunduğu koca '
    'bir imparatorluktu. {~Osmanlı İmparatorluğu’nda~} kontrolsüz harcamalar, savaşlarda alınan yenilgiler, devlet '
    'içerisindeki bürokrasinin güç yarışı, padişahın etkisini {~gitgide~} kaybetmesi ve ulemanın yeniliklere karşı uzak '
    'durması devletin {~gitgide~} kendi içinde çökmesinin yolunu yıllar boyu açacaktı ve bir yerden sonra yeniden reform '
    'hareketleri yaşanacak olsa da devlet için geç kalınmış olacaktı. III. Selim ile başlayacak olan ve ondan sonraki '
    '{~padişahların da~} katıldığı reform hareketleri devleti yeniden eski günlerine {~getirme amacı~} ve kurumları '
    'güçlendirerek tebaaya hizmeti {~artırmayı~} hedeflese de sadece Osmanlı Devleti’nin yıkımını geciktirecekti. Ancak '
    'bu reform hareketleri içerisinde, özellikle II. Abdülhamid döneminde, {~savaşta yaralanan ve uzvunu kaybeden '
    'askerler için yardım kampanyaları düzenlenmiş,~}[[fn:' + KT + ' 142.]] {~engelli insanların eğitimi için de yeni '
    'kurumlar açılmıştır.~} {+Örneğin 30 Eylül 1889’da İstanbul’da Avusturyalı Ferdinand Grati’nin önerisiyle Sağır ve '
    'Dilsiz Mektebi açılmış, bir yıl sonra körler için de izin alınmıştır.[[fn:Günay ve Görür 57-58, 60.]] +}Bu '
    'kurumların bazıları faal olmuş, bazıları daha az faal olmuş,[[fn:Günay ve Görür 68-69.]] ancak bazıları günümüze '
    'kadar gelmeyi başarmıştır. Bu kurumlardan bazıları günümüzde isim değişikliğine uğramış bir hâlde faal bir şekilde '
    'işler yapmaya devam etmektedir. Türk Kızılayı eski adıyla Hilal-i Ahmer Cemiyeti, Darülaceze gibi kurumlar '
    '{~Osmanlı döneminde kurulmuştur; Darülaceze Cumhuriyet döneminde gelirlerini toplamakta zorlansa da~} faal bir '
    'şekilde çalışmaya devam etmiştir.[[fn:Buğra 135.]] II. Meşrutiyet ile oluşan gergin ortam, Osmanlı Devleti’nin I. '
    'Dünya Savaşı’na katılımı {~ve Mondros Mütarekesi’nin (30 Ekim 1918) ardından ülke işgal altına girmiş~} ve Sevr '
    'Antlaşması dayatılmaya çalışılmıştır. Ancak 19 Mayıs 1919’da İstanbul’dan Samsun’a Bandırma Vapuru ile gönderilen '
    'Mustafa Kemal Paşa, Kurtuluş Savaşı’nın fitilini ateşlemiştir. Kurtuluş Savaşı’nda halk ve cemiyetler '
    '{~ellerinden~} geleni yapmış ve bu {~savaşın sonunda Osmanlı Devleti’nin devamı olacak Türkiye Cumhuriyeti '
    'kurulmuştur~}. Türkiye Cumhuriyeti, Osmanlı Devleti’nden gelen kurumları elden geçirerek {~daha istikrarlı ve '
    'kurallara bağlı dinamik bir yapıya kavuşturmuştur~}. Hilal-i Ahmer Cemiyeti Kurtuluş Savaşı’nda sağlık '
    'çalışmaları {~yapmış~} ve askerleri tedavi etmekle uğraşmıştır. {~Darülaceze gibi kurumlar ise işgal yıllarında güç '
    'koşullar altında çalışmak zorunda kalmıştır.~} Cumhuriyet kurulduğunda bu cemiyet ve kurumlar yeniliklerle yeniden '
    'işlevsel hâle getirilmiştir. Bunun yanında savaş gazilerinin ve {~halkın kurduğu cemiyetler~} gelir kazanma, sosyal '
    've yardım faaliyetlerinde bulunacaktı. Böylelikle ülkedeki yardımlaşma ve dayanışma ruhuyla {~birtakım~} girişimler '
    'yapılacak ve bu girişimler sonucu önemli işlere imza atılacaktı. {~Bu çalışmada söz konusu kurumların yapısı ve '
    'faaliyetleri kaynaklara dayanarak ortaya konmaktadır.~}'
)

GIRIS_KAVRAM = (
    '{+Çalışmada iki grup birlikte ele alınmaktadır: savaşta sakat kalan harp malulleri ile doğuştan ya da sonradan '
    'engelli olan siviller. Dönemin kaynakları ilki için “malûl”, ikincisi için “sakat”, “âmâ” ve “sağır-dilsiz” gibi '
    'terimler kullanır; “engelli” bugünün terimidir ve metinde üst kavram olarak kullanılmıştır. Gazilere yönelik yardım '
    '1929’da düzenli bir devlet mekanizmasına bağlandığı için bu kısım 1929-1930’da sona ermekte; sağır, dilsiz ve '
    'körlere yönelik devlet ve dernek faaliyetleri ise arşiv belgelerinin izin verdiği ölçüde 1963’e kadar '
    'izlenmektedir. Akademik literatürün yanı sıra birincil kaynaklardan da yararlanılmıştır: 1485 sayılı Kanun’un '
    'yayımlandığı 8 Haziran 1929 tarihli *Resmî Gazete*, kanunun görüşüldüğü TBMM zabıtları ve Cumhurbaşkanlığı Devlet '
    'Arşivleri Başkanlığı Cumhuriyet Arşivinde (BCA) bulunan, sağır, dilsiz ve körlerle ilgili 1938-1963 tarihli altı '
    'İcra Vekilleri Heyeti ve Bakanlar Kurulu kararı.+}'
)

# ---------------------------------------------------------------- HİLAL-İ AHMER
HILAL_1 = (
    'Hilal-i Ahmer Cemiyeti 1868 yılında Mecruhin ve Marda-i Askeriyeye İmdad ve Muavenet Cemiyet-i Osmaniye adıyla '
    'kurulmuş, 1876 yılında Hilal-i Ahmer adını almıştır{+; cemiyetin bu adla resmen faaliyete geçmesi ise 14 Nisan '
    '1877’yi bulmuştur+}. Bu kurum 1863 yılında Cenevre’de kurulan Kızılhaç’tan {~ilham almıştır~}.[[fn:Karal Akgün '
    '111-12; Macar 951.]] {~Cemiyetin kuruluş amacı savaşlarda yaralı askerlere yardım etmekti~}; sağlık hizmetleriyle '
    'halka yardım etmek gibi görevleri de üstlenmiştir. {~1877-1878 Osmanlı-Rus Savaşı’nda~} faaliyette bulunmuş, II. '
    'Abdülhamid dönemindeki baskılar sebebiyle faaliyetleri azalmış, ancak II. Meşrutiyet’in ilanından sonra yeniden '
    'canlanmıştır. Trablusgarp, Balkan ve I. Dünya savaşlarında cephede aktif {~görev almış~} ve halka ve askerlere '
    'hizmet etmiştir.[[fn:Karal Akgün 111, 113-14.]]'
)

HILAL_KADIN = (
    'Hilal-i Ahmer Cemiyetinin en önemli işlerinden biri de, {~o dönem ev işleriyle sınırlandırılmış kadınları toplumsal '
    'hayata katmak, ekonomik ve üretim faaliyetlerine katılımlarını sağlamak amacıyla Kadınlar Merkezini kurmasıydı. '
    'Merkezde~} hastabakıcılık ve bakım kursları {~düzenlenmiş, kadınların sağlık hizmetlerinde görev alması '
    'sağlanmış, sergiler, satış etkinlikleri, balolar ve çeşitli organizasyonlar düzenlenmiş, kadınların el emeği '
    'ürünlerini satmalarına imkân verilmiş ve böylece kadınların toplumdaki görünürlüğünün önü açılmıştır~}.'
    '[[fn:Karal Akgün 114-17.]]'
)

HILAL_SANATEVI = (
    'Hilal-i Ahmer Cemiyetinin yapmış olduğu bu faaliyetler kadınların sadece yardım alan ve ev işleriyle sınırlı kalan '
    'değil, yardım eden, üretim yapan, çalışan ve toplumsal hayata katılabilen bireyler hâline gelmesine katkıda '
    'bulunmuştur. Ayrıca {~Balkan Savaşları sırasında kurulan Sanat Evinde (Darü’s-sınaa) göç eden kadınlara iş ve '
    'eğitim verilmiş, kısa sürede 300 kadın örgücülük öğrenmiştir. Sanat Evi 1924’te Kadınlar Merkezi ile birlikte '
    'sona ermiştir.~}[[fn:Karal Akgün 118-20.]]'
)

HILAL_2 = (
    'I. Dünya Savaşı’nda da faaliyetlerine devam eden Hilal-i Ahmer Cemiyeti, Kurtuluş Savaşı’nda her bir yanı işgal '
    'altında olan ülkede faaliyetleri zorlaşsa da Millî Mücadele’ye destek vermeye {~devam etmiştir~}. Yaptığı '
    'faaliyetler {~imdat heyetleri, menzil istasyonları, aşevleri, gezici ve sabit sağlık merkezleri ve hastanelerle~} '
    'yaralanan askerlerin tedavisi, göç eden halka ve sivillere yardım ulaştırılması, İstanbul ile Anadolu arasında '
    'bağlantının sağlanması gibi pek çok amaca hizmet etmiştir. {~İstanbul’un işgal edildiği gece Genel Merkez İtilaf '
    'askerlerince basılıp evrakı tahrip edilse de~} cemiyet faaliyetlerine devam etmiştir.[[fn:Karal Akgün 120-21.]] '
    'TBMM’nin açılmasıyla cemiyetin Ankara ile olan ilişkisi daha da güçlenmiş, {~yurt içinden ve dışından gelen '
    'bağışlar Meclisten yönlendirilmeye başlanmıştır. Uluslararası Kızılhaç Komitesinin barış çağrısını İstanbul '
    'Hükûmeti yerine cemiyete göndermesi, uluslararası alanda tanındığını göstermektedir.~} {~Sovyet Rusya’nın 1921’de '
    'gönderdiği 30.000 altın rublelik yardımın 3.000 rublesi Mustafa Kemal Paşa tarafından Hilal-i Ahmere '
    'ayrılmıştır.~}[[fn:Karal Akgün 121-23.]] Cumhuriyet’in ilanından sonra Hilal-i Ahmer Cemiyeti, yaptığı hizmetler, '
    'modern sağlık anlayışı ile örgütlenmesi ve uluslararası yardım kuruluşlarıyla ilişkilerinin güçlü olması gibi '
    'sebeplerden Cumhuriyet’te de yer edinmiştir. {~Cemiyetin adı 2 Kasım 1922’de Türkiye Hilal-i Ahmer Cemiyeti, '
    '1935’te ise Türkiye Kızılay Cemiyeti olmuştur.~}[[fn:Karal Akgün 125; Çapa 545. Çapa ilk ad değişikliğini 1923 '
    'olarak verir.]]'
)

DARULACEZE_BASLIK = '{+DARÜLACEZE+}'
DARULACEZE = (
    '{+II. Abdülhamid döneminde sokaklarda dilenen kimsesiz çocukları, sakat erkek ve kadınları barındırmak amacıyla '
    'kurulan Darülaceze 1896’da hizmete açılmıştır.[[fn:Nuhoğlu 512-13.]] 1916 nizamnamesiyle Dahiliye Nezaretine '
    'bağlanan kurum, İstanbul’un kurtuluşundan sonra Sıhhat ve Muavenet-i İçtimaiye Vekâletine katılmış; 15 Ekim 1924 '
    'tarihli ve 970 sayılı İcra Vekilleri Heyeti kararıyla İstanbul Belediyesine devredilmiş ve 1925’ten itibaren '
    'belediyeye bağlı olarak faaliyet göstermiştir.[[fn:Çelik 429; Tekir 1305, 1315; Nuhoğlu 514.]] 1930’larda '
    'dilencilere yönelik kampanyalarda sakat ve muhtaç İstanbullular Darülacezeye yerleştirilmiş; kurum 1930’lar ve '
    '1940’larda kreş hariç yaklaşık 1.000 kişiyi barındırmıştır.[[fn:Buğra 134-36.]] Darülaceze bugün de faaliyetini '
    'sürdürmektedir.+}'
)

# ---------------------------------------------------------------- HÜKÜMET
HUK_1 = (
    '{~Millî Mücadele devam ederken~} TBMM Hükûmeti savaşta vefat eden, yaralanan ve malul kalan askerler için yardım '
    'sağlamayı çok önemli bir politika olarak görmüştür. Alaşehir Kongresi’nde {~şehit ailelerine ve yaralılara yardım '
    'yapılması ilke olarak kabul edilmiş, miktarın belirlenmesi ise komutanlara ve millî heyetlere bırakılmıştı~}. 1921 '
    'yılının Nisan ayında TBMM’ye verilen kanun teklifinde ise Millî Mücadele sırasında şehit olanların ailelerine ve '
    'malul kalan askerlere maddi yardım yapılması {~önerilmiş; şehit subay ailelerine 1.000’er, şehit astsubay ve er '
    'ailelerine 100’er lira, malullere de bu miktarların yarısının bir defaya mahsus ödenmesi teklif edilmişti~}.'
    '[[fn:Hayta ve Belenli 286, 289.]] {+Teklif 2 Nisan 1921’de Meclis’te okunarak ivedilikle encümene havale edilmiş, '
    'ancak bu hâliyle kanunlaştığına dair bir bilgiye ulaşılamamıştır.[[fn:*TBMM Zabıt Ceridesi*, D. 1, c. 9, '
    '328-29.]]+}'
)

HUK_2 = (
    'Millî Mücadele döneminde ordunun ihtiyaçlarına göre hastaneler kurulmuş ve yaralı askerlerin tedavisi '
    'sağlanmıştır. {~Örneğin yaralı subaylar için 100 yataklı bir hastane açılmış, Yunan ilerleyişi üzerine Nazilli’deki '
    'hastaneler Dinar ve Burdur’a taşınarak 50’şer yataklı iki hastane oluşturulmuştur.~} {~Sıhhat ve Muavenet-i '
    'İçtimaiye Vekâleti 2 Mayıs 1920’de 3 sayılı Kanun ile kurulmuş, ilk vekili Dr. Adnan (Adıvar) Bey olmuştur.~} '
    'Vekâlet, dönemin diğer bir yardım kuruluşu olan Hilal-i Ahmer Cemiyeti ile birlikte çalışmış, {~ihtiyaç duyduğu '
    'malzemeleri cemiyet aracılığıyla sağlamıştır~}.[[fn:Karavar 54-55, 57, 71.]] Ayrıca {~kararnamelerle şehit '
    'ailelerine maaş bağlanmış, 3 Temmuz 1921 kararnamesiyle Kuva-yı Milliyeden malul kalanlara ve şehitlerin '
    'ailelerine nizamiye askerleri gibi maaş tahsis edilmiştir~}. {~29 Aralık 1922 kararnamesiyle de işgalden '
    'kurtarılan yerlerdeki emekli, dul ve yetimlerin maaşlarının kurtuluş tarihinden itibaren ödenmesine karar '
    'verilmiştir.~}[[fn:Hayta ve Belenli 293-95.]] {~Ankara Merkez Kumandanlığı da yaralı subaylara yalnızca iplik parası '
    'alarak dikiş hizmeti veren bir terzi dükkânı açmıştır.~}[[fn:Hayta ve Belenli 289n43.]]'
)

HUK_3 = (
    '{~Sıhhat ve Muavenet-i İçtimaiye Vekâletinin görev alanı savaş sırasında ve sonrasında genişletilmiştir.~} 11 Mayıs '
    '1921 {~tarihli kararnameyle~} Dahiliye Vekâletine bağlı Muhacirin Müdüriyeti {~Umumiyesi vekâlete bağlanmış, '
    'muhacir işleri ise daha sonra kurulan Mübadele, İmar ve İskân Vekâletine devredilmiştir~}. {~İstanbul’un '
    'kurtuluşunun ardından~} darüleytamlar ve {~1.000 kadrolu~} Darülaceze vekâlete {~katılmış~}, darüleytamlar 1924’te '
    'Tevhid-i Tedrisat Kanunu gereğince Maarif Vekâletine devredilmiştir.[[fn:Tekir 1305, 1307.]] Kurtuluş '
    'Savaşı’ndan sonraki dönemde devlet kendisini toparlama yoluna girmişti. Ekonomik zorluklar ve isyanlarla '
    'mücadelenin yanı sıra Mustafa Kemal {~Paşa~} inkılaplarla ülkeyi muasır medeniyetler seviyesine ulaştırmayı '
    'benimsemiş ve gerekli hamleleri uygulamaktaydı. 1923’te savaş bittikten sonra ülkedeki sağlık hizmeti eksikliği '
    'hissedilmekteydi; hükûmet bazı bölgelerde görülen hastalıklara müdahale için yatırım yapması gerektiğinin '
    'farkındaydı. 1924’te {~zorunlu hizmet kanunu çerçevesinde~} kazalara doktor gönderilmeye başlanmış, {+kaza '
    'dispanserleri ve numune hastaneleri açılmıştır+}.[[fn:Tekir 1307-08.]] Bundan sonraki süreçte inkılaplarla eş '
    'zamanlı ilerleyerek sağlık hizmeti yaygınlaşmış, dönemin en tehlikeli sorunlarından biri olan salgın hastalıklarla '
    'mücadele edilmiş{+, 13 Mayıs 1926’da Sıtma Mücadelesi Kanunu çıkarılmıştır+}.[[fn:Tekir 1308; Akagündüz 5.]] Tüm '
    'bunları halka ulaştırmak ve bilgilendirmek önemliydi; çünkü sıtma gibi hastalıkların ölüm riski, Türkiye '
    'Cumhuriyeti’nin sağlık alanında yatırımlarını artırması ve teşkilatlanması gerektiğini hatırlatmaktaydı. 1926 '
    'yılında {~İzmir Sağır, Dilsiz ve Körler Müessesesinin müdürü Dr. Necati Kemal (Kip) Beyin~} *Sağır, Dilsiz ve '
    'Körler Müessesesi* adlı {~64 sayfalık eseri İzmir’de basılmıştır; bu eser Akagündüz’ün vekâletin bilgilendirme '
    'yayınları arasında saydığı eserlerden biridir~}.[[fn:Akagündüz 8; Atayurt Fenge ve Subaşıoğlu 1203.]]'
)

# ---------------------------------------------------------------- CEMİYETLER
MMC = (
    '1 Şubat 1913’te İstanbul Darülfünununda {~partiler üstü bir cemiyet olarak~} kurulmuştur. Cemiyette dönemin ileri '
    'gelen isimleri bulunmaktaydı; Talat Paşa, Fuat Paşa, Cavit Bey ve Yusuf Akçura bunlardan birkaçıdır. Cemiyet '
    'particilikten uzak kalarak millî bir ruhla halka yardım sağlamak amacını gütmüştür. {~Cemiyet, yardım heyetlerinin '
    'ihtiyaçlarını karşılamak ve gelir elde etmek amacıyla sinema faaliyetlerine başlamıştır.~}[[fn:' + KS + ' 6.]] '
    '{~Dönemde Hilal-i Ahmer Cemiyeti yararına sinemalarda film oynatılması da sık karşılaşılan '
    'bir durum olmuştu. Konulu film çekimleriyle Müdafaa-i Milliye Cemiyetinin yanı sıra Malûlîn-i Guzâta Muâvenet '
    'Heyeti de ilgilenmiştir.~} {~Ancak her film gelir getirmemiş; örneğin Malûlîn-i Guzâta Muâvenet Heyeti bazı '
    'kurumlar için çektiği filmlerin ücretini tahsil edememiştir.~}[[fn:' + KS + ' 5, 17.]] {+Müdafaa-i Milliye '
    'Cemiyeti 10 Mart 1919’da Harbiye Nezaretine bağlanmış, sinema makineleri ve aletleri Malûlîn-i Guzâta Muâvenet '
    'Heyetine bağışlanmıştır.[[fn:' + KS + ' 9-10.]] +}{~Sinema, ahlaka aykırı bulunan bazı Avrupa filmleri yüzünden '
    'zararlı görülse de halk ve aydınlar sinemanın gücünü fark etmiştir.~} Yardım cemiyetlerinin sinema faaliyetleri '
    'kamuoyunda bir sinema bilinci yaratmış ve hayır kurumlarına önemli bir gelir kapısı olmuştur.[[fn:' + KS +
    ' 20, 29.]]'
)

MGP = (
    'Malûlîn-i Guzâta Muâvenet Heyeti, {+Müdafaa-i Milliye ve Donanma cemiyetlerinin de desteğiyle+} 20 Mayıs 1917’de '
    'Harbiye Nezaretine bağlı olarak kurulmuş ve hükûmetten {+yaklaşık 120.000 liralık+} yardım almıştır. {~Eylül '
    '1919’da yeniden teşkilatlandırılan heyetin ilk nizamnamesi 6 Eylül 1920’de onaylanmış ve adı Malûlîn-i Askeriyeye '
    'Muâvenet Heyeti olmuştur.~}[[fn:' + KM + ' 578-79.]] {~Heyet, çalışabilen malulleri resmî dairelere yerleştirmiş, '
    'kendi ticarethanesini açanlara geri ödemeli sermaye vermiş, çalışamayacak durumda olanlara ise az miktarda da olsa '
    'maaş bağlamıştır.~}[[fn:' + KM + ' 580, 591.]] {~Heyetin açtığı Malûl Gaziler Muâvenet Pazarı adlı mağaza, ilk '
    'açıldığında gazetelerde reklam ve karikatürlerle tanıtılmıştır. Heyete yönelik usulsüzlük iddiaları 1920’den '
    'itibaren basında dile getirilmiş, ancak suiistimal iddiaları kanıtlanamamıştır.~}[[fn:' + KM + ' 580-81, 591-92.]] '
    '{~Arşiv belgelerine göre mağaza zamanla iflas etmiş; ancak Müdafaa-i Milliye Vekili Kâzım Paşa 1923’te bunun '
    'sebebinin, hatta doğru olup olmadığının kanıtlanamadığını söylemiştir.~}[[fn:' + KM + ' 582-83.]] Mağaza 23 Kasım '
    '1924’te Malûl Gaziler Pazarı Türk Anonim Şirketine dönüştürülmüş ve {~Ticaret Vekâletince tescil edilerek onun '
    'denetimine girmiştir~}.[[fn:' + KM + ' 580, 583-84.]] {~Şirket fabrika kurmayı amaçlamış, ancak bunu başaramayıp '
    'imalathane düzeyinde kalmıştır.~} Hem bir hayır kurumu hem de kâr getiren bir şirket olarak çalışmış, alım gücü '
    'düşük halka uygun fiyatlı mal sağlamış ve yerli malı kullanımını teşvik etmiştir.[[fn:' + KM + ' 594, 596.]]'
)

KANUN_BASLIK = '{+1485 Sayılı Kanun ve Heyetin Tasfiyesi (1929)+}'
GORSEL_ALTI = (
    '{~Görsel 1. 1485 sayılı Kanun’un yayımlandığı *Resmî Gazete* sayfaları (sy. 1210, 8 Haziran 1929, ss. '
    '7475-76).~}'
)
GORSEL_ACIK = (
    '{~Görsel 1’de sayfaları verilen 1485 sayılı Kanun’a göre devlet inhisarındaki maddelerin bayiliği öncelikle harp malullerine, onlar '
    'bulunmazsa şehit yetimlerine verilecekti. Bayilik tezkeresi alan herkesin bayilik ücretinin üçte biri her ay Ziraat '
    'Bankasında “Harp malülleri ve şehit yetimleri hesab” adıyla açılan hesaba yatırılacak, yıllık toplamın yarısı '
    'harp malullerine, yarısı da şehit yetimlerine dağıtılacaktı.~}[[fn:' + IBK + ' md. 1-2, 4.]] {+Kanun, malul '
    'gazilere bayilik hakkı tanıyan 1921 tarihli 166 ve 1924 tarihli 419 sayılı kanunların ve Malûlîn-i Askeriyeye '
    'Muâvenet Heyeti nizamnamesinin yerini almıştır.[[fn:' + IBK + ' md. 6; ' + KM + ' 593.]] Önceki uygulamanın sınırlı '
    'kaldığı da görülmektedir: 1924’te İstanbul’da bayiliği bizzat yürüten gazi sayısı yalnızca 128’di.[[fn:' + KT +
    ' 480.]] TBMM’de 30 Mayıs 1929’da tartışmasız kabul edilen kanuna ilişkin Millî Müdafaa Encümeni mazbatası, '
    'yardımın kaç kişiyi ilgilendirdiğini de göstermektedir: 1928’e kadar şehit yetimlerinin sayısı 70.000 çocuk ve '
    '50.000 kadın, harp malullerinin sayısı ise 1.047 subay ve 12.934 erdi. O güne kadar malullere 125.207 lira '
    'dağıtılmış, dağıtılmayı bekleyen birikmiş pay ise 507.000 lirayı aşmıştı. Encümen, heyetin kurduğu pazar ve '
    'şirketin ne malullere ne de şehit yetimlerine bir fayda sağladığını ileri sürmüştür.[[fn:' + ZC29 + ', 194-95 ve '
    'Sıra Sayısı 213, 2-3.]] Kanunla heyetin hesapları tasfiye edilmiş; heyet 18 Haziran 1929’da faaliyetine son '
    'vermiş, mağaza Sanayi ve Maadin Bankasına geçmiş ve 14 Ocak 1930’da Yerli Mallar Pazarı açılmıştır.[[fn:' + IBK +
    ' md. 5; ' + KM + ' 593-94.]]+}'
)
GORSEL_YORUM = (
    'Bu da bize bu dönemde savaş sebebiyle malul kalan insanların, {~şehit yetimlerinin ve dulların unutulmadığını '
    'gösterse de rakamlar, toplanan paranın hak sahiplerine yavaş ve eksik ulaştığını da ortaya koymaktadır. 1485 '
    'sayılı Kanun, bu aksaklığa verilmiş bir cevap olarak okunabilir.~}'
)

# ---------------------------------------------------------------- YENİ BÖLÜM: ARŞİV
ARSIV_BASLIK = '{+CUMHURİYET ARŞİVİ BELGELERİNDE SAĞIR, DİLSİZ VE KÖRLER (1938-1963)+}'
ARSIV_ALT1 = '{+İzmir Sağır, Dilsiz ve Körler Müessesesi+}'
ARSIV_1 = (
    '{+Cumhuriyet döneminin ilk sağır ve dilsizler okulu İzmir Sağır, Dilsiz ve Körler Müessesesidir. Kaynaklar '
    'kuruluş yılını 1923 ya da 1924 olarak vermektedir; yatılı olarak açılan kurum Sıhhat ve İçtimaî Muavenet '
    'Vekâletine bağlanmıştır.[[fn:Dincel 1069-70; Atayurt Fenge ve Subaşıoğlu 1203; Tekir 1308.]] Osmanlı döneminden '
    'kalan İstanbul’daki Sağır ve Dilsiz Mektebi 1926’da kapatılarak İzmir’deki okula bağlanmış, okulun binası 1928’de '
    'vekâletçe satın alınmıştır. 1929’da okulda 65 öğrenci bulunuyordu.[[fn:Günay ve Görür 68; Tekir 1318; Dincel '
    '1070.]] İcra Vekilleri Heyeti 13 Ocak 1941’de, eksiltmeye istekli çıkmadığı ve bir ay içinde pazarlıkla da ihale '
    'edilemediği için müessesenin 1940 malî yılına ait 22.000 kilo ekmek ihtiyacının pazarlıkla alınmasını kabul '
    'etmiştir.[[fn:BCA, 30.18.1.2/93.124.5 (Kararname 2/15030, 13 Ocak 1941).]] 19 Şubat 1942 tarihli kararnameyle de '
    'aynı gerekçeyle 1941 malî yılına ait 2.000 kilo ekmek, 1.500 kilo Urfa sadeyağı, 1.200 kilo Tosya pirinci ve 1.500 '
    'kilo toz şekerin pazarlıkla temini onaylanmıştır.[[fn:BCA, 30.18.1.2/97.119.13 (Kararname 2/17366, 19 Şubat '
    '1942). Belgede Maliye mütalaasının tarihi 7 Şubat 1941 (7/2/1941) olarak geçer.]] Her iki karar da 2490 sayılı '
    'Artırma ve Eksiltme ve İhale Kanunu’nun 46. maddesinin (R) fıkrasına dayanmaktadır. Bu fıkra, talip çıkmayan '
    'işlerin pazarlıkla yapılmasına izin vermekte, ancak bu durumda İcra Vekilleri Heyeti kararını şart '
    'koşmaktadır.[[fn:Artırma ve Eksiltme ve İhale Kanunu md. 46.]] Dolayısıyla kararların Bakanlar Kurulundan geçmesi '
    'bir ayrıcalık değil, usulün gereğidir. Belgelerin asıl tanıklığı, İkinci Dünya Savaşı yıllarında bir devlet '
    'okulunun temel gıdası için bile ihaleye istekli bulunamamasıdır.+}'
)

ARSIV_ALT2 = '{+Uzman Yetiştirme: Dr. Abdülkadir Cahit Tümer’in Berlin’e Gönderilmesi+}'
ARSIV_2 = (
    '{+Devlet bu alanda uzman yetiştirmeye de önem vermiştir. 28 Kasım 1938 tarihli kararname ile Ödemiş’te serbest '
    'çalışan akıl ve sinir hastalıkları uzmanı Dr. Abdülkadir Cahit Tümer’in, ruhen ve bedenen geri kalmış çocuklar ile '
    'sağır, dilsiz ve körlerin “terbiye ve tedrisleri hakkında tetkikat ve tetebbuatta bulunmak” üzere vekâlet hesabına '
    'Berlin’e gönderilmesi, kendisine orada kaldığı sürece aylık iki yüz lira ödenmesi ve dönüşünde bu alanda görev '
    'verilmesi kararlaştırılmıştır.[[fn:BCA, 30.18.1.2/85.98.16 (Kararname 2/9925, 28 Kasım 1938).]] Vekâletin teklifi 8 '
    'Ekim 1938’de, Atatürk hayattayken yapılmış; kararname ise onun ölümünden sonra, Reisicumhur İsmet İnönü’nün '
    'imzasıyla onanmıştır. Bir biyografiye göre Tümer, daha sonra İzmir Sağır-Dilsiz ve Körler Müessesesinin '
    'müdürlüğünü yapmıştır.[[fn:Tunçbay 66. Kararnamede “Tümer”, biyografinin başlığında “Tuner”, metninde “Tüner” '
    'olarak geçer.]] Müessese 1951’de 5822 sayılı Kanun ile Millî Eğitim Bakanlığına devredilmiş ve sağır ve kör '
    'çocukların eğitimi bu bakanlığın sorumluluğuna girmiştir.[[fn:Yedek 1892, 1903.]]+}'
)

ARSIV_ALT3 = '{+Sivil Örgütlenme: Dernekler ve Millî Federasyon+}'
ARSIV_3 = (
    '{+Sağırlar bu dönemde kendi derneklerini de kurmaya başlamıştır. Kendisi de işitme engelli olan Süleyman Sırrı '
    '(Gök), 1930’da İstanbul’da Sağır, Dilsiz ve Körler Tesanüt Cemiyetini kurmuştur. Onları himaye amacıyla kurulan '
    'cemiyetler de vardı; ancak 1933’te kurulan Sağır, Dilsiz ve Körleri Himaye Cemiyetinin kamuya yararlı sayılması '
    'hükûmetçe kabul edilmemiştir.[[fn:Dincel 1071, 1079; Atayurt Fenge ve Subaşıoğlu 1204.]] Türkiye Sağır, Dilsiz ve '
    'Körler Tesanüt Derneği ise İçişleri Bakanlığının yazısı ve Danıştay Genel Kurulunun kararı üzerine 2 Ağustos '
    '1947’de Bakanlar Kurulu kararıyla “genel menfaatlere yarar dernekler”den sayılmıştır.[[fn:BCA, 30.18.1.2/114.56.2 '
    '(Karar 3/6283, 2 Ağustos 1947).]] Aynı statü 6 Mart 1951’de Türkiye Sağır, Dilsiz ve Körler Derneğine de '
    'tanınmıştır;[[fn:BCA, 30.18.1.2/125.18.5 (Karar 3/12632, 6 Mart 1951).]] bu iki derneğin 1930’da kurulan '
    'cemiyetle ilişkisi belgelerden anlaşılamamaktadır. Her iki karar da bir derneğin “umumî menfaatlere hadim” '
    'sayılmasını Danıştay kararına ve Bakanlar Kurulu onayına bağlayan 3512 sayılı Cemiyetler Kanunu’nun 37. maddesine '
    'dayanmaktadır.[[fn:Cemiyetler Kanunu md. 37.]] 1 Nisan 1963 tarihli kararnameyle ise merkezi İstanbul’da kurulacak '
    'olan Türkiye Sağır Dilsiz Dernekleri Millî Federasyonunun unvanında “Millî” kelimesini kullanmasına ve merkezi '
    'Roma’da bulunan Dünya Sağırlar Federasyonu ile iş birliği yapmasına izin verilmiştir.[[fn:BCA, 30.18.1.2/168.19.3 '
    '(Kararname 6/1604, 1 Nisan 1963). Bazı ikincil kaynaklar federasyonun kuruluşunu 1960’a tarihlendirse de '
    'kararname federasyondan “kurulacak olan” diye söz etmektedir; bk. Atayurt Fenge ve Subaşıoğlu 1204.]] Bu izinler, '
    '“Millî” unvanının kullanımını Bakanlar Kurulu kararına bağlayan 16. maddeye ve milletlerarası iş birliğini '
    'düzenleyen 10. maddeye dayanmaktadır.[[fn:Cemiyetler Kanunu md. 10, 16. Dünya Sağırlar Federasyonu 23 Eylül '
    '1951’de Roma’da kurulmuştur; bk. Atayurt Fenge ve Subaşıoğlu 1198.]]+}'
)

# ---------------------------------------------------------------- SONUÇ
SONUC_1 = (
    'Sonuç olarak Osmanlı Devleti içerisinde bulunan pek çok kurum Cumhuriyet’e geçildiğinde korunmuş ve gelişimi '
    'sağlanmıştır. Engellilere ve gazilere yönelik çalışmalar yapan bu kurumlar her dönem verimli veya verimsiz bir '
    'şekilde çalışarak vatana hizmet etmeyi hiç bırakmamış, ancak bazıları günümüze kadar devamlılığını '
    'sürdürememiştir. {~Gerekli düzenlemeler yapılarak hak sahiplerinin mağduriyeti giderilmeye çalışılmıştır.~}'
)
SONUC_2 = (
    '{+Kaynaklar, yardımların yaygınlığının yanında sınırlarını da göstermektedir. 1929’da yaklaşık 120.000 şehit '
    'yetimi ve dulu ile 14.000 kadar harp malulü bulunmasına karşın o güne kadar malullere yalnızca 125.207 lira '
    'dağıtılabilmiştir. 1485 sayılı Kanun bu nedenle yardımı gönüllü kuruluşlardan alıp düzenli bir devlet '
    'mekanizmasına bağlamıştır. İncelenen altı arşiv kararı sınırlı bir örneklem olmakla birlikte, devletin 1938-1942 '
    'arasında kurum, iaşe ve uzman yetiştirme yoluyla engelli eğitiminde doğrudan sorumluluk aldığına; 1947-1963 '
    'arasında ise sağırların kurduğu derneklerin kamu yararı statüsü ve uluslararası bağlantı kazandığına işaret '
    'etmektedir. Bu eğilimin genel olup olmadığı daha geniş bir arşiv taramasıyla sınanmalıdır.+}'
)

# ---------------------------------------------------------------- KAYNAKÇA (MLA 9)
KAYNAKCA_ARSIV_GIRIS = (
    'BCA: Cumhurbaşkanlığı Devlet Arşivleri Başkanlığı Cumhuriyet Arşivi, Ankara (fon 30.18.1.2).'
)
KAYNAKCA_ARSIV = [
    'İcra Vekilleri Heyeti. Dr. Abdülkadir Cahit Tümer’in Berlin’e Gönderilmesine Dair Kararname, no. 2/9925. 28 Kasım '
    '1938. BCA, 30.18.1.2/85.98.16.',
    '---. İzmir Sağır, Dilsiz ve Körler Müessesesinin 1940 Malî Yılı Ekmek İhtiyacının Pazarlıkla Teminine Dair '
    'Kararname, no. 2/15030. 13 Ocak 1941. BCA, 30.18.1.2/93.124.5.',
    '---. İzmir Sağır, Dilsiz ve Körler Müessesesinin 1941 Malî Yılı Erzak İhtiyacının Pazarlıkla Teminine Dair '
    'Kararname, no. 2/17366. 19 Şubat 1942. BCA, 30.18.1.2/97.119.13.',
    'Bakanlar Kurulu. Türkiye Sağır, Dilsiz ve Körler Tesanüt Derneğinin Genel Menfaatlere Yarar Derneklerden '
    'Sayılmasına Dair Karar, no. 3/6283. 2 Ağustos 1947. BCA, 30.18.1.2/114.56.2.',
    '---. Türkiye Sağır, Dilsiz ve Körler Derneğinin Genel Menfaatlere Yarar Derneklerden Sayılmasına Dair Karar, no. '
    '3/12632. 6 Mart 1951. BCA, 30.18.1.2/125.18.5.',
    '---. Türkiye Sağır Dilsiz Dernekleri Millî Federasyonuna Unvan ve İş Birliği İzni Verilmesine Dair Kararname, no. '
    '6/1604. 1 Nisan 1963. BCA, 30.18.1.2/168.19.3.',
]
KAYNAKCA_RESMI = [
    'Artırma ve Eksiltme ve İhale Kanunu. Kanun no. 2490, kabul 2 Haziran 1934. *Resmî Gazete*, sy. 2723, 10 Haziran '
    '1934. *TBMM Kanunlar Dergisi*, c. 13, ss. 706-22.',
    'Cemiyetler Kanunu. Kanun no. 3512, kabul 28 Haziran 1938. *Resmî Gazete*, sy. 3959, 14 Temmuz 1938. *TBMM '
    'Kanunlar Dergisi*, c. 18, ss. 1091-96.',
    'İnhisar Beyiyeleri Üçte Birlerinin Harp Malûllerine ve Şehit Yetimlerine Tahsis ve Tevziine Dair Kanun. Kanun no. '
    '1485, kabul 30 Mayıs 1929. *Resmî Gazete*, sy. 1210, 8 Haziran 1929, ss. 7475-76. *TBMM Kanunlar Dergisi*, c. 7, '
    'ss. 765-66.',
    '*TBMM Zabıt Ceridesi*. Devre 1, c. 9, 15. İçtima, 2 Nisan 1337 [1921], ss. 328-29.',
    '*TBMM Zabıt Ceridesi*. Devre 3, c. 12, 73. İnikat, 30 Mayıs 1929, ss. 194-95; ekli Sıra Sayısı 213, ss. 1-9.',
]
KAYNAKCA_ARASTIRMA = [
    'Akagündüz, Ümüt. “Cumhuriyet’in İlk Yıllarında Sıhhat ve İçtimai Muavenet Vekâletinin Sağlık Bilgisini Halka '
    'Ulaştırma Çabası.” *Atatürk Yolu Dergisi*, sy. 73, 2023, ss. 1-24, https://doi.org/10.46955/ankuayd.1353054.',
    'Atayurt Fenge, Zeynep Zeren, ve Fatoş Subaşıoğlu. “Dünyada ve Türkiye’de İşitme Engellilik: Zaman Çizelgesi.” '
    '*Ankara Üniversitesi Dil ve Tarih-Coğrafya Fakültesi Dergisi*, c. 59, sy. 2, 2019, ss. 1188-207, '
    'https://doi.org/10.33171/dtcfjournal.2019.59.2.21.',
    'Buğra, Ayşe. *Kapitalizm, Yoksulluk ve Türkiye’de Sosyal Politika*. İletişim Yayınları, 2008.',
    'Çapa, Mesut. “Kızılay.” *TDV İslâm Ansiklopedisi*, c. 25, TDV İslâm Araştırmaları Merkezi, 2022, ss. 544-46.',
    'Çelik, Recep. “Beceri Eğitimine Bir Model: Darülaceze Mektepleri ve İmalathaneler.” *Dumlupınar Üniversitesi '
    'Sosyal Bilimler Dergisi*, sy. 85, 2025, ss. 426-36, https://doi.org/10.51290/dpusbe.1695028.',
    'Dincel, Anıl. “Atatürk Dönemi Sağır ve Dilsiz Kongrelerinin Türk Basını’na Yansımaları (1930-1938).” '
    '*Cumhuriyet Tarihi Araştırmaları Dergisi*, yıl 18, sy. 36, 2022, ss. 1063-100.',
    'Günay, Ramazan, ve Halil İbrahim Görür. “Osmanlı Devleti’nde Sağır, Dilsiz ve A’mâ Mektebi.” *Tarih Araştırmaları '
    'Dergisi*, c. 32, sy. 53, 2013, ss. 55-76.',
    'Hayta, Necdet, ve Tuğba Belenli. “Milli Mücadele Dönemi’nde Türkiye Büyük Millet Meclisi Hükümeti Tarafından '
    'Uygulanan Sosyal Politikalar.” *Belleten*, c. 80, sy. 287, 2016, ss. 279-305, '
    'https://doi.org/10.37879/belleten.2016.279.',
    'Karal Akgün, Seçil. “Cumhuriyet Duyurulurken Geride Bırakılamayan Bir Kurum: Hilal-i Ahmer Cemiyeti.” *ODTÜ '
    'Gelişme Dergisi*, c. 39, Nisan 2012, ss. 111-36.',
    'Karavar, Hilâl. “Milli Mücadele Döneminde Sıhhat ve Muavenet-i İçtimaiye Vekillerinin Faaliyetleri.” *Yakın Dönem '
    'Türkiye Araştırmaları*, sy. 42, 2022, ss. 47-75, https://doi.org/10.26650/YTA2022-1106785.',
    'Kurnaz Şahin, Feyza. “Cumhuriyetin Kuruluşuna Kadar Türkiye’de Yardım Cemiyetlerinin Sinema Faaliyetleri ve '
    'Kamuoyunda Sinema Algısı (1910-1923).” *Atatürk Araştırma Merkezi Dergisi*, c. 30, sy. 88, 2014, ss. 1-36.',
    '---. “Erken Cumhuriyet Döneminde İz Bırakan Bir Yardım Şirketi: Malûl Gaziler Pazarı Türk Anonim Şirketi.” '
    '*Tarih İncelemeleri Dergisi*, c. 35, sy. 2, 2020, ss. 577-602, https://doi.org/10.18513/egetid.849756.',
    '---. *Osmanlı’dan Cumhuriyet’e Harp Malûllerinin Sosyo-Ekonomik ve Sağlık Durumları (1877-1939)*. 2012. Afyon '
    'Kocatepe Üniversitesi, doktora tezi.',
    'Macar, Oya Dağlar. “Hilal-i Ahmer Cemiyeti’nin Kurumsal Tarihinde Önemli Bir Deneyim: Trablusgarp Savaşı '
    '(1911-1912).” *Belleten*, c. 81, sy. 292, 2017, ss. 947-86, https://doi.org/10.37879/belleten.2017.947.',
    'Nuhoğlu, Hidayet Yavuz. “Darülaceze.” *TDV İslâm Ansiklopedisi*, c. 8, Türkiye Diyanet Vakfı, 1993, ss. 512-14.',
    'Tekir, Süleyman. “Sıhhiye ve Muavenet-i İçtimaiye Vekâleti’nin Kuruluşu ve Erken Cumhuriyet Dönemindeki '
    'Faaliyetleri (1920-1930).” *Belgi Dergisi*, c. 2, sy. 18, 2019, ss. 1301-26, '
    'https://doi.org/10.33431/belgi.547721.',
    'Tunçbay, Erdem. “Merhum Dr. Abdülkadir Cahit Tuner’in Biyografisi.” *Ege Nörolojik Bilimler Dergisi*, c. 1, sy. '
    '1, Ocak 1984. Dursun Kırbaş, *Türkiye Nöroloji Tarihçesi*, s. 66.',
    'Yedek, Şahin. “Arşiv Belgelerine Göre Demokrat Parti Döneminde Eğitim Yatırım ve Ödenekleri.” *Anemon Muş '
    'Alparslan Üniversitesi Sosyal Bilimler Dergisi*, c. 9, sy. 6, 2021, ss. 1891-909, '
    'https://doi.org/10.18506/anemon.897536.',
]

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


def build(out, marked, image_scale=0.56):
    d = Doc(SRC, highlight=('on' if marked else None))
    P = d.paras()
    T = {i: P[i] for i in range(len(P))}  # özgün indeksler (kaymadan önce sabitle)

    # Kapak
    d.rebuild(T[6], 'Kurtuluş Savaşı’nda, Sonrasında ve {~Cumhuriyet’te~}', bold=True, size=28)
    d.rebuild(T[10], '{~YÜKSEK LİSANS~} VİZE TESLİM', bold=True, size=28)
    d.rebuild(T[21], 'Kasım{~ ~}2026', bold=True, size=28)
    # Özet / Abstract
    d.rebuild(T[23], OZET)
    d.rebuild(T[25], '**Anahtar Kelimeler:** {~Gazi, Harp Malulü, Engelli, Yardım Cemiyetleri, Sağır-Dilsiz Eğitimi, '
                     'Darülaceze~}')
    d.rebuild(T[28], '{~ABSTRACT~}', bold=True)
    d.rebuild(T[29], ABSTRACT)
    d.rebuild(T[30], '**Keywords:** {~Veteran, Disabled Veteran, Disability, Charitable Associations, Deaf Education, '
                     'Darülaceze~}')
    # Giriş
    d.rebuild(T[33], GIRIS)
    d.insert_after(T[33], [d.para_like(T[33], GIRIS_KAVRAM)])
    # Hilal-i Ahmer: kadınlar merkezi listesi tek paragrafa
    d.rebuild(T[36], HILAL_1)
    d.rebuild(T[37], HILAL_KADIN)
    for i in range(38, 43):
        d.remove(T[i])
    d.rebuild(T[43], HILAL_SANATEVI)
    d.rebuild(T[44], HILAL_2)
    # Darülaceze: Osmanlı'dan devralınan ikinci kurum olarak Hilal-i Ahmer'in ardından
    d.insert_after(T[44], [d.para_like(T[45], DARULACEZE_BASLIK, bold=True), d.para_like(T[44], DARULACEZE)])
    # Hükümet
    d.rebuild(T[46], HUK_1)
    d.rebuild(T[47], HUK_2)
    d.insert_after(T[47], [d.para_like(T[47], HUK_3)])
    # Cemiyetler
    d.rebuild(T[55], MMC)
    d.rebuild(T[58], MGP)
    # 1485 sayılı Kanun alt bölümü: görsel ve açıklaması Malûl Gaziler'in ardına taşınır
    for ext in T[48].iter():
        if ext.tag.endswith('}extent') or ext.tag.endswith('}ext'):
            for k in ('cx', 'cy'):
                if ext.get(k):
                    ext.set(k, str(int(int(ext.get(k)) * image_scale)))
    d.rebuild(T[49], GORSEL_ALTI)
    d.rebuild(T[50], GORSEL_ACIK)
    d.rebuild(T[51], GORSEL_YORUM)
    sub = lambda s: d.para_like(T[58], s, bold=True)
    kb = sub(KANUN_BASLIK)
    T[58].addnext(kb)
    kb.addnext(T[50]); T[50].addnext(T[48]); T[48].addnext(T[49]); T[49].addnext(T[51])
    # Yeni bölüm: Sonuç'tan önce
    head = lambda s: d.para_like(T[54], s, bold=True)
    body = lambda s: d.para_like(T[58], s)
    d.insert_before(T[59], [head(ARSIV_BASLIK), sub(ARSIV_ALT1), body(ARSIV_1), sub(ARSIV_ALT2), body(ARSIV_2),
                            sub(ARSIV_ALT3), body(ARSIV_3)])
    # Sonuç
    d.rebuild(T[60], SONUC_1)
    d.insert_after(T[60], [d.para_like(T[60], SONUC_2)])
    # Kaynakça
    d.rebuild(T[62], '{~ARŞİV BELGELERİ~}', bold=True)
    for i in range(63, 72):
        d.remove(T[i])
    sp = {'after': '0', 'line': '240', 'lineRule': 'auto'}
    bib = lambda s: d.para_like(T[62], s, hanging=True, spacing=sp)
    items = [bib(KAYNAKCA_ARSIV_GIRIS)] + [bib(x) for x in KAYNAKCA_ARSIV]
    items += [d.para_like(T[62], '{~RESMÎ YAYINLAR~}', bold=True)] + [bib(x) for x in KAYNAKCA_RESMI]
    items += [d.para_like(T[62], '{~ARAŞTIRMALAR~}', bold=True)] + [bib(x) for x in KAYNAKCA_ARASTIRMA]
    d.insert_after(T[62], items)
    # boş ara paragraflar (yer kazanmak için)
    for i in (34, 52, 56, 72, 73, 74):
        if T[i].getparent() is not None and not d.ptext(T[i]).strip() and \
                T[i].find('.//' + W + 'drawing') is None:
            d.remove(T[i])
    d.prune_footnotes()
    d.save(out)


if __name__ == '__main__':
    scale = float(sys.argv[3]) if len(sys.argv) > 3 else 0.56
    build(sys.argv[1], True, scale)
    build(sys.argv[2], False, scale)
    print('ok')
