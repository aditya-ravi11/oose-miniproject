import { useState } from 'react';
import { useNotificationStore } from '../app/store/notifications';

const NotificationBell = () => {
  const { items, unread, markRead } = useNotificationStore((state) => ({
    items: state.items,
    unread: state.unread,
    markRead: state.markRead,
  }));
  const [open, setOpen] = useState(false);

  return (
    <div className="relative">
      <button
        onClick={() => {
          setOpen((prev) => !prev);
          markRead();
        }}
        className="relative rounded-full bg-slate-100 p-2 text-slate-600"
        aria-label="Notifications"
      >
        <span role="img" aria-hidden="true">
          ??
        </span>
        {unread > 0 && (
          <span className="absolute -right-1 -top-1 inline-flex h-4 w-4 items-center justify-center rounded-full bg-rose-500 text-xs text-white">
            {unread}
          </span>
        )}
      </button>
      {open && (
        <div className="absolute right-0 z-20 mt-2 w-64 rounded-lg border border-slate-200 bg-white p-3 shadow-xl">
          <p className="mb-2 text-sm font-semibold text-slate-700">Notifications</p>
          <div className="max-h-64 space-y-2 overflow-y-auto">
            {items.length === 0 && <p className="text-sm text-slate-500">No notifications yet.</p>}
            {items.map((item, idx) => (
              <div key={item.id || item._id || idx} className="rounded-md bg-slate-50 p-2 text-sm">
                <p className="font-medium text-slate-800">{item.title}</p>
                <p className="text-slate-600">{item.body}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default NotificationBell;