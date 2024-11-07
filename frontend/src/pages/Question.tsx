import React, { useEffect, useState } from "react";
import SubmissionWidget from "../components/SubmissionWidget";
import { QuestionsPublic, Question, Document } from "../models/questions";

const QuestionPage = () => {
  const [questions, setQuestions] = useState<Question[] | null>(null);
  const [selectedQuestion, setSelectedQuestion] = useState<Question | null>(
    null
  );
  const [globalDocs, setGlobalDocs] = useState<Document[]>([]);

  useEffect(() => {
    fetch("/api/questions/questions", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
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

  const handleQuestionClick = (questionNum: number) => {
    const question = questions?.find((q) => q.num === questionNum) || null;
    setSelectedQuestion(question);
  };

  return (
    <div className="flex">
      <section>
        <h1>Questions</h1>
        {questions ? (
          <div className="question-list">
            {questions.map((question) => (
              <div
                key={question.num}
                className="question-item"
                onClick={() => handleQuestionClick(question.num)}
                style={{ cursor: "pointer", marginBottom: "10px" }}
              >
                <h2>Question {question.num}</h2>
                <p>{question.writeup}</p>
                <span>🔍 Click for details</span>
              </div>
            ))}
          </div>
        ) : (
          <p>Loading questions...</p>
        )}
      </section>

      {selectedQuestion && (
        <SubmissionWidget question={selectedQuestion} globalDocs={globalDocs} />
      )}
    </div>
  );
};

export default QuestionPage;
