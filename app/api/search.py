from fastapi import APIRouter, HTTPException
from app.models.schemas import SearchRequest, SearchResponse, SearchResult
from app.services.document_service import document_store
from app.services.embedding_service import generate_embedding
from app.services.faiss_service import faiss_service

router = APIRouter()

@router.post("/search", response_model=SearchResponse)
def search_documents(request: SearchRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty.")
    if request.top_k <= 0:
        raise HTTPException(status_code=400, detail="top_k must be greater than 0.")
        
    if faiss_service.get_total_vectors() == 0:
        return SearchResponse(query=request.query, results=[])
        
    # 1. Generate embedding for query
    try:
        query_embedding = generate_embedding(request.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate query embedding: {e}")
        
    # 2. Search FAISS index
    try:
        distances, indices = faiss_service.search(query_embedding, request.top_k)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {e}")
        
    # 3. Format results
    results = []
    for score, doc_id in zip(distances, indices):
        # FAISS returns -1 for empty slots if there aren't enough documents
        if doc_id == -1:
            continue
            
        doc_id = int(doc_id)
        doc = document_store.get_document(doc_id)
        
        # Skip if document was deleted
        if doc:
            results.append(SearchResult(
                id=doc.id,
                title=doc.title,
                content=doc.content,
                score=float(score)
            ))
            
    # Sort results by score descending (just to be safe, FAISS already does this)
    results.sort(key=lambda x: x.score, reverse=True)
            
    return SearchResponse(query=request.query, results=results)
