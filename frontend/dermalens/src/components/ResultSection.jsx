import { useState } from "react";

export default function ResultSection({
  image,
  enhanced,
  metrics,
  confidence,
  mode,
  insights,
  enhancementAccepted,
  degradedImage,
  evaluation
}) {
  const [slider, setSlider] = useState(50);
  const [zoom, setZoom] = useState(false);

  const m = metrics || {};
  const c = confidence || {};

  const format = (value, digits = 1) => {
    if (value === null || value === undefined || Number.isNaN(Number(value))) {
      return "—";
    }

    return Number(value).toFixed(digits);
  };

  const percentage = (value) => {
    if (
      value === null ||
      value === undefined ||
      Number.isNaN(Number(value))
    ) {
      return "—";
    }

    return `${(Number(value) * 100).toFixed(1)}%`;
  };

  const signedPercentagePoints = (value) => {
    if (
      value === null ||
      value === undefined ||
      Number.isNaN(Number(value))
    ) {
      return "—";
    }

    const n = Number(value) * 100;

    return `${n >= 0 ? "+" : ""}${n.toFixed(1)} pp`;
  };

  const qualityImprovement =
    m.quality_improvement !== undefined
      ? Number(m.quality_improvement)
      : null;

  const qualityImproved =
    qualityImprovement !== null && qualityImprovement > 0;

  const accepted =
    enhancementAccepted !== undefined
      ? enhancementAccepted
      : mode !== "No Enhancement";

  return (
    <section className="relative z-10 px-6 pb-24">
      <div className="max-w-6xl mx-auto">

        {/* HEADER */}
        <div className="mb-8">

          <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-5">

            <div>
              <p className="text-xs uppercase tracking-[0.2em] text-cyan-400 font-semibold">
                Pipeline Result
              </p>

              <h2 className="mt-2 text-3xl md:text-4xl font-bold text-white">
                {accepted
                  ? "Enhancement accepted"
                  : "Original image preserved"}
              </h2>

              <p className="mt-3 text-sm text-slate-400 max-w-2xl leading-relaxed">
                {accepted
                  ? "A candidate enhancement passed the image-quality validation gate and was selected as the final output."
                  : "No enhancement candidate provided sufficient benefit under the validation criteria, so the original image was safely retained."}
              </p>
            </div>

            <div
              className={`shrink-0 px-4 py-3 rounded-xl border ${
                accepted
                  ? "border-cyan-400/20 bg-cyan-400/[0.06]"
                  : "border-amber-400/20 bg-amber-400/[0.05]"
              }`}
            >
              <p className="text-[10px] uppercase tracking-widest text-slate-500">
                Final decision
              </p>

              <p
                className={`mt-1 text-sm font-semibold ${
                  accepted
                    ? "text-cyan-300"
                    : "text-amber-300"
                }`}
              >
                {accepted ? "✓ Enhancement accepted" : "↺ Original preserved"}
              </p>
            </div>

          </div>
        </div>

        {/* IMAGE COMPARISON */}
        <div className="rounded-3xl border border-white/10 bg-slate-950/80 overflow-hidden">

          <div className="px-6 py-5 border-b border-white/10 flex flex-col md:flex-row md:items-center md:justify-between gap-3">
            <div>
              <h3 className="text-lg font-semibold text-white">
                Before / After Comparison
              </h3>

              <p className="text-xs text-slate-500 mt-1">
                Interactive comparison of the original and final pipeline output
              </p>
            </div>

            <button
              onClick={() => setZoom(!zoom)}
              className="px-3 py-2 rounded-lg border border-white/10 text-xs text-slate-300 hover:bg-white/5 transition"
            >
              {zoom ? "Exit zoom" : "Zoom image"}
            </button>
          </div>

          <div
            className={`relative overflow-hidden bg-black ${
              zoom ? "min-h-[650px]" : "min-h-[420px]"
            }`}
          >

            {/* AFTER */}
            <img
              src={enhanced}
              alt="DermaLens final output"
              className={`absolute inset-0 w-full h-full object-contain ${
                zoom ? "scale-125" : ""
              } transition-transform duration-300`}
            />

            {/* BEFORE */}
            <div
              className="absolute inset-0 overflow-hidden"
              style={{ width: `${slider}%` }}
            >
              <img
                src={image}
                alt="Original dermatology image"
                className={`absolute inset-0 w-full h-full object-contain ${
                  zoom ? "scale-125" : ""
                } max-w-none`}
                style={{
                  width: "100vw",
                  maxWidth: "none"
                }}
              />
            </div>

            {/* DIVIDER */}
            <div
              className="absolute top-0 bottom-0 w-px bg-white/80"
              style={{ left: `${slider}%` }}
            >
              <div className="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 w-10 h-10 rounded-full bg-slate-950 border border-white/30 flex items-center justify-center text-white shadow-xl">
                ↔
              </div>
            </div>

            {/* SLIDER */}
            <input
              type="range"
              min="0"
              max="100"
              value={slider}
              onChange={(e) => setSlider(Number(e.target.value))}
              className="absolute inset-0 w-full h-full opacity-0 cursor-ew-resize z-20"
              aria-label="Compare original and enhanced image"
            />

            <div className="absolute top-4 left-4 px-3 py-1.5 rounded-lg bg-black/60 backdrop-blur text-xs text-white z-10">
              Original
            </div>

            <div className="absolute top-4 right-4 px-3 py-1.5 rounded-lg bg-cyan-400/90 text-slate-950 font-semibold text-xs z-10">
              DermaLens output
            </div>

          </div>

          <div className="px-6 py-4 text-center text-xs text-slate-500">
            Drag the center control to compare the original and final image.
          </div>
        </div>

        {/* QUALITY ANALYSIS */}
        {evaluation && degradedImage && (
          <ReferenceEvaluation
            evaluation={evaluation}
            originalImage={image}
            degradedImage={degradedImage}
            enhancedImage={enhanced}
          />
        )}

        <div className="mt-8">

          <SectionHeader
            eyebrow="IMAGE QUALITY"
            title="What changed in the image?"
            description="These are image-quality indicators used by the current pipeline to evaluate the input and candidate output."
          />

          <div className="grid md:grid-cols-3 gap-4 mt-5">

            <MetricCard
              title="Sharpness"
              before={format(m.sharpness_before)}
              after={format(m.sharpness_after)}
              multiplier={m.sharpness_multiplier}
              description="Higher generally indicates more high-frequency detail."
            />

            <MetricCard
              title="Brightness"
              before={format(m.brightness_before)}
              after={format(m.brightness_after)}
              change={
                m.brightness_improvement !== undefined
                  ? percentage(m.brightness_improvement)
                  : null
              }
              description="Used to assess illumination and exposure."
            />

            <MetricCard
              title="Contrast"
              before={format(m.contrast_before)}
              after={format(m.contrast_after)}
              description="Measures separation between image intensities."
            />

          </div>

          <div className="mt-4 rounded-2xl border border-white/10 bg-white/[0.025] p-5">

            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">

              <div>
                <p className="text-xs uppercase tracking-widest text-slate-500">
                  Composite pipeline quality score
                </p>

                <p className="text-sm text-slate-400 mt-1">
                  Based on the current sharpness, contrast and brightness scoring function.
                </p>
              </div>

              <div className="flex items-center gap-4">
                <ScoreValue
                  label="Before"
                  value={format(m.quality_before)}
                />

                <span className="text-slate-600">→</span>

                <ScoreValue
                  label="After"
                  value={format(m.quality_after)}
                  highlight
                />

                <div className="px-3 py-2 rounded-lg bg-cyan-400/10 border border-cyan-400/20">
                  <p className="text-xs text-cyan-300 font-semibold">
                    {qualityImprovement !== null
                      ? `${qualityImprovement >= 0 ? "+" : ""}${(
                          qualityImprovement * 100
                        ).toFixed(1)}%`
                      : "—"}
                  </p>
                </div>
              </div>

            </div>
          </div>
        </div>

        {/* VALIDATION */}
        <div className="mt-10">

          <SectionHeader
            eyebrow="VALIDATION GATE"
            title="Why was this output accepted?"
            description="The current backend evaluates enhancement candidates using safety and quality signals rather than classifier confidence."
          />

          <div className="grid md:grid-cols-2 lg:grid-cols-5 gap-3 mt-5">

            <ValidationCard
              title="Structure"
              text="Preserved"
            />

            <ValidationCard
              title="Brightness"
              text="Controlled"
            />

            <ValidationCard
              title="Sharpness"
              text="Controlled"
            />

            <ValidationCard
              title="Noise"
              text="Monitored"
            />

            <ValidationCard
              title="Color shift"
              text="Monitored"
            />

          </div>

          <div className="mt-4 p-5 rounded-2xl border border-cyan-400/15 bg-cyan-400/[0.035]">
            <p className="text-sm text-slate-300 leading-relaxed">
              <span className="font-semibold text-cyan-300">
                Safety-first selection:
              </span>{" "}
              DermaLens does not simply choose the sharpest image.
              Candidate enhancements are scored while penalizing excessive
              sharpening, noise growth and structural or color changes.
            </p>
          </div>
        </div>

        {/* WHAT IT DID */}
        <div className="mt-10">

          <SectionHeader
            eyebrow="INTERPRETATION"
            title="What DermaLens detected"
            description="The system interprets image condition and explains the selected processing path."
          />

          <div className="mt-5 rounded-2xl border border-white/10 bg-white/[0.025] p-6">

            <div className="flex flex-wrap gap-3">

              {insights && insights.length > 0 ? (
                insights.map((insight, index) => (
                  <div
                    key={`${insight}-${index}`}
                    className="px-4 py-3 rounded-xl border border-white/10 bg-slate-950/60 text-sm text-slate-300"
                  >
                    <span className="text-cyan-400 mr-2">•</span>
                    {cleanConfidenceText(insight)}
                  </div>
                ))
              ) : (
                <p className="text-sm text-slate-500">
                  No additional interpretation was returned.
                </p>
              )}

            </div>

            <div className="mt-6 pt-5 border-t border-white/10">

              <p className="text-xs uppercase tracking-widest text-slate-500">
                Selected processing path
              </p>

              <p className="mt-2 text-sm font-semibold text-white">
                {mode || "Not specified"}
              </p>

            </div>
          </div>
        </div>

        {/* DOWNSTREAM MODEL */}
        <div className="mt-10">

          <SectionHeader
            eyebrow="DOWNSTREAM AI SIGNAL"
            title="Does the downstream model respond differently?"
            description="The current system reports a ResNet18 confidence comparison as a secondary signal. This is not yet a full model-performance evaluation."
          />

          <div className="mt-5 rounded-2xl border border-white/10 bg-white/[0.025] p-6">

            <div className="grid md:grid-cols-3 gap-5">

              <ConfidenceCard
                label="Before DermaLens"
                value={percentage(c.before)}
              />

              <ConfidenceCard
                label="After DermaLens"
                value={percentage(c.after)}
                highlight
              />

              <ConfidenceCard
                label="Change"
                value={signedPercentagePoints(c.delta)}
                highlight={Number(c.delta) > 0}
              />

            </div>

            <div className="mt-5 p-4 rounded-xl bg-amber-400/[0.04] border border-amber-400/15">
              <p className="text-xs text-amber-200/80 leading-relaxed">
                <span className="font-semibold text-amber-200">
                  Important:
                </span>{" "}
                A change in classifier confidence does not prove improved
                diagnostic accuracy. The current signal is informational;
                enhancement acceptance is determined independently using
                image-quality validation.
              </p>
            </div>

          </div>
        </div>

        {/* WHY IT MATTERS */}
        <div className="mt-10 rounded-3xl border border-cyan-400/15 bg-gradient-to-br from-cyan-400/[0.06] to-transparent p-7 md:p-9">

          <p className="text-xs uppercase tracking-[0.2em] text-cyan-400 font-semibold">
            Why DermaLens matters
          </p>

          <h3 className="mt-3 text-2xl font-bold text-white">
            A preprocessing layer between the image and the AI model.
          </h3>

          <p className="mt-4 text-sm text-slate-400 leading-relaxed max-w-3xl">
            Dermatology AI systems depend on the quality of their input
            images. DermaLens is designed to sit before those systems:
            assessing image degradation, applying adaptive enhancement,
            validating the result, and providing a safer optimized input
            for downstream classification, detection or other AI tasks.
          </p>

          <div className="mt-7 grid md:grid-cols-5 gap-2 items-center">

            <FlowBox text="Raw Image" />

            <FlowArrow />

            <FlowBox text="DermaLens" active />

            <FlowArrow />

            <FlowBox text="Downstream AI" />

          </div>

        </div>

        {/* EVALUATION NOTE */}
        <div className="mt-8 text-center">
          <p className="text-xs text-slate-600 max-w-2xl mx-auto leading-relaxed">
            Current live metrics describe image-quality changes. Formal
            PSNR, SSIM, LPIPS and downstream task-performance evaluation
            belong to the experimental evaluation stage of the project.
          </p>
        </div>

      </div>
    </section>
  );
}

function ReferenceEvaluation({ evaluation, originalImage, degradedImage, enhancedImage }) {
  const psnr = evaluation.psnr || {};
  const ssim = evaluation.ssim || {};
  const lpips = evaluation.lpips || {};
  const number = (value, digits) => Number.isFinite(Number(value)) ? Number(value).toFixed(digits) : "—";
  const signed = (value, digits) => {
    if (!Number.isFinite(Number(value))) return "—";
    const n = Number(value);
    return `${n >= 0 ? "+" : ""}${n.toFixed(digits)}`;
  };

  return (
    <div className="mt-8 rounded-3xl border border-cyan-400/20 bg-cyan-400/[0.035] p-6 md:p-8">
      <SectionHeader
        eyebrow="REFERENCE EVALUATION"
        title="Reference-based image quality evaluation"
        description="Both the degraded input and DermaLens output are compared against the original clean image."
      />

      <div className="mt-5 overflow-x-auto">
        <table className="w-full min-w-[520px] text-left text-sm">
          <thead className="text-xs uppercase tracking-wider text-slate-500">
            <tr><th className="py-3">Metric</th><th>Degraded</th><th>DermaLens</th><th>Change</th></tr>
          </thead>
          <tbody className="divide-y divide-white/10 text-slate-200">
            <MetricRow label="PSNR (dB)" degraded={number(psnr.degraded_vs_original, 3)} enhanced={number(psnr.enhanced_vs_original, 3)} change={signed(psnr.change_db, 3)} />
            <MetricRow label="SSIM" degraded={number(ssim.degraded_vs_original, 4)} enhanced={number(ssim.enhanced_vs_original, 4)} change={signed(ssim.change, 4)} />
            <MetricRow label="LPIPS" degraded={number(lpips.degraded_vs_original, 4)} enhanced={number(lpips.enhanced_vs_original, 4)} change={signed(lpips.change, 4)} />
          </tbody>
        </table>
      </div>

      <div className="mt-6 grid md:grid-cols-3 gap-3">
        <ReferenceImage label="Original" source={originalImage} />
        <ReferenceImage label="Degraded" source={degradedImage} />
        <ReferenceImage label="DermaLens output" source={enhancedImage} />
      </div>

      <div className="mt-6 grid md:grid-cols-3 gap-3 text-xs text-slate-400 leading-relaxed">
        <p><strong className="text-white">PSNR:</strong> Pixel-level reconstruction fidelity. Higher is better.</p>
        <p><strong className="text-white">SSIM:</strong> Structural similarity to the reference. Higher is better.</p>
        <p><strong className="text-white">LPIPS:</strong> Learned perceptual similarity. Lower is better.</p>
      </div>
      <p className="mt-5 text-xs text-amber-200/80">These are image-quality metrics, not diagnostic accuracy metrics.</p>
    </div>
  );
}

function MetricRow({ label, degraded, enhanced, change }) {
  return <tr><td className="py-4 font-semibold text-white">{label}</td><td>{degraded}</td><td className="font-semibold text-cyan-300">{enhanced}</td><td className="text-cyan-300">{change}</td></tr>;
}

function ReferenceImage({ label, source }) {
  return <div className="overflow-hidden rounded-xl border border-white/10 bg-black"><p className="px-3 py-2 text-xs font-semibold text-white">{label}</p><img src={source} alt={label} className="h-48 w-full object-contain" /></div>;
}

function SectionHeader({ eyebrow, title, description }) {
  return (
    <div>
      <p className="text-xs uppercase tracking-[0.2em] text-cyan-400 font-semibold">
        {eyebrow}
      </p>

      <h3 className="mt-2 text-2xl font-bold text-white">
        {title}
      </h3>

      <p className="mt-2 text-sm text-slate-500 max-w-3xl leading-relaxed">
        {description}
      </p>
    </div>
  );
}

function MetricCard({
  title,
  before,
  after,
  multiplier,
  change,
  description
}) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/[0.025] p-5">

      <p className="text-sm font-semibold text-white">
        {title}
      </p>

      <div className="mt-5 flex items-end gap-3">

        <div>
          <p className="text-[10px] uppercase text-slate-600">
            Before
          </p>
          <p className="text-xl font-bold text-slate-300">
            {before}
          </p>
        </div>

        <span className="text-slate-600 mb-1">→</span>

        <div>
          <p className="text-[10px] uppercase text-cyan-500">
            After
          </p>
          <p className="text-xl font-bold text-cyan-300">
            {after}
          </p>
        </div>

      </div>

      {multiplier !== undefined && multiplier !== null && (
        <div className="mt-4 text-xs text-slate-500">
          Change factor:{" "}
          <span className="text-slate-300">
            {Number(multiplier).toFixed(2)}×
          </span>
        </div>
      )}

      {change !== undefined && change !== null && (
        <div className="mt-4 text-xs text-cyan-300">
          Improvement: {change}
        </div>
      )}

      <p className="mt-4 text-xs text-slate-600 leading-relaxed">
        {description}
      </p>
    </div>
  );
}

function ScoreValue({ label, value, highlight }) {
  return (
    <div>
      <p className="text-[10px] uppercase tracking-wider text-slate-600">
        {label}
      </p>

      <p
        className={`mt-1 text-lg font-bold ${
          highlight ? "text-cyan-300" : "text-slate-300"
        }`}
      >
        {value}
      </p>
    </div>
  );
}

function ValidationCard({ title, text }) {
  return (
    <div className="rounded-xl border border-white/10 bg-slate-950/50 p-4">
      <div className="w-7 h-7 rounded-full bg-cyan-400/10 border border-cyan-400/20 flex items-center justify-center text-cyan-400 text-xs">
        ✓
      </div>

      <p className="mt-3 text-sm font-semibold text-white">
        {title}
      </p>

      <p className="mt-1 text-xs text-slate-500">
        {text}
      </p>
    </div>
  );
}

function ConfidenceCard({ label, value, highlight }) {
  return (
    <div className="rounded-xl border border-white/10 bg-slate-950/50 p-5">
      <p className="text-xs text-slate-500">
        {label}
      </p>

      <p
        className={`mt-3 text-3xl font-bold ${
          highlight ? "text-cyan-300" : "text-white"
        }`}
      >
        {value}
      </p>
    </div>
  );
}

function FlowBox({ text, active }) {
  return (
    <div
      className={`rounded-xl border p-4 text-center text-xs font-semibold ${
        active
          ? "border-cyan-400/30 bg-cyan-400/10 text-cyan-300"
          : "border-white/10 bg-white/[0.025] text-slate-300"
      }`}
    >
      {text}
    </div>
  );
}

function FlowArrow() {
  return (
    <div className="text-center text-slate-600 hidden md:block">
      →
    </div>
  );
}

function cleanConfidenceText(text) {
  if (!text) return text;

  return text
    .replace(/AI classifier confidence changed by/gi, "Downstream model signal changed by")
    .replace(/AI classifier confidence remained unchanged/gi, "Downstream model signal remained unchanged");
}