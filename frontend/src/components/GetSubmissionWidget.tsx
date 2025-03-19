import { useState } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";

export default function GetTeamSubmissionWidget() {
  const [selectedTeam, setSelectedTeam] = useState("");
  const [selectedQuestion, setSelectedQuestion] = useState("");

  const handleGetSubmissions = () => {
    console.log(
      `Fetching submissions for Team: ${selectedTeam}, Question: ${selectedQuestion}`
    );
  };

  return (
    <Card className="w-fit min-w-[300px] flex flex-col">
      <CardHeader>
        <CardTitle className="text-xl font-bold">Submissions</CardTitle>
        <CardDescription>Team submission history</CardDescription>
        <Separator />
      </CardHeader>
      <CardContent className="flex-1 overflow-y-auto">
        <CardTitle>Get Submissions</CardTitle>
      </CardContent>
    </Card>
  );
}
