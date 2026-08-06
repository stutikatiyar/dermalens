import cv2

from skimage.metrics import (
    peak_signal_noise_ratio,
    structural_similarity
)


def calculate_psnr(original, enhanced):

    return float(
        peak_signal_noise_ratio(
            original,
            enhanced,
            data_range=255
        )
    )


def calculate_ssim(original, enhanced):

    gray_original = cv2.cvtColor(
        original,
        cv2.COLOR_BGR2GRAY
    )

    gray_enhanced = cv2.cvtColor(
        enhanced,
        cv2.COLOR_BGR2GRAY
    )

    score = structural_similarity(
        gray_original,
        gray_enhanced
    )

    return float(score)