import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";

import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Question from "./pages/Question";
import MarkdownViewer from "./components/MarkdownViewer";
import ThankYouPage from "./pages/ThankYouPage";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/question" element={<Question />} />
        <Route path="/thank-you" element={<ThankYouPage />} />
        {/** The route below is where we view the markdown. */}
        <Route path="/markdown-viewer/:docTitle" element={<MarkdownViewer />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>
);
