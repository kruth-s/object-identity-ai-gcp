from branch_c.mask import generate_object_mask_bytes
from branch_c.edges_depth import edge_map_bytes, depth_prior_bytes
from branch_c.imagen_inpaint import imagen_inpaint_completions
from branch_c.completion_embeddings import embed_completion_image_bytes

def run_partial_object_completion(norm_jpg_bytes: bytes, n: int = 5) -> dict:
    """
    Full Branch C:
    - mask generation
    - edge map + depth prior
    - Imagen inpainting completions
    - embedding extraction per completion
    """
    mask_png = generate_object_mask_bytes(norm_jpg_bytes)
    edges_png = edge_map_bytes(norm_jpg_bytes)
    depth_png = depth_prior_bytes(norm_jpg_bytes)

    # prompt guided by your slide’s intent (occlusion robustness)
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
        # Vertex Image object exposes bytes as private sometimes; robust access:
        img_bytes = getattr(img, "_image_bytes", None) or getattr(img, "image_bytes", None)
        if img_bytes is None:
            # fallback: save() not used in Cloud Run; skip
            continue
        emb = embed_completion_image_bytes(img_bytes)
        completion_outputs.append({
            "embedding_dims": emb["dims"],
            "embedding": emb["embedding"],
        })

    return {
        "confidence": 0.78,  # Branch confidence (you can calibrate later)
        "completions_generated": len(completion_outputs),
        "has_edges": True,
        "has_depth_prior": True,
        "interpretation": "Imagen inpainting completions + embeddings for occlusion robustness",
        "completion_embeddings": completion_outputs,
    }
