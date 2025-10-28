import client from './client';
import type { Notification } from '../models';

export const fetchNotifications = async () => {
  const { data } = await client.get<Notification[]>('/notifications');
  return data;
};