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
    <div className="mt-12 flex flex-col items-center">

      <input
        type="file"
        accept="image/*"
        onChange={handleChange}
        className="hidden"
        id="upload"
      />

      <label
        htmlFor="upload"
        className="px-6 py-3 border border-gray-300 rounded-md text-sm font-medium cursor-pointer hover:bg-black hover:text-white transition-all duration-200"
      >
        {loading ? "Processing..." : "Upload Image"}
      </label>

      {image && enhanced && (
        <div className="mt-12 w-full max-w-4xl bg-white border border-gray-200 rounded-xl p-6 shadow-sm">

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

            {/* Original */}
            <div className="flex flex-col items-center">
              <p className="text-sm text-gray-500 mb-3">Original</p>
              <img
                src={image}
                alt="original"
                className="w-full rounded-lg border border-gray-200"
              />
            </div>

            {/* Enhanced */}
            <div className="flex flex-col items-center">
              <p className="text-sm text-gray-500 mb-3">Enhanced</p>
              <img
                src={enhanced}
                alt="enhanced"
                className="w-full rounded-lg border border-gray-200"
              />
            </div>

          </div>

        </div>
      )}

      {/* Metrics */}
      {metrics && metrics.sharpness_before && (
        <div className="mt-6 text-sm text-gray-600 text-center">
          <p>
            Sharpness: {metrics.sharpness_before.toFixed(2)} → {metrics.sharpness_after.toFixed(2)}
          </p>
          <p>
            Contrast: {metrics.contrast_before.toFixed(2)} → {metrics.contrast_after.toFixed(2)}
          </p>
          <p className="mt-2 font-semibold text-black">
             Quality Score: {metrics.quality_before.toFixed(2)} → {metrics.quality_after.toFixed(2)}
          </p>
        </div>
      )}

      {/* Mode */}
      {mode && (
        <p className="mt-2 text-sm text-green-600 text-center">
          Mode: {mode}
        </p>
      )}
      {insights && (
        <div className="mt-4 text-sm text-gray-700 text-center space-y-1">
    {insights.map((item, index) => (
      <p key={index}>✔ {item}</p>
    ))}
      </div>
      )}

    </div>
  );
}

export default UploadBox;