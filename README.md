# 📦 Video Processor - Shared Library

[![PyPI](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Biblioteca compartilhada contendo Value Objects, DTOs, Events e AWS Clients usados por todos os microserviços.

## 📋 Índice

- [Instalação](#-instalação)
- [Componentes](#-componentes)
- [Uso](#-uso)
- [AWS Services](#-aws-services)
- [Testes](#-testes)

---

## 📦 Instalação

### Via pip (de outro microserviço)

```bash
pip install git+https://github.com/morgadope/fiap-soat-video-shared.git
```

### Para desenvolvimento local

```bash
git clone https://github.com/morgadope/fiap-soat-video-shared.git
cd fiap-soat-video-shared
pip install -e ".[dev]"
```

---

## 🧩 Componentes

### Value Objects

```python
from video_processor_shared.domain.value_objects import JobStatus, Email, Password

# Job Status (Enum)
status = JobStatus.PENDING  # PENDING, PROCESSING, COMPLETED, FAILED, CANCELLED

# Email (validação automática)
email = Email("user@example.com")

# Password (requer senha forte)
password = Password("SecurePass123!")
```

### Domain Events

```python
from video_processor_shared.domain.events import (
    VideoUploaded,
    JobStarted,
    JobCompleted,
    JobFailed,
)

# Evento de job completo
event = JobCompleted(
    job_id=uuid4(),
    user_id=uuid4(),
    video_id=uuid4(),
    output_url="https://s3.../frames.zip",
    frame_count=120,
)
```

### DTOs

```python
from video_processor_shared.dto import JobDTO, UserDTO, VideoDTO

job = JobDTO(
    id=uuid4(),
    status="COMPLETED",
    progress=100,
    output_url="https://..."
)
```

---

## ☁️ AWS Services

A biblioteca inclui clients para integração com AWS (funcionam com LocalStack e AWS real):

### S3 Storage

```python
from video_processor_shared.aws.s3_storage import S3StorageService

s3 = S3StorageService()

# Upload
key = await s3.upload_video(file, "video.mp4", "user-123")

# Download URL
url = s3.get_download_url(key, expires_in=3600)
```

### SQS Queue

```python
from video_processor_shared.aws.sqs_service import SQSService

sqs = SQSService(queue_name="job-queue")

# Enviar mensagem
await sqs.send_message({"job_id": "123", "video_key": "..."})

# Receber mensagens
messages = await sqs.receive_messages(max_messages=5)
```

### SNS Topics

```python
from video_processor_shared.aws.sns_service import SNSService

sns = SNSService(topic_name="job-events")

# Publicar evento
await sns.publish_job_completed(
    job_id="123",
    user_id="456",
    video_id="789",
    output_url="https://...",
    frame_count=100,
)
```

### SES Email

```python
from video_processor_shared.aws.ses_service import SESService

ses = SESService()

# Enviar email
await ses.send_job_completed_email(
    to="user@example.com",
    video_name="video.mp4",
    frame_count=100,
    download_url="https://..."
)
```

---

## 🔧 Configuração

Configure via variáveis de ambiente:

```bash
# Para LocalStack
export AWS_ENDPOINT_URL=http://localhost:4566
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_REGION=us-east-1

# Para AWS real (não precisa de endpoint)
# Apenas configure as credenciais AWS
```

---

## 🧪 Testes

```bash
pytest tests/ -v --cov=video_processor_shared
```

---

## 📁 Estrutura

```
src/video_processor_shared/
├── domain/
│   ├── value_objects/    # Email, Password, JobStatus
│   ├── events/           # DomainEvents
│   └── exceptions/       # Custom exceptions
├── dto/                  # Data Transfer Objects
├── contracts/            # API response contracts
└── aws/                  # AWS service clients
    ├── __init__.py       # Client factory
    ├── s3_storage.py    
    ├── sqs_service.py   
    ├── sns_service.py   
    └── ses_service.py   
```

---

## 📄 Licença

MIT License
