import { useState } from "react";
import axios from "axios";
import { Trash2, Plus, FileText, CheckCircle2, Circle, Loader2 } from "lucide-react";
import { useFiles } from "@contexts/FileContext.jsx";

export default function DocumentSourceManager() {
  const { files, setFiles, selectedFiles, setSelectedFiles, collection } = useFiles();
  const [uploadQueue, setUploadQueue] = useState({});

  const API_BASE = "http://localhost:8000";

  const handleUpload = async (e) => {
    const selectedFilesList = Array.from(e.target.files);
    if (!selectedFilesList.length) return;

    selectedFilesList.forEach(async (file) => {
      const fileName = file.name;
      setUploadQueue((prev) => ({ ...prev, [fileName]: 0 }));

      const formData = new FormData();
      formData.append("file", file);

      try {
        const res = await axios.post(
          `${API_BASE}/uploadFile?collectionName=${collection}`,
          formData,
          {
            onUploadProgress: (progressEvent) => {
              const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
              setUploadQueue((prev) => ({ ...prev, [fileName]: progress }));
            },
          }
        );

        const savedName = res.data.filename;
        setFiles((prev) => [...new Set([...prev, savedName])]);
        setSelectedFiles((prev) => [...new Set([...prev, savedName])]);
      } catch (err) {
        console.error(`Upload failed for ${fileName}`, err);
      } finally {
        setUploadQueue((prev) => {
          const newQueue = { ...prev };
          delete newQueue[fileName];
          return newQueue;
        });
      }
    });

    e.target.value = "";
  };

  const handleDelete = async (e, fileName) => {
    e.stopPropagation();
    try {
      await axios.delete(`${API_BASE}/deleteFiles?collectionName=${collection}`, {
        data: [fileName],
      });
      setFiles((prev) => prev.filter((f) => f !== fileName));
      setSelectedFiles((prev) => prev.filter((f) => f !== fileName));
    } catch (err) {
      console.error("Local delete error", err);
    }
  };

  const toggleSelection = (fileName) => {
    setSelectedFiles((prev) =>
      prev.includes(fileName) ? prev.filter((f) => f !== fileName) : [...prev, fileName]
    );
  };

  return (
    <div className="p-4 border-b border-gray-800 bg-[#0f172a]">
      <div className="flex justify-between items-center mb-4">
        <div className="min-w-0">
          <h3 className="text-sm font-bold text-white">Local Library</h3>
          <p className="text-[10px] text-blue-400 font-medium uppercase tracking-wider">
            Parallel Local Sync
          </p>
        </div>
        <label className="shrink-0 flex items-center gap-1 bg-blue-600 px-3 py-1.5 rounded text-[10px] font-bold cursor-pointer hover:bg-blue-500 transition-all active:scale-95 text-white shadow-lg">
          <Plus size={12} className="shrink-0" /> ADD FILES
          <input type="file" hidden multiple onChange={handleUpload} accept=".pdf" />
        </label>
      </div>

      <div className="space-y-2">
        {/* PROGRESS QUEUE */}
        {Object.entries(uploadQueue).map(([name, progress]) => (
          <div key={name} className="p-2 rounded-lg border border-blue-500 bg-blue-500/10 min-w-0">
            <div className="flex items-center justify-between mb-2 gap-2">
              <div className="flex items-center gap-2 text-[10px] text-blue-100 min-w-0">
                <Loader2 size={12} className="animate-spin shrink-0" />
                <span className="truncate font-medium">{name}</span>
              </div>
              <span className="text-[10px] text-blue-400 font-mono shrink-0">{progress}%</span>
            </div>
            <div className="w-full bg-gray-900 h-1.5 rounded-full overflow-hidden">
              <div 
                className="bg-blue-400 h-full transition-all duration-300" 
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>
        ))}

        {/* FILE LIST */}
        {files.map((file) => {
          const isSelected = selectedFiles.includes(file);
          return (
            <div
              key={file}
              onClick={() => toggleSelection(file)}
              className={`group flex items-center justify-between p-2.5 rounded-lg border transition-all duration-200 cursor-pointer gap-3 ${
                isSelected
                  ? "border-blue-500 bg-blue-500/10 shadow-[0_0_15px_rgba(59,130,246,0.15)]"
                  : "border-gray-700 bg-gray-800/40 hover:border-gray-500"
              }`}
            >
              {/* min-w-0 allows truncate to work, shrink-0 keeps icons fixed */}
              <div className="flex items-center gap-3 min-w-0 flex-1">
                {isSelected ? (
                  <CheckCircle2 size={16} className="text-blue-400 shrink-0" />
                ) : (
                  <Circle size={16} className="text-gray-500 shrink-0" />
                )}
                <FileText size={16} className={`${isSelected ? "text-blue-300" : "text-gray-400"} shrink-0`} />
                <span className={`truncate text-xs ${isSelected ? "text-white font-bold" : "text-gray-200"}`}>
                  {file}
                </span>
              </div>

              <button
                onClick={(e) => handleDelete(e, file)}
                className="p-1.5 text-gray-500 hover:text-red-500 hover:bg-red-500/10 rounded-md transition-all shrink-0"
              >
                <Trash2 size={14} className="shrink-0" />
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
}