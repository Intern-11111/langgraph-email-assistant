from fastapi import APIRouter
from src.eval.evaluator import run_full_evaluation

router = APIRouter()

@router.get("/evaluate")
def evaluate_agent():
    report = run_full_evaluation()

    # Save to output file
    import json, os
    os.makedirs("results", exist_ok=True)
    with open("results/m2_eval_report.json", "w") as f:
        json.dump(report, f, indent=2)

    return {
        "summary": {
            "accuracy": report["accuracy"],
            "total": report["total"],
            "correct": report["correct_predictions"]
        },
        "message": "Full evaluation report saved to results/m2_eval_report.json"
    }
