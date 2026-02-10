import numpy as np
from collections import Counter


def byte_frequency(data: bytes) -> list:
    if not data:
        return [0.0] * 256
    freq = Counter(data)
    return [freq.get(i, 0) / len(data) for i in range(256)]


def chi_square_statistic(data: bytes) -> float:
    if not data:
        return 0.0
    expected = len(data) / 256
    freq = Counter(data)

    chi_sq = 0.0
    for i in range(256):
        observed = freq.get(i, 0)
        chi_sq += ((observed - expected) ** 2) / expected

    return chi_sq


def index_of_coincidence(data: bytes) -> float:
    if not data:
        return 0.0
    freq = Counter(data)
    n = len(data)

    if n <= 1:
        return 0.0

    ic = sum(f * (f - 1) for f in freq.values())
    return ic / (n * (n - 1))
