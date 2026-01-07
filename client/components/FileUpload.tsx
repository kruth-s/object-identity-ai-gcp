"use client";
import React, { useState, useEffect } from "react";
import { FileUpload } from "@/components/ui/file-upload";

export function FileUploadComponent({
  onFilesChange,
}: {
  onFilesChange?: (files: File[]) => void;
}) {
  const [files, setFiles] = useState<File[]>([]);
  const [previews, setPreviews] = useState<string[]>([]);

  const handleFileUpload = (files: File[]) => {
    setFiles(files);
    onFilesChange?.(files);
  };

  // Generate previews whenever files change
  useEffect(() => {
    const urls = files.map((file) => URL.createObjectURL(file));
    setPreviews(urls);

    // Revoke URLs when component unmounts or files change
    return () => {
      urls.forEach((url) => URL.revokeObjectURL(url));
    };
  }, [files]);

  return (
    <div className="w-full max-w-4xl mx-auto min-h-96 border border-dashed bg-white dark:bg-black border-neutral-200 dark:border-neutral-800 rounded-lg p-4 flex flex-col items-center justify-center">
      <FileUpload onChange={handleFileUpload} />

      {previews.length > 0 && (
        <div className="mt-4 flex flex-wrap gap-4">
          {previews.map((url, idx) => (
            <img
              key={idx}
              src={url}
              alt={`Preview ${idx + 1}`}
              className="w-32 h-32 object-cover rounded-md shadow-md"
            />
          ))}
        </div>
      )}
    </div>
  );
}