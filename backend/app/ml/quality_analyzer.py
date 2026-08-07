import cv2
import numpy as np


def estimate_noise(gray):
    """
    Fast noise estimation (Immerkaer, 1996). Convolves with a kernel
    designed to cancel out smooth/edge structure so what's left is
    mostly sensor noise, then scales by image size. This is independent
    of the Laplacian-variance sharpness metric below -- a blurry image
    and a noisy image will now produce different signals instead of
    both only showing up (or not) as "low sharpness".
    """
    H, W = gray.shape
    kernel = np.array([
        [1, -2, 1],
        [-2, 4, -2],
        [1, -2, 1],
    ], dtype=np.float64)

    conv = cv2.filter2D(gray.astype(np.float64), -1, kernel)
    sigma = np.sum(np.abs(conv))
    sigma = sigma * np.sqrt(0.5 * np.pi) / (6 * (W - 2) * (H - 2))
    return float(sigma)


def analyze_quality(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Sharpness using Laplacian variance
    sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()

    # Brightness
    brightness = np.mean(gray)

    # Contrast
    contrast = gray.std()

    # NEW: noise level -- this was previously missing entirely, which is
    # why noisy images were never routed to DnCNN denoising (there was
    # no signal for the enhancement router to act on).
    noise_level = estimate_noise(gray)

    # Quality score
    quality_score = (
        (sharpness * 0.5) +
        (contrast * 0.3) +
        (brightness * 0.2)
    ) / 10

    return {
        "sharpness": float(sharpness),
        "brightness": float(brightness),
        "contrast": float(contrast),
        "noise_level": noise_level,
        "quality_score": float(quality_score)
    }