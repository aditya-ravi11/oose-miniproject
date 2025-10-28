import { useAuthStore } from "../app/store/auth";

const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000";

export const FilesApi = {
  async upload(file: File): Promise<string> {
    const formData = new FormData();
    formData.append("file", file);
    const token = useAuthStore.getState().token;
    const response = await fetch(`${API_BASE}/files/upload`, {
      method: "POST",
      headers: token ? { Authorization: `Bearer ${token}` } : {},
      body: formData,
    });
    if (!response.ok) {
      throw new Error("Upload failed");
    }
    const data = await response.json();
    return data.url;
  },
};
