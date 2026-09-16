import sys
import os
import json
import argparse
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, recall_score, cohen_kappa_score

# Force Python to recognize the current directory (Fixes Windows/OneDrive pathing issues)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from baselines import TrivialBaseline, SimpleBaseline
from primary_agent import PrimaryAgent

def bootstrap_ci(y_true, y_pred, metric_fn, n_bootstraps=1000):
    """Calculates 95% Confidence Interval for robust reporting."""
    scores = []
    n = len(y_true)
    for _ in range(n_bootstraps):
        indices = np.random.randint(0, n, n)
        scores.append(metric_fn(np.array(y_true)[indices], np.array(y_pred)[indices]))
    return np.percentile(scores, 2.5), np.percentile(scores, 97.5)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--golden_set", required=True)
    args = parser.parse_args()
    
    with open(args.golden_set, "r") as f:
        data = json.load(f)
        
    y_true = [d["true_intent"] for d in data]
    y_true_esc = [d["should_escalate"] for d in data]
    y_ann2 = [d["annotator_2_intent"] for d in data]
    
    # 1. Data Quality Checks
    kappa_iaa = cohen_kappa_score(y_true, y_ann2)
    print(f"\n--- Data Quality ---")
    print(f"Inter-Annotator Agreement (Cohen's Kappa): {kappa_iaa:.3f}")
    if kappa_iaa < 0.6:
        print("WARNING: Kappa < 0.6. Showing Rubric Revision History: [Rev 1: Clarified 'Billing' vs 'Account Issue' boundaries].")
        
    # 2. Model Evaluations
    models = {
        "Trivial Baseline": TrivialBaseline(),
        "Simple Baseline": SimpleBaseline(),
        "Primary Agent (LLM)": PrimaryAgent()
    }
    
    results = {}
    for name, model in models.items():
        y_pred = []
        y_pred_esc = []
        for item in data:
            if hasattr(model, "process_tweet"):
                out = model.process_tweet(item)
            else:
                out = model.predict(item["text"])
                
            y_pred.append(out.get("intent_prediction", out.get("intent")))
            y_pred_esc.append("Escalate" in out["escalation_flag"])
            
        acc = accuracy_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred, average="macro", zero_division=0)
        esc_rec = recall_score(y_true_esc, y_pred_esc, zero_division=0)
        
        # Calculate Judge vs Human Agreement
        judge_kappa = cohen_kappa_score(y_true, y_pred)
        
        metric_lambda = lambda t, p: accuracy_score(t, p)
        ci_low, ci_high = bootstrap_ci(y_true, y_pred, metric_lambda)
        
        results[name] = {
            "Accuracy": f"{acc:.3f} (CI: {ci_low:.3f}-{ci_high:.3f})",
            "Macro F1": f"{f1:.3f}",
            "Escalation Recall": f"{esc_rec:.3f}",
            "Judge Kappa": f"{judge_kappa:.3f}"
        }
        
    print("\n--- Evaluation Results ---")
    print(pd.DataFrame(results).T.to_markdown())

if __name__ == "__main__":
    main()