import Navbar from "../components/Navbar";
import UploadBox from "../components/UploadBox";

function Home() {
  return (
    <div className="min-h-screen bg-[#fafafa] text-[#111]">
      
      <Navbar />

      <div className="max-w-6xl mx-auto flex flex-col items-center justify-center text-center px-6 mt-28">
        {/* Label */}
  <p className="text-xs text-gray-500 uppercase tracking-wide mb-4">
    Dermatology AI Middleware
  </p>

        {/* Headline */}
        <h1 className="text-4xl md:text-5xl font-semibold max-w-2xl leading-tight">
          Poor medical images lead to unreliable AI decisions.
        </h1>

        {/* Subtext */}
        <p className="mt-6 text-gray-600 max-w-md text-lg">
          DermaLens enhances dermatology images before they reach diagnostic models, improving clarity and reliability.
        </p>

        {/* Button */}
        <UploadBox className="mt-10 px-6 py-3 border border-gray-300 rounded-md hover:bg-black hover:text-white transition">
  Upload Image
</UploadBox>

      </div>

    </div>
  );
}

export default Home;