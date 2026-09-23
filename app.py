"""
=============================================================================
Intrusion Detection System (IDS) - Flask Web Application (app.py)
Provides web dashboard routes and REST API endpoints for real-time
network traffic classification using the trained Random Forest model.
=============================================================================
"""

import os
import json
import time
from flask import Flask, render_template, request, jsonify, send_file
from predict import predict_traffic, PRESET_SAMPLES, MODEL_PATH, PREPROCESSOR_PATH

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
METRICS_PATH = os.path.join(BASE_DIR, 'results', 'model_metrics.json')

app = Flask(
    __name__,
    template_folder=TEMPLATES_DIR,
    static_folder=STATIC_DIR
)

# Session / runtime state for dashboard counters & history
runtime_stats = {
    "total_predictions": 0,
    "normal_predictions": 0,
    "intrusion_predictions": 0,
    "history": [] # Stores the last 15 predictions for live demonstration table
}


def load_model_metrics():
    """Read saved evaluation metrics from JSON file."""
    if os.path.exists(METRICS_PATH):
        try:
            with open(METRICS_PATH, 'r') as f:
                return json.load(f)
        except Exception:
            return None
    return None


def is_model_ready():
    """Check if trained model files exist."""
    return os.path.exists(MODEL_PATH) and os.path.exists(PREPROCESSOR_PATH)


# ---------------------------------------------------------------------------
# Frontend Page Routes
# ---------------------------------------------------------------------------
@app.route('/')
@app.route('/api/index')
def index():
    """Home / Dashboard Page."""
    metrics = load_model_metrics()
    ready = is_model_ready()
    return render_template(
        'index.html',
        active_page='dashboard',
        model_ready=ready,
        metrics=metrics,
        stats=runtime_stats
    )


@app.route('/detect')
def detect_page():
    """Intrusion Detection Page (Manual form + Preset samples)."""
    metrics = load_model_metrics()
    ready = is_model_ready()
    return render_template(
        'detect.html',
        active_page='detect',
        model_ready=ready,
        metrics=metrics,
        presets=PRESET_SAMPLES
    )


@app.route('/performance')
def performance_page():
    """Model Evaluation & Metrics Page."""
    metrics = load_model_metrics()
    ready = is_model_ready()
    return render_template(
        'performance.html',
        active_page='performance',
        model_ready=ready,
        metrics=metrics
    )


@app.route('/about')
def about_page():
    """About System & Viva Preparation Guide Page."""
    metrics = load_model_metrics()
    return render_template(
        'about.html',
        active_page='about',
        metrics=metrics
    )


@app.route('/download-guide')
def download_guide():
    """Download the academic practical guide PDF."""
    pdf_path = os.path.join(BASE_DIR, 'Intrusion_Detection_System_Practical_Guide.pdf')
    if os.path.exists(pdf_path):
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name='Intrusion_Detection_System_Practical_Guide.pdf',
            mimetype='application/pdf'
        )
    return "PDF guide not found. Run 'python generate_project_pdf.py' to generate it.", 404


# ---------------------------------------------------------------------------
# REST API Endpoints
# ---------------------------------------------------------------------------
@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Return live system counters and metrics."""
    metrics = load_model_metrics()
    return jsonify({
        "status": "success",
        "model_ready": is_model_ready(),
        "runtime_stats": runtime_stats,
        "model_accuracy": metrics.get('accuracy') if metrics else None,
        "dataset": metrics.get('dataset') if metrics else "NSL-KDD",
        "algorithm": metrics.get('algorithm') if metrics else "Random Forest"
    })


@app.route('/api/model-performance', methods=['GET'])
def get_model_performance():
    """Return complete evaluation report and confusion matrix."""
    metrics = load_model_metrics()
    if not metrics:
        return jsonify({
            "status": "error",
            "message": "Model evaluation metrics not found. Please train the model with 'python train_model.py'."
        }), 404
    return jsonify({"status": "success", "data": metrics})


@app.route('/api/sample-data', methods=['GET'])
def get_sample_data():
    """Return pre-configured legitimate and malicious network payloads."""
    return jsonify({"status": "success", "samples": PRESET_SAMPLES})


@app.route('/api/predict', methods=['POST'])
def api_predict():
    """
    Classify a network traffic observation.
    Accepts JSON body with feature values.
    Returns prediction ('NORMAL' or 'INTRUSION'), probability, risk, and explanation.
    """
    if not is_model_ready():
        return jsonify({
            "status": "error",
            "message": "Model is not trained yet! Please run 'python train_model.py' in your terminal."
        }), 503

    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({
            "status": "error",
            "message": "Invalid request. Please provide JSON network traffic features in request body."
        }), 400

    try:
        result = predict_traffic(payload)

        # Update runtime stats
        runtime_stats["total_predictions"] += 1
        if result["prediction"] == "NORMAL":
            runtime_stats["normal_predictions"] += 1
        else:
            runtime_stats["intrusion_predictions"] += 1

        # Keep recent history log
        history_entry = {
            "id": runtime_stats["total_predictions"],
            "timestamp": time.strftime("%H:%M:%S"),
            "protocol": payload.get("protocol_type", "tcp").upper(),
            "service": payload.get("service", "http"),
            "flag": payload.get("flag", "SF"),
            "prediction": result["prediction"],
            "risk_level": result["risk_level"],
            "confidence": f"{result['confidence_percent']}%",
            "status_color": result["status_color"]
        }
        runtime_stats["history"].insert(0, history_entry)
        if len(runtime_stats["history"]) > 15:
            runtime_stats["history"].pop()

        return jsonify(result), 200

    except ValueError as ve:
        return jsonify({
            "status": "error",
            "message": str(ve)
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Inference engine error: {str(e)}"
        }), 500


# ---------------------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    print("\n" + "=" * 65)
    print("   Starting ML Intrusion Detection System Web Application...")
    print("   Open your browser at: http://127.0.0.1:5000")
    print("=" * 65 + "\n")
    app.run(host='127.0.0.1', port=5000, debug=True)
