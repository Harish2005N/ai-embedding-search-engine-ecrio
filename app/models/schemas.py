from pydantic import BaseModel
from typing import List, Optional

class DocumentCreate(BaseModel):
    title: str
    content: str

class DocumentResponse(BaseModel):
    id: int
    message: str

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class SearchResult(BaseModel):
    id: int
    title: str
    content: str
    score: float

class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]

class DocumentInfo(BaseModel):
    id: int
    title: str
    content: str

class StatsResponse(BaseModel):
    total_documents: int
    embedding_dimension: int
    index_type: str
    vector_engine: dict
