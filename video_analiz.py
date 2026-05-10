import cv2
import os
import matplotlib.pyplot as plt

# Video dosyası
VIDEO_DOSYASI = "video.mp4"

# Video bilgilerini göster
cap = cv2.VideoCapture(VIDEO_DOSYASI)

fps = cap.get(cv2.CAP_PROP_FPS)
frame_sayisi = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
genislik = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
yukseklik = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
sure = frame_sayisi / fps

print(f"Video Bilgileri:")
print(f"  FPS: {fps}")
print(f"  Toplam Frame: {frame_sayisi}")
print(f"  Boyut: {genislik}x{yukseklik}")
print(f"  Süre: {sure:.1f} saniye")

# Her 30 frame'de bir görüntü al
os.makedirs("kareler", exist_ok=True)
kaydedilen = []
frame_no = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    if frame_no % 30 == 0:
        dosya_adi = f"kareler/frame_{frame_no:04d}.jpg"
        cv2.imwrite(dosya_adi, frame)
        kaydedilen.append(dosya_adi)
    frame_no += 1

cap.release()
print(f"\n{len(kaydedilen)} kare kaydedildi!")

# İlk 6 kareyi göster
fig, axlar = plt.subplots(2, 3, figsize=(15, 8))
fig.suptitle("Video Kareleri", fontsize=14)

for i, kare_yolu in enumerate(kaydedilen[:6]):
    goruntu = cv2.imread(kare_yolu)
    goruntu = cv2.cvtColor(goruntu, cv2.COLOR_BGR2RGB)
    ax = axlar[i // 3][i % 3]
    ax.imshow(goruntu)
    ax.set_title(f"Frame {i*30}")
    ax.axis("off")

plt.tight_layout()
plt.savefig("video_kareleri.png")
plt.show()
print("Görsel kaydedildi: video_kareleri.png")