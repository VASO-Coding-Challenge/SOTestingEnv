import React, { useState, useEffect } from "react";
import {
  Box,
  Tabs,
  Tab,
  Typography,
  Paper,
  Button,
  IconButton,
} from "@mui/material";
import { SubmissionWidgetProps } from "../models/submission";
import { Link } from "react-router-dom";
import UploadIcon from "@mui/icons-material/Upload";
import { Editor } from "@monaco-editor/react";

const SubmissionWidget: React.FC<SubmissionWidgetProps> = ({
  question,
  globalDocs,
}) => {
  const [activeTab, setActiveTab] = useState<"submission" | "docs">("submission");
  const [docsTab, setDocsTab] = useState<"question" | "global">("question");
  const [code, setCode] = useState<string>("");
  const [submissionResponse, setSubmissionResponse] = useState("");

  useEffect(() => {
    sessionStorage.setItem(`question_${question.num}`, code);
    // console.log(`Code saved for question_${question.num}:`, code);
  }, [code]);

  useEffect(() => {
    sessionStorage.setItem(`output_${question.num}`, submissionResponse);
    // console.log(`Code saved for question_${question.num}:`, code);
  }, [submissionResponse]);

  useEffect(() => {
    const savedCode =
      sessionStorage.getItem(`question_${question.num}`) || question.starterCode || "# Start coding here";
    setCode(savedCode);
    const savedResponse =
      sessionStorage.getItem(`output_${question.num}`);
    setSubmissionResponse(savedResponse);
    // console.log(`Code loaded for question_${question.num}:`, savedCode);
  }, [question]);

  // Logs whenever submissionResponse is changed; using for debugging 
  useEffect(() => {
    console.log(submissionResponse);
  }, [submissionResponse]);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files?.[0]) {
      const file = event.target.files[0];
      if (file.type === "text/x-python" || file.name.endsWith(".py")) {
        const fileContent = await file.text(); 
        setCode(fileContent); 
      } else {
        alert("Please upload a valid Python (.py) file.");
      }
    }
  };

  // POST request to submit code, setSubmissionResponse to console_log output for API route
  const handleQuestionSubmission = (questionNum: string, code: string) => {
    console.log("Running Code:", code);

    fetch("/api/submissions/submit", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify({
        file_contents: code,
        question_num: questionNum,
      }),
      }).then((response) => {
        if (!response.ok) {
          return response.json().then((json: { message: string }) => {
            throw new Error(json.message);
          });
        }
        return response.json();
      })
      .then((responseData: string) => {
        setSubmissionResponse(responseData.console_log); 
      }).catch((error: Error) => {
        console.error("Error :", error.message);
        return <></>;
      })
    }


  const handleSubmitCode = () => {
    console.log("Submitting Code:", code);
    // TODO: Add logic to handle code submission
  };

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
    <Box
      sx={{
        width: "70%",
        height: "100vh",
        position: "sticky",
        top: 0,
        margin: "0 auto",
        borderRadius: "12px",
        overflow: "hidden",
        boxShadow: 3,
        display: "flex",
        flexDirection: "column",
        bgcolor: "#fff",
      }}
    >
      {/* Tabs */}
      <Tabs
        value={activeTab}
        onChange={(event, newValue) => handleTabSwitch(newValue)}
        variant="fullWidth"
        indicatorColor="primary"
        textColor="primary"
      >
        <Tab value="submission" label="Submission" />
        <Tab value="docs" label="Docs" />
      </Tabs>

      {/* Submission Tab */}
      {activeTab === "submission" && (
        <Box
          sx={{
            flex: 1,
            display: "flex",
            flexDirection: "column",
            padding: 2,
          }}
        >
          <Paper
            sx={{
              flex: 1,
              border: "1px solid #ddd",
              borderRadius: "8px",
              overflow: "hidden",
              mb: 2,
            }}
          >
            <Editor
              height="100%"
              defaultLanguage="python"
              value={code}
              theme="vs-light"
              onChange={(value) => setCode(value || "")}
              options={{
                fontSize: 14,
                minimap: { enabled: true },
                scrollBeyondLastLine: false,
              }}
            />
          </Paper>

          <Paper
    sx={{
      flex: 1,
      border: "1px solid #ddd",
      borderRadius: "8px",
      overflow: "hidden",
      padding: 2,
      mb: 2,
      bgcolor: "#f9f9f9",
    }}
  >
    <Typography variant="h6" sx={{ mb: 1 }}>
      Output
    </Typography>
    <Box
      sx={{
        maxHeight: "200px",
        overflowY: "auto",
        padding: 1,
        backgroundColor: "#f0f0f0",
        border: "1px solid #ccc",
        borderRadius: "8px",
      }}
    >
      <Typography
        variant="body1"
        sx={{
          whiteSpace: "pre-wrap",
          wordBreak: "break-word",
        }}
      >
        {submissionResponse || "No output yet. Run your code to see the result here."}
      </Typography>
    </Box>
  </Paper>

          {/* File Upload and Action Buttons */}
          <Box
            sx={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <IconButton
              color="primary"
              component="label"
              sx={{ border: "1px solid #ddd", borderRadius: "50%", p: 1 }}
            >
              <UploadIcon />
              <input
                hidden
                type="file"
                accept=".py"
                onChange={handleFileUpload}
              />
            </IconButton>

            <Box sx={{ display: "flex", gap: 2 }}>
              <Button
                variant="outlined"
                color="primary"
                onClick={() => handleQuestionSubmission(String(question.num), code)}
              >
                Run Code
              </Button>
              <Button
                variant="contained"
                color="primary"
                onClick={handleSubmitCode}
              >
                Submit Code
              </Button>
            </Box>
          </Box>
        </Box>
      )}

      {/* Docs Tab */}
      {activeTab === "docs" && (
        <Box
          sx={{
            flex: 1,
            display: "flex",
            flexDirection: "column",
            padding: 2,
          }}
        >
          <Tabs
            value={docsTab}
            onChange={(event, newValue) => handleDocsTabSwitch(newValue)}
            variant="fullWidth"
            textColor="primary"
            indicatorColor="primary"
            sx={{ mb: 2 }}
          >
            <Tab value="question" label="Question Docs" />
            <Tab value="global" label="Global Docs" />
          </Tabs>

          {docsTab === "question" && (
            <Box>
              <Typography variant="h6" sx={{ mb: 1 }}>
                Documentation for Question
              </Typography>
              <ul>
                {question.docs.map((doc) => (
                  <li key={doc.title}>
                    <Typography
                      variant="body2"
                      color="primary"
                      sx={{ cursor: "pointer" }}
                      onClick={() => openDocInNewTab(doc)}
                    >
                      {doc.title}
                    </Typography>
                  </li>
                ))}
              </ul>
            </Box>
          )}

          {docsTab === "global" && (
            <Box>
              <Typography variant="h6" sx={{ mb: 1 }}>
                Global Documentation
              </Typography>
              <ul>
                <li>
                  <Link
                    to="/python_docs/index.html"
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{ textDecoration: "none", color: "#1976d2" }}
                  >
                    Python 3 Documentation
                  </Link>
                </li>
                {globalDocs.map((doc) => (
                  <li key={doc.title}>
                    <Typography
                      variant="body2"
                      color="primary"
                      sx={{ cursor: "pointer" }}
                      onClick={() => openDocInNewTab(doc)}
                    >
                      {doc.title}
                    </Typography>
                  </li>
                ))}
              </ul>
            </Box>
          )}
        </Box>
      )}
    </Box>
  );
};

export default SubmissionWidget