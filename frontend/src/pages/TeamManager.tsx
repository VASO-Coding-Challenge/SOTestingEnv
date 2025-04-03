import { jwtDecode } from "jwt-decode";
import { styled } from "@mui/system";
import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import ESNavBar from "../components/ESNavBar";
import CreateTeamWidget from "@/components/CreateTeamWidget";
import ConfirmationAlert from "@/components/ConfirmationAlert";
import GetTeamSubmissionWidget from "@/components/GetSubmissionWidget";
import { Skeleton } from "@/components/ui/skeleton";

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

import { Team, TeamMember, TeamScore } from "@/models/team";

import { Trash2, Download } from "lucide-react";

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
  const [teams, setTeams] = useState<Team[]>([]);
  const [teamMembers, setTeamMembers] = useState<{ [key: number]: string[] }>(
    {}
  );
  const [scores, setScores] = useState<TeamScore[]>([]);
  const [isLoadingTeams, setIsLoadingTeams] = useState(true);
  const [isLoadingScores, setIsLoadingScores] = useState(true);
  const [loadingMembers, setLoadingMembers] = useState<{
    [key: number]: boolean;
  }>({});

  const getUserRole = (token: string): boolean => {
    try {
      const decoded = jwtDecode<DecodedToken>(token);
      return decoded.is_admin;
    } catch (error) {
      console.error("Invalid token:", error);
      return false;
    }
  };

  const fetchTeams = useCallback(async () => {
    setIsLoadingTeams(true);
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

      const data: Team[] = (await response.json()) as Team[];
      setTeams(data);

      // Initialize loading state for each team's members
      const membersLoadingState: { [key: number]: boolean } = {};
      data.forEach((team: { id: number }) => {
        membersLoadingState[team.id] = true;
        void fetchTeamMembers(team.id);
      });
      setLoadingMembers(membersLoadingState);

      console.log("Teams:", data);
    } catch (error) {
      console.error("Error fetching teams:", error);
    } finally {
      setIsLoadingTeams(false);
    }
  }, []);

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
  }, [navigate, fetchTeams]);

  const fetchScores = async () => {
    setIsLoadingScores(true);
    try {
      const response = await fetch("/api/score", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      if (!response.ok) throw new Error("Failed to fetch scores");

      const data: TeamScore[] = (await response.json()) as TeamScore[];
      setScores(data);
    } catch (error) {
      console.error("Error fetching scores:", error);
    } finally {
      setIsLoadingScores(false);
    }
  };

  const fetchTeamMembers = async (teamId: number) => {
    try {
      const response = await fetch(`/api/team/${teamId}/members`, {
        // Path parameter instead of query
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

      const data: TeamMember[] = (await response.json()) as TeamMember[];
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
    } finally {
      setLoadingMembers((prev) => ({
        ...prev,
        [teamId]: false,
      }));
    }
  };

  // const handleEdit = (teamId: number) => {
  //   // Handle edit team
  //   console.log("Edit team:", teamId);
  // };

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

  const handleDeleteAll = async () => {
    try {
      const response = await fetch("/api/team", {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to delete all teams");
      }

      await fetchTeams();
    } catch (error) {
      console.error("Error deleting all teams:", error);
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

  // Skeleton row component for loading state
  const SkeletonRow = () => (
    <TableRow>
      <TableCell>
        <Skeleton className="h-5 w-[180px]" />
      </TableCell>
      <TableCell>
        <Skeleton className="h-5 w-[250px]" />
      </TableCell>
      <TableCell>
        <Skeleton className="h-5 w-[100px]" />
      </TableCell>
      <TableCell className="flex gap-2 justify-end">
        <Skeleton className="h-8 w-8 rounded-md" />
      </TableCell>
    </TableRow>
  );

  return (
    <LayoutContainer>
      <ESNavBar />

      {/* Main Content */}
      <main className="flex-1 flex flex-col gap-4 p-4 overflow-y-hidden">
        {/* Team Management Card */}
        <Card className="w-full flex flex-col max-h-[calc(100vh_-_24rem)] overflow-hidden">
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
                  <TableHead>Members</TableHead>
                  <TableHead>Score</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {isLoadingTeams
                  ? // Show skeleton rows when loading
                    Array(5)
                      .fill(0)
                      .map((_, index) => (
                        <SkeletonRow key={`skeleton-${index}`} />
                      ))
                  : teams.map((team: Team) => (
                      <TableRow key={team.id}>
                        <TableCell className="font-medium">
                          {team.name}
                        </TableCell>
                        <TableCell>
                          {loadingMembers[team.id] ? (
                            <Skeleton className="h-5 w-[250px]" />
                          ) : teamMembers[team.id]?.length ? (
                            teamMembers[team.id].join(", ")
                          ) : (
                            "No members"
                          )}
                        </TableCell>
                        <TableCell>
                          {isLoadingScores ? (
                            <Skeleton className="h-5 w-[100px]" />
                          ) : scores.find(
                              (s) => s["Team Number"] === team.name
                            ) ? (
                            `${
                              scores.find((s) => s["Team Number"] === team.name)
                                ?.Score
                            } / ${
                              scores.find(
                                (s) => s["Team Number"] === team.name
                              )?.["Max Score"]
                            }`
                          ) : (
                            "N/A"
                          )}
                        </TableCell>
                        <TableCell className="flex gap-2 justify-end">
                          <ConfirmationAlert
                            title="Delete Team"
                            description="Are you sure you want to delete this team?"
                            actionText="Delete"
                            cancelText="Cancel"
                            onAction={() => {
                              void handleDelete(team.id);
                            }}
                            trigger={
                              <Button size="icon" variant="ghost">
                                <Trash2 className="w-4 h-4 text-[#FE7A7A] hover:text-[#ffcfcf]" />
                              </Button>
                            }
                          />
                        </TableCell>
                      </TableRow>
                    ))}
              </TableBody>
            </Table>
          </CardContent>

          <CardFooter className="flex justify-between pt-4">
            <CreateTeamWidget onCreate={handleCreate} />

            <div className="flex gap-2">
              <Button
                variant="secondary"
                onClick={() => {
                  void handleDownload();
                }}
                disabled={isLoadingScores}
              >
                {isLoadingScores ? (
                  <Skeleton className="h-4 w-4 mr-2 rounded-full" />
                ) : (
                  <Download className="w-4 h-4 mr-2" />
                )}
                Download Scores
              </Button>
              <ConfirmationAlert
                title="Delete All Teams"
                description="Are you sure you want to delete all teams?"
                actionText="Delete All"
                cancelText="Cancel"
                onAction={() => {
                  void handleDeleteAll();
                }}
                trigger={
                  <Button variant="destructive">
                    <Trash2 className="w-4 h-4 text-white" />
                    Delete All Teams
                  </Button>
                }
              />
            </div>
          </CardFooter>
        </Card>

        {/* Submissions Card */}
        <GetTeamSubmissionWidget
          teamNames={teams.map((team: Team) => team.name)}
        />
      </main>
    </LayoutContainer>
  );
}
