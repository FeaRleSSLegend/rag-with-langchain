import os
from pathlib import Path
from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from app.config import DOCS_DIR, VECTORSTORE_DIR, EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP


def load_documents():
    documents = []
    docs_path = Path(DOCS_DIR)

    for file in docs_path.iterdir():
        if file.suffix == ".docx":
            loader = Docx2txtLoader(str(file))
            documents.extend(loader.load())
        elif file.suffix == ".pdf":
            loader = PyPDFLoader(str(file))
            documents.extend(loader.load())

    print(f"Loaded {len(documents)} documents/pages")
    return documents


def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks")
    return chunks


def embed_and_store(chunks):
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTORSTORE_DIR,
    )
    vectorstore.persist()
    print("Vectorstore saved successfully")


def run_ingest():
    documents = load_documents()
    chunks = chunk_documents(documents)
    embed_and_store(chunks)
    return {
        "status": "success",
        "documents_loaded": len(documents),
        "chunks_created": len(chunks),
    }
