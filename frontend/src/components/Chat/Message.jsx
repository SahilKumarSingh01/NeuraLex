import { useState } from "react";
import { Copy, Check, FileText, ChevronDown, ChevronUp, BrainCircuit } from "lucide-react";
import MarkdownRenderer from "./MarkdownRenderer";

export default function Message({ msg }) {
  const [showSources, setShowSources] = useState(false);
  const [showThinking, setShowThinking] = useState(false);
  const [copied, setCopied] = useState(false);
  const isAssistant = msg.role === "assistant";

  const copyText = () => {
    navigator.clipboard.writeText(msg.text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className={`flex w-full mb-8 ${msg.role === "user" ? "justify-end" : "justify-start"} animate-in fade-in slide-in-from-bottom-2 duration-300`}>
      <div className={`group relative max-w-[85%] ${msg.role === "user" ? "px-4 py-3 rounded-2xl bg-blue-600 text-white shadow-sm" : "text-gray-100"}`}>
        
        <button 
          onClick={copyText}
          className={`absolute top-0 ${msg.role === "user" ? "-left-8" : "-right-8"} p-1.5 opacity-0 group-hover:opacity-100 transition-opacity text-gray-500 hover:text-gray-300`}
        >
          {copied ? <Check size={14} className="text-green-500" /> : <Copy size={14} />}
        </button>

        {isAssistant && msg.thinking && (
          <div className="mb-4">
            <button 
              onClick={() => setShowThinking(!showThinking)}
              className="flex items-center gap-2 text-[10px] text-purple-400 font-mono uppercase tracking-widest opacity-80 hover:opacity-100 transition-opacity"
            >
              <div className="relative flex h-2 w-2">
                {msg.mode === "Thinking" && (
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-purple-400 opacity-75"></span>
                )}
                <span className={`relative inline-flex rounded-full h-2 w-2 ${msg.mode === "Thinking" ? "bg-purple-500" : "bg-purple-900"}`}></span>
              </div>
              <BrainCircuit size={12} />
              {showThinking ? "Hide Thought Process" : "Show Thought Process"}
            </button>

            {showThinking && (
              <div className="mt-2 p-3 border-l-2 border-purple-500/30 bg-purple-500/5 text-gray-400 text-sm italic font-mono leading-relaxed rounded-r-lg animate-in slide-in-from-left-1 duration-200">
                <MarkdownRenderer content={msg.thinking} />
              </div>
            )}
          </div>
        )}

        <MarkdownRenderer content={msg.text} />

        {isAssistant && msg.sources && msg.sources.length > 0 && (
          <div className="mt-4 pt-3 border-t border-white/5">
            <button 
              onClick={() => setShowSources(!showSources)}
              className="flex items-center gap-2 text-[10px] font-bold uppercase tracking-widest text-gray-500 hover:text-blue-400 transition-colors"
            >
              <FileText size={12} />
              {msg.sources.length} Context Sources
              {showSources ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
            </button>

            {showSources && (
              <div className="mt-3 space-y-2 animate-in fade-in zoom-in-95 duration-200">
                {msg.sources.map((source, idx) => (
                  <div key={idx} className="p-3 rounded-lg bg-white/5 border border-white/5 text-[11px]">
                    <div className="flex justify-between items-start mb-1.5">
                    <span className="font-bold text-blue-400 truncate max-w-[180px]">
                      {source.metadata.source}
                    </span>
                    <div className="flex gap-2 text-gray-500 font-mono shrink-0">
                      <span>Pg {source.metadata.page}</span>
                      <span className="text-gray-700">|</span>
                      <span>S {source.metadata.sentence}</span>
                    </div>
                  </div>

                    {/* Main Content Preview */}
                    <p className="text-gray-400 italic line-clamp-3">"{source.text}"</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}