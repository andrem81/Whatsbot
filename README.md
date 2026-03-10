# WhatsApp Bot com RAG, Redis e Evolution API

Backend em Python para atendimento automatizado no WhatsApp com recuperação de contexto via RAG e memória conversacional por sessão. A aplicação recebe eventos da Evolution API, consulta uma base documental local e envia respostas geradas por modelo da OpenAI.

## Sobre o projeto

Este projeto foi desenvolvido como projeto de portfólio durante o curso **WhatsApp Bot Master**, da **PycodeBR**. A implementação presente neste repositório foi expandida além da proposta base do curso com uma organização modular do backend, uso de **FastAPI** para webhook, memória conversacional com **Redis**, persistência vetorial com **ChromaDB**, ingestão local de arquivos `.pdf` e `.txt` e orquestração com **Docker Compose**.

Essas adaptações deixam o projeto mais próximo de um cenário real de integração entre mensageria, IA generativa e recuperação de conhecimento.

## Tecnologias utilizadas

- Python 3.13
- FastAPI
- Uvicorn
- LangChain
- OpenAI API
- ChromaDB
- Redis
- Evolution API
- Docker
- Docker Compose

## Funcionalidades principais

- Recebimento de mensagens do WhatsApp via webhook
- Geração de respostas automáticas com modelos da OpenAI
- Recuperação de contexto com RAG a partir de documentos locais
- Memória conversacional por sessão usando Redis
- Persistência de embeddings em ChromaDB
- Ingestão de arquivos `.pdf` e `.txt` para atualizar a base de conhecimento
- Execução local via Python ou containers

## Como executar localmente

### Pré-requisitos

- Python 3.13
- Docker e Docker Compose
- Conta com acesso à OpenAI API
- Instância configurada da Evolution API

### 1. Clonar o projeto

```bash
git clone <url-do-repositorio>
cd whatsappbot
```

### 2. Criar o ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Criar os diretórios locais de dados

```bash
mkdir -p rag_files vectorestore_data
```

### 5. Configurar o `.env`

Use o arquivo de exemplo como base:

```bash
cp .env.example .env
```

Depois ajuste os valores necessários no `.env`:

```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL_NAME=gpt-4o-mini
OPENAI_MODEL_TEMPERATURE=0
AI_CONTEXTUALIZE_PROMPT=Reescreva a pergunta do usuario considerando o historico da conversa.
AI_SYSTEM_PROMPT=Voce e um assistente que responde com base apenas nos documentos carregados.
VECTOR_STORE_PATH=./vectorestore_data
RAG_FILES_DIR=./rag_files
EVOLUTION_API_URL=http://localhost:8080
EVOLUTION_INSTANCE_NAME=bot
AUTHENTICATION_API_KEY=sua_chave_da_evolution
CACHE_REDIS_URI=redis://localhost:6379/0
BUFFER_KEY_SUFIX=:buffer
DEBOUNCE_SECONDS=2
BUFFER_TTL=30
CONFIG_SESSION_PHONE_VERSION=2.3000.1023204200
DATABASE_ENABLED=true
DATABASE_PROVIDER=postgresql
POSTGRES_PASSWORD=postgres_dev_123
DATABASE_CONNECTION_URI=postgresql://postgres:postgres_dev_123@postgres:5432/evolution
DATABASE_CONNECTION_CLIENT_NAME=evolution_exchange
DATABASE_SAVE_DATA_INSTANCE=true
DATABASE_SAVE_DATA_NEW_MESSAGE=true
DATABASE_SAVE_MESSAGE_UPDATE=true
DATABASE_SAVE_DATA_CONTACTS=true
DATABASE_SAVE_DATA_CHATS=true
DATABASE_SAVE_DATA_LABELS=true
DATABASE_SAVE_DATA_HISTORIC=true
CACHE_REDIS_ENABLED=true
CACHE_REDIS_PREFIX_KEY=evolution
CACHE_REDIS_SAVE_INSTANCES=false
CACHE_LOCAL_ENABLED=false
```

### 6. Subir os serviços auxiliares

Para rodar Redis e Evolution API:

```bash
docker compose up -d redis evolution-api postgres
```

Para subir toda a stack:

```bash
docker compose up --build
```

### 7. Executar a aplicação

Execução local com Python:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### 8. Carregar documentos para o RAG

1. Adicione arquivos `.pdf` ou `.txt` no diretório definido em `RAG_FILES_DIR`.
2. Inicie a aplicação.
3. Os arquivos serão processados e movidos para `rag_files/processed`.
4. Os embeddings serão persistidos no diretório configurado em `VECTOR_STORE_PATH`.

### 9. Configurar o webhook

Aponte a Evolution API para o endpoint:

```text
POST http://<host>:8000/webhook
```

## Configuração do `.env`

| Variável | Uso no projeto |
| --- | --- |
| `OPENAI_API_KEY` | Chave da API da OpenAI |
| `OPENAI_MODEL_NAME` | Modelo usado para respostas |
| `OPENAI_MODEL_TEMPERATURE` | Temperatura do modelo |
| `AI_CONTEXTUALIZE_PROMPT` | Prompt para reescrever perguntas com contexto |
| `AI_SYSTEM_PROMPT` | Prompt principal de resposta |
| `VECTOR_STORE_PATH` | Diretório de persistência do ChromaDB |
| `RAG_FILES_DIR` | Diretório de entrada dos documentos |
| `EVOLUTION_API_URL` | URL base da Evolution API |
| `EVOLUTION_INSTANCE_NAME` | Nome da instância do WhatsApp na Evolution |
| `AUTHENTICATION_API_KEY` | Chave usada nas chamadas da Evolution API |
| `CACHE_REDIS_URI` | URL de conexão com Redis |
| `BUFFER_KEY_SUFIX` | Sufixo de chave para buffer de mensagens |
| `DEBOUNCE_SECONDS` | Janela de debounce do agrupamento |
| `BUFFER_TTL` | TTL do buffer no Redis |
| `CONFIG_SESSION_PHONE_VERSION` | Configuração consumida pela Evolution API |
| `POSTGRES_PASSWORD` | Senha do container PostgreSQL usado pela Evolution API |
| `DATABASE_*` | Variáveis exigidas pela Evolution API para persistência |
| `CACHE_REDIS_*` | Configurações de cache da Evolution API |
| `CACHE_LOCAL_ENABLED` | Habilita ou desabilita cache local da Evolution API |

## Estrutura do projeto

```text
.
├── app.py
├── chains.py
├── config.py
├── evolution_api.py
├── memory.py
├── message_buffer.py
├── prompts.py
├── script.py
├── vectorstore.py
├── docker-compose.yml
├── dockerfile
├── requirements.txt
├── rag_files/
│   └── processed/
└── vectorestore_data/
```

## Melhorias futuras

- Validar o payload recebido com modelos Pydantic
- Adicionar tratamento de erros e logging estruturado
- Implementar testes automatizados para webhook, integração e ingestão
- Separar a ingestão do vector store do fluxo de inicialização da API
- Padronizar configuração com tipagem e validação de ambiente
- Adicionar observabilidade, rate limiting e autenticação do webhook

## Objetivo no portfólio

Este projeto demonstra capacidade de integrar APIs externas, mensageria, IA generativa, recuperação semântica de documentos e persistência de estado conversacional. Também evidencia familiaridade com organização modular de backend, containers, configuração por ambiente e construção de aplicações orientadas a integração.
