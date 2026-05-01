import cv2
import numpy as np

def calculate_sharpness(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return float(cv2.Laplacian(gray, cv2.CV_64F).var())

def calculate_contrast(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return float(gray.std())

# 🔥 NEW: blur detection (same as sharpness, but semantic meaning changes)
def detect_blur(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return float(cv2.Laplacian(gray, cv2.CV_64F).var())

# 🔥 NEW: quality score
def quality_score(sharpness, contrast):
    # normalize values into reasonable range
    sharp_norm = min(sharpness / 500, 1.0)
    contrast_norm = min(contrast / 100, 1.0)

    score = (0.7 * sharp_norm) + (0.3 * contrast_norm)

    return float(score * 100)  # scale to 0–100