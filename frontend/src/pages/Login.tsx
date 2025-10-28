import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { z } from 'zod';
import Button from '../components/Button';
import { useAuthStore } from '../app/store/auth';

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(6),
});

type FormValues = z.infer<typeof schema>;

const Login = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const login = useAuthStore((state) => state.login);
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({ resolver: zodResolver(schema) });

  const onSubmit = async (values: FormValues) => {
    await login(values.email, values.password);
    const redirect = (location.state as { from?: { pathname: string } })?.from?.pathname || '/';
    navigate(redirect);
  };

  return (
    <div className="flex min-h-screen bg-slate-50">
      <div className="m-auto w-full max-w-md rounded-3xl border border-slate-100 bg-white p-10 shadow-xl">
        <h1 className="text-2xl font-semibold text-slate-900">Sign in</h1>
        <p className="text-sm text-slate-500">Access your recycling dashboard</p>
        <form onSubmit={handleSubmit(onSubmit)} className="mt-8 space-y-4">
          <div>
            <label className="text-sm font-medium text-slate-700">Email</label>
            <input className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2" type="email" {...register('email')} />
            {errors.email && <p className="text-xs text-rose-500">{errors.email.message}</p>}
          </div>
          <div>
            <label className="text-sm font-medium text-slate-700">Password</label>
            <input className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2" type="password" {...register('password')} />
            {errors.password && <p className="text-xs text-rose-500">{errors.password.message}</p>}
          </div>
          <Button disabled={isSubmitting} type="submit" className="w-full">
            {isSubmitting ? 'Signing in...' : 'Sign in'}
          </Button>
        </form>
        <p className="mt-6 text-sm text-slate-500">
          No account? <Link to="/signup" className="text-brand">Create one</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;