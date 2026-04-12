import { useEffect, useState } from "react";
import DocumentSourceManager from "@components/Sidebar/DocumentSourceManager";
import CitationPanel from "@components/Sidebar/CitationPanel";

export default function SummaryPanel() {
  const [summary, setSummary] = useState("");

  useEffect(() => {
    const handler = (e) => {
      // We only care about the summary here now
      // Sources are handled internally by CitationPanel
      setSummary(e.detail.summary || "");
    };

    window.addEventListener("ragData", handler);
    return () => window.removeEventListener("ragData", handler);
  }, []);

  return (
    <div className="h-full flex flex-col bg-[#0b0f1a] text-white">
      
      {/* SECTION 1: LIBRARY MANAGEMENT */}
      {/* Handles uploads, list fetching, and selection context */}
      <DocumentSourceManager />

      <div className="flex-1 overflow-y-auto p-4 space-y-6 custom-scrollbar">
        
        {/* SECTION 2: AI SUMMARY */}
        <section>
          <h2 className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-3">
            Analysis Summary
          </h2>
          <div className="bg-[#1e293b]/30 border border-gray-800 p-4 rounded-xl">
            <p className="text-sm text-gray-300 leading-relaxed">
              {summary || "Select documents and ask a question to generate an automated summary of the findings."}
            </p>
          </div>
        </section>

        {/* SECTION 3: CITATIONS & SOURCES */}
        {/* Strictly displays the snippets and page numbers */}
        <CitationPanel />
        
      </div>
    </div>
  );
}