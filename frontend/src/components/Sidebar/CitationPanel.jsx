import { useEffect, useState } from "react";
import { Quote } from "lucide-react";

export default function CitationPanel() {
  const [citations, setCitations] = useState([]);

  useEffect(() => {
    const handler = (e) => {
      if (e.detail.llm_response_source) {
        setCitations(e.detail.llm_response_source);
      }
    };
    window.addEventListener("ragData", handler);
    return () => window.removeEventListener("ragData", handler);
  }, []);

  if (citations.length === 0) return null;

  return (
    <div className="mt-4">
      <h2 className="text-[10px] font-bold text-gray-500 uppercase tracking-widest mb-3 flex items-center gap-2">
        <Quote size={12} /> Source Evidence
      </h2>
      <div className="space-y-3">
        {citations.map((src, i) => (
          <div key={i} className="bg-gray-900/40 border border-gray-800 p-3 rounded-xl">
            <div className="flex justify-between text-[10px] mb-2 font-mono">
              <span className="text-blue-400 truncate max-w-[150px]">{src.source}</span>
              <span className="text-gray-500">PAGE {src.page}</span>
            </div>
            <p className="text-xs text-gray-400 leading-relaxed italic">
              "{src.text}"
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}