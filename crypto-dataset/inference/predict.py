import sys
import os
import joblib

# Add project root to PYTHONPATH
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from feature_engineering.extractor import extract_features

MODEL = "model/crypto_classifier.pkl"

def main(file_path):
    if not os.path.exists(file_path):
        print("[-] File does not exist")
        return

    with open(file_path, "rb") as f:
        ciphertext = f.read()

    features = extract_features(ciphertext).reshape(1, -1)
    clf = joblib.load(MODEL)

    prediction = clf.predict(features)[0]
    confidence = max(clf.predict_proba(features)[0])

    print(f"[+] Predicted Algorithm: {prediction}")
    print(f"[+] Confidence: {confidence:.2f}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: py inference/predict.py <ciphertext_file>")
    else:
        main(sys.argv[1])
