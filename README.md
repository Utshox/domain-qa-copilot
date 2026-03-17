# Domain Q&A Copilot

A comprehensive RAG application for a portfolio.

## Tech Stack
- **API**: FastAPI
- **LLM**: OpenAI GPT-4
- **Vector DB**: Qdrant (Local)
- **Database**: Postgres
- **Orchestration**: LangChain
- **Evaluation**: Ragas
- **Observability**: Arize Phoenix / LangSmith

## Setup

1.  **Clone the repository**:
    ```bash
    git clone ...
    cd domain-qa-copilot
    ```

2.  **Environment Variables**:
    Create a `.env` file from `.env.example` and add your `OPENAI_API_KEY`.

3.  **Start Infrastructure**:
    ```bash
    docker-compose up -d
    ```

4.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the application**:
    ```bash
    uvicorn app.main:app --reload
    ```

## API Endpoints

- `POST /api/v1/auth/signup`: Create a new user (role: 'admin' or 'user').
- `POST /api/v1/auth/login`: Get access token.
- `POST /api/v1/ingest/upload`: Upload PDF/TXT (Admin only).
- `POST /api/v1/query/`: Ask a question.
- `POST /api/v1/feedback/`: Submit feedback.

## Evaluation
Run the evaluation script in `scripts/evaluate_rag.py` to get RAG metrics.

## Observability
Start Arize Phoenix for local tracing:
```bash
python -m phoenix.server.main serve
```
Then visit `http://localhost:6006`.

## Contributors
- [Utshox](https://github.com/Utshox)
