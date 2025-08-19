import React from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import Sidebar from './components/Sidebar';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';

function AppContent() {
  const { token } = useAuth();
  if (!token) {
    return <Login />;
  }
  return (
    <div className="app">
      <Sidebar />
      <Dashboard />
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}
