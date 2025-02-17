/* eslint-disable @typescript-eslint/no-unsafe-member-access */
/* eslint-disable @typescript-eslint/no-unsafe-argument */
/* eslint-disable @typescript-eslint/no-unsafe-assignment */
import * as React from "react";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import StarsIcon from "@mui/icons-material/Stars";
import { useEffect, useState } from "react";
import { Box } from "@mui/material";
import { styled } from "@mui/system";
import { LogOut } from "./LogOutButton";
import { CountdownTimer } from "./timer";
import { useNavigate } from "react-router-dom";

interface numberOfTabsProps {
  num: number;
  onTabClick: (index: number) => void;
}

const TimerContainer = styled(Box)({
  padding: "10px",
  textAlign: "center",
  fontSize: "18px",
});

const SidebarContainer = styled(Box)({
  display: "flex",
  width: "180px",
  maxWidth: "180px",
  padding: "0px 0px",
  borderRight: "1px solid #ccc",
  flexDirection: "column",
  height: "100vh",
});

const TabsContainer = styled(Box)({
  flexGrow: 1,
  display: "flex",
  flexDirection: "column",
});

const StyledTab = styled(Tab)({
  minHeight: "80px",
  fontSize: "1rem",
  fontWeight: "bold",
  textTransform: "none",
  color: "dark-gray",
  "&.Mui-selected": {
    color: "purple",
    boxShadow: "0px 4px 12px rgba(0, 0, 0, 0.2)",
  },
});

const LogoutContainer = styled(Box)({
  padding: "10px",
  marginTop: "15px",
  textAlign: "center",
});

export default function LeftSideBar({ num, onTabClick }: numberOfTabsProps) {
  const [value, setValue] = useState(0);
  const [startTime, setStartTime] = useState<Date | null>(null);
  const [endTime, setEndTime] = useState<Date | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch the team data
    const fetchTeam = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        return;
      }

      const resp = await fetch("/api/team", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (resp.ok) {
        const team = await resp.json();
        setStartTime(new Date(team.session.start_time));
        setEndTime(new Date(team.session.end_time));
      } else {
        console.error("Failed to fetch team data");
      }
    };

    void fetchTeam();
  }, []);

  const handleChange = (_event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
    onTabClick(newValue);
  };

  const handleTimerEnd = () => {
    navigate("/thank-you");
  };

  return (
    <SidebarContainer>
      <TimerContainer>
        {startTime && endTime ? (
          <CountdownTimer end_time={endTime} end_fn={handleTimerEnd} />
        ) : (
          <p>Loading Timer...</p>
        )}
      </TimerContainer>
      <TabsContainer>
        <Tabs
          value={value}
          onChange={handleChange}
          orientation="vertical"
          indicatorColor="secondary"
        >
          {Array.from({ length: num }, (_, index) => (
            <StyledTab
              key={index}
              label={`Problem ${index + 1}`}
              icon={<StarsIcon />}
              iconPosition="top"
            />
          ))}
        </Tabs>
      </TabsContainer>
      {/* Logout Button */}
      <LogoutContainer>
        <LogOut />
      </LogoutContainer>
    </SidebarContainer>
  );
}
