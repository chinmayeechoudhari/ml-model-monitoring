import os
import time
import joblib
import numpy as np
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import Response, JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST,
)

# ---------------------------------------------------------
# Prometheus Metrics Definition (as specified in Assignment Tasks)
# ---------------------------------------------------------
PREDICTION_REQUESTS = Counter(
    "ml_prediction_requests_total",
    "Total prediction requests",
    ["endpoint", "status"]
)

PREDICTION_ERRORS = Counter(
    "ml_prediction_errors_total",
    "Total failed prediction requests",
    ["endpoint", "error_type"]
)

PREDICTION_LATENCY = Histogram(
    "ml_prediction_latency_seconds",
    "Distribution of prediction request latency",
    ["endpoint"],
    buckets=[0.002, 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)

PREDICTIONS_COUNT = Counter(
    "ml_predictions_total",
    "Total successfully generated predictions",
    ["model_version", "predicted_class"]
)

# Global model container
model_data = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load model on startup
    model_paths = [
        os.path.join(os.path.dirname(__file__), "iris_model.joblib"),
        os.path.join(os.path.dirname(__file__), "..", "model", "iris_model.joblib"),
        "iris_model.joblib"
    ]
    loaded = False
    for path in model_paths:
        if os.path.exists(path):
            print(f"Loading model from {path}...")
            model_data["artifact"] = joblib.load(path)
            model_data["model"] = model_data["artifact"]["model"]
            model_data["target_names"] = model_data["artifact"]["target_names"]
            model_data["model_version"] = model_data["artifact"].get("model_version", "1.0.0")
            print(f"Model loaded successfully! Version: {model_data['model_version']}")
            loaded = True
            break
    if not loaded:
        print("WARNING: Model file not found. Predictions will return 500.")
    yield
    model_data.clear()

app = FastAPI(
    title="Iris ML Model Serving API",
    description="REST API for Iris flower classification instrumented with Prometheus metrics",
    version="1.0.0",
    lifespan=lifespan
)

# ---------------------------------------------------------
# Exception Handlers to track metric errors accurately
# ---------------------------------------------------------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    if request.url.path == "/predict":
        PREDICTION_REQUESTS.labels(endpoint="/predict", status="error").inc()
        PREDICTION_ERRORS.labels(endpoint="/predict", error_type="pydantic_validation").inc()
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "message": "Invalid request schema or feature values"}
    )

# ---------------------------------------------------------
# Request & Response Schemas
# ---------------------------------------------------------
class IrisInput(BaseModel):
    sepal_length: float = Field(..., description="Sepal length in cm", example=5.1)
    sepal_width: float = Field(..., description="Sepal width in cm", example=3.5)
    petal_length: float = Field(..., description="Petal length in cm", example=1.4)
    petal_width: float = Field(..., description="Petal width in cm", example=0.2)

class IrisResponse(BaseModel):
    prediction: int
    class_name: str
    probabilities: Dict[str, float]
    latency_ms: float
    model_version: str
    status: str

# ---------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------
@app.get("/")
def root():
    return {
        "service": "Iris ML Model Serving API",
        "status": "online",
        "documentation": "/docs",
        "metrics": "/metrics",
        "health": "/health"
    }

@app.get("/health")
def health_check():
    is_loaded = "model" in model_data and model_data["model"] is not None
    return {
        "status": "healthy" if is_loaded else "degraded",
        "model_loaded": is_loaded,
        "model_version": model_data.get("model_version", "unknown")
    }

@app.get("/metrics")
def metrics():
    """Prometheus scrape endpoint"""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/predict", response_model=IrisResponse)
def predict(payload: IrisInput):
    start_time = time.perf_counter()

    # Domain-specific validation (e.g. realistic physical dimensions)
    features = [payload.sepal_length, payload.sepal_width, payload.petal_length, payload.petal_width]
    if any(f <= 0.0 or f > 25.0 for f in features):
        PREDICTION_REQUESTS.labels(endpoint="/predict", status="error").inc()
        PREDICTION_ERRORS.labels(endpoint="/predict", error_type="value_out_of_range").inc()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Feature measurements must be positive numbers between 0 and 25 cm."
        )

    if "model" not in model_data or model_data["model"] is None:
        PREDICTION_REQUESTS.labels(endpoint="/predict", status="error").inc()
        PREDICTION_ERRORS.labels(endpoint="/predict", error_type="model_not_loaded").inc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Model is not loaded."
        )

    try:
        model = model_data["model"]
        target_names = model_data["target_names"]
        model_version = model_data["model_version"]

        # Run inference
        input_array = np.array([features])
        pred_idx = int(model.predict(input_array)[0])
        pred_class = str(target_names[pred_idx])

        # Get probabilities
        proba = model.predict_proba(input_array)[0]
        prob_dict = {str(target_names[i]): round(float(proba[i]), 4) for i in range(len(target_names))}

        # Calculate latency
        latency_sec = time.perf_counter() - start_time
        latency_ms = round(latency_sec * 1000, 2)

        # Record Prometheus metrics
        PREDICTION_REQUESTS.labels(endpoint="/predict", status="success").inc()
        PREDICTIONS_COUNT.labels(model_version=model_version, predicted_class=pred_class).inc()
        PREDICTION_LATENCY.labels(endpoint="/predict").observe(latency_sec)

        return IrisResponse(
            prediction=pred_idx,
            class_name=pred_class,
            probabilities=prob_dict,
            latency_ms=latency_ms,
            model_version=model_version,
            status="success"
        )
    except Exception as e:
        PREDICTION_REQUESTS.labels(endpoint="/predict", status="error").inc()
        PREDICTION_ERRORS.labels(endpoint="/predict", error_type=type(e).__name__).inc()
        raise HTTPException(status_code=500, detail=str(e))
