import React, { useEffect, useState } from 'react';
import { fetchLogs } from '../api';

export default function Logs() {
  const [logs, setLogs] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchLogs()
      .then(setLogs)
      .catch((e) => setError(e.message));
  }, []);

  return (
    <div>
      <h1>Logs</h1>
      {error && <p>Error: {error}</p>}
      <ul>
        {logs.map((l) => (
          <li key={l.id}>{l.body || l.title}</li>
        ))}
      </ul>
    </div>
  );
}
