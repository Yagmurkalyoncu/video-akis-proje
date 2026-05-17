import boto3
import os

s3 = boto3.client('s3', region_name='us-east-1')
BUCKET = 'video-akis-proje'

kareler = os.listdir('kareler')
for kare in kareler:
    s3.upload_file(f'kareler/{kare}', BUCKET, f'kareler/{kare}')
    print(f"Yüklendi: {kare}")

print("Tüm kareler S3'e yüklendi!")