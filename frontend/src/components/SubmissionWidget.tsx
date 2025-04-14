/* eslint-disable @typescript-eslint/no-misused-promises */
/* eslint-disable @typescript-eslint/no-unsafe-argument */
/* eslint-disable @typescript-eslint/no-unsafe-assignment */
import React, { useState, useEffect } from "react";
import {
  Box,
  Tabs,
  Tab,
  Typography,
  Paper,
  Button,
  IconButton,
  Link as MuiLink,
  List,
  ListItem,
  Divider,
} from "@mui/material";
import { SubmissionWidgetProps } from "../models/submission";
import UploadIcon from "@mui/icons-material/Upload";
import RestoreIcon from "@mui/icons-material/Restore";
import DownloadIcon from "@mui/icons-material/Download";
import Tooltip from "@mui/material/Tooltip";
import { Editor } from "@monaco-editor/react";
import { Link } from "react-router-dom";

import { Skeleton } from "@/components/ui/skeleton";
import { CircleX, CircleCheck } from "lucide-react";

type SubmissionResponse = {
  console_log: string;
};

const SubmissionWidget: React.FC<SubmissionWidgetProps> = ({
  question,
  globalDocs,
}) => {
  const [activeTab, setActiveTab] = useState<"submission" | "docs">(
    "submission"
  );
  const [code, setCode] = useState<string>(
    sessionStorage.getItem(`question_${question.num}`) || question.starter_code
  );

  const [submissionResponse, setSubmissionResponse] = useState<string>(
    sessionStorage.getItem(`output_${question.num}`) || "No Submission Yet"
  );

  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    sessionStorage.setItem(`question_${question.num}`, code);
  }, [code]);

  useEffect(() => {
    sessionStorage.setItem(`output_${question.num}`, submissionResponse);
  }, [submissionResponse]);

  useEffect(() => {
    if (question) {
      const savedCode =
        sessionStorage.getItem(`question_${question.num}`) ||
        question.starter_code ||
        "# Start Coding Here";
      setCode(savedCode);
      const savedResponse =
        sessionStorage.getItem(`output_${question.num}`) || "No Submission Yet";
      setSubmissionResponse(savedResponse);
    }
  }, [question]);

  useEffect(() => {
    console.log(submissionResponse);
  }, [submissionResponse]);

  const handleFileUpload = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
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

  const downloadCode = () => {
    const blob = new Blob([code], { type: "text/x-python" });
    const url = URL.createObjectURL(blob);

    // Create a temporary anchor element to trigger the download
    const a = document.createElement("a");
    a.href = url;
    a.download = `code_question_${question.num}.py`; // File name
    a.click();

    // Clean up the URL object
    URL.revokeObjectURL(url);
  };

  const resetCode = () => {
    if (question.starter_code) {
      setCode(question.starter_code);
    } else {
      setCode("# Start Coding Here");
    }
  };

  // POST request to submit code, setSubmissionResponse to console_log output for API route
  const handleQuestionSubmission = (questionNum: string, code: string) => {
    console.log("Running Code:", code);
    setIsSubmitting(true);

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
    })
      .then((response) => {
        if (!response.ok) {
          return response.json().then((json: { message: string }) => {
            throw new Error(json.message);
          });
        }
        return response.json();
      })
      .then((responseData: SubmissionResponse) => {
        setSubmissionResponse(responseData.console_log);
        setIsSubmitting(false);
      })
      .catch((error: Error) => {
        console.error("Error :", error.message);
        return <></>;
      });
  };

  const handleTabSwitch = (tab: "submission" | "docs") => {
    setActiveTab(tab);
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
        width: "100%",
        height: "100vh",
        position: "sticky",
        top: 0,
        margin: "0 auto",
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
        onChange={(_event, newValue) => handleTabSwitch(newValue)}
        variant="fullWidth"
        indicatorColor="secondary"
        textColor="secondary"
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
            overflow: "hidden",
          }}
        >
          <Box
            sx={{
              flex: 1,
              overflow: "auto", // Enable scrolling for content
              display: "flex",
              flexDirection: "column",
              gap: 2,
            }}
          >
            <Paper
              sx={{
                flex: 1,
                border: "1px solid #ddd",
                borderRadius: "8px",
                overflow: "hidden",
                position: "relative",
                mb: 2,
                paddingTop: "50px",
              }}
            >
              {/* Toolbar */}
              <Box
                sx={{
                  position: "absolute",
                  top: 1,
                  right: 3,
                  zIndex: 1,
                  display: "flex",
                  alignItems: "center",
                  gap: 1,
                }}
              >
                {/* Upload Icon Button */}
                <Tooltip title="Upload Code" arrow>
                  <IconButton
                    color="secondary"
                    component="label"
                    sx={{
                      border: "1px #ddd",
                      borderRadius: "50%",
                      width: 30,
                      height: 30,
                    }}
                  >
                    <UploadIcon />
                    <input
                      hidden
                      type="file"
                      accept=".py"
                      onChange={handleFileUpload}
                    />
                  </IconButton>
                </Tooltip>

                {/* Download Code Button */}
                <Tooltip title="Download Code" arrow>
                  <IconButton
                    color="secondary"
                    sx={{
                      border: "1px #ddd",
                      borderRadius: "50%",
                      width: 30,
                      height: 30,
                    }}
                    onClick={downloadCode}
                  >
                    <DownloadIcon />
                  </IconButton>
                </Tooltip>

                {/* Reset Code Button */}
                <Tooltip title="Reset Code" arrow>
                  <IconButton
                    color="secondary"
                    sx={{
                      border: "1px #ddd",
                      borderRadius: "50%",
                      width: 30,
                      height: 30,
                    }}
                    onClick={resetCode}
                  >
                    <RestoreIcon />
                  </IconButton>
                </Tooltip>
              </Box>

              {/* Divider Under Toolbar */}
              <Divider
                sx={{
                  position: "absolute",
                  top: "30px",
                  left: 0,
                  right: 0,
                  zIndex: 1,
                }}
              />
              <Editor
                height="100%"
                defaultLanguage="python"
                value={code}
                theme="vs-light"
                onChange={(value) => setCode(value || "")}
                options={{
                  fontSize: 14,
                  minimap: { enabled: false },
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
              {/* TODO: */}
              {/* Display the output */}
              <Box
                sx={{
                  maxHeight: "250px",
                  overflowY: "auto",
                  padding: 1,
                  backgroundColor: "#f0f0f0",
                  border: "1px solid #ccc",
                  borderRadius: "8px",
                }}
              >
                {isSubmitting ? (
                  <div className="flex flex-col gap-3">
                    <div className="flex items-center space-x-4">
                      <Skeleton className="h-6 w-6 rounded-full" />
                      <div className="space-y-2">
                        <Skeleton className="h-4 w-[250px]" />
                      </div>
                    </div>
                    <div className="flex items-center space-x-4">
                      <Skeleton className="h-6 w-6 rounded-full" />
                      <div className="space-y-2">
                        <Skeleton className="h-4 w-[200px]" />
                      </div>
                    </div>
                  </div>
                ) : (
                  (() => {
                    // Attempt to parse the submissionResponse as JSON.
                    let parsed;
                    try {
                      parsed = JSON.parse(submissionResponse);
                    } catch (e) {
                      parsed = null;
                    }

                    if (
                      parsed &&
                      typeof parsed === "object" &&
                      "disclaimer" in parsed &&
                      "results" in parsed &&
                      Array.isArray(parsed.results)
                    ) {
                      return (
                        <Box>
                          <Typography
                            variant="body2"
                            sx={{ fontStyle: "italic", mb: 1 }}
                          >
                            {parsed.disclaimer}
                          </Typography>
                          {parsed.results.map((result: any, index: number) => (
                            <Box
                              key={index}
                              sx={{
                                display: "flex",
                                mb: 1,
                              }}
                            >
                              <div>
                                {result.passed ? (
                                  <CircleCheck
                                    color="green"
                                    style={{ marginRight: 8 }}
                                  />
                                ) : (
                                  <CircleX
                                    color="red"
                                    style={{ marginRight: 8 }}
                                  />
                                )}
                              </div>
                              <Typography
                                variant="body1"
                                sx={{
                                  whiteSpace: "pre-wrap",
                                  wordBreak: "break-word",
                                }}
                              >
                                {result.name}: {result.message}
                              </Typography>
                            </Box>
                          ))}
                        </Box>
                      );
                    } else {
                      return (
                        <Typography
                          variant="body1"
                          sx={{
                            whiteSpace: "pre-wrap",
                            wordBreak: "break-word",
                          }}
                        >
                          {submissionResponse ||
                            "No output yet. Run your code to see the result here."}
                        </Typography>
                      );
                    }
                  })()
                )}
              </Box>
            </Paper>
          </Box>

          {/* File Upload and Action Buttons */}
          <Box
            sx={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            {/* Box for submit code button */}
            <Box sx={{ display: "flex", gap: 2 }}>
              <Button
                variant="contained"
                color="primary"
                onClick={() =>
                  handleQuestionSubmission(String(question.num), code)
                }
              >
                Submit
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
          <Box>
            <Typography variant="h6" sx={{ mb: 2, textAlign: "center" }}>
              Global Documentation
            </Typography>
            <List
              sx={{
                paddingLeft: "1rem",
                paddingRight: "1rem",
                "& .MuiListItem-root": {
                  padding: "0.5rem 0",
                },
              }}
            >
              {/* Static Documentation Link */}
              <ListItem
                sx={{
                  padding: 0,
                  marginBottom: "0.5rem",
                  borderRadius: "4px",
                  "&:hover": {
                    backgroundColor: "rgba(0, 0, 0, 0.04)",
                  },
                }}
              >
                <MuiLink
                  to="/python_docs/index.html"
                  target="_blank"
                  rel="noopener noreferrer"
                  underline="none"
                  sx={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    width: "100%",
                    height: "100%",
                    color: "#1976d2",
                    fontSize: "1rem",
                    fontWeight: 500,
                    textAlign: "center",
                    cursor: "pointer",
                    "&:hover": {
                      textDecoration: "underline",
                      color: "secondary.main",
                    },
                  }}
                  component={Link}
                >
                  Python 3 Documentation
                </MuiLink>
              </ListItem>

              {/* Dynamic Documentation Links */}
              {globalDocs.map((doc) => (
                <ListItem
                  key={doc.title}
                  sx={{
                    padding: 0,
                    marginBottom: "0.5rem",
                    borderRadius: "4px",
                    "&:hover": {
                      backgroundColor: "rgba(0, 0, 0, 0.04)",
                    },
                  }}
                >
                  <MuiLink
                    underline="none"
                    sx={{
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      width: "100%",
                      height: "100%",
                      color: "primary.main",
                      fontSize: "1rem",
                      fontWeight: 500,
                      textAlign: "center",
                      cursor: "pointer",
                      "&:hover": {
                        textDecoration: "underline",
                        color: "secondary.main",
                      },
                    }}
                    onClick={() => openDocInNewTab(doc)}
                  >
                    {doc.title}
                  </MuiLink>
                </ListItem>
              ))}
            </List>
          </Box>
        </Box>
      )}
    </Box>
  );
};

export default SubmissionWidget;
