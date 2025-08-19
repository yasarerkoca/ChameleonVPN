import React, { useEffect, useState } from 'react';
import { fetchSubscriptions } from '../api';

export default function Subscriptions() {
  const [subs, setSubs] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchSubscriptions()
      .then(setSubs)
      .catch((e) => setError(e.message));
  }, []);

  return (
    <div>
      <h1>Subscriptions</h1>
      {error && <p>Error: {error}</p>}
      <ul>
        {subs.map((s) => (
          <li key={s.id}>{s.title}</li>
        ))}
      </ul>
    </div>
  );
}
