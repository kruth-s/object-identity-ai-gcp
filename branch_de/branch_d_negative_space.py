from branch_de.segmentation import segment_foreground_mask
from branch_de.negative_space_signature import (
    edge_irregularity_score,
    find_void_regions,
    negative_space_signature_128,
)
from branch_de.void_graph import build_void_graph

def run_branch_d_negative_space(norm_jpg_bytes: bytes) -> dict:
    fg_mask = segment_foreground_mask(norm_jpg_bytes)
    edge_irreg = edge_irregularity_score(fg_mask)
    voids, void_mask = find_void_regions(fg_mask)

    sig128 = negative_space_signature_128(voids, edge_irreg)
    graph = build_void_graph(voids)

    # confidence: fewer voids but stable edge irregularity => higher
    conf = 1.0 / (1.0 + 0.08 * edge_irreg + 0.03 * len(voids))

    return {
        "confidence": round(float(max(0.0, min(1.0, conf))), 3),
        "void_signature_128d": sig128,
        "void_graph": graph,
        "edge_irregularity_score": round(float(edge_irreg), 3),
        "void_count": len(voids),
        "interpretation": "Negative space signature + void graph + edge irregularity (OpenCV)",
    }
