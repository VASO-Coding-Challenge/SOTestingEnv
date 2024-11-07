import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { TokenJSON } from "../models/auth";

const LoginPage = () => {
  const [number, setNumber] = useState<string>("");
  const [password, setPassword] = useState<string>("");

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
          return response.json().then((json: { message: string }) => {
            throw new Error(json.message);
          });
        }
        return response.json();
      })
      .then((responseData: TokenJSON) => {
        console.log("Success :", responseData.access_token);
        localStorage.setItem("token", responseData.access_token);
        navigate("/");
      })
      .catch((error: Error) => {
        console.error("Error :", error.message);
        login_error_handler(error.message);
        return <></>;
      });
  };

  const login_error_handler = (msg: string = "") => {
    setErrorDisplay(
      <div className="flex flex-col items-center justify-center rounded-[10px] mb-3 pl-3 pr-3 w-half border-2 border-red-900 bg-[rgba(255,112,121,0.65)]">
        <p className="text-[#0000008e] text-center">Error: {msg}</p>
      </div>
    );
    setTimeout(() => setErrorDisplay(<></>), 10000);
  };

  return (
    <div className="flex flex-col items-center min-h-screen pt-12 bg-[#fef7ff] text-[#000000] font-sans">
      <div className="flex flex-col items-center text-center justify-center text-[64px] font-extrabold">
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
        {errorDisplay}
        <button
          onClick={handleSubmit}
          className="mt-2 px-4 py-2 bg-gray-800 text-white font-bold rounded hover:bg-gray-400 active:bg-gray-950"
        >
          Submit
        </button>
      </div>
    </div>
  );
};

export default LoginPage;
