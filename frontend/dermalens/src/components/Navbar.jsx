function Navbar() {
  return (
    <div className="w-full border-b border-gray-200 bg-white">
      <div className="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
        
        {/* Logo */}
        <h1 className="text-lg font-semibold tracking-tight">
          DermaLens
        </h1>

        {/* Links */}
        <div className="flex items-center gap-8 text-sm text-gray-600">
          <span className="hover:text-black cursor-pointer">Product</span>
          <span className="hover:text-black cursor-pointer">Docs</span>
          <span className="hover:text-black cursor-pointer">Demo</span>
        </div>

      </div>
    </div>
  );
}

export default Navbar;