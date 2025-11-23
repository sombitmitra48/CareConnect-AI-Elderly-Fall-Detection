import React, { useState, useEffect } from 'react';
import './App.css';
import Dashboard from './components/Dashboard';
import Navbar from './components/Navbar';

function App() {
  const [user, setUser] = useState({
    id: 1,
    name: "John Smith",
    role: "elderly"
  });

  return (
    <div className="App">
      <Navbar user={user} />
      <main className="main-content">
        <Dashboard user={user} />
      </main>
    </div>
  );
}

export default App;