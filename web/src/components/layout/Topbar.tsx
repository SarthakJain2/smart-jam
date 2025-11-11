import ThemeToggle from "./ThemeToggle";
import { useTheme } from "@/hooks/useTheme";
import { useAuth } from "@/hooks/useAuth";
import { Button } from "@/components/ui/button";

export default function Topbar() {
  const { dark, setDark } = useTheme();
  const { logout } = useAuth();
  
  return (
    <header className="h-16 border-b border-border glass-card backdrop-blur-xl flex items-center justify-between px-6">
      <div className="text-lg font-semibold">
        <span className="text-foreground">Welcome </span>
        <span className="gradient-text">👋</span>
      </div>
      <div className="flex items-center gap-3">
        <ThemeToggle dark={dark} setDark={setDark} />
        <Button
          className="bg-muted/50 hover:bg-muted text-foreground border border-border/50 hover:border-border transition-all duration-300"
          onClick={logout}
        >
          Logout
        </Button>
      </div>
    </header>
  );
}
