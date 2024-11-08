import * as React from "react";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import StarsIcon from "@mui/icons-material/Stars";
import { Box } from "@mui/material";
import { styled } from "@mui/system";

interface numberOfTabsProps {
  num: number;
  onTabClick: (index: number) => void;
}

const SidebarContainer = styled(Box)({
  width: "180px",
  maxWidth: "180px",
  padding: "50px 0px",
  borderRight: "1px solid #ccc",
  height: "100vh",
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

export default function LeftSideBar({ num, onTabClick }: numberOfTabsProps) {
  const [value, setValue] = React.useState(0);

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
    onTabClick(newValue);
  };

  return (
    <SidebarContainer>
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
    </SidebarContainer>
  );
}
