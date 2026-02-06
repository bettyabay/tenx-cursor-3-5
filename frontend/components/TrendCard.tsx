import { Trend } from '@/lib/api';

interface TrendCardProps {
  trend: Trend;
}

export function TrendCard({ trend }: TrendCardProps) {
  const platformColors: Record<string, string> = {
    twitter: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    tiktok: 'bg-black text-white',
    instagram: 'bg-gradient-to-r from-purple-500 to-pink-500 text-white',
  };

  const platformColor = platformColors[trend.platform.toLowerCase()] || 'bg-gray-100 text-gray-800';

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 hover:shadow-lg transition">
      <div className="flex items-start justify-between mb-3">
        <h3 className="font-semibold text-lg line-clamp-2">{trend.topic_name}</h3>
        <span className={`px-2 py-1 rounded text-xs font-medium ${platformColor}`}>
          {trend.platform}
        </span>
      </div>

      {trend.relevance_score !== undefined && (
        <div className="mb-3">
          <div className="flex items-center justify-between text-sm mb-1">
            <span className="text-gray-600 dark:text-gray-400">Relevance</span>
            <span className="font-medium">{(trend.relevance_score * 100).toFixed(0)}%</span>
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <div
              className="bg-primary-600 h-2 rounded-full"
              style={{ width: `${trend.relevance_score * 100}%` }}
            />
          </div>
        </div>
      )}

      <div className="space-y-2 text-sm">
        <div className="flex justify-between">
          <span className="text-gray-600 dark:text-gray-400">Velocity</span>
          <span className="font-medium">{trend.trend_velocity.toFixed(1)}/hr</span>
        </div>

        {trend.engagement_metrics && (
          <div className="grid grid-cols-3 gap-2 pt-2 border-t border-gray-200 dark:border-gray-700">
            {trend.engagement_metrics.likes !== undefined && (
              <div>
                <div className="text-gray-600 dark:text-gray-400 text-xs">Likes</div>
                <div className="font-medium">{trend.engagement_metrics.likes.toLocaleString()}</div>
              </div>
            )}
            {trend.engagement_metrics.shares !== undefined && (
              <div>
                <div className="text-gray-600 dark:text-gray-400 text-xs">Shares</div>
                <div className="font-medium">{trend.engagement_metrics.shares.toLocaleString()}</div>
              </div>
            )}
            {trend.engagement_metrics.comments !== undefined && (
              <div>
                <div className="text-gray-600 dark:text-gray-400 text-xs">Comments</div>
                <div className="font-medium">{trend.engagement_metrics.comments.toLocaleString()}</div>
              </div>
            )}
          </div>
        )}

        {trend.related_hashtags && trend.related_hashtags.length > 0 && (
          <div className="pt-2 border-t border-gray-200 dark:border-gray-700">
            <div className="flex flex-wrap gap-1">
              {trend.related_hashtags.slice(0, 3).map((tag, idx) => (
                <span
                  key={idx}
                  className="px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded text-xs"
                >
                  {tag}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
