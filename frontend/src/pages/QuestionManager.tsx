import { jwtDecode } from "jwt-decode";
import { styled } from "@mui/system";

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import ESNavBar from "../components/ESNavBar";

import SubmissionWidgetCopy from "../components/SubmissionWidgetCopy";
import { QuestionsPublic, Question, Document } from "../models/questions";
import LeftSideBarCopy from "../components/LeftSideBarCopy";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";

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
      <div className="fixed">
        <LeftSideBarCopy
          num={questions?.length ?? 0}
          onTabClick={handleQuestionClick}
        ></LeftSideBarCopy>
      </div>
      <section className="w-4/5 prose px-3 pt-3 overscroll-contain ml-[200px]">
        <Markdown className="markdown" remarkPlugins={[remarkGfm]}>
          {"## Problem " + selectedQuestion?.num}
        </Markdown>
        <Markdown className="markdown" remarkPlugins={[remarkGfm]}>
          {selectedQuestion?.writeup}
        </Markdown>
      </section>
      {/** The selected question and the global docs get passed in as props. */}
       {selectedQuestion && (
        <SubmissionWidgetCopy question={selectedQuestion} globalDocs={globalDocs} />
      )}
    </div>
    </LayoutContainer>
  );
};

