import { cn } from "@/lib/utils";
import React, { useRef, useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { IconUpload } from "@tabler/icons-react";
import { useDropzone } from "react-dropzone";
import { X } from "lucide-react";

const mainVariant = {
  initial: { x: 0, y: 0 },
  animate: { x: 20, y: -20, opacity: 0.9 },
};

const secondaryVariant = {
  initial: { opacity: 0 },
  animate: { opacity: 1 },
};

export const FileUpload = ({
  onChange,
}: {
  onChange?: (files: File[]) => void;
}) => {
  const [files, setFiles] = useState<File[]>([]);
  const [previewImage, setPreviewImage] = useState<string | null>(null);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (newFiles: File[]) => {
    setFiles((prev) => [...prev, ...newFiles]);
    onChange?.(newFiles);
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const { getRootProps, isDragActive } = useDropzone({
    multiple: false,
    noClick: true,
    onDrop: handleFileChange,
  });

  return (
    <>
      <div className="w-full" {...getRootProps()}>
        <motion.div
          onClick={handleClick}
          whileHover="animate"
          className="p-10 group/file block rounded-lg cursor-pointer w-full relative overflow-hidden"
        >
          <input
            ref={fileInputRef}
            type="file"
            className="hidden"
            onChange={(e) =>
              handleFileChange(Array.from(e.target.files || []))
            }
          />

          {/* Grid background */}
          <div className="absolute inset-0 [mask-image:radial-gradient(ellipse_at_center,white,transparent)]">
            <GridPattern />
          </div>

          <div className="flex flex-col items-center justify-center">
            <p className="relative z-20 font-bold text-neutral-700 dark:text-neutral-300">
              Upload file
            </p>
            <p className="relative z-20 text-neutral-400 mt-2">
              Drag or drop your files here or click to upload
            </p>

            <div className="relative w-full mt-10 max-w-xl mx-auto">
              {/* FILE LIST */}
              {files.map((file, idx) => {
                const isImage = file.type.startsWith("image/");
                const previewUrl = URL.createObjectURL(file);

                return (
                  <motion.div
                    key={idx}
                    layoutId={`file-${idx}`}
                    className="relative z-40 bg-white dark:bg-neutral-900 flex gap-4 p-4 mt-4 rounded-md shadow-sm"
                  >
                    {/* Image preview */}
                    {isImage && (
                      <div
                        onClick={(e) => {
                          e.stopPropagation();
                          setPreviewImage(previewUrl);
                        }}
                        className="relative cursor-pointer group"
                      >
                        <img
                          src={previewUrl}
                          alt={file.name}
                          className="h-16 w-16 rounded-md object-cover border"
                        />
                        <div className="absolute inset-0 rounded-md bg-black/50 opacity-0 group-hover:opacity-80 transition" />
                      </div>
                    )}

                    {/* File info */}
                    <div className="flex-1">
                      <div className="flex justify-between items-center">
                        <p className="truncate text-neutral-700 dark:text-neutral-300">
                          {file.name}
                        </p>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            setFiles((prev) =>
                              prev.filter((_, i) => i !== idx)
                            );
                          }}
                          className="p-1 rounded-full hover:bg-red-100 dark:hover:bg-red-900"
                        >
                          <X className="h-4 w-4" />
                        </button>
                      </div>

                      <div className="flex justify-between text-sm mt-2 text-neutral-500">
                        <span>{file.type}</span>
                        <span>
                          {(file.size / (1024 * 1024)).toFixed(2)} MB
                        </span>
                      </div>
                    </div>
                  </motion.div>
                );
              })}

              {/* EMPTY STATE */}
              {!files.length && (
                <>
                  <motion.div
                    layoutId="file-upload"
                    variants={mainVariant}
                    className="relative z-40 bg-white dark:bg-neutral-900 flex items-center justify-center h-32 mt-1 w-full max-w-[8rem] mx-auto rounded-md shadow-lg"
                  >
                    {isDragActive ? (
                      <p className="flex flex-col items-center">
                        Drop it <IconUpload />
                      </p>
                    ) : (
                      <IconUpload />
                    )}
                  </motion.div>

                  <motion.div
                    variants={secondaryVariant}
                    className="absolute inset-0 z-30 border border-dashed border-sky-400 h-32 max-w-[8rem] mx-auto rounded-md"
                  />
                </>
              )}
            </div>
          </div>
        </motion.div>
      </div>

      {/* IMAGE MODAL */}
      <AnimatePresence>
        {previewImage && (
          <motion.div
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/80"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setPreviewImage(null)}
          >
            <motion.img
              src={previewImage}
              className="max-h-[90vh] max-w-[90vw] rounded-lg shadow-2xl"
              initial={{ scale: 0.9 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0.9 }}
              onClick={(e) => e.stopPropagation()}
            />

            <button
              onClick={() => setPreviewImage(null)}
              className="absolute top-6 right-6 text-white cursor-pointer"
            >
              <X className="h-6 w-6" />
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};

export function GridPattern() {
  return (
    <div className="flex flex-wrap scale-105">
      {Array.from({ length: 11 * 41 }).map((_, i) => (
        <div
          key={i}
          className="w-10 h-10 bg-gray-50 dark:bg-neutral-950"
        />
      ))}
    </div>
  );
}
