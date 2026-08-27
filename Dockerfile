# Multi-stage Dockerfile for VectorUnforget Enterprise Microservice
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends     build-essential     && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY vector_unforget ./vector_unforget

RUN pip install --no-cache-dir --upgrade pip &&     pip install --no-cache-dir ".[api]"

# Runtime stage
FROM python:3.11-slim AS runtime

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY vector_unforget ./vector_unforget

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "vector_unforget.api.server:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
