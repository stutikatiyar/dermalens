import { useRef, useState } from "react";

export default function UploadSection({ handleChange, handleEvaluation }) {
  const originalInput = useRef(null);
  const degradedInput = useRef(null);
  const [originalFile, setOriginalFile] = useState(null);
  const [degradedFile, setDegradedFile] = useState(null);

  function runEvaluation() {
    if (originalFile && degradedFile) {
      handleEvaluation(originalFile, degradedFile);
    }
  }

  return (
    <section className="relative z-10 px-6 pb-24">
      <div className="max-w-6xl mx-auto">

        {/* SECTION INTRO */}
        <div className="text-center mb-10">
          <p className="text-xs uppercase tracking-[0.2em] text-cyan-400 font-semibold">
            Test the middleware
          </p>

          <h2 className="mt-3 text-3xl md:text-4xl font-bold text-white">
            See what DermaLens does to an image
          </h2>

          <p className="mt-4 text-slate-400 max-w-2xl mx-auto leading-relaxed">
            Upload a dermatological image and watch the pipeline assess
            image quality, generate enhancement candidates, validate the
            result, and produce an optimized input for downstream AI.
          </p>
        </div>

        {/* PIPELINE CARDS */}
        <div className="grid md:grid-cols-4 gap-3 mb-8">

          <InfoCard
            number="01"
            title="Analyze"
            text="Identify blur, illumination, contrast and image-quality issues."
          />

          <InfoCard
            number="02"
            title="Enhance"
            text="Generate adaptive restoration candidates based on image condition."
          />

          <InfoCard
            number="03"
            title="Validate"
            text="Check structure, noise, brightness, sharpness and color stability."
          />

          <InfoCard
            number="04"
            title="Output"
            text="Return the improved image or safely preserve the original."
          />

        </div>

        {/* UPLOAD */}
        <div className="max-w-4xl mx-auto">

          <label
            htmlFor="dermalens-upload"
            className="group block cursor-pointer"
          >
            <div className="relative overflow-hidden rounded-3xl border border-cyan-400/20 bg-slate-950/70 backdrop-blur-xl p-8 md:p-12 text-center transition-all duration-300 hover:border-cyan-400/40 hover:bg-slate-900/80">

              <div className="absolute inset-0 bg-gradient-to-b from-cyan-400/[0.04] to-transparent pointer-events-none" />

              <div className="relative">

                <div className="mx-auto w-16 h-16 rounded-2xl bg-cyan-400/10 border border-cyan-400/20 flex items-center justify-center text-2xl text-cyan-400 group-hover:scale-105 transition-transform">
                  ↑
                </div>

                <h3 className="mt-6 text-xl font-semibold text-white">
                  Upload a dermatology image
                </h3>

                <p className="mt-2 text-sm text-slate-400">
                  JPG, JPEG or PNG
                </p>

                <div className="mt-6 inline-flex items-center gap-2 px-5 py-3 rounded-xl bg-cyan-400 text-slate-950 font-semibold text-sm group-hover:bg-cyan-300 transition">
                  Run DermaLens
                  <span>→</span>
                </div>

                <p className="mt-5 text-xs text-slate-500">
                  Your image is analyzed for quality degradation — not diagnosed.
                </p>

              </div>
            </div>

            <input
              id="dermalens-upload"
              type="file"
              accept="image/png,image/jpeg,image/jpg"
              onChange={handleChange}
              className="hidden"
            />
          </label>

          {/* TECHNICAL NOTE */}
          <div className="mt-6 flex flex-col md:flex-row items-center justify-center gap-3 text-xs text-slate-500">
            <span>Quality indicators</span>
            <span className="hidden md:block">•</span>
            <span>Candidate-based enhancement</span>
            <span className="hidden md:block">•</span>
            <span>Validation gate</span>
            <span className="hidden md:block">•</span>
            <span>Downstream model comparison</span>
          </div>

          <div className="mt-10 rounded-3xl border border-cyan-400/20 bg-slate-950/70 p-6 md:p-8">
            <div className="text-center">
              <p className="text-xs uppercase tracking-[0.2em] text-cyan-400 font-semibold">
                Reference experiment
              </p>
              <h3 className="mt-2 text-xl font-semibold text-white">
                Compare restoration against a clean reference
              </h3>
              <p className="mt-2 text-sm text-slate-400 max-w-2xl mx-auto">
                Reference-based evaluation compares both the degraded input and DermaLens output against the original clean image.
              </p>
            </div>

            <div className="mt-6 grid md:grid-cols-2 gap-4">
              <FilePicker
                label="Original clean image"
                file={originalFile}
                inputRef={originalInput}
                onChange={(event) => setOriginalFile(event.target.files?.[0] || null)}
              />
              <FilePicker
                label="Degraded image"
                file={degradedFile}
                inputRef={degradedInput}
                onChange={(event) => setDegradedFile(event.target.files?.[0] || null)}
              />
            </div>

            <button
              type="button"
              disabled={!originalFile || !degradedFile}
              onClick={runEvaluation}
              className="mt-6 w-full rounded-xl bg-cyan-400 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-40"
            >
              Run DermaLens Evaluation
            </button>

            <p className="mt-4 text-center text-xs text-slate-500">
              PSNR and SSIM should increase; LPIPS should decrease. These are image-quality metrics, not diagnostic accuracy metrics.
            </p>
          </div>

        </div>
      </div>
    </section>
  );
}

function FilePicker({ label, file, inputRef, onChange }) {
  return (
    <button
      type="button"
      onClick={() => inputRef.current?.click()}
      className="rounded-xl border border-white/10 bg-white/[0.025] p-5 text-left hover:border-cyan-400/30 transition"
    >
      <span className="block text-xs uppercase tracking-wider text-slate-500">{label}</span>
      <span className="mt-2 block truncate text-sm text-white">{file ? file.name : "Choose JPG, JPEG or PNG"}</span>
      <input
        ref={inputRef}
        type="file"
        accept="image/png,image/jpeg,image/jpg"
        onChange={onChange}
        className="hidden"
      />
    </button>
  );
}

function InfoCard({ number, title, text }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/[0.025] p-5">
      <div className="text-xs font-mono text-cyan-400 mb-3">
        {number}
      </div>

      <h3 className="text-sm font-semibold text-white">
        {title}
      </h3>

      <p className="text-xs text-slate-500 leading-relaxed mt-2">
        {text}
      </p>
    </div>
  );
}