'use client';

import { useQuery } from '@tanstack/react-query';
import { fetchAgents } from '@/lib/api';
import { AgentCard } from '@/components/AgentCard';
import Link from 'next/link';

export default function AgentsPage() {
  const { data: agents, isLoading, error } = useQuery({
    queryKey: ['agents'],
    queryFn: fetchAgents,
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
          <h1 className="text-4xl font-bold mb-2">Agents</h1>
          <p className="text-gray-600 dark:text-gray-400">
            Monitor and manage autonomous AI agents
          </p>
        </div>

        {isLoading && (
          <div className="text-center py-12">
            <div className="text-gray-500">Loading agents...</div>
          </div>
        )}

        {error && (
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 mb-6">
            <p className="text-red-800 dark:text-red-200">
              Error loading agents: {error instanceof Error ? error.message : 'Unknown error'}
            </p>
            <p className="text-sm text-red-600 dark:text-red-300 mt-2">
              Make sure the backend API is running on http://localhost:8000
            </p>
          </div>
        )}

        {agents && agents.agents.length === 0 && (
          <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6">
            <h3 className="font-semibold text-blue-800 dark:text-blue-200 mb-2">
              No Agents Registered
            </h3>
            <p className="text-blue-700 dark:text-blue-300">
              The API endpoints are ready, but agent registration needs to be implemented.
              Agents will appear here once registered with the OpenClaw network.
            </p>
          </div>
        )}

        {agents && agents.agents.length > 0 && (
          <>
            <div className="mb-4 text-sm text-gray-600 dark:text-gray-400">
              Showing {agents.agents.length} of {agents.total} agents
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {agents.agents.map((agent: any) => (
                <AgentCard key={agent.agent_id} agent={agent} />
              ))}
            </div>
          </>
        )}
      </div>
    </main>
  );
}
