import math
from collections import Counter

def shannon_entropy(data: bytes) -> float:
    if not data:
        return 0.0

    freq = Counter(data)
    length = len(data)

    entropy = 0.0
    for count in freq.values():
        p = count / length
        entropy -= p * math.log2(p)

    return entropy
