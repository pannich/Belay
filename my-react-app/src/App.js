import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ProtectedRoute } from './Components/ProtectedRoute';

import SignIn  from './Components/SignIn';
import SignUp  from './Components/SignUp';
import Profile  from './Components/Profile';
import ChannelsList from './Components/Channel';
import Welcome from './Components/Welcome';
import Menubar from './Components/Menubar';

// react router : https://reactrouter.com/en/main/routers/picking-a-router
// https://www.w3schools.com/react/react_router.asp

function App() {
  return (
    <BrowserRouter>
       <Menubar /> {/* This places the menu bar at the top */}
        <Routes>
            <Route path="/" element={<Welcome />} />
            <Route path="/login" element={<SignIn />} />
            <Route path="/signup" element={<SignUp />} />
            {/* Protected */}
            <Route path="/channel/:channelId" element={
              <ProtectedRoute><ChannelsList /></ProtectedRoute>} />
            <Route path="/channel" element={
              <ProtectedRoute><ChannelsList /></ProtectedRoute>
            } />
            <Route path="/profile" element={
              <ProtectedRoute><Profile /></ProtectedRoute>
            } />
        </Routes>
    </BrowserRouter>
  )
}

export default App;
