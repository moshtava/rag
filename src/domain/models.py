from pydantic import BaseModel

class Document(BaseModel):
 text: str

class Question(BaseModel):
 question: str
