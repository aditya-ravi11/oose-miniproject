import { useEffect, useState } from 'react';
import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { fetchRewardSummary } from '../api/rewards';
import { useAuthStore } from '../app/store/auth';
import NotificationBell from './NotificationBell';

const links = [
  { to: '/', label: 'Dashboard' },
  { to: '/requests', label: 'Requests' },
  { to: '/requests/new', label: 'New Request' },
];

const AppLayout = () => {
  const user = useAuthStore((state) => state.user);
  const logout = useAuthStore((state) => state.logout);
  const navigate = useNavigate();
  const [points, setPoints] = useState(0);

  useEffect(() => {
    fetchRewardSummary()
      .then((summary) => setPoints(summary.total_points))
      .catch(() => undefined);
  }, []);

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="bg-white shadow">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <div>
            <p className="text-sm text-slate-500">Welcome back</p>
            <h1 className="text-xl font-semibold text-slate-900">{user?.name}</h1>
          </div>
          <div className="flex items-center gap-4">
            <div className="rounded-lg bg-emerald-50 px-3 py-1 text-sm font-medium text-emerald-700">{points} pts</div>
            <NotificationBell />
            <button
              className="rounded-md border border-slate-200 px-3 py-1 text-sm text-slate-600"
              onClick={() => {
                logout();
                navigate('/login');
              }}
            >
              Logout
            </button>
          </div>
        </div>
      </header>
      <nav className="mx-auto flex max-w-6xl gap-4 px-6 py-3">
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            className={({ isActive }) =>
              `rounded-full px-3 py-1 text-sm ${isActive ? 'bg-brand text-white' : 'text-slate-600 hover:bg-slate-100'}`
            }
            end={link.to === '/'}
          >
            {link.label}
          </NavLink>
        ))}
      </nav>
      <main className="mx-auto max-w-6xl px-6 py-6">
        <Outlet />
      </main>
    </div>
  );
};

export default AppLayout;