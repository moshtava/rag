import os
from fastapi import FastAPI
from src.infrastructure.qdrant_client import QdrantVectorDB
from src.application.endpoint_handle import EndpointHandle
from src.infrastructure.qdrant_client_adapter import QdrantClientAdapter
from src.infrastructure.mistral_client_adapter import MistralClientAdapter, MistralClientWrapp
from src.domain.models import Document, Question

app = FastAPI()

client_adapter = QdrantClientAdapter()
qvd = QdrantVectorDB(client_adapter)
mistral_client_adapter = MistralClientAdapter(api_key=str(os.environ.get("API_KEY")))
mistral_client_wrapp = MistralClientWrapp(mistral_client_adapter)
 
@app.post("/insert", summary="Insert Document", description="Insert a document into the vector database. This document would be used as knowledge base")
def insert_document(document: Document):
 EndpointHandle(qvd=qvd, mcw=mistral_client_wrapp).insert_document(document)
 return {"status": "Document inserted successfully"}

@app.post("/ask", summary="Ask Question", description="Ask a question and get an answer based on the inserted documents.")
def ask_question(question: Question):
 answer = EndpointHandle(qvd=qvd, mcw=mistral_client_wrapp).ask_question(question)
 return {"answer": answer}
