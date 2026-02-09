import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

DATASET = "data/features.csv"
MODEL_OUT = "model/crypto_classifier.pkl"

def main():
    df = pd.read_csv(DATASET, header=None)
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    clf = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    )
    clf.fit(X_train, y_train)

    joblib.dump(clf, MODEL_OUT)
    print("[✔] Model trained and saved")

if __name__ == "__main__":
    main()
