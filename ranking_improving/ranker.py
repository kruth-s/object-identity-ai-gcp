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
    ts_now = int(query_meta.get("timestamp", time.time()))
    q_loc = query_meta.get("location")

    q_sem = query_embeddings.get("semantic_embedding")
    q_neg = query_embeddings.get("negative_space_128d")
    q_mfg = query_embeddings.get("mfg_embedding")

    if not q_sem:
        return []

    results = []

    for doc in list_candidate_objects(limit=fetch_limit):
        obj = doc.to_dict() or {}
        obj_id = doc.id

        emb = obj.get("embeddings", {})
        sem_emb = emb.get("semantic_embedding")
        neg_emb = emb.get("negative_space_128d")

        if not sem_emb:
            continue

        sim_scores = {
            "semantic": cosine_sim(q_sem, sem_emb),
            "negative": cosine_sim(q_neg, neg_emb) if q_neg and neg_emb else 0.0,
        }

        if q_mfg and emb.get("mfg_embedding"):
            sim_scores["mfg"] = cosine_sim(
                q_mfg, emb.get("mfg_embedding")
            )

        sim = blend_similarity(
            sim_scores,
            weights={"semantic": 0.65, "negative": 0.25, "mfg": 0.10},
        )

        ts_old = int(obj.get("updated_at", ts_now))
        tscore = time_decay_score(ts_now, ts_old, half_life_hours=72.0)
        lscore = location_consistency_score(q_loc, obj.get("location"))

        obj_conf = float(obj.get("object_confidence", 0.5))

        match_prob = max(
            0.0,
            min(
                1.0,
                0.55 * sim
                + 0.20 * obj_conf
                + 0.15 * tscore
                + 0.10 * lscore,
            ),
        )

        results.append(
            {
                "object_id": obj_id,
                "match_probability": round(match_prob, 3),
                "similarity": round(sim, 3),
                "location_consistency_score": round(lscore, 3),
                "time_decay_score": round(tscore, 3),
            }
        )

    results.sort(key=lambda x: x["match_probability"], reverse=True)
    top = results[:k]

    for i, r in enumerate(top, start=1):
        r["rank"] = i

    return top
