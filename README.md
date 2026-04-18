# Tayo RAG

A document-based Retrieval-Augmented Generation (RAG) system built with LangChain, FastAPI, ChromaDB, and Groq. Upload your `.docx` and `.pdf` files, embed them once, and query them in natural language.

## Stack

- **FastAPI** — REST API
- **LangChain** — document loading, chunking, RAG chain
- **ChromaDB** — local vector store (persisted to disk)
- **HuggingFace Embeddings** — `all-MiniLM-L6-v2` (runs locally, no API key needed)
- **Groq (LLaMA 3)** — LLM for generating answers

## Project Structure
tayo_rag/
├── app/
│   ├── main.py        — FastAPI app and endpoints
│   ├── ingest.py      — Document loading, chunking, embedding
│   ├── retriever.py   — Vectorstore loading and RAG query chain
│   └── config.py      — Settings and environment variables
├── docs/              — Add your .docx and .pdf files here
├── vectorstore/       — Auto-populated when you run /ingest
├── .env.example       — Copy to .env and fill in your key
└── requirements.txt

## Setup

### 1. Clone the repo

```bash
git clone <repo-url>
cd tayo_rag
```

### 2. Install dependencies

With `uv` (recommended):
```bash
uv venv
uv pip install -r requirements.txt
```

Or with pip:
```bash
pip install -r requirements.txt
```

### 3. Set up your environment

```bash
cp .env.example .env
```

Open `.env` and add your Groq API key:
GROQ_API_KEY=your_groq_api_key_here

Get a free Groq API key at https://console.groq.com

### 4. Add your documents

Place all your `.docx` and `.pdf` files inside the `docs/` folder. These are gitignored and will not be uploaded to GitHub.

### 5. Run the server

```bash
uv run uvicorn app.main:app --port 8080 --reload
```

## Usage

Once the server is running, open your browser at:
http://127.0.0.1:8080/docs

This opens the interactive Swagger UI where you can use all endpoints.

### Endpoints

#### `POST /ingest`
Loads all documents from `docs/`, chunks them, embeds them, and saves the vectorstore to disk. Run this once after adding your documents. You only need to re-run it if you add new documents.

#### `POST /query`
Query the documents in natural language.

Request body:
```json
{
  "question": "What was the main theme of the 2025 keynote address?"
}
```

Response:
```json
{
  "answer": "The main theme was...",
  "sources": [
    {
      "source": "2025 KEYNOTE ADDRESS BY THE ARCHBISHOP.docx",
      "page_content": "..."
    }
  ]
}
```

#### `GET /health`
Returns `{"status": "ok"}` to confirm the server is running.

## Deployment

This project is ready to deploy on Railway or Render. Make sure to:
1. Set `GROQ_API_KEY` as an environment variable on the platform
2. Re-run `/ingest` after deployment to rebuild the vectorstore on the server

## Notes

- The `vectorstore/` folder is gitignored. Each deployment needs its own ingest run.
- The `docs/` folder is gitignored. Never commit sensitive documents to the repo.
- The HuggingFace embedding model downloads automatically on first run.
