import os
import numpy as np

from feature_engineering.entropy import shannon_entropy
from feature_engineering.frequency import (
    byte_frequency,
    chi_square_statistic,
    index_of_coincidence
)
from feature_engineering.structural import (
    block_repetition_ratio,
    length_features
)
from feature_engineering.advanced import (
    compression_ratio,
    sliding_entropy_stats,
    hashed_bigrams
)


def extract_features(ciphertext: bytes) -> np.ndarray:
    features = []

    # Statistical
    features.append(shannon_entropy(ciphertext))
    features.append(chi_square_statistic(ciphertext))
    features.append(index_of_coincidence(ciphertext))

    # Structural
    features.extend(length_features(ciphertext))
    features.append(block_repetition_ratio(ciphertext, 8))
    features.append(block_repetition_ratio(ciphertext, 16))
    features.append(block_repetition_ratio(ciphertext, 32))

    # Compression and local entropy
    features.append(compression_ratio(ciphertext))
    features.extend(sliding_entropy_stats(ciphertext, window_size=256, step=64))

    # Frequency distribution (256 features)
    features.extend(byte_frequency(ciphertext))

    # Hashed bigrams (512 features)
    features.extend(hashed_bigrams(ciphertext, bins=512))

    return np.array(features, dtype=float)
