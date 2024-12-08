import { useNavigate } from "react-router-dom";
import { Button } from "@mui/material";

export const LogOut = () => {
  const nav = useNavigate();

  const handle_log_out = () => {
    localStorage.removeItem("token");
    nav("/login");
  };

  return (
    <Button
      onClick={handle_log_out}
      variant="contained"
      color="warning"
    >
      Log Out
    </Button>
  );
};
