from sklearn.metrics import accuracy_score
from src.triage.dataset import load_and_split
from src.triage.model import build_model


def evaluate():
    print("Loading dataset...")

    X_train, X_test, y_train, y_test = load_and_split("data/emails_dataset.csv")

    model = build_model()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    acc = accuracy_score(y_test, preds)

    print(f"\nModel Accuracy: {acc:.2f}")


if __name__ == "__main__":
    evaluate()
