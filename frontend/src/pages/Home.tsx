import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { CountdownTimer } from "../components/timer";

enum Display {
  LOADING,
  COUNTDOWN,
  STARTED
}

interface Team {
  id: number;
  name: string;
  start_time: Date;
  end_time: Date;
}

const Home = () => {
  const [token] = useState<string>(localStorage.getItem("token") ?? "");
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
  }, [nav, token]);

  // Holds the JSX of either the timer or the continue button
  let timer_or_continue: JSX.Element = (
    <>
      <h1 className="text-[32px]">Your Competition Starts In:</h1>
      <div className="font-sans text-[64px] font-bold pb-10">
        <CountdownTimer end_time={team!.start_time} end_fn={null} /> {/* TODO: Add end functionality to display Start Test button */}
      </div>
    </>
  )

  // TODO: Finish this button display
  if (display == Display.STARTED) {
    timer_or_continue = (
      <>
        <h1 className="text-[32px]">Your Competition has Started:</h1>
        <Link to={'/question'}><button className="pb-10"></button></Link>
      </>
    )
  }

  if (display == Display.LOADING) {
    return (
      <div className="flex flex-col items-center min-h-screen pt-12 bg-[#fef7ff] text-[#000000] font-sans">
        <p>Loading...</p>
      </div>
    )
  } else {
    return (
      <div className="flex flex-col items-center min-h-screen p-12 bg-[#fef7ff] text-[#000000] font-sans">
        <h1 className="text-[64px] text-center pb-10 font-bold">Welcome Team {team!.name} to the Computer Science Competition!</h1>
        {timer_or_continue}
        <h2 className="text-[30px] font-bold">Please tell us your team member&apos;s names:</h2>
        <div className="pb-8 mt-6 rounded-[25px] bg-[#e8def8] w-full max-w-[600px]">

        </div>
      </div>
    )
  }

};

export default Home;
