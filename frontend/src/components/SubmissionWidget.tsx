import React, { useState } from "react";

// interface Judge0Response {
//   stdout: string | null;
//   stderr: string | null;
//   message?: string;
// }

const SubmissionWidget = () => {
  const [activeTab, setActiveTab] = useState("submission");
  const [submissionType, setSubmissionType] = useState("code");
  const [code, setCode] = useState<string>("");
  const [file, setFile] = useState<File | null>(null);
  const [consoleVisible, setConsoleVisible] = useState(false);
  // const [consoleOutput, setConsoleOutput] = useState<string | null>(null);

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

  // const handleRun = async () => {
  //   setConsoleVisible(true);
  //   setConsoleOutput("Running code...");

  //   try {
  //     const response = await fetch(
  //       "https://api.judge0.com/submissions?base64_encoded=false&wait=true",
  //       {
  //         method: "POST",
  //         headers: {
  //           "Content-Type": "application/json",
  //           "X-RapidAPI-Key": "YOUR_JUDGE0_API_KEY", // Optional if needed
  //         },
  //         body: JSON.stringify({
  //           source_code: code,
  //           language_id: 71,
  //         }),
  //       }
  //     );

  //     if (!response.ok) {
  //       let errorMessage = "Error running code.";

  //       // Attempt to parse JSON error message if available
  //       try {
  //         const errorData = await response.json();
  //         errorMessage = errorData.message || errorMessage;
  //       } catch {
  //         console.error("Could not parse error response as JSON.");
  //       }

  //       throw new Error(errorMessage);
  //     }

  //     const data: Judge0Response = await response.json();
  //     setConsoleOutput(data.stdout || data.stderr || "No output.");
  //   } catch (error) {
  //     const errorMessage = error instanceof Error ? error.message : "Unexpected error occurred.";
  //     setConsoleOutput(`Error running code: ${errorMessage}`);
  //     console.error("Error:", error);
  //   }
  // };

  const handleSubmit = () => {
    console.log("Submitting code or file");
    console.log("Code:", code);
    console.log("File:", file);
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
            <button
              // onClick={handleRun}
              className="bg-purple-500 text-white px-3 py-1 rounded mr-2"
            >
              Run
            </button>
            <button
              onClick={handleSubmit}
              className="bg-blue-500 text-white px-3 py-1 rounded"
            >
              Submit
            </button>
          </div>

          {consoleVisible && (
            <div className="mt-4 bg-gray-100 border border-gray-300 rounded p-3 h-24 overflow-y-auto">
              <div className="text-sm text-gray-800">
                <strong>Output:</strong>
              </div>
              <pre className="text-xs text-gray-800 whitespace-pre-wrap">
                {/* {consoleOutput} */}
              </pre>
            </div>
          )}

          <button
            onClick={() => setConsoleVisible((prev) => !prev)}
            className="text-xs text-purple-500 mt-2"
          >
            {/* {consoleVisible ? "Hide Console" : "Show Console"} */}
          </button>
        </div>
      )}

      {activeTab === "docs" && (
        <div className="p-4">
          <h3 className="text-lg font-semibold mb-2">Documentation</h3>
          <ul className="list-disc list-inside">
            <li>How to use the submission area</li>
            <li>Tips for writing efficient code</li>
            <li>Common errors and debugging tips</li>
            <li>Resources for improving coding skills</li>
          </ul>
        </div>
      )}
    </section>
  );
};

export default SubmissionWidget;
