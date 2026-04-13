// CodeBlock component remains same as previous version
import { useState } from "react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { atomDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import { Copy, Check } from "lucide-react";


export function CodeBlock({ language, value }) {
  const [copied, setCopied] = useState(false);

  const copyToClipboard = () => {
    navigator.clipboard.writeText(value);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="relative my-3 group rounded-lg overflow-hidden border border-white/5">
      <div className="flex items-center justify-between px-4 py-1.5 bg-gray-900/80 border-b border-white/5">
        <span className="text-[10px] font-mono uppercase text-gray-400 tracking-wider">{language}</span>
        <button
          onClick={copyToClipboard}
          className="flex items-center gap-1.5 text-[10px] text-gray-400 hover:text-white transition-colors"
        >
          {copied ? (
            <> <Check size={12} className="text-green-400" /> <span>Copied!</span> </>
          ) : (
            <> <Copy size={12} /> <span>Copy</span> </>
          )}
        </button>
      </div>
      <SyntaxHighlighter
        language={language}
        style={atomDark}
        wrapLongLines={true}
        customStyle={{ 
          borderRadius: "0px", 
          margin: 0, 
          padding: "1rem",
          fontSize: "0.8rem", 
          lineHeight: "1.5",
          background: "#0f172a" 
        }}
      >
        {value}
      </SyntaxHighlighter>
    </div>
  );
}