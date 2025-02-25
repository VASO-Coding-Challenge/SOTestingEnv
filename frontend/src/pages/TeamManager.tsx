import { jwtDecode } from "jwt-decode";
import { styled } from "@mui/system";

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import ESNavBar from "../components/ESNavBar";

const LayoutContainer = styled("div")({
  display: "flex",
  height: "100vh",
  width: "100vw",
  overflow: "hidden",
});
const Title = styled("h6")({
  textAlign: "center",
  margin: "20px 0",
  fontSize: "50px",
  display: "block", // Ensures it takes full width
  width: "100%",    // Forces it to occupy a full line
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

const TeamItem = styled("div")({
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  padding: "10px",
  borderBottom: "1px solid #ccc",
});

const TeamInfo = styled("div")({
  display: "flex",
  flexDirection: "column",
});

const TeamActions = styled("div")({
  display: "flex",
  gap: "10px",
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

  return (
    <LayoutContainer>
      <ESNavBar />
      <TitleContainer>
      <Title>Team Management</Title>
      <Hr />
    
      <TeamList>
        {teams.map((team) => (
          <TeamItem key={team.id}>
            <TeamInfo>
              <p>Name: {team.name}</p>
              <p>Password: {team.password}</p>
              <p>Members: {team.members.join(", ")}</p>
            </TeamInfo>
            <TeamActions>
              <Button onClick={() => handleEdit(team.id)}>Edit</Button>
              <Button onClick={() => handleDelete(team.id)}>Delete</Button>
            </TeamActions>
          </TeamItem>
        ))}
      </TeamList>
      </TitleContainer>

    </LayoutContainer>
  );
}
