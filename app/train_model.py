import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ml_model import DiabetesMLPipeline

def main():
    print("=" * 60)
    print("      DIABETES PREDICTION - MACHINE LEARNING MODEL TRAINING     ")
    print("=" * 60)
    
    pipeline = DiabetesMLPipeline()
    metrics = pipeline.train_and_evaluate()
    
    print(f"\n[+] Best Model Selected: {metrics['best_model_name']}")
    print("-" * 60)
    print(f"{'Model Name':<25} | {'Accuracy':<8} | {'F1-Score':<8} | {'ROC-AUC':<8}")
    print("-" * 60)
    for model_name, model_metrics in metrics['models'].items():
        acc = model_metrics['accuracy']
        f1 = model_metrics['f1_score']
        auc = model_metrics['roc_auc']
        print(f"{model_name:<25} | {acc:<8.4f} | {f1:<8.4f} | {auc:<8.4f}")
    print("-" * 60)
    print("[+] Model artifacts successfully saved to model/best_model.pkl and model/metrics.json")

if __name__ == '__main__':
    main()
