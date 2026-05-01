import os
import cv2

from app.ml.enhancement import enhance_image
from app.ml.derm_model import load_model, predict

# path to weights
WEIGHTS_PATH = "app/ml/models/isic_resnet18.pth"

# load model once
model = load_model(WEIGHTS_PATH)


def evaluate(image_path):
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    full_path = os.path.join(base_dir, image_path)

    img = cv2.imread(full_path)
    if img is None:
        raise ValueError(f"Image not found: {full_path}")

    # original
    cls_o, conf_o = predict(model, img)

    # enhanced
    with open(full_path, "rb") as f:
        image_bytes = f.read()

    _, enhanced, _ = enhance_image(image_bytes)
    cls_e, conf_e = predict(model, enhanced)

    delta = conf_e - conf_o

    print("\n---", image_path, "---")
    print(f"Original   → class: {cls_o}, conf: {round(conf_o, 4)}")
    print(f"Enhanced   → class: {cls_e}, conf: {round(conf_e, 4)}")
    print(f"Delta      → {round(delta, 4)}")

    if delta > 0.02:
        print("✔ Improvement")
    elif delta < -0.02:
        print("⚠ Degradation")
    else:
        print("~ No significant change")


if __name__ == "__main__":
    images = [
        "sample.jpg",
        "data/img1.jpg",
        "data/img2.jpg"
    ]

    for img_path in images:
        evaluate(img_path)