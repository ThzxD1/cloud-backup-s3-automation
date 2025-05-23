![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![AWS](https://img.shields.io/badge/AWS-S3-orange?logo=amazon-aws)
![License](https://img.shields.io/badge/License-MIT-green)
# Cloud Backup Automation com AWS S3

Automatize seus backups locais com segurança e flexibilidade utilizando Python, AWS S3 e agendamento via cron.

## 🔧 Stack Utilizada

- Python 3
- Boto3 (AWS SDK para Python)
- AWS CLI (pré-requisito)
- Cron (Linux)

## 🚀 Funcionalidades

- Backup automático de arquivos locais para S3
- Log de execução com datas e status
- Organização por pastas e estrutura replicada no S3
- Agendamento via cron

## 🗂️ Estrutura do Projeto

cloud-backup-s3-automation/
├── backup/
│   └── main.py            # Script principal de backup
├── config/
│   └── config.json        # Configurações de diretório e bucket
├── logs/                  # Pasta para armazenar logs (mantida com .gitkeep)
│   └── .gitkeep
├── requirements.txt       # Dependências do projeto
├── README.md              # Instruções e documentação             
└── .gitignore             # Arquivos e pastas ignorados pelo Git

## 🔧 Configuração (config/config.json)
```json
{
  "source_dir": "/caminho/dos/arquivos",
  "s3_bucket": "nome-do-bucket",
  "log_file": "logs/backup.log",
  "compression": "zip",      // ou "tar" ou "none"
  "incremental": true        // evita reenvio de arquivos inalterados
}
```
| Parâmetro       | Descrição                                      | Opções                |
|------------------|------------------------------------------------|------------------------|
| `source_dir`     | Caminho da pasta a ser enviada                 | Ex: `/home/user/data` |
| `s3_bucket`      | Nome do bucket S3 de destino                   | Ex: `backup-cloud`    |
| `log_file`       | Caminho do arquivo de log                      | Ex: `logs/backup.log` |
| `compression`    | Tipo de compressão antes do envio              | `zip`, `tar`, `none`  |
| `incremental`    | Ativa o envio apenas de arquivos alterados     | `true`, `false`       |

## 🔍 Testes Locais

Antes de agendar com `cron`, execute manualmente:

```bash
python3 backup/main.py


## ✨ Novidades

- ✅ Suporte a compressão `.zip` e `.tar.gz` (configurável)
- ✅ Backup incremental com verificação de hash SHA1
- ✅ Upload seguro e com metadados no S3
