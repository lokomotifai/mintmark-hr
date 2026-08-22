<p align="center">
  <img src="assets/brand/mintmark-logo.svg" width="112" height="112" alt="Mintmark">
</p>

<h1 align="center">Mintmark insan kaynakları</h1>

<p align="center"><strong>Türkçe iş gücü ve bordro verisi; çoğu kişinin modellemek istemeyeceği iki yüzey dahil.</strong></p>

<p align="center">
  Çalışanlar, görev geçmişleri, izin ve bordro kayıtları,<br>
  ve sağlık ile adli sicil ifadelerinin gerçekten göründüğü serbest metin.
</p>

<p align="center">
  <a href="https://github.com/lokomotifai/mintmark-hr/actions/workflows/ci.yml"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/lokomotifai/mintmark-hr/ci.yml?branch=main&amp;style=flat-square&amp;label=CI"></a>
  <img alt="Motor kodu yok" src="https://img.shields.io/badge/motor%20kodu-yok-3C873A?style=flat-square">
  <img alt="18 kapsam hedefinin 18'i karşılandı" src="https://img.shields.io/badge/kapsam%20hedefleri-18%2F18-3C873A?style=flat-square">
  <img alt="Yayımlanmış sürüm yok" src="https://img.shields.io/badge/sürüm-yayımlanmadı-3B3F46?style=flat-square">
  <a href="LICENSE"><img alt="Apache-2.0 lisansı" src="https://img.shields.io/badge/lisans-Apache--2.0-3B3F46?style=flat-square"></a>
</p>

<p align="center">
  <a href="https://github.com/lokomotifai/mintmark"><img alt="Mintmark çekirdeği gerekir" src="https://img.shields.io/badge/çekirdek-%3E%3D0.1%2C%3C0.2-17191F?style=flat-square"></a>
  <img alt="Yedi kayıt türü" src="https://img.shields.io/badge/kayıt%20türü-7-17191F?style=flat-square">
  <img alt="Üç belge ailesi" src="https://img.shields.io/badge/belge%20ailesi-3-17191F?style=flat-square">
  <img alt="26 kurgusal işveren adı" src="https://img.shields.io/badge/kurgusal%20işveren-26-D11F26?style=flat-square">
  <img alt="İki hassas sınır" src="https://img.shields.io/badge/sınırlar-sağlık%20%2B%20itham-C98A2B?style=flat-square">
  <a href="README.md"><img alt="English" src="https://img.shields.io/badge/docs-English-D11F26?style=flat-square"></a>
</p>

<p align="center">
  <a href="#kendiniz-üretin"><strong>Kendiniz üretin</strong></a>
  ·
  <a href="#bu-paketin-tuttuğu-iki-sınır"><strong>İki sınır</strong></a>
  ·
  <a href="#sözleşmenin-bizim-yerimize-verdiği-üç-karar"><strong>Sözleşmenin kararları</strong></a>
  ·
  <a href="README.md"><strong>English</strong></a>
</p>

---

> **Bu depoda motor kodu yoktur.** İçeriği bildirimler ve veridir. Onları okuyan
> motor [mintmark](https://github.com/lokomotifai/mintmark) deposundadır ve burada
> üst sınırı kapalı bir sürüm aralığıyla sabitlenmiştir.

Türkiye'deki her şirket çalışan verisi tutar ve bu verinin neredeyse hiçbiri test
ortamına taşınamaz. Bordro banka bilgisi taşır. İzin kayıtları hastalık günü
taşır. İşe alım adli sicil kontrolü taşır. Bu paket o veriyi bildirir, motor da
üretir: belirlenimci, aralık etiketli ve bir künye ile mühürlü.

**Sürüm 0.1, ön yayın. Yayımlanmış bir sürüm yok ve indirilebilecek bir referans
veri kümesi henüz mevcut değil.** Bugün doğru olanlar: `packcheck` sabitlenmiş
çekirdeğe karşı geçiyor, test paketi geçiyor ve değerlendirme tarifi on sekiz
kapsam hedefinin hepsini karşılıyor.

> [!IMPORTANT]
> **Bu paket ne değildir.** İK sisteminizin anonimleştirmesi değildir; hiçbir veri
> almaz. Uyum garantisi değildir, hukuki güvenli liman değildir. **Klinik veri
> değildir**: sağlık, tasarım gereği kategori ayrıntısında kalır. **Hiç kimse
> hakkında itham içermez**, sentetik olsun ya da olmasın: adli sicil yüzeyi bir
> belgenin istendiğini kaydeder, ne içerdiğini asla kaydetmez. Bordro tutarları
> hiçbir vergi mevzuatını ve asgari ücreti modellemez. Üretilen telefon numaraları
> tahsis edilmiş numaralarla çakışabilir, çünkü Türkiye numaralandırma planı
> kurgusal bir aralık ayırmaz. Bu veri sistemleri test etmek içindir. Hiçbir zaman
> kimseye ulaşmak için değildir.

## Burada ne var, ne yok

![İnsan kaynakları paketinin kayıt türlerini gösteren diyagram: kimlik numarası, on sekiz ile altmış beş yaş aralığından çekilen doğum tarihi ve referans değil çekiliş olan yönetici adı taşıyan çalışan; görev geçmişi; tür sütunu hiçbir etiket taşımayan izin kaydı; ve etiketli anomali türü taşıyan bordro kaydı. Altta kırmızı üç belge türü, performans notu, işe alım notu ve İK talebi, her biri bir etiket dosyası üretir; işe alım notu tasarım gereği hiçbir üst kayda bağlanmaz. En altta iki bant sağlık sınırını ve itham sınırını belirtir](assets/readme/record-map.png)

<p align="center"><sub><a href="assets/readme/record-map.svg">Erişilebilir SVG kaynağını görüntüleyin</a></sub></p>

| Burada var | Burada yok |
| --- | --- |
| Üçü serbest metin olmak üzere yedi kayıt türü | Motor kodu. Tek Python `tests/` ve `tools/` altında |
| Brüt, net, IBAN ve etiketli anomali türü taşıyan bordro | Vergi hesabı. Net bir çekiliştir, bir kesinti değil |
| Referans kontrolleri üzerinden ulaşılan adli sicil yüzeyi | Bir sicilin içeriğine dair herhangi bir ifade. Aşağıya bakın |
| Gerçek şirket listesine karşı taranan 26 kurgusal işveren adı | Gerçek şirket. Tarama CI'da her üretimde çalışır |

## Bu paketin tuttuğu iki sınır

Ailedeki paketlerin çoğu tek bir hassas yüzey tutar. Bu paket iki tane tutuyor ve
ikisi de gözden geçirmeyle değil bir denetimle tutuluyor, çünkü gözden geçirme
yorulur, liste yorulmaz.

### Sağlık kategori ayrıntısında kalır

Sağlık, İK metnine iki sıradan yoldan girer: gerekçe belirten bir izin talebi ve
çalışma düzenine değinen bir performans görüşmesi. İkisi de burada. Bir durum
sınıfı ve fazlası değil: teşhis yok, klinik bulgu yok, tedavi yok, ilaç yok,
prognoz yok.

Her sağlık aralığı çekirdeğin elle derlenmiş durum sınıfı tanımlayıcılarından
çekilir ve `lexicons/clinical_denied_tr.txt` bu paketin reddettiği söz dağarını
listeler. Bir test her üretilmiş belgeyi bu listeye karşı tarar. Hata biçimi
sessizdir, denetimin varlık nedeni budur: klinik ayrıntıya kayan bir şablon yine
de render olur, yine de etiketlenir ve diğer bütün kontrolleri yine de geçer.

### Adli sicil yüzeyi usule ilişkin kalır

Referans kontrolü bir süreçtir. Bu paketin belgeleri bir adli sicil belgesinin
**istendiğini**, **teslim alındığını** veya **beklendiğini** kaydeder. Ne
içerdiğini asla kaydetmez.

Bir kişinin suç işlediğini, mahkûm olduğunu veya soruşturulduğunu öne süren metin
o kişi hakkında bir ithamdır ve sentetik bir kişi de kişi biçimli bir iddiadır.
Sentetik insanları mahkûm eden metinle eğitilmiş bir model, aynı metni gerçek
insanlar hakkında üretmeyi öğrenir. Bu nedenle
`lexicons/accusatory_denied_tr.txt` bu paketin reddettiği 43 ifadeyi
listeler: mahkûmiyet, isnat, adlandırılmış suç sınıfları ve itham olarak
kurulmuş işyeri davranışı. Her üretilmiş belge bu listeye karşı taranır ve bir
test, listenin hâlâ yakaladığını kanıtlamak için reddedilmiş bir ifade eker.

## Sözleşmenin bizim yerimize verdiği üç karar

Hiçbiri gözden kaçmış değil ve üçü de okurun aksi hâlde hata sanacağı türden.

**İzin türü hiçbir etiket taşımaz, raporlu kodu dahil.** `leave_record.type`
yapısal bir enum ve son değeri `raporlu`. Buna HEALTH etiketi koymak bir
dedektöre, veritabanı sütunundaki yedi karakterlik bir enum değerinin sağlık
ifşası olduğunu öğretirdi; o veri kümesiyle yürütülen her değerlendirme de artık
dedektörleri kodları işaretleyip işaretlemediklerine göre puanlardı. Tespit
edilmeye değer sağlık sinyali belge gövdelerinde yaşar; orada bir durum sınıfı
akan Türkçe metinde geçer ve bir aralık onu gösterir.

**İşe alım notu hiçbir çalışana bağlanmaz.** Konusu bir adaydır ve aday tanımı
gereği henüz çalışan değildir. Buradaki bir üst kayıt referansı, paketin ürettiği
her veri kümesine bunun tersini yazardı. Tür, kayıt grafiğinde bir yetimdir;
verinin dürüst biçimi budur.

**Yönetici adı hiçbir çalışan kaydına karşılık gelmez.** Paket sözleşmesinde öz
referans yoktur, bu yüzden `employee.manager_name` bir soyadı sözlüğü çekilişidir.
Organizasyon şeması gezinmesi test edenler için bu gerçek bir modelleme kaybıdır
ve veri alındıktan sonra keşfedilmek yerine burada belirtilmiştir.

## Kendiniz üretin

```bash
uv tool install mintmark
git clone https://github.com/lokomotifai/mintmark-hr
cd mintmark-hr

mintmark packcheck .
mintmark mint --pack . --recipe workforce-baseline --seed 20261101 --out ./run
mintmark verify ./run
```

Üretildiği hâliyle bir işe alım notu:

```
Aday degerlendirme notu. Aday Mustafa Çelik, basvurdugu pozisyon
icin on_gorusme asamasinda degerlendirildi. Iletisim +90 597 216 26
34, eposta kullanici8708.9268@example.net. Onceki isvereni Anka
Lojistik. Teknik yetkinlik kismen karsiliyor olarak notlandi. Surec
devam ediyor.
```

Bu, [`samples/recruiter_note.jsonl`](samples/recruiter_note.jsonl) dosyasındaki
ilk kayıttır; README için yazılmış bir örnekleme değil. Bir test ikisini
karşılaştırır.

## Değerlendirme kümesi

`pii-eval` her etiket için bir kapsam hedefi bildirir ve on sekizinin hepsini
karşılar.

| Etiket grubu | Hedef | Ulaşılan |
| --- | --- | --- |
| PERSON, ADDRESS, ORG, DOB | her biri 300 | her biri 3000 |
| Sekiz özel nitelikli kategori | her biri 300 | 726 ile 773 arası |
| TCKN, VKN, IBAN, PAN, PHONE, EMAIL | her biri 500 | her biri 3000 |

Sekiz özel nitelikli etiket ve her biri için 300 aralık, 2400 yerleştirme demek.
Temel tarif özel oranını 0,06'da çalıştırır ve bu, temel belge hacminde o sayıya
yaklaşmaz; hedefe ulaşmak için temel oranı yükseltmek ise özel nitelikli
kategorilerin İK metninde gerçekte ne sıklıkta göründüğünü yanlış gösterirdi. Bu
yüzden değerlendirme ikizleri, oranı bir olan kendi şablon ailesine sahip ayrı
kayıt türleridir; şablon başına iki özel yuva, etiketlere eşit dağıtılmış.
Sigorta paketinin ikisi yerine üç belge ailesi olması aritmetiği burada rahat
kılıyor.

## Üç tarif

| Tarif | Biçim | Ne için |
| --- | --- | --- |
| **workforce-baseline** | 6 000 çalışan, 11 000 görev satırı, 24 000 izin kaydı, 72 000 bordro kaydı ve 11 000 belge | Bir test ortamını iş gücü gibi davranan bir şeyle doldurmak |
| **pii-eval** | 3 000 belge, her etiket hedefinin üzerinde | Türkçe İK metninde bir dedektörü ölçmek |
| **anomaly-mix** | Temel tarif artı her bordro kaydında etiketli bir anomali alanı | Bir izleme sistemini gerçek referansa karşı puanlamak |

### anomaly-mix'in açıkça belirtilen bir sınırı

Her bordro kaydı `anomaly_kind` ve `is_anomaly` taşır ve ikisi asla çelişmez. Ama
türler **bildirilmiş oranlarda çekilen satır başı etiketlerdir; gerçek zamansal
veya kayıtlar arası yapılar değil**. Gerçek bir bordro anomalisi, bir çalışanın
diğer aylarındaki örüntüyü bozan bir aydır; burada tek satırdaki bir etikettir.

Bu, gözden kaçmış bir nokta değil paket sözleşmesinin sınırıdır: her alan bağımsız
bir akıştan çekilir, dolayısıyla bir paket satırları ilişkilendiren bir örüntü
bildiremez. Bu tarifi hattınızın etiketleri doğru taşıyıp taşımadığını kontrol
etmek için kullanın. Bir dedektörün gerçek örüntüleri bulup bulmadığını ölçmek
için kullanmayın.

## Kendi insanlarımıza ateş eden bir denylist

Anlatmaya değer, çünkü bir denetimin varlık nedeni budur ve düzeltme belirtiyi
değil kuralı değiştirdi.

Bu paket işveren adları uyduruyor ve ne çekirdeğin banka listesi ne de sigorta
paketinin sigortacı listesi bir sanayi holdingiyle çakışmayı yakalamak için
kurulmuştu. Bu yüzden yaygın olarak bilinen 51 Türk kurumsal şirketinin bir
derlemesi paket denylist'ine girdi; her ad ayırt edici parçasına indirgenerek.

O indirgeme **Doğan Holding**'i `dogan`, **Yıldız Holding**'i `yildiz` yaptı. İkisi
de Türkiye'nin en yaygın soyadları arasında ve ikisi de çekirdeğin kendi soyadı
sözlüğünden çekiliyor. Liste tek bir temel üretimde dört kez ateşledi; her isabet
gerçek bir şirket değil sentetik bir çalışandı.

Paketin kendi verisini işaretleyen bir denylist, birinin kapatacağı bir
denylist'tir; bu yüzden kural değişti: tek kelimelik bir çekirdek artık
çekirdeğin ad, soyadı, il ve sokak sözlüklerine karşı denetleniyor ve ayırt edici
parçası sıradan bir Türkçe kelime olan bir ad, şirket adının tamamını koruyor.
Aynı kural `Toros Tarım`ın iki kelime olarak listelenmesinin nedeni; böylece
uydurma bir `Toros Lojistik` çakışmıyor, gerçek gübre üreticisi ise kapsanmaya
devam ediyor.

Belirtilmeye değer bir sınır var: işlem gören şirketlerin yetkili listesini borsa
yayımlıyor ve buradan makine tarafından okunabilir açık bir uç nokta olarak
erişilebilir değildi; dolayısıyla kullanılan liste sicilin kendisi değil bir
derlemedir. Borsanın kendi listesinin elle okunması yayın kontrol listesine
aittir. Kaydın tamamı
[docs/normative-verification.md](docs/normative-verification.md) dosyasında.

## Depo haritası

```
pack.yaml           kimlik, çekirdek sabitlemesi, izin verilen kimlik politikaları
fields/             üretim sırasına göre kayıt türü başına bir dosya
recipes/            workforce-baseline, pii-eval, anomaly-mix
templates/          temel kümeler ve ayrı değerlendirme kümeleri
lexicons/           kurgusal işverenler, unvanlar ve birimler, denylist ve bu
                    paketin reddettiği klinik ve itham söz dağarları
samples/            tür başına elli kayıt, sabit bir tohumdan yeniden üretilir
vendor/             zorunlu CI çalışmalarının kullandığı çekirdek wheel, sağlama ile
tests/              her iki sınır kontrolü dahil uygunluk paketi
docs/               referans veri kümesi kaydı ve doğrulama kaydı
```

## Depoyu geliştirin

```bash
uv sync
uv run mintmark packcheck .
uv run pytest
uv run python tools/mdlint.py .
```

Hepsi paketlenmiş çekirdek wheel'e karşı çevrimdışı çalışır.

## Proje durumu

Sürüm 0.1, ön yayın. Yayımlanmış sürüm yok, yayımlanmış veri kümesi yok. Referans
veri kümeleri [docs/reference-datasets.json](docs/reference-datasets.json)
dosyasında, kararlaştırılmış tohumlarıyla bildirilmiştir.

Bu paket diğerlerinde olmayan bir yönetişim kontrol noktası taşıyor: temel özel
oran ve özel nitelikli şablon alt kümesinin tamamı, herhangi bir kamuya açık
yayın yüzeyi oluşmadan önce kayıt altına alınmış bir onay gerektiriyor. Referans
veri kümelerinin yayımlanması ve veri kümesi lisansının teyidi bunun üzerine
gelen olağan dış kontrol noktalarıdır.

## Topluluk sözleşmesi

Katkılar Developer Certificate of Origin 1.1 kapsamında, katkıcı lisans sözleşmesi
olmadan kabul edilir. [CONTRIBUTING.md](CONTRIBUTING.md),
[GOVERNANCE.md](GOVERNANCE.md) ve [SECURITY.md](SECURITY.md) dosyalarına bakın.

`README.md` esas metindir ve bu dosya onun tam bir aynasıdır.

## Lisans ve marka

Apache-2.0. [LICENSE](LICENSE) ve [NOTICE](NOTICE) dosyalarına bakın. Lisans,
Mintmark adı veya logosu üzerinde hiçbir hak vermez; [TRADEMARKS.md](TRADEMARKS.md)
dosyasına bakın.

Yayımlanacak referans veri kümeleri için önerilen veri lisansı CC0-1.0'dır ve
hukuki teyit beklemektedir.

<p align="center"><sub>Mintmark ailesinin parçası: <a href="https://github.com/lokomotifai/mintmark">motor</a> · <a href="https://github.com/lokomotifai/mintmark-banking">bankacılık</a> · <a href="https://github.com/lokomotifai/mintmark-insurance">sigorta</a></sub></p>
