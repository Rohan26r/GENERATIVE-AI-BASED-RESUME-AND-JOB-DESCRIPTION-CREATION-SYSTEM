import { useNavigate, useLocation } from "react-router-dom";
import { signOut } from "firebase/auth";
import { auth } from "../firebase";

export default function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();

  const links = [
    { label: "Dashboard", path: "/" },
    { label: "History", path: "/history" },
  ];

  return (
    <nav className="glass border-b border-white/10 px-6 py-4 flex justify-between items-center sticky top-0 z-50">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-lg gradient-btn flex items-center justify-center text-white font-bold text-sm shadow">
          R
        </div>
        <span className="font-bold gradient-text text-lg">Resume Matcher</span>
      </div>

      <div className="flex items-center gap-1">
        {links.map((l) => (
          <button
            key={l.path}
            onClick={() => navigate(l.path)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
              location.pathname === l.path
                ? "bg-purple-600/30 text-purple-300 border border-purple-500/30"
                : "text-slate-400 hover:text-white hover:bg-white/5"
            }`}
          >
            {l.label}
          </button>
        ))}
        <button
          onClick={() => signOut(auth)}
          className="ml-2 px-4 py-2 rounded-lg text-sm font-medium text-slate-400 hover:text-red-400 hover:bg-red-500/10 transition border border-transparent hover:border-red-500/20"
        >
          Sign Out
        </button>
      </div>
    </nav>
  );
}
