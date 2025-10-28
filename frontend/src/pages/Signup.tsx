import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { Link, useNavigate } from 'react-router-dom';
import { z } from 'zod';
import Button from '../components/Button';
import { useAuthStore } from '../app/store/auth';

const schema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
  phone: z.string().min(8),
  password: z.string().min(6),
});

type FormValues = z.infer<typeof schema>;

const Signup = () => {
  const signup = useAuthStore((state) => state.signup);
  const navigate = useNavigate();
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({ resolver: zodResolver(schema) });

  const onSubmit = async (values: FormValues) => {
    await signup(values);
    navigate('/');
  };

  return (
    <div className="flex min-h-screen bg-slate-50">
      <div className="m-auto w-full max-w-lg rounded-3xl border border-slate-100 bg-white p-10 shadow-xl">
        <h1 className="text-2xl font-semibold text-slate-900">Create account</h1>
        <p className="text-sm text-slate-500">Join the recycling movement</p>
        <form onSubmit={handleSubmit(onSubmit)} className="mt-8 grid gap-4">
          <div>
            <label className="text-sm font-medium text-slate-700">Name</label>
            <input className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2" {...register('name')} />
            {errors.name && <p className="text-xs text-rose-500">{errors.name.message}</p>}
          </div>
          <div>
            <label className="text-sm font-medium text-slate-700">Email</label>
            <input className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2" type="email" {...register('email')} />
            {errors.email && <p className="text-xs text-rose-500">{errors.email.message}</p>}
          </div>
          <div>
            <label className="text-sm font-medium text-slate-700">Phone</label>
            <input className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2" {...register('phone')} />
            {errors.phone && <p className="text-xs text-rose-500">{errors.phone.message}</p>}
          </div>
          <div>
            <label className="text-sm font-medium text-slate-700">Password</label>
            <input className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2" type="password" {...register('password')} />
            {errors.password && <p className="text-xs text-rose-500">{errors.password.message}</p>}
          </div>
          <Button disabled={isSubmitting} type="submit" className="w-full">
            {isSubmitting ? 'Creating...' : 'Sign up'}
          </Button>
        </form>
        <p className="mt-6 text-sm text-slate-500">
          Already have an account? <Link to="/login" className="text-brand">Sign in</Link>
        </p>
      </div>
    </div>
  );
};

export default Signup;