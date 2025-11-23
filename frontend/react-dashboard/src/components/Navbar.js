import React from 'react';
import './Navbar.css';

const Navbar = ({ user }) => {
  return (
    <nav className="navbar">
      <div className="nav-brand">
        <h1>🌟 CareConnect</h1>
        <p>AI Guardian for the Elderly</p>
      </div>
      <div className="nav-user">
        <span>Welcome, {user.name}</span>
        <div className="user-avatar">
          👤
        </div>
      </div>
    </nav>
  );
};

export default Navbar;