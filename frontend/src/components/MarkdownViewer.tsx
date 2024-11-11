import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import remarkGfm from "remark-gfm";
import Prism from "prismjs";
import "github-markdown-css/github-markdown.css";
import "prismjs/themes/prism-tomorrow.css";

const MarkdownViewer: React.FC = () => {
  const { docType, questionNum, docTitle } = useParams<{
    docType: string;
    questionNum?: string;
    docTitle: string;
  }>();

  /*
    This is where I try to reconstruct the URL for re-routing.
    TODO: Make sure that this routes correctly with React Router.
   */
  const finalUrl =
    docType === "global"
      ? `/docs/global/${docTitle}.md`
      : `/docs/question/${questionNum}/doc_${docTitle}.md`;

  const [content, setContent] = useState<string>("");

  useEffect(() => {
    const fetchMarkdown = async () => {
      try {
        const res = await fetch(finalUrl);
        if (!res.ok) {
          throw new Error(`Failed to fetch: ${res.status}`);
        }
        const text = await res.text();
        setContent(text);
      } catch (error) {
        console.error("Error fetching markdown:", error);
      }
    };

    void fetchMarkdown();
  }, [finalUrl]);

  useEffect(() => {
    Prism.highlightAll();
  }, [content]);

  return (
    <div className="markdown-body">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
    </div>
  );
};

export default MarkdownViewer;
