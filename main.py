import time
import uuid
import os
import json
import logging
import google.auth
from fastapi import FastAPI, File, UploadFile, Body
from fastapi.responses import JSONResponse
from google.cloud import storage, firestore

# -------------------------------------------------------------------
# Environment
# -------------------------------------------------------------------

def get_project_id():
    # 1. Explicit env var (preferred if set)
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if project_id:
        return project_id

    # 2. Cloud Run / GCP metadata fallback
    try:
        _, project_id = google.auth.default()
        if project_id:
            return project_id
    except Exception as e:
        logging.warning(f"google.auth.default() failed: {e}")

    # 3. FINAL fallback (do NOT crash)
    logging.error("GOOGLE_CLOUD_PROJECT not found; running in degraded mode")
    return "unknown-project"

PROJECT_ID = get_project_id()
logging.info(f"Running in project: {PROJECT_ID}")

GEMINI_LOCATION = os.environ.get("GEMINI_LOCATION", "asia-south1")
BUCKET_NAME = os.environ.get(
    "BUCKET_NAME", f"object-identity-images-{PROJECT_ID}"
)

# -------------------------------------------------------------------
# FastAPI app
# -------------------------------------------------------------------

app = FastAPI()

# -------------------------------------------------------------------
# Lazy GCP clients
# -------------------------------------------------------------------

_storage_client = None
_firestore_client = None
_bucket = None

def get_storage():
    global _storage_client, _bucket
    if _storage_client is None:
        _storage_client = storage.Client()
        _bucket = _storage_client.bucket(BUCKET_NAME)
    return _bucket

def get_firestore():
    global _firestore_client
    if _firestore_client is None:
        _firestore_client = firestore.Client()
    return _firestore_client

# -------------------------------------------------------------------
# Ranking alias shim (unchanged)
# -------------------------------------------------------------------

import sys, importlib, types

try:
    sys.modules["ranking"] = types.ModuleType("ranking")
    sys.modules["ranking.object_store"] = importlib.import_module(
        "ranking_improving.object_store"
    )
    sys.modules["ranking.similarity"] = importlib.import_module(
        "ranking_improving.similarity"
    )
    sys.modules["ranking.decay"] = importlib.import_module(
        "ranking_improving.decay"
    )
except Exception:
    logging.exception("Ranking module alias setup failed")

# -------------------------------------------------------------------
# Local imports (SAFE)
# -------------------------------------------------------------------

from preprocess import normalize_image

from branch_a.clip_vit_signs import process_image_bytes as run_branch_a
from branch_b.ghost_context import build_ghost_context_embedding
from branch_c.partial_completion import run_partial_object_completion
from branch_de.branch_d_negative_space import run_branch_d_negative_space
from branch_de.branch_e_semantic_grounding import (
    run_branch_e_semantics_from_gcs,
)

from fusion.fusion_service import run_fusion
from explainability.visual_identity_confidence import (
    build_visual_identity_confidence,
)

from ranking_improving.ranker import rank_top_k_objects
from ranking_improving.feedback import apply_user_feedback
from utils.sanitize import sanitize_for_logs

DEBUG = os.getenv("DEBUG", "false").lower() == "true"

def _sanitize_and_store(uid: str, ts: int, branches: dict, bucket):
    large = {}
    def walk(obj, path):
        if isinstance(obj, dict):
            out = {}
            for k, v in obj.items():
                p = f"{path}.{k}" if path else k
                if isinstance(v, list) and len(v) > 50:
                    large[p] = v
                    out[k] = {"vector_ref": f"gs://{BUCKET_NAME}/embeddings/{ts}_{uid}.json#{p}", "len": len(v)}
                elif isinstance(v, dict):
                    out[k] = walk(v, p)
                else:
                    out[k] = v
            return out
        elif isinstance(obj, list):
            if len(obj) > 50:
                large[path or "list"] = obj
                return {"list_ref": f"gs://{BUCKET_NAME}/embeddings/{ts}_{uid}.json#{path or 'list'}", "len": len(obj)}
            return obj
        return obj
    sanitized = walk(branches, "")
    ref = None
    if large:
        blob_path = f"embeddings/{ts}_{uid}.json"
        bucket.blob(blob_path).upload_from_string(json.dumps(large), content_type="application/json")
        ref = f"gs://{BUCKET_NAME}/{blob_path}"
    return sanitized, ref

# -------------------------------------------------------------------
# Health check (must always succeed)
# -------------------------------------------------------------------

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "services": ["storage", "firestore"],
        "branches": ["A", "B", "C", "D", "E"],
    }

# -------------------------------------------------------------------
# Firestore persistence
# -------------------------------------------------------------------

def store_analysis_in_firestore(
    uid: str,
    ts: int,
    filename: str,
    gcs_uri: str,
    branches: dict,
    fusion_result: dict,
):
    db = get_firestore()
    doc_ref = (
        db.collection("objects")
        .document(uid)
        .collection("sightings")
        .document(str(ts))
    )

    doc_ref.set(
        {
            "timestamp": ts,
            "filename": filename,
            "image_uri": gcs_uri,
            "branches": branches,
            "fusion_result": fusion_result,
            "confirmed": None,
            "created_at": firestore.SERVER_TIMESTAMP,
        }
    )

# -------------------------------------------------------------------
# Main analysis endpoint
# -------------------------------------------------------------------

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    ts = int(time.time())
    uid = str(uuid.uuid4())
    logging.info(f"[{uid}] Analyze request started")

    try:
        raw_bytes = await file.read()

        bucket = get_storage()

        # 1) Store raw image
        raw_name = f"raw/{ts}_{uid}_{file.filename}"
        bucket.blob(raw_name).upload_from_string(
            raw_bytes, content_type=file.content_type
        )

        # 2) Normalize
        norm_bytes = normalize_image(raw_bytes)
        norm_name = f"normalized/{ts}_{uid}.jpg"
        bucket.blob(norm_name).upload_from_string(
            norm_bytes, content_type="image/jpeg"
        )

        gcs_uri = f"gs://{BUCKET_NAME}/{norm_name}"

        # 3) Branch execution (fail-soft)
        branches = {}

        try:
            branches["manufacturing_signature"] = run_branch_a(
                norm_bytes
            )["manufacturing_signature"]
        except Exception:
            logging.exception("Branch A failed")
            branches["manufacturing_signature"] = {"confidence": 0.0}

        try:
            branches["ghost_context"] = build_ghost_context_embedding(
                norm_bytes
            )
        except Exception:
            logging.exception("Branch B failed")
            branches["ghost_context"] = {"confidence": 0.0}

        try:
            branches["partial_completion"] = run_partial_object_completion(
                norm_bytes, n=5
            )
        except Exception:
            logging.exception("Branch C failed")
            branches["partial_completion"] = {"confidence": 0.0}

        try:
            branches["negative_space"] = run_branch_d_negative_space(
                norm_bytes
            )
        except Exception:
            logging.exception("Branch D failed")
            branches["negative_space"] = {"confidence": 0.0}

        try:
            branches["visual_semantics"] = run_branch_e_semantics_from_gcs(
                gcs_uri,
                contextual_text="Object identity grounding",
            )
        except Exception:
            logging.exception("Branch E failed")
            branches["visual_semantics"] = {"confidence": 0.0}

        # 4) Fusion
        fusion_result = run_fusion(branches)

        # 5) Explainability
        explainability = build_visual_identity_confidence(
            norm_jpg_bytes=norm_bytes,
            bucket_name=BUCKET_NAME,
            heatmap_object_path=f"heatmaps/{ts}_{uid}_vit_gradcam.jpg",
            context_for_gemini={
                "fusion_result": fusion_result,
                "branch_weights": fusion_result.get("branch_weights", {}),
            },
        )

        # 6) Ranking
        top_k = []
        try:
            top_k = rank_top_k_objects(
                query_embeddings={
                    "semantic_embedding": branches.get(
                        "visual_semantics", {}
                    ).get("semantic_embedding", []),
                    "negative_space_128d": branches.get(
                        "negative_space", {}
                    ).get("void_signature_128d", []),
                },
                query_meta={
                    "timestamp": ts,
                    "location": {"city": "Bengaluru"},
                },
                k=5,
            )
        except Exception:
            logging.exception("Ranking failed")

        # 7) Sanitize and persist
        try:
            sanitized_branches, embeddings_ref = _sanitize_and_store(uid, ts, branches, bucket)
            store_analysis_in_firestore(
                uid=uid,
                ts=ts,
                filename=file.filename,
                gcs_uri=gcs_uri,
                branches=sanitized_branches,
                fusion_result=fusion_result,
            )
        except Exception:
            logging.exception("Firestore write failed")

        logging.info(f"[{uid}] Analyze request completed")

        response_payload = {
            "request_id": uid,
            "timestamp": ts,
            "normalized_gcs_uri": gcs_uri,
            "fusion_summary": {
                "confidence": fusion_result.get("confidence"),
                "branch_weights": fusion_result.get("branch_weights", {}),
            },
            "branch_confidences": {k: v.get("confidence") for k, v in branches.items()},
            "explainability": {
                "summary": explainability.get("interpretation"),
                "heatmap_object_path": explainability.get("heatmap_object_path"),
            },
            "embeddings_ref": embeddings_ref,
            "top_k": top_k,
        }
        if DEBUG:
            logging.debug(sanitize_for_logs(response_payload))
        return JSONResponse(response_payload)

    except Exception as e:
        logging.exception(f"[{uid}] Analyze request failed")
        return JSONResponse(
            {"status": "error", "message": str(e)}, status_code=500
        )

# -------------------------------------------------------------------
# Feedback endpoint
# -------------------------------------------------------------------

@app.post("/feedback")
async def feedback(payload: dict = Body(...)):
    try:
        apply_user_feedback(
            request_id=payload["request_id"],
            correct_object_id=payload["correct_object_id"],
            branches_used=payload.get(
                "branches_used",
                list(payload.get("branch_weights", {}).keys()),
            ),
            was_correct=bool(payload.get("was_correct", True)),
        )
        return {"status": "ok"}
    except Exception as e:
        logging.exception("Feedback failed")
        return JSONResponse(
            {"status": "error", "message": str(e)}, status_code=500
        )
