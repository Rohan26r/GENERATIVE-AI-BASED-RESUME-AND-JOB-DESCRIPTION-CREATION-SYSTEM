import { useState } from "react";
import { signInWithEmailAndPassword, createUserWithEmailAndPassword } from "firebase/auth";
import { useNavigate } from "react-router-dom";
import { auth } from "../firebase";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isRegister, setIsRegister] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      if (isRegister) {
        await createUserWithEmailAndPassword(auth, email, password);
      } else {
        await signInWithEmailAndPassword(auth, email, password);
      }
      navigate("/");
    } catch (err) {
      setError(err.message.replace("Firebase: ", "").replace(/\(auth.*\)\.?/, ""));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4 relative overflow-hidden">
      {/* Ambient blobs */}
      <div className="absolute top-[-10%] left-[-10%] w-96 h-96 bg-purple-600 rounded-full opacity-20 blur-3xl pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-5%] w-80 h-80 bg-blue-500 rounded-full opacity-20 blur-3xl pointer-events-none" />
      <div className="absolute top-[40%] right-[20%] w-64 h-64 bg-emerald-500 rounded-full opacity-10 blur-3xl pointer-events-none" />

      <div className="glass-strong rounded-3xl p-8 w-full max-w-md relative z-10 shadow-2xl">
        {/* Logo */}
        <div className="flex items-center gap-3 mb-8">
          <div className="w-10 h-10 rounded-xl gradient-btn flex items-center justify-center text-white font-bold text-lg shadow-lg">
            R
          </div>
          <div>
            <h1 className="text-xl font-bold gradient-text">Resume Matcher</h1>
            <p className="text-xs text-slate-400">AI-powered career intelligence</p>
          </div>
        </div>

        <h2 className="text-2xl font-bold text-white mb-1">
          {isRegister ? "Create account" : "Welcome back"}
        </h2>
        <p className="text-slate-400 text-sm mb-7">
          {isRegister ? "Start matching your resume today" : "Sign in to your dashboard"}
        </p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-1">
            <label className="text-xs text-slate-400 font-medium uppercase tracking-wider">Email</label>
            <input
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full glass rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition text-sm"
            />
          </div>
          <div className="space-y-1">
            <label className="text-xs text-slate-400 font-medium uppercase tracking-wider">Password</label>
            <input
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full glass rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500 transition text-sm"
            />
          </div>

          {error && (
            <div className="bg-red-500/10 border border-red-500/30 rounded-xl px-4 py-3 text-red-400 text-sm">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full gradient-btn text-white font-semibold py-3 rounded-xl shadow-lg text-sm mt-2"
          >
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
                </svg>
                {isRegister ? "Creating account..." : "Signing in..."}
              </span>
            ) : (
              isRegister ? "Create Account" : "Sign In"
            )}
          </button>
        </form>

        <div className="mt-6 text-center">
          <span className="text-slate-500 text-sm">
            {isRegister ? "Already have an account? " : "Don't have an account? "}
          </span>
          <button
            onClick={() => { setIsRegister(!isRegister); setError(""); }}
            className="text-purple-400 hover:text-purple-300 text-sm font-medium transition"
          >
            {isRegister ? "Sign In" : "Register"}
          </button>
        </div>

        {/* Feature pills */}
        <div className="mt-8 pt-6 border-t border-white/10 flex flex-wrap gap-2 justify-center">
          {["ATS Check", "Match Score", "Skill Gap", "AI Suggestions"].map((f) => (
            <span key={f} className="text-xs px-3 py-1 rounded-full glass text-slate-400">{f}</span>
          ))}
        </div>
      </div>
    </div>
  );
}
