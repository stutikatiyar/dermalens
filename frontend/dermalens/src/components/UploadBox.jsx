import { useState } from "react";

import HeroSection from "./HeroSection";
import BackgroundGlow from "./BackgroundGlow";
import AIProcessing from "./AIProcessing";
import ResultSection from "./ResultSection";
import UploadSection from "./UploadSection";
import Navbar from "./Navbar";

function getBackendURL() {
  const hostname = window.location.hostname;

  if (hostname.includes("-5173.app.github.dev")) {
    return `https://${hostname.replace(
      "-5173.app.github.dev",
      "-8000.app.github.dev"
    )}`;
  }

  return "http://127.0.0.1:8000";
}

export default function UploadBox() {
  const [loading, setLoading] = useState(false);

  const [image, setImage] = useState(null);
  const [enhanced, setEnhanced] = useState(null);

  const [metrics, setMetrics] = useState(null);
  const [confidence, setConfidence] = useState(null);

  const [mode, setMode] = useState("");
  const [insights, setInsights] = useState([]);

  const [enhancementAccepted, setEnhancementAccepted] = useState(true);
  const [degradedImage, setDegradedImage] = useState(null);
  const [evaluation, setEvaluation] = useState(null);

  const [error, setError] = useState("");

  async function handleChange(e) {
    const file = e.target.files?.[0];

    if (!file) return;

    setError("");

    const allowedTypes = [
      "image/jpeg",
      "image/jpg",
      "image/png"
    ];

    if (!allowedTypes.includes(file.type)) {
      setError("Please upload a JPG, JPEG, or PNG image.");
      return;
    }

    if (file.size > 15 * 1024 * 1024) {
      setError("Please upload an image smaller than 15 MB.");
      return;
    }

    setLoading(true);

    setEnhanced(null);
    setMetrics(null);
    setConfidence(null);
    setMode("");
    setInsights([]);
    setEnhancementAccepted(true);
    setDegradedImage(null);
    setEvaluation(null);

    const previewURL = URL.createObjectURL(file);
    setImage(previewURL);

    try {
      const backendURL = getBackendURL();

      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch(`${backendURL}/upload`, {
        method: "POST",
        body: formData
      });

      if (!res.ok) {
        const errorText = await res.text();

        console.error(
          "DermaLens backend error:",
          res.status,
          errorText
        );

        throw new Error(
          `Backend returned HTTP ${res.status}`
        );
      }

      const data = await res.json();

      if (!data.image) {
        throw new Error(
          "The backend did not return a processed image."
        );
      }

      setEnhanced(
        `data:image/jpeg;base64,${data.image}`
      );

      setMetrics(data.metrics || null);

      setConfidence(data.confidence || null);

      setMode(data.mode || "Not specified");

      setInsights(
        Array.isArray(data.interpretation)
          ? data.interpretation
          : []
      );

      setEnhancementAccepted(
        data.enhancement_accepted !== undefined
          ? Boolean(data.enhancement_accepted)
          : data.mode !== "No Enhancement"
      );

    } catch (err) {
      console.error(
        "DermaLens processing failed:",
        err
      );

      setError(
        "Unable to process this image. Make sure the FastAPI backend is running and try again."
      );

      setEnhanced(null);

    } finally {
      setLoading(false);
    }
  }

  async function handleEvaluation(originalFile, degradedFile) {
    setError("");
    setLoading(true);
    setImage(URL.createObjectURL(originalFile));
    setDegradedImage(URL.createObjectURL(degradedFile));
    setEnhanced(null);
    setEvaluation(null);

    try {
      const formData = new FormData();
      formData.append("original", originalFile);
      formData.append("degraded", degradedFile);

      const res = await fetch(`${getBackendURL()}/evaluate`, {
        method: "POST",
        body: formData
      });

      if (!res.ok) {
        throw new Error(`Backend returned HTTP ${res.status}: ${await res.text()}`);
      }

      const data = await res.json();
      setEnhanced(`data:image/jpeg;base64,${data.enhanced_image}`);
      setEvaluation(data.evaluation || null);
      setMode(data.mode || "Not specified");
      setConfidence(data.confidence || null);
      setEnhancementAccepted(true);
    } catch (err) {
      console.error("DermaLens evaluation failed:", err);
      setError("Unable to run the reference evaluation. Check that the backend and LPIPS dependencies are running.");
      setEnhanced(null);
    } finally {
      setLoading(false);
    }
  }

  function resetPipeline() {
    setImage(null);
    setEnhanced(null);
    setMetrics(null);
    setConfidence(null);
    setMode("");
    setInsights([]);
    setEnhancementAccepted(true);
    setDegradedImage(null);
    setEvaluation(null);
    setError("");
  }

  return (
    <div className="relative min-h-screen bg-[#020617] overflow-hidden">

      <BackgroundGlow />

      <Navbar />

      <HeroSection />

      {error && (
        <div className="relative z-20 px-6 mb-6">
          <div className="max-w-3xl mx-auto rounded-xl border border-red-400/20 bg-red-400/[0.05] px-5 py-4 text-sm text-red-300 text-center">
            {error}
          </div>
        </div>
      )}

      {!loading && !enhanced && (
        <UploadSection
          handleChange={handleChange}
          handleEvaluation={handleEvaluation}
        />
      )}

      {loading && (
        <div className="relative z-10 px-6 pb-24 -mt-4">
          <div className="max-w-4xl mx-auto">
            <AIProcessing />
          </div>
        </div>
      )}

      {!loading && enhanced && (
        <>
          <ResultSection
            image={image}
            enhanced={enhanced}
            metrics={metrics}
            confidence={confidence}
            mode={mode}
            insights={insights}
            enhancementAccepted={enhancementAccepted}
            degradedImage={degradedImage}
            evaluation={evaluation}
          />

          <div className="relative z-10 pb-20 text-center">
            <button
              onClick={resetPipeline}
              className="px-6 py-3 rounded-xl border border-white/10 bg-white/[0.03] text-sm text-slate-300 hover:bg-white/[0.06] hover:border-cyan-400/20 transition"
            >
              ← Analyze another image
            </button>
          </div>
        </>
      )}

    </div>
  );
}