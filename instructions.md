# realmate-challenge — INSTRUCTIONS

## Visão geral do sistema

Este projeto contém:

- **Backend (Django + DRF)**
  - Modelos principais: `Conversation` e `ChatMessage` (Message).
  - Endpoint de webhook: `POST /webhook/` — recebe eventos externos e cria conversas / mensagens / fecha conversas.
  - Endpoint público para consulta: `GET /conversations/{id}/` — retorna a conversa com o seu `state` e as `messages`.
  - Auditoria: `django-auditlog` está registrado para as models principais.

- **Frontend (Vue 3 + Vite + Tailwind)**
  - Duas telas principais:
    1. **`/` (principal)** — lista de conversas e possibilidade de clicar em uma conversa para ver detalhes.
    2. **`/chat/:id` (visualização da conversa)** — mostra as mensagens da conversa selecionada e permite enviar mensagens (via webhook POST).

- **Banco de dados**: PostgreSQL (container `db`).

- **Orquestração**: `docker-compose`.

- **Gerenciamento de dependências (backend)**: Poetry.

- **Linter**: `ruff` (Python).

---

## Requisitos (locais / antes de rodar)

- Docker e Docker Compose instalados (versão compatível com Compose v1 ou v2).
- Para desenvolvimento front: Node (opcional, já executamos o dev server dentro do container via `docker-compose`).
- (Opcional) Poetry local caso prefira rodar o backend sem Docker.

---

## Arquivos e configurações importantes

- `docker-compose.yml` — define 3 serviços:
  - `db` (postgres:15)
  - `backend` (constrói `./backend`, expõe porta `80`)
  - `frontend` (constrói `./frontend`, expõe porta `8000` do host apontando para Vite)

- `backend/Dockerfile` — imagem Python + Poetry, expõe `80` e tem `entrypoint.sh` para boot (migrations / wait-for-db etc).

- `frontend/Dockerfile` — imagem Node que inicia Vite e mapeia porta `5173` do container para `8000` no host.

- `.env` (backend): o `docker-compose` referencia `./backend/.env`. Certifique-se de ter as variáveis:
  - `SECRET_KEY`
  - `DATABASE_HOST=db`
  - `DATABASE_NAME=realmate`
  - `DATABASE_USER=postgres`
  - `DATABASE_PASSWORD=postgres`
  - `DATABASE_PORT=5432`
  - `DEBUG=True` (apenas dev)
  - `ALLOWED_HOSTS=localhost,127.0.0.1`

  **Exemplo** (`backend/.env`):
  ```env
  SECRET_KEY=uma_chave_segura_aqui
  DATABASE_HOST=db
  DATABASE_NAME=realmate
  DATABASE_USER=postgres
  DATABASE_PASSWORD=postgres
  DATABASE_PORT=5432
  DEBUG=True
  ALLOWED_HOSTS=localhost,127.0.0.1

## Subindo a aplicação (com Docker)
1.  Isso cria e sobe os containers:
  - DB em localhost:5432
  - Backend (Django) disponível em http://localhost/ (porta 80)
  - Frontend (Vite) disponível em http://localhost:8000/
2. Rodar migrations:
  - docker-compose exec backend python manage.py migrate
3. Criar superuser Django (opcional, para acessar admin):
  - docker-compose exec backend python manage.py createsuperuser

## Rodando os testes
1. Os testes Django (unit/integration) podem ser executados dentro do container do backend:
  - docker-compose exec backend python manage.py pytest -v

## Lint com ruff
1. O projeto usa ruff como linter. Para rodar o ruff dentro do container backend:
  - docker-compose exec backend ruff check .

## Auditlog
1. O projeto utiliza django-auditlog. Entradas de auditoria são registradas automaticamente para os modelos registrados (Conversation, ChatMessage). Para visualizar os registros:
  - Acesse o Django admin: http://localhost/admin/
  - Procure por seção Audit log / Log entries (dependendo da versão do pacote, o modelo pode aparecer como Log entry ou Audit log).

## Indexes importantes
  - BaseModel.created_at tem db_index=True (index para criação).
  - ChatMessage.timestamp tem db_index=True (index para queries por horário).
Esses índices melhoram performance em consultas de listagem/ordenamento por tempo.

## API — endpoints e uso
1. Webhook — receber eventos
POST http://localhost/webhook/
O backend aceita os seguintes eventos (formato exato abaixo):
  - NEW_CONVERSATION
  ```json
  {
      "type": "NEW_CONVERSATION",
      "timestamp": "2025-02-21T10:20:41.349308",
      "data": {
          "id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a"
      }
  }
  ```
  Resposta esperada: 201 Created com JSON contendo status e id.
  - NEW_MESSAGE(Received)
  ```json
  {
      "type": "NEW_MESSAGE",
      "timestamp": "2025-02-21T10:20:42.349308",
      "data": {
          "id": "49108c71-4dca-4af3-9f32-61bc745926e2",
          "direction": "RECEIVED",
          "content": "Olá, tudo bem?",
          "conversation_id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a"
      }
  }
  ```
  - NEW_MESSAGE(Received)
  ```json
  {
      "type": "NEW_MESSAGE",
      "timestamp": "2025-02-21T10:20:44.349308",
      "data": {
          "id": "16b63b04-60de-4257-b1a1-20a5154abc6d",
          "direction": "SENT",
          "content": "Tudo ótimo e você?",
          "conversation_id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a"
      }
  }
  ```
  Resposta esperada: 201 Created com status: "message_created".
  - CLOSE_CONVERSATION
  ```json
  {
      "type": "CLOSE_CONVERSATION",
      "timestamp": "2025-02-21T10:20:45.349308",
      "data": {
          "id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a"
      }
  }
  ```
  Resposta esperada: 200 OK com status: "conversation_closed".
2. Conversation retrieval (API)
  - GET http://localhost/conversations/{conversation_id}/
  - Retorna JSON com:
  ```json
  {
    "id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a",
    "state": "OPEN",
    "messages": [
      {
        "id": "49108c71-4dca-4af3-9f32-61bc745926e2",
        "direction": "RECEIVED",
        "content": "Olá, tudo bem?",
        "timestamp": "2025-02-21T10:20:42.349308"
      },
    ]
  }
  ```
3. Você também tem os endpoints do ViewSet:
  - GET /conversations/ (lista)
  - GET /conversations/{id}/ (detalhe)
  - GET /messages/ (lista)
  - GET /messages/{id}/ (detalhe)

## Frontend (telas e comportamento)
  - Tela principal (/)
    - Lista todas as conversas (consuma GET /conversations/).
    - Clique em uma conversa para navegar para /chat/:id.
    - Visualiza estado (OPEN / CLOSED) no resumo.

  - Tela da conversa (/chat/:id)
    - Carrega GET /conversations/:id/ — preenche mensagens e estado.
    - Faz polling (ex.: a cada 1–2s) para buscar novas mensagens na conversa.
    - Permite enviar mensagem (POST para /webhook/ usando evento NEW_MESSAGE com direction: "SENT").
    - Se a conversa estiver CLOSED, o input para enviar mensagens fica desabilitado e o frontend deve mostrar aviso.

## Como o backend aplica as regras de negócio
- Toda Conversation é criada com state = OPEN (default).
- Caso CLOSE_CONVERSATION seja recebido, o serviço ConversationService.close_conversation seta state = CLOSED.
- ConversationService.new_message valida se a conversation_id existe e se ela está OPEN (se estiver CLOSED, retorna erro/validation).
- ChatMessage.direction é limitado a SENT ou RECEIVED.
- IDs de Conversation e ChatMessage são UUIDs e únicos (campo id em BaseModel com UUIDField).
