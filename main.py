import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/path/to/google-cloud-storage-key.json'
from google.cloud import storage
import csv
import uuid


def upload_to_gcs(bucket_name, local_file_path, remote_file_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(remote_file_name)
    blob.upload_from_filename(local_file_path)
    print(f"파일이 성공적으로 업로드되었습니다: gs://{bucket_name}/{remote_file_name}")
    return f"https://storage.googleapis.com/{bucket_name}/{remote_file_name}"

def write_csv_file(csv_file_path, data):
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['폴더이름', '사진링크'])
        writer.writerows(data)
    print(f"CSV 파일이 작성되었습니다: {csv_file_path}")

# 사용 예시:
bucket_name = 'artbridge-bucket'
image_directory = 'images/images'  # 이미지 파일들이 있는 상위 디렉토리 경로
csv_file_path = 'result.csv'  # 작성될 CSV 파일 경로

# 데이터 예시
data = []

# 현재 스크립트 파일의 디렉토리 경로를 기준으로 상대 경로 계산
script_directory = os.path.dirname(os.path.abspath(__file__))
image_directory = os.path.join(script_directory, image_directory)
csv_file_path = os.path.join(script_directory, csv_file_path)

# 각 폴더의 이미지 파일 업로드 및 CSV 작성
for folder_name in os.listdir(image_directory):
    folder_path = os.path.join(image_directory, folder_name)
    if os.path.isdir(folder_path):
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.jpg'):
                local_file_path = os.path.join(folder_path, file_name)
                remote_file_name = str(uuid.uuid4()) + '.jpg'
                # 파일 업로드
                url = upload_to_gcs(bucket_name, local_file_path, remote_file_name)
                # 데이터 추가
                data.append([folder_name, url])

# CSV 파일 작성
write_csv_file(csv_file_path, data)
