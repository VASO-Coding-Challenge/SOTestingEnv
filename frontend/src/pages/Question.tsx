import { useEffect, useState } from "react";
import SubmissionWidget from "../components/SubmissionWidget";
import { QuestionsPublic, Question, Document } from "../models/questions";
import LeftSideBar from "../components/LeftSideBar";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { useNavigate } from "react-router-dom";
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable";

const QuestionPage = () => {
  const [questions, setQuestions] = useState<Question[] | null>(null);
  const [selectedQuestion, setSelectedQuestion] = useState<Question | null>(
    null
  );
  const [globalDocs, setGlobalDocs] = useState<Document[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    const handleUnauthorized = (status: number) => {
      localStorage.removeItem("token");
      navigate(status === 401 ? "/login" : "/thank-you");
    };

    fetch("/api/questions", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    })
      .then((response) => {
        if (response.status === 401 || response.status === 403) {
          handleUnauthorized(response.status);
          return null;
        }
        if (!response.ok) {
          throw new Error(`HTTP Error with Status Code: ${response.status}`);
        }
        return response.json();
      })
      .then((responseData: QuestionsPublic) => {
        if (responseData && responseData.questions) {
          setQuestions(responseData.questions);
          setGlobalDocs(responseData.global_docs);
          setSelectedQuestion(responseData.questions[0]);
        } else {
          console.warn("No Questions Found.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }, [navigate]);

  // State stores the selected question.
  const handleQuestionClick = (questionNum: number) => {
    const question = questions?.find((q) => q.num - 1 === questionNum) || null;
    setSelectedQuestion(question);
  };

  return (
    <div className="flex flex-row">
      <div>
        <LeftSideBar
          num={questions?.length ?? 0}
          onTabClick={handleQuestionClick}
        ></LeftSideBar>
      </div>
      <ResizablePanelGroup direction="horizontal">
        <ResizablePanel className="overscroll-contain">
          <div className="px-3 pt-3">
            <Markdown className="markdown" remarkPlugins={[remarkGfm]}>
              {"## Problem " + selectedQuestion?.num}
            </Markdown>
            <Markdown className="markdown" remarkPlugins={[remarkGfm]}>
              {selectedQuestion?.writeup}
            </Markdown>
          </div>
        </ResizablePanel>
        <ResizableHandle withHandle></ResizableHandle>
        {/** The selected question and the global docs get passed in as props. */}
        <ResizablePanel defaultSize={50}>
          {selectedQuestion && (
            <SubmissionWidget
              question={selectedQuestion}
              globalDocs={globalDocs}
            />
          )}
        </ResizablePanel>
      </ResizablePanelGroup>
    </div>
  );
};

export default QuestionPage;
