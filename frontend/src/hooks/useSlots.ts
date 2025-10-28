import { useEffect, useState } from 'react';
import { availableSlots } from '../api/requests';

export const useSlots = (date: string | null, category: string | null) => {
  const [slots, setSlots] = useState<{ start: string; end: string }[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!date || !category) {
      setSlots([]);
      return;
    }
    setLoading(true);
    availableSlots(date, category)
      .then(setSlots)
      .finally(() => setLoading(false));
  }, [date, category]);

  return { slots, loading };
};