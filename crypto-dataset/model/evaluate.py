import pandas as pd
import joblib
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

MODEL = "model/crypto_classifier.pkl"
DATASET = "data/features.csv"

def main():
    df = pd.read_csv(DATASET, header=None)
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    clf = joblib.load(MODEL)
    y_pred = clf.predict(X)

    print(classification_report(y, y_pred))

    cm = confusion_matrix(y, y_pred, labels=clf.classes_)
    sns.heatmap(cm, annot=True, fmt="d",
                xticklabels=clf.classes_,
                yticklabels=clf.classes_)
    plt.title("Confusion Matrix")
    plt.savefig("reports/confusion_matrix.png")
    plt.show()

if __name__ == "__main__":
    main()
