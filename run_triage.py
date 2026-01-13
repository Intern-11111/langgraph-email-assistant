from src.triage.dataset import load_and_prepare_dataset
from src.triage.model import build_model
from src.triage.evaluate import evaluate_model
from src.triage.triage_node import triage_node

# Load & split data
X_train, X_test, y_train, y_test = load_and_prepare_dataset(
    "data/raw/emails_raw.csv"
)

# Train model
model = build_model()
model.fit(X_train, y_train)

# Evaluate
evaluate_model(model, X_test, y_test)

# Test triage node
state = {
    "email": {
        "subject": "Urgent client meeting",
        "body": "Please review the contract before tomorrow"
    }
}

output = triage_node(state, model)
print("\nTriage Node Output:", output)
