"""
Checks whether Restormer actually reduced measured noise, not just
whether it ran without crashing. Run from backend/ folder:
    python check_denoise_effect.py data/eval/noise_ISIC_0029306.png
"""
import sys
import cv2
from app.ml.enhancement import enhance_image
from app.ml.quality_analyzer import estimate_noise

image_path = sys.argv[1]

with open(image_path, "rb") as f:
    image_bytes = f.read()

original, enhanced, mode = enhance_image(image_bytes)

gray_before = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
gray_after = cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY)

noise_before = estimate_noise(gray_before)
noise_after = estimate_noise(gray_after)

print(f"\nMode: {mode}")
print(f"noise_level BEFORE enhancement: {noise_before:.3f}")
print(f"noise_level AFTER  enhancement: {noise_after:.3f}")

if noise_after < noise_before * 0.5:
    print("-> Strong noise reduction")
elif noise_after < noise_before:
    print("-> Some noise reduction, but modest")
else:
    print("-> WARNING: noise did not decrease (or got worse) after enhancement")