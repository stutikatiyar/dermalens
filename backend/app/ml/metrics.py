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
    return float((0.7 * sharpness) + (0.3 * contrast))