# fiap-soat-video-shared

## Introdução
Biblioteca compartilhada do ecossistema FIAP SOAT Video Processor. Ela concentra contratos, eventos de domínio, value objects e utilitários AWS usados pelos microserviços.

## Sumário
- Explicação do projeto
- Objetivo
- Como funciona
- Repositórios relacionados
- Integrações com outros repositórios
- Como executar
- Como testar

## Repositórios relacionados
- [fiap-soat-video-local-dev](https://github.com/SOAT-264/fiap-soat-video-local-dev)
- [fiap-soat-video-auth](https://github.com/SOAT-264/fiap-soat-video-auth)
- [fiap-soat-video-jobs](https://github.com/SOAT-264/fiap-soat-video-jobs)
- [fiap-soat-video-notifications](https://github.com/SOAT-264/fiap-soat-video-notifications)
- [fiap-soat-video-service](https://github.com/SOAT-264/fiap-soat-video-service)

## Explicação do projeto
Este repositório não expõe API própria. Ele é um pacote Python reutilizável com:
- `domain`: eventos, exceções e value objects.
- `contracts` e `dto`: modelos compartilhados para troca de dados.
- `aws`: wrappers para S3, SQS, SNS e SES.

Sua principal função é evitar duplicação de regras e manter contratos consistentes em todo o sistema.

## Objetivo
Padronizar o núcleo de contratos e comportamentos transversais da arquitetura de microserviços.

## Como funciona
1. Os microserviços instalam este pacote como dependência (`video-processor-shared`).
2. Eventos de domínio comuns (`VideoUploadedEvent`, `JobCompletedEvent`, `JobFailedEvent`) são reaproveitados nos fluxos assíncronos.
3. Value objects como `Email`, `Password` e `JobStatus` reforçam regras de domínio compartilhadas.
4. Adaptadores AWS compartilham padrão de acesso para storage e mensageria.

## Integrações com outros repositórios
| Repositório integrado | Como integra | Para que serve |
| --- | --- | --- |
| `fiap-soat-video-auth` | Reuso de value objects e exceções de domínio | Uniformizar validações de identidade e erros de negócio |
| `fiap-soat-video-service` | Reuso de eventos/exceções (`VideoUploadedEvent`, erros de upload) | Padronizar contratos do início do pipeline de vídeo |
| `fiap-soat-video-jobs` | Reuso de eventos e `JobStatus` | Padronizar estados e eventos de processamento |
| `fiap-soat-video-notifications` | Dependência de contratos compartilhados no ecossistema | Garantir consistência entre eventos recebidos e enviados |
| `fiap-soat-video-local-dev` | Imagens Docker dos serviços instalam o pacote localmente no build | Garantir que todos os serviços rodem com o mesmo contrato compartilhado |

## Como executar
### Pré-requisitos
- Python 3.11+

### Instalar em modo desenvolvimento
```powershell
cd /fiap-soat-video-shared
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

### Verificação rápida do pacote
```powershell
cd /fiap-soat-video-shared
.\.venv\Scripts\Activate.ps1
python -c "from video_processor_shared import VideoUploadedEvent, JobStatus; print(VideoUploadedEvent.__name__, JobStatus.PENDING.value)"
```

## Como testar
```powershell
cd /fiap-soat-video-shared
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest
```

