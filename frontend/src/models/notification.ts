export type Notification = {
  id: number;
  user_id: number;
  channel: 'email' | 'sms' | 'push' | 'inapp';
  title: string;
  body: string;
  status: 'queued' | 'sent' | 'failed';
  meta?: Record<string, unknown>;
  created_at?: string;
  sent_at?: string | null;
};
