import os
import sys
import subprocess

print("==> 1. Scrittura corretta di vector_unforget/metrics.py...")
metrics_lines = [
    '"""',
    'Prometheus Metrics & MLOps Telemetry Module for VectorUnforget.',
    'Tracks vector throughput, unlearning latencies, and privacy leakage distribution.',
    '"""',
    '',
    'from typing import Dict, Any',
    'import time',
    '',
    '',
    'class MetricsTracker:',
    '    """',
    '    Lightweight, dependency-free Prometheus exposition metrics collector.',
    '    """',
    '',
    '    def __init__(self):',
    '        self.unlearned_vectors_total = 0',
    '        self.cascading_nodes_erased_total = 0',
    '        self.certificates_generated_total = 0',
    '        self.last_projection_latency_seconds = 0.0',
    '        self.last_leakage_score = 0.0',
    '',
    '    def record_unlearn(self, count: int, latency: float):',
    '        self.unlearned_vectors_total += count',
    '        self.last_projection_latency_seconds = latency',
    '',
    '    def record_graph_resolve(self, nodes_count: int):',
    '        self.cascading_nodes_erased_total += nodes_count',
    '',
    '    def record_certificate(self, leakage_score: float):',
    '        self.certificates_generated_total += 1',
    '        self.last_leakage_score = leakage_score',
    '',
    '    def generate_prometheus_payload(self) -> str:',
    '        items = [',
    '            "# HELP vector_unforget_unlearned_vectors_total Total number of vector embeddings scrubbed via subspace projection.",',
    '            "# TYPE vector_unforget_unlearned_vectors_total counter",',
    '            f"vector_unforget_unlearned_vectors_total {self.unlearned_vectors_total}",',
    '            "",',
    '            "# HELP vector_unforget_cascading_nodes_total Total number of PII graph nodes resolved and erased.",',
    '            "# TYPE vector_unforget_cascading_nodes_total counter",',
    '            f"vector_unforget_cascading_nodes_total {self.cascading_nodes_erased_total}",',
    '            "",',
    '            "# HELP vector_unforget_certificates_total Total compliance audit receipts generated.",',
    '            "# TYPE vector_unforget_certificates_total counter",',
    '            f"vector_unforget_certificates_total {self.certificates_generated_total}",',
    '            "",',
    '            "# HELP vector_unforget_last_projection_latency_seconds Latency of the most recent vector projection batch.",',
    '            "# TYPE vector_unforget_last_projection_latency_seconds gauge",',
    '            f"vector_unforget_last_projection_latency_seconds {round(self.last_projection_latency_seconds, 6)}",',
    '            "",',
    '            "# HELP vector_unforget_last_leakage_score Zero Residual Leakage score of the latest audit.",',
    '            "# TYPE vector_unforget_last_leakage_score gauge",',
    '            f"vector_unforget_last_leakage_score {round(self.last_leakage_score, 6)}",',
    '            ""',
    '        ]',
    '        return "\\n".join(items)',
    '',
    '',
    '# Singleton instance for the runtime',
    'metrics_collector = MetricsTracker()',
    ''
]

with open(os.path.join("vector_unforget", "metrics.py"), "w", encoding="utf-8") as f:
    f.write("\n".join(metrics_lines))

print("==> 2. Esecuzione test suite con pytest...")
test_res = subprocess.run([sys.executable, "-m", "pytest"], capture_output=True, text=True)
print(test_res.stdout)
if test_res.returncode != 0:
    print(test_res.stderr)
    print("ERRORE: I test sono falliti!")
    sys.exit(1)

print("==> 3. Aggiornamento pyproject.toml alla v3.6.0...")
with open("pyproject.toml", "r", encoding="utf-8") as f:
    toml_str = f.read()
toml_str = toml_str.replace('version = "3.5.0"', 'version = "3.6.0"')
with open("pyproject.toml", "w", encoding="utf-8") as f:
    f.write(toml_str)

print("==> 4. Git commit e tag v3.6.0...")
subprocess.run(["git", "add", "."], check=True)
subprocess.run(["git", "commit", "-m", "feat(release): v3.6.0 with Prometheus metrics endpoint and MLOps telemetry"], check=True)
subprocess.run(["git", "tag", "v3.6.0"], check=True)
subprocess.run(["git", "push", "origin", "main", "--tags"], check=True)

print("\nRelease v3.6.0 completata con successo al 100%!")
