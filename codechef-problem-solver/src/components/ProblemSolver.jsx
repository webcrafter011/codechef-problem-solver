// ProblemSolver.js
import React, { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

// Import the custom CodeBlock
import CodeBlock from "./CodeBlock";

const ProblemSolver = () => {
  const [url, setUrl] = useState("");
  const [markdownResponse, setMarkdownResponse] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState("");
  const [error, setError] = useState("");

  const handleSolve = async () => {
    if (!url) {
      setError("Please enter a valid CodeChef URL.");
      return;
    }

    // Reset previous data
    setError("");
    setMarkdownResponse("");

    // Show loading spinner
    setIsLoading(true);
    setLoadingStep("Extracting & Generating...");

    try {
      const response = await fetch("http://localhost:5000/solve", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url }),
      });

      const data = await response.json();

      if (response.ok) {
        // Some LLMs might return something like: "\"```python\n...```\""
        // If so, strip leading/trailing quotes.
        let cleaned = data.markdown;
        if (cleaned.startsWith('"') && cleaned.endsWith('"')) {
          cleaned = cleaned.slice(1, -1);
        }
        setMarkdownResponse(cleaned);
      } else {
        setError(data.error || "Failed to generate a solution.");
      }
    } catch (err) {
      setError("An error occurred. Please try again.");
    } finally {
      setIsLoading(false);
      setLoadingStep("");
    }
  };

  return (
    <div className="container mx-auto p-6 relative">
      {/* Loading Modal */}
      {isLoading && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
          <div className="bg-white p-6 rounded-lg shadow-lg w-96 text-center">
            <h2 className="text-xl font-semibold mb-2">Please Wait</h2>
            <p className="mb-4 text-gray-600">{loadingStep}</p>
            <div className="flex justify-center items-center">
              <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-blue-600"></div>
            </div>
          </div>
        </div>
      )}

      {/* Main Card */}
      <div className="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold mb-4">Solve CodeChef Problems</h2>

        {/* URL Input */}
        <div className="mb-4">
          <label
            className="block text-gray-700 text-sm font-bold mb-2"
            htmlFor="url"
          >
            Enter CodeChef Problem URL:
          </label>
          <input
            type="text"
            id="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="https://www.codechef.com/..."
          />
        </div>

        {/* Solve button */}
        <button
          onClick={handleSolve}
          disabled={isLoading}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition duration-300 disabled:bg-blue-300"
        >
          Solve Problem
        </button>

        {/* Error display */}
        {error && <p className="mt-4 text-red-500">{error}</p>}

        {/* Render the Markdown response */}
        {markdownResponse && (
          <div className="mt-6">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              components={{
                code({ node, inline, className, children, ...props }) {
                  const match = /language-(\w+)/.exec(className || "");

                  // For inline code, just render it normally
                  if (inline) {
                    return (
                      <code className={className} {...props}>
                        {children}
                      </code>
                    );
                  }

                  // For fenced code blocks (```python), use our custom CodeBlock
                  return (
                    <CodeBlock
                      language={match ? match[1] : ""}
                      codeString={String(children).replace(/\n$/, "")}
                    />
                  );
                },
              }}
            >
              {markdownResponse}
            </ReactMarkdown>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProblemSolver;
