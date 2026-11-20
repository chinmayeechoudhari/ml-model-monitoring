# Assignment 8: Monitor a Machine Learning Model Using Prometheus and Grafana

This repository contains the complete implementation for **Assignment No - 8: Monitor a Machine Learning Model Using Prometheus and Grafana**.

---

## 📁 Project Directory Structure

```text
ml-model-monitoring/
├── app/
│   ├── main.py                     # FastAPI application instrumented with Prometheus metrics
│   └── iris_model.joblib           # Trained ML model artifact
├── model/
│   ├── train.py                    # Scikit-learn model training & evaluation script
│   └── iris_model.joblib           # Backup/source model artifact
├── prometheus/
│   └── prometheus.yml              # Prometheus configuration (scrape interval: 5s, target: ml_api)
├── grafana/
│   ├── provisioning/
│   │   ├── datasources/
│   │   │   └── datasource.yml      # Auto-provisions Prometheus datasource
│   │   └── dashboards/
│   │       └── dashboards.yml      # Auto-loads dashboards on startup
│   └── dashboards/
│       └── ml_model_monitoring_dashboard.json  # Complete pre-built Grafana dashboard
├── traffic_generator/
│   └── generate_traffic.py         # Traffic generator simulating valid and controlled invalid requests
├── Dockerfile                      # Container definition for FastAPI app
├── docker-compose.yml              # Multi-container orchestration (FastAPI + Prometheus + Grafana)
├── requirements.txt                # Python dependencies
├── test_pipeline.py                # Automated local sanity test script
├── run_local.ps1 / run_local.bat   # Local standalone runner scripts
├── ASSIGNMENT_REPORT.md            # Ready-to-use assignment report with Task 7 answers
└── README.md                       # This guide
```

---

## 🛠️ Step-by-Step Instructions: What You Need To Do Manually

Follow these straightforward steps to run, observe, and capture everything needed for your assignment submission.

### Step 1: Start Docker Desktop
1. Open **Docker Desktop** from your Windows Start Menu.
2. Wait until the whale icon in the bottom-left shows **Engine running** (green).

---

### Step 2: Launch the Entire Monitoring Pipeline
1. Open PowerShell or Command Prompt.
2. Navigate to this project folder:
   ```powershell
   cd C:\Users\Chinmayee\Documents\ml-model-monitoring
   ```
3. Run the following command:
   ```powershell
   docker compose up --build -d
   ```
4. This will build the ML API container and download/start Prometheus and Grafana automatically.
5. Verify all containers are running:
   ```powershell
   docker compose ps
   ```
   You should see 3 running services:
   - `ml_prediction_api` on port `8000`
   - `prometheus_service` on port `9090`
   - `grafana_service` on port `3000`

---

### Step 3: Verify the FastAPI App & Prometheus Target
1. Open your browser and visit:
   - Swagger Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Raw Prometheus Metrics: [http://localhost:8000/metrics](http://localhost:8000/metrics)
2. Open Prometheus in your browser:
   - [http://localhost:9090](http://localhost:9090)
3. Navigate to **Status** -> **Targets** ([http://localhost:9090/targets](http://localhost:9090/targets)):
   - Check the `ml_api` target.
   - It should display **State: UP** (green pill).
4. 📸 **Screenshot 1 to capture**: Take a screenshot of the Prometheus targets page showing `ml_api` in the **UP** state (Deliverable for Task 4).

---

### Step 4: Open Grafana & Access the Dashboard
1. Open Grafana in your browser: [http://localhost:3000](http://localhost:3000)
2. Log in with the default credentials:
   - **Username**: `admin`
   - **Password**: `admin`
   *(If prompted to change password, you can click "Skip")*
3. The dashboard and data source are **automatically provisioned**!
4. Navigate to **Dashboards** -> click on **"Machine Learning Model Monitoring Dashboard"**.
5. Set the time range in the top right to **"Last 15 minutes"** and auto-refresh to **"5s"**.

---

### Step 5: Generate Traffic (Valid & Controlled Errors)
To test monitoring under load and verify latency, error rate, and throughput:

1. In your terminal, run the traffic generator script:
   ```powershell
   python traffic_generator/generate_traffic.py --requests 150 --error-rate 0.2 --delay 0.1
   ```
   - This sends 150 requests:
     - ~80% valid requests (realistic flower measurements across Setosa, Versicolor, and Virginica).
     - ~20% controlled invalid requests (negative numbers, schema violations) to test error counters.
2. If you want continuous background traffic while exploring Grafana:
   ```powershell
   python traffic_generator/generate_traffic.py --continuous --delay 0.3
   ```
   *(Press `Ctrl + C` in the terminal when you wish to stop).*

---

### Step 6: Observe Metrics & Take Screenshots
Return to your Grafana dashboard ([http://localhost:3000](http://localhost:3000)) and observe:
1. **Total Prediction Requests**: counter increases as requests arrive.
2. **Prediction Request Rate**: displays requests per second graph.
3. **Average & P95 Prediction Latency**: displays response time distributions.
4. **Prediction Error Rate**: displays the % of failed requests (shows spikes matching the 20% error rate).
5. **Predictions by Class**: donut chart displaying Setosa, Versicolor, and Virginica distribution.
6. **Service Availability**: shows `UP` (value = 1).

📸 **Screenshot 2 to capture**: Full Grafana dashboard showing live graphs with traffic and error spikes (Deliverable for Task 5 & Task 6).

---

### Step 7: Clean Up / Stop Services
When you have finished taking screenshots and completing your observations:
```powershell
docker compose down
```
This stops and removes the containers safely.

---

## 🧪 Alternative: Running Locally Without Docker
If you ever want to run without Docker:
1. Start the FastAPI API:
   ```powershell
   python -m uvicorn app.main:app --port 8000
   ```
2. Run the automated verification test:
   ```powershell
   python test_pipeline.py
   ```
3. Run the traffic generator:
   ```powershell
   python traffic_generator/generate_traffic.py
   ```

---

## 📑 Report Deliverable
All answers to the 7 review questions, model evaluation metrics, PromQL queries, and report structure are provided in [ASSIGNMENT_REPORT.md](file:///C:/Users/Chinmayee/Documents/ml-model-monitoring/ASSIGNMENT_REPORT.md).
