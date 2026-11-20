Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Starting ML Model Serving API locally with Uvicorn..." -ForegroundColor Green
Write-Host "Swagger Docs: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "Metrics:      http://localhost:8000/metrics" -ForegroundColor Yellow
Write-Host "Health Check: http://localhost:8000/health" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
