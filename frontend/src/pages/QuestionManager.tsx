import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { TokenJSON } from "../models/auth";
import ESNavBar from "../components/ESNavBar";

export default function QuestionManager() {
  return (
    <>
      <ESNavBar />
      <p>Questions</p>
    </>
  );
}
