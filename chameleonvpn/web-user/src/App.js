import React, { useState } from "react";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Servers from "./pages/Servers";
import Account from "./pages/Account";
import Login from "./pages/Login";
import Register from "./pages/Register";
import ForgotPassword from "./pages/ForgotPassword";
import Help from "./pages/Help";
import Snackbar from "./components/Snackbar";
import ProfileModal from "./components/ProfileModal";
import "./styles.css";

export default function App() {
  const [page, setPage] = useState("home");
  const [loggedIn, setLoggedIn] = useState(true);
  const [snackbar, setSnackbar] = useState("");
  const [showProfile, setShowProfile] = useState(false);
  const [theme, setTheme] = useState("light");
  const user = { email: "user@demo.com", package: "Pro" };

  if (!loggedIn) return <Login onLogin={() => setLoggedIn(true)} />;
  return (
    <div className={theme === "dark" ? "theme-dark" : ""}>
      <Navbar page={page} setPage={setPage} setTheme={setTheme} theme={theme} />
      <div className="content">
        {page === "home" && <Home />}
        {page === "servers" && <Servers />}
        {page === "account" && <Account user={user} onEdit={() => setShowProfile(true)} />}
        {page === "register" && <Register onRegister={() => setSnackbar("Kayıt başarılı!")} />}
        {page === "forgot" && <ForgotPassword onReset={() => setSnackbar("Mail gönderildi!")} />}
        {page === "help" && <Help />}
      </div>
      <Snackbar msg={snackbar} onClose={() => setSnackbar("")} />
      {showProfile && <ProfileModal user={user} onSave={() => setShowProfile(false)} onClose={() => setShowProfile(false)} />}
    </div>
  );
}
