import React from "react";
export default function Sidebar({ page, setPage }) {
  return (
    <div className="sidebar">
      <div className="logo">ChameleonVPN</div>
      <nav>
        <button className={page==="dashboard"?"active":""} onClick={() => setPage("dashboard")}>Dashboard</button>
        <button className={page==="users"?"active":""} onClick={() => setPage("users")}>Kullanıcılar</button>
        <button className={page==="servers"?"active":""} onClick={() => setPage("servers")}>Sunucular</button>
        <button className={page==="settings"?"active":""} onClick={() => setPage("settings")}>Ayarlar</button>
      </nav>
    </div>
  );
}
