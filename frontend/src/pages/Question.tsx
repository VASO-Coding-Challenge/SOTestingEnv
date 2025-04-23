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

    let redirectTimer: ReturnType<typeof setTimeout>;

    const init = async () => {
      const token = localStorage.getItem("token") ?? "";
      const nowRes = await fetch("/api/now", {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });
      if (!nowRes.ok) {
        console.error("Failed to fetch server time");
        navigate("/login");
        return;
      }
      const { now } = await nowRes.json(); // { now: "2025-04-16T18:30:00.000Z" }
      const serverMs = new Date(now).getTime();

      // 1b) fetch team/session info
      const teamRes = await fetch("/api/team", {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });
      if (teamRes.status === 401 || teamRes.status === 403) {
        handleUnauthorized(teamRes.status);
        return;
      }
      if (!teamRes.ok) {
        console.error("Could not load team info");
        navigate("/thank-you");
        return;
      }
      const teamData = (await teamRes.json()) as {
        session: { end_time: string };
      };
      const endMs = new Date(teamData.session.end_time).getTime();

      if (serverMs > endMs) {
        navigate("/thank-you");
        return;
      }

      const msUntilEnd = endMs - serverMs;
      redirectTimer = setTimeout(() => {
        navigate("/thank-you");
      }, msUntilEnd);
    };

    void init();

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

    return () => {
      if (redirectTimer) clearTimeout(redirectTimer);
    };
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
