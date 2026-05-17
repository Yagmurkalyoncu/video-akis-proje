import boto3
import cv2
import json
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

# AWS bağlantısı
rekognition = boto3.client('rekognition', region_name='us-east-1')

KARELER_KLASORU = "kareler"
SONUCLAR_KLASORU = "sonuclar"
os.makedirs(SONUCLAR_KLASORU, exist_ok=True)

def kare_analiz_et(goruntu_yolu):
    with open(goruntu_yolu, 'rb') as f:
        goruntu_bytes = f.read()
    
    response = rekognition.detect_labels(
        Image={'Bytes': goruntu_bytes},
        MaxLabels=10,
        MinConfidence=70
    )
    return response['Labels']

def sonuc_goster(goruntu_yolu, etiketler, kayit_yolu):
    goruntu = cv2.imread(goruntu_yolu)
    goruntu = cv2.cvtColor(goruntu, cv2.COLOR_BGR2RGB)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    ax1.imshow(goruntu)
    ax1.set_title("Video Karesi", fontsize=12)
    ax1.axis("off")
    
    isimler = [e['Name'] for e in etiketler[:8]]
    guvenler = [e['Confidence'] for e in etiketler[:8]]
    
    renkler = ['#2196F3' if g > 90 else '#4CAF50' for g in guvenler]
    bars = ax2.barh(isimler, guvenler, color=renkler)
    ax2.set_xlim(0, 100)
    ax2.set_xlabel("Güven Skoru (%)")
    ax2.set_title("Tespit Edilen Nesneler", fontsize=12)
    
    for bar, guven in zip(bars, guvenler):
        ax2.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                f'%{guven:.1f}', va='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(kayit_yolu)
    plt.close()

# İlk 5 kareyi analiz et
kareler = sorted(os.listdir(KARELER_KLASORU))[:5]
tum_sonuclar = []

print("AWS Rekognition ile video analizi başlıyor...\n")

for i, kare_dosyasi in enumerate(kareler):
    kare_yolu = os.path.join(KARELER_KLASORU, kare_dosyasi)
    print(f"Analiz ediliyor: {kare_dosyasi}")
    
    etiketler = kare_analiz_et(kare_yolu)
    
    print(f"  Tespit edilen nesneler:")
    for etiket in etiketler[:5]:
        print(f"    - {etiket['Name']}: %{etiket['Confidence']:.1f}")
    
    kayit_yolu = os.path.join(SONUCLAR_KLASORU, f"sonuc_{i+1}.png")
    sonuc_goster(kare_yolu, etiketler, kayit_yolu)
    
    tum_sonuclar.append({
        'kare': kare_dosyasi,
        'etiketler': [{'isim': e['Name'], 'guven': e['Confidence']} 
                      for e in etiketler]
    })
    print(f"  Sonuç kaydedildi: {kayit_yolu}\n")

# JSON olarak kaydet
with open('analiz_sonuclari.json', 'w', encoding='utf-8') as f:
    json.dump(tum_sonuclar, f, ensure_ascii=False, indent=2)

print("Tüm analizler tamamlandı!")
print(f"Sonuçlar '{SONUCLAR_KLASORU}' klasöründe.")
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
tablo = dynamodb.Table('video-analiz-sonuclari')

# DynamoDB tablosu oluştur (ilk çalıştırmada)
try:
    tablo = dynamodb.create_table(
        TableName='video-analiz-sonuclari',
        KeySchema=[{'AttributeName': 'analiz_id', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'analiz_id', 'AttributeType': 'S'}],
        BillingMode='PAY_PER_REQUEST'
    )
    tablo.wait_until_exists()
    print("DynamoDB tablosu oluşturuldu!")
except:
    tablo = dynamodb.Table('video-analiz-sonuclari')

# Sonuçları kaydet
for sonuc in tum_sonuclar:
    tablo.put_item(Item={
        'analiz_id': str(uuid.uuid4()),
        'kare': sonuc['kare'],
        'etiketler': str(sonuc['etiketler']),
        'tarih': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

print("Tüm sonuçlar DynamoDB'ye kaydedildi!")