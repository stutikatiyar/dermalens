# backend/app/ml/evaluate_derm.py

import os
import csv
import time
import math
import cv2
import numpy as np
import pandas as pd

from app.ml.enhancement import enhance_image
from app.ml.derm_model import load_model, predict

# ASSUMPTION: app/ml/metrics.py exists and defines these three functions.
# This matches what's currently on GitHub (origin/main). If this module
# doesn't exist yet, either create it with these three functions, or
# fall back to defining calculate_contrast/quality_score locally as in
# the previous version of this file.
from app.ml.metrics import (
    calculate_sharpness,
    calculate_contrast,
    quality_score,
)

from app.evaluation.quality_metrics import (
    calculate_psnr,
    calculate_ssim,
)

# path to weights
WEIGHTS_PATH = "app/ml/models/isic_resnet18.pth"

# load model once
model = load_model(WEIGHTS_PATH)

CSV_OUTPUT_PATH = "reports/evaluation_results.csv"
CATEGORY_CSV_DIR = "reports/by_category"

# NOTE: keep this in sync with the prefixes stripped in
# find_reference_image() below (dark_, blur_, motion_, noise_,
# compressed_, lowres_) so every degradation type actually gets
# bucketed into a category instead of falling through to "original".
CATEGORY_PREFIXES = ["dark", "blur", "motion", "noise", "compressed", "lowres"]


def predict_confidence(image):
    _, confidence = predict(model, image)
    return float(confidence)


def get_category(filename):
    for prefix in CATEGORY_PREFIXES:
        if filename.startswith(prefix + "_"):
            return prefix
    return "original"


def find_reference_image(base_dir, filename):
    """
    Strips known degradation prefixes off `filename` and looks for a
    matching clean image under data/eval/original/, trying a few common
    extensions. Returns (reference_path, reference_image) where
    reference_image is None if nothing was found.
    """
    reference_name = (
        filename
        .replace("dark_", "")
        .replace("blur_", "")
        .replace("motion_", "")
        .replace("noise_", "")
        .replace("compressed_", "")
        .replace("lowres_", "")
    )

    reference_base = os.path.splitext(reference_name)[0]

    reference_folder = os.path.join(
        base_dir,
        "data",
        "eval",
        "original"
    )

    for ext in [".png", ".jpg", ".jpeg"]:
        candidate = os.path.join(reference_folder, reference_base + ext)
        if os.path.exists(candidate):
            reference = cv2.imread(candidate)
            if reference is None:
                print(f"Couldn't load {candidate}")
            return candidate, reference

    return None, None


def evaluate(image_path):
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    full_path = os.path.join(base_dir, image_path)

    img = cv2.imread(full_path)
    if img is None:
        print(f"Skipping {image_path} (not found)")
        return None

    start_time = time.time()

    filename = os.path.basename(image_path)
    category = get_category(filename)

    # ---- BEFORE metrics ----
    sharpness_before = calculate_sharpness(img)
    contrast_before = calculate_contrast(img)
    quality_before = quality_score(sharpness_before, contrast_before)
    cls_o, conf_o = predict(model, img)

    # ---- LOAD ORIGINAL REFERENCE IMAGE (for full-reference PSNR/SSIM) ----
    reference_path, reference = find_reference_image(base_dir, filename)

    # ---- ENHANCEMENT ----
    with open(full_path, "rb") as f:
        image_bytes = f.read()

    # CONFIRMED against enhancement.py: enhance_image returns
    # (original, enhanced, mode) where mode is a string like
    # "Brightness Enhanced + AI Super Resolution" or "No Enhancement".
    _, enhanced, mode = enhance_image(image_bytes)

    # ---- AFTER metrics ----
    sharpness_after = calculate_sharpness(enhanced)
    contrast_after = calculate_contrast(enhanced)
    quality_after = quality_score(sharpness_after, contrast_after)
    cls_e, conf_e = predict(model, enhanced)

    delta = conf_e - conf_o

    # ---- FULL-REFERENCE metrics (PSNR / SSIM) ----
    psnr_val = None
    ssim_val = None
    if reference is not None:
        ref_for_metrics = reference
        enh_for_metrics = enhanced

        if ref_for_metrics.shape != enh_for_metrics.shape:
            ref_for_metrics = cv2.resize(
                ref_for_metrics,
                (enh_for_metrics.shape[1], enh_for_metrics.shape[0])
            )

        psnr_val = calculate_psnr(ref_for_metrics, enh_for_metrics)
        ssim_val = calculate_ssim(ref_for_metrics, enh_for_metrics)

    elapsed = time.time() - start_time

    # ---- PRINT ----
    print("\n---", image_path, f"({category}) ---")
    print(f"Mode       → {mode}")
    print(f"Sharpness  → {round(sharpness_before, 2)} → {round(sharpness_after, 2)}")
    print(f"Contrast   → {round(contrast_before, 2)} → {round(contrast_after, 2)}")
    print(f"Quality    → {quality_before} → {quality_after}")
    print(f"Confidence → {cls_o} ({round(conf_o, 4)}) → {cls_e} ({round(conf_e, 4)})")
    print(f"Delta      → {round(delta, 4)}")
    if psnr_val is not None:
        print(f"PSNR       → {round(psnr_val, 4)}")
        print(f"SSIM       → {round(ssim_val, 4)}")
    else:
        print(f"Reference  → not found at {reference_path}, skipping PSNR/SSIM")
    print(f"Time       → {round(elapsed, 3)}s")

    if delta > 0.02:
        print("✔ Improvement")
    elif delta < -0.02:
        print("⚠ Degradation")
    else:
        print("~ No significant change")

    return {
        "image": image_path,
        "category": category,
        "mode": mode,
        "sharpness_before": round(sharpness_before, 4),
        "sharpness_after": round(sharpness_after, 4),
        "contrast_before": round(contrast_before, 4),
        "contrast_after": round(contrast_after, 4),
        "quality_before": quality_before,
        "quality_after": quality_after,
        "confidence_before": round(conf_o, 4),
        "confidence_after": round(conf_e, 4),
        "delta": round(delta, 4),
        "psnr": round(psnr_val, 4) if psnr_val is not None else "",
        "ssim": round(ssim_val, 4) if ssim_val is not None else "",
        "time_sec": round(elapsed, 4),
    }


def write_csv(rows, output_path):
    if not rows:
        print("No rows to write, skipping CSV.")
        return

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    fieldnames = [
        "image", "category", "mode",
        "sharpness_before", "sharpness_after",
        "contrast_before", "contrast_after",
        "quality_before", "quality_after",
        "confidence_before", "confidence_after",
        "delta",
        "psnr", "ssim",
        "time_sec",
    ]

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print(f"\nCSV written to {output_path}")


def write_category_csvs(rows, output_dir):
    """
    Splits results by category (dark/blur/motion/noise/compressed/lowres/
    original) into separate CSVs, for per-degradation-type analysis --
    useful for the paper's Results section breakdown.
    """
    if not rows:
        print("No rows to write, skipping category CSVs.")
        return

    os.makedirs(output_dir, exist_ok=True)

    df = pd.DataFrame(rows)

    for category in CATEGORY_PREFIXES + ["original"]:
        subset = df[df["category"] == category]
        if subset.empty:
            continue
        out_path = os.path.join(output_dir, f"{category}_results.csv")
        subset.to_csv(out_path, index=False)
        print(f"Saved {out_path} ({len(subset)} rows)")


if __name__ == "__main__":

    images = []

    eval_folder = "data/eval"

    for file in sorted(os.listdir(eval_folder)):
        full_path = os.path.join(eval_folder, file)

        # Skip folders (like original/)
        if os.path.isdir(full_path):
            continue

        # Only process image files
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            images.append(full_path)

    results = []
    deltas = []
    sharpness_gains = []
    quality_gains = []
    improved = 0
    degraded = 0
    unchanged = 0

    for img_path in images:
        result = evaluate(img_path)

        if result is None:
            continue

        results.append(result)
        deltas.append(result["delta"])
        sharpness_gains.append(result["sharpness_after"] - result["sharpness_before"])
        quality_gains.append(result["quality_after"] - result["quality_before"])

        if result["delta"] > 0.02:
            improved += 1
        elif result["delta"] < -0.02:
            degraded += 1
        else:
            unchanged += 1

    write_csv(results, CSV_OUTPUT_PATH)
    write_category_csvs(results, CATEGORY_CSV_DIR)

    # FINAL SUMMARY
    if results:
        psnr_vals = [
            r["psnr"]
            for r in results
            if r["psnr"] != "" and math.isfinite(r["psnr"])
        ]
        ssim_vals = [r["ssim"] for r in results if r["ssim"] != ""]

        print("\n========== FINAL REPORT ==========")
        print("Images Evaluated       :", len(results))
        print("Avg Sharpness Gain (abs):", round(float(np.mean(sharpness_gains)), 4))
        print("Avg Quality Gain (abs)  :", round(float(np.mean(quality_gains)), 4))
        print("Avg Confidence Δ        :", round(float(np.mean(deltas)), 4))
        if psnr_vals:
            print("Average PSNR            :", round(float(np.mean(psnr_vals)), 2), "dB")
        if ssim_vals:
            print("Average SSIM            :", round(float(np.mean(ssim_vals)), 4))
        print("Improved                :", improved)
        print("Degraded                :", degraded)
        print("Unchanged               :", unchanged)
        print("===================================")