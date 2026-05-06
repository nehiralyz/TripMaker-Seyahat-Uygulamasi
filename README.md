# ✈️ TripMaker - Kapsamlı Seyahat Planlama ve Yönetim Sistemi

![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg?logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/GUI-PyQt5-brightgreen.svg?logo=qt&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite3-lightgrey.svg?logo=sqlite&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

TripMaker, Python ve PyQt5 kullanılarak geliştirilmiş, modern arayüze sahip bir seyahat asistanı ve biletleme otomasyonudur. Kullanıcıların sıfırdan detaylı bir tatil rotası oluşturmasına veya sistemdeki hazır paketleri tek tıkla satın almasına olanak tanır.

Uçak biletinden konaklamaya, şehir içi transferden aktivitelere kadar tüm süreci tek ekrandan yöneterek toplam bütçeyi hesaplar ve SQLite veritabanında güvenle saklar.

---

## 📸 Ekran Görüntüleri

*(Not: Ekran görüntülerini GitHub'da bu dosyayı düzenlerken direkt buraya sürükleyip bırakabilirsiniz)*

### 1. Yeni Rota Çizimi (Akıllı Form)
> *Ülke seçimine göre şehirlerin filtrelendiği, şehir seçildiğinde havalimanı ve transfer rotasının otomatik doldurulduğu dinamik planlama ekranı.*
<img width="1586" height="818" alt="Ekran görüntüsü 2026-05-06 205018" src="https://github.com/user-attachments/assets/20e88a98-e823-485c-86d2-9ba3434cb183" />

### 2. Önerilen Paket Rotalar
> *Roma, Paris, Kapadokya, Dubai gibi popüler destinasyonlar için önceden bütçelendirilmiş hazır tatil paketlerinin tek tıkla alındığı vitrin.*
<img width="1613" height="928" alt="Ekran görüntüsü 2026-05-06 205033" src="https://github.com/user-attachments/assets/2c1e9538-d99c-4e98-9f2c-efa85fc2ac36" />

### 3. Seyahat Listesi ve İptal Yönetimi
> *Seyahate kalan günlerin (veya "Tamamlandı" durumunun) dinamik hesaplandığı, detayların incelenebildiği ve iptal işlemlerinin yapıldığı kontrol paneli.*
<img width="1599" height="501" alt="Ekran görüntüsü 2026-05-06 205046" src="https://github.com/user-attachments/assets/82db71dc-5de6-4176-b4a3-ad469dd1d8fc" />

---

## 🚀 Temel Özellikler ve Modüller

Uygulama 3 ana modülden oluşmaktadır:

### 🌍 1. Dinamik Rota ve Planlama (Yeni Seyahat)
* **Akıllı Lokasyon Asistanı:** Seçilen ülkeye (Örn: Türkiye, İtalya, Fransa) göre şehirlerin listelenmesi ve hedef şehre göre (Örn: Paris) uygun havalimanı rotasının (İst -> Paris CDG -> Şehir Merkezi) sisteme otomatik yazılması.
* **Kapsamlı Maliyet Hesaplama:** Ulaşım (Uçak, Otobüs vb.) ve Konaklama (gecelik fiyat x kalınacak gün) masraflarının birleştirilerek otomatik toplam bütçe çıkarılması.
* **Gidiş-Dönüş Yönetimi:** Dönüş bileti istenirse, konaklanacak gece sayısına göre dönüş tarihinin otomatik belirlenmesi.

### 🌟 2. Hazır Paket Vitrini
* Kullanıcılara detaylı düşünülmüş hazır turlar sunan ekran. 
* Sadece yolcu iletişim bilgileri girilerek bütün otel, uçuş ve aktivite planının saniyeler içinde veritabanına işlenmesi.

### 📊 3. Seyahatlerim ve Operasyon Yönetimi
* **Durum Takibi:** Sistemdeki her seyahatin tarihinin bugünün tarihiyle karşılaştırılarak "Bugün!", "Tamamlandı" veya "X gün kaldı" şeklinde dinamik durum bildirimleri.
* **Bilet İptali:** İptal edilen seyahat planlarının veritabanından kalıcı olarak silinmesi ve listenin anında güncellenmesi.
* **Gelişmiş İnceleme:** Yolcu bilgisi, bütçe dağılımı ve tur planının (aktiviteler dahil) detaylı pop-up ekranında gösterilmesi.

---

## 🗄️ Veritabanı Mimarisi

Proje, herhangi bir sunucu kurulumu gerektirmeyen gömülü **SQLite3** altyapısını kullanır. Veritabanı (`seyahat_veritabani.db`) uygulama ilk çalıştığında otomatik olarak oluşturulur. 

Tüm veriler geniş kapsamlı **`seyahatler`** tablosunda tutulur:
* `id`, `gidis_yeri`, `tarih`, `otel_adi`, `otel_fiyat`, `gece`, `rota`, `aktiviteler`, `yolcu_ad`, `yolcu_email`, `yolcu_tel`, `donus_tarihi`, `ulasim_fiyati`, `ulasim_tipi`.

Sistem arka planda bu verileri çekerken Object-Oriented (Nesne Yönelimli) bir yaklaşım kullanarak `Seyahat`, `Konaklama` ve `Plan` sınıfları (class) aracılığıyla verileri işler.

---

## 💻 Kurulum ve Çalıştırma

Projeyi bilgisayarınızda yerel olarak çalıştırmak için aşağıdaki adımları izleyebilirsiniz.

**Ön Koşullar:**
* Python 3.8 veya üzeri bir sürüm.
* İşletim sistemi: Windows, macOS veya Linux.

**Adımlar:**

1. Repoyu bilgisayarınıza klonlayın:
   ```bash
   git clone [https://github.com/KULLANICI_ADINIZ/TripMaker.git](https://github.com/KULLANICI_ADINIZ/TripMaker.git)
   cd TripMaker
