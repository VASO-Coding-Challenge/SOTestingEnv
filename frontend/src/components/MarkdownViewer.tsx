import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import Prism from "prismjs";
import "github-markdown-css/github-markdown.css";
import "prismjs/themes/prism-tomorrow.css";

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const __Authors__ = ["Mustafa ALjumayli"];

const MarkdownViewer: React.FC = () => {
  const { questionNum, docTitle } = useParams<{
    questionNum: string;
    docTitle: string;
  }>();

  const [content, setContent] = useState<string>("");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchMarkdown = async () => {
      const url = `http://localhost:4402/docs/questions/${questionNum}/${docTitle}`;
      try {
        const response = await fetch(url, { cache: "no-store" });
        if (!response.ok) {
          throw new Error(`Failed to fetch document: ${response.statusText}`);
        }
        const text = await response.text();
        setContent(text);
      } catch (error) {
        console.error("Error fetching document:", error);
        setError("Failed to load the markdown document.");
      }
    };

    void fetchMarkdown();
  }, [questionNum, docTitle]);

  useEffect(() => {
    Prism.highlightAll();
  }, [content]);

  return (
    <div className="markdown-body">
      {error ? (
        <div className="text-red-500">{error}</div>
      ) : (
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
      )}
    </div>
  );
};

export default MarkdownViewer;
