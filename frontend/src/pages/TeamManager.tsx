import { jwtDecode } from "jwt-decode";
import { styled } from "@mui/system";

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import ESNavBar from "../components/ESNavBar";
import GetTeamSubmissions from "../components/GetTeamSubmissions";
import { PencilLine, Trash2 } from "lucide-react";


const LayoutContainer = styled("div")({
  display: "flex",
  height: "100vh",
  width: "100vw",
  overflow: "hidden",
});
const Title = styled("h6")({
  textAlign: "left",
  margin: "20px",
  paddingLeft: "300 px",
  fontSize: "50px",
  display: "block", // Ensures it takes full width
  width: "80%",    // Forces it to occupy a full line
});
const TitleContainer = styled("div")({
  width: "100%",
  display: "flex",
  flexDirection: "column", // Ensures vertical stacking
  alignItems: "center", // Centers content
});

const Hr = styled("hr")({
  width: "80%", 
  margin: "10px auto", // Centers the line
  border: "none",
  borderTop: "2px solid #ccc",
  display: "block", // Ensures it takes up the full width
});

const TeamList = styled("div")({
  marginTop: "20px",
});



const Button = styled("button")({
  padding: "5px 10px",
  cursor: "pointer",
});

export default function TeamManager() {
  const navigate = useNavigate();
  const [teams, setTeams] = useState<any[]>([
    {
      id: 1,
      name: "Team Alpha",
      password: "alpha123",
      members: ["Alice", "Bob"],
    },
    {
      id: 2,
      name: "Team Beta",
      password: "beta123",
      members: ["Charlie", "Dave"],
    },
    {
      id: 3,
      name: "Team Gamma",
      password: "gamma123",
      members: ["Eve", "Frank"],
    },
  ]);

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
    //fetch in future
    

  }, [navigate]);

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
      <TitleContainer>
      <Title>Team Management</Title>
      <Hr />
    
      <TeamList>
      <div className="grid grid-cols-5 gap-0 mb-4 p-6 border border-gray-300 rounded-md">
        {/* Header Row */}
        <div className="font-bold bg-purple-600 pr-20 mb-4">Team Number</div>
        <div className="font-bold bg-purple-600 pr-20 mb-4">Name</div>
        <div className="font-bold bg-purple-600 pr-20 mb-4">Password</div>
        <div className="font-bold bg-purple-600 pr-20 mb-4">Members</div>
        <div className="font-bold bg-purple-600 pr-20 mb-4">Actions</div>

        {/* Team Rows */}
        {teams.map((team, index) => (
          <>
            <div className="mb-2">{index + 1}</div>
            <div className="mb-2">{team.name}</div>
            <div className="mb-2">{team.password}</div>
            <div className="mb-2">{team.members.join(", ")}</div>
            <div className="flex gap-2 mb-2">
              <Button size="sm"  variant="ghost" onClick={() => handleEdit(team.id)}>
                <PencilLine className="w-4 h-4" />
              </Button>
              <Button size="sm" variant="ghost" onClick={() => handleDelete(team.id)}>
                <Trash2 className="w-4 h-4" />
              </Button>
            </div>
          </>
        ))}
      </div>
      </TeamList>
      <div className="flex gap-10 m=10">
      <Button className="w-full p-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:bg-gray-300" onClick={() => handleCreate()}>
        Create
      </Button>
      <Button className="w-full p-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:bg-gray-300" onClick={() => handleDownload()}>
        Download Scores
      </Button>
      </div>
      <GetTeamSubmissions />
      </TitleContainer>

    </LayoutContainer>
  );
}
