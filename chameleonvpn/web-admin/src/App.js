import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Topbar from "./components/Topbar";
import Dashboard from "./pages/Dashboard";
import Users from "./pages/Users";
import Servers from "./pages/Servers";
import Settings from "./pages/Settings";
import Login from "./pages/Login";
import "./styles.css";

export default function App() {
  const [loggedIn, setLoggedIn] = useState(!!localStorage.getItem("token"));
  return (
    <Router>
      {!loggedIn ? (
        <Login
          onLogin={token => {
            localStorage.setItem("token", token);
            setLoggedIn(true);
          }}
        />
      ) : (
        <div className="main-layout">
          <Sidebar />
          <div className="content">
            <Topbar />
            <Routes>
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/users" element={<Users />} />
              <Route path="/servers" element={<Servers />} />
              <Route path="/settings" element={<Settings />} />
              {/* Tüm diğer path’ler için dashboard’a yönlendir */}
              <Route path="*" element={<Navigate to="/dashboard" replace />} />
            </Routes>
          </div>
        </div>
      )}
    </Router>
  );
}
