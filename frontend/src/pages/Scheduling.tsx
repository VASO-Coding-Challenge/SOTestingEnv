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
  const navigate = useNavigate();

  const getUserRole = (token: string): boolean => {
    try {
      const decoded = jwtDecode<DecodedToken>(token); // Explicitly type the decoded token
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
      navigate("/login"); // Fix: Ensure navigate is defined
      return;
    }

    console.log("Token found:", token);

    const isAdmin = getUserRole(token);

    if (!isAdmin) {
      console.error("User is not an admin");
      localStorage.removeItem("token");
      navigate("/login"); // Fix: Ensure navigate is defined
    }
  }, [navigate]);

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
          </CardHeader>
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
