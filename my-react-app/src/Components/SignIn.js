import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, useLocation } from 'react-router-dom';

// ---- UseState vs. Static
// https://legacy.reactjs.org/docs/hooks-state.html#:~:text=Normally%2C%20variables%20%E2%80%9Cdisappear%E2%80%9D%20when,have%20to%20be%20an%20object.
// React UseState : React remember the current state between each re-render.
  // Any change to the variable's state will trigger a re-render of the component, allowing you to react dynamically to changes.
// Static Value : you only need to check the token once when the component loads.
// --------------------------

function SignIn() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const USERTOKEN = localStorage.getItem('nichada_belay_auth_key');
    const navigate = useNavigate();
    const location = useLocation();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            // Ref : Property Value Shorthand EC6
              // { username, password } same as { "username": username, "password": password }
              // https://medium.com/@musturi.rakesh/best-es6-features-in-javascript-69a0b16425ce
            const response = await axios.post('/api/login', { username, password });

            localStorage.setItem('nichada_belay_auth_key', response.data.token);
            localStorage.setItem('nichada_userId', response.data.id);
            localStorage.setItem('nichada_userName', response.data.username);

            alert('Login successful');

            const from = location.state?.from?.pathname || '/';
            navigate(from, { replace: true });

        } catch (error) {
            const errorMessage = error.response ? error.response.data.message : 'An error occurred. Please try again.';
            console.error('Login failed:', errorMessage);
            alert(errorMessage);
        }
    };

    return (
      <div>
        <form onSubmit={handleSubmit}>
          <div>
            <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" required />
          </div>
          <div>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" required />
          </div>
          <div>
            <button type="submit">Sign In</button>
          </div>
          <div> If user currently logged in. They can't signup until they logout. </div>
        </form>
      </div>
    );
}

export default SignIn;
