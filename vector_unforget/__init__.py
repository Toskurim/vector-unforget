"""
VectorUnforget: GDPR/CCPA Right-to-be-Forgotten Engine for Vector Databases.
Author: Toskurim
License: AGPLv3
"""

from .engine import VectorUnforgetEngine
from .verifier import ReverseRAGVerifier

try:
    from .auditor import Auditor
except ImportError:
    try:
        from .auditor import AuditLogger as Auditor
    except ImportError:
        Auditor = None

__all__ = [
    "VectorUnforgetEngine",
    "ReverseRAGVerifier",
    "Auditor",
]