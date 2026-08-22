# Yönetişim

<sub><a href="GOVERNANCE.md">English</a></sub>

Bu dosya, bu depoda kararların bugün nasıl alındığını anlatır; eninde sonunda
nasıl alınmasını istediğimizi değil.

## Mevcut durum, açıkça

Kurucu yönetiminde, tek bakımcı. Bağımsız bakımcı gözden geçirmesi şu anda
mümkün değil. Bu gerçek bir sınırlılıktır ve tek katılımcılı bir gözden geçirme
süreciyle gizlenmek yerine burada kayda geçirilmiştir.

## Bu deponun neye karar verdiği ve neye vermediği

Bir sektör paketi, kontrol etmediği iki şeyin akışında yer alır: çekirdek motorun
sözleşmesi ve aile bildirgesi. Burada karar gibi görünen şeylerin çoğu başka bir
yerde alınmıştır.

| Sınıf | Örnekler | Kim karar verir |
| --- | --- | --- |
| Paket içeriği | Bir sözlük girdisi, bir şablonun ifadesi, bir dağılım parametresi | Bakımcı birleştirmesi |
| Paket biçimi | Bir kayıt türü, bir tarif, bir kapsam hedefi | Değişiklik günlüğüne geçirilen bakımcı kararı |
| Sözleşme | Alan türleri, üreteç türleri, etiket taksonomisi, kimlik politikası anlamları | Burada karara bağlanmaz. Bunlar çekirdek motora aittir |
| Yerleşik aile kararı | Topoloji, sektör sırası, lisanslama, model kullanmama kuralı | Burada karara bağlanmaz. Bunlar aile bildirgesinden gelir |
| Dış yetki | Depo oluşturma, sürümler, referans veri kümeleri, bir düzenlemeye atıf yapan her cümle | Bakımcı kararı değildir. Sahibin kayıt altına alınmış onayını gerektirir |

## Kurucu yönetiminde birleştirme kuralı ve onun yerini alan denetim

Tek bir bakımcı bulunduğu sürece, o bakımcı kendi değişikliklerini
birleştirebilir. Bunu telafi eden denetim şudur: zorunlu CI yeşil olmadan hiçbir
birleştirme geçmez ve CI uygunluk çalışmasını, denylist taramasını ve kapsam
uygulanabilirlik kontrolünü içerir. Bir kusurla ana dal arasında duran şey gözden
geçiren değil, kontrollerdir.

İkinci bir bakımcı katıldığında bu kural kaldırılır ve paket içeriğinin ötesindeki
her şey için iki taraflı gözden geçirme uygulanır.

## Sürümler

Bir sürüm, tüketicilerin gerçekte aldığı şey olan referans veri kümelerini taşır.
Bir bakımcı tarafından çıkarılır, yayımlandıktan sonra değiştirilemez ve sahibin
kayıt altına alınmış onayının arkasındadır. `packcheck` başarısızken bir sürüm
etiketlenemez.

## Süreklilik

Tek bakımcı erişilemez hâle gelirse, bu depo sessizce devredilmek yerine arşive
kaldırılır. Yayımlanmış veri kümeleri doğrulanabilir kalır, çünkü doğrulama için
yalnızca çıktılar ve sabitlenmiş aralıkta bir çekirdek gerekir.
