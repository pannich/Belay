import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function SignUp() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const USERTOKEN = localStorage.getItem('nichada_belay_auth_key');
    if (USERTOKEN) {
      navigate("/login");
    }
  }, [navigate]); // Add `navigate` as a dependency load only when component has been mounted to avoid recursion

  const handleSubmit = async (e) => {
      console.log(username);
      e.preventDefault();
      try {
          await axios.post('/api/signup', { username, password });
          alert('User created successfully');
      } catch (error) {
          alert(error.response.data.message);
      }
  };

  return (
      <form onSubmit={handleSubmit}>
          <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" required />
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" required />
          <button type="submit">Sign Up</button>
      </form>
  );
}

export default SignUp;
