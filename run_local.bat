@echo off
echo ============================================================
echo Starting ML Model Serving API locally with Uvicorn...
echo Access Swagger Docs at: http://localhost:8000/docs
echo Access Prometheus Metrics at: http://localhost:8000/metrics
echo ============================================================
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
