import os
import json
import argparse
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt

DATASET = "data/features.csv"
MODEL_OUT = "model/crypto_classifier.pkl"
REPORT_DIR = "reports"


def parse_args():
    parser = argparse.ArgumentParser(description="Train calibrated classifier.")
    parser.add_argument("--dataset", type=str, default=DATASET)
    parser.add_argument("--model-out", type=str, default=MODEL_OUT)
    parser.add_argument("--report-dir", type=str, default=REPORT_DIR)
    parser.add_argument("--test-size", type=float, default=0.15)
    parser.add_argument("--val-size", type=float, default=0.15)
    parser.add_argument("--random-state", type=int, default=42)

    parser.add_argument("--n-estimators", type=int, default=600)
    parser.add_argument("--max-depth", type=int, default=None)
    parser.add_argument("--min-samples-leaf", type=int, default=1)
    parser.add_argument("--max-features", type=str, default="sqrt")
    parser.add_argument("--class-weight", type=str, default=None)

    parser.add_argument("--calibration", type=str, default="sigmoid")
    parser.add_argument("--calibration-cv", type=int, default=3)

    parser.add_argument("--no-tune", action="store_true", help="Disable hyperparameter tuning.")
    parser.add_argument("--tune-iter", type=int, default=12)
    parser.add_argument("--cv-folds", type=int, default=3)

    return parser.parse_args()


def parse_class_weight(value: str):
    if value is None:
        return None
    if value.lower() == "balanced":
        return "balanced"
    return None


def parse_max_features(value: str):
    if value is None:
        return "sqrt"
    value = value.strip()
    if value in {"sqrt", "log2"}:
        return value
    try:
        return float(value)
    except ValueError:
        return "sqrt"


def main():
    args = parse_args()

    df = pd.read_csv(args.dataset, header=None)
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    X_temp, X_test, y_temp, y_test = train_test_split(
        X,
        y,
        test_size=args.test_size,
        random_state=args.random_state,
        stratify=y,
    )

    val_size_adjusted = args.val_size / (1.0 - args.test_size)
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp,
        y_temp,
        test_size=val_size_adjusted,
        random_state=args.random_state,
        stratify=y_temp,
    )

    best_params = None
    if args.no_tune:
        clf = RandomForestClassifier(
            n_estimators=args.n_estimators,
            random_state=args.random_state,
            n_jobs=-1,
            max_depth=args.max_depth,
            min_samples_leaf=args.min_samples_leaf,
            max_features=parse_max_features(args.max_features),
            class_weight=parse_class_weight(args.class_weight),
        )
    else:
        base = RandomForestClassifier(
            random_state=args.random_state,
            n_jobs=-1,
        )
        param_dist = {
            "n_estimators": [400, 600, 800],
            "max_depth": [None, 16, 24, 32],
            "min_samples_leaf": [1, 2, 4],
            "min_samples_split": [2, 4, 8],
            "max_features": ["sqrt", 0.5, 0.7],
            "class_weight": [None, "balanced"],
        }
        search = RandomizedSearchCV(
            base,
            param_distributions=param_dist,
            n_iter=args.tune_iter,
            cv=args.cv_folds,
            scoring="accuracy",
            random_state=args.random_state,
            n_jobs=-1,
            verbose=1,
        )
        search.fit(X_train, y_train)
        clf = search.best_estimator_
        best_params = search.best_params_

    X_train_full = pd.concat([X_train, X_val])
    y_train_full = pd.concat([y_train, y_val])

    calibrator = CalibratedClassifierCV(
        clf,
        method=args.calibration,
        cv=args.calibration_cv,
    )
    calibrator.fit(X_train_full, y_train_full)

    y_pred = calibrator.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    os.makedirs(os.path.dirname(args.model_out), exist_ok=True)
    joblib.dump(calibrator, args.model_out)

    os.makedirs(args.report_dir, exist_ok=True)
    report_path = os.path.join(args.report_dir, "classification_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
        f.write(f"\nAccuracy: {accuracy:.4f}\n")

    labels = sorted(y.unique())
    cm = confusion_matrix(y_test, y_pred, labels=labels)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(cmap="Blues", colorbar=False, xticks_rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(args.report_dir, "confusion_matrix.png"))
    plt.close()

    metadata = {
        "dataset": args.dataset,
        "features": X.shape[1],
        "train_size": len(X_train),
        "val_size": len(X_val),
        "test_size": len(X_test),
        "accuracy": accuracy,
        "random_state": args.random_state,
        "calibration": args.calibration,
        "calibration_cv": args.calibration_cv,
        "tuning": {
            "enabled": not args.no_tune,
            "n_iter": args.tune_iter,
            "cv_folds": args.cv_folds,
            "best_params": best_params,
        },
        "model": {
            "n_estimators": getattr(clf, "n_estimators", None),
            "max_depth": getattr(clf, "max_depth", None),
            "min_samples_leaf": getattr(clf, "min_samples_leaf", None),
            "max_features": getattr(clf, "max_features", None),
            "class_weight": getattr(clf, "class_weight", None),
        },
    }

    with open(os.path.join(args.report_dir, "training_metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print("[?] Model trained, calibrated, and saved.")
    print(f"[?] Accuracy: {accuracy:.4f}")
    print(f"[?] Report saved to {report_path}")


if __name__ == "__main__":
    main()
