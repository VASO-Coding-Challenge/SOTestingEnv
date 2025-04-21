import { jwtDecode } from "jwt-decode";
import { styled } from "@mui/system";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import ESNavBar from "../components/ESNavBar";
import StarsIcon from "@mui/icons-material/Stars";
import { QuestionsPublic, Question, Document } from "../models/questions";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Editor } from "@monaco-editor/react";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import { Button } from "@/components/ui/button";
import {
  Box,
  IconButton,
  TextField,
  Typography,
  List,
  ListItem,
  Link as MuiLink,
} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";

const LayoutContainer = styled("div")({
  display: "flex",
  height: "100vh",
  width: "100vw",
  overflow: "hidden",
});

// A reusable component for the Editor panel in prompt, starter, and both autograder tabs.
function EditorPanel({
  headerTitle,
  panelLabel,
  editorValue,
  onEditorChange,
  onSave,
  onDelete,
}) {
  return (
    <div className="flex flex-col h-full">
      <CardHeader>
        <CardTitle className="text-4xl">{headerTitle}</CardTitle>
        <Separator />
      </CardHeader>
      <CardContent className="flex-grow min-h-0 overflow-y-auto flex flex-col">
        <h3 className="text-red-500 font-semibold">{panelLabel}</h3>
        <Card className="px-4 flex flex-col flex-grow">
          <Editor
            className="flex-grow"
            value={editorValue}
            defaultLanguage="python"
            theme="vs-light"
            options={{
              fontSize: 14,
              minimap: { enabled: false },
              scrollBeyondLastLine: false,
            }}
            onChange={onEditorChange}
          />
        </Card>
      </CardContent>
      <CardFooter className="flex flex-row gap-4">
        <Button variant="create" onClick={onSave} className="w-60">
          SAVE
        </Button>
        <Button
          variant="destructive"
          onClick={onDelete}
          className="w-60 text-lg font-bold"
        >
          Delete
        </Button>
      </CardFooter>
    </div>
  );
}

export default function QuestionManager() {
  const [questions, setQuestions] = useState<Question[] | null>();
  // The name of the active tab now matches the keys in the configuration below.
  const [activeTab, setActiveTab] = useState("prompt");

  const [selectedQuestion, setSelectedQuestion] = useState<Question | null>(
    null
  );
  // Code states for the different editor tabs:
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

  const SidebarContainer = styled(Box)({
    display: "flex",
    width: "180px",
    maxWidth: "180px",
    padding: "0px 0px",
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

  const [value, setValue] = useState(0);
  const navigate = useNavigate();
  const [selectedFile, setSelectedFile] = useState(null);

  const handleChange = (_event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
    handleQuestionClick(newValue);
    setHeaderTitle("");
  };

  const [docs, setDocs] = useState([]);
  const [newDocName, setNewDocName] = useState("");
  const [newDocUrl, setNewDocUrl] = useState("");

  const [headerTitle, setHeaderTitle] = useState("");

  const addDoc = () => {
    if (newDocName && newDocUrl) {
      fetch("/docs/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: newDocName, content: newDocUrl }),
      })
        .then((response) => response.json())
        .then((newDoc) => setDocs([...docs, newDoc]))
        .catch((error) => console.error("Error adding document:", error));
      setNewDocName("");
      setNewDocUrl("");
    }
  };

  const removeDoc = (title) => {
    fetch(`/docs/${title}`, { method: "DELETE" })
      .then(() => setDocs(docs.filter((doc) => doc.title !== title)))
      .catch((error) => console.error("Error deleting document:", error));
  };

  const handleCreate = async () => {
    try {
      const response = await fetch("/api/problems/create/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({}),
      });
      if (response.ok) {
        await getQuestions(questions.length + 1);
      } else {
        console.error("Failed to create new problem");
      }
    } catch (error) {
      console.error("An error occurred while creating a new problem:", error);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;
    const formData = new FormData();
    formData.append("file", selectedFile);
    if (newDocName) formData.append("title", newDocName);
    try {
      const response = await fetch("/docs/upload", {
        method: "POST",
        body: formData,
      });
      if (!response.ok) throw new Error("Upload failed");
      const uploadedDoc = await response.json();
      setDocs((prev) => [...prev, uploadedDoc]);
      setSelectedFile(null);
      setNewDocName("");
    } catch (err) {
      console.error("Error uploading file:", err);
      alert("Upload failed. Check console for details.");
    }
  };

  const getQuestions = async (index) => {
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
      const question = data?.find((q) => q.num === index) || null;
      setSelectedQuestion(question);
      setValue(index - 1);
    } catch (error) {
      console.error("Error fetching questions:", error);
    }
  };

  const getUserRole = (token: string): boolean => {
    try {
      const decoded = jwtDecode(token);
      return decoded.is_admin;
    } catch (error) {
      console.error("Invalid token:", error);
      return false;
    }
  };

  const openDocInNewTab = (doc: { content: string; title: string }) => {
    sessionStorage.setItem("docContent", doc.content);
    sessionStorage.setItem("docTitle", doc.title);
    const fullUrl = `${window.location.origin}/markdown-viewer/${doc.title}`;
    window.open(fullUrl, "_blank");
  };

  useEffect(() => {
    const token = localStorage.getItem("token");
    fetch("/docs/")
      .then((response) => response.json())
      .then((data) => setDocs(data))
      .catch((error) => console.error("Error fetching documents:", error));

    if (!token) {
      console.error("No token found");
      navigate("/login");
      return;
    }
    const isAdmin = getUserRole(token);
    if (!isAdmin) {
      console.error("User is not an admin");
      localStorage.removeItem("token");
      navigate("/login");
    }
    void getQuestions(1);
  }, [navigate]);

  const handleQuestionClick = (questionNum: number) => {
    const question = questions?.find((q) => q.num - 1 === questionNum) || null;
    setSelectedQuestion(question);
  };

  async function DeleteQuestions() {
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
      await response.json();
      void getQuestions(1);
    } catch (error) {
      console.error("Error updating question:", error);
    }
  }

  useEffect(() => {
    if (selectedQuestion) {
      setCode(selectedQuestion.prompt);
      setCode1(selectedQuestion.starter_code);
      setCode2(selectedQuestion.demo_cases);
      setCode3(selectedQuestion.test_cases);
    }
  }, [navigate]);

  async function UpdateQuestions() {
    if (!selectedQuestion) {
      console.error("No question selected to update.");
      return;
    }
    // Update the selected question's values based on which tab edited its content
    selectedQuestion.prompt = code;
    selectedQuestion.starter_code = code1;
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
      setQuestions(
        (prevQuestions) =>
          prevQuestions?.map((q) =>
            q.num === updatedQuestion.num ? updatedQuestion : q
          ) || null
      );
    } catch (error) {
      console.error("Error updating question:", error);
    }
  }

  // Mapping configuration for the four tabs that use the EditorPanel layout.
  const tabConfig = {
    prompt: {
      label: "Prompt",
      value: selectedQuestion?.prompt ?? "",
      setValue: setCode,
    },
    starter: {
      label: "Starter Code",
      value: selectedQuestion?.starter_code ?? "",
      setValue: setCode1,
    },
    "autograder: Demo": {
      label: "Demo Test Case(s)",
      value: selectedQuestion?.demo_cases ?? "",
      setValue: setCode2,
    },
    "autograder: Test": {
      label: "Test Case(s)",
      value: selectedQuestion?.test_cases ?? "",
      setValue: setCode3,
    },
  };

  return (
    <LayoutContainer>
      <ESNavBar />
      <main className="flex-1 flex flex-row overflow-y-hidden">
        {/* Sidebar */}
        <div className="flex flex-col h-full bg-white shadow-md border-r border-[#ccc]">
          <div className="flex-1 overflow-hidden">
            <div className="h-full overflow-y-auto">
              <SidebarContainer className="flex flex-col">
                <TabsContainer>
                  <Tabs
                    value={value}
                    onChange={handleChange}
                    orientation="vertical"
                    indicatorColor="secondary"
                  >
                    {Array.from(
                      { length: questions ? questions.length : 0 },
                      (_, index) => (
                        <StyledTab
                          key={index}
                          label={`Problem ${index + 1}`}
                          icon={<StarsIcon />}
                          iconPosition="top"
                        />
                      )
                    )}
                  </Tabs>
                </TabsContainer>
              </SidebarContainer>
            </div>
          </div>
          <Button
            onClick={() => void handleCreate()}
            variant="create"
            className="w-[calc(100%-1rem)] m-2"
          >
            Create
          </Button>
        </div>
        {/* Main Content */}
        <div className="flex flex-1 flex-col p-6">
          {/* Tabs Navigation */}
          <div className="flex border-b">
            {[
              "prompt",
              "starter",
              "autograder: Demo",
              "autograder: Test",
              "docs",
            ].map((tab) => (
              <button
                key={tab}
                className={`w-1/4 py-2 font-bold ${activeTab === tab
                  ? "border-b-4 border-red-500 text-red-500"
                  : "text-gray-500"
                  }`}
                onClick={() => { setActiveTab(tab); setHeaderTitle(""); }}
              >
                {tab.charAt(0).toUpperCase() + tab.slice(1)}
              </button>
            ))}
          </div>
          <Card className="mt-4 h-full">
            {/* Render EditorPanel for the four tabs that use cards */}
            {activeTab in tabConfig ? (
              <EditorPanel
                headerTitle={"Problem " + selectedQuestion?.num}
                panelLabel={tabConfig[activeTab].label + headerTitle}
                editorValue={tabConfig[activeTab].value}
                onEditorChange={(value) => {
                  tabConfig[activeTab].setValue(value || "");
                  setHeaderTitle("*");
                }}
                onSave={() => {

                  UpdateQuestions();
                  setHeaderTitle("");
                }
                }

                onDelete={DeleteQuestions}
              />
            ) : activeTab === "docs" ? (
              // The docs tab remains unchanged.
              <Box
                sx={{
                  flex: 1,
                  display: "flex",
                  flexDirection: "column",
                  padding: 3,
                }}
              >
                <Typography variant="h6" sx={{ mb: 2, textAlign: "center" }}>
                  Global Documentation
                </Typography>
                <List sx={{ paddingLeft: "1rem", paddingRight: "1rem" }}>
                  {docs.map((doc) => (
                    <ListItem
                      key={doc.title}
                      sx={{
                        padding: 0,
                        marginBottom: "0.5rem",
                        borderRadius: "4px",
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center",
                        "&:hover": { backgroundColor: "rgba(0, 0, 0, 0.04)" },
                      }}
                    >
                      {/*<h1>Title: {doc.title}</h1>*/}
                      <MuiLink
                        underline="none"
                        sx={{
                          display: "flex",
                          alignItems: "center",
                          justifyContent: "center",
                          width: "100%",
                          height: "100%",
                          color: "primary.main",
                          fontSize: "1rem",
                          fontWeight: 500,
                          textAlign: "center",
                          cursor: "pointer",
                          "&:hover": {
                            textDecoration: "underline",
                            color: "secondary.main",
                          },
                        }}
                        onClick={() => openDocInNewTab(doc)} >{doc.title}</MuiLink>

                      <IconButton onClick={() => removeDoc(doc.title)}>
                        <DeleteIcon color="error" />
                      </IconButton>
                    </ListItem>
                  ))}
                </List>
                <Box sx={{ display: "flex", gap: 1, mt: 2 }}>
                  <TextField
                    label="Document Name"
                    variant="outlined"
                    size="small"
                    value={newDocName}
                    onChange={(e) => setNewDocName(e.target.value)}
                  />
                  <input
                    type="file"
                    onChange={(e) => setSelectedFile(e.target.files[0])}
                    accept=".txt,.md"
                    style={{ flexGrow: 1 }}
                  />
                  <Button onClick={handleUpload} disabled={!selectedFile}>
                    Upload
                  </Button>
                </Box>
              </Box>
            ) : null}
          </Card>
        </div>
      </main>
    </LayoutContainer>
  );
}
