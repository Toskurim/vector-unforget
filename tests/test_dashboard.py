import importlib
from vector_unforget import dashboard


def test_dashboard_import():
    assert hasattr(dashboard, "run_dashboard")
