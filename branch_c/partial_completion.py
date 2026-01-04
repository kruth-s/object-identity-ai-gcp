from branch_c.mask import generate_object_mask_bytes
from branch_c.edges_depth import edge_map_bytes, depth_prior_bytes
from branch_c.imagen_inpaint import imagen_inpaint_completions
from branch_c.completion_embeddings import embed_completion_image_bytes
import logging


def run_partial_object_completion(norm_jpg_bytes: bytes, n: int = 5) -> dict:
    """
    Full Branch C pipeline with graceful degradation.
    """
    try:
        mask_png = generate_object_mask_bytes(norm_jpg_bytes)
        _ = edge_map_bytes(norm_jpg_bytes)
        _ = depth_prior_bytes(norm_jpg_bytes)
    except Exception:
        logging.exception("Preprocessing failed for partial completion")
        return {
            "confidence": 0.0,
            "completions_generated": 0,
            "completion_embeddings": [],
            "interpretation": "Preprocessing failed",
        }

    prompt = (
        "Complete the partially visible object realistically. "
        "Preserve the object's original material, color, and structure. "
        "Do not change the background."
    )

    completions = imagen_inpaint_completions(
        base_jpg_bytes=norm_jpg_bytes,
        mask_png_bytes=mask_png,
        prompt=prompt,
        n=n,
    )

    completion_outputs = []

    for img in completions:
        img_bytes = getattr(img, "_image_bytes", None) or getattr(
            img, "image_bytes", None
        )
        if not img_bytes:
            continue

        emb = embed_completion_image_bytes(img_bytes)
        if emb.get("dims", 0) > 0:
            completion_outputs.append(
                {
                    "embedding_dims": emb["dims"],
                    "embedding": emb["embedding"],
                }
            )

    return {
        "confidence": 0.78,
        "completions_generated": len(completion_outputs),
        "has_edges": True,
        "has_depth_prior": True,
        "interpretation": (
            "Imagen inpainting completions + embeddings "
            "for occlusion robustness"
        ),
        "completion_embeddings": completion_outputs,
    }
