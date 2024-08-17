# test_api.py
import os
from fastapi.testclient import TestClient
from src.presentation.api import app

os.environ["API_KEY"] = "test_api_key"
client = TestClient(app)
def test_insert_document():
 response = client.post("/insert", json={"text": "This is a test document."})
 assert response.status_code == 200
 assert response.json() == {"status": "Document inserted successfully"}

def test_ask_question():
 # First, insert a document to ensure there is data to query
 client.post("/insert", json={"text": "This is a test document."})
 
 response = client.post("/ask", json={"question": "What is this document about?"})
 assert response.status_code == 200
 assert "answer" in response.json()
