import numpy as np
import torch
import timm

# pip: pytorch-grad-cam
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import preprocess_image

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load once at startup (same as your manufacturing ViT, but here we use it for explainability)
_vit = timm.create_model("vit_base_patch16_224", pretrained=True)
_vit.eval()
_vit.to(device)

def _reshape_transform(tensor, height=14, width=14):
    """
    ViT tokens -> feature map:
    tensor: [B, tokens, C]
    drop CLS token then reshape to [B, C, H, W]
    """
    result = tensor[:, 1:, :].reshape(tensor.size(0), height, width, tensor.size(2))
    result = result.transpose(2, 3).transpose(1, 2)  # [B, C, H, W]
    return result

def vit_gradcam_heatmap(rgb_float01: np.ndarray, target_category: int | None = None) -> np.ndarray:
    """
    Input: rgb image float32 in [0,1], shape [H,W,3]
    Output: grayscale_cam float32 in [0,1], shape [H,W]
    """
    input_tensor = preprocess_image(
        rgb_float01,
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225],
    ).to(device)

    target_layers = [_vit.blocks[-1].norm1]

    cam = GradCAM(
        model=_vit,
        target_layers=target_layers,
        reshape_transform=_reshape_transform,
    )

    grayscale_cam = cam(input_tensor=input_tensor, target_category=target_category)
    return grayscale_cam[0].astype(np.float32)
