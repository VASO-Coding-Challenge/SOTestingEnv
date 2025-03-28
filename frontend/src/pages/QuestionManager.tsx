import { jwtDecode } from "jwt-decode";
import { styled } from "@mui/system";

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import ESNavBar from "../components/ESNavBar";

import { QuestionsPublic, Question, Document } from "../models/questions";
import LeftSideBarCopy from "../components/LeftSideBarCopy";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Editor } from "@monaco-editor/react"

import { Box, Typography, List, ListItem, Link as MuiLink } from "@mui/material";
import { Link } from "react-router-dom";



const LayoutContainer = styled("div")({
  display: "flex",
  height: "100vh",
  width: "100vw",
  overflow: "hidden",
});

export default function QuestionManager() {
  const [questions, setQuestions] = useState<Question[] | null>([
    {
      num: 1,
      writeup: "Write a function that calculates the factorial of a given number.",
      starter_code: "function factorial(n) {\n  // Your code here\n}" 
    },
    {
      num: 2,
      writeup: "Implement a function to check if a given string is a palindrome.",
      starter_code: "function isPalindrome(str) {\n  // Your code here\n}"
    },
    {
      num: 3,
      writeup: "Create a function that returns the nth Fibonacci number.",
      starter_code: "function fibonacci(n) {\n  // Your code here\n}"
    },
    {
      num: 4,
      writeup: "Write a function to sort an array using the Bubble Sort algorithm.",
      starter_code: "function bubbleSort(arr) {\n  // Your code here\n}"
    },
    {
      num: 5,
      writeup: "Develop a function that finds the maximum value in an array.",
      starter_code: "function findMax(arr) {\n  // Your code here\n}"
    }
  ]);

  const [activeTab, setActiveTab] = useState("autograder");
  
  const [selectedQuestion, setSelectedQuestion] = useState<Question | null>(
    null
  );
  const [globalDocs, setGlobalDocs] = useState<Document[]>([]);
  const navigate = useNavigate()
  //setSelectedQuestion(questions[0]);
  const getUserRole = (token: string): boolean => {
    try {
      const decoded = jwtDecode<DecodedToken>(token); // Explicitly type the decoded token
      return decoded.is_admin;
    } catch (error) {
      console.error("Invalid token:", error);
      return false;
    }
  };

  useEffect(() => {
    const token = localStorage.getItem("token");
    setSelectedQuestion(questions[0]);

    if (!token) {
      console.error("No token found");
      navigate("/login"); // Fix: Ensure navigate is defined
      return;
    }

    console.log("Token found:", token);

    const isAdmin = getUserRole(token);

    if (!isAdmin) {
      console.error("User is not an admin");
      localStorage.removeItem("token");
      navigate("/login"); // Fix: Ensure navigate is defined
    }
  }, [navigate]);

  const handleQuestionClick = (questionNum: number) => {
    const question = questions?.find((q) => q.num - 1 === questionNum) || null;
    setSelectedQuestion(question);
  };

  return (
    <LayoutContainer>
      <ESNavBar />
      <div className="flex">
        {/* Sidebar */}
        <div className="w-64 fixed h-full bg-white shadow-md">
          <LeftSideBarCopy num={questions?.length ?? 0} onTabClick={handleQuestionClick} />
        </div>

        {/* Main Content */}
        <div className="flex-1 ml-64 p-6 grid grid-cols-2 gap-6 w-[1200px]">
          {/* Left Side: Problem Statement & Starter Code */}
          <div className="col-span-1">
            <section className="w-full">
              <Markdown className="markdown text-2xl font-bold" remarkPlugins={[remarkGfm]}>
                {"## Problem " + selectedQuestion?.num}
              </Markdown>
              
              {/* Problem Statement */}
              <div className="mt-4 p-6 bg-white shadow-md rounded-lg">
                <p className="text-red-500 font-semibold">Prompt</p>
                <Editor className="h-72 w-full" value={selectedQuestion?.writeup} />
              </div>

              {/* Starter Code */}
              <div className="mt-6 p-6 bg-white shadow-md rounded-lg">
                <p className="text-red-500 font-semibold">Starter Code</p>
                <Editor className="h-72 w-full" value={selectedQuestion?.starter_code} />
              </div>
            </section>
          </div>

          {/* Right Side: Tabs for Autograder & Docs */}
          <div className="col-span-1 bg-white shadow-md rounded-lg">
            {/* Tabs */}
            <div className="flex border-b">
              <button
                className={`w-1/2 py-2 font-bold ${activeTab === "autograder" ? "border-b-4 border-red-500 text-red-500" : "text-gray-500"}`}
                onClick={() => setActiveTab("autograder")}
              >
                Autograder
              </button>
              <button
                className={`w-1/2 py-2 font-bold ${activeTab === "docs" ? "border-b-4 border-blue-500 text-blue-500" : "text-gray-500"}`}
                onClick={() => setActiveTab("docs")}
              >
                Docs
              </button>
            </div>

            {/* Autograder Tab */}
            {activeTab === "autograder" && (
              <div className="p-6">
                <div className="mb-4">
                  <p className="text-red-500 font-semibold">Demo Test Case(s)</p>
                  <Editor className="h-64 w-full" value={selectedQuestion?.demo_tests} />
                </div>

                <div>
                  <p className="text-red-500 font-semibold">Test Case(s)</p>
                  <Editor className="h-64 w-full" value={selectedQuestion?.test_cases} />
                </div>

                <button className="mt-6 w-full bg-blue-500 text-white py-2 rounded-md shadow-md text-lg font-bold">
                  SAVE
                </button>
              </div>
            )}

            {/* Docs Tab */}
            {activeTab === "docs" && (
              <Box sx={{ flex: 1, display: "flex", flexDirection: "column", padding: 3 }}>
                <Typography variant="h6" sx={{ mb: 2, textAlign: "center" }}>
                  Global Documentation
                </Typography>
                <List sx={{ paddingLeft: "1rem", paddingRight: "1rem" }}>
                  {/* Static Documentation Link */}
                  <ListItem sx={{ padding: 0, marginBottom: "0.5rem", borderRadius: "4px", "&:hover": { backgroundColor: "rgba(0, 0, 0, 0.04)" } }}>
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
                        "&:hover": { textDecoration: "underline", color: "secondary.main" },
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
                      sx={{ padding: 0, marginBottom: "0.5rem", borderRadius: "4px", "&:hover": { backgroundColor: "rgba(0, 0, 0, 0.04)" } }}
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
                          "&:hover": { textDecoration: "underline", color: "secondary.main" },
                        }}
                        onClick={() => openDocInNewTab(doc)}
                      >
                        {doc.title}
                      </MuiLink>
                    </ListItem>
                  ))}
                </List>
              </Box>
            )}
          </div>
        </div>
      </div>
    </LayoutContainer>
  );
};

