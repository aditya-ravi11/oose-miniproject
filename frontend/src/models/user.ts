export type User = {
  id: number;
  name: string;
  email: string;
  phone?: string;
  role: 'citizen' | 'vendor' | 'admin';
};

export type TokenResponse = {
  access_token: string;
  token_type: string;
  user: User;
};
