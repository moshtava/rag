### Prerequisites


•  Python 3.8+

•  FastAPI

•  Qdrant (or another vector database)

## Installation not using and using docker


## Installation not using docker

1. Clone the repository:

`git clone https://github.com/moshtava/rag.git`

`cd rag`

2. Create a virtual environment:

`python -m venv venv`

`source venv/bin/activate`  # On Windows use `venv\Scripts\activate`

3. Install the dependencies:

`pip install -r requirements.txt`

## Running the API
1. Start the FastAPI server:

`uvicorn main:app --reload`

2. Access the API documentation:

Open your browser and go to http://127.0.0.1:8000/docs to see the Swagger documentation.

## Using Docker Compose
1. make sure docker-compose.yml file is set up like the following:

```
version: '3.8'

services:
app:
build:
context: .
dockerfile: Dockerfile
container_name: rag_app
ports:
•  "8000:8000"

environment:
•  API_KEY=${API_KEY}

•  HF_TOKEN=${HF_TOKEN}

depends_on:
•  qdrant


qdrant:
image: qdrant/qdrant:v1.10.0
container_name: qdrant_db
ports:
•  "6333:6333"

volumes:
•  qdrant_data:/qdrant/storage


volumes:
qdrant_data:
```

*note* 

use .env file to store values of api_key environment variable. value for hf_token is setby me and it's correct. so, don't need to change it:

`API_KEY=your_api_key_value`

`HF_TOKEN=your_hf_token_value`

1. Run Docker Compose:

`docker-compose up`


### Usage


•  Submit a question:

Use the /ask endpoint to submit a question and receive an answer based on the embedded data.

•  Insert some knowledge into the database:

Use the /insert endpoint to insert knowledge into the database.