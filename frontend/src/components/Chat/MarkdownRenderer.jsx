import ReactMarkdown from "react-markdown";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import { CodeBlock } from "./CodeBlock";
import "katex/dist/katex.min.css";

export default function MarkdownRenderer({ content }) {
  const preprocessLaTeX = (text) => {
    if (typeof text !== "string") return text;
    return text
      .replace(/\\\\\(/g, "$")
      .replace(/\\\\\)/g, "$")
      .replace(/\\\\\[/g, "$$")
      .replace(/\\\\\]/g, "$$")
      .replace(/\\\(/g, "$")
      .replace(/\\\)/g, "$")
      .replace(/\\\[/g, "$$")
      .replace(/\\\]/g, "$$");
  };

  return (
    /* Added overflow-x-hidden and w-full to prevent the "large scroll" issue */
    <div className="prose prose-invert max-w-full w-full overflow-x-hidden text-sm leading-relaxed prose-p:leading-relaxed prose-pre:p-0">
      {/* Forced styles to hide the visual HTML layer per your request */}
      {/* <style>{`
        .katex-html { display: block !important; }
        .katex-mathml { display: none !important; }
      `}</style> */}
      <ReactMarkdown
        remarkPlugins={[remarkMath]}
        rehypePlugins={[rehypeKatex]}
        components={{
          code({ node, inline, className, children, ...props }) {
            const match = /language-(\w+)/.exec(className || "");
            return !inline && match ? (
              <CodeBlock
                language={match[1]}
                value={String(children).replace(/\n$/, "")}
                {...props}
              />
            ) : (
              <code className="bg-white/10 px-1.5 py-0.5 rounded text-blue-300 font-mono text-[0.85rem]" {...props}>
                {children}
              </code>
            );
          },
        }}
      >
        {preprocessLaTeX(content)}
      </ReactMarkdown>
    </div>
  );
}