import os
import logging

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
IMAGEN_LOCATION = os.environ.get("IMAGEN_LOCATION", "us-central1")
IMAGEN_MODEL = os.environ.get("IMAGEN_MODEL", "imagegeneration@002")

_vertex_initialized = False
_imagen_model = None


def _init_vertex():
    global _vertex_initialized
    if not _vertex_initialized:
        import vertexai
        vertexai.init(project=PROJECT_ID, location=IMAGEN_LOCATION)
        _vertex_initialized = True


def _get_imagen_model():
    global _imagen_model
    if _imagen_model is None:
        from vertexai.preview.vision_models import ImageGenerationModel
        _imagen_model = ImageGenerationModel.from_pretrained(IMAGEN_MODEL)
    return _imagen_model


def imagen_inpaint_completions(
    base_jpg_bytes: bytes,
    mask_png_bytes: bytes,
    prompt: str,
    n: int = 5,
):
    """
    Returns a list of Vertex Image objects (completions).
    """
    try:
        _init_vertex()
        model = _get_imagen_model()

        from vertexai.preview.vision_models import Image

        base_img = Image(image_bytes=base_jpg_bytes)
        mask_img = Image(image_bytes=mask_png_bytes)

        images = model.edit_image(
            base_image=base_img,
            mask=mask_img,
            prompt=prompt,
            guidance_scale=21,
            number_of_images=n,
            seed=1,
        )
        return images

    except Exception as e:
        logging.exception("Imagen inpainting failed")
        return []
