import os
import sys
import joblib
import numpy as np

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from feature_engineering.extractor import extract_features

MODEL_PATH = os.path.join(PROJECT_ROOT, "model", "crypto_classifier.pkl")
CONFIDENCE_THRESHOLD = float(os.getenv("PREDICT_THRESHOLD", "0.55"))

# Load model ONCE (important for performance)
model = joblib.load(MODEL_PATH)


def _top_predictions(proba, classes, k=2):
    order = np.argsort(proba)[::-1][:k]
    results = []
    for idx in order:
        results.append({
            "algorithm": str(classes[idx]),
            "confidence": round(float(proba[idx]), 2),
        })
    return results


def predict_cipher(ciphertext: bytes):
    features = extract_features(ciphertext).reshape(1, -1)

    if hasattr(model, "n_features_in_") and model.n_features_in_ != features.shape[1]:
        raise ValueError(
            "Model feature size mismatch. Rebuild features and retrain the model."
        )

    proba = model.predict_proba(features)[0]
    classes = model.classes_
    top_preds = _top_predictions(proba, classes, k=2)

    best_conf = float(proba[np.argmax(proba)])
    predicted = top_preds[0]["algorithm"] if top_preds else "Unknown"
    is_uncertain = best_conf < CONFIDENCE_THRESHOLD

    return {
        "predicted_algorithm": "Unknown" if is_uncertain else predicted,
        "confidence": round(best_conf, 2),
        "top_predictions": top_preds,
        "is_uncertain": is_uncertain,
        "threshold": CONFIDENCE_THRESHOLD,
    }
