import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { TokenJSON } from "../models/auth";
import ESNavBar from "../components/ESNavBar";

export default function TeamManager() {
  return (
    <>
      <ESNavBar />
      <p>Teams</p>
    </>
  );
}
