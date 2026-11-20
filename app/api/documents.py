from fastapi import APIRouter, HTTPException
from typing import List
from app.models.schemas import DocumentCreate, DocumentResponse, DocumentInfo
from app.services.document_service import document_store
from app.services.embedding_service import generate_embedding
from app.services.faiss_service import faiss_service

router = APIRouter()

@router.post("/documents", response_model=DocumentResponse)
def add_document(doc: DocumentCreate):
    if not doc.title.strip() or not doc.content.strip():
        raise HTTPException(status_code=400, detail="Title and content cannot be empty.")
    
    # 1. Generate normalized embedding by combining Title and Content
    try:
        combined_text = f"{doc.title}. {doc.content}"
        embedding = generate_embedding(combined_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate embedding: {e}")
        
    # 2. Store document metadata
    new_doc = document_store.add_document(doc.title, doc.content)
    
    # 3. Store embedding in FAISS
    try:
        faiss_service.add_embedding(new_doc.id, embedding)
    except Exception as e:
        # Rollback document if FAISS fails
        document_store.delete_document(new_doc.id)
        raise HTTPException(status_code=500, detail=f"Failed to store embedding in FAISS: {e}")
        
    return DocumentResponse(id=new_doc.id, message="Document added successfully")

@router.get("/documents", response_model=List[DocumentInfo])
def get_documents():
    return document_store.get_all_documents()

@router.get("/documents/{document_id}", response_model=DocumentInfo)
def get_document(document_id: int):
    doc = document_store.get_document(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")
    return doc

@router.delete("/documents/{document_id}")
def delete_document(document_id: int):
    # Note: Removing from FAISS is complex without rebuilding the index.
    # For this mini-project, we will just remove the metadata.
    # The search results will filter out deleted documents.
    if document_store.delete_document(document_id):
        return {"message": "Document deleted successfully"}
    raise HTTPException(status_code=404, detail="Document not found.")
