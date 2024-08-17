from abc import ABC, abstractmethod
from qdrant_client.models import PointStruct, VectorParams, Distance
import numpy as np
from qdrant_client import QdrantClient
from src.domain.models import Document, Question
from src.domain.interfaces import QdrantVectorDBInterface, MistralClientWrappInterface

class EndpointHandleInterface(ABC):
   @abstractmethod
   def insert_document(self, document: Document):
    pass   
   
   @abstractmethod
   def ask_question(self, question: Question):
    pass

class EndpointHandle(EndpointHandleInterface):
   def __init__(self, qvd: QdrantVectorDBInterface, mcw: MistralClientWrappInterface, chunk_size: int = 2048, vector_size: int = 1024) -> None:
    self.qvd = qvd
    self.mcw = mcw
    self.chunk_size = chunk_size
    self.vector_size = vector_size
   
   def insert_document(self, document: Document):
    chunks = [document.text[i:i + self.chunk_size] for i in range(0, len(document.text), self.chunk_size)]
    text_embeddings = np.array([self.mcw.get_text_embedding(input=chunk) for chunk in chunks])
    
    cine = self.qvd.create_collection_if_not_exists("knowledge_base", self.vector_size)
    avwt = self.qvd.add_vectors_with_text("knowledge_base", text_embeddings, chunks)
    
    return {"status": "Document inserted successfully"}
   
   def ask_question(self, question: Question):
    question_embeddings = np.array([self.mcw.get_text_embedding(question.question)])
    retrieved_chunk = self.qvd.search_vectors("knowledge_base", question_embeddings[0])
    print(retrieved_chunk)
    prompt = f"""
    Context information is below.
    ---------------------
    {retrieved_chunk}
    ---------------------
    Given the context information and not prior knowledge, answer the query.
    Query: {question.question}
    Answer:
    """
    
    answer = self.mcw.run_mistral(prompt) 
    return {"answer": answer}
 