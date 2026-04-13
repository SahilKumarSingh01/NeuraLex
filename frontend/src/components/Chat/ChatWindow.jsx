import { useState, useEffect, useRef, lazy, Suspense } from "react";
const Message = lazy(() => import("./Message")); 
import InputBox from "./InputBox";
import { useFiles } from "@contexts/FileContext.jsx";

export default function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const { selectedFiles, collection } = useFiles();
  
  const scrollContainerRef = useRef(null);
  const bottomRef = useRef(null);
  const [shouldAutoScroll, setShouldAutoScroll] = useState(true);

  const handleScroll = () => {
    const container = scrollContainerRef.current;
    if (!container) return;
    const isAtBottom = 
      container.scrollHeight - container.scrollTop <= container.clientHeight + 100;
    setShouldAutoScroll(isAtBottom);
  };

  const handleSend = async (text, mode) => {
    if (!text.trim()) return;

    const newMessages = [...messages, { role: "user", text: text }];
    setMessages(newMessages);
    setLoading(true);
    setShouldAutoScroll(true);
    try {
    const params = new URLSearchParams({ 
      collectionName: collection, 
      mode: mode 
    }).toString();

    const response = await fetch(`http://localhost:8000/chat?${params}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        messages: newMessages.map(m => ({ role: m.role, content: m.text })),
        sourceFileNameList: selectedFiles,
      }),
    });

      if (!response.body) return;

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = ""; // Critical for handling partial JSON chunks

      setMessages((prev) => [
        ...prev, 
        { role: "assistant", text: "", sources: [], thinking: "", mode: mode }
      ]);

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        
        // Keep the last (potentially partial) line in the buffer
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (!line.trim()) continue;
          try {
            const { type, content } = JSON.parse(line);
            
            setMessages((prev) => {
              const lastArr = [...prev];
              const lastMsg = { ...lastArr[lastArr.length - 1] };

              if (type === "source") {
                lastMsg.sources = content;
              } else if (type === "thinking") {
                lastMsg.thinking += content;
              } else if (type === "answer") {
                lastMsg.text += content;
                // Once we get real text, switch mode from thinking to active
                if(lastMsg.mode=="Thinking")
                  lastMsg.mode = "Normal"; 
              } else if (type === "error") {
                lastMsg.text = "Error: " + content;
              }

              lastArr[lastArr.length - 1] = lastMsg;
              return lastArr;
            });
          } catch (e) {
            console.error("Stream parse error", e);
          }
        }
      }
    } catch (err) {
      setMessages((prev) => [...prev, { role: "assistant", text: "Connection error." }]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (shouldAutoScroll) {
      bottomRef.current?.scrollIntoView({ behavior: "auto" });
    }
  }, [messages, loading]);

  return (
    <div className="grid grid-rows-[1fr_auto] h-screen w-full bg-[#0b0f1a] overflow-hidden">
      
      <div 
        ref={scrollContainerRef}
        onScroll={handleScroll}
        className="overflow-y-auto p-4 md:p-6 space-y-8 custom-scrollbar scroll-smooth"
      >
        <div className="max-w-4xl mx-auto w-full">
          {messages.length === 0 && (
            <div className="flex flex-col items-center justify-center min-h-[60vh] text-gray-600 opacity-30">
              <p className="text-xs font-mono tracking-[0.3em]">SYSTEM_READY_V3</p>
            </div>
          )}

          {/* Wrap lazy messages in Suspense */}
          <Suspense fallback={<div className="h-12 w-full animate-pulse bg-white/5 rounded-xl mb-8" />}>
            {messages.map((msg, i) => (
              <Message key={i} msg={msg} allMessages={messages} />
            ))}
          </Suspense>

          {loading && !messages[messages.length-1]?.text && !messages[messages.length-1]?.thinking && (
            <div className="flex items-center gap-3 px-2 py-4">
              <div className="flex gap-1.5">
                <span className="w-1.5 h-1.5 bg-blue-500/50 rounded-full animate-bounce"></span>
                <span className="w-1.5 h-1.5 bg-blue-500/50 rounded-full animate-bounce [animation-delay:0.2s]"></span>
                <span className="w-1.5 h-1.5 bg-blue-500/50 rounded-full animate-bounce [animation-delay:0.4s]"></span>
              </div>
            </div>
          )}
          <div ref={bottomRef} className="h-4" />
        </div>
      </div>

      <div className="p-4 bg-[#0b0f1a] border-t border-white/5">
        <div className="mx-auto w-full">
          <InputBox onSend={handleSend} loading={loading} />
        </div>
      </div>
    </div>
  );
}