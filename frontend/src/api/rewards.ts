import client from './client';
import type { RewardSummary } from '../models';

export const fetchRewardSummary = async () => {
  const { data } = await client.get<RewardSummary>('/rewards/summary');
  return data;
};