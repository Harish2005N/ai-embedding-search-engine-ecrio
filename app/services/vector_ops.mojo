"""
Mojo Vector Math Kernels
=========================
Native Mojo implementation for high-performance vector math operations.

Compiled on Ubuntu with Mojo 1.0.0:
    mojo build vector_ops.mojo -o vector_ops

Used via Python interop through mojo_service.py which executes
this module via subprocess for vector normalization and dot-product.

Supports two modes based on input format:
1. Normalization: pass comma-separated vector, get normalized vector
2. Dot product: pass vec1|vec2, get dot product value
"""

from std.math import sqrt

def l2_norm(vec: List[Float32]) -> Float32:
    """Compute the L2 norm (Euclidean length) of a vector."""
    var sum_sq: Float32 = 0.0
    for i in range(len(vec)):
        sum_sq += vec[i] * vec[i]
    return sqrt(sum_sq)

def normalize_vector_mojo(vec: List[Float32]) -> List[Float32]:
    """Normalize vector and return a new normalized list."""
    var norm = l2_norm(vec)
    var result = List[Float32]()
    if norm == 0.0:
        result = vec.copy()
        return result.copy()
    for i in range(len(vec)):
        result.append(vec[i] / norm)
    return result.copy()

def dot_product_mojo(vec1: List[Float32], vec2: List[Float32]) -> Float32:
    """Compute dot product similarity between two vectors."""
    var dot: Float32 = 0.0
    for i in range(len(vec1)):
        dot += vec1[i] * vec2[i]
    return dot

def main() raises:
    var line = input()
    var parts = line.split("|")
    if len(parts) > 1:
        var vec1 = List[Float32](capacity=0)
        var vec2 = List[Float32](capacity=0)
        for p in parts[0].split(","):
            var t = p.strip()
            if t.byte_length() > 0:
                vec1.append(Float32(Float64(t)))
        for p in parts[1].split(","):
            var t = p.strip()
            if t.byte_length() > 0:
                vec2.append(Float32(Float64(t)))
        print(dot_product_mojo(vec1, vec2))
    else:
            var vec = List[Float32](capacity=0)
            for p in parts[0].split(","):
                var t = p.strip()
                if t.byte_length() > 0:
                    vec.append(Float32(Float64(t)))
            var norm_vec = normalize_vector_mojo(vec)
            var output = ""
            for i in range(len(norm_vec)):
                if i > 0:
                    output += ","
                output += "{}".format(norm_vec[i])
            print(output)
