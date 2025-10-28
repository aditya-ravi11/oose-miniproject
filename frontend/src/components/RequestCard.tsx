import { Link } from 'react-router-dom';
import type { PickupRequest } from '../models';

const statusColors: Record<string, string> = {
  scheduled: 'bg-emerald-50 text-emerald-700',
  submitted: 'bg-sky-50 text-sky-700',
  completed: 'bg-indigo-50 text-indigo-700',
  cancelled: 'bg-rose-50 text-rose-700',
};

const RequestCard = ({ request }: { request: PickupRequest }) => (
  <Link to={`/requests/${request.id}`} className="block rounded-2xl border border-slate-100 bg-white p-4 shadow-sm hover:border-brand">
    <div className="flex items-center justify-between">
      <div>
        <p className="text-sm uppercase text-slate-500">{request.category}</p>
        <p className="text-lg font-semibold text-slate-900">{request.description}</p>
      </div>
      <span className={`rounded-full px-3 py-1 text-xs font-medium ${statusColors[request.status] || 'bg-slate-100 text-slate-700'}`}>
        {request.status}
      </span>
    </div>
    <p className="mt-2 text-sm text-slate-600">
      Preferred slots: {request.preferred_slots.map((slot) => new Date(slot.start).toLocaleString()).join(', ')}
    </p>
  </Link>
);

export default RequestCard;