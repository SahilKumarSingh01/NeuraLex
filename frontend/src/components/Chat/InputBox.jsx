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
    /* Removed p-3 and border-t (border-t is already in the ChatWindow parent div) */
    <div className="w-full">
      <div className="bg-[#1e293b] rounded-2xl px-3 py-2.5 w-full flex items-center shadow-lg border border-white/5 focus-within:border-blue-500/50 transition-all">
        <input
          className="flex-1 bg-transparent outline-none text-sm px-2 text-white placeholder-gray-400"
          placeholder="Ask a question about your documents..."
          value={text}
          disabled={loading}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />

        <div className="relative mr-2 shrink-0">
          <button
            onClick={() => setOpen(!open)}
            className="bg-gray-700/80 hover:bg-gray-600 text-white px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider transition-colors"
          >
            {mode}
          </button>

          {open && (
            <div className="absolute right-0 bottom-12 bg-[#111827] rounded-xl w-52 p-2 shadow-2xl z-50 border border-white/10 animate-in fade-in slide-in-from-bottom-2">
              <div
                onClick={() => { setMode("Normal"); setOpen(false); }}
                className={`p-2 rounded-lg cursor-pointer transition-colors ${mode === "Normal" ? "bg-blue-600/20 text-blue-400" : "hover:bg-gray-800 text-gray-300"}`}
              >
                <div className="text-xs font-bold"> Normal</div>
                <div className="text-[10px] opacity-70">Fast answers</div>
              </div>
              <div
                onClick={() => { setMode("Thinking"); setOpen(false); }}
                className={`p-2 rounded-lg cursor-pointer mt-1 transition-colors ${mode === "Thinking" ? "bg-purple-600/20 text-purple-400" : "hover:bg-gray-800 text-gray-300"}`}
              >
                <div className="text-xs font-bold">Thinking</div>
                <div className="text-[10px] opacity-70">Better reasoning</div>
              </div>
            </div>
          )}
        </div>

        <button
          onClick={handleSend}
          disabled={loading || !text.trim()}
          className="bg-white text-black w-8 h-8 rounded-full flex items-center justify-center hover:bg-gray-200 disabled:bg-gray-700 disabled:text-gray-500 transition-all shrink-0"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
            <path d="m5 12 7-7 7 7"/><path d="M12 19V5"/>
          </svg>
        </button>
      </div>
    </div>
  );
}