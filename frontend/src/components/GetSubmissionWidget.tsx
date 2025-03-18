import { useState } from "react";


// Fake data for teams and questions
const fakeTeams = [
  { id: "1", name: "Team Alpha" },
  { id: "2", name: "Team Beta" },
  { id: "3", name: "Team Gamma" },
];

const fakeQuestions = [
  { id: "101", text: "Question 1" },
  { id: "102", text: "Question 2" },
  { id: "103", text: "Question 3" },
];

export default function GetTeamSubmissions() {
    const [selectedTeam, setSelectedTeam] = useState("");
    const [selectedQuestion, setSelectedQuestion] = useState("");
  
    const handleGetSubmissions = () => {
      console.log(`Fetching submissions for Team: ${selectedTeam}, Question: ${selectedQuestion}`);
    };
  
    return (
      <div className="p-4 border border-gray-300 rounded-md w-96 m-5 space-y-4 bg-white shadow-md">
        <h2 className="text-lg font-bold">Submissions</h2>
  
        {/* Team Selection */}
        <select
          className="w-full p-2 border rounded-md"
          value={selectedTeam}
          onChange={(e) => setSelectedTeam(e.target.value)}
        >
          <option value="" disabled>Select Team</option>
          {fakeTeams.map((team) => (
            <option key={team.id} value={team.id}>
              {team.name}
            </option>
          ))}
        </select>
  
        {/* Question Selection */}
        <select
          className="w-full p-2 border rounded-md"
          value={selectedQuestion}
          onChange={(e) => setSelectedQuestion(e.target.value)}
        >
          <option value="" disabled>Select Question</option>
          {fakeQuestions.map((question) => (
            <option key={question.id} value={question.id}>
              {question.text}
            </option>
          ))}
        </select>
  
        {/* Get Button */}
        <button
          className="w-full p-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:bg-gray-300"
          onClick={handleGetSubmissions}
          disabled={!selectedTeam || !selectedQuestion}
        >
          Get
        </button>
      </div>
    );
  }