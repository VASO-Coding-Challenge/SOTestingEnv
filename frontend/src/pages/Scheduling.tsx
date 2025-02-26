import { emphasize, styled } from "@mui/system";
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
import { PencilLine, Trash2, Plus } from "lucide-react";

import { jwtDecode } from "jwt-decode";

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import ESNavBar from "../components/ESNavBar";

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

export default function Scheduling() {
  const [sessions, setSessions] = useState(session_data);
  const [teams, setTeams] = useState(session_teams);

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
      <main className="flex-1 flex flex-row gap-4 m-4">
        {/* Session List */}
        <Card className="flex-1">
          <CardHeader>
            <CardTitle>Sessions</CardTitle>
            <CardDescription>View and manage all sessions</CardDescription>
          </CardHeader>
          {/* Sessions */}
          {sessions.map((session) => (
            <Card key={session.id} className="m-4">
              <CardHeader className="flex flex-row justify-between items-center">
                <CardTitle>{session.name}</CardTitle>
                <div className="flex flex-row gap-2">
                  <PencilLine />
                  <Trash2 color="#FE7A7A" />
                </div>
              </CardHeader>
              <CardContent>
                <div>{formatDate(session.start_time)}</div>
                <br />
                <div>Start: {formatTime(session.start_time)}</div>
                <div>End: {formatTime(session.end_time)}</div>
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
        <Card className="flex-1">
          <CardHeader>
            <CardTitle>Create Session</CardTitle>
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
