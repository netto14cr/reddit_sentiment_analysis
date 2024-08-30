import React, { useState } from 'react';

const PAGE_SIZE_OPTIONS = [5 ,10, 50, 100, 500, 1000];
const NGROK_URL = process.env.REACT_APP_NGROK_URL;

function SearchComponent() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [resultsPerPage, setResultsPerPage] = useState(PAGE_SIZE_OPTIONS[0]);

  const handleSearch = async () => {
    try {
      const response = await fetch(`${NGROK_URL}/api/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'ngrok-skip-browser-warning': 'true'
        },
        body: JSON.stringify({ query })
      });

      if (!response.ok) {
        throw new Error('Error in request');
      }

      const data = await response.json();
      setResults(data);
      setError(null);
      setCurrentPage(1); // Reset to first page on new search
    } catch (error) {
      console.error('Error:', error);
      setError('Error making request. Please try again later.');
    }
  };

  const handleClearResults = () => {
    setResults([]);
    setQuery('');
    setError(null);
    setCurrentPage(1);
  };

  const handleResetSearch = () => {
    setResults([]);
    setCurrentPage(1);
  };

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  const handleResultsPerPageChange = (event) => {
    setResultsPerPage(Number(event.target.value));
    setCurrentPage(1); // Reset to first page on results per page change
  };

  const indexOfLastResult = currentPage * resultsPerPage;
  const indexOfFirstResult = indexOfLastResult - resultsPerPage;
  const currentResults = results.slice(indexOfFirstResult, indexOfLastResult);

  const totalPages = Math.ceil(results.length / resultsPerPage);

  return (
    <div className="w-full max-w-4xl mx-auto p-4 bg-white rounded-lg shadow-md">
      <input 
        type="text" 
        value={query} 
        onChange={(e) => setQuery(e.target.value)} 
        placeholder="Enter a hashtag or search term" 
        className="w-full p-2 border border-gray-300 rounded-md mb-4"
      />
      <button 
        onClick={handleSearch} 
        className="w-full bg-blue-500 text-white p-2 rounded-md hover:bg-blue-600 mb-4"
      >
        Search
      </button>

      {results.length > 0 && (
        <div className="flex gap-4 mb-4">
          <button 
            onClick={handleResetSearch} 
            className="w-full bg-yellow-500 text-white p-2 rounded-md hover:bg-yellow-600"
          >
            Reset
          </button>
          <button 
            onClick={handleClearResults} 
            className="w-full bg-red-500 text-white p-2 rounded-md hover:bg-red-600"
          >
            Clear Results
          </button>
        </div>
      )}

      {error && <div className="mt-4 text-red-500">{error}</div>}

      <div className="mt-4">
        {results.length > 0 && (
          <div>
            <div className="flex justify-between mb-4">
              <div>
                <label htmlFor="resultsPerPage" className="mr-2">Results per page:</label>
                <select 
                  id="resultsPerPage" 
                  value={resultsPerPage} 
                  onChange={handleResultsPerPageChange} 
                  className="p-2 border border-gray-300 rounded-md"
                >
                  {PAGE_SIZE_OPTIONS.map(size => (
                    <option key={size} value={size}>{size}</option>
                  ))}
                </select>
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="min-w-full bg-white border border-gray-300">
                <thead>
                  <tr className="bg-gray-200">
                    <th className="p-3 border-b text-left">Title</th>
                    <th className="p-3 border-b text-left">Sentiment</th>
                    <th className="p-3 border-b text-left">Explanation</th>
                    <th className="p-3 border-b text-left">Link</th>
                  </tr>
                </thead>
                <tbody>
                  {currentResults.map((result, index) => (
                    <tr key={index} className="hover:bg-gray-100">
                      <td className="p-3 border-b">{result.title}</td>
                      <td className="p-3 border-b">{result.sentiment}</td>
                      <td className="p-3 border-b">{result.sentiment_explanation}</td>
                      <td className="p-3 border-b">
                        <a href={result.url} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">View on Reddit</a>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {totalPages > 1 && (
              <div className="flex justify-between items-center mt-4">
                <button 
                  onClick={() => handlePageChange(currentPage - 1)} 
                  disabled={currentPage === 1} 
                  className="bg-gray-300 text-gray-700 p-2 rounded-md hover:bg-gray-400"
                >
                  Previous
                </button>
                <span>Page {currentPage} of {totalPages}</span>
                <button 
                  onClick={() => handlePageChange(currentPage + 1)} 
                  disabled={currentPage === totalPages} 
                  className="bg-gray-300 text-gray-700 p-2 rounded-md hover:bg-gray-400"
                >
                  Next
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default SearchComponent;
