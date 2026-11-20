# AI Embedding Search Engine

## Problem Statement
Traditional keyword-based search engines fail to understand the actual meaning of a search query, leading to irrelevant results when synonyms or related concepts are used. There is a need for a system that understands the *semantics* (meaning) of text.

## Objective
To build a web-based AI semantic search engine that can generate text embeddings, efficiently store them, and retrieve semantically similar documents using a natural language query.

## Features
- Natural Language Search: Search by meaning, not just exact keywords.
- Dynamic Embeddings: Uses AI to convert text into vector representations.
- Lightning Fast Search: Uses FAISS for high-speed vector similarity search.
- Modern Dashboard: A clean UI for adding documents and visualizing similarity scores.
- Persistent Storage: Data and index survive server restarts.
- High-Performance Vector Math: Uses native Mojo (MAX Engine) for vector normalization and dot-product computations on Ubuntu/Linux.

## Architecture

                  USER
                   │
                   ▼
            Web Dashboard
                   │
                   ▼
              FastAPI
             /       \
            /         \
           ▼           ▼
   Embedding Service   Document Store
           │
           ▼
    Vector Processing
     (Mojo MAX Engine)
           │
           ▼
      FAISS Index
            │
            ▼
     Similarity Search
            │
            ▼
        Top-K Results
            │
            ▼
         Web Dashboard

## Technology Stack
- **Backend**: Python 3.12+, FastAPI, Uvicorn, Pydantic
- **AI / Embeddings**: `sentence-transformers` (`all-MiniLM-L6-v2`)
- **Vector Search**: FAISS (Facebook AI Similarity Search)
- **Vector Operations**: Native Mojo (MAX Engine) on Ubuntu via `mojo build` + subprocess interop, with NumPy fallback
- **Frontend**: HTML, CSS (Custom styling), Vanilla JavaScript

## Core Concepts

### How Embeddings Work
Embeddings are arrays of numbers (vectors) that represent the semantic meaning of text. Words or sentences with similar meanings will have vectors that are closer together in a high-dimensional space. We use `sentence-transformers` to generate these 384-dimensional vectors.

### How FAISS Works
FAISS is a library developed by Facebook AI that allows for extremely fast similarity search of dense vectors. Instead of comparing a query vector to every single document one by one (which is slow), FAISS uses indexing structures to find the closest vectors in milliseconds.

### How Cosine Similarity Works
Cosine similarity measures the angle between two vectors. A smaller angle means higher similarity. Since we *normalize* our vectors (make their length equal to 1), the dot product of two normalized vectors is mathematically equal to their cosine similarity. We use FAISS `IndexFlatIP` (Inner Product) to compute this instantly.

### Vector Processing with Mojo (MAX Engine)
The project uses native Mojo for high-performance vector operations on Ubuntu/Linux:
- **`app/services/vector_ops.mojo`** — Native Mojo 1.0.0 implementation of L2 norm, vector normalization, and dot-product computation using `List[Float32]` and `std.math.sqrt`.
- **`app/services/mojo_service.py`** — Compiles the Mojo source via `mojo build` on Ubuntu and executes vector operations via subprocess interop. Falls back to NumPy if Mojo is unavailable or compilation fails.

The Mojo functions are compiled to a native binary by `mojo build` and invoked from Python via subprocess, passing vector data through stdin and reading results from stdout. The compiled binary leverages MAX Engine for hardware-accelerated SIMD operations.

> **Note**: Direct C ABI (`.so`/ctypes) integration is currently limited by Mojo 1.0.0 syntax changes (Pointer type inference). The subprocess approach provides the same SIMD acceleration through MAX Engine with a clean Python interface.

## API Documentation

- `GET /`: Serves the web dashboard.
- `GET /health`: Returns system health status.
- `GET /stats`: Returns document count, FAISS configuration, and vector engine status.
- `POST /documents`: Adds a new document. Requires `{"title": "...", "content": "..."}`.
- `GET /documents`: Returns all stored documents.
- `POST /search`: Performs semantic search. Requires `{"query": "...", "top_k": 5}`.

## Setup and Installation

1. Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Ensure Mojo and MAX are installed (optional but recommended for performance):
    ```bash
    mojo --version
    max --version
    ```

## Running the Project

1. Start the server:
    ```bash
    python run.py
    ```
    Or alternatively:
    ```bash
    uvicorn app.main:app --reload
    ```

2. Open your browser and navigate to:
    [http://localhost:8000](http://localhost:8000)

## Adding Documents & Searching
1. (Optional) Run the seed script to automatically populate the database with sample AI/CS documents:
    ```bash
    python seed_data.py
    ```
2. Go to the web UI and use the "Add Document" section to add custom texts.
3. Use the "Semantic Search" section to ask natural language questions (e.g., "How do machines think?").

## Testing and Benchmarking
To run the automated test suite:
```bash
pytest tests/
```

To run performance benchmarks measuring API latency and vector operations:
```bash
python benchmark.py
```

The benchmark will report which vector engine is active (Mojo MAX Engine vs NumPy fallback) and measure operation performance accordingly.

## Future Enhancements
- Compile Mojo to shared library (.so) for direct ctypes C ABI interop.
- Add document chunking for very long texts.
- Add hybrid search (Keyword + Semantic).
- Replace local JSON storage with PostgreSQL/SQLite.
