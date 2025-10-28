export type Notification = {
  id?: string;
  _id?: string;
  user_id: string;
  channel: 'email' | 'sms' | 'push' | 'inapp';
  title: string;
  body: string;
  status: 'queued' | 'sent' | 'failed';
  meta?: Record<string, unknown>;
  created_at?: string;
  sent_at?: string | null;
};