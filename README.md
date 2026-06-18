# 🎬 Video Akışı ve İşleme Projesi
**3522 Bulut Bilişim Dersi — Proje 6**
youtube link: https://www.youtube.com/watch?v=BTl2FG5WMIE
*Trafik videoları üzerinde AWS Rekognition ile gerçek zamanlı nesne tespiti ve bulut tabanlı video işleme*

## 🎯 Proje Hakkında

Bu proje, trafik videoları üzerinde **AWS Rekognition** yapay zeka servisi kullanarak otomatik nesne tespiti ve etiketleme gerçekleştiren bir bulut uygulamasıdır.

**OpenCV** ile video karelerine ayrılan görüntüler, AWS Rekognition API'sine gönderilerek araç, yol, dış mekan gibi nesneler yüksek güven skoru ile tespit edilmektedir. Tüm analiz sonuçları **AWS DynamoDB** veritabanına, video kareleri ise **AWS S3** depolama hizmetine kaydedilmektedir.

### Gerçek Hayat Uygulama Alanları

- 🚦 Akıllı trafik yönetimi
- 📷 Güvenlik kamerası izleme
- 🚗 Otomatik araç sayımı
- 🏙️ Kentsel planlama ve analiz

---

## 🛠 Kullanılan Teknolojiler

| Teknoloji | Kullanım Amacı |
|-----------|----------------|
| Python 3.11 | Ana programlama dili |
| OpenCV | Video işleme ve kare çıkarma |
| Boto3 | AWS SDK |
| Matplotlib | Sonuç görselleştirme |
| Pillow | Görüntü işleme |
| AWS Rekognition | Nesne tanıma ve etiketleme |
| AWS S3 | Video karelerinin bulut depolama |
| AWS DynamoDB | Analiz sonuçları veritabanı |
| AWS IAM | Güvenli erişim yönetimi |

---

## 🏗 Sistem Mimarisi

```
📹 Video (MP4)
       │
       ▼
🔧 OpenCV — Kare Çıkarma (Her 150 frame'de 1 kare)
       │
       ▼
☁️  AWS Rekognition — DetectLabels API
       │
       ├──────────────────────┐
       ▼                      ▼
🪣 AWS S3               🗄️ AWS DynamoDB
(Video Kareleri)        (Analiz Sonuçları)
```

---

## ⚙️ Kurulum

### Gereksinimler

```bash
pip install boto3 opencv-python matplotlib pillow
```

### AWS CLI Kurulumu

```bash
# AWS CLI kur ve yapılandır
aws configure
# Access Key ID, Secret Key, Region: us-east-1
```

### IAM İzinleri

Aşağıdaki politikaların IAM kullanıcısına eklenmiş olması gerekir:
- `AmazonRekognitionFullAccess`
- `AmazonS3FullAccess`
- `AmazonDynamoDBFullAccess`

---

## 🚀 Kullanım

### 1. Video Analizi — Kare Çıkarma

```bash
python video_analiz.py
```

Video dosyasından her 150 frame'de bir kare alır, `kareler/` klasörüne kaydeder.

### 2. AWS Rekognition Analizi

```bash
python rekognition_analiz.py
```

Her kareyi Rekognition API'sine gönderir, nesneleri tespit eder, sonuçları görselleştirir ve DynamoDB'ye kaydeder.

### 3. S3'e Yükleme

```bash
python s3_yukle.py
```

Tüm video karelerini AWS S3 bucket'ına yükler.

---

## 📊 Sonuçlar

### Tespit Edilen Nesneler ve Güven Skorları

| Nesne | Güven Skoru | Açıklama |
|-------|-------------|----------|
| 🛣️ Road | %98.8 | Yol/asfalt tespiti |
| 🌳 Outdoors | %98.7 | Açık alan tespiti |
| 🚗 Vehicle | %86.5 | Genel araç tespiti |
| 🚌 Transportation | %86.5 | Ulaşım kategorisi |
| 🚙 Car | %85.4 | Binek araç tespiti |

> **Not:** AWS Rekognition hiyerarşik etiketleme sistemi kullanır. Car tespit edildiğinde otomatik olarak Vehicle ve Transportation da döndürülür.

---

## ☁️ AWS Servisleri

### S3 Bucket
- **Bucket Adı:** `video-akis-proje`
- **İçerik:** Video kareleri (JPEG formatında)
- **Bölge:** us-east-1

### DynamoDB Tablosu
- **Tablo Adı:** `video-analiz-sonuclari`
- **Partition Key:** `analiz_id` (UUID)
- **Alanlar:** analiz_id, kare, etiketler, tarih

---

## 📁 Dosya Yapısı

```
video-akis-proje/
├── video.mp4                  # Kaynak video
├── video_analiz.py            # Video kare çıkarma
├── rekognition_analiz.py      # AWS Rekognition analizi
├── s3_yukle.py                # S3 yükleme
├── video_kareleri.png         # Video karelerinin görseli
├── kareler/                   # Çıkarılan kareler
│   ├── frame_0000.jpg
│   ├── frame_0150.jpg
│   └── ...
├── sonuclar/                  # Analiz sonuç görselleri
│   ├── sonuc_1.png
│   └── ...
└── README.md
```

## 👩‍💻 Geliştirici

**Yağmur Kalyoncu**

- GitHub:https://github.com/Yagmurkalyoncu

3522 Bulut Bilişim Dersi — Mayıs 2026

