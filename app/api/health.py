from fastapi import APIRouter
from app.models.schemas import StatsResponse
from app.services.document_service import document_store
from app.services.faiss_service import faiss_service
from app.services.embedding_service import EMBEDDING_DIMENSION
from app.services.mojo_service import get_vector_engine_status

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "healthy"}

@router.get("/stats", response_model=StatsResponse)
def get_stats():
    engine_status = get_vector_engine_status()
    return StatsResponse(
        total_documents=len(document_store.documents),
        embedding_dimension=EMBEDDING_DIMENSION,
        index_type="FAISS IndexFlatIP",
        vector_engine=engine_status,
    )