import base64

import cv2
import numpy as np
from fastapi import APIRouter, File, HTTPException, UploadFile

from app.evaluation.reference_metrics import evaluate_reference_pair
from app.ml.enhancement import enhance_image
from app.routes.upload import (
    predict_confidence,
    select_best_candidate,
)


router = APIRouter()


def decode_image(image_bytes, field_name):
    image = cv2.imdecode(
        np.frombuffer(image_bytes, dtype=np.uint8),
        cv2.IMREAD_COLOR,
    )

    if image is None:
        raise HTTPException(
            status_code=400,
            detail=f"{field_name} is not a valid JPEG or PNG image.",
        )

    return image


def encode_image(image):
    success, buffer = cv2.imencode(".jpg", image)

    if not success:
        raise HTTPException(
            status_code=500,
            detail="Failed to encode the enhanced image.",
        )

    return base64.b64encode(buffer).decode("utf-8")


@router.post("/evaluate")
async def evaluate_images(
    original: UploadFile = File(...),
    degraded: UploadFile = File(...),
):
    original_bytes = await original.read()
    degraded_bytes = await degraded.read()

    if not original_bytes or not degraded_bytes:
        raise HTTPException(
            status_code=400,
            detail="Both original and degraded image files are required.",
        )

    reference_image = decode_image(original_bytes, "original")
    degraded_image = decode_image(degraded_bytes, "degraded")

    try:
        pipeline_original, candidates, _ = enhance_image(degraded_bytes)
        enhanced_image, final_mode = select_best_candidate(
            pipeline_original,
            candidates,
        )

        degraded_metrics = evaluate_reference_pair(
            reference_image,
            degraded_image,
        )
        enhanced_metrics = evaluate_reference_pair(
            reference_image,
            enhanced_image,
        )
    except (RuntimeError, ValueError, OSError) as error:
        raise HTTPException(status_code=422, detail=str(error)) from error

    confidence_before = predict_confidence(degraded_image)
    confidence_after = predict_confidence(enhanced_image)

    return {
        "success": True,
        "enhanced_image": encode_image(enhanced_image),
        "mode": final_mode,
        "evaluation": {
            "reference_available": True,
            "alignment": {
                "reference_shape": [
                    int(reference_image.shape[1]),
                    int(reference_image.shape[0]),
                ],
                "metric_space": "comparison images resized to reference dimensions",
            },
            "psnr": {
                "degraded_vs_original": degraded_metrics["psnr"],
                "enhanced_vs_original": enhanced_metrics["psnr"],
                "change_db": enhanced_metrics["psnr"] - degraded_metrics["psnr"],
            },
            "ssim": {
                "degraded_vs_original": degraded_metrics["ssim"],
                "enhanced_vs_original": enhanced_metrics["ssim"],
                "change": enhanced_metrics["ssim"] - degraded_metrics["ssim"],
            },
            "lpips": {
                "degraded_vs_original": degraded_metrics["lpips"],
                "enhanced_vs_original": enhanced_metrics["lpips"],
                "change": enhanced_metrics["lpips"] - degraded_metrics["lpips"],
            },
        },
        "confidence": {
            "degraded": confidence_before,
            "enhanced": confidence_after,
            "delta": confidence_after - confidence_before,
        },
    }