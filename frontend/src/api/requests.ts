import client from './client';
import type { PaginatedRequests, PickupRequest } from '../models';

export type RequestPayload = {
  category: PickupRequest['category'];
  is_special: boolean;
  description: string;
  quantity: number;
  address: PickupRequest['address'];
  preferred_slots: PickupRequest['preferred_slots'];
  photos: string[];
};

export const fetchRequests = async (params: { status?: string; category?: string; page?: number }) => {
  const { data } = await client.get<PaginatedRequests>('/requests', {
    params: {
      status: params.status,
      category: params.category,
      skip: ((params.page || 1) - 1) * 20,
    },
  });
  return data;
};

export const createRequest = async (payload: RequestPayload) => {
  const { data } = await client.post<PickupRequest>('/requests', payload);
  return data;
};

export const getRequest = async (id: string) => {
  const { data } = await client.get<PickupRequest>(`/requests/${id}`);
  return data;
};

export const cancelRequest = async (id: string, reason?: string) => {
  const { data } = await client.post<PickupRequest>(`/requests/${id}/cancel`, { reason });
  return data;
};

export const confirmSlot = async (id: string, slot_start: string, slot_end: string) => {
  const { data } = await client.post<PickupRequest>(`/requests/${id}/confirm-slot`, { slot_start, slot_end });
  return data;
};

export const availableSlots = async (date: string, category: string) => {
  const { data } = await client.get(`/slots/available`, { params: { date, category } });
  return data as { start: string; end: string }[];
};