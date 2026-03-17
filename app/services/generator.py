from typing import List, Dict, Any
from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from app.core.config import settings
from app.db.vector import vector_db

class GeneratorService:
    def __init__(self):
        self.llm = ChatVertexAI(
            model_name="gemini-1.5-flash",
            temperature=0,
            project=settings.GOOGLE_CLOUD_PROJECT
        )
        self.prompt = ChatPromptTemplate.from_template(
            """You are a helpful assistant for domain-specific Q&A. Use the following context to answer the user's question.
            If you don't know the answer, just say you don't know. Don't make up an answer.
            Provide citations for your answers by referencing the source documents.

            Context:
            {context}

            Question:
            {question}

            Answer with citations:"""
        )

    def _format_docs(self, docs: List[Document]) -> str:
        return "\n\n".join(f"Source: {doc.metadata.get('source', 'unknown')}\nContent: {doc.page_content}" for doc in docs)

    async def generate_answer(self, question: str) -> Dict[str, Any]:
        retriever = vector_db.get_retriever()
        
        # Define the chain
        rag_chain = (
            {"context": retriever | self._format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
        
        # Execute chain and get retrieved docs for citations
        docs = await retriever.ainvoke(question)
        answer = await rag_chain.ainvoke(question)
        
        return {
            "answer": answer,
            "sources": [doc.metadata for doc in docs]
        }

generator = GeneratorService()
