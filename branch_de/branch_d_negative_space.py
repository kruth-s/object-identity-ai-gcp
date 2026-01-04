from branch_de.segmentation import segment_foreground_mask
from branch_de.negative_space_signature import (
    edge_irregularity_score,
    find_void_regions,
    negative_space_signature_128,
)
from branch_de.void_graph import build_void_graph
import logging


def run_branch_d_negative_space(norm_jpg_bytes: bytes) -> dict:
    try:
        fg_mask = segment_foreground_mask(norm_jpg_bytes)
        edge_irreg = edge_irregularity_score(fg_mask)
        voids, _ = find_void_regions(fg_mask)

        sig128 = negative_space_signature_128(voids, edge_irreg)
        graph = build_void_graph(voids)

        conf = 1.0 / (1.0 + 0.08 * edge_irreg + 0.03 * len(voids))
        conf = max(0.0, min(1.0, conf))

        return {
            "confidence": round(float(conf), 3),
            "void_signature_128d": sig128,
            "void_graph": graph,
            "edge_irregularity_score": round(float(edge_irreg), 3),
            "void_count": len(voids),
            "interpretation": (
                "Negative space signature + void graph + edge irregularity (OpenCV)"
            ),
        }

    except Exception as e:
        logging.exception("Branch D negative space failed")
        return {
            "confidence": 0.0,
            "void_signature_128d": [0.0] * 128,
            "void_graph": {"nodes": [], "edges": []},
            "edge_irregularity_score": 0.0,
            "void_count": 0,
            "interpretation": f"error: {e}",
        }
