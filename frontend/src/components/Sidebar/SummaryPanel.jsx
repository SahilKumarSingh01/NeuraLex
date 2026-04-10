

import { useEffect, useState } from "react";

export default function SummaryPanel() {
  const [summary, setSummary] = useState("");
  const [sources, setSources] = useState([]);

  useEffect(() => {
    const handler = (e) => {
      setSummary(e.detail.summary || "");
      setSources(e.detail.sources || []);
    };

    window.addEventListener("ragData", handler);
    return () => window.removeEventListener("ragData", handler);
  }, []);

  return (
    <div>
      <h2 className="text-lg font-bold mb-2">Summary</h2>
      <p className="text-sm text-gray-300">{summary}</p>

      <h2 className="mt-4 font-bold">Sources</h2>

      {sources.map((src, i) => (
        <div key={i} className="bg-gray-800 p-3 rounded mt-2 text-sm">
          <b>Page {src.page}</b>
          <p>{src.text.slice(0, 100)}...</p>
        </div>
      ))}
    </div>
  );
}