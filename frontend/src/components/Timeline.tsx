const Timeline = ({ events }: { events: { type: string; at: string; by: string; data?: Record<string, unknown> }[] }) => (
  <ol className="space-y-4 border-l-2 border-slate-200 pl-4">
    {events?.map((event, idx) => (
      <li key={`${event.type}-${idx}`} className="relative">
        <span className="absolute -left-[19px] top-2 h-3 w-3 rounded-full bg-brand"></span>
        <p className="text-sm font-medium text-slate-900">{event.type}</p>
        <p className="text-xs text-slate-500">{new Date(event.at).toLocaleString()} · {event.by}</p>
      </li>
    ))}
  </ol>
);

export default Timeline;