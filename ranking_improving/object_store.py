import os
import time
from google.cloud import firestore

db = firestore.Client()

COLL_OBJECTS = "objects"           # one doc per stable object_id
COLL_SIGHTINGS = "sightings"       # one doc per capture/event

def upsert_object(object_id: str, payload: dict):
    db.collection(COLL_OBJECTS).document(object_id).set(payload, merge=True)

def add_sighting(sighting_id: str, payload: dict):
    db.collection(COLL_SIGHTINGS).document(sighting_id).set(payload, merge=False)

def get_object(object_id: str) -> dict | None:
    doc = db.collection(COLL_OBJECTS).document(object_id).get()
    return doc.to_dict() if doc.exists else None

def list_candidate_objects(limit: int = 200):
    # Fallback mode (no vector index): fetch recent objects
    return db.collection(COLL_OBJECTS).order_by("updated_at", direction=firestore.Query.DESCENDING).limit(limit).stream()
