from typing import List
from qdrant_client import QdrantClient
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_qdrant import Qdrant
from langchain_core.documents import Document
from app.core.config import settings

class VectorDBService:
    def __init__(self):
        try:
            self.client = QdrantClient(
                host=settings.QDRANT_HOST,
                port=settings.QDRANT_PORT,
                timeout=5
            )
            # Check if it's reachable
            self.client.get_collections()
            print("Connected to Qdrant at localhost:6333")
        except Exception as e:
            print(f"Warning: Could not connect to Qdrant at {settings.QDRANT_HOST}. Using in-memory Qdrant: {e}")
            self.client = QdrantClient(":memory:")
        
        self.embeddings = VertexAIEmbeddings(
            model_name="text-multilingual-embedding-002",
            project=settings.GOOGLE_CLOUD_PROJECT
        )
        self.collection_name = settings.QDRANT_COLLECTION

    def _ensure_collection_exists(self):
        collections = self.client.get_collections().collections
        exists = any(c.name == self.collection_name for c in collections)
        if not exists:
            # Vertex text-multilingual-embedding-002 is 768
            from qdrant_client.http import models
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
            )

    def add_documents(self, documents: List[Document]):
        self._ensure_collection_exists()
        Qdrant.from_documents(
            documents,
            self.embeddings,
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
            collection_name=self.collection_name,
        )

    def get_retriever(self, search_kwargs: dict = {"k": 4}):
        vector_store = Qdrant(
            client=self.client,
            collection_name=self.collection_name,
            embeddings=self.embeddings,
        )
        return vector_store.as_retriever(search_kwargs=search_kwargs)

vector_db = VectorDBService()
