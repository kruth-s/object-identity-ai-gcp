import numpy as np
import torch
import timm
import logging

from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import preprocess_image

# -------------------------------------------------------------------
# Force CPU (Cloud Run safe)
# -------------------------------------------------------------------

_DEVICE = torch.device("cpu")

_vit = None
_cam = None


def _load_vit():
    global _vit
    if _vit is None:
        _vit = timm.create_model(
            "vit_base_patch16_224",
            pretrained=True,
        )
        _vit.eval()
        _vit.to(_DEVICE)
    return _vit


def _reshape_transform(tensor, height=14, width=14):
    """
    ViT tokens → [B, C, H, W]
    """
    result = tensor[:, 1:, :]  # drop CLS token
    result = result.reshape(
        result.size(0),
        height,
        width,
        result.size(2),
    )
    result = result.permute(0, 3, 1, 2)
    return result


def _get_cam():
    global _cam
    if _cam is None:
        vit = _load_vit()
        _cam = GradCAM(
            model=vit,
            target_layers=[vit.blocks[-1].norm1],
            reshape_transform=_reshape_transform,
        )
    return _cam


def vit_gradcam_heatmap(rgb_float01: np.ndarray) -> np.ndarray:
    """
    Input: RGB float32 [H,W,3] in [0,1]
    Output: grayscale CAM [H,W] in [0,1]
    """
    try:
        # Resize input for ViT (224x224)
        import torch.nn.functional as F
        
        input_tensor = preprocess_image(
            rgb_float01,
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ).to(_DEVICE)

        # Resize to 224x224 if needed
        if input_tensor.shape[2:] != (224, 224):
            input_tensor = F.interpolate(
                input_tensor,
                size=(224, 224),
                mode="bilinear",
                align_corners=False
            )

        cam = _get_cam()

        # ✅ NEW API — NO target_category
        grayscale_cam = cam(
            input_tensor=input_tensor,
            targets=None,
        )

        return grayscale_cam[0].astype(np.float32)

    except Exception:
        logging.exception("Grad-CAM failed")
        h, w = rgb_float01.shape[:2]
        return np.zeros((h, w), dtype=np.float32)
