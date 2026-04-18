import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from app.config import GROQ_API_KEY, VECTORSTORE_DIR, EMBEDDING_MODEL, LLM_MODEL


def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = Chroma(
        persist_directory=VECTORSTORE_DIR,
        embedding_function=embeddings,
    )
    return vectorstore


def get_rag_chain():
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    llm = ChatGroq(api_key=GROQ_API_KEY, model_name=LLM_MODEL)

    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are a helpful assistant that answers questions based only on the provided context. "
            "If the answer is not in the context, say \"I don't have enough information to answer that\"."
        )),
        ("human", "Context:\n{context}\n\nQuestion: {question}"),
    ])

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain, retriever


def query_rag(question: str):
    chain, retriever = get_rag_chain()
    answer = chain.invoke(question)
    source_docs = retriever.invoke(question)

    sources = [
        {
            "source": os.path.basename(doc.metadata.get("source", "unknown")),
            "page_content": doc.page_content[:200],
        }
        for doc in source_docs
    ]

    return {"answer": answer, "sources": sources}
