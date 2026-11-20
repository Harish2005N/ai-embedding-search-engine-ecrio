import time
import numpy as np
import httpx
import asyncio
from app.services.embedding_service import generate_embedding
from app.services.faiss_service import faiss_service
from app.services.mojo_service import normalize_vector_python, compute_similarity_python, get_vector_engine_status

API_URL = "http://127.0.0.1:8000"

def run_local_benchmark():
    print("=" * 50)
    print("LOCAL COMPONENT BENCHMARK")
    print("=" * 50)

    engine_status = get_vector_engine_status()
    print(f"Vector Engine: {engine_status['engine']}")
    print(f"Mojo Available: {engine_status['mojo_cli_available']}")
    print(f"Mojo Active: {engine_status['native_mojo_active']}")
    print()

    # 1. Embedding Generation
    text = "This is a test sentence to measure embedding generation performance."
    print("Measuring Embedding Generation Time...")
    start = time.time()
    for _ in range(10):
        emb = generate_embedding(text)
    end = time.time()
    avg_gen_time = (end - start) / 10
    print(f"Average generation time: {avg_gen_time:.4f} seconds\n")

    # 2. Vector operations (Mojo vs NumPy)
    vec1 = np.random.rand(384).astype(np.float32)
    vec2 = np.random.rand(384).astype(np.float32)

    print("Measuring Vector Operations (Mojo MAX Engine)...")
    start = time.time()
    for _ in range(10000):
        norm_v = normalize_vector_python(vec1)
        sim = compute_similarity_python(norm_v, vec2)
    end = time.time()
    avg_op_time = (end - start) / 10000
    print(f"10,000 operations took: {end - start:.4f} seconds")
    print(f"Average per-operation time: {avg_op_time:.6f} seconds")

    if engine_status['native_mojo_active']:
        print("Running with Mojo MAX Engine - hardware accelerated!")
    else:
        print("Running with NumPy fallback - install Mojo for better performance.\n")

async def run_api_benchmark():
    print("=" * 50)
    print("API SEARCH LATENCY BENCHMARK")
    print("=" * 50)

    query = {"query": "What is machine learning?", "top_k": 3}

    async with httpx.AsyncClient() as client:
        try:
            await client.post(f"{API_URL}/search", json=query)

            latencies = []
            for i in range(5):
                start = time.time()
                response = await client.post(f"{API_URL}/search", json=query)
                end = time.time()

                if response.status_code == 200:
                    latencies.append(end - start)
                else:
                    print(f"Request {i+1} failed: {response.status_code}")

            if latencies:
                avg_latency = sum(latencies) / len(latencies)
                print(f"Average Search API Latency: {avg_latency*1000:.2f} ms")
                print(f"Min Latency: {min(latencies)*1000:.2f} ms")
                print(f"Max Latency: {max(latencies)*1000:.2f} ms")

            stats = await client.get(f"{API_URL}/stats")
            if stats.status_code == 200:
                s = stats.json()
                print(f"\nTotal Documents in Index: {s['total_documents']}")
                if 'vector_engine' in s:
                    print(f"Vector Engine: {s['vector_engine'].get('engine', 'N/A')}")

        except Exception as e:
            print(f"API Benchmark failed. Make sure the server is running. Error: {e}")

if __name__ == "__main__":
    run_local_benchmark()
    asyncio.run(run_api_benchmark())
