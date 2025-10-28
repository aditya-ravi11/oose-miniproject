import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Button from '../components/Button';
import Card from '../components/Card';
import Timeline from '../components/Timeline';
import { useRequestStore } from '../app/store/requests';

const cancellableStatuses = new Set(['draft', 'submitted', 'scheduled']);

const RequestDetail = () => {
  const { id } = useParams();
  const loadOne = useRequestStore((state) => state.loadOne);
  const cancel = useRequestStore((state) => state.cancel);
  const request = useRequestStore((state) => state.current);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    loadOne(id).finally(() => setLoading(false));
  }, [id, loadOne]);

  if (loading || !request) {
    return <p className="text-slate-500">Loading request...</p>;
  }

  const canCancel = cancellableStatuses.has(request.status);

  return (
    <div className="grid gap-6 md:grid-cols-2">
      <Card title={request.description}>
        <p className="text-sm text-slate-600">Category: {request.category}</p>
        <p className="text-sm text-slate-600">Quantity: {request.quantity}</p>
        <p className="text-sm text-slate-600">Status: {request.status}</p>
        <p className="mt-2 text-sm text-slate-600">Address: {request.address.line1}</p>

        {canCancel && (
          <Button variant="secondary" className="mt-4" onClick={() => id && cancel(id, 'Changed mind')}>
            Cancel request
          </Button>
        )}
      </Card>
      <Card title="Timeline">
        <Timeline events={request.events || []} />
      </Card>
    </div>
  );
};

export default RequestDetail;