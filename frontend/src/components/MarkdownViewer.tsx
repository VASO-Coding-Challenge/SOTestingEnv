// MarkdownViewer.tsx
import React, { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import Prism from "prismjs";
import "github-markdown-css/github-markdown.css";
import "prismjs/themes/prism-tomorrow.css";

const MarkdownViewer: React.FC = () => {
  const [content, setContent] = useState<string>("");
  const [title, setTitle] = useState<string>("");

  useEffect(() => {
    const docContent = sessionStorage.getItem("docContent");
    const docTitle = sessionStorage.getItem("docTitle");

    if (docContent && docTitle) {
      setContent(docContent);
      setTitle(docTitle);
    } else {
      console.error("Failed to load document content.");
    }

    Prism.highlightAll();
  }, [content]);

  return (
    <div className="markdown-body">
      <h1>{title}</h1>
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
    </div>
  );
};

export default MarkdownViewer;
