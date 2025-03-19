import { jwtDecode } from "jwt-decode";
import { styled } from "@mui/system";

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import ESNavBar from "../components/ESNavBar";
import CreateTeamWidget from "@/components/CreateTeamWidget";
import EditTeamWidget from "@/components/EditTeamWidget";
import GetTeamSubmissionWidget from "@/components/GetSubmissionWidget";

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

import { PencilLine, Trash2, Download } from "lucide-react";

const LayoutContainer = styled("div")({
  display: "flex",
  height: "100vh",
  width: "100vw",
  overflow: "hidden",
});

interface DecodedToken {
  is_admin: boolean;
}

export default function TeamManager() {
  const navigate = useNavigate();
  const [teams, setTeams] = useState([]);
  const [teamMembers, setTeamMembers] = useState<{ [key: number]: string[] }>(
    {}
  );
  const [scores, setScores] = useState<
    Array<{
      "Team Number": string;
      Score: string;
      "Max Score": string;
    }>
  >([]);

  const getUserRole = (token: string): boolean => {
    try {
      const decoded = jwtDecode<DecodedToken>(token);
      return decoded.is_admin;
    } catch (error) {
      console.error("Invalid token:", error);
      return false;
    }
  };

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      console.error("No token found");
      navigate("/login");
      return;
    }

    console.log("Token found:", token);

    const isAdmin = getUserRole(token);

    if (!isAdmin) {
      console.error("User is not an admin");
      localStorage.removeItem("token");
      navigate("/login");
    }
    void fetchTeams();
    void fetchScores();
  }, [navigate]);

  const fetchTeams = async () => {
    try {
      const response = await fetch("/api/team/all", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      if (!response.ok) {
        console.error("Failed to fetch teams");
        return;
      }

      const data = await response.json();
      setTeams(data);

      data.forEach((team: { id: number }) => {
        void fetchTeamMembers(team.id);
      });

      console.log("Teams:", data);
    } catch (error) {
      console.error("Error fetching teams:", error);
    }
  };

  const fetchTeamMembers = async (teamId: number) => {
    try {
      const response = await fetch(`/api/team/members?team_id=${teamId}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      if (!response.ok) {
        console.error(`Failed to fetch members for team ${teamId}`);
        return;
      }

      const data = await response.json();
      setTeamMembers((prev) => ({
        ...prev,
        [teamId]: data.map(
          (m: { first_name: string; last_name: string }) =>
            `${m.first_name} ${m.last_name}`
        ),
      }));
      console.log(`Team ${teamId} members:`, data);
    } catch (error) {
      console.error("Error fetching team members:", error);
    }
  };

  const fetchScores = async () => {
    try {
      const response = await fetch("/api/score", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      if (!response.ok) throw new Error("Failed to fetch scores");

      const data = await response.json();
      setScores(data);
    } catch (error) {
      console.error("Error fetching scores:", error);
    }
  };

  const handleEdit = (teamId: number) => {
    // Handle edit team
    console.log("Edit team:", teamId);
  };

  const handleDelete = async (teamId: number) => {
    try {
      const response = await fetch(`/api/team/${teamId}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to delete team");
      }

      console.log("Team deleted successfully");
      await fetchTeams();
    } catch (error) {
      console.error("Error deleting team:", error);
    }
  };

  const handleCreate = () => {
    void fetchTeams();
  };

  const handleDownload = async () => {
    try {
      await fetch("/api/score", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      const response = await fetch("/api/score/download", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      if (!response.ok) throw new Error("Failed to download file");

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "scores.csv";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
      await fetchScores();
    } catch (error) {
      console.error("Download error:", error);
    }
  };

  return (
    <LayoutContainer>
      <ESNavBar />

      {/* Main Content */}
      <main className="flex-1 flex flex-col gap-4 p-4 overflow-y-hidden">
        {/* Team Management Card */}
        <Card className="max-h-md w-full flex flex-col h-[calc(100vh-26rem)]">
          <CardHeader>
            <CardTitle className="text-xl font-bold">Team Management</CardTitle>
            <CardDescription>Manage all competition teams</CardDescription>
            <Separator />
          </CardHeader>

          <CardContent className="flex-1 overflow-y-auto pb-4">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-[200px]">Team Name</TableHead>
                  {/* <TableHead>Password</TableHead> */}
                  <TableHead>Members</TableHead>
                  <TableHead>Score</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {teams.map((team) => (
                  <TableRow key={team.id}>
                    <TableCell className="font-medium">{team.name}</TableCell>
                    {/* <TableCell>{team.password}</TableCell> */}
                    <TableCell>
                      {teamMembers[team.id]?.length
                        ? teamMembers[team.id].join(", ")
                        : "No members"}
                    </TableCell>
                    <TableCell>
                      {scores.find((s) => s["Team Number"] === team.name)
                        ? `${
                            scores.find((s) => s["Team Number"] === team.name)
                              ?.Score
                          } / ${
                            scores.find(
                              (s) => s["Team Number"] === team.name
                            )?.["Max Score"]
                          }`
                        : "N/A"}
                    </TableCell>
                    <TableCell className="flex gap-2 justify-end">
                      <EditTeamWidget team={team} onSave={handleEdit} />
                      <Button
                        size="icon"
                        variant="ghost"
                        onClick={() => handleDelete(team.id)}
                      >
                        <Trash2 className="w-4 h-4 text-[#FE7A7A] hover:text-[#ffcfcf]" />
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>

          <CardFooter className="flex justify-between pt-4">
            <CreateTeamWidget teams={teams} onCreate={handleCreate} />

            <Button variant="secondary" onClick={handleDownload}>
              <Download className="w-4 h-4 mr-2" />
              Download Scores
            </Button>
          </CardFooter>
        </Card>

        {/* Submissions Card */}
        <GetTeamSubmissionWidget />
      </main>
    </LayoutContainer>
  );
}
