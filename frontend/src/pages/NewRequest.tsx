import { zodResolver } from '@hookform/resolvers/zod';
import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { z } from 'zod';
import Button from '../components/Button';
import Card from '../components/Card';
import { useRequestStore } from '../app/store/requests';
import { useSlots } from '../hooks/useSlots';
import { useFileUpload } from '../hooks/useFileUpload';

const categories = ['organic', 'recyclable', 'hazardous', 'e-waste', 'bulk', 'other'] as const;

const schema = z.object({
  category: z.enum(categories),
  is_special: z.boolean().default(false),
  description: z.string().min(5),
  quantity: z.coerce.number().min(1),
  address: z.object({
    line1: z.string().min(3),
    line2: z.string().optional(),
    city: z.string().min(2),
    pincode: z.string().min(4),
    lat: z.coerce.number().optional(),
    lng: z.coerce.number().optional(),
  }),
  preferred_slots: z.array(z.object({ start: z.string(), end: z.string() })).min(1),
  photos: z.array(z.string()).optional(),
});

type FormValues = z.infer<typeof schema>;

const NewRequest = () => {
  const [step, setStep] = useState(1);
  const [date, setDate] = useState('');
  const navigate = useNavigate();
  const create = useRequestStore((state) => state.create);
  const {
    register,
    handleSubmit,
    setValue,
    watch,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: {
      category: 'recyclable',
      is_special: false,
      preferred_slots: [],
      photos: [],
      address: { city: '', line1: '', pincode: '' },
    },
  });

  const category = watch('category');
  const preferredSlots = watch('preferred_slots');
  const photos = watch('photos');
  const { slots } = useSlots(date || null, category);
  const { upload, loading: uploading } = useFileUpload();

  const onSubmit = async (values: FormValues) => {
    await create({ ...values, photos: values.photos || [] });
    navigate('/requests');
  };

  const addSlot = (slot: { start: string; end: string }) => {
    if (preferredSlots.find((item) => item.start === slot.start)) return;
    setValue('preferred_slots', [...preferredSlots, slot], { shouldDirty: true, shouldValidate: true });
  };

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    const urls = await upload(files);
    if (!urls.length) return;
    setValue('photos', [...(photos || []), ...urls], { shouldDirty: true });
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <Card title={`Step ${step} of 3`}>
        {step === 1 && (
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <label className="text-sm font-medium text-slate-700">Category</label>
              <select className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2" {...register('category')}>
                {categories.map((cat) => (
                  <option key={cat} value={cat}>
                    {cat}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="text-sm font-medium text-slate-700">Quantity (bags)</label>
              <input type="number" className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2" {...register('quantity')} />
              {errors.quantity && <p className="text-xs text-rose-500">{errors.quantity.message}</p>}
            </div>
            <div className="md:col-span-2">
              <label className="text-sm font-medium text-slate-700">Description</label>
              <textarea className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2" rows={3} {...register('description')} />
              {errors.description && <p className="text-xs text-rose-500">{errors.description.message}</p>}
            </div>
            <label className="flex items-center gap-2 text-sm text-slate-700">
              <input type="checkbox" {...register('is_special')} />
              Hazardous or e-waste item
            </label>
          </div>
        )}

        {step === 2 && (
          <div className="space-y-4">
            <div className="grid gap-4 md:grid-cols-2">
              <div>
                <label className="text-sm font-medium text-slate-700">Address line 1</label>
                <input className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2" {...register('address.line1')} />
              </div>
              <div>
                <label className="text-sm font-medium text-slate-700">Address line 2</label>
                <input className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2" {...register('address.line2')} />
              </div>
              <div>
                <label className="text-sm font-medium text-slate-700">City</label>
                <input className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2" {...register('address.city')} />
              </div>
              <div>
                <label className="text-sm font-medium text-slate-700">Pincode</label>
                <input className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2" {...register('address.pincode')} />
              </div>
            </div>
            <div>
              <label className="text-sm font-medium text-slate-700">Preferred date</label>
              <input type="date" className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2" value={date} onChange={(event) => setDate(event.target.value)} />
            </div>
            {date && (
              <div>
                <p className="text-sm font-medium text-slate-700">Available slots</p>
                <div className="mt-2 grid grid-cols-2 gap-2 md:grid-cols-3">
                  {slots.map((slot) => (
                    <button
                      type="button"
                      key={slot.start}
                      onClick={() => addSlot(slot)}
                      className="rounded-xl border border-slate-200 px-3 py-2 text-sm text-slate-700 hover:border-brand"
                    >
                      {new Date(slot.start).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </button>
                  ))}
                  {slots.length === 0 && <p className="text-sm text-slate-500">Select a date to view slots</p>}
                </div>
                <p className="mt-2 text-sm text-slate-600">Selected: {preferredSlots.length}</p>
              </div>
            )}
          </div>
        )}

        {step === 3 && (
          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium text-slate-700">Upload photos (optional)</label>
              <input type="file" multiple className="mt-1 w-full rounded-xl border border-dashed border-slate-300 px-3 py-2" onChange={handleFileChange} />
              {uploading && <p className="text-xs text-slate-500">Uploading...</p>}
            </div>
            <ul className="space-y-2 text-sm text-slate-600">
              {(photos || []).map((photo) => (
                <li key={photo} className="truncate rounded-md bg-slate-100 px-3 py-1">
                  {photo}
                </li>
              ))}
            </ul>
            <p className="text-sm text-slate-500">Review your request and submit.</p>
          </div>
        )}

        <div className="mt-6 flex justify-between">
          <Button type="button" variant="secondary" disabled={step === 1} onClick={() => setStep((prev) => Math.max(1, prev - 1))}>
            Back
          </Button>
          {step < 3 ? (
            <Button type="button" onClick={() => setStep((prev) => Math.min(3, prev + 1))}>
              Next
            </Button>
          ) : (
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? 'Submitting...' : 'Submit request'}
            </Button>
          )}
        </div>
      </Card>
    </form>
  );
};

export default NewRequest;