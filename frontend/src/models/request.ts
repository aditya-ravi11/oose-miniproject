export type Address = {
  line1: string;
  line2?: string;
  city: string;
  pincode: string;
  lat?: number;
  lng?: number;
};

export type SlotWindow = {
  start: string;
  end: string;
};

export type RequestStatus =
  | 'draft'
  | 'submitted'
  | 'pending_review'
  | 'scheduled'
  | 'enroute'
  | 'onsite'
  | 'collecting'
  | 'collected'
  | 'handover'
  | 'verification'
  | 'completed'
  | 'cancelled'
  | 'failed';

export type PickupRequest = {
  id: number;
  user_id: number;
  category: 'organic' | 'recyclable' | 'hazardous' | 'e-waste' | 'bulk' | 'other';
  is_special: boolean;
  description: string;
  quantity: number;
  photos: string[];
  address: Address;
  preferred_slots: SlotWindow[];
  assigned_slot?: SlotWindow | null;
  status: RequestStatus;
  reward_points: number;
  events?: { type: string; at: string; by: string; data?: Record<string, unknown> }[];
  created_at?: string;
  updated_at?: string;
};

export type PaginatedRequests = {
  items: PickupRequest[];
  total: number;
  skip: number;
  limit: number;
};
