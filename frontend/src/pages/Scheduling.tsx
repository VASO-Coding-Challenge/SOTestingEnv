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
import { Trash2, Plus } from "lucide-react";

import { jwtDecode } from "jwt-decode";

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import ESNavBar from "../components/ESNavBar";
import EditSessionWidget from "@/components/EditSessionWidget";

// Fake Data for testing purposes
import { session_data, session_teams } from "../data/session";

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

export default function Scheduling() {
  const [sessions, setSessions] = useState(session_data);
  const [teams, setTeams] = useState(session_teams);
  const [unassignedTeams, setUnassignedTeams] = useState([]);
  const [selectedTeams, setSelectedTeams] = useState([]);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);

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
  }, [navigate]);

  const handleGetSessions = () => {
    // Fetch the session data
    console.log("Fetching session data");
  };

  const handleCreateSession = () => {
    // Create a new session
    console.log("Creating a new session");
  };

  const handleEditSession = () => {
    // Edit a session
    console.log("Editing a session");
  };

  const handleDeleteSession = () => {
    // Delete a session
    console.log("Deleting a session");
  };

  const handleGetTeamForSession = () => {
    // Fetch the team data for a session
    // TODO: Decide if this should be done in backend
    console.log("Fetching team data for a session");
  };

  const handleSubmit = () => {
    // Submit the created session data
    console.log("Submitting session data");
  };

  // May not be necessary depending on backend implementation
  const formatDate = (isoString: string) => {
    const date = new Date(isoString);
    return new Intl.DateTimeFormat("en-US", {
      month: "long",
      day: "numeric",
      year: "numeric",
    }).format(date);
  };

  // May not be necessary depending on backend implementation
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
      <main className="flex-1 flex flex-row gap-4 p-4 overflow-x-auto">
        {/* Session List */}
        <Card className="max-w-md w-full h-fit">
          <CardHeader>
            <CardTitle className="text-xl font-bold">Sessions</CardTitle>
            <CardDescription>View and manage all sessions</CardDescription>
          </CardHeader>
          {/* Sessions */}
          {sessions.map((session) => (
            <Card key={session.id} className="m-4">
              <CardHeader className="flex flex-row justify-between items-center">
                <CardTitle>{session.name}</CardTitle>
                <div className="flex flex-row gap-2">
                  <EditSessionWidget
                    session={session}
                    teams={teams}
                    onSave={(updatedSession) => {
                      handleEditSession(updatedSession);
                    }}
                  />
                  <Trash2 color="#FE7A7A" />
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
                  {teams.map((team) => (
                    <Badge
                      key={team.id}
                      variant="basic"
                      className="bg-blue-400"
                    >
                      {team.name}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </Card>

        {/* Create Session */}
        <Card className="max-w-lg w-full h-fit">
          <CardHeader>
            <CardTitle className="text-xl font-bold">Create Session</CardTitle>
            <Separator />
          </CardHeader>
          <CardContent className="flex flex-col gap-4">
            <CardTitle>Name</CardTitle>
            <Input placeholder="Session Name" />
            <Separator />
          </CardContent>
          <CardContent className="flex flex-col gap-4">
            <CardTitle>Date & Time</CardTitle>
            <div className="flex flex-row gap-4 items-center">
              Date: <Input type="date" />
            </div>
            <div className="flex flex-row gap-4 items-center">
              Time: <Input type="time" /> to <Input type="time" />
            </div>
            <Separator />
          </CardContent>
          <CardContent className="flex flex-col gap-4">
            <CardTitle>Team Selection</CardTitle>
            <div className="flex flex-row gap-2">
              {teams.map((team) => (
                <Badge key={team.id} variant="basic" className="bg-blue-400">
                  {team.name}
                </Badge>
              ))}
            </div>
            <div className="flex flex-row items-center">
              {/* TODO: Could be improved to be more efficient */}
              <Select>
                <SelectTrigger className="rounded-r-none">
                  <SelectValue placeholder="Select a Team" />
                </SelectTrigger>
                <SelectContent>
                  {teams.map((team) => (
                    <SelectItem key={team.id} value={team.name}>
                      {team.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <Button type="submit" className="rounded-l-none -ml-px">
                <Plus />
              </Button>
            </div>
            <Separator />
          </CardContent>
          <CardFooter>
            <Button>CREATE</Button>
          </CardFooter>
        </Card>
      </main>
    </LayoutContainer>
  );
}
