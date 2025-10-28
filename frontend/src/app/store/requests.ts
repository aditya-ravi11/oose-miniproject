import { create } from 'zustand';
import type { PaginatedRequests, PickupRequest } from '../../models';
import { cancelRequest, createRequest, fetchRequests, getRequest } from '../../api/requests';

type RequestState = {
  list?: PaginatedRequests;
  current?: PickupRequest;
  loading: boolean;
  error?: string;
};

type RequestActions = {
  load: (filters?: { status?: string; category?: string; page?: number }) => Promise<void>;
  loadOne: (id: string) => Promise<PickupRequest>;
  create: (payload: Parameters<typeof createRequest>[0]) => Promise<PickupRequest>;
  cancel: (id: string, reason?: string) => Promise<PickupRequest>;
};

export const useRequestStore = create<RequestState & RequestActions>((set) => ({
  list: undefined,
  current: undefined,
  loading: false,

  load: async (filters) => {
    set({ loading: true });
    try {
      const items = await fetchRequests(filters || {});
      set({ list: items });
    } finally {
      set({ loading: false });
    }
  },

  loadOne: async (id) => {
    set({ loading: true });
    try {
      const request = await getRequest(id);
      set({ current: request });
      return request;
    } finally {
      set({ loading: false });
    }
  },

  create: async (payload) => {
    set({ loading: true });
    try {
      const created = await createRequest(payload);
      set((state) => ({
        list: state.list
          ? { ...state.list, items: [created, ...state.list.items], total: state.list.total + 1 }
          : undefined,
      }));
      return created;
    } finally {
      set({ loading: false });
    }
  },

  cancel: async (id, reason) => {
    const cancelled = await cancelRequest(id, reason);
    set((state) => ({
      current: state.current && state.current.id === id ? cancelled : state.current,
      list: state.list
        ? {
            ...state.list,
            items: state.list.items.map((item) => (item.id === id ? cancelled : item)),
          }
        : undefined,
    }));
    return cancelled;
  },
}));