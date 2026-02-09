import os
import sys
import joblib
import numpy as np

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from feature_engineering.extractor import extract_features

MODEL_PATH = os.path.join(PROJECT_ROOT, "model", "crypto_classifier.pkl")

# Load model ONCE (important for performance)
model = joblib.load(MODEL_PATH)

def predict_cipher(ciphertext: bytes):
    features = extract_features(ciphertext).reshape(1, -1)
    prediction = model.predict(features)[0]
    confidence = float(max(model.predict_proba(features)[0]))

    return {
        "predicted_algorithm": prediction,
        "confidence": round(confidence, 2)
    }
