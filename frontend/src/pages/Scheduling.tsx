import { styled } from "@mui/system";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
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
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Trash2, Plus, X } from "lucide-react";

import { jwtDecode } from "jwt-decode";

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import ESNavBar from "../components/ESNavBar";
import EditSessionWidget from "@/components/EditSessionWidget";

const LayoutContainer = styled("div")({
  display: "flex",
  height: "100vh",
  width: "100vw",
  overflow: "hidden",
});

interface DecodedToken {
  is_admin: boolean;
}

interface Session {
  id: number;
  name: string;
  start_time: string;
  end_time: string;
  teams: number[];
}

interface Team {
  name: string;
  id: number;
  session_id: number | null;
  session: Session | null;
}

export default function Scheduling() {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [teams, setTeams] = useState<Team[]>([]);

  // Form Input States
  const [sessionName, setSessionName] = useState("");
  const [sessionDate, setSessionDate] = useState("");
  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");
  const [selectedTeams, setSelectedTeams] = useState<Team[]>([]);
  const [selectedTeamId, setSelectedTeamId] = useState<number | null>();

  const navigate = useNavigate();

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

    void fetchSessions();
    void fetchTeams();
  }, [navigate]);

  const fetchSessions = async () => {
    try {
      const response = await fetch("/api/sessions", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      if (!response.ok) {
        console.error("Failed to fetch sessions");
        return;
      }

      const data = (await response.json()) as Session[];
      setSessions(data);
      console.log("Sessions:", data);
    } catch (error) {
      console.error("Error fetching sessions:", error);
    }
  };

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

      const data = (await response.json()) as Team[];
      setTeams(data);
      console.log("Teams:", data);
    } catch (error) {
      console.error("Error fetching teams:", error);
    }
  };

  const handleEditSession = async (
    updatedSession: Session,
    oldSession: Session
  ) => {
    const { teams, ...sessionWithoutTeams } = updatedSession;
    try {
      const response = await fetch(`/api/sessions/${updatedSession.id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify(sessionWithoutTeams),
      });

      if (!response.ok) {
        console.error("Failed to update session: ", response.status);
        return;
      }

      console.log("Session updated successfully");
    } catch (error) {
      console.error("Error updating session:", error);
    }

    const addedTeams = updatedSession.teams.filter(
      (teamId) => !oldSession.teams.includes(teamId)
    );
    const removedTeams = oldSession.teams.filter(
      (teamId) => !updatedSession.teams.includes(teamId)
    );

    try {
      const response = await fetch(`/api/sessions/${updatedSession.id}/teams`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify(addedTeams),
      });

      if (!response.ok) {
        console.error("Failed to add teams to session: ", response.status);
        return;
      }
    } catch (error) {
      console.error("Error adding teams to session:", error);
    }

    try {
      const response = await fetch(`/api/sessions/${updatedSession.id}/teams`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify(removedTeams),
      });

      if (!response.ok) {
        console.error("Failed to remove teams from session: ", response.status);
        return;
      }
    } catch (error) {
      console.error("Error removing teams from session:", error);
    }

    void fetchSessions();
  };

  const handleDeleteSession = async (sessionId: string) => {
    try {
      const response = await fetch(`/api/sessions/${sessionId}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      if (!response.ok) {
        console.error("Failed to delete session");
        return;
      }

      console.log("Session deleted successfully");
      void fetchSessions(); // Refresh sessions list
    } catch (error) {
      console.error("Error deleting session:", error);
    }
  };

  const handleGetTeamForSession = () => {
    // Fetch the team data for a session
    console.log("Fetching team data for a session");
  };

  // Form Input Handlers
  const handleSessionNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSessionName(e.target.value);
  };

  const handleSessionDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSessionDate(e.target.value);
  };

  const handleStartTimeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setStartTime(e.target.value);
  };

  const handleEndTimeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setEndTime(e.target.value);
  };

  const handleAddTeam = (teamId: number) => {
    const team = teams.find((t) => t.id === teamId);
    if (team && !selectedTeams.some((t) => t.id === team.id)) {
      setSelectedTeams([...selectedTeams, team]);
    }
  };

  const handleRemoveTeam = (teamId: number) => {
    setSelectedTeams(selectedTeams.filter((team) => team.id !== teamId));
  };

  const handleSubmit = async () => {
    if (!sessionName || !sessionDate || !startTime || !endTime) {
      alert("Please fill out all fields");
      return;
    }

    const startDateTime = `${sessionDate}T${startTime}:00Z`;
    const endDateTime = `${sessionDate}T${endTime}:00Z`;

    const sessionData = {
      name: sessionName,
      start_time: startDateTime,
      end_time: endDateTime,
      id: 0,
      // teams: selectedTeams.map((team) => team.id),
    };

    try {
      const response = await fetch("/api/sessions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify(sessionData),
      });

      if (!response.ok) {
        console.error("Failed to create session");
        return;
      }

      console.log("Session created successfully");
      setSessionName("");
      setSessionDate("");
      setStartTime("");
      setEndTime("");
      setSelectedTeams([]);
      void fetchSessions(); // Refresh sessions list
    } catch (error) {
      console.error("Error creating session:", error);
    }
  };

  const formatDate = (isoString: string) => {
    const date = new Date(isoString);
    return new Intl.DateTimeFormat("en-US", {
      month: "long",
      day: "numeric",
      year: "numeric",
    }).format(date);
  };

  const formatTime = (isoString: string) => {
    const date = new Date(isoString);
    return new Intl.DateTimeFormat("en-US", {
      hour: "numeric",
      minute: "numeric",
      hour12: true,
    }).format(date);
  };

  return (
    <LayoutContainer>
      {/* Sidebar */}
      <ESNavBar />

      {/* Main Content */}
      {/* TODO: overflow/scroll */}
      <main className="flex-1 flex flex-row gap-4 p-4 overflow-y-hidden">
        {/* Session List */}
        <Card className="max-w-md w-full min-w-[260px] flex flex-col max-h-[calc(100vh-32px)] h-fit">
          <CardHeader>
            <CardTitle className="text-xl font-bold">Sessions</CardTitle>
            <CardDescription>View and manage all sessions</CardDescription>
          </CardHeader>
          {/* Sessions*/}
          <div className="overflow-y-auto flex-1 pb-4">
            {sessions.length > 0 &&
              sessions.map((session) => (
                <Card key={session.id} className="m-4">
                  <CardHeader className="flex flex-row justify-between items-center">
                    <CardTitle>{session.name}</CardTitle>
                    <div className="flex flex-row gap-2">
                      <EditSessionWidget
                        session={session}
                        teams={teams}
                        onSave={(updatedSession, oldSession) => {
                          handleEditSession(updatedSession, oldSession);
                        }}
                      />
                      <Trash2
                        color="#FE7A7A"
                        className="cursor-pointer"
                        onClick={() =>
                          handleDeleteSession(session.id.toString())
                        }
                      />
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div>{formatDate(session.start_time)}</div>
                    <br />
                    <div>
                      <strong>Start: </strong>
                      {formatTime(session.start_time)}
                    </div>
                    <div>
                      <strong>End: </strong>
                      {formatTime(session.end_time)}
                    </div>
                  </CardContent>
                  <CardContent>
                    <CardTitle>Teams</CardTitle>
                    <div className="flex flex-row gap-2 pt-2">
                      {teams
                        .filter((team) => team.session_id === session.id)
                        .map((team) => (
                          <Badge
                            key={team.id}
                            variant="basic"
                            className="bg-blue-400 hover:bg-blue-500 transition-colors"
                          >
                            {team.name}
                          </Badge>
                        ))}
                      {!teams.some(
                        (team) => team.session_id === session.id
                      ) && (
                        <span className="text-gray-500 text-sm">
                          No assigned teams
                        </span>
                      )}
                    </div>
                  </CardContent>
                </Card>
              ))}
            {sessions.length === 0 && (
              <div className="text-gray-500 text-sm text-center">
                No sessions found
              </div>
            )}
          </div>
        </Card>

        {/* Create Session */}
        <Card className="max-w-lg w-full h-fit">
          <CardHeader>
            <CardTitle className="text-xl font-bold">Create Session</CardTitle>
            <Separator />
          </CardHeader>
          <CardContent className="flex flex-col gap-4">
            <CardTitle>Name</CardTitle>
            <Input
              placeholder="Session Name"
              value={sessionName}
              onChange={handleSessionNameChange}
            />
            <Separator />
          </CardContent>
          <CardContent className="flex flex-col gap-4">
            <CardTitle>Date & Time</CardTitle>
            <div className="flex flex-row gap-4 items-center">
              Date:{" "}
              <Input
                type="date"
                value={sessionDate}
                onChange={handleSessionDateChange}
              />
            </div>
            <div className="flex flex-row gap-4 items-center">
              Time:{" "}
              <Input
                type="time"
                value={startTime}
                onChange={handleStartTimeChange}
              />{" "}
              to{" "}
              <Input
                type="time"
                value={endTime}
                onChange={handleEndTimeChange}
              />
            </div>
            <Separator />
          </CardContent>
          <CardContent className="flex flex-col gap-4">
            <CardTitle>Team Selection</CardTitle>
            <div className="flex flex-row gap-2">
              {/* TODO: Ask if teams can be applied to more than one session */}
              {selectedTeams.length > 0 &&
                selectedTeams.map((team) => (
                  <Badge
                    key={team.id}
                    variant="basic"
                    className="bg-blue-400 items-center"
                  >
                    {team.name}
                    <X
                      size={16}
                      className="-mr-1 hover:text-[#FE7A7A] cursor-pointer transition-colors"
                      onClick={() => handleRemoveTeam(team.id)}
                    />
                  </Badge>
                ))}
              {selectedTeams.length === 0 && (
                <span className="text-gray-500 text-sm">No teams selected</span>
              )}
            </div>
            <div className="flex flex-row items-center">
              {/* TODO: Could be improved to be more efficient */}
              <Select
                onValueChange={(value) => setSelectedTeamId(Number(value))}
                value={selectedTeamId?.toString() || ""}
              >
                <SelectTrigger className="rounded-r-none">
                  <SelectValue placeholder="Select a Team" />
                </SelectTrigger>
                <SelectContent>
                  {teams.map((team) => (
                    <SelectItem key={team.id} value={team.id.toString()}>
                      {team.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <Button
                type="button"
                className="rounded-l-none -ml-px"
                onClick={() => {
                  if (selectedTeamId) {
                    handleAddTeam(selectedTeamId);
                  }
                }}
              >
                <Plus />
              </Button>
            </div>
            <Separator />
          </CardContent>
          <CardFooter>
            <Button
              onClick={() => {
                void handleSubmit();
              }}
            >
              CREATE
            </Button>
          </CardFooter>
        </Card>
      </main>
    </LayoutContainer>
  );
}
