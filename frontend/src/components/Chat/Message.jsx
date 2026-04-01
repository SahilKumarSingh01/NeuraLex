

export default function Message({ msg }) {
  return (
    <div className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>

      <div className={`px-4 py-2 rounded-2xl max-w-[80%] text-sm
        ${msg.role === "user" ? "bg-blue-600" : "bg-gray-800"}`}>

        {/* MODE ONLY IF THINKING */}
        {msg.role === "bot" && msg.mode === "Thinking" && (
          <div className="text-xs text-purple-400 mb-1">Thinking Mode</div>
        )}

        {msg.text}
      </div>

    </div>
  );
}