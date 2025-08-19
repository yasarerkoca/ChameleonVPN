import React, { useEffect, useState } from 'react';
import { fetchServers } from '../api';

export default function Servers() {
  const [servers, setServers] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchServers()
      .then(setServers)
      .catch((e) => setError(e.message));
  }, []);

  return (
    <div>
      <h1>Servers</h1>
      {error && <p>Error: {error}</p>}
      <ul>
        {servers.map((s) => (
          <li key={s.id}>{s.title}</li>
        ))}
      </ul>
    </div>
  );
}
