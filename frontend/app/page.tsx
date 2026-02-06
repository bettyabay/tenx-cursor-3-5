'use client';

import Link from 'next/link';
import { useQuery } from '@tanstack/react-query';
import { fetchHealth, fetchTrends, fetchAgents } from '@/lib/api';
import { TrendCard } from '@/components/TrendCard';
import { AgentCard } from '@/components/AgentCard';
import { StatusBadge } from '@/components/StatusBadge';

export default function Home() {
  const { data: health, isLoading: healthLoading } = useQuery({
    queryKey: ['health'],
    queryFn: fetchHealth,
  });

  const { data: trends, isLoading: trendsLoading } = useQuery({
    queryKey: ['trends'],
    queryFn: fetchTrends,
  });

  const { data: agents, isLoading: agentsLoading } = useQuery({
    queryKey: ['agents'],
    queryFn: fetchAgents,
  });

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Project Chimera</h1>
          <p className="text-gray-600 dark:text-gray-400">
            Autonomous AI Influencer Factory Dashboard
          </p>
        </div>

        {/* Health Status */}
        <div className="mb-8">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h2 className="text-2xl font-semibold mb-4">System Status</h2>
            {healthLoading ? (
              <div className="text-gray-500">Loading...</div>
            ) : health ? (
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <StatusBadge status={health.status} />
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    API Version {health.version}
                  </span>
                </div>
                {health.services && (
                  <div className="mt-4 space-y-1">
                    <div className="text-sm">
                      Database:{' '}
                      <StatusBadge
                        status={health.services.database?.status || 'unknown'}
                      />
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="text-red-500">Unable to connect to API</div>
            )}
          </div>
        </div>

        {/* Navigation */}
        <div className="mb-8 flex gap-4">
          <Link
            href="/trends"
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition"
          >
            View Trends
          </Link>
          <Link
            href="/agents"
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition"
          >
            View Agents
          </Link>
          <Link
            href="/api/docs"
            target="_blank"
            className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition"
          >
            API Docs
          </Link>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {/* Trends Summary */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Trending Topics</h2>
            {trendsLoading ? (
              <div className="text-gray-500">Loading trends...</div>
            ) : trends && trends.trends.length > 0 ? (
              <div>
                <p className="text-2xl font-bold">{trends.total}</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Total trends found
                </p>
              </div>
            ) : (
              <div className="text-gray-500">
                No trends available. API endpoints are ready but need
                implementation.
              </div>
            )}
          </div>

          {/* Agents Summary */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Active Agents</h2>
            {agentsLoading ? (
              <div className="text-gray-500">Loading agents...</div>
            ) : agents && agents.agents.length > 0 ? (
              <div>
                <p className="text-2xl font-bold">{agents.total}</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Registered agents
                </p>
              </div>
            ) : (
              <div className="text-gray-500">
                No agents registered yet. Agent registration pending.
              </div>
            )}
          </div>
        </div>

        {/* Recent Trends */}
        {trends && trends.trends.length > 0 && (
          <div className="mb-8">
            <h2 className="text-2xl font-semibold mb-4">Recent Trends</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {trends.trends.slice(0, 6).map((trend: any) => (
                <TrendCard key={trend.trend_id} trend={trend} />
              ))}
            </div>
          </div>
        )}

        {/* Active Agents */}
        {agents && agents.agents.length > 0 && (
          <div>
            <h2 className="text-2xl font-semibold mb-4">Active Agents</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {agents.agents.map((agent: any) => (
                <AgentCard key={agent.agent_id} agent={agent} />
              ))}
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
