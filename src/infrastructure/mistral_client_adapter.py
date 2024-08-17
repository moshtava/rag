from typing import Any, List
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from src.domain.interfaces import MistralClientWrappInterface
from src.domain.interfaces import MistralClientInterface

class MistralClientAdapter(MistralClientInterface):
   def __init__(self, api_key: str):
    self.client = MistralClient(api_key=api_key)
   
   def chat(self, messages: List[Any], model: str | None = None) -> Any:
    return self.client.chat(messages=messages, model=model)
   
   def embeddings(self, model: str, input: str | List[str]) -> Any:
    return self.client.embeddings(model=model, input=input)
   
class MistralClientWrapp(MistralClientWrappInterface):
   def __init__(self, mistral_client: MistralClientInterface, llm_model: str = "mistral-medium-latest", embedding_model: str = "mistral-embed") -> None:
    self.mistral_client = mistral_client
    self.llm_model = llm_model
    self.embedding_model = embedding_model

   def run_mistral(self, user_message: str):
    messages = [ChatMessage(role="user", content=user_message)]
    chat_response = self.mistral_client.chat(messages=messages, model=self.llm_model)
    return chat_response.choices[0].message.content
   
   def get_text_embedding(self, input: str):
    my_list: List[str] = [input]  
    embeddings_batch_response = self.mistral_client.embeddings(model=self.embedding_model, input=my_list)
    return embeddings_batch_response.data[0].embedding

