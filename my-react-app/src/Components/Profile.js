import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import "./Profile.css";

var USERTOKEN = '';
var USER_ID = '';
var USER_NAME = '';
var config = {};

function Profile() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [repeatPassword, setRepeatPassword] = useState('');
  const navigate = useNavigate();
  USER_ID = localStorage.getItem('nichada_userId');
  USERTOKEN = localStorage.getItem('nichada_belay_auth_key');
  config = {
    headers: {
      'Content-Type': 'application/json', // Specify the content type
      'Authorization': `${USERTOKEN}` // Authorization header, for example, a Bearer token
    }
  };

  const handleChangeUsername = async (newUsername) => {
    try {
      const response = await axios.post('/api/user/change-username', { newUsername }, config);
      const data = response.data;
      USER_NAME = data.username;
      console.log(data.username);
      localStorage.setItem('nichada_userName', newUsername);

      // Handle successful username change
      alert('Username successfully changed.');
    } catch (error) {
      // Handle error
      console.error('Failed to change username', error);
    }
  };

  const handleChangePassword = async (newPassword) => {
    try {
      const response = await axios.post('/api/user/change-password', { newPassword }, config);
      // Handle successful password change
      alert('Password successfully changed.');
    } catch (error) {
      // Handle error
      console.error('Failed to change password', error);
    }
  };

  const handleSignOut = () => {
    localStorage.removeItem('nichada_belay_auth_key');
    localStorage.removeItem('nichada_userId');
    localStorage.removeItem('nichada_userName');

    alert('SignOut successful');
  };

  const updateUserName = () => {
    handleChangeUsername(username);
  };

  const updatePassword = () => {
    if (password === repeatPassword) {
      handleChangePassword(password);
    } else {
      alert("Passwords don't match");
    }
  };

  return (
    <div className="clip">
      <div className="auth container">
        <h2>Welcome to Belay!</h2>
        <div className="alignedForm">
          <label htmlFor="username">Username: </label>
          <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" />
          <button onClick={()=>{handleChangeUsername(username)}}>update</button>
          <label htmlFor="password">Password: </label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
          <button onClick={updatePassword}>update</button>
          <label htmlFor="repeatPassword">Repeat: </label>
          <input type="password" value={repeatPassword} onChange={(e) => setRepeatPassword(e.target.value)} placeholder="Repeat Password" />
          {/* Error handling for password match can be done here */}
        </div>
        <div>
          <button className="exit logout" onClick={handleSignOut}>Log out</button>
        </div>
      </div>
    </div>
  );
}

export default Profile;
