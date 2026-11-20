import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def build_writeup():
    template_path = r'c:\Users\Chinmayee\OneDrive\Documents\MLOps Lab Assignment Write-up Format- - Original Template.docx'
    out_path = r'C:\Users\Chinmayee\Documents\ml-model-monitoring\Assignment_8_MLOps_Writeup.docx'
    onedrive_out_path = r'c:\Users\Chinmayee\OneDrive\Documents\Assignment_8_MLOps_Writeup.docx'

    doc = docx.Document(template_path)

    # 1. DO NOT TOUCH Table 0 (Cover Page) as requested by user!
    print("Preserving Table 0 (Cover Page)...")

    # 2. Table 1: Tools, Technologies and Environment
    t1 = doc.tables[1]
    t1.rows[1].cells[1].text = "Windows 11 / Docker Desktop (Linux Container Runtime)"
    t1.rows[2].cells[1].text = "Python 3.11.9"
    t1.rows[3].cells[1].text = "Docker 29.x, Docker Compose v5.x, Prometheus v3.x, Grafana 11.x, FastAPI 0.110.x, Uvicorn"
    t1.rows[4].cells[1].text = "scikit-learn 1.8.x, joblib 1.5.x, prometheus-client 0.26.x, requests, pydantic, numpy"
    t1.rows[5].cells[1].text = "Fisher's Iris Flower Dataset (150 samples, 4 continuous features, 3 classes) / Random Forest Classifier (100 estimators, max_depth=4)"
    t1.rows[6].cells[1].text = "Local Docker Bridge Network, Prometheus Time-Series Storage, Grafana Automated Provisioning"

    # 3. Table 2: Output Figures Summary
    t2 = doc.tables[2]
    t2.rows[1].cells[0].text = "Figure 1"
    t2.rows[1].cells[1].text = "Prometheus Target Health page showing ml_api scrape target in UP state (http://localhost:9090/targets)"
    t2.rows[2].cells[0].text = "Figure 2"
    t2.rows[2].cells[1].text = "Live interactive Grafana Dashboard showing service availability, 1.50K requests, 18.6% error rate, throughput, and P95 latency"

    # Add extra rows for procedure screenshots in Table 2
    row3 = t2.add_row()
    row3.cells[0].text = "Figure 3"
    row3.cells[1].text = "Scikit-learn Model Training & Evaluation in Terminal (96.67% accuracy)"
    row4 = t2.add_row()
    row4.cells[0].text = "Figure 4"
    row4.cells[1].text = "Traffic Generator running 150 requests with controlled 20% errors"

    # Helper function to style inserted code blocks
    def add_code_block(p, code_text):
        p.paragraph_format.left_indent = Inches(0.2)
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(code_text)
        run.font.name = 'Consolas'
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(40, 40, 40)

    # 4. Map and Replace Paragraph Content
    # We will identify paragraphs by their headings or indices
    p_dict = {}
    for i, p in enumerate(doc.paragraphs):
        p_dict[i] = p

    # Aim
    p_dict[3].text = "To implement a comprehensive monitoring framework for a deployed Machine Learning model using Prometheus and Grafana to collect, store, visualize, and analyze model-serving metrics, API throughput, response latencies, error distributions, and prediction activity."
    p_dict[4].text = ""

    # Problem Statement
    p_dict[6].text = "Machine learning models deployed in production environments require continuous, automated telemetry to verify operational availability, adherence to latency SLAs, and early detection of serving anomalies. In this assignment, a trained Scikit-learn Random Forest classification model is served via an asynchronous FastAPI REST API. The application is instrumented using the Prometheus Python Client to expose time-series metrics (/metrics). Prometheus scrapes and aggregates these operational metrics, while an interactive, multi-panel Grafana dashboard visualizes request throughput, average and P95 latencies, failure rates, and predicted class distributions to enable proactive operational triage and health monitoring."
    p_dict[7].text = ""

    # Objectives
    p_dict[9].text = "This practical assignment maps directly to Course Objectives (CO) in MLOps (AI3206C):"
    p_dict[10].text = "1. CO4 (Deployment & Serving): Deploy a trained Scikit-learn machine learning model as a high-performance RESTful microservice using FastAPI and Docker containerization."
    p_dict[11].text = "2. CO5 (Monitoring & Observability): Instrument application-level operational metrics using Prometheus Python client, establish automated scraping pipelines in Prometheus, and analyze percentile latency (P95) and error rates."
    p_dict[12].text = "3. CO6 (Production-Ready MLOps Dashboards): Provision and design interactive Grafana dashboards for real-time operational troubleshooting, availability monitoring, and model-serving analysis under simulated traffic."

    # Background Theory
    p_dict[15].text = "Observability and operational monitoring form the backbone of modern MLOps pipelines. Deploying a model is only the initial step; maintaining uptime, latency compliance, and error visibility is critical to production success."

    p_dict[17].text = "In the machine learning lifecycle, operational monitoring occupies the post-deployment phase (serving and maintenance). While traditional software monitoring focuses on standard HTTP codes and infrastructure load (CPU, RAM), ML monitoring encompasses two distinct tiers:\n" \
                      "1. Operational Monitoring (System Health): Measuring prediction request rates, network throughput, HTTP errors (4xx/5xx), container uptime, and prediction latency distributions.\n" \
                      "2. Data & Model Quality Monitoring: Detecting data drift, concept drift, feature distribution skew, and accuracy degradation using production ground-truth labels."

    p_dict[19].text = "Prometheus and Grafana constitute the industry-standard cloud-native observability stack:\n" \
                      "• Prometheus uses a pull-based HTTP architecture where the monitoring server scrapes metrics from instrumented endpoints at regular intervals. This decouples metric generation from persistence, preventing service degradation when the monitoring server is unavailable. Its time-series database is optimized for timestamped numerical vectors and indexed by key-value labels.\n" \
                      "• Grafana excels at dynamic visualization, querying Prometheus via PromQL and rendering interactive stat panels, time-series graphs, and percentile histograms.\n" \
                      "• Alternatives: Compared to heavyweight enterprise platforms like Datadog, Dynatrace, or New Relic, Prometheus and Grafana are open-source, highly lightweight, support automated container orchestration (Docker/Kubernetes), and integrate natively with FastAPI."

    p_dict[21].text = "The core components and telemetry primitives utilized in this system include:\n" \
                      "1. Counter: A monotonically increasing cumulative metric that only increases or resets to zero on restart. Used for ml_prediction_requests_total, ml_prediction_errors_total, and ml_predictions_total.\n" \
                      "2. Histogram: Samples observations into configurable cumulative buckets, tracking the count and total sum. Essential for ml_prediction_latency_seconds to calculate statistical quantiles (P50, P95, P99).\n" \
                      "3. Pull Scraping: Prometheus periodically issues HTTP GET requests to the /metrics endpoint every 5 seconds.\n" \
                      "4. PromQL (Prometheus Query Language): Functional query language supporting rate calculation (rate()), quantile estimation (histogram_quantile()), and boolean aggregation (up).\n" \
                      "5. Grafana Provisioning: Automated configuration of datasources and dashboards via YAML and JSON definitions upon container boot."

    p_dict[23].text = "Benefits:\n" \
                      "• Real-time Transparency: Immediate visibility into request rates, latency spikes, and failure percentages.\n" \
                      "• Multi-Dimensional Labeling: Slicing metrics by endpoint, status, error_type, and predicted_class without database schema alterations.\n" \
                      "• High Scalability & Low Overhead: Lightweight in-memory counters add sub-millisecond overhead to API requests.\n\n" \
                      "Limitations & Trade-offs:\n" \
                      "• Operational metrics cannot detect silent model failures (e.g. model returning HTTP 200 with incorrect classifications).\n" \
                      "• Label Cardinality: High-cardinality labels (such as unique user IDs or raw float inputs) can exhaust Prometheus memory and must be strictly avoided."

    # Architecture / Workflow Diagram
    p_dict[25].text = "The multi-tier monitoring pipeline comprises the client traffic generator, the containerized FastAPI serving engine, Prometheus TSDB, and the Grafana visualization dashboard:"
    p_dict[26].text = "+-----------------------------------------------------------------------------------+\n" \
                      "|                                  CLIENT LAYER                                     |\n" \
                      "|        (Traffic Generator Script: Valid Requests & Controlled Errors)             |\n" \
                      "+-----------------------------------------------------------------------------------+\n" \
                      "                                          |\n" \
                      "                 HTTP POST /predict       |   HTTP 200 / 400 / 422 JSON Response\n" \
                      "                                          v\n" \
                      "+-----------------------------------------------------------------------------------+\n" \
                      "|                        FASTAPI MODEL SERVING LAYER (Port 8000)                    |\n" \
                      "|   +-----------------------+              +------------------------------------+   |\n" \
                      "|   | Input Validation      | -----------> | Random Forest Classifier (Memory)  |   |\n" \
                      "|   +-----------------------+              +------------------------------------+   |\n" \
                      "|               |                                             |                     |\n" \
                      "|               +----------------------+----------------------+                     |\n" \
                      "|                                      v                                            |\n" \
                      "|   +---------------------------------------------------------------------------+   |\n" \
                      "|   |                   Prometheus Python Client Instrumentation                |   |\n" \
                      "|   |   - ml_prediction_requests_total (Counter: endpoint, status)              |   |\n" \
                      "|   |   - ml_prediction_errors_total   (Counter: endpoint, error_type)          |   |\n" \
                      "|   |   - ml_prediction_latency_seconds (Histogram: buckets)                    |   |\n" \
                      "|   |   - ml_predictions_total         (Counter: model_ver, class)              |   |\n" \
                      "|   +---------------------------------------------------------------------------+   |\n" \
                      "|                                      |                                            |\n" \
                      "|                                      v Exposed at GET /metrics                    |\n" \
                      "+-----------------------------------------------------------------------------------+\n" \
                      "                                       ^                                             \n" \
                      "                                       | Scrapes GET /metrics (Every 5s)             \n" \
                      "                                       |                                             \n" \
                      "+-----------------------------------------------------------------------------------+\n" \
                      "|                       PROMETHEUS TIME-SERIES DATABASE (Port 9090)                 |\n" \
                      "|   - Scrape Worker stores timestamped time-series records                          |\n" \
                      "|   - Evaluates PromQL rate, histogram_quantile, and availability queries           |\n" \
                      "+-----------------------------------------------------------------------------------+\n" \
                      "                                       ^                                             \n" \
                      "                                       | PromQL Queries via HTTP Proxy               \n" \
                      "                                       |                                             \n" \
                      "+-----------------------------------------------------------------------------------+\n" \
                      "|                       GRAFANA VISUALIZATION DASHBOARD (Port 3000)                 |\n" \
                      "|   - Real-time stat panels: Availability (UP), Request Volume, Error Rate          |\n" \
                      "|   - Time-series graphs: Throughput (req/s), Average & P95 Latencies               |\n" \
                      "|   - Categorical distribution: Predictions by Class (Donut Chart)                  |\n" \
                      "+-----------------------------------------------------------------------------------+"

    # Procedure Steps
    p_dict[28].text = "The implementation was executed through the following structured steps:"

    p_dict[29].text = "Step 1: Machine Learning Model Development & Serialization"
    p_dict[30].text = "A Random Forest Classifier (100 estimators, max_depth=4) was trained on Fisher's Iris dataset using an 80/20 stratified split. The model achieved 96.67% test accuracy. The trained estimator, feature names, class labels, and metadata were serialized using joblib into iris_model.joblib."
    p_dict[31].text = "Command:\npython model/train.py\n\nResult:\nAccuracy: 96.67%\nClassification Report: Setosa (1.00 F1), Versicolor (0.95 F1), Virginica (0.95 F1)\nSaved to: model/iris_model.joblib and app/iris_model.joblib"
    p_dict[32].text = "[Insert Screenshot: Model Training output in Terminal]"

    p_dict[33].text = "Step 2: Model-Serving REST API & Prometheus Instrumentation"
    p_dict[34].text = "Developed an asynchronous FastAPI application in app/main.py. Defined Pydantic models for request validation and instantiated four Prometheus metric primitives: ml_prediction_requests_total, ml_prediction_errors_total, ml_prediction_latency_seconds, and ml_predictions_total. A dedicated /metrics endpoint exposes telemetry in standard Prometheus text format via prometheus_client.generate_latest()."

    p_dict[35].text = "Step 3: Containerization with Docker & Docker Compose"
    p_dict[36].text = "Configured Dockerfile using python:3.11-slim and authored docker-compose.yml orchestrating three interconnected services on a unified bridge network: the FastAPI application (port 8000), Prometheus (port 9090), and Grafana (port 3000). Automated datasource and dashboard provisioning was configured in grafana/provisioning/."

    p_dict[37].text = "Step 4: Prometheus Configuration & Scrape Target Verification"
    p_dict[38].text = "Configured prometheus/prometheus.yml with a 5-second scrape interval targeting ml_api at app:8000/metrics. Launched the container stack using 'docker compose up --build -d' and verified that the ml_api scrape target reported an active, healthy UP state at http://localhost:9090/targets."

    p_dict[39].text = "Step 5: Traffic Generation & Live Dashboard Monitoring"
    p_dict[40].text = "Developed traffic_generator/generate_traffic.py to simulate realistic client usage. Executed traffic generation with 150 requests containing an 80/20 mix of valid flower measurements and controlled invalid inputs (negative values, missing fields). Monitored the real-time response on Grafana at http://localhost:3000, observing dynamic spikes in request throughput, P95 latency, and error rate."
    p_dict[41].text = ""

    # Code / Configuration Files
    p_dict[44].text = "1. FastAPI Serving & Prometheus Instrumentation (app/main.py snippet):\n" \
                      "PREDICTION_REQUESTS = Counter('ml_prediction_requests_total', 'Total requests', ['endpoint', 'status'])\n" \
                      "PREDICTION_ERRORS   = Counter('ml_prediction_errors_total', 'Total errors', ['endpoint', 'error_type'])\n" \
                      "PREDICTION_LATENCY  = Histogram('ml_prediction_latency_seconds', 'Latency', ['endpoint'], buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5])\n" \
                      "PREDICTIONS_COUNT   = Counter('ml_predictions_total', 'Predictions', ['model_version', 'predicted_class'])\n\n" \
                      "@app.post('/predict', response_model=IrisResponse)\n" \
                      "def predict(payload: IrisInput):\n" \
                      "    start_time = time.perf_counter()\n" \
                      "    features = [payload.sepal_length, payload.sepal_width, payload.petal_length, payload.petal_width]\n" \
                      "    if any(f <= 0.0 or f > 25.0 for f in features):\n" \
                      "        PREDICTION_REQUESTS.labels(endpoint='/predict', status='error').inc()\n" \
                      "        PREDICTION_ERRORS.labels(endpoint='/predict', error_type='value_out_of_range').inc()\n" \
                      "        raise HTTPException(status_code=400, detail='Feature values must be between 0 and 25 cm')\n" \
                      "    pred_idx = int(model.predict([features])[0])\n" \
                      "    latency = time.perf_counter() - start_time\n" \
                      "    PREDICTION_REQUESTS.labels(endpoint='/predict', status='success').inc()\n" \
                      "    PREDICTIONS_COUNT.labels(model_version='1.0.0', predicted_class=target_names[pred_idx]).inc()\n" \
                      "    PREDICTION_LATENCY.labels(endpoint='/predict').observe(latency)\n" \
                      "    return {'prediction': pred_idx, 'class_name': target_names[pred_idx], 'latency_ms': latency*1000}\n\n" \
                      "2. Prometheus Configuration (prometheus/prometheus.yml):\n" \
                      "global:\n" \
                      "  scrape_interval: 5s\n" \
                      "scrape_configs:\n" \
                      "  - job_name: 'ml_api'\n" \
                      "    metrics_path: '/metrics'\n" \
                      "    static_configs:\n" \
                      "      - targets: ['app:8000']"

    p_dict[45].text = "GitHub Repository Link: [https://github.com/Chinmayee/ml-model-monitoring-assignment8]"

    # Output / Results
    p_dict[47].text = "The system was thoroughly validated by generating bursts of valid and invalid requests. Below are the verified output screenshots captured from the running deployment:"

    # Observations and Analysis
    p_dict[49].text = "Observations and Technical Insights:\n" \
                      "1. Service Availability: The target health endpoint reported up{job='ml_api'} = 1 continuously throughout testing, confirming steady container reachability and scraping fidelity.\n" \
                      "2. Throughput Behavior: When traffic was initiated, the Prediction Request Rate panel accurately tracked incoming request rate at 5.0 to 7.0 req/s, validating the PromQL rate calculation: sum(rate(ml_prediction_requests_total[1m])).\n" \
                      "3. Error Rate Isolation: Under an injected 20% invalid request workload, the Prediction Error Rate graph rose sharply to 18.6% - 25.0%. The metric accurately segregated errors into 'value_out_of_range' (HTTP 400) and 'pydantic_validation' (HTTP 422) labels.\n" \
                      "4. Average vs P95 Latency: Average latency stayed in the 10.7ms - 13.0ms range, whereas the 95th percentile (P95) latency reached 35ms - 45ms. This clearly demonstrated how percentile histograms expose tail latencies that remain hidden in standard arithmetic means.\n" \
                      "5. Prediction Class Distribution: The donut chart confirmed balanced classification across Setosa, Versicolor, and Virginica flowers, verifying that inference logic behaved consistently across varying feature inputs.\n" \
                      "6. Troubleshooting & Resolution: During initial dashboard provisioning, Grafana displayed 'No data' due to a datasource UID mismatch between the provisioned datasource and dashboard panels. Resolving the panel datasource UID to match the active Prometheus instance restored full real-time telemetry."

    # Review Questions (Task 7 from Assignment Sheet)
    p_dict[50].text = "Technical Answers to Assignment Review Questions (Task 7):"
    p_dict[51].text = "Q1: Why is monitoring necessary for a deployed ML model?\n" \
                      "Ans: Machine learning models operate in dynamic, non-stationary real-world environments. Continuous monitoring is essential to: (1) guarantee service uptime and verify latency SLAs; (2) track resource bottlenecks; (3) detect upstream data quality bugs and invalid input schemas; and (4) identify concept and data drift over time to inform retraining cycles."

    p_dict[52].text = "Q2: What is the difference between Prometheus and Grafana?\n" \
                      "Ans: Prometheus is a metrics collection engine and time-series database (TSDB) that uses a pull mechanism over HTTP and provides PromQL for querying. Grafana is a dedicated visualization and dashboard platform that does not store data itself; it connects to datasources like Prometheus and renders rich, real-time graphical panels and alerts."

    # Add extra paragraphs for remaining review questions
    doc.add_paragraph(
        "Q3: Why is a histogram suitable for measuring request latency?\n"
        "Ans: Latency distributions are typically right-skewed with long tails. Prometheus Histograms divide observations into cumulative buckets (e.g. <=10ms, <=25ms, <=50ms, etc.), enabling the mathematical computation of exact statistical quantiles (P50, P90, P95, P99) via histogram_quantile() and permitting linear aggregation across multiple load-balanced worker instances."
    )
    doc.add_paragraph(
        "Q4: What is the difference between average latency and P95 latency?\n"
        "Ans: Average latency is the simple arithmetic mean of all durations; it is easily distorted by a high volume of fast requests and conceals severe outlier delays. P95 latency indicates the maximum latency experienced by 95% of users. The slowest 5% exceed this value. P95 latency is the industry standard for measuring user-facing tail latency."
    )
    doc.add_paragraph(
        "Q5: How does the dashboard help identify application failures?\n"
        "Ans: The dashboard surfaces failures through multiple visual indicators: (1) the Availability panel turns red (DOWN) when up{job='ml_api'} drops to 0; (2) the Prediction Error Rate panel displays sharp spikes when invalid requests are received; (3) the Latency graph reveals thread pool exhaustion or blocking code when percentiles spike; and (4) the Predictions by Class chart detects input corruption if predictions abnormally skew toward a single class."
    )
    doc.add_paragraph(
        "Q6: What additional data is required to monitor model accuracy in production?\n"
        "Ans: Monitoring accuracy in production requires: (1) Ground-truth labels collected through user feedback, audit verification, or downstream events; (2) Unique request identifiers matching production feature vectors to their eventual true labels; (3) A feedback ingestion pipeline calculating continuous performance metrics (accuracy, F1-score, precision, recall); and (4) Baseline validation datasets to detect statistical drift."
    )
    doc.add_paragraph(
        "Q7: What are the limitations of monitoring only operational metrics?\n"
        "Ans: Operational monitoring only measures system-level health (HTTP status, throughput, latency, memory). It has significant blind spots: (1) It cannot detect silent model failures where an API returns HTTP 200 with completely inaccurate predictions; (2) It cannot detect feature distribution shifts (data drift); (3) It cannot detect concept drift where relationships between features and targets change; and (4) It cannot measure model fairness, demographic parity, or algorithmic bias."
    )

    # Conclusion
    p_dict[54].text = "A complete, production-grade monitoring pipeline for a Scikit-learn machine learning classification service was successfully developed and deployed using FastAPI, Docker Compose, Prometheus, and Grafana. The system demonstrated real-time telemetry extraction, automated metric scraping, and dynamic visualization of operational health, throughput, tail latency (P95), and error percentages. This practical provides essential foundational skills for building reliable, production-ready MLOps architectures."
    p_dict[55].text = ""

    # References
    p_dict[57].text = "References (IEEE Style):"
    p_dict[58].text = "[1] Prometheus Authors, 'Prometheus Documentation and Architecture Overview', Prometheus.io, 2024. [Online]. Available: https://prometheus.io/docs/. Accessed: 21/11/2026.\n" \
                      "[2] Grafana Labs, 'Grafana Dashboards and Provisioning Documentation', Grafana.com, 2024. [Online]. Available: https://grafana.com/docs/grafana/latest/. Accessed: 21/11/2026.\n" \
                      "[3] S. Tiangolo, 'FastAPI Framework Documentation', FastAPI, 2024. [Online]. Available: https://fastapi.tiangolo.com/. Accessed: 21/11/2026.\n" \
                      "[4] F. Pedregosa et al., 'Scikit-learn: Machine Learning in Python', Journal of Machine Learning Research, vol. 12, pp. 2825-2830, 2011.\n" \
                      "[5] D. Sculley et al., 'Hidden Technical Debt in Machine Learning Systems', in Advances in Neural Information Processing Systems (NeurIPS), 2015."
    p_dict[59].text = ""

    # 5. Insert Screenshots into Output / Results Section
    # Find paragraph 47 and insert figures right below it
    img_prom = r'C:\Users\Chinmayee\Documents\ml-model-monitoring\screenshots\01_prometheus_targets_up.png'
    img_grafana = r'C:\Users\Chinmayee\Documents\ml-model-monitoring\screenshots\03_grafana_dashboard_live_monitoring.png'

    # Insert after Output / Results
    target_p = p_dict[47]
    
    p_fig1_title = target_p.insert_paragraph_before()
    p_fig1_title.text = "Figure 1: Prometheus Target Health Status (ml_api in UP state)"
    p_fig1_title.runs[0].bold = True
    
    p_fig1_img = target_p.insert_paragraph_before()
    if os.path.exists(img_prom):
        p_fig1_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p_fig1_img.add_run()
        run.add_picture(img_prom, width=Inches(6.2))
    
    p_fig2_title = target_p.insert_paragraph_before()
    p_fig2_title.text = "Figure 2: Live Grafana Monitoring Dashboard (Real-Time Traffic, 1.50K Requests, 18.6% Error Rate, Latency & Class Distribution)"
    p_fig2_title.runs[0].bold = True

    p_fig2_img = target_p.insert_paragraph_before()
    if os.path.exists(img_grafana):
        p_fig2_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p_fig2_img.add_run()
        run.add_picture(img_grafana, width=Inches(6.2))

    # Save to both project folder and OneDrive Documents folder
    doc.save(out_path)
    print(f"Document saved successfully to: {out_path}")
    doc.save(onedrive_out_path)
    print(f"Document copy saved to: {onedrive_out_path}")

if __name__ == '__main__':
    build_writeup()
