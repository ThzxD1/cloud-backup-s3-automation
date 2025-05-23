import boto3
import os
import json
import logging
import hashlib
import tarfile
import zipfile
from datetime import datetime

# Carrega configuração
with open('config/config.json') as f:
    config = json.load(f)

SOURCE_DIR = config['source_dir']
S3_BUCKET = config['s3_bucket']
LOG_FILE = config['log_file']
COMPRESSION = config.get('compression', 'none')
INCREMENTAL = config.get('incremental', False)

logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

s3 = boto3.client('s3')

def file_hash(file_path):
    """Gera hash SHA1 do arquivo"""
    sha1 = hashlib.sha1()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha1.update(chunk)
    return sha1.hexdigest()

def s3_file_exists(bucket, key, local_hash):
    try:
        response = s3.head_object(Bucket=bucket, Key=key)
        return response['Metadata'].get('file-hash') == local_hash
    except s3.exceptions.ClientError:
        return False

def compress_directory():
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    output_file = f"/tmp/backup-{timestamp}"
    
    if COMPRESSION == 'zip':
        output_path = f"{output_file}.zip"
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(SOURCE_DIR):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, SOURCE_DIR)
                    zipf.write(full_path, arcname=rel_path)
    elif COMPRESSION == 'tar':
        output_path = f"{output_file}.tar.gz"
        with tarfile.open(output_path, "w:gz") as tar:
            tar.add(SOURCE_DIR, arcname=os.path.basename(SOURCE_DIR))
    else:
        return None

    return output_path

def upload_file(file_path, key, extra_args=None):
    try:
        s3.upload_file(file_path, S3_BUCKET, key, ExtraArgs=extra_args or {})
        logging.info(f"{datetime.now()} - Upload: {file_path} -> s3://{S3_BUCKET}/{key}")
    except Exception as e:
        logging.error(f"{datetime.now()} - Falha no upload de {file_path}: {e}")

def full_upload():
    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, SOURCE_DIR)
            key = rel_path.replace("\\", "/")  # compatível com S3

            if INCREMENTAL:
                hash_val = file_hash(full_path)
                if s3_file_exists(S3_BUCKET, key, hash_val):
                    logging.info(f"{datetime.now()} - Ignorado (sem alterações): {rel_path}")
                    continue
                upload_file(full_path, key, extra_args={'Metadata': {'file-hash': hash_val}})
            else:
                upload_file(full_path, key)

if __name__ == '__main__':
    if COMPRESSION in ['zip', 'tar']:
        archive_path = compress_directory()
        if archive_path:
            upload_file(archive_path, os.path.basename(archive_path))
    else:
        full_upload()
