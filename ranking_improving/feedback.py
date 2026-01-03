import time
from google.cloud import firestore
from fusion.weights_store import update_branch_reliability
from ranking.object_store import upsert_object

db = firestore.Client()

def apply_user_feedback(
    request_id: str,
    correct_object_id: str,
    branches_used: list[str],
    was_correct: bool,
):
    """
    Updates:
    1) Fusion reliability (per branch)
    2) Object confidence score
    3) Feedback record
    """
    ts = int(time.time())

    # 1) Update fusion branch reliabilities
    for b in branches_used:
        update_branch_reliability(b, is_correct=was_correct)

    # 2) Update object confidence (simple moving update)
    obj_ref = db.collection("objects").document(correct_object_id)
    obj = obj_ref.get().to_dict() or {}

    prev = float(obj.get("object_confidence", 0.5))
    new = min(1.0, prev + 0.05) if was_correct else max(0.0, prev - 0.08)

    upsert_object(correct_object_id, {
        "object_confidence": new,
        "updated_at": ts,
    })

    # 3) Store feedback event
    db.collection("feedback").document(request_id).set({
        "timestamp": ts,
        "correct_object_id": correct_object_id,
        "was_correct": was_correct,
        "branches_used": branches_used,
    })
