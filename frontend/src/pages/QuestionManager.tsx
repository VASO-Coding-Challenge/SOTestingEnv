import { jwtDecode } from "jwt-decode";
import { styled } from "@mui/system";

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import ESNavBar from "../components/ESNavBar";
import StarsIcon from "@mui/icons-material/Stars";
import { QuestionsPublic, Question, Document } from "../models/questions";
//import LeftSideBarCopy from "../components/LeftSideBarCopy";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Editor } from "@monaco-editor/react"
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import { Button } from "@/components/ui/button";
import { Box, Typography, List, ListItem, Link as MuiLink } from "@mui/material";
import { Link } from "react-router-dom";




const LayoutContainer = styled("div")({
  display: "flex",
  height: "100vh",
  width: "100vw",
  overflow: "hidden",
});

export default function QuestionManager() {
  //get questions
  //add questions
  //remove questions
  //update questions
  const [questions, setQuestions] = useState<Question[] | null>();

  const [activeTab, setActiveTab] = useState("problem");
  
  const [selectedQuestion, setSelectedQuestion] = useState<Question | null>(
    null
  );
  const [code, setCode] = useState<string>(
        questions ? questions[0]?.prompt : ""
  );

  const [code1, setCode1] = useState<string>(
      questions ? questions[0]?.starter_code : ""
  );
  const [code2, setCode2] = useState<string>(
    questions ? questions[0]?.demo_cases : ""
  );
  const [code3, setCode3] = useState<string>(
    questions ? questions[0]?.test_cases : ""
  );
  
  const [globalDocs, setGlobalDocs] = useState<Document[]>([]);
  //const navigate = useNavigate()
  interface numberOfTabsProps {
    num: number;
    onTabClick: (index: number) => void;
  }
  
  
  
  const SidebarContainer = styled(Box)({
    display: "flex",
    width: "180px",
    maxWidth: "180px",
    padding: "0px 0px",
    borderRight: "1px solid #ccc",
    flexDirection: "column",
    height: "100vh",
  });
  
  const TabsContainer = styled(Box)({
    flexGrow: 1,
    display: "flex",
    flexDirection: "column",
  });
  
  const StyledTab = styled(Tab)({
    minHeight: "80px",
    fontSize: "1rem",
    fontWeight: "bold",
    textTransform: "none",
    color: "dark-gray",
    "&.Mui-selected": {
      color: "purple",
      boxShadow: "0px 4px 12px rgba(0, 0, 0, 0.2)",
    },
  });
  
  const LogoutContainer = styled(Box)({
    padding: "10px",
    marginTop: "15px",
    textAlign: "center",
  });
  

  const [value, setValue] = useState(0);
  const [startTime, setStartTime] = useState<Date | null>(null);
  const [endTime, setEndTime] = useState<Date | null>(null);
  const navigate = useNavigate();
  
    
  
  const handleChange = (_event: React.SyntheticEvent, newValue: number) => {
    console.log(newValue);
    setValue(newValue);
    onTabClick(newValue);
    handleQuestionClick(newValue);


  };
  const handleCreate = async ()  => {
    // create new question using /api/problems/create
    try {
      const response = await fetch('/api/problems/create/', {
        method: 'POST',
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({})
      });
      if (response.ok) {
        void getQuestions();
        navigate('/question-manager');
      } else {
        console.error('Failed to create new problem');
      }
    } catch (error) {
      console.error('An error occurred while creating a new problem:', error);
    }
  };
  
  
  

      

  

  const getQuestions = async() => {
    // get from API
    try {
      const response = await fetch("/api/problems/all", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      if (!response.ok) {
        console.error("Failed to fetch questions");
        return;
      }

      const data = (await response.json()) as Question[];
      setQuestions(data);
      console.log("Questions:", data);
      const question = data?.find((q) => q.num - 1 === 0) || null;
      console.log("Question 1: ", question)
      setSelectedQuestion(question);
    } catch (error) {
      console.error("Error fetching questions:", error);
    }
  };
  //setSelectedQuestion(questions[0]);
  const getUserRole = (token: string): boolean => {
    try {
      const decoded = jwtDecode<DecodedToken>(token); // Explicitly type the decoded token
      return decoded.is_admin;
    } catch (error) {
      console.error("Invalid token:", error);
      return false;
    }
  };

  useEffect(() => {
    const token = localStorage.getItem("token");
    //void getQuestions();
    

    if (!token) {
      console.error("No token found");
      navigate("/login"); // Fix: Ensure navigate is defined
      return;
    }

    console.log("Token found:", token);

    const isAdmin = getUserRole(token);

    if (!isAdmin) {
      console.error("User is not an admin");
      localStorage.removeItem("token");
      navigate("/login"); // Fix: Ensure navigate is defined
    }
    void getQuestions();
  }, [navigate]);

  const handleQuestionClick = (questionNum: number) => {
    const question = questions?.find((q) => q.num - 1 === questionNum) || null;
    setSelectedQuestion(question);
  };

  async function DeleteQuestions() {
    //add
    if (!selectedQuestion) {
      console.error("No question selected to update.");
      return;
    }
    try {
      const response = await fetch(`/api/problems/${selectedQuestion.num}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify(selectedQuestion),
      });

      if (!response.ok) {
        console.error("Failed to update question");
        return;
      }

      const updatedQuestion = await response.json();
      console.log("Question updated successfully:", updatedQuestion);

      // Update the local state with the updated question
      void getQuestions();
    } catch (error) {
      console.error("Error updating question:", error);
    }

  }

  async function UpdateQuestions() {
    if (!selectedQuestion) {
      console.error("No question selected to update.");
      return;
    }
    selectedQuestion.prompt = code;
    selectedQuestion.starter_code = code1; // Update the starter_code with the current code from the editor
    selectedQuestion.demo_cases = code2;
    selectedQuestion.test_cases = code3;

    try {
      const response = await fetch(`/api/problems/${selectedQuestion.num}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify(selectedQuestion),
      });

      if (!response.ok) {
        console.error("Failed to update question");
        return;
      }

      const updatedQuestion = await response.json();
      console.log("Question updated successfully:", updatedQuestion);

      // Update the local state with the updated question
      setQuestions((prevQuestions) =>
        prevQuestions?.map((q) =>
          q.num === updatedQuestion.num ? updatedQuestion : q
        ) || null
      );
    } catch (error) {
      console.error("Error updating question:", error);
    }
  }
  return (
    <LayoutContainer>
      <ESNavBar />
      <div className="flex">
        {/* Sidebar */}
        <div className="w-64 fixed h-full bg-white shadow-md">
        <SidebarContainer>
       
          <TabsContainer onTabClick={handleQuestionClick}>
            <Tabs
              value={value}
              onChange={handleChange}
              orientation="vertical"
              indicatorColor="secondary"
            >
              {Array.from({ length: questions ? questions.length : 0 }, (_, index) => (
                <StyledTab
                  key={index}
                  label={`Problem ${index + 1}`}
                  icon={<StarsIcon />}
                  iconPosition="top"
                />
              ))}
            </Tabs>
          </TabsContainer>
          
          <div>
          <Button className="w-full p-2 bg-green-500 text-white rounded-md hover:bg-blue-600 disabled:bg-gray-300" onClick={() => handleCreate()}>
            Create
          </Button>
          </div>
          
        </SidebarContainer>
        </div>
        {/* Main Content */}
        <div className="flex-1 ml-64 p-6 w-[1200px]">
          {/* Tabs Navigation */}
          <div className="flex border-b">
            {["problem", "starter", "autograder: Demo", "autograder: Test", "docs"].map((tab) => (
              <button
                key={tab}
                className={`w-1/4 py-2 font-bold ${activeTab === tab ? "border-b-4 border-red-500 text-red-500" : "text-gray-500"}`}
                onClick={() => setActiveTab(tab)}
              >
                {tab.charAt(0).toUpperCase() + tab.slice(1)}
              </button>
            ))}
          </div>

          {/* Tab Content */}
          <div className="p-6 bg-white shadow-md rounded-lg mt-4">
            {activeTab === "problem" && (
              <div>
                <Markdown className="markdown text-2xl font-bold" remarkPlugins={[remarkGfm]}>
                  {"## Problem " + selectedQuestion?.num}
                </Markdown>
                <p className="text-red-500 font-semibold mt-4">Prompt</p>
                <Editor className="h-72 w-full" value={selectedQuestion?.prompt} onChange={(value) => setCode(value || "")}/>
                <button className="mt-6 w-full bg-blue-500 text-white py-2 rounded-md shadow-md text-lg font-bold" onClick={UpdateQuestions}>
                  SAVE
                </button>
                <button className="mt-6 w-full bg-red-500 text-white py-2 rounded-md shadow-md text-lg font-bold" onClick={DeleteQuestions}>
                  Delete
                </button>
              </div>
            )}

            {activeTab === "starter" && (
              <div>
                <p className="text-red-500 font-semibold">Starter Code</p>
                <Editor className="h-72 w-full" value={selectedQuestion?.starter_code} onChange={(value) => setCode1(value || "")}/>
                <button className="mt-6 w-full bg-blue-500 text-white py-2 rounded-md shadow-md text-lg font-bold" onClick={UpdateQuestions}>
                  SAVE
                </button>
                <button className="mt-6 w-full bg-red-500 text-white py-2 rounded-md shadow-md text-lg font-bold" onClick={DeleteQuestions}>
                  Delete
                </button>
              </div>
            )}

            {activeTab === "autograder: Demo" && (
              <div>
                <p className="text-red-500 font-semibold">Demo Test Case(s)</p>
                <Editor className="h-64 w-full" value={selectedQuestion?.demo_cases} onChange={(value) => setCode2(value || "")} />
              <button className="mt-6 w-full bg-blue-500 text-white py-2 rounded-md shadow-md text-lg font-bold" onClick={UpdateQuestions}>
                  SAVE
              </button>
              <button className="mt-6 w-full bg-red-500 text-white py-2 rounded-md shadow-md text-lg font-bold" onClick={DeleteQuestions}>
                  Delete
                </button>
              </div>
            )}

            {activeTab === "autograder: Test" && (
              <div>
              <p className="text-red-500 font-semibold mt-4">Test Case(s)</p>
                <Editor className="h-64 w-full" value={selectedQuestion?.test_cases} onChange={(value) => setCode3(value || "")} />
                <button className="mt-6 w-full bg-blue-500 text-white py-2 rounded-md shadow-md text-lg font-bold" onClick={UpdateQuestions}>
                  SAVE
                </button>
                <button className="mt-6 w-full bg-red-500 text-white py-2 rounded-md shadow-md text-lg font-bold" onClick={DeleteQuestions}>
                  Delete
                </button>
              </div>
            )}

            {activeTab === "docs" && (
              <Box sx={{ flex: 1, display: "flex", flexDirection: "column", padding: 3 }}>
                <Typography variant="h6" sx={{ mb: 2, textAlign: "center" }}>
                  Global Documentation
                </Typography>
                <List sx={{ paddingLeft: "1rem", paddingRight: "1rem" }}>
                  <ListItem sx={{ padding: 0, marginBottom: "0.5rem", borderRadius: "4px", "&:hover": { backgroundColor: "rgba(0, 0, 0, 0.04)" } }}>
                    <MuiLink to="/python_docs/index.html" target="_blank" rel="noopener noreferrer" underline="none" sx={{ color: "#1976d2", fontSize: "1rem", fontWeight: 500, textAlign: "center", cursor: "pointer", "&:hover": { textDecoration: "underline", color: "secondary.main" } }} component={Link}>
                      Python 3 Documentation
                    </MuiLink>
                  </ListItem>
                </List>
              </Box>
            )}
          </div>
        </div>
      </div>
    </LayoutContainer>

  );
};

