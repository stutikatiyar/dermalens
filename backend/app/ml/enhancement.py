import cv2
import numpy as np

def detect_blur(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return float(cv2.Laplacian(gray, cv2.CV_64F).var())

def enhance_image(image_bytes):
    # decode
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    original = img.copy()

    # analyze
    sharpness = detect_blur(img)

    # decide + enhance
    if sharpness < 80:
        # -------- STRONG --------
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)

        lab = cv2.merge((l, a, b))
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

        blur = cv2.GaussianBlur(enhanced, (0, 0), 1.2)
        enhanced = cv2.addWeighted(enhanced, 1.4, blur, -0.4, 0)

        mode = "Strong Enhancement"

    elif sharpness < 200:
        # -------- MODERATE --------
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        clahe = cv2.createCLAHE(clipLimit=1.6, tileGridSize=(8, 8))
        l = clahe.apply(l)

        lab = cv2.merge((l, a, b))
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

        blur = cv2.GaussianBlur(enhanced, (0, 0), 1.0)
        enhanced = cv2.addWeighted(enhanced, 1.3, blur, -0.3, 0)

        mode = "Moderate Enhancement"

    else:
        # -------- MINIMAL --------
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        clahe = cv2.createCLAHE(clipLimit=1.2, tileGridSize=(8, 8))
        l = clahe.apply(l)

        lab = cv2.merge((l, a, b))
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

        blur = cv2.GaussianBlur(enhanced, (0, 0), 0.6)
        enhanced = cv2.addWeighted(enhanced, 1.1, blur, -0.1, 0)

        mode = "Minimal Enhancement"

    # ALWAYS return at the end
    return original, enhanced, mode