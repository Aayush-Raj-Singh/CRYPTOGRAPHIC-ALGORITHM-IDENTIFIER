import os
import argparse
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt

MODEL = "model/crypto_classifier.pkl"
DATASET = "data/features.csv"
REPORT_DIR = "reports"


def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate trained model.")
    parser.add_argument("--dataset", type=str, default=DATASET)
    parser.add_argument("--model", type=str, default=MODEL)
    parser.add_argument("--report-dir", type=str, default=REPORT_DIR)
    parser.add_argument("--test-size", type=float, default=0.15)
    parser.add_argument("--random-state", type=int, default=42)
    return parser.parse_args()


def main():
    args = parse_args()

    df = pd.read_csv(args.dataset, header=None)
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    _, X_test, _, y_test = train_test_split(
        X,
        y,
        test_size=args.test_size,
        random_state=args.random_state,
        stratify=y,
    )

    clf = joblib.load(args.model)
    y_pred = clf.predict(X_test)

    print(classification_report(y_test, y_pred))

    os.makedirs(args.report_dir, exist_ok=True)
    labels = sorted(y.unique())
    cm = confusion_matrix(y_test, y_pred, labels=labels)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(cmap="Blues", colorbar=False, xticks_rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(args.report_dir, "confusion_matrix.png"))
    plt.close()


if __name__ == "__main__":
    main()
