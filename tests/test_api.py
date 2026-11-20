import pytest
from fastapi.testclient import TestClient
from app.main import app
import numpy as np

from app.services.embedding_service import generate_embedding
from app.services.mojo_service import normalize_vector_python, compute_similarity_python
from app.services.document_service import document_store
from app.services.faiss_service import faiss_service

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_vector_normalization():
    vec = np.array([3.0, 4.0])
    norm_vec = normalize_vector_python(vec)
    assert np.allclose(norm_vec, [0.6, 0.8])
    assert np.isclose(np.linalg.norm(norm_vec), 1.0)

def test_compute_similarity():
    vec1 = np.array([1.0, 0.0])
    vec2 = np.array([1.0, 0.0])
    sim = compute_similarity_python(vec1, vec2)
    assert np.isclose(sim, 1.0)

    vec3 = np.array([0.0, 1.0])
    sim2 = compute_similarity_python(vec1, vec3)
    assert np.isclose(sim2, 0.0)

def test_embedding_generation():
    text = "Test sentence"
    emb = generate_embedding(text)
    assert isinstance(emb, np.ndarray)
    assert emb.shape[0] == 384
    # Check if normalized
    assert np.isclose(np.linalg.norm(emb), 1.0, atol=1e-5)

def test_add_and_search_document():
    # Clear existing data for test
    document_store.documents.clear()
    if faiss_service.index is not None:
        faiss_service.initialize_index()

    # 1. Add document
    doc_data = {
        "title": "Test Document",
        "content": "This is a test document for unit testing the search engine."
    }
    add_resp = client.post("/documents", json=doc_data)
    assert add_resp.status_code == 200
    assert "id" in add_resp.json()

    # 2. Search
    search_data = {
        "query": "unit testing",
        "top_k": 1
    }
    search_resp = client.post("/search", json=search_data)
    assert search_resp.status_code == 200
    
    results = search_resp.json()["results"]
    assert len(results) == 1
    assert results[0]["title"] == "Test Document"
    assert results[0]["score"] > 0.0  # Should have some similarity
