import type { PropsWithChildren, ReactNode } from 'react';

type CardProps = PropsWithChildren<{ title?: ReactNode; action?: ReactNode; className?: string }>;

const Card = ({ title, action, className = '', children }: CardProps) => (
  <section className={`rounded-2xl border border-slate-100 bg-white p-5 shadow-sm ${className}`}>
    {(title || action) && (
      <header className="mb-4 flex items-center justify-between">
        <h2 className="text-lg font-semibold text-slate-900">{title}</h2>
        {action}
      </header>
    )}
    {children}
  </section>
);

export default Card;