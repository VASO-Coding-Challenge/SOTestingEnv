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
      
      // Simulate API call with mock data for now
      await new Promise(resolve => setTimeout(resolve, 500));
      const mockData = [1, 2, 3];
      setProblems(mockData);
      addDebugInfo('Fetched problems successfully');
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : String(err);
      addDebugInfo(`Error fetching problems: ${errorMsg}`);
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
      
      // Simulate API call with mock data
      await new Promise(resolve => setTimeout(resolve, 500));
      const mockProblem: Problem = {
        num: problemNum,
        prompt: `Example prompt for problem ${problemNum}`,
        starter_code: `def solution_${problemNum}():\n    # Your code here\n    pass`,
        test_cases: `# Test cases for problem ${problemNum}`,
        demo_cases: `# Demo cases for problem ${problemNum}`,
        docs: []
      };
      
      setSelectedProblem(mockProblem);
      addDebugInfo(`Fetched details for problem ${problemNum} successfully`);
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : String(err);
      addDebugInfo(`Error fetching details for problem ${problemNum}: ${errorMsg}`);
      setError(`Failed to load problem ${problemNum}. Please try again.`);
    } finally {
      setLoading(false);
    }
  };

  const createProblem = async (): Promise<void> => {
    try {
      setLoading(true);
      setError(null);
      addDebugInfo('Problem creation started');
      
      // Try the actual API call first
      try {
        addDebugInfo('Attempting to call actual API endpoint');
        const response = await fetch('/api/problems/create/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP Error with Status Code: ${response.status}`);
        }

        const data = await response.json() as ProblemCreateResponse;
        addDebugInfo(`Problem created with response: ${JSON.stringify(data)}`);
        await fetchProblems(); // Refresh the problem list
        return;
      } catch (apiErr) {
        // If the actual API fails, fallback to mock implementation
        const errorMsg = apiErr instanceof Error ? apiErr.message : String(apiErr);
        addDebugInfo(`API call failed: ${errorMsg}. Falling back to mock data.`);
      }
      
      // Mock implementation as fallback
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // Create a new problem with next number
      const nextProblemNum = problems.length > 0 ? Math.max(...problems) + 1 : 1;
      setProblems(prevProblems => [...prevProblems, nextProblemNum]);
      
      addDebugInfo(`Created mock problem with number ${nextProblemNum}`);
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : String(err);
      addDebugInfo(`Error in createProblem: ${errorMsg}`);
      setError('Failed to create problem. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateFile = async (problemNum: number, filename: string, content: string): Promise<void> => {
    try {
      setLoading(true);
      setError(null);
      addDebugInfo(`Updating file ${filename} for problem ${problemNum}`);
      
      // Simulate API call with timeout
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // Just update the local state for now
      if (selectedProblem && selectedProblem.num === problemNum) {
        setSelectedProblem({
          ...selectedProblem,
          [filename === 'prompt.md' ? 'prompt' : 
           filename === 'starter.py' ? 'starter_code' :
           filename === 'test_cases.py' ? 'test_cases' :
           filename === 'demo_cases.py' ? 'demo_cases' : '']: content
        });
      }
      addDebugInfo(`Updated file ${filename} successfully`);
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : String(err);
      addDebugInfo(`Error updating ${filename}: ${errorMsg}`);
      setError(`Failed to update ${filename}. Please try again.`);
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
          className="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded"
        >
          {loading ? 'Creating...' : 'Create New Problem'}
        </button>
        
        {/* Force reset button */}
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
                      className="text-blue-500 hover:text-blue-700"
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
                  className="mt-2 bg-blue-500 hover:bg-blue-600 text-white py-1 px-3 rounded"
                >
                  Save Prompt
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
                  className="mt-2 bg-blue-500 hover:bg-blue-600 text-white py-1 px-3 rounded"
                >
                  Save Starter Code
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
                  className="mt-2 bg-blue-500 hover:bg-blue-600 text-white py-1 px-3 rounded"
                >
                  Save Test Cases
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
                  className="mt-2 bg-blue-500 hover:bg-blue-600 text-white py-1 px-3 rounded"
                >
                  Save Demo Cases
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