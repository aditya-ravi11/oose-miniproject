import type { ButtonHTMLAttributes } from 'react';

const base = 'inline-flex items-center justify-center rounded-md px-4 py-2 font-medium transition focus:outline-none focus:ring-2 focus:ring-offset-2';

const variants = {
  primary: `${base} bg-brand text-white hover:bg-brand-dark focus:ring-brand`,
  secondary: `${base} border border-slate-200 bg-white text-slate-700 hover:bg-slate-50 focus:ring-slate-200`,
  ghost: `${base} text-slate-600 hover:bg-slate-100 focus:ring-brand`,
} as const;

type Props = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: keyof typeof variants;
};

const Button = ({ variant = 'primary', className = '', ...props }: Props) => {
  return <button className={`${variants[variant]} ${className}`} {...props} />;
};

export default Button;