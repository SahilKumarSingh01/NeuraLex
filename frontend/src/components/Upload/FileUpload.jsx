import axios from "axios";
import { useState } from "react";

export default function FileUpload() {
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);

  const handleUpload = async (e) => {
    const selectedFiles = Array.from(e.target.files);
    if (!selectedFiles.length) return;

    setUploading(true);

    const formData = new FormData();

    selectedFiles.forEach((file) => {
      formData.append("files", file); // backend expects "files"
    });

    try {
      await axios.post("http://localhost:8000/upload", formData);

      const newFileNames = selectedFiles.map((f) => f.name);

      // ✅ Append + remove duplicates
      setFiles((prev) => {
        const all = [...prev, ...newFileNames];
        return [...new Set(all)];
      });

    } catch (err) {
      console.error(err);
      alert("Upload failed");
    }

    setUploading(false);

    // 🔥 reset input so same file can be uploaded again
    e.target.value = "";
  };

  return (
    <div className="p-3 border-b border-gray-800 flex items-center gap-4">

      {/* Title */}
      <h1 className="font-bold text-lg">NeuraLex AI</h1>

      {/* Upload Button */}
      <input
        type="file"
        multiple
        accept=".pdf,.doc,.docx"
        onChange={handleUpload}
        className="text-sm"
      />

      {/* Uploaded Files List */}
      {files.length > 0 && (
        <div className="text-sm bg-gray-800 px-3 py-2 rounded max-w-md overflow-auto">
          📄 Files:
          {files.map((f, i) => (
            <div key={i}>• {f}</div>
          ))}
        </div>
      )}

      {/* Uploading Indicator */}
      {uploading && (
        <span className="text-xs text-gray-400">Uploading...</span>
      )}

    </div>
  );
}