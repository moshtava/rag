from typing import Any, Dict, List
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance, PointStruct
from src.domain.interfaces import QdrantClientAdapterInterface

class QdrantClientAdapter(QdrantClientAdapterInterface):
   def __init__(self, host='localhost', port=6333, in_memory=True):
    if in_memory:
     self.client = QdrantClient(path=":memory:")  
    else:
     self.client = QdrantClient(host=host, port=port) 
   
   def collection_exists(self, collection_name: str) -> bool:
    return self.client.collection_exists(collection_name)
   
   def delete_collection(self, collection_name: str) -> bool:
    return self.client.delete_collection(collection_name)
   
   def create_collection(self, collection_name: str, vectors_config) -> bool:
    return self.client.create_collection(collection_name=collection_name, vectors_config=vectors_config, timeout = 180)
   
   def upsert(self, collection_name: str, points) -> Any:
    self.client.upsert(collection_name=collection_name, points=points)
   
   def search(self, collection_name: str, query_vector, limit: int) -> Any:
    return self.client.search(collection_name=collection_name, query_vector=query_vector, limit=limit)
   
   def retrieve(self, collection_name: str, point_ids) -> List[Any]:
    return self.client.retrieve(collection_name=collection_name, ids=point_ids)
   
   def delete(self, collection_name: str, point_ids: Any) -> Any:
    return self.client.delete(collection_name=collection_name, points_selector=point_ids)
