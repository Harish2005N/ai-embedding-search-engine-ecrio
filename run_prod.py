import uvicorn
import subprocess
import sys

def run_seed():
    """Run the startup seed script."""
    print("Checking for preloaded documents...")
    result = subprocess.run([sys.executable, "startup_seed.py"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Seed script failed: {result.stderr}")
        sys.exit(1)
    print(result.stdout)

if __name__ == "__main__":
    run_seed()
    print("Starting AI Embedding Search Engine (Production)...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=10000, reload=False)