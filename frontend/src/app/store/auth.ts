import { create } from 'zustand';
import { login as apiLogin, me, signup as apiSignup } from '../../api/auth';
import type { TokenResponse, User } from '../../models';

type AuthState = {
  user?: User;
  token?: string;
  loading: boolean;
  initialized: boolean;
  error?: string;
};

type AuthActions = {
  bootstrap: () => Promise<void>;
  login: (email: string, password: string) => Promise<TokenResponse>;
  signup: (payload: { name: string; email: string; phone: string; password: string }) => Promise<TokenResponse>;
  logout: () => void;
};

const persistToken = (token?: string) => {
  if (token) {
    localStorage.setItem('swmra_token', token);
  } else {
    localStorage.removeItem('swmra_token');
  }
};

export const useAuthStore = create<AuthState & AuthActions>((set, get) => ({
  user: undefined,
  token: localStorage.getItem('swmra_token') || undefined,
  loading: false,
  initialized: false,
  error: undefined,

  bootstrap: async () => {
    const token = get().token;
    if (!token) {
      set({ initialized: true });
      return;
    }
    set({ loading: true });
    try {
      const profile = await me();
      set({ user: profile, initialized: true, loading: false });
    } catch (error) {
      persistToken(undefined);
      set({ user: undefined, token: undefined, initialized: true, loading: false });
    }
  },

  login: async (email, password) => {
    set({ loading: true, error: undefined });
    try {
      const response = await apiLogin({ email, password });
      persistToken(response.access_token);
      set({ user: response.user, token: response.access_token, loading: false });
      return response;
    } catch (error: any) {
      set({ loading: false, error: error?.message || 'Unable to login' });
      throw error;
    }
  },

  signup: async (payload) => {
    set({ loading: true, error: undefined });
    try {
      const response = await apiSignup(payload);
      persistToken(response.access_token);
      set({ user: response.user, token: response.access_token, loading: false });
      return response;
    } catch (error: any) {
      set({ loading: false, error: error?.message || 'Unable to signup' });
      throw error;
    }
  },

  logout: () => {
    persistToken(undefined);
    set({ user: undefined, token: undefined });
  },
}));