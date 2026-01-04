import os
import time
import logging
from google.cloud import firestore

_COLL_OBJECTS = "objects"
_COLL_SIGHTINGS = "sightings"

_db = None

def _get_db():
    global _db
    if _db is None:
        _db = firestore.Client()
    return _db

def upsert_object(object_id: str, payload: dict):
    db = _get_db()
    db.collection(_COLL_OBJECTS).document(object_id).set(payload, merge=True)

def add_sighting(sighting_id: str, payload: dict):
    db = _get_db()
    db.collection(_COLL_SIGHTINGS).document(sighting_id).set(payload, merge=False)

def get_object(object_id: str) -> dict | None:
    db = _get_db()
    doc = db.collection(_COLL_OBJECTS).document(object_id).get()
    return doc.to_dict() if doc.exists else None

def list_candidate_objects(limit: int = 200):
    db = _get_db()
    return (
        db.collection(_COLL_OBJECTS)
        .order_by("updated_at", direction=firestore.Query.DESCENDING)
        .limit(limit)
        .stream()
    )
