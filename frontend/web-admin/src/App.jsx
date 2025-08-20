import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Sidebar from './components/Sidebar';
import Login from './pages/Login';
import Register from './pages/Register';
import Verify2FA from './pages/Verify2FA';
import Dashboard from './pages/Dashboard';
import Users from './pages/Users';
import Subscriptions from './pages/Subscriptions';
import Servers from './pages/Servers';
import Logs from './pages/Logs';

function AppContent() {
  const { token } = useAuth();

  return (
    <BrowserRouter>
      {!token ? (
        <Routes>
          <Route path="/register" element={<Register />} />
          <Route path="/verify-2fa" element={<Verify2FA />} />
          <Route path="*" element={<Login />} />
        </Routes>
      ) : (
        <div className="app">
          <Sidebar />
          <main>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/users" element={<Users />} />
              <Route path="/subscriptions" element={<Subscriptions />} />
              <Route path="/servers" element={<Servers />} />
              <Route path="/logs" element={<Logs />} />
            </Routes>
          </main>
        </div>
      )}
    </BrowserRouter>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}
