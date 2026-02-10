import math
import zlib
import numpy as np

from feature_engineering.entropy import shannon_entropy


def compression_ratio(data: bytes) -> float:
    if not data:
        return 0.0
    compressed = zlib.compress(data)
    return len(compressed) / len(data)


def sliding_entropy_stats(data: bytes, window_size: int = 256, step: int = 64) -> list:
    if not data:
        return [0.0, 0.0, 0.0, 0.0]

    if len(data) <= window_size:
        ent = shannon_entropy(data)
        return [ent, 0.0, ent, ent]

    entropies = []
    for start in range(0, len(data) - window_size + 1, step):
        window = data[start:start + window_size]
        entropies.append(shannon_entropy(window))

    if not entropies:
        ent = shannon_entropy(data)
        return [ent, 0.0, ent, ent]

    arr = np.array(entropies, dtype=float)
    return [float(arr.mean()), float(arr.std()), float(arr.min()), float(arr.max())]


def hashed_bigrams(data: bytes, bins: int = 512) -> list:
    if len(data) < 2:
        return [0.0] * bins

    counts = [0] * bins
    total = len(data) - 1

    for i in range(total):
        idx = (data[i] * 256 + data[i + 1]) % bins
        counts[idx] += 1

    return [c / total for c in counts]
