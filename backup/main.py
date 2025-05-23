import boto3
import os
import json
import logging
from datetime import datetime

# Carrega configuração
with open('config/config.json') as f:
    config = json.load(f)

SOURCE_DIR = config['source_dir']
S3_BUCKET = config['s3_bucket']
LOG_FILE = config['log_file']

# Configuração de log
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

def upload_files():
    s3 = boto3.client('s3')
    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            s3_key = os.path.relpath(file_path, SOURCE_DIR)
            try:
                s3.upload_file(file_path, S3_BUCKET, s3_key)
                logging.info(f"{datetime.now()} - Upload: {file_path} -> s3://{S3_BUCKET}/{s3_key}")
            except Exception as e:
                logging.error(f"{datetime.now()} - Erro ao enviar {file_path}: {e}")

if __name__ == '__main__':
    upload_files()
