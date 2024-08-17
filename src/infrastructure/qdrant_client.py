from typing import Any, Dict, List
from src.domain.exceptions import CollectionExistsError
from src.domain.interfaces import QdrantClientAdapterInterface, QdrantVectorDBInterface
from qdrant_client.http.models import VectorParams, Distance, PointStruct

class QdrantVectorDB(QdrantVectorDBInterface):
   def __init__(self, client: QdrantClientAdapterInterface):
    self.__client = client
   
   def create_collection_if_not_exists(self, collection_name: str, vector_size: int) -> bool:
    if not self.__client.collection_exists(collection_name):
     return self.__client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.DOT)
            )
    else:
     return False
       
   def recreate_collection(self, collection_name: str, vector_size: int) -> bool:
    if self.__client.collection_exists(collection_name):
     self.__client.delete_collection(collection_name)

    return  self.__client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size,distance=Distance.DOT)
           )   
      
   def create_collection(self, collection_name: str, vector_size: int) -> bool:
    if not self.__client.collection_exists(collection_name):
     return self.__client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size,distance=Distance.COSINE)
            )
    else:
     raise CollectionExistsError(collection_name)
     
   def add_vectors(self, collection_name: str, vectors: list[list[float]], ids: list[str]) -> Any:
    points = [PointStruct(id=idx, vector=vec) for idx, vec in enumerate(vectors)] if ids is None else \
    [PointStruct(id=id, vector=vec) for id, vec in zip(ids, vectors)]
    return self.__client.upsert(collection_name=collection_name, points=points)
   
   def add_vectors_with_text(self, collection_name: str, vectors: List[list[float]], texts, ids=None) -> Any:
    points = [
    PointStruct(id=idx, vector=vec, payload={"text": text}) 
    for idx, (vec, text) in enumerate(zip(vectors, texts))
    ] if ids is None else [
    PointStruct(id=id, vector=vec, payload={"text": text}) 
    for id, vec, text in zip(ids, vectors, texts)
    ]
    return self.__client.upsert(collection_name=collection_name, points=points)
   
   def search_vectors(self, collection_name: str, query_vector: list[float], top_k=5) -> List[Any]:
    if not self.__client.collection_exists(collection_name):
     raise ValueError(f"Collection {collection_name} does not exist")
    search_result = self.__client.search(
    collection_name=collection_name,
    query_vector=query_vector,
    limit=top_k
    )
    return search_result
   
   def delete_vector(self, collection_name: str, vector_id: str) -> Any:
    if self.__client.collection_exists(collection_name):
     self.__client.delete(collection_name=collection_name, point_ids=[vector_id])
