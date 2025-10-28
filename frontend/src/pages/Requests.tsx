import { useEffect } from 'react';
import RequestCard from '../components/RequestCard';
import EmptyState from '../components/EmptyState';
import { useRequestStore } from '../app/store/requests';

const Requests = () => {
  const load = useRequestStore((state) => state.load);
  const list = useRequestStore((state) => state.list);

  useEffect(() => {
    load({}).catch(() => undefined);
  }, [load]);

  if (!list || list.items.length === 0) {
    return <EmptyState title="No requests" description="Create your first pickup request" />;
  }

  return (
    <div className="grid gap-4">
      {list.items.map((request) => (
        <RequestCard key={request.id} request={request} />
      ))}
    </div>
  );
};

export default Requests;