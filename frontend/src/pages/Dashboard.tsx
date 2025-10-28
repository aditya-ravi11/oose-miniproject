import { useEffect } from 'react';
import { Link } from 'react-router-dom';
import Card from '../components/Card';
import EmptyState from '../components/EmptyState';
import { useRequestStore } from '../app/store/requests';

const Dashboard = () => {
  const load = useRequestStore((state) => state.load);
  const requests = useRequestStore((state) => state.list?.items || []);

  useEffect(() => {
    load({}).catch(() => undefined);
  }, [load]);

  const next = requests.find((req) => req.status === 'scheduled');

  return (
    <div className="space-y-6">
      <Card title="Next pickup">
        {next ? (
          <div>
            <p className="text-lg font-semibold text-slate-900">{next.description}</p>
            <p className="text-sm text-slate-500">{next.assigned_slot ? new Date(next.assigned_slot.start).toLocaleString() : 'Awaiting slot'}</p>
            <p className="mt-1 text-sm text-slate-600">{next.address.line1}</p>
          </div>
        ) : (
          <EmptyState title="No scheduled pickups" description="Create a new request to get started" />
        )}
      </Card>

      <Card title="Recent activity" action={<Link to="/requests" className="text-sm text-brand">View all</Link>}>
        <ul className="divide-y divide-slate-100">
          {requests.slice(0, 3).map((req) => (
            <li key={req.id} className="py-3">
              <p className="font-medium text-slate-900">{req.description}</p>
              <p className="text-sm text-slate-500">
                {req.status} · {new Date(req.created_at || new Date().toISOString()).toLocaleDateString()}
              </p>
            </li>
          ))}
          {requests.length === 0 && <p className="text-sm text-slate-500">You have no requests yet.</p>}
        </ul>
      </Card>
    </div>
  );
};

export default Dashboard;