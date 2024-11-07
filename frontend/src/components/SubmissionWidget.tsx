import React, { useState } from "react";
import { SubmissionWidgetProps } from "../models/submission";

const SubmissionWidget: React.FC<SubmissionWidgetProps> = ({
  question,
  globalDocs,
}) => {
  const [activeTab, setActiveTab] = useState("submission");
  const [submissionType, setSubmissionType] = useState("code");
  const [code, setCode] = useState<string>("");
  const [file, setFile] = useState<File | null>(null);
  const [consoleVisible, setConsoleVisible] = useState(false);

  const handleTabSwitch = (tab: "submission" | "docs") => {
    setActiveTab(tab);
  };

  const handleSubmissionSwitch = (submission: "code" | "file") => {
    setSubmissionType(submission);
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleCodeChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setCode(e.target.value);
  };

  const handleSubmit = () => {
    console.log("Submitting code or file");
    console.log("Code:", code);
    console.log("File:", file);
    setConsoleVisible(true);
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
          <div className="flex mb-4">
            <button
              onClick={() => handleSubmissionSwitch("code")}
              className={`flex-1 py-2 ${
                submissionType === "code" ? "bg-gray-200" : "bg-white"
              } border rounded-l`}
            >
              Code
            </button>
            <button
              onClick={() => handleSubmissionSwitch("file")}
              className={`flex-1 py-2 ${
                submissionType === "file" ? "bg-gray-200" : "bg-white"
              } border rounded-r`}
            >
              File
            </button>
          </div>

          {submissionType === "code" ? (
            <textarea
              value={code}
              onChange={handleCodeChange}
              placeholder="Paste your code here"
              className={`w-full p-2 mb-3 border rounded bg-white text-black ${
                consoleVisible ? "h-40" : "flex-grow"
              }`}
            ></textarea>
          ) : (
            <input
              type="file"
              onChange={handleFileUpload}
              className="w-full p-2 mb-4 border rounded bg-white text-black"
            />
          )}

          <div className="flex justify-end mt-auto">
            <button className="bg-purple-500 text-white px-3 py-1 rounded mr-2">
              Run
            </button>
            <button
              onClick={handleSubmit}
              className="bg-blue-500 text-white px-3 py-1 rounded"
            >
              Submit
            </button>
          </div>
        </div>
      )}

      {activeTab === "docs" && question && (
        <div className="p-4">
          <h3 className="text-lg font-semibold mb-2">
            Documentation for Question {question.num}
          </h3>
          {globalDocs.map((doc) => (
            <div key={doc.title}>
              <h5>{doc.title}</h5>
            </div>
          ))}
        </div>
      )}
    </section>
  );
};

export default SubmissionWidget;
