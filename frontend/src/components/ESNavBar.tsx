import * as React from "react";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import StarsIcon from "@mui/icons-material/Stars";
import { Box } from "@mui/material";
import { styled } from "@mui/system";
import { LogOut } from "./LogOutButton";
import { useLocation, useNavigate } from "react-router-dom";

const tabs = [
  { label: "Scheduling", path: "/scheduling" },
  { label: "Questions", path: "/question-manager" },
  { label: "Teams", path: "/team-manager" },
];

const SidebarContainer = styled(Box)({
  width: "180px",
  flexShrink: 0,
  padding: "0px",
  borderRight: "1px solid #ccc",
  display: "flex",
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
  const navigate = useNavigate();
  const location = useLocation();

  const currentTabIndex = tabs.findIndex(
    (tab) => tab.path === location.pathname
  );

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    navigate(tabs[newValue].path);
  };

  return (
    <SidebarContainer>
      <img src="/SO.png" alt="Image" />

      <TabsContainer>
        <Tabs
          value={currentTabIndex !== -1 ? currentTabIndex : 0}
          onChange={handleChange}
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
