import { jwtDecode } from "jwt-decode";
import { styled } from "@mui/system";

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import ESNavBar from "../components/ESNavBar";
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
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

import { PencilLine, Trashs, Download, Plus } from "lucide-react";


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
    fetchTeams();
  }, [navigate]);

  const fetchTeams = async() => {
    try {
      const response = await fetch("/api/teams", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        }
      });

      if (!response.ok) {
        console.error("Failed to fetch teams");
        return;
      }

      const data = await response.json();
      setTeams(data);
      console.log("Teams:", data);
    } catch (error) {
      console.error("Error fetching teams:", error);
    }
  }

  const handleEdit = (teamId: number) => {
    // Handle edit team
    console.log("Edit team:", teamId);
  };

  const handleDelete = (teamId: number) => {
    // Handle delete team
    console.log("Delete team:", teamId);
  };
  const handleCreate = () => {
    // Handle delete team
    console.log("Create team:");
  };
  const handleDownload = () => {
    // Handle delete team
    console.log("Create team:");
  };


  return (
    <LayoutContainer>
      <ESNavBar />
      
      {/* Main Content */}
      <main className="flex-1 flex flex-col gap-4 p-4 overflow-y-hidden">
        {/* Team Management Card */}
        <Card className="w-full flex flex-col">
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
                  <TableHead>Password</TableHead>
                  <TableHead>Members</TableHead>
                  <TableHead>Score</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {teams.map((team) => (
                  <TableRow key={team.id}>
                    <TableCell className="font-medium">{team.name}</TableCell>
                    <TableCell>{team.password}</TableCell>
                    <TableCell>{team.members.join(", ")}</TableCell>
                    <TableCell>{team.score}</TableCell>
                    <TableCell className="flex gap-2 justify-end">
                      <Button 
                        size="icon" 
                        variant="ghost"
                        onClick={() => handleEdit(team.id)}
                      >
                        <Pencil className="w-4 h-4" />
                      </Button>
                      <Button
                        size="icon"
                        variant="ghost"
                        onClick={() => handleDelete(team.id)}
                      >
                        <Trash className="w-4 h-4 text-[#FE7A7A] hover:text-[#ffcfcf]" />
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
          
          <CardFooter className="flex justify-between pt-4">
            <Button onClick={handleCreate}>
              <Plus className="w-4 h-4 mr-2" />
              Create Team
            </Button>
            <Button variant="secondary" onClick={handleDownload}>
              <Download className="w-4 h-4 mr-2" />
              Download Scores
            </Button>
          </CardFooter>
        </Card>

        {/* Submissions Card */}
        <Card className="w-fit min-w-[300px] flex flex-col">
          <CardHeader>
            <CardTitle className="text-xl font-bold">Submissions</CardTitle>
            <CardDescription>Team submission history</CardDescription>
            <Separator />
          </CardHeader>
          <CardContent className="flex-1 overflow-y-auto">
          </CardContent>
        </Card>
      </main>
    </LayoutContainer>
  );
}
