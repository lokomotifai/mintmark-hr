# Katkı

<sub><a href="CONTRIBUTING.md">English</a></sub>

Katkıda bulunmayı düşündüğünüz için teşekkürler. Burası bir bildirim ve veri
deposudur, dolayısıyla değiştireceğiniz şeylerin çoğu kod değil YAML olacaktır.

## Commit'lerinizi imzalayın

Katkılar Developer Certificate of Origin, sürüm 1.1 kapsamında kabul edilir.
Katkıcı lisans sözleşmesi yoktur. Her commit, commit yazarıyla eşleşen bir
imza satırı taşır:

    git commit -s -m "mesajınız"

## Bu depoda motor kodu yoktur

Ailenin üzerine kurulduğu kural budur ve bir testle uygulanır. Buradaki tek
Python `tests/` altındadır ve çekirdeğin açık API'si dışında hiçbir şeyi içe
aktarmaz. Sözlük üreten bir yardımcı `tools/` altında durur, commit'lenmiş çıktı
üretir ve hiçbir zaman bir testten içe aktarılmaz ya da üretim sırasında
çalıştırılmaz.

Bir bildirim bu paketin ihtiyacını ifade edemiyorsa, bu bir çekirdek
değişikliğidir. Çekirdek deposunda bir konu açın ve boşluğu kayda geçirin. Bir
betikle etrafından dolaşmayın: kendi verisini üreten bir paket, paket olmaktan
çıkmıştır.

## Çekme isteği açmadan önce

    uv sync
    uv run mintmark packcheck .
    uv run pytest
    uv run python tools/mdlint.py .

`packcheck` paketlenmiş çekirdek wheel'e karşı çalışır, dolayısıyla çevrimdışı
işler.

## Bir sözlüğe ekleme yapmak

Bilinmesi gereken iki şey var.

Uydurulmuş her ad, zorunlu CI'da gerçek kurum denylist'ine karşı taranır. Bir
çakışma yapıyı düşürür ve her iki tarafı da adıyla bildirir. Çakışan bir ad
savunulmaz, kaldırılır.

İlk etiketli sürümden sonra mevcut bir sözlüğe girdi eklemek, sonraki her indeks
için çekilişi değiştirir ve dolayısıyla sabit bir tohum için üretilen baytları
değiştirir. Bu, minör değil majör bir sürüm artışıdır, çünkü yayımlanmış her
künyenin yeniden üretilebilirliğini bozar.

## Metin için dil kuralları

Zorunlu CI'da `tools/mdlint.py` tarafından, iki dilde birden uygulanır: cümle
düzeninde başlıklar, yasaklı bir tanıtım söz dağarı ve hiçbir yerde uzun tire ya
da orta tire bulunmaması. Alıntılanan üçüncü taraf metni, gerekçe taşıyan bir
işaretle muaf tutulur.

`README.md` esas metindir ve `README.tr.md` özet değil tam bir aynasıdır. Birini
diğeri olmadan değiştirmek gözden geçirmede reddedilir. Aynı kural bu deponun
diğer `.tr.md` aynaları için de geçerlidir.

## Reddedilecek olanlar

`tests/` ve `tools/` dışındaki her Python. `samples/` dışında commit'lenmiş her
veri kümesi. Herhangi bir yerde geçen gerçek kurum, marka veya kişi. README'de
takvime bağlı her söz. Her uyum garantisi.
