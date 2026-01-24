# 📦 Video Processor - Shared Library

Biblioteca compartilhada contendo Value Objects, DTOs, Events e Exceptions usados por todos os microserviços.

## 📐 Arquitetura

Esta biblioteca é utilizada por todos os microserviços:

```
fiap-soat-video-shared/
├── src/video_processor_shared/
│   ├── domain/
│   │   ├── value_objects/    # Email, Password, JobStatus
│   │   ├── events/           # JobStarted, JobCompleted, JobFailed
│   │   └── exceptions/       # Domain-specific exceptions
│   ├── dto/                  # Data Transfer Objects
│   └── contracts/            # API response contracts
└── tests/
```

## 🚀 Instalação

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

## 📖 Uso

### Value Objects

```python
from video_processor_shared.domain.value_objects import JobStatus, Email, Password

# Job Status
status = JobStatus.PENDING
if status == JobStatus.COMPLETED:
    print("Job finalizado!")

# Email validation
email = Email("user@example.com")

# Password validation
password = Password("SecurePass123!")
```

### Events

```python
from video_processor_shared.domain.events import JobCompleted, JobFailed

# Publicar evento de job completo
event = JobCompleted(
    job_id=uuid4(),
    user_id=uuid4(),
    video_id=uuid4(),
    output_url="https://s3.../frames.zip"
)
```

### DTOs

```python
from video_processor_shared.dto import JobDTO, UserDTO, VideoDTO

job = JobDTO(
    id=uuid4(),
    status="COMPLETED",
    progress=100
)
```

## 🧪 Testes

```bash
pytest tests/ -v --cov=video_processor_shared
```

## 📝 Componentes

| Componente | Descrição |
|------------|-----------|
| `JobStatus` | Enum: PENDING, PROCESSING, COMPLETED, FAILED, CANCELLED |
| `Email` | Value Object com validação de email |
| `Password` | Value Object com validação de senha forte |
| `JobStarted` | Evento disparado quando job inicia |
| `JobCompleted` | Evento disparado quando job completa |
| `JobFailed` | Evento disparado quando job falha |
| `VideoUploaded` | Evento disparado quando vídeo é uploaded |

## 📄 Licença

MIT License
