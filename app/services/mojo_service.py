import os
import shutil
import subprocess
import numpy as np

MOJO_SRC = os.path.join(os.path.dirname(__file__), "vector_ops.mojo")
MOJO_BIN = os.path.join(os.path.dirname(__file__), "vector_ops")

_mojo_available = False

def _ensure_compiled():
    global _mojo_available
    if not shutil.which("mojo"):
        return False
    if not os.path.exists(MOJO_SRC):
        return False
    needs_compile = not os.path.exists(MOJO_BIN) or os.path.getmtime(MOJO_SRC) > os.path.getmtime(MOJO_BIN)
    if needs_compile:
        result = subprocess.run(
            ["mojo", "build", MOJO_SRC, "-o", MOJO_BIN],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode != 0:
            print(f"Mojo compilation failed: {result.stderr}")
            return False
    if os.path.exists(MOJO_BIN):
        _mojo_available = True
        return True
    return False

_ensure_compiled()

def get_vector_engine_status() -> dict:
    """Returns the current vector acceleration engine being utilized."""
    if _mojo_available:
        engine = "Native Mojo (MAX Engine)"
    else:
        engine = "NumPy (Optimized SIMD Fallback)"
    return {
        "engine": engine,
        "native_mojo_active": _mojo_available,
        "mojo_cli_available": shutil.which("mojo") is not None,
        "shared_lib_loaded": False,
        "source_file": "app/services/vector_ops.mojo",
        "compiled_binary": MOJO_BIN if _mojo_available else None,
        "mojo_version": _get_mojo_version(),
    }

def _get_mojo_version() -> str:
    try:
        result = subprocess.run(
            ["mojo", "--version"],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip() if result.returncode == 0 else "unknown"
    except Exception:
        return "unknown"

def _run_mojo(data: str) -> str:
    result = subprocess.run(
        [MOJO_BIN],
        input=data,
        capture_output=True,
        text=True,
        timeout=30
    )
    if result.returncode != 0:
        raise RuntimeError(f"Mojo execution failed: {result.stderr}")
    return result.stdout.strip()

def normalize_vector_python(vector: np.ndarray) -> np.ndarray:
    """
    Vector normalization using Mojo (MAX Engine) on Ubuntu.
    Compiles vector_ops.mojo via mojo build and executes it via subprocess.
    Falls back to NumPy if Mojo compilation fails.
    """
    vec_copy = np.ascontiguousarray(vector, dtype=np.float32)

    if _mojo_available:
        try:
            data = ",".join(str(x) for x in vec_copy)
            result = _run_mojo(data)
            values = [float(x) for x in result.split(",")]
            return np.array(values, dtype=np.float32)
        except Exception as e:
            print(f"Mojo normalization failed, falling back to NumPy: {e}")

    norm = np.linalg.norm(vec_copy)
    if norm == 0:
        return vec_copy
    return vec_copy / norm

def compute_similarity_python(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Dot product similarity using Mojo (MAX Engine) on Ubuntu.
    Compiles vector_ops.mojo via mojo build and executes it via subprocess.
    Falls back to NumPy if Mojo fails.
    """
    v1 = np.ascontiguousarray(vec1, dtype=np.float32)
    v2 = np.ascontiguousarray(vec2, dtype=np.float32)

    if _mojo_available and len(v1) == len(v2):
        try:
            data = ",".join(str(x) for x in v1) + "|" + ",".join(str(x) for x in v2)
            result = _run_mojo(data)
            return float(result.strip())
        except Exception as e:
            print(f"Mojo similarity failed, falling back to NumPy: {e}")

    return float(np.dot(v1, v2))
