"use client";
import React, { useState } from "react";
// import axios from "axios";
const LoginPage = () => {
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  async function handleSubmit(e: React.ChangeEvent<any>) {
    e.preventDefault();
    try {
      await axios.post("http://localhost:", {
        email: email,
        password: password,
        loginTime: String(new Date().getHours),
      });
    } catch (e) {
      alert(e);
    }
  }
  return (
    <div
      className="flex flex-col items-center min-h-screen pt-12 bg-[#fef7ff] text-[#000000] font-
sans"
    >
      <div className="flex flex-col items-center justify-center text-[64px] font-extrabold">
        Virginia Science Olympiad
      </div>
      <br />
      <div className="flex flex-col items-center justify-center text-[30px] font-bold">
        Please Sign in
      </div>
      <div
        className="flex flex-col items-center pb-8 mt-6 rounded-[25px] bg-[#e8def8] w-full
max-w-[600px]"
      >
        <br />
        <div className="flex flex-col text-[25px]">
          Team Number
          <form action="POST">
            <input
              value={email}
              placeholder="Team Number"
              onChange={(e) => setEmail(e.target.value)}
              className="h-[50px] w-96 max-w-[500px] text-lg rounded-[8px] border border-gray-
300 pl-2 mt-2"
              required
            />
          </form>
        </div>
        <br />
        <div className="flex flex-col text-[25px]">
          Password
          <form action="POST">
            <input
              type="password"
              value={password}
              placeholder="Password"
              onChange={(e) => setPassword(e.target.value)}
              className="h-[50px] w-96 text-lg rounded-[8px] border border-gray-300 pl-2 mt-2"
              required
            />
          </form>
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
