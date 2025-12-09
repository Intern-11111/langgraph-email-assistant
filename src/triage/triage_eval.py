import json
import os
from collections import defaultdict
from triage_rules import RuleBasedTriage
from triage_llm import LLMFallbackTriage


class TriageEvaluator:

    def __init__(self, golden_set_path=None, use_llm=False, llm_threshold=0.80):
        if golden_set_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.golden_set_path = os.path.join(base_dir, "..", "..", "data", "golden_emails.json")
        else:
            self.golden_set_path = golden_set_path
        self.rules = RuleBasedTriage()
        self.use_llm = use_llm
        self.llm_threshold = llm_threshold
        self.llm = LLMFallbackTriage() if use_llm else None

        # For confusion matrix and prediction counts
        self.confusion = defaultdict(lambda: defaultdict(int))
        self.pred_counts = defaultdict(int)

    # Load golden dataset
    def load_dataset(self):
        with open(self.golden_set_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # Evaluate one email
    def classify_email(self, email):
        subject = email["subject"]
        body = email["body"]
        sender = email.get("sender", "")

        # 1. Rule-based
        rule_result = self.rules.classify(subject, body, sender)
        label = rule_result["label"]
        conf = rule_result["confidence"]

        # 2. If low confidence → fallback to LLM (optional)
        if self.use_llm and conf < self.llm_threshold:
            try:
                llm_result = self.llm.classify(subject, body)
                label = llm_result["label"]
            except Exception as e:
                #rule label on LLM errors (e.g., rate limits)
                label = label

        return label

    # Full evaluation
    def evaluate(self):
        dataset = self.load_dataset()
        correct = 0
        total = len(dataset)

        print("Evaluating triage system...\n")

        for email in dataset:
            human_label = email["human_label"]
            predicted_label = self.classify_email(email)

            # Update confusion matrix
            self.confusion[human_label][predicted_label] += 1
            # Update prediction counts
            self.pred_counts[predicted_label] += 1

            if human_label == predicted_label:
                correct += 1

        accuracy = correct / total

        return accuracy

    def export_excel(self, accuracy: float, output_path: str):
        """Export summary counts and accuracy to an Excel file.

        Includes:
        - Summary sheet with counts for key categories
        - Confusion matrix sheet with full breakdown
        """
        try:
            from openpyxl import Workbook
        except ImportError:
            raise ImportError("openpyxl is not installed. Please add it to requirements or install it.")

        # Map display names to underlying labels
        summary_map = {
            "Spam": ["spam"],
            "Promotion": ["promotion"],
            "Finance": ["finance"],
            "Action Intent": ["meeting"],
            "Job Related": ["job_related"],
            "Transactional": ["transactional"],
            "Automated": ["automated"],
            "Personal": ["personal"],
            "Unknown": ["unknown", "uncertain"],
        }

        wb = Workbook()

        # Summary sheet
        ws_summary = wb.active
        ws_summary.title = "Summary"
        ws_summary.append(["Category", "Count"])
        for display, labels in summary_map.items():
            count = sum(self.pred_counts.get(lbl, 0) for lbl in labels)
            ws_summary.append([display, count])
        ws_summary.append([])
        ws_summary.append(["Final Accuracy", f"{accuracy*100:.2f}%"])

        # Confusion Matrix sheet
        ws_cm = wb.create_sheet("ConfusionMatrix")
        labels = sorted(set(self.confusion.keys()) |
                        {pred for true in self.confusion.values() for pred in true})

        # Header row
        ws_cm.append(["True \\ Pred"] + labels)
        for true_label in labels:
            row = [true_label]
            for pred_label in labels:
                row.append(self.confusion[true_label][pred_label])
            ws_cm.append(row)

        # Ensure directory exists
        out_dir = os.path.dirname(output_path)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)

        wb.save(output_path)

    def print_summary_counts(self, accuracy: float):
        """Print category counts and final accuracy to the terminal."""
        summary_map = {
            "Spam": ["spam"],
            "Promotion": ["promotion"],
            "Finance": ["finance"],
            "Action Intent": ["meeting"],
            "Job Related": ["job_related"],
            "Transactional": ["transactional"],
            "Automated": ["automated"],
            "Personal": ["personal"],
            "Unknown": ["unknown", "uncertain"],
        }

        print("\nSummary Counts:")
        for display, labels in summary_map.items():
            count = sum(self.pred_counts.get(lbl, 0) for lbl in labels)
            print(f"{display}: {count}")
        print(f"\nFinal Accuracy: {accuracy*100:.2f}%")

    #confusion matrix
    def print_confusion_matrix(self):
        labels = sorted(set(self.confusion.keys()) |
                        {pred for true in self.confusion.values() for pred in true})

        print("\nConfusion Matrix:")
        print("True ↓  Pred →\n")

        # Header row
        print("{:<15}".format(""), end="")
        for label in labels:
            print("{:<15}".format(label), end="")
        print()

        # Each row
        for true_label in labels:
            print("{:<15}".format(true_label), end="")
            for pred_label in labels:
                count = self.confusion[true_label][pred_label]
                print("{:<15}".format(count), end="")
            print()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Evaluate the triage system")
    parser.add_argument("--use-llm", action="store_true", help="Enable LLM fallback during evaluation")
    parser.add_argument("--llm-threshold", type=float, default=0.80, help="Confidence threshold to trigger LLM fallback")
    args = parser.parse_args()

    evaluator = TriageEvaluator(use_llm=args.use_llm, llm_threshold=args.llm_threshold)
    accuracy = evaluator.evaluate()

    print(f"\nInitial Accuracy: {accuracy*100:.2f}%")

    evaluator.print_confusion_matrix()
    evaluator.print_summary_counts(accuracy)
    # Always interactive prompt for Excel export
    try:
        default_out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "triage_results.xlsx")
        choice = input("\nExport results to Excel? (y=save to default, c=choose path, N=skip) [y/N/c]: ").strip().lower()
        if choice in ("y", "yes"):
            out_path = default_out
            evaluator.export_excel(accuracy, out_path)
            print(f"\nExcel results saved to: {out_path}")
        elif choice in ("c", "choose", "custom"):
            out_path = input(f"Enter Excel output path [{default_out}]: ").strip()
            if not out_path:
                out_path = default_out
            evaluator.export_excel(accuracy, out_path)
            print(f"\nExcel results saved to: {out_path}")
        else:
            print("\nSkipping Excel export.")
    except Exception as e:
        print("\nExcel export failed:", e)
