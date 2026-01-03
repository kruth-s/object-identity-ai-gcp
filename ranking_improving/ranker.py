import time
from ranking.object_store import list_candidate_objects
from ranking.similarity import cosine_sim, blend_similarity
from ranking.decay import time_decay_score, location_consistency_score

def rank_top_k_objects(
    query_embeddings: dict,
    query_meta: dict,
    k: int = 5,
    fetch_limit: int = 200,
) -> list:
    """
    query_embeddings:
      {
        "semantic_embedding": [...],
        "negative_space_128d": [...],
        "mfg_embedding": [...] (optional)
      }
    query_meta:
      {"timestamp": int, "location": {...}}
    """
    ts_now = int(query_meta.get("timestamp", time.time()))
    q_loc = query_meta.get("location")

    results = []

    # Fallback retrieval: pull recent objects then compute cosine locally.
    # (Upgrade to Firestore/Vertex vector KNN later.)
    for doc in list_candidate_objects(limit=fetch_limit):
        obj = doc.to_dict()
        obj_id = doc.id

        emb = obj.get("embeddings", {})
        if not emb.get("semantic_embedding"):
            continue

        sim_scores = {
            "semantic": cosine_sim(query_embeddings["semantic_embedding"], emb["semantic_embedding"]),
            "negative": cosine_sim(query_embeddings["negative_space_128d"], emb.get("negative_space_128d", query_embeddings["negative_space_128d"])),
        }
        if query_embeddings.get("mfg_embedding") and emb.get("mfg_embedding"):
            sim_scores["mfg"] = cosine_sim(query_embeddings["mfg_embedding"], emb["mfg_embedding"])

        # Similarity weights (tuneable)
        sim = blend_similarity(sim_scores, weights={"semantic": 0.65, "negative": 0.25, "mfg": 0.10})

        # Time/location terms
        ts_old = int(obj.get("updated_at", ts_now))
        tscore = time_decay_score(ts_now, ts_old, half_life_hours=72.0)
        lscore = location_consistency_score(q_loc, obj.get("location"))

        # Use object’s historical confidence
        obj_conf = float(obj.get("object_confidence", 0.5))

        # Final match probability (bounded)
        match_prob = max(0.0, min(1.0, 0.55 * sim + 0.20 * obj_conf + 0.15 * tscore + 0.10 * lscore))

        results.append({
            "object_id": obj_id,
            "match_probability": round(match_prob, 3),
            "similarity": round(sim, 3),
            "location_consistency_score": round(lscore, 3),
            "time_decay_score": round(tscore, 3),
        })

    results.sort(key=lambda x: x["match_probability"], reverse=True)
    top = results[:k]

    # Add ranks
    for i, r in enumerate(top, start=1):
        r["rank"] = i

    return top
