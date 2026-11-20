# pyrefly: ignore [missing-import]
from sentence_transformers import SentenceTransformer
import numpy as np
import logging
import os

from app.services.mojo_service import normalize_vector_python

# Use smaller model for memory-constrained environments
MODEL_NAME = os.getenv("EMBEDDING_MODEL", "paraphrase-MiniLM-L3-v2")
logger = logging.getLogger(__name__)

_model = None
EMBEDDING_DIMENSION = 384

def _get_model():
    global _model
    if _model is None:
        logger.info(f"Loading embedding model: {MODEL_NAME}")
        # Use low memory settings
        _model = SentenceTransformer(MODEL_NAME, device='cpu')
    return _model

def generate_embedding(text: str) -> np.ndarray:
    """
    Generates a normalized embedding for a given text.
    Uses Mojo vector kernel for normalization (MAX Engine).
    """
    model = _get_model()
    
    # Generate the raw embedding
    raw_embedding = model.encode(text)
    
    # Normalize using Mojo vector kernel (MAX Engine on Ubuntu)
    normalized_embedding = normalize_vector_python(raw_embedding)
    
    return np.array(normalized_embedding, dtype=np.float32)

def generate_embeddings(texts: list[str]) -> np.ndarray:
    """
    Generates normalized embeddings for a batch of texts.
    """
    model = _get_model()
        
    raw_embeddings = model.encode(texts)
    
    # Normalize each vector using Mojo vector kernel (MAX Engine)
    normalized_embeddings = np.array([normalize_vector_python(vec) for vec in raw_embeddings], dtype=np.float32)
    return normalized_embeddings
