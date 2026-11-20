import time
import requests
import subprocess
import sys

def test_api():
    print("Testing API locally...")
    # Health check
    try:
        r = requests.get("http://127.0.0.1:8000/health", timeout=3)
        print("GET /health ->", r.status_code, r.json())
        assert r.status_code == 200

        # Valid predict
        payload = {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}
        r = requests.post("http://127.0.0.1:8000/predict", json=payload, timeout=3)
        print("POST /predict (valid) ->", r.status_code, r.json())
        assert r.status_code == 200

        # Invalid predict (negative value)
        invalid_payload = {"sepal_length": -5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}
        r = requests.post("http://127.0.0.1:8000/predict", json=invalid_payload, timeout=3)
        print("POST /predict (invalid value) ->", r.status_code, r.json())
        assert r.status_code == 400

        # Invalid schema (missing field)
        missing_payload = {"sepal_length": 5.1, "sepal_width": 3.5}
        r = requests.post("http://127.0.0.1:8000/predict", json=missing_payload, timeout=3)
        print("POST /predict (missing field) ->", r.status_code, r.json())
        assert r.status_code == 422

        # Check /metrics
        r = requests.get("http://127.0.0.1:8000/metrics", timeout=3)
        print("GET /metrics ->", r.status_code)
        assert r.status_code == 200
        text = r.text
        assert "ml_prediction_requests_total" in text
        assert "ml_prediction_errors_total" in text
        assert "ml_prediction_latency_seconds" in text
        assert "ml_predictions_total" in text
        print("\nAll 4 mandatory Prometheus metrics found in /metrics output!")
        for line in text.splitlines():
            if line.startswith("ml_"):
                print("  ", line)

        print("\nAPI test PASSED successfully!")
    except Exception as e:
        print("API test failed:", e)
        sys.exit(1)

if __name__ == "__main__":
    test_api()
