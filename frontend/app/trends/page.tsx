'use client';

import { useQuery } from '@tanstack/react-query';
import { fetchTrends } from '@/lib/api';
import { TrendCard } from '@/components/TrendCard';
import Link from 'next/link';

export default function TrendsPage() {
  const { data: trends, isLoading, error } = useQuery({
    queryKey: ['trends'],
    queryFn: fetchTrends,
  });

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-6">
          <Link
            href="/"
            className="text-primary-600 hover:text-primary-700 mb-4 inline-block"
          >
            ← Back to Dashboard
          </Link>
          <h1 className="text-4xl font-bold mb-2">Trending Topics</h1>
          <p className="text-gray-600 dark:text-gray-400">
            Discover trending topics across social media platforms
          </p>
        </div>

        {isLoading && (
          <div className="text-center py-12">
            <div className="text-gray-500">Loading trends...</div>
          </div>
        )}

        {error && (
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 mb-6">
            <p className="text-red-800 dark:text-red-200">
              Error loading trends: {error instanceof Error ? error.message : 'Unknown error'}
            </p>
            <p className="text-sm text-red-600 dark:text-red-300 mt-2">
              Make sure the backend API is running on http://localhost:8000
            </p>
          </div>
        )}

        {trends && trends.trends.length === 0 && (
          <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-6">
            <h3 className="font-semibold text-yellow-800 dark:text-yellow-200 mb-2">
              No Trends Available
            </h3>
            <p className="text-yellow-700 dark:text-yellow-300">
              The API endpoints are ready, but trend data needs to be implemented.
              The backend is connected and responding correctly.
            </p>
          </div>
        )}

        {trends && trends.trends.length > 0 && (
          <>
            <div className="mb-4 text-sm text-gray-600 dark:text-gray-400">
              Showing {trends.trends.length} of {trends.total} trends
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {trends.trends.map((trend: any) => (
                <TrendCard key={trend.trend_id} trend={trend} />
              ))}
            </div>
          </>
        )}
      </div>
    </main>
  );
}
