import os
import uuid
import vertexai
from vertexai.preview.vision_models import Image, ImageGenerationModel

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("IMAGEN_LOCATION", "us-central1")  # Imagen often available in us-central1
IMAGEN_MODEL = os.environ.get("IMAGEN_MODEL", "imagegeneration@002")  # Imagen v.002 editing sample [web:97]

vertexai.init(project=PROJECT_ID, location=LOCATION)

_model = ImageGenerationModel.from_pretrained(IMAGEN_MODEL)

def _to_vx_image(image_bytes: bytes) -> Image:
    return Image(image_bytes=image_bytes)

def imagen_inpaint_completions(
    base_jpg_bytes: bytes,
    mask_png_bytes: bytes,
    prompt: str,
    n: int = 5,
):
    """
    Returns a list of Vertex Image objects (completions).
    """
    base_img = _to_vx_image(base_jpg_bytes)
    mask_img = _to_vx_image(mask_png_bytes)

    images = _model.edit_image(
        base_image=base_img,
        mask=mask_img,
        prompt=prompt,
        guidance_scale=21,      # strong prompt adherence [web:97]
        number_of_images=n,
        seed=1,
    )
    return images
