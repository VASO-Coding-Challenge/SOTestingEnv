import { useState, useEffect } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import JSZip from "jszip";
import { saveAs } from "file-saver";

export default function GetTeamSubmissionWidget({
  teamNames,
}: {
  teamNames: string[];
}) {
  const [selectedTeam, setSelectedTeam] = useState("");
  const [selectedQuestion, setSelectedQuestion] = useState("");
  const [questions, setQuestions] = useState<number[]>([]);
  const [teamScope, setTeamScope] = useState<"all" | "specific">("specific");
  const [questionScope, setQuestionScope] = useState<"all" | "specific">("all");

  useEffect(() => {
    if (teamScope === "all") {
      setQuestionScope("all");
      setSelectedQuestion("");
    }
    void fetchQuestions();
  }, [teamScope]);

  const fetchQuestions = async () => {
    try {
      const response = await fetch("/api/problems/", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      const text = await response.text(); // Read as plain text first
      console.log("Raw response:", text);

      if (!response.ok)
        throw new Error(
          `HTTP Error: ${response.status} ${response.statusText}`
        );

      const data: number[] = JSON.parse(text); // Manually parse
      setQuestions(data);
    } catch (error) {
      console.error("Error fetching questions:", error);
    }
  };

  const handleDownload = async () => {
    if (teamScope === "all") {
      await fetchAndDownloadAllSubmissions();
    } else {
      if (!selectedTeam) return alert("Please select a team");

      if (questionScope === "all") {
        await fetchAndDownloadTeamSubmissions(selectedTeam);
      } else {
        if (!selectedQuestion) return alert("Please select a question");
        await fetchAndDownloadSingleSubmission(selectedTeam, selectedQuestion);
      }
    }
  };

  const fetchAndDownloadTeamSubmissions = async (teamName: string) => {
    try {
      const response = await fetch(`/api/submissions/team/${teamName}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      const submissions = await response.json();
      const zip = new JSZip();

      Object.entries(submissions).forEach(([problemNum, code]) => {
        zip.file(`problem_${problemNum}.py`, code as string);
      });

      const content = await zip.generateAsync({ type: "blob" });
      saveAs(content, `${teamName}_submissions.zip`);
    } catch (error) {
      console.error("Download error:", error);
      alert("Failed to download submissions");
    }
  };

  const fetchAndDownloadSingleSubmission = async (
    teamName: string,
    problemNum: string
  ) => {
    try {
      const response = await fetch(
        `/api/submissions/team/${teamName}/problem/${problemNum}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );

      const code = await response.text();
      saveAs(new Blob([code]), `problem_${problemNum}_${teamName}.py`);
    } catch (error) {
      console.error("Download error:", error);
      alert("Failed to download submission");
    }
  };

  const fetchAndDownloadAllSubmissions = async () => {
    try {
      const response = await fetch("/api/submissions/all", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      const data = await response.json();
      const zip = new JSZip();

      Object.entries(data).forEach(([teamName, submissions]) => {
        const teamFolder = zip.folder(teamName);
        Object.entries(submissions as Record<string, string>).forEach(
          ([problemNum, code]) => {
            teamFolder?.file(`problem_${problemNum}.py`, code);
          }
        );
      });

      const content = await zip.generateAsync({ type: "blob" });
      saveAs(content, "all_submissions.zip");
    } catch (error) {
      console.error("Download error:", error);
      alert("Failed to download all submissions");
    }
  };

  const isDisabled =
    teamScope === "specific"
      ? questionScope === "specific"
        ? !selectedTeam || !selectedQuestion
        : !selectedTeam
      : false;

  return (
    <Card className="w-full max-w-2xl">
      <CardHeader>
        <CardTitle className="text-xl font-bold">Submissions</CardTitle>
        <CardDescription>Download team code submissions</CardDescription>
        <Separator />
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <CardTitle>Team Selection</CardTitle>
          <RadioGroup
            value={teamScope}
            onValueChange={(v: "all" | "specific") => setTeamScope(v)}
            className="flex gap-4"
          >
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="specific" id="specific-team" />
              <Label htmlFor="specific-team">Specific Team</Label>
            </div>
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="all" id="all-teams" />
              <Label htmlFor="all-teams">All Teams</Label>
            </div>
          </RadioGroup>
        </div>

        {teamScope === "specific" && (
          <div className="space-y-2">
            <Label>Select Team</Label>
            <Select value={selectedTeam} onValueChange={setSelectedTeam}>
              <SelectTrigger>
                <SelectValue placeholder="Select a team" />
              </SelectTrigger>
              <SelectContent>
                {teamNames.map((team) => (
                  <SelectItem key={team} value={team}>
                    {team}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        )}

        {teamScope === "specific" && (
          <div className="space-y-2">
            <CardTitle>Question Selection</CardTitle>
            <RadioGroup
              value={questionScope}
              onValueChange={(v: "all" | "specific") => setQuestionScope(v)}
              className="flex gap-4"
            >
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="all" id="all-questions" />
                <Label htmlFor="all-questions">All Questions</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="specific" id="specific-question" />
                <Label htmlFor="specific-question">Specific Question</Label>
              </div>
            </RadioGroup>
          </div>
        )}

        {teamScope === "specific" && questionScope === "specific" && (
          <div className="space-y-2">
            <Label>Select Question</Label>
            <Select
              value={selectedQuestion}
              onValueChange={setSelectedQuestion}
            >
              <SelectTrigger>
                <SelectValue placeholder="Select a question" />
              </SelectTrigger>
              <SelectContent>
                {questions.map((problemNumber) => (
                  <SelectItem
                    key={problemNumber}
                    value={problemNumber.toString()}
                  >
                    Problem {problemNumber}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        )}

        <Button
          onClick={handleDownload}
          disabled={isDisabled}
          className="w-full"
        >
          Download Submissions
        </Button>
      </CardContent>
    </Card>
  );
}
