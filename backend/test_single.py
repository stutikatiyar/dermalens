"""
Quick standalone sanity check -- run this instead of the full
evaluate_derm.py while testing the noise/Restormer changes.
Only processes ONE image, so it won't take anywhere near 2 hours.

Usage (from your backend/ folder):
    python test_single.py data/eval/noise_ISIC_0032673.jpg
    python test_single.py data/eval/ISIC_0029306.jpg   # a clean/original one for comparison
"""

import sys
import time
import cv2
from app.ml.enhancement import enhance_image

if len(sys.argv) < 2:
    print("Usage: python test_single.py <path_to_image>")
    sys.exit(1)

image_path = sys.argv[1]

with open(image_path, "rb") as f:
    image_bytes = f.read()

print(f"Running enhance_image() on {image_path} ...")
start = time.time()

original, enhanced, mode = enhance_image(image_bytes)

elapsed = time.time() - start
print(f"\nDone in {elapsed:.1f}s")
print(f"Mode selected: {mode}")

# Save both images side by side so you can visually check colors
out_path = "test_single_output.jpg"
comparison = cv2.hconcat([
    cv2.resize(original, (400, 400)),
    cv2.resize(enhanced, (400, 400)),
])
cv2.imwrite(out_path, comparison)
print(f"Saved comparison image (original | enhanced) to {out_path}")
print("Open that file and check: does the enhanced side look like natural")
print("skin tones, or does it look bluish/greenish/color-swapped?")