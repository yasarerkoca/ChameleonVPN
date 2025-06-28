import React, { useState } from "react";
import ServerCard from "../components/ServerCard";
export default function Servers() {
  const [filter, setFilter] = useState("");
  const servers = [
    { name: "Almanya", ip: "1.2.3.4", status: "online" },
    { name: "ABD", ip: "5.6.7.8", status: "offline" }
  ];
  return (
    <div>
      <h2>Sunucu Seçimi</h2>
      <input placeholder="Sunucu ara..." value={filter} onChange={e=>setFilter(e.target.value)} />
      <div className="server-list">
        {servers.filter(srv => srv.name.toLowerCase().includes(filter.toLowerCase()))
          .map((srv, i) => <ServerCard key={i} {...srv} />)}
      </div>
    </div>
  );
}
