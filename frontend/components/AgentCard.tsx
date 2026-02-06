import { Agent } from '@/lib/api';
import { StatusBadge } from './StatusBadge';

interface AgentCardProps {
  agent: Agent;
}

export function AgentCard({ agent }: AgentCardProps) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 hover:shadow-lg transition">
      <div className="flex items-start justify-between mb-3">
        <div>
          <h3 className="font-semibold text-lg">{agent.name || agent.agent_id}</h3>
          <p className="text-sm text-gray-600 dark:text-gray-400">{agent.agent_id}</p>
        </div>
        <StatusBadge status={agent.status} />
      </div>

      {agent.capabilities && agent.capabilities.length > 0 && (
        <div className="mb-3">
          <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Capabilities</div>
          <div className="flex flex-wrap gap-1">
            {agent.capabilities.map((capability, idx) => (
              <span
                key={idx}
                className="px-2 py-1 bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-200 rounded text-xs"
              >
                {capability}
              </span>
            ))}
          </div>
        </div>
      )}

      <div className="space-y-1 text-sm">
        <div className="flex items-center gap-2">
          <span className="text-gray-600 dark:text-gray-400">OpenClaw</span>
          {agent.openclaw_registered ? (
            <span className="text-green-600 dark:text-green-400">✓ Registered</span>
          ) : (
            <span className="text-gray-400">Not registered</span>
          )}
        </div>
        {agent.last_heartbeat && (
          <div className="text-xs text-gray-500 dark:text-gray-400">
            Last heartbeat: {new Date(agent.last_heartbeat).toLocaleString()}
          </div>
        )}
      </div>
    </div>
  );
}
