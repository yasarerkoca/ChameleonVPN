import React, { useEffect, useState } from 'react';
import { fetchUsers } from '../api';

export default function Users() {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchUsers()
      .then(setUsers)
      .catch((e) => setError(e.message));
  }, []);

  return (
    <div>
      <h1>Users</h1>
      {error && <p>Error: {error}</p>}
      <ul>
        {users.map((u) => (
          <li key={u.id}>{u.name}</li>
        ))}
      </ul>
    </div>
  );
}
