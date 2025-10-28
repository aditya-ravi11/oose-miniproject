const EmptyState = ({ title, description }: { title: string; description?: string }) => (
  <div className="rounded-2xl border border-dashed border-slate-200 bg-white p-10 text-center">
    <p className="text-lg font-semibold text-slate-800">{title}</p>
    {description && <p className="mt-1 text-slate-500">{description}</p>}
  </div>
);

export default EmptyState;