from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.api import documents, search, health

app = FastAPI(
    title="AI Embedding Search Engine",
    description="A complete mini project demonstrating semantic search with FAISS and FastAPI.",
    version="1.0.0"
)

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(documents.router, tags=["Documents"])
app.include_router(search.router, tags=["Search"])
app.include_router(health.router, tags=["System"])

# Ensure frontend directory exists
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
os.makedirs(frontend_dir, exist_ok=True)

# Mount the static files (CSS, JS)
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/", tags=["UI"])
def serve_frontend():
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Frontend not found. Please ensure frontend/index.html exists."}
