import React, { useState, useEffect } from 'react';

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

const Test: React.FC = () => {
  const [problems, setProblems] = useState<number[]>([]);
  const [selectedProblem, setSelectedProblem] = useState<Problem | null>(null);
  const [allProblems, setAllProblems] = useState<Problem[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  
  // Form fields for updating a problem
  const [prompt, setPrompt] = useState<string>('');
  const [starterCode, setStarterCode] = useState<string>('');
  const [testCases, setTestCases] = useState<string>('');
  const [demoCases, setDemoCases] = useState<string>('');

  const apiBaseUrl = '/api/problems'; // Adjust this to your API base URL

  // Helper function to handle fetch errors
  const handleFetchResponse = async (response: Response) => {
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(errorText || `Error: ${response.status}`);
    }
    return response.json();
  };

  // Fetch the list of problem numbers
  const fetchProblems = async (): Promise<void> => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${apiBaseUrl}/`);
      const data = await handleFetchResponse(response);
      setProblems(data);
      setSuccess('Problems list fetched successfully');
    } catch (err) {
      setError('Failed to fetch problems list');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Fetch all problem details
  const fetchAllProblems = async (): Promise<void> => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${apiBaseUrl}/all`);
      const data = await handleFetchResponse(response);
      setAllProblems(data);
      setSuccess('All problems fetched successfully');
    } catch (err) {
      setError('Failed to fetch all problems');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Fetch a specific problem's details
  const fetchProblem = async (qNum: number): Promise<void> => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${apiBaseUrl}/${qNum}`);
      const data = await handleFetchResponse(response);
      setSelectedProblem(data);
      
      // Update form fields with the fetched data
      setPrompt(data.prompt);
      setStarterCode(data.starter_code);
      setTestCases(data.test_cases);
      setDemoCases(data.demo_cases);
      
      setSuccess(`Problem ${qNum} fetched successfully`);
    } catch (err) {
      setError(`Failed to fetch problem ${qNum}`);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Create a new problem
  const createProblem = async (): Promise<void> => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${apiBaseUrl}/create/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      const data = await handleFetchResponse(response);
      setSuccess(data.message);
      // Refresh the problem list after creating a new problem
      await fetchProblems();
    } catch (err) {
      setError('Failed to create a new problem');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Update a problem
  const updateProblem = async (qNum: number): Promise<void> => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${apiBaseUrl}/${qNum}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          prompt,
          starter_code: starterCode,
          test_cases: testCases,
          demo_cases: demoCases
        })
      });
      const data = await handleFetchResponse(response);
      setSuccess(data.message);
      // Refresh the selected problem data
      await fetchProblem(qNum);
    } catch (err) {
      setError(`Failed to update problem ${qNum}`);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Delete a problem
  const deleteProblem = async (qNum: number): Promise<void> => {
    if (!window.confirm(`Are you sure you want to delete problem ${qNum}?`)) {
      return;
    }
    
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${apiBaseUrl}/${qNum}`, {
        method: 'DELETE'
      });
      const data = await handleFetchResponse(response);
      setSuccess(data.message);
      // Clear selected problem if it was deleted
      if (selectedProblem?.num === qNum) {
        setSelectedProblem(null);
        setPrompt('');
        setStarterCode('');
        setTestCases('');
        setDemoCases('');
      }
      // Refresh the problem list after deletion
      await fetchProblems();
    } catch (err) {
      setError(`Failed to delete problem ${qNum}`);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Delete all problems
  const deleteAllProblems = async (): Promise<void> => {
    if (!window.confirm('Are you sure you want to delete ALL problems? This cannot be undone!')) {
      return;
    }
    
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${apiBaseUrl}/`, {
        method: 'DELETE'
      });
      const data = await handleFetchResponse(response);
      setSuccess(data.message);
      // Clear selected problem and list
      setSelectedProblem(null);
      setProblems([]);
      setAllProblems([]);
      setPrompt('');
      setStarterCode('');
      setTestCases('');
      setDemoCases('');
    } catch (err) {
      setError('Failed to delete all problems');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Handle button clicks safely
  const handleFetchProblems = () => {
    void fetchProblems();
  };

  const handleFetchAllProblems = () => {
    void fetchAllProblems();
  };

  const handleCreateProblem = () => {
    void createProblem();
  };

  const handleDeleteAllProblems = () => {
    void deleteAllProblems();
  };

  const handleFetchProblem = (qNum: number) => {
    void fetchProblem(qNum);
  };

  const handleDeleteProblem = (qNum: number) => {
    void deleteProblem(qNum);
  };

  const handleUpdateProblem = (qNum: number) => {
    void updateProblem(qNum);
  };

  // Load problems list on component mount
  useEffect(() => {
    void fetchProblems();
  }, []);

  // Clear success message after 3 seconds
  useEffect(() => {
    if (success) {
      const timer = setTimeout(() => {
        setSuccess(null);
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [success]);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">API Testing Dashboard</h1>
      
      {/* Status messages */}
      {loading && <div className="bg-blue-100 p-3 mb-4 rounded">Loading...</div>}
      {error && <div className="bg-red-100 p-3 mb-4 rounded">{error}</div>}
      {success && <div className="bg-green-100 p-3 mb-4 rounded">{success}</div>}
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Left side: Problem list and actions */}
        <div className="bg-gray-50 p-4 rounded shadow">
          <h2 className="text-xl font-bold mb-4">Problems</h2>
          
          <div className="flex space-x-2 mb-4">
            <button 
              onClick={handleFetchProblems} 
              className="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600"
            >
              Refresh List
            </button>
            <button 
              onClick={handleFetchAllProblems} 
              className="bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600"
            >
              Fetch All Details
            </button>
            <button 
              onClick={handleCreateProblem} 
              className="bg-purple-500 text-white px-3 py-1 rounded hover:bg-purple-600"
            >
              Create New
            </button>
            <button 
              onClick={handleDeleteAllProblems} 
              className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
            >
              Delete All
            </button>
          </div>
          
          <div>
            <h3 className="font-semibold mb-2">Problem Numbers:</h3>
            {problems.length > 0 ? (
              <ul className="bg-white p-2 border rounded">
                {problems.map(num => (
                  <li key={num} className="flex justify-between items-center p-2 hover:bg-gray-100">
                    <span>Problem {num}</span>
                    <div>
                      <button 
                        onClick={() => handleFetchProblem(num)} 
                        className="bg-blue-500 text-white px-2 py-1 text-xs rounded mr-2 hover:bg-blue-600"
                      >
                        View
                      </button>
                      <button 
                        onClick={() => handleDeleteProblem(num)} 
                        className="bg-red-500 text-white px-2 py-1 text-xs rounded hover:bg-red-600"
                      >
                        Delete
                      </button>
                    </div>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500">No problems found.</p>
            )}
          </div>
          
          {allProblems.length > 0 && (
            <div className="mt-4">
              <h3 className="font-semibold mb-2">All Problem Details:</h3>
              <div className="bg-white p-2 border rounded max-h-64 overflow-y-auto">
                {allProblems.map(problem => (
                  <details key={problem.num} className="mb-2">
                    <summary className="cursor-pointer font-medium">Problem {problem.num}</summary>
                    <div className="p-2 text-sm">
                      <p><strong>Prompt:</strong> {problem.prompt.substring(0, 100)}...</p>
                      <p><strong>Starter Code:</strong> {problem.starter_code.substring(0, 100)}...</p>
                      <p><strong>Test Cases:</strong> {problem.test_cases.substring(0, 100)}...</p>
                      <p><strong>Demo Cases:</strong> {problem.demo_cases.substring(0, 100)}...</p>
                    </div>
                  </details>
                ))}
              </div>
            </div>
          )}
        </div>
        
        {/* Right side: Selected problem editor */}
        <div className="bg-gray-50 p-4 rounded shadow">
          <h2 className="text-xl font-bold mb-4">
            {selectedProblem ? `Edit Problem ${selectedProblem.num}` : 'Select a Problem to Edit'}
          </h2>
          
          {selectedProblem ? (
            <form onSubmit={(e) => {
              e.preventDefault();
              handleUpdateProblem(selectedProblem.num);
            }}>
              <div className="mb-4">
                <label className="block font-medium mb-1">Prompt:</label>
                <textarea 
                  value={prompt} 
                  onChange={(e) => setPrompt(e.target.value)}
                  className="w-full p-2 border rounded"
                  rows={4}
                />
              </div>
              
              <div className="mb-4">
                <label className="block font-medium mb-1">Starter Code:</label>
                <textarea 
                  value={starterCode} 
                  onChange={(e) => setStarterCode(e.target.value)}
                  className="w-full p-2 border rounded font-mono"
                  rows={6}
                />
              </div>
              
              <div className="mb-4">
                <label className="block font-medium mb-1">Test Cases:</label>
                <textarea 
                  value={testCases} 
                  onChange={(e) => setTestCases(e.target.value)}
                  className="w-full p-2 border rounded font-mono"
                  rows={6}
                />
              </div>
              
              <div className="mb-4">
                <label className="block font-medium mb-1">Demo Cases:</label>
                <textarea 
                  value={demoCases} 
                  onChange={(e) => setDemoCases(e.target.value)}
                  className="w-full p-2 border rounded font-mono"
                  rows={4}
                />
              </div>
              
              <div className="flex justify-end">
                <button 
                  type="submit"
                  className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
                >
                  Update Problem
                </button>
              </div>
            </form>
          ) : (
            <p className="text-gray-500">No problem selected. Click "View" on a problem from the list to edit it.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Test;