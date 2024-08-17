from abc import ABC, abstractmethod
from typing import Any, Dict, List, Mapping
from qdrant_client.http.models import VectorParams, Distance, PointStruct
import numpy as np

class QdrantVectorDBInterface(ABC):
   @abstractmethod
   def create_collection_if_not_exists(self, collection_name: str, vector_size: int) -> bool:
    pass
   
   @abstractmethod
   def recreate_collection(self, collection_name: str, vector_size: int) -> bool:
    pass
   
   @abstractmethod
   def create_collection(self, collection_name: str, vector_size: int) -> bool:
    pass
   
   @abstractmethod
   def add_vectors(self, collection_name: str, vectors: np.ndarray, ids: list[str]) -> Any:
    pass
   
   @abstractmethod
   def add_vectors_with_text(self, collection_name: str, vectors: np.ndarray, texts: list, ids: list[str]) -> Any:
    pass
   
   @abstractmethod
   def search_vectors(self, collection_name: str, query_vector: np.ndarray, top_k: int = 5) -> List[Any]:
    pass
   
   @abstractmethod
   def delete_vector(self, collection_name: str, vector_id: int) -> Any:
    pass
   

class QdrantClientAdapterInterface(ABC):
   @abstractmethod
   def collection_exists(self, collection_name: str) -> bool:
    pass
   
   @abstractmethod
   def delete_collection(self, collection_name: str) -> bool:
    pass
   
   @abstractmethod
   def create_collection(self, collection_name: str, vectors_config: VectorParams) -> bool:
    pass
   
   @abstractmethod
   def upsert(self, collection_name: str, points: Any) -> Any:
    pass
   
   @abstractmethod
   def search(self, collection_name: str, query_vector: List[float], limit: int = 5) -> Any:
    pass
   
   @abstractmethod
   def retrieve(self, collection_name: str, point_ids: List[str]) -> List[Any]:
    pass
   
   @abstractmethod
   def delete(self, collection_name: str, point_ids: Any) -> Any:
    pass

class MistralClientInterface(ABC):
   @abstractmethod
   def chat(self, messages: List[Any], model: str) -> Any:
    pass
   
   @abstractmethod
   def embeddings(self, model: str, input: List[str]) -> Any:
    pass

class MistralClientWrappInterface(ABC):
    @abstractmethod
    def run_mistral(self, user_message: str) -> Any:
     pass
    
    @abstractmethod
    def get_text_embedding(self, input: str) -> Any:
     pass
