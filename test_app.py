"""
Automated Verification Suite for ML Intrusion Detection System
Tests Flask endpoints, inference pipeline, presets, and error handling.
"""

import unittest
import json
from app import app
from predict import PRESET_SAMPLES

class TestIntrusionDetectionSystem(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_01_index_page(self):
        """Test home / dashboard page loads successfully."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Machine Learning Intrusion Detection System", response.data)

    def test_02_detect_page(self):
        """Test detection page loads with presets and form."""
        response = self.app.get('/detect')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"PREDICT ACTIVITY", response.data)
        self.assertIn(b"Normal Traffic", response.data)
        self.assertIn(b"Attack Traffic", response.data)

    def test_03_performance_page(self):
        """Test performance page loads with metrics and confusion matrix."""
        response = self.app.get('/performance')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Visual Confusion Matrix", response.data)
        self.assertIn(b"Classification Report", response.data)

    def test_04_about_page(self):
        """Test about page loads with viva questions."""
        response = self.app.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Practical / Viva Examination Q&A", response.data)

    def test_05_api_stats(self):
        """Test API stats endpoint."""
        response = self.app.get('/api/stats')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data["status"], "success")
        self.assertTrue(data["model_ready"])
        self.assertIn("model_accuracy", data)

    def test_06_api_model_performance(self):
        """Test API model performance endpoint."""
        response = self.app.get('/api/model-performance')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data["status"], "success")
        self.assertGreater(data["data"]["accuracy"], 95.0)
        self.assertIn("confusion_matrix", data["data"])

    def test_07_api_sample_data(self):
        """Test API sample presets endpoint."""
        response = self.app.get('/api/sample-data')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn("normal", data["samples"])
        self.assertIn("attack", data["samples"])

    def test_08_predict_normal_traffic(self):
        """Test prediction with legitimate Normal network features."""
        payload = PRESET_SAMPLES["normal"]["features"]
        response = self.app.post(
            '/api/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data["prediction"], "NORMAL")
        self.assertEqual(data["risk_level"], "LOW")
        self.assertGreaterEqual(data["confidence_percent"], 50.0)
        self.assertIn("classified this activity as NORMAL", data["explanation"])

    def test_09_predict_attack_traffic(self):
        """Test prediction with malicious Attack (Neptune DoS) features."""
        payload = PRESET_SAMPLES["attack"]["features"]
        response = self.app.post(
            '/api/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data["prediction"], "INTRUSION")
        self.assertEqual(data["risk_level"], "HIGH")
        self.assertGreaterEqual(data["confidence_percent"], 50.0)
        self.assertIn("classified this activity as an INTRUSION", data["explanation"])

    def test_10_predict_invalid_data(self):
        """Test error handling when required features are missing or invalid."""
        payload = {"protocol_type": "tcp", "src_bytes": "invalid_number"}
        response = self.app.post(
            '/api/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data["status"], "error")


if __name__ == '__main__':
    unittest.main()
