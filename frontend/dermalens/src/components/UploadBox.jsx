import { useState } from "react";
import { uploadImage } from "../api/api";

function UploadBox() {
  const [image, setImage] = useState(null);
  const [enhanced, setEnhanced] = useState(null);
  const [loading, setLoading] = useState(false);
  const [metrics, setMetrics] = useState(null);
  const [mode, setMode] = useState(null);
  const [insights, setInsights] = useState(null);

  const handleChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // reset old state (important)
    setMetrics(null);
    setMode(null);
    setInsights(null);

    setImage(URL.createObjectURL(file));

    try {
      setLoading(true);

      const response = await uploadImage(file);

      // base64 → image
      const imageURL = `data:image/jpeg;base64,${response.image}`;
      setEnhanced(imageURL);

      // metrics
      if (response.metrics) {
        setMetrics(response.metrics);
      }

      if (response.interpretation) {
        setInsights(response.interpretation);
}

      // mode
      if (response.mode) {
        setMode(response.mode);
      }

    } catch (error) {
      console.error("Upload failed:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
  <div className="w-full max-w-6xl mx-auto px-6 py-10">

    <div className="bg-[#0f172a]/80 border border-white/10 backdrop-blur-xl rounded-3xl shadow-2xl p-8 space-y-8">

      {/* Header */}
      <div className="text-center space-y-3">
        <h1 className="text-4xl font-bold text-white tracking-tight">
          DermaLens
        </h1>

        <p className="text-slate-400 max-w-2xl mx-auto leading-relaxed">
          AI-aware image preprocessing and confidence validation framework
          for analyzing low-quality image enhancement reliability.
        </p>
      </div>

      {/* Upload */}
      <div className="flex justify-center">

        <input
          type="file"
          accept="image/*"
          onChange={handleChange}
          className="hidden"
          id="upload"
        />

        <label
          htmlFor="upload"
          className="px-6 py-3 rounded-2xl bg-blue-600 hover:bg-blue-500 transition-all text-white font-medium cursor-pointer shadow-lg shadow-blue-500/20"
        >
          {loading ? "Processing..." : "Upload Image"}
        </label>

      </div>

      {/* Images */}
      {image && enhanced && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">

          <div className="space-y-3">
            <p className="text-sm text-slate-400 font-medium">
              Original Image
            </p>

            <div className="bg-[#020617] border border-white/10 rounded-2xl overflow-hidden">
              <img
                src={image}
                alt="original"
                className="w-full object-cover"
              />
            </div>
          </div>

          <div className="space-y-3">
            <p className="text-sm text-blue-400 font-medium">
              Enhanced Image
            </p>

            <div className="bg-[#020617] border border-blue-500/30 rounded-2xl overflow-hidden shadow-lg shadow-blue-500/10">
              <img
                src={enhanced}
                alt="enhanced"
                className="w-full object-cover"
              />
            </div>
          </div>

        </div>
      )}

      {/* Metrics */}
      {metrics && metrics.sharpness_before && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">

          <div className="bg-[#020617] border border-white/10 rounded-2xl p-5 text-center">
            <p className="text-slate-400 text-sm mb-2">Sharpness</p>

            <h2 className="text-white text-xl font-bold">
              {metrics.sharpness_before.toFixed(2)}
              <span className="text-blue-400 mx-2">→</span>
              {metrics.sharpness_after.toFixed(2)}
            </h2>
          </div>

          <div className="bg-[#020617] border border-white/10 rounded-2xl p-5 text-center">
            <p className="text-slate-400 text-sm mb-2">Contrast</p>

            <h2 className="text-white text-xl font-bold">
              {metrics.contrast_before.toFixed(2)}
              <span className="text-blue-400 mx-2">→</span>
              {metrics.contrast_after.toFixed(2)}
            </h2>
          </div>

          <div className="bg-[#020617] border border-blue-500/20 rounded-2xl p-5 text-center">
            <p className="text-slate-400 text-sm mb-2">Quality Score</p>

            <h2 className="text-blue-400 text-xl font-bold">
              {metrics.quality_before.toFixed(2)}
              <span className="mx-2">→</span>
              {metrics.quality_after.toFixed(2)}
            </h2>
          </div>

        </div>
      )}

      {/* Mode */}
      {mode && (
        <div className="flex justify-center">
          <div className="px-4 py-2 rounded-full bg-green-500/10 border border-green-500/20 text-green-400 text-sm font-medium">
            Mode: {mode}
          </div>
        </div>
      )}

      {/* Insights */}
      {insights && (
        <div className="bg-[#020617] border border-white/10 rounded-2xl p-6">

          <h3 className="text-white font-semibold mb-4">
            AI Insights
          </h3>

          <div className="space-y-3">
            {insights.map((item, index) => (
              <p
                key={index}
                className="text-slate-300 flex items-center gap-2"
              >
                <span className="text-blue-400">●</span>
                {item}
              </p>
            ))}
          </div>

        </div>
      )}

    </div>

  </div>
  );
}

export default UploadBox;
