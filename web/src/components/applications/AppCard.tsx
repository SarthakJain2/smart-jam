import Badge from "../ui/Badge";
import { statusColor } from "../../lib/utils";

export default function AppCard({
  company,
  role,
  status,
}: {
  company: string;
  role: string;
  status: any;
}) {
  return (
    <div className="rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-3 shadow-sm">
      <div className="font-medium">{company}</div>
      <div className="text-sm text-gray-500">{role}</div>
      <div className="mt-2">
        <Badge className={statusColor[status]}>{status}</Badge>
      </div>
    </div>
  );
}
