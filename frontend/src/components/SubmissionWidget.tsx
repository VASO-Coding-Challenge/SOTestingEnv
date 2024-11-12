// SubmissionWidget.tsx
import React, { useState } from "react";
import { SubmissionWidgetProps } from "../models/submission";
import { Link } from "react-router-dom";

const SubmissionWidget: React.FC<SubmissionWidgetProps> = ({
  question,
  globalDocs,
}) => {
  const [activeTab, setActiveTab] = useState("submission");
  const [docsTab, setDocsTab] = useState("question");

  const handleTabSwitch = (tab: "submission" | "docs") => {
    setActiveTab(tab);
  };

  const handleDocsTabSwitch = (tab: "question" | "global") => {
    setDocsTab(tab);
  };

  const openDocInNewTab = (doc: { content: string; title: string }) => {
    sessionStorage.setItem("docContent", doc.content);
    sessionStorage.setItem("docTitle", doc.title);
    const fullUrl = `${window.location.origin}/markdown-viewer/${doc.title}`;
    window.open(fullUrl, "_blank");
  };

  return (
    <section className="w-full max-w-lg h-[95vh] mx-auto bg-white rounded-lg shadow-md p-4 mt-1 mb-2 lg:ml-auto lg:mr-4 relative">
      <div className="flex border-b">
        <button
          onClick={() => handleTabSwitch("submission")}
          className={`w-1/2 py-2 text-center ${
            activeTab === "submission"
              ? "border-b-2 border-purple-500 font-semibold"
              : ""
          }`}
        >
          Submission
        </button>
        <button
          onClick={() => handleTabSwitch("docs")}
          className={`w-1/2 py-2 text-center ${
            activeTab === "docs"
              ? "border-b-2 border-purple-500 font-semibold"
              : ""
          }`}
        >
          Docs
        </button>
      </div>

      {activeTab === "submission" && (
        <div className="p-4 h-full flex flex-col">
          <h3 className="text-lg font-semibold mb-2">Run Your Solution</h3>
          {/* Code submission form goes here */}
        </div>
      )}

      {activeTab === "docs" && (
        <div className="p-4">
          <div className="flex border-b mb-4">
            <button
              onClick={() => handleDocsTabSwitch("question")}
              className={`w-1/2 py-2 text-center ${
                docsTab === "question"
                  ? "border-b-2 border-purple-500 font-semibold"
                  : ""
              }`}
            >
              Question Docs
            </button>
            <button
              onClick={() => handleDocsTabSwitch("global")}
              className={`w-1/2 py-2 text-center ${
                docsTab === "global"
                  ? "border-b-2 border-purple-500 font-semibold"
                  : ""
              }`}
            >
              Global Docs
            </button>
          </div>

          {docsTab === "question" && (
            <div>
              <h4>
                <strong>Documentation for Question {question.num}</strong>
              </h4>
              {question.docs.map((doc) => (
                <div key={doc.title} className="mb-4">
                  <ul className="list-disc pl-6 text-black">
                    <li>
                      <button
                        onClick={() => openDocInNewTab(doc)}
                        className="text-blue-500 hover:text-blue-300"
                      >
                        {doc.title}
                      </button>
                    </li>
                  </ul>
                </div>
              ))}
            </div>
          )}

          {docsTab === "global" && (
            <div>
              <h4>
                <strong>Global Documentation</strong>
              </h4>
              {globalDocs.map((doc) => (
                <div key={doc.title} className="mb-4">
                  <ul className="list-disc pl-6 text-black">
                    <li>
                      <button
                        onClick={() => openDocInNewTab(doc)}
                        className="text-blue-500 hover:text-blue-300"
                      >
                        {doc.title}
                      </button>
                      <li>
                        <Link
                          to="../../public/python-3.13-docs-html/index.html"
                          target="__blank"
                          rel="noopener noreferrer"
                          className="text-blue-500 hover:text-blue-300"
                        >
                          Python 3 Documentation
                        </Link>
                      </li>
                    </li>
                  </ul>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </section>
  );
};

export default SubmissionWidget;
