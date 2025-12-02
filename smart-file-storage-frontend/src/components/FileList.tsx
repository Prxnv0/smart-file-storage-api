import React, { useEffect, useState } from "react";
import type { FileRecord } from "../api/client";
import { listFiles } from "../api/client";

interface Props {
  reloadToken: number;
}

export const FileList: React.FC<Props> = ({ reloadToken }) => {
  const [files, setFiles] = useState<FileRecord[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await listFiles();
        setFiles(data);
      } catch (err: any) {
        setError(err.message ?? "Failed to load files.");
      } finally {
        setLoading(false);
      }
    };

    load();
  }, [reloadToken]);

  return (
    <section>
      <h2>Uploaded Files</h2>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "crimson" }}>{error}</p>}
      {!loading && !error && files.length === 0 && <p>No files yet.</p>}

      {files.length > 0 && (
        <table style={{ borderCollapse: "collapse", width: "100%" }}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Filename</th>
              <th>Content Type</th>
              <th>Created At</th>
            </tr>
          </thead>
          <tbody>
            {files.map((f) => (
              <tr key={f.id}>
                <td>{f.id}</td>
                <td>{f.filename}</td>
                <td>{f.content_type}</td>
                <td>{new Date(f.created_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
};