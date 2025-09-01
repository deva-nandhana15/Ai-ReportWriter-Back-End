from pydantic import BaseModel
from typing import List

# User Schemas
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    class Config:
        orm_mode = True

# Paper Schemas
class PaperRequest(BaseModel):
    title: str
    abstract: str

class PlagiarismRequest(BaseModel):
    source_text: str
    corpus_texts: List[str]
