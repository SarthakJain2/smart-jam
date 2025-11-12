import { NavLink } from "react-router-dom";
import { Briefcase, Gauge, Bot, LineChart, Settings, Sparkles } from "lucide-react";
import { cn } from "@/lib/utils";

const items = [
  { to: "/", label: "Dashboard", icon: Gauge },
  { to: "/applications", label: "Applications", icon: Briefcase },
  { to: "/matcher", label: "Matcher", icon: Bot },
  { to: "/analytics", label: "Analytics", icon: LineChart },
  { to: "/settings", label: "Settings", icon: Settings },
];

export default function Sidebar() {
  return (
    <aside className="hidden md:flex md:flex-col w-64 shrink-0 border-r border-border glass-card">
      {/* Logo */}
      <div className="px-4 py-6 flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary via-secondary to-accent flex items-center justify-center glow-primary">
          <Sparkles className="w-5 h-5 text-white" />
        </div>
        <div>
          <div className="text-lg font-bold gradient-text">Smart JAM</div>
          <div className="text-xs text-muted-foreground">v1.0</div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-2">
        {items.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              cn(
                "flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium transition-all duration-300",
                isActive
                  ? "bg-gradient-to-r from-primary via-secondary to-accent text-white glow-primary"
                  : "text-foreground hover:bg-muted/50"
              )
            }
          >
            <Icon size={18} />
            <span>{label}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
