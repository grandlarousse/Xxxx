# Bağımsız yeniden çekim (ana ajan, 26.11.2026 gecesi)

Komut: `node ek/kod/gmaps_scrape.js --place <url>`. İlk çekimden saatler sonra, her yer için ayrı. Önerinin dayandığı yorumların anahtar sözcükleri taze çıktıda arandı (büyük-küçük harf duyarsız).

| Kafe | Puan (yorum) | Çekilen yorum | Aranan sözcükler | Sonuç |
|---|---|---|---|---|
| Node Coffee | 4,7 (138) | 17 | ders çalışmak için çok uygun, kitap, ekşi, sessiz | hepsi var |
| Kino Coffee | 4,8 (93) | 17 | internet, ders, acı | hepsi var |
| Casual Coffee & Bakery Myvia | 4,1 (26) | 12 | sessiz, internet, sensör, pahalı | hepsi var |
| Rudy Coffee 3. Nesil Kahve Dükkanı | 4,7 (331) | 27 | ders, bahçe, sigara, kitap | hepsi var |
| Avoir L'Atelier | 4,6 (225) | 22 | sessiz, fiyat | hepsi var |
| Monday's coffee | 4,8 (58) | 14 | çalışmak için | var |
| Herms Coffee & More | 3,9 (145) | 20 | sipariş, saat | hepsi var |
| People's Social Bornova | 4,0 (78) | 13 | dakika, masa | "dakika" yok, "masa" var |
| Colombia Coffee Bornova | 4,2 (83) | 18 | priz, sigara | hepsi var |
| Boston Drink & Dessert | — | — | — | süre aşımı, çekilemedi |

Hepsi "açık (kalıcı kapanma yok)" döndü. Sınır: sözcük eşleşmesi alıntının tamamını değil varlığını gösterir; alıntının birebir hâli ilk çekimde (`veri/gmaps_kafeler.json`) doğrulayıcılarca kontrol edildi.
