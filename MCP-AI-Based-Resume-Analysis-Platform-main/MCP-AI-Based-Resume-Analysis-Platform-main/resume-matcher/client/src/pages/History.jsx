import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { useAuthState } from "../hooks/useAuthState";
import Navbar from "../components/Navbar";

function RatingDot({ rating }) {
  const map = {
    Excellent: "bg-emerald-400",
    Good: "bg-blue-400",
    Moderate: "bg-yellow-400",
    Weak: "bg-red-400",
  };
  return <span className={`w-2 h-2 rounded-full ${map[rating] || "bg-slate-400"}`} />;
}

export default function History() {
  const { user } = useAuthState();
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    if (!user) return;
    axios.get(`/api/history/${user.uid}`)
      .then((res) => setReports(res.data.reports || []))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [user]);

  return (
    <div className="min-h-screen">
      <div className="fixed top-0 left-1/2 w-96 h-96 bg-purple-700 rounded-full opacity-10 blur-3xl pointer-events-none -translate-x-1/2" />

      <Navbar />

      <main className="max-w-3xl mx-auto px-4 py-10 relative z-10">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-white">Analysis History</h2>
          <p className="text-slate-400 text-sm mt-1">Your past resume analyses</p>
        </div>

        {loading && (
          <div className="flex items-center justify-center py-20">
            <svg className="animate-spin h-8 w-8 text-purple-400" viewBox="0 0 24 24" fill="none">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
            </svg>
          </div>
        )}

        {!loading && reports.length === 0 && (
          <div className="glass rounded-2xl p-16 text-center">
            <div className="text-5xl mb-4">📭</div>
            <p className="text-slate-400 font-medium">No analyses yet</p>
            <p className="text-slate-600 text-sm mt-1 mb-6">Run your first resume analysis to see results here</p>
            <button
              onClick={() => navigate("/")}
              className="gradient-btn px-6 py-2.5 rounded-xl text-white text-sm font-semibold"
            >
              Start Analyzing
            </button>
          </div>
        )}

        <div className="space-y-3">
          {reports.map((r, i) => (
            <div
              key={r.id}
              onClick={() => navigate("/results", { state: { report: r } })}
              className="glass rounded-2xl p-5 cursor-pointer hover:border-purple-500/30 border border-white/10 transition-all duration-200 card-glow group"
            >
              <div className="flex justify-between items-start">
                <div className="flex items-start gap-3">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500/30 to-blue-500/30 flex items-center justify-center text-white font-bold text-sm shrink-0 mt-0.5">
                    {i + 1}
                  </div>
                  <div>
                    <p className="font-semibold text-white group-hover:text-purple-300 transition">
                      {r.job?.role || "Resume Analysis"}
                    </p>
                    <p className="text-xs text-slate-500 mt-0.5">
                      {r.created_at ? new Date(r.created_at).toLocaleDateString("en-US", {
                        year: "numeric", month: "short", day: "numeric",
                      }) : "—"}
                    </p>
                    {r.resume?.name && (
                      <p className="text-xs text-slate-600 mt-0.5">👤 {r.resume.name}</p>
                    )}
                  </div>
                </div>

                <div className="flex items-center gap-3 shrink-0">
                  <div className="text-right">
                    <div className="flex items-center gap-1.5 justify-end">
                      <RatingDot rating={r.match?.rating} />
                      <span className="text-sm font-bold text-white">{r.match?.score ?? "—"}</span>
                    </div>
                    <p className="text-xs text-slate-500">Match</p>
                  </div>
                  <div className="w-px h-8 bg-white/10" />
                  <div className="text-right">
                    <span className="text-sm font-bold text-emerald-400">{r.ats?.ats_score ?? "—"}</span>
                    <p className="text-xs text-slate-500">ATS</p>
                  </div>
                  <div className="text-slate-600 group-hover:text-purple-400 transition text-lg ml-1">→</div>
                </div>
              </div>

              {/* Skill pills preview */}
              {r.match?.matched_skills?.length > 0 && (
                <div className="flex flex-wrap gap-1.5 mt-3 pt-3 border-t border-white/5">
                  {r.match.matched_skills.slice(0, 5).map((s) => (
                    <span key={s} className="text-xs px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                      {s}
                    </span>
                  ))}
                  {r.match.matched_skills.length > 5 && (
                    <span className="text-xs px-2 py-0.5 rounded-full glass text-slate-500">
                      +{r.match.matched_skills.length - 5} more
                    </span>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
