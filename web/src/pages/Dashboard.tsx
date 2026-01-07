import { Card, CardContent, CardHeader } from "../components/ui/Card";
import MiniArea from "../components/charts/MiniArea";
import Donut from "../components/charts/Donut";
import { useApplications } from "../hooks/useApplications";
import { Briefcase, Award, Calendar, ClipboardCheck } from "lucide-react";

export default function Dashboard() {
  const { apps } = useApplications();
  const rows = apps.data || [];
  const counts: Record<string, number> = rows.reduce((acc: any, r) => {
    acc[r.status] = (acc[r.status] || 0) + 1;
    return acc;
  }, {});
  const donut = Object.entries(counts).map(([name, value]) => ({
    name,
    value,
  }));
  const weekly = Array.from({ length: 7 }).map((_, i) => ({
    name: `D${i + 1}`,
    value: Math.floor(Math.random() * 5),
  }));

  const stats = [
    { 
      label: "Applications", 
      value: rows.length, 
      icon: Briefcase, 
      gradient: "from-primary to-secondary",
      data: weekly 
    },
    { 
      label: "Offers", 
      value: counts["Offer"] || 0, 
      icon: Award, 
      gradient: "from-secondary to-accent" 
    },
    { 
      label: "Interviews", 
      value: counts["Interview"] || 0, 
      icon: Calendar, 
      gradient: "from-accent to-primary" 
    },
    { 
      label: "OAs", 
      value: counts["OA"] || 0, 
      icon: ClipboardCheck, 
      gradient: "from-primary to-accent" 
    },
  ];

  return (
    <div className="p-6 space-y-6 animate-fade-in">
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {stats.map((stat, index) => (
          <Card
            key={stat.label}
            className="group glass-card border-border/50 hover:border-border hover:glow-primary transition-all duration-500 overflow-hidden relative animate-fade-in-up"
            style={{ animationDelay: `${index * 100}ms` }}
          >
            <div className={`absolute inset-0 bg-gradient-to-br ${stat.gradient} opacity-0 group-hover:opacity-5 transition-opacity duration-500`} />
            
            <CardHeader className="relative z-10">{stat.label}</CardHeader>
            <CardContent className="relative z-10">
              <div className="flex items-start justify-between">
                <div className="text-4xl font-bold text-foreground">{stat.value}</div>
                <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${stat.gradient} flex items-center justify-center transform group-hover:scale-110 transition-transform duration-300`}>
                  <stat.icon className="w-6 h-6 text-white" />
                </div>
              </div>
              {stat.data && (
                <div className="mt-4">
                  <MiniArea data={stat.data} />
                </div>
              )}
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="glass-card border-border/50 hover:border-border hover:glow-accent transition-all duration-500">
          <CardHeader>Status Distribution</CardHeader>
          <CardContent>
            <Donut data={donut} />
          </CardContent>
        </Card>
        
        <Card className="glass-card border-border/50 hover:border-border hover:glow-accent transition-all duration-500">
          <CardHeader>Upcoming Deadlines</CardHeader>
          <CardContent>
            <ul className="space-y-3">
              {rows
                .filter((r) => !!r.deadline)
                .slice(0, 5)
                .map((r) => (
                  <li
                    key={r.id}
                    className="flex items-center justify-between border-b border-border/30 pb-3 hover:border-border transition-colors duration-300"
                  >
                    <span className="font-semibold text-foreground">{r.company}</span>
                    <span className="text-sm text-muted-foreground">
                      {new Date(r.deadline!).toLocaleString()}
                    </span>
                  </li>
                ))}
              {rows.filter((r) => !!r.deadline).length === 0 && (
                <div className="text-center py-8 text-muted-foreground">
                  No upcoming deadlines.
                </div>
              )}
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
