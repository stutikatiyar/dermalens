from app.ml.superres_enhancer import enhance_superres
from app.ml.restormer.restormer_enhancer import enhance_restormer
from app.ml.quality_analyzer import estimate_noise  # added to quality_analyzer.py earlier
import cv2
import numpy as np


def fix_brightness_lab(img, gamma=0.70):

    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    l, a, b = cv2.split(lab)

    l_norm = l / 255.0

    l_gamma = np.power(l_norm, gamma)

    l_out = np.clip(
        l_gamma * 255,
        0,
        255
    ).astype(np.uint8)

    lab = cv2.merge((l_out, a, b))

    return cv2.cvtColor(
        lab,
        cv2.COLOR_LAB2BGR
    )


def detect_blur(image):

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    return float(
        cv2.Laplacian(gray, cv2.CV_64F).var()
    )


# NEW: threshold for noise-based routing. This is a starting estimate,
# NOT calibrated against your actual dataset -- run the pipeline once,
# look at the printed "DEBUG -> noise_level" values for noise_* images
# vs. clean/original images, and adjust this number to sit between the
# two clusters you actually see.
NOISE_THRESHOLD = 5.0


def enhance_image(image_bytes):

    # decode image
    np_arr = np.frombuffer(
        image_bytes,
        np.uint8
    )

    img = cv2.imdecode(
        np_arr,
        cv2.IMREAD_COLOR
    )

    original = img.copy()

    # metrics
    sharpness = detect_blur(img)

    brightness = np.mean(
        cv2.cvtColor(
            img,
            cv2.COLOR_BGR2GRAY
        )
    )

    # NEW: noise metric -- this was previously never computed here,
    # which is why noisy images fell through every branch below and
    # always ended up as "No Enhancement".
    gray_for_noise = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    noise_level = estimate_noise(gray_for_noise)

    print("DEBUG → brightness:", brightness)

    print("DEBUG → sharpness:", sharpness)

    print("DEBUG → noise_level:", noise_level)

    # default
    enhanced = img.copy()

    modes = []

   # VERY DARK IMAGE
    if brightness < 40:

        enhanced = fix_brightness_lab(
            enhanced,
            gamma=0.55
        )

        modes.append(
            "Brightness Enhanced"
        )

    elif brightness < 70:

        enhanced = fix_brightness_lab(
            enhanced,
            gamma=0.70
        )

        modes.append(
            "Brightness Enhanced"
        )

    elif brightness < 90:

        enhanced = fix_brightness_lab(
            enhanced,
            gamma=0.80
        )

        modes.append(
            "Brightness Enhanced"
        )

    # NEW: NOISY IMAGE
    # Checked before the blur/super-res branch on purpose: noise inflates
    # Laplacian-variance sharpness (random noise reads as fake high-freq
    # "edges"), so a noisy image would otherwise dodge the sharpness<80
    # branch below and also get super-resolved on top of its noise,
    # amplifying it instead of removing it.
    if noise_level > NOISE_THRESHOLD:

        enhanced = enhance_restormer(
            enhanced
        )

        modes.append(
            "Restormer Denoising"
        )

    # BLURRY IMAGE
    if sharpness < 80:

        enhanced = enhance_superres(
            enhanced
        )

        modes.append(
            "AI Super Resolution"
        )

    print("DEBUG MODE:", modes)
    if len(modes) == 0:

        mode = "No Enhancement"

    else:
        

        mode = " + ".join(modes)
        

    new_brightness = np.mean(
        cv2.cvtColor(
            enhanced,
            cv2.COLOR_BGR2GRAY
        )
    )

    print(
        "DEBUG → brightness after:",
        new_brightness
    )

    return original, enhanced, mode