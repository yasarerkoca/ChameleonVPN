import React, { useEffect, useState } from "react";
import { fetchWithAuth } from "../api";

export default function Users() {
  const [users, setUsers] = useState([]);
  useEffect(() => {
    fetchWithAuth("/admin/users")
      .then(res => res.json())
      .then(setUsers)
      .catch(console.error);
  }, []);
  return (
    <div>
      <h2>Kullanıcılar</h2>
      <ul>
        {users.map(u => (
          <li key={u.id}>{u.email} {u.is_admin && " (Admin)"}</li>
        ))}
      </ul>
    </div>
  );
}