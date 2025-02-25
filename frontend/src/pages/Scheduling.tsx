import { styled } from "@mui/system";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
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

  return (
    <LayoutContainer>
      {/* Sidebar */}
      <ESNavBar />

      {/* Main Content */}
      <main className="flex-1 flex flex-row gap-4 m-4">
        {/* Session List */}
        <Card className="flex-1">
          <CardHeader>
            <CardTitle>Sessions</CardTitle>
            <CardDescription>View and manage all sessions</CardDescription>
          </CardHeader>
          {/* Sessions */}
          {sessions.map((session) => (
            <Card key={session.id}>
              <CardHeader>
                <CardTitle>{session.name}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  {session.start_time} - {session.end_time}
                </CardDescription>
                <CardFooter>
                  <button>View Teams</button>
                </CardFooter>
              </CardContent>
            </Card>
          ))}
        </Card>

        {/* Create Session */}
        <Card className="flex-1">
          <CardHeader>
            <CardTitle>Create Session</CardTitle>
          </CardHeader>
        </Card>
      </main>
    </LayoutContainer>
  );
}
