import React from "react";
export default function Navbar({ page, setPage, theme, setTheme }) {
  return (
    <nav className="navbar">
      <button className={page==="home"?"active":""} onClick={() => setPage("home")}>Ana Sayfa</button>
      <button className={page==="servers"?"active":""} onClick={() => setPage("servers")}>Sunucular</button>
      <button className={page==="account"?"active":""} onClick={() => setPage("account")}>Hesabım</button>
      <button onClick={() => setPage("help")}>Yardım</button>
      <button onClick={() => setTheme(theme==="dark"?"light":"dark")}>
        {theme==="dark" ? "Açık Tema" : "Koyu Tema"}
      </button>
    </nav>
  );
}
