import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#0B1120] text-white">

      <nav className="fixed top-0 w-full backdrop-blur-xl bg-white/5 border-b border-white/10 z-50">
        <div className="max-w-7xl mx-auto flex justify-between items-center px-8 py-4">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent">
            AgaraMart
          </h1>

          <div className="flex gap-4">
            <Link href="/login">
              <button className="px-5 py-2 rounded-xl border border-white/20 hover:bg-white/10 transition">
                Login
              </button>
            </Link>

            <Link href="/register">
              <button className="px-5 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-purple-600">
                Register
              </button>
            </Link>
          </div>
        </div>
      </nav>

      <section className="min-h-screen flex flex-col justify-center items-center text-center px-6">

        <div className="absolute w-96 h-96 bg-cyan-500/20 blur-[120px] rounded-full" />

        <div className="absolute right-20 w-96 h-96 bg-purple-500/20 blur-[120px] rounded-full" />

        <h1 className="text-6xl md:text-8xl font-bold mb-6">
          Future of
          <span className="block bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent">
            Shopping
          </span>
        </h1>

        <p className="text-gray-400 text-lg max-w-2xl">
          A premium multi-vendor e-commerce platform powered by
          FastAPI, PostgreSQL, Razorpay and Next.js.
        </p>

        <div className="flex gap-5 mt-10">
          <Link href="/products">
            <button className="px-8 py-4 rounded-2xl bg-gradient-to-r from-cyan-500 to-purple-600">
              Explore Products
            </button>
          </Link>

          <Link href="/login">
            <button className="px-8 py-4 rounded-2xl border border-white/20 backdrop-blur-lg">
              Sign In
            </button>
          </Link>
        </div>

      </section>

    </main>
  );
}