import React from 'react';
import './styles.css';  // styles.css をインポート

function App() {
  return (
    <div className="app-container">
      <h1>Welcome to NXTSquare Member Portal</h1>
      <p>Test Pages</p>
      
      <div>
        <h2>Quick Links:</h2>
        <ul>
          <li>
            <a href="http://localhost:5002/create_user">Client Create</a>
          </li>
          <li>
            <a href="http://localhost:5002/admin-create">Admin Create</a>
          </li>
          <li>
            <a href="http://localhost:5002/admin-login">Admin Login</a>
          </li>
          <li>
            <a href="http://localhost:5002/client-login">Client Login</a>
          </li>
          <li>
            <a href="http://localhost:5002/test-db">Test DB</a>
          </li>
        </ul>
      </div>
    </div>
  );
}

export default App;
