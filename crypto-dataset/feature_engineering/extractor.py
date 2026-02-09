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

    # Frequency distribution (256 features)
    features.extend(byte_frequency(ciphertext))

    return np.array(features, dtype=float)
