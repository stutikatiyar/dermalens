# DermaLens 🧠🩺

Domain-aware dermatology image enhancement system with model-based validation.

---

## Overview

DermaLens is not just an image enhancement tool—it is a validation-aware preprocessing system for dermatology AI.

Instead of blindly improving image quality, DermaLens applies **minimal, selective enhancement** and verifies whether the enhancement actually improves AI model confidence.

This prevents distortion of medically important features and ensures that enhancement does not harm downstream predictions.

---

## Problem

In real-world telemedicine scenarios, dermatology images are often:

* blurry
* poorly lit
* noisy

Traditional pipelines apply enhancement blindly, which can:

* distort lesion textures
* alter color distribution
* reduce model reliability

---

## Solution

DermaLens introduces a **selective enhancement + validation pipeline**:

* Detect image quality (blur, brightness)
* Apply minimal correction only when necessary
* Evaluate impact using a trained dermatology model
* Compare confidence before and after enhancement

---

## Pipeline

Image
↓
Quality Analysis (Sharpness, Brightness)
↓
Selective Enhancement (if needed)
↓
Dermatology Classifier (ResNet18)
↓
Confidence Comparison (Before vs After)

---

## How It Works

1. User uploads a skin image
2. System computes:

   * sharpness (blur detection)
   * brightness level
3. Based on conditions:

   * applies mild brightness correction OR
   * applies light sharpening OR
   * skips enhancement
4. Runs ML model on:

   * original image
   * enhanced image
5. Compares confidence scores
6. Outputs:

   * enhanced image
   * metrics
   * improvement / degradation status

---

## Key Insight

> Image enhancement does not always improve AI performance.

DermaLens demonstrates that:

* aggressive enhancement can degrade model confidence
* preserving original data distribution is critical
* enhancement should be **selective and validated**, not blind

---

## Features

* 📸 Image upload and preview
* 🔍 Selective enhancement (not over-processing)
* 📊 Quality metrics:

  * Sharpness
  * Contrast
* 🧠 Blur & brightness-based decision logic
* 🤖 Model-based validation (confidence comparison)
* ⚡ FastAPI backend
* 🎨 React + Vite frontend

---

## Tech Stack

* Frontend: React, Vite, Tailwind CSS
* Backend: FastAPI (Python)
* Image Processing: OpenCV
* Machine Learning: PyTorch (ResNet18)
* Communication: Axios

---

## Project Structure

backend/
app/
ml/
enhancement.py
evaluate_derm.py
train_derm.py
derm_model.py

frontend/
dermalens/
src/

---

## How to Run

### Backend

cd backend
python -m venv venv
venv\Scripts\activate
pip install -r ../requirements.txt

Run API:
python -m uvicorn app.main:app --reload

---

### Frontend

cd frontend/dermalens
npm install
npm run dev

---

## Evaluation

The system evaluates enhancement using:

* model confidence before enhancement
* model confidence after enhancement
* delta (difference)

Example:

Original → 0.80
Enhanced → 0.83
Δ → +0.03 (Improvement)

---

## Current Status

* ✔ Full pipeline implemented
* ✔ Model training completed (dermatology dataset)
* ✔ Enhancement logic stabilized (non-destructive)
* ✔ Evaluation framework integrated
* ✔ UI working

---

## Limitations

* Improvements are small due to conservative enhancement
* No paired real-world low-quality dataset
* Model trained on clean data (distribution mismatch possible)

---

## Future Improvements

* Learned enhancement models (U-Net / GANs)
* Adaptive threshold tuning
* Larger dermatology datasets
* Mobile integration
* Real-world deployment in telemedicine

---

## Author

Stuti Katiyar
