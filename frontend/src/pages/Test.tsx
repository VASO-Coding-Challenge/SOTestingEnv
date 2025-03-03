import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

interface Document {
  title: string;
  content: string;
}

interface Problem {
  num: number;
  prompt: string;
  starter_code: string;
  test_cases: string;
  demo_cases: string;
  docs: Document[];
}

interface ProblemCreateResponse {
  message: string;
  problem_number?: number;
}

const Test: React.FC = () => {
  const [problems, setProblems] = useState<number[]>([]);
  const [selectedProblem, setSelectedProblem] = useState<Problem | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [debugInfo, setDebugInfo] = useState<string[]>([]);
  const navigate = useNavigate();

  // Fetch all problems on component mount
  useEffect(() => {
    void fetchProblems();
  }, []);

  // Debug logger function
  const addDebugInfo = (message: string) => {
    console.log(`DEBUG: ${message}`);
    setDebugInfo(prev => [...prev, `${new Date().toISOString()} - ${message}`]);
  };

  const fetchProblems = async (): Promise<void> => {
    try {
      setLoading(true);
      setError(null);
      addDebugInfo('Fetching problems started');
      
      try {
        // Try to fetch problems from API
        const response = await fetch('/api/problems/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP Error with Status Code: ${response.status}`);
        }

        const data = await response.json() as number[];
        setProblems(data);
        addDebugInfo(`Fetched ${data.length} problems successfully`);
      } catch (apiErr) {
        // Handle API error, but continue with local fallback
        const errorMsg = apiErr instanceof Error ? apiErr.message : String(apiErr);
        addDebugInfo(`API error: ${errorMsg}, falling back to local storage`);
        
        // Get existing problems from localStorage
        try {
          // Get all localStorage keys and filter for problem keys
          const allKeys = Object.keys(localStorage);
          const problemKeys = allKeys.filter(key => key.startsWith('problem_'));
          
          // Extract problem numbers
          const existingProblems = problemKeys.map(key => {
            return parseInt(key.replace('problem_', ''));
          }).sort((a, b) => a - b);
          
          if (existingProblems.length > 0) {
            setProblems(existingProblems);
            addDebugInfo(`Loaded ${existingProblems.length} existing problems from local storage`);
          } else {
            addDebugInfo('No problems found in local storage');
            setProblems([]);
          }
        } catch (localErr) {
          addDebugInfo(`LocalStorage error: ${String(localErr)}`);
          setProblems([]);
        }
      }
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : String(err);
      addDebugInfo(`Error in fetchProblems: ${errorMsg}`);
      setError('Failed to load problems. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const fetchProblemDetails = async (problemNum: number): Promise<void> => {
    try {
      setLoading(true);
      setError(null);
      addDebugInfo(`Fetching details for problem ${problemNum}`);
      
      try {
        // Try to fetch from API
        const response = await fetch(`/api/problems/${problemNum}/`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP Error with Status Code: ${response.status}`);
        }

        const data = await response.json() as Problem;
        setSelectedProblem(data);
        addDebugInfo(`Fetched details for problem ${problemNum} successfully`);
        
        // Save to localStorage for backup
        localStorage.setItem(`problem_${problemNum}`, JSON.stringify(data));
      } catch (apiErr) {
        // Try localStorage backup
        const errorMsg = apiErr instanceof Error ? apiErr.message : String(apiErr);
        addDebugInfo(`API error: ${errorMsg}, trying localStorage backup`);
        
        const storedProblem = localStorage.getItem(`problem_${problemNum}`);
        if (storedProblem) {
          try {
            const parsedProblem = JSON.parse(storedProblem) as Problem;
            setSelectedProblem(parsedProblem);
            addDebugInfo(`Loaded problem ${problemNum} from localStorage`);
            return;
          } catch (parseErr) {
            addDebugInfo(`Error parsing stored problem: ${String(parseErr)}`);
          }
        }
        
        // Fallback to default problem template with custom initial content
        const defaultProblem: Problem = createDefaultProblem(problemNum);
        
        setSelectedProblem(defaultProblem);
        addDebugInfo(`Created default template for problem ${problemNum}`);
        
        // Save default template to localStorage
        localStorage.setItem(`problem_${problemNum}`, JSON.stringify(defaultProblem));
      }
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : String(err);
      addDebugInfo(`Error in fetchProblemDetails: ${errorMsg}`);
      setError(`Failed to load problem ${problemNum}. Please try again.`);
    } finally {
      setLoading(false);
    }
  };

  // Helper function to create a default problem with specified templates
  const createDefaultProblem = (problemNum: number): Problem => {
    return {
      num: problemNum,
      prompt: "",
      starter_code: `def function_name(input_data: str) -> str:
    # TODO: Implement your solution here
    return None`,
      test_cases: `"""Test cases for problem ${problemNum}"""

import unittest
from decorators import weight

class Test(unittest.TestCase):
    @weight(1)
    def test_insert_name(self):
        self.assertEqual(temp("Hello World"), "Hello")`,
      demo_cases: `import unittest

class Test(unittest.TestCase):
    def test_insert_name(self):
        self.assertEqual(temp("Hello World"), "el ol")`,
      docs: []
    };
  };

  const createProblem = async (): Promise<void> => {
    try {
      setLoading(true);
      setError(null);
      addDebugInfo('Problem creation started');
      
      try {
        // Try to create via API
        const response = await fetch('/api/problems/create/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({})
        });

        if (!response.ok) {
          throw new Error(`HTTP Error with Status Code: ${response.status}`);
        }

        const data = await response.json() as ProblemCreateResponse;
        addDebugInfo(`Problem created with response: ${JSON.stringify(data)}`);
        
        // Refresh the problem list
        await fetchProblems();
        
        // Select the newly created problem if available
        if (data.problem_number) {
          void fetchProblemDetails(data.problem_number);
        }
      } catch (apiErr) {
        // Fallback to local creation
        const errorMsg = apiErr instanceof Error ? apiErr.message : String(apiErr);
        addDebugInfo(`API error: ${errorMsg}, falling back to local creation`);
        
        // Get current problems from localStorage
        let currentProblems: number[] = [];
        try {
          // Get all localStorage keys and filter for problem keys
          const allKeys = Object.keys(localStorage);
          const problemKeys = allKeys.filter(key => key.startsWith('problem_'));
          
          // Extract problem numbers
          currentProblems = problemKeys.map(key => {
            return parseInt(key.replace('problem_', ''));
          }).sort((a, b) => a - b);
        } catch (localErr) {
          addDebugInfo(`LocalStorage error: ${String(localErr)}`);
        }
        
        // Create a new problem with next number
        const nextProblemNum = currentProblems.length > 0 ? Math.max(...currentProblems) + 1 : 1;
        
        // Create default problem content with custom templates
        const defaultProblem = createDefaultProblem(nextProblemNum);
        
        // Save to localStorage
        localStorage.setItem(`problem_${nextProblemNum}`, JSON.stringify(defaultProblem));
        
        addDebugInfo(`Created problem ${nextProblemNum} locally`);
        
        // Refresh problem list and select the new problem
        setSelectedProblem(defaultProblem);
        void fetchProblems();
      }
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : String(err);
      addDebugInfo(`Error in createProblem: ${errorMsg}`);
      setError('Failed to create problem. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteProblem = async (problemNum: number): Promise<void> => {
    try {
      setLoading(true);
      setError(null);
      addDebugInfo(`Deleting problem ${problemNum}`);
  
      try {
        // Try to delete via API
        const response = await fetch(`/api/problems/${problemNum}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
          },
        });
  
        if (!response.ok) {
          throw new Error(`HTTP Error with Status Code: ${response.status}`);
        }
  
        addDebugInfo(`Problem ${problemNum} deleted successfully from the server`);
      } catch (apiErr) {
        // API call failed, fallback to localStorage deletion
        const errorMsg = apiErr instanceof Error ? apiErr.message : String(apiErr);
        addDebugInfo(`API error deleting problem: ${errorMsg}, falling back to localStorage`);
  
        // Remove problem from localStorage
        localStorage.removeItem(`problem_${problemNum}`);
      }
  
      // Remove from state
      setProblems((prevProblems) => prevProblems.filter((num) => num !== problemNum));
      
      // If the deleted problem was selected, clear selection
      if (selectedProblem?.num === problemNum) {
        setSelectedProblem(null);
      }
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : String(err);
      addDebugInfo(`Error in handleDeleteProblem: ${errorMsg}`);
      setError(`Failed to delete problem ${problemNum}. Please try again.`);
    } finally {
      setLoading(false);
    }
  };
  
  const handleUpdateFile = async (problemNum: number, filename: string, content: string): Promise<void> => {
    if (!selectedProblem) return;
    
    try {
      setLoading(true);
      setError(null);
      addDebugInfo(`Updating file ${filename} for problem ${problemNum}`);
      
      // First update local state to make UI responsive
      const updatedProblem = {
        ...selectedProblem,
        [filename === 'prompt.md' ? 'prompt' : 
         filename === 'starter.py' ? 'starter_code' :
         filename === 'test_cases.py' ? 'test_cases' :
         filename === 'demo_cases.py' ? 'demo_cases' : '']: content
      };
      
      setSelectedProblem(updatedProblem);
      
      // Save to localStorage as backup
      localStorage.setItem(`problem_${problemNum}`, JSON.stringify(updatedProblem));
      
      try {
        // Only use PUT for API updates
        const response = await fetch(`/api/problems/${problemNum}/files/${filename}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ content: content })
        });
        
        if (!response.ok) {
          throw new Error(`HTTP Error with Status Code: ${response.status}`);
        }

        addDebugInfo(`Updated file ${filename} successfully on server using PUT`);
      } catch (apiErr) {
        // Log API error but don't show to user since we already updated locally
        const errorMsg = apiErr instanceof Error ? apiErr.message : String(apiErr);
        addDebugInfo(`API error saving ${filename}: ${errorMsg}, but saved locally`);
      }
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : String(err);
      addDebugInfo(`Error in handleUpdateFile: ${errorMsg}`);
      setError(`Failed to update ${filename}. Changes saved locally but not on server.`);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateProblemClick = (): void => {
    addDebugInfo('Create button clicked');
    void createProblem();
  };

  const handleProblemClick = (num: number): void => {
    addDebugInfo(`Clicked on problem ${num}`);
    void fetchProblemDetails(num);
  };

  const handleSaveFile = (
    problemNum: number, 
    filename: string, 
    content: string
  ): void => {
    addDebugInfo(`Save requested for ${filename}`);
    void handleUpdateFile(problemNum, filename, content);
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Problem Manager</h1>
      
      {/* Error message display */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}
      
      {/* Create Problem Button */}
      <div className="mb-6">
        <button
          onClick={handleCreateProblemClick}
          disabled={loading}
          className="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Creating...' : 'Create New Problem'}
        </button>
        
        {/* Reset loading state button for development */}
        <button
          onClick={() => setLoading(false)}
          className="ml-4 bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded"
        >
          Reset Loading State
        </button>
      </div>
      
      {/* Debug Info Panel */}
      <div className="mb-6 p-4 bg-gray-100 rounded overflow-auto max-h-40">
        <h3 className="font-bold mb-2">Debug Info:</h3>
        <button 
          onClick={() => setDebugInfo([])}
          className="mb-2 px-2 py-1 bg-gray-500 text-white text-xs rounded"
        >
          Clear Log
        </button>
        <div className="text-xs font-mono">
          {debugInfo.length === 0 ? (
            <p>No debug info yet</p>
          ) : (
            debugInfo.map((info, idx) => (
              <div key={idx} className="mb-1">{info}</div>
            ))
          )}
        </div>
      </div>
      
      {/* Problem List */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="md:col-span-1 border p-4 rounded">
          <h2 className="text-xl font-semibold mb-3">Problems</h2>
          {loading && problems.length === 0 ? (
            <p>Loading problems...</p>
          ) : (
            <ul className="space-y-2">
              {problems.length === 0 ? (
                <p>No problems found. Create one to get started.</p>
              ) : (
                problems.map((num) => (
                  <li key={num}>
                    <button
                      onClick={() => handleProblemClick(num)}
                      className={`text-blue-500 hover:text-blue-700 ${
                        selectedProblem?.num === num ? 'font-bold' : ''
                      }`}
                    >
                      Problem {num}
                    </button>
                  </li>
                ))
              )}
            </ul>
          )}
        </div>
        
        {/* Problem Details */}
        <div className="md:col-span-2 border p-4 rounded">
          <h2 className="text-xl font-semibold mb-3">Problem Details</h2>
          {loading && !selectedProblem ? (
            <p>Loading problem details...</p>
          ) : selectedProblem ? (
            <div>
              <h3 className="text-lg font-medium mb-2">Problem {selectedProblem.num}</h3>

              {/* Delete */}
              <button onClick={() => 
                { void handleDeleteProblem(selectedProblem.num); }
              } 
                disabled={loading} className="mt-2 bg-red-500 hover:bg-red-600 text-white py-1 px-3 rounded disabled:opacity-50 disabled:cursor-not-allowed"> 
                {loading ? 'Deleting...' : 'Delete Problem'}
              </button>

              {/* Prompt */}
              <div className="mb-4">
                <h4 className="font-medium mb-1">Prompt</h4>
                <textarea
                  value={selectedProblem.prompt}
                  onChange={(e) => 
                    setSelectedProblem({...selectedProblem, prompt: e.target.value})
                  }
                  className="w-full p-2 border rounded"
                  rows={5}
                ></textarea>
                <button
                  onClick={() => 
                    handleSaveFile(selectedProblem.num, 'prompt.md', selectedProblem.prompt)
                  }
                  disabled={loading}
                  className="mt-2 bg-blue-500 hover:bg-blue-600 text-white py-1 px-3 rounded disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? 'Saving...' : 'Save Prompt'}
                </button>
              </div>
              
              {/* Starter Code */}
              <div className="mb-4">
                <h4 className="font-medium mb-1">Starter Code</h4>
                <textarea
                  value={selectedProblem.starter_code}
                  onChange={(e) => 
                    setSelectedProblem({...selectedProblem, starter_code: e.target.value})
                  }
                  className="w-full p-2 border rounded font-mono"
                  rows={5}
                ></textarea>
                <button
                  onClick={() => 
                    handleSaveFile(selectedProblem.num, 'starter.py', selectedProblem.starter_code)
                  }
                  disabled={loading}
                  className="mt-2 bg-blue-500 hover:bg-blue-600 text-white py-1 px-3 rounded disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? 'Saving...' : 'Save Starter Code'}
                </button>
              </div>
              
              {/* Test Cases */}
              <div className="mb-4">
                <h4 className="font-medium mb-1">Test Cases</h4>
                <textarea
                  value={selectedProblem.test_cases}
                  onChange={(e) => 
                    setSelectedProblem({...selectedProblem, test_cases: e.target.value})
                  }
                  className="w-full p-2 border rounded font-mono"
                  rows={5}
                ></textarea>
                <button
                  onClick={() => 
                    handleSaveFile(selectedProblem.num, 'test_cases.py', selectedProblem.test_cases)
                  }
                  disabled={loading}
                  className="mt-2 bg-blue-500 hover:bg-blue-600 text-white py-1 px-3 rounded disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? 'Saving...' : 'Save Test Cases'}
                </button>
              </div>
              
              {/* Demo Cases */}
              <div className="mb-4">
                <h4 className="font-medium mb-1">Demo Cases</h4>
                <textarea
                  value={selectedProblem.demo_cases}
                  onChange={(e) => 
                    setSelectedProblem({...selectedProblem, demo_cases: e.target.value})
                  }
                  className="w-full p-2 border rounded font-mono"
                  rows={5}
                ></textarea>
                <button
                  onClick={() => 
                    handleSaveFile(selectedProblem.num, 'demo_cases.py', selectedProblem.demo_cases)
                  }
                  disabled={loading}
                  className="mt-2 bg-blue-500 hover:bg-blue-600 text-white py-1 px-3 rounded disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? 'Saving...' : 'Save Demo Cases'}
                </button>
              </div>
            </div>
          ) : (
            <p>Select a problem to view details</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Test;