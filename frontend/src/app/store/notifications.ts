import { create } from 'zustand';
import type { Notification } from '../../models';
import { fetchNotifications } from '../../api/notifications';

type NotificationState = {
  items: Notification[];
  unread: number;
  socket?: WebSocket;
};

type NotificationActions = {
  bootstrap: () => Promise<void>;
  connect: (token?: string) => void;
  markRead: () => void;
};

export const useNotificationStore = create<NotificationState & NotificationActions>((set, get) => ({
  items: [],
  unread: 0,

  bootstrap: async () => {
    if (!localStorage.getItem('swmra_token')) {
      set({ items: [], unread: 0 });
      return;
    }
    const items = await fetchNotifications();
    set({ items, unread: 0 });
  },

  connect: (token) => {
    const existing = get().socket;
    if (existing) {
      existing.close();
    }
    if (!token) {
      set({ socket: undefined });
      return;
    }
    const base = (import.meta.env.VITE_API_BASE || 'http://localhost:8000').replace('http', 'ws');
    const socket = new WebSocket(`${base}/ws/notifications?token=${token}`);
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      set((state) => ({ items: [data, ...state.items], unread: state.unread + 1 }));
    };
    socket.onclose = () => set({ socket: undefined });
    set({ socket });
  },

  markRead: () => set({ unread: 0 }),
}));