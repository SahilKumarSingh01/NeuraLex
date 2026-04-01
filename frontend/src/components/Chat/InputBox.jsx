


import { useState } from "react";

export default function InputBox({ onSend, loading }) {
  const [text, setText] = useState("");
  const [files, setFiles] = useState([]);
  const [selected, setSelected] = useState([]);
  const [mode, setMode] = useState("Normal");
  const [open, setOpen] = useState(false);

  // 📎 Upload
  const handleUpload = (e) => {
    const selectedFiles = Array.from(e.target.files);
    const names = selectedFiles.map((f) => f.name);
    setFiles((prev) => [...new Set([...prev, ...names])]);
  };

  // ✔ Select
  const toggleFile = (file) => {
    setSelected((prev) =>
      prev.includes(file)
        ? prev.filter((f) => f !== file)
        : [...prev, file]
    );
  };

  // ❌ Delete
  const deleteFile = (file) => {
    setFiles((prev) => prev.filter((f) => f !== file));
    setSelected((prev) => prev.filter((f) => f !== file));
  };

  // 🚀 SEND
  const handleSend = () => {
    if (!text.trim() && selected.length === 0) return;

    onSend(text || "Analyze selected file", selected, mode);

    setText("");

    // 🔥 AUTO REMOVE USED FILES (GPT behavior)
    setFiles((prev) => prev.filter((f) => !selected.includes(f)));
    setSelected([]);

    // 🔥 COLLAPSE FILE UI
    setFiles([]);
  };

  return (
    <div className="p-3 w-full border-t border-gray-800">

      {/* INPUT CONTAINER */}
      <div className="bg-[#1e293b] rounded-2xl px-3 py-2 w-full">

        {/* 📎 FILE CHIPS (INSIDE INPUT) */}
        {files.length > 0 && (
          <div className="flex gap-2 mb-2 overflow-x-auto">
            {files.map((f, i) => (
              <div
                key={i}
                className={`flex items-center gap-2 px-2 py-1 rounded-full text-xs cursor-pointer whitespace-nowrap
                  ${selected.includes(f)
                    ? "bg-blue-600"
                    : "bg-gray-700"}`}
                onClick={() => toggleFile(f)}
              >
                📄 {f.slice(0, 15)}...

                {/* ❌ */}
                <span
                  className="ml-1 text-red-300"
                  onClick={(e) => {
                    e.stopPropagation();
                    deleteFile(f);
                  }}
                >
                  ✖
                </span>
              </div>
            ))}
          </div>
        )}

        {/* 💬 INPUT ROW */}
        <div className="flex items-center">

          {/* + */}
          <label className="text-xl px-2 cursor-pointer">
            +
            <input type="file" hidden multiple onChange={handleUpload} />
          </label>

          {/* INPUT */}
          <input
            className="flex-1 bg-transparent outline-none text-sm px-2"
            placeholder="Ask anything"
            value={text}
            disabled={loading}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />

          {/* MODE */}
          <div className="relative mr-2">
            <button
              onClick={() => setOpen(!open)}
              className="bg-gray-700 px-3 py-1 rounded-full text-xs"
            >
              {mode}
            </button>

            {open && (
              <div className="absolute right-0 bottom-10 bg-[#111827] rounded-xl w-52 p-2 shadow z-50">

                <div
                  onClick={() => { setMode("Normal"); setOpen(false); }}
                  className={`p-2 rounded cursor-pointer ${
                    mode === "Normal" ? "bg-gray-700" : "hover:bg-gray-800"
                  }`}
                >
                  ⚡ Normal
                  <div className="text-xs text-gray-400">Fast answers</div>
                </div>

                <div
                  onClick={() => { setMode("Thinking"); setOpen(false); }}
                  className={`p-2 rounded cursor-pointer ${
                    mode === "Thinking" ? "bg-gray-700" : "hover:bg-gray-800"
                  }`}
                >
                  🧠 Thinking
                  <div className="text-xs text-gray-400">Better reasoning</div>
                </div>

              </div>
            )}
          </div>

          {/* SEND */}
          <button
            onClick={handleSend}
            disabled={loading}
            className="bg-white text-black w-9 h-9 rounded-full flex items-center justify-center hover:bg-gray-300"
          >
            ↑
          </button>

        </div>
      </div>
    </div>
  );
}