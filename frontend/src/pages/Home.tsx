// Author: Andrew Lockard
import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { CountdownTimer } from "../components/timer";
import { MemberInput } from "../components/member_input";
import { LogOut } from "../components/LogOutButton";

enum Display {
  LOADING,
  COUNTDOWN,
  STARTED,
  ENDED,
}

interface Team {
  id: number;
  name: string;
  session: Session;
}

interface Session {
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
            Authorization: `Bearer ${token}`,
          },
        });
        if (resp.status == 401) {
          const json = (await resp.json()) as { message: string };
          console.log(json.message);
          nav("/login");
        } else {
          const team = (await resp.json()) as Team;
          // Convert session times to Date objects
          team.session.start_time = new Date(team.session.start_time);
          team.session.end_time = new Date(team.session.end_time);
          setTeam(team);
          if (team.session.start_time.getTime() > Date.now()) {
            setDisplay(Display.COUNTDOWN);
          } else if (team.session.end_time.getTime() > Date.now()) {
            setDisplay(Display.STARTED);
          } else {
            setDisplay(Display.ENDED);
          }
        }
      }
    };
    void validateToken();
  }, [nav, token]);

  const timer_end = () => {
    setDisplay(Display.STARTED);
  };

  if (display == Display.LOADING) {
    return (
      <div className="flex flex-col items-center min-h-screen pt-12 bg-[#fef7ff] text-[#000000] font-sans">
        <p>Loading...</p>
      </div>
    );
  } else {
    // Holds the JSX of either the timer or the continue button
    let timer_or_continue: JSX.Element = (
      <>
        <h1 className="text-[32px]">Your Competition Starts In:</h1>
        <div className="font-sans text-[64px] font-bold pb-10">
          <CountdownTimer
            end_time={team!.session.start_time}
            end_fn={timer_end}
          />{" "}
        </div>
      </>
    );

    // TODO: Finish this button display
    if (display == Display.STARTED) {
      timer_or_continue = (
        <>
          <h1 className="text-[32px]">Your Competition is active:</h1>
          <Link to={"/question"}>
            <button className="my-10 px-4 py-2 bg-gray-800 text-white font-bold rounded-lg text-[28px] hover:bg-gray-400 active:bg-gray-950">
              Start
            </button>
          </Link>
        </>
      );
    } else if (display == Display.ENDED) {
      timer_or_continue = (
        <>
          <h1 className="text-[32px]">Your Competition has Ended.</h1>
          <LogOut />
        </>
      );
    }
    return (
      <div className="flex flex-col items-center min-h-screen p-12 bg-[#fef7ff] text-[#000000] font-sans">
        <h1 className="text-[48px] text-center pb-10 font-bold">
          Welcome Team {team!.name} to the Computer Science Competition!
        </h1>
        {timer_or_continue}
        <div className="flex flex-col items-center pb-8 mt-5 rounded-[25px] bg-[#e8def8] w-full max-w-[600px]">
          <MemberInput token={token} />
        </div>
      </div>
    );
  }
};

export default Home;
