export default function HeroSection() {
  return (
    <section className="relative z-10 px-6 pt-16 pb-12">
      <div className="max-w-7xl mx-auto">
        <div className="grid lg:grid-cols-2 gap-12 items-center">

          {/* LEFT */}
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-cyan-400/20 bg-cyan-400/5 text-cyan-300 text-xs font-medium mb-6">
              <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-pulse" />
              AI IMAGE-QUALITY MIDDLEWARE
            </div>

            <h1 className="text-5xl md:text-6xl font-bold tracking-tight text-white leading-[1.05]">
              Prepare Dermatology
              <span className="block text-cyan-400">
                Images for Better AI.
              </span>
            </h1>

            <p className="mt-6 text-lg md:text-xl text-slate-300 leading-relaxed max-w-2xl">
              DermaLens is an AI-powered image-quality middleware that
              analyzes, enhances, and validates dermatological images
              before they reach downstream AI models.
            </p>

            <div className="mt-6 p-4 rounded-xl border border-white/10 bg-white/[0.03] max-w-2xl">
              <div className="flex gap-3">
                <div className="text-cyan-400 text-lg">ⓘ</div>

                <div>
                  <p className="text-sm font-semibold text-white">
                    Not a diagnostic model.
                  </p>

                  <p className="text-sm text-slate-400 mt-1 leading-relaxed">
                    DermaLens improves the image input — it does not
                    diagnose skin conditions or replace a downstream
                    dermatology AI system.
                  </p>
                </div>
              </div>
            </div>

            <div className="mt-8 flex flex-wrap gap-3">
              {[
                "Quality Analysis",
                "Adaptive Enhancement",
                "Validation Gate",
                "Downstream AI Ready"
              ].map((item) => (
                <div
                  key={item}
                  className="px-3 py-2 rounded-lg border border-white/10 bg-white/[0.025] text-xs text-slate-300"
                >
                  {item}
                </div>
              ))}
            </div>
          </div>

          {/* RIGHT — PIPELINE */}
          <div className="relative">
            <div className="absolute inset-0 bg-cyan-500/10 blur-3xl rounded-full" />

            <div className="relative rounded-3xl border border-white/10 bg-slate-950/80 backdrop-blur-xl p-6 shadow-2xl">

              <div className="flex items-center justify-between mb-6">
                <div>
                  <p className="text-xs text-slate-500 uppercase tracking-widest">
                    DermaLens Pipeline
                  </p>
                  <p className="text-sm text-slate-300 mt-1">
                    Image → optimized AI input
                  </p>
                </div>

                <div className="w-10 h-10 rounded-xl bg-cyan-400/10 border border-cyan-400/20 flex items-center justify-center text-cyan-400">
                  ✦
                </div>
              </div>

              <div className="space-y-3">

                <PipelineStep
                  number="01"
                  title="Raw Dermatology Image"
                  description="Original image received"
                />

                <Arrow />

                <PipelineStep
                  number="02"
                  title="Quality Analysis"
                  description="Blur • illumination • contrast • noise"
                />

                <Arrow />

                <PipelineStep
                  number="03"
                  title="Adaptive Enhancement"
                  description="Generate and compare restoration candidates"
                  active
                />

                <Arrow />

                <PipelineStep
                  number="04"
                  title="Validation Gate"
                  description="Check structure, noise, brightness & artifacts"
                />

                <Arrow />

                <PipelineStep
                  number="05"
                  title="Downstream AI"
                  description="Prepared image can be passed to another model"
                />

              </div>

              <div className="mt-6 pt-5 border-t border-white/10">
                <p className="text-xs text-slate-500 leading-relaxed">
                  Enhancement is accepted only when the validation criteria
                  indicate that the candidate is beneficial and safe.
                </p>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>
  );
}

function PipelineStep({ number, title, description, active }) {
  return (
    <div
      className={`flex items-center gap-4 p-4 rounded-xl border transition ${
        active
          ? "border-cyan-400/30 bg-cyan-400/[0.07]"
          : "border-white/10 bg-white/[0.02]"
      }`}
    >
      <div
        className={`w-9 h-9 rounded-lg flex items-center justify-center text-xs font-bold ${
          active
            ? "bg-cyan-400 text-slate-950"
            : "bg-white/5 text-slate-400"
        }`}
      >
        {number}
      </div>

      <div className="min-w-0">
        <p className="text-sm font-semibold text-white">
          {title}
        </p>

        <p className="text-xs text-slate-500 mt-0.5">
          {description}
        </p>
      </div>
    </div>
  );
}

function Arrow() {
  return (
    <div className="flex justify-center text-slate-600 text-sm">
      ↓
    </div>
  );
}