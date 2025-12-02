import React, { useState } from "react";
import { uploadFile } from "../api/client";

interface Props {
  onUploaded: () => void;
}

export const FileUploadForm: React.FC<Props> = ({ onUploaded }) => {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setError("Please choose a file to upload.");
      return;
    }

    setIsUploading(true);
    setError(null);
    setMessage(null);

    try {
      await uploadFile(file);
      setMessage("File uploaded successfully.");
      setFile(null);
      // Clear file input visually
      (e.target as HTMLFormElement).reset();
      onUploaded();
    } catch (err: any) {
      setError(err.message ?? "Upload failed.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: "2rem" }}>
      <h2>Upload File</h2>
      <input
        type="file"
        onChange={(e) => {
          const f = e.target.files?.[0] ?? null;
          setFile(f);
        }}
      />
      <button
        type="submit"
        disabled={isUploading}
        style={{ marginLeft: "0.5rem" }}
      >
        {isUploading ? "Uploading..." : "Upload"}
      </button>

      {message && <p style={{ color: "limegreen" }}>{message}</p>}
      {error && <p style={{ color: "crimson" }}>{error}</p>}
    </form>
  );
};