import faiss
import numpy as np
import os
import logging
from app.services.embedding_service import EMBEDDING_DIMENSION

logger = logging.getLogger(__name__)

DATA_DIR = "data"
INDEX_FILE = os.path.join(DATA_DIR, "faiss.index")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

class FaissService:
    def __init__(self):
        self.dimension = EMBEDDING_DIMENSION
        self.index = None
        self.doc_ids = []  # Map FAISS internal IDs to Document Store IDs
        # Don't load at init - lazy load on first use

    def _ensure_loaded(self):
        """Lazy load the FAISS index on first access."""
        if self.index is None:
            self.load_index()

    def initialize_index(self):
        # We use IndexFlatIP for Cosine Similarity (assuming normalized vectors)
        logger.info(f"Initializing new FAISS IndexFlatIP with dimension {self.dimension}")
        self.index = faiss.IndexFlatIP(self.dimension)
        # Wrap in an IDMap to maintain our custom document IDs
        self.index = faiss.IndexIDMap(self.index)
        self.doc_ids = []

    def load_index(self):
        if os.path.exists(INDEX_FILE):
            try:
                logger.info(f"Loading FAISS index from {INDEX_FILE}")
                self.index = faiss.read_index(INDEX_FILE)
                
                # To sync doc_ids, we could store them separately or rely on document_store
                # Actually, IndexIDMap stores IDs internally, we can fetch them if needed
                # However, for simplicity, we will just rely on the document store for metadata
            except Exception as e:
                logger.error(f"Error loading FAISS index: {e}")
                self.initialize_index()
        else:
            self.initialize_index()

    def save_index(self):
        if self.index is not None:
            try:
                faiss.write_index(self.index, INDEX_FILE)
                logger.info("FAISS index saved successfully.")
            except Exception as e:
                logger.error(f"Error saving FAISS index: {e}")

    def add_embedding(self, doc_id: int, embedding: np.ndarray):
        """
        Adds a single embedding to the FAISS index.
        """
        self._ensure_loaded()
        
        # Ensure it's a 2D array for FAISS
        emb_2d = embedding.reshape(1, -1)
        ids_array = np.array([doc_id], dtype=np.int64)
        
        self.index.add_with_ids(emb_2d, ids_array)
        self.save_index()

    def add_embeddings(self, doc_ids: list[int], embeddings: np.ndarray):
        """
        Adds multiple embeddings.
        """
        self._ensure_loaded()
        
        ids_array = np.array(doc_ids, dtype=np.int64)
        self.index.add_with_ids(embeddings, ids_array)
        self.save_index()

    def search(self, query_embedding: np.ndarray, top_k: int = 5):
        """
        Searches the index for the top_k most similar vectors.
        """
        self._ensure_loaded()
        
        if self.index is None or self.index.ntotal == 0:
            return [], []
            
        # Ensure 2D
        q_emb_2d = query_embedding.reshape(1, -1)
        
        # Search FAISS
        distances, indices = self.index.search(q_emb_2d, top_k)
        
        return distances[0], indices[0]

    def get_total_vectors(self) -> int:
        self._ensure_loaded()
        if self.index:
            return self.index.ntotal
        return 0

# Global instance
faiss_service = FaissService()
