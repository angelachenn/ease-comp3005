import React, { useState } from 'react';
import './App.css'
const App = () => {
  const [relation, setRelation] = useState('');
  const [query, setQuery] = useState('');
  const [result, setResult] = useState('');

  const executeQuery = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/execute_query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          relation: relation,
          query: query,
        }),
      });

      // Check if the response is successful (status code 200)
      if (response.ok) {
        const result = await response.json();
        setResult(result)
      } else {
        console.error('Error:', response.statusText);
      }
    } catch (error) {
      console.error('Error during the request:', error);
    }
  };
  const ResultComponent = ({ textWithNewlines }) => {
    return (
      <div style={{ whiteSpace: 'pre-line' }}>
        {textWithNewlines}
      </div>
    );
  };
  return (
    <div className="main-container">
      <h3>Execute relational algebra queries with</h3>
      <h1>Ease</h1>
      <div>
        <label htmlFor="relation">Enter Relation:</label>
        <textarea
          id="relation"
          name="relation"
          rows="4"
          cols="50"
          value={relation}
          onChange={(e) => setRelation(e.target.value)}
        ></textarea>
      </div>
      <div>
        <label htmlFor="query">Enter Query:</label>
        <input
          type="text"
          id="query"
          name="query"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
      </div>
      <button onClick={executeQuery}>Execute Query</button>
      <div>
        <h2>Query Result</h2>
        {/* Display the result here */}
        <ResultComponent textWithNewlines={result} />
      </div>
    </div>
  );
};

export default App;