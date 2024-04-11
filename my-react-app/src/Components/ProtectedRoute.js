import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';

export const ProtectedRoute = ({ children }) => {
  const USERTOKEN = localStorage.getItem('nichada_belay_auth_key');
  const location = useLocation();

  if (!USERTOKEN) {
    // Redirect to the login page, but remember the location the user was trying to go to
    // Ref ProtectRoute & location : https://dev.to/collins87mbathi/reactjs-protected-route-m3j
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // If authenticated, render the child components
  return children;
};
