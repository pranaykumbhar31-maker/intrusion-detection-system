"""
=============================================================================
Intrusion Detection System (IDS) - Inference Engine (predict.py)
Loads the serialized preprocessor and Random Forest model to evaluate
network traffic features and output predictions with probabilities.
=============================================================================
"""

import os
import joblib
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'intrusion_model.pkl')
PREPROCESSOR_PATH = os.path.join(BASE_DIR, 'model', 'preprocessor.pkl')

# Expected feature schema
REQUIRED_NUMERICAL = [
    'duration', 'src_bytes', 'dst_bytes', 'logged_in',
    'count', 'srv_count', 'same_srv_rate', 'diff_srv_rate',
    'dst_host_srv_count', 'dst_host_same_srv_rate'
]
REQUIRED_CATEGORICAL = ['protocol_type', 'service', 'flag']
ALL_FEATURES = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
    'logged_in', 'count', 'srv_count', 'same_srv_rate', 'diff_srv_rate',
    'dst_host_srv_count', 'dst_host_same_srv_rate'
]

# In-memory cached artifacts
_model = None
_preprocessor = None

def load_artifacts():
    """Load model and preprocessor from disk if not already in memory."""
    global _model, _preprocessor
    if _model is None or _preprocessor is None:
        if not os.path.exists(MODEL_PATH) or not os.path.exists(PREPROCESSOR_PATH):
            raise FileNotFoundError(
                "Trained model artifacts not found. Please run 'python train_model.py' first."
            )
        _model = joblib.load(MODEL_PATH)
        _preprocessor = joblib.load(PREPROCESSOR_PATH)
    return _model, _preprocessor


def validate_input(input_data):
    """
    Validate input dictionary and convert values to expected data types.
    Returns cleaned dictionary or raises ValueError with a descriptive message.
    """
    cleaned = {}

    for cat in REQUIRED_CATEGORICAL:
        val = input_data.get(cat)
        if val is None or str(val).strip() == "":
            raise ValueError(f"Missing required categorical feature: '{cat}'")
        cleaned[cat] = str(val).strip().lower()

    for num in REQUIRED_NUMERICAL:
        val = input_data.get(num)
        if val is None or str(val).strip() == "":
            raise ValueError(f"Missing required numeric feature: '{num}'")
        try:
            val_float = float(val)
            if num in ['duration', 'src_bytes', 'dst_bytes', 'logged_in', 'count', 'srv_count', 'dst_host_srv_count']:
                cleaned[num] = int(round(val_float))
            else:
                cleaned[num] = float(val_float)
        except (ValueError, TypeError):
            raise ValueError(f"Feature '{num}' must be a valid number, got: '{val}'")

    # Basic bounds checking for percentage/rate features
    for rate_col in ['same_srv_rate', 'diff_srv_rate', 'dst_host_same_srv_rate']:
        if not (0.0 <= cleaned[rate_col] <= 1.0):
            # If user entered 0-100%, normalize to 0-1
            if 1.0 < cleaned[rate_col] <= 100.0:
                cleaned[rate_col] = round(cleaned[rate_col] / 100.0, 4)
            else:
                raise ValueError(f"Rate feature '{rate_col}' must be between 0.0 and 1.0 (or 0-100%).")

    return cleaned


def predict_traffic(raw_features):
    """
    Performs end-to-end inference on a single network traffic observation.

    Parameters:
        raw_features (dict): Dictionary mapping feature names to values.

    Returns:
        dict: Result with prediction ('NORMAL' or 'INTRUSION'), probability,
              risk level, confidence percentage, and student-friendly explanation.
    """
    model, preprocessor = load_artifacts()

    # 1. Validate & sanitize
    clean_dict = validate_input(raw_features)

    # 2. Convert to DataFrame with exact column ordering
    df_row = pd.DataFrame([clean_dict])[ALL_FEATURES]

    # 3. Apply saved ColumnTransformer preprocessing
    processed_features = preprocessor.transform(df_row)

    # 4. Model inference
    pred_code = int(model.predict(processed_features)[0]) # 0 = NORMAL, 1 = INTRUSION
    probabilities = model.predict_proba(processed_features)[0] # [P(normal), P(intrusion)]

    prob_normal = float(probabilities[0])
    prob_intrusion = float(probabilities[1])

    if pred_code == 1:
        prediction_label = "INTRUSION"
        probability = round(prob_intrusion, 4)
        confidence_percent = round(prob_intrusion * 100, 2)
        risk_level = "HIGH"
        status_color = "danger"
        explanation = (
            f"Based on the supplied network traffic features, the trained Random Forest model classified "
            f"this activity as an INTRUSION with {confidence_percent}% confidence. "
            f"Indicators such as anomalous connection flags ('{clean_dict['flag']}'), "
            f"rapid connection frequency (count={clean_dict['count']}), and transfer volume suggest suspicious behavior. "
            f"[Academic Disclaimer: This is a Machine Learning statistical prediction based on the NSL-KDD benchmark "
            f"and not a guaranteed forensic determination of malicious activity.]"
        )
    else:
        prediction_label = "NORMAL"
        probability = round(prob_normal, 4)
        confidence_percent = round(prob_normal * 100, 2)
        risk_level = "LOW"
        status_color = "success"
        explanation = (
            f"Based on the supplied network traffic features, the trained Random Forest model classified "
            f"this activity as NORMAL with {confidence_percent}% confidence. "
            f"The connection exhibited standard protocol patterns ('{clean_dict['protocol_type']}'), "
            f"a normal completion flag ('{clean_dict['flag']}'), and balanced transmission rates consistent with benign traffic. "
            f"[Academic Disclaimer: This is a Machine Learning statistical prediction based on the NSL-KDD benchmark "
            f"and not a guaranteed determination of benign activity.]"
        )

    return {
        "status": "success",
        "prediction": prediction_label,
        "probability": probability,
        "confidence_percent": confidence_percent,
        "risk_level": risk_level,
        "status_color": status_color,
        "probabilities": {
            "normal": round(prob_normal * 100, 2),
            "intrusion": round(prob_intrusion * 100, 2)
        },
        "input_features": clean_dict,
        "explanation": explanation
    }


# Realistic Sample Profiles for One-Click Demonstrations
PRESET_SAMPLES = {
    "normal": {
        "title": "Normal Web Browsing Traffic",
        "description": "Legitimate HTTP session over TCP with successful handshake (SF flag) and normal payload bytes.",
        "features": {
            "duration": 0,
            "protocol_type": "tcp",
            "service": "http",
            "flag": "SF",
            "src_bytes": 232,
            "dst_bytes": 8153,
            "logged_in": 1,
            "count": 5,
            "srv_count": 5,
            "same_srv_rate": 1.0,
            "diff_srv_rate": 0.0,
            "dst_host_srv_count": 255,
            "dst_host_same_srv_rate": 1.0
        }
    },
    "attack": {
        "title": "Neptune SYN Flood DoS Attack",
        "description": "Denial of Service SYN flood attack: High burst of unanswered connection attempts (S0 flag) with 0 payload bytes.",
        "features": {
            "duration": 0,
            "protocol_type": "tcp",
            "service": "private",
            "flag": "S0",
            "src_bytes": 0,
            "dst_bytes": 0,
            "logged_in": 0,
            "count": 123,
            "srv_count": 6,
            "same_srv_rate": 0.05,
            "diff_srv_rate": 0.07,
            "dst_host_srv_count": 26,
            "dst_host_same_srv_rate": 0.10
        }
    },
    "probe": {
        "title": "Port Sweep / Network Probe Attack",
        "description": "Port scanning attempt probing multiple services, resulting in rejected connections (REJ flag) and high diff_srv_rate.",
        "features": {
            "duration": 0,
            "protocol_type": "tcp",
            "service": "private",
            "flag": "REJ",
            "src_bytes": 0,
            "dst_bytes": 0,
            "logged_in": 0,
            "count": 2,
            "srv_count": 1,
            "same_srv_rate": 0.5,
            "diff_srv_rate": 1.0,
            "dst_host_srv_count": 1,
            "dst_host_same_srv_rate": 0.0
        }
    }
}
