import { useState } from "react";

export default function InputBox({ onSend, loading }) {
  const [text, setText] = useState("");
  const [mode, setMode] = useState("Normal");
  const [open, setOpen] = useState(false);

  const handleSend = () => {
    if (!text.trim()) return;
    onSend(text, mode);
    setText("");
  };

  return (
    <div className="p-3 w-full border-t border-gray-800">
      <div className="bg-[#1e293b] rounded-2xl px-3 py-2 w-full flex items-center">
        <input
          className="flex-1 bg-transparent outline-none text-sm px-2 text-white"
          placeholder="Ask a question about your documents..."
          value={text}
          disabled={loading}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />

        <div className="relative mr-2">
          <button
            onClick={() => setOpen(!open)}
            className="bg-gray-700 text-white px-3 py-1 rounded-full text-xs"
          >
            {mode}
          </button>

          {open && (
            <div className="absolute right-0 bottom-10 bg-[#111827] rounded-xl w-52 p-2 shadow-xl z-50 border border-gray-700">
              <div
                onClick={() => { setMode("Normal"); setOpen(false); }}
                className={`p-2 rounded cursor-pointer ${mode === "Normal" ? "bg-gray-700" : "hover:bg-gray-800"}`}
              >
                ⚡ Normal
                <div className="text-xs text-gray-400">Fast answers</div>
              </div>
              <div
                onClick={() => { setMode("Thinking"); setOpen(false); }}
                className={`p-2 rounded cursor-pointer ${mode === "Thinking" ? "bg-gray-700" : "hover:bg-gray-800"}`}
              >
                🧠 Thinking
                <div className="text-xs text-gray-400">Better reasoning</div>
              </div>
            </div>
          )}
        </div>

        <button
          onClick={handleSend}
          disabled={loading || !text.trim()}
          className="bg-white text-black w-9 h-9 rounded-full flex items-center justify-center hover:bg-gray-300 disabled:bg-gray-600"
        >
          ↑
        </button>
      </div>
    </div>
  );
}