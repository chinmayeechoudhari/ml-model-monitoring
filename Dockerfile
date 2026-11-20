FROM python:3.11-slim

WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application and model files
COPY app/ ./app/
COPY model/ ./model/

# Ensure iris_model.joblib exists; if not, train it
RUN if [ ! -f ./app/iris_model.joblib ]; then python ./model/train.py; fi

ENV PYTHONPATH=/workspace
EXPOSE 8000

# Run FastAPI via Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
