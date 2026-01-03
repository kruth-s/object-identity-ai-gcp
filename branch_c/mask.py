import numpy as np
import cv2
import mediapipe as mp

mp_selfie = mp.solutions.selfie_segmentation

def generate_object_mask_bytes(image_bytes: bytes) -> bytes:
    """
    Returns a PNG mask (white=edit area, black=keep area).
    Inpainting needs a mask; this produces a usable one for demos.
    """
    bgr = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    if bgr is None:
        raise ValueError("Invalid image for mask")

    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

    with mp_selfie.SelfieSegmentation(model_selection=1) as seg:
        res = seg.process(rgb)

    # res.segmentation_mask is float [0..1]
    mask = (res.segmentation_mask > 0.5).astype(np.uint8) * 255

    # Invert mask: we want to edit the occluded/background area around subject/object
    # For object completion, edit the "missing/occluded" region:
    inv = 255 - mask

    # Smooth edges
    inv = cv2.GaussianBlur(inv, (9, 9), 0)

    ok, png = cv2.imencode(".png", inv)
    if not ok:
        raise RuntimeError("Mask encode failed")
    return png.tobytes()
