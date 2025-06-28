import React from "react";
export default function ServerCard({ name, ip, status }) {
  return (
    <div className="server-card">
      <b>{name}</b> <br />
      IP: {ip} <br />
      Durum: <span style={{color: status==="online"?"green":"red"}}>{status}</span>
      <button style={{marginTop: 8}}>Bu Sunucuya Bağlan</button>
    </div>
  );
}
