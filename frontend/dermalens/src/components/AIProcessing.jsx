import { useEffect, useState } from "react";

export default function AIProcessing() {
  const steps = [
    {
      title: "Assessing image quality",
      description: "Measuring image condition and degradation signals"
    },
    {
      title: "Detecting image degradation",
      description: "Checking illumination, blur, contrast and noise"
    },
    {
      title: "Generating enhancement candidates",
      description: "Testing adaptive restoration strategies"
    },
    {
      title: "Running validation gate",
      description: "Checking structure, artifacts and image safety"
    },
    {
      title: "Selecting optimal output",
      description: "Choosing enhancement or preserving the original"
    },
    {
      title: "Preparing downstream AI input",
      description: "Final image ready for model evaluation"
    }
  ];

  const [active, setActive] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setActive((prev) =>
        prev < steps.length - 1 ? prev + 1 : prev
      );
    }, 850);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="rounded-3xl border border-cyan-400/20 bg-slate-950/80 backdrop-blur-xl p-8 md:p-10 shadow-2xl">

      <div className="text-center mb-10">

        <div className="mx-auto w-14 h-14 rounded-2xl bg-cyan-400/10 border border-cyan-400/20 flex items-center justify-center text-cyan-400 text-xl animate-pulse">
          ✦
        </div>

        <h2 className="mt-5 text-2xl font-bold text-white">
          DermaLens is processing the image
        </h2>

        <p className="mt-2 text-sm text-slate-500">
          Evaluating image quality before downstream AI processing
        </p>

      </div>

      <div className="max-w-2xl mx-auto space-y-3">

        {steps.map((step, index) => {
          const completed = index < active;
          const current = index === active;

          return (
            <div
              key={step.title}
              className={`flex items-center gap-4 rounded-xl border p-4 transition-all duration-500 ${
                current
                  ? "border-cyan-400/30 bg-cyan-400/[0.06]"
                  : completed
                  ? "border-white/10 bg-white/[0.025]"
                  : "border-white/5 bg-white/[0.015] opacity-45"
              }`}
            >

              <div
                className={`w-9 h-9 shrink-0 rounded-lg flex items-center justify-center text-xs font-bold ${
                  completed
                    ? "bg-cyan-400 text-slate-950"
                    : current
                    ? "border border-cyan-400 text-cyan-400"
                    : "bg-white/5 text-slate-600"
                }`}
              >
                {completed ? "✓" : `0${index + 1}`}
              </div>

              <div className="flex-1">
                <p className="text-sm font-semibold text-white">
                  {step.title}
                </p>

                <p className="text-xs text-slate-500 mt-1">
                  {step.description}
                </p>
              </div>

              {current && (
                <div className="flex gap-1">
                  <span className="w-1 h-1 rounded-full bg-cyan-400 animate-bounce" />
                  <span className="w-1 h-1 rounded-full bg-cyan-400 animate-bounce [animation-delay:100ms]" />
                  <span className="w-1 h-1 rounded-full bg-cyan-400 animate-bounce [animation-delay:200ms]" />
                </div>
              )}

            </div>
          );
        })}

      </div>

      <div className="max-w-2xl mx-auto mt-8 pt-6 border-t border-white/10 text-center">
        <p className="text-xs text-slate-500">
          Enhancement acceptance is based on image-quality validation,
          not classifier confidence.
        </p>
      </div>

    </div>
  );
}