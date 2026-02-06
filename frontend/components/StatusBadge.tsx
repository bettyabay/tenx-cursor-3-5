interface StatusBadgeProps {
  status: string;
}

export function StatusBadge({ status }: StatusBadgeProps) {
  const statusColors: Record<string, string> = {
    healthy: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    healthy: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    online: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    available: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    busy: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
    degraded: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
    offline: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200',
    unhealthy: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
    disconnected: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
  };

  const colorClass =
    statusColors[status.toLowerCase()] ||
    'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200';

  return (
    <span
      className={`px-2 py-1 rounded text-xs font-medium capitalize ${colorClass}`}
    >
      {status}
    </span>
  );
}
