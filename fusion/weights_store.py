import os
import logging
from google.cloud import firestore

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")

_DOC_PATH = "fusion/reliability"
_db = None

DEFAULTS = {
    "manufacturing_signature": {"alpha": 8.0, "beta": 2.0},
    "ghost_context": {"alpha": 7.0, "beta": 3.0},
    "partial_completion": {"alpha": 5.0, "beta": 5.0},
    "negative_space": {"alpha": 7.0, "beta": 3.0},
    "visual_semantics": {"alpha": 6.0, "beta": 4.0},
}

def _get_db():
    global _db
    if _db is None:
        _db = firestore.Client()
    return _db

def get_branch_reliability():
    try:
        db = _get_db()
        ref = db.document(_DOC_PATH)
        doc = ref.get()

        if not doc.exists:
            ref.set(DEFAULTS)
            return DEFAULTS

        return doc.to_dict()

    except Exception:
        logging.exception("Failed to read fusion reliability; using defaults")
        return DEFAULTS

def update_branch_reliability(branch_name: str, is_correct: bool):
    try:
        db = _get_db()
        ref = db.document(_DOC_PATH)
        data = ref.get().to_dict() or DEFAULTS

        if branch_name not in data:
            data[branch_name] = {"alpha": 5.0, "beta": 5.0}

        if is_correct:
            data[branch_name]["alpha"] += 1.0
        else:
            data[branch_name]["beta"] += 1.0

        ref.set(data)
        return data[branch_name]

    except Exception:
        logging.exception("Failed to update branch reliability")
        return DEFAULTS.get(branch_name, {"alpha": 5.0, "beta": 5.0})
