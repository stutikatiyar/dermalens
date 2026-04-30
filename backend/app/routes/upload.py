from fastapi import APIRouter, UploadFile, File
import base64
import cv2

from app.ml.enhancement import enhance_image
from app.ml.metrics import calculate_sharpness, calculate_contrast

router = APIRouter()

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    image_bytes = await file.read()

    original, enhanced, mode = enhance_image(image_bytes)

    # calculate metrics
    sharp_before = calculate_sharpness(original)
    sharp_after = calculate_sharpness(enhanced)

    contrast_before = calculate_contrast(original)
    contrast_after = calculate_contrast(enhanced)

    # encode enhanced image
    _, buffer = cv2.imencode(".jpg", enhanced)
    image_base64 = base64.b64encode(buffer).decode("utf-8")

    return {
    "image": image_base64,
    "mode": mode,   # 🔥 separate it
    "metrics": {
        "sharpness_before": sharp_before,
        "sharpness_after": sharp_after,
        "contrast_before": contrast_before,
        "contrast_after": contrast_after
    }
}