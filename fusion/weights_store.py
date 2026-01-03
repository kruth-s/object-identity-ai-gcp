import os
from google.cloud import firestore

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")

db = firestore.Client()

DOC_PATH = "fusion/reliability"

DEFAULTS = {
    "manufacturing_signature": {"alpha": 8.0, "beta": 2.0},
    "ghost_context": {"alpha": 7.0, "beta": 3.0},
    "partial_completion": {"alpha": 5.0, "beta": 5.0},
    "negative_space": {"alpha": 7.0, "beta": 3.0},
    "visual_semantics": {"alpha": 6.0, "beta": 4.0},
}

def get_branch_reliability():
    doc = db.document(DOC_PATH).get()
    if not doc.exists:
        db.document(DOC_PATH).set(DEFAULTS)
        return DEFAULTS
    return doc.to_dict()

def update_branch_reliability(branch_name: str, is_correct: bool):
    ref = db.document(DOC_PATH)
    data = ref.get().to_dict() or DEFAULTS

    if branch_name not in data:
        data[branch_name] = {"alpha": 5.0, "beta": 5.0}

    if is_correct:
        data[branch_name]["alpha"] += 1.0
    else:
        data[branch_name]["beta"] += 1.0

    ref.set(data)
    return data[branch_name]
