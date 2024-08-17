from unittest.mock import MagicMock
import pytest
from mistralai.models.chat_completion import ChatMessage, ChatCompletionResponse, ChatCompletionResponseChoice
from mistralai.models.embeddings import EmbeddingResponse, EmbeddingObject
from infrastructure.mistral_client_adapter import MistralClientAdapter, MistralClientWrapp

@pytest.fixture
def mock_mistral_client():
 mock_client = MagicMock()
 return mock_client

def test_mistral_client_adapter_chat(mock_mistral_client):
 adapter = MistralClientAdapter(api_key="test_api_key")
 adapter.client = mock_mistral_client
 
 messages = [ChatMessage(role="user", content="Hello")]
 mock_response = ChatCompletionResponse(choices=[ChatCompletionResponseChoice(message=ChatMessage(role="assistant", content="Hi there!"))])
 mock_mistral_client.chat.return_value = mock_response
 
 response = adapter.chat(messages=messages)
 assert response.choices[0].message.content == "Hi there!"

def test_mistral_client_adapter_embeddings(mock_mistral_client):
 adapter = MistralClientAdapter(api_key="test_api_key")
 adapter.client = mock_mistral_client
 
 input_text = "Test input"
 mock_response = EmbeddingResponse(data=[EmbeddingObject(embedding=[0.1, 0.2, 0.3])])
 mock_mistral_client.embeddings.return_value = mock_response
 
 response = adapter.embeddings(model="test_model", input=input_text)
 assert response.data[0].embedding == [0.1, 0.2, 0.3]

def test_mistral_client_wrapp_run_mistral(mock_mistral_client):
 wrapper = MistralClientWrapp(mistral_client=mock_mistral_client)
 user_message = "Hello"
 mock_response = ChatCompletionResponse(choices=[ChatCompletionResponseChoice(message=ChatMessage(role="assistant", content="Hi there!"))])
 mock_mistral_client.chat.return_value = mock_response
 
 response = wrapper.run_mistral(user_message=user_message)
 assert response == "Hi there!"

def test_mistral_client_wrapp_get_text_embedding(mock_mistral_client):
 wrapper = MistralClientWrapp(mistral_client=mock_mistral_client)
 input_text = "Test input"
 mock_response = EmbeddingResponse(data=[EmbeddingObject(embedding=[0.1, 0.2, 0.3])])
 mock_mistral_client.embeddings.return_value = mock_response

 response = wrapper.get_text_embedding(input=input_text)
 assert response == [0.1, 0.2, 0.3]
