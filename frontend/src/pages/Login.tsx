import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const LoginPage = () => {
  const [number, setNumber] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  type resp = {
    access_token: string;
    token_type: string;
  };
  const navigate = useNavigate();

  const handleSubmit = (
    event: React.MouseEvent<HTMLButtonElement, MouseEvent>
  ) => {
    event.preventDefault();
    fetch("/api/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: number,
        password: password,
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP Error with Status Code : ${response.status}`);
        }
        return response.json();
      })
      .then((responseData: resp) => {
        console.log("Success :", responseData.access_token);
        sessionStorage.setItem("token", responseData.access_token);
        navigate("/Question");
      })
      .catch((error) => {
        console.error("Error :", error);
      });
  };

  return (
    <div className="flex flex-col items-center min-h-screen pt-12 bg-[#fef7ff] text-[#000000] font-sans">
      <div className="flex flex-col items-center justify-center text-[64px] font-extrabold">
        Virginia Science Olympiad
      </div>
      <br />
      <div className="flex flex-col items-center justify-center text-[30px] font-bold">
        Please Sign in
      </div>
      <div className="flex flex-col items-center pb-8 mt-6 rounded-[25px] bg-[#e8def8] w-full max-w-[600px]">
        <br />
        <div className="flex flex-col text-[25px]">
          Team Number
          <input
            value={number}
            placeholder="Team Number"
            onChange={(e) => setNumber(e.target.value)}
            className="h-[50px] w-96 max-w-[500px] text-lg rounded-[8px] border bg-white border-gray-300 pl-2 mt-2"
            required
          />
        </div>
        <br />
        <div className="flex flex-col text-[25px]">
          Password
          <input
            type="password"
            value={password}
            placeholder="Password"
            onChange={(e) => setPassword(e.target.value)}
            className="h-[50px] w-96 text-lg rounded-[8px] border bg-white border-gray-300 pl-2 mt-2"
            required
          />
        </div>
        <br />
        <button
          onClick={handleSubmit}
          className="mt-2 px-4 py-2 bg-gray-800 text-white font-bold rounded"
        >
          Submit
        </button>
      </div>
    </div>
  );
};

export default LoginPage;
