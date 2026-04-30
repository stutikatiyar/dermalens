# DermaLens 🧠🩺

AI-powered dermatology image enhancement middleware that improves image quality while preserving diagnostic integrity.

---

##  Overview

DermaLens processes dermatological images before they reach AI diagnostic models.  
It enhances clarity, reduces noise, and preserves lesion features to improve reliability.

---

##  Features

- 📸 Image Upload & Preview
- 🔍 Adaptive Enhancement (Strong / Moderate / Minimal)
- 📊 Quality Metrics:
  - Sharpness
  - Contrast
- 🧠 Blur-based Decision Engine
- ⚡ Fast API backend (FastAPI)
- 🎨 Modern UI (React + Vite)

---

## 🏗️ Architecture
Frontend (React)
↓
Backend API (FastAPI)
↓
Enhancement Engine (OpenCV)
↓
Metrics + Decision Logic

---

##  How It Works

1. Upload image
2. System analyzes blur (sharpness)
3. Chooses enhancement mode:
   - Strong → blurry image
   - Moderate → average image
   - Minimal → already clear image
4. Enhances image
5. Returns:
   - Enhanced image
   - Metrics
   - Mode

---

##  Tech Stack

- Frontend: React, Vite, Tailwind CSS
- Backend: FastAPI, Python
- Image Processing: OpenCV
- Communication: Axios

---

##  Current Status

- ✔ Upload & preview working
- ✔ Adaptive enhancement working
- ✔ Metrics integrated
- ✔ UI complete

---
##  Future Improvements

- Advanced quality scoring (PSNR / SSIM)
- AI-based enhancement models (ESRGAN)
- Dermatology dataset integration
- Model-based diagnosis pipeline

---

##  Key Idea

> Improve image quality without altering medical features.

---

##  Author

Stuti katiyar
