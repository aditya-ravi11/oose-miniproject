import client from './client';
import type { TokenResponse, User } from '../models';

export type LoginPayload = { email: string; password: string };
export type SignupPayload = { name: string; email: string; phone: string; password: string };

export const login = async (payload: LoginPayload): Promise<TokenResponse> => {
  const { data } = await client.post<TokenResponse>('/auth/login', payload);
  return data;
};

export const signup = async (payload: SignupPayload): Promise<TokenResponse> => {
  const { data } = await client.post<TokenResponse>('/auth/register', payload);
  return data;
};

export const me = async (): Promise<User> => {
  const { data } = await client.get<User>('/auth/me');
  return data;
};