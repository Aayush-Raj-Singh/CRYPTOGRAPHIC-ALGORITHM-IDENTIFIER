from collections import Counter

def block_repetition_ratio(data: bytes, block_size: int) -> float:
    if len(data) < block_size:
        return 0.0

    blocks = [
        data[i:i + block_size]
        for i in range(0, len(data), block_size)
        if len(data[i:i + block_size]) == block_size
    ]

    total = len(blocks)
    unique = len(set(blocks))

    if total == 0:
        return 0.0

    return 1 - (unique / total)

def length_features(data: bytes) -> list:
    length = len(data)
    return [
        length,
        length % 8,
        length % 16
    ]
