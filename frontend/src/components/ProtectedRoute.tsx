import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuthStore } from '../app/store/auth';

const ProtectedRoute = () => {
  const user = useAuthStore((state) => state.user);
  const token = useAuthStore((state) => state.token);
  const location = useLocation();

  if (!token || !user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <Outlet />;
};

export default ProtectedRoute;