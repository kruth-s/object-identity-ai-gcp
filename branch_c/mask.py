import numpy as np
import cv2
import mediapipe as mp
import logging

mp_selfie = mp.solutions.selfie_segmentation

# Reusable segmentation model
_SELFIE = mp_selfie.SelfieSegmentation(model_selection=1)


def generate_object_mask_bytes(image_bytes: bytes) -> bytes:
    """
    Returns a PNG mask (white=edit area, black=keep area).
    """
    try:
        bgr = cv2.imdecode(
            np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR
        )
        if bgr is None:
            raise ValueError("Invalid image for mask")

        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        res = _SELFIE.process(rgb)

        if res.segmentation_mask is None:
            raise RuntimeError("Segmentation failed")

        mask = (res.segmentation_mask > 0.5).astype(np.uint8) * 255
        inv = 255 - mask
        inv = cv2.GaussianBlur(inv, (9, 9), 0)

        ok, png = cv2.imencode(".png", inv)
        if not ok:
            raise RuntimeError("Mask encode failed")
        return png.tobytes()

    except Exception as e:
        logging.exception("Mask generation failed")
        raise
