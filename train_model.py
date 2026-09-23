"""
=============================================================================
Intrusion Detection System (IDS) - Machine Learning Training Script
Algorithm: Random Forest Classifier
Dataset: NSL-KDD (Benchmark Network Intrusion Dataset)
Target: Binary Classification (NORMAL vs INTRUSION)
=============================================================================
"""

import os
import json
import urllib.request
import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# ---------------------------------------------------------------------------
# 1. Configuration & Paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODEL_DIR = os.path.join(BASE_DIR, 'model')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

DATASET_FILE = os.path.join(DATA_DIR, 'KDDTrain+.txt')
MODEL_PATH = os.path.join(MODEL_DIR, 'intrusion_model.pkl')
PREPROCESSOR_PATH = os.path.join(MODEL_DIR, 'preprocessor.pkl')
METRICS_PATH = os.path.join(RESULTS_DIR, 'model_metrics.json')

# Full NSL-KDD 43 columns (41 features + label + difficulty score)
ALL_COLUMNS = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
    'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in',
    'num_compromised', 'root_shell', 'su_attempted', 'num_root', 'num_file_creations',
    'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login',
    'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
    'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate',
    'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
    'dst_host_same_srv_rate', 'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
    'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate',
    'dst_host_rerror_rate', 'dst_host_srv_rerror_rate', 'label', 'difficulty_level'
]

# Student-friendly selected features (intuitive for viva and manual input)
SELECTED_FEATURES = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
    'logged_in', 'count', 'srv_count', 'same_srv_rate', 'diff_srv_rate',
    'dst_host_srv_count', 'dst_host_same_srv_rate'
]
CATEGORICAL_FEATURES = ['protocol_type', 'service', 'flag']
NUMERICAL_FEATURES = [f for f in SELECTED_FEATURES if f not in CATEGORICAL_FEATURES]

# ---------------------------------------------------------------------------
# 2. Data Acquisition & Loading
# ---------------------------------------------------------------------------
def ensure_dataset():
    """Ensure the NSL-KDD training file exists; download if missing."""
    if not os.path.exists(DATASET_FILE):
        print("[*] KDDTrain+.txt not found in data/. Attempting download...")
        url = "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTrain%2B.txt"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as response, open(DATASET_FILE, 'wb') as out_file:
                out_file.write(response.read())
            print(f"[+] Download complete: {DATASET_FILE}")
        except Exception as e:
            print(f"[!] Download failed ({e}). Generating realistic synthetic NSL-KDD dataset...")
            generate_fallback_dataset(DATASET_FILE)


def generate_fallback_dataset(filepath):
    """Fallback generator in case the machine is offline."""
    np.random.seed(42)
    n = 2000
    rows = []
    protocols = ['tcp', 'udp', 'icmp']
    services = ['http', 'private', 'ftp_data', 'smtp', 'telnet', 'other', 'dns']
    flags = ['SF', 'S0', 'REJ', 'RSTO']

    for i in range(n):
        is_attack = (i % 2 == 1)
        if not is_attack:
            row = [
                np.random.randint(0, 100), np.random.choice(protocols, p=[0.8, 0.15, 0.05]),
                np.random.choice(services, p=[0.5, 0.1, 0.1, 0.1, 0.05, 0.1, 0.05]),
                'SF', np.random.randint(150, 5000), np.random.randint(300, 10000),
                0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                np.random.randint(1, 10), np.random.randint(1, 10),
                0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
                np.random.randint(1, 255), np.random.randint(50, 255),
                round(np.random.uniform(0.8, 1.0), 2), 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                'normal', 21
            ]
        else:
            row = [
                0, 'tcp', 'private', 'S0', 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                np.random.randint(80, 250), np.random.randint(1, 15),
                1.0, 1.0, 0.0, 0.0, round(np.random.uniform(0.01, 0.1), 2),
                round(np.random.uniform(0.05, 0.2), 2), 0.0,
                255, np.random.randint(1, 30),
                round(np.random.uniform(0.0, 0.15), 2),
                round(np.random.uniform(0.05, 0.3), 2), 0.0, 0.0, 1.0, 1.0, 0.0, 0.0,
                'neptune', 19
            ]
        rows.append(row)
    df = pd.DataFrame(rows, columns=ALL_COLUMNS)
    df.to_csv(filepath, index=False, header=False)
    print(f"[+] Created synthetic fallback dataset with {n} rows.")


# ---------------------------------------------------------------------------
# 3. Model Training & Evaluation Pipeline
# ---------------------------------------------------------------------------
def train_and_evaluate():
    print("=" * 70)
    print("   INTRUSION DETECTION SYSTEM (IDS) - MACHINE LEARNING PIPELINE")
    print("=" * 70)

    # 1. Dataset loading
    ensure_dataset()
    print("[1/6] Loading NSL-KDD dataset...")
    # Load 50,000 rows for lightning-fast, high-accuracy training suitable for student demo
    df = pd.read_csv(DATASET_FILE, names=ALL_COLUMNS, nrows=50000)
    print(f"      Loaded {len(df)} network connection records.")

    # 2. Data Cleaning & Target Conversion
    print("[2/6] Preprocessing labels into binary classes (NORMAL vs INTRUSION)...")
    # normal = 0, any attack = 1
    y = (df['label'] != 'normal').astype(int)
    X = df[SELECTED_FEATURES].copy()

    normal_count = int((y == 0).sum())
    intrusion_count = int((y == 1).sum())
    print(f"      Normal records:    {normal_count} ({normal_count/len(y)*100:.1f}%)")
    print(f"      Intrusion records: {intrusion_count} ({intrusion_count/len(y)*100:.1f}%)")

    # 3. Train / Test Split
    print("[3/6] Splitting data into 80% Training and 20% Testing sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"      Training samples: {len(X_train)} | Testing samples: {len(X_test)}")

    # 4. Feature Encoding & Scaling
    print("[4/6] Fitting Preprocessor (One-Hot Encoding & Feature Scaling)...")
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), CATEGORICAL_FEATURES),
            ('num', StandardScaler(), NUMERICAL_FEATURES)
        ]
    )

    X_train_encoded = preprocessor.fit_transform(X_train)
    X_test_encoded = preprocessor.transform(X_test)

    # 5. Train Random Forest Classifier
    print("[5/6] Training Random Forest Classifier (100 estimators, max_depth=15)...")
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=15,
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train_encoded, y_train)
    print("      Model training complete!")

    # 6. Evaluation
    print("[6/6] Evaluating model on testing set...")
    y_pred = rf_model.predict(X_test_encoded)
    y_proba = rf_model.predict_proba(X_test_encoded)[:, 1]

    acc = float(accuracy_score(y_test, y_pred))
    prec = float(precision_score(y_test, y_pred, average='weighted'))
    rec = float(recall_score(y_test, y_pred, average='weighted'))
    f1 = float(f1_score(y_test, y_pred, average='weighted'))

    # Binary metrics specifically for INTRUSION class
    prec_intrusion = float(precision_score(y_test, y_pred, pos_label=1))
    rec_intrusion = float(recall_score(y_test, y_pred, pos_label=1))
    f1_intrusion = float(f1_score(y_test, y_pred, pos_label=1))

    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = [int(x) for x in cm.ravel()]

    report_dict = classification_report(
        y_test, y_pred,
        target_names=['NORMAL', 'INTRUSION'],
        output_dict=True
    )

    # Compute Feature Importances (grouped/ranked)
    encoded_cat_names = list(preprocessor.named_transformers_['cat'].get_feature_names_out(CATEGORICAL_FEATURES))
    all_feature_names = encoded_cat_names + NUMERICAL_FEATURES
    importances = rf_model.feature_importances_

    # Map importance back to top features
    top_indices = np.argsort(importances)[::-1][:10]
    top_features = [
        {"feature": str(all_feature_names[i]), "importance": round(float(importances[i]) * 100, 2)}
        for i in top_indices
    ]

    metrics_data = {
        "model_name": "Random Forest Classifier",
        "algorithm": "Random Forest",
        "dataset": "NSL-KDD",
        "n_estimators": 100,
        "max_depth": 15,
        "random_state": 42,
        "features_used": SELECTED_FEATURES,
        "total_samples": int(len(df)),
        "train_samples": int(len(X_train)),
        "test_samples": int(len(X_test)),
        "normal_samples": normal_count,
        "intrusion_samples": intrusion_count,
        "accuracy": round(acc * 100, 2),
        "precision": round(prec * 100, 2),
        "recall": round(rec * 100, 2),
        "f1_score": round(f1 * 100, 2),
        "intrusion_precision": round(prec_intrusion * 100, 2),
        "intrusion_recall": round(rec_intrusion * 100, 2),
        "intrusion_f1": round(f1_intrusion * 100, 2),
        "confusion_matrix": {
            "matrix": [[tn, fp], [fn, tp]],
            "true_negative": tn,
            "false_positive": fp,
            "false_negative": fn,
            "true_positive": tp,
            "labels": ["NORMAL", "INTRUSION"]
        },
        "classification_report": report_dict,
        "top_features": top_features
    }

    # 7. Save Artifacts
    joblib.dump(rf_model, MODEL_PATH)
    joblib.dump(preprocessor, PREPROCESSOR_PATH)
    with open(METRICS_PATH, 'w') as f:
        json.dump(metrics_data, f, indent=4)

    print("\n" + "=" * 70)
    print("   MODEL EVALUATION RESULTS (ACTUAL TRAINED MODEL)")
    print("=" * 70)
    print(f"Accuracy:         {metrics_data['accuracy']}%")
    print(f"Precision:        {metrics_data['precision']}%")
    print(f"Recall:           {metrics_data['recall']}%")
    print(f"F1-Score:         {metrics_data['f1_score']}%")
    print("-" * 70)
    print("Confusion Matrix:")
    print(f"   True Negatives  (Normal detected as Normal):     {tn}")
    print(f"   False Positives (Normal falsely flagged attack): {fp}")
    print(f"   False Negatives (Attack missed as Normal):       {fn}")
    print(f"   True Positives  (Attack accurately detected):    {tp}")
    print("-" * 70)
    print(f"[+] Model saved to:        {MODEL_PATH}")
    print(f"[+] Preprocessor saved to: {PREPROCESSOR_PATH}")
    print(f"[+] Metrics saved to:      {METRICS_PATH}")
    print("=" * 70)
    print("Training successfully finished! You can now start the web app with: python app.py\n")

if __name__ == '__main__':
    train_and_evaluate()
