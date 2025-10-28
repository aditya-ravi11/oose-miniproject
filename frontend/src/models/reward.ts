export type Reward = {
  id: string;
  user_id: string;
  points: number;
  reason: string;
  created_at: string;
};

export type RewardSummary = {
  total_points: number;
  recent: Reward[];
};