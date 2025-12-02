export interface FileRecord {
  id: number;
  filename: string;
  content_type: string;
  storage_path: string;
  size_bytes: number | null;
  created_at: string;
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL as string;

if (!API_BASE_URL) {
  console.warn("VITE_API_BASE_URL is not set");
}

export async function uploadFile(file: File): Promise<FileRecord> {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE_URL}/files/upload`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Upload failed (${res.status}): ${text}`);
  }

  const data = await res.json();
  return data.file as FileRecord;
}

export async function listFiles(): Promise<FileRecord[]> {
  const res = await fetch(`${API_BASE_URL}/files`);

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`List failed (${res.status}): ${text}`);
  }

  return (await res.json()) as FileRecord[];
}