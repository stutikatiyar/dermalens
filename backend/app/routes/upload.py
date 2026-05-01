from fastapi import APIRouter, UploadFile, File
import base64
import cv2

from app.ml.enhancement import enhance_image
from app.ml.metrics import calculate_sharpness, calculate_contrast
from app.ml.metrics import quality_score

def generate_interpretation(q_before, q_after, mode):
    improvement = q_after - q_before

    insights = []

    if improvement > 40:
        insights.append("Significant clarity improvement detected")
    elif improvement > 20:
        insights.append("Moderate improvement in image quality")
    else:
        insights.append("Minor enhancement applied")

    if mode == "Strong Enhancement":
        insights.append("Image was initially blurry or low quality")
    elif mode == "Moderate Enhancement":
        insights.append("Image had moderate quality issues")
    else:
        insights.append("Image was already fairly clear")

    if q_after > 75:
        insights.append("Suitable for AI-based analysis")
    elif q_after > 50:
        insights.append("Acceptable for analysis with caution")
    else:
        insights.append("May still be insufficient for reliable analysis")

    return insights
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

    quality_before = quality_score(sharp_before, contrast_before)
    quality_after = quality_score(sharp_after, contrast_after)

    interpretation = generate_interpretation(quality_before, quality_after, mode)

    # encode enhanced image
    _, buffer = cv2.imencode(".jpg", enhanced)
    image_base64 = base64.b64encode(buffer).decode("utf-8")

    return {
    "image": image_base64,
    "mode": mode,
    "metrics": {
        "sharpness_before": sharp_before,
        "sharpness_after": sharp_after,
        "contrast_before": contrast_before,
        "contrast_after": contrast_after,
        "quality_before": quality_before,
        "quality_after": quality_after
    },
    "interpretation": interpretation
}