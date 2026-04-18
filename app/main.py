import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.ingest import run_ingest
from app.retriever import query_rag
from app.config import VECTORSTORE_DIR

app = FastAPI(title="Document RAG API", version="1.0.0")


class QueryRequest(BaseModel):
    question: str


@app.post("/ingest")
async def ingest():
    try:
        result = run_ingest()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query")
async def query(request: QueryRequest):
    vs_path = Path(VECTORSTORE_DIR)
    if not vs_path.exists() or not any(vs_path.iterdir()):
        raise HTTPException(
            status_code=400,
            detail="Vectorstore not found. Please run /ingest first.",
        )
    try:
        result = query_rag(request.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
