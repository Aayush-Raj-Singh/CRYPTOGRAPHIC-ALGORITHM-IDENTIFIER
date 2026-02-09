import os
import csv
from feature_engineering.extractor import extract_features

ENCRYPTED_DIR = "data/encrypted"
LABEL_FILE = "data/labels.csv"
OUTPUT_FILE = "data/features.csv"

def load_labels():
    labels = {}
    with open(LABEL_FILE, newline="") as f:
        reader = csv.reader(f)
        next(reader)
        for fname, algo in reader:
            labels[fname] = algo
    return labels

def main():
    labels = load_labels()
    rows = []

    for algo in os.listdir(ENCRYPTED_DIR):
        algo_dir = os.path.join(ENCRYPTED_DIR, algo)
        if not os.path.isdir(algo_dir):
            continue

        for file in os.listdir(algo_dir):
            path = os.path.join(algo_dir, file)
            with open(path, "rb") as f:
                ciphertext = f.read()

            features = extract_features(ciphertext)
            rows.append(features.tolist() + [labels[file]])

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print("[✔] features.csv generated successfully")

if __name__ == "__main__":
    main()
