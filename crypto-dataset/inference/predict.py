import sys
import os
import joblib
import numpy as np

# Add project root to PYTHONPATH
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from feature_engineering.extractor import extract_features

MODEL = "model/crypto_classifier.pkl"
CONFIDENCE_THRESHOLD = float(os.getenv("PREDICT_THRESHOLD", "0.55"))


def main(file_path):
    if not os.path.exists(file_path):
        print("[-] File does not exist")
        return

    with open(file_path, "rb") as f:
        ciphertext = f.read()

    features = extract_features(ciphertext).reshape(1, -1)
    clf = joblib.load(MODEL)

    if hasattr(clf, "n_features_in_") and clf.n_features_in_ != features.shape[1]:
        print("[-] Model feature size mismatch. Retrain the model first.")
        return

    proba = clf.predict_proba(features)[0]
    classes = clf.classes_
    order = np.argsort(proba)[::-1]

    best_idx = order[0]
    best_conf = float(proba[best_idx])
    predicted = classes[best_idx]
    is_uncertain = best_conf < CONFIDENCE_THRESHOLD

    print(f"[+] Predicted Algorithm: {'Unknown' if is_uncertain else predicted}")
    print(f"[+] Confidence: {best_conf:.2f}")
    print("[+] Top 2 Predictions:")
    for idx in order[:2]:
        print(f"    - {classes[idx]}: {proba[idx]:.2f}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: py inference/predict.py <ciphertext_file>")
    else:
        main(sys.argv[1])
