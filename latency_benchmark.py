import time
import numpy as np
import httpx
from app.services.embedding_service import generate_embedding
from app.services.faiss_service import faiss_service
from app.services.mojo_service import normalize_vector_python
from app.services.document_service import document_store

def run_benchmarks():
    query = "machine learning algorithms and neural network architectures"
    
    # Warmup
    emb = generate_embedding(query)

    # 1. Embedding Model
    emb_times = []
    for _ in range(30):
        t0 = time.perf_counter()
        _ = generate_embedding(query)
        emb_times.append((time.perf_counter() - t0) * 1000)

    # 2. Vector Normalization
    vec = np.random.rand(384).astype(np.float32)
    norm_times = []
    for _ in range(10000):
        t0 = time.perf_counter()
        _ = normalize_vector_python(vec)
        norm_times.append((time.perf_counter() - t0) * 1e6)

    # 3. FAISS Search
    faiss_times = []
    for _ in range(200):
        t0 = time.perf_counter()
        distances, indices = faiss_service.search(emb, top_k=5)
        faiss_times.append((time.perf_counter() - t0) * 1000)

    # 4. Doc Store Hydration
    doc_ids = [int(idx) for idx in indices if int(idx) != -1]
    hydro_times = []
    for _ in range(200):
        t0 = time.perf_counter()
        _ = [document_store.get_document(did) for did in doc_ids]
        hydro_times.append((time.perf_counter() - t0) * 1000)

    # 5. End-to-End Search API
    api_times = []
    with httpx.Client() as client:
        # warm up API
        client.post("http://127.0.0.1:8000/search", json={"query": query, "top_k": 5})
        for _ in range(30):
            t0 = time.perf_counter()
            r = client.post("http://127.0.0.1:8000/search", json={"query": query, "top_k": 5})
            api_times.append((time.perf_counter() - t0) * 1000)

    print("=== DETAILED LATENCY BENCHMARK RESULTS ===")
    print(f"1. Embedding Model (all-MiniLM-L6-v2): Avg={np.mean(emb_times):.2f} ms | Min={np.min(emb_times):.2f} ms | P95={np.percentile(emb_times, 95):.2f} ms")
    print(f"2. Vector Normalization (L2 Norm):         Avg={np.mean(norm_times):.2f} us | Min={np.min(norm_times):.2f} us | P95={np.percentile(norm_times, 95):.2f} us")
    print(f"3. FAISS Vector Search (IndexFlatIP):       Avg={np.mean(faiss_times):.3f} ms | Min={np.min(faiss_times):.3f} ms | P95={np.percentile(faiss_times, 95):.3f} ms")
    print(f"4. Document Metadata Hydration (JSON):     Avg={np.mean(hydro_times):.3f} ms | Min={np.min(hydro_times):.3f} ms | P95={np.percentile(hydro_times, 95):.3f} ms")
    print(f"5. Full End-to-End API Search (HTTP):       Avg={np.mean(api_times):.2f} ms | Min={np.min(api_times):.2f} ms | P95={np.percentile(api_times, 95):.2f} ms")

if __name__ == "__main__":
    run_benchmarks()
