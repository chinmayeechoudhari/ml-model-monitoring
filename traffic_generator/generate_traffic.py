import time
import random
import argparse
import requests

DEFAULT_URL = "http://localhost:8000/predict"

# Realistic Iris feature profiles
SAMPLE_PROFILES = [
    # Setosa-like
    {"sepal_length": 5.0, "sepal_width": 3.4, "petal_length": 1.5, "petal_width": 0.2},
    {"sepal_length": 4.9, "sepal_width": 3.0, "petal_length": 1.4, "petal_width": 0.2},
    {"sepal_length": 5.4, "sepal_width": 3.9, "petal_length": 1.7, "petal_width": 0.4},
    # Versicolor-like
    {"sepal_length": 6.0, "sepal_width": 2.7, "petal_length": 4.0, "petal_width": 1.2},
    {"sepal_length": 5.7, "sepal_width": 2.8, "petal_length": 4.5, "petal_width": 1.3},
    {"sepal_length": 6.3, "sepal_width": 3.3, "petal_length": 4.7, "petal_width": 1.6},
    # Virginica-like
    {"sepal_length": 7.2, "sepal_width": 3.6, "petal_length": 6.1, "petal_width": 2.5},
    {"sepal_length": 6.5, "sepal_width": 3.0, "petal_length": 5.5, "petal_width": 1.8},
    {"sepal_length": 7.7, "sepal_width": 3.8, "petal_length": 6.7, "petal_width": 2.2},
]

INVALID_PAYLOADS = [
    # Negative measurements (violates > 0 rule)
    {"payload": {"sepal_length": -5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}, "desc": "Negative sepal_length"},
    {"payload": {"sepal_length": 5.1, "sepal_width": -3.5, "petal_length": 1.4, "petal_width": 0.2}, "desc": "Negative sepal_width"},
    # Exceeds max range (> 25 cm)
    {"payload": {"sepal_length": 99.9, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}, "desc": "Out of range value (> 25 cm)"},
    # Missing required field
    {"payload": {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4}, "desc": "Missing petal_width"},
    # Wrong data type (string instead of float)
    {"payload": {"sepal_length": "invalid_string", "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}, "desc": "String type in numeric field"},
]

def generate_random_valid():
    base = random.choice(SAMPLE_PROFILES)
    return {
        "sepal_length": round(base["sepal_length"] + random.uniform(-0.3, 0.3), 2),
        "sepal_width": round(base["sepal_width"] + random.uniform(-0.2, 0.2), 2),
        "petal_length": round(base["petal_length"] + random.uniform(-0.3, 0.3), 2),
        "petal_width": round(base["petal_width"] + random.uniform(-0.1, 0.1), 2),
    }

def send_request(url, payload):
    try:
        response = requests.post(url, json=payload, timeout=5)
        return response.status_code, response.text
    except Exception as e:
        return 0, str(e)

def run_traffic(url, total_requests=100, error_rate=0.2, delay=0.1):
    print(f"==================================================")
    print(f" Traffic Generator for ML Model Monitoring")
    print(f" Target URL     : {url}")
    print(f" Total Requests : {total_requests}")
    print(f" Error Target   : {int(error_rate * 100)}%")
    print(f" Request Delay  : {delay}s")
    print(f"==================================================\n")

    success_count = 0
    error_count = 0

    for i in range(1, total_requests + 1):
        # Determine whether to send an invalid request
        is_error_test = (random.random() < error_rate)

        if is_error_test:
            test_case = random.choice(INVALID_PAYLOADS)
            payload = test_case["payload"]
            desc = test_case["desc"]
            status_code, resp = send_request(url, payload)
            error_count += 1
            print(f"[{i:03d}/{total_requests}] [ERR-TEST] Status: {status_code} | Case: {desc}")
        else:
            payload = generate_random_valid()
            status_code, resp = send_request(url, payload)
            if status_code == 200:
                success_count += 1
                try:
                    data = requests.compat.json.loads(resp)
                    pred_class = data.get("class_name")
                    latency = data.get("latency_ms")
                    print(f"[{i:03d}/{total_requests}] [SUCCESS]  Status: {status_code} | Predicted: {pred_class:<10} | Latency: {latency:.2f}ms")
                except Exception:
                    print(f"[{i:03d}/{total_requests}] [SUCCESS]  Status: {status_code}")
            else:
                error_count += 1
                print(f"[{i:03d}/{total_requests}] [FAILED]   Status: {status_code} | Resp: {resp[:60]}")

        if delay > 0:
            time.sleep(delay)

    print("\n--------------------------------------------------")
    print("Traffic Generation Completed!")
    print(f"Total Sent : {total_requests}")
    print(f"Successes  : {success_count} ({(success_count/total_requests)*100:.1f}%)")
    print(f"Errors     : {error_count} ({(error_count/total_requests)*100:.1f}%)")
    print("--------------------------------------------------")
    print("Check Prometheus (http://localhost:9090) and Grafana (http://localhost:3000) to view dashboard updates!\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate ML API Prediction Traffic")
    parser.add_argument("--url", default=DEFAULT_URL, help="Prediction endpoint URL")
    parser.add_argument("--requests", type=int, default=100, help="Number of requests to send (default: 100)")
    parser.add_argument("--error-rate", type=float, default=0.2, help="Fraction of requests that are invalid (default: 0.2 = 20%)")
    parser.add_argument("--delay", type=float, default=0.1, help="Delay between requests in seconds (default: 0.1)")
    parser.add_argument("--continuous", action="store_true", help="Run continuously until Ctrl+C")

    args = parser.parse_args()

    if args.continuous:
        print("Running in continuous mode. Press Ctrl+C to stop...")
        req_id = 1
        try:
            while True:
                is_error_test = (random.random() < args.error_rate)
                if is_error_test:
                    test_case = random.choice(INVALID_PAYLOADS)
                    status_code, _ = send_request(args.url, test_case["payload"])
                    print(f"[{req_id}] Controlled Error ({test_case['desc']}) -> HTTP {status_code}")
                else:
                    status_code, resp = send_request(args.url, generate_random_valid())
                    print(f"[{req_id}] Valid Request -> HTTP {status_code}")
                req_id += 1
                time.sleep(args.delay)
        except KeyboardInterrupt:
            print("\nContinuous generator stopped.")
    else:
        run_traffic(args.url, total_requests=args.requests, error_rate=args.error_rate, delay=args.delay)
