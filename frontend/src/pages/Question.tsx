import React, { useEffect, useState } from "react";
import SubmissionWidget from "../components/SubmissionWidget";
import { QuestionsPublic, Question, Document } from "../models/questions";
import LeftSideBar from "../components/LeftSideBar";
import Markdown from "react-markdown";
import { LogOut } from "../components/LogOutButton";
import remarkGfm from "remark-gfm";

const QuestionPage = () => {
  const [questions, setQuestions] = useState<Question[] | null>(null);
  const [selectedQuestion, setSelectedQuestion] = useState<Question | null>(
    null
  );
  const [submissionResponse, setSubmissionResponse] = useState("");
  const [globalDocs, setGlobalDocs] = useState<Document[]>([]);

  useEffect(() => {
    fetch("/api/questions", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP Error with Status Code: ${response.status}`);
        }
        return response.json();
      })
      .then((responseData: QuestionsPublic) => {
        setQuestions(responseData.questions);
        setGlobalDocs(responseData.global_docs);
        setSelectedQuestion(responseData.questions[0]);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }, []);

  useEffect(() => {
    console.log(submissionResponse);
  }, [submissionResponse]);

  const handleQuestionSubmission = (questionNum: string, code: string) => {
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



  // State stores the selected question.
  const handleQuestionClick = (questionNum: number) => {
    const question = questions?.find((q) => q.num - 1 === questionNum) || null;
    setSelectedQuestion(question);
  };

  return (
    <div className="flex">
      <div className="fixed">
        <LeftSideBar
          num={questions?.length}
          onTabClick={handleQuestionClick}
        ></LeftSideBar>
      </div>
      <section className="w-4/6 prose px-3 pt-3 overscroll-contain ml-[200px]">
        {/**<p className="text-2xl">{`Problem ` + selectedQuestion?.num}</p> */}
        <Markdown className="markdown" remarkPlugins={[remarkGfm]}>
          {"## Problem " + selectedQuestion?.num}
        </Markdown>
        <Markdown className="markdown" remarkPlugins={[remarkGfm]}>{selectedQuestion?.writeup}</Markdown>
      </section>
      <button onClick={() => handleQuestionSubmission("3", "def func(arr):\n\treturn max(arr)\nprint(func([1,2,4,5,10,100]))")}>
        Submit
      </button> 
      {/** The selected question and the global docs get passed in as props. */}
      {selectedQuestion && (
        <SubmissionWidget question={selectedQuestion} globalDocs={globalDocs} />
      )}
    </div>
  );
};

export default QuestionPage;
