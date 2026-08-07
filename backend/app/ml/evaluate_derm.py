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

from app.ml.metrics import (
    calculate_sharpness,
    calculate_contrast,
    quality_score,
)

from app.evaluation.quality_metrics import (
    calculate_psnr,
    calculate_ssim,
)

WEIGHTS_PATH = "app/ml/models/isic_resnet18.pth"
model = load_model(WEIGHTS_PATH)

CSV_OUTPUT_PATH = "reports/evaluation_results.csv"
CATEGORY_CSV_DIR = "reports/by_category"

CATEGORY_PREFIXES = ["dark", "blur", "motion", "noise", "compressed", "lowres"]

# ---------------------------------------------------------------------------
# NEW: verified against train_derm.py — this is the exact order
# torchvision.datasets.ImageFolder assigned class indices in, confirmed by
# running sorted(os.listdir("data/train")) against the real training data.
# derm_model.predict() returns an int index into THIS list — do not
# reorder it or re-derive it by guessing (e.g. standard ISIC abbreviations
# "mel"/"nv" do NOT match this project's actual folder names).
# ---------------------------------------------------------------------------
CLASS_NAMES = ["akiec", "bcc", "bkl", "df", "melanoma", "nevus", "vasc"]

# ---------------------------------------------------------------------------
# NEW: ground-truth labels for accuracy (Table II).
# Expects a CSV at data/eval/labels.csv with columns: image_id,label
# where image_id matches the reference filename stem (e.g. "ISIC_0030875")
# and label matches whatever classes derm_model.predict() returns
# (e.g. "melanoma", "nevus", ...). This is the standard HAM10000/ISIC
# metadata format (GroundTruth.csv), just renamed/trimmed to two columns.
# If this file doesn't exist, accuracy is skipped and everything else
# still runs unchanged.
# ---------------------------------------------------------------------------
LABELS_PATH = "data/eval/labels.csv"


def load_labels(base_dir):
    full_path = os.path.join(base_dir, LABELS_PATH)
    if not os.path.exists(full_path):
        print(f"[warn] {LABELS_PATH} not found — accuracy metrics will be skipped.")
        return {}
    df = pd.read_csv(full_path)
    return dict(zip(df["image_id"].astype(str), df["label"].astype(str)))


def predict_confidence(image):
    _, confidence = predict(model, image)
    return float(confidence)


def get_category(filename):
    for prefix in CATEGORY_PREFIXES:
        if filename.startswith(prefix + "_"):
            return prefix
    return "original"


def find_reference_image(base_dir, filename):
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

    reference_folder = os.path.join(base_dir, "data", "eval", "original")

    for ext in [".png", ".jpg", ".jpeg"]:
        candidate = os.path.join(reference_folder, reference_base + ext)
        if os.path.exists(candidate):
            reference = cv2.imread(candidate)
            if reference is None:
                print(f"Couldn't load {candidate}")
            return candidate, reference, reference_base

    return None, None, reference_base


def evaluate(image_path, labels):
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
    reference_path, reference, reference_base = find_reference_image(base_dir, filename)

    # ---- ENHANCEMENT ----
    with open(full_path, "rb") as f:
        image_bytes = f.read()

    _, enhanced, mode = enhance_image(image_bytes)

    # ---- AFTER metrics ----
    sharpness_after = calculate_sharpness(enhanced)
    contrast_after = calculate_contrast(enhanced)
    quality_after = quality_score(sharpness_after, contrast_after)
    cls_e, conf_e = predict(model, enhanced)

    delta = conf_e - conf_o

    # ---- FULL-REFERENCE metrics (PSNR / SSIM) ----
    # NEW: compute BEFORE (degraded vs. reference) as well as AFTER
    # (enhanced vs. reference), so Table I has a real before/after pair
    # instead of only an "after" value.
    psnr_before = ssim_before = None
    psnr_after = ssim_after = None

    if reference is not None:
        ref_for_img = reference
        img_for_metrics = img
        if ref_for_img.shape != img_for_metrics.shape:
            ref_for_img = cv2.resize(ref_for_img, (img_for_metrics.shape[1], img_for_metrics.shape[0]))
        psnr_before = calculate_psnr(ref_for_img, img_for_metrics)
        ssim_before = calculate_ssim(ref_for_img, img_for_metrics)

        ref_for_enh = reference
        enh_for_metrics = enhanced
        if ref_for_enh.shape != enh_for_metrics.shape:
            ref_for_enh = cv2.resize(ref_for_enh, (enh_for_metrics.shape[1], enh_for_metrics.shape[0]))
        psnr_after = calculate_psnr(ref_for_enh, enh_for_metrics)
        ssim_after = calculate_ssim(ref_for_enh, enh_for_metrics)

    # ---- NEW: accuracy (needs ground-truth label) ----
    # cls_o / cls_e are integer class indices from predict(); map them to
    # label strings via CLASS_NAMES before comparing to true_label, which
    # is expected to be a string matching one of CLASS_NAMES.
    pred_label_o = CLASS_NAMES[cls_o] if 0 <= cls_o < len(CLASS_NAMES) else None
    pred_label_e = CLASS_NAMES[cls_e] if 0 <= cls_e < len(CLASS_NAMES) else None

    true_label = labels.get(reference_base)
    correct_before = correct_after = None
    if true_label is not None and pred_label_o is not None and pred_label_e is not None:
        correct_before = int(pred_label_o == true_label)
        correct_after = int(pred_label_e == true_label)

    elapsed = time.time() - start_time

    print("\n---", image_path, f"({category}) ---")
    print(f"Mode       → {mode}")
    print(f"Sharpness  → {round(sharpness_before, 2)} → {round(sharpness_after, 2)}")
    print(f"Contrast   → {round(contrast_before, 2)} → {round(contrast_after, 2)}")
    print(f"Quality    → {quality_before} → {quality_after}")
    print(f"Confidence → {pred_label_o} ({round(conf_o, 4)}) → {pred_label_e} ({round(conf_e, 4)})")
    print(f"Delta      → {round(delta, 4)}")
    if psnr_after is not None:
        print(f"PSNR       → {round(psnr_before, 4)} → {round(psnr_after, 4)}")
        print(f"SSIM       → {round(ssim_before, 4)} → {round(ssim_after, 4)}")
    else:
        print(f"Reference  → not found at {reference_path}, skipping PSNR/SSIM")
    if true_label is not None:
        print(f"Label      → {true_label} | correct before={bool(correct_before)} after={bool(correct_after)}")
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
        "psnr_before": round(psnr_before, 4) if psnr_before is not None else "",
        "psnr_after": round(psnr_after, 4) if psnr_after is not None else "",
        "ssim_before": round(ssim_before, 4) if ssim_before is not None else "",
        "ssim_after": round(ssim_after, 4) if ssim_after is not None else "",
        "pred_label_before": pred_label_o if pred_label_o is not None else "",
        "pred_label_after": pred_label_e if pred_label_e is not None else "",
        "true_label": true_label if true_label is not None else "",
        "correct_before": correct_before if correct_before is not None else "",
        "correct_after": correct_after if correct_after is not None else "",
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
        "psnr_before", "psnr_after",
        "ssim_before", "ssim_after",
        "pred_label_before", "pred_label_after",
        "true_label", "correct_before", "correct_after",
        "time_sec",
    ]

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print(f"\nCSV written to {output_path}")


def write_category_csvs(rows, output_dir):
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

    base_dir_main = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    labels = load_labels(base_dir_main)

    images = []
    eval_folder = "data/eval"

    for file in sorted(os.listdir(eval_folder)):
        full_path = os.path.join(eval_folder, file)
        if os.path.isdir(full_path):
            continue
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
        result = evaluate(img_path, labels)

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

    if results:
        psnr_before_vals = [r["psnr_before"] for r in results if r["psnr_before"] != "" and math.isfinite(r["psnr_before"])]
        psnr_after_vals = [r["psnr_after"] for r in results if r["psnr_after"] != "" and math.isfinite(r["psnr_after"])]
        ssim_before_vals = [r["ssim_before"] for r in results if r["ssim_before"] != ""]
        ssim_after_vals = [r["ssim_after"] for r in results if r["ssim_after"] != ""]

        # NEW: accuracy summary for Table II
        acc_before_vals = [r["correct_before"] for r in results if r["correct_before"] != ""]
        acc_after_vals = [r["correct_after"] for r in results if r["correct_after"] != ""]

        print("\n========== FINAL REPORT ==========")
        print("Images Evaluated       :", len(results))
        print("Avg Sharpness Gain (abs):", round(float(np.mean(sharpness_gains)), 4))
        print("Avg Quality Gain (abs)  :", round(float(np.mean(quality_gains)), 4))
        print("Avg Confidence Δ        :", round(float(np.mean(deltas)), 4))
        if psnr_before_vals and psnr_after_vals:
            print("Average PSNR (before)   :", round(float(np.mean(psnr_before_vals)), 2), "dB")
            print("Average PSNR (after)    :", round(float(np.mean(psnr_after_vals)), 2), "dB")
        if ssim_before_vals and ssim_after_vals:
            print("Average SSIM (before)   :", round(float(np.mean(ssim_before_vals)), 4))
            print("Average SSIM (after)    :", round(float(np.mean(ssim_after_vals)), 4))
        if acc_before_vals and acc_after_vals:
            print("Accuracy (before) %     :", round(100 * float(np.mean(acc_before_vals)), 2))
            print("Accuracy (after) %      :", round(100 * float(np.mean(acc_after_vals)), 2))
        else:
            print("Accuracy                : skipped (no data/eval/labels.csv found)")
        print("Improved                :", improved)
        print("Degraded                :", degraded)
        print("Unchanged               :", unchanged)
        print("===================================")