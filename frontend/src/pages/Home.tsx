import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { CountdownTimer } from "../components/timer";

enum Display {
  LOADING,
  COUNTDOWN
}

interface Team {
  id: number;
  name: string;
  start_time: Date;
  end_time: Date;
}

const Home = () => {
  const [token, setToken] = useState<string>(localStorage.getItem("token") ?? "");
  const [display, setDisplay] = useState<Display>(Display.LOADING);
  const [team, setTeam] = useState<Team | null>(null);

  const nav = useNavigate();
  // Navigate to login page if there is no current login
  useEffect(() => {
    const validateToken = async (): Promise<void> => {
      if (token == "") {
        nav("/login");
      } else {
        // Run route to make sure the saved token is not expired, and collect current user
        const resp = await fetch("/api/team", {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        if (resp.status == 401) {
          const json = await resp.json() as {message: string};
          console.log(json.message);
          nav("/login");
        } else {
          const team = await resp.json() as Team;
          team.start_time = new Date(team.start_time)
          team.end_time = new Date(team.end_time)
          setTeam(team);
          setDisplay(Display.COUNTDOWN);
        }
      }
    };
    void validateToken();
  }, []);

  if (display == Display.LOADING) {
    return (
      <div>
        <p>Loading...</p>
      </div>
    )
  } else if (display == Display.COUNTDOWN) {
    return (
      <div>
        <h1>Time Until You Start:</h1>
        <CountdownTimer end_time={team!.start_time} />
      </div>
    )
  }

};

export default Home;
