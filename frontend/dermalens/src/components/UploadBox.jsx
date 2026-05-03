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
  <div className="bg-[#1e293b] rounded-2xl shadow-2xl p-6 w-full max-w-4xl mx-auto space-y-6">
    
    <div className="bg-[#1e293b] rounded-2xl shadow-2xl p-6 w-full max-w-5xl space-y-6">

      <input
        type="file"
        accept="image/*"
        onChange={handleChange}
        className="hidden"
        id="upload"
      />

      <label
        htmlFor="upload"
        className="bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded-lg text-white font-medium cursor-pointer transition-all"
      >
        {loading ? "Processing..." : "Upload Image"}
      </label>

      {image && enhanced && (
        <div className="mt-6 w-full bg-[#020617] border border-gray-700 rounded-xl p-6 shadow-sm">

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

            {/* Original */}
            <div className="flex flex-col items-center">
              <p className="text-sm text-gray-400 mb-3">Original</p>
              <img src={image} alt="original" className="w-full rounded-lg border border-gray-700" />
            </div>

            {/* Enhanced */}
            <div className="flex flex-col items-center">
              <p className="text-sm text-blue-400 mb-3">Enhanced</p>
              <img src={enhanced} alt="enhanced" className="w-full rounded-lg border border-blue-500" />
            </div>

          </div>

        </div>
      )}

      {/* Metrics */}
      {metrics && metrics.sharpness_before && (
        <div className="text-sm text-gray-300 text-center">
          <p>
            Sharpness: {metrics.sharpness_before.toFixed(2)} → {metrics.sharpness_after.toFixed(2)}
          </p>
          <p>
            Contrast: {metrics.contrast_before.toFixed(2)} → {metrics.contrast_after.toFixed(2)}
          </p>
          <p className="mt-2 font-semibold text-white">
            Quality Score: {metrics.quality_before.toFixed(2)} → {metrics.quality_after.toFixed(2)}
          </p>
        </div>
      )}

      {/* Mode */}
      {mode && (
        <p className="text-sm text-green-400 text-center">
          Mode: {mode}
        </p>
      )}

      {/* Insights */}
      {insights && (
        <div className="text-sm text-gray-300 text-center space-y-1">
          {insights.map((item, index) => (
            <p key={index}>✔ {item}</p>
          ))}
        </div>
      )}

    </div>

  </div>
);

}

export default UploadBox;