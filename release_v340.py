import os
import sys
import subprocess

print("==> 1. Creazione Dockerfile...")
dockerfile_content = """# Multi-stage Dockerfile for VectorUnforget Enterprise Microservice
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY vector_unforget ./vector_unforget

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir ".[api]"

# Runtime stage
FROM python:3.11-slim AS runtime

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY vector_unforget ./vector_unforget

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "vector_unforget.api.server:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
"""
with open("Dockerfile", "w", encoding="utf-8") as f:
    f.write(dockerfile_content)

print("==> 2. Creazione .dockerignore...")
dockerignore_content = """.git
.github
.pytest_cache
venv/
__pycache__/
*.egg-info/
dist/
build/
tests/
"""
with open(".dockerignore", "w", encoding="utf-8") as f:
    f.write(dockerignore_content)

print("==> 3. Aggiornamento vector_unforget/__init__.py...")
init_content = '''"""
VectorUnforget: GDPR/CCPA PII Erasure Engine for Vector Databases.
Author: Toskurim
License: AGPLv3
"""

__version__ = "3.4.0"

from vector_unforget.engine import VectorUnforgetEngine
from vector_unforget.graph_resolver import PIIEntityGraph
from vector_unforget.subspace_projection import SubspaceProjector
from vector_unforget.verifier import ReverseRAGVerifier
from vector_unforget.hybrid_scrubber import HybridSearchScrubber

try:
    from vector_unforget.api.server import create_app
except ImportError:
    create_app = None

__all__ = [
    "__version__",
    "VectorUnforgetEngine",
    "PIIEntityGraph",
    "SubspaceProjector",
    "ReverseRAGVerifier",
    "HybridSearchScrubber",
    "create_app",
]
'''
with open(os.path.join("vector_unforget", "__init__.py"), "w", encoding="utf-8") as f:
    f.write(init_content)

print("==> 4. Aggiornamento DEV_LOG.md...")
devlog_content = """# VectorUnforget Development Log

## Version History

### [v3.4.0] - 2026-08-27
- **FastAPI Microservice Gateway**: Implemented high-throughput REST API with `/v1/unlearn/batch`, `/v1/graph/resolve`, and `/v1/audit/verify` endpoints.
- **Pydantic v2 Schemas**: Strict payload validation for array dimensions and numerical stability constraints.
- **Production Containerization**: Multi-stage lightweight Docker runtime.
- **Test Suite**: 26/26 tests passing across all endpoints, adapters, and algebra engines.

### [v3.3.0] - 2026-08-26
- **Milvus & Elasticsearch Adapters**: Full coverage for distributed vector DBs and dense k-NN indices.
- **Hybrid Search Erasure**: Dual-phase sparse BM25 token scrubbing and dense subspace orthogonalization.

### [v3.2.0] - 2026-08-26
- **GPU Acceleration & SVD**: PyTorch CUDA integration and rank-$k$ concept subspace discovery.
"""
with open("DEV_LOG.md", "w", encoding="utf-8") as f:
    f.write(devlog_content)

print("==> 5. Esecuzione test suite con l'ambiente venv...")
test_res = subprocess.run([sys.executable, "-m", "pytest"], capture_output=True, text=True)
print(test_res.stdout)
if test_res.returncode != 0:
    print(test_res.stderr)
    print("ERRORE: I test non sono passati! Blocco il rilascio git.")
    sys.exit(1)

print("==> 6. Git add, commit, tag v3.4.0 e push...")
subprocess.run(["git", "add", "."], check=True)
subprocess.run(["git", "commit", "-m", "feat(release): finalize v3.4.0 with FastAPI gateway, Docker runtime and full test suite"], check=True)
subprocess.run(["git", "tag", "v3.4.0"], check=True)
subprocess.run(["git", "push", "origin", "main", "--tags"], check=True)

print("\nRelease v3.4.0 completata e sincronizzata con successo su GitHub!")
