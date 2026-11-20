# pyrefly: ignore [missing-import]
from sentence_transformers import SentenceTransformer
import numpy as np
import logging

from app.services.mojo_service import normalize_vector_python

# Load the lightweight model once at module initialization
MODEL_NAME = "all-MiniLM-L6-v2"
logger = logging.getLogger(__name__)

try:
    logger.info(f"Loading embedding model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)
    # The dimension for all-MiniLM-L6-v2 is 384
    EMBEDDING_DIMENSION = 384
except Exception as e:
    logger.error(f"Failed to load model {MODEL_NAME}: {e}")
    model = None
    EMBEDDING_DIMENSION = 384

def generate_embedding(text: str) -> np.ndarray:
    """
    Generates a normalized embedding for a given text.
    Uses Mojo vector kernel for normalization (MAX Engine).
    """
    if not model:
        raise RuntimeError("Embedding model is not loaded.")
    
    # Generate the raw embedding
    raw_embedding = model.encode(text)
    
    # Normalize using Mojo vector kernel (MAX Engine on Ubuntu)
    normalized_embedding = normalize_vector_python(raw_embedding)
    
    return np.array(normalized_embedding, dtype=np.float32)

def generate_embeddings(texts: list[str]) -> np.ndarray:
    """
    Generates normalized embeddings for a batch of texts.
    """
    if not model:
        raise RuntimeError("Embedding model is not loaded.")
        
    raw_embeddings = model.encode(texts)
    
    # Normalize each vector using Mojo vector kernel (MAX Engine)
    normalized_embeddings = np.array([normalize_vector_python(vec) for vec in raw_embeddings], dtype=np.float32)
    return normalized_embeddings
