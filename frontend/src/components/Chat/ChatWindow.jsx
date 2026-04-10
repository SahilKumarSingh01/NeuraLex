
import { useState, useEffect, useRef } from "react";
import Message from "./Message";
import InputBox from "./InputBox";

export default function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef();

  const handleSend = (text, files, mode) => {
    if (!text.trim() && files.length === 0) return;

    const userText = text || "Analyze selected file";

    setMessages((prev) => [
      ...prev,
      { role: "user", text: userText }
    ]);

    setLoading(true);

    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: `Files: ${files.length}`,
          mode: mode
        }
      ]);
      setLoading(false);
    }, 800);
  };

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  return (
    <div className="flex flex-col flex-1 min-h-0">

      <div className="flex-1 overflow-y-auto p-4 space-y-3 min-h-0">
        {messages.map((msg, i) => (
          <Message key={i} msg={msg} />
        ))}

        {loading && <div className="text-gray-400">Thinking...</div>}

        <div ref={bottomRef}></div>
      </div>

      <div className="border-t border-gray-800 shrink-0">
  <InputBox onSend={handleSend} loading={loading} />
</div>
    </div>
  );
}