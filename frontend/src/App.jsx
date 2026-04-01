


import { useState } from "react";
import ChatWindow from "./components/Chat/ChatWindow";
import SummaryPanel from "./components/Sidebar/SummaryPanel";

function App() {
  const [showSummary, setShowSummary] = useState(false);

  return (
    <div className="h-screen overflow-hidden flex flex-col bg-[#020617] text-white">

      {/* HEADER */}
      <div className="flex justify-between items-center px-4 py-3 border-b border-gray-800">
        <h1 className="font-bold text-lg">NeuraLex</h1>

        <button
          onClick={() => setShowSummary(!showSummary)}
          className="bg-blue-600 px-3 py-1 rounded text-sm hover:bg-blue-500"
        >
          {showSummary ? "Close Summary" : "Open Summary"}
        </button>
      </div>

      {/* MAIN */}
      <div className="flex flex-1 min-h-0">

        {/* CHAT */}
        <div className="flex-1 flex flex-col min-h-0">
          <ChatWindow />
        </div>

        {/* SUMMARY */}
        {showSummary && (
          <div className="w-[320px] border-l border-gray-800 p-4 overflow-y-auto">
            <SummaryPanel />
          </div>
        )}

      </div>
    </div>
  );
}

export default App;