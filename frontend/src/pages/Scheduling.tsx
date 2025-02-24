import { styled } from "@mui/system";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import { useState, useEffect } from "react";
import ESNavBar from "../components/ESNavBar";

const LayoutContainer = styled("div")({
  display: "flex",
  height: "100vh",
  width: "100vw",
  overflow: "hidden",
});

export default function Scheduling() {
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
