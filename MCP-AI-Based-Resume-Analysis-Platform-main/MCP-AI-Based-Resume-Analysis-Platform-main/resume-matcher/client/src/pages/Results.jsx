import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import {
  RadialBarChart, RadialBar, ResponsiveContainer,
  BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, Cell,
} from "recharts";
import Navbar from "../components/Navbar";

// ── Sub-components ────────────────────────────────────────────────────────────

function ScoreRing({ score, label, color }) {
  return (
    <div className="glass rounded-2xl p-6 flex flex-col items-center card-glow">
      <div className="relative w-32 h-32">
        <ResponsiveContainer width="100%" height="100%">
          <RadialBarChart innerRadius="70%" outerRadius="100%" data={[{ value: score, fill: color }]} startAngle={90} endAngle={-270}>
            <RadialBar dataKey="value" cornerRadius={6} background={{ fill: "rgba(255,255,255,0.05)" }} />
          </RadialBarChart>
        </ResponsiveContainer>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-3xl font-bold text-white">{score}</span>
          <span className="text-xs text-slate-400">/100</span>
        </div>
      </div>
      <p className="text-sm font-semibold text-slate-300 mt-3">{label}</p>
    </div>
  );
}

function RatingBadge({ rating }) {
  const map = { Excellent: "from-emerald-500 to-teal-400", Good: "from-blue-500 to-cyan-400", Moderate: "from-yellow-500 to-orange-400", Weak: "from-red-500 to-pink-400" };
  return (
    <div className="glass rounded-2xl p-6 flex flex-col items-center justify-center card-glow">
      <div className={`text-3xl font-black bg-gradient-to-r ${map[rating] || map.Weak} bg-clip-text text-transparent`}>{rating}</div>
      <p className="text-sm font-semibold text-slate-300 mt-2">Overall Rating</p>
      <div className={`mt-3 h-1.5 w-20 rounded-full bg-gradient-to-r ${map[rating] || map.Weak} opacity-60`} />
    </div>
  );
}

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload?.length) {
    return (
      <div className="glass rounded-xl px-3 py-2 text-xs text-white border border-white/10">
        <p className="font-semibold">{label}</p>
        <p className="text-purple-300">{payload[0].value} pts</p>
      </div>
    );
  }
  return null;
};

function Tag({ text, color = "purple" }) {
  const colors = {
    purple: "bg-purple-500/15 text-purple-300 border-purple-500/25",
    green: "bg-emerald-500/15 text-emerald-300 border-emerald-500/25",
    red: "bg-red-500/15 text-red-300 border-red-500/25",
    blue: "bg-blue-500/15 text-blue-300 border-blue-500/25",
    yellow: "bg-yellow-500/15 text-yellow-300 border-yellow-500/25",
  };
  return <span className={`px-3 py-1 rounded-full text-xs font-medium border ${colors[color]}`}>{text}</span>;
}

function SectionHeader({ dot, title }) {
  const dotColors = { purple: "bg-purple-400", green: "bg-emerald-400", blue: "bg-blue-400", yellow: "bg-yellow-400", cyan: "bg-cyan-400", red: "bg-red-400" };
  return (
    <h3 className="font-semibold text-white mb-4 flex items-center gap-2">
      <span className={`w-2 h-2 rounded-full ${dotColors[dot] || "bg-purple-400"}`} />
      {title}
    </h3>
  );
}

// ── Tab panels ────────────────────────────────────────────────────────────────

function RecruiterTab({ data, match }) {
  if (!data) return <p className="text-slate-500 text-sm">No recruiter data available.</p>;
  const probColor = data.hiring_probability?.startsWith("High") ? "green" : data.hiring_probability?.startsWith("Moderate") ? "yellow" : "red";
  return (
    <div className="space-y-5">
      <div className="glass rounded-2xl p-5">
        <SectionHeader dot="purple" title="Recruiter Verdict" />
        <p className="text-slate-300 text-sm leading-relaxed">{data.verdict}</p>
        <div className="mt-3 flex items-center gap-3">
          <span className="text-xs text-slate-500">Hiring Probability:</span>
          <Tag text={data.hiring_probability} color={probColor} />
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="glass rounded-2xl p-5">
          <SectionHeader dot="green" title="Strengths" />
          <ul className="space-y-2">
            {(data.strengths || []).map((s, i) => (
              <li key={i} className="flex gap-2 text-sm text-slate-300"><span className="text-emerald-400 mt-0.5">✓</span>{s}</li>
            ))}
          </ul>
        </div>
        <div className="glass rounded-2xl p-5">
          <SectionHeader dot="red" title="Weaknesses" />
          <ul className="space-y-2">
            {(data.weaknesses || []).map((w, i) => (
              <li key={i} className="flex gap-2 text-sm text-slate-300"><span className="text-red-400 mt-0.5">✗</span>{w}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

function ATSTab({ data }) {
  if (!data) return <p className="text-slate-500 text-sm">No ATS data available.</p>;
  return (
    <div className="space-y-5">
      <div className="glass rounded-2xl p-5">
        <SectionHeader dot="yellow" title="ATS Verdict" />
        <p className="text-slate-300 text-sm">{data.ats_verdict}</p>
      </div>
      {data.issues?.length > 0 && (
        <div className="glass rounded-2xl p-5">
          <SectionHeader dot="yellow" title="Issues & Fixes" />
          <div className="space-y-3">
            {data.issues.map((issue, i) => (
              <div key={i} className="bg-yellow-500/5 border border-yellow-500/15 rounded-xl px-4 py-3">
                <p className="text-sm text-slate-200 flex gap-2"><span className="text-yellow-400">⚠</span>{issue}</p>
                {data.recommendations?.[i] && (
                  <p className="text-xs text-slate-500 mt-1 ml-5"><span className="text-purple-400">→</span> {data.recommendations[i]}</p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
      {data.improved_summary && (
        <div className="glass rounded-2xl p-5">
          <SectionHeader dot="blue" title="Improved Summary" />
          <p className="text-sm text-slate-300 bg-blue-500/5 border border-blue-500/20 rounded-xl p-4 leading-relaxed">{data.improved_summary}</p>
        </div>
      )}
      {data.improved_skills?.length > 0 && (
        <div className="glass rounded-2xl p-5">
          <SectionHeader dot="green" title="Suggested Skills Section" />
          <div className="flex flex-wrap gap-2">{data.improved_skills.map(s => <Tag key={s} text={s} color="purple" />)}</div>
        </div>
      )}
    </div>
  );
}

function CoachTab({ data }) {
  if (!data) return <p className="text-slate-500 text-sm">No coaching data available.</p>;
  const priorityColor = { High: "red", Medium: "yellow", Low: "blue" };
  return (
    <div className="space-y-5">
      <div className="glass rounded-2xl p-5">
        <SectionHeader dot="cyan" title="Coach Summary" />
        <p className="text-slate-300 text-sm leading-relaxed">{data.coaching_summary}</p>
        {data.top_priorities?.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-2">
            <span className="text-xs text-slate-500 self-center">Top priorities:</span>
            {data.top_priorities.map(s => <Tag key={s} text={s} color="red" />)}
          </div>
        )}
      </div>
      {data.roadmap_30_days?.length > 0 && (
        <div className="glass rounded-2xl p-5">
          <SectionHeader dot="purple" title="30-Day Learning Roadmap" />
          <div className="space-y-3">
            {data.roadmap_30_days.map((item, i) => (
              <div key={i} className="flex gap-4 items-start bg-white/3 border border-white/8 rounded-xl px-4 py-3">
                <div className="shrink-0 text-center">
                  <div className="w-8 h-8 rounded-lg gradient-btn flex items-center justify-center text-white text-xs font-bold">{i + 1}</div>
                </div>
                <div className="min-w-0">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="text-sm font-semibold text-white capitalize">{item.skill}</span>
                    <Tag text={item.priority} color={priorityColor[item.priority] || "blue"} />
                    <span className="text-xs text-slate-500">{item.week}</span>
                  </div>
                  <p className="text-xs text-slate-500 mt-1">{item.action}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
      {data.learning_resources?.length > 0 && (
        <div className="glass rounded-2xl p-5">
          <SectionHeader dot="cyan" title="Learning Resources" />
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {data.learning_resources.map((item, i) => (
              <a key={i} href={item.resource?.startsWith("http") ? item.resource : "#"} target="_blank" rel="noreferrer"
                className="flex items-center gap-3 bg-white/3 hover:bg-white/6 border border-white/8 hover:border-purple-500/30 rounded-xl px-4 py-3 transition group">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-500/30 to-blue-500/30 flex items-center justify-center text-sm font-bold text-purple-300 shrink-0">
                  {item.skill?.[0]?.toUpperCase()}
                </div>
                <div className="min-w-0">
                  <p className="text-sm font-medium text-white capitalize">{item.skill}</p>
                  <p className="text-xs text-slate-500 truncate group-hover:text-purple-400 transition">{item.resource}</p>
                </div>
              </a>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function InterviewTab({ data }) {
  if (!data) return <p className="text-slate-500 text-sm">No interview data available.</p>;
  return (
    <div className="space-y-5">
      {data.preparation_note && (
        <div className="glass rounded-2xl p-5">
          <SectionHeader dot="blue" title="Preparation Focus" />
          <p className="text-slate-300 text-sm">{data.preparation_note}</p>
        </div>
      )}
      {data.technical_questions?.length > 0 && (
        <div className="glass rounded-2xl p-5">
          <SectionHeader dot="purple" title="Technical Questions" />
          <div className="space-y-2">
            {data.technical_questions.map((q, i) => (
              <div key={i} className="flex gap-3 bg-purple-500/5 border border-purple-500/15 rounded-xl px-4 py-3">
                <span className="text-purple-400 font-bold text-xs shrink-0 mt-0.5">Q{i + 1}</span>
                <p className="text-sm text-slate-300">{q}</p>
              </div>
            ))}
          </div>
        </div>
      )}
      {data.hr_questions?.length > 0 && (
        <div className="glass rounded-2xl p-5">
          <SectionHeader dot="cyan" title="HR / Behavioral Questions" />
          <div className="space-y-2">
            {data.hr_questions.map((q, i) => (
              <div key={i} className="flex gap-3 bg-cyan-500/5 border border-cyan-500/15 rounded-xl px-4 py-3">
                <span className="text-cyan-400 font-bold text-xs shrink-0 mt-0.5">HR</span>
                <p className="text-sm text-slate-300">{q}</p>
              </div>
            ))}
          </div>
        </div>
      )}
      {data.mock_tips?.length > 0 && (
        <div className="glass rounded-2xl p-5">
          <SectionHeader dot="green" title="Mock Interview Tips" />
          <ul className="space-y-2">
            {data.mock_tips.map((tip, i) => (
              <li key={i} className="flex gap-2 text-sm text-slate-300"><span className="text-emerald-400 shrink-0">💡</span>{tip}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

function FinalReportTab({ data }) {
  if (!data) return <p className="text-slate-500 text-sm">No final report available.</p>;
  const readinessColor = { High: "emerald", "Medium-High": "blue", Medium: "yellow", Low: "red" };
  const rc = readinessColor[data.readiness_level] || "blue";
  const gradMap = { emerald: "from-emerald-500 to-teal-400", blue: "from-blue-500 to-cyan-400", yellow: "from-yellow-500 to-orange-400", red: "from-red-500 to-pink-400" };
  return (
    <div className="space-y-5">
      <div className="glass rounded-2xl p-6 text-center">
        <p className="text-xs text-slate-500 uppercase tracking-wider mb-2">Final Verdict</p>
        <p className="text-lg font-bold text-white leading-snug">{data.final_verdict}</p>
        <div className={`inline-block mt-3 px-4 py-1.5 rounded-full text-sm font-semibold bg-gradient-to-r ${gradMap[rc]} text-white`}>
          Readiness: {data.readiness_level}
        </div>
      </div>
      <div className="glass rounded-2xl p-5">
        <SectionHeader dot="blue" title="Recommended Action" />
        <p className="text-slate-300 text-sm leading-relaxed">{data.recommended_action}</p>
      </div>
      {data.summary_points?.length > 0 && (
        <div className="glass rounded-2xl p-5">
          <SectionHeader dot="purple" title="AI Summary" />
          <ul className="space-y-3">
            {data.summary_points.map((pt, i) => (
              <li key={i} className="flex gap-3 text-sm text-slate-300 bg-white/3 border border-white/8 rounded-xl px-4 py-3">
                <span className="text-purple-400 shrink-0">→</span>{pt}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

// ── Main Results page ─────────────────────────────────────────────────────────

const TABS = [
  { id: "recruiter", label: "👔 Recruiter", dot: "purple" },
  { id: "ats", label: "🤖 ATS", dot: "yellow" },
  { id: "coach", label: "📈 Roadmap", dot: "cyan" },
  { id: "interview", label: "🎤 Interview", dot: "blue" },
  { id: "report", label: "📋 Final Report", dot: "green" },
];

const barColors = ["#a78bfa", "#60a5fa", "#34d399"];

export default function Results() {
  const { state } = useLocation();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState("recruiter");

  const report = state?.report;

  if (!report) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center gap-4">
        <div className="text-6xl">🔍</div>
        <p className="text-slate-400 text-lg">No report data found.</p>
        <button onClick={() => navigate("/")} className="gradient-btn px-6 py-2 rounded-xl text-white text-sm font-medium">Go back</button>
      </div>
    );
  }

  const { match, ats_review, recruiter_review, roadmap, interview_questions, final_report, job } = report;

  // Support both old (ats) and new (ats_review) field names for backwards compat
  const atsData = ats_review || report.ats;
  const matchData = match || {};

  const breakdownData = matchData.breakdown
    ? Object.entries(matchData.breakdown).map(([k, v]) => ({ name: k.replace("_score", "").replace("_", " "), value: v }))
    : [];

  return (
    <div className="min-h-screen">
      <div className="fixed top-0 right-0 w-96 h-96 bg-purple-700 rounded-full opacity-10 blur-3xl pointer-events-none" />
      <div className="fixed bottom-0 left-0 w-80 h-80 bg-blue-600 rounded-full opacity-10 blur-3xl pointer-events-none" />

      <Navbar />

      <main className="max-w-5xl mx-auto px-4 py-10 relative z-10 space-y-6 pb-20">
        {/* Header */}
        <div className="flex items-center justify-between flex-wrap gap-3">
          <div>
            <h2 className="text-3xl font-bold text-white">Analysis Results</h2>
            <p className="text-slate-400 text-sm mt-1">
              Role: <span className="text-purple-300 font-medium">{job?.role || "—"}</span>
            </p>
          </div>
          <button onClick={() => navigate("/")} className="glass px-4 py-2 rounded-xl text-sm text-slate-300 hover:text-white border border-white/10 hover:border-purple-500/30 transition">
            ← New Analysis
          </button>
        </div>

        {/* Score cards */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <ScoreRing score={matchData.score ?? 0} label="Match Score" color="#a78bfa" />
          <ScoreRing score={atsData?.ats_score ?? 0} label="ATS Score" color="#34d399" />
          <RatingBadge rating={matchData.rating ?? "Weak"} />
        </div>

        {/* Breakdown chart */}
        {breakdownData.length > 0 && (
          <div className="glass rounded-2xl p-6">
            <SectionHeader dot="purple" title="Score Breakdown" />
            <ResponsiveContainer width="100%" height={180}>
              <BarChart data={breakdownData} barSize={40}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                <XAxis dataKey="name" tick={{ fill: "#94a3b8", fontSize: 12 }} axisLine={false} tickLine={false} />
                <YAxis domain={[0, 50]} tick={{ fill: "#94a3b8", fontSize: 11 }} axisLine={false} tickLine={false} />
                <Tooltip content={<CustomTooltip />} cursor={{ fill: "rgba(255,255,255,0.03)" }} />
                <Bar dataKey="value" radius={[6, 6, 0, 0]}>
                  {breakdownData.map((_, i) => <Cell key={i} fill={barColors[i % barColors.length]} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Agent tabs */}
        <div className="glass rounded-2xl overflow-hidden">
          {/* Tab bar */}
          <div className="flex overflow-x-auto border-b border-white/10 scrollbar-none">
            {TABS.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-5 py-4 text-sm font-medium whitespace-nowrap transition flex-shrink-0 ${
                  activeTab === tab.id
                    ? "text-white border-b-2 border-purple-400 bg-purple-500/10"
                    : "text-slate-400 hover:text-white hover:bg-white/5"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* Tab content */}
          <div className="p-6">
            {activeTab === "recruiter" && <RecruiterTab data={recruiter_review} match={matchData} />}
            {activeTab === "ats" && <ATSTab data={atsData} />}
            {activeTab === "coach" && <CoachTab data={roadmap} />}
            {activeTab === "interview" && <InterviewTab data={interview_questions} />}
            {activeTab === "report" && <FinalReportTab data={final_report} />}
          </div>
        </div>
      </main>
    </div>
  );
}
