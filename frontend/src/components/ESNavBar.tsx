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

const tabs = [
  { label: "Scheduling", path: "/scheduling" },
  { label: "Questions", path: "/questions-manager" },
  { label: "Teams", path: "/team-manager" },
];

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

export default function ESNavBar() {
  return (
    <SidebarContainer>
      <div>Image</div>

      <TabsContainer>
        <Tabs
          value={0}
          variant="fullWidth"
          orientation="vertical"
          indicatorColor="secondary"
        >
          {tabs.map((tab, index) => (
            <StyledTab
              key={index}
              label={tab.label}
              icon={<StarsIcon />}
              iconPosition="top"
            />
          ))}
        </Tabs>
      </TabsContainer>
      <LogoutContainer>
        <LogOut />
      </LogoutContainer>
    </SidebarContainer>
  );
}
