import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import "./Menubar.css";

export default function Menubar() {
  const [userName, setUserName] = useState('')
  useEffect(() => {
    setUserName(localStorage.getItem('nichada_userName'));
  }, []);

  return (
    <nav className="navbar">
      <div className="userDisplay">{userName}</div>
      <ul>
        <li><Link to="/" className="nav-link">Home</Link></li>
        <li><Link to="/signup" className="nav-link">Sign Up</Link></li>
        <li><Link to="/login" className="nav-link">Login</Link></li>
        <li><Link to="/profile" className="nav-link">Profile</Link></li>
        <li><Link to="/channel" className="nav-link">Channels</Link></li> {/* Example channel ID */}
      </ul>
    </nav>
  );
}
