import threading

import cv2
import lpips
import numpy as np
import torch

from .quality_metrics import calculate_psnr, calculate_ssim


_LPIPS_MODEL = None
_LPIPS_LOCK = threading.Lock()


def resize_to_reference(reference, image):
    """Resize a comparison image to the reference dimensions deterministically."""
    if reference.shape[:2] == image.shape[:2]:
        return image

    return cv2.resize(
        image,
        (reference.shape[1], reference.shape[0]),
        interpolation=cv2.INTER_AREA,
    )


def _get_lpips_model():
    global _LPIPS_MODEL

    if _LPIPS_MODEL is None:
        with _LPIPS_LOCK:
            if _LPIPS_MODEL is None:
                device = "cuda" if torch.cuda.is_available() else "cpu"
                model = lpips.LPIPS(net="alex", version="0.1")
                _LPIPS_MODEL = model.to(device).eval()

    return _LPIPS_MODEL


def _to_lpips_tensor(image):
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    tensor = torch.from_numpy(rgb.transpose(2, 0, 1)).float() / 127.5 - 1.0
    return tensor.unsqueeze(0)


def calculate_lpips(reference, comparison):
    if reference.shape != comparison.shape:
        raise ValueError("LPIPS inputs must have identical dimensions")

    model = _get_lpips_model()
    device = next(model.parameters()).device

    with torch.no_grad():
        value = model(
            _to_lpips_tensor(reference).to(device),
            _to_lpips_tensor(comparison).to(device),
        )

    return float(value.item())


def evaluate_reference_pair(reference, comparison):
    aligned = resize_to_reference(reference, comparison)

    return {
        "psnr": calculate_psnr(reference, aligned),
        "ssim": calculate_ssim(reference, aligned),
        "lpips": calculate_lpips(reference, aligned),
    }