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
  Divider
} from "@mui/material";
import { SubmissionWidgetProps } from "../models/submission";
import UploadIcon from "@mui/icons-material/Upload";
import RestoreIcon from '@mui/icons-material/Restore';
import DownloadIcon from '@mui/icons-material/Download';
import Tooltip from "@mui/material/Tooltip";
import { Editor } from "@monaco-editor/react";
import { Link } from "react-router-dom";

type SubmissionResponse = {
  console_log: string;
};

const SubmissionWidgetCopy: React.FC<SubmissionWidgetProps> = ({
  question,
  globalDocs,
}) => {
  const [activeTab, setActiveTab] = useState<"submission" | "docs">(
    "submission"
  );
  const [docsTab, setDocsTab] = useState<"question" | "global">("question");
  const [code, setCode] = useState<string>(
    sessionStorage.getItem(`question_1`) ||
      question.starter_code 
  );

  const [submissionResponse, setSubmissionResponse] = useState<string>(
    sessionStorage.getItem(`output_1`) || "No Submission Yet"
  );

  useEffect(() => {
    sessionStorage.setItem(`question_${question.num}`, code);
  }, [code]);

  useEffect(() => {
    sessionStorage.setItem(`output_${question.num}`, submissionResponse);
  }, [submissionResponse]);

  useEffect(() => {
    if (question){
    const savedCode =
      sessionStorage.getItem(`question_${question.num}`) ||
      question.starter_code || "# Start Coding Here";
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




  const handleTabSwitch = (tab: "Autograder" | "docs") => {
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
        onChange={(_event, newValue) => handleTabSwitch(newValue)}
        variant="fullWidth"
        indicatorColor="secondary"
        textColor="secondary"
      >
        <Tab value="autograder" label="autograder" />
        <Tab value="docs" label="Docs" />
      </Tabs>

      {/* Submission Tab */}
      {activeTab === "autograder" && (
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
              position: "relative",
              mb: 2,
              paddingTop: "50px",
            }}
          >
            <p>demo test case</p>
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

export default SubmissionWidgetCopy
