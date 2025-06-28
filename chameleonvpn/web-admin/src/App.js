import React, { useState } from "react";
import { BrowserRouter as Router, Route, Switch, Redirect } from "react-router-dom";
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
        <Login onLogin={token => { localStorage.setItem("token", token); setLoggedIn(true); }} />
      ) : (
        <div className="main-layout">
          <Sidebar />
          <div className="content">
            <Topbar />
            <Switch>
              <Route path="/dashboard" component={Dashboard} />
              <Route path="/users" component={Users} />
              <Route path="/servers" component={Servers} />
              <Route path="/settings" component={Settings} />
              <Redirect to="/dashboard" />
            </Switch>
          </div>
        </div>
      )}
    </Router>
  );
}