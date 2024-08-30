import React from 'react';
import './App.css'; // Ensure this file contains Tailwind CSS directives
import SearchComponent from './SearchComponent'; // Import the SearchComponent

function App() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <header className="w-full max-w-4xl mx-auto p-6 bg-white shadow-lg rounded-lg">
        <h1 className="text-3xl font-bold text-gray-800 mb-4">Search and Analyze Reddit Posts</h1>
        <SearchComponent />  {/* Include the SearchComponent */}
      </header>
    </div>
  );
}

export default App;
