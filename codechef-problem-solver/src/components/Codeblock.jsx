// CodeBlock.js
import React, { useState } from "react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";

const CodeBlock = ({ language, codeString }) => {
  const [copied, setCopied] = useState(false);

  const handleCopyClick = async () => {
    try {
      // Copy just the raw code, no triple backticks
      await navigator.clipboard.writeText(codeString);
      setCopied(true);
      // Reset "Copied!" after 2 seconds
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error("Failed to copy code: ", err);
    }
  };

  return (
    <div className="relative my-4 border border-gray-300 rounded-md overflow-hidden">
      {/* Header bar */}
      <div className="flex justify-between items-center bg-[#1e1e1e] text-gray-200 px-3 py-2">
        <span className="text-xs uppercase font-semibold">
          {language || "code"}
        </span>
        <button
          onClick={handleCopyClick}
          className="text-xs bg-gray-600 hover:bg-gray-500 px-2 py-1 rounded"
        >
          {copied ? "Copied!" : "Copy"}
        </button>
      </div>
      {/* The actual code block with syntax highlighting */}
      <SyntaxHighlighter
        language={(language || "").toLowerCase()}
        style={vscDarkPlus}
        showLineNumbers
        customStyle={{
          margin: 0,
          backgroundColor: "#1e1e1e",
          padding: "1rem",
        }}
      >
        {codeString}
      </SyntaxHighlighter>
    </div>
  );
};

export default CodeBlock;
