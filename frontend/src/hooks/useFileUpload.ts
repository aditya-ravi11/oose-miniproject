import { useState } from 'react';
import { uploadFile } from '../api/files';

export const useFileUpload = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleUpload = async (files: FileList | null) => {
    if (!files?.length) return [];
    setLoading(true);
    setError(null);
    try {
      const uploads = await Promise.all(Array.from(files).map((file) => uploadFile(file)));
      return uploads.map((u) => u.url);
    } catch (err) {
      setError('Upload failed');
      return [];
    } finally {
      setLoading(false);
    }
  };

  return { upload: handleUpload, loading, error };
};