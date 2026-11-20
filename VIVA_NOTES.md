# Viva Notes: AI Embedding Search Engine

## 1-Minute Pitch
"My project is an AI Embedding Search Engine. It solves the problem of traditional keyword search by understanding the *meaning* of text. It uses an AI model to convert documents into math vectors called embeddings. When a user searches, it converts the query into a vector and uses a high-speed library called FAISS to find the closest matching documents instantly. It's built with a FastAPI backend and a clean, modern web interface."

## 3-Minute Explanation
"Traditional search engines look for exact words. If you search for 'automobile', they might miss a document about 'cars'. My project solves this using Semantic Search. 
Here is how it works:
1. When a document is added, a Python backend uses `sentence-transformers` (a lightweight AI model) to convert the text into a 384-dimensional vector, known as an embedding.
2. This vector represents the meaning of the text. I then normalize this vector so its length is exactly 1.
3. The normalized vector is stored in FAISS, a highly optimized database created by Facebook specifically for vector similarity search.
4. When a user enters a natural language query, it is also converted into a vector. FAISS instantly calculates the 'Cosine Similarity' between the query and all stored documents by performing an inner product search.
5. The highest scoring documents are returned via a FastAPI REST interface and displayed on the web dashboard.
The architecture is designed to support high-performance vector processing, with a dedicated module ready for MAX/Mojo integration for hardware-accelerated numerical operations."

## 20 Likely Viva Questions & Answers

**1. What is an embedding?**
An embedding is an array of numbers (a vector) that captures the semantic meaning of a piece of text. Words with similar meanings have vectors that are closer together in space.

**2. Why is semantic search better than keyword search?**
Keyword search only finds exact string matches. Semantic search understands context and synonyms. If I search "canines", semantic search can find documents about "dogs", whereas keyword search would fail.

**3. What model did you use for embeddings and why?**
I used `all-MiniLM-L6-v2` via `sentence-transformers`. It's a lightweight, open-source model that runs fast locally without requiring a GPU or expensive API calls like OpenAI.

**4. What is vector similarity?**
It's a mathematical way to measure how close two vectors are in space. The closer they are, the more similar the texts they represent.

**5. What is cosine similarity?**
Cosine similarity measures the angle between two vectors. A smaller angle means higher similarity. It ranges from -1 to 1.

**6. Why did you normalize your embeddings?**
When vectors are normalized (magnitude is 1), computing the dot product (inner product) is mathematically identical to calculating cosine similarity. Dot products are much faster for computers to calculate.

**7. What is FAISS?**
FAISS stands for Facebook AI Similarity Search. It's a library optimized for searching massive databases of vectors extremely quickly.

**8. Why use FAISS instead of a standard database or simple Python loop?**
A standard loop comparing arrays in Python is too slow for thousands or millions of documents. FAISS is written in C++ and highly optimized for this specific mathematical task.

**9. What is FastAPI?**
FastAPI is a modern, high-performance web framework for building APIs with Python. It's fast, easy to use, and automatically handles data validation.

**10. Why is MAX/Mojo mentioned in the architecture, and how is it structured?**
Mojo is designed by Modular as a high-performance language with hardware-level SIMD capabilities for AI vector operations.
In this project:
- We have the native Mojo implementation in [`app/services/vector_ops.mojo`](file:///home/harish/mojo-project/ai-embedding-search-engine-main/app/services/vector_ops.mojo) using Mojo 1.0.0 syntax with `List[Float32]`, `def`, `var`, and `from std.math import sqrt`.
- [`app/services/mojo_service.py`](file:///home/harish/mojo-project/ai-embedding-search-engine-main/app/services/mojo_service.py) compiles the Mojo source via `mojo build` on Ubuntu and executes vector operations via subprocess interop. The Mojo executable is compiled to a native binary that handles normalization and dot-product computation with SIMD acceleration through the MAX Engine.


**11. How does the complete data flow work?**
User Input -> FastAPI -> Embedding Service (Text to Vector) -> Mojo/Vector Service (Normalization) -> FAISS (Index Storage) -> Search results returned to Dashboard.

**12. Where is data stored?**
The FAISS vectors are stored in a binary `.index` file, and the document metadata (Title, Content) is stored in a JSON file in the `data/` directory.

**13. What happens when I restart the server?**
The application reads the JSON file and the FAISS index file on startup, so no data is lost. It is fully persistent.

**14. What are the dimensions of your embeddings?**
384 dimensions, which is the output size of the MiniLM model.

**15. Can I search for a document immediately after adding it?**
Yes. The FAISS index is updated dynamically in memory and saved to disk immediately after a document is added.

**16. How did you handle errors?**
FastAPI automatically handles bad requests (like missing fields). I also added `try/except` blocks around model generation and FAISS insertion. If FAISS fails, the document metadata is rolled back so the system remains consistent.

**17. Did you use React for the frontend?**
No, I used plain HTML, CSS, and Vanilla JavaScript. For a mini-project, React adds unnecessary complexity and build steps. This approach is lightweight, easier to deploy, and perfectly responsive.

**18. What is the role of `uvicorn`?**
FastAPI is the framework, but Uvicorn is the actual ASGI web server that runs the code and listens for HTTP requests.

**19. What limitations does this project have?**
- Very long texts might get truncated by the embedding model (usually limited to 256 or 512 tokens).
- JSON storage isn't suitable for millions of records (a proper database like PostgreSQL would be better).

**20. What are some future enhancements?**
- Compile Mojo to shared library (.so) for direct ctypes C ABI interop on Ubuntu.
- Implement document "chunking" (splitting large PDFs/documents into smaller paragraphs before embedding).
- Implement Hybrid Search (combining Semantic FAISS search with Keyword TF-IDF search).

## Technical Concepts to Demonstrate
- Open the `benchmark.py` script to show the Mojo MAX Engine integration and performance metrics.
- Run `python benchmark.py` to see the vector engine status (Mojo MAX Engine vs NumPy fallback).
- Add a document about "Space Exploration" and search for "Astronauts" to prove it finds the document without matching exact words.
- Explain the `vector_ops.mojo` file to show understanding of Mojo on Ubuntu with MAX Engine.
- Show `get_vector_engine_status()` in the `/stats` API endpoint to demonstrate Mojo integration is active.
