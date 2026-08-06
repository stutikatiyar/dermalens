import os
import cv2
import numpy as np


# ==============================
# INPUT / OUTPUT
# ==============================

INPUT_FOLDER = "data/eval/original"
OUTPUT_FOLDER = "data/eval"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ==============================
# DARK IMAGE
# ==============================

def make_dark(img, brightness=0.35):
    dark = np.clip(img.astype(np.float32) * brightness, 0, 255)
    return dark.astype(np.uint8)


# ==============================
# GAUSSIAN NOISE
# ==============================

def make_noise(img, sigma=25):

    noise = np.random.normal(
        0,
        sigma,
        img.shape
    )

    noisy = img.astype(np.float32) + noise

    noisy = np.clip(
        noisy,
        0,
        255
    )

    return noisy.astype(np.uint8)


# ==============================
# GAUSSIAN BLUR
# ==============================

def make_blur(img):

    return cv2.GaussianBlur(
        img,
        (11, 11),
        0
    )


# ==============================
# MOTION BLUR
# ==============================

def make_motion_blur(img, size=21):

    kernel = np.zeros((size, size))

    kernel[int((size - 1) / 2), :] = np.ones(size)

    kernel = kernel / size

    motion = cv2.filter2D(
        img,
        -1,
        kernel
    )

    return motion


# ==============================
# LOW RESOLUTION
# ==============================

def make_low_resolution(img, scale=0.35):

    h, w = img.shape[:2]

    small = cv2.resize(
        img,
        (
            int(w * scale),
            int(h * scale)
        ),
        interpolation=cv2.INTER_AREA
    )

    restored = cv2.resize(
        small,
        (w, h),
        interpolation=cv2.INTER_LINEAR
    )

    return restored


# ==============================
# JPEG COMPRESSION
# ==============================

def make_compression(img, quality=20):

    encode_param = [
        int(cv2.IMWRITE_JPEG_QUALITY),
        quality
    ]

    _, enc = cv2.imencode(
        ".jpg",
        img,
        encode_param
    )

    dec = cv2.imdecode(
        enc,
        cv2.IMREAD_COLOR
    )

    return dec


# ==============================
# PROCESS DATASET
# ==============================

images = [
    f for f in os.listdir(INPUT_FOLDER)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
]

for filename in images:

    path = os.path.join(
        INPUT_FOLDER,
        filename
    )

    img = cv2.imread(path)

    if img is None:
        continue

    name, ext = os.path.splitext(filename)

    # Save original copy
    cv2.imwrite(
        os.path.join(
            OUTPUT_FOLDER,
            filename
        ),
        img
    )

    cv2.imwrite(
        os.path.join(
            OUTPUT_FOLDER,
            f"dark_{name}.png"
        ),
        make_dark(img)
    )

    cv2.imwrite(
        os.path.join(
            OUTPUT_FOLDER,
            f"noise_{name}.png"
        ),
        make_noise(img)
    )

    cv2.imwrite(
        os.path.join(
            OUTPUT_FOLDER,
            f"blur_{name}.png"
        ),
        make_blur(img)
    )

    cv2.imwrite(
        os.path.join(
            OUTPUT_FOLDER,
            f"motion_{name}.png"
        ),
        make_motion_blur(img)
    )

    cv2.imwrite(
        os.path.join(
            OUTPUT_FOLDER,
            f"lowres_{name}.png"
        ),
        make_low_resolution(img)
    )

    cv2.imwrite(
        os.path.join(
            OUTPUT_FOLDER,
            f"compressed_{name}.jpg"
        ),
        make_compression(img)
    )

    print(f"Processed {filename}")

print("\nDone!")