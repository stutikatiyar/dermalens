function Navbar() {
  return (
    <nav className="w-full border-b border-white/10 bg-[#020617]/80 backdrop-blur-xl sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">

        {/* Logo */}
        <div className="flex items-center gap-3">
          <div className="h-3 w-3 rounded-full bg-blue-500 shadow-[0_0_20px_rgba(59,130,246,0.8)]"></div>

          <h1 className="text-xl font-semibold tracking-tight text-white">
            DermaLens
          </h1>

          <span className="text-xs px-2 py-1 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 font-mono">
            AI
          </span>
        </div>

        {/* Links */}
        <div className="flex items-center gap-8 text-sm text-slate-400 font-medium">

          <span className="hover:text-white transition cursor-pointer">
            Product
          </span>

          <span className="hover:text-white transition cursor-pointer">
            Docs
          </span>

          <span className="hover:text-white transition cursor-pointer">
            Demo
          </span>

          {/* CTA */}
          <button className="px-4 py-2 rounded-xl bg-blue-500 text-white hover:bg-blue-400 transition shadow-lg shadow-blue-500/20">
            Launch
          </button>
        </div>

      </div>
    </nav>
  );
}

export default Navbar;