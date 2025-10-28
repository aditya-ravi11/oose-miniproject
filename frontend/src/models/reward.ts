export type Reward = {
  id: number;
  user_id: number;
  points: number;
  reason: string;
  created_at: string;
};

export type RewardSummary = {
  total_points: number;
  recent: Reward[];
};
