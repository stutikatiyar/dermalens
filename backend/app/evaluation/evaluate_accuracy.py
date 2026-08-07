# evaluate_accuracy.py
import os, csv, cv2, pandas as pd
from app.ml.derm_model import load_model, predict
from app.ml.enhancement import enhance_image

WEIGHTS_PATH = "app/ml/models/isic_resnet18.pth"
LABELS_CSV = "data/eval/labels.csv"
IMAGE_FOLDER = "data/eval"
OUTPUT_CSV = "reports/accuracy_results.csv"

CLASS_NAMES = ["akiec", "bcc", "bkl", "df", "melanoma", "nevus", "vasc"]
LABEL_MAPPING = {"mel": "melanoma", "nv": "nevus", "akiec": "akiec", "bcc": "bcc", "bkl": "bkl", "df": "df", "vasc": "vasc"}

CATEGORY_PREFIXES = ["dark", "blur", "motion", "noise", "compressed", "lowres"]

FIELDNAMES = [
    "image", "category", "true_label",
    "prediction_before", "prediction_after",
    "confidence_before", "confidence_after",
    "correct_before", "correct_after",
    "mode",
]

model = load_model(WEIGHTS_PATH)

df = pd.read_csv(LABELS_CSV)
df["label"] = df["label"].map(lambda x: LABEL_MAPPING.get(str(x), str(x)))
GROUND_TRUTH = dict(zip(df["image_id"].astype(str), df["label"]))


def image_id_from_name(filename):
    name = os.path.splitext(filename)[0]
    for p in ["dark_", "blur_", "motion_", "noise_", "compressed_", "lowres_"]:
        name = name.replace(p, "")
    return name


def get_category(filename):
    for prefix in CATEGORY_PREFIXES:
        if filename.startswith(prefix + "_"):
            return prefix
    return "original"


def load_already_processed(output_csv):
    """
    Resume support: if OUTPUT_CSV already has rows from a previous
    (possibly crashed) run, skip those filenames instead of redoing them.
    Returns a set of already-processed original filenames.
    """
    processed = set()
    if os.path.exists(output_csv):
        try:
            existing = pd.read_csv(output_csv)
            if "filename" in existing.columns:
                processed = set(existing["filename"].astype(str))
        except Exception as e:
            print(f"⚠ Couldn't read existing CSV for resume, starting fresh: {e}")
    return processed


os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

already_processed = load_already_processed(OUTPUT_CSV)
if already_processed:
    print(f"Resuming — {len(already_processed)} images already processed, will skip those.")

file_exists_with_header = os.path.exists(OUTPUT_CSV) and len(already_processed) > 0

# Open in append mode if resuming, otherwise fresh write with header.
csv_mode = "a" if file_exists_with_header else "w"
csv_file = open(OUTPUT_CSV, csv_mode, newline="")
writer = csv.DictWriter(csv_file, fieldnames=["filename"] + FIELDNAMES)
if csv_mode == "w":
    writer.writeheader()
    csv_file.flush()

total = 0
cb_total = 0
ca_total = 0
skipped_errors = 0

# Per-category running totals for the breakdown table
category_stats = {}  # category -> {"total": n, "correct_before": n, "correct_after": n}

try:
    for file in sorted(os.listdir(IMAGE_FOLDER)):
        if not file.lower().endswith((".png", ".jpg", ".jpeg")):
            continue

        if file in already_processed:
            continue

        full_path = os.path.join(IMAGE_FOLDER, file)

        try:
            img = cv2.imread(full_path)
            if img is None:
                print(f"⚠ Skipping {file} (couldn't read image)")
                continue

            image_id = image_id_from_name(file)
            true_label = GROUND_TRUTH.get(image_id)
            if true_label is None:
                continue

            category = get_category(file)

            idx_b, conf_b = predict(model, img)
            pred_b = CLASS_NAMES[idx_b]

            with open(full_path, "rb") as f:
                _, enhanced, mode = enhance_image(f.read())

            idx_a, conf_a = predict(model, enhanced)
            pred_a = CLASS_NAMES[idx_a]

            correct_b = pred_b == true_label
            correct_a = pred_a == true_label

            cb_total += int(correct_b)
            ca_total += int(correct_a)
            total += 1

            cat = category_stats.setdefault(category, {"total": 0, "correct_before": 0, "correct_after": 0})
            cat["total"] += 1
            cat["correct_before"] += int(correct_b)
            cat["correct_after"] += int(correct_a)

            row = {
                "filename": file,
                "image": image_id,
                "category": category,
                "true_label": true_label,
                "prediction_before": pred_b,
                "prediction_after": pred_a,
                "confidence_before": round(conf_b, 4),
                "confidence_after": round(conf_a, 4),
                "correct_before": correct_b,
                "correct_after": correct_a,
                "mode": mode,
            }

            writer.writerow(row)
            csv_file.flush()   # persist immediately — survives crash/disconnect

            status = "✔" if (correct_b or correct_a) else "✘"
            print(f"{status} {file} ({category}) — {pred_b}→{pred_a} | true={true_label} | before={correct_b} after={correct_a}")

        except cv2.error as e:
            print(f"⚠ OpenCV error on {file}, skipping: {e}")
            skipped_errors += 1
            continue
        except Exception as e:
            print(f"⚠ Unexpected error on {file}, skipping: {e}")
            skipped_errors += 1
            continue

except KeyboardInterrupt:
    print("\nInterrupted by user — partial results already saved to CSV.")

finally:
    csv_file.close()

print("=" * 50)
print("Images Evaluated (this run):", total)
print("Images Skipped (errors)    :", skipped_errors)
if total:
    b = cb_total / total * 100
    a = ca_total / total * 100
    print(f"Accuracy Before : {b:.2f}%")
    print(f"Accuracy After  : {a:.2f}%")
    print(f"Improvement     : {a - b:.2f}%")

print("\n--- Per-Category Breakdown (this run) ---")
for cat, stats in sorted(category_stats.items()):
    n = stats["total"]
    if n == 0:
        continue
    cb_pct = stats["correct_before"] / n * 100
    ca_pct = stats["correct_after"] / n * 100
    print(f"{cat:12s} n={n:4d}  before={cb_pct:6.2f}%  after={ca_pct:6.2f}%  Δ={ca_pct - cb_pct:+.2f}")

print("\nCSV:", OUTPUT_CSV)
print("(Run this script again to resume — it will skip already-processed images.)")