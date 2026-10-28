import { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { useAuthState } from "../hooks/useAuthState";
import Navbar from "../components/Navbar";

export default function Dashboard() {
  const { user } = useAuthState();
  const [file, setFile] = useState(null);
  const [jobDesc, setJobDesc] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [dragOver, setDragOver] = useState(false);
  const fileRef = useRef();
  const navigate = useNavigate();

  function handleDrop(e) {
    e.preventDefault();
    setDragOver(false);
    const dropped = e.dataTransfer.files[0];
    if (dropped) setFile(dropped);
  }

  async function handleAnalyze(e) {
    e.preventDefault();
    if (!file || !jobDesc.trim()) {
      setError("Please upload a resume and paste a job description.");
      return;
    }
    setError("");
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("uid", user.uid);
      const uploadRes = await axios.post("/api/upload-resume", formData);
      const { file_path } = uploadRes.data;

      const analysisRes = await axios.post("/api/agent/full-analysis", {
        file_path,
        job_description: jobDesc,
        uid: user.uid,
      });
      navigate("/results", { state: { report: analysisRes.data.data } });
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen">
      {/* Ambient blobs */}
      <div className="fixed top-0 left-0 w-96 h-96 bg-purple-700 rounded-full opacity-10 blur-3xl pointer-events-none" />
      <div className="fixed bottom-0 right-0 w-80 h-80 bg-blue-600 rounded-full opacity-10 blur-3xl pointer-events-none" />

      <Navbar />

      <main className="max-w-3xl mx-auto px-4 py-12 relative z-10">
        {/* Hero */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 glass px-4 py-2 rounded-full text-xs text-purple-300 mb-4 border border-purple-500/20">
            <span className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
            MCP-Powered Analysis Engine
          </div>
          <h1 className="text-4xl font-bold text-white mb-3">
            Match Your Resume to{" "}
            <span className="gradient-text">Any Job</span>
          </h1>
          <p className="text-slate-400 text-base max-w-lg mx-auto">
            Upload your resume, paste a job description, and get an instant AI-powered match score with actionable improvements.
          </p>
        </div>

        {/* Stats row */}
        <div className="grid grid-cols-3 gap-4 mb-10">
          {[
            { label: "Match Score", icon: "🎯", desc: "Skills & experience" },
            { label: "ATS Check", icon: "🤖", desc: "Keyword analysis" },
            { label: "Skill Gap", icon: "📈", desc: "Learning roadmap" },
          ].map((s) => (
            <div key={s.label} className="glass rounded-2xl p-4 text-center card-glow cursor-default">
              <div className="text-2xl mb-1">{s.icon}</div>
              <div className="text-sm font-semibold text-white">{s.label}</div>
              <div className="text-xs text-slate-500 mt-0.5">{s.desc}</div>
            </div>
          ))}
        </div>

        <form onSubmit={handleAnalyze} className="space-y-5">
          {/* File upload */}
          <div
            onClick={() => fileRef.current.click()}
            onDrop={handleDrop}
            onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
            onDragLeave={() => setDragOver(false)}
            className={`glass rounded-2xl p-8 text-center cursor-pointer transition-all duration-300 ${
              dragOver
                ? "border-purple-400 bg-purple-500/10 scale-[1.01]"
                : "border-white/10 hover:border-purple-500/40 hover:bg-white/5"
            } border-2 border-dashed`}
          >
            <input
              ref={fileRef}
              type="file"
              accept=".pdf,.docx"
              className="hidden"
              onChange={(e) => setFile(e.target.files[0])}
            />
            {file ? (
              <div className="flex flex-col items-center gap-2">
                <div className="w-12 h-12 rounded-xl bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-2xl">
                  📄
                </div>
                <p className="text-emerald-400 font-semibold text-sm">{file.name}</p>
                <p className="text-slate-500 text-xs">{(file.size / 1024).toFixed(1)} KB — click to change</p>
              </div>
            ) : (
              <div className="flex flex-col items-center gap-3">
                <div className="w-14 h-14 rounded-2xl glass flex items-center justify-center text-3xl">
                  ☁️
                </div>
                <div>
                  <p className="text-white font-medium">Drop your resume here</p>
                  <p className="text-slate-500 text-sm mt-1">or click to browse — PDF or DOCX</p>
                </div>
              </div>
            )}
          </div>

          {/* Job description */}
          <div className="glass rounded-2xl p-1">
            <div className="flex items-center gap-2 px-4 pt-3 pb-1">
              <span className="text-base">💼</span>
              <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">Job Description</span>
            </div>
            <textarea
              value={jobDesc}
              onChange={(e) => setJobDesc(e.target.value)}
              placeholder="Paste the full job description here — the more detail, the better your match score..."
              rows={7}
              className="w-full bg-transparent px-4 py-2 text-sm text-white placeholder-slate-600 focus:outline-none resize-none"
            />
          </div>

          {error && (
            <div className="bg-red-500/10 border border-red-500/30 rounded-xl px-4 py-3 text-red-400 text-sm flex items-center gap-2">
              <span>⚠️</span> {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full gradient-btn text-white font-bold py-4 rounded-2xl shadow-xl text-base tracking-wide"
          >
            {loading ? (
              <span className="flex items-center justify-center gap-3">
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24" fill="none">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
                </svg>
                Running MCP Analysis Pipeline...
              </span>
            ) : (
              "⚡ Analyze Resume"
            )}
          </button>
        </form>
      </main>
    </div>
  );
}
