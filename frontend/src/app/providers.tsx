import { useEffect } from 'react';
import { RouterProvider } from 'react-router-dom';
import router from './router';
import { useAuthStore } from './store/auth';
import { useNotificationStore } from './store/notifications';

const Splash = () => (
  <div className="flex min-h-screen items-center justify-center bg-slate-100 text-brand">
    Loading SWMRA...
  </div>
);

const AppProviders = () => {
  const bootstrap = useAuthStore((state) => state.bootstrap);
  const initialized = useAuthStore((state) => state.initialized);
  const token = useAuthStore((state) => state.token);
  const connect = useNotificationStore((state) => state.connect);
  const loadNotifications = useNotificationStore((state) => state.bootstrap);

  useEffect(() => {
    bootstrap();
  }, [bootstrap]);

  useEffect(() => {
    if (!initialized) return;
    if (token) {
      loadNotifications().catch(() => undefined);
    } else {
      useNotificationStore.setState({ items: [], unread: 0 });
    }
  }, [initialized, token, loadNotifications]);

  useEffect(() => {
    connect(token);
  }, [token, connect]);

  useEffect(() => {
    const handler = () => useAuthStore.getState().logout();
    window.addEventListener('swmra:unauthorized', handler);
    return () => window.removeEventListener('swmra:unauthorized', handler);
  }, []);

  if (!initialized) return <Splash />;

  return <RouterProvider router={router} />;
};

export default AppProviders;